# Group Edge 명세서

**버전:** v0.1  
**작성일:** 2026-01-30  
**목적:** 복수 개체의 집합/그룹 관계를 표현하기 위한 Group Edge 구조 정의

---

## 1. 개요

Group Edge는 **복수의 Node를 하나의 그룹으로 묶어** 표현하는 Edge 타입이다.

**핵심 특징:**
- **논리 연산:** AND, OR, XOR
- **집합 표현:** LIST (순서 있음), SET (순서 없음)
- **관계 표현:** RANGE (범위), PAIR (순서쌍)
- **가변 멤버:** 종결 마커 방식

**용도:**
- "철수와 영희가 만났다" → AND 그룹
- "A 또는 B를 선택" → OR 그룹
- "1번부터 10번까지" → RANGE
- "(x, y) 좌표" → PAIR

---

## 2. Prefix

`SIDX.md` 참조

| 항목 | 값 |
|------|-----|
| Standard | `0 000 111 000` (10비트) |
| Proposal | `1100 000 111 000` (13비트) |
| 1st 워드 나머지 | 3비트 (GroupType) |

**위치:** `0 000 111` 확장 영역의 첫 번째 타입 (`000`)

---

## 3. 패킷 구조

### 3.1 전체 구조

```
1st WORD (16비트)
┌───────────────────────┬───────────┐
│        Prefix         │ GroupType │
│        13비트          │   3비트   │
└───────────────────────┴───────────┘
  [1100 000 111 000]       [TTT]

2nd WORD (16비트)
┌────────────────────────────────────┐
│             Edge TID               │
│              16비트                │
└────────────────────────────────────┘

3rd+ WORD: 멤버 TID들 (가변)
┌────────────────────────────────────┐
│            멤버 TID 1              │
├────────────────────────────────────┤
│            멤버 TID 2              │
├────────────────────────────────────┤
│               ...                  │
├────────────────────────────────────┤
│         종결 마커 (0x0000)          │
└────────────────────────────────────┘
```

### 3.2 필드 설명

| 필드 | 비트 | 설명 |
|------|------|------|
| Prefix | 13 | `1100 000 111 000` |
| GroupType | 3 | 그룹 종류 (8개) |
| Edge TID | 16 | 이 Edge의 고유 식별자 |
| 멤버 TID | 16×N | 그룹 멤버 참조 |
| 종결 마커 | 16 | `0x0000` |

### 3.3 워드 수

```
최소: 4워드 (멤버 1개)
일반: 5~6워드 (멤버 2~3개)
최대: 제한 없음 (종결 마커 사용)
```

---

## 4. GroupType (3비트 = 8개)

| 코드 | 타입 | 의미 | 멤버 수 |
|------|------|------|---------|
| 000 | **AND** | 논리곱 (conjunction) | 2+ |
| 001 | **OR** | 논리합 (disjunction) | 2+ |
| 010 | **XOR** | 배타적 선택 | 2+ |
| 011 | **LIST** | 순서 있는 목록 | 1+ |
| 100 | **SET** | 순서 없는 집합 | 1+ |
| 101 | **RANGE** | 범위 (시작~끝) | 2 |
| 110 | **PAIR** | 순서쌍 | 2 |
| 111 | 확장 | 미래 확장 | - |

**사용: 7개 / 확장: 1개**

---

## 5. GroupType 상세

### 5.1 AND (000)

모든 멤버가 동시에 참여.

```
"철수와 영희와 민수가 회의했다"

Group Edge (AND):
  멤버: [철수, 영희, 민수]
```

**의미:** 멤버 전체가 해당 관계/동작에 참여

### 5.2 OR (001)

멤버 중 하나 이상이 해당.

```
"커피 또는 차를 주문하세요"

Group Edge (OR):
  멤버: [커피, 차]
```

**의미:** 포괄적 선택 (inclusive or)

### 5.3 XOR (010)

멤버 중 정확히 하나만 해당.

```
"합격 또는 불합격 (둘 중 하나)"

Group Edge (XOR):
  멤버: [합격, 불합격]
```

**의미:** 배타적 선택 (exclusive or)

### 5.4 LIST (011)

순서가 의미 있는 목록.

```
"1등 철수, 2등 영희, 3등 민수"

Group Edge (LIST):
  멤버: [철수, 영희, 민수]  ← 순서 중요
```

