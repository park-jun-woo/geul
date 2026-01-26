# 개체 SIDX 명세서

**버전:** v0.3  
**작성일:** 2026-01-27  
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

```
동일 인물, 다른 SIDX:
  SIDX_A: 사업가 시절 트럼프 (UID=22686)
  SIDX_B: 대통령 트럼프 (UID=22686)
  
  → 하위 32비트 (UID) 비교로 동일성 즉시 확인
  → is_same_entity = (sidx_a & 0xFFFFFFFF) == (sidx_b & 0xFFFFFFFF)
```

### 1.3 약식 사용

**상위 32비트만으로 약식 사용 가능:**
- Entity Type, Attributes, Lane, Source 포함
- UID 없이도 분류/필터링 가능
- 메모리 절약 시 활용

### 1.4 표준 제안 상태

| 상태 | Prefix | 가용 비트 |
|------|--------|----------|
| **표준 제안** | `1100 000` (7비트) | **57비트** |
| 표준 채택 후 | `0000` (4비트) | 60비트 |

---

## 2. 비트 레이아웃

### 2.1 전체 구조 (64비트)

```
┌──────────────────── 상위 32비트 (약식) ────────────────────┐┌─── 하위 32비트 (UID) ───┐
│                                                            ││                          │
┌─────────┬─────────────┬────────────┬──────┬─────┬────────┬┬──────────────────────────┐
│ Prefix  │ Entity Type │ Attributes │ Lane │ Rsv │ Source ││ ID Value (UID)           │
│ (7b)    │ (8b)        │ (12b)      │ (1b) │ (1b)│ (3b)   ││ (32b)                    │
└─────────┴─────────────┴────────────┴──────┴─────┴────────┴┴──────────────────────────┘
  bit1-7    bit8-15       bit16-27    bit28  bit29  bit30-32  bit33-64
```

### 2.2 필드별 상세

| 필드 | 비트 범위 | 크기 | 설명 |
|------|----------|------|------|
| Prefix | 1-7 | 7 | 고정값 `1100 000` |
| Entity Type | 8-15 | 8 | 256개 타입 (이진 트리) |
| Attributes | 16-27 | 12 | 4,096 조합 |
| Lane | 28 | 1 | 0=공식, 1=자유 |
| **Reserved** | **29** | **1** | **향후 확장 (Lane과 Source 사이)** |
| Source | 30-32 | 3 | ID 출처 (8개) |
| ID Value | 33-64 | 32 | **UID (uint32)** |

### 2.3 32비트 경계 설계

```
상위 32비트 (bit1-32):  메타데이터
  - 7 + 8 + 12 + 1 + 1 + 3 = 32비트

하위 32비트 (bit33-64): UID
  - 32비트 uint32 정렬
```

**이점:**
- 약식 사용: 상위 32비트만 추출
- UID 추출: 하위 32비트만 추출 `sidx & 0xFFFFFFFF`
- 메모리/캐시 친화적

---

## 3. Prefix (bit 1-7)

GEUL_비트명세.md에 따른 고정값:

```
bit1:   1 (Extension)
bit2:   1 (Free/Future)
bit3:   0 (Free)
bit4:   0 (Standard Proposal)
bit5:   0 (Node)
bit6:   0 (Entity/Verb/Context 그룹)
bit7:   0 (Entity)
─────────────────────────
합계:   1100 000
```

---

## 4. Entity Type (bit 8-15)

### 4.1 이진 트리 구조

**Level 0 (bit 8):**
```
0: Document 계열 (52%)
1: Entity 계열 (48%)
```

**Level 1 (bit 9):**
```
00: Article     01: Media
10: Living      11: Non-living
```

**Level 2 (bit 10):**
```
000: Academic   001: Reference
010: Visual     011: Literary
100: Sapient    101: Non-sapient
110: Physical   111: Abstract
```

**Level 3 (bit 11):**
```
1000: Human         1001: Organization
1010: Organism      1011: Celestial
1100: Location      1101: Artifact
1110: Concept       1111: Measure
```

