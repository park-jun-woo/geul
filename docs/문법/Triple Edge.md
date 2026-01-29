# Triple Edge 명세서

**버전:** v0.1  
**작성일:** 2026-01-29  
**목적:** GEUL 속성/관계 표현을 위한 Triple Edge 패킷 구조 정의

---

## 1. 개요

Triple Edge는 `(Subject, Property, Object)` 형태의 **관계/속성**을 표현하는 Edge 타입이다.

**이중 모드 설계:**
- **기본 모드 (4워드):** Top 63 고빈도 속성용
- **확장 모드 (5워드):** 전체 P-ID 커버 (의미정렬 16비트)

**핵심 원칙:**
- Edge TID는 **헤더 다음** (파싱 효율)
- PropCode 63 = 확장 모드 표시자
- 고빈도 속성은 양쪽 표기 가능 (4워드 단축 OR 5워드 정식)

---

## 2. Prefix

| 항목 | 값 |
|------|-----|
| Prefix | `1100000 001` |
| 비트 수 | 10 |
| 1st 워드 나머지 | 6비트 (PropCode) |

---

## 3. 기본 모드 (4워드 = 64비트)

### 3.1 구조

```
1st WORD (16비트)
┌────────────────────┬────────────────────┐
│      Prefix        │     PropCode       │
│      10bit         │       6bit         │
└────────────────────┴────────────────────┘

2nd WORD (16비트)
┌────────────────────────────────────────────┐
│                Edge TID                    │
│                  16bit                     │
└────────────────────────────────────────────┘

3rd WORD (16비트)
┌────────────────────────────────────────────┐
│               Subject TID                  │
│                  16bit                     │
└────────────────────────────────────────────┘

4th WORD (16비트)
┌────────────────────────────────────────────┐
│               Object TID                   │
│                  16bit                     │
└────────────────────────────────────────────┘
```

### 3.2 필드 설명

| 필드 | 비트 | 설명 |
|------|------|------|
| Prefix | 10 | `1100000 001` |
| PropCode | 6 | 0~62: Top 63 속성, 63: 확장 모드 |
| Edge TID | 16 | 이 Edge의 TID |
| Subject TID | 16 | 주어 Entity/Node TID |
| Object TID | 16 | 목적어 Entity/Node/Quantity TID |

### 3.3 PropCode (6비트 = 0~63)

- **0~62:** Top 63 고빈도 속성 (아래 테이블 참조)
- **63:** 확장 모드 표시자 → 5워드 구조

---

## 4. 확장 모드 (5워드 = 80비트)

### 4.1 구조

```
1st WORD (16비트)
┌────────────────────┬────────────────────┐
│      Prefix        │  PropCode = 63     │
│      10bit         │   6bit (111111)    │
└────────────────────┴────────────────────┘

2nd WORD (16비트)
┌────────────────────────────────────────────┐
│                Edge TID                    │
│                  16bit                     │
└────────────────────────────────────────────┘

3rd WORD (16비트)
┌────────────────────────────────────────────┐
│           P-ID (의미정렬)                  │
│                  16bit                     │
└────────────────────────────────────────────┘

4th WORD (16비트)
┌────────────────────────────────────────────┐
│               Subject TID                  │
│                  16bit                     │
└────────────────────────────────────────────┘

5th WORD (16비트)
┌────────────────────────────────────────────┐
│               Object TID                   │
│                  16bit                     │
└────────────────────────────────────────────┘
```

### 4.2 필드 설명

| 필드 | 비트 | 설명 |
|------|------|------|
| Prefix | 10 | `1100000 001` |
| PropCode | 6 | `111111` (63 = 확장 표시) |
| Edge TID | 16 | 이 Edge의 TID |
| P-ID | 16 | 의미정렬 Property ID |
| Subject TID | 16 | 주어 Entity/Node TID |
| Object TID | 16 | 목적어 Entity/Node/Quantity TID |

---

## 5. Top 63 속성 (PropCode 0~62)

위키데이터 사용 빈도 기반 선정. 의미그룹별 정렬.

### 5.1 분류/타입 (0x00~0x07)

