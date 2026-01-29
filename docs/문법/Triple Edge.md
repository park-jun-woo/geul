# Triple Edge 명세서

**버전:** v0.4  
**작성일:** 2026-01-29  
**목적:** GEUL 속성/관계 표현을 위한 Triple Edge 패킷 구조 정의

---

## 1. 개요

Triple Edge는 `(Subject, Property, Object)` 형태의 **관계/속성**을 표현하는 Edge 타입이다.

**이중 모드 설계:**
- **기본 모드 (4워드):** PropCode 0~62 (Top 63 속성)
- **확장 모드 (5워드):** 전체 P-ID 커버 (의미정렬 16비트)

**핵심 원칙:**
- PropCode 0~62 = Top 63 고빈도 속성
- PropCode 63 = 확장 모드 표시자
- Edge TID는 **헤더 다음** (파싱 효율)

---

## 2. Prefix

`SIDX.md` 참조

| 항목 | 값 |
|------|-----|
| Standard | `0 000 001` (7비트) |
| Proposal | `1100 000 001` (10비트) |
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

2nd WORD: Edge TID (16비트)
3rd WORD: Subject TID (16비트)
4th WORD: Object TID (16비트)
```

### 3.2 필드 설명

| 필드 | 비트 | 설명 |
|------|------|------|
| Prefix | 10 | `1100 000 001` |
| PropCode | 6 | 0~62: Top 63 속성, 63: 확장 모드 |
| Edge TID | 16 | 이 Edge의 TID |
| Subject TID | 16 | 주어 Entity/Node TID |
| Object TID | 16 | 목적어 Entity/Node/Quantity TID |

---

## 4. 확장 모드 (5워드 = 80비트)

### 4.1 구조

```
1st WORD: [Prefix 10bit] + [PropCode=63 6bit]
2nd WORD: Edge TID (16비트)
3rd WORD: P-ID 의미정렬 (16비트)
4th WORD: Subject TID (16비트)
5th WORD: Object TID (16비트)
```

### 4.2 필드 설명

| 필드 | 비트 | 설명 |
|------|------|------|
| Prefix | 10 | `1100 000 001` |
| PropCode | 6 | `111111` (63 = 확장 표시) |
| Edge TID | 16 | 이 Edge의 TID |
| P-ID | 16 | 의미정렬 Property ID |
| Subject TID | 16 | 주어 Entity/Node TID |
| Object TID | 16 | 목적어 Entity/Node/Quantity TID |

---

## 5. Top 63 속성 (PropCode 0~62)

위키데이터 사용 빈도 기반 선정. 의미그룹별 정렬.

### 5.1 분류/타입 (Code 0~7)

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

### 5.2 공간/위치 (Code 8~15)

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

### 5.3 시간 (Code 16~23)

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

### 5.4 인물 기본 (Code 24~31)

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

### 5.5 관계/소속 (Code 32~39)

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

### 5.6 직업/활동 (Code 40~47)

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

### 5.7 미디어/식별 (Code 48~55)

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

### 5.8 작품/창작 (Code 56~62)

| Code | P-ID | 속성명 | 설명 |
|------|------|--------|------|
| 56 | P50 | author | 저자 |
| 57 | P57 | director | 감독 |
| 58 | P86 | composer | 작곡가 |
| 59 | P175 | performer | 연주자/가수 |
| 60 | P136 | genre | 장르 |
| 61 | P364 | original language | 원어 |
| 62 | P123 | publisher | 출판사 |

### 5.9 확장 표시자 (Code 63)

| Code | 의미 |
|------|------|
| 63 | **확장 모드** → 5워드 구조 사용 |

---

## 6. PropCode 요약

```
┌─────────────────────────────────────────────┐
│  0~7:   분류/타입 (P31, P279, ...)          │
│  8~15:  공간/위치 (P17, P131, ...)          │
│  16~23: 시간 (P569, P570, ...)              │
│  24~31: 인물 기본 (P19, P20, ...)           │
│  32~39: 관계/소속 (P22, P25, ...)           │
│  40~47: 직업/활동 (P106, P39, ...)          │
│  48~55: 미디어/식별 (P18, P856, ...)        │
│  56~62: 작품/창작 (P50, P57, ...)           │
├─────────────────────────────────────────────┤
│  63: 확장 모드 표시자                        │
└─────────────────────────────────────────────┘
```

---

## 7. P-ID 의미정렬 (16비트)

확장 모드에서 사용하는 P-ID 구조.

### 7.1 구조

```
┌────────────────────┬────────────────────────────┐
│   의미그룹 (SG)    │      P-ID 하위 12비트       │
│       4bit         │           12bit            │
└────────────────────┴────────────────────────────┘
```

### 7.2 의미그룹 (Semantic Group, 4비트)

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
| 12~14 | 예약 | - |
| 15 | 사용자 정의 | 커스텀 속성 |

---

## 8. 예시

### 8.1 기본 모드: "Apple은 회사이다"

```
P31 (instance of) → PropCode = 0

