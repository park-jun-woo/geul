#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
import argparse
import asyncio
from pathlib import Path
from tqdm import tqdm
from typing import List, Dict
import nltk
from nltk.corpus import wordnet as wn

FACTORIZED_DIR = 'geulso/factorize/factorized/'
INVALID_DIR = 'geulso/factorize/invalid/'

class SynsetValidator:
    """JSON 파일의 synset 참조를 검증하고 후보를 찾는 클래스"""
    
    def __init__(self):
        """NLTK WordNet 초기화 및 캐시 준비"""
        try:
            nltk.data.find('corpora/wordnet.zip')
        except nltk.downloader.DownloadError:
            print("WordNet 데이터 다운로드 중...")
            nltk.download('wordnet')
        
        self.validation_cache = {}
        self.stats = {
            'total_files': 0,
            'skipped_files': 0,
            'processed_files': 0,
            'invalid_files': 0,
            'sememe_errors': 0,
            'participant_errors': 0
        }
    
    def is_valid_synset(self, synset_id: str) -> bool:
        """synset_id가 NLTK에서 유효한지 확인 (캐싱)"""
        if not synset_id or synset_id.strip() == "":
            return True
        
        if synset_id in self.validation_cache:
            return self.validation_cache[synset_id]
        
        try:
            wn.synset(synset_id)
            self.validation_cache[synset_id] = True
            return True
        except (nltk.corpus.reader.wordnet.WordNetError, ValueError, KeyError):
            self.validation_cache[synset_id] = False
            return False
    
    def find_candidates(self, invalid_synset_id: str, max_candidates: int = 5) -> List[Dict[str, str]]:
        """find.py의 3단계 로직을 사용해 후보 synset 찾기"""
        candidates = []
        
        # 2단계: 동의어(Lemma) 검색
        candidates.extend(self._find_by_lemma(invalid_synset_id, max_candidates))
        if len(candidates) >= max_candidates:
            return candidates[:max_candidates]
        
        # 3단계: 키워드(Gloss) 검색
        remaining = max_candidates - len(candidates)
        candidates.extend(self._find_by_gloss(invalid_synset_id, remaining))
        
        return candidates[:max_candidates]
    
    def _find_by_lemma(self, synset_id: str, max_results: int) -> List[Dict[str, str]]:
        """2단계: 동의어 검색"""
        keyword = synset_id.split('.')[0].replace('_', ' ')
        pos_match = re.search(r'\.([nvasr])\.', synset_id)
        pos = pos_match.group(1) if pos_match else None
        if pos == 's':
            pos = 'a'
        
        candidates = []
        seen = set()
        
        try:
            for synset in wn.all_synsets(pos=pos if pos else None):
                if len(candidates) >= max_results:
                    break
                for lemma in synset.lemmas():
                    if keyword.lower() == lemma.name().lower().replace('_', ' '):
                        if synset.name() not in seen:
                            candidates.append({
                                "synset_id": synset.name(),
                                "description": f"{synset.definition()} (lemma match)"
                            })
                            seen.add(synset.name())
                        break
        except Exception:
            pass
        
        return candidates
    
    def _find_by_gloss(self, synset_id: str, max_results: int) -> List[Dict[str, str]]:
        """3단계: 정의(Gloss) 검색"""
        keywords_str = synset_id.split('.')[0]
        keywords = keywords_str.replace('-', ' ').split('_')
        pos_match = re.search(r'\.([nvasr])\.', synset_id)
        pos = pos_match.group(1) if pos_match else None
        if pos == 's':
            pos = 'a'
        
        candidates = []
        seen = set()
        
        try:
            for synset in wn.all_synsets(pos=pos if pos else None):
                if len(candidates) >= max_results:
                    break
                
                gloss = synset.definition()
                for example in synset.examples():
                    gloss += " " + example
                
                if any(keyword.lower() in gloss.lower() for keyword in keywords):
                    if synset.name() not in seen:
                        candidates.append({
                            "synset_id": synset.name(),
                            "description": f"{synset.definition()} (gloss match)"
                        })
                        seen.add(synset.name())
        except Exception:
            pass
        
        return candidates
    
    async def validate_json_file(self, filepath: Path, output_path: Path) -> bool:
        """JSON 파일을 검증하고 오류가 있으면 저장 (비동기)"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            synset_id = data.get('synset_id')
            frame_id = data.get('frame_id')
            
            if not synset_id or frame_id is None:
                return False
            
            errors = {
                'sememes': [],
                'participants': []
            }
            
            # Sememes 검증
            sememes = data.get('sememes', [])
            if isinstance(sememes, list):
                for sememe in sememes:
                    verb_property = sememe.get('verb_property')
                    if verb_property and not self.is_valid_synset(verb_property):
                        candidates = self.find_candidates(verb_property)
                        errors['sememes'].append({
                            "synset_id": synset_id,
                            "frame_id": frame_id,
                            "key": "verb_property",
                            "value": verb_property,
                            "reasoning": f"verb_property '{verb_property}' is not a valid synset in NLTK.",
                            "candidates": candidates if candidates else [{"synset_id": "", "description": ""}]
                        })
                        self.stats['sememe_errors'] += 1
                    
                    # Participants 검증
                    participants = sememe.get('participants', [])
                    for participant in participants:
                        # semantic_role 검증
                        semantic_role = participant.get('semantic_role')
                        if semantic_role and not self.is_valid_synset(semantic_role):
                            candidates = self.find_candidates(semantic_role)
                            errors['participants'].append({
                                "synset_id": synset_id,
                                "frame_id": frame_id,
                                "key": "semantic_role",
                                "value": semantic_role,
                                "reasoning": f"semantic_role '{semantic_role}' is not a valid synset in NLTK.",
                                "candidates": candidates if candidates else [{"synset_id": "", "description": ""}]
                            })
                            self.stats['participant_errors'] += 1
                        
                        # value_type 검증
                        value_type = participant.get('value_type')
                        if value_type and not self.is_valid_synset(value_type):
                            candidates = self.find_candidates(value_type)
                            errors['participants'].append({
                                "synset_id": synset_id,
                                "frame_id": frame_id,
                                "key": "value_type",
                                "value": value_type,
                                "reasoning": f"value_type '{value_type}' is not a valid synset in NLTK.",
                                "candidates": candidates if candidates else [{"synset_id": "", "description": ""}]
                            })
                            self.stats['participant_errors'] += 1
            
            # 오류가 있으면 저장
            if errors['sememes'] or errors['participants']:
                output_file = output_path / filepath.name
                # 원본 데이터와 오류 정보를 함께 저장
                result = {
                    'original': data,  # 원본 factorized 데이터
                    'errors': errors   # 검증 오류 정보
                }
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                self.stats['invalid_files'] += 1
                return True
            
            return False
            
        except json.JSONDecodeError:
            return False
        except Exception as e:
            return False
    
    async def process_directory(self, concurrent: int, skip_existing: bool, limit: int):
        """디렉토리의 모든 JSON 파일 처리 (비동기 병렬)"""
        input_path = Path(FACTORIZED_DIR)
        output_path = Path(INVALID_DIR)
        
        if not input_path.exists():
            print(f"✗ 입력 디렉토리를 찾을 수 없습니다: {FACTORIZED_DIR}")
            return
        
        # 출력 디렉토리 생성
        output_path.mkdir(parents=True, exist_ok=True)
        
        # JSON 파일 목록
        json_files = list(input_path.glob('*.json'))
        
        # limit 옵션 적용
        if limit > 0:
            json_files = json_files[:limit]
        
        # skip_existing 옵션 처리
        if skip_existing:
            filtered_files = []
            for filepath in json_files:
                output_file = output_path / filepath.name
                if not output_file.exists():
                    filtered_files.append(filepath)
                else:
                    self.stats['skipped_files'] += 1
            json_files = filtered_files
        
        self.stats['total_files'] = len(json_files)
        
        if skip_existing and self.stats['skipped_files'] > 0:
            print(f"이미 처리된 파일 {self.stats['skipped_files']:,}개 건너뛰기")
        
        if limit > 0:
            print(f"처리 대상: {len(json_files):,}개로 제한")
        
        print(f"\n총 {len(json_files):,}개의 JSON 파일 검증 중 (동시 처리: {concurrent}개)...")
        print("="*60)
        
        # 세마포어로 동시 처리 수 제어
        semaphore = asyncio.Semaphore(concurrent)
        
        async def process_with_semaphore(filepath):
            async with semaphore:
                return await self.validate_json_file(filepath, output_path)
        
        # 프로그레스 바와 함께 비동기 처리
        tasks = []
        with tqdm(total=len(json_files), desc="JSON 파일 검증") as pbar:
            for filepath in json_files:
                task = asyncio.create_task(process_with_semaphore(filepath))
                tasks.append(task)
            
            # 태스크가 완료될 때마다 프로그레스 바 업데이트
            for coro in asyncio.as_completed(tasks):
                await coro
                self.stats['processed_files'] += 1
                pbar.update(1)
        
        print("="*60)
        print("검증 완료!")
    
    def print_stats(self):
        """최종 통계 출력"""
        print("\n========== 검증 결과 ==========")
        print(f"전체 파일: {self.stats['total_files']:,}개")
        if self.stats['skipped_files'] > 0:
            print(f"건너뛴 파일: {self.stats['skipped_files']:,}개")
        print(f"처리한 파일: {self.stats['processed_files']:,}개")
        print(f"오류가 있는 파일: {self.stats['invalid_files']:,}개")
        print(f"Sememe 오류: {self.stats['sememe_errors']:,}개")
        print(f"Participant 오류: {self.stats['participant_errors']:,}개")
        
        if self.stats['invalid_files'] > 0:
            print(f"\n✗ 오류 파일 저장 위치: {INVALID_DIR}")
        else:
            print("\n✓ 모든 파일이 유효합니다!")
        print("==============================")


async def main():
    parser = argparse.ArgumentParser(
        description="Factorized JSON 파일의 synset 참조를 검증하고 후보를 찾습니다."
    )
    parser.add_argument(
        "--concurrent",
        type=int,
        default=10,
        help="동시 처리할 파일 수 (기본값: 10)"
    )
    parser.add_argument(
        "--skip-existing",
        action='store_true',
        help="이미 처리된 파일 건너뛰기"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="처리할 최대 파일 수 (0=전체)"
    )
    args = parser.parse_args()
    
    print("="*60)
    print("GEUL Factorized JSON Synset 검증 및 후보 탐색")
    print("="*60)
    
    validator = SynsetValidator()
    
    try:
        await validator.process_directory(
            args.concurrent,
            args.skip_existing,
            args.limit
        )
        validator.print_stats()
        
    except Exception as e:
        print(f"\n✗ 치명적 오류 발생: {e}")


if __name__ == "__main__":
    asyncio.run(main())