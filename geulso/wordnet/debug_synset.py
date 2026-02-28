#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nltk
from nltk.corpus import wordnet as wn
import psycopg2

# PostgreSQL 연결 설정
DB_CONFIG = {
    'host': 'localhost',
    'database': 'geuldev',
    'user': 'postgres',
    'password': 'test1224!'
}

# 테스트할 Synset ID
SYNSET_TO_DEBUG = 'quantity.n.01'

def debug_single_synset():
    """특정 Synset 하나를 대상으로 DB 조회 및 삽입을 시도하여 문제를 진단합니다."""
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        print("="*50)
        print(f"'{SYNSET_TO_DEBUG}' 디버깅 시작")
        print("="*50)

        # 1. DB에 이미 존재하는지 확인
        print("\n[1단계] 데이터베이스 조회 시도...")
        cur.execute("SELECT * FROM wordnet_synsets WHERE synset_id = %s", (SYNSET_TO_DEBUG,))
        result = cur.fetchone()
        if result:
            print(f"-> ✅ 확인: '{SYNSET_TO_DEBUG}'는 이미 데이터베이스에 존재합니다.")
            print(f"-> 데이터: {result}")
            # 이미 존재하므로 더 이상 진행할 필요 없음
            return
        else:
            print(f"-> ❌ 확인: '{SYNSET_TO_DEBUG}'는 현재 데이터베이스에 없습니다.")

        # 2. NLTK에서 데이터 추출
        print("\n[2단계] NLTK에서 데이터 추출 시도...")
        try:
            synset = wn.synset(SYNSET_TO_DEBUG)
            print("-> ✅ NLTK에서 Synset 객체를 성공적으로 가져왔습니다.")
        except Exception as e:
            print(f"-> ❌ NLTK에서 Synset 객체를 가져오는 데 실패했습니다: {e}")
            return
            
        # 3. 삽입할 데이터 생성 (postgres.py와 동일한 로직)
        print("\n[3단계] DB에 삽입할 데이터 생성...")
        pos = synset.pos()
        lexname = synset.lexname()
        definition = synset.definition()
        examples = '; '.join(synset.examples()) if synset.examples() else None
        gloss = definition + (' ' + examples if examples else '')
        
        data_tuple = (SYNSET_TO_DEBUG, pos, lexname, definition, examples, gloss)
        print(f"-> 생성된 데이터 튜플:\n{data_tuple}")

        # 4. DB에 단일 행(Row) 삽입 시도
        print("\n[4단계] 데이터베이스에 단일 행 삽입 시도...")
        try:
            cur.execute("""
                INSERT INTO wordnet_synsets (synset_id, pos, lexname, definition, example, gloss)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, data_tuple)
            conn.commit()
            print("-> ✅ 삽입 성공!")
        except psycopg2.Error as e:
            print(f"-> ❌ 삽입 실패! 데이터베이스 오류 발생:")
            print(f"-> 에러 유형: {type(e).__name__}")
            print(f"-> 에러 메시지: {e}")
            conn.rollback()

    except psycopg2.Error as e:
        print(f"데이터베이스 연결 또는 기본 작업 중 에러 발생: {e}")
    finally:
        if conn:
            conn.close()
        print("\n" + "="*50)
        print("디버깅 완료")
        print("="*50)

if __name__ == "__main__":
    debug_single_synset()