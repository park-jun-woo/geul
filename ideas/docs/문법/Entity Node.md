# Entity Node 명세서

**버전:** v0.4
**작성일:** 2026-02-01 (2026-02-28 갱신)
**범위:** 개체(Entity) SIDX
**상태:** 표준 제안 (Standard Proposal)

---

## 1. 개요

### 1.1 정의

**Entity Node**는 GEUL 스트림에서 개체(사람, 장소, 사물, 조직, 개념 등)를 식별하는 **고정 길이 4워드 패킷**이다.

### 1.2 SIDX 본질

| 특성 | 설명 |
|------|------|
| **Non-unique** | 같은 SIDX에 여러 개체 가능 |
| **Multi-SIDX** | 한 개체가 여러 SIDX 가능 (시점/역할별) |
| **비트 = 의미** | 비트 위치 자체가 속성을 나타냄 |
| **추상/구체 연속** | Mode와 Attributes 채움 정도로 구분 |

**예시:**
- 트럼프 (부동산 사업가) → SIDX_A
- 트럼프 (대통령) → SIDX_B (다른 SIDX)
- "Human + Male + Korea" → 추상적 "한국 남자"
- "Human + Male + Korea + 1946 + Business + ..." → 거의 특정 인물

### 1.3 설계 원칙

**Q아이디 내재 포기:**
- 순수 의미정렬에 비트 전체 투자
- SIMD 필터링 성능 극대화
- Q아이디는 Triple로 별도 연결: `(Entity_SIDX, P-외부ID, "Q12345")`

**Serial 비트 불필요:**
- 쿼리는 2단계: SIMD 범위 좁히기 → 범위 내 디테일 체크
- Serial은 의미 없는 숫자라 SIMD에 기여 안 함
- 그 비트를 의미정렬에 투자하면 1단계에서 더 좁혀짐

---

## 2. Prefix

`SIDX.md` 참조

| 항목 | 값 |
|------|-----|
| Standard | `001 001` (6비트) |
| Proposal | `0001 001` (7비트) |
| 1st 워드 나머지 | 9비트 (Mode + EntityType) |

---

## 3. 구조 (4워드 = 64비트)

### 3.1 비트 레이아웃

```
1st WORD (16비트)
┌─────────┬──────┬────────────┐
│ Prefix  │ Mode │ EntityType │
│  7bit   │ 3bit │   6bit     │
└─────────┴──────┴────────────┘

2nd WORD (16비트)
┌─────────────────────────────┐
│     Attributes 상위 16비트   │
└─────────────────────────────┘

3rd WORD (16비트)
┌─────────────────────────────┐
│     Attributes 중위 16비트   │
└─────────────────────────────┘

4th WORD (16비트)
┌─────────────────────────────┐
│     Attributes 하위 16비트   │
└─────────────────────────────┘
```

### 3.2 필드 요약

| 필드 | 비트 | 크기 | 설명 |
|------|------|------|------|
| Prefix | 1-7 | 7 | `0001001` (Proposal) |
| Mode | 8-10 | 3 | 8가지 양화/수 모드 |
| EntityType | 11-16 | 6 | 64개 상위 타입 |
| Attributes | 17-64 | 48 | 타입별 가변 스키마 |

### 3.3 v0.3 대비 개선

| 항목 | v0.3 | v0.4 |
|------|------|------|
| 구조 | 고정 3워드 (48비트) | **고정 4워드 (64비트)** |
| Attributes | 32비트 | **48비트** |
| EntityType | 6비트 (64개) | 6비트 (64개, 코드 테이블 재배치) |
| **의미정렬 총량** | 41비트 | **57비트** |

---

## 4. Mode (bit 8-10)

### 4.1 정의

Mode는 개체의 **양화(Quantification)와 수(Number)**를 3비트로 통합 표현한다.

### 4.2 코드 테이블

| 코드 | 이진 | 의미 | 예시 |
|------|------|------|------|
| 0 | 000 | **등록 개체** | 이순신, 삼성전자, BTS |
| 1 | 001 | 특정 단수 | "그 사람" |
| 2 | 010 | 특정 소수 | "그 몇몇" |
| 3 | 011 | 특정 다수 | "그 사람들" |
| 4 | 100 | 전칭 | "모든 ~" |
| 5 | 101 | 존재 | "어떤 ~" |
| 6 | 110 | 불특정 | "아무 ~" |
| 7 | 111 | 총칭 | "한국인이란" |

