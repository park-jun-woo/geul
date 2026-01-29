# Quantity Node 명세서

**버전:** v0.3  
**작성일:** 2026-01-30  
**목적:** GEUL 물리량/수치 표현을 위한 Quantity Node 패킷 구조 정의

---

## 1. 개요

Quantity Node는 **물리량, 수치, 화폐, 리터럴** 등을 표현하는 가변 길이 Node 타입이다.

**핵심 특징:**
- **가변 길이:** 4~N워드 (값 크기에 따라)
- **단위 명시:** SI 기본/유도 + 비SI (화폐, 시간 등)
- **스케일 지원:** 10의 거듭제곱으로 접두어 표현
- **특수 리터럴:** 시간(timestamp), 문자열(UTF-16), 색상(RGBA)
- **TID 마지막:** Node 특성 (Entity와 일관성)

**용도:**
- Triple Edge의 Object (높이, 무게, 가격 등)
- Verb Edge의 참여자 (수량 표현)
- Event6의 참여자 (금액, 거리 등)
- Entity의 이름/라벨 (UTF-16 문자열)
- 시간 표현 (Unix timestamp)

---

## 2. Prefix

`SIDX.md` 참조

| 항목 | 값 |
|------|-----|
| Standard | `0 000 101` (7비트) |
| Proposal | `1100 000 101` (10비트) |
| 1st 워드 나머지 | 6비트 (Unit) |

---

## 3. 패킷 구조

### 3.1 기본 구조

```
1st WORD (16비트)
┌────────────────────┬────────────────────┐
│      Prefix        │       Unit         │
│      10bit         │       6bit         │
└────────────────────┴────────────────────┘

2nd WORD (16비트)
┌──────┬──────┬──────┬────────────────────┐
│ Sign │ Size │ Type │      Scale         │
│ 1bit │ 2bit │ 1bit │       4bit         │
├──────┴──────┴──────┴────────────────────┤
│              Reserved (8bit)            │
└─────────────────────────────────────────┘

3rd+ WORD: Value (가변, Size에 따라 1/2/4워드)

Last WORD (16비트)
┌─────────────────────────────────────────┐
│                  TID                    │
│                 16bit                   │
└─────────────────────────────────────────┘
```

### 3.2 워드 수

| Size | Value 워드 | 총 워드 |
|------|------------|---------|
| 00 | 1 | 4 |
| 01 | 2 | 5 |
| 10 | 4 | 7 |
| 11 | Reserved | - |

---

## 4. 필드 상세

### 4.1 1st WORD

| 필드 | 비트 | 크기 | 설명 |
|------|------|------|------|
| Prefix | 1-10 | 10 | `1100 000 101` |
| Unit | 11-16 | 6 | 단위 코드 (64개) |

### 4.2 2nd WORD

| 필드 | 비트 | 크기 | 설명 |
|------|------|------|------|
| Sign | 1 | 1 | 0=양수/무부호, 1=음수 |
| Size | 2-3 | 2 | 값 크기 (00/01/10) |
| Type | 4 | 1 | 0=정수, 1=부동소수점 |
| Scale | 5-8 | 4 | 10의 거듭제곱 (-8 ~ +7) |
| Reserved | 9-16 | 8 | 예약 (0으로 채움) |

### 4.3 Value (가변)

| Size | 크기 | 정수 범위 | 부동소수점 |
|------|------|-----------|------------|
| 00 | 16비트 | 0~65,535 | float16 |
| 01 | 32비트 | 0~4.2×10⁹ | float32 |
| 10 | 64비트 | 0~1.8×10¹⁹ | float64 |

### 4.4 TID

항상 마지막 워드. Node 특성 유지 (Entity와 일관성).

---

## 5. Unit 코드 (6비트 = 64개)

### 5.1 SI 기본 단위 (0x00~0x06)

| 코드 | 단위 | 기호 | 물리량 |
|------|------|------|--------|
| 0x00 | meter | m | 길이 |
| 0x01 | kilogram | kg | 질량 |
| 0x02 | second | s | 시간 |
| 0x03 | ampere | A | 전류 |
| 0x04 | kelvin | K | 온도 |
| 0x05 | mole | mol | 물질량 |
| 0x06 | candela | cd | 광도 |