**의미:** 
- 순위, 순서, 시퀀스
- SEQUENCE 개념 포함

### 5.5 SET (100)

순서가 무의미한 집합.

```
"참석자: 철수, 영희, 민수"

Group Edge (SET):
  멤버: [철수, 영희, 민수]  ← 순서 무관
```

**의미:** 
- 단순 집합
- 멤버십만 중요

### 5.6 RANGE (101)

연속 범위 (사이 값 포함).

```
"1부터 10까지"

Group Edge (RANGE):
  멤버: [1, 10]  ← 시작, 끝
```

**의미:** 
- 시작과 끝 사이의 모든 값 포함
- 날짜 범위, 숫자 범위 등

**멤버 수:** 정확히 2개 (시작, 끝)

### 5.7 PAIR (110)

단순 순서쌍.

```
"좌표 (3, 5)"
"키-값 (name, 철수)"

Group Edge (PAIR):
  멤버: [3, 5] 또는 [name, 철수]
```

**의미:**
- 순서가 있는 두 원소의 쌍
- 좌표, key-value, 관계 등

**멤버 수:** 정확히 2개

### 5.8 RANGE vs PAIR 구분

| 타입 | 의미 | 사이 값 |
|------|------|---------|
| RANGE | 연속 범위 | 포함 |
| PAIR | 단순 쌍 | 없음 |

```
RANGE [1, 5] → 1, 2, 3, 4, 5 (사이 값 존재)
PAIR [1, 5] → (1, 5) (두 값만)
```

---

## 6. 예시

### 6.1 "철수와 영희가 만났다"

```
1. Entity Node: 철수 (TID=0x0001)
2. Entity Node: 영희 (TID=0x0002)
3. Group Edge: AND (TID=0x0100)
   1st: [1100 000 111 000] [000] = Prefix + AND
   2nd: [0x0100]                 = Edge TID
   3rd: [0x0001]                 = 철수
   4th: [0x0002]                 = 영희
   5th: [0x0000]                 = 종결

4. Verb Edge: meet
   Subject: 0x0100 (그룹 참조)

총: 5워드
```

### 6.2 "A 또는 B를 선택하세요"

```
1. Entity Node: A (TID=0x0001)
2. Entity Node: B (TID=0x0002)
3. Group Edge: OR (TID=0x0100)
   1st: [1100 000 111 000] [001] = Prefix + OR
   2nd: [0x0100]
   3rd: [0x0001]
   4th: [0x0002]
   5th: [0x0000]

4. Verb Edge: select
   Target: 0x0100

총: 5워드
```

### 6.3 "1등부터 3등까지 시상"

```
1. Quantity Node: 1등 (TID=0x0001)
2. Quantity Node: 3등 (TID=0x0002)
3. Group Edge: RANGE (TID=0x0100)
   1st: [1100 000 111 000] [101] = Prefix + RANGE
   2nd: [0x0100]
   3rd: [0x0001]                 = 시작 (1등)
   4th: [0x0002]                 = 끝 (3등)
   5th: [0x0000]

총: 5워드
```

### 6.4 "좌표 (3, 5)"

```
1. Quantity Node: 3 (TID=0x0001)
2. Quantity Node: 5 (TID=0x0002)
3. Group Edge: PAIR (TID=0x0100)
   1st: [1100 000 111 000] [110] = Prefix + PAIR
   2nd: [0x0100]
   3rd: [0x0001]                 = 첫 번째 (x)
   4th: [0x0002]                 = 두 번째 (y)
   5th: [0x0000]

총: 5워드
```

---

## 7. 파싱

```python
def parse_group_edge(data: bytes) -> dict:
    word1 = int.from_bytes(data[0:2], 'big')
    word2 = int.from_bytes(data[2:4], 'big')
    
    # Prefix 확인 (상위 13비트)
    prefix = word1 >> 3
    assert prefix == 0b1100000111000, "Not Group Edge"
    
    # GroupType 추출 (하위 3비트)
    group_type = word1 & 0x7
    
    GROUP_NAMES = {
        0: "AND",
        1: "OR",
        2: "XOR",
        3: "LIST",
        4: "SET",
        5: "RANGE",
        6: "PAIR",
        7: "EXTENSION"
    }
    
    # Edge TID
    edge_tid = word2
    
    # 멤버 TID 수집
    members = []
    offset = 4
    while offset < len(data):
        member_tid = int.from_bytes(data[offset:offset+2], 'big')
        if member_tid == 0x0000:
            break
        members.append(member_tid)
        offset += 2
    
    return {
        'group_type': GROUP_NAMES.get(group_type, f"UNKNOWN_{group_type}"),
        'group_type_code': group_type,
        'edge_tid': edge_tid,
        'members': members,
        'words': 2 + len(members) + 1
    }
```

