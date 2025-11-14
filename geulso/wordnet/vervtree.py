#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
from psycopg2.extras import execute_batch
from collections import defaultdict, deque
from typing import Dict, Set, List, Tuple
from tqdm import tqdm

DB_CONFIG = {
    'host': 'localhost',
    'database': 'geuldev',
    'user': 'postgres',
    'password': 'test1224!'
}

class VerbHypernymTreeBuilder:
    """
    워드넷의 동사 synset들을 상위어(hypernym) 관계로 ltree 구조를 만드는 클래스
    """
    def __init__(self, db_config: Dict[str, str]):
        self.conn = psycopg2.connect(**db_config)
        self.cursor = self.conn.cursor()
        
        # 그래프 구조 저장
        self.verb_synsets = {}  # synset_id -> definition
        self.children_map = defaultdict(list)  # parent_id -> [child_ids]
        self.parent_map = defaultdict(list)  # child_id -> [parent_ids]
        self.root_nodes = set()
        
        # ltree 경로 저장
        self.synset_paths = {}  # synset_id -> ltree_path
        
    def synset_to_label(self, synset_id: str) -> str:
        """synset_id를 ltree 레이블로 변환
        ltree 규칙:
        - 알파벳, 숫자, 언더스코어만 허용
        - 숫자로 시작 불가
        - 최대 256자
        """
        # . 와 - 를 _ 로 변환
        label = synset_id.replace('.', '_').replace('-', '_')
        
        # 숫자로 시작하면 앞에 'v' 추가
        if label and label[0].isdigit():
            label = 'v' + label
        
        # 알파벳, 숫자, 언더스코어가 아닌 문자 제거
        label = ''.join(c for c in label if c.isalnum() or c == '_')
        
        # 빈 문자열이면 기본값
        if not label:
            label = 'unknown'
        
        # 최대 길이 제한
        if len(label) > 256:
            label = label[:256]
        
        return label
    
    def load_verb_data(self):
        """동사 synset과 hypernym 관계를 메모리로 로드"""
        print("1단계: 동사 synset 데이터 로딩 중...")
        
        # 모든 동사 synset 로드
        self.cursor.execute("""
            SELECT synset_id, definition 
            FROM wordnet_synsets 
            WHERE pos = 'v'
        """)
        
        for synset_id, definition in self.cursor.fetchall():
            self.verb_synsets[synset_id] = definition
        
        print(f"   -> {len(self.verb_synsets):,}개의 동사 synset 로드 완료")
        
        # hypernym 관계 로드 (동사끼리만)
        print("2단계: hypernym 관계 로딩 중...")
        self.cursor.execute("""
            SELECT r.from_synset, r.to_synset
            FROM wordnet_synset_relations r
            JOIN wordnet_synsets s1 ON r.from_synset = s1.synset_id
            JOIN wordnet_synsets s2 ON r.to_synset = s2.synset_id
            WHERE r.relation_type = 'hypernym'
              AND s1.pos = 'v'
              AND s2.pos = 'v'
        """)
        
        relation_count = 0
        for child_id, parent_id in self.cursor.fetchall():
            self.children_map[parent_id].append(child_id)
            self.parent_map[child_id].append(parent_id)
            relation_count += 1
        
        print(f"   -> {relation_count:,}개의 hypernym 관계 로드 완료")
        
    def find_root_nodes(self):
        """상위어가 없는 루트 노드들을 찾음"""
        print("3단계: 루트 노드 찾기...")
        
        for synset_id in self.verb_synsets.keys():
            if synset_id not in self.parent_map:
                self.root_nodes.add(synset_id)
        
        print(f"   -> {len(self.root_nodes):,}개의 루트 노드 발견")
        
        # 루트 노드 샘플 출력
        if self.root_nodes:
            print("   루트 노드 샘플 (최대 5개):")
            for i, root_id in enumerate(list(self.root_nodes)[:5]):
                print(f"      - {root_id}: {self.verb_synsets[root_id][:50]}...")
    
    def build_tree_paths_bfs(self):
        """BFS로 트리 경로를 구축 (순환 참조 방지)"""
        print("4단계: ltree 경로 구축 중...")
        
        visited = set()
        queue = deque()
        
        # 루트 노드들을 시작점으로 추가
        for root_id in self.root_nodes:
            label = self.synset_to_label(root_id)
            self.synset_paths[root_id] = label
            queue.append((root_id, label, 0))  # (synset_id, path, depth)
            visited.add(root_id)
        
        processed = 0
        skipped_cycles = 0
        multiple_paths = defaultdict(list)  # 여러 경로를 가진 노드 추적
        
        with tqdm(total=len(self.verb_synsets), desc="   경로 생성") as pbar:
            while queue:
                current_id, current_path, depth = queue.popleft()
                processed += 1
                pbar.update(1)
                
                # 자식 노드 처리
                for child_id in self.children_map.get(current_id, []):
                    child_label = self.synset_to_label(child_id)
                    new_path = f"{current_path}.{child_label}"
                    
                    if child_id in visited:
                        # 이미 방문했으면 순환 참조이거나 다중 경로
                        if child_id in self.synset_paths:
                            multiple_paths[child_id].append(new_path)
                        skipped_cycles += 1
                        continue
                    
                    self.synset_paths[child_id] = new_path
                    visited.add(child_id)
                    queue.append((child_id, new_path, depth + 1))
        
        print(f"   -> {processed:,}개 노드 처리 완료")
        print(f"   -> {skipped_cycles:,}개 순환/중복 참조 건너뜀")
        
        # 경로가 없는 노드 처리 (고립된 노드)
        orphaned = set(self.verb_synsets.keys()) - set(self.synset_paths.keys())
        if orphaned:
            print(f"   -> {len(orphaned):,}개 고립 노드 발견, 독립 경로 생성...")
            for orphan_id in orphaned:
                label = self.synset_to_label(orphan_id)
                self.synset_paths[orphan_id] = label
        
        # 다중 경로 정보 출력
        if multiple_paths:
            print(f"   -> {len(multiple_paths):,}개 노드가 여러 부모를 가짐 (첫 번째 경로 사용)")
    
    def insert_to_database(self):
        """구축된 트리를 데이터베이스에 삽입"""
        print("5단계: 데이터베이스 삽입 중...")
        
        # 기존 데이터 삭제
        self.cursor.execute("TRUNCATE TABLE verb_hypernym_ltree")
        self.conn.commit()
        
        # 배치 삽입 준비
        batch = []
        for synset_id, path in tqdm(self.synset_paths.items(), desc="   삽입 준비"):
            definition = self.verb_synsets.get(synset_id, '')
            depth = path.count('.') + 1  # ltree 깊이 계산
            batch.append((synset_id, definition, path, depth))
        
        # 배치 삽입 실행
        print(f"   -> {len(batch):,}개 레코드 삽입 중...")
        execute_batch(self.cursor, """
            INSERT INTO verb_hypernym_ltree (synset_id, definition, tree_path, depth)
            VALUES (%s, %s, %s, %s)
        """, batch, page_size=1000)
        
        self.conn.commit()
        print("   -> 삽입 완료")
    
    def print_statistics(self):
        """통계 정보 출력"""
        print("\n========== 구축 완료 ==========")
        
        # 전체 노드 수
        self.cursor.execute("SELECT COUNT(*) FROM verb_hypernym_ltree")
        total = self.cursor.fetchone()[0]
        print(f"총 동사 노드: {total:,}개")
        
        # 깊이별 분포
        self.cursor.execute("""
            SELECT depth, COUNT(*) as cnt
            FROM verb_hypernym_ltree
            GROUP BY depth
            ORDER BY depth
        """)
        print("\n깊이별 분포:")
        for depth, count in self.cursor.fetchall():
            print(f"   레벨 {depth}: {count:,}개")
        
        # 루트 노드 수
        self.cursor.execute("SELECT COUNT(*) FROM verb_hypernym_ltree WHERE depth = 1")
        roots = self.cursor.fetchone()[0]
        print(f"\n루트 노드: {roots:,}개")
        
        # 최대 깊이
        self.cursor.execute("SELECT MAX(depth) FROM verb_hypernym_ltree")
        max_depth = self.cursor.fetchone()[0]
        print(f"최대 깊이: {max_depth}")
        
        print("==============================\n")
    
    def show_sample_queries(self):
        """샘플 쿼리 실행 및 결과 출력"""
        print("========== 샘플 쿼리 ==========")
        
        # 1. 특정 동사의 하위어 찾기
        print("\n1) 'run.v.01'의 모든 하위어 (직접/간접):")
        self.cursor.execute("""
            SELECT synset_id, definition, depth
            FROM verb_hypernym_ltree
            WHERE tree_path <@ (
                SELECT tree_path FROM verb_hypernym_ltree WHERE synset_id = 'run.v.01'
            )
            AND synset_id != 'run.v.01'
            ORDER BY depth, synset_id
            LIMIT 10
        """)
        for synset_id, definition, depth in self.cursor.fetchall():
            print(f"   [{depth}] {synset_id}: {definition[:60]}...")
        
        # 2. 특정 동사의 상위어 찾기
        print("\n2) 'sprint.v.01'의 모든 상위어 (경로):")
        self.cursor.execute("""
            SELECT synset_id, definition, depth
            FROM verb_hypernym_ltree
            WHERE tree_path @> (
                SELECT tree_path FROM verb_hypernym_ltree WHERE synset_id = 'sprint.v.01'
            )
            ORDER BY depth
        """)
        for synset_id, definition, depth in self.cursor.fetchall():
            print(f"   [{depth}] {synset_id}: {definition[:60]}...")
        
        print("\n==============================")
    
    def close(self):
        self.cursor.close()
        self.conn.close()


def main():
    import time
    
    builder = VerbHypernymTreeBuilder(DB_CONFIG)
    
    try:
        start_time = time.time()
        
        builder.load_verb_data()
        builder.find_root_nodes()
        builder.build_tree_paths_bfs()
        builder.insert_to_database()
        builder.print_statistics()
        builder.show_sample_queries()
        
        elapsed = time.time() - start_time
        print(f"\n전체 소요 시간: {elapsed:.1f}초")
        
    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()
        builder.conn.rollback()
    finally:
        builder.close()


if __name__ == "__main__":
    main()