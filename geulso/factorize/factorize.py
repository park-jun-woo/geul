#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import psycopg2
import asyncio
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import argparse
import re
from google import genai
import copy # deepcopy를 위해 추가

# 기본 설정값
DB_CONFIG = {
    'host': 'localhost',
    'database': 'geuldev',
    'user': 'postgres',
    'password': 'test1224!'
}

PROMPT_TEMPLATE_PATH = 'geulso/factorize/factorize_prompt.json'
SAMPLES_DIR = 'geulso/factorize/samples/'
RESULTS_DIR = 'geulso/factorize/factorized/'
API_KEY_PATH = 'geulso/.key'

def load_api_key(path: str) -> str:
    """API 키를 파일에서 로드합니다."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"✗ API 키 파일을 찾을 수 없습니다: {path}")
        exit(1)
    except Exception as e:
        print(f"✗ API 키 로드 실패: {e}")
        exit(1)

def load_prompt_template(path: str) -> Dict[str, Any]:
    """프롬프트 템플릿 JSON 파일을 로드합니다."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            template = json.load(f)
            print(f"✓ 프롬프트 템플릿 로드 완료: {path}")
            return template
    except FileNotFoundError:
        print(f"✗ 프롬프트 템플릿 파일을 찾을 수 없습니다: {path}")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"✗ 프롬프트 템플릿 파일이 유효한 JSON 형식이 아닙니다: {e}")
        exit(1)

def load_samples(directory: str) -> List[Dict[str, Any]]:
    """샘플 디렉토리에서 모든 JSON 샘플을 로드합니다."""
    samples = []
    sample_path = Path(directory)
    
    if not sample_path.exists():
        print(f"⚠ 샘플 디렉토리가 존재하지 않습니다: {directory}")
        return samples
    
    json_files = list(sample_path.glob('*.json'))
    print(f"샘플 파일 {len(json_files)}개 발견")
    
    for filepath in json_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                sample = json.load(f)
                samples.append(sample)
                print(f"  ✓ {filepath.name}")
        except json.JSONDecodeError:
            print(f"  ✗ 유효하지 않은 JSON: {filepath.name}")
        except Exception as e:
            print(f"  ✗ 로드 실패 {filepath.name}: {e}")
    
    print(f"✓ 총 {len(samples)}개 샘플 로드 완료")
    return samples

def count_tokens(text: str) -> int:
    """텍스트의 대략적인 토큰 수를 계산합니다."""
    return len(text) // 4

def fetch_all_verb_synsets(conn) -> List[str]:
    """워드넷에서 모든 동사 synset_id를 가져옵니다."""
    query = """
        SELECT DISTINCT synset_id 
        FROM wordnet_synsets 
        WHERE pos = 'v' 
        ORDER BY synset_id
    """
    with conn.cursor() as cur:
        cur.execute(query)
        return [row[0] for row in cur.fetchall()]

def fetch_verb_frames_for_synset(conn, synset_id: str) -> List[Tuple[int, str]]:
    """주어진 synset의 모든 verb frame을 가져옵니다."""
    query = """
        SELECT frame_id, frame_text
        FROM wordnet_verb_frames
        WHERE synset_id = %s
        ORDER BY frame_id
    """
    with conn.cursor() as cur:
        cur.execute(query, (synset_id,))
        return cur.fetchall()

