# Stream Format 명세서

**버전:** v0.2  
**작성일:** 2026-01-30  
**목적:** GEUL 패킷들의 스트림 구성 규칙 정의

---

## 1. 개요

GEUL 스트림은 **Meta Node로 시작하고 끝나는 패킷 시퀀스**이다.

**핵심 특징:**
- **경계 명시:** STREAM_START / STREAM_END (Meta Node)
- **TID 스코프:** 스트림 내에서만 유효
- **순방향 참조:** 선언된 TID만 참조 가능
- **Big Endian:** Network Byte Order

**스트림 = 하나의 완결된 GEUL 문서**

---

## 2. 스트림 구조

### 2.1 기본 형식

```
┌─────────────────────────────────────┐
│          STREAM_START               │  ← 필수 (Meta Node)
│          (TID 폭 선언)               │     0xC000 (16비트 TID)
├─────────────────────────────────────┤
│          메타데이터 (선택)            │
│          - VERSION    (0xC014)      │
│          - CREATED_AT (0xC008)      │
│          - CREATOR    (0xC010)      │
├─────────────────────────────────────┤
│          본문 패킷들                  │
│          - Meta Node (제어)         │  0 000 000
│          - Entity Node              │  0 001
│          - Quantity Node            │  0 000 101
│          - Tiny Verb Edge           │  0 1
│          - Verb Edge                │  0 01
│          - Triple Edge              │  0 000 001
│          - Event6 Edge              │  0 000 011
│          - Clause Edge              │  0 000 010
│          - Context Edge             │  0 000 100
│          - Group Edge               │  0 000 111 000
│          - Faber Edge               │  0 000 110
├─────────────────────────────────────┤
│          STREAM_END                 │  ← 선택 (권장)
│                                     │     0xC004
└─────────────────────────────────────┘
```

### 2.2 최소 스트림

```
[STREAM_START]     - 1워드 (0xC000)
[STREAM_END]       - 1워드 (0xC004)

총: 2워드 (4바이트)
```

빈 스트림도 유효함.

### 2.3 일반 스트림

```
[STREAM_START]     - 1워드 (0xC000, TID 16비트)
[Entity Node]      - N워드
[Entity Node]      - N워드
[Verb Edge]        - N워드
[STREAM_END]       - 1워드 (0xC004)
```

---

## 3. Meta Node (스트림 제어)

### 3.1 STREAM_START

**Prefix:** `1100 000 000` (10비트)

```
1st WORD: [1100 000 000] [0000] [PP]
          └─ Prefix ─┘   └Type┘ └Payload
```

| Payload | TID 폭 | 범위 | 헥스 값 |
|---------|--------|------|---------|
| 00 | 16비트 | 0~65,535 | 0xC000 |
| 01 | 32비트 | 0~4.2B | 0xC001 |
| 10 | 64비트 | 무제한 | 0xC002 |
| 11 | 예약 | - | 0xC003 |

**필수 규칙:**
- 모든 GEUL 스트림은 STREAM_START로 시작
- 기본값: Payload `00` (16비트 TID) 권장
- 이후 모든 TID 참조는 선언된 폭을 따름

### 3.2 STREAM_END

```
1st WORD: [1100 000 000] [0001] [00] = 0xC004
```

**선택 규칙:**
- 스트림 끝에 명시적 종료 표시 (권장)
- 파싱 완료 확인용

### 3.3 기타 Meta Node

| Type | 이름 | 헥스 | 용도 |
|------|------|------|------|
| 0010 | CREATED_AT | 0xC008 | 생성 시간 |
| 0011 | MODIFIED_AT | 0xC00C | 수정 시간 |
| 0100 | CREATOR | 0xC010 | 생성자 |
| 0101 | VERSION | 0xC014 | 버전 정보 |

상세: `Meta_Node.md` 참조

---

## 4. TID 할당 원칙

### 4.1 기본 규칙

