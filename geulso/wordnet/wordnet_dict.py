#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import time
import argparse
import psycopg2
from psycopg2.extras import execute_batch
from collections import defaultdict
from typing import Dict, Set, List, Tuple
from tqdm import tqdm

# PostgreSQL 연결 설정
DB_CONFIG = {
    'host': 'localhost',
    'database': 'geuldev',
    'user': 'postgres',
    'password': 'test1224!'
}

class WordNetDictParser:
    """
    WordNet 원본 dict 파일을 파싱하여 PostgreSQL에 삽입하는 클래스.
    """
    def __init__(self, db_config: Dict[str, str], dict_path: str):
        self.conn = psycopg2.connect(**db_config)
        self.dict_path = dict_path
        self.stats = defaultdict(int)
        self.batch_size = 1000

        # 데이터 처리를 위한 내부 자료구조
        self.offset_to_synset_info = {}
        self.offset_to_synset_id = {}
        self.pos_map = {'n': 'n', 'v': 'v', 'a': 'a', 's': 'a', 'r': 'r'}

    def clear_tables(self):
        print("기존 워드넷 데이터 삭제 중...")
        tables = [
            'wordnet_lemma_relations', 'wordnet_synset_relations',
            'wordnet_verb_frames', 'wordnet_multilingual',
            'wordnet_wikidata_mapping', 'wordnet_lemmas',
            'wordnet_synsets', 'wordnet_metadata'
        ]
        with self.conn.cursor() as cur:
            for table in tables:
                cur.execute(f"TRUNCATE TABLE {table} CASCADE")
        self.conn.commit()
        print("데이터 삭제 완료.")

    def _parse_data_files(self):
        """data.noun, data.verb 등의 파일을 파싱하여 기본 정보를 구축합니다."""
        print("1단계: WordNet 데이터 파일 파싱 중...")
        for pos_file in ['data.noun', 'data.verb', 'data.adj', 'data.adv']:
            filepath = os.path.join(self.dict_path, pos_file)
            if not os.path.exists(filepath):
                continue

            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith(' '): continue # 주석 라인 건너뛰기
                    
                    parts = line.split('|')
                    main_data = parts[0].strip().split()
                    gloss = parts[1].strip() if len(parts) > 1 else ''

                    offset = main_data[0]
                    pos = main_data[2]
                    
                    if pos not in self.pos_map: continue
                    
                    num_lemmas = int(main_data[3], 16)
                    lemmas = [main_data[4 + i*2] for i in range(num_lemmas)]

                    # 관계(포인터) 정보 파싱
                    p_cnt_index = 4 + num_lemmas * 2
                    p_cnt = int(main_data[p_cnt_index])
                    pointers = []
                    for i in range(p_cnt):
                        pointer_index = p_cnt_index + 1 + i * 4
                        pointers.append({
                            "symbol": main_data[pointer_index],
                            "offset": main_data[pointer_index+1],
                            "pos": main_data[pointer_index+2]
                        })

                    # 파싱된 정보를 딕셔너리에 저장
                    unique_key = f"{self.pos_map[pos]}{offset}"
                    self.offset_to_synset_info[unique_key] = {
                        "lemmas": lemmas,
                        "pos": self.pos_map[pos],
                        "gloss": gloss,
                        "pointers": pointers
                    }

    def _build_synset_ids(self):
        """파싱된 데이터를 기반으로 NLTK 스타일의 Synset ID를 생성합니다."""
        print("2단계: NLTK 스타일 Synset ID 생성 중...")
        word_sense_counts = defaultdict(int)
        
        # index.sense 파일을 읽어 NLTK와 유사한 순서로 ID를 생성
        filepath = os.path.join(self.dict_path, 'index.sense')
        if not os.path.exists(filepath):
            raise FileNotFoundError("ID 생성을 위해 index.sense 파일이 필요합니다.")

        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                # 예: dog%1:03:00::
                sense_key = line.split(' ')[0]
                offset = line.split(' ')[1]
                
                match = re.match(r"(\w+)%(\d):", sense_key)
                if not match: continue

                word = match.group(1)
                pos_num = match.group(2)
                
                pos_char_map = {'1':'n', '2':'v', '3':'a', '4':'r', '5':'a'}
                pos = pos_char_map.get(pos_num)
                if not pos: continue

                unique_key = f"{pos}{offset}"
                if unique_key not in self.offset_to_synset_id:
                    word_sense_counts[f"{word}.{pos}"] += 1
                    sense_num = word_sense_counts[f"{word}.{pos}"]
                    self.offset_to_synset_id[unique_key] = f"{word}.{pos}.{sense_num:02d}"

    def _insert_data_batch(self, table_name, columns, batch):
        """범용 배치 삽입 메서드"""
        if not batch: return
        cols = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))
        
        # ON CONFLICT 로직 추가 (필요시)
        conflict_action = ""
        if table_name == "wordnet_synsets":
            conflict_action = "ON CONFLICT (synset_id) DO NOTHING"
        elif table_name == "wordnet_synset_relations":
            conflict_action = "ON CONFLICT (from_synset, to_synset, relation_type) DO NOTHING"
        
        query = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders}) {conflict_action}"
        
        with self.conn.cursor() as cur:
            psycopg2.extras.execute_batch(cur, query, batch)
        self.conn.commit()
        self.stats[table_name] += len(batch)


    def run_insertion(self):
        """모든 데이터를 DB에 삽입하는 메인 프로세스 실행"""
        print("3단계: 데이터베이스 삽입 시작...")
        
        # Synsets와 Lemmas 삽입
        synsets_batch = []
        lemmas_batch = []
        for offset_key, synset_id in tqdm(self.offset_to_synset_id.items(), desc="Synsets/Lemmas 준비"):
            info = self.offset_to_synset_info.get(offset_key)
            if not info: continue
            
            definition, *examples_list = info['gloss'].split(';')
            example = '; '.join(ex.strip('" ') for ex in examples_list) if examples_list else None
            
            synsets_batch.append((
                synset_id, info['pos'], None, definition.strip(), example, info['gloss']
            ))
            
            for word in info['lemmas']:
                lemmas_batch.append((synset_id, word.replace('_', ' '), None, None, None))
            
            if len(synsets_batch) >= self.batch_size:
                self._insert_data_batch("wordnet_synsets", ["synset_id", "pos", "lexname", "definition", "example", "gloss"], synsets_batch)
                synsets_batch = []
            if len(lemmas_batch) >= self.batch_size:
                 self._insert_data_batch("wordnet_lemmas", ["synset_id", "word", "lemma_key", "sense_number", "tag_count"], lemmas_batch)
                 lemmas_batch = []
        
        self._insert_data_batch("wordnet_synsets", ["synset_id", "pos", "lexname", "definition", "example", "gloss"], synsets_batch)
        self._insert_data_batch("wordnet_lemmas", ["synset_id", "word", "lemma_key", "sense_number", "tag_count"], lemmas_batch)

        print("Synsets/Lemmas 삽입 완료.")
        
        # Synset 관계 삽입
        # (간략화를 위해 이 예제에서는 모든 관계를 hypernym으로 가정, 실제로는 symbol 매핑 필요)
        relations_batch = []
        for offset_key, synset_id in tqdm(self.offset_to_synset_id.items(), desc="관계 준비"):
             info = self.offset_to_synset_info.get(offset_key)
             if not info: continue
             
             from_synset = synset_id
             for pointer in info['pointers']:
                 to_offset_key = f"{pointer['pos']}{pointer['offset']}"
                 to_synset = self.offset_to_synset_id.get(to_offset_key)
                 if to_synset:
                     # 실제로는 pointer['symbol']을 'hypernym' 등으로 변환해야 함
                     relations_batch.append((from_synset, to_synset, 'unknown_relation'))

        self._insert_data_batch("wordnet_synset_relations", ["from_synset", "to_synset", "relation_type"], relations_batch)
        print("관계 삽입 완료.")

    def print_summary(self):
        print("\n========== 처리 완료 ==========")
        for key, value in self.stats.items():
            print(f"{key.replace('_', ' ').capitalize()}: {value:,}개")
        print("==============================")
        
    def close(self):
        self.conn.close()

def main():
    parser = argparse.ArgumentParser(description="WordNet 원본 dict 파일을 파싱하여 PostgreSQL에 삽입합니다.")
    parser.add_argument("--dict-path", type=str, default="~/dict/", help="압축 해제된 WordNet 'dict' 디렉토리 경로")
    parser.add_argument("--clear", action='store_true', help="기존 워드넷 데이터를 모두 삭제하고 새로 삽입합니다.")
    args = parser.parse_args()

    expanded_path = os.path.expanduser(args.dict_path)
    parser_instance = WordNetDictParser(DB_CONFIG, expanded_path)
    
    try:
        start_time = time.time()
        
        if args.clear:
            parser_instance.clear_tables()
            
        parser_instance._parse_data_files()
        parser_instance._build_synset_ids()
        parser_instance.run_insertion()
        parser_instance.print_summary()
        
        elapsed = time.time() - start_time
        print(f"\n전체 소요 시간: {elapsed:.2f}초")
        
    except Exception as e:
        print(f"치명적 에러 발생: {e}")
        parser_instance.conn.rollback()
    finally:
        parser_instance.close()

if __name__ == "__main__":
    main()