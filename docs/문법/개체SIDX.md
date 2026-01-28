# 개체 SIDX 명세서

**버전:** v0.5  
**작성일:** 2026-01-29  
**범위:** 개체(Entity) SIDX  
**상태:** 표준 제안 (Standard Proposal)

---

## 1. 개요

### 1.1 정의

**개체 SIDX**는 GEUL 스트림에서 개체(사람, 장소, 사물, 조직, 개념 등)를 식별하는 64비트 의미정렬 식별자이다.

### 1.2 UID 포함

**SIDX는 UID를 하위 32비트에 직접 포함한다.**

| 영역 | 비트 | 용도 |
|------|------|------|
| 상위 32비트 | bit1-32 | 메타데이터 (약식 사용 가능) |
| 하위 32비트 | bit33-64 | **UID (절대 식별자)** |

### 1.3 Lane별 분기 설계

**핵심 통찰:**

| Lane | 특성 | 양화 필요? | Source 필요? |
|------|------|-----------|-------------|
| 0 (공식) | 특정 UID 있음 | ✗ (항상 특정) | ✓ (출처 중요) |
| 1 (자유) | 추상적 가능 | ✓ | ✗ (출처 불명) |

- **공식(Lane=0):** Q-ID 등 등록된 ID → 항상 특정 개체 → Source 명시
- **자유(Lane=1):** 임시/추상 개체 → 양화 + 수량 명시

### 1.4 표준 제안 상태

| 상태 | Prefix | 가용 비트 |
|------|--------|----------|
| **표준 제안** | `1100 01` (6비트) | **58비트** |
| 표준 채택 후 | `0001` (4비트) | 60비트 |

---

## 2. 비트 레이아웃

### 2.1 전체 구조 (64비트)

```
┌──────────────────── 상위 32비트 (약식) ────────────────────┐┌─── 하위 32비트 (UID) ───┐
│                                                            ││                          │
┌─────────┬─────────────┬────────────┬──────┬───────────────┬┬──────────────────────────┐
│ Prefix  │ Entity Type │ Attributes │ Lane │ Lane별 해석    ││ ID Value (UID)           │
│ (6b)    │ (8b)        │ (12b)      │ (1b) │ (5b)          ││ (32b)                    │
└─────────┴─────────────┴────────────┴──────┴───────────────┴┴──────────────────────────┘
  bit1-6    bit7-14       bit15-26    bit27   bit28-32         bit33-64
```

### 2.2 필드별 상세

| 필드 | 비트 범위 | 크기 | 설명 |
|------|----------|------|------|
| Prefix | 1-6 | 6 | 고정값 `1100 01` |
| Entity Type | 7-14 | 8 | 256개 타입 (이진 트리) |
| Attributes | 15-26 | 12 | 4,096 조합 |
| Lane | 27 | 1 | 0=공식, 1=자유 |
| Lane별 해석 | 28-32 | 5 | Lane에 따라 다름 (섹션 3 참조) |
| ID Value | 33-64 | 32 | **UID (uint32)** |

### 2.3 32비트 경계 설계

```
상위 32비트 (bit1-32):  메타데이터
  - 6 + 8 + 12 + 1 + 5 = 32비트

하위 32비트 (bit33-64): UID
  - 32비트 uint32 정렬
```

**이점:**
- 약식 사용: 상위 32비트만 추출
- UID 추출: 하위 32비트만 추출 `sidx & 0xFFFFFFFF`
- 메모리/캐시 친화적

---

## 3. Lane별 필드 해석 (bit 28-32)

### 3.1 공식 영역 (Lane=0)

```
bit27:    0 (공식)
bit28-29: Reserved (00)
bit30-32: Source (3비트)
```

| Source | 코드 | 출처 | 현재 규모 |
|--------|------|------|----------|
| 000 | Q-ID | 위키데이터 Item | ~1.5억 |
| 001 | Synset | 워드넷 | ~12만 |
| 010 | P-ID | 위키데이터 Property | ~1.2만 |
| 011 | Lexeme | 위키데이터 어휘 | ~100만 |
| 100 | Schema | Schema.org | ~2천 |
| 101-111 | Reserved | - | - |

**공식 ID는 항상 특정(Specific) 개체** → 양화 불필요

### 3.2 자유 영역 (Lane=1)

```
bit27:    1 (자유)
bit28-29: Quantification (2비트)
bit30-32: Number (3비트)
```

#### 3.2.1 Quantification (bit 28-29)

