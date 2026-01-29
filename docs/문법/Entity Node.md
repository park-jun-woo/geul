# Entity Node 명세서

**버전:** v0.2  
**작성일:** 2026-01-29  
**범위:** 개체(Entity) SIDX  
**상태:** 표준 제안 (Standard Proposal)

---

## 1. 개요

### 1.1 정의

**Entity Node**는 GEUL 스트림에서 개체(사람, 장소, 사물, 조직, 개념 등)를 식별하는 가변 길이 패킷이다.

### 1.2 Lane 분기

| Lane | 의미 | UID | 워드 |
|------|------|-----|------|
| 0 | 개체 (구체적) | 선택적 | 3 또는 5 |
| 1 | 추상개체 | ✗ | 3 |

- **개체(Lane=0):** Q-ID 등 등록된 ID, UID 명시 여부 선택
- **추상개체(Lane=1):** "모든 학생", "어떤 것" 등, UID 불필요

### 1.3 모드 요약

| 모드 | Lane | UIDflag | 워드 | 용도 |
|------|------|---------|------|------|
| 약식 | 0 | 0 | 3 | 재참조, 문맥 내 |
| 정식 | 0 | 1 | 5 | Q-ID 명시, 외부 참조 |
| 추상 | 1 | - | 3 | 양화 표현 |

---

## 2. Prefix

`SIDX.md` 참조

| 항목 | 값 |
|------|-----|
| Standard | `0 001` (4비트) |
| Proposal | `1100 001` (7비트) |
| 1st 워드 나머지 | 9비트 (Lane + EntityType) |

---

## 3. 약식/추상 Entity (3워드 = 48비트)

### 3.1 구조

```
1st WORD (16비트)
┌─────────┬──────┬────────────┐
│ Prefix  │ Lane │ EntityType │
│  7bit   │ 1bit │   8bit     │
└─────────┴──────┴────────────┘

2nd WORD (16비트)
┌────────────┬────────────────┐
│ Attributes │    Lane별      │
│   12bit    │     4bit       │
└────────────┴────────────────┘

3rd WORD (16비트)
┌────────────────────────────────┐
│              TID               │
│             16bit              │
└────────────────────────────────┘
```

### 3.2 필드 요약

| 필드 | 비트 | 크기 | 설명 |
|------|------|------|------|
| Prefix | 1-7 | 7 | `1100001` |
| Lane | 8 | 1 | 0=개체, 1=추상 |
| EntityType | 9-16 | 8 | 256개 타입 |
| Attributes | 17-28 | 12 | 4,096 조합 |
| Lane별 해석 | 29-32 | 4 | Lane에 따라 다름 |
| TID | 33-48 | 16 | 문맥 내 참조 ID |

### 3.3 Lane별 해석 (bit 29-32)

#### Lane=0 (개체 약식)

```
bit29-31: Source (3비트)
bit32:    UIDflag = 0 (약식)
```

| Source | 코드 | 출처 |
|--------|------|------|
| 000 | Q-ID | 위키데이터 Item |
| 001 | Synset | 워드넷 |
| 010 | P-ID | 위키데이터 Property |
| 011 | Lexeme | 위키데이터 어휘 |
| 100 | Schema | Schema.org |
| 101-111 | Reserved | - |

#### Lane=1 (추상개체)

```
bit29-30: Quantification (2비트)
bit31-32: Number (2비트)
```

**Quantification:**

| 값 | 의미 | 논리 | 예시 |
|----|------|------|------|
| 00 | 특정 | ι | "그 사람" |
| 01 | 전칭 | ∀ | "모든 학생" |
| 10 | 존재 | ∃ | "어떤 사람" |
| 11 | 불특정 | ε | "아무나" |

**Number:**

| 값 | 의미 | 예시 |
|----|------|------|
| 00 | 알 수 없음 | "사람(들)" |
| 01 | 단수 | "한 사람" |
| 10 | 소수 | "몇몇" |
| 11 | 다수 | "많은" |

---

## 4. 정식 Entity (5워드 = 80비트)

### 4.1 구조

```
1st WORD (16비트)
┌─────────┬──────┬────────────┐
│ Prefix  │ Lane │ EntityType │
│  7bit   │ 1bit │   8bit     │
└─────────┴──────┴────────────┘

2nd WORD (16비트)
┌────────────┬────────┬─────────┐
│ Attributes │ Source │ UIDflag │
│   12bit    │  3bit  │ 1bit=1  │
└────────────┴────────┴─────────┘

3rd + 4th WORD (32비트)
┌────────────────────────────────┐
│              UID               │
│             32bit              │
└────────────────────────────────┘

5th WORD (16비트)
┌────────────────────────────────┐
│              TID               │
│             16bit              │
└────────────────────────────────┘
```

### 4.2 필드 요약

