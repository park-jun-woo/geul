---
name: team
description: GEUL Entity 개발팀 구성, 역할, 워크플로우 확인. 팀 현황 및 진행 상황 조회.
---

# GEUL Entity Node 개발팀

## 팀 구성 (5인)

| 역할 | 스킬 | 핵심 책임 |
|------|------|-----------|
| **Architect** | `/architect` | 설계 결정, 트레이드오프, 사용자 토론 |
| **Analyst** | `/analyst` | 데이터 분석, 통계, 의존성 탐지 |
| **Builder** | `/builder` | 스크립트 구현, 파이프라인 실행 |
| **Ontologist** | `/ontologist` | 분류 체계 검증, 경계 사례 판단 |
| **DBA** | `/dba` | DB 성능 분석, 인덱스 최적화, 충돌 비용 모델 |

## 워크플로우

```
User (승인권자)
    ↓
Architect ←→ Ontologist (분류 검토)
    ↓
Analyst (데이터 분석) ←→ DBA (성능 분석)
    ↓
Builder (구현/실행)
    ↓
Architect (결과 검토) → User (최종 승인)
```

## 의사결정 프로세스

1. **설계 이슈 발생** → Architect 주도
2. **분류 관련 질문** → Ontologist 자문
3. **데이터 필요** → Analyst 분석
4. **성능/인덱스 이슈** → DBA 분석
5. **구현 필요** → Builder 실행
6. **결과 검토** → Architect → User 승인

## 파이프라인 단계별 담당

| Stage | 주담당 | 보조 |
|-------|--------|------|
| Stage 1: 속성 추출 | Analyst | Builder |
| Stage 2: 의존성 탐지 | Analyst | Ontologist |
| Stage 3: 비트 할당 | Architect | Analyst, DBA |
| Stage 4: 코드북 생성 | Builder | Ontologist |
| Stage 5: 검증 | Builder | Analyst, DBA |

## 현재 진행 상황 (2026-02-01)

| 항목 | 수치 |
|------|------|
| 위키데이터 전체 개체 | 117,419,925 |
| Wikimedia 내부 제외 | 8,565,353 (7.3%) |
| SIDX 대상 개체 | 108,854,572 (92.7%) |
| 64개 타입 직접 커버 | 36,295,074 (33.3%) |
| 하위 타입 매핑 흡수 | 71,842,429 (66.0%) |
| Other 폴백 | 717,069 (0.7%) |
| **최종 커버리지** | **100%** |
| 충돌률 | < 0.01% |

### Stage 완료 현황
- [x] Stage 1 완료 (64개 타입 분석)
- [x] Stage 2 완료 (의존성 DAG)
- [x] Stage 3 완료 (48비트 할당)
- [x] Stage 4 완료 (스키마 문서화)
- [x] Stage 5 완료 (검증 통과)

## Phase 상태

- [x] **Phase 1**: 준비 (스크립트 수정)
- [x] **Phase 2**: 파일럿 실행 (5개 타입)
- [x] **Phase 2.5**: 최적화 (OPT-1~4)
- [x] **Phase 4**: 전체 타입 확장
- [x] **Phase 5**: 코드북 상세 생성 ← **완료**
- [ ] **Phase 6**: 인코더 프로토타입
- [ ] **Phase 7**: 운영 검증

## 주요 산출물

| 파일 | 내용 |
|------|------|
| references/type_schemas.json | 64개 타입 48비트 스키마 (v1.0) |
| references/entity_types_64.json | 64개 EntityType 정의 |
| references/category_templates.json | 9개 카테고리 템플릿 |
| references/primary_mapping.json | P31→EntityType 매핑 (63+52개) |
| references/codebooks.json | 6개 코드북 (country, occupation 등) |
| references/encoder_spec.md | 인코더 로직 설계서 |
| output/phase4_final_report.md | Phase 4 최종 보고서 |

## 보고서 (finished/)

| 파일 | 내용 |
|------|------|
| finished/reports/00_executive_summary.md | 종합 요약 |
| finished/reports/01_architect_report.md | 설계 결정 |
| finished/reports/02_analyst_report.md | 데이터 분석 |
| finished/reports/03_builder_report.md | 구현 결과 |
| finished/reports/04_ontologist_report.md | 분류 체계 검증 |

## DB 접속 주의

**psql 사용 불가** - Python psycopg2 사용 (.venv 활성화 필요)

```bash
source .venv/bin/activate
python3 -c "
import psycopg2
conn = psycopg2.connect('postgresql://geul_reader:test1224@localhost:5432/geuldev')
cur = conn.cursor()
cur.execute('SELECT COUNT(*) FROM entities')
print(cur.fetchone()[0])
"
```
