#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
import copy

INVALID_DIR = 'geulso/factorize/invalid/'
FACTORIZED_DIR = 'geulso/factorize/factorized/'
CORRECTED_DIR = 'geulso/factorize/corrected/'

class CorrectionApplier:
    """교정 정보를 원본 JSON에 적용하는 클래스"""
    
    def __init__(self):
        self.stats = {
            'total_files': 0,
            'processed_files': 0,
            'skipped_has_no_candidate': 0,
            'skipped_no_original': 0,
            'applied_sememes': 0,
            'applied_participants': 0,
            'failed_files': 0
        }
    
    def load_json(self, filepath: Path) -> Optional[Dict[str, Any]]:
        """JSON 파일을 로드합니다."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"  ✗ JSON 파싱 실패: {filepath.name}")
            return None
        except Exception as e:
            print(f"  ✗ 파일 읽기 실패 {filepath.name}: {e}")
            return None
    
    def has_no_candidate(self, invalid_data: Dict[str, Any]) -> bool:
        """NO_CANDIDATE가 하나라도 있는지 확인합니다."""
        corrections = invalid_data.get('corrections', {})
        
        # Sememes 확인
        for item in corrections.get('sememes', []):
            if item.get('corrected_value') == 'NO_CANDIDATE':
                return True
        
        # Participants 확인
        for item in corrections.get('participants', []):
            if item.get('corrected_value') == 'NO_CANDIDATE':
                return True
        
        return False
    
    def apply_sememe_correction(self, factorized_data: Dict[str, Any], 
                               error: Dict[str, Any], 
                               correction: Dict[str, Any]) -> bool:
        """Sememe의 교정을 적용합니다."""
        synset_id = error.get('synset_id')
        frame_id = error.get('frame_id')
        key = error.get('key')
        original_value = error.get('value')
        corrected_value = correction.get('corrected_value')
        
        if not corrected_value or corrected_value == 'NO_CANDIDATE':
            return False
        
        # factorized_data의 synset_id와 frame_id가 일치하는지 확인
        if (factorized_data.get('synset_id') != synset_id or 
            factorized_data.get('frame_id') != frame_id):
            return False
        
        # sememes 리스트 순회
        sememes = factorized_data.get('sememes', [])
        for sememe in sememes:
            # key에 해당하는 필드가 있고, 값이 original_value와 일치하면 교정
            if key in sememe and sememe[key] == original_value:
                sememe[key] = corrected_value
                self.stats['applied_sememes'] += 1
                print(f"    ✓ Sememe {key}: {original_value} → {corrected_value}")
                return True
        
        return False
    
    def apply_participant_correction(self, factorized_data: Dict[str, Any], 
                                    error: Dict[str, Any], 
                                    correction: Dict[str, Any]) -> bool:
        """Participant의 교정을 적용합니다."""
        synset_id = error.get('synset_id')
        frame_id = error.get('frame_id')
        key = error.get('key')
        original_value = error.get('value')
        corrected_value = correction.get('corrected_value')
        
        if not corrected_value or corrected_value == 'NO_CANDIDATE':
            return False
        
        # factorized_data의 synset_id와 frame_id가 일치하는지 확인
        if (factorized_data.get('synset_id') != synset_id or 
            factorized_data.get('frame_id') != frame_id):
            return False
        
        # sememes > participants 리스트 순회
        sememes = factorized_data.get('sememes', [])
        for sememe in sememes:
            participants = sememe.get('participants', [])
            for participant in participants:
                # key에 해당하는 필드가 있고, 값이 original_value와 일치하면 교정
                if key in participant and participant[key] == original_value:
                    participant[key] = corrected_value
                    self.stats['applied_participants'] += 1
                    print(f"    ✓ Participant {key}: {original_value} → {corrected_value}")
                    return True
        
        return False
    
    def apply_corrections(self, invalid_data: Dict[str, Any], 
                         factorized_data: Dict[str, Any]) -> Dict[str, Any]:
        """모든 교정을 적용한 새로운 데이터를 반환합니다."""
        # 원본 데이터의 깊은 복사본 생성
        corrected_data = copy.deepcopy(factorized_data)
        
        errors = invalid_data.get('errors', {})
        corrections = invalid_data.get('corrections', {})
        
        # Sememes 교정 적용
        sememe_errors = errors.get('sememes', [])
        sememe_corrections = corrections.get('sememes', [])
        
        for i, (error, correction) in enumerate(zip(sememe_errors, sememe_corrections)):
            self.apply_sememe_correction(corrected_data, error, correction)
        
        # Participants 교정 적용
        participant_errors = errors.get('participants', [])
        participant_corrections = corrections.get('participants', [])
        
        for i, (error, correction) in enumerate(zip(participant_errors, participant_corrections)):
            self.apply_participant_correction(corrected_data, error, correction)
        
        return corrected_data
    
    def process_file(self, invalid_filepath: Path, 
                    factorized_dir: Path, 
                    corrected_dir: Path) -> bool:
        """단일 파일을 처리합니다."""
        print(f"\n처리 중: {invalid_filepath.name}")
        
        # invalid JSON 로드
        invalid_data = self.load_json(invalid_filepath)
        if not invalid_data:
            self.stats['failed_files'] += 1
            return False
        
        # NO_CANDIDATE가 하나라도 있으면 건너뛰기
        if self.has_no_candidate(invalid_data):
            print(f"  ⊗ NO_CANDIDATE 포함 - 건너뛰기")
            self.stats['skipped_has_no_candidate'] += 1
            return False
        
        # 원본 factorized JSON 로드
        factorized_filepath = factorized_dir / invalid_filepath.name
        if not factorized_filepath.exists():
            print(f"  ✗ 원본 파일 없음: {factorized_filepath.name}")
            self.stats['skipped_no_original'] += 1
            return False
        
        factorized_data = self.load_json(factorized_filepath)
        if not factorized_data:
            self.stats['failed_files'] += 1
            return False
        
        # 교정 적용
        corrected_data = self.apply_corrections(invalid_data, factorized_data)
        
        # 결과 저장
        corrected_dir.mkdir(parents=True, exist_ok=True)
        output_filepath = corrected_dir / invalid_filepath.name
        
        try:
            with open(output_filepath, 'w', encoding='utf-8') as f:
                json.dump(corrected_data, f, indent=2, ensure_ascii=False)
            print(f"  ✓ 저장 완료: {output_filepath.name}")
            self.stats['processed_files'] += 1
            return True
        except Exception as e:
            print(f"  ✗ 저장 실패: {e}")
            self.stats['failed_files'] += 1
            return False
    
    def process_directory(self):
        """디렉토리의 모든 파일을 처리합니다."""
        invalid_path = Path(INVALID_DIR)
        factorized_path = Path(FACTORIZED_DIR)
        corrected_path = Path(CORRECTED_DIR)
        
        if not invalid_path.exists():
            print(f"✗ Invalid 디렉토리를 찾을 수 없습니다: {INVALID_DIR}")
            sys.exit(1)
        
        if not factorized_path.exists():
            print(f"✗ Factorized 디렉토리를 찾을 수 없습니다: {FACTORIZED_DIR}")
            sys.exit(1)
        
        json_files = list(invalid_path.glob('*.json'))
        self.stats['total_files'] = len(json_files)
        
        if not json_files:
            print(f"✗ JSON 파일이 없습니다: {INVALID_DIR}")
            sys.exit(1)
        
        print(f"\n총 {len(json_files):,}개의 JSON 파일 처리 시작...")
        print("="*70)
        
        for filepath in json_files:
            self.process_file(filepath, factorized_path, corrected_path)
        
        print("\n" + "="*70)
        print("처리 완료!")
        print("="*70)
    
    def print_stats(self):
        """통계를 출력합니다."""
        print("\n" + "="*70)
        print("처리 통계")
        print("="*70)
        print(f"전체 파일: {self.stats['total_files']:,}개")
        print(f"성공적으로 처리: {self.stats['processed_files']:,}개")
        print(f"NO_CANDIDATE 포함으로 건너뜀: {self.stats['skipped_has_no_candidate']:,}개")
        print(f"원본 파일 없음: {self.stats['skipped_no_original']:,}개")
        print(f"처리 실패: {self.stats['failed_files']:,}개")
        print("-"*70)
        print(f"적용된 Sememe 교정: {self.stats['applied_sememes']:,}개")
        print(f"적용된 Participant 교정: {self.stats['applied_participants']:,}개")
        print(f"총 적용된 교정: {self.stats['applied_sememes'] + self.stats['applied_participants']:,}개")
        print("="*70)
        
        if self.stats['processed_files'] > 0:
            print(f"\n✓ 교정된 파일 저장 위치: {CORRECTED_DIR}")
        
        # 처리 가능 vs 불가능 요약
        processable = self.stats['total_files'] - self.stats['skipped_has_no_candidate']
        print(f"\n📊 요약:")
        print(f"  • 교정 가능한 파일: {processable:,}개 ({processable/self.stats['total_files']*100:.1f}%)")
        print(f"  • 교정 불가능한 파일 (NO_CANDIDATE 포함): {self.stats['skipped_has_no_candidate']:,}개 ({self.stats['skipped_has_no_candidate']/self.stats['total_files']*100:.1f}%)")

def main():
    """메인 실행 함수"""
    print("="*70)
    print("GEUL Factorized JSON 교정 적용 스크립트")
    print("="*70)
    print("\n⚠️  주의: NO_CANDIDATE가 하나라도 있는 파일은 건너뜁니다.\n")
    
    applier = CorrectionApplier()
    
    try:
        applier.process_directory()
        applier.print_stats()
    except KeyboardInterrupt:
        print("\n\n처리가 중단되었습니다.")
        applier.print_stats()
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ 치명적 오류 발생: {e}")
        applier.print_stats()
        sys.exit(1)

if __name__ == "__main__":
    main()