def fetch_verb_frame_data(conn, synset_id: str, frame_id: int, frame_text: str) -> Optional[Dict[str, Any]]:
    """특정 verb frame에 대한 입력 데이터를 구성합니다."""
    input_data = {
        'synset_id': synset_id,
        'frame_id': frame_id,
        'verb_frame': frame_text
    }
    
    with conn.cursor() as cur:
        cur.execute("""
            SELECT definition, example 
            FROM wordnet_synsets 
            WHERE synset_id = %s
        """, (synset_id,))
        row = cur.fetchone()
        if not row:
            return None
            
        input_data['definition'] = row[0] if row[0] else ""
        
        input_data['semantic_neighbors'] = {}
        
        cur.execute("""
            SELECT r.to_synset, s.definition
            FROM wordnet_synset_relations r
            JOIN wordnet_synsets s ON r.to_synset = s.synset_id
            WHERE r.from_synset = %s AND r.relation_type = 'hypernym'
            LIMIT 3
        """, (synset_id,))
        input_data['semantic_neighbors']['hypernyms'] = [
            {'synset_id': r[0], 'definition': r[1]} 
            for r in cur.fetchall()
        ]
        
        cur.execute("""
            SELECT DISTINCT s2.synset_id, s2.definition
            FROM wordnet_lemmas l1
            JOIN wordnet_lemma_relations lr ON l1.lemma_id = lr.from_lemma_id
            JOIN wordnet_lemmas l2 ON lr.to_lemma_id = l2.lemma_id
            JOIN wordnet_synsets s2 ON l2.synset_id = s2.synset_id
            WHERE l1.synset_id = %s AND lr.relation_type = 'antonym'
            LIMIT 3
        """, (synset_id,))
        input_data['semantic_neighbors']['antonyms'] = [
            {'synset_id': r[0], 'definition': r[1]} 
            for r in cur.fetchall()
        ]

    return input_data

def extract_json_from_response(response_text: str) -> Dict[str, Any]:
    """Gemini 응답 텍스트에서 JSON 객체를 추출합니다."""
    if not response_text or not response_text.strip():
        raise ValueError("응답 내용이 비어 있습니다.")

    cleaned = response_text.strip()
    
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    patterns = [
        r'```json\s*(.*?)\s*```',
        r'```\s*(.*?)\s*```'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, cleaned, re.DOTALL | re.IGNORECASE)
        if matches:
            for match in matches:
                try:
                    return json.loads(match.strip())
                except json.JSONDecodeError:
                    continue

    brace_count = 0
    start_idx = -1
    end_idx = -1
    
    for i, char in enumerate(cleaned):
        if char == '{':
            if start_idx == -1:
                start_idx = i
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0 and start_idx != -1:
                end_idx = i
                break
    
    if start_idx != -1 and end_idx != -1:
        try:
            json_str = cleaned[start_idx:end_idx+1]
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON 파싱 실패: {str(e)}")
    
    raise ValueError("유효한 JSON 객체를 찾을 수 없습니다.")

def save_result_immediately(result: Dict[str, Any], synset_id: str, frame_id: int, output_dir: Path) -> bool:
    """결과를 즉시 파일로 저장합니다."""
    safe_synset = synset_id.replace('.', '_')
    filename = f"{safe_synset}.f.{frame_id:02d}"
    
    if result.get("success") and "response" in result:
        output_dir.mkdir(parents=True, exist_ok=True)
        final_path = output_dir / f"{filename}.json"
        try:
            with open(final_path, 'w', encoding='utf-8') as f:
                json.dump(result["response"], f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"  ✗ 파일 저장 실패 {filename}: {e}")
            return False
    return False