### 5.2 SI 유도 단위 (0x07~0x1C)

| 코드 | 단위 | 기호 | 물리량 |
|------|------|------|--------|
| 0x07 | hertz | Hz | 주파수 |
| 0x08 | newton | N | 힘 |
| 0x09 | pascal | Pa | 압력 |
| 0x0A | joule | J | 에너지 |
| 0x0B | watt | W | 일률 |
| 0x0C | coulomb | C | 전하량 |
| 0x0D | volt | V | 전압 |
| 0x0E | farad | F | 전기용량 |
| 0x0F | ohm | Ω | 저항 |
| 0x10 | siemens | S | 전도율 |
| 0x11 | weber | Wb | 자기선속 |
| 0x12 | tesla | T | 자기장 |
| 0x13 | henry | H | 인덕턴스 |
| 0x14 | celsius | °C | 온도 |
| 0x15 | lumen | lm | 광선속 |
| 0x16 | lux | lx | 조도 |
| 0x17 | becquerel | Bq | 방사능 |
| 0x18 | gray | Gy | 흡수선량 |
| 0x19 | sievert | Sv | 선량당량 |
| 0x1A | katal | kat | 촉매활성 |
| 0x1B | radian | rad | 평면각 |
| 0x1C | steradian | sr | 입체각 |

### 5.3 SI 예약 (0x1D~0x1F)

| 코드 | 용도 |
|------|------|
| 0x1D-0x1F | SI 확장 예약 |

### 5.4 비SI 단위 (0x20~0x2F)

| 코드 | 단위 | 용도 |
|------|------|------|
| 0x20 | CURRENCY | 화폐 (아래 확장 참조) |
| 0x21 | percent | % (비율) |
| 0x22 | degree | ° (각도) |
| 0x23 | minute_time | 분 (시간) |
| 0x24 | hour | 시 |
| 0x25 | day | 일 |
| 0x26 | week | 주 |
| 0x27 | month | 월 |
| 0x28 | year | 년 |
| 0x29 | bit | 정보량 |
| 0x2A | byte | 정보량 |
| 0x2B | COUNT | 개수 (무단위) |
| 0x2C | RATIO | 비율 (무차원) |
| 0x2D | SCORE | 점수 |
| 0x2E | RANK | 순위 |
| 0x2F | INDEX | 지수 |

### 5.5 특수 리터럴 (0x30~0x3F)

| 코드 | 타입 | Payload | 용도 |
|------|------|---------|------|
| 0x30 | TIMESTAMP_SEC | 2/4워드 | Unix timestamp (초) |
| 0x31 | TIMESTAMP_MS | 4워드 | Unix timestamp (밀리초) |
| 0x32 | UTF16 | 2 + N워드 | UTF-16 문자열 |
| 0x33 | RGBA | 2워드 | 색상 (32비트) |
| 0x34~0x3F | Reserved | - | 확장용 (12개) |

---

## 6. Scale (4비트)

10의 거듭제곱. 오프셋 8 적용 (-8 ~ +7).

| 코드 | 값 | 접두어 | 의미 |
|------|-----|--------|------|
| 0000 | 10⁻⁸ | - | 0.00000001 |
| 0001 | 10⁻⁷ | - | 0.0000001 |
| 0010 | 10⁻⁶ | μ (마이크로) | 0.000001 |
| 0011 | 10⁻⁵ | - | 0.00001 |
| 0100 | 10⁻⁴ | - | 0.0001 |
| 0101 | 10⁻³ | m (밀리) | 0.001 |
| 0110 | 10⁻² | c (센티) | 0.01 |
| 0111 | 10⁻¹ | d (데시) | 0.1 |
| **1000** | **10⁰** | **(기본)** | **1** |
| 1001 | 10¹ | da (데카) | 10 |
| 1010 | 10² | h (헥토) | 100 |
| 1011 | 10³ | k (킬로) | 1,000 |
| 1100 | 10⁴ | - | 10,000 |
| 1101 | 10⁵ | - | 100,000 |
| 1110 | 10⁶ | M (메가) | 1,000,000 |
| 1111 | 10⁷ | - | 10,000,000 |

