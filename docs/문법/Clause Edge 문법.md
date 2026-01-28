# Clause Edge 명세서

**버전:** v0.2  
**작성일:** 2026-01-28  
**목적:** GEUL 서술/사건 간 논리적 관계 표현을 위한 Clause Edge 구조 정의

---

## 1. 개요

Clause Edge는 서술(Verb Edge), 사건(Event6), 관계(Triple), 또는 다른 Clause 간의 **논리적/담화적 관계**를 표현하는 Edge 타입이다.

RST(Rhetorical Structure Theory)의 담화 관계를 기반으로 설계되었다.

---

## 2. 연결 대상

Clause Edge는 TID를 통해 다양한 Edge 타입을 연결할 수 있다.

| TID 타입 | 설명 | 연결 가능 |
|----------|------|-----------|
| Entity | 개체 | △ (제한적) |
| Verb Edge | 서술 | ✓ |
| Triple Edge | 속성/관계 | ✓ |
| Clause Edge | 복합 절 | ✓ (중첩) |
| Event6 Edge | 6하원칙 사건 | ✓ |
| Context Edge | 맥락 | △ |
| Inner Edge | 내부 수식 | △ |

**TID 체계:** 16비트 통합 풀 (65,536개). 타입 비트 없이 WMS가 TID→타입 매핑 관리.

---

## 3. 관계 타입 (4비트 = 16개)

RST(Rhetorical Structure Theory) 기반 담화 관계:

### 3.1 인과 관계

| 코드 | 타입 | 설명 | 예시 |
|------|------|------|------|
| 0000 | CAUSE | 원인→결과 | "비가 와서 집에 있었다" |
| 0001 | RESULT | 결과←원인 | "집에 있었다, 비가 왔기에" |
| 0010 | CONDITION | 조건→귀결 | "비가 오면 안 간다" |
| 0011 | PURPOSE | 목적 | "살기 위해 먹는다" |

### 3.2 시간/순서 관계

| 코드 | 타입 | 설명 | 예시 |
|------|------|------|------|
| 0100 | SEQUENCE | 시간순 | "밥 먹고 잤다" |
| 0101 | PARALLEL | 동시/병렬 | "웃으면서 말했다" |

### 3.3 대조/양보 관계

| 코드 | 타입 | 설명 | 예시 |
|------|------|------|------|
| 0110 | CONTRAST | 대조 | "A는 크고 B는 작다" |
| 0111 | CONCESSION | 양보 | "어렵지만 했다" |

### 3.4 부연/배경 관계

| 코드 | 타입 | 설명 | 예시 |
|------|------|------|------|
| 1000 | ELABORATION | 상세화 | "구체적으로 말하면" |
| 1001 | BACKGROUND | 배경 정보 | "참고로, 당시 상황은" |

### 3.5 논증 관계

| 코드 | 타입 | 설명 | 예시 |
|------|------|------|------|
| 1010 | EVIDENCE | 증거 제시 | "왜냐하면... 때문이다" |
| 1011 | EVALUATION | 평가 | "이것은 좋다/나쁘다" |

### 3.6 기타 관계

| 코드 | 타입 | 설명 | 예시 |
|------|------|------|------|
| 1100 | SOLUTIONHOOD | 문제→해결 | "문제는 X, 해결책은 Y" |
| 1101 | ALTERNATIVE | 선택/대안 | "가거나 말거나" |
| 1110 | MEANS | 수단 | "이렇게 해서 달성했다" |
| 1111 | RESERVED | 예약 | 미래 확장용 |

---

## 4. Clause Edge 구조

### 4.1 패킷 구조

```
Clause Edge: 16비트 (1워드)
┌──────────────┬──────────────┐
│   관계타입    │     예약     │
│    4비트     │    12비트    │
└──────────────┴──────────────┘

+ Edge TID 선언: 1워드 (16비트)
+ TID 1: 1워드 (16비트) - 첫 번째 절
+ TID 2: 1워드 (16비트) - 두 번째 절

총: 4워드 (64비트)
```

### 4.2 필드 설명

