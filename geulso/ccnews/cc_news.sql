CREATE TABLE cc_news (
    -- 기본 키 (Primary Key), 8바이트 부호 없는 정수 (BIGINT)와 동일하며 자동 증가
    id BIGSERIAL PRIMARY KEY,

    -- 뉴스 기사 제목 (가변 길이 텍스트)
    title TEXT,

    -- 뉴스 기사 본문 (매우 긴 텍스트도 저장 가능)
    article_text TEXT NOT NULL, -- 본문은 필수 데이터로 가정

    -- 발행일 (타임존 정보 포함)
    published_date TIMESTAMP WITH TIME ZONE,

    -- 언론사 또는 출처 (가변 길이 텍스트)
    publisher VARCHAR(255),

    -- 저자 (가변 길이 텍스트)
    author VARCHAR(255),

    -- 원본 데이터 출처 URL 등 (중복 체크 등에 활용 가능)
    source_url TEXT UNIQUE,

    -- 데이터베이스에 추가된 시각 (기본값으로 현재 시간 자동 입력)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 테이블 생성에 대한 주석 추가
COMMENT ON TABLE cc_news IS 'Common Crawl News 데이터셋의 원본 기사를 저장하는 테이블';
COMMENT ON COLUMN cc_news.id IS '고유 식별자 (자동 증가)';
COMMENT ON COLUMN cc_news.article_text IS '뉴스 기사 본문 원본 텍스트';
COMMENT ON COLUMN cc_news.published_date IS '기사가 발행된 날짜와 시간';
COMMENT ON COLUMN cc_news.publisher IS '뉴스를 발행한 언론사 또는 기관';
COMMENT ON COLUMN cc_news.source_url IS '데이터를 수집한 원본 URL';


CREATE TABLE cc_news_sentences (
    -- 기본 키 (자동 증가)
    id BIGSERIAL PRIMARY KEY,

    -- cc_news 테이블의 id 컬럼을 참조합니다. 부모 기사가 삭제되면 문장도 함께 삭제됩니다.
    cc_news_id BIGINT NOT NULL REFERENCES cc_news(id) ON DELETE CASCADE,

    -- 기사 내에서 문장의 순서 (0부터 시작)
    sentence_index INT NOT NULL,

    -- 분리된 문장 텍스트 원본
    sentence_text TEXT NOT NULL,

    -- 데이터 생성 시각
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- cc_news_id와 sentence_index의 조합은 고유해야 함
    UNIQUE (cc_news_id, sentence_index)
);

-- 테이블 및 컬럼 주석 추가
COMMENT ON TABLE cc_news_sentences IS 'cc_news 테이블의 article_text를 문장 단위로 분리하여 저장하는 테이블';
COMMENT ON COLUMN cc_news_sentences.cc_news_id IS '원본 뉴스 기사의 ID (cc_news.id)';
COMMENT ON COLUMN cc_news_sentences.sentence_index IS '기사 내 문장의 순서 (0-based)';
COMMENT ON COLUMN cc_news_sentences.sentence_text IS '분리된 개별 문장의 텍스트';