**기본값:** `1000` (10⁰ = 1)

**계산:** `실제값 = Value × 10^(Scale - 8)`

---

## 7. 특수 리터럴 (Unit = 0x30~0x33)

특수 리터럴은 2nd WORD의 기존 필드(Sign/Size/Type/Scale)를 다르게 사용한다.

### 7.1 TIMESTAMP_SEC (Unit = 0x30)

Unix timestamp를 **초 단위**로 표현한다.

#### 구조

```
1st WORD: [Prefix 10bit] + [0x30]
2nd WORD: [Size 2bit] + [Reserved 14bit]
3rd+ WORD: Timestamp (Size에 따라 2/4워드)
Last WORD: TID
```

#### Size 필드

| Size | Payload | 범위 | 총 워드 |
|------|---------|------|---------|
| 01 | 2워드 (32비트) | 1970~2106년 | 5 |
| 10 | 4워드 (64비트) | 무제한 | 7 |

#### 예시: 2026-01-30 12:00:00 UTC

```
Unix timestamp = 1769774400 (32비트로 충분)

1st: [1100 000 101] + [110000] = Prefix + 0x30
2nd: [01] + [00...0] = Size 01 (32비트)
3rd: [0x6978] (상위)
4th: [0xC900] (하위)
5th: [TID]

총: 5워드
```

### 7.2 TIMESTAMP_MS (Unit = 0x31)

Unix timestamp를 **밀리초 단위**로 표현한다.

#### 구조

```
1st WORD: [Prefix 10bit] + [0x31]
2nd WORD: [Reserved 16bit]
3rd~6th WORD: Timestamp (64비트 고정)
Last WORD: TID
```

#### 설명

- 밀리초 정밀도는 64비트 필요 (32비트는 ~50일만 표현)
- 따라서 4워드 고정

#### 예시: 2026-01-30 12:00:00.123 UTC

```
Unix timestamp (ms) = 1769774400123

1st: [1100 000 101] + [110001] = Prefix + 0x31
2nd: [0x0000] (Reserved)
3rd: [0x0000] 
4th: [0x019C]
5th: [0x1B63]
6th: [0x887B]
7th: [TID]

총: 7워드
```

### 7.3 UTF16 (Unit = 0x32)

UTF-16 Big Endian 문자열을 표현한다.

#### 구조

```
1st WORD: [Prefix 10bit] + [0x32]
2nd WORD: Length 상위 16비트
3rd WORD: Length 하위 16비트
4th~(3+Length) WORD: UTF-16 BE 문자열
Last WORD: TID
```

#### Length

- 32비트 (2워드)
- 단위: **워드 수** (글자 수 ≈ 워드 수, BMP 기준)
- 최대: ~4.2B 워드 (약 8GB)

#### BMP vs Surrogate Pair

| 범위 | 워드 | 예시 |
|------|------|------|
| U+0000~FFFF (BMP) | 1워드/글자 | 한글, 영문, 한자 |
| U+10000+ (보조) | 2워드/글자 | 이모지 |

#### 예시: "철수"

```
"철" = U+CCA0, "수" = U+C218

1st: [1100 000 101] + [110010] = Prefix + 0x32
2nd: [0x0000] (Length 상위)
3rd: [0x0002] (Length 하위 = 2워드)
4th: [0xCCA0] ("철")
5th: [0xC218] ("수")
6th: [TID]

총: 6워드
```

#### 예시: "Hello"

```
"H"=0x0048, "e"=0x0065, "l"=0x006C, "l"=0x006C, "o"=0x006F

1st: [1100 000 101] + [110010] = Prefix + 0x32
2nd: [0x0000] (Length 상위)
3rd: [0x0005] (Length 하위 = 5워드)
4th: [0x0048] ("H")
5th: [0x0065] ("e")
6th: [0x006C] ("l")
7th: [0x006C] ("l")
8th: [0x006F] ("o")
9th: [TID]

총: 9워드
```

#### 예시: 이모지 "😀" (U+1F600)