| Code | P-ID | 속성명 | 설명 |
|------|------|--------|------|
| 0 | P31 | instance of | ~의 인스턴스 |
| 1 | P279 | subclass of | ~의 하위 클래스 |
| 2 | P361 | part of | ~의 부분 |
| 3 | P527 | has part | ~을 포함 |
| 4 | P1552 | has quality | 속성/특성 |
| 5 | P460 | same as | 동일 |
| 6 | P1889 | different from | 다름 |
| 7 | P156 | followed by | 후속 |

### 5.2 공간/위치 (0x08~0x0F)

| Code | P-ID | 속성명 | 설명 |
|------|------|--------|------|
| 8 | P17 | country | 국가 |
| 9 | P131 | located in | 위치 (행정구역) |
| 10 | P276 | location | 위치 (장소) |
| 11 | P625 | coordinate | 좌표 |
| 12 | P30 | continent | 대륙 |
| 13 | P36 | capital | 수도 |
| 14 | P150 | contains | 포함 (지역) |
| 15 | P206 | located next to | 인접 수역 |

### 5.3 시간 (0x10~0x17)

| Code | P-ID | 속성명 | 설명 |
|------|------|--------|------|
| 16 | P569 | date of birth | 생년월일 |
| 17 | P570 | date of death | 사망일 |
| 18 | P571 | inception | 설립일 |
| 19 | P576 | dissolved | 해산일 |
| 20 | P577 | publication date | 발표일 |
| 21 | P580 | start time | 시작 시점 |
| 22 | P582 | end time | 종료 시점 |
| 23 | P585 | point in time | 시점 |

### 5.4 인물 기본 (0x18~0x1F)

| Code | P-ID | 속성명 | 설명 |
|------|------|--------|------|
| 24 | P19 | place of birth | 출생지 |
| 25 | P20 | place of death | 사망지 |
| 26 | P21 | sex or gender | 성별 |
| 27 | P27 | citizenship | 국적 |
| 28 | P735 | given name | 이름 |
| 29 | P734 | family name | 성 |
| 30 | P1559 | name in native language | 본명 |
| 31 | P742 | pseudonym | 필명/예명 |

### 5.5 관계/소속 (0x20~0x27)

| Code | P-ID | 속성명 | 설명 |
|------|------|--------|------|
| 32 | P22 | father | 아버지 |
| 33 | P25 | mother | 어머니 |
| 34 | P26 | spouse | 배우자 |
| 35 | P40 | child | 자녀 |
| 36 | P3373 | sibling | 형제자매 |
| 37 | P463 | member of | 소속 |
| 38 | P108 | employer | 고용주 |
| 39 | P1027 | conferred by | 수여 기관 |

### 5.6 직업/활동 (0x28~0x2F)

| Code | P-ID | 속성명 | 설명 |
|------|------|--------|------|
| 40 | P106 | occupation | 직업 |
| 41 | P39 | position held | 직위 |
| 42 | P69 | educated at | 학력 |
| 43 | P101 | field of work | 분야 |
| 44 | P1344 | participant in | 참가 (이벤트) |
| 45 | P166 | award received | 수상 |
| 46 | P800 | notable work | 대표작 |
| 47 | P1412 | languages spoken | 사용 언어 |

### 5.7 미디어/식별 (0x30~0x37)

| Code | P-ID | 속성명 | 설명 |
|------|------|--------|------|
| 48 | P18 | image | 이미지 |
| 49 | P154 | logo | 로고 |
| 50 | P41 | flag image | 국기/기 |
| 51 | P373 | Commons category | 위키미디어 |
| 52 | P856 | official website | 공식 웹사이트 |
| 53 | P214 | VIAF ID | VIAF |
| 54 | P227 | GND ID | GND |
| 55 | P213 | ISNI | ISNI |

### 5.8 작품/창작 (0x38~0x3D)

| Code | P-ID | 속성명 | 설명 |
|------|------|--------|------|
| 56 | P50 | author | 저자 |
| 57 | P57 | director | 감독 |
| 58 | P86 | composer | 작곡가 |
| 59 | P175 | performer | 연주자/가수 |
| 60 | P136 | genre | 장르 |
| 61 | P364 | original language | 원어 |
| 62 | P123 | publisher | 출판사 |

### 5.9 확장 표시자 (0x3F)

| Code | 의미 |
|------|------|
| 63 | **확장 모드** → 5워드 구조 사용 |