### 4.2 코드 테이블

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

## 5. Attributes (bit 16-27)

### 5.1 구조 (12비트)

```
bit16:    is_fictional
bit17:    is_historical
bit18:    is_notable
bit19:    is_controversial
bit20-23: region (16개)
bit24-27: era (16개)
```

### 5.2 Region (bit 20-23)

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

### 5.3 Era (bit 24-27)

| 코드 | 시대 | 코드 | 시대 |
|------|------|------|------|
| 0x0 | Unknown | 0x5 | Early Modern |
| 0x1 | Prehistoric | 0x6 | Modern |
| 0x2 | Ancient | 0x7 | Contemporary |
| 0x3 | Classical | 0x8 | Current |
| 0x4 | Medieval | 0x9-F | Reserved |

---

## 6. Lane (bit 28)

| 값 | 의미 | 용도 |
|----|------|------|
| 0 | **공식** | Q-ID, Synset 등 등록된 ID |
| 1 | **자유** | 소설 캐릭터, 게임 NPC, 임시 개체 |

**충돌 방지:**
```
Q312:        Lane=0, UID=312
내 캐릭터:   Lane=1, UID=hash(...)
→ Lane이 다르므로 충돌 없음
```

---

## 7. Reserved (bit 29)

**Lane과 Source 사이에 위치한 1비트 예약 필드.**

| 용도 | 설명 |
|------|------|
| 향후 확장 | Lane 또는 Source 확장 시 활용 |
| 버전 구분 | 스키마 버전 표시 가능 |
| 현재 | **항상 0** |

**위치 선정 이유:**
- 상위 32비트 경계 맞춤
- Lane/Source 확장 여지 확보

---

## 8. Source (bit 30-32)

### 8.1 공식 영역 (Lane=0)

| 코드 | 출처 | 현재 규모 | 32비트 용량 |
|------|------|----------|------------|
| 000 | **Q-ID** | ~1.5억 | 42억 |
| 001 | **Synset** | ~12만 | 42억 |
| 010 | **P-ID** | ~1.2만 | 42억 |
| 011 | **Lexeme** | ~100만 | 42억 |
| 100 | Schema.org | ~2천 | 42억 |
| 101-111 | Reserved | - | - |

### 8.2 자유 영역 (Lane=1)

| 코드 | 용도 |
|------|------|
| 000 | Hash 기반 |
| 001 | Sequential |
| 010 | UUID 축약 |
| 011-111 | 사용자 정의 |

---

## 9. ID Value / UID (bit 33-64)

### 9.1 정의

**하위 32비트는 UID (절대 식별자)를 직접 포함한다.**

| 항목 | 값 |
|------|-----|
| 크기 | 32비트 (uint32) |
| 최대값 | 4,294,967,295 (42억) |
| 위키데이터 현재 | ~1.5억 |
| **여유** | **28배** |

### 9.2 UID 추출

```python
def get_uid(sidx: int) -> int:
    """하위 32비트 = UID"""
    return sidx & 0xFFFFFFFF
```

### 9.3 동일성 확인

```python
def is_same_entity(sidx_a: int, sidx_b: int) -> bool:
    """UID 비교로 동일 개체인지 확인"""
    return get_uid(sidx_a) == get_uid(sidx_b)
```

**MAP DB 불필요** — UID가 SIDX에 직접 포함되어 있으므로 즉시 비교 가능.

---

## 10. 연산

### 10.1 SIDX 생성

```python
def make_entity_sidx(
    entity_type: int,    # 8비트
    attrs: int,          # 12비트
    lane: int,           # 1비트
    source: int,         # 3비트
    uid: int             # 32비트
) -> int:
    PREFIX = 0b1100_000
    RESERVED = 0  # 항상 0
    
    sidx = PREFIX << 57           # bit1-7
    sidx |= (entity_type << 49)   # bit8-15
    sidx |= (attrs << 37)         # bit16-27
    sidx |= (lane << 36)          # bit28
    sidx |= (RESERVED << 35)      # bit29
    sidx |= (source << 32)        # bit30-32
    sidx |= uid                   # bit33-64
    
    return sidx
```