| 필드 | 비트 | 설명 |
|------|------|------|
| 관계타입 | 4 | 16개 RST 관계 |
| 예약 | 12 | 미래 확장용 |

### 4.3 TID 순서 규칙

방향은 TID 순서로 결정:

| 관계 | TID 1 | TID 2 |
|------|-------|-------|
| CAUSE | 원인 | 결과 |
| RESULT | 결과 | 원인 |
| CONDITION | 조건 | 귀결 |
| PURPOSE | 행위 | 목적 |
| SEQUENCE | 선행 | 후행 |
| EVIDENCE | 증거 | 주장 |
| ELABORATION | 핵심 | 부연 |

### 4.4 패킷 레이아웃

```
[Clause Edge 1워드] - 관계타입 + 예약
[Edge TID 1워드]    - 이 Edge의 TID 선언
[TID 1 1워드]       - 첫 번째 절
[TID 2 1워드]       - 두 번째 절
───────────────────
총: 4워드 (64비트)
```

---

## 5. 예시

### 5.1 단순 인과

**"비가 와서 집에 있었다"**

```
Verb Edge E01: rain(비) | TID=0x0001
Verb Edge E02: stay(나, 집) | TID=0x0002

Clause Edge:
  [CAUSE | 예약]     - 1워드
  [TID: 0x0100]      - 1워드 (이 Edge의 TID)
  [TID 1: 0x0001]    - 1워드 (원인: E01)
  [TID 2: 0x0002]    - 1워드 (결과: E02)
```

### 5.2 조건문

**"비가 오면 안 간다"**

```
Verb Edge E01: rain(비) | TID=0x0001
Verb Edge E02: go(나) [Polarity=부정] | TID=0x0002

Clause Edge:
  [CONDITION | 예약]
  [TID: 0x0101]
  [TID 1: 0x0001]    - 조건: E01
  [TID 2: 0x0002]    - 귀결: E02
```

### 5.3 Triple 연결

**"철수가 CEO이기 때문에 결정했다"**

```
Triple T01: (철수, is_a, CEO) | TID=0x0010
Verb Edge E01: decide(철수, ...) | TID=0x0001

Clause Edge:
  [CAUSE | 예약]
  [TID: 0x0102]
  [TID 1: 0x0010]    - 원인: Triple
  [TID 2: 0x0001]    - 결과: Verb Edge
```

### 5.4 Event6 연결

**"애플이 테슬라를 인수해서 주가가 올랐다"**

```
Event6 E01: (Apple, acquire, Tesla, $2B, 2025-03-15) | TID=0x0020
Verb Edge E02: rise(주가) | TID=0x0002

Clause Edge:
  [CAUSE | 예약]
  [TID: 0x0103]
  [TID 1: 0x0020]    - 원인: Event6
  [TID 2: 0x0002]    - 결과: Verb Edge
```

### 5.5 중첩 Clause

**"비가 와서 집에 있었고, 그래서 공부했다"**

```
Verb Edge E01: rain(비) | TID=0x0001
Verb Edge E02: stay(나, 집) | TID=0x0002
Verb Edge E03: study(나) | TID=0x0003

Clause Edge C01:
  [CAUSE | 예약]
  [TID: 0x0100]
  [TID 1: 0x0001]    - E01
  [TID 2: 0x0002]    - E02

Clause Edge C02:
  [RESULT | 예약]
  [TID: 0x0101]
  [TID 1: 0x0100]    - C01 (Clause TID 참조!)
  [TID 2: 0x0003]    - E03
```

### 5.6 복합 논증

**"A이고 B이므로 C이다"**

```
Verb Edge E01: A | TID=0x0001
Verb Edge E02: B | TID=0x0002
Verb Edge E03: C | TID=0x0003

Clause Edge C01:
  [PARALLEL | 예약]
  [TID: 0x0100]
  [TID 1: 0x0001]    - E01
  [TID 2: 0x0002]    - E02

Clause Edge C02:
  [EVIDENCE | 예약]
  [TID: 0x0101]
  [TID 1: 0x0100]    - C01 (증거)
  [TID 2: 0x0003]    - E03 (주장)
```

