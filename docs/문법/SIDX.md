# GEUL SIDX 비트 명세서

**버전:** v0.7  
**작성일:** 2026-01-30  
**범위:** SIDX 64비트 최상위 구조  
**비트 규칙:** bit1 = MSB, bit64 = LSB  
**바이트 오더:** Big Endian (Network Byte Order)

---

## 1. 개요

SIDX(Semantic-aligned Index)는 64비트 전역 의미 식별자이다.

**최상위 4비트**(bit1~4)가 영역을 결정한다:

| Prefix | 영역 | 용도 |
|--------|------|------|
| `0xxx` | **Standard** | 공식 표준 (bit1=0) |
| `10xx` | **Issuer** | 등록기관 네임스페이스 |
| `1100` | **Proposal** | 표준 제안 (실험/후보) |
| `1101` | **Free** | 완전 자유 |
| `111x` | **Reserved** | 차세대 예약 |

---

## 2. 비트 분기 구조

### 2.1 1차 분기 (bit1)

```
bit1 = 0 : GEUL Standard (표준)
bit1 = 1 : GEUL Extension (확장)
```

### 2.2 Standard 내부 분기 (bit1=0)

**허프만 + 7비트 통일 혼합 체계:**

| Prefix | 비트 | 타입 | 빈도 |
|--------|------|------|------|
| `0 1` | 2 | Tiny Verb Edge | 최고빈도 |
| `0 01` | 3 | Verb Edge | 고빈도 |
| `0 001` | 4 | Entity Node | 고빈도 |
| `0 000 000` | 7 | **Meta Node** | 스트림 제어 |
| `0 000 001` | 7 | Triple Edge | 중빈도 |
| `0 000 010` | 7 | Clause Edge | 저빈도 |
| `0 000 011` | 7 | Event6 Edge | 저빈도 |
| `0 000 100` | 7 | Context Edge | 저빈도 |
| `0 000 101` | 7 | Quantity Node | 중빈도 |
| `0 000 110` | 7 | **Faber Edge** | 코드/AST |
| `0 000 111` | 7 | 확장 | - |

### 2.3 Extension 분기

```
bit1=1, bit2=0 : Issuer Namespace
bit1=1, bit2=1 : Free/Future
```

---

## 3. 전체 분기 트리

```
bit1
├─ 0: GEUL Standard ─────────────────────────────────────
│     │
│     └─ bit2~
│         ├─ 1           (0 1)         → Tiny Verb Edge
│         ├─ 01          (0 01)        → Verb Edge
│         ├─ 001         (0 001)       → Entity Node
│         └─ 000         (0 000)       → 7비트 통일 영역
│               │
│               └─ bit5~7 (3비트)
│                   ├─ 000 (0 000 000) → Meta Node
│                   ├─ 001 (0 000 001) → Triple Edge
│                   ├─ 010 (0 000 010) → Clause Edge
│                   ├─ 011 (0 000 011) → Event6 Edge
│                   ├─ 100 (0 000 100) → Context Edge
│                   ├─ 101 (0 000 101) → Quantity Node
│                   ├─ 110 (0 000 110) → Faber Edge
│                   └─ 111 (0 000 111) → 확장 영역
│                         │
│                         └─ bit8~10 (3비트)
│                             ├─ 000 (0 000 111 000) → Group Edge
│                             ├─ 001~110            → 예약
│                             └─ 111               → 2차 확장
│
└─ 1: GEUL Extension ────────────────────────────────────
      │
      └─ bit2
          ├─ 0: Issuer Namespace
          │     └─ bit3
          │         ├─ 0: 엄격 심사 (8,192개)
          │         └─ 1: 최소 심사 (5.3억개)
          │
          └─ 1: Free/Future
                └─ bit3
                    ├─ 0: Proposal (bit4=0) / Free (bit4=1)
                    └─ 1: Reserved
```

---

## 4. 영역별 상세

### 4.1 Standard (bit1=0)

**공식 GEUL 표준 영역.**

| Prefix | 비트 | 타입 | 설명 |
|--------|------|------|------|
| `0 1` | 2 | Tiny Verb Edge | 고빈도 단순 서술 |
| `0 01` | 3 | Verb Edge | 일반 서술 |
| `0 001` | 4 | Entity Node | 개체 |
| `0 000 000` | 7 | **Meta Node** | 스트림 제어/메타데이터 |
| `0 000 001` | 7 | Triple Edge | 속성/관계 |
| `0 000 010` | 7 | Clause Edge | 담화/논리 관계 |
| `0 000 011` | 7 | Event6 Edge | 6하원칙 사건 |
| `0 000 100` | 7 | Context Edge | 세계관/출처/맥락 |
| `0 000 101` | 7 | Quantity Node | 물리량/수치 |
| `0 000 110` | 7 | **Faber Edge** | 코드/AST 표현 |

### 4.2 Proposal (bit1~4 = 1100)

**표준 제안 레인.** Standard를 미러링.

