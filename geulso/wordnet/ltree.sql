CREATE EXTENSION IF NOT EXISTS ltree;

CREATE TABLE verb_hypernym_ltree (
    synset_id VARCHAR(100) NOT NULL PRIMARY KEY,
    definition TEXT,
    tree_path LTREE NOT NULL,
    depth INTEGER DEFAULT 0  -- 트리 깊이 추가
);

CREATE INDEX idx_verb_ltree_path_gist ON verb_hypernym_ltree USING GIST (tree_path);
CREATE INDEX idx_verb_ltree_depth ON verb_hypernym_ltree (depth);