async def process_verb_frame(client, prompt_template: Dict, synset_id: str, 
                            frame_id: int, frame_text: str, conn,
                            output_dir: Path, retry_count: int = 3) -> Dict[str, Any]:
    """단일 verb frame을 처리하고 즉시 저장합니다."""
    
    start_time = time.time()
    
    frame_data = fetch_verb_frame_data(conn, synset_id, frame_id, frame_text)
    if not frame_data:
        return {
            "synset_id": synset_id,
            "frame_id": frame_id,
            "success": False,
            "error": "DB 데이터 없음",
            "inference_time": 0,
            "token_count": 0
        }
    
    # *** 수정된 부분 시작 ***
    # 템플릿의 복사본을 만들어 현재 작업 데이터를 삽입합니다.
    final_prompt_object = copy.deepcopy(prompt_template)
    final_prompt_object['user_query']['input'] = frame_data
    
    # 완성된 JSON 객체를 문자열로 변환하여 최종 프롬프트로 사용합니다.
    prompt_text = json.dumps(final_prompt_object, ensure_ascii=False, indent=2)
    # *** 수정된 부분 끝 ***

    token_count = count_tokens(prompt_text)

    for attempt in range(retry_count):
        raw_response_text = ""
        try:
            response = await asyncio.to_thread(
                client.models.generate_content,
                model="gemini-2.5-flash",
                contents=prompt_text
            )
            
            if not response or not response.text:
                raise ValueError("빈 응답 받음")
            
            raw_response_text = response.text
            parsed_json = extract_json_from_response(raw_response_text)

            from collections import OrderedDict
            ordered_json = OrderedDict()
            for key, value in parsed_json.items():
                ordered_json[key] = value
                if key == 'frame_id':
                    ordered_json['frame_text'] = frame_text
            parsed_json = ordered_json

            inference_time = time.time() - start_time
            
            result_data = {
                "synset_id": synset_id,
                "frame_id": frame_id,
                "success": True,
                "response": parsed_json,
                "inference_time": inference_time,
                "token_count": token_count
            }
            
            saved = save_result_immediately(result_data, synset_id, frame_id, output_dir)
            result_data["saved"] = saved
            return result_data

        except (ValueError, json.JSONDecodeError) as e:
            error_msg = f"JSON 처리 실패: {str(e)}"
            if attempt < retry_count - 1:
                await asyncio.sleep(2 * (attempt + 1))
                continue
            inference_time = time.time() - start_time
            result_data = {
                "synset_id": synset_id,
                "frame_id": frame_id,
                "success": False,
                "error": error_msg,
                "raw_response": raw_response_text,
                "inference_time": inference_time,
                "token_count": token_count
            }
            save_result_immediately(result_data, synset_id, frame_id, output_dir)
            return result_data
            
        except Exception as e:
            error_msg = f"API 에러: {str(e)}"
            if attempt < retry_count - 1:
                await asyncio.sleep(3 * (attempt + 1))
                continue
            inference_time = time.time() - start_time
            result_data = {
                "synset_id": synset_id,
                "frame_id": frame_id,
                "success": False,
                "error": error_msg,
                "raw_response": raw_response_text if raw_response_text else "",
                "inference_time": inference_time,
                "token_count": token_count
            }
            save_result_immediately(result_data, synset_id, frame_id, output_dir)
            return result_data

async def test_gemini_connection(client) -> bool:
    """Gemini API 연결을 테스트합니다."""
    try:
        test_prompt = "Return only this JSON: {\"test\": \"ok\"}"
        response = await asyncio.to_thread(
            client.models.generate_content,
            model="gemini-2.5-flash",
            contents=test_prompt
        )
        if response and response.text:
            print(f"✓ Gemini API 연결 테스트 성공")
            return True
        else:
            print(f"✗ Gemini API 연결 실패: 빈 응답")
            return False
    except Exception as e:
        print(f"✗ Gemini API 연결 실패: {e}")
        return False

def format_time(seconds: float) -> str:
    """초를 읽기 좋은 형식으로 변환합니다."""
    if seconds < 60:
        return f"{seconds:.1f}초"
    elif seconds < 3600:
        return f"{seconds/60:.1f}분"
    else:
        return f"{seconds/3600:.1f}시간"

