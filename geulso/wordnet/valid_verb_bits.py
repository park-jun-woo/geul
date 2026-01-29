#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verb_bits.json 유효성 검증기

검증 항목:
1. primitive_code + code = 16비트
2. synset_id 중복 없음
3. full_code (primitive_code + code) 중복 없음
4. code가 해당 primitive의 가용 비트 내인지

Usage:
    python3 geulso/wordnet/valid_verb_bits.py
"""

import json
from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = Path(__file__).parent
VERB_BITS_PATH = SCRIPT_DIR / "verb_bits.json"
SUB_PRIMITIVE_MAP_PATH = SCRIPT_DIR / "primitive-map.json"


def main():
    # 1. 파일 로드
    with open(VERB_BITS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    with open(SUB_PRIMITIVE_MAP_PATH, "r", encoding="utf-8") as f:
        sub_primitive_map = json.load(f)
    
    verbs = data["verbs"]
    
    # 2. 검증용 추적
    errors = []
    warnings = []
    
    seen_ids = {}  # synset_id -> index
    seen_full_codes = {}  # full_code -> synset_id
    primitive_code_counts = defaultdict(int)
    
    # 3. 검증 수행
    for idx, verb in enumerate(verbs):
        synset_id = verb["id"]
        primitive = verb["primitive"]
        primitive_code = verb["primitive_code"]
        code = verb["code"]
        full_code = primitive_code + code
        
        # 검증 1: 16비트 체크
        if len(full_code) != 16:
            errors.append(f"[{idx}] {synset_id}: 16비트 아님 ({len(full_code)}비트) - {full_code}")
        
        # 검증 2: synset_id 중복 체크
        if synset_id in seen_ids:
            errors.append(f"[{idx}] {synset_id}: ID 중복 (first at [{seen_ids[synset_id]}])")
        else:
            seen_ids[synset_id] = idx
        
        # 검증 3: full_code 중복 체크
        if full_code in seen_full_codes:
            errors.append(f"[{idx}] {synset_id}: 코드 중복 '{full_code}' (already assigned to {seen_full_codes[full_code]})")
        else:
            seen_full_codes[full_code] = synset_id
        
        # 검증 4: primitive_code 매핑 확인
        if primitive in sub_primitive_map:
            expected_primitive_code = sub_primitive_map[primitive]
            if primitive_code != expected_primitive_code:
                errors.append(f"[{idx}] {synset_id}: primitive_code 불일치 - got '{primitive_code}', expected '{expected_primitive_code}'")
        else:
            warnings.append(f"[{idx}] {synset_id}: primitive '{primitive}' not in sub_primitive_map")
        
        # 검증 5: code 비트 범위 체크
        expected_code_bits = 16 - len(primitive_code)
        if len(code) != expected_code_bits:
            errors.append(f"[{idx}] {synset_id}: code 비트 불일치 - got {len(code)}비트, expected {expected_code_bits}비트")
        
        # 검증 6: code가 이진수인지
        if not all(c in '01' for c in full_code):
            errors.append(f"[{idx}] {synset_id}: 이진수 아님 - {full_code}")
        
        primitive_code_counts[primitive_code] += 1
    
    # 4. 결과 출력
    print("=" * 60)
    print("verb_bits.json 검증 결과")
    print("=" * 60)
    print(f"총 동사 수: {len(verbs)}")
    print(f"고유 ID 수: {len(seen_ids)}")
    print(f"고유 코드 수: {len(seen_full_codes)}")
    print()
    
    if errors:
        print(f"❌ 오류: {len(errors)}개")
        for err in errors[:20]:  # 최대 20개만 출력
            print(f"  {err}")
        if len(errors) > 20:
            print(f"  ... 외 {len(errors) - 20}개")
    else:
        print("✓ 오류 없음")
    
    print()
    
    if warnings:
        print(f"⚠ 경고: {len(warnings)}개")
        for warn in warnings[:10]:
            print(f"  {warn}")
        if len(warnings) > 10:
            print(f"  ... 외 {len(warnings) - 10}개")
    else:
        print("✓ 경고 없음")
    
    print()
    print("primitive_code별 동사 수:")
    for pc in sorted(primitive_code_counts.keys()):
        count = primitive_code_counts[pc]
        bits = 16 - len(pc)
        max_capacity = 2 ** bits
        usage = count / max_capacity * 100
        print(f"  {pc} ({len(pc)}b): {count:>5} / {max_capacity} ({usage:.1f}%)")
    
    print()
    print("=" * 60)
    if errors:
        print("❌ 검증 실패")
        return 1
    else:
        print("✓ 검증 통과")
        return 0


if __name__ == "__main__":
    exit(main())