---

## 8. 인코딩

```python
def encode_group_edge(group_type: int, edge_tid: int, 
                      members: list[int]) -> bytes:
    # 1st 워드: Prefix (13비트) + GroupType (3비트)
    prefix = 0b1100000111000
    word1 = (prefix << 3) | (group_type & 0x7)
    
    result = bytearray()
    result += word1.to_bytes(2, 'big')
    result += edge_tid.to_bytes(2, 'big')
    
    # 멤버 TID
    for member in members:
        result += member.to_bytes(2, 'big')
    
    # 종결 마커
    result += (0x0000).to_bytes(2, 'big')
    
    return bytes(result)

# 편의 함수
def encode_and_group(edge_tid: int, members: list[int]) -> bytes:
    return encode_group_edge(0, edge_tid, members)

def encode_or_group(edge_tid: int, members: list[int]) -> bytes:
    return encode_group_edge(1, edge_tid, members)

def encode_pair(edge_tid: int, first: int, second: int) -> bytes:
    return encode_group_edge(6, edge_tid, [first, second])

def encode_range(edge_tid: int, start: int, end: int) -> bytes:
    return encode_group_edge(5, edge_tid, [start, end])
```

---

## 9. 제약 조건

### 9.1 멤버 수 제약

| GroupType | 최소 | 최대 | 비고 |
|-----------|------|------|------|
| AND | 2 | ∞ | - |
| OR | 2 | ∞ | - |
| XOR | 2 | ∞ | - |
| LIST | 1 | ∞ | 빈 리스트 불가 |
| SET | 1 | ∞ | 빈 셋 불가 |
| RANGE | 2 | 2 | 정확히 2개 |
| PAIR | 2 | 2 | 정확히 2개 |

### 9.2 TID 참조 규칙

- 멤버 TID는 **이미 선언된 Node/Edge**를 참조
- 자기 참조 (순환) 불가
- TID=0x0000은 종결 마커로 예약됨

---

## 10. GEUL 생태계 내 위치

```
GEUL 패킷 체계:

제어:
└── Meta Node

지식/개체:
├── Entity Node
├── Triple Edge
└── Quantity Node

서술/사건:
├── Verb Edge (Tiny/Short/Full)
├── Event6 Edge
└── Clause Edge

맥락:
└── Context Edge

코드:
└── Faber Edge

집합/그룹:                          ← 신규
└── Group Edge
        │
        ├── AND (논리곱)
        ├── OR (논리합)
        ├── XOR (배타적 선택)
        ├── LIST (순서 목록)
        ├── SET (순서 없는 집합)
        ├── RANGE (범위)
        └── PAIR (순서쌍)
```

---

## 11. 확장 영역

`0 000 111` 확장 영역 할당:

| Prefix (10비트) | 타입 |
|-----------------|------|
| `0 000 111 000` | **Group Edge** |
| `0 000 111 001` | 예약 |
| `0 000 111 010` | 예약 |
| `0 000 111 011` | 예약 |
| `0 000 111 100` | 예약 |
| `0 000 111 101` | 예약 |
| `0 000 111 110` | 예약 |
| `0 000 111 111` | 2차 확장 |

---

## 12. 버전 히스토리

| 버전 | 날짜 | 변경 |
|------|------|------|
| v0.1 | 2026-01-30 | 초안: 7개 GroupType 정의 |

---

## 13. TODO

- [ ] 중첩 그룹 (그룹 안의 그룹) 테스트
- [ ] 빈 그룹 표현 필요성 검토
- [ ] GroupType 111 확장 용도 정의

---

## 14. 관련 문서

| 문서 | 내용 |
|------|------|
| `SIDX.md` | SIDX 비트 구조, 확장 영역 |
| `Verb_Edge.md` | 그룹을 Subject로 참조 |
| `Event6_Edge.md` | 그룹을 참여자로 참조 |

---

**문서 종료**