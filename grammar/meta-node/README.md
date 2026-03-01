# Meta Node 명세서

**버전:** v0.1  
**작성일:** 2026-01-30  
**목적:** GEUL 스트림 메타정보 표현을 위한 Meta Node 구조 정의

---

## 1. 개요

Meta Node는 **GEUL 스트림의 메타정보**를 표현하는 제어용 Node 타입이다.

**핵심 특징:**
- **스트림 제어:** 시작, 종료, TID 설정
- **메타데이터:** 생성시간, 수정시간, 생성자, 버전
- **1워드 헤더:** Type + Payload로 간결한 구조
- **가변 확장:** Type에 따라 추가 워드

**용도:**
- 스트림 경계 표시 (시작/종료)
- TID 비트폭 선언
- 스트림 출처 및 버전 관리
- 시간 메타데이터

---

## 2. Prefix

`SIDX.md` 참조

| 항목 | 값 |
|------|-----|
| Standard | `001 000 111` (9비트) |
| Proposal | `0001 000 111` (10비트) |
| 1st 워드 나머지 | 6비트 (Type 4 + Payload 2) |

**설계 근거:** 10비트 통일 영역의 3비트 분기에서 `111`(최상위)을 배정. 스트림 제어 메타정보는 모든 패킷에 선행하므로 최우선 코드를 부여한다.

---

## 3. 패킷 구조

### 3.1 1st 워드 (공통)

```
1st WORD (16비트)
┌───────────────────┬──────────┬─────────┐
│      Prefix       │   Type   │ Payload │
│      10비트       │   4비트   │  2비트  │
└───────────────────┴──────────┴─────────┘
  [0001 000 111]      [TTTT]     [PP]
```

### 3.2 필드 설명

| 필드 | 비트 | 설명 |
|------|------|------|
| Prefix | 10 | `0001 000 111` |
| Type | 4 | Meta Node 타입 (0~15) |
| Payload | 2 | 타입별 파라미터 |

---

## 4. Type 정의 (4비트 = 16개)

### 4.1 Type 할당 표

| Type | 이름 | Payload 용도 | 확장 워드 |
|------|------|--------------|-----------|
| 0000 | STREAM_START | TID 폭 | 없음 |
| 0001 | STREAM_END | 미사용 | 없음 |
| 0010 | CREATED_AT | 시간 폭 | 2 또는 4 |
| 0011 | MODIFIED_AT | 시간 폭 | 2 또는 4 |
| 0100 | CREATOR | 표기방법 | 0 또는 4 |
| 0101 | VERSION | 버전 폭 | 1, 2, 또는 4 |
| 0110 | RESERVED | - | - |
| 0111 | RESERVED | - | - |
| 1000 | RESERVED | - | - |
| 1001 | RESERVED | - | - |
| 1010 | RESERVED | - | - |
| 1011 | RESERVED | - | - |
| 1100 | RESERVED | - | - |
| 1101 | RESERVED | - | - |
| 1110 | RESERVED | - | - |
| 1111 | RESERVED | - | - |

**사용:** 6개 / **예약:** 10개

---

## 5. Type별 상세

### 5.1 STREAM_START (Type = 0000)

스트림의 시작을 표시하고 TID 비트폭을 선언한다.

#### 구조

```
1st WORD: [Prefix 10] + [0000] + [PP]
```

#### Payload (TID 폭)

| Payload | TID 폭 | TID 범위 | 용도 |
|---------|--------|----------|------|
| 00 | 1워드 (16비트) | 0~65,535 | 일반 스트림 |
| 01 | 2워드 (32비트) | 0~4.2B | 대규모 스트림 |
| 10 | 4워드 (64비트) | 무제한 | 초대규모 |
| 11 | 확장 | 예약 | 미래 확장 |

#### 규칙

- **필수:** 모든 GEUL 스트림은 STREAM_START로 시작해야 함
- **기본값:** Payload `00` (16비트 TID) 권장
- **영향 범위:** 이후 모든 TID 참조에 적용

#### 예시

```
16비트 TID 스트림 시작:
  [0001 000 111] [0000] [00] = 0x11C0

32비트 TID 스트림 시작:
  [0001 000 111] [0000] [01] = 0x11C1
```

---

### 5.2 STREAM_END (Type = 0001)

스트림의 종료를 표시한다.

#### 구조

```
1st WORD: [Prefix 10] + [0001] + [00]
```

#### Payload

미사용. `00`으로 고정.

#### 규칙

- **선택:** 스트림 끝에 명시적 종료 표시
- **용도:** 스트림 경계 명확화, 파싱 완료 확인

#### 예시

```
스트림 종료:
  [0001 000 111] [0001] [00] = 0x11C4
```

---

### 5.3 CREATED_AT (Type = 0010)

스트림 생성 시간을 표시한다.

#### 구조

```
1st WORD: [Prefix 10] + [0010] + [PP]
2nd~3rd (또는 5th) WORD: Unix timestamp
```