### 4.3 등록 개체 (Mode=0)

- 위키데이터 Q아이디, 워드넷 Synset 등 외부 ID와 매핑된 개체
- Q아이디 자체는 Triple로 연결: `(Entity_SIDX, P-외부ID, "Q12345")`
- **수(Number) 개념과 무관**: 삼성전자는 "하나"지만 단수라 하기 애매, BTS는 그룹이지만 하나의 개체

### 4.4 대명사/추상 (Mode=1~7)

- EntityType + Attributes로 의미 범위 지정
- 비트가 채워질수록 구체적
- 예: Human(Type) + Male(Attr) + Korea(Attr) = "한국 남자"

---

## 5. EntityType (bit 11-16)

### 5.1 설계 원칙

- **6비트 = 64개** 상위 타입
- 위키데이터 P31(instance of) 빈도 통계 기반
- 위키미디어 메타 타입 제외 (category, disambiguation 등)
- 세부 분류는 Attributes 내 소분류 비트로
- 9개 카테고리로 그룹화

### 5.2 코드 테이블

**생물/인물 (0x00-0x07)**

| 코드 | 타입 | 대표 Q-ID | 개체수 |
|------|------|-----------|--------|
| 0x00 | Human | Q5 | 12.5M |
| 0x01 | Taxon | Q16521 | 3.8M |
| 0x02 | Gene | Q7187 | 1.2M |
| 0x03 | Protein | Q8054 | 1.0M |
| 0x04 | CellLine | Q21014462 | 154K |
| 0x05 | FamilyName | Q101352 | 662K |
| 0x06 | GivenName | Q202444 | 128K |
| 0x07 | FictionalCharacter | Q15632617 | 98K |

**화학/물질 (0x08-0x0B)**

| 코드 | 타입 | 대표 Q-ID | 개체수 |
|------|------|-----------|--------|
| 0x08 | Chemical | Q113145171 | 1.3M |
| 0x09 | Compound | Q11173 | 1.1M |
| 0x0A | Mineral | Q7946 | 62K |
| 0x0B | Drug | Q12140 | 45K |

**천체 (0x0C-0x13)**

| 코드 | 타입 | 대표 Q-ID | 개체수 |
|------|------|-----------|--------|
| 0x0C | Star | Q523 | 3.6M |
| 0x0D | Galaxy | Q318 | 2.1M |
| 0x0E | Asteroid | Q3863 | 249K |
| 0x0F | Quasar | Q83373 | 178K |
| 0x10 | Planet | Q634 | 15K |
| 0x11 | Nebula | Q12057 | 8K |
| 0x12 | StarCluster | Q168845 | 5K |
| 0x13 | Moon | Q2537 | 3K |

**지형/자연 (0x14-0x1B)**

| 코드 | 타입 | 대표 Q-ID | 개체수 |
|------|------|-----------|--------|
| 0x14 | Mountain | Q8502 | 518K |
| 0x15 | Hill | Q54050 | 321K |
| 0x16 | River | Q4022 | 427K |
| 0x17 | Lake | Q23397 | 292K |
| 0x18 | Stream | Q47521 | 194K |
| 0x19 | Island | Q23442 | 153K |
| 0x1A | Bay | Q39594 | 25K |
| 0x1B | Cave | Q35509 | 20K |

**장소/행정 (0x1C-0x23)**

| 코드 | 타입 | 대표 Q-ID | 개체수 |
|------|------|-----------|--------|
| 0x1C | Settlement | Q486972 | 580K |
| 0x1D | Village | Q532 | 245K |
| 0x1E | Hamlet | Q5084 | 148K |
| 0x1F | Street | Q79007 | 711K |
| 0x20 | Cemetery | Q39614 | 298K |
| 0x21 | AdminRegion | Q15284 | 100K |
| 0x22 | Park | Q22698 | 45K |
| 0x23 | ProtectedArea | Q473972 | 35K |

**건축물 (0x24-0x2B)**

| 코드 | 타입 | 대표 Q-ID | 개체수 |
|------|------|-----------|--------|
| 0x24 | Building | Q41176 | 292K |
| 0x25 | Church | Q16970 | 286K |
| 0x26 | School | Q9842 | 242K |
| 0x27 | House | Q3947 | 235K |
| 0x28 | Structure | Q811979 | 216K |
| 0x29 | SportsVenue | Q1076486 | 145K |
| 0x2A | Castle | Q23413 | 42K |
| 0x2B | Bridge | Q12280 | 38K |

