# Clause Edge 명세서

**버전:** v0.4  
**작성일:** 2026-01-29  
**목적:** GEUL 서술/사건 간 논리적 관계 표현을 위한 Clause Edge 구조 정의

---

## 1. 개요

Clause Edge는 서술(Verb Edge), 사건(Event6), 관계(Triple), 또는 다른 Clause 간의 **논리적/담화적 관계**를 표현하는 Edge 타입이다.

RST(Rhetorical Structure Theory)의 담화 관계를 기반으로 설계되었다.

---

## 2. Prefix

`SIDX.md` 참조

| 항목 | 값 |
|------|-----|
| Standard | `0 000 010` (7비트) |
| Proposal | `1100 000 010` (10비트) |
| 1st 워드 나머지 | 6비트 (관계타입 4 + 예약 2) |

---

## 3. 패킷 구조 (4워드, 64비트)

### 3.1 레이아웃

```
1st WORD (16비트):
┌─────────────────────┬────────────┬────────┐
│      Prefix         │  관계타입   │  예약   │
│       10비트         │   4비트    │  2비트  │
└─────────────────────┴────────────┴────────┘
 [1100 000 010]        [RRRR]       [xx]

2nd WORD: Edge TID (16비트)
3rd WORD: TID 1 (16비트) - 첫 번째 절
4th WORD: TID 2 (16비트) - 두 번째 절

총: 4워드 (64비트)
```

### 3.2 필드 설명

| 필드 | 비트 | 위치 | 설명 |
|------|------|------|------|
| Prefix | 10 | 1st[15:6] | `1100 000 010` |
| 관계타입 | 4 | 1st[5:2] | 16개 RST 관계 |
| 예약 | 2 | 1st[1:0] | 미래 확장용 |
| Edge TID | 16 | 2nd | 이 Edge의 고유 식별자 |
| TID 1 | 16 | 3rd | 첫 번째 절 참조 |
| TID 2 | 16 | 4th | 두 번째 절 참조 |

---

## 4. 연결 대상

Clause Edge는 TID를 통해 다양한 Edge 타입을 연결할 수 있다.

| TID 타입 | 설명 | 연결 가능 |
|----------|------|-----------|
| Entity | 개체 | △ (제한적) |
| Verb Edge | 서술 | ✓ |
| Triple Edge | 속성/관계 | ✓ |
| Clause Edge | 복합 절 | ✓ (중첩) |
| Event6 Edge | 6하원칙 사건 | ✓ |
| Context Edge | 맥락 | △ |

**TID 체계:** 16비트 통합 풀 (65,536개). 타입 비트 없이 WMS가 TID→타입 매핑 관리.

---

## 5. 관계 타입 (4비트 = 16개)

RST(Rhetorical Structure Theory) 기반 담화 관계:

### 5.1 인과 관계

| 코드 | 타입 | 설명 | 예시 |
|------|------|------|------|
| 0000 | CAUSE | 원인→결과 | "비가 와서 집에 있었다" |
| 0001 | RESULT | 결과←원인 | "집에 있었다, 비가 왔기에" |
| 0010 | CONDITION | 조건→귀결 | "비가 오면 안 간다" |
| 0011 | PURPOSE | 목적 | "살기 위해 먹는다" |

### 5.2 시간/순서 관계

| 코드 | 타입 | 설명 | 예시 |
|------|------|------|------|
| 0100 | SEQUENCE | 시간순 | "밥 먹고 잤다" |
| 0101 | PARALLEL | 동시/병렬 | "웃으면서 말했다" |

### 5.3 대조/양보 관계

| 코드 | 타입 | 설명 | 예시 |
|------|------|------|------|
| 0110 | CONTRAST | 대조 | "A는 크고 B는 작다" |
| 0111 | CONCESSION | 양보 | "어렵지만 했다" |

### 5.4 부연/배경 관계

| 코드 | 타입 | 설명 | 예시 |
|------|------|------|------|
| 1000 | ELABORATION | 상세화 | "구체적으로 말하면" |
| 1001 | BACKGROUND | 배경 정보 | "참고로, 당시 상황은" |

### 5.5 논증 관계

| 코드 | 타입 | 설명 | 예시 |
|------|------|------|------|
| 1010 | EVIDENCE | 증거 제시 | "왜냐하면... 때문이다" |
| 1011 | EVALUATION | 평가 | "이것은 좋다/나쁘다" |

### 5.6 기타 관계

