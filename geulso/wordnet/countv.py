import nltk
from nltk.corpus import wordnet as wn

# 1. NLTK 워드넷 데이터 다운로드 (최초 1회 실행 필요)
# 이미 다운로드했다면 이 줄은 주석 처리해도 됩니다.
try:
    wn.all_synsets()
except LookupError:
    print("Downloading WordNet data package...")
    # 'wordnet'과 다국어 확장을 함께 다운로드합니다.
    nltk.download('wordnet')
    nltk.download('omw-1.4')

# 2. 모든 '동사(verb)' synset을 리스트로 가져옵니다.
# pos=wn.VERB는 Part-of-Speech(품사)가 동사인 것만 필터링합니다.
all_verb_synsets = list(wn.all_synsets(pos=wn.VERB))

# 3. 개수를 출력합니다.
print(f"Total number of verb synsets in WordNet: {len(all_verb_synsets)}")

# (참고) 다른 품사의 synset 개수
# print(f"Noun synsets: {len(list(wn.all_synsets(pos=wn.NOUN)))}")
# print(f"Adjective synsets: {len(list(wn.all_synsets(pos=wn.ADJ)))}")
# print(f"Adverb synsets: {len(list(wn.all_synsets(pos=wn.ADV)))}")