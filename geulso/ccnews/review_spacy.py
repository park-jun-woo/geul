#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras
import requests
import json
from tqdm import tqdm
import argparse
import logging
import time
import re

# --- 설정 ---
DB_CONFIG = {
    'host': 'localhost',
    'database': 'geuldev',
    'user': 'postgres',
    'password': 'test1224!'
}
OLLAMA_API_URL = 'http://localhost:11434/api/generate'
LOG_FILE = 'geulso/ccnews/review_parses.log'

# 로깅 설정
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# --- 추가할 코드 ---

# 프롬프트 로깅을 위한 별도 로거 설정
PROMPT_LOG_FILE = 'geulso/ccnews/review_prompts.log'
prompt_logger = logging.getLogger('prompt_logger')
prompt_logger.setLevel(logging.INFO)

# 핸들러 설정 (기존 로그 파일과 겹치지 않도록)
prompt_handler = logging.FileHandler(PROMPT_LOG_FILE, encoding='utf-8')
prompt_handler.setFormatter(logging.Formatter('%(message)s')) # 프롬프트 내용만 깔끔하게 저장
prompt_logger.addHandler(prompt_handler)

# --- 여기까지 ---

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        logging.error(f"데이터베이스 연결 실패: {e}")
        print(f"✗ 데이터베이스 연결 실패: {e}")
        return None

def read_prompt_template(filepath: str) -> str:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        logging.error(f"프롬프트 파일을 찾을 수 없습니다: {filepath}")
        print(f"✗ 프롬프트 파일을 찾을 수 없습니다: {filepath}")
        return None

def extract_json_from_text(text: str) -> dict:
    """텍스트에서 JSON 객체를 추출하려고 시도합니다."""
    # 먼저 전체 텍스트를 JSON으로 파싱 시도
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # JSON 블록을 찾아서 추출 시도
    json_patterns = [
        r'\{[^{}]*\{[^{}]*\}[^{}]*\}',  # 중첩된 JSON 객체
        r'\{[^}]+\}'  # 단순 JSON 객체
    ]
    
    for pattern in json_patterns:
        matches = re.findall(pattern, text, re.DOTALL)
        for match in matches:
            try:
                data = json.loads(match)
                if 'sentence' in data or 'tokens' in data:
                    return data
            except json.JSONDecodeError:
                continue
    
    return None

def call_ollama_streaming(prompt: str, model: str, max_retries: int = 3) -> dict:
    """Ollama API를 스트리밍 모드로 호출하여 완전한 응답을 조합합니다."""
    
    for attempt in range(max_retries):
        try:
            # 스트리밍 모드로 호출
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": True,  # 스트리밍 활성화
                "options": {
                    "temperature": 0.1,
                    "num_predict": 4096,  # 토큰 수 증가
                    "stop": ["\n\n\n", "###", "---"]  # 응답 종료 시그널
                }
            }
            
            response = requests.post(OLLAMA_API_URL, json=payload, stream=True, timeout=300)
            response.raise_for_status()
            
            # 전체 응답 조합
            full_response = ""
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        if 'response' in chunk:
                            full_response += chunk['response']
                        
                        # 응답이 완료되면 중단
                        if chunk.get('done', False):
                            break
                    except json.JSONDecodeError:
                        continue
            
            # 조합된 응답에서 JSON 추출
            if full_response:
                # JSON 형식 응답 시도
                parsed_json = extract_json_from_text(full_response)
                if parsed_json and 'sentence' in parsed_json and 'tokens' in parsed_json:
                    # correction_log가 없으면 기본값 추가
                    if 'correction_log' not in parsed_json:
                        parsed_json['correction_log'] = {
                            'is_corrected': False,
                            'changes': []
                        }
                    return parsed_json
                
        except requests.exceptions.Timeout:
            logging.error(f"Ollama API 타임아웃 (시도 {attempt+1}/{max_retries})")
        except requests.exceptions.RequestException as e:
            logging.error(f"Ollama API 호출 에러 (시도 {attempt+1}/{max_retries}): {e}")
        except Exception as e:
            logging.error(f"예상치 못한 에러 (시도 {attempt+1}/{max_retries}): {e}")
        
        # 재시도 전 대기
        if attempt < max_retries - 1:
            wait_time = 2 ** attempt
            time.sleep(wait_time)
    
    return None

def call_ollama_simple(prompt: str, model: str) -> dict:
    """단순화된 Ollama API 호출 (format 옵션 없이)"""
    try:
        # format 옵션을 제거하고 호출
        payload = {
            "model": model,
            "prompt": prompt + "\n\nRemember to respond with ONLY a valid JSON object.",
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_predict": 4096
            }
        }
        
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=300)
        response.raise_for_status()
        
        result = response.json()
        if result.get('done', False):
            response_text = result.get('response', '')
            parsed_json = extract_json_from_text(response_text)
            if parsed_json:
                # correction_log가 없으면 기본값 추가
                if 'correction_log' not in parsed_json:
                    parsed_json['correction_log'] = {
                        'is_corrected': False,
                        'changes': []
                    }
                return parsed_json
                
    except Exception as e:
        logging.error(f"단순 API 호출 실패: {e}")
    
    return None

