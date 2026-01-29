# GEUL SIDX 비트 명세서

**버전:** v0.5  
**작성일:** 2026-01-29  
**범위:** SIDX 64비트 최상위 구조  
**비트 규칙:** bit1 = MSB, bit64 = LSB

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
| `1` | 1 | Tiny Verb Edge | 최고빈도 |
| `01` | 2 | Verb Edge | 고빈도 |
| `001` | 3 | Entity Node | 고빈도 |
| `0001 001` | 7 | Triple Edge | 중빈도 |
| `0001 010` | 7 | Clause Edge | 저빈도 |
| `0001 011` | 7 | Event6 Edge | 저빈도 |
| `0001 100` | 7 | Context Edge | 저빈도 |
| `0001 101` | 7 | Quantity Node | 중빈도 |
| `0001 110` | 7 | Reserved | - |
| `0001 111` | 7 | Reserved | - |
| `0001 000` | 7 | Reserved | - |

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
│         ├─ 1          (1)         → Tiny Verb Edge
│         ├─ 01         (01)        → Verb Edge
│         ├─ 001        (001)       → Entity Node
│         └─ 0001       (0001)      → 7비트 통일 영역
│               │
│               └─ bit5~7 (3비트)
│                   ├─ 001 (0001 001) → Triple Edge
│                   ├─ 010 (0001 010) → Clause Edge
│                   ├─ 011 (0001 011) → Event6 Edge
│                   ├─ 100 (0001 100) → Context Edge
│                   ├─ 101 (0001 101) → Quantity Node
│                   ├─ 110 (0001 110) → Reserved
│                   ├─ 111 (0001 111) → Reserved
│                   └─ 000 (0001 000) → Reserved
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
| `1` | 1 | Tiny Verb Edge | 고빈도 단순 서술 |
| `01` | 2 | Verb Edge | 일반 서술 |
| `001` | 3 | Entity Node | 개체 |
| `0001 001` | 7 | Triple Edge | 속성/관계 |
| `0001 010` | 7 | Clause Edge | 담화/논리 관계 |
| `0001 011` | 7 | Event6 Edge | 6하원칙 사건 |
| `0001 100` | 7 | Context Edge | 세계관/출처/맥락 |
| `0001 101` | 7 | Quantity Node | 물리량/수치 |

### 4.2 Proposal (bit1~4 = 1100)

**표준 제안 레인.** Standard를 미러링.

| Standard | Proposal | 비트 | 타입 |
|----------|----------|------|------|
| `1` | `11001` | 5 | Tiny Verb Edge |
| `01` | `110001` | 6 | Verb Edge |
| `001` | `1100001` | 7 | Entity Node |
| `0001 001` | `1100000 001` | 10 | Triple Edge |
| `0001 010` | `1100000 010` | 10 | Clause Edge |
| `0001 011` | `1100000 011` | 10 | Event6 Edge |
| `0001 100` | `1100000 100` | 10 | Context Edge |
| `0001 101` | `1100000 101` | 10 | Quantity Node |

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

### 5.2 Standard 타입 Prefix (7비트)

| Prefix | 타입 |
|--------|------|
| `1` | Tiny Verb Edge |
| `01` | Verb Edge |
| `001` | Entity Node |
| `0001 001` | Triple Edge |
| `0001 010` | Clause Edge |
| `0001 011` | Event6 Edge |
| `0001 100` | Context Edge |
| `0001 101` | Quantity Node |
| `0001 110` | Reserved |
| `0001 111` | Reserved |
| `0001 000` | Reserved |

### 5.3 Proposal 패킷 Prefix (현재 사용)

| Prefix | 비트 | 타입 |
|--------|------|------|
| `11001` | 5 | Tiny Verb Edge |
| `110001` | 6 | Verb Edge |
| `1100001` | 7 | Entity Node |
| `1100000 001` | 10 | Triple Edge |
| `1100000 010` | 10 | Clause Edge |
| `1100000 011` | 10 | Event6 Edge |
| `1100000 100` | 10 | Context Edge |
| `1100000 101` | 10 | Quantity Node |

---

## 6. 타입별 요약

| 타입 | Prefix (Proposal) | 워드 | 용도 |
|------|-------------------|------|------|
| Tiny Verb Edge | `11001` | 2 | 고빈도 단순 서술 |
| Verb Edge | `110001` | 3~5 | 일반 서술 |
| Entity Node | `1100001` | 3~5 | 개체 정의 |
| Triple Edge | `1100000 001` | 4~5 | 속성/관계 |
| Clause Edge | `1100000 010` | 4 | 담화/논리 |
| Event6 Edge | `1100000 011` | 3~8 | 6하원칙 사건 |
| Context Edge | `1100000 100` | 3 | 세계관/맥락 |
| Quantity Node | `1100000 101` | 4~7 | 물리량/수치 |

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
    
    # 7비트 통일 영역
    sub = (sidx >> 57) & 0x7
    return {
        0b001: "Triple Edge",
        0b010: "Clause Edge",
        0b011: "Event6 Edge",
        0b100: "Context Edge",
        0b101: "Quantity Node",
    }.get(sub, "Reserved")
```

### 7.3 패킷 Prefix 파서

```python
def parse_packet_prefix(word1: int) -> str:
    if (word1 >> 11) == 0b11001:
        return "Tiny Verb Edge"
    if (word1 >> 10) == 0b110001:
        return "Verb Edge"
    if (word1 >> 9) == 0b1100001:
        return "Entity Node"
    if (word1 >> 9) == 0b1100000:
        sub = (word1 >> 6) & 0x7
        return {
            0b001: "Triple Edge",
            0b010: "Clause Edge",
            0b011: "Event6 Edge",
            0b100: "Context Edge",
            0b101: "Quantity Node",
        }.get(sub, "Unknown")
    return "Unknown"
```

---

## 8. 버전 히스토리

| 버전 | 날짜 | 변경 |
|------|------|------|
| v0.1 | - | 초기 구조 |
| v0.2 | 2026-01-29 | Proposal을 Free 하위로 이동 |
| v0.3 | 2026-01-29 | 허프만 스타일 추가 |
| v0.4 | 2026-01-29 | 2단계 Prefix 체계, Quantity Node 추가 |
| v0.5 | 2026-01-29 | **Context Edge 확정**, Reserved 슬롯 정리 |

---

## 9. 관련 문서

| 문서 | 내용 |
|------|------|
| `Verb_Edge.md` | Tiny/Verb Edge 상세 |
| `Entity_Node.md` | Entity Node 상세 |
| `Triple_Edge.md` | Triple Edge 상세 |
| `Clause_Edge.md` | Clause Edge 상세 |
| `Event6_Edge.md` | Event6 Edge 상세 |
| `Context_Edge.md` | Context Edge 상세 |
| `Quantity_Node.md` | Quantity Node 상세 |

---

**문서 종료**