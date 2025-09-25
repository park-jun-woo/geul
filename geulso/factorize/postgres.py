#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import json
import time
import argparse
import psycopg2
from psycopg2.extras import execute_values
from tqdm import tqdm
from typing import List, Dict, Any

# PostgreSQL 연결 설정
DB_CONFIG = {
    'host': 'localhost',
    'database': 'geuldev',
    'user': 'postgres',
    'password': 'test1224!'
}

class FactorizedDataToPostgres:
    """
    JSON 형식의 의미 분해 데이터를 PostgreSQL에 삽입하는 클래스.
    """
    def __init__(self, db_config: Dict[str, str]):
        """PostgreSQL 연결 초기화"""
        self.conn = psycopg2.connect(**db_config)
        self.stats = {
            'files_processed': 0,
            'qualifiers': 0,
            'sememes': 0,
            'participants': 0
        }

    def clear_tables(self):
        """기존 데이터 삭제"""
        print("기존 factorized 데이터 삭제 중...")
        tables = [
            'wordnet_factorized_participants',
            'wordnet_factorized_sememes',
            'wordnet_factorized_qualifiers'
        ]
        with self.conn.cursor() as cur:
            for table in tables:
                cur.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE")
        self.conn.commit()
        print("데이터 삭제 완료.")

    def process_directory(self, dir_path: str, batch_size: int):
        """
        지정된 디렉토리의 모든 JSON 파일을 처리하여 DB에 삽입합니다.
        """
        print(f"디렉토리 처리 시작: {dir_path}")
        try:
            filepaths = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('.json')]
        except FileNotFoundError:
            print(f"오류: 디렉토리를 찾을 수 없습니다 -> {dir_path}")
            return
            
        qualifiers_batch = []
        sememes_batch_data = [] # (sememe_tuple, [participant_tuple, ...])
        
        with tqdm(total=len(filepaths), desc="JSON 파일 처리 중") as pbar:
            for path in filepaths:
                try:
                    pbar.write(f"--> Processing: {os.path.basename(path)}")

                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    synset_id = data.get("synset_id")
                    frame_id = data.get("frame_id")

                    if not synset_id or frame_id is None:
                        continue

                    # 1. Qualifiers 데이터 준비
                    for name, props in data.get("qualifiers", {}).items():
                        if props is None:
                            continue # props가 None이면 이 qualifier는 건너뜁니다.
                        qualifier_value = props.get('value')
                        reasoning = props.get('reasoning')

                        has_valid_value = qualifier_value is not None and qualifier_value != {}
                        # reasoning이 존재하고, 공백 문자가 아닌 내용이 있는지 확인
                        has_reasoning = reasoning and reasoning.strip()

                        if has_valid_value or has_reasoning:
                            # 유효한 value가 아닐 경우 DB에 NULL로 입력되도록 None으로 설정
                            db_value = qualifier_value if has_valid_value else None
                            
                            qualifiers_batch.append((
                                synset_id, frame_id, name, db_value, reasoning
                            ))

                    # 2. Sememes와 Participants 데이터 준비
                    sememes_data = data.get("sememes", [])

                    # sememes 데이터가 리스트가 아닌 딕셔너리 형태일 경우 처리
                    if isinstance(sememes_data, dict):
                        # 딕셔너리 구조를 리스트 구조로 변환하는 로직 추가
                        # 이 부분은 데이터의 정확한 의도를 파악하고 변환해야 합니다.
                        # 예시: 딕셔너리를 하나의 sememe 객체로 간주
                        sememe_tuple = (
                            synset_id, frame_id,
                            sememes_data.get("VerbType", {}).get('value'),
                            sememes_data.get("VerbProperty", {}).get('value'),
                            "Converted from dict format" # reasoning은 임의로 지정
                        )
                        # 이 구조에서는 participants를 파싱하기 어려우므로 빈 리스트로 처리
                        participants_list = []
                        sememes_batch_data.append((sememe_tuple, participants_list))

                    # 기존의 리스트 구조 처리
                    elif isinstance(sememes_data, list):
                        for sememe in data.get("sememes", []):
                            sememe_tuple = (
                                synset_id, frame_id,
                                sememe.get('verb_type'), sememe.get('verb_property'), sememe.get('reasoning')
                            )
                            participants_list = []
                            for participant in sememe.get("participants", []):
                                participants_list.append((
                                    participant.get('semantic_role'),
                                    participant.get('value_type'),
                                    participant.get('reasoning')
                                ))
                            sememes_batch_data.append((sememe_tuple, participants_list))

                except (json.JSONDecodeError, KeyError) as e:
                    pbar.write(f"경고: 파일 {os.path.basename(path)} 처리 중 오류: {e}")
                    continue
                finally:
                    pbar.update(1)

                # qualifiers 또는 sememes 데이터 중 하나라도 배치 사이즈에 도달하면 DB에 삽입
                if len(qualifiers_batch) >= batch_size or len(sememes_batch_data) >= batch_size:
                    try:
                        self._insert_data_batch(qualifiers_batch, sememes_batch_data)
                        qualifiers_batch, sememes_batch_data = [], []
                    except psycopg2.Error as e: # Exception을 psycopg2.Error로 더 구체화
                        pbar.write("\n" + "="*80)
                        pbar.write(f"🔥 데이터베이스 삽입 중 치명적 에러 발생!")
                        pbar.write(f"🔥 에러 유형: {type(e).__name__}")
                        pbar.write(f"🔥 에러 메시지: {e}")
                        pbar.write("="*80)
                        raise # 에러를 다시 발생시켜 상위 except 블록이 처리하도록 함

        # 루프 종료 후 남은 데이터 삽입
        if qualifiers_batch or sememes_batch_data:
            try:
                self._insert_data_batch(qualifiers_batch, sememes_batch_data)
            except psycopg2.Error as e:
                # ▼▼▼▼▼ [수정] 상세 에러 로깅 적용 ▼▼▼▼▼
                print("\n" + "="*80)
                print(f"🔥 마지막 배치 삽입 중 치명적 에러 발생!")
                print(f"🔥 에러 유형: {type(e).__name__}")
                print(f"🔥 에러 메시지: {e}")
                print("="*80)
                raise

        self.conn.commit()
        print("모든 파일 처리 및 DB 삽입 완료.")

    def _insert_data_batch(self, qualifiers_batch: List, sememes_batch_data: List):
        """
        준비된 데이터 배치를 유효성 검사 후 DB에 삽입하는 내부 함수.
        데이터 타입 오류를 사전에 검사하여 상세한 에러를 발생시킵니다.
        """
        with self.conn.cursor() as cur:
            try:
                # 1. Qualifiers 처리
                if qualifiers_batch:
                    # DB에 보내기 전 최종 유효성 검사
                    for q_row in qualifiers_batch:
                        # q_row = (synset_id, frame_id, name, value, reasoning)
                        for item in q_row:
                            if isinstance(item, (dict, list)):
                                raise TypeError(
                                    f"Qualifiers 데이터 타입 오류. synset_id='{q_row[0]}', frame_id={q_row[1]}. "
                                    f"문제 필드 '{q_row[2]}', 문제 값: {json.dumps(item, ensure_ascii=False)}"
                                )
                    # Qualifiers 삽입
                    execute_values(cur, """
                        INSERT INTO wordnet_factorized_qualifiers (synset_id, frame_id, qualifier_name, value, reasoning)
                        VALUES %s ON CONFLICT DO NOTHING
                    """, qualifiers_batch)
                    self.stats['qualifiers'] += len(qualifiers_batch)

                # 2. Sememes와 Participants 처리
                if sememes_batch_data:
                    sememes_to_insert = [s_data[0] for s_data in sememes_batch_data]

                    # Sememes 유효성 검사
                    for s_row in sememes_to_insert:
                        # s_row = (synset_id, frame_id, verb_type, verb_property, reasoning)
                        for item in s_row:
                            if isinstance(item, (dict, list)):
                                raise TypeError(
                                    f"Sememes 데이터 타입 오류. synset_id='{s_row[0]}', frame_id={s_row[1]}. "
                                    f"문제 값: {json.dumps(item, ensure_ascii=False)}"
                                )
                    
                    # Sememes 삽입 및 생성된 ID 반환
                    inserted_sememe_ids = execute_values(cur, """
                        INSERT INTO wordnet_factorized_sememes (synset_id, frame_id, verb_type, verb_property, reasoning)
                        VALUES %s RETURNING sememe_id
                    """, sememes_to_insert, fetch=True)
                    self.stats['sememes'] += len(inserted_sememe_ids)

                    # Participants 데이터 준비 및 유효성 검사
                    participants_to_insert = []
                    for i, sememe_id_tuple in enumerate(inserted_sememe_ids):
                        sememe_id = sememe_id_tuple[0]
                        participants_list = sememes_batch_data[i][1]
                        parent_sememe = sememes_to_insert[i] # 에러 로깅용

                        for p_tuple in participants_list:
                            # p_tuple = (semantic_role, value_type, reasoning)
                            for item in p_tuple:
                                if isinstance(item, (dict, list)):
                                    raise TypeError(
                                        f"Participants 데이터 타입 오류. synset_id='{parent_sememe[0]}', frame_id={parent_sememe[1]}. "
                                        f"문제 값: {json.dumps(item, ensure_ascii=False)}"
                                    )
                            participants_to_insert.append((sememe_id,) + p_tuple)
                    
                    # Participants 삽입
                    if participants_to_insert:
                        execute_values(cur, """
                            INSERT INTO wordnet_factorized_participants (sememe_id, semantic_role, value_type, reasoning)
                            VALUES %s
                        """, participants_to_insert)
                        self.stats['participants'] += len(participants_to_insert)

            except (Exception, psycopg2.Error) as e:
                # 여기서 에러가 발생하면 DB 상태를 되돌리고,
                # 상위 에러 핸들러가 상세 정보를 출력하도록 에러를 다시 전달
                self.conn.rollback()
                raise e

    def print_stats(self):
        """최종 통계 출력"""
        print("\n========== 처리 완료 ==========")
        print(f"Qualifiers 삽입: {self.stats['qualifiers']:,}개")
        print(f"Sememes 삽입: {self.stats['sememes']:,}개")
        print(f"Participants 삽입: {self.stats['participants']:,}개")
        print("==============================")
        
    def close(self):
        """연결 종료"""
        self.conn.close()
        print("데이터베이스 연결 종료.")


def main():
    parser = argparse.ArgumentParser(description="Factorized WordNet JSON 데이터를 PostgreSQL에 삽입합니다.")
    parser.add_argument("--input-dir", type=str, default="geulso/factorize/factorized/", help="입력 JSON 파일들이 있는 디렉토리 경로")
    parser.add_argument("--batch-size", type=int, default=1000, help="한 번에 DB에 삽입할 레코드 수")
    parser.add_argument("--clear", action='store_true', help="기존 데이터를 모두 삭제하고 새로 삽입합니다.")
    args = parser.parse_args()

    loader = FactorizedDataToPostgres(DB_CONFIG)
    
    try:
        start_time = time.time()
        
        if args.clear:
            loader.clear_tables()
        
        loader.process_directory(args.input_dir, args.batch_size)
        loader.print_stats()
        
        elapsed = time.time() - start_time
        print(f"\n전체 소요 시간: {elapsed:.2f}초")
        
    except Exception as e:
        print(f"치명적 에러 발생: {e}")
        loader.conn.rollback()
        
    finally:
        loader.close()

if __name__ == "__main__":
    main()