| 값 | 의미 | 논리 | 예시 |
|----|------|------|------|
| 00 | 특정 (Specific) | ι | "그 사람", "저 고양이" |
| 01 | 전칭 (Universal) | ∀ | "모든 학생", "각 사람" |
| 10 | 존재 (Existential) | ∃ | "어떤 사람", "누군가" |
| 11 | 불특정 (Arbitrary) | ε | "아무나", "임의의" |

#### 3.2.2 Number (bit 30-32)

| 값 | 의미 | 예시 |
|----|------|------|
| 000 | 알 수 없음 | "사람(들)" |
| 001 | 단수 (1) | "한 사람" |
| 010 | 2개 | "두 마리" |
| 011 | 3개 | "세 권" |
| 100 | 4개 | "네 개" |
| 101 | 5개 | "다섯 명" |
| 110 | 6개 | "여섯 개" |
| 111 | 많다 (복수) | "여러/많은" |

---

## 4. Prefix (bit 1-6)

GEUL_비트명세.md에 따른 고정값:

```
bit1:   1 (Extension)
bit2:   1 (Free/Future)
bit3:   0 (Free)
bit4:   0 (Standard Proposal)
bit5:   0 (Node 미러링)
bit6:   1 (Entity)
─────────────────────────
합계:   1100 01
```

---

## 5. Entity Type (bit 7-14)

### 5.1 이진 트리 구조

**Level 0 (bit 7):**
```
0: Document 계열 (52%)
1: Entity 계열 (48%)
```

**Level 1 (bit 8):**
```
00: Article     01: Media
10: Living      11: Non-living
```

**Level 2 (bit 9):**
```
000: Academic   001: Reference
010: Visual     011: Literary
100: Sapient    101: Non-sapient
110: Physical   111: Abstract
```

**Level 3 (bit 10):**
```
1000: Human         1001: Organization
1010: Organism      1011: Celestial
1100: Location      1101: Artifact
1110: Concept       1111: Measure
```

### 5.2 코드 테이블

| 코드 | 분류 | 코드 | 분류 |
|------|------|------|------|
| 0x00 | Scholarly Article | 0x80 | Human |
| 0x01 | Clinical Trial | 0x81 | Fictional Human |
| 0x02 | Patent | 0x82 | Historical Figure |
| 0x10 | Encyclopedia | 0x90 | Organization |
| 0x11 | News Article | 0x91 | Business |
| 0x20 | Painting | 0x92 | School |
| 0x21 | Film | 0xA0 | Taxon |
| 0x30 | Book | 0xA1 | Gene |
| 0x31 | Literary Work | 0xB0 | Star |
| 0x32 | Album | 0xB1 | Galaxy |
| | | 0xC0 | Settlement |
| | | 0xC1 | City |
| | | 0xD0 | Building |
| | | 0xD4 | Product |
| | | 0xE0 | Concept |
| | | 0xF0 | Quantity |
| | | 0xFF | Reserved |

---

## 6. Attributes (bit 15-26)

### 6.1 구조 (12비트)

```
bit15:    is_fictional
bit16:    is_historical
bit17:    is_notable
bit18:    is_controversial
bit19-22: region (16개)
bit23-26: era (16개)
```

### 6.2 Region (bit 19-22)

| 코드 | 권역 | 코드 | 권역 |
|------|------|------|------|
| 0x0 | Global | 0x8 | Africa North |
| 0x1 | East Asia | 0x9 | Africa Sub |
| 0x2 | Southeast Asia | 0xA | North America |
| 0x3 | South Asia | 0xB | Central America |
| 0x4 | Central Asia | 0xC | South America |
| 0x5 | Middle East | 0xD | Oceania |
| 0x6 | Europe West | 0xE | Polar |
| 0x7 | Europe East | 0xF | Space |

### 6.3 Era (bit 23-26)

| 코드 | 시대 | 코드 | 시대 |
|------|------|------|------|
| 0x0 | Unknown | 0x5 | Early Modern |
| 0x1 | Prehistoric | 0x6 | Modern |
| 0x2 | Ancient | 0x7 | Contemporary |
| 0x3 | Classical | 0x8 | Current |
| 0x4 | Medieval | 0x9-F | Reserved |

---

## 7. ID Value / UID (bit 33-64)

### 7.1 정의

**하위 32비트는 UID (절대 식별자)를 직접 포함한다.**

| 항목 | 값 |
|------|-----|
| 크기 | 32비트 (uint32) |
| 최대값 | 4,294,967,295 (42억) |
| 위키데이터 현재 | ~1.5억 |
| **여유** | **28배** |

### 7.2 Lane별 UID 의미

| Lane | UID 의미 |
|------|----------|
| 0 (공식) | Q-ID/Synset 등 등록된 ID |
| 1 (자유) | Hash 기반 또는 Sequential ID |

