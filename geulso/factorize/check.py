#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GEUL 동사 의미소 분해(Factorized) JSON 파일 검증 스크립트

41,000+개의 AI 생성 JSON 파일을 'factorize_prompt.json'의 명세를 기준으로 검증합니다.
- 'sememes'가 리스트가 아닌 경우: 자동으로 []로 교정하여 원본 파일 덮어쓰기
- 기타 오류가 발견된 파일: 'OUTPUT_DIR'에 "errors" 필드가 추가된 채로 복사
- verb_type + verb_property 조합 통계를 수집하여 verb_types.json에 저장
"""

import json
import os
from pathlib import Path
import shutil
from tqdm import tqdm
from typing import Dict, Any, Set, List, Union, Tuple
from collections import defaultdict

# --- 설정 ---
# 원본 Factorized JSON 파일이 있는 디렉터리
SOURCE_DIR = Path("geulso/factorize/corrected")

# 오류가 발견된 JSON을 저장할 디렉터리
OUTPUT_DIR = Path("geulso/factorize/checked")

# 유효성 검사의 기준이 되는 프롬프트 파일
PROMPT_FILE = Path("geulso/factorize/factorize_prompt.json")

# verb_type 통계 저장 파일
VERB_TYPES_STATS_FILE = OUTPUT_DIR / "_verb_stats.json"
# --- 설정 끝 ---


def load_validation_rules(prompt_path: Path) -> Dict[str, Set[Union[int, float, str]]]:
    """
    factorize_prompt.json 파일을 로드하여
    Qualifier의 유효성 검사 규칙(허용된 값)을 생성합니다.
    """
    if not prompt_path.exists():
        print(f"오류: 프롬프트 파일 '{prompt_path}'를 찾을 수 없습니다.")
        return {}

    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_data = json.load(f)
    
    spec = prompt_data.get("qualifier_specification", {})
    rules = {}
    
    for q_name, q_spec in spec.items():
        allowed_values = set()
        for v_str in q_spec.get("values", {}).keys():
            try:
                # 문자열 값 (예: "MAX-1", "MAX")
                if not v_str.replace('.', '').replace('-', '').isdigit():
                    allowed_values.add(v_str)
                # 정수 시도 (예: "1")
                elif '.' not in v_str:
                    val = int(v_str)
                    allowed_values.add(val)
                    allowed_values.add(float(val))  # 1과 1.0을 동일하게 처리
                else:
                    # 실수 시도 (예: "-1.0")
                    val = float(v_str)
                    allowed_values.add(val)
                    if val.is_integer():
                        allowed_values.add(int(val))  # 1.0과 1을 동일하게 처리
            except ValueError:
                # 문자열로 처리
                allowed_values.add(v_str)
        rules[q_name] = allowed_values
    
    print(f"유효성 검사 규칙 로드 완료. {len(rules)}개 Qualifier 명세 확인.")
    return rules


def check_json_file(
    file_path: Path, 
    rules: Dict[str, Set[Union[int, float, str]]],
    verb_type_stats: Dict[Tuple[str, str], int]
) -> tuple[List[str], bool, Dict]:
    """
    단일 JSON 파일을 로드하고 모든 유효성 검사를 수행합니다.
    
    Args:
        file_path: 검사할 파일 경로
        rules: 유효성 검사 규칙
        verb_type_stats: (verb_type, verb_property) 튜플을 키로 하는 통계 딕셔너리 (참조로 전달)
    
    Returns:
        (errors, needs_sememes_correction, content)
        - errors: 오류 문자열 리스트
        - needs_sememes_correction: sememes를 []로 교정해야 하는지 여부
        - content: JSON 내용
    """
    errors = []
    needs_sememes_correction = False
    content = None

    # 1. JSON 파싱 오류 검사
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = json.load(f)
    except json.JSONDecodeError as e:
        return ([f"JSON 파싱 오류: {e}"], False, None)
    except Exception as e:
        return ([f"파일 읽기 오류: {e}"], False, None)

    # 2. 필수 최상위 키 검사
    required_top_keys = {"synset_id", "definition", "frame_id", "frame_text", "sememes", "qualifiers"}
    missing_top_keys = required_top_keys - set(content.keys())
    if missing_top_keys:
        errors.append(f"필수 최상위 키 누락: {sorted(missing_top_keys)}")

    # 3. 'sememes' 구조 검사
    sememes = content.get("sememes")
    if not isinstance(sememes, list):
        # sememes가 리스트가 아니면 교정 플래그 설정
        needs_sememes_correction = True
        # 객체인 경우 통계 수집 (교정 전)
        if isinstance(sememes, dict):
            verb_type = sememes.get("verb_type", "unknown")
            verb_property = sememes.get("verb_property", None)
            
            # verb_type이 dict나 list인 경우 문자열로 변환
            if isinstance(verb_type, (dict, list)):
                verb_type = str(verb_type)
            elif verb_type is None:
                verb_type = "unknown"
            
            # verb_property가 dict나 list인 경우 문자열로 변환
            if isinstance(verb_property, (dict, list)):
                verb_property = str(verb_property)
            
            key = (verb_type, verb_property)
            verb_type_stats[key] += 1
    elif not sememes:
        errors.append("`sememes` 리스트가 비어 있습니다.")
    else:
        # sememes가 정상 리스트인 경우에만 내부 검사
        for i, sememe in enumerate(sememes):
            if not isinstance(sememe, dict):
                errors.append(f"`sememes[{i}]`가 객체(dict)가 아닙니다.")
                continue
            
            # verb_type 검사 및 통계 수집
            if "verb_type" not in sememe:
                errors.append(f"`sememes[{i}]`에 'verb_type' 키 누락")
            else:
                verb_type = sememe.get("verb_type")
                verb_property = sememe.get("verb_property", None)
                
                # verb_type이 dict나 list인 경우 문자열로 변환 (해시 가능하게)
                if isinstance(verb_type, (dict, list)):
                    verb_type = str(verb_type)
                elif verb_type is None:
                    verb_type = "unknown"
                
                # verb_property가 dict나 list인 경우 문자열로 변환 (해시 가능하게)
                if isinstance(verb_property, (dict, list)):
                    verb_property = str(verb_property)
                
                # 통계 수집: (verb_type, verb_property) 튜플을 키로 사용
                key = (verb_type, verb_property)
                verb_type_stats[key] += 1
                
                # change/state가 원칙이지만 action/property 등도 허용
                valid_verb_types = {"change", "state", "action", "property"}
                if verb_type not in valid_verb_types:
                    errors.append(
                        f"`sememes[{i}].verb_type`의 값 '{verb_type}'가 "
                        f"일반적인 값({valid_verb_types})이 아닙니다. (경고)"
                    )
            
            # reasoning 검사
            if "reasoning" not in sememe:
                errors.append(f"`sememes[{i}]`에 'reasoning' 키 누락")
            
            # participants 검사 (있는 경우만)
            if "participants" in sememe:
                if not isinstance(sememe["participants"], list):
                    errors.append(f"`sememes[{i}].participants`가 리스트가 아닙니다.")
                else:
                    # participants 내부 구조 검사
                    for j, participant in enumerate(sememe["participants"]):
                        if not isinstance(participant, dict):
                            errors.append(f"`sememes[{i}].participants[{j}]`가 객체(dict)가 아닙니다.")
                            continue
                        
                        if "semantic_role" not in participant:
                            errors.append(f"`sememes[{i}].participants[{j}]`에 'semantic_role' 키 누락")
                        
                        if "reasoning" not in participant:
                            errors.append(f"`sememes[{i}].participants[{j}]`에 'reasoning' 키 누락")

    # 4. 'qualifiers' 구조 검사
    qualifiers = content.get("qualifiers")
    valid_qualifier_names = set(rules.keys())
    
    if isinstance(qualifiers, dict):
        present_qualifier_names = set(qualifiers.keys())
        
        # 5. 알 수 없는 Qualifier 검사
        unknown_qualifiers = present_qualifier_names - valid_qualifier_names
        if unknown_qualifiers:
            errors.append(f"알 수 없는 Qualifier 키 포함: {sorted(unknown_qualifiers)}")

        # 6. 각 Qualifier의 값과 구조 검사
        for q_name, q_data in qualifiers.items():
            if q_name not in valid_qualifier_names:
                continue  # 이미 "알 수 없는 Qualifier"로 처리됨

            if not isinstance(q_data, dict):
                errors.append(f"`qualifiers.{q_name}`이 객체(dict)가 아닙니다.")
                continue

            # 6a. 'value', 'reasoning' 키 존재 여부
            if "value" not in q_data:
                errors.append(f"`qualifiers.{q_name}`에 'value' 키 누락")
            if "reasoning" not in q_data:
                errors.append(f"`qualifiers.{q_name}`에 'reasoning' 키 누락")

            # 6b. 'value' 값 유효성 검사
            if "value" in q_data:
                q_value = q_data["value"]
                allowed_values = rules.get(q_name)
                
                # 빈 values (예: Period/Point)는 검사하지 않음
                if allowed_values and q_value not in allowed_values:
                    errors.append(
                        f"`qualifiers.{q_name}`의 'value'({q_value}, 타입: {type(q_value).__name__})가 "
                        f"허용된 값 목록에 없습니다."
                    )
    else:
        errors.append("`qualifiers`가 객체(dict)가 아닙니다.")

    return (errors, needs_sememes_correction, content)


def save_verb_type_stats(stats: Dict[Tuple[str, str], int], output_path: Path):
    """
    verb_type + verb_property 조합 통계를 JSON 파일로 저장합니다.
    """
    # 카운트 기준 내림차순 정렬
    sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
    
    # JSON 배열 형식으로 변환
    stats_list = [
        {
            "verb_type": verb_type,
            "verb_property": verb_property,
            "count": count
        }
        for (verb_type, verb_property), count in sorted_stats
    ]
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(stats_list, f, indent=2, ensure_ascii=False)
        print(f"\n✓ verb_type 통계가 '{output_path}'에 저장되었습니다.")
    except Exception as e:
        print(f"\n✗ verb_type 통계 저장 중 오류: {e}")


def main():
    """
    메인 실행 함수
    """
    print("========== GEUL 동사 의미소 분해 JSON 검증 시작 ==========\n")
    
    # 0. 규칙 로드
    validation_rules = load_validation_rules(PROMPT_FILE)
    if not validation_rules:
        print("유효성 검사 규칙을 로드할 수 없어 스크립트를 종료합니다.")
        return

    # 1. 소스 파일 목록 가져오기
    if not SOURCE_DIR.is_dir():
        print(f"오류: 소스 디렉터리 '{SOURCE_DIR}'를 찾을 수 없습니다.")
        print("스크립트 상단의 'SOURCE_DIR' 변수를 수정해주세요.")
        print(f"현재 작업 디렉터리: {Path.cwd()}")
        return
        
    print(f"소스 디렉터리: '{SOURCE_DIR}'")
    all_files = list(SOURCE_DIR.glob("*.json"))
    
    if not all_files:
        print(f"경고: '{SOURCE_DIR}'에 .json 파일이 없습니다.")
        return
    
    print(f"총 {len(all_files):,}개의 .json 파일 발견")

    # 2. 출력 디렉터리 생성
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"오류 파일 저장 경로: '{OUTPUT_DIR}'\n")

    # 3. verb_type + verb_property 통계 초기화
    verb_type_stats = defaultdict(int)

    # 4. 파일 검증 및 처리
    error_file_count = 0
    corrected_file_count = 0
    total_error_count = 0
    error_files_list = []
    
    for file_path in tqdm(all_files, desc="파일 검증 중"):
        errors, needs_correction, content = check_json_file(file_path, validation_rules, verb_type_stats)
        
        # sememes 교정이 필요한 경우
        if needs_correction and content is not None:
            try:
                sememes_value = content.get("sememes")
                # sememes가 객체(dict)면 배열로 감싸고, 그 외(None, 문자열 등)는 빈 배열
                if isinstance(sememes_value, dict):
                    content["sememes"] = [sememes_value]
                else:
                    content["sememes"] = []
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(content, f, indent=2, ensure_ascii=False)
                corrected_file_count += 1
            except Exception as e:
                tqdm.write(f"\n파일 '{file_path.name}' 교정 중 오류: {e}")
        
        # 기타 오류가 있는 경우 (sememes 교정 제외)
        elif errors:
            error_file_count += 1
            total_error_count += len(errors)
            error_files_list.append((file_path.name, errors))
            
            # 오류 파일을 'checked' 디렉터리로 복사하고 "errors" 키 추가
            try:
                if content is None:
                    # 파싱 오류로 content를 읽을 수 없는 경우 원본 복사
                    output_path = OUTPUT_DIR / file_path.name
                    shutil.copy2(file_path, output_path)
                else:
                    content["errors"] = errors
                    output_path = OUTPUT_DIR / file_path.name
                    
                    with open(output_path, 'w', encoding='utf-8') as f_out:
                        json.dump(content, f_out, indent=2, ensure_ascii=False)
                    
            except Exception as e:
                tqdm.write(f"\n오류 파일 '{file_path.name}' 저장 중 예외 발생: {e}")

    # 5. verb_type 통계 저장
    save_verb_type_stats(verb_type_stats, VERB_TYPES_STATS_FILE)

    # 6. 최종 결과 요약
    print("\n========== 검증 완료 ==========")
    print(f"총 검사 파일: {len(all_files):,}개")
    print(f"sememes 자동 교정: {corrected_file_count:,}개")
    print(f"오류가 발견된 파일: {error_file_count:,}개")
    print(f"총 발견된 오류 수: {total_error_count:,}개")
    
    # verb_type 통계 간단 요약
    if verb_type_stats:
        total_sememes = sum(verb_type_stats.values())
        print(f"\nverb_type + verb_property 조합 통계 (총 {total_sememes:,}개 sememe):")
        sorted_types = sorted(verb_type_stats.items(), key=lambda x: x[1], reverse=True)
        for (verb_type, verb_property), count in sorted_types[:10]:  # 상위 10개만 표시
            prop_str = verb_property if verb_property else "(없음)"
            print(f"  - {verb_type} + {prop_str}: {count:,}개")
        if len(sorted_types) > 10:
            print(f"  ... 외 {len(sorted_types) - 10}개 조합")
    
    if corrected_file_count > 0:
        print(f"\n✓ {corrected_file_count:,}개 파일의 sememes를 배열로 교정하여 '{SOURCE_DIR}'에 덮어썼습니다.")
    
    if error_file_count > 0:
        print(f"\n✗ {error_file_count:,}개 오류 파일이 '{OUTPUT_DIR}'에 저장되었습니다.")
        print("\n오류 파일 샘플 (최대 5개):")
        for filename, errors in error_files_list[:5]:
            print(f"\n  파일: {filename}")
            for err in errors[:3]:  # 파일당 최대 3개 오류만 표시
                print(f"    - {err}")
            if len(errors) > 3:
                print(f"    ... 외 {len(errors) - 3}개 오류")
    else:
        print("\n✓ 모든 파일이 유효성 검사를 통과했습니다!")
    
    print("==============================")


if __name__ == "__main__":
    main()