| 규칙 | 설명 |
|------|------|
| **필수성** | 스트림 내 모든 Edge/Node는 TID를 가진다 |
| **유일성** | 스트림 내에서 TID는 유일하다 |
| **스코프** | TID는 해당 스트림 내에서만 유효하다 |
| **순방향** | 참조 시점에 이미 선언된 TID만 참조 가능 |

### 4.2 TID 위치

**원칙:** TID 선언은 참조 나열보다 앞에 위치한다.

| 타입 | TID 위치 | 참조 위치 | 비고 |
|------|----------|-----------|------|
| **Meta Node** | 없음 | 없음 | TID 불필요 |
| **Entity Node** | 마지막 워드 | 없음 | 참조 없음 |
| **Quantity Node** | 마지막 워드 | 없음 | 참조 없음 |
| **Tiny Verb Edge** | 없음 | 없음 | TID 없음 (인라인) |
| **Verb Edge** | Header 영역 | Payload 이후 | 참여자 TID |
| **Triple Edge** | Header 영역 | Payload 이후 | S, P, O TID |
| **Event6 Edge** | Header 영역 | Payload 이후 | 6하원칙 TID |
| **Clause Edge** | Header 영역 | Payload 이후 | 절 TID |
| **Context Edge** | Header 영역 | Payload 이후 | 대상 TID |
| **Group Edge** | 2nd 워드 | 3rd+ 워드 | 멤버 TID |
| **Faber Edge** | 3rd 워드 | 4th+ 워드 | 자식 TID |

**Node vs Edge:**
- **Node:** 자기 자신만 정의 (참조 없음) → TID 마지막
- **Edge:** 다른 TID 참조 → TID가 참조보다 앞

**특수 케이스:**
- **Meta Node:** 스트림 제어용, TID 불필요
- **Tiny Verb Edge:** 인라인 서술용, TID 없음

### 4.3 TID 할당 전략

| 전략 | 설명 | 예시 |
|------|------|------|
| 순차 할당 | 0x0001부터 순차 증가 | 0x0001, 0x0002, 0x0003... |
| 영역 분리 | 타입별 범위 지정 | Node: 0x0001~0x7FFF, Edge: 0x8000~0xFFFF |
| 해시 기반 | 내용 해시의 하위 비트 | 충돌 시 재할당 |

**권장:** 순차 할당 (단순, 예측 가능)

### 4.4 예약 TID

| TID | 용도 |
|-----|------|
| 0x0000 | **종결 마커** (Group/Faber Edge) |
| 0xFFFF | 예약 (16비트 기준) |

---

## 5. 패킷 순서 규칙

### 5.1 선언-참조 순서

```
✅ 올바름:
  [Entity: 철수, TID=0x0001]
  [Entity: 영희, TID=0x0002]
  [Verb Edge: 만나다, Subject=0x0001, Object=0x0002]

❌ 잘못됨:
  [Verb Edge: 만나다, Subject=0x0001, Object=0x0002]  ← 0x0001 미선언
  [Entity: 철수, TID=0x0001]
  [Entity: 영희, TID=0x0002]
```

### 5.2 권장 순서

```
1. STREAM_START
2. 메타데이터 (VERSION, CREATED_AT, CREATOR)
3. Entity Node들 (개체 선언)
4. Quantity Node들 (수량/리터럴)
5. Group Edge들 (그룹 정의)
6. Tiny Verb Edge들 (인라인 서술)
7. Verb Edge들 (일반 서술)
8. Triple Edge들 (속성/관계)
9. Event6 Edge들 (사건)
10. Clause Edge들 (담화 관계)
11. Context Edge들 (맥락)
12. Faber Edge들 (코드/AST)
13. STREAM_END
```

**참고:** 권장 순서일 뿐, 선언-참조 규칙만 지키면 자유

### 5.3 순환 참조

**금지:** A → B → A 형태의 순환 참조 불가

```
❌ 불가능:
  [Edge A, TID=0x0001, 참조=0x0002]  ← 0x0002 미선언
  [Edge B, TID=0x0002, 참조=0x0001]
```