| 필드 | 비트 | 크기 | 설명 |
|------|------|------|------|
| Prefix | 1-7 | 7 | `1100001` |
| Lane | 8 | 1 | 0 (개체) |
| EntityType | 9-16 | 8 | 256개 타입 |
| Attributes | 17-28 | 12 | 4,096 조합 |
| Source | 29-31 | 3 | Q-ID, Synset 등 |
| UIDflag | 32 | 1 | 1 (정식) |
| UID | 33-64 | 32 | 절대 식별자 |
| TID | 65-80 | 16 | 문맥 내 참조 ID |

### 4.3 UID (32비트)

| 항목 | 값 |
|------|-----|
| 크기 | 32비트 (uint32) |
| 최대값 | 4,294,967,295 (42억) |
| 위키데이터 현재 | ~1.5억 |
| **여유** | **28배** |

---

## 5. Entity Type (bit 9-16)

### 5.1 이진 트리 구조

**Level 0 (bit 9):**
```
0: Document 계열
1: Entity 계열
```

**Level 1 (bit 10):**
```
00: Article     01: Media
10: Living      11: Non-living
```

**Level 2 (bit 11):**
```
100: Sapient    101: Non-sapient
110: Physical   111: Abstract
```

**Level 3 (bit 12):**
```
1000: Human         1001: Organization
1010: Organism      1011: Celestial
1100: Location      1101: Artifact
1110: Concept       1111: Measure
```

### 5.2 주요 코드

| 코드 | 분류 | 코드 | 분류 |
|------|------|------|------|
| 0x00 | Scholarly Article | 0x80 | Human |
| 0x10 | Encyclopedia | 0x90 | Organization |
| 0x20 | Painting | 0x91 | Business |
| 0x21 | Film | 0xA0 | Taxon |
| 0x30 | Book | 0xC0 | Settlement |
| 0x31 | Literary Work | 0xD0 | Building |
| 0x32 | Album | 0xE0 | Concept |

---

## 6. Attributes (bit 17-28)

### 6.1 구조 (12비트)

```
bit17:    is_fictional
bit18:    is_historical
bit19:    is_notable
bit20:    is_controversial
bit21-24: region (16개)
bit25-28: era (16개)
```

### 6.2 Region (bit 21-24)

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

### 6.3 Era (bit 25-28)

| 코드 | 시대 | 코드 | 시대 |
|------|------|------|------|
| 0x0 | Unknown | 0x5 | Early Modern |
| 0x1 | Prehistoric | 0x6 | Modern |
| 0x2 | Ancient | 0x7 | Contemporary |
| 0x3 | Classical | 0x8 | Current |
| 0x4 | Medieval | 0x9-F | Reserved |

---

## 7. 연산

### 7.1 약식 Entity 생성 (Lane=0, UIDflag=0)

```python
def make_short_entity(
    entity_type: int,    # 8비트
    attrs: int,          # 12비트
    source: int,         # 3비트
    tid: int             # 16비트
) -> int:
    PREFIX = 0b1100001   # 7비트
    LANE = 0             # 개체
    UIDFLAG = 0          # 약식
    
    word1 = (PREFIX << 9) | (LANE << 8) | entity_type
    word2 = (attrs << 4) | (source << 1) | UIDFLAG
    word3 = tid
    
    return (word1 << 32) | (word2 << 16) | word3
```

### 7.2 정식 Entity 생성 (Lane=0, UIDflag=1)

```python
def make_full_entity(
    entity_type: int,    # 8비트
    attrs: int,          # 12비트
    source: int,         # 3비트
    uid: int,            # 32비트
    tid: int             # 16비트
) -> int:
    PREFIX = 0b1100001   # 7비트
    LANE = 0             # 개체
    UIDFLAG = 1          # 정식
    
    word1 = (PREFIX << 9) | (LANE << 8) | entity_type
    word2 = (attrs << 4) | (source << 1) | UIDFLAG
    word3_4 = uid
    word5 = tid
    
    return (word1 << 64) | (word2 << 48) | (word3_4 << 16) | word5
```

### 7.3 추상 Entity 생성 (Lane=1)

```python
def make_abstract_entity(
    entity_type: int,    # 8비트
    attrs: int,          # 12비트
    quant: int,          # 2비트
    number: int,         # 2비트
    tid: int             # 16비트
) -> int:
    PREFIX = 0b1100001   # 7비트
    LANE = 1             # 추상
    
    word1 = (PREFIX << 9) | (LANE << 8) | entity_type
    word2 = (attrs << 4) | (quant << 2) | number
    word3 = tid
    
    return (word1 << 32) | (word2 << 16) | word3
```

### 7.4 파싱