### 7.3 UID 추출

```python
def get_uid(sidx: int) -> int:
    """하위 32비트 = UID"""
    return sidx & 0xFFFFFFFF
```

### 7.4 동일성 확인

```python
def is_same_entity(sidx_a: int, sidx_b: int) -> bool:
    """Lane + UID 비교로 동일 개체인지 확인"""
    lane_a = (sidx_a >> 37) & 0x1
    lane_b = (sidx_b >> 37) & 0x1
    uid_a = sidx_a & 0xFFFFFFFF
    uid_b = sidx_b & 0xFFFFFFFF
    return lane_a == lane_b and uid_a == uid_b
```

---

## 8. 연산

### 8.1 공식 SIDX 생성

```python
def make_official_sidx(
    entity_type: int,    # 8비트
    attrs: int,          # 12비트
    source: int,         # 3비트
    uid: int             # 32비트
) -> int:
    PREFIX = 0b110001    # 6비트
    LANE = 0             # 공식
    RESERVED = 0         # 2비트
    
    sidx = PREFIX << 58           # bit1-6
    sidx |= (entity_type << 50)   # bit7-14
    sidx |= (attrs << 38)         # bit15-26
    sidx |= (LANE << 37)          # bit27
    sidx |= (RESERVED << 35)      # bit28-29
    sidx |= (source << 32)        # bit30-32
    sidx |= uid                   # bit33-64
    
    return sidx
```

### 8.2 자유 SIDX 생성

```python
def make_free_sidx(
    entity_type: int,    # 8비트
    attrs: int,          # 12비트
    quant: int,          # 2비트
    number: int,         # 3비트
    uid: int             # 32비트
) -> int:
    PREFIX = 0b110001    # 6비트
    LANE = 1             # 자유
    
    sidx = PREFIX << 58           # bit1-6
    sidx |= (entity_type << 50)   # bit7-14
    sidx |= (attrs << 38)         # bit15-26
    sidx |= (LANE << 37)          # bit27
    sidx |= (quant << 35)         # bit28-29
    sidx |= (number << 32)        # bit30-32
    sidx |= uid                   # bit33-64
    
    return sidx
```

### 8.3 SIDX 파싱

```python
def parse_entity_sidx(sidx: int) -> dict:
    lane = (sidx >> 37) & 0x1
    
    result = {
        'entity_type': (sidx >> 50) & 0xFF,
        'attrs': (sidx >> 38) & 0xFFF,
        'lane': lane,
        'uid': sidx & 0xFFFFFFFF
    }
    
    if lane == 0:  # 공식
        result['source'] = (sidx >> 32) & 0x7
    else:          # 자유
        result['quant'] = (sidx >> 35) & 0x3
        result['number'] = (sidx >> 32) & 0x7
    
    return result
```

### 8.4 필드 추출

```python
# 상위 32비트 (약식)
def get_meta(sidx: int) -> int:
    return sidx >> 32

# 하위 32비트 (UID)
def get_uid(sidx: int) -> int:
    return sidx & 0xFFFFFFFF

# 공통 필드
def get_entity_type(sidx: int) -> int:
    return (sidx >> 50) & 0xFF

def get_attrs(sidx: int) -> int:
    return (sidx >> 38) & 0xFFF

def get_lane(sidx: int) -> int:
    return (sidx >> 37) & 0x1

def is_official(sidx: int) -> bool:
    return get_lane(sidx) == 0

def is_free(sidx: int) -> bool:
    return get_lane(sidx) == 1

# 공식 전용
def get_source(sidx: int) -> int:
    assert is_official(sidx)
    return (sidx >> 32) & 0x7

def is_qid(sidx: int) -> bool:
    return is_official(sidx) and get_source(sidx) == 0

# 자유 전용
def get_quant(sidx: int) -> int:
    assert is_free(sidx)
    return (sidx >> 35) & 0x3

def get_number(sidx: int) -> int:
    assert is_free(sidx)
    return (sidx >> 32) & 0x7

def is_singular(sidx: int) -> bool:
    return is_free(sidx) and get_number(sidx) == 1

def is_plural(sidx: int) -> bool:
    return is_free(sidx) and get_number(sidx) == 7

def is_universal(sidx: int) -> bool:
    return is_free(sidx) and get_quant(sidx) == 1

def is_existential(sidx: int) -> bool:
    return is_free(sidx) and get_quant(sidx) == 2
```

### 8.5 Q-ID → SIDX