---

## 6. P-ID 의미정렬 (16비트)

확장 모드에서 사용하는 P-ID 구조.

### 6.1 구조

```
┌────────────────────┬────────────────────────────┐
│   의미그룹 (SG)    │      P-ID 하위 12비트       │
│       4bit         │           12bit            │
└────────────────────┴────────────────────────────┘
```

### 6.2 의미그룹 (Semantic Group, 4비트)

| SG | 의미 | 예시 P-ID |
|----|------|-----------|
| 0 | 분류/타입 | P31, P279, P361, P527 |
| 1 | 공간/위치 | P17, P131, P625, P276 |
| 2 | 시간 | P569, P570, P577, P580 |
| 3 | 인물 기본 | P19, P20, P21, P27 |
| 4 | 관계/소속 | P22, P25, P26, P40, P463 |
| 5 | 직업/활동 | P106, P108, P39, P69 |
| 6 | 미디어 | P18, P154, P41, P373 |
| 7 | 식별자 | P213, P214, P227, P856 |
| 8 | 작품 | P50, P57, P86, P175 |
| 9 | 과학/분류 | P703, P171, P225 |
| 10 | 수량/측정 | P2048, P2046, P2067 |
| 11 | 사회/법률 | P1001, P797, P3461 |
| 12 | 예약 | - |
| 13 | 예약 | - |
| 14 | 예약 | - |
| 15 | 사용자 정의 | 커스텀 속성 |

### 6.3 인코딩 규칙

1. **Top 63 속성:** 원본 P-ID 하위 12비트 + 의미그룹
2. **기타 속성:** 의미그룹 내 순번 (빈도순)

**예시:**
```
P31 (instance of):
  → SG=0 (분류), 하위=0x01F
  → 16비트: 0000 0000 0001 1111 = 0x001F

P17 (country):
  → SG=1 (공간), 하위=0x011
  → 16비트: 0001 0000 0001 0001 = 0x1011

P2048 (height):
  → SG=10 (수량), 하위=0x800
  → 16비트: 1010 1000 0000 0000 = 0xA800
```

### 6.4 장점

- **의미 클러스터링:** 유사 속성이 인접 코드
- **SIMD 필터링:** 상위 4비트로 그룹 필터
- **우아한 열화:** 하위 비트 손실 시 그룹만 유지

---

## 7. 모드 비교

| | 기본 모드 | 확장 모드 |
|--|-----------|-----------|
| **워드** | 4 | 5 |
| **비트** | 64 | 80 |
| **PropCode** | 0~62 | 63 (표시자) |
| **속성 범위** | Top 63 | 전체 (~65,536) |
| **용도** | 고빈도 속성 | 전체 P-ID |

**선택 가이드:**
- Top 63 속성 → 기본 모드 (효율)
- 그 외 속성 → 확장 모드 (범용)
- Top 63 속성도 확장 모드 사용 가능 (호환성)

---

## 8. 패킷 파싱

### 8.1 모드 판별

```python
def parse_triple_edge(data: bytes) -> dict:
    word1 = int.from_bytes(data[0:2], 'big')
    
    # Prefix 확인 (상위 10비트)
    prefix = word1 >> 6
    assert prefix == 0b1100000001, "Not Triple Edge"
    
    # PropCode (하위 6비트)
    prop_code = word1 & 0x3F
    
    if prop_code < 63:
        # 기본 모드 (4워드)
        return parse_basic_mode(data, prop_code)
    else:
        # 확장 모드 (5워드)
        return parse_extended_mode(data)
```

### 8.2 기본 모드 파싱

```python
def parse_basic_mode(data: bytes, prop_code: int) -> dict:
    edge_tid = int.from_bytes(data[2:4], 'big')
    subject_tid = int.from_bytes(data[4:6], 'big')
    object_tid = int.from_bytes(data[6:8], 'big')
    
    return {
        'mode': 'basic',
        'prop_code': prop_code,
        'property': TOP_63_MAP[prop_code],  # P-ID 조회
        'edge_tid': edge_tid,
        'subject_tid': subject_tid,
        'object_tid': object_tid,
        'words': 4
    }
```

### 8.3 확장 모드 파싱

