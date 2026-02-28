#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras
from datasets import load_dataset
from tqdm import tqdm
import argparse
import logging
from typing import List, Dict, Any

# ... (상단 설정 및 다른 함수들은 그대로 둡니다) ...
# 로깅 설정
logging.basicConfig(
    filename='geulso/ccnews/ccnews.log',
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

def insert_data_batch(conn, data_batch: List[Dict[str, Any]]):
    """데이터 배치를 cc_news 테이블에 삽입합니다."""
    # 이전에 논의했던 공식 cc_news 데이터셋 필드명으로 수정합니다.
    insert_query = """
        INSERT INTO cc_news (title, article_text, published_date, publisher, author, source_url)
        VALUES %s
        ON CONFLICT (source_url) DO NOTHING;
    """
    values = [
        (
            item.get('title'),
            item.get('text'),
            item.get('publish_date'),
            item.get('domain'),
            item.get('author'),
            item.get('url')
        ) for item in data_batch
    ]
    
    if not values:
        return

    try:
        with conn.cursor() as cur:
            psycopg2.extras.execute_values(cur, insert_query, values)
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        logging.error(f"배치 삽입 실패: {e}")
        # 개별 삽입으로 재시도 (필요 시)
        for value_tuple in values:
            try:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO cc_news (title, article_text, published_date, publisher, author, source_url)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (source_url) DO NOTHING;
                    """, value_tuple)
                conn.commit()
            except psycopg2.Error as inner_e:
                conn.rollback()
                logging.error(f"개별 삽입 실패 (URL: {value_tuple[5]}): {inner_e}")


def main():
    """메인 실행 함수"""
    # *** 수정된 부분: argparse 코드를 main 함수 안으로 이동 ***
    parser = argparse.ArgumentParser(description="Hugging Face CC-News 데이터셋을 PostgreSQL에 삽입합니다.")
    parser.add_argument("--batch-size", type=int, default=1000, help="한 번에 삽입할 데이터 배치 크기")
    parser.add_argument("--limit", type=int, default=0, help="처리할 최대 기사 수 (0=전체)")
    args = parser.parse_args()

    print("="*60)
    print("CC-News 데이터 PostgreSQL 삽입 시작")
    print("="*60)
    
    conn = get_db_connection()
    if not conn:
        return

    # 'stanford-oval/ccnews' 대신 공식 'cc_news'를 사용하는 것을 권장합니다.
    print(f"Hugging Face에서 'cc_news' 데이터셋 로딩 중 (스트리밍)...")
    try:
        dataset = load_dataset("cc_news", split="train", streaming=True)
        print("✓ 데이터셋 로딩 완료")
    except Exception as e:
        print(f"✗ 데이터셋 로드 실패: {e}")
        logging.error(f"데이터셋 로드 실패: {e}")
        conn.close()
        return

    data_batch = []
    processed_count = 0

    # tqdm의 total 값에 args를 사용
    pbar = tqdm(total=args.limit if args.limit > 0 else 708241, desc="기사 처리 중")

    try:
        for item in iter(dataset):
            if args.limit > 0 and processed_count >= args.limit:
                break
            
            # cc_news 데이터셋의 필드명에 맞게 수정
            prepared_item = {
                'title': item.get('title'),
                'text': item.get('text'),
                'publish_date': item.get('publish_date'),
                'domain': item.get('domain'),
                'author': item.get('author'),
                'url': item.get('url'),
            }
            
            if not prepared_item['text'] or not prepared_item['url']:
                continue

            data_batch.append(prepared_item)

            if len(data_batch) >= args.batch_size:
                insert_data_batch(conn, data_batch)
                processed_count += len(data_batch)
                pbar.update(len(data_batch))
                data_batch = []
        
        if data_batch:
            insert_data_batch(conn, data_batch)
            processed_count += len(data_batch)
            pbar.update(len(data_batch))

    except Exception as e:
        print(f"\n✗ 처리 중 에러 발생: {e}")
        logging.error(f"처리 중 에러 발생: {e}")
    finally:
        pbar.close()
        conn.close()
        print("\n✓ 데이터베이스 연결 종료")

    print("\n" + "="*60)
    print("처리 완료!")
    print("="*60)
    print(f"총 처리한 기사: {processed_count:,}개")
    print(f"로그 파일: geulso/ccnews/ccnews.log")


if __name__ == "__main__":
    main()