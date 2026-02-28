#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GEUL 동사 트리 추출기
559개 최상위 동사 각각의 hyponym 트리를 JSON으로 저장
PostgreSQL WordNet DB 사용

Usage:
    python3 geulso/wordnet/verbtrees.py
    
Output:
    geulso/wordnet/verbtrees/001_abandon.v.02.json
    ...
"""

import json
import os
from pathlib import Path
import psycopg2

DB_CONFIG = {
    'host': 'localhost',
    'database': 'geuldev',
    'user': 'postgres',
    'password': 'test1224!'
}

SCRIPT_DIR = Path(__file__).parent
VERB559_PATH = SCRIPT_DIR / "verb559.json"
OUTPUT_DIR = SCRIPT_DIR / "verbtrees"


def get_definition(cursor, synset_id: str) -> str:
    """synset의 definition 조회"""
    cursor.execute(
        "SELECT definition FROM wordnet_synsets WHERE synset_id = %s",
        (synset_id,)
    )
    row = cursor.fetchone()
    return row[0] if row else ""


def get_hyponyms(cursor, synset_id: str) -> list:
    """synset의 직접 hyponym들 조회"""
    cursor.execute("""
        SELECT from_synset 
        FROM wordnet_synset_relations 
        WHERE to_synset = %s AND relation_type = 'hypernym'
        ORDER BY from_synset
    """, (synset_id,))
    return [row[0] for row in cursor.fetchall()]


def build_tree(cursor, synset_id: str, depth: int = 0, visited: set = None) -> dict:
    """hyponym 트리를 재귀적으로 구축"""
    if visited is None:
        visited = set()
    
    if synset_id in visited:
        return None
    visited.add(synset_id)
    
    node = {
        "id": synset_id,
        "definition": get_definition(cursor, synset_id),
        "depth": depth,
        "children": []
    }
    
    for hypo_id in get_hyponyms(cursor, synset_id):
        child = build_tree(cursor, hypo_id, depth + 1, visited.copy())
        if child:
            node["children"].append(child)
    
    return node


def main():
    if not VERB559_PATH.exists():
        print(f"ERROR: {VERB559_PATH} not found")
        return
    
    with open(VERB559_PATH, "r", encoding="utf-8") as f:
        verb559 = json.load(f)
    
    roots = verb559["roots"]
    
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        for idx, root_info in enumerate(roots, 1):
            synset_id = root_info["synset_id"]
            
            try:
                tree = build_tree(cursor, synset_id)
                
                filename = f"{idx:03d}_{synset_id}.json"
                filepath = OUTPUT_DIR / filename
                
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(tree, f, indent=2, ensure_ascii=False)
                
                print(filename)
                
            except Exception as e:
                print(f"{synset_id} ERROR: {e}")
    
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()