#### Payload (시간 폭)

| Payload | 확장 워드 | 범위 |
|---------|-----------|------|
| 00 | 2워드 (32비트) | 1970~2106년 |
| 01 | 4워드 (64비트) | 사실상 무제한 |
| 10 | 예약 | - |
| 11 | 예약 | - |

#### 시간 형식

- **단위:** 초 (Unix timestamp)
- **기준:** 1970-01-01 00:00:00 UTC
- **바이트 오더:** Big Endian

#### 예시

```
2026-01-30 12:00:00 UTC (32비트):
  Unix timestamp = 1769774400 = 0x6978C900
  
  1st: [0001 000 111] [0010] [00] = 0x11C8
  2nd: [0x6978]
  3rd: [0xC900]

총: 3워드
```

---

### 5.4 MODIFIED_AT (Type = 0011)

스트림 수정 시간을 표시한다.

#### 구조

CREATED_AT과 동일.

```
1st WORD: [Prefix 10] + [0011] + [PP]
2nd~3rd (또는 5th) WORD: Unix timestamp
```

#### Payload

CREATED_AT과 동일.

| Payload | 확장 워드 |
|---------|-----------|
| 00 | 2워드 (32비트) |
| 01 | 4워드 (64비트) |
| 10 | 예약 |
| 11 | 예약 |

---

### 5.5 CREATOR (Type = 0100)

스트림 생성자를 표시한다.

#### 구조

```
Payload=00: 1st WORD만 (생성자 미상)
Payload=01: 1st WORD + 4워드 (EntityNode)
```

#### Payload (표기방법)

| Payload | 표기방법 | 확장 워드 |
|---------|----------|-----------|
| 00 | 생성자 미상 | 없음 |
| 01 | EntityNode 정식 (TID 없음) | 4워드 |
| 10 | 예약 | - |
| 11 | 예약 | - |

#### EntityNode 정식 (TID 없음) 구조 (Payload=01)

Entity_Node.md 정식 구조에서 TID 워드 제외:

```
2nd WORD: [Prefix 7] + [Lane 1] + [EntityType 8]
3rd WORD: LocalUID 상위 16비트
4th WORD: LocalUID 하위 16비트
5th WORD: [SG 4] + [Q-ID 12비트]
```

#### 예시

```
생성자 미상:
  1st: [0001 000 111] [0100] [00] = 0x11D0

총: 1워드

생성자: Wikidata Q5 (human):
  1st: [0001 000 111] [0100] [01] = 0x11D1
  2nd: Entity Prefix + Type
  3rd: LocalUID 상위
  4th: LocalUID 하위
  5th: SG + Q-ID

총: 5워드
```

---

### 5.6 VERSION (Type = 0101)

스트림 버전 정보를 표시한다.

#### 구조

```
1st WORD: [Prefix 10] + [0101] + [PP]
2nd+ WORD: 버전 정보
```

#### Payload (버전 폭)

| Payload | 확장 워드 | 용도 |
|---------|-----------|------|
| 00 | 1워드 | 단순 버전 (예: 0x0100 = v1.0) |
| 01 | 2워드 | 확장 버전 |
| 10 | 4워드 | 상세 버전 |
| 11 | 확장 | 예약 |

#### 버전 형식 (1워드 기준)

```
VERSION WORD (16비트)
┌──────────┬──────────┐
│  Major   │  Minor   │
│  8비트   │  8비트   │
└──────────┴──────────┘
```

- `0x0100` = v1.0
- `0x0201` = v2.1
- `0x0A05` = v10.5

#### 예시

```
버전 v1.0:
  1st: [0001 000 111] [0101] [00] = 0x11D4
  2nd: [0x0100]

총: 2워드
```

---

## 6. 스트림 구조 예시

### 6.1 최소 스트림

```
[STREAM_START]     - 1워드
[... 패킷들 ...]   - N워드
[STREAM_END]       - 1워드 (선택)
```

### 6.2 메타데이터 포함 스트림

```
[STREAM_START]     - 1워드 (TID 폭 선언)
[VERSION]          - 2워드
[CREATED_AT]       - 3워드
[CREATOR]          - 5워드
[... 패킷들 ...]   - N워드
[MODIFIED_AT]      - 3워드 (선택)
[STREAM_END]       - 1워드
```

### 6.3 전체 예시

```
"Apple이 Tesla를 인수했다" 스트림:

1. STREAM_START (TID 16비트)
   0x11C0

2. VERSION (v1.0)
   0x11D4, 0x0100

3. CREATED_AT (2026-01-30)
   0x11C8, 0x6978, 0xC900

4. Entity Node: Apple (TID=0x0001)
   [Entity 패킷...]

5. Entity Node: Tesla (TID=0x0002)
   [Entity 패킷...]

6. Verb Edge: acquire (TID=0x0100)
   [Verb 패킷...]

7. Event6 Edge: (Apple, acquire, Tesla)
   [Event6 패킷...]

8. STREAM_END
   0x11C4
```

