#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import nltk
from nltk.corpus import wordnet as wn
from tqdm import tqdm

def build_all_lemma_names():
    """
    NLTK WordNet에 존재하는 모든 고유한 lemma 이름을 수집하여 set으로 반환합니다.
    """
    print("WordNet의 모든 동의어(lemma)를 수집 중입니다. 시간이 다소 걸릴 수 있습니다...")
    all_lemmas = set()
    # wn.all_synsets()는 매우 빠르지만, 모든 lemma를 순회하는 것은 시간이 걸립니다.
    for synset in tqdm(wn.all_synsets(), desc="Synsets 순회"):
        for lemma in synset.lemmas():
            # word_form, drive-in -> word form, drive in
            all_lemmas.add(lemma.name().lower().replace('_', ' '))
    return all_lemmas

def verify_lemma_existence(lemma_to_check: str, all_lemmas: set):
    """
    주어진 lemma가 수집된 전체 lemma 목록에 있는지 확인하고 결과를 출력합니다.
    """
    print(f"\n--- '{lemma_to_check}' 단어 존재 여부 확인 ---")
    if lemma_to_check.lower() in all_lemmas:
        print(f"✅ 확인: '{lemma_to_check}'는 WordNet에 동의어(lemma)로 존재합니다.")
        # 만약 존재한다면, 어떤 synset에 속해있는지 찾아 출력
        found_in = [s.name() for s in wn.synsets(lemma_to_check.replace(' ', '_'))]
        print(f"   -> 소속된 Synsets: {found_in}")
    else:
        print(f"❌ 확인: '{lemma_to_check}'는 WordNet에 동의어(lemma)로 존재하지 않습니다.")

def main():
    parser = argparse.ArgumentParser(description="WordNet에 특정 단어가 동의어(lemma)로 존재하는지 확인합니다.")
    parser.add_argument("words", nargs='+', help="확인할 단어들 (공백으로 구분)")
    args = parser.parse_args()

    try:
        nltk.data.find('corpora/wordnet.zip')
    except nltk.downloader.DownloadError:
        nltk.download('wordnet')

    # 한 번만 전체 lemma 목록을 생성
    all_lemma_names = build_all_lemma_names()
    print(f"\n총 {len(all_lemma_names):,}개의 고유한 동의어를 수집했습니다.")

    # 입력받은 모든 단어에 대해 존재 여부 확인
    for word in args.words:
        verify_lemma_existence(word, all_lemma_names)

if __name__ == "__main__":
    main()