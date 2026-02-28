#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import psycopg2
from pathlib import Path
from tqdm import tqdm
from typing import Dict, Optional
from collections import OrderedDict

# PostgreSQL 연결 설정
DB_CONFIG = {
    'host': 'localhost',
    'database': 'geuldev',
    'user': 'postgres',
    'password': 'test1224!'
}

FACTORIZED_DIR = 'geulso/factorize/factorized/'

class FrameTextUpdater:
    """JSON 파일에 frame_text를 추가하는 클래스"""
    
    def __init__(self, db_config: Dict[str, str]):
        """PostgreSQL 연결 초기화"""
        self.conn = psycopg2.connect(**db_config)
        self.frame_cache = {}  # 성능 향상을 위한 캐시
        self.stats = {
            'total': 0,
            'updated': 0,
            'not_found': 0,
            'error': 0
        }
    
    def load_frame_cache(self):
        """모든 verb frame을 미리 메모리에 로드"""
        print("데이터베이스에서 모든 verb frame 로딩 중...")
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT synset_id, frame_id, frame_text 
                FROM wordnet_verb_frames
            """)
            for synset_id, frame_id, frame_text in cur.fetchall():
                key = (synset_id, frame_id)
                self.frame_cache[key] = frame_text
        print(f"✓ {len(self.frame_cache):,}개의 frame 로드 완료")
    
    def get_frame_text(self, synset_id: str, frame_id: int) -> Optional[str]:
        """캐시에서 frame_text 조회"""
        key = (synset_id, frame_id)
        return self.frame_cache.get(key)
    
    def update_json_file(self, filepath: Path) -> bool:
        """JSON 파일에 frame_text 추가"""
        try:
            # JSON 파일 읽기
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            synset_id = data.get('synset_id')
            frame_id = data.get('frame_id')
            
            if not synset_id or frame_id is None:
                self.stats['error'] += 1
                return False
            
            # 이미 frame_text가 있으면 건너뛰기
            if 'frame_text' in data:
                self.stats['updated'] += 1
                return True
            
            # DB에서 frame_text 조회
            frame_text = self.get_frame_text(synset_id, frame_id)
            
            if frame_text is None:
                self.stats['not_found'] += 1
                print(f"  ⚠ frame_text 없음: {synset_id}, frame_id={frame_id}")
                return False
            
            # frame_id 바로 아래에 frame_text 삽입
            new_data = OrderedDict()
            for key, value in data.items():
                new_data[key] = value
                if key == 'frame_id':
                    new_data['frame_text'] = frame_text
            
            # JSON 파일에 저장 (들여쓰기 유지)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, indent=2, ensure_ascii=False)
            
            self.stats['updated'] += 1
            return True
            
        except json.JSONDecodeError as e:
            print(f"  ✗ JSON 파싱 오류: {filepath.name} - {e}")
            self.stats['error'] += 1
            return False
        except Exception as e:
            print(f"  ✗ 파일 처리 오류: {filepath.name} - {e}")
            self.stats['error'] += 1
            return False
    
    def process_directory(self, directory: str):
        """디렉토리의 모든 JSON 파일 처리"""
        dir_path = Path(directory)
        
        if not dir_path.exists():
            print(f"✗ 디렉토리를 찾을 수 없습니다: {directory}")
            return
        
        # JSON 파일 목록 가져오기
        json_files = list(dir_path.glob('*.json'))
        self.stats['total'] = len(json_files)
        
        print(f"\n총 {len(json_files):,}개의 JSON 파일 발견")
        print("="*60)
        
        # 프로그레스 바와 함께 파일 처리
        with tqdm(total=len(json_files), desc="JSON 파일 업데이트 중") as pbar:
            for filepath in json_files:
                self.update_json_file(filepath)
                pbar.update(1)
        
        print("="*60)
        print("처리 완료!")
    
    def print_stats(self):
        """최종 통계 출력"""
        print("\n========== 처리 결과 ==========")
        print(f"전체 파일: {self.stats['total']:,}개")
        print(f"업데이트 성공: {self.stats['updated']:,}개")
        print(f"frame_text 없음: {self.stats['not_found']:,}개")
        print(f"오류: {self.stats['error']:,}개")
        print("==============================")
    
    def close(self):
        """데이터베이스 연결 종료"""
        self.conn.close()


def main():
    print("="*60)
    print("GEUL JSON 파일에 frame_text 추가")
    print("="*60)
    
    updater = FrameTextUpdater(DB_CONFIG)
    
    try:
        # 모든 frame을 먼저 캐시에 로드 (성능 향상)
        updater.load_frame_cache()
        
        # 디렉토리의 모든 JSON 파일 처리
        updater.process_directory(FACTORIZED_DIR)
        
        # 통계 출력
        updater.print_stats()
        
    except Exception as e:
        print(f"\n✗ 치명적 오류 발생: {e}")
        
    finally:
        updater.close()
        print("\n데이터베이스 연결 종료.")


if __name__ == "__main__":
    main()