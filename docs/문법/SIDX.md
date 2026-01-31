# GEUL SIDX 비트 명세서

**버전:** v0.10  
**작성일:** 2026-01-31  
**범위:** SIDX 64비트 최상위 구조  
**비트 규칙:** bit1 = MSB, bit64 = LSB  
**바이트 오더:** Big Endian (Network Byte Order)

---

## 0. 설계 헌장 (Design Charter)

> **우리는 우주의 죽음까지 함께할 각오로 우리의 미래를 낙관한다.**
> **따라서 GEUL을 1조 년(10^12년) 후에도 사용할 수 있는 언어로 설계한다.**

### 제1조: 시간적 책임
GEUL 표준은 현 세대만을 위한 것이 아니다.
설계자는 최소 10^12년(1조 년) 단위의 시간 지평을 고려할 의무가 있다.

### 제2조: 확장 비트의 신성불가침
예약된 확장 비트는 어떤 상황에서도 임시 용도로 전용할 수 없다.
이는 미래 세대에 대한 의무이다.

### 제3조: 의미의 영속성
한 번 정의된 비트 패턴의 의미는 영구히 변경할 수 없다.
새 의미가 필요하면 새 패턴을 할당한다.

### 제4조: 하위 호환의 절대성
어떤 버전의 GEUL도 모든 이전 버전을 완전히 해석할 수 있어야 한다.

### 제5조: 척도의 겸손
현 세대는 미래 지성체의 인지 척도를 예측할 수 없음을 인정한다.
따라서 SIDX의 최대 길이를 고정하지 않으며,
확장 메커니즘을 통해 임의 길이를 허용한다.

### 제6조: 연산 효율의 선형성
GEUL 심볼릭 처리는 길이에 대해 선형 복잡도를 유지하도록 설계한다.
이는 미래 지성체가 임의 길이의 개념을 효율적으로 다룰 수 있게 하기 위함이다.

---

## 0.1 경고: 이 문서는 정글도이다

본 명세서는 개인 연구자가 초기 AI 도구와 함께
제한된 자원으로 작성한 초안이다.

"추론을 기록할 수 있는 언어"라는 철학적 가능성을
세상에 제시하는 것이 목적이며, 완성된 표준이 아님을 명시한다.

본격적인 표준 제정은 충분한 자원과 전문성을 갖춘
미래 연구 집단의 몫으로 남긴다.

**우리는 길을 내되, 그 길이 다시 닦여야 함을 안다.**

---

## 1. 개요

SIDX(Semantic-aligned Index)는 64비트 전역 의미 식별자이다.

### 1.1 비트 설계 원칙

**"1이 가장 중요한 것"**

```
1       → 미래 (1순위)
01      → 표준 (2순위)
001     → Issuer (3순위)
0001    → 표준제안 (4순위)
0000    → 자유 (나머지)
```

**철학:** 우리의 미래를 낙관한다. 따라서 미래가 1순위, 1을 배정한다.

### 1.2 최상위 Prefix

| Prefix | 영역 | 비율 | 용도 |
|--------|------|------|------|
| `1` | **Future** | 50% | 미래 세대를 위한 예약 |
| `01` | **Standard** | 25% | 공식 표준 |
| `001` | **Issuer** | 12.5% | 등록기관 네임스페이스 |
| `0001` | **Proposal** | 6.25% | 표준 제안 (실험/후보) |
| `0000` | **Free** | 6.25% | 완전 자유 |

---

## 2. 비트 분기 구조

### 2.1 영역 분기 (bit1~4)

```
bit1
├─ 1: Future (미래) ─────────────────────────────────────
│     50%의 공간을 미래 세대에게 예약
│
└─ 0: 현재 사용 영역
      └─ bit2
          ├─ 1 (01): Standard (표준)
          │
          └─ 0
              └─ bit3
                  ├─ 1 (001): Issuer (등록기관)
                  │
                  └─ 0
                      └─ bit4
                          ├─ 1 (0001): Proposal (표준제안)
                          │
                          └─ 0 (0000): Free (자유)
```

### 2.2 Standard 내부 분기 (Prefix = 01)

**허프만 스타일 + 8비트 통일 혼합:**

