# Event6 Edge 명세서

**버전:** v0.2  
**작성일:** 2026-01-29  
**목적:** GEUL 6하원칙 사건 표현을 위한 Event6 Edge 패킷 구조 정의

---

## 1. 개요

Event6 Edge는 **6하원칙**(Who, What, Whom, When, Where, Why)을 한 번에 표현하는 사건 Edge 타입이다.

**핵심 특징:**
- **가변 길이:** 3~9워드 (Presence에 따라)
- **Presence 비트마스크:** 어떤 요소가 있는지 명시
- **Edge TID 헤더 다음:** 파싱 효율
- **각 요소 TID 참조:** Entity, Verb Edge, Quantity 등

**용도:**
- 뉴스 이벤트: "Apple이 2025년에 Tesla를 인수했다"
- 역사 사건: "이순신이 1598년 노량해전에서 전사했다"
- 일상 사건: "철수가 어제 학교에서 영희에게 선물을 줬다"

---

## 2. Prefix

`SIDX.md` 참조

| 항목 | 값 |
|------|-----|
| Standard | `0 000 011` (7비트) |
| Proposal | `1100 000 011` (10비트) |
| 1st 워드 나머지 | 6비트 (Presence) |

---

## 3. 6하원칙 요소

| 요소 | 영문 | 비트 | 의미 | TID 참조 대상 |
|------|------|------|------|---------------|
| Who | Agent | 0 | 행위자 | Entity |
| What | Action | 1 | 행위/동작 | Verb Edge |
| Whom | Patient | 2 | 대상/피행위자 | Entity |
| When | Time | 3 | 시간 | Quantity/Entity |
| Where | Location | 4 | 장소 | Entity |
| Why | Reason | 5 | 이유/목적 | Clause/Entity |

---

## 4. 패킷 구조

### 4.1 기본 구조

```
1st WORD (16비트)
┌────────────────────┬────────────────────┐
│      Prefix        │     Presence       │
│      10bit         │       6bit         │
└────────────────────┴────────────────────┘

2nd WORD (16비트)
┌────────────────────────────────────────────┐
│                Edge TID                    │
│                  16bit                     │
└────────────────────────────────────────────┘

3rd+ WORD: 요소 TID들 (Presence 순서대로)
```

### 4.2 Presence 비트마스크 (6비트)

| 비트 | 요소 | 있으면 |
|------|------|--------|
| 0 | Who | 해당 TID 포함 |
| 1 | What | 해당 TID 포함 |
| 2 | Whom | 해당 TID 포함 |
| 3 | When | 해당 TID 포함 |
| 4 | Where | 해당 TID 포함 |
| 5 | Why | 해당 TID 포함 |

**TID 순서:** 비트 0부터 순차적으로 (있는 것만)

### 4.3 워드 수 계산

```
총 워드 = 2 (헤더 + Edge TID) + popcount(Presence)
```

| Presence | 요소 수 | 총 워드 |
|----------|---------|---------|
| `000001` | 1 | 3 |
| `000011` | 2 | 4 |
| `000111` | 3 | 5 |
| `001111` | 4 | 6 |
| `011111` | 5 | 7 |
| `111111` | 6 | 8 |

**범위:** 3~8워드 (48~128비트)

---

## 5. 모드별 구조

### 5.1 최소 모드 (3워드)

단일 요소만 있는 경우.

```
예: "비가 왔다" (What만)

1st: [Prefix] + [000010]      - What만 존재
2nd: [Edge TID]
3rd: [What TID]               - "rain" Verb Edge

총: 3워드
```

### 5.2 핵심 모드 (5워드)

Who + What + Whom (가장 빈번).

```
예: "철수가 영희를 때렸다"

1st: [Prefix] + [000111]      - Who, What, Whom
2nd: [Edge TID]
3rd: [Who TID]                - 철수
4th: [What TID]               - "hit" Verb Edge
5th: [Whom TID]               - 영희

총: 5워드
```

### 5.3 표준 모드 (6워드)

Who + What + Whom + When 또는 Where.

```
예: "철수가 어제 영희를 만났다"

1st: [Prefix] + [001111]      - Who, What, Whom, When
2nd: [Edge TID]
3rd: [Who TID]                - 철수
4th: [What TID]               - "meet" Verb Edge
5th: [Whom TID]               - 영희
6th: [When TID]               - 어제 (시간 Entity/Quantity)

총: 6워드
```

### 5.4 완전 모드 (8워드)

6개 요소 전부.

```
예: "철수가 사랑 때문에 어제 학교에서 영희에게 선물을 줬다"

1st: [Prefix] + [111111]      - 전체
2nd: [Edge TID]
3rd: [Who TID]                - 철수
4th: [What TID]               - "give" Verb Edge
5th: [Whom TID]               - 영희 (또는 선물?)
6th: [When TID]               - 어제
7th: [Where TID]              - 학교
8th: [Why TID]                - 사랑 (이유)

총: 8워드
```

---

## 6. 필드 상세

