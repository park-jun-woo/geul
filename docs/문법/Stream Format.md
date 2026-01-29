# Stream Format 명세서

**버전:** v0.1  
**작성일:** 2026-01-30  
**목적:** GEUL 패킷들의 스트림 구성 규칙 정의

---

## 1. 개요

GEUL 스트림은 **Meta Node로 시작하고 끝나는 패킷 시퀀스**이다.

**핵심 특징:**
- **경계 명시:** STREAM_START / STREAM_END
- **TID 스코프:** 스트림 내에서만 유효
- **순방향 참조:** 선언된 TID만 참조 가능
- **Big Endian:** Network Byte Order

**스트림 = 하나의 완결된 GEUL 문서**

---

## 2. 스트림 구조

### 2.1 기본 형식

```
┌─────────────────────────────────────┐
│          STREAM_START               │  ← 필수
│          (TID 폭 선언)               │
├─────────────────────────────────────┤
│          메타데이터 (선택)            │
│          - VERSION                  │
│          - CREATED_AT               │
│          - CREATOR                  │
├─────────────────────────────────────┤
│          패킷들                      │
│          - Entity Node              │
│          - Quantity Node            │
│          - Verb Edge                │
│          - Triple Edge              │
│          - Event6 Edge              │
│          - Clause Edge              │
│          - Context Edge             │
│          - Group Edge               │
│          - Faber Edge               │
├─────────────────────────────────────┤
│          STREAM_END                 │  ← 선택 (권장)
└─────────────────────────────────────┘
```

### 2.2 최소 스트림

```
[STREAM_START]     - 1워드
[STREAM_END]       - 1워드

총: 2워드 (4바이트)
```

빈 스트림도 유효함.

### 2.3 일반 스트림

```
[STREAM_START]     - 1워드 (TID 16비트)
[Entity Node]      - N워드
[Entity Node]      - N워드
[Verb Edge]        - N워드
[STREAM_END]       - 1워드
```

---

## 3. TID 할당 원칙

### 3.1 기본 규칙

| 규칙 | 설명 |
|------|------|
| **필수성** | 스트림 내 모든 Edge/Node는 TID를 가진다 |
| **유일성** | 스트림 내에서 TID는 유일하다 |
| **스코프** | TID는 해당 스트림 내에서만 유효하다 |
| **순방향** | 참조 시점에 이미 선언된 TID만 참조 가능 |

### 3.2 TID 위치

**원칙:** TID 선언은 참조 나열보다 앞에 위치한다.

| 타입 | TID 위치 | 참조 위치 | 비고 |
|------|----------|-----------|------|
| Entity Node | 마지막 워드 | 없음 | 참조 없음 |
| Quantity Node | 마지막 워드 | 없음 | 참조 없음 |
| Verb Edge | Header 영역 | Payload 이후 | 참여자 TID |
| Triple Edge | Header 영역 | Payload 이후 | S, P, O TID |
| Event6 Edge | Header 영역 | Payload 이후 | 6하원칙 TID |
| Clause Edge | Header 영역 | Payload 이후 | 절 TID |
| Context Edge | Header 영역 | Payload 이후 | 대상 TID |
| Group Edge | 2nd 워드 | 3rd+ 워드 | 멤버 TID |
| Faber Edge | 3rd 워드 | 4th+ 워드 | 자식 TID |

**Node vs Edge:**
- **Node:** 자기 자신만 정의 (참조 없음) → TID 마지막
- **Edge:** 다른 TID 참조 → TID가 참조보다 앞

### 3.3 TID 할당 전략

| 전략 | 설명 | 예시 |
|------|------|------|
| 순차 할당 | 0x0001부터 순차 증가 | 0x0001, 0x0002, 0x0003... |
| 영역 분리 | 타입별 범위 지정 | Node: 0x0001~0x7FFF, Edge: 0x8000~0xFFFF |
| 해시 기반 | 내용 해시의 하위 비트 | 충돌 시 재할당 |

**권장:** 순차 할당 (단순, 예측 가능)

### 3.4 TID 폭

STREAM_START의 Payload로 선언:

| Payload | TID 폭 | 범위 | 용도 |
|---------|--------|------|------|
| 00 | 16비트 | 0~65,535 | 일반 스트림 |
| 01 | 32비트 | 0~4.2B | 대규모 스트림 |
| 10 | 64비트 | 무제한 | 초대규모 |

**기본값:** 16비트 (대부분 충분)

### 3.5 예약 TID

| TID | 용도 |
|-----|------|
| 0x0000 | **종결 마커** (Group/Faber Edge) |
| 0xFFFF | 예약 (16비트 기준) |

---

## 4. 패킷 순서 규칙