**조직 (0x2C-0x2F)**

| 코드 | 타입 | 대표 Q-ID | 개체수 |
|------|------|-----------|--------|
| 0x2C | Organization | Q43229 | 531K |
| 0x2D | Business | Q4830453 | 242K |
| 0x2E | PoliticalParty | Q7278 | 35K |
| 0x2F | SportsTeam | Q847017 | 95K |

**창작물 (0x30-0x3B)**

| 코드 | 타입 | 대표 Q-ID | 개체수 |
|------|------|-----------|--------|
| 0x30 | Painting | Q3305213 | 1.1M |
| 0x31 | Document | Q49848 | 45.0M |
| 0x32 | LiteraryWork | Q7725634 | 395K |
| 0x33 | Film | Q11424 | 336K |
| 0x34 | Album | Q482994 | 303K |
| 0x35 | MusicalWork | Q105543609 | 195K |
| 0x36 | TVEpisode | Q21191270 | 177K |
| 0x37 | VideoGame | Q7889 | 172K |
| 0x38 | TVSeries | Q5398426 | 85K |
| 0x39 | Patent | Q43305660 | 289K |
| 0x3A | Software | Q7397 | 13K |
| 0x3B | Website | Q35127 | 12K |

**이벤트/예약 (0x3C-0x3F)**

| 코드 | 타입 | 대표 Q-ID | 개체수 |
|------|------|-----------|--------|
| 0x3C | SportsSeason | Q27020041 | 183K |
| 0x3D | Event | Q1656682 | 10K |
| 0x3E | Election | Q40231 | 11K |
| 0x3F | Other | - | 예약 |

---

## 6. Attributes (bit 17-64)

### 6.1 설계 원칙

- **48비트 = 타입별 가변 스키마**
- EntityType마다 다른 의미로 해석
- 고빈도 속성에 더 많은 비트 할당
- SIMD 필터링에 직접 활용
- 상위 필드 값이 하위 필드 코드북을 결정 (계층적 해석)

### 6.2 Human (0x00) Attributes — 48비트

```
┌──────────┬────────┬────────┬──────┬────────┬────────┬─────────┬────────┬──────────┬──────────┐
│ 소분류   │ 직업   │ 국적   │ 시대 │ 연대   │ 성별   │ 저명도  │ 언어   │ 출생지역 │ 활동분야 │
│  5bit    │  6bit  │  8bit  │ 4bit │  4bit  │  2bit  │  3bit   │  6bit  │   6bit   │   4bit   │
└──────────┴────────┴────────┴──────┴────────┴────────┴─────────┴────────┴──────────┴──────────┘
= 48비트
```

**소분류 (5비트 = 32개):**

| 코드 | 소분류 |
|------|--------|
| 0x00 | 일반 |
| 0x01 | Politician |
| 0x02 | Scientist |
| 0x03 | Artist |
| 0x04 | Athlete |
| 0x05 | Business Person |
| 0x06 | Military |
| 0x07 | Religious Figure |
| 0x08 | Royalty |
| 0x09 | Criminal |
| 0x0A | Fictional Human |
| ... | ... |

**시대 (4비트 = 16개):**

| 코드 | 시대 |
|------|------|
| 0x0 | Unknown |
| 0x1 | Prehistoric |
| 0x2 | Ancient (~500) |
| 0x3 | Classical (500~1000) |
| 0x4 | Medieval (1000~1500) |
| 0x5 | Early Modern (1500~1800) |
| 0x6 | Modern (1800~1950) |
| 0x7 | Contemporary (1950~2000) |
| 0x8 | Current (2000~) |
| 0x9-F | Reserved |

**성별 (2비트):**

| 코드 | 성별 |
|------|------|
| 00 | Unknown |
| 01 | Male |
| 10 | Female |
| 11 | Other |

**저명도 (3비트 = 8개):**
- 위키데이터 sitelinks 수 기반
- 0: Unknown, 1: 1-10, 2: 11-50, 3: 51-100, 4: 101-200, 5: 201-500, 6: 501-1000, 7: 1000+

### 6.3 Star (0x0C) Attributes — 48비트