### 10.2 SIDX 파싱

```python
def parse_entity_sidx(sidx: int) -> dict:
    return {
        'entity_type': (sidx >> 49) & 0xFF,
        'attrs': (sidx >> 37) & 0xFFF,
        'lane': (sidx >> 36) & 0x1,
        'reserved': (sidx >> 35) & 0x1,
        'source': (sidx >> 32) & 0x7,
        'uid': sidx & 0xFFFFFFFF
    }
```

### 10.3 필드 추출

```python
# 상위 32비트 (약식)
def get_meta(sidx: int) -> int:
    return sidx >> 32

# 하위 32비트 (UID)
def get_uid(sidx: int) -> int:
    return sidx & 0xFFFFFFFF

# 개별 필드
def get_entity_type(sidx: int) -> int:
    return (sidx >> 49) & 0xFF

def get_attrs(sidx: int) -> int:
    return (sidx >> 37) & 0xFFF

def get_lane(sidx: int) -> int:
    return (sidx >> 36) & 0x1

def get_source(sidx: int) -> int:
    return (sidx >> 32) & 0x7

def is_official(sidx: int) -> bool:
    return get_lane(sidx) == 0

def is_free(sidx: int) -> bool:
    return get_lane(sidx) == 1

def is_qid(sidx: int) -> bool:
    return is_official(sidx) and get_source(sidx) == 0
```

### 10.4 Q-ID → SIDX

```python
def qid_to_sidx(qid: str, entity_type: int, attrs: int = 0) -> int:
    uid = int(qid[1:])  # "Q312" → 312
    return make_entity_sidx(entity_type, attrs, 0, 0, uid)

# Apple Inc.
apple = qid_to_sidx("Q312", 0x91)  # Business
trump = qid_to_sidx("Q22686", 0x80)  # Human
```

### 10.5 자유 ID 생성

```python
import hashlib

def make_free_sidx(name: str, entity_type: int, attrs: int = 0) -> int:
    hash_bytes = hashlib.sha256(name.encode()).digest()
    uid = int.from_bytes(hash_bytes[:4], 'big')
    return make_entity_sidx(entity_type, attrs, 1, 0, uid)

# 소설 캐릭터
hero = make_free_sidx("김철수", 0x81)  # Fictional Human
```

---

## 11. SIMD 필터링

```python
# 모든 Document (bit8 = 0)
def is_document(sidx): 
    return (sidx & (0x80 << 49)) == 0

# 모든 Human (0x80-0x8F)
def is_human(sidx):
    return ((sidx >> 49) & 0xF0) == 0x80

# 모든 Living (0x80-0xBF)
def is_living(sidx):
    return ((sidx >> 49) & 0xC0) == 0x80

# 공식 Q-ID인가?
def is_qid(sidx):
    lane = (sidx >> 36) & 0x1
    source = (sidx >> 32) & 0x7
    return lane == 0 and source == 0
```

---

## 12. 약식 사용

### 12.1 상위 32비트만 사용

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

### 12.2 활용 시나리오

| 시나리오 | 사용 |
|----------|------|
| 메모리 절약 | 상위 32비트만 저장 |
| 분류/필터링 | 상위 32비트로 충분 |
| 동일성 확인 필요 | 전체 64비트 사용 |
| UID 직접 접근 | 하위 32비트 추출 |

---

## 13. 사용 예시

### 13.1 Apple Inc. (Q312)

```python
sidx = make_entity_sidx(
    entity_type=0x91,  # Business
    attrs=0x2A8,       # notable=1, region=NorthAmerica, era=Current
    lane=0,            # 공식
    source=0,          # Q-ID
    uid=312            # Q312
)

# 비트 구조:
# [상위 32비트]                              [하위 32비트]
# 1100000 | 10010001 | 001010101000 | 0 | 0 | 000 || 00000000000000000000000100111000
# prefix  | Business | attrs        | L | R | Src || 312

# UID 추출
uid = sidx & 0xFFFFFFFF  # → 312
```