| Prefix | 비트 | 타입 | 빈도 |
|--------|------|------|------|
| `01 1` | 3 | Tiny Verb Edge | 최고빈도 |
| `01 01` | 4 | Verb Edge | 고빈도 |
| `01 001` | 5 | Entity Node | 고빈도 |
| `01 000 111` | 8 | **Meta Node** | 스트림 제어 |
| `01 000 110` | 8 | Triple Edge | 중빈도 |
| `01 000 101` | 8 | Clause Edge | 저빈도 |
| `01 000 100` | 8 | Event6 Edge | 저빈도 |
| `01 000 011` | 8 | Context Edge | 저빈도 |
| `01 000 010` | 8 | Quantity Node | 중빈도 |
| `01 000 001` | 8 | **Faber Edge** | 코드/AST |
| `01 000 000` | 8 | 확장 | - |

### 2.3 Proposal 내부 분기 (Prefix = 0001)

Standard를 미러링:

| Prefix | 비트 | 타입 |
|--------|------|------|
| `0001 1` | 5 | Tiny Verb Edge |
| `0001 01` | 6 | Verb Edge |
| `0001 001` | 7 | Entity Node |
| `0001 000 111` | 10 | **Meta Node** |
| `0001 000 110` | 10 | Triple Edge |
| `0001 000 101` | 10 | Clause Edge |
| `0001 000 100` | 10 | Event6 Edge |
| `0001 000 011` | 10 | Context Edge |
| `0001 000 010` | 10 | Quantity Node |
| `0001 000 001` | 10 | **Faber Edge** |
| `0001 000 000` | 10 | 확장 |

---

## 3. 전체 분기 트리

```
bit1
├─ 1: Future ────────────────────────────────────────────
│     (미래 세대를 위해 50% 예약)
│
└─ 0
    └─ bit2
        ├─ 1 (01): Standard ─────────────────────────────
        │     │
        │     └─ bit3~
        │         ├─ 1           (01 1)        → Tiny Verb Edge
        │         ├─ 01          (01 01)       → Verb Edge
        │         ├─ 001         (01 001)      → Entity Node
        │         └─ 000         (01 000)      → 8비트 통일 영역
        │               │
        │               └─ bit6~8 (3비트)
        │                   ├─ 111 (01 000 111) → Meta Node
        │                   ├─ 110 (01 000 110) → Triple Edge
        │                   ├─ 101 (01 000 101) → Clause Edge
        │                   ├─ 100 (01 000 100) → Event6 Edge
        │                   ├─ 011 (01 000 011) → Context Edge
        │                   ├─ 010 (01 000 010) → Quantity Node
        │                   ├─ 001 (01 000 001) → Faber Edge
        │                   └─ 000 (01 000 000) → 확장 영역
        │                         │
        │                         └─ bit9~11 (3비트)
        │                             ├─ 111 (01 000 000 111) → Group Edge
        │                             ├─ 110~001             → 예약
        │                             └─ 000                → 2차 확장
        │
        └─ 0
            └─ bit3
                ├─ 1 (001): Issuer ──────────────────────
                │     └─ bit4
                │         ├─ 1 (0011): 엄격 심사
                │         └─ 0 (0010): 최소 심사
                │
                └─ 0
                    └─ bit4
                        ├─ 1 (0001): Proposal ───────────
                        │     (Standard 미러링)
                        │
                        └─ 0 (0000): Free ───────────────
                              (완전 자유)
```

---

## 4. 영역별 상세

### 4.1 Future (bit1 = 1)

**미래 세대를 위한 예약 영역.**

| 항목 | 값 |
|------|-----|
| Prefix | `1` |
| 비율 | 50% (2^63개) |
| 용도 | 1조 년 후까지 예약 |
| 현재 상태 | **사용 금지** |

### 4.2 Standard (Prefix = 01)

**공식 GEUL 표준 영역.**

