# GEUL Grammar Specification

**버전:** v0.11
**작성일:** 2026-01-31
**범위:** SIDX 64비트 최상위 구조 및 패킷 타입 분기
**비트 규칙:** bit1 = MSB, bit64 = LSB
**바이트 오더:** Big Endian (Network Byte Order)
**문서 성격:** 권고안 (Recommendation)

> 이 문서는 개인 연구자의 초안이며, 완성된 표준이 아니다.
> 모든 "~한다" 표현은 권고로 해석한다.

---

## 0. 설계 원칙

1. **장기 확장성:** 예약 비트를 임시 용도로 전용하지 않는다. 미래 세대가 사용할 공간을 보존한다.
2. **의미의 영속성:** 한 번 정의된 비트 패턴의 의미는 변경하지 않는다. 새 의미가 필요하면 새 패턴을 할당한다.
3. **하위 호환:** 어떤 버전의 GEUL도 모든 이전 버전을 완전히 해석할 수 있어야 한다.
4. **선형 복잡도:** GEUL 심볼릭 처리는 길이에 대해 O(n)을 유지한다. SIDX 최대 길이를 고정하지 않으며 확장 메커니즘을 통해 임의 길이를 허용한다.

---

## 1. 개요

SIDX(Semantic-aligned Index)는 64비트 전역 의미 식별자이다.

### 1.1 비트 설계 원칙

```
1     → 먼 미래 (1순위)
01    → 미래 (2순위)
001   → 표준 (3순위)
000   → 자유 (나머지)
```

### 1.2 최상위 Prefix

| Prefix | 영역 | 비율 | 용도 |
|--------|------|------|------|
| `1` | Far Future | 50% | 먼 미래를 위한 예약 |
| `01` | Future | 25% | 가까운 미래를 위한 예약 |
| `001` | Standard | 12.5% | 공식 표준 영역 |
| `000` | Free | 12.5% | 완전 자유 |

`0001`은 자유 영역(000) 내에서 본 제안이 사용하는 관례적 공간이다.
표준이 제정되면 덮어쓰여질 수 있다.

---

## 2. 비트 분기 구조

### 2.1 영역 분기 (bit1~3)

```
bit1
├─ 1: Far Future ─────────── 50% 예약 권고
│
└─ 0
    └─ bit2
        ├─ 1 (01): Future ── 25% 예약 권고
        │
        └─ 0
            └─ bit3
                ├─ 1 (001): Standard
                │
                └─ 0 (000): Free
                      └─ 0001: Proposal (본 제안)
```

### 2.2 Standard 내부 분기 권고 (Prefix = 001)

표준이 제정될 때 다음 구조를 권고한다:

| Prefix | 비트 | 타입 | 빈도 |
|--------|------|------|------|
| `001 1` | 4 | Tiny Verb Edge | 최고빈도 |
| `001 01` | 5 | Verb Edge | 고빈도 |
| `001 001` | 6 | Entity Node | 고빈도 |
| `001 000 111` | 9 | Meta Node | 스트림 제어 |
| `001 000 110` | 9 | Triple Edge | 중빈도 |
| `001 000 101` | 9 | Clause Edge | 저빈도 |
| `001 000 100` | 9 | Event6 Edge | 저빈도 |
| `001 000 011` | 9 | Context Edge | 저빈도 |
| `001 000 010` | 9 | Quantity Node | 중빈도 |
| `001 000 001` | 9 | Faber Edge | 코드/AST |
| `001 000 000` | 9 | 확장 | - |

### 2.3 Proposal 내부 분기 (Prefix = 0001)

본 제안이 자유 영역 내에서 관례적으로 사용하는 구조:

| Prefix | 비트 | 타입 |
|--------|------|------|
| `0001 1` | 5 | Tiny Verb Edge |
| `0001 01` | 6 | Verb Edge |
| `0001 001` | 7 | Entity Node |
| `0001 000 111` | 10 | Meta Node |
| `0001 000 110` | 10 | Triple Edge |
| `0001 000 101` | 10 | Clause Edge |
| `0001 000 100` | 10 | Event6 Edge |
| `0001 000 011` | 10 | Context Edge |
| `0001 000 010` | 10 | Quantity Node |
| `0001 000 001` | 10 | Faber Edge |
| `0001 000 000` | 10 | 확장 |

10비트 통일 영역의 3비트 분기(8슬롯)가 모두 소진되었으므로, 이후 추가 타입은
`0001 000 000` 확장 슬롯 하위에 3비트를 추가하여 13비트로 배정한다:

| Prefix | 비트 | 타입 |
|--------|------|------|
| `0001 000 000 000` | 13 | Group Edge |
| `0001 000 000 001`~`110` | 13 | 예약 |
| `0001 000 000 111` | 13 | 2차 확장 |

---

## 3. 전체 분기 트리

```
bit1
├─ 1: Far Future
│
└─ 0
    └─ bit2
        ├─ 1 (01): Future
        │
        └─ 0
            └─ bit3
                ├─ 1 (001): Standard
                │     └─ bit4~
                │         ├─ 1           (001 1)        → Tiny Verb Edge
                │         ├─ 01          (001 01)       → Verb Edge
                │         ├─ 001         (001 001)      → Entity Node
                │         └─ 000         (001 000)      → 9비트 통일 영역
                │               └─ bit7~9 (3비트)
                │                   ├─ 111 → Meta Node
                │                   ├─ 110 → Triple Edge
                │                   ├─ 101 → Clause Edge
                │                   ├─ 100 → Event6 Edge
                │                   ├─ 011 → Context Edge
                │                   ├─ 010 → Quantity Node
                │                   ├─ 001 → Faber Edge
                │                   └─ 000 → 확장
                │
                └─ 0 (000): Free
                      └─ 0001: Proposal (Standard 미러링)
```

