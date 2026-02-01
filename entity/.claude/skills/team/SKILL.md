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

## 현재 진행 상황

- [x] Stage 1 완료 (63개 타입 분석)
- [x] Stage 2 완료 (5개 타입, 298개 DAG 엣지)
- [x] Stage 3 완료 (5개 타입 비트 할당)
- [x] Stage 4 완료 (43,439개 코드북)
- [x] Stage 5 완료 (33% 통과, 열화 테스트 100%)

## Phase 상태

- [x] **Phase 1**: 준비 (스크립트 수정)
- [x] **Phase 2**: 파일럿 실행 (5개 타입)
- [x] **Phase 2.5**: 최적화 (OPT-1~4)
- [ ] **Phase 3**: 재검증 및 튜닝
- [ ] **Phase 4**: 전체 타입 확장

## 보고서

| 파일 | 내용 |
|------|------|
| reports/00_executive_summary.md | 종합 요약 (1페이지) |
| reports/01_architect_report.md | 설계 결정 |
| reports/02_analyst_report.md | 데이터 분석 |
| reports/03_builder_report.md | 구현 결과 |
| reports/04_ontologist_report.md | 분류 체계 검증 |