```
┌──────────┬────────────┬──────────┬──────────┬──────────┬──────────┬────────────┬──────────┬──────────┬──────────┬────────┐
│ 별자리   │ 분광형     │ 광도등급 │ 겉보기등급│ 적경구간 │ 적위구간 │ 특성플래그 │ 시선속도 │ 적색편이 │ 시차     │ 예비   │
│   7bit   │    4bit    │   3bit   │   4bit   │   4bit   │   4bit   │    6bit    │   5bit   │   5bit   │   4bit   │  2bit  │
└──────────┴────────────┴──────────┴──────────┴──────────┴──────────┴────────────┴──────────┴──────────┴──────────┴────────┘
= 48비트
```

**분광형 (4비트):** O, B, A, F, G, K, M 등
**광도등급 (3비트):** I~VII
**특성플래그 (6비트):** 변광성, 쌍성, 펄서 등

### 6.4 기타 타입

각 EntityType별 48비트 Attributes 스키마는 `entity/references/type_schemas.json`에 정의.
상세 설계는 `docs/history/위키데이터-엔티티-코드북-history.md` Phase 5 참조.

---

## 7. 연산

### 7.1 Entity 생성

```python
def make_entity(
    mode: int,           # 3비트
    entity_type: int,    # 6비트
    attrs: int           # 48비트
) -> bytes:
    PREFIX = 0b0001001   # 7비트

    word1 = (PREFIX << 9) | (mode << 6) | entity_type
    word2 = (attrs >> 32) & 0xFFFF
    word3 = (attrs >> 16) & 0xFFFF
    word4 = attrs & 0xFFFF

    return (
        word1.to_bytes(2, 'big') +
        word2.to_bytes(2, 'big') +
        word3.to_bytes(2, 'big') +
        word4.to_bytes(2, 'big')
    )
```

### 7.2 Entity 파싱

```python
def parse_entity(data: bytes) -> dict:
    word1 = int.from_bytes(data[0:2], 'big')
    word2 = int.from_bytes(data[2:4], 'big')
    word3 = int.from_bytes(data[4:6], 'big')
    word4 = int.from_bytes(data[6:8], 'big')

    prefix = (word1 >> 9) & 0x7F
    mode = (word1 >> 6) & 0x7
    entity_type = word1 & 0x3F
    attrs = (word2 << 32) | (word3 << 16) | word4

    return {
        'prefix': prefix,
        'mode': mode,
        'entity_type': entity_type,
        'attrs': attrs
    }
```

### 7.3 Mode 판별

```python
def is_registered_entity(data: bytes) -> bool:
    """Mode=0이면 등록된 개체 (Q아이디 등)"""
    word1 = int.from_bytes(data[0:2], 'big')
    mode = (word1 >> 6) & 0x7
    return mode == 0

def is_abstract_entity(data: bytes) -> bool:
    """Mode≠0이면 추상/대명사"""
    return not is_registered_entity(data)
```

---

## 8. 사용 예시

### 8.1 등록 개체: 이순신

```python
# 이순신 (Q211789)
# Q아이디 연결은 별도 Triple로
yi_sun_sin = make_entity(
    mode=0,              # 등록 개체
    entity_type=0x00,    # Human
    attrs=(
        (0x06 << 43) |   # 소분류: Military
        (0x01 << 37) |   # 직업: Admiral
        (0x52 << 29) |   # 국적: Korea
        (0x5 << 25) |    # 시대: Early Modern
        (0x0 << 21) |    # 연대
        (0x01 << 19) |   # 성별: Male
        (0x7 << 16) |    # 저명도: 1000+
        (0x0)            # 언어/출생지역/활동분야
    )
)
# 4워드 = 64비트
```

### 8.2 등록 개체: 삼성전자

```python
# 삼성전자 (Q20718)
samsung = make_entity(
    mode=0,              # 등록 개체
    entity_type=0x2D,    # Business
    attrs=0x...          # Business용 Attributes
)
# Q아이디 연결:
# Triple(samsung_SIDX, P-외부ID, "Q20718")
```

### 8.3 추상: "모든 한국 남자"

```python
all_korean_men = make_entity(
    mode=4,              # 전칭 (모든)
    entity_type=0x00,    # Human
    attrs=(
        (0x00 << 43) |   # 소분류: 일반
        (0x00 << 37) |   # 직업: 일반
        (0x52 << 29) |   # 국적: Korea
        (0x0 << 25) |    # 시대: Unknown
        (0x0 << 21) |    # 연대: Unknown
        (0x01 << 19) |   # 성별: Male
        (0x0 << 16)      # 저명도: Unknown
    )
)
```

