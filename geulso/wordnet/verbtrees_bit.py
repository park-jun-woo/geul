#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GEUL 동사 비트 할당기
559개 최상위 동사 트리를 DFS Pre-order로 순회하며 16비트 코드 할당

- sub_primitive별로 코드 카운터 공유
- 중복 동사는 먼저 할당된 코드 유지

Usage:
    python3 geulso/wordnet/verbtrees_bit.py

Input:
    geulso/wordnet/verbtrees/*.json (559개 트리)
    geulso/wordnet/verb559.json (root별 primitive 정보)
    geulso/wordnet/sub_primitive_map.json (primitive→code 매핑)

Output:
    geulso/wordnet/verb_bits.json
"""

import json
from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = Path(__file__).parent
VERBTREES_DIR = SCRIPT_DIR / "verbtrees"
VERB559_PATH = SCRIPT_DIR / "json" / "verb559.json"
SUB_PRIMITIVE_MAP_PATH = SCRIPT_DIR / "json" / "primitive-map.json"
OUTPUT_PATH = SCRIPT_DIR / "json" / "verb_bits.json"


def load_primitive_info():
    """verb559.json에서 root별 primitive 정보 로드"""
    with open(VERB559_PATH, "r", encoding="utf-8") as f:
        verb559 = json.load(f)
    
    info = {}
    for root in verb559["roots"]:
        synset_id = root["synset_id"]
        prim = root.get("primitive", "")
        sub = root.get("sub_primitive", "")
        info[synset_id] = f"{prim}-{sub}"
    return info


def load_sub_primitive_map():
    """sub_primitive_map.json 로드"""
    with open(SUB_PRIMITIVE_MAP_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def collect_dfs_preorder(node, result_list):
    """DFS Pre-order 순회하여 노드 수집 (중복 체크 없이)"""
    result_list.append({
        "id": node["id"],
        "definition": node.get("definition", "")
    })
    for child in node.get("children", []):
        collect_dfs_preorder(child, result_list)


def main():
    # 1. 매핑 정보 로드
    primitive_info = load_primitive_info()
    sub_primitive_map = load_sub_primitive_map()
    
    # 2. sub_primitive별 코드 카운터
    code_counters = defaultdict(int)
    
    # 3. 전역 할당 추적: synset_id -> 할당 정보
    global_assigned = {}
    
    # 4. 559개 트리 파일 순회 (파일명 순)
    tree_files = sorted(VERBTREES_DIR.glob("*.json"))
    
    for tree_file in tree_files:
        with open(tree_file, "r", encoding="utf-8") as f:
            tree = json.load(f)
        
        root_id = tree["id"]
        
        # primitive 정보 가져오기
        if root_id not in primitive_info:
            print(f"WARN: {root_id} not in verb559.json, skipping")
            continue
        
        primitive = primitive_info[root_id]
        
        # primitive_code 가져오기
        if primitive not in sub_primitive_map:
            print(f"WARN: {primitive} not in sub_primitive_map, skipping")
            continue
        
        primitive_code = sub_primitive_map[primitive]
        primitive_bits = len(primitive_code)
        code_bits = 16 - primitive_bits
        
        # DFS Pre-order로 노드 수집
        tree_verbs = []
        collect_dfs_preorder(tree, tree_verbs)
        
        # 코드 할당
        new_count = 0
        skip_count = 0
        
        for verb in tree_verbs:
            synset_id = verb["id"]
            
            # 이미 할당됐으면 스킵
            if synset_id in global_assigned:
                skip_count += 1
                continue
            
            # 새 코드 할당
            code_num = code_counters[primitive]
            code = format(code_num, f'0{code_bits}b')
            
            global_assigned[synset_id] = {
                "id": synset_id,
                "definition": verb["definition"],
                "root": root_id,
                "primitive": primitive,
                "primitive_code": primitive_code,
                "code": code
            }
            
            code_counters[primitive] += 1
            new_count += 1
        
        print(f"{tree_file.name}: +{new_count}, skip {skip_count}")
    
    # 5. 결과 정렬 (primitive_code + code 순)
    all_verbs = sorted(
        global_assigned.values(),
        key=lambda v: v["primitive_code"] + v["code"]
    )
    
    # 6. 결과 저장
    output = {
        "description": "GEUL 동사 16비트 코드 할당 (DFS Pre-order)",
        "total_verbs": len(all_verbs),
        "sub_primitive_counts": dict(code_counters),
        "verbs": all_verbs
    }
    
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n완료: {OUTPUT_PATH.name}")
    print(f"총 동사: {len(all_verbs)}")


if __name__ == "__main__":
    main()