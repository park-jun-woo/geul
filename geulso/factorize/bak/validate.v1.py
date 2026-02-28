#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os
import json
import argparse
import psycopg2
import psycopg2.extras
from tqdm import tqdm
from typing import Dict, Set

# PostgreSQL 연결 설정
DB_CONFIG = {
    'host': 'localhost',
    'database': 'geuldev',
    'user': 'postgres',
    'password': 'test1224!'
}

class FactorizedDataValidator:
    """
    DB에 저장된 Factorized WordNet 데이터의 참조 무결성을 검사하고,
    오류를 종류별 파일에 기록하는 클래스.
    """
    def __init__(self, db_config: Dict[str, str], sememes_output: str, participants_output: str):
        """PostgreSQL 연결 및 유효한 Synset ID 로드"""
        self.conn = psycopg2.connect(**db_config)
        self.sememes_output_file = sememes_output
        self.participants_output_file = participants_output
        self.valid_synset_ids = self._load_valid_synset_ids()
        self.error_count = 0

        # 출력 디렉토리 생성 및 기존 로그 파일 삭제
        for filepath in [self.sememes_output_file, self.participants_output_file]:
            output_dir = os.path.dirname(filepath)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            if os.path.exists(filepath):
                os.remove(filepath)

    def _load_valid_synset_ids(self) -> Set[str]:
        """wordnet_synsets 테이블에서 모든 synset_id를 로드하여 set으로 반환합니다."""
        print("유효성 검사를 위해 DB에서 모든 Synset ID 로드 중...")
        with self.conn.cursor() as cur:
            cur.execute("SELECT synset_id FROM wordnet_synsets")
            synset_ids = {row[0] for row in cur.fetchall()}
        print(f"-> {len(synset_ids):,}개의 유효한 Synset ID 로드 완료.")
        return synset_ids

    def _log_error(self, output_file: str, error_entry: Dict):
        """잘못된 참조를 가진 데이터를 지정된 JSON 파일에 한 줄씩 기록합니다."""
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(error_entry, ensure_ascii=False) + '\n')
        self.error_count += 1

    def validate_sememes(self):
        """wordnet_factorized_sememes 테이블의 verb_property를 검사합니다."""
        print("\n'wordnet_factorized_sememes' 테이블 검사 중...")
        query = "SELECT sememe_id, synset_id, frame_id, verb_property FROM wordnet_factorized_sememes"
        with self.conn.cursor(name='sememes_cursor') as cur:
            cur.execute(query)
            
            # 서버 사이드 커서는 rowcount를 알 수 없으므로, 별도 카운트 쿼리 실행
            with self.conn.cursor() as count_cur:
                count_cur.execute("SELECT COUNT(*) FROM wordnet_factorized_sememes")
                total_rows = count_cur.fetchone()[0]

            for sememe_id, synset_id, frame_id, verb_property in tqdm(cur, total=total_rows, desc="Sememes 검사"):
                if verb_property and verb_property not in self.valid_synset_ids:
                    reason = f"verb_property '{verb_property}' is not exists."
                    error_data = {
                        "sememe_id": sememe_id,
                        "synset_id": synset_id,
                        "frame_id": frame_id,
                        "key": "verb_property",
                        "value": verb_property,
                        "reasoning": reason
                    }
                    self._log_error(self.sememes_output_file, error_data)

    def validate_participants(self):
        """wordnet_factorized_participants 테이블의 semantic_role과 value_type을 검사합니다."""
        print("\n'wordnet_factorized_participants' 테이블 검사 중...")
        query = """
            SELECT p.sememe_id, s.synset_id, s.frame_id, p.semantic_role, p.value_type
            FROM wordnet_factorized_participants p
            JOIN wordnet_factorized_sememes s ON p.sememe_id = s.sememe_id
        """
        with self.conn.cursor(name='participants_cursor') as cur:
            cur.execute(query)

            with self.conn.cursor() as count_cur:
                count_cur.execute("SELECT COUNT(*) FROM wordnet_factorized_participants")
                total_rows = count_cur.fetchone()[0]

            for sememe_id, synset_id, frame_id, semantic_role, value_type in tqdm(cur, total=total_rows, desc="Participants 검사"):
                if semantic_role and semantic_role not in self.valid_synset_ids:
                    reason = f"semantic_role '{semantic_role}' is not exists."
                    error_data = {
                        "sememe_id": sememe_id,
                        "synset_id": synset_id,
                        "frame_id": frame_id,
                        "key": "semantic_role",
                        "value": semantic_role,
                        "reasoning": reason
                    }
                    self._log_error(self.participants_output_file, error_data)
                
                if value_type and value_type not in self.valid_synset_ids:
                    reason = f"value_type '{value_type}' is not exists."
                    error_data = {
                        "sememe_id": sememe_id,
                        "synset_id": synset_id,
                        "frame_id": frame_id,
                        "key": "value_type",
                        "value": value_type,
                        "reasoning": reason
                    }
                    self._log_error(self.participants_output_file, error_data)

    def print_summary(self):
        """검사 결과를 요약하여 출력합니다."""
        print("\n========== 유효성 검사 완료 ==========")
        if self.error_count == 0:
            print("  - ✅ 모든 참조가 유효합니다.")
        else:
            print(f"  - ❌ 총 {self.error_count:,}개의 잘못된 참조를 발견했습니다.")
            print(f"  - Sememe 오류 로그: '{self.sememes_output_file}'")
            print(f"  - Participant 오류 로그: '{self.participants_output_file}'")
        print("======================================")

    def close(self):
        """연결 종료"""
        self.conn.close()

def main():
    parser = argparse.ArgumentParser(description="DB에 저장된 Factorized WordNet 데이터의 참조 무결성을 검사합니다.")
    parser.add_argument(
        "--sememes-output", 
        default="geulso/factorize/invalid.sememes.json", 
        help="잘못된 Sememe 참조 로그를 저장할 JSON 파일 경로"
    )
    parser.add_argument(
        "--participants-output", 
        default="geulso/factorize/invalid.participants.json", 
        help="잘못된 Participant 참조 로그를 저장할 JSON 파일 경로"
    )
    args = parser.parse_args()

    validator = FactorizedDataValidator(DB_CONFIG, args.sememes_output, args.participants_output)
    
    try:
        start_time = time.time()
        
        validator.validate_sememes()
        validator.validate_participants()
        validator.print_summary()

        elapsed = time.time() - start_time
        print(f"\n전체 소요 시간: {elapsed:.2f}초")

    except Exception as e:
        print(f"치명적 에러 발생: {e}")
    finally:
        validator.close()

if __name__ == "__main__":
    main()