### 4.1 선언-참조 순서

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

### 4.2 권장 순서

```
1. STREAM_START
2. 메타데이터 (VERSION, CREATED_AT, CREATOR)
3. Entity Node들 (개체 선언)
4. Quantity Node들 (수량/리터럴)
5. Group Edge들 (그룹 정의)
6. Verb Edge들 (서술)
7. Triple Edge들 (속성/관계)
8. Event6 Edge들 (사건)
9. Clause Edge들 (담화 관계)
10. Context Edge들 (맥락)
11. STREAM_END
```

**참고:** 권장 순서일 뿐, 선언-참조 규칙만 지키면 자유

### 4.3 순환 참조

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

## 5. 바이트 오더

`SIDX.md` 참조

| 항목 | 규칙 |
|------|------|
| 바이트 오더 | **Big Endian** (Network Byte Order) |
| 비트 오더 | MSB First (bit1 = MSB) |
| 워드 크기 | 16비트 (2바이트) |

---

## 6. 스트림 예시

### 6.1 "철수가 영희를 만났다"

```
1. STREAM_START (TID 16비트)
   0xC000

2. Entity: 철수 (TID=0x0001)
   [Entity 패킷...]
   
3. Entity: 영희 (TID=0x0002)
   [Entity 패킷...]

4. Verb Edge: meet (TID=0x0100)
   Subject: 0x0001
   Object: 0x0002
   [Verb 패킷...]

5. STREAM_END
   0xC004
```

### 6.2 "철수와 영희가 학교에서 만났다"

```
1. STREAM_START
   0xC000

2. Entity: 철수 (TID=0x0001)
3. Entity: 영희 (TID=0x0002)
4. Entity: 학교 (TID=0x0003)

5. Group Edge: AND (TID=0x0010)
   멤버: 0x0001, 0x0002

6. Verb Edge: meet (TID=0x0100)
   Subject: 0x0010 (그룹)
   Location: 0x0003

7. STREAM_END
   0xC004
```

### 6.3 메타데이터 포함 스트림

```
1. STREAM_START (TID 16비트)
   0xC000

2. VERSION (v1.0)
   0xC014, 0x0100

3. CREATED_AT (2026-01-30)
   0xC008, 0x6978, 0xC900

4. CREATOR (생성자 미상)
   0xC010

5. Entity: Apple (TID=0x0001)
6. Entity: Tesla (TID=0x0002)

7. Verb Edge: acquire (TID=0x0100)
   Subject: 0x0001
   Object: 0x0002

8. STREAM_END
   0xC004
```

---

## 7. 스트림 검증

### 7.1 필수 검증

| 항목 | 검증 |
|------|------|
| 시작 | STREAM_START로 시작하는가? |
| TID 유일성 | 중복 TID가 없는가? |
| 참조 유효성 | 참조된 TID가 모두 선언되었는가? |
| 순방향 | 참조 시점에 TID가 이미 선언되었는가? |

### 7.2 선택 검증

| 항목 | 검증 |
|------|------|
| 종료 | STREAM_END로 끝나는가? |
| 메타데이터 | VERSION이 있는가? |
| 완결성 | 모든 참조가 해결되는가? |

---

## 8. 다중 스트림

### 8.1 연결 (Concatenation)

```
[Stream A: STREAM_START ~ STREAM_END]
[Stream B: STREAM_START ~ STREAM_END]
```

- 각 스트림은 독립적
- TID 스코프는 스트림별로 분리
- Stream A의 TID=0x0001과 Stream B의 TID=0x0001은 다른 개체

### 8.2 참조 (Cross-reference)

**스트림 간 참조는 현재 미지원**

향후 확장:
- 스트림 ID 도입
- 글로벌 TID 체계
- Import/Export 메커니즘

---

## 9. 버전 히스토리

| 버전 | 날짜 | 변경 |
|------|------|------|
| v0.1 | 2026-01-30 | 초안: 스트림 구조, TID 할당 원칙, 패킷 순서 |

---

## 10. TODO

- [ ] 스트림 압축 방안
- [ ] 스트림 분할/병합 규칙
- [ ] 스트림 간 참조 메커니즘
- [ ] 스트림 서명/검증

---

## 11. 관련 문서

| 문서 | 내용 |
|------|------|
| `SIDX.md` | Prefix 체계, 바이트 오더 |
| `Meta_Node.md` | STREAM_START/END, 메타데이터 |
| `Entity_Node.md` | Entity TID 위치 |
| `Quantity_Node.md` | Quantity TID 위치 |
| `Verb_Edge.md` | Verb TID 위치 |
| `Group_Edge.md` | Group TID 위치 |

---

**문서 종료**