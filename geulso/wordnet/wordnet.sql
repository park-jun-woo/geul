-- 위키데이터 대량 로드용 테이블 생성 (인덱스 없음)
-- PRIMARY KEY와 FOREIGN KEY 제약도 제거하여 최대 성능

-- 1. Synset (동의어 집합) - 워드넷의 핵심 단위
CREATE TABLE wordnet_synsets (
    synset_id VARCHAR(100) NOT NULL,      -- 수정됨
    pos CHAR(1) NOT NULL,
    lexname VARCHAR(50),
    definition TEXT,
    example TEXT,
    gloss TEXT
);

ALTER TABLE wordnet_synsets ADD PRIMARY KEY (synset_id);

-- 2. Lemma (단어 형태)
CREATE TABLE wordnet_lemmas (
    lemma_id SERIAL,
    synset_id VARCHAR(100) NOT NULL,      -- 수정됨
    word VARCHAR(100) NOT NULL,
    lemma_key VARCHAR(150),
    sense_number INT,
    tag_count INT DEFAULT 0
);

-- 3. Synset 관계
CREATE TABLE wordnet_synset_relations (
    from_synset VARCHAR(100) NOT NULL,    -- 수정됨
    to_synset VARCHAR(100) NOT NULL,      -- 수정됨
    relation_type VARCHAR(30) NOT NULL
);

-- 4. Lemma 간 관계
CREATE TABLE wordnet_lemma_relations (
    from_lemma_id INT NOT NULL,
    to_lemma_id INT NOT NULL,
    relation_type VARCHAR(30) NOT NULL
);

-- 5. 동사 프레임 (동사 전용)
CREATE TABLE wordnet_verb_frames (
    synset_id VARCHAR(100) NOT NULL,      -- 수정됨
    frame_id INT NOT NULL,
    frame_text TEXT
);

-- 6. 다국어 지원 (Open Multilingual Wordnet)
CREATE TABLE wordnet_multilingual (
    synset_id VARCHAR(100) NOT NULL,      -- 수정됨
    language VARCHAR(10) NOT NULL,
    word VARCHAR(200) NOT NULL,
    confidence FLOAT DEFAULT 1.0
);

-- 7. 위키데이터 매핑 테이블
CREATE TABLE wordnet_wikidata_mapping (
    synset_id VARCHAR(100) NOT NULL,      -- 수정됨
    wikidata_id VARCHAR(20),
    mapping_type VARCHAR(20),
    confidence FLOAT DEFAULT 1.0
);

-- 8. 메타데이터
CREATE TABLE wordnet_metadata (
    version VARCHAR(10),
    language VARCHAR(10),
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- 1. Synset 인덱스
CREATE INDEX idx_synsets_pos ON wordnet_synsets(pos);
CREATE INDEX idx_synsets_lexname ON wordnet_synsets(lexname);

-- 2. Lemma 인덱스
ALTER TABLE wordnet_lemmas ADD PRIMARY KEY (lemma_id);
CREATE INDEX idx_lemmas_synset ON wordnet_lemmas(synset_id);
CREATE INDEX idx_lemmas_word ON wordnet_lemmas(word);
CREATE INDEX idx_lemmas_word_lower ON wordnet_lemmas(LOWER(word)); -- 대소문자 무시 검색용
CREATE INDEX idx_lemmas_tag_count ON wordnet_lemmas(tag_count DESC); -- 빈도순 정렬용

-- 3. Synset 관계 인덱스
CREATE INDEX idx_synset_rel_from ON wordnet_synset_relations(from_synset);
CREATE INDEX idx_synset_rel_to ON wordnet_synset_relations(to_synset);
CREATE INDEX idx_synset_rel_type ON wordnet_synset_relations(relation_type);
-- 복합 인덱스 (관계 탐색 최적화)
CREATE INDEX idx_synset_rel_from_type ON wordnet_synset_relations(from_synset, relation_type);

-- 4. Lemma 관계 인덱스
CREATE INDEX idx_lemma_rel_from ON wordnet_lemma_relations(from_lemma_id);
CREATE INDEX idx_lemma_rel_to ON wordnet_lemma_relations(to_lemma_id);
CREATE INDEX idx_lemma_rel_type ON wordnet_lemma_relations(relation_type);

-- 5. 동사 프레임 인덱스
CREATE INDEX idx_verb_frames_synset ON wordnet_verb_frames(synset_id);

-- 6. 다국어 인덱스
CREATE INDEX idx_multi_synset ON wordnet_multilingual(synset_id);
CREATE INDEX idx_multi_lang ON wordnet_multilingual(language);
CREATE INDEX idx_multi_word ON wordnet_multilingual(word);
-- 복합 인덱스 (언어별 검색)
CREATE INDEX idx_multi_lang_word ON wordnet_multilingual(language, word);

-- 7. 위키데이터 매핑 인덱스
CREATE INDEX idx_mapping_synset ON wordnet_wikidata_mapping(synset_id);
CREATE INDEX idx_mapping_wikidata ON wordnet_wikidata_mapping(wikidata_id);
CREATE INDEX idx_mapping_type ON wordnet_wikidata_mapping(mapping_type);

-- 8. 유니크 제약 (중복 방지)
ALTER TABLE wordnet_synset_relations 
ADD CONSTRAINT uk_synset_relations UNIQUE (from_synset, to_synset, relation_type);

ALTER TABLE wordnet_lemma_relations 
ADD CONSTRAINT uk_lemma_relations UNIQUE (from_lemma_id, to_lemma_id, relation_type);

ALTER TABLE wordnet_verb_frames 
ADD CONSTRAINT uk_verb_frames UNIQUE (synset_id, frame_id);

ALTER TABLE wordnet_multilingual 
ADD CONSTRAINT uk_multilingual UNIQUE (synset_id, language, word);