| Standard | Proposal | 비트 | 타입 |
|----------|----------|------|------|
| `0 1` | `1100 1` | 5 | Tiny Verb Edge |
| `0 01` | `1100 01` | 6 | Verb Edge |
| `0 001` | `1100 001` | 7 | Entity Node |
| `0 000 000` | `1100 000 000` | 10 | **Meta Node** |
| `0 000 001` | `1100 000 001` | 10 | Triple Edge |
| `0 000 010` | `1100 000 010` | 10 | Clause Edge |
| `0 000 011` | `1100 000 011` | 10 | Event6 Edge |
| `0 000 100` | `1100 000 100` | 10 | Context Edge |
| `0 000 101` | `1100 000 101` | 10 | Quantity Node |
| `0 000 110` | `1100 000 110` | 10 | **Faber Edge** |
| `0 000 111 000` | `1100 000 111 000` | 13 | **Group Edge** |

### 4.3 Issuer Namespace (bit1=1, bit2=0)

| 심사 | Prefix | Issuer 수 | 내부 공간 |
|------|--------|-----------|-----------|
| 엄격 | `100` | 8,192 | 48비트 |
| 최소 | `101` | 5.3억 | 32비트 |

### 4.4 Free / Reserved

| Prefix | 영역 |
|--------|------|
| `1101` | 완전 자유 |
| `111` | 차세대 예약 |

---

## 5. Prefix 요약표

### 5.1 영역 Prefix

| Prefix | 영역 |
|--------|------|
| `0` | Standard |
| `100` | Issuer (엄격) |
| `101` | Issuer (최소) |
| `1100` | Proposal |
| `1101` | Free |
| `111` | Reserved |

### 5.2 Standard 타입 Prefix

| Prefix | 비트 | 타입 |
|--------|------|------|
| `0 1` | 2 | Tiny Verb Edge |
| `0 01` | 3 | Verb Edge |
| `0 001` | 4 | Entity Node |
| `0 000 000` | 7 | **Meta Node** |
| `0 000 001` | 7 | Triple Edge |
| `0 000 010` | 7 | Clause Edge |
| `0 000 011` | 7 | Event6 Edge |
| `0 000 100` | 7 | Context Edge |
| `0 000 101` | 7 | Quantity Node |
| `0 000 110` | 7 | **Faber Edge** |
| `0 000 111` | 7 | 확장 영역 |
| `0 000 111 000` | 10 | **Group Edge** |
| `0 000 111 001~110` | 10 | 예약 |
| `0 000 111 111` | 10 | 2차 확장 |

### 5.3 Proposal 패킷 Prefix (현재 사용)

| Prefix | 비트 | 타입 |
|--------|------|------|
| `1100 1` | 5 | Tiny Verb Edge |
| `1100 01` | 6 | Verb Edge |
| `1100 001` | 7 | Entity Node |
| `1100 000 000` | 10 | **Meta Node** |
| `1100 000 001` | 10 | Triple Edge |
| `1100 000 010` | 10 | Clause Edge |
| `1100 000 011` | 10 | Event6 Edge |
| `1100 000 100` | 10 | Context Edge |
| `1100 000 101` | 10 | Quantity Node |
| `1100 000 110` | 10 | **Faber Edge** |

---

## 6. 타입별 요약

| 타입 | Prefix (Proposal) | 워드 | 용도 |
|------|-------------------|------|------|
| **Meta Node** | `1100 000 000` | 1~5 | 스트림 제어/메타데이터 |
| Tiny Verb Edge | `1100 1` | 2 | 고빈도 단순 서술 |
| Verb Edge | `1100 01` | 3~5 | 일반 서술 |
| Entity Node | `1100 001` | 3~5 | 개체 정의 |
| Triple Edge | `1100 000 001` | 4~5 | 속성/관계 |
| Clause Edge | `1100 000 010` | 4 | 담화/논리 |
| Event6 Edge | `1100 000 011` | 3~8 | 6하원칙 사건 |
| Context Edge | `1100 000 100` | 3 | 세계관/맥락 |
| Quantity Node | `1100 000 101` | 4~7 | 물리량/수치 |
| **Faber Edge** | `1100 000 110` | 4+ | 코드/AST 표현 |
| **Group Edge** | `1100 000 111 000` | 4+ | 집합/그룹 |

---

## 7. 구현

### 7.1 영역 파서

```python
def parse_sidx_region(sidx: int) -> str:
    bit1 = (sidx >> 63) & 1
    
    if bit1 == 0:
        return "Standard"
    
    bit2 = (sidx >> 62) & 1
    if bit2 == 0:
        bit3 = (sidx >> 61) & 1
        return "Issuer_Strict" if bit3 == 0 else "Issuer_Loose"
    
    bit3 = (sidx >> 61) & 1
    if bit3 == 1:
        return "Reserved"
    
    bit4 = (sidx >> 60) & 1
    return "Proposal" if bit4 == 0 else "Free"
```

### 7.2 Standard 타입 파서