async def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(description="WordNet 동사 frame별 의미소 분해 (Gemini)")
    parser.add_argument("--concurrent", type=int, default=1, help="동시 실행 수")
    parser.add_argument("--limit", type=int, default=0, help="처리할 최대 synset 수 (0=전체)")
    parser.add_argument("--skip-existing", action="store_true", help="이미 처리된 파일 건너뛰기")
    args = parser.parse_args()
    
    print("="*60)
    print("GEUL 동사 Frame별 의미소 분해 시작 (Gemini 2.5 Flash)")
    print("="*60)
    
    api_key = load_api_key(API_KEY_PATH)
    client = genai.Client(api_key=api_key)
    
    prompt_template = load_prompt_template(PROMPT_TEMPLATE_PATH)
    
    # *** 수정된 부분 시작 ***
    # 샘플을 한번만 로드하여 템플릿에 영구적으로 삽입합니다.
    samples = load_samples(SAMPLES_DIR)
    prompt_template['samples'] = samples
    # *** 수정된 부분 끝 ***

    print("\nGemini API 연결 테스트 중...")
    if not await test_gemini_connection(client):
        print("Gemini API 연결 실패. API 키를 확인하세요.")
        return
    
    print("\nPostgreSQL 연결 중...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        verb_synsets = fetch_all_verb_synsets(conn)
        print(f"✓ 총 {len(verb_synsets):,}개의 동사 synset 발견")
    except psycopg2.Error as e:
        print(f"✗ 데이터베이스 연결 실패: {e}")
        return
    
    if args.limit > 0:
        verb_synsets = verb_synsets[:args.limit]
        print(f"  처리 대상: {len(verb_synsets):,}개로 제한")
    
    all_frames = []
    output_dir = Path(RESULTS_DIR)
    
    print("\n동사 frame 수집 중...")
    for synset_id in verb_synsets:
        frames = fetch_verb_frames_for_synset(conn, synset_id)
        for frame_id, frame_text in frames:
            if args.skip_existing:
                safe_synset = synset_id.replace('.', '_')
                filename = f"{safe_synset}.f.{frame_id:02d}.json"
                if (output_dir / filename).exists():
                    continue
            all_frames.append((synset_id, frame_id, frame_text))
    
    print(f"✓ 총 {len(all_frames):,}개 frame 처리 대상")
    
    if not all_frames:
        print("처리할 frame이 없습니다.")
        conn.close()
        return
    
    print(f"\n처리 시작 (동시 실행: {args.concurrent}개)")
    print("-"*60)
    
    start_time = time.time()
    semaphore = asyncio.Semaphore(args.concurrent)
    
    success_count = 0
    fail_count = 0
    progress = 0
    total_inference_time = 0
    total_tokens = 0
    
    async def process_with_semaphore(synset_id, frame_id, frame_text):
        nonlocal success_count, fail_count, progress, total_inference_time, total_tokens
        
        async with semaphore:
            result = await process_verb_frame(
                client, prompt_template, synset_id, frame_id, frame_text,
                conn, output_dir
            )
            
            progress += 1
            total_inference_time += result.get('inference_time', 0)
            total_tokens += result.get('token_count', 0)
            
            if result['success']:
                success_count += 1
                status = '✓'
            else:
                fail_count += 1
                error = result.get('error', 'Unknown')
                if len(error) > 30:
                    error = error[:27] + "..."
                status = f"✗ ({error})"
            
            elapsed = time.time() - start_time
            avg_inference = total_inference_time / max(1, progress)
            
            print(f"[{progress:5d}/{len(all_frames):5d}] "
                  f"{synset_id:20s}.f.{frame_id:02d} - {status:35s} | "
                  f"성공: {success_count:4d}, 실패: {fail_count:4d} | "
                  f"추론: {result.get('inference_time', 0):.1f}초 | "
                  f"토큰: {result.get('token_count', 0):5d} | "
                  f"평균: {avg_inference:.1f}초")
            
            return result
    
    tasks = [process_with_semaphore(synset_id, frame_id, frame_text) 
             for synset_id, frame_id, frame_text in all_frames]
    await asyncio.gather(*tasks)
    
    elapsed = time.time() - start_time
    print("\n" + "="*60)
    print("처리 완료!")
    print("="*60)
    print(f"총 소요 시간: {format_time(elapsed)}")
    print(f"처리한 frame: {len(all_frames):,}개")
    print(f"성공: {success_count:,}개 ({success_count/max(1, len(all_frames))*100:.1f}%)")
    print(f"실패: {fail_count:,}개 ({fail_count/max(1, len(all_frames))*100:.1f}%)")
    print(f"평균 추론 시간: {total_inference_time/max(1, len(all_frames)):.2f}초/frame")
    print(f"총 토큰 수: {total_tokens:,}개")
    print(f"평균 토큰 수: {total_tokens/max(1, len(all_frames)):.0f}개/frame")
    print("-"*60)
    print(f"✓ 결과 파일: {output_dir}")
    
    conn.close()

if __name__ == "__main__":
    asyncio.run(main())