### 6.1 Who (행위자)

| 항목 | 설명 |
|------|------|
| 의미 | 행위를 수행하는 주체 |
| 참조 | Entity TID |
| 의미역 | Agent, Experiencer |
| 예시 | "철수가", "Apple이" |

### 6.2 What (행위)

| 항목 | 설명 |
|------|------|
| 의미 | 수행되는 행위/동작 |
| 참조 | Verb Edge TID |
| 특징 | 한정자 정보 포함 (시제, 상 등) |
| 예시 | "먹었다", "인수했다" |

**중요:** What은 Verb Edge를 참조하므로, 해당 Verb Edge에 한정자 정보가 담김.

### 6.3 Whom (대상)

| 항목 | 설명 |
|------|------|
| 의미 | 행위의 대상/피행위자 |
| 참조 | Entity TID |
| 의미역 | Patient, Theme, Recipient |
| 예시 | "밥을", "영희에게", "Tesla를" |

### 6.4 When (시간)

| 항목 | 설명 |
|------|------|
| 의미 | 사건 발생 시점/기간 |
| 참조 | Quantity TID (시간) 또는 Entity TID (시점) |
| 예시 | "2025년", "어제", "3시간 동안" |

**시간 표현:**
- 시점: Entity (Q-ID로 연도, 날짜 등)
- 기간: Quantity (Unit = 시간 단위)

### 6.5 Where (장소)

| 항목 | 설명 |
|------|------|
| 의미 | 사건 발생 장소 |
| 참조 | Entity TID (Location 타입) |
| 예시 | "서울에서", "학교에서", "노량해전에서" |

### 6.6 Why (이유)

| 항목 | 설명 |
|------|------|
| 의미 | 행위의 이유/목적/원인 |
| 참조 | Clause TID, Entity TID, 또는 Verb Edge TID |
| 예시 | "배고파서", "돈을 위해", "사랑 때문에" |

**복잡한 이유:**
- 단순: Entity TID ("사랑")
- 복잡: Clause Edge TID ("비가 와서")

---

## 7. 파싱

### 7.1 워드 수 결정

```python
def get_event6_words(data: bytes) -> int:
    word1 = int.from_bytes(data[0:2], 'big')
    presence = word1 & 0x3F
    
    # popcount
    count = bin(presence).count('1')
    return 2 + count  # 헤더 + Edge TID + 요소들
```

### 7.2 전체 파싱

```python
def parse_event6(data: bytes) -> dict:
    word1 = int.from_bytes(data[0:2], 'big')
    
    # Prefix 확인
    prefix = word1 >> 6
    assert prefix == 0b1100000011, "Not Event6 Edge"
    
    # Presence
    presence = word1 & 0x3F
    
    # Edge TID
    edge_tid = int.from_bytes(data[2:4], 'big')
    
    # 요소 TID들 추출
    elements = {}
    element_names = ['who', 'what', 'whom', 'when', 'where', 'why']
    offset = 4  # 3rd 워드부터
    
    for i, name in enumerate(element_names):
        if presence & (1 << i):
            tid = int.from_bytes(data[offset:offset+2], 'big')
            elements[name] = tid
            offset += 2
    
    return {
        'presence': presence,
        'edge_tid': edge_tid,
        'elements': elements,
        'words': 2 + bin(presence).count('1')
    }
```

---

## 8. 인코딩

```python
def encode_event6(
    edge_tid: int,
    who: int = None,
    what: int = None,
    whom: int = None,
    when: int = None,
    where: int = None,
    why: int = None
) -> bytes:
    # Presence 계산
    presence = 0
    elements = []
    
    for i, val in enumerate([who, what, whom, when, where, why]):
        if val is not None:
            presence |= (1 << i)
            elements.append(val)
    
    # 1st WORD
    word1 = (0b1100000011 << 6) | presence
    
    # 조립
    result = word1.to_bytes(2, 'big')
    result += edge_tid.to_bytes(2, 'big')
    
    for tid in elements:
        result += tid.to_bytes(2, 'big')
    
    return result
```

---

## 9. 예시

### 9.1 "Apple이 Tesla를 인수했다"

```
Who:  Apple (Q312)     → Entity TID 0x0001
What: acquire          → Verb Edge TID 0x0100
Whom: Tesla (Q478214)  → Entity TID 0x0002

Event6 Edge:
  1st: [1100 000 011] + [000111]  - Prefix + Who,What,Whom
  2nd: [TID: 0x0200]              - Edge TID
  3rd: [TID: 0x0001]              - Apple (Who)
  4th: [TID: 0x0100]              - acquire (What)
  5th: [TID: 0x0002]              - Tesla (Whom)

총: 5워드
```

### 9.2 "Apple이 2025년에 Tesla를 $2B에 인수했다"

