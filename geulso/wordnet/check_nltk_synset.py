#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nltk
from nltk.corpus import wordnet as wn

SYNSET_TO_CHECK = 'quantity.n.01'

def check_synset_integrity():
    """
    특정 Synset 객체를 NLTK가 문제없이 처리할 수 있는지 모든 속성을 검사합니다.
    """
    print("="*60)
    print(f"NLTK 라이브러리가 '{SYNSET_TO_CHECK}'를 정상적으로 처리하는지 검사합니다.")
    print("="*60)

    try:
        synset = wn.synset(SYNSET_TO_CHECK)
        print(f"✅ Synset 객체 로드 성공: {synset}")
    except Exception as e:
        print(f"❌ 치명적 오류: '{SYNSET_TO_CHECK}' Synset 객체 자체를 로드할 수 없습니다.")
        print(f"   -> 원인: {e}")
        return

    # postgres.py에서 사용하는 모든 속성에 접근을 시도합니다.
    attributes_to_check = [
        'name', 'pos', 'lexname', 'definition', 'examples', 'lemmas', 'offset'
    ]

    all_successful = True
    for attr in attributes_to_check:
        print(f"\n- 속성 '.{attr}()' 접근 시도...")
        try:
            # .lemmas() 처럼 함수일 수도 있고, .offset 처럼 속성일 수도 있으므로 getattr 사용
            method_or_attr = getattr(synset, attr)
            if callable(method_or_attr):
                result = method_or_attr()
            else:
                result = method_or_attr
            
            print(f"  -> ✅ 성공. 결과 타입: {type(result)}")
        except Exception as e:
            print(f"  -> ❌ 실패!")
            print(f"  -> 에러 메시지: {e}")
            all_successful = False

    print("\n" + "="*60)
    if all_successful:
        print("✅ 최종 결론: NLTK는 이 Synset의 모든 정보를 문제없이 읽을 수 있습니다.")
        print("   이 경우, postgres.py의 루프 로직에 다른 미묘한 문제가 있을 수 있습니다.")
    else:
        print("❌ 최종 결론: NLTK가 이 Synset의 특정 정보를 읽는 데 실패했습니다.")
        print("   이것이 postgres.py가 해당 Synset을 건너뛰는 원인입니다.")
    print("="*60)

if __name__ == "__main__":
    check_synset_integrity()