---

## 4. 영역별 상세

| 영역 | Prefix | 비율 | 용도 | 현재 상태 |
|------|--------|------|------|-----------|
| Far Future | `1` | 50% (2^63개) | 먼 미래 예약 | 미사용 권고 |
| Future | `01` | 25% (2^62개) | 가까운 미래 예약 | 미사용 권고 |
| Standard | `001` | 12.5% (2^61개) | 공식 표준 | 표준 제정 시 사용 |
| Free | `000` | 12.5% (2^61개) | 실험, 사적 사용 | 제한 없음 |
| Proposal | `0001` | 6.25% | 본 제안의 관례적 공간 | Free 내, 보호 없음 |

---

## 5. 패킷 타입

### 외부 레포 (별도 코드북 보유)

| 타입 | Prefix (Proposal) | 워드 | 명세 | 설명 |
|------|-------------------|------|------|------|
| Tiny Verb Edge | `0001 1` | 2 | [geul-verb](https://github.com/park-jun-woo/geul-verb) | 고빈도 단순 서술 |
| Verb Edge | `0001 01` | 3~5 | [geul-verb](https://github.com/park-jun-woo/geul-verb) | 559 루트 → 13,767 WordNet 동사, 16비트 코드북 |
| Entity Node | `0001 001` | 3~5 | [geul-entity](https://github.com/park-jun-woo/geul-entity) | 64 EntityType, 48비트 속성, Wikidata 108.8M 개체 |
| Quantity Node | `0001 000 010` | 4~7 | [geul-quantities](https://github.com/park-jun-woo/geul-quantities) | 64 단위 코드, SI/통화/타임스탬프 |
| Faber Edge | `0001 000 001` | 3+ | [geul-ast](https://github.com/park-jun-woo/geul-ast) | 64 프로그래밍 언어, 256 AST 노드 타입 |

### 모노레포 모듈

| 타입 | Prefix (Proposal) | 워드 | 명세 | 설명 |
|------|-------------------|------|------|------|
| Triple Edge | `0001 000 110` | 4~5 | [triple-edge/](triple-edge/) | 속성/관계, Top63 + 확장 |
| Clause Edge | `0001 000 101` | 4 | [clause-edge/](clause-edge/) | RST 기반 담화/논리 16관계 |
| Event6 Edge | `0001 000 100` | 3~8 | [event6-edge/](event6-edge/) | 6하원칙 사건 |
| Context Edge | `0001 000 011` | 3 | [context-edge/](context-edge/) | 세계관/맥락 64타입 |
| Meta Node | `0001 000 111` | 1~5 | [meta-node/](meta-node/) | 스트림 제어 6타입 |
| Group Edge | `0001 000 000 111` | 4+ | [group-edge/](group-edge/) | 집합/그룹 7타입 (AND/OR/XOR/LIST/SET/RANGE/PAIR) |

### 공통 명세

- [stream-format.md](stream-format.md) -- 스트림 포맷 규칙, TID 스코핑, 패킷 순서
- 참여자 역할 (16개 Semantic Role) → [geul-verb/docs/participants.md](https://github.com/park-jun-woo/geul-verb)

---

## 6. 인코딩 규칙

### 6.1 바이트 오더

| 항목 | 규칙 |
|------|------|
| 바이트 오더 | Big Endian |
| 비트 오더 | MSB First (bit1 = MSB) |
| 워드 크기 | 16비트 (2바이트) |

```
16비트 값 0x1234:   메모리: [0x12] [0x34]
64비트 값 0x123456789ABCDEF0:   메모리: [0x12] [0x34] [0x56] [0x78] [0x9A] [0xBC] [0xDE] [0xF0]
```

### 6.2 워드 정렬

- 모든 필드는 16비트 워드 경계에 정렬
- 패킷 크기는 항상 워드 단위 (2바이트 배수)
- 패딩 필요 시 0x00으로 채움

---

## 7. 구현

### 7.1 영역 파서

```python
def parse_sidx_region(sidx: int) -> str:
    if (sidx >> 63) & 1:
        return "Far Future"
    if (sidx >> 62) & 1:
        return "Future"
    if (sidx >> 61) & 1:
        return "Standard"
    return "Free"
```

### 7.2 Proposal 타입 파서

```python
def parse_proposal_type(sidx: int) -> str:
    """Prefix=0001 확인 후 호출"""
    if (sidx >> 59) & 1:
        return "Tiny Verb Edge"
    if (sidx >> 58) & 1:
        return "Verb Edge"
    if (sidx >> 57) & 1:
        return "Entity Node"

    sub = (sidx >> 54) & 0x7
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

---

## 8. 표준이 정할 것들

본 문서는 다음 사항을 정하지 않는다:

| 항목 | 설명 |
|------|------|
| Issuer 구조 | 등록기관 네임스페이스 규칙 |
| Standard 내부 세부 | 타입별 상세 비트 배치 |
| 버전 관리 | 하위 호환성 규칙 |
| 거버넌스 | 표준 제정/수정 절차 |

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
| v0.10 | 2026-01-31 | Prefix 전면 재설계, 설계 헌장 추가 |
| v0.11 | 2026-01-31 | 구조 단순화, 권고 톤으로 전환 |