```
Who:   Apple           → Entity TID 0x0001
What:  acquire         → Verb Edge TID 0x0100
Whom:  Tesla           → Entity TID 0x0002
When:  2025            → Entity TID 0x0003 (연도)
(가격은 Verb Edge 내부 또는 별도 Triple로)

Event6 Edge:
  1st: [1100 000 011] + [001111]  - Who,What,Whom,When
  2nd: [TID: 0x0201]              - Edge TID
  3rd: [TID: 0x0001]              - Apple
  4th: [TID: 0x0100]              - acquire
  5th: [TID: 0x0002]              - Tesla
  6th: [TID: 0x0003]              - 2025

총: 6워드
```

### 9.3 "이순신이 1598년 노량해전에서 전사했다"

```
Who:   이순신           → Entity TID 0x0010
What:  die (전사)       → Verb Edge TID 0x0101
When:  1598            → Entity TID 0x0011
Where: 노량해전         → Entity TID 0x0012

Event6 Edge:
  1st: [1100 000 011] + [011011]  - Who,What,When,Where
  2nd: [TID: 0x0202]
  3rd: [TID: 0x0010]              - 이순신
  4th: [TID: 0x0101]              - die
  5th: [TID: 0x0011]              - 1598
  6th: [TID: 0x0012]              - 노량해전

총: 6워드
```

### 9.4 "비가 왔다" (최소)

```
What: rain → Verb Edge TID 0x0102

Event6 Edge:
  1st: [1100 000 011] + [000010]  - What만
  2nd: [TID: 0x0203]
  3rd: [TID: 0x0102]              - rain

총: 3워드
```

### 9.5 "배고파서 밥을 먹었다" (이유 포함)

```
Who:  (암묵적 나)       → Entity TID 0x0020
What: eat              → Verb Edge TID 0x0103
Whom: 밥               → Entity TID 0x0021
Why:  배고프다          → Clause Edge TID 0x0300 (또는 Verb Edge)

Event6 Edge:
  1st: [1100 000 011] + [100111]  - Who,What,Whom,Why
  2nd: [TID: 0x0204]
  3rd: [TID: 0x0020]              - 나
  4th: [TID: 0x0103]              - eat
  5th: [TID: 0x0021]              - 밥
  6th: [TID: 0x0300]              - 배고파서 (Clause)

총: 6워드
```

---

## 10. Event6 vs Verb Edge 비교

| | Verb Edge | Event6 Edge |
|--|-----------|-------------|
| **초점** | 서술/동작 | 완결된 사건 |
| **참여자** | Participant 구조 | 6하원칙 TID |
| **시공간** | 별도 표현 | When/Where 내장 |
| **이유** | 별도 Clause | Why 내장 |
| **워드** | 2~5 | 3~8 |
| **용도** | 서술 표현 | 사건 저장 |

**선택 가이드:**
- 서술/문장 분석 → Verb Edge
- 사건/기록 저장 → Event6 Edge
- 간단한 사실 → Triple Edge

---

## 11. What과 Verb Edge 관계

Event6의 What은 **Verb Edge TID**를 참조한다.

```
Verb Edge (What):
  - 동사: acquire.v.01
  - 시제: 과거
  - 상: 완료
  - (참여자 정보는 Event6에서)

Event6:
  - Who: Apple
  - What: [Verb Edge TID] → 위 Verb Edge 참조
  - Whom: Tesla
```

**장점:**
- Verb Edge에 한정자 정보 집중
- Event6는 참여자 구조에 집중
- 중복 제거

---

## 12. 중첩 이벤트

복잡한 이벤트는 Clause Edge로 연결.

```
"Apple이 Tesla를 인수해서 주가가 올랐다"

Event6 #1: Apple → acquire → Tesla
Event6 #2: 주가 → rise

Clause Edge:
  [CAUSE]
  [TID 1: Event6 #1]
  [TID 2: Event6 #2]
```

---

## 13. 설계 근거

### 13.1 가변 길이 이유

- **효율:** 대부분 3~5요소 (3~5워드 아님, 5~7워드)
- **유연:** 요소 수에 따라 자연스럽게 확장
- **Presence 비트:** 6비트로 간결하게 표현

### 13.2 What = Verb Edge TID 이유

- **한정자 분리:** 시제/상/극성은 Verb Edge에
- **재사용:** 같은 동사 여러 Event6에서 참조
- **일관성:** 서술 분석과 통합

### 13.3 6요소 제한 이유

- **6하원칙:** 언어학/저널리즘 표준
- **6비트:** 1워드 내 깔끔한 배치
- **확장:** 추가 정보는 Triple Edge로

---

## 14. 버전 히스토리

| 버전 | 날짜 | 변경 |
|------|------|------|
| v0.1 | 2026-01-29 | 초안: 가변 길이 구조 |
| v0.2 | 2026-01-29 | Prefix 표기 수정, SIDX.md 참조로 변경 |

---

## 15. TODO

- [ ] Whom의 다중 대상 처리 (Theme vs Recipient)
- [ ] When의 기간 vs 시점 구분
- [ ] Where의 Source/Destination 구분
- [ ] Context Edge 연결 (출처/신뢰도)
- [ ] WMS 인덱싱 전략

---

**문서 종료**