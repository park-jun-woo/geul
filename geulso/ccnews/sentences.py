import psycopg2
import psycopg2.extras
import nltk
import os
from tqdm import tqdm

# --- 설정 ---
# 데이터베이스 연결 정보 (환경에 맞게 수정)
DB_HOST = "localhost"
DB_NAME = "geuldev"
DB_USER = "postgres"
DB_PASSWORD = "test1224!" # 실제 비밀번호로 변경

# 한 번에 처리할 기사의 수
BATCH_SIZE = 100

def process_articles_batch(write_conn, articles):
    """
    여러 기사를 받아 문장으로 분리하고, 별도의 쓰기용 연결(write_conn)을
    사용하여 DB에 한 번에 저장합니다.
    """
    sentences_to_insert = []
    for article_id, article_text in articles:
        try:
            # NLTK를 사용하여 문장 단위로 분리
            sentences = nltk.sent_tokenize(article_text)
            for i, sentence in enumerate(sentences):
                # 공백만 있는 문장은 제외
                if sentence.strip():
                    sentences_to_insert.append((article_id, i, sentence))
        except Exception as e:
            print(f"Error processing article {article_id}: {e}")

    if not sentences_to_insert:
        return

    # executemany를 사용하여 여러 문장을 효율적으로 INSERT
    insert_query = """
        INSERT INTO cc_news_sentences (cc_news_id, sentence_index, sentence_text)
        VALUES %s
        ON CONFLICT (cc_news_id, sentence_index) DO NOTHING;
    """
    try:
        # 쓰기용 연결(write_conn)에서 커서를 새로 생성하여 사용
        with write_conn.cursor() as write_cursor:
            psycopg2.extras.execute_values(
                write_cursor,
                insert_query,
                sentences_to_insert,
                template=None,
                page_size=len(sentences_to_insert)
            )
        # 쓰기 작업이 성공하면 커밋
        write_conn.commit()
    except Exception as e:
        # 오류 발생 시 롤백하여 트랜잭션 취소
        write_conn.rollback()
        print(f"Database insert error: {e}")


def main():
    """
    DB에 읽기용/쓰기용 연결을 별도로 생성하고 cc_news 테이블의 모든 기사를
    문장으로 분리하여 저장합니다.
    """
    read_conn = None
    write_conn = None
    try:
        # 데이터베이스 연결 (읽기용, 쓰기용 2개 생성)
        read_conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        write_conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        print("PostgreSQL 읽기/쓰기 연결 성공!")

        with read_conn.cursor() as read_cursor:
            # 처리할 전체 기사 수 확인
            read_cursor.execute("SELECT COUNT(id) FROM cc_news;")
            total_articles = read_cursor.fetchone()[0]
            print(f"총 {total_articles}개의 기사를 처리합니다.")

            # 서버 사이드 커서를 사용하여 대용량 데이터를 효율적으로 처리
            # 'WITH HOLD' 없이도 연결이 분리되어 있어 안전합니다.
            read_cursor.execute("DECLARE articles_cursor CURSOR FOR SELECT id, article_text FROM cc_news;")

            with tqdm(total=total_articles, desc="Processing Articles") as pbar:
                while True:
                    # 읽기용 커서로 데이터 가져오기
                    read_cursor.execute(f"FETCH {BATCH_SIZE} FROM articles_cursor;")
                    articles_batch = read_cursor.fetchall()

                    if not articles_batch:
                        break # 더 이상 가져올 기사가 없으면 종료

                    # 쓰기용 연결을 사용하여 데이터 처리 및 저장
                    process_articles_batch(write_conn, articles_batch)
                    
                    # 루프 내의 commit은 이제 process_articles_batch 함수가 담당하므로 제거됨
                    pbar.update(len(articles_batch))

    except psycopg2.Error as e:
        print(f"Database error: {e}")
    finally:
        # 두 개의 연결을 모두 안전하게 종료
        if write_conn:
            write_conn.close()
            print("PostgreSQL 쓰기용 연결 종료.")
        if read_conn:
            read_conn.close()
            print("PostgreSQL 읽기용 연결 종료.")

if __name__ == "__main__":
    # NLTK 데이터 경로 확인 (선택적)
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError as e:
        print(f"NLTK 데이터가 필요합니다. 오류: {e}")
        print("파이썬에서 nltk.download('punkt') 와 nltk.download('punkt_tab')을 실행해주세요.")
        exit()

    main()