| 코드 | 타입 | 설명 | 예시 |
|------|------|------|------|
| 1100 | SOLUTIONHOOD | 문제→해결 | "문제는 X, 해결책은 Y" |
| 1101 | ALTERNATIVE | 선택/대안 | "가거나 말거나" |
| 1110 | MEANS | 수단 | "이렇게 해서 달성했다" |
| 1111 | RESERVED | 예약 | 미래 확장용 |

---

## 6. TID 순서 규칙

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

---

## 7. 예시

### 7.1 단순 인과

**"비가 와서 집에 있었다"**

```
Verb Edge E01: rain(비) | TID=0x0001
Verb Edge E02: stay(나, 집) | TID=0x0002

Clause Edge:
  1st: [1100 000 010] [0000] [00]  - Prefix + CAUSE + 예약
  2nd: [0x0100]                    - Edge TID
  3rd: [0x0001]                    - TID 1 (원인: E01)
  4th: [0x0002]                    - TID 2 (결과: E02)
```

### 7.2 조건문

**"비가 오면 안 간다"**

```
Verb Edge E01: rain(비) | TID=0x0001
Verb Edge E02: go(나) [Polarity=부정] | TID=0x0002

Clause Edge:
  1st: [1100 000 010] [0010] [00]  - Prefix + CONDITION + 예약
  2nd: [0x0101]                    - Edge TID
  3rd: [0x0001]                    - TID 1 (조건: E01)
  4th: [0x0002]                    - TID 2 (귀결: E02)
```

### 7.3 Triple 연결

**"철수가 CEO이기 때문에 결정했다"**

```
Triple T01: (철수, is_a, CEO) | TID=0x0010
Verb Edge E01: decide(철수, ...) | TID=0x0001

Clause Edge:
  1st: [1100 000 010] [0000] [00]  - Prefix + CAUSE + 예약
  2nd: [0x0102]                    - Edge TID
  3rd: [0x0010]                    - TID 1 (원인: Triple)
  4th: [0x0001]                    - TID 2 (결과: Verb Edge)
```

### 7.4 Event6 연결

**"애플이 테슬라를 인수해서 주가가 올랐다"**

```
Event6 E01: (Apple, acquire, Tesla, $2B, 2025-03-15) | TID=0x0020
Verb Edge E02: rise(주가) | TID=0x0002

Clause Edge:
  1st: [1100 000 010] [0000] [00]  - Prefix + CAUSE + 예약
  2nd: [0x0103]                    - Edge TID
  3rd: [0x0020]                    - TID 1 (원인: Event6)
  4th: [0x0002]                    - TID 2 (결과: Verb Edge)
```

### 7.5 중첩 Clause

**"비가 와서 집에 있었고, 그래서 공부했다"**

```
Verb Edge E01: rain(비) | TID=0x0001
Verb Edge E02: stay(나, 집) | TID=0x0002
Verb Edge E03: study(나) | TID=0x0003

Clause Edge C01:
  1st: [1100 000 010] [0000] [00]  - Prefix + CAUSE
  2nd: [0x0100]                    - Edge TID
  3rd: [0x0001]                    - E01
  4th: [0x0002]                    - E02

Clause Edge C02:
  1st: [1100 000 010] [0001] [00]  - Prefix + RESULT
  2nd: [0x0101]                    - Edge TID
  3rd: [0x0100]                    - C01 (Clause TID 참조!)
  4th: [0x0003]                    - E03
```

---

## 8. Multinuclear vs Nucleus-Satellite

RST 구분을 따름:

### 8.1 Nucleus-Satellite (비대칭)

| 관계 | TID 1 | TID 2 |
|------|-------|-------|
| CAUSE | 원인 (Satellite) | 결과 (Nucleus) |
| CONDITION | 조건 (Satellite) | 귀결 (Nucleus) |
| EVIDENCE | 증거 (Satellite) | 주장 (Nucleus) |
| ELABORATION | 핵심 (Nucleus) | 부연 (Satellite) |

### 8.2 Multinuclear (대칭)

| 관계 | TID 1 | TID 2 |
|------|-------|-------|
| SEQUENCE | 선행 | 후행 |
| PARALLEL | 첫 번째 | 두 번째 |
| CONTRAST | 첫 번째 | 두 번째 |
| ALTERNATIVE | 첫 번째 | 두 번째 |

**대칭 관계는 TID 순서가 의미적 우선순위가 아님.**

---

## 9. 파싱/인코딩

### 9.1 파싱