```
U+1F600 → Surrogate Pair: 0xD83D 0xDE00

1st: [1100 000 101] + [110010] = Prefix + 0x32
2nd: [0x0000]
3rd: [0x0002] (Length = 2워드)
4th: [0xD83D] (High Surrogate)
5th: [0xDE00] (Low Surrogate)
6th: [TID]

총: 6워드
```

### 7.4 RGBA (Unit = 0x33)

32비트 RGBA 색상을 표현한다.

#### 구조

```
1st WORD: [Prefix 10bit] + [0x33]
2nd WORD: [R 8bit] + [G 8bit]
3rd WORD: [B 8bit] + [A 8bit]
4th WORD: TID
```

#### 필드

| 필드 | 비트 | 범위 |
|------|------|------|
| R (Red) | 8 | 0~255 |
| G (Green) | 8 | 0~255 |
| B (Blue) | 8 | 0~255 |
| A (Alpha) | 8 | 0~255 (0=투명, 255=불투명) |

#### 예시: 빨간색 (불투명)

```
R=255, G=0, B=0, A=255

1st: [1100 000 101] + [110011] = Prefix + 0x33
2nd: [0xFF00] (R=255, G=0)
3rd: [0x00FF] (B=0, A=255)
4th: [TID]

총: 4워드
```

#### 예시: 반투명 파란색

```
R=0, G=0, B=255, A=128

1st: [1100 000 101] + [110011] = Prefix + 0x33
2nd: [0x0000] (R=0, G=0)
3rd: [0xFF80] (B=255, A=128)
4th: [TID]

총: 4워드
```

---

## 8. 화폐 확장 (Unit = 0x20)

### 8.1 구조

화폐(CURRENCY)일 때 Reserved 8비트를 통화 코드로 사용.

```
2nd WORD (Unit = CURRENCY)
┌──────┬──────┬──────┬───────┬────────────────┐
│ Sign │ Size │ Type │ Scale │  Currency Code │
│ 1bit │ 2bit │ 1bit │  4bit │      8bit      │
└──────┴──────┴──────┴───────┴────────────────┘
```

### 8.2 통화 코드 (8비트 = 256개)

**주요 통화:**

| 코드 | 통화 | ISO |
|------|------|-----|
| 0x00 | 미국 달러 | USD |
| 0x01 | 유로 | EUR |
| 0x02 | 일본 엔 | JPY |
| 0x03 | 영국 파운드 | GBP |
| 0x04 | 중국 위안 | CNY |
| 0x05 | 한국 원 | KRW |
| 0x06 | 스위스 프랑 | CHF |
| 0x07 | 호주 달러 | AUD |
| 0x08 | 캐나다 달러 | CAD |
| 0x09 | 홍콩 달러 | HKD |
| 0x0A | 싱가포르 달러 | SGD |
| 0x0B | 인도 루피 | INR |
| 0x0C | 러시아 루블 | RUB |
| 0x0D | 브라질 헤알 | BRL |
| 0x0E | 멕시코 페소 | MXN |
| 0x0F | 대만 달러 | TWD |

**암호화폐:**

| 코드 | 통화 |
|------|------|
| 0x80 | Bitcoin (BTC) |
| 0x81 | Ethereum (ETH) |
| 0x82 | Tether (USDT) |
| 0x83-0x8F | 암호화폐 예약 |

**예약:**

| 코드 | 용도 |
|------|------|
| 0x10-0x7F | 기타 법정화폐 (112개) |
| 0x90-0xFE | 예약 |
| 0xFF | 사용자 정의 |

---

## 9. 파싱

### 9.1 워드 수 결정

```python
def get_quantity_words(data: bytes) -> int:
    word2 = int.from_bytes(data[2:4], 'big')
    size = (word2 >> 13) & 0x3  # bit 2-3
    
    if size == 0b00:
        return 4  # 1워드 Value
    elif size == 0b01:
        return 5  # 2워드 Value
    elif size == 0b10:
        return 7  # 4워드 Value
    else:
        raise ValueError("Reserved size")
```

### 9.2 전체 파싱