### 13.2 동일 인물, 다른 상태

```python
# 사업가 시절 트럼프
trump_business = make_entity_sidx(
    entity_type=0x80,  # Human
    attrs=0x2A7,       # era=Contemporary
    lane=0, source=0,
    uid=22686
)

# 대통령 트럼프
trump_president = make_entity_sidx(
    entity_type=0x80,  # Human
    attrs=0x2A8,       # era=Current
    lane=0, source=0,
    uid=22686
)

# 동일성 확인
is_same_entity(trump_business, trump_president)  # True (UID 동일)
```

### 13.3 소설 캐릭터

```python
# 자유 영역 (Lane=1)
hero = make_free_sidx("김철수", 0x81, 0x118)

# 공식 Q-ID와 절대 충돌 없음
get_lane(hero)  # → 1 (자유)
```

---

## 14. 표준 채택 시 변경

### 14.1 Prefix 변경

```
표준 제안:  1100 000 (7비트)
표준 채택:  0000     (4비트)
```

### 14.2 비트 재배치

| 필드 | 표준 제안 | 표준 채택 |
|------|----------|----------|
| Prefix | bit1-7 (7) | bit1-4 (4) |
| Entity Type | bit8-15 (8) | bit5-12 (8) |
| Attributes | bit16-27 (12) | bit13-24 (12) |
| Lane | bit28 (1) | bit25 (1) |
| Reserved | bit29 (1) | bit26 (1) |
| Source | bit30-32 (3) | bit27-29 (3) |
| **Reserved2** | - | **bit30-32 (3)** |
| UID | bit33-64 (32) | bit33-64 (32) |

**표준 채택 시 3비트 추가 Reserved 확보.**

---

## 부록 A: 비트 요약

### 표준 제안 (현재)

```
[상위 32비트 - 약식 사용 가능]
bit1-7:   1100 000 (Standard Proposal Entity)
bit8-15:  Entity Type (8비트)
bit16-19: Flags (fictional, historical, notable, controversial)
bit20-23: Region (16개)
bit24-27: Era (16개)
bit28:    Lane (0=공식, 1=자유)
bit29:    Reserved (항상 0)
bit30-32: Source (Q-ID/Synset/P-ID/Lexeme)

[하위 32비트 - UID]
bit33-64: UID (32비트, uint32)
```

### 필드 오프셋

| 필드 | 시프트 | 마스크 |
|------|--------|--------|
| Entity Type | >> 49 | & 0xFF |
| Attributes | >> 37 | & 0xFFF |
| Lane | >> 36 | & 0x1 |
| Reserved | >> 35 | & 0x1 |
| Source | >> 32 | & 0x7 |
| UID | - | & 0xFFFFFFFF |

---

## 부록 B: Source 코드

| Lane | Source | 코드 | 용도 |
|------|--------|------|------|
| 0 | 000 | Q-ID | 위키데이터 Item |
| 0 | 001 | Synset | 워드넷 |
| 0 | 010 | P-ID | 위키데이터 Property |
| 0 | 011 | Lexeme | 위키데이터 어휘 |
| 0 | 100 | Schema.org | 웹 표준 |
| 0 | 101-111 | Reserved | - |
| 1 | 000-111 | User NS | 사용자 정의 |

---

## 부록 C: 참고 문서

- `GEUL_비트명세.md` - 전체 비트 레이아웃
- `동사_SIDX.md` - 동사 SIDX (별도)
- `GEUL_문법.md` - 전체 문법 명세

---

**버전:** v0.3  
**상태:** 표준 제안  
**작성일:** 2026-01-27

**v0.3 주요 변경:**
- UID를 SIDX 하위 32비트에 직접 포함
- Reserved를 Lane과 Source 사이에 배치 (bit29)
- 상위/하위 32비트 경계 정렬 (약식 사용 지원)
- 동일성 확인: UID 직접 비교 (MAP DB 불필요)