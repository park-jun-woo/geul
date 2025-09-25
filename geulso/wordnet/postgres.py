#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nltk
from nltk.corpus import wordnet as wn
import psycopg2
from psycopg2.extras import execute_batch
import time
from datetime import datetime
from typing import Dict, Set
from tqdm import tqdm

# NLTK 데이터 다운로드 (필요시)
try:
    nltk.data.find('corpora/wordnet.zip')
except nltk.downloader.DownloadError:
    nltk.download('wordnet')

try:
    nltk.data.find('corpora/omw-1.4.zip')
except nltk.downloader.DownloadError:
    nltk.download('omw-1.4')

class WordNetToPostgres:
    def __init__(self, db_config: Dict[str, str]):
        self.conn = psycopg2.connect(**db_config)
        self.cursor = self.conn.cursor()
        self.stats = {
            'synsets': 0, 'lemmas': 0, 'relations': 0,
            'verb_frames': 0, 'multilingual': 0
        }
        self.batch_size = 1000
        self.existing_synset_ids = self._load_existing_synset_ids()

    def _load_existing_synset_ids(self) -> Set[str]:
        print("데이터베이스에서 기존 Synset ID 로드 중...")
        with self.conn.cursor() as cur:
            cur.execute("SELECT synset_id FROM wordnet_synsets")
            synset_ids = {row[0] for row in cur.fetchall()}
        print(f"-> {len(synset_ids):,}개의 기존 Synset ID 로드 완료.")
        return synset_ids

    def clear_tables(self):
        print("기존 데이터 삭제 중...")
        tables = [
            'wordnet_lemma_relations', 'wordnet_synset_relations',
            'wordnet_verb_frames', 'wordnet_multilingual',
            'wordnet_wikidata_mapping', 'wordnet_lemmas',
            'wordnet_synsets', 'wordnet_metadata'
        ]
        
        for table in tables:
            self.cursor.execute(f"TRUNCATE TABLE {table} CASCADE")
        self.conn.commit()
        print("데이터 삭제 완료")
        
    def insert_metadata(self):
        self.cursor.execute("TRUNCATE TABLE wordnet_metadata")
        self.cursor.execute("""
            INSERT INTO wordnet_metadata (version, language, imported_at)
            VALUES (%s, %s, %s)
        """, ('3.0', 'en', datetime.now()))
        self.conn.commit()
        
    def process_synsets(self):
        print("Synsets 처리 중 (신규 데이터만 선별)...")
        synsets_batch = []
        lemmas_batch = []
        
        all_synsets = list(wn.all_synsets())
        for synset in tqdm(all_synsets, desc="Synsets/Lemmas 처리"):
            try: 
                synset_id = synset.name()
                if synset_id in self.existing_synset_ids:
                    continue
                
                pos = synset.pos()
                lexname = synset.lexname()
                definition = synset.definition()
                examples = '; '.join(synset.examples()) if synset.examples() else None
                
                synsets_batch.append((
                    synset_id, pos, lexname, definition, examples,
                    definition + (' ' + examples if examples else '')
                ))
                
                for lemma in synset.lemmas():
                    lemmas_batch.append((
                        synset_id, lemma.name().replace('_', ' '),
                        lemma.key(), synset.offset(), lemma.count()
                    ))
                
                if len(synsets_batch) >= self.batch_size:
                    self._insert_synsets_batch(synsets_batch)
                    synsets_batch = []
                if len(lemmas_batch) >= self.batch_size:
                    self._insert_lemmas_batch(lemmas_batch)
                    lemmas_batch = []
            except Exception as e:
                tqdm.write(f"경고: Synset {synset.name()} 처리 중 오류 발생, 건너뜁니다. 오류: {e}")
                continue
                
        if synsets_batch: self._insert_synsets_batch(synsets_batch)
        if lemmas_batch: self._insert_lemmas_batch(lemmas_batch)
        print(f"신규 Synsets: {self.stats['synsets']}개, 신규 Lemmas: {self.stats['lemmas']}개 처리 완료")
        
    def _insert_synsets_batch(self, batch):
        execute_batch(self.cursor, """
            INSERT INTO wordnet_synsets (synset_id, pos, lexname, definition, example, gloss)
            VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (synset_id) DO NOTHING
        """, batch)
        self.stats['synsets'] += len(batch)
        self.conn.commit()
        
    def _insert_lemmas_batch(self, batch):
        execute_batch(self.cursor, """
            INSERT INTO wordnet_lemmas (synset_id, word, lemma_key, sense_number, tag_count)
            VALUES (%s, %s, %s, %s, %s)
        """, batch)
        self.stats['lemmas'] += len(batch)
        self.conn.commit()

    def process_relations(self):
        print("Synset 관계 처리 중 (ON CONFLICT로 중복 방지)...")
        relations_batch = []
        relation_types = [
            ('hypernym', lambda s: s.hypernyms()), ('hyponym', lambda s: s.hyponyms()),
            ('instance_hypernym', lambda s: s.instance_hypernyms()), ('instance_hyponym', lambda s: s.instance_hyponyms()),
            ('member_holonym', lambda s: s.member_holonyms()), ('part_holonym', lambda s: s.part_holonyms()), ('substance_holonym', lambda s: s.substance_holonyms()),
            ('member_meronym', lambda s: s.member_meronyms()), ('part_meronym', lambda s: s.part_meronyms()), ('substance_meronym', lambda s: s.substance_meronyms()),
            ('similar_to', lambda s: s.similar_tos()), ('attribute', lambda s: s.attributes()),
            ('entailment', lambda s: s.entailments()), ('cause', lambda s: s.causes()),
            ('also_see', lambda s: s.also_sees()), ('verb_group', lambda s: s.verb_groups()),
            ('topic_domain', lambda s: s.topic_domains()), ('region_domain', lambda s: s.region_domains()), ('usage_domain', lambda s: s.usage_domains())
        ]
        
        for synset in tqdm(wn.all_synsets(), desc="관계 처리"):
            synset_id = synset.name()
            for rel_type, rel_func in relation_types:
                try: 
                    related = rel_func(synset)
                    for related_synset in related:
                        relations_batch.append((synset_id, related_synset.name(), rel_type))
                        if len(relations_batch) >= self.batch_size:
                            self._insert_relations_batch(relations_batch)
                            relations_batch = []
                except Exception as e:
                    tqdm.write(f"경고: 관계 '{rel_type}' 처리 중 {synset_id}에서 오류 발생, 건너뜁니다. 오류: {e}")
                    continue
                    
        if relations_batch: self._insert_relations_batch(relations_batch)
        print(f"관계: {self.stats['relations']}개 삽입 시도 완료")
        
    def _insert_relations_batch(self, batch):
        execute_batch(self.cursor, """
            INSERT INTO wordnet_synset_relations (from_synset, to_synset, relation_type)
            VALUES (%s, %s, %s) ON CONFLICT (from_synset, to_synset, relation_type) DO NOTHING
        """, batch)
        self.stats['relations'] += len(batch)
        self.conn.commit()
        
    def process_verb_frames(self):
        print("동사 프레임 처리 중 (ON CONFLICT로 중복 방지)...")
        frames_batch = []
        for synset in tqdm(wn.all_synsets(pos='v'), desc="동사 프레임 처리"):
            try: 
                synset_id = synset.name()
                unique_frames = set()
                for lemma in synset.lemmas():
                    unique_frames.update(lemma.frame_strings())
                
                for frame_id, frame_text in enumerate(sorted(list(unique_frames))):
                    frames_batch.append((synset_id, frame_id, frame_text))
                
                if len(frames_batch) >= self.batch_size:
                    self._insert_verb_frames_batch(frames_batch)
                    frames_batch = []
            except Exception as e:
                tqdm.write(f"경고: 동사 프레임 처리 중 {synset.name()}에서 오류 발생, 건너뜁니다. 오류: {e}")
                continue
                        
        if frames_batch: self._insert_verb_frames_batch(frames_batch)
        print(f"동사 프레임: {self.stats['verb_frames']}개 삽입 시도 완료")
        
    def _insert_verb_frames_batch(self, batch):
        execute_batch(self.cursor, """
            INSERT INTO wordnet_verb_frames (synset_id, frame_id, frame_text)
            VALUES (%s, %s, %s) ON CONFLICT (synset_id, frame_id) DO NOTHING
        """, batch)
        self.stats['verb_frames'] += len(batch)
        self.conn.commit()
        
    def process_multilingual(self):
        print("다국어 데이터 처리 중 (ON CONFLICT로 중복 방지)...")
        multi_batch = []
        languages = wn.langs()
        
        for lang in tqdm(languages, desc="다국어 처리"):
            if lang == 'en': continue
            try:
                for synset in wn.all_synsets():
                    for lemma in synset.lemmas(lang=lang):
                        multi_batch.append((synset.name(), lang, lemma.name().replace('_', ' ')))
                        if len(multi_batch) >= self.batch_size:
                            self._insert_multilingual_batch(multi_batch)
                            multi_batch = []
            except Exception as e:
                tqdm.write(f"경고: 다국어 '{lang}' 처리 중 오류 발생, 해당 언어를 건너뛸 수 있습니다. 오류: {e}")
                continue
                
        if multi_batch: self._insert_multilingual_batch(multi_batch)
        print(f"다국어: {self.stats['multilingual']}개 삽입 시도 완료")
        
    def _insert_multilingual_batch(self, batch):
        execute_batch(self.cursor, """
            INSERT INTO wordnet_multilingual (synset_id, language, word)
            VALUES (%s, %s, %s) ON CONFLICT (synset_id, language, word) DO NOTHING
        """, batch)
        self.stats['multilingual'] += len(batch)
        self.conn.commit()
        
    def print_stats(self):
        print("\n========== 처리 완료 ==========")
        print(f"신규 Synsets: {self.stats['synsets']:,}개")
        print(f"신규 Lemmas: {self.stats['lemmas']:,}개")
        print(f"관계 (삽입 시도): {self.stats['relations']:,}개")
        print(f"동사 프레임 (삽입 시도): {self.stats['verb_frames']:,}개")
        print(f"다국어 (삽입 시도): {self.stats['multilingual']:,}개")
        print("==============================")
        
    def close(self):
        self.cursor.close()
        self.conn.close()