```python
def qid_to_sidx(qid: str, entity_type: int, attrs: int = 0) -> int:
    uid = int(qid[1:])  # "Q312" → 312
    return make_official_sidx(entity_type, attrs, 0, uid)

# Apple Inc.
apple = qid_to_sidx("Q312", 0x91)  # Business
trump = qid_to_sidx("Q22686", 0x80)  # Human
```

### 8.6 자유 Entity 생성

```python
import hashlib

def make_abstract_entity(
    name: str, 
    entity_type: int, 
    quant: int = 0, 
    number: int = 0,
    attrs: int = 0
) -> int:
    hash_bytes = hashlib.sha256(name.encode()).digest()
    uid = int.from_bytes(hash_bytes[:4], 'big')
    return make_free_sidx(entity_type, attrs, quant, number, uid)

# "모든 학생들"
all_students = make_abstract_entity(
    "학생", 0x80,
    quant=0b01,    # 전칭
    number=0b111   # 복수
)

# "어떤 사람"
some_person = make_abstract_entity(
    "사람", 0x80,
    quant=0b10,    # 존재
    number=0b001   # 단수
)

# "세 마리의 고양이"
three_cats = make_abstract_entity(
    "고양이", 0xA0,
    quant=0b00,    # 특정
    number=0b011   # 3개
)
```

---

## 9. 사용 예시

### 9.1 공식: Apple Inc. (Q312)

```python
sidx = make_official_sidx(
    entity_type=0x91,  # Business
    attrs=0x2A8,       # notable=1, region=NorthAmerica, era=Current
    source=0,          # Q-ID
    uid=312            # Q312
)

# Lane=0 → 양화 없음 (항상 특정)
# Source=000 → Q-ID
```

### 9.2 자유: "모든 학생이 시험을 봤다"

```python
all_students = make_free_sidx(
    entity_type=0x80,  # Human
    attrs=0,
    quant=0b01,        # 전칭
    number=0b111,      # 복수
    uid=hash("학생")
)

# Verb Edge
exam = make_short_verb_edge(
    verb_id=TAKE_EXAM,
    tense=PAST,
    participants={AGT: all_students}
)
```

### 9.3 자유: "누가 왔어?" (질문)

```python
who = make_free_sidx(
    entity_type=0x80,  # Human
    attrs=0,
    quant=0b10,        # 존재
    number=0b001,      # 단수
    uid=0              # 미지정
)

# Verb Edge (의문)
query = make_short_verb_edge(
    verb_id=COME,
    mood=INTERROGATIVE,
    participants={AGT: who}
)
```

### 9.4 자유: "세 권의 책"

```python
three_books = make_free_sidx(
    entity_type=0x30,  # Book
    attrs=0,
    quant=0b00,        # 특정
    number=0b011,      # 3개
    uid=hash("책")
)
```

### 9.5 동일 인물, 다른 상태 (공식)

```python
# 사업가 시절 트럼프
trump_business = make_official_sidx(
    entity_type=0x80,  # Human
    attrs=0x2A7,       # era=Contemporary
    source=0,
    uid=22686
)

# 대통령 트럼프
trump_president = make_official_sidx(
    entity_type=0x80,  # Human
    attrs=0x2A8,       # era=Current
    source=0,
    uid=22686
)

# 동일성 확인
is_same_entity(trump_business, trump_president)  # True (Lane+UID 동일)
```

---

## 10. SIMD 필터링

```python
# 모든 Document (bit7 = 0)
def is_document(sidx): 
    return (sidx & (0x80 << 50)) == 0

# 모든 Human (0x80-0x8F)
def is_human(sidx):
    return ((sidx >> 50) & 0xF0) == 0x80

# 모든 Living (0x80-0xBF)
def is_living(sidx):
    return ((sidx >> 50) & 0xC0) == 0x80

# 공식 Q-ID인가?
def is_qid(sidx):
    lane = (sidx >> 37) & 0x1
    source = (sidx >> 32) & 0x7
    return lane == 0 and source == 0

# 자유 전칭 양화인가?
def is_universal(sidx):
    lane = (sidx >> 37) & 0x1
    quant = (sidx >> 35) & 0x3
    return lane == 1 and quant == 1

# 복수인가?
def is_plural(sidx):
    lane = (sidx >> 37) & 0x1
    number = (sidx >> 32) & 0x7
    return lane == 1 and number == 7
```

---

## 11. 약식 사용

### 11.1 상위 32비트만 사용

```python
# 약식 추출
def to_compact(sidx: int) -> int:
    """64비트 → 32비트 약식"""
    return sidx >> 32

# 약식에서 복원 (UID 없음)
def from_compact(compact: int, uid: int = 0) -> int:
    """32비트 약식 + UID → 64비트"""
    return (compact << 32) | uid
```

