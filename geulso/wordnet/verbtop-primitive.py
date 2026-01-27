#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
특정 primitive의 동사만 추출

Usage:
    python3 verbtop-primitive.py <PRIMITIVE> <output_path> [input_path]
    
Example:
    python3 geulso/wordnet/verbtop-primitive.py CAUSE geulso/wordnet/top/verbtop-cause.json
    python3 verbtop-primitive.py BE verbtop-be.json verbclassified559.json
"""

import sys
import json
import os

DEFAULT_INPUT = os.path.join(os.path.dirname(__file__), 'verbclassified559.json')

VALID_PRIMITIVES = [
    'BE', 'PERCEIVE', 'FEEL', 'THINK',
    'CHANGE', 'CAUSE', 'MOVE',
    'TRANSFER', 'COMMUNICATE', 'SOCIAL'
]


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 verbtop-primitive.py <PRIMITIVE> <output_path> [input_path]")
        print(f"Valid primitives: {', '.join(VALID_PRIMITIVES)}")
        sys.exit(1)
    
    primitive = sys.argv[1].upper()
    output_path = sys.argv[2]
    input_path = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_INPUT
    
    if primitive not in VALID_PRIMITIVES:
        print(f"Error: Invalid primitive '{primitive}'")
        print(f"Valid primitives: {', '.join(VALID_PRIMITIVES)}")
        sys.exit(1)
    
    # 입력 파일 로드
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 필터링
    filtered = [r for r in data['roots'] if r['primitive'] == primitive]
    
    # 출력 구조
    output = {
        'primitive': primitive,
        'description': data['primitives'].get(primitive, ''),
        'count': len(filtered),
        'roots': filtered
    }
    
    # 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"{primitive}: {len(filtered)}개 추출 → {output_path}")


if __name__ == "__main__":
    main()