def validate_response(response: dict, original_sentence: str) -> bool:
    """LLM 응답의 유효성을 검증합니다."""
    try:
        # 필수 필드 확인
        if not all(key in response for key in ['sentence', 'tokens']):
            return False
        
        # tokens가 리스트인지 확인
        if not isinstance(response.get('tokens'), list):
            return False
        
        # correction_log가 있으면 검증, 없으면 기본값 생성
        if 'correction_log' in response:
            correction_log = response.get('correction_log', {})
            if not isinstance(correction_log, dict):
                response['correction_log'] = {
                    'is_corrected': False,
                    'changes': []
                }
        else:
            response['correction_log'] = {
                'is_corrected': False,
                'changes': []
            }
        
        return True
        
    except Exception as e:
        logging.error(f"응답 검증 중 에러: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="DB의 spaCy 파싱 결과를 Ollama LLM으로 검수합니다.")
    parser.add_argument("--prompt-file", type=str, default="geulso/ccnews/review_prompt.txt", 
                       help="Ollama에 전달할 프롬프트 템플릿 파일 경로")
    parser.add_argument("--model", type=str, default="gpt-oss:20b", help="사용할 Ollama 모델")
    parser.add_argument("--limit", type=int, default=0, help="처리할 최대 문장 수 (0=전체)")
    parser.add_argument("--batch-size", type=int, default=1, help="커밋 배치 크기")
    parser.add_argument("--streaming", action='store_true', help="스트리밍 모드 사용")
    args = parser.parse_args()

    prompt_template = read_prompt_template(args.prompt_file)
    if not prompt_template:
        return

    read_conn = get_db_connection()
    write_conn = get_db_connection()
    if not read_conn or not write_conn:
        return

    # 아직 검수되지 않은 문장을 선택하는 쿼리
    select_query = """
        SELECT s.id, s.spacy_data
        FROM spacied_sentences s
        LEFT JOIN corrected_sentences c ON s.id = c.sentence_id AND c.model = %s
        WHERE c.id IS NULL
        ORDER BY s.id
    """
    if args.limit > 0:
        select_query += f" LIMIT {args.limit}"

    insert_query = """
        INSERT INTO corrected_sentences (sentence_id, model, is_corrected, correction_log, corrected_tokens)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (sentence_id, model) DO NOTHING;
    """

    print("="*60)
    print(f"'{args.model}' 모델로 구문 분석 검수를 시작합니다.")
    print(f"배치 크기: {args.batch_size}")
    print(f"스트리밍 모드: {'활성화' if args.streaming else '비활성화'}")
    print("="*60)

    success_count = 0
    fail_count = 0
    batch_count = 0

    try:
        with read_conn.cursor('server_side_cursor') as read_cur, write_conn.cursor() as write_cur:
            read_cur.execute(select_query, (args.model,))
            
            pbar = tqdm(desc="문장 검수 중")
            
            for sentence_id, spacy_data in read_cur:
                # spacy_data에서 원본 문장 추출
                original_sentence = spacy_data.get('sentence', '')
                
                # 입력 JSON 준비
                input_json = {
                    'sentence': original_sentence,
                    'tokens': spacy_data.get('tokens', [])
                }
                input_json_str = json.dumps(input_json, ensure_ascii=False, indent=2)
                
                # 프롬프트 생성
                prompt = prompt_template.replace('{{input}}', input_json_str)

                # --- 추가할 코드 (한 줄) ---
                prompt_logger.info(f"--- SENTENCE ID: {sentence_id} ---\n{prompt}\n")
                
                # LLM 호출 (스트리밍 모드 선택)
                if args.streaming:
                    llm_response = call_ollama_streaming(prompt, args.model)
                else:
                    llm_response = call_ollama_simple(prompt, args.model)
                
                if not llm_response:
                    logging.warning(f"문장 ID {sentence_id}에 대한 LLM 응답 실패")
                    fail_count += 1
                    pbar.update(1)
                    pbar.set_postfix({'성공': success_count, '실패': fail_count})
                    continue
                
                # 응답 검증
                if not validate_response(llm_response, original_sentence):
                    logging.warning(f"문장 ID {sentence_id}에 대한 응답 검증 실패")
                    fail_count += 1
                    pbar.update(1)
                    pbar.set_postfix({'성공': success_count, '실패': fail_count})
                    continue
                
                # LLM 응답에서 데이터 추출
                correction_log = llm_response.get('correction_log', {})
                is_corrected = correction_log.get('is_corrected', False)
                corrected_tokens = llm_response.get('tokens', [])
                
                # DB에 결과 저장
                write_cur.execute(insert_query, (
                    sentence_id,
                    args.model,
                    is_corrected,
                    json.dumps(correction_log, ensure_ascii=False),
                    json.dumps(corrected_tokens, ensure_ascii=False)
                ))
                
                success_count += 1
                batch_count += 1
                
                # 배치 커밋
                if batch_count >= args.batch_size:
                    write_conn.commit()
                    batch_count = 0
                    logging.info(f"배치 커밋 완료. 누적 성공: {success_count}, 실패: {fail_count}")
                
                pbar.update(1)
                pbar.set_postfix({'성공': success_count, '실패': fail_count})
            
            # 마지막 배치 커밋
            if batch_count > 0:
                write_conn.commit()
                logging.info(f"최종 커밋 완료. 총 성공: {success_count}, 실패: {fail_count}")

    except KeyboardInterrupt:
        print("\n\n사용자에 의해 중단됨")
        logging.info("사용자에 의해 프로세스 중단")
    except Exception as e:
        logging.error(f"처리 중 심각한 에러 발생: {e}")
        print(f"\n✗ 처리 중 심각한 에러 발생: {e}")
    finally:
        read_conn.close()
        write_conn.close()
        print("\n✓ 데이터베이스 연결 종료")

    print("\n" + "="*60)
    print("검수 작업 완료!")
    print(f"성공: {success_count}, 실패: {fail_count}")
    print(f"로그 파일: {LOG_FILE}")
    print("="*60)

if __name__ == "__main__":
    main()