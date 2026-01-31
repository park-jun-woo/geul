#!/usr/bin/env python3
"""
Stage 2: 속성 간 계층 의존성 탐지

Stage 1 결과를 기반으로 조건부 엔트로피를 계산하여
속성 간 종속 관계 DAG를 생성한다.

사용법:
    python stage2_dependency.py --entity-type 0 --top-k 15
"""

import argparse
import math
import os
from collections import Counter, defaultdict
from itertools import combinations

import psycopg2

def get_wikidata_conn():
    return psycopg2.connect(
        host="localhost", port=5432, dbname="wikidata",
        user="geul_reader", password=os.environ["GEUL_READ_PW"]
    )

def get_work_conn():
    return psycopg2.connect(
        host="localhost", port=5432, dbname="geul_work",
        user="geul_writer", password=os.environ["GEUL_WRITE_PW"]
    )

# ─── 조건부 엔트로피 ───

def conditional_entropy(values_a: list, values_b: list) -> float:
    """H(B|A): A를 알 때 B의 불확실성"""
    assert len(values_a) == len(values_b)
    n = len(values_a)
    if n == 0:
        return 0.0
    
    # A 값별 B 분포
    groups = defaultdict(list)
    for a, b in zip(values_a, values_b):
        groups[a].append(b)
    
    h = 0.0
    for a_val, b_vals in groups.items():
        p_a = len(b_vals) / n
        counter = Counter(b_vals)
        h_b_given_a = 0.0
        for count in counter.values():
            p = count / len(b_vals)
            if p > 0:
                h_b_given_a -= p * math.log2(p)
        h += p_a * h_b_given_a
    
    return h

def entropy(values: list) -> float:
    counter = Counter(values)
    total = len(values)
    h = 0.0
    for count in counter.values():
        p = count / total
        if p > 0:
            h -= p * math.log2(p)
    return h

def mutual_information(values_a: list, values_b: list) -> float:
    """I(A;B) = H(B) - H(B|A)"""
    return entropy(values_b) - conditional_entropy(values_a, values_b)

# ─── DAG 사이클 제거 ───

def remove_cycles(edges: list) -> list:
    """약한 간선부터 제거하여 DAG 보장"""
    edges_sorted = sorted(edges, key=lambda e: e['mi'], reverse=True)
    
    dag = []
    visited = set()
    
    def has_path(graph, start, end, seen=None):
        if seen is None:
            seen = set()
        if start == end:
            return True
        seen.add(start)
        for e in graph:
            if e['parent'] == start and e['child'] not in seen:
                if has_path(graph, e['child'], end, seen):
                    return True
        return False
    
    for edge in edges_sorted:
        # 이 간선을 추가했을 때 사이클이 생기는지 확인
        if not has_path(dag, edge['child'], edge['parent']):
            dag.append(edge)
    
    return dag

# ─── 메인 ───

def analyze_dependencies(wiki_conn, work_conn, entity_type_code: int, top_k: int):
    """
    상위 top_k 속성 간 종속 관계를 분석한다.
    
    TODO: wikidata DB 스키마에 맞게 쿼리 수정
    """
    # Stage 1 결과에서 상위 속성 가져오기
    with work_conn.cursor() as cur:
        cur.execute("""
            SELECT property_id, entropy 
            FROM property_stats 
            WHERE entity_type = %s 
            ORDER BY coverage DESC, entropy DESC 
            LIMIT %s
        """, (entity_type_code, top_k))
        properties = [(row[0], row[1]) for row in cur.fetchall()]
    
    if len(properties) < 2:
        print("Not enough properties to analyze")
        return
    
    prop_ids = [p[0] for p in properties]
    prop_entropy = {p[0]: p[1] for p in properties}
    
    print(f"Analyzing {len(prop_ids)} properties: {prop_ids}")
    
    # TODO: wikidata에서 해당 개체들의 속성값 쌍을 가져오는 쿼리
    # 실제 스키마에 맞게 수정 필요
    # 아래는 개념적 pseudocode
    
    # entity_values[entity_id][property_id] = value
    # ... DB에서 로드 ...
    
    # 모든 속성 쌍에 대해 MI 계산
    edges = []
    for prop_a, prop_b in combinations(prop_ids, 2):
        # TODO: 실제 값 로드 후 계산
        # values_a = [entity_values[eid].get(prop_a) for eid in entities]
        # values_b = [entity_values[eid].get(prop_b) for eid in entities]
        
        # mi = mutual_information(values_a, values_b)
        # h_b_given_a = conditional_entropy(values_a, values_b)
        # h_a_given_b = conditional_entropy(values_b, values_a)
        
        # threshold = 0.3 * min(prop_entropy[prop_a], prop_entropy[prop_b])
        # if mi > threshold:
        #     if h_b_given_a < h_a_given_b:
        #         edges.append({'parent': prop_a, 'child': prop_b, 'mi': mi})
        #     else:
        #         edges.append({'parent': prop_b, 'child': prop_a, 'mi': mi})
        pass
    
    dag = remove_cycles(edges)
    
    # 결과 저장
    with work_conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS dependency_dag (
                entity_type INTEGER NOT NULL,
                parent_prop TEXT NOT NULL,
                child_prop TEXT NOT NULL,
                mutual_info REAL NOT NULL,
                PRIMARY KEY (entity_type, parent_prop, child_prop)
            )
        """)
        cur.execute(
            "DELETE FROM dependency_dag WHERE entity_type = %s",
            (entity_type_code,)
        )
        for e in dag:
            cur.execute("""
                INSERT INTO dependency_dag VALUES (%s, %s, %s, %s)
            """, (entity_type_code, e['parent'], e['child'], e['mi']))
    work_conn.commit()
    
    # DAG 출력
    print(f"\nDependency DAG ({len(dag)} edges):")
    for e in dag:
        print(f"  {e['parent']} → {e['child']}  (MI={e['mi']:.3f})")

def main():
    parser = argparse.ArgumentParser(description="Stage 2: 의존성 탐지")
    parser.add_argument("--entity-type", type=int, required=True)
    parser.add_argument("--top-k", type=int, default=15)
    args = parser.parse_args()
    
    wiki_conn = get_wikidata_conn()
    work_conn = get_work_conn()
    
    analyze_dependencies(wiki_conn, work_conn, args.entity_type, args.top_k)
    
    wiki_conn.close()
    work_conn.close()

if __name__ == "__main__":
    main()
