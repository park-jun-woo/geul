#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import argparse
import nltk
from nltk.corpus import wordnet as wn

def print_synset_details(synset: wn.synset, source: str):
    """주어진 Synset 객체의 상세 정보를 출력합니다."""
    print("-" * 60)
    print(f"Synset: {synset.name()} ({source}에서 찾음)")
    print(f"  - 정의: {synset.definition()}")
    print(f"  - 예시: {synset.examples()}")
    print(f"  - 동의어 목록(Lemmas): {[lemma.name() for lemma in synset.lemmas()]}")
    print("-" * 60)

def find_by_direct_lookup(search_id: str) -> bool:
    """1단계: Synset ID를 직접 조회합니다."""
    print("\n--- 1단계: Synset ID 직접 조회 시도 ---")
    try:
        found_synset = wn.synset(search_id)
        print(f"✅ 성공: '{search_id}'를 찾았습니다 (리다이렉트 포함).")
        print_synset_details(found_synset, "직접 조회")
        return True
    except (nltk.corpus.reader.wordnet.WordNetError, ValueError):
        print(f"❌ 실패: '{search_id}'는 유효한 Synset ID가 아닙니다.")
        return False

def find_by_lemma_search(search_id: str):
    """2단계: ID에서 추출한 단어로 동의어(lemma)를 검색합니다."""
    print("\n--- 2단계: 동의어(Lemma) 검색 시도 ---")
    
    # ▼▼▼▼▼ [수정] 파싱 로직 개선 ▼▼▼▼▼
    keyword = search_id.split('.')[0].replace('_', ' ')
    pos_match = re.search(r'\.([nvasr])\.', search_id)
    pos = pos_match.group(1) if pos_match else None
    if pos == 's': pos = 'a'
    # ▲▲▲▲▲ [수정] 파싱 로직 개선 ▲▲▲▲▲

    print(f"-> 검색 키워드: '{keyword}', 품사: {pos if pos else '모든 품사'}")
    
    lemma_candidates = set()
    for synset in wn.all_synsets(pos=pos if pos else None):
        for lemma in synset.lemmas():
            if keyword.lower() == lemma.name().lower().replace('_', ' '):
                lemma_candidates.add(synset)
    
    if lemma_candidates:
        print(f"✅ 성공: 총 {len(lemma_candidates)}개의 Synset이 '{keyword}'를 동의어로 포함합니다.")
        for i, candidate in enumerate(lemma_candidates, 1):
            print(f"\n후보 {i}:")
            print_synset_details(candidate, "동의어 검색")
        return True
    else:
        print(f"❌ 실패: '{keyword}'를 동의어로 포함하는 Synset을 찾지 못했습니다.")
        return False

def find_by_keyword_in_gloss(search_id: str):
    """3단계: ID에서 추출한 키워드로 정의(gloss)를 검색합니다."""
    print("\n--- 3단계: 키워드(Gloss) 검색 시도 ---")

    # ▼▼▼▼▼ [수정] 파싱 로직 개선 ▼▼▼▼▲
    keywords_str = search_id.split('.')[0]
    keywords = keywords_str.replace('-', ' ').split('_')
    pos_match = re.search(r'\.([nvasr])\.', search_id)
    pos = pos_match.group(1) if pos_match else None
    if pos == 's': pos = 'a'
    # ▲▲▲▲▲ [수정] 파싱 로직 개선 ▲▲▲▲▲

    print(f"-> 검색 키워드: {keywords}, 품사: {pos if pos else '모든 품사'}")

    gloss_candidates = []
    for synset in wn.all_synsets(pos=pos if pos else None):
        gloss = synset.definition()
        for example in synset.examples():
            gloss += " " + example
        
        if all(keyword.lower() in gloss.lower() for keyword in keywords):
            gloss_candidates.append(synset)
            
    if gloss_candidates:
        print(f"✅ 성공: 총 {len(gloss_candidates)}개의 Synset이 키워드를 정의/예시에 포함합니다.")
        for i, candidate in enumerate(gloss_candidates, 1):
            print(f"\n후보 {i}:")
            print_synset_details(candidate, "정의 검색")
    else:
        print("❌ 실패: 키워드를 포함하는 Synset을 찾지 못했습니다.")

def main():
    parser = argparse.ArgumentParser(
        description="3단계에 걸쳐 Synset을 검색합니다: 1.직접조회 2.동의어검색 3.키워드검색"
    )
    parser.add_argument("search_term", type=str, help="조회 또는 검색할 Synset ID/키워드")
    args = parser.parse_args()

    try:
        nltk.data.find('corpora/wordnet.zip')
    except nltk.downloader.DownloadError:
        nltk.download('wordnet')

    if find_by_direct_lookup(args.search_term):
        pass
    elif find_by_lemma_search(args.search_term):
        pass
    else:
        find_by_keyword_in_gloss(args.search_term)

if __name__ == "__main__":
    main()