def main():
    db_config = {
        'host': 'localhost',
        'database': 'geuldev',
        'user': 'postgres',
        'password': 'test1224!'
    }
    
    loader = WordNetToPostgres(db_config)
    current_process = "" 
    try:
        start_time = time.time()
        
        # 데이터를 완전히 새로 넣으려면 아래 주석을 해제하세요.
        # print("경고: 모든 테이블의 데이터를 삭제합니다. 5초 후 시작...")
        # time.sleep(5)
        loader.clear_tables()
        loader.existing_synset_ids = set() # clear 후에는 메모리의 집합도 비워줘야 함
        
        current_process = "insert_metadata"
        loader.insert_metadata()
        
        current_process = "process_synsets"
        loader.process_synsets()

        current_process = "process_relations"
        loader.process_relations()

        current_process = "process_verb_frames"
        loader.process_verb_frames()

        current_process = "process_multilingual"
        loader.process_multilingual()
        
        loader.print_stats()
        
        elapsed = time.time() - start_time
        print(f"\n전체 소요 시간: {elapsed:.1f}초")
        
    except Exception as e:
        print("\n" + "="*80)
        print(f"🔥 '{current_process}' 작업 중 치명적 에러가 발생하여 중단되었습니다.")
        print(f"🔥 에러 유형: {type(e).__name__}")
        print(f"🔥 에러 메시지: {e}")
        print("="*80)
        loader.conn.rollback()
        
    finally:
        loader.close()

if __name__ == "__main__":
    main()