#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
valid_flat.py - verb559.json의 flat 필드 검증 스크립트

검증 항목:
1. primitive + sub_primitive → flat_map 일치 여부
2. classified/*.json과 sub_primitive 일치 여부
3. 비트 구조 정합성 (prefix + primitive_code + sub_primitive_code)
"""

import json
import os
import sys
from collections import defaultdict

def load_json(filepath):
    """JSON 파일 로드"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def validate_flat_mapping(verb_data, prim_map):
    """flat_map과 실제 flat 필드 일치 검증"""
    print("=" * 60)
    print("1. FLAT_MAP 일치 검증")
    print("=" * 60)
    
    flat_map = prim_map['flat_map']
    errors = []
    success = 0
    
    for root in verb_data['roots']:
        synset_id = root['synset_id']
        prim = root.get('primitive')
        sub_prim = root.get('sub_primitive')
        actual_flat = root.get('flat')
        
        if not prim or not sub_prim:
            errors.append(f"[MISSING] {synset_id}: primitive={prim}, sub_primitive={sub_prim}")
            continue
        
        key = f"{prim}-{sub_prim}"
        expected_flat = flat_map.get(key)
        
        if not expected_flat:
            errors.append(f"[NO_KEY] {synset_id}: key '{key}' not in flat_map")
            continue
        
        if actual_flat != expected_flat:
            errors.append(f"[MISMATCH] {synset_id}: expected={expected_flat}, actual={actual_flat}")
        else:
            success += 1
    
    print(f"✓ 성공: {success}개")
    print(f"✗ 실패: {len(errors)}개")
    
    if errors:
        print("\n오류 목록:")
        for e in errors[:20]:  # 최대 20개만 출력
            print(f"  {e}")
        if len(errors) > 20:
            print(f"  ... 외 {len(errors) - 20}개")
    
    return len(errors) == 0

def validate_sub_primitive_consistency(verb_data, classified_dir):
    """classified/*.json과 sub_primitive 일치 검증"""
    print("\n" + "=" * 60)
    print("2. CLASSIFIED 파일과 SUB_PRIMITIVE 일치 검증")
    print("=" * 60)
    
    # verb559.json에서 synset_id → sub_primitive 맵 생성
    verb_map = {}
    for root in verb_data['roots']:
        verb_map[root['synset_id']] = {
            'primitive': root.get('primitive'),
            'sub_primitive': root.get('sub_primitive')
        }
    
    # classified 폴더의 파일들 검사
    primitive_files = [
        'be.json', 'cause.json', 'change.json', 'communicate.json',
        'feel.json', 'move.json', 'perceive.json', 'social.json',
        'think.json', 'transfer.json'
    ]
    
    errors = []
    total_checked = 0
    
    for filename in primitive_files:
        filepath = os.path.join(classified_dir, filename)
        if not os.path.exists(filepath):
            print(f"[SKIP] {filename} not found")
            continue
        
        try:
            class_data = load_json(filepath)
            expected_prim = class_data.get('primitive')
            
            for root in class_data.get('roots', []):
                synset_id = root['synset_id']
                expected_sub = root.get('sub_primitive')
                total_checked += 1
                
                if synset_id not in verb_map:
                    errors.append(f"[NOT_FOUND] {synset_id} not in verb559.json")
                    continue
                
                actual = verb_map[synset_id]
                
                if actual['primitive'] != expected_prim:
                    errors.append(f"[PRIM] {synset_id}: expected={expected_prim}, actual={actual['primitive']}")
                
                if actual['sub_primitive'] != expected_sub:
                    errors.append(f"[SUB] {synset_id}: expected={expected_sub}, actual={actual['sub_primitive']}")
            
            print(f"✓ {filename}: {len(class_data.get('roots', []))}개 검사")
            
        except Exception as e:
            print(f"[ERROR] {filename}: {e}")
    
    print(f"\n총 검사: {total_checked}개")
    print(f"✓ 성공: {total_checked - len(errors)}개")
    print(f"✗ 실패: {len(errors)}개")
    
    if errors:
        print("\n오류 목록:")
        for e in errors[:20]:
            print(f"  {e}")
        if len(errors) > 20:
            print(f"  ... 외 {len(errors) - 20}개")
    
    return len(errors) == 0

def validate_bit_structure(verb_data, prim_map):
    """비트 구조 정합성 검증"""
    print("\n" + "=" * 60)
    print("3. 비트 구조 정합성 검증")
    print("=" * 60)
    
    prefix = prim_map['prefix']['full_prefix']  # "11000010"
    primitives = prim_map['primitives']
    
    errors = []
    success = 0
    
    for root in verb_data['roots']:
        synset_id = root['synset_id']
        prim = root.get('primitive')
        sub_prim = root.get('sub_primitive')
        flat = root.get('flat')
        
        if not all([prim, sub_prim, flat]):
            continue
        
        # primitive 코드 가져오기
        prim_info = primitives.get(prim)
        if not prim_info:
            errors.append(f"[NO_PRIM] {synset_id}: primitive '{prim}' not in map")
            continue
        
        prim_code = prim_info['code']
        sub_prims = prim_info['sub_primitives']
        
        sub_code = sub_prims.get(sub_prim)
        if not sub_code:
            errors.append(f"[NO_SUB] {synset_id}: sub_primitive '{sub_prim}' not in {prim}")
            continue
        
        # 예상 flat 구성
        expected = prefix + prim_code + sub_code
        
        if flat != expected:
            errors.append(f"[BIT] {synset_id}: expected={expected}, actual={flat}")
            errors.append(f"      prefix={prefix}, prim={prim_code}, sub={sub_code}")
        else:
            success += 1
    
    print(f"✓ 성공: {success}개")
    print(f"✗ 실패: {len(errors)}개")
    
    if errors:
        print("\n오류 목록:")
        for e in errors[:30]:
            print(f"  {e}")
        if len(errors) > 30:
            print(f"  ... 외 {len(errors) - 30}개")
    
    return len(errors) == 0

def print_statistics(verb_data, prim_map):
    """통계 출력"""
    print("\n" + "=" * 60)
    print("4. 통계")
    print("=" * 60)
    
    # primitive별 카운트
    prim_count = defaultdict(int)
    sub_count = defaultdict(lambda: defaultdict(int))
    bit_lengths = defaultdict(int)
    
    for root in verb_data['roots']:
        prim = root.get('primitive', 'UNKNOWN')
        sub = root.get('sub_primitive', 'UNKNOWN')
        flat = root.get('flat', '')
        
        prim_count[prim] += 1
        sub_count[prim][sub] += 1
        bit_lengths[len(flat)] += 1
    
    print("\n[Primitive별 분포]")
    for prim, count in sorted(prim_count.items()):
        print(f"  {prim}: {count}개")
    
    print("\n[비트 길이별 분포]")
    for length, count in sorted(bit_lengths.items()):
        print(f"  {length}비트: {count}개")
    
    print("\n[Sub-primitive별 분포]")
    for prim in sorted(sub_count.keys()):
        print(f"\n  {prim}:")
        for sub, count in sorted(sub_count[prim].items()):
            print(f"    {sub}: {count}개")

def main():
    # 파일 경로 설정
    verb_file = os.path.join(os.path.dirname(__file__), 'verb559.json')
    prim_map_file = os.path.join(os.path.dirname(__file__), 'primitive-map.json')
    classified_dir = os.path.join(os.path.dirname(__file__), 'classified')
    
    # 대체 경로 (uploads에 직접 있는 경우)
    if not os.path.exists(classified_dir):
        classified_dir = os.path.join(os.path.dirname(__file__), 'classified')
    
    print("GEUL Verb Flat Field Validator")
    print("=" * 60)
    print(f"verb559.json: {verb_file}")
    print(f"primitive-map.json: {prim_map_file}")
    print(f"classified dir: {classified_dir}")
    print()
    
    # 파일 로드
    try:
        verb_data = load_json(verb_file)
        print(f"✓ verb559.json 로드: {len(verb_data.get('roots', []))}개 항목")
    except Exception as e:
        print(f"✗ verb559.json 로드 실패: {e}")
        sys.exit(1)
    
    try:
        prim_map = load_json(prim_map_file)
        print(f"✓ primitive-map.json 로드: {len(prim_map.get('flat_map', {}))}개 매핑")
    except Exception as e:
        print(f"✗ primitive-map.json 로드 실패: {e}")
        sys.exit(1)
    
    # 검증 실행
    results = []
    
    results.append(("FLAT_MAP 일치", validate_flat_mapping(verb_data, prim_map)))
    results.append(("CLASSIFIED 일치", validate_sub_primitive_consistency(verb_data, classified_dir)))
    results.append(("비트 구조", validate_bit_structure(verb_data, prim_map)))
    
    # 통계 출력
    print_statistics(verb_data, prim_map)
    
    # 최종 결과
    print("\n" + "=" * 60)
    print("최종 결과")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {name}: {status}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 모든 검증 통과!")
    else:
        print("⚠️  일부 검증 실패")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())