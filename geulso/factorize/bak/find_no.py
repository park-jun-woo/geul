#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from pathlib import Path
from typing import List, Dict, Any

FACTORIZE_DIR = 'geulso/factorize/'
INVALID_DIR = 'geulso/factorize/invalid/'

def find_no_candidates_in_file(filepath: Path) -> Dict[str, Any]:
    """JSON 파일에서 NO_CANDIDATE를 찾습니다."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        no_candidates = {
            'sememes': [],
            'participants': []
        }
        
        corrections = data.get('corrections', {})
        
        # sememes 검사
        for item in corrections.get('sememes', []):
            if item.get('corrected_value') == 'NO_CANDIDATE':
                no_candidates['sememes'].append({
                    'synset_id': item.get('synset_id'),
                    'frame_id': item.get('frame_id'),
                    'key': item.get('key'),
                    'original_value': data.get('errors', {}).get('sememes', [{}])[
                        corrections.get('sememes', []).index(item)
                    ].get('value', ''),
                    'reasoning': item.get('corrected_reasoning', '')
                })
        
        # participants 검사
        for item in corrections.get('participants', []):
            if item.get('corrected_value') == 'NO_CANDIDATE':
                # participants 인덱스 찾기
                idx = corrections.get('participants', []).index(item)
                original_value = ''
                if idx < len(data.get('errors', {}).get('participants', [])):
                    original_value = data.get('errors', {}).get('participants', [])[idx].get('value', '')
                
                no_candidates['participants'].append({
                    'synset_id': item.get('synset_id'),
                    'frame_id': item.get('frame_id'),
                    'key': item.get('key'),
                    'original_value': original_value,
                    'reasoning': item.get('corrected_reasoning', '')
                })
        
        if no_candidates['sememes'] or no_candidates['participants']:
            return {
                'filename': filepath.name,
                'no_candidates': no_candidates
            }
        
        return None
        
    except json.JSONDecodeError:
        print(f"  ✗ JSON 파싱 실패: {filepath.name}")
        return None
    except Exception as e:
        print(f"  ✗ 파일 읽기 실패 {filepath.name}: {e}")
        return None

def main():
    """메인 실행 함수"""
    print("="*70)
    print("NO_CANDIDATE 검색 스크립트")
    print("="*70)
    
    invalid_path = Path(INVALID_DIR)
    
    if not invalid_path.exists():
        print(f"✗ 디렉토리를 찾을 수 없습니다: {INVALID_DIR}")
        sys.exit(1)
    
    json_files = list(invalid_path.glob('*.json'))
    
    if not json_files:
        print(f"✗ JSON 파일이 없습니다: {INVALID_DIR}")
        sys.exit(1)
    
    print(f"\n총 {len(json_files):,}개의 JSON 파일 검색 중...\n")
    
    results = []
    total_no_candidates = 0
    sememe_count = 0
    participant_count = 0
    
    for filepath in json_files:
        result = find_no_candidates_in_file(filepath)
        if result:
            results.append(result)
            sememe_count += len(result['no_candidates']['sememes'])
            participant_count += len(result['no_candidates']['participants'])
            total_no_candidates += sememe_count + participant_count
    
    # 결과 출력
    print("="*70)
    print("검색 결과")
    print("="*70)
    
    if not results:
        print("\n✓ NO_CANDIDATE가 있는 파일이 없습니다!")
    else:
        print(f"\n✗ NO_CANDIDATE가 있는 파일: {len(results):,}개\n")
        
        for idx, result in enumerate(results, 1):
            print(f"\n[{idx}] {result['filename']}")
            print("-"*70)
            
            # Sememes 출력
            if result['no_candidates']['sememes']:
                print("  📌 Sememes:")
                for item in result['no_candidates']['sememes']:
                    print(f"     • {item['synset_id']}.f.{item['frame_id']:02d}")
                    print(f"       - Key: {item['key']}")
                    print(f"       - Original: {item['original_value']}")
                    print(f"       - Reasoning: {item['reasoning'][:100]}...")
                    print()
            
            # Participants 출력
            if result['no_candidates']['participants']:
                print("  📌 Participants:")
                for item in result['no_candidates']['participants']:
                    print(f"     • {item['synset_id']}.f.{item['frame_id']:02d}")
                    print(f"       - Key: {item['key']}")
                    print(f"       - Original: {item['original_value']}")
                    print(f"       - Reasoning: {item['reasoning'][:100]}...")
                    print()
    
    # 통계 출력
    print("="*70)
    print("통계")
    print("="*70)
    print(f"전체 파일 수: {len(json_files):,}개")
    print(f"NO_CANDIDATE 포함 파일: {len(results):,}개 ({len(results)/len(json_files)*100:.1f}%)")
    print(f"  - Sememe NO_CANDIDATE: {sememe_count:,}개")
    print(f"  - Participant NO_CANDIDATE: {participant_count:,}개")
    print(f"  - 총 NO_CANDIDATE: {sememe_count + participant_count:,}개")
    print("="*70)
    
    # 파일 리스트 저장 (선택사항)
    if results:
        output_file = Path(FACTORIZE_DIR) / 'no_candidate_list.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("NO_CANDIDATE가 있는 파일 목록\n")
            f.write("="*70 + "\n\n")
            for result in results:
                f.write(f"{result['filename']}\n")
                for item in result['no_candidates']['sememes']:
                    f.write(f"  [Sememe] {item['key']}: {item['original_value']}\n")
                for item in result['no_candidates']['participants']:
                    f.write(f"  [Participant] {item['key']}: {item['original_value']}\n")
                f.write("\n")
        print(f"\n✓ 파일 목록 저장: {output_file}")

if __name__ == "__main__":
    main()