```python
def parse_standard_type(sidx: int) -> str:
    """bit1=0 확인 후 호출"""
    
    bit2 = (sidx >> 62) & 1
    if bit2 == 1:
        return "Tiny Verb Edge"
    
    bit3 = (sidx >> 61) & 1
    if bit3 == 1:
        return "Verb Edge"
    
    bit4 = (sidx >> 60) & 1
    if bit4 == 1:
        return "Entity Node"
    
    # 7비트 통일 영역 (bit2~4 = 000)
    sub = (sidx >> 57) & 0x7
    return {
        0b000: "Meta Node",
        0b001: "Triple Edge",
        0b010: "Clause Edge",
        0b011: "Event6 Edge",
        0b100: "Context Edge",
        0b101: "Quantity Node",
        0b110: "Faber Edge",
        0b111: "Extension",
    }.get(sub, "Unknown")
```

### 7.3 패킷 Prefix 파서

```python
def parse_packet_prefix(word1: int) -> str:
    # Proposal Tiny Verb: 11001 (5비트)
    if (word1 >> 11) == 0b11001:
        return "Tiny Verb Edge"
    
    # Proposal Verb: 110001 (6비트)
    if (word1 >> 10) == 0b110001:
        return "Verb Edge"
    
    # Proposal Entity: 1100001 (7비트)
    if (word1 >> 9) == 0b1100001:
        return "Entity Node"
    
    # Proposal 7비트 통일: 1100000 (7비트) + xxx (3비트) = 10비트
    if (word1 >> 9) == 0b1100000:
        sub = (word1 >> 6) & 0x7
        if sub == 0b111:
            # 확장 영역: 추가 3비트 확인
            ext = (word1 >> 3) & 0x7
            return {
                0b000: "Group Edge",
                0b111: "Extension2",
            }.get(ext, f"Reserved_ext_{ext}")
        return {
            0b000: "Meta Node",
            0b001: "Triple Edge",
            0b010: "Clause Edge",
            0b011: "Event6 Edge",
            0b100: "Context Edge",
            0b101: "Quantity Node",
            0b110: "Faber Edge",
        }.get(sub, "Unknown")
    
    return "Unknown"
```

---

## 8. 인코딩 규칙

### 8.1 바이트 오더

**GEUL은 Big Endian (Network Byte Order)를 사용한다.**

| 항목 | 규칙 |
|------|------|
| 바이트 오더 | **Big Endian** |
| 비트 오더 | MSB First (bit1 = MSB) |
| 워드 크기 | 16비트 (2바이트) |

### 8.2 Big Endian 예시

```
16비트 값 0x1234:
  메모리: [0x12] [0x34]
  
32비트 값 0x12345678:
  메모리: [0x12] [0x34] [0x56] [0x78]

64비트 값 0x123456789ABCDEF0:
  메모리: [0x12] [0x34] [0x56] [0x78] [0x9A] [0xBC] [0xDE] [0xF0]
```

### 8.3 워드 정렬

- 모든 필드는 **16비트 워드 경계**에 정렬
- 패킷 크기는 항상 **워드 단위** (2바이트 배수)
- 패딩 필요 시 **0x00**으로 채움

### 8.4 선택 근거

| 이유 | 설명 |
|------|------|
| SIDX 일관성 | bit1 = MSB 규칙과 일치 |
| 가독성 | 사람이 읽는 순서와 동일 |
| 네트워크 호환 | TCP/IP 표준과 동일 |
| 디버깅 용이 | 헥스 덤프가 직관적 |

---

## 9. 버전 히스토리

| 버전 | 날짜 | 변경 |
|------|------|------|
| v0.1 | - | 초기 구조 |
| v0.2 | 2026-01-29 | Proposal을 Free 하위로 이동 |
| v0.3 | 2026-01-29 | 허프만 스타일 추가 |
| v0.4 | 2026-01-29 | 2단계 Prefix 체계, Quantity Node 추가 |
| v0.5 | 2026-01-29 | Context Edge 확정, Reserved 슬롯 정리 |
| v0.6 | 2026-01-29 | Prefix 표기 일관성 수정, Faber Edge 추가 |
| v0.7 | 2026-01-30 | **Meta Node 추가** (`0 000 000`), **Faber Edge 이동** (`0 000 110`) |
| v0.8 | 2026-01-30 | **Group Edge 추가** (`0 000 111 000`), 확장 영역 정의 |
| v0.9 | 2026-01-30 | **인코딩 규칙 추가**: Big Endian (Network Byte Order) 확정 |

---

## 10. 관련 문서

| 문서 | 내용 |
|------|------|
| `Meta_Node.md` | **Meta Node 상세 (스트림 제어)** |
| `Verb_Edge.md` | Tiny/Verb Edge 상세 |
| `Entity_Node.md` | Entity Node 상세 |
| `Triple_Edge.md` | Triple Edge 상세 |
| `Clause_Edge.md` | Clause Edge 상세 |
| `Event6_Edge.md` | Event6 Edge 상세 |
| `Context_Edge.md` | Context Edge 상세 |
| `Quantity_Node.md` | Quantity Node 상세 |
| `Faber_Edge.md` | Faber Edge 상세 (코드/AST) |
| `Group_Edge.md` | **Group Edge 상세 (집합/그룹)** |

---

**문서 종료**