```python
def parse_entity(data: bytes) -> dict:
    word1 = int.from_bytes(data[0:2], 'big')
    word2 = int.from_bytes(data[2:4], 'big')
    
    lane = (word1 >> 8) & 0x1
    entity_type = word1 & 0xFF
    attrs = (word2 >> 4) & 0xFFF
    
    result = {
        'lane': lane,
        'entity_type': entity_type,
        'attrs': attrs
    }
    
    if lane == 0:  # 개체
        source = (word2 >> 1) & 0x7
        uidflag = word2 & 0x1
        result['source'] = source
        result['uidflag'] = uidflag
        
        if uidflag == 0:  # 약식 (3워드)
            result['tid'] = int.from_bytes(data[4:6], 'big')
        else:             # 정식 (5워드)
            result['uid'] = int.from_bytes(data[4:8], 'big')
            result['tid'] = int.from_bytes(data[8:10], 'big')
    
    else:  # 추상 (Lane=1)
        result['quant'] = (word2 >> 2) & 0x3
        result['number'] = word2 & 0x3
        result['tid'] = int.from_bytes(data[4:6], 'big')
    
    return result
```

---

## 8. 사용 예시

### 8.1 정식: Apple Inc. (Q312)

```python
apple = make_full_entity(
    entity_type=0x91,  # Business
    attrs=0x2A8,       # notable, NorthAmerica, Current
    source=0,          # Q-ID
    uid=312,           # Q312
    tid=0x0001
)
# 5워드 = 80비트
```

### 8.2 약식: 재참조

```python
# 이미 정식으로 선언된 Apple을 재참조
apple_ref = make_short_entity(
    entity_type=0x91,  # Business
    attrs=0x2A8,
    source=0,          # Q-ID
    tid=0x0001         # 같은 TID
)
# 3워드 = 48비트
```

### 8.3 추상: "모든 학생"

```python
all_students = make_abstract_entity(
    entity_type=0x80,  # Human
    attrs=0,
    quant=0b01,        # 전칭 (Universal)
    number=0b11,       # 다수
    tid=0x0010
)
# 3워드 = 48비트
```

### 8.4 추상: "어떤 사람"

```python
someone = make_abstract_entity(
    entity_type=0x80,  # Human
    attrs=0,
    quant=0b10,        # 존재 (Existential)
    number=0b01,       # 단수
    tid=0x0011
)
# 3워드 = 48비트
```

---

## 9. 모드 판별

```python
def get_entity_mode(data: bytes) -> str:
    word1 = int.from_bytes(data[0:2], 'big')
    word2 = int.from_bytes(data[2:4], 'big')
    
    lane = (word1 >> 8) & 0x1
    
    if lane == 1:
        return "추상"
    
    uidflag = word2 & 0x1
    return "정식" if uidflag else "약식"

def get_entity_words(data: bytes) -> int:
    mode = get_entity_mode(data)
    return 5 if mode == "정식" else 3
```

---

## 부록 A: 비트 요약

### 약식/추상 (3워드)

```
1st WORD (bit 1-16):
  bit1-7:   1100001 (Prefix)
  bit8:     Lane (0=개체, 1=추상)
  bit9-16:  EntityType

2nd WORD (bit 17-32):
  bit17-28: Attributes
  bit29-32: Lane별 해석
    Lane=0: Source(3) + UIDflag(1)=0
    Lane=1: Quant(2) + Number(2)

3rd WORD (bit 33-48):
  bit33-48: TID
```

### 정식 (5워드)

```
1st WORD (bit 1-16):
  bit1-7:   1100001 (Prefix)
  bit8:     Lane = 0
  bit9-16:  EntityType

2nd WORD (bit 17-32):
  bit17-28: Attributes
  bit29-31: Source
  bit32:    UIDflag = 1

3rd+4th WORD (bit 33-64):
  bit33-64: UID (32비트)

5th WORD (bit 65-80):
  bit65-80: TID
```

---

## 부록 B: 필드 오프셋

### 1st WORD

| 필드 | 마스크 | 시프트 |
|------|--------|--------|
| Prefix | 0xFE00 | >> 9 |
| Lane | 0x0100 | >> 8 |
| EntityType | 0x00FF | - |

### 2nd WORD (Lane=0)

| 필드 | 마스크 | 시프트 |
|------|--------|--------|
| Attributes | 0xFFF0 | >> 4 |
| Source | 0x000E | >> 1 |
| UIDflag | 0x0001 | - |

### 2nd WORD (Lane=1)

| 필드 | 마스크 | 시프트 |
|------|--------|--------|
| Attributes | 0xFFF0 | >> 4 |
| Quant | 0x000C | >> 2 |
| Number | 0x0003 | - |

---

## 버전 히스토리

| 버전 | 날짜 | 변경 |
|------|------|------|
| v0.1 | 2026-01-29 | 초안 작성 |
| v0.2 | 2026-01-29 | Prefix 섹션 간소화, SIDX.md 참조로 변경 |

---

**문서 종료**