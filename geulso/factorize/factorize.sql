
-- Qualifier 이름을 위한 ENUM 타입 생성 (기존과 동일)
CREATE TYPE qualifier_enum AS ENUM (
    'Evidentiality', 'Mood', 'Modality', 'Tense', 'Aspect',
    'Period/Point', 'Politeness', 'Polarity', 'Volitionality',
    'Confidence', 'Iterativity'
);

-- 1. Qualifiers 테이블 (이름 변경 및 FK 수정)
CREATE TABLE wordnet_factorized_qualifiers (
    synset_id VARCHAR(100) NOT NULL,
    frame_id INT NOT NULL,
    qualifier_name qualifier_enum NOT NULL,
    value NUMERIC(5, 2) NOT NULL,
    reasoning TEXT,
    -- PK 및 FK
    PRIMARY KEY (synset_id, frame_id, qualifier_name),
    -- wordnet_verb_frames를 직접 참조하도록 수정
    FOREIGN KEY (synset_id, frame_id) REFERENCES wordnet_verb_frames(synset_id, frame_id) ON DELETE CASCADE
);
COMMENT ON TABLE wordnet_factorized_qualifiers IS '하나의 동사 프레임(verb_frame)에 속한 여러 Qualifier와 그 값을 저장';

ALTER TABLE wordnet_factorized_qualifiers ALTER COLUMN value TYPE VARCHAR(50);
ALTER TABLE wordnet_factorized_qualifiers ALTER COLUMN value DROP NOT NULL;

-- 2. Sememes 테이블 (이름 변경 및 FK 수정)
CREATE TABLE wordnet_factorized_sememes (
    sememe_id SERIAL PRIMARY KEY,
    synset_id VARCHAR(100) NOT NULL,
    frame_id INT NOT NULL,
    verb_type VARCHAR(50),
    verb_property VARCHAR(100),
    reasoning TEXT,
    -- wordnet_verb_frames를 직접 참조하도록 수정
    FOREIGN KEY (synset_id, frame_id) REFERENCES wordnet_verb_frames(synset_id, frame_id) ON DELETE CASCADE
);
COMMENT ON TABLE wordnet_factorized_sememes IS '하나의 동사 프레임(verb_frame)에 속한 여러 Sememe 정보를 저장';


-- 3. Participants 테이블 (이름 변경)
CREATE TABLE wordnet_factorized_participants (
    participant_id SERIAL PRIMARY KEY,
    sememe_id INT NOT NULL,
    semantic_role VARCHAR(100),
    value_type VARCHAR(100), -- NULL일 수 있음
    reasoning TEXT,
    -- wordnet_factorized_sememes를 참조
    FOREIGN KEY (sememe_id) REFERENCES wordnet_factorized_sememes(sememe_id) ON DELETE CASCADE
);
COMMENT ON TABLE wordnet_factorized_participants IS '하나의 Sememe에 속한 여러 Participant 정보를 저장';


-- Qualifier 검색 최적화 인덱스
CREATE INDEX idx_factorized_qualifiers_name_value ON wordnet_factorized_qualifiers(qualifier_name, value);

-- Sememe의 verb_property 검색 최적화 인덱스
CREATE INDEX idx_factorized_sememes_verb_property ON wordnet_factorized_sememes(verb_property);

-- Participant의 semantic_role 검색 최적화 인덱스
CREATE INDEX idx_factorized_participants_semantic_role ON wordnet_factorized_participants(semantic_role);