```python
def parse_clause_edge(words: list[int]) -> dict:
    """4워드 Clause Edge 파싱"""
    
    # 1st 워드
    word1 = words[0]
    prefix = (word1 >> 6) & 0x3FF  # 10비트
    assert prefix == 0b1100000010, "Invalid Clause Edge prefix"
    
    relation = (word1 >> 2) & 0xF  # 4비트
    reserved = word1 & 0x3         # 2비트
    
    # 2nd~4th 워드
    edge_tid = words[1]
    tid_1 = words[2]
    tid_2 = words[3]
    
    RELATION_NAMES = {
        0: "CAUSE", 1: "RESULT", 2: "CONDITION", 3: "PURPOSE",
        4: "SEQUENCE", 5: "PARALLEL", 6: "CONTRAST", 7: "CONCESSION",
        8: "ELABORATION", 9: "BACKGROUND", 10: "EVIDENCE", 11: "EVALUATION",
        12: "SOLUTIONHOOD", 13: "ALTERNATIVE", 14: "MEANS", 15: "RESERVED"
    }
    
    return {
        "type": "Clause Edge",
        "edge_tid": edge_tid,
        "relation": RELATION_NAMES[relation],
        "relation_code": relation,
        "tid_1": tid_1,
        "tid_2": tid_2
    }
```

### 9.2 인코딩

```python
def encode_clause_edge(relation: int, edge_tid: int, tid_1: int, tid_2: int) -> list[int]:
    """Clause Edge → 4워드 인코딩"""
    
    # 1st 워드: Prefix(10) + Relation(4) + Reserved(2)
    prefix = 0b1100000010  # 10비트
    word1 = (prefix << 6) | (relation << 2) | 0x00
    
    return [word1, edge_tid, tid_1, tid_2]

# 사용 예시
CAUSE = 0
words = encode_clause_edge(CAUSE, 0x0100, 0x0001, 0x0002)
# → [0xC080, 0x0100, 0x0001, 0x0002]
```

---

## 10. WMS 저장 구조

### 10.1 인덱싱

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

### 10.2 그래프 탐색

```
GEUL-Path 예시:
/Event6[0x0020]/->CAUSE/->*
  → 0x0020에서 CAUSE로 연결된 모든 노드

/VerbEdge[0x0002]/<-CONDITION
  → 0x0002를 TID 2로 가지는 CONDITION의 TID 1
```

---

## 11. 설계 근거

### 11.1 RST 기반 이유

- 30년+ 연구 축적
- 다양한 코퍼스 검증
- 담화 파싱 도구 존재
- 언어 독립적

### 11.2 4비트(16개) 이유

- RST 핵심 관계 12개+
- 확장 여유 확보
- 3비트(8개)는 부족

### 11.3 4워드 간소화 이유

- 방향: TID 순서로 결정 (별도 비트 불필요)
- 확신도: 별도 메타데이터로 처리
- 2비트 예약: 향후 확장

---

## 12. GEUL 생태계 내 위치

```
GEUL Edge 체계:

지식/개체:
├── Entity Node (개체 선언)
└── Triple Edge (속성/관계)

서술/사건:
├── Verb Edge (서술)
└── Event6 Edge (6하원칙 사건)

논리/담화:
└── Clause Edge (절 관계) ← 이 문서

수량:
└── Quantity Node (물리량/수치)

맥락:
└── Context Edge (출처/신뢰도)
```

---

## 13. 버전 히스토리

| 버전 | 날짜 | 변경 |
|------|------|------|
| v0.1 | 2026-01-27 | 초안 (5워드) |
| v0.2 | 2026-01-28 | 4워드로 간소화, 방향/확신도 제거 |
| v0.3 | 2026-01-29 | 10비트 Prefix 체계 반영, 파싱/인코딩 코드 추가 |
| v0.4 | 2026-01-29 | Prefix 표기 수정, SIDX.md 참조로 변경 |

---

## 14. 향후 과제

- [ ] 3개 이상 노드 연결 (예: A이고 B이고 C이므로 D)
- [ ] GEUL-Path 쿼리 문법 정의
- [ ] 담화 파싱 → Clause Edge 자동 생성
- [ ] Context Edge 연결 (출처/신뢰도 표기)

---

## 15. 참고 문헌

- Mann, W.C. & Thompson, S.A. (1988). Rhetorical Structure Theory
- Carlson, L., Marcu, D., & Okurowski, M.E. (2003). RST Discourse Treebank
- Zeldes, A. et al. (2024). eRST: Enhanced Rhetorical Structure Theory

---

**문서 종료**