```python
def parse_quantity(data: bytes) -> dict:
    word1 = int.from_bytes(data[0:2], 'big')
    word2 = int.from_bytes(data[2:4], 'big')
    
    # 1st WORD
    prefix = word1 >> 6
    assert prefix == 0b1100000101, "Not Quantity Node"
    unit = word1 & 0x3F
    
    # 2nd WORD
    sign = (word2 >> 15) & 0x1
    size = (word2 >> 13) & 0x3
    vtype = (word2 >> 12) & 0x1
    scale = (word2 >> 8) & 0xF
    reserved = word2 & 0xFF
    
    # Value 크기 결정
    if size == 0b00:
        value_bytes = 2
        value_start = 4
    elif size == 0b01:
        value_bytes = 4
        value_start = 4
    elif size == 0b10:
        value_bytes = 8
        value_start = 4
    
    # Value 파싱
    value_raw = int.from_bytes(
        data[value_start:value_start+value_bytes], 'big'
    )
    
    # TID (마지막 워드)
    tid_start = value_start + value_bytes
    tid = int.from_bytes(data[tid_start:tid_start+2], 'big')
    
    # 부동소수점 변환
    if vtype == 1:
        value = decode_float(value_raw, value_bytes)
    else:
        value = value_raw
    
    # 부호 적용
    if sign == 1:
        value = -value
    
    # 스케일 적용
    scale_factor = 10 ** (scale - 8)
    actual_value = value * scale_factor
    
    # 화폐 처리
    currency = None
    if unit == 0x20:  # CURRENCY
        currency = reserved
    
    return {
        'unit': unit,
        'sign': sign,
        'size': size,
        'vtype': 'float' if vtype else 'int',
        'scale': scale - 8,
        'value_raw': value,
        'value': actual_value,
        'currency': currency,
        'tid': tid
    }
```

---

## 10. 인코딩

```python
def encode_quantity(
    value: float,
    unit: int,
    tid: int,
    currency: int = None
) -> bytes:
    # 부호 결정
    sign = 1 if value < 0 else 0
    abs_value = abs(value)
    
    # 스케일 및 정규화
    scale, normalized = normalize_value(abs_value)
    
    # 크기 및 타입 결정
    size, vtype, encoded_value = encode_value(normalized)
    
    # 1st WORD
    word1 = (0b1100000101 << 6) | unit
    
    # 2nd WORD
    reserved = currency if (unit == 0x20 and currency) else 0
    word2 = (sign << 15) | (size << 13) | (vtype << 12) | ((scale + 8) << 8) | reserved
    
    # 조립
    result = word1.to_bytes(2, 'big')
    result += word2.to_bytes(2, 'big')
    result += encoded_value
    result += tid.to_bytes(2, 'big')
    
    return result

def normalize_value(value: float) -> tuple:
    """값을 정규화하여 (scale, normalized) 반환"""
    if value == 0:
        return 8, 0  # scale=0, value=0
    
    import math
    log_val = math.log10(abs(value))
    scale = int(math.floor(log_val))
    
    # 범위 제한 (-8 ~ +7)
    scale = max(-8, min(7, scale))
    
    normalized = value / (10 ** scale)
    return scale, normalized
```

---

## 11. 예시

### 11.1 "100kg"

```
값: 100, 단위: kg (0x01)

Quantity Node:
  1st: [1100 000 101] + [000001]   - Prefix + kg
  2nd: [0][00][0][1000][00000000]  - +, 1워드, int, ×1
       = 0x0800
  3rd: [0x0064]                    - 100
  4th: [TID: 0x0050]

총: 4워드

해석: +100 × 10⁰ kg = 100kg
```

### 11.2 "330.5m" (부동소수점)

```
값: 330.5, 단위: meter (0x00)

Quantity Node:
  1st: [1100 000 101] + [000000]   - Prefix + meter
  2nd: [0][01][1][1000][00000000]  - +, 2워드, float, ×1
       = 0x3800
  3rd: [330.5 상위 16비트]         - IEEE 754 float32
  4th: [330.5 하위 16비트]
  5th: [TID: 0x0051]

총: 5워드

해석: +330.5 × 10⁰ m = 330.5m
```