```python
def parse_extended_mode(data: bytes) -> dict:
    edge_tid = int.from_bytes(data[2:4], 'big')
    p_id_raw = int.from_bytes(data[4:6], 'big')
    subject_tid = int.from_bytes(data[6:8], 'big')
    object_tid = int.from_bytes(data[8:10], 'big')
    
    # 의미정렬 P-ID 디코딩
    semantic_group = (p_id_raw >> 12) & 0xF
    p_id_lower = p_id_raw & 0xFFF
    
    return {
        'mode': 'extended',
        'semantic_group': semantic_group,
        'p_id': decode_p_id(semantic_group, p_id_lower),
        'edge_tid': edge_tid,
        'subject_tid': subject_tid,
        'object_tid': object_tid,
        'words': 5
    }
```

---

## 9. 예시

### 9.1 기본 모드: "철수의 아버지는 영수이다"

```
P22 (father) → PropCode = 32 (0x20)

Triple Edge (기본):
  1st: [1100000 001] + [100000]   - Prefix + PropCode 32
  2nd: [TID: 0x0100]              - Edge TID
  3rd: [TID: 0x0001]              - 철수 (Subject)
  4th: [TID: 0x0002]              - 영수 (Object)

총: 4워드
```

### 9.2 기본 모드: "Apple은 회사이다"

```
P31 (instance of) → PropCode = 0

Triple Edge (기본):
  1st: [1100000 001] + [000000]   - Prefix + PropCode 0
  2nd: [TID: 0x0101]              - Edge TID
  3rd: [TID: 0x0010]              - Apple (Subject)
  4th: [TID: 0x0020]              - 회사 (Object)

총: 4워드
```

### 9.3 확장 모드: "에펠탑의 높이는 330m"

```
P2048 (height) → Top 63 외 → 확장 모드
P2048 의미정렬: SG=10 (수량), 하위=0x800 → 0xA800

Triple Edge (확장):
  1st: [1100000 001] + [111111]   - Prefix + Ext(63)
  2nd: [TID: 0x0102]              - Edge TID
  3rd: [0xA800]                    - P2048 의미정렬
  4th: [TID: 0x0030]              - 에펠탑 (Subject)
  5th: [TID: 0x0050]              - 330m Quantity (Object)

총: 5워드
```

### 9.4 확장 모드: "서울의 인구"

```
P1082 (population) → 확장 모드
P1082 의미정렬: SG=10 (수량), 하위=... → 계산

Triple Edge (확장):
  1st: [1100000 001] + [111111]
  2nd: [TID: 0x0103]
  3rd: [P1082 의미정렬]
  4th: [TID: 0x0040]              - 서울
  5th: [TID: 0x0060]              - 9,700,000 Quantity

총: 5워드
```

---

## 10. 설계 근거

### 10.1 이중 모드 이유

**문제:**
- 위키데이터 속성 ~13,000개
- 전부 16비트면 낭비 (상위 속성만 사용 빈번)

**해결:**
- 상위 63개로 **사용량 80% 이상** 커버 (추정)
- 기본 모드: 4워드 (효율)
- 확장 모드: 5워드 (범용)

### 10.2 PropCode 63 표시자 이유

- 6비트 공간에서 63(0x3F)은 **자연스러운 확장 표시**
- 파싱 시 단일 비교로 모드 판별
- 0~62 범위는 깔끔한 연속 인덱스

### 10.3 Edge TID 위치 이유

**헤더 다음 배치:**
- 타입 판별 후 즉시 TID 확보
- 참조 해결 빠름
- 다른 Edge 타입과 일관성

### 10.4 의미정렬 P-ID 이유

- **클러스터링:** 유사 속성 인접
- **필터링:** 상위 4비트로 그룹 선별
- **확장성:** 65,536개 속성 커버

---

## 11. 버전 히스토리

| 버전 | 날짜 | 변경 |
|------|------|------|
| v0.1 | 2026-01-29 | 초안: 이중 모드 구조 정의 |

---

## 12. TODO

- [ ] Top 63 속성 빈도 검증 (위키데이터 쿼리)
- [ ] 의미그룹별 P-ID 재배치 테이블 작성
- [ ] Modifier Flags 추가 여부 검토
- [ ] Context Edge 연결 예시 추가

---

**문서 종료**