**해결책:** 순환 관계는 별도 Edge로 표현

```
✅ 가능:
  [Entity A, TID=0x0001]
  [Entity B, TID=0x0002]
  [Edge: A→B, TID=0x0003]
  [Edge: B→A, TID=0x0004]
```

---

## 6. 바이트 오더

`SIDX.md` 참조

| 항목 | 규칙 |
|------|------|
| 바이트 오더 | **Big Endian** (Network Byte Order) |
| 비트 오더 | MSB First (bit1 = MSB) |
| 워드 크기 | 16비트 (2바이트) |

**Big Endian 예시:**

```
16비트 값 0x1234:
  메모리: [0x12] [0x34]
  
32비트 값 0x12345678:
  메모리: [0x12] [0x34] [0x56] [0x78]
```

---

## 7. 스트림 예시

### 7.1 "철수가 영희를 만났다"

```
바이트 스트림:

1. STREAM_START (TID 16비트)
   0xC0 0x00

2. Entity: 철수 (TID=0x0001)
   [Entity 패킷...] 0x00 0x01

3. Entity: 영희 (TID=0x0002)
   [Entity 패킷...] 0x00 0x02

4. Verb Edge: meet (TID=0x0100)
   Subject: 0x0001
   Object: 0x0002
   [Verb 패킷...] 0x01 0x00

5. STREAM_END
   0xC0 0x04
```

### 7.2 "철수와 영희가 학교에서 만났다"

```
1. STREAM_START
   0xC0 0x00

2. Entity: 철수 (TID=0x0001)
3. Entity: 영희 (TID=0x0002)
4. Entity: 학교 (TID=0x0003)

5. Group Edge: AND (TID=0x0010)
   멤버: 0x0001, 0x0002, 0x0000 (종결)

6. Verb Edge: meet (TID=0x0100)
   Subject: 0x0010 (그룹)
   Location: 0x0003

7. STREAM_END
   0xC0 0x04
```

### 7.3 메타데이터 포함 스트림

```
1. STREAM_START (TID 16비트)
   0xC0 0x00

2. VERSION (v1.0)
   0xC0 0x14, 0x01 0x00

3. CREATED_AT (2026-01-30 12:00:00 UTC)
   0xC0 0x08, 0x69 0x78, 0xC9 0x00
   (Unix timestamp: 1769774400 = 0x6978C900)

4. CREATOR (생성자 미상)
   0xC0 0x10

5. Entity: Apple (TID=0x0001)
6. Entity: Tesla (TID=0x0002)

7. Verb Edge: acquire (TID=0x0100)
   Subject: 0x0001
   Object: 0x0002

8. STREAM_END
   0xC0 0x04
```

---

## 8. 스트림 검증

### 8.1 필수 검증

| 항목 | 검증 |
|------|------|
| 시작 | STREAM_START로 시작하는가? |
| TID 유일성 | 중복 TID가 없는가? |
| 참조 유효성 | 참조된 TID가 모두 선언되었는가? |
| 순방향 | 참조 시점에 TID가 이미 선언되었는가? |

### 8.2 선택 검증

| 항목 | 검증 |
|------|------|
| 종료 | STREAM_END로 끝나는가? |
| 메타데이터 | VERSION이 있는가? |
| 완결성 | 모든 참조가 해결되는가? |

### 8.3 검증 예시 코드

```python
def validate_stream(packets: list) -> dict:
    """스트림 유효성 검증"""
    
    errors = []
    declared_tids = set()
    
    # 1. 시작 검증
    if not packets or packets[0].type != "STREAM_START":
        errors.append("스트림이 STREAM_START로 시작하지 않음")
    
    for packet in packets:
        # 2. TID 유일성 검증
        if packet.tid is not None:
            if packet.tid in declared_tids:
                errors.append(f"중복 TID: {packet.tid}")
            declared_tids.add(packet.tid)
        
        # 3. 참조 유효성 검증
        for ref_tid in packet.references:
            if ref_tid not in declared_tids:
                errors.append(f"미선언 TID 참조: {ref_tid}")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "tid_count": len(declared_tids)
    }
```