### 11.2 활용 시나리오

| 시나리오 | 사용 |
|----------|------|
| 메모리 절약 | 상위 32비트만 저장 |
| 분류/필터링 | 상위 32비트로 충분 |
| 동일성 확인 필요 | 전체 64비트 사용 |
| UID 직접 접근 | 하위 32비트 추출 |

---

## 12. 표준 채택 시 변경

### 12.1 Prefix 변경

```
표준 제안:  1100 01 (6비트)
표준 채택:  0001    (4비트)
```

### 12.2 비트 재배치

| 필드 | 표준 제안 | 표준 채택 |
|------|----------|----------|
| Prefix | bit1-6 (6) | bit1-4 (4) |
| Entity Type | bit7-14 (8) | bit5-12 (8) |
| Attributes | bit15-26 (12) | bit13-24 (12) |
| Lane | bit27 (1) | bit25 (1) |
| Lane별 해석 | bit28-32 (5) | bit26-30 (5) |
| **Reserved** | - | **bit31-32 (2)** |
| UID | bit33-64 (32) | bit33-64 (32) |

**표준 채택 시 2비트 추가 Reserved 확보.**

---

## 부록 A: 비트 요약

### 표준 제안 (현재)

```
[상위 32비트 - 약식 사용 가능]
bit1-6:   110001 (Standard Proposal Entity)
bit7-14:  Entity Type (8비트)
bit15-18: Flags (fictional, historical, notable, controversial)
bit19-22: Region (16개)
bit23-26: Era (16개)
bit27:    Lane (0=공식, 1=자유)
bit28-32: Lane별 해석 (5비트)
  Lane=0: Reserved(2) + Source(3)
  Lane=1: Quantification(2) + Number(3)

[하위 32비트 - UID]
bit33-64: UID (32비트, uint32)
```

### 필드 오프셋

| 필드 | 시프트 | 마스크 |
|------|--------|--------|
| Entity Type | >> 50 | & 0xFF |
| Attributes | >> 38 | & 0xFFF |
| Lane | >> 37 | & 0x1 |
| Source (Lane=0) | >> 32 | & 0x7 |
| Quant (Lane=1) | >> 35 | & 0x3 |
| Number (Lane=1) | >> 32 | & 0x7 |
| UID | - | & 0xFFFFFFFF |

---

## 부록 B: Lane별 bit28-32 해석

### 공식 (Lane=0)

```
bit28-29: Reserved (00)
bit30-32: Source
  000: Q-ID (위키데이터 Item)
  001: Synset (워드넷)
  010: P-ID (위키데이터 Property)
  011: Lexeme (위키데이터 어휘)
  100: Schema.org
  101-111: Reserved
```

### 자유 (Lane=1)

```
bit28-29: Quantification
  00: 특정 (Specific)
  01: 전칭 (Universal, ∀)
  10: 존재 (Existential, ∃)
  11: 불특정 (Arbitrary)

bit30-32: Number
  000: 알 수 없음
  001: 단수 (1)
  010: 2개
  011: 3개
  100: 4개
  101: 5개
  110: 6개
  111: 복수 (많다)
```

---

## 부록 C: Prefix 할당 체계

| 타입 | Prefix | 비트 | 워드 |
|------|--------|------|------|
| Short Verb Edge | `1100 1` | 5 | 3 |
| Entity | `1100 01` | 6 | 4 |
| Verb Edge | `1100 001` | 7 | 5 |
| Triple Edge | `1100 0001` | 8 | 2 |
| Clause Edge | `1100 00001` | 9 | 1 |
| Event6 Edge | `1100 000001` | 10 | 1 |
| Context Edge | `1100 0000001` | 11 | 1 |
| Reserved | `1100 0000000` | 11 | - |

---

## 부록 D: 참고 문서

- `GEUL_비트명세.md` - 전체 비트 레이아웃
- `Verb_Edge_문법.md` - Verb Edge 명세
- `Triple_Edge_문법.md` - Triple Edge 명세
- `Clause_Edge_문법.md` - Clause Edge 명세

---

**버전:** v0.5  
**상태:** 표준 제안  
**작성일:** 2026-01-29

**v0.5 주요 변경:**
- Lane별 필드 분기 설계
  - Lane=0 (공식): Reserved(2) + Source(3)
  - Lane=1 (자유): Quantification(2) + Number(3)
- 비트 레이아웃 재정렬 (bit27=Lane, bit28-32=Lane별)
- Number 3비트 추가 (수량 명시)
- 공식 ID는 항상 특정 → 양화 불필요