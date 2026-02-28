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

# NLTK 라이브러리 import
import nltk
from nltk.corpus import wordnet as wn

# PostgreSQL 연결 설정
DB_CONFIG = {
    'host': 'localhost',
    'database': 'geuldev',
    'user': 'postgres',
    'password': 'test1224!'
}

class FactorizedDataValidator:
    """
    DB에 저장된 Factorized WordNet 데이터의 참조 무결성을 NLTK 실시간 조회를 통해 검사하고,
    오류를 종류별 파일에 기록하는 클래스.
    """
    def __init__(self, db_config: Dict[str, str], sememes_output: str, participants_output: str):
        self.conn = psycopg2.connect(**db_config)
        self.sememes_output_file = sememes_output
        self.participants_output_file = participants_output
        self.error_count = 0

        # [개선] Synset 유효성 검사 결과를 저장할 캐시(cache) 초기화
        self.validation_cache = {}

        # NLTK 데이터 다운로드 (필요시)
        try:
            nltk.data.find('corpora/wordnet.zip')
        except nltk.downloader.DownloadError:
            print("WordNet 데이터 다운로드 중...")
            nltk.download('wordnet')

        for filepath in [self.sememes_output_file, self.participants_output_file]:
            output_dir = os.path.dirname(filepath)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            if os.path.exists(filepath):
                os.remove(filepath)

    # [개선] NLTK 실시간 조회 및 캐싱을 사용한 유효성 검사 메서드
    def _is_valid_synset(self, synset_id: str) -> bool:
        """
        주어진 synset_id가 NLTK에서 유효한지 (리다이렉트 포함) 확인합니다.
        성능 향상을 위해 결과를 캐싱합니다.
        """
        if not synset_id:  # None 또는 빈 문자열은 유효한 것으로 간주
            return True
        
        if synset_id in self.validation_cache:
            return self.validation_cache[synset_id]
        
        try:
            wn.synset(synset_id)
            self.validation_cache[synset_id] = True
            return True
        except (nltk.corpus.reader.wordnet.WordNetError, ValueError, KeyError):
            self.validation_cache[synset_id] = False
            return False

    def _log_error(self, output_file: str, error_entry: Dict):
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(error_entry, ensure_ascii=False) + '\n')
        self.error_count += 1

    def validate_sememes(self):
        print("\n'wordnet_factorized_sememes' 테이블 검사 중...")
        query = "SELECT sememe_id, synset_id, frame_id, verb_property FROM wordnet_factorized_sememes"
        
        with self.conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM wordnet_factorized_sememes")
            total_rows = cur.fetchone()[0]
            if total_rows == 0:
                print("-> 검사할 데이터가 없습니다.")
                return
            
            cur.execute(query)
            for sememe_id, synset_id, frame_id, verb_property in tqdm(cur, total=total_rows, desc="Sememes 검사"):
                # [개선] _is_valid_synset 메서드로 유효성 확인
                if not self._is_valid_synset(verb_property):
                    reason = f"verb_property '{verb_property}' is not a valid synset in NLTK."
                    error_data = { "sememe_id": sememe_id, "synset_id": synset_id, "frame_id": frame_id, "key": "verb_property", "value": verb_property, "reasoning": reason }
                    self._log_error(self.sememes_output_file, error_data)

    def validate_participants(self):
        print("\n'wordnet_factorized_participants' 테이블 검사 중...")
        query = """
            SELECT p.sememe_id, s.synset_id, s.frame_id, p.semantic_role, p.value_type
            FROM wordnet_factorized_participants p
            JOIN wordnet_factorized_sememes s ON p.sememe_id = s.sememe_id
        """
        with self.conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM wordnet_factorized_participants")
            total_rows = cur.fetchone()[0]
            if total_rows == 0:
                print("-> 검사할 데이터가 없습니다.")
                return

            cur.execute(query)
            for sememe_id, synset_id, frame_id, semantic_role, value_type in tqdm(cur, total=total_rows, desc="Participants 검사"):
                # [개선] _is_valid_synset 메서드로 유효성 확인
                if not self._is_valid_synset(semantic_role):
                    reason = f"semantic_role '{semantic_role}' is not a valid synset in NLTK."
                    error_data = { "sememe_id": sememe_id, "synset_id": synset_id, "frame_id": frame_id, "key": "semantic_role", "value": semantic_role, "reasoning": reason }
                    self._log_error(self.participants_output_file, error_data)
                
                if not self._is_valid_synset(value_type):
                    reason = f"value_type '{value_type}' is not a valid synset in NLTK."
                    error_data = { "sememe_id": sememe_id, "synset_id": synset_id, "frame_id": frame_id, "key": "value_type", "value": value_type, "reasoning": reason }
                    self._log_error(self.participants_output_file, error_data)

    def print_summary(self):
        print("\n========== 유효성 검사 완료 ==========")
        if self.error_count == 0:
            print("  - ✅ 모든 참조가 유효합니다.")
        else:
            print(f"  - ❌ 총 {self.error_count:,}개의 잘못된 참조를 발견했습니다.")
            print(f"  - Sememe 오류 로그: '{self.sememes_output_file}'")
            print(f"  - Participant 오류 로그: '{self.participants_output_file}'")
        print("======================================")

    def close(self):
        self.conn.close()

def main():
    parser = argparse.ArgumentParser(description="DB에 저장된 Factorized WordNet 데이터의 참조 무결성을 NLTK 기준으로 검사합니다.")
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