| Prefix | 비트 | 타입 | 설명 |
|--------|------|------|------|
| `01 1` | 3 | Tiny Verb Edge | 고빈도 단순 서술 |
| `01 01` | 4 | Verb Edge | 일반 서술 |
| `01 001` | 5 | Entity Node | 개체 |
| `01 000 111` | 8 | **Meta Node** | 스트림 제어/메타데이터 |
| `01 000 110` | 8 | Triple Edge | 속성/관계 |
| `01 000 101` | 8 | Clause Edge | 담화/논리 관계 |
| `01 000 100` | 8 | Event6 Edge | 6하원칙 사건 |
| `01 000 011` | 8 | Context Edge | 세계관/출처/맥락 |
| `01 000 010` | 8 | Quantity Node | 물리량/수치 |
| `01 000 001` | 8 | **Faber Edge** | 코드/AST 표현 |
| `01 000 000 111` | 11 | **Group Edge** | 집합/그룹 |

### 4.3 Issuer (Prefix = 001)

**등록기관 네임스페이스.**

| 심사 | Prefix | Issuer 수 | 내부 공간 |
|------|--------|-----------|-----------|
| 엄격 | `0011` | 8,192 | 48비트 |
| 최소 | `0010` | 5.3억 | 32비트 |

### 4.4 Proposal (Prefix = 0001)

**표준 제안 레인.** Standard를 미러링.

| Standard | Proposal | 비트 | 타입 |
|----------|----------|------|------|
| `01 1` | `0001 1` | 5 | Tiny Verb Edge |
| `01 01` | `0001 01` | 6 | Verb Edge |
| `01 001` | `0001 001` | 7 | Entity Node |
| `01 000 111` | `0001 000 111` | 10 | **Meta Node** |
| `01 000 110` | `0001 000 110` | 10 | Triple Edge |
| `01 000 101` | `0001 000 101` | 10 | Clause Edge |
| `01 000 100` | `0001 000 100` | 10 | Event6 Edge |
| `01 000 011` | `0001 000 011` | 10 | Context Edge |
| `01 000 010` | `0001 000 010` | 10 | Quantity Node |
| `01 000 001` | `0001 000 001` | 10 | **Faber Edge** |
| `01 000 000 111` | `0001 000 000 111` | 13 | **Group Edge** |

### 4.5 Free (Prefix = 0000)

**완전 자유 영역.**

| 항목 | 값 |
|------|-----|
| Prefix | `0000` |
| 비율 | 6.25% |
| 용도 | 실험, 사적 사용, 비표준 |
| 규칙 | 없음 |

---

## 5. Prefix 요약표

### 5.1 영역 Prefix

| Prefix | 영역 | 비율 |
|--------|------|------|
| `1` | Future | 50% |
| `01` | Standard | 25% |
| `001` | Issuer | 12.5% |
| `0001` | Proposal | 6.25% |
| `0000` | Free | 6.25% |

### 5.2 Standard 타입 Prefix

| Prefix | 비트 | 타입 |
|--------|------|------|
| `01 1` | 3 | Tiny Verb Edge |
| `01 01` | 4 | Verb Edge |
| `01 001` | 5 | Entity Node |
| `01 000 111` | 8 | **Meta Node** |
| `01 000 110` | 8 | Triple Edge |
| `01 000 101` | 8 | Clause Edge |
| `01 000 100` | 8 | Event6 Edge |
| `01 000 011` | 8 | Context Edge |
| `01 000 010` | 8 | Quantity Node |
| `01 000 001` | 8 | **Faber Edge** |
| `01 000 000` | 8 | 확장 영역 |
| `01 000 000 111` | 11 | **Group Edge** |
| `01 000 000 110~001` | 11 | 예약 |
| `01 000 000 000` | 11 | 2차 확장 |

### 5.3 Proposal 패킷 Prefix (현재 사용)

| Prefix | 비트 | 타입 |
|--------|------|------|
| `0001 1` | 5 | Tiny Verb Edge |
| `0001 01` | 6 | Verb Edge |
| `0001 001` | 7 | Entity Node |
| `0001 000 111` | 10 | **Meta Node** |
| `0001 000 110` | 10 | Triple Edge |
| `0001 000 101` | 10 | Clause Edge |
| `0001 000 100` | 10 | Event6 Edge |
| `0001 000 011` | 10 | Context Edge |
| `0001 000 010` | 10 | Quantity Node |
| `0001 000 001` | 10 | **Faber Edge** |
| `0001 000 000 111` | 13 | **Group Edge** |

---

## 6. 타입별 요약