---

## 7. 파싱

```python
def parse_meta_node(data: bytes) -> dict:
    word1 = int.from_bytes(data[0:2], 'big')
    
    # Prefix 확인
    prefix = word1 >> 6
    assert prefix == 0b0001000111, "Not Meta Node"
    
    # Type, Payload 추출
    type_code = (word1 >> 2) & 0xF
    payload = word1 & 0x3
    
    TYPE_NAMES = {
        0: "STREAM_START",
        1: "STREAM_END",
        2: "CREATED_AT",
        3: "MODIFIED_AT",
        4: "CREATOR",
        5: "VERSION"
    }
    
    result = {
        "type": TYPE_NAMES.get(type_code, f"RESERVED_{type_code}"),
        "type_code": type_code,
        "payload": payload
    }
    
    # Type별 추가 파싱
    if type_code == 0:  # STREAM_START
        tid_width = [16, 32, 64, None][payload]
        result["tid_bits"] = tid_width
        result["words"] = 1
        
    elif type_code == 1:  # STREAM_END
        result["words"] = 1
        
    elif type_code in (2, 3):  # CREATED_AT, MODIFIED_AT
        if payload == 0:
            ts = int.from_bytes(data[2:6], 'big')
            result["timestamp"] = ts
            result["words"] = 3
        elif payload == 1:
            ts = int.from_bytes(data[2:10], 'big')
            result["timestamp"] = ts
            result["words"] = 5
            
    elif type_code == 4:  # CREATOR
        result["words"] = 5  # 1 + 4 (EntityNode without TID)
        # EntityNode 파싱은 별도 함수로
        
    elif type_code == 5:  # VERSION
        ext_words = [1, 2, 4, None][payload]
        if ext_words:
            result["version_data"] = data[2:2+ext_words*2]
            result["words"] = 1 + ext_words
    
    return result
```

---

## 8. 인코딩

```python
def encode_stream_start(tid_bits: int = 16) -> bytes:
    """STREAM_START 인코딩"""
    payload = {16: 0, 32: 1, 64: 2}[tid_bits]
    word1 = (0b0001000111 << 6) | (0 << 2) | payload
    return word1.to_bytes(2, 'big')

def encode_stream_end() -> bytes:
    """STREAM_END 인코딩"""
    word1 = (0b0001000111 << 6) | (1 << 2) | 0
    return word1.to_bytes(2, 'big')

def encode_created_at(timestamp: int, bits: int = 32) -> bytes:
    """CREATED_AT 인코딩"""
    payload = 0 if bits == 32 else 1
    word1 = (0b0001000111 << 6) | (2 << 2) | payload
    
    result = word1.to_bytes(2, 'big')
    result += timestamp.to_bytes(bits // 8, 'big')
    return result

def encode_version(major: int, minor: int) -> bytes:
    """VERSION 인코딩 (1워드 버전)"""
    word1 = (0b0001000111 << 6) | (5 << 2) | 0
    word2 = (major << 8) | minor
    
    return word1.to_bytes(2, 'big') + word2.to_bytes(2, 'big')
```

---

## 9. 설계 근거

### 9.1 Prefix `001 000 111` / `0001 000 111` 선택 이유

- **최우선 코드:** 10비트 통일 영역의 3비트 분기에서 `111`(최상위) 배정
- **파싱 우선순위:** 모든 스트림은 STREAM_START로 시작하므로 가장 먼저 만남
- **제어와 내용 분리:** 가장 높은 코드로 제어 패킷을 구분

### 9.2 Type 4비트 선택 이유

- **확장성:** 16개 타입으로 충분한 여유
- **현재 6개 사용**, 10개 예약
- **Payload 2비트**와 균형

### 9.3 TID 가변 폭 지원 이유

- **효율성:** 작은 스트림은 16비트로 충분
- **확장성:** 대규모 스트림은 32/64비트 필요
- **선언적:** 스트림 시작 시 명시적 선언

---

## 10. GEUL 생태계 내 위치

```
GEUL 패킷 체계:

제어 (Meta):
└── Meta Node ← 이 문서
        │
        ├── 스트림 시작/종료
        ├── TID 설정
        └── 메타데이터

지식/개체:
├── Entity Node
├── Triple Edge
└── Quantity Node

서술/사건:
├── Verb Edge
├── Event6 Edge
└── Clause Edge

맥락:
└── Context Edge

코드:
└── Faber Edge
```

---

## 11. 버전 히스토리

| 버전 | 날짜 | 변경 |
|------|------|------|
| v0.1 | 2026-01-30 | 초안: 6개 Type 정의, 가변 TID 지원 |

---

## 12. TODO

- [ ] CREATOR EntityNode 4워드 구조 상세화
- [ ] CHECKSUM Type 추가 검토
- [ ] 64비트 시간 필요 케이스 정의
- [ ] 스트림 병합/분할 규칙

---

**문서 종료**