### 8.4 대명사: "그 사람"

```python
that_person = make_entity(
    mode=1,              # 특정 단수
    entity_type=0x00,    # Human
    attrs=0              # 속성 미지정
)
```

### 8.5 존재: "어떤 과학자"

```python
some_scientist = make_entity(
    mode=5,              # 존재 (어떤)
    entity_type=0x00,    # Human
    attrs=(
        (0x02 << 43)     # 소분류: Scientist
    )
)
```

---

## 9. TID 연계

### 9.1 TID란?

- TID (Temporary ID): 16비트 스트림 내 임시 식별자
- 대명사 역할: 한 번 선언 후 짧게 참조
- 스트림 종료 시 해제

### 9.2 Entity Node와 TID

Entity Node 자체에는 TID를 포함하지 않음.
TID 할당은 별도 메커니즘으로:

**옵션 A: Meta Node로 선언**
```
[Meta: TID_ASSIGN] [Entity Node 4워드] [TID 1워드]
```

**옵션 B: 스트림 컨텍스트에서 암묵적 할당**
- Entity Node 등장 순서대로 TID 자동 할당

> **TODO:** TID 연계 방식 확정 필요

---

## 10. Q아이디 연결

### 10.1 Triple로 연결

```
Subject:  Entity_SIDX (64비트)
Property: P-외부ID (예: P-Wikidata)
Object:   "Q12345" (문자열 또는 정수)
```

### 10.2 내부 매핑 테이블

```
| SIDX (64bit) | Source | External_ID |
|--------------|--------|-------------|
| 0x...        | Q-ID   | 211789      |
| 0x...        | Q-ID   | 20718       |
| 0x...        | Synset | 12345678    |
```

### 10.3 역방향 조회

Q아이디 → SIDX 조회:
- 인덱스로 O(1) 조회 가능
- 하나의 Q아이디가 여러 SIDX에 매핑될 수 있음 (역할/시점별)

---

## 부록 A: 비트 요약

```
1st WORD (bit 1-16):
  bit 1-7:   Prefix (0001001)
  bit 8-10:  Mode (0-7)
  bit 11-16: EntityType (0-63)

2nd WORD (bit 17-32):
  bit 17-32: Attributes 상위 16비트

3rd WORD (bit 33-48):
  bit 33-48: Attributes 중위 16비트

4th WORD (bit 49-64):
  bit 49-64: Attributes 하위 16비트
```

---

## 부록 B: 필드 오프셋

### 1st WORD

| 필드 | 마스크 | 시프트 |
|------|--------|--------|
| Prefix | 0xFE00 | >> 9 |
| Mode | 0x01C0 | >> 6 |
| EntityType | 0x003F | - |

### 2nd-4th WORD

| 필드 | 워드 | 마스크 | 시프트 |
|------|------|--------|--------|
| Attrs High | 2nd | 0xFFFF | - |
| Attrs Mid | 3rd | 0xFFFF | - |
| Attrs Low | 4th | 0xFFFF | - |

---

## 부록 C: v0.3 → v0.4 마이그레이션

| v0.3 필드 | v0.4 대응 |
|-----------|-----------|
| 3워드 (48비트) | 4워드 (64비트) |
| Attributes (32비트) | Attributes (**48비트**) |
| EntityType 코드 테이블 (임시) | EntityType 코드 테이블 (**Phase 4 확정**) |
| 의미정렬 총량 41비트 | 의미정렬 총량 **57비트** |

---

## 버전 히스토리

| 버전 | 날짜 | 변경 |
|------|------|------|
| v0.1 | 2026-01-29 | 초안 작성 |
| v0.2 | 2026-01-29 | Prefix 섹션 간소화, SIDX.md 참조로 변경 |
| v0.3 | 2026-01-30 | Lane/UID 제거, Mode 3비트 통합, Attributes 32비트 확장, 순수 의미정렬 구조 |
| v0.4 | 2026-02-01 | **4워드 64비트 확정**: Attributes 48비트 확장, EntityType 코드 테이블 Phase 4 확정 (64개 9카테고리), 타입별 완전 독립 스키마 |

---

## TODO

- [ ] 64개 타입별 Attributes 48비트 스키마 상세 검증
- [ ] TID 연계 방식 확정
- [ ] SIMD 필터링 최적화 검증
- [ ] 분류율 62% → 90%+ 개선 (P279 체인 탐색)

---

**문서 종료**
