#!/usr/bin/env python3
"""
Stage 3: 48비트 속성 비트 할당 최적화

Stage 1(속성 통계) + Stage 2(DAG)를 기반으로
48비트에 속성을 배치하고 충돌률을 측정한다.

사용법:
    python stage3_allocate.py --entity-type 0
"""

import argparse
import math
import os
from collections import defaultdict

import psycopg2

def get_work_conn():
    return psycopg2.connect(
        host="localhost", port=5432, dbname="geul_work",
        user="geul_writer", password=os.environ["GEUL_WRITE_PW"]
    )

TOTAL_BITS = 48
MIN_BITS = 2
MAX_BITS = 12

# ─── DAG 위상 정렬 ───

def topological_sort(properties: list, dag_edges: list, prop_stats: dict) -> list:
    """
    DAG 위상 정렬 + 독립 노드는 엔트로피 내림차순.
    보편 속성(카디널리티 낮고 커버리지 높은)은 상위 우선.
    """
    children = defaultdict(set)
    parents = defaultdict(set)
    
    for edge in dag_edges:
        children[edge['parent']].add(edge['child'])
        parents[edge['child']].add(edge['parent'])
    
    # 독립 노드 (부모 없는 것)
    independent = [p for p in properties if p not in parents]
    dependent = [p for p in properties if p in parents]
    
    # 독립 노드: 보편성(커버리지 높고 카디널리티 낮은) 우선, 그 다음 엔트로피 순
    def independent_priority(prop):
        s = prop_stats[prop]
        universality = s['coverage'] / max(math.log2(s['cardinality'] + 1), 1)
        return (-universality, -s['entropy'])
    
    independent.sort(key=independent_priority)
    
    # 위상 정렬
    result = []
    placed = set()
    
    for p in independent:
        result.append(p)
        placed.add(p)
        # 이 노드의 자식들을 재귀적으로 배치
        queue = sorted(children.get(p, []),
                      key=lambda x: -prop_stats[x]['entropy'])
        for child in queue:
            if child not in placed and parents[child].issubset(placed):
                result.append(child)
                placed.add(child)
    
    # 누락된 것 추가
    for p in properties:
        if p not in placed:
            result.append(p)
    
    return result

# ─── 비트 할당 ───

def allocate_bits(sorted_props: list, prop_stats: dict, dag_edges: list) -> list:
    """탐욕적 비트 할당"""
    parent_map = {}
    for edge in dag_edges:
        parent_map[edge['child']] = edge['parent']
    
    budget = TOTAL_BITS
    allocation = []
    
    for prop in sorted_props:
        if budget <= 0:
            break
        
        stats = prop_stats[prop]
        
        if prop in parent_map:
            # 종속 필드: 부모 값별 최대 카디널리티 기준
            # TODO: 실제 데이터에서 부모 값별 카디널리티 계산
            bits = min(math.ceil(math.log2(max(stats['cardinality'], 2))), MAX_BITS)
        else:
            # 독립 필드
            bits = min(math.ceil(math.log2(max(stats['cardinality'], 2))), MAX_BITS)
        
        bits = max(bits, MIN_BITS)
        bits = min(bits, budget)
        
        allocation.append({
            'property': prop,
            'bits': bits,
            'offset': TOTAL_BITS - budget,
            'parent': parent_map.get(prop),
            'cardinality': stats['cardinality'],
            'coverage': stats['coverage'],
            'entropy': stats['entropy'],
            'quantization_loss': max(0, math.log2(max(stats['cardinality'], 1)) - bits)
        })
        
        budget -= bits
    
    if budget > 0:
        # 잔여: Reserved로
        allocation.append({
            'property': '_reserved',
            'bits': budget,
            'offset': TOTAL_BITS - budget,
            'parent': None,
            'cardinality': 0,
            'coverage': 0,
            'entropy': 0,
            'quantization_loss': 0
        })
    
    return allocation

# ─── 보고서 ───

def print_allocation(allocation: list, entity_type: int):
    print(f"\n{'='*70}")
    print(f"Entity Type {entity_type}: 48-bit Allocation")
    print(f"{'='*70}")
    print(f"{'Property':<15} {'Offset':>6} {'Bits':>4} {'Card':>8} {'Covr':>6} {'Ent':>6} {'QLoss':>6} {'Parent':<10}")
    print(f"{'-'*70}")
    
    total_used = 0
    for a in allocation:
        parent = a['parent'] or '-'
        print(f"{a['property']:<15} {a['offset']:>6} {a['bits']:>4} "
              f"{a['cardinality']:>8} {a['coverage']:>5.1%} "
              f"{a['entropy']:>5.2f} {a['quantization_loss']:>5.2f} {parent:<10}")
        total_used += a['bits']
    
    print(f"{'-'*70}")
    print(f"Total: {total_used}/48 bits used")

def save_allocation(work_conn, entity_type: int, allocation: list):
    with work_conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS bit_allocation (
                entity_type  INTEGER NOT NULL,
                property_id  TEXT NOT NULL,
                bit_offset   INTEGER NOT NULL,
                bit_width    INTEGER NOT NULL,
                parent_prop  TEXT,
                cardinality  INTEGER,
                coverage     REAL,
                entropy      REAL,
                quant_loss   REAL,
                PRIMARY KEY (entity_type, property_id)
            )
        """)
        cur.execute(
            "DELETE FROM bit_allocation WHERE entity_type = %s",
            (entity_type,)
        )
        for a in allocation:
            cur.execute("""
                INSERT INTO bit_allocation VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                entity_type, a['property'], a['offset'], a['bits'],
                a['parent'], a['cardinality'], a['coverage'],
                a['entropy'], a['quantization_loss']
            ))
    work_conn.commit()

# ─── 메인 ───

def main():
    parser = argparse.ArgumentParser(description="Stage 3: 비트 할당")
    parser.add_argument("--entity-type", type=int, required=True)
    args = parser.parse_args()
    
    work_conn = get_work_conn()
    
    # Stage 1 결과 로드
    with work_conn.cursor() as cur:
        cur.execute("""
            SELECT property_id, coverage, cardinality, entropy
            FROM property_stats
            WHERE entity_type = %s AND coverage >= 0.10
            ORDER BY coverage DESC
        """, (args.entity_type,))
        rows = cur.fetchall()
    
    prop_stats = {}
    properties = []
    for pid, cov, card, ent in rows:
        prop_stats[pid] = {
            'coverage': cov, 'cardinality': card, 'entropy': ent
        }
        properties.append(pid)
    
    # Stage 2 결과 로드
    with work_conn.cursor() as cur:
        cur.execute("""
            SELECT parent_prop, child_prop, mutual_info
            FROM dependency_dag
            WHERE entity_type = %s
        """, (args.entity_type,))
        dag_edges = [
            {'parent': p, 'child': c, 'mi': mi}
            for p, c, mi in cur.fetchall()
        ]
    
    # 위상 정렬
    sorted_props = topological_sort(properties, dag_edges, prop_stats)
    
    # 비트 할당
    allocation = allocate_bits(sorted_props, prop_stats, dag_edges)
    
    # 출력 및 저장
    print_allocation(allocation, args.entity_type)
    save_allocation(work_conn, args.entity_type, allocation)
    
    work_conn.close()

if __name__ == "__main__":
    main()
