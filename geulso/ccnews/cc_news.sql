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



CREATE TABLE spacied_sentences (
    -- 기본 키 (자동 증가)
    id BIGSERIAL PRIMARY KEY,
    -- cc_news 테이블의 id 컬럼을 참조합니다.
    cc_news_id BIGINT NOT NULL REFERENCES cc_news(id) ON DELETE CASCADE,
    -- 기사 내에서 문장의 순서
    sentence_index INT NOT NULL,
    -- spaCy로 처리된 결과 전체를 저장 (검색 및 분석에 매우 효율적)
    spacy_data JSONB NOT NULL,
    -- 데이터 생성 시각
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    -- cc_news_id와 sentence_index의 조합은 고유해야 함
    UNIQUE (cc_news_id, sentence_index)
);

-- 인덱스 생성 (자주 사용할 컬럼에 대해)
CREATE INDEX idx_spacied_sentences_cc_news_id ON spacied_sentences(cc_news_id);

-- 테이블 및 컬럼에 대한 주석 추가
COMMENT ON TABLE spacied_sentences IS 'cc_news 기사를 문장 단위로 spaCy 처리한 결과';
COMMENT ON COLUMN spacied_sentences.cc_news_id IS '원본 cc_news 테이블의 ID (FK)';
COMMENT ON COLUMN spacied_sentences.sentence_index IS '원본 기사 내에서의 문장 순번';
COMMENT ON COLUMN spacied_sentences.spacy_data IS 'spaCy 분석 결과 전체 (sentence, tokens)';



-- spacy_news.py로 생성한 문장 분석 결과에 대한 LLM의 교정/검수 결과를 저장하는 테이블
CREATE TABLE corrected_sentences (
    -- 기본 키 (자동 증가)
    id BIGSERIAL PRIMARY KEY,
    -- 원본 문장 ID (spacied_sentences 테이블의 외래 키)
    sentence_id BIGINT NOT NULL REFERENCES spacied_sentences(id) ON DELETE CASCADE,
    -- 검수를 수행한 모델 정보 (예: 'ollama gpt-oss:20b')
    model VARCHAR(255) NOT NULL,
    -- 교정이 실제로 발생했는지 여부
    is_corrected BOOLEAN NOT NULL,
    -- 교정 내용 상세 로그 (JSONB)
    correction_log JSONB,
    -- 최종 토큰 리스트 (교정되었거나, 원본이거나) (JSONB)
    corrected_tokens JSONB NOT NULL,
    -- 데이터 생성 시각
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    -- 동일한 문장을 동일한 모델로 중복 검수하는 것을 방지
    UNIQUE (sentence_id, model)
);

-- 인덱스 생성
CREATE INDEX idx_corrected_sentences_sentence_id ON corrected_sentences(sentence_id);

-- 테이블 및 컬럼 주석
COMMENT ON TABLE corrected_sentences IS 'LLM을 통해 구문 분석(dependency parse)을 교정한 결과';
COMMENT ON COLUMN corrected_sentences.sentence_id IS '원본 spacied_sentences 테이블의 ID (FK)';
COMMENT ON COLUMN corrected_sentences.model IS '검수를 수행한 모델의 이름';
COMMENT ON COLUMN corrected_sentences.correction_log IS 'LLM이 생성한 교정 상세 내역';
COMMENT ON COLUMN corrected_sentences.corrected_tokens IS 'LLM이 최종적으로 반환한 토큰 리스트';