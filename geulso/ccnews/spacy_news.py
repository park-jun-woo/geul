#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import spacy
import psycopg2
import psycopg2.extras
from tqdm import tqdm
import argparse
import json
import logging
from typing import List, Dict, Any, Tuple

# 로깅 설정
logging.basicConfig(
    filename='geulso/ccnews/spacy_db.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 데이터베이스 설정값
DB_CONFIG = {
    'host': 'localhost',
    'database': 'geuldev',
    'user': 'postgres',
    'password': 'test1224!'
}

def preprocess_text(text: str) -> str:
    """HGS 처리를 위해 텍스트를 정규화하고 불필요한 문자를 제거합니다."""
    if not isinstance(text, str):
        return ""
    # 모든 공백 문자(줄바꿈, 탭 등)를 단일 공백으로 정규화
    text = re.sub(r'\s+', ' ', text).strip()
    # 허용된 문자 집합 외의 모든 문자 제거
    allowed_chars = r"[^a-zA-Z0-9\s.,?'\"()[\]{}:;%$&-]"
    cleaned_text = re.sub(allowed_chars, '', text)
    return cleaned_text

def spacy_to_dict(sentence: spacy.tokens.span.Span) -> dict:
    """spaCy의 문장(Span) 객체를 지정된 JSON 형식의 딕셔너리로 변환합니다."""
    tokens = []
    start_token_offset = sentence.start
    for i, token in enumerate(sentence):
        tokens.append({
            "id": i,
            "text": token.text,
            "dep": token.dep_,
            "head_id": token.head.i - start_token_offset
        })
    return {"sentence": sentence.text, "tokens": tokens}

def get_db_connection():
    """PostgreSQL 데이터베이스에 연결합니다."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✓ PostgreSQL 데이터베이스 연결 성공")
        return conn
    except psycopg2.Error as e:
        print(f"✗ 데이터베이스 연결 실패: {e}")
        logging.error(f"데이터베이스 연결 실패: {e}")
        return None

def insert_sentences_batch(conn, data_batch: List[Tuple[int, int, str]]):
    """처리된 문장 배치를 spacied_sentences 테이블에 삽입합니다."""
    insert_query = """
        INSERT INTO spacied_sentences (cc_news_id, sentence_index, spacy_data)
        VALUES %s
        ON CONFLICT (cc_news_id, sentence_index) DO NOTHING;
    """
    if not data_batch:
        return
    try:
        with conn.cursor() as cur:
            psycopg2.extras.execute_values(cur, insert_query, data_batch)
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        logging.error(f"배치 삽입 실패: {e}")

def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(description="PostgreSQL의 CC-News 기사를 spaCy 처리하여 DB에 저장합니다.")
    parser.add_argument("--limit", type=int, default=0, help="처리할 최대 기사 수 (0=전체)")
    parser.add_argument("--batch-size", type=int, default=500, help="한 번에 DB에 삽입할 문장 수")
    parser.add_argument("--model", type=str, default="en_core_web_trf", help="사용할 spaCy 모델")
    args = parser.parse_args()

    print("="*60)
    print("CC-News spaCy 처리 및 PostgreSQL 저장 시작")
    print("="*60)

    # 읽기용과 쓰기용 연결을 분리하여 생성합니다.
    read_conn = get_db_connection()
    write_conn = get_db_connection()
    if not read_conn or not write_conn:
        if read_conn: read_conn.close()
        if write_conn: write_conn.close()
        return

    print(f"spaCy 모델 '{args.model}' 로딩 중...")
    try:
        spacy.prefer_gpu()
        nlp = spacy.load(args.model)
        print("✓ spaCy 모델 로딩 완료")
    except OSError:
        print(f"✗ spaCy 모델 '{args.model}'를 찾을 수 없습니다.")
        print(f"  실행: python -m spacy download {args.model}")
        if read_conn: read_conn.close()
        if write_conn: write_conn.close()
        return

    sentence_batch = []
    article_count = 0
    sentence_count = 0

    try:
        # 읽기용 연결(read_conn)로 서버 사이드 커서를 생성합니다.
        with read_conn.cursor('server_side_cursor') as cur:
            query = "SELECT id, article_text FROM cc_news"
            if args.limit > 0:
                query += f" LIMIT {args.limit}"
            cur.execute(query)

            pbar_total = args.limit if args.limit > 0 else None
            with tqdm(total=pbar_total, desc="기사 처리 중") as pbar:
                for article_id, article_text in cur:
                    cleaned_text = preprocess_text(article_text)
                    if not cleaned_text:
                        pbar.update(1)
                        continue

                    try:
                        doc = nlp(cleaned_text)
                        for j, sent in enumerate(doc.sents):
                            if len(sent.text.split()) < 3:
                                continue
                            
                            sentence_data_dict = spacy_to_dict(sent)
                            spacy_data_json = json.dumps(sentence_data_dict)
                            
                            sentence_batch.append((article_id, j, spacy_data_json))
                            sentence_count += 1

                            if len(sentence_batch) >= args.batch_size:
                                # 쓰기용 연결(write_conn)을 사용하여 배치 데이터를 삽입합니다.
                                insert_sentences_batch(write_conn, sentence_batch)
                                sentence_batch = []

                    except Exception as e:
                        logging.error(f"기사 ID {article_id} 처리 중 에러: {e}")
                        continue
                    
                    article_count += 1
                    pbar.update(1)

        # 마지막 남은 배치를 쓰기용 연결로 삽입합니다.
        if sentence_batch:
            insert_sentences_batch(write_conn, sentence_batch)

    except Exception as e:
        print(f"\n✗ 처리 중 심각한 에러 발생: {e}")
        logging.error(f"처리 중 심각한 에러 발생: {e}")
    finally:
        # 두 개의 연결을 모두 닫아줍니다.
        if read_conn:
            read_conn.close()
        if write_conn:
            write_conn.close()
        print("\n✓ 데이터베이스 연결 종료")

    print("\n" + "="*60)
    print("처리 완료!")
    print("="*60)
    print(f"총 처리한 기사: {article_count:,}개")
    print(f"총 DB에 저장된 문장: {sentence_count:,}개")
    print(f"로그 파일: geulso/ccnews/spacy_db.log")

if __name__ == "__main__":
    main()