Triple Edge:
  1st: [1100 000 001] + [000000]  - Prefix + PropCode 0
  2nd: [TID: 0x0101]              - Edge TID
  3rd: [TID: 0x0010]              - Apple (Subject)
  4th: [TID: 0x0020]              - 회사 (Object)

총: 4워드
```

### 8.2 기본 모드: "철수의 아버지는 영수이다"

```
P22 (father) → PropCode = 32

Triple Edge:
  1st: [1100 000 001] + [100000]  - Prefix + PropCode 32
  2nd: [TID: 0x0100]              - Edge TID
  3rd: [TID: 0x0001]              - 철수 (Subject)
  4th: [TID: 0x0002]              - 영수 (Object)

총: 4워드
```

### 8.3 확장 모드: "에펠탑의 높이는 330m"

```
P2048 (height) → Top 63 외 → 확장 모드

Triple Edge:
  1st: [1100 000 001] + [111111]  - Prefix + Ext(63)
  2nd: [TID: 0x0102]              - Edge TID
  3rd: [0xA800]                   - P2048 의미정렬
  4th: [TID: 0x0030]              - 에펠탑 (Subject)
  5th: [TID: 0x0050]              - 330m Quantity (Object)

총: 5워드
```

---

## 9. 파싱

```python
def parse_triple_edge(data: bytes) -> dict:
    word1 = int.from_bytes(data[0:2], 'big')
    
    prefix = word1 >> 6
    assert prefix == 0b1100000001, "Not Triple Edge"
    
    prop_code = word1 & 0x3F
    
    if prop_code < 63:
        # 기본 모드 (4워드)
        return {
            'mode': 'basic',
            'prop_code': prop_code,
            'edge_tid': int.from_bytes(data[2:4], 'big'),
            'subject_tid': int.from_bytes(data[4:6], 'big'),
            'object_tid': int.from_bytes(data[6:8], 'big'),
            'words': 4
        }
    else:
        # 확장 모드 (5워드)
        return {
            'mode': 'extended',
            'p_id': int.from_bytes(data[4:6], 'big'),
            'edge_tid': int.from_bytes(data[2:4], 'big'),
            'subject_tid': int.from_bytes(data[6:8], 'big'),
            'object_tid': int.from_bytes(data[8:10], 'big'),
            'words': 5
        }
```

---

## 10. 버전 히스토리

| 버전 | 날짜 | 변경 |
|------|------|------|
| v0.1 | 2026-01-29 | 초안: 이중 모드 구조 정의 |
| v0.2 | 2026-01-29 | PropCode 0 = context 추가 |
| v0.3 | 2026-01-29 | context 제거, PropCode 0 = P31 복귀 |
| v0.4 | 2026-01-29 | Prefix 표기 수정, SIDX.md 참조로 변경 |

---

**문서 종료**