### 11.3 "-273.15°C"

```
값: -273.15, 단위: celsius (0x14)

Quantity Node:
  1st: [1100 000 101] + [010100]   - Prefix + celsius
  2nd: [1][01][1][1000][00000000]  - -, 2워드, float, ×1
       = 0xB800
  3rd: [273.15 상위]
  4th: [273.15 하위]
  5th: [TID: 0x0052]

총: 5워드

해석: -273.15 × 10⁰ °C = -273.15°C
```

### 11.4 "$2,500,000 (250만 달러)"

```
값: 2,500,000, 단위: CURRENCY (0x20), 통화: USD (0x00)

Quantity Node:
  1st: [1100 000 101] + [100000]   - Prefix + CURRENCY
  2nd: [0][01][0][1110][00000000]  - +, 2워드, int, ×10⁶, USD
       = 0x2E00
  3rd: [0x0002]                    - 2 (상위)
  4th: [0x625A]                    - 0x2625A = 2,500,000? 
       
       또는 Scale 활용:
  2nd: [0][00][0][1011][00000000]  - +, 1워드, int, ×10³ (킬로)
       = 0x0B00
  3rd: [0x09C4]                    - 2500
  4th: [TID: 0x0053]

총: 4워드 (스케일 활용)

해석: +2500 × 10³ USD = $2,500,000
```

### 11.5 "₩9,700,000,000 (97억 원)"

```
값: 9,700,000,000, 단위: CURRENCY (0x20), 통화: KRW (0x05)

Quantity Node:
  1st: [1100 000 101] + [100000]   - Prefix + CURRENCY
  2nd: [0][00][0][1110][00000101]  - +, 1워드, int, ×10⁶, KRW
       = 0x0E05
  3rd: [0x25F2]                    - 9700
  4th: [TID: 0x0054]

총: 4워드

해석: +9700 × 10⁶ KRW = ₩9,700,000,000
```

---

## 12. 설계 근거

### 12.1 가변 길이 이유

- **16비트 값:** 대부분의 일상 수치 (나이, 개수 등)
- **32비트 값:** 정밀 측정, 중간 금액
- **64비트 값:** 천문학적 수치, 대규모 금액

고정 64비트면 낭비, 가변으로 효율 확보.

### 12.2 Scale 분리 이유

- **표현 범위 확장:** 16비트 값으로도 10⁻⁸ ~ 10⁷ 커버
- **SI 접두어 대응:** km, mm, μm 등 자연스럽게 표현
- **금액 표현:** 백만, 십억 단위 간결하게

### 12.3 화폐 확장 이유

- **Unit 통합:** 모든 화폐를 0x20 하나로
- **통화 분리:** Reserved 8비트로 256개 통화
- **확장성:** 법정화폐 + 암호화폐 모두 커버

### 12.4 TID 마지막 이유

- **Node 일관성:** Entity Node도 TID 마지막
- **가변 길이 호환:** Value 크기와 무관하게 마지막

---

## 13. 비교: Entity vs Quantity

| | Entity Node | Quantity Node |
|--|-------------|---------------|
| Prefix | 7비트 | 10비트 |
| 가변 | Lane+UIDflag | Size |
| 워드 | 3/5 | 4/5/7 |
| TID 위치 | 마지막 | 마지막 |
| 용도 | 개체 식별 | 수치 표현 |

---

## 14. 버전 히스토리

| 버전 | 날짜 | 변경 |
|------|------|------|
| v0.1 | 2026-01-29 | 초안: 가변 길이 구조, 화폐 확장 |
| v0.2 | 2026-01-29 | Prefix 표기 수정, SIDX.md 참조로 변경 |
| v0.3 | 2026-01-30 | **특수 리터럴 추가**: TIMESTAMP_SEC, TIMESTAMP_MS, UTF16, RGBA |

---

## 15. TODO

- [ ] 부동소수점 인코딩 상세 (float16/32/64)
- [ ] 통화 코드 전체 목록 (ISO 4217 대응)
- [ ] 복합 단위 표현 방안 (m/s, kg·m² 등)
- [ ] 오차/정밀도 표현 방안

---

**문서 종료**