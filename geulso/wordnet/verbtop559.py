#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WordNet 동사 최상위 노드(루트) 추출기
hypernym이 없는 동사 synset들을 JSON으로 저장

Usage:
    python3 verbtop559.py <output_path>
    
Example:
    python3 geulso/wordnet/verbtop559.py geulso/wordnet/verbtop559.json
"""

import sys
import json
import psycopg2
from typing import Dict, List

DB_CONFIG = {
    'host': 'localhost',
    'database': 'geuldev',
    'user': 'postgres',
    'password': 'test1224!'
}


def get_root_verbs() -> List[Dict]:
    """
    hypernym이 없는 동사 synset(루트 노드)들을 조회
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # 방법 1: verb_hypernym_ltree 테이블 사용 (이미 구축된 경우)
        cursor.execute("""
            SELECT synset_id, definition, tree_path
            FROM verb_hypernym_ltree
            WHERE depth = 1
            ORDER BY synset_id
        """)
        
        roots = []
        for synset_id, definition, tree_path in cursor.fetchall():
            # 하위 노드 개수 조회
            cursor.execute("""
                SELECT COUNT(*) 
                FROM verb_hypernym_ltree 
                WHERE tree_path <@ %s AND synset_id != %s
            """, (tree_path, synset_id))
            descendant_count = cursor.fetchone()[0]
            
            roots.append({
                'synset_id': synset_id,
                'definition': definition,
                'descendant_count': descendant_count,
                'primitive': None  # 수작업으로 채울 필드
            })
        
        return roots
        
    finally:
        cursor.close()
        conn.close()


def save_to_json(roots: List[Dict], output_path: str):
    """
    루트 노드들을 JSON 파일로 저장
    """
    output = {
        'description': 'WordNet 동사 최상위 노드 (hypernym 없는 synset)',
        'total_count': len(roots),
        'primitives': {
            'BE': '상태 유지 (exist, know, love)',
            'CHANGE': '상태 변화 (die, break, become)',
            'CAUSE': '사역 (kill, make, force)',
            'MOVE': '이동 (go, run, travel)',
            'TRANSFER': '전달 (give, send, tell)',
            'PERCEIVE': '인지 (see, hear, notice)',
            'COMMUNICATE': '소통 (say, speak, write)',
            'FEEL': '감정 (fear, love, enjoy)'
        },
        'roots': roots
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"저장 완료: {output_path}")
    print(f"총 {len(roots)}개 루트 노드")


def print_summary(roots: List[Dict]):
    """
    요약 통계 출력
    """
    print("\n========== 루트 노드 요약 ==========")
    print(f"총 개수: {len(roots)}개")
    
    # 하위 노드 개수별 분포
    ranges = [
        (0, 0, "하위 없음"),
        (1, 10, "1-10개"),
        (11, 50, "11-50개"),
        (51, 100, "51-100개"),
        (101, 500, "101-500개"),
        (501, 10000, "500개 초과")
    ]
    
    print("\n하위 노드 개수별 분포:")
    for min_val, max_val, label in ranges:
        count = sum(1 for r in roots if min_val <= r['descendant_count'] <= max_val)
        if count > 0:
            print(f"  {label}: {count}개")
    
    # 하위 노드가 가장 많은 루트 Top 10
    print("\n하위 노드 최다 루트 Top 10:")
    sorted_roots = sorted(roots, key=lambda x: x['descendant_count'], reverse=True)
    for i, r in enumerate(sorted_roots[:10], 1):
        print(f"  {i}. {r['synset_id']} ({r['descendant_count']}개): {r['definition'][:50]}...")
    
    print("====================================\n")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 verbtop559.py <output_path>")
        print("Example: python3 geulso/wordnet/verbtop559.py geulso/wordnet/verbtop559.json")
        sys.exit(1)
    
    output_path = sys.argv[1]
    
    print("동사 루트 노드 추출 중...")
    roots = get_root_verbs()
    
    print_summary(roots)
    save_to_json(roots, output_path)


if __name__ == "__main__":
    main()