---

## 9. 다중 스트림

### 9.1 연결 (Concatenation)

```
[Stream A: STREAM_START ~ STREAM_END]
[Stream B: STREAM_START ~ STREAM_END]
```

- 각 스트림은 독립적
- TID 스코프는 스트림별로 분리
- Stream A의 TID=0x0001과 Stream B의 TID=0x0001은 다른 개체

### 9.2 참조 (Cross-reference)

**스트림 간 참조는 현재 미지원**

향후 확장:
- 스트림 ID 도입
- 글로벌 TID 체계
- Import/Export 메커니즘

---

## 10. 구현 가이드

### 10.1 스트림 생성

```python
def create_stream(packets: list, tid_bits: int = 16) -> bytes:
    """GEUL 스트림 생성"""
    
    result = bytearray()
    
    # 1. STREAM_START
    payload = {16: 0, 32: 1, 64: 2}[tid_bits]
    start = (0b1100000000 << 6) | (0 << 2) | payload
    result.extend(start.to_bytes(2, 'big'))
    
    # 2. 패킷들
    for packet in packets:
        result.extend(packet.encode())
    
    # 3. STREAM_END
    end = (0b1100000000 << 6) | (1 << 2) | 0
    result.extend(end.to_bytes(2, 'big'))
    
    return bytes(result)
```

### 10.2 스트림 파싱

```python
def parse_stream(data: bytes) -> list:
    """GEUL 스트림 파싱"""
    
    packets = []
    offset = 0
    tid_bits = 16  # 기본값
    
    while offset < len(data):
        word1 = int.from_bytes(data[offset:offset+2], 'big')
        
        # Prefix 확인
        packet_type = identify_packet_type(word1)
        
        if packet_type == "STREAM_START":
            payload = word1 & 0x3
            tid_bits = [16, 32, 64, None][payload]
            packets.append({"type": "STREAM_START", "tid_bits": tid_bits})
            offset += 2
            
        elif packet_type == "STREAM_END":
            packets.append({"type": "STREAM_END"})
            offset += 2
            break
            
        else:
            packet, size = parse_packet(data, offset, packet_type, tid_bits)
            packets.append(packet)
            offset += size
    
    return packets
```

---

## 11. 버전 히스토리

| 버전 | 날짜 | 변경 |
|------|------|------|
| v0.1 | 2026-01-30 | 초안: 스트림 구조, TID 할당 원칙, 패킷 순서 |
| v0.2 | 2026-01-30 | Meta Node 헥스 값 추가, TID 위치 표 완성, 구현 가이드 추가 |

---

## 12. TODO

- [ ] 스트림 압축 방안 (LZ4, Snappy 등)
- [ ] 스트림 분할/병합 규칙 (청크 단위)
- [ ] 스트림 간 참조 메커니즘 (Import/Export)
- [ ] 스트림 서명/검증 (무결성)
- [ ] 스트리밍 모드 (부분 전송)

---

## 13. 관련 문서

| 문서 | 내용 |
|------|------|
| `SIDX.md` | Prefix 체계, 바이트 오더 |
| `Meta_Node.md` | STREAM_START/END, 메타데이터 |
| `Entity_Node.md` | Entity TID 위치 |
| `Quantity_Node.md` | Quantity TID 위치 |
| `Verb_Edge.md` | Verb/Tiny Verb TID 위치 |
| `Triple_Edge.md` | Triple TID 위치 |
| `Event6_Edge.md` | Event6 TID 위치 |
| `Clause_Edge.md` | Clause TID 위치 |
| `Context_Edge.md` | Context TID 위치 |
| `Group_Edge.md` | Group TID 위치 |
| `Faber_Edge.md` | Faber TID 위치 |

---

**문서 종료**
