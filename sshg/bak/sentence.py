import nltk
from nltk.corpus import treebank
from nltk.grammar import induce_pcfg, Nonterminal
from nltk.parse import EarleyChartParser
import argparse
import pickle
import os
import sys

# 학습된 문법을 저장할 파일 이름
GRAMMAR_FILE = 'penn_treebank_grammar.pcfg'

def train_and_save_grammar():
    """
    Penn Treebank에서 PCFG 문법을 학습하고 파일로 저장합니다.
    """
    print("Penn Treebank로부터 PCFG 문법을 학습합니다. 이 작업은 몇 분 정도 소요될 수 있습니다...")
    
    # NLTK의 Treebank 코퍼스에서 모든 생성 규칙(production)을 추출
    productions = []
    # treebank.parsed_sents()는 모든 파싱된 문장 트리를 제공합니다.
    for tree in treebank.parsed_sents():
        productions.extend(tree.productions())
        
    # 문법의 시작 기호를 'S' (Sentence)로 지정
    start_symbol = Nonterminal('S')
    
    # 추출된 규칙들로부터 확률적 문맥 자유 문법(PCFG)을 학습
    grammar = induce_pcfg(start_symbol, productions)
    
    # 학습된 문법을 파일에 저장 (pickle 사용)
    with open(GRAMMAR_FILE, 'wb') as f:
        pickle.dump(grammar, f)
        
    print(f"✅ 문법 학습 완료! '{GRAMMAR_FILE}' 파일에 저장되었습니다.")
    return grammar

def load_grammar():
    """
    저장된 문법 파일을 불러오거나, 파일이 없으면 새로 학습합니다.
    """
    # NLTK 데이터 다운로드 확인
    try:
        nltk.data.find('corpora/treebank/parsed')
    except LookupError:
        print("Penn Treebank 데이터가 필요합니다. python -c \"import nltk; nltk.download('treebank')\" 를 실행해주세요.")
        sys.exit(1)
        
    if not os.path.exists(GRAMMAR_FILE):
        print(f"'{GRAMMAR_FILE}' 파일을 찾을 수 없습니다.")
        grammar = train_and_save_grammar()
    else:
        print(f"'{GRAMMAR_FILE}' 파일에서 학습된 문법을 불러옵니다.")
        with open(GRAMMAR_FILE, 'rb') as f:
            grammar = pickle.load(f)
        print("✅ 문법 로딩 완료!")
    return grammar

def main():
    """
    메인 실행 함수
    """
    # 1. 명령줄 인자 파서 설정
    cli_parser = argparse.ArgumentParser(description="Earley 파서를 사용하여 문장의 모든 가능한 구문 해석을 탐색합니다.")
    cli_parser.add_argument(
        '--sentence', 
        type=str, 
        required=True, 
        help='파싱할 영어 문장을 큰따옴표("")로 묶어 입력하세요.'
    )
    args = cli_parser.parse_args()
    
    # 2. 문법 로드
    grammar = load_grammar()
    
    # 3. 파서 생성
    parser = EarleyChartParser(grammar)
    
    # 4. 입력 문장 토큰화
    sentence_to_parse = args.sentence.split()
    
    # 5. 파싱 실행 및 결과 출력
    parses = parser.parse(sentence_to_parse)
    
    print("-" * 50)
    print(f"'{args.sentence}' 문장에 대한 모든 구문 해석 결과:")
    print("-" * 50)

    found_parses = False
    for i, tree in enumerate(parses):
        found_parses = True
        print(f"✅ 해석 #{i + 1}")
        tree.pretty_print()
        print()

    if not found_parses:
        print("❌ 문법 규칙에 맞는 해석을 찾을 수 없습니다. (문법에 없는 단어가 포함되었을 수 있습니다)")

if __name__ == "__main__":
    main()