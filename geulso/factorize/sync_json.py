#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shutil
from pathlib import Path
from tqdm import tqdm

# --- 설정 ---
# 'factorized' JSON 파일이 있는 소스 디렉터리
FACTORIZED_DIR = Path('geulso/factorize/factorized/')

# 'corrected' JSON 파일을 저장할 대상 디렉터리
CORRECTED_DIR = Path('geulso/factorize/corrected/')
# --- 설정 끝 ---

def sync_missing_files(src_dir: Path, dest_dir: Path):
    """
    src_dir에 있지만 dest_dir에는 없는 .json 파일을 찾아
    dest_dir로 복사합니다.
    """
    
    print(f"소스 디렉터리: {src_dir}")
    print(f"대상 디렉터리: {dest_dir}")
    
    # 0. 소스 디렉터리 존재 확인
    if not src_dir.exists():
        print(f"오류: 소스 디렉터리 '{src_dir}'를 찾을 수 없습니다.")
        return
    
    if not src_dir.is_dir():
        print(f"오류: '{src_dir}'는 디렉터리가 아닙니다.")
        return
    
    # 1. 대상 디렉터리가 없으면 생성합니다.
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    # 2. 소스 디렉터리에서 .json 파일 목록을 스캔합니다. (파일명만 Set으로 저장)
    print(f"'{src_dir}' 스캔 중...")
    src_files = {p.name for p in src_dir.glob('*.json') if p.is_file()}
    print(f" -> {len(src_files):,}개의 .json 파일 발견")
    
    if not src_files:
        print(f"경고: '{src_dir}'에 .json 파일이 없습니다.")
        return

    # 3. 대상 디렉터리에서 .json 파일 목록을 스캔합니다. (파일명만 Set으로 저장)
    print(f"'{dest_dir}' 스캔 중...")
    dest_files = {p.name for p in dest_dir.glob('*.json') if p.is_file()}
    print(f" -> {len(dest_files):,}개의 .json 파일 발견")

    # 4. 차집합을 구해 복사할 파일 목록을 찾습니다.
    files_to_copy = src_files - dest_files
    
    if not files_to_copy:
        print("\n✓ 모든 파일이 동기화되었습니다. 새로 복사할 파일이 없습니다.")
        return

    print(f"\n총 {len(files_to_copy):,}개의 새 파일을 '{dest_dir}'로 복사합니다.")

    # 5. 파일 복사 실행
    copied_count = 0
    errors = []
    
    for filename in tqdm(sorted(list(files_to_copy)), desc="파일 복사 중"):
        src_path = src_dir / filename
        dest_path = dest_dir / filename
        
        try:
            # copy2를 사용해 메타데이터(수정 시간 등)도 함께 복사
            shutil.copy2(src_path, dest_path)
            copied_count += 1
        except Exception as e:
            tqdm.write(f"\n'{filename}' 복사 중 오류 발생: {e}")
            errors.append((filename, e))

    # 6. 최종 결과 보고
    print("\n========== 작업 완료 ==========")
    print(f"✓ 성공: {copied_count:,}개 파일 복사 완료")
    if errors:
        print(f"✗ 실패: {len(errors):,}개 파일 복사 실패")
        # (디버깅을 위해 실패한 파일 목록 5개만 출력)
        for fname, err in errors[:5]:
            print(f"  - {fname}: {err}")
    print("==============================")

if __name__ == "__main__":
    print("========== JSON 파일 동기화 시작 ==========\n")
    
    if not FACTORIZED_DIR.is_dir():
        print(f"오류: '{FACTORIZED_DIR}' 디렉터리를 찾을 수 없습니다.")
        print("FACTORIZED_DIR 변수의 경로를 올바르게 수정해주세요.")
        print(f"\n현재 작업 디렉터리: {Path.cwd()}")
    else:
        sync_missing_files(FACTORIZED_DIR, CORRECTED_DIR)