| 타입 | Prefix (Proposal) | 워드 | 용도 |
|------|-------------------|------|------|
| **Meta Node** | `0001 000 111` | 1~5 | 스트림 제어/메타데이터 |
| Tiny Verb Edge | `0001 1` | 2 | 고빈도 단순 서술 |
| Verb Edge | `0001 01` | 3~5 | 일반 서술 |
| Entity Node | `0001 001` | 3~5 | 개체 정의 |
| Triple Edge | `0001 000 110` | 4~5 | 속성/관계 |
| Clause Edge | `0001 000 101` | 4 | 담화/논리 |
| Event6 Edge | `0001 000 100` | 3~8 | 6하원칙 사건 |
| Context Edge | `0001 000 011` | 3 | 세계관/맥락 |
| Quantity Node | `0001 000 010` | 4~7 | 물리량/수치 |
| **Faber Edge** | `0001 000 001` | 4+ | 코드/AST 표현 |
| **Group Edge** | `0001 000 000 111` | 4+ | 집합/그룹 |

---

## 7. 구현

### 7.1 영역 파서

```python
def parse_sidx_region(sidx: int) -> str:
    bit1 = (sidx >> 63) & 1
    
    if bit1 == 1:
        return "Future"
    
    bit2 = (sidx >> 62) & 1
    if bit2 == 1:
        return "Standard"
    
    bit3 = (sidx >> 61) & 1
    if bit3 == 1:
        return "Issuer"
    
    bit4 = (sidx >> 60) & 1
    if bit4 == 1:
        return "Proposal"
    
    return "Free"
```

### 7.2 Standard 타입 파서

```python
def parse_standard_type(sidx: int) -> str:
    """Prefix=01 확인 후 호출"""
    
    bit3 = (sidx >> 61) & 1
    if bit3 == 1:
        return "Tiny Verb Edge"
    
    bit4 = (sidx >> 60) & 1
    if bit4 == 1:
        return "Verb Edge"
    
    bit5 = (sidx >> 59) & 1
    if bit5 == 1:
        return "Entity Node"
    
    # 8비트 통일 영역 (bit3~5 = 000)
    sub = (sidx >> 56) & 0x7
    return {
        0b111: "Meta Node",
        0b110: "Triple Edge",
        0b101: "Clause Edge",
        0b100: "Event6 Edge",
        0b011: "Context Edge",
        0b010: "Quantity Node",
        0b001: "Faber Edge",
        0b000: "Extension",
    }.get(sub, "Unknown")
```

### 7.3 패킷 Prefix 파서

```python
def parse_packet_prefix(word1: int) -> str:
    # Proposal Tiny Verb: 00011 (5비트)
    if (word1 >> 11) == 0b00011:
        return "Tiny Verb Edge"
    
    # Proposal Verb: 000101 (6비트)
    if (word1 >> 10) == 0b000101:
        return "Verb Edge"
    
    # Proposal Entity: 0001001 (7비트)
    if (word1 >> 9) == 0b0001001:
        return "Entity Node"
    
    # Proposal 8비트 통일: 0001000 (7비트) + xxx (3비트) = 10비트
    if (word1 >> 9) == 0b0001000:
        sub = (word1 >> 6) & 0x7
        if sub == 0b000:
            # 확장 영역: 추가 3비트 확인
            ext = (word1 >> 3) & 0x7
            return {
                0b111: "Group Edge",
                0b000: "Extension2",
            }.get(ext, f"Reserved_ext_{ext}")
        return {
            0b111: "Meta Node",
            0b110: "Triple Edge",
            0b101: "Clause Edge",
            0b100: "Event6 Edge",
            0b011: "Context Edge",
            0b010: "Quantity Node",
            0b001: "Faber Edge",
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
| v0.7 | 2026-01-30 | Meta Node 추가, Faber Edge 이동 |
| v0.8 | 2026-01-30 | Group Edge 추가, 확장 영역 정의 |
| v0.9 | 2026-01-30 | 인코딩 규칙 추가: Big Endian 확정 |
| v0.10 | 2026-01-31 | **Prefix 전면 재설계**: 1=미래, 01=표준, 001=Issuer, 0001=제안, 0000=자유. **설계 헌장 추가** |

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