---

## 6. Multinuclear vs Nucleus-Satellite

RST 구분을 따름:

### 6.1 Nucleus-Satellite (비대칭)

| 관계 | TID 1 | TID 2 |
|------|-------|-------|
| CAUSE | 원인 (Satellite) | 결과 (Nucleus) |
| CONDITION | 조건 (Satellite) | 귀결 (Nucleus) |
| EVIDENCE | 증거 (Satellite) | 주장 (Nucleus) |
| ELABORATION | 핵심 (Nucleus) | 부연 (Satellite) |

### 6.2 Multinuclear (대칭)

| 관계 | TID 1 | TID 2 |
|------|-------|-------|
| SEQUENCE | 선행 | 후행 |
| PARALLEL | 첫 번째 | 두 번째 |
| CONTRAST | 첫 번째 | 두 번째 |
| ALTERNATIVE | 첫 번째 | 두 번째 |

**대칭 관계는 TID 순서가 의미적 우선순위가 아님.**

---

## 7. WMS 저장 구조

### 7.1 인덱싱

```sql
CREATE TABLE clause_edges (
    edge_tid INTEGER PRIMARY KEY,    -- 16비트
    relation_type SMALLINT,          -- 4비트 (0-15)
    tid_1 INTEGER,                   -- 16비트
    tid_2 INTEGER,                   -- 16비트
    created_at TIMESTAMP
);

CREATE INDEX idx_tid1 ON clause_edges(tid_1);
CREATE INDEX idx_tid2 ON clause_edges(tid_2);
CREATE INDEX idx_relation ON clause_edges(relation_type);
```

### 7.2 그래프 탐색

```
GEUL-Path 예시:
/Event6[0x0020]/->CAUSE/->*
  → 0x0020에서 CAUSE로 연결된 모든 노드

/VerbEdge[0x0002]/<-CONDITION
  → 0x0002를 TID 2로 가지는 CONDITION의 TID 1
```

---

## 8. 설계 근거

### 8.1 RST 기반 이유

- 30년+ 연구 축적
- 다양한 코퍼스 검증
- 담화 파싱 도구 존재
- 언어 독립적

### 8.2 4비트(16개) 이유

- RST 핵심 관계 12개+
- 확장 여유 확보
- 3비트(8개)는 부족

### 8.3 16비트 간소화 이유

- 방향: TID 순서로 결정 (별도 비트 불필요)
- 확신도: 별도 메타데이터로 처리
- 12비트 예약: 향후 확장

### 8.4 TID 통합 풀 이유

- 65,536개 충분
- 타입 비트 불필요
- WMS lookup으로 타입 확인

---

## 9. GEUL 생태계 내 위치

```
GEUL Edge 체계:

지식/개체:
├── Entity (개체 선언)
└── Triple Edge (속성/관계)

서술/사건:
├── Verb Edge (서술)
├── Verb Inner Edge (내부 수식)
└── Event6 Edge (6하원칙 사건)

논리/담화:
└── Clause Edge (절 관계) ← 이 문서

맥락:
└── Context Edge (출처/신뢰도)
```

---

## 10. 버전 히스토리

| 버전 | 날짜 | 변경 |
|------|------|------|
| v0.1 | 2026-01-27 | 초안 (5워드) |
| v0.2 | 2026-01-28 | 4워드로 간소화, 방향/확신도 제거 |

---

## 11. 향후 과제

- [ ] 3개 이상 노드 연결 (예: A이고 B이고 C이므로 D)
- [ ] GEUL-Path 쿼리 문법 정의
- [ ] 담화 파싱 → Clause Edge 자동 생성

---

## 12. 참고 문헌

- Mann, W.C. & Thompson, S.A. (1988). Rhetorical Structure Theory
- Carlson, L., Marcu, D., & Okurowski, M.E. (2003). RST Discourse Treebank
- Zeldes, A. et al. (2024). eRST: Enhanced Rhetorical Structure Theory

---

**문서 종료**