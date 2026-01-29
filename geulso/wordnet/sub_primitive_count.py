#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sub_primitive별 verb_count 집계기
verb559.json을 분석하여 각 sub_primitive의 총 동사 수 계산

Usage:
    python3 geulso/wordnet/sub_primitive_count.py

Output:
    geulso/wordnet/sub_primitive_count.json
"""

import json
from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = Path(__file__).parent
VERB559_PATH = SCRIPT_DIR / "verb559.json"
OUTPUT_PATH = SCRIPT_DIR / "sub_primitive_count.json"


def main():
    with open(VERB559_PATH, "r", encoding="utf-8") as f:
        verb559 = json.load(f)
    
    # sub_primitive별 집계
    counts = defaultdict(lambda: {"roots": 0, "descendants": 0, "total": 0})
    
    for root in verb559["roots"]:
        prim = root.get("primitive", "UNKNOWN")
        sub = root.get("sub_primitive", "UNKNOWN")
        key = f"{prim}-{sub}"
        
        desc = root.get("descendant_count", 0)
        counts[key]["roots"] += 1
        counts[key]["descendants"] += desc
        counts[key]["total"] += desc + 1  # 자기 자신 포함
    
    # 정렬 (total 내림차순)
    sorted_counts = sorted(counts.items(), key=lambda x: x[1]["total"], reverse=True)
    
    # 결과 구성
    result = {
        "description": "Sub_primitive별 동사 수 집계",
        "total_sub_primitives": len(sorted_counts),
        "total_verbs": sum(v["total"] for v in counts.values()),
        "sub_primitives": []
    }
    
    for key, data in sorted_counts:
        result["sub_primitives"].append({
            "id": key,
            "roots": data["roots"],
            "descendants": data["descendants"],
            "total": data["total"]
        })
    
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"{OUTPUT_PATH.name}")


if __name__ == "__main__":
    main()