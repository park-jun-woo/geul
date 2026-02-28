# SIDX 인코딩 방법

*2026년 2월 27일*

---

## 핵심 요약

```
sidx.yaml (코드북 정의)
  → LLM 프롬프트 자동 생성
    → LLM 배치 태깅 (제한된 키워드 내에서만 선택)
      → 유효성 검증 (invalid → reject → 재시도)
        → 태그 → 코드북 lookup → 비트 조립
          → uint64 배열 저장 (index.bin)
            → 검색 시 SIMD AND/OR → 후보 → LLM 전수 검사
```

---

## 1. 왜 16비트만으로 충분한가

### 산수

```
목표: 1.08억건을 3000건 이하로 줄이기
필요한 버킷 수: 108,000,000 / 3,000 = 36,000
필요한 비트: log2(36,000) = 15.1비트

16비트면 충분. 64비트 중 48비트가 남는다.
```

### 차원의 곱셈 효과

```
1차원 (64타입):
  1.08억 / 64 = 168만건

2차원 (64타입 × 32분류):
  1.08억 / 2,048 = 52,734건

3차원 (+ 16권역):
  1.08억 / 32,768 = 3,296건

4차원 (+ 8시대):
  1.08억 / 262,144 = 412건
```

차원 하나 추가할 때마다 버킷이 N분의 1로 쪼개진다.
코드북을 정교하게 만드는 게 아니라 **축을 하나 더 세우면** 해결.

### 위키데이터 실제 분포 기반 계산

```
위키데이터 P31 (instance of) 상위 분포:

scholarly article:  45,216,368  (41.6%)
human:             12,553,810  (11.5%)
Wikimedia category: 5,698,822  (5.2%)
taxon:              3,787,844  (3.5%)
star:               3,634,978  (3.3%)
infrared source:    2,621,805  (2.4%)
galaxy:             2,133,383  (2.0%)
chemical entity:    1,278,857  (1.2%)
gene:               1,225,271  (1.1%)
painting:           1,060,257  (1.0%)
...
```

#### 실제 쿼리별 후보 수

```
"한국 정치인":
  type=human(1255만) × 1/200국 × 1/32직업 = ~1,962건

"19세기 프랑스 화가":
  type=human(1255만) × 1/200 × 1/32 × 1/8시대 = ~245건

"적색왜성":
  type=star(363만) × 1/8분광 × 1/4광도 × 1/16온도 = ~7,100건

"르네상스 이탈리아 유화":
  type=painting(106만) × 1/8시대 × 1/8매체 × 1/16지역 = ~1,035건

"딥러닝 관련 논문 2024":
  type=article(4520만) × 1/32분야 × 1/16세부 × 1/30연도 = ~2,944건
```

대충 나눠도 대부분 쿼리에서 수백~수천건.

---

## 2. 64비트 SIDX 구조

### 비트 배치

```
64비트 = 공통 필드(18비트) + 커스텀 필드(가변) + 예약(나머지)

[ type 6 | subtype 5 | region 4 | era 3 | custom 0-46 | reserved ]
  MSB                                                          LSB
```

### 공통 필드 (18비트)

```
type:     6비트 → 64가지 상위 타입
subtype:  5비트 → 타입별 32가지 하위 분류
region:   4비트 → 16개 권역
era:      3비트 → 8개 시대 구간
```

18비트 = 262,144 버킷 → 1.08억 / 262,144 = **412건**

### 커스텀 필드 (최대 46비트)

남는 46비트를 도메인별로 자유롭게 할당.

```
법률 회사:
  court_level:    3비트 (대법원/고등/지방/헌재/행정/가정/특허/군사)
  case_type:      4비트 (민사/형사/행정/가사/파산/노동...)
  outcome:        2비트 (원고승/피고승/화해/각하)
  statute_area:   4비트 (헌법/민법/형법/상법/노동법...)
  client_tag:     8비트 (내부 고객 256개 분류)
  사용: 21비트. 25비트 남음.

의료:
  organ_system:   4비트 (순환/호흡/소화/신경...)
  condition_type: 4비트 (급성/만성/선천/후천...)
  severity:       2비트 (경증/중등/중증/위독)
  drug_class:     6비트 (64개 약물 분류)
  trial_phase:    3비트 (전임상/1상/2상/3상/4상/승인/철회)
  사용: 19비트. 27비트 남음.

이커머스:
  product_cat:    6비트 (64개 카테고리)
  price_range:    3비트 (8구간)
  brand_tier:     2비트 (럭셔리/프리미엄/중가/저가)
  season:         2비트 (춘하추동)
  stock_status:   2비트 (재고/부족/품절/단종)
  customer_seg:   4비트 (16개 세그먼트)
  사용: 19비트. 27비트 남음.

GEULC 이벤트:
  action:         4비트 (decision/todo/bug/progress...)
  status:         4비트 (open/resolved/superseded/blocked)
  priority:       4비트 (16단계)
  session_id:    12비트 (4096 세션)
  사용: 24비트. 22비트 남음.
```

---

## 3. 코드북 정의: sidx.yaml

### 포맷

```yaml
# sidx.yaml — SIDX 인코딩 코드북 정의

version: 1
total_bits: 64

# ─── 공통 필드 (모든 도메인) ───
common:
  type:
    bits: 6
    values:
      - person          # 0
      - organization    # 1
      - location        # 2
      - creative_work   # 3
      - event           # 4
      - taxon           # 5
      - star            # 6
      - galaxy          # 7
      - chemical        # 8
      - gene            # 9
      - painting        # 10
      - protein         # 11
      - street          # 12
      - article         # 13
      # ... 최대 64개

  subtype:
    bits: 5
    values_per_type:
      person:
        - politician     # 0
        - scientist      # 1
        - artist         # 2
        - athlete        # 3
        - writer         # 4
        - military       # 5
        - religious      # 6
        - business       # 7
        - diplomat       # 8
        - activist       # 9
        - educator       # 10
        - engineer       # 11
        - medical        # 12
        - legal          # 13
        - entertainer    # 14
        - royalty        # 15
        # ... 최대 32개
      organization:
        - company        # 0
        - university     # 1
        - ngo            # 2
        - government     # 3
        - military       # 4
        - religious      # 5
        - media          # 6
        - sports         # 7
        # ... 최대 32개
      location:
        - city           # 0
        - country        # 1
        - mountain       # 2
        - river          # 3
        - building       # 4
        - region         # 5
        - island         # 6
        - continent      # 7
        # ... 최대 32개
      # ... 타입별 정의

  region:
    bits: 4
    values:
      - east_asia        # 0 (한국, 일본, 중국, 몽골, 대만)
      - southeast_asia   # 1
      - south_asia       # 2
      - central_asia     # 3
      - west_asia        # 4 (중동)
      - north_africa     # 5
      - sub_saharan      # 6
      - west_europe      # 7
      - east_europe      # 8
      - north_europe     # 9
      - south_europe     # 10
      - north_america    # 11
      - central_america  # 12
      - south_america    # 13
      - oceania          # 14
      - global           # 15 (지역 무관)

  era:
    bits: 3
    values:
      - ancient          # 0 (~500)
      - medieval         # 1 (500~1500)
      - early_modern     # 2 (1500~1800)
      - modern           # 3 (1800~1945)
      - contemporary     # 4 (1945~2000)
      - current          # 5 (2000~)
      - timeless         # 6 (시대 무관)
      - unknown          # 7

# ─── 커스텀 필드 (도메인별) ───
custom:
  # 예시: 법률 도메인
  court_level:
    bits: 3
    values: [supreme, high, district, constitutional, 
             administrative, family, patent, military]
  case_type:
    bits: 4
    values: [civil, criminal, administrative, family, bankruptcy,
             labor, tax, ip, environmental, election, 
             international, constitutional, maritime, antitrust,
             consumer, other]
  outcome:
    bits: 2
    values: [plaintiff_win, defendant_win, settlement, dismissed]

# ─── 타입 간 정합성 규칙 ───
constraints:
  - if: { type: star }
    then: { region: global, era: timeless }  # 별에 지역/시대 무의미
  - if: { type: painting }
    then: { subtype_from: [oil, watercolor, portrait, landscape, 
                           abstract, religious, historical, genre] }
  - if: { type: gene }
    then: { region: global }  # 유전자에 지역 무의미
```

### 제로 설정 기본값

```yaml
# 최소 설정 (커스텀 없이)
version: 1
total_bits: 64
common:
  type: { bits: 6 }
  subtype: { bits: 5 }
  region: { bits: 4 }
  era: { bits: 3 }
# → 공통 18비트만 사용. 나머지 46비트 0.
# → 이것만으로 1.08억 → 412건.
```

---

## 4. LLM 태깅 파이프라인

### 4-1. 프롬프트 자동 생성

sidx.yaml에서 LLM 프롬프트를 자동 생성.

```
[시스템 프롬프트]
당신은 문서 분류 전문가입니다.
다음 문서를 읽고, 각 필드에 대해 주어진 유효값 목록에서
정확히 하나만 선택하여 태그하십시오.
반드시 유효값 내에서만 선택할 것.
유효값에 적합한 것이 없으면 "unknown" 또는 "other"를 선택할 것.

[필드 정의]
type (필수): person, organization, location, creative_work, event,
             taxon, star, galaxy, chemical, gene, painting, protein,
             street, article
subtype (필수): {type에 따른 유효값 목록}
region (필수): east_asia, southeast_asia, south_asia, central_asia,
               west_asia, north_africa, sub_saharan, west_europe,
               east_europe, north_europe, south_europe, north_america,
               central_america, south_america, oceania, global
era (필수): ancient, medieval, early_modern, modern, contemporary,
            current, timeless, unknown

[출력 형식]
JSON만 출력. 다른 텍스트 없이.
{"type": "...", "subtype": "...", "region": "...", "era": "..."}

[문서]
{document_text}
```

### 4-2. LLM 태깅 실행

```
입력: "이순신(李舜臣, 1545년 4월 28일 ~ 1598년 12월 16일)은
       조선 중기의 무신이다. 임진왜란 때 조선 수군을 이끌어..."

LLM 응답:
{"type": "person", "subtype": "military", "region": "east_asia", "era": "early_modern"}
```

LLM의 태스크: **닫힌 선택지에서 고르기**. 가장 쉬운 태스크.
자유 생성이 아니라 객관식. 환각할 여지 최소.

### 4-3. 배치 처리 비용

```
문서당:
  입력: ~200토큰 (프롬프트 + 문서 요약)
  출력: ~30토큰 (JSON)

모델별 비용 (1.08억건):
  GPT-4o-mini ($0.15/1M input):
    108M × 200 = 21.6B 토큰 입력
    21.6B × $0.00000015 = $3,240

  로컬 8B 모델 (Llama 3):
    비용 $0. A100 1대로 ~3일.

  Claude Haiku:
    108M × 230토큰 × $0.00000025 = ~$6,210
```

1억건 전체 SIDX 인코딩: **$3,000~6,000**. 1회성 비용.

### 4-4. 부분 재인코딩

코드북 수정 시 전체 재인코딩 불필요. 영향받는 타입만 재태깅.

```
코드북에 subtype "diplomat" 추가:
  → type=person만 재태깅 대상
  → 1255만건 × $0.00003 = $376
  → 나머지 9500만건은 그대로

코드북에 region 분류 변경:
  → 전체 재태깅 필요
  → 하지만 region만 재분류하면 되니까
  → 프롬프트를 region만 물어보게 축소
  → 비용 절감
```

---

## 5. 유효성 검증 (Validation)

### 벡터 임베딩과의 결정적 차이

```
벡터 임베딩:
  문서 → [0.234, -0.891, 0.445, ..., 0.112] (384차원 float)
  맞는지 틀린지 확인 방법 없음. 블랙박스.
  잘못됐을 때 고칠 수 없음. 재임베딩밖에 답 없음.

SIDX 태깅:
  문서 → {"type": "person", "subtype": "military", "region": "east_asia"}
  각 필드가 유효한지 즉시 확인. 화이트박스.
  잘못됐을 때 태그 하나 고치면 됨.
```

### 4단계 검증 체계

#### 레벨 1 — 유효값 체크 (즉시, 자동)

```
LLM 응답: {"type": "person", "subtype": "admiral", "region": "east_asia"}

검증:
  type: "person"      → ✅ codebook.common.type.values에 있음
  subtype: "admiral"  → ❌ codebook.common.subtype.values_per_type.person에 없음
  region: "east_asia" → ✅ codebook.common.region.values에 있음

결과: REJECT
사유: subtype "admiral"은 유효값이 아님
액션: LLM에 재질의 — "subtype을 다음 중에서 선택: [politician, scientist,
      artist, athlete, writer, military, ...]"
재응답: {"subtype": "military"} → ✅ 통과
```

```go
func validateField(value string, validValues []string) error {
    if !slices.Contains(validValues, value) {
        return fmt.Errorf("invalid value %q, valid: %v", value, validValues)
    }
    return nil
}
```

#### 레벨 2 — 타입 정합성 체크 (즉시, 자동)

```
LLM 응답: {"type": "painting", "subtype": "politician"}

검증:
  type=painting의 유효 subtype: [oil, watercolor, portrait, landscape, ...]
  "politician"은 painting의 subtype이 아님.

결과: REJECT
사유: type-subtype 불일치
액션: LLM에 재질의 — painting의 subtype 목록 제시
```

```go
func validateTypeConsistency(tag Tag, codebook Codebook) error {
    validSubtypes := codebook.SubtypesFor(tag.Type)
    if !slices.Contains(validSubtypes, tag.Subtype) {
        return fmt.Errorf("subtype %q invalid for type %q", tag.Subtype, tag.Type)
    }
    return nil
}
```

#### 레벨 3 — 제약조건 체크 (즉시, 자동)

sidx.yaml의 constraints 적용.

```
LLM 응답: {"type": "star", "region": "east_asia", "era": "modern"}

제약조건: type=star → region=global, era=timeless
  region "east_asia" → 자동 보정 → "global"
  era "modern" → 자동 보정 → "timeless"

결과: AUTO-CORRECT (reject하지 않고 자동 보정)
로그: "star entity: region east_asia → global (auto-corrected by constraint)"
```

```go
func applyConstraints(tag *Tag, constraints []Constraint) {
    for _, c := range constraints {
        if c.Matches(tag) {
            c.Apply(tag)  // 자동 보정
        }
    }
}
```

#### 레벨 4 — 통계적 이상치 탐지 (배치, 후처리)

```
전체 태깅 완료 후 버킷 크기 분석:

  type=person, subtype=politician, region=east_asia: 2,100건 ← 정상
  type=person, subtype=politician, region=global:   450,000건 ← 이상

  기대치 대비 10배 이상 → alert
  원인: LLM이 지역 판별 실패, 대부분 "global"로 태깅
  조치: region=global인 politician 재태깅 (프롬프트 보강)
```

```go
func detectAnomalies(index []uint64, codebook Codebook) []Alert {
    bucketCounts := countBuckets(index)
    expected := len(index) / codebook.TotalBuckets()
    
    var alerts []Alert
    for bucket, count := range bucketCounts {
        if count > expected*10 {
            alerts = append(alerts, Alert{
                Bucket:   bucket,
                Count:    count,
                Expected: expected,
                Ratio:    float64(count) / float64(expected),
            })
        }
    }
    return alerts
}
```

### 검증 파이프라인 요약

```
LLM 태깅 결과
    │
    ▼
[레벨 1] 유효값 체크 ──── invalid → reject → LLM 재질의
    │                                            │
    ▼                                            ▼
[레벨 2] 타입 정합성 ──── 불일치 → reject → LLM 재질의
    │
    ▼
[레벨 3] 제약조건 ──────── 위반 → auto-correct + 로그
    │
    ▼
[레벨 4] 통계 이상치 ───── 이상 → alert → 배치 재태깅
    │
    ▼
비트 조립 → index.bin 저장
```

레벨 1-3: 건당 즉시. 레벨 4: 전체 완료 후 배치.

---

## 6. 비트 조립

### 태그 → 비트 변환

```
LLM 태깅 결과 (검증 통과):
  type:    "person"       → codebook lookup → 0  (6비트: 000000)
  subtype: "military"     → codebook lookup → 5  (5비트: 00101)
  region:  "east_asia"    → codebook lookup → 0  (4비트: 0000)
  era:     "early_modern" → codebook lookup → 2  (3비트: 010)
```

### 비트 배치

```
비트 63                                              비트 0
[  type  |subtype| reg |era|     custom / reserved      ]
[ 000000 | 00101 | 0000| 010 | 0000...0000000000000000  ]
  6비트    5비트   4비트 3비트        46비트
```

### Go 코드

```go
type SIDX uint64

type Tag struct {
    Type    string `json:"type"`
    Subtype string `json:"subtype"`
    Region  string `json:"region"`
    Era     string `json:"era"`
    Custom  map[string]string `json:"custom,omitempty"`
}

type Codebook struct {
    Common  CommonFields         `yaml:"common"`
    Custom  map[string]Field     `yaml:"custom"`
    Layout  []FieldLayout        // 비트 위치 계산 결과
}

type FieldLayout struct {
    Name   string
    Bits   int
    Offset int  // 비트 시작 위치 (MSB부터)
}

func (cb *Codebook) Encode(tag Tag) (SIDX, error) {
    var sidx SIDX

    // 공통 필드 인코딩
    typeCode, err := cb.Common.Type.Lookup(tag.Type)
    if err != nil {
        return 0, fmt.Errorf("type: %w", err)
    }
    subtypeCode, err := cb.Common.Subtype.LookupFor(tag.Type, tag.Subtype)
    if err != nil {
        return 0, fmt.Errorf("subtype: %w", err)
    }
    regionCode, err := cb.Common.Region.Lookup(tag.Region)
    if err != nil {
        return 0, fmt.Errorf("region: %w", err)
    }
    eraCode, err := cb.Common.Era.Lookup(tag.Era)
    if err != nil {
        return 0, fmt.Errorf("era: %w", err)
    }

    // 비트 조립 (MSB부터)
    sidx |= SIDX(typeCode) << 58    // 비트 63-58: type (6비트)
    sidx |= SIDX(subtypeCode) << 53 // 비트 57-53: subtype (5비트)
    sidx |= SIDX(regionCode) << 49  // 비트 52-49: region (4비트)
    sidx |= SIDX(eraCode) << 46     // 비트 48-46: era (3비트)

    // 커스텀 필드 인코딩
    offset := 46
    for _, layout := range cb.Layout {
        if layout.Name == "type" || layout.Name == "subtype" ||
           layout.Name == "region" || layout.Name == "era" {
            continue
        }
        if val, ok := tag.Custom[layout.Name]; ok {
            code, err := cb.Custom[layout.Name].Lookup(val)
            if err != nil {
                return 0, fmt.Errorf("custom %s: %w", layout.Name, err)
            }
            offset -= layout.Bits
            sidx |= SIDX(code) << offset
        }
    }

    return sidx, nil
}

// Lookup: 값 → 코드 (인덱스)
func (f *Field) Lookup(value string) (int, error) {
    for i, v := range f.Values {
        if v == value {
            return i, nil
        }
    }
    return 0, fmt.Errorf("invalid value %q, valid: %v", value, f.Values)
}
```

### 검색 시 마스크 생성

```go
func (cb *Codebook) BuildMask(query map[string]string) (mask SIDX, pattern SIDX) {
    // mask: 검사할 비트 위치 (1 = 검사함)
    // pattern: 기대하는 값

    if typ, ok := query["type"]; ok {
        code, _ := cb.Common.Type.Lookup(typ)
        mask |= 0x3F << 58              // 6비트 마스크
        pattern |= SIDX(code) << 58
    }
    if sub, ok := query["subtype"]; ok {
        code, _ := cb.Common.Subtype.LookupFor(query["type"], sub)
        mask |= 0x1F << 53              // 5비트 마스크
        pattern |= SIDX(code) << 53
    }
    if reg, ok := query["region"]; ok {
        code, _ := cb.Common.Region.Lookup(reg)
        mask |= 0x0F << 49              // 4비트 마스크
        pattern |= SIDX(code) << 49
    }
    if era, ok := query["era"]; ok {
        code, _ := cb.Common.Era.Lookup(era)
        mask |= 0x07 << 46              // 3비트 마스크
        pattern |= SIDX(code) << 46
    }

    return mask, pattern
}

// SIMD 검색: (sidx & mask) == pattern 인 엔티티만 통과
func Search(index []SIDX, mask, pattern SIDX) []int {
    var results []int
    for i, sidx := range index {
        if (sidx & mask) == pattern {
            results = append(results, i)
        }
    }
    return results
}
// 실제로는 SIMD 명령어(AVX-512 등)로 벡터화
```

---

## 7. 전체 인코딩 파이프라인

### 단계별 흐름

```
[1단계] 코드북 정의
  사용자가 sidx.yaml 작성 (최소 1줄, 기본 공통 필드)
  또는 도메인별 커스텀 필드 추가
    ↓
[2단계] 프롬프트 생성
  sidx.yaml → LLM 프롬프트 자동 생성
  유효값 목록을 프롬프트에 포함
    ↓
[3단계] 배치 태깅
  문서 → LLM → JSON 태그
  병렬 처리: 1000건/배치 × 다중 워커
    ↓
[4단계] 검증
  레벨 1: 유효값 체크 → reject → 재질의
  레벨 2: 타입 정합성 → reject → 재질의
  레벨 3: 제약조건 → auto-correct
    ↓
[5단계] 비트 조립
  JSON 태그 → codebook lookup → 비트 시프트 → uint64
    ↓
[6단계] 인덱스 저장
  uint64 배열 → index.bin (바이너리)
  1.08억건 × 8바이트 = 864MB
    ↓
[7단계] 후처리 검증
  레벨 4: 버킷 크기 통계 → 이상치 탐지 → 재태깅 대상 식별
    ↓
[완료] 검색 가능 상태
```

### 시간 및 비용 추정

```
1.08억건 기준:

태깅 (GPT-4o-mini):
  시간: ~12시간 (1000 req/s, 배치)
  비용: ~$3,240

태깅 (로컬 Llama 8B, A100 1대):
  시간: ~3일
  비용: ~$0 (전기세 제외)

검증 + 비트 조립:
  시간: ~30분 (Go, 단일 코어)
  비용: $0

인덱스 저장:
  크기: 864MB
  시간: 수 초

총합: $3,240 + 반나절.
      한 번만 하면 됨.
```

---

## 8. 코드북 진화 전략

### MVP — 대충 시작 (v0.1)

```
위키데이터 P31 상위 타입 64개 그대로 사용.
각 타입을 기계적으로 32분류.
지역 16권역. 시대 8구간.
18비트. 끝.

SIMD Recall: 0.6-0.7 (대충이니까)
그래도 현업 RAG 10배 이상.
```

### 누락 분석 (v0.2)

```
검색 후 "놓친 정답" 분석 자동화.

geulc에 기능 추가:
  "이 쿼리에서 SIMD가 놓친 정답 리포트"

리포트:
  쿼리: "한국 외교관"
  SIMD 결과: 1,962건 (subtype=politician)
  누락: 이순신 → subtype=military (외교관이 아닌 군인으로 분류)
        김대중 → subtype=politician (포함됨 ✓)
        반기문 → subtype=diplomat (코드북에 diplomat 없음 ❌)

→ "diplomat"을 subtype에 추가하면 Recall 개선.
```

### 코드북 확장 (v0.3)

```
P279 (subclass of) 체인 반영.
  "외교관" → P279 → "정치인"
  → 쿼리 "정치인" 검색 시 "외교관"도 포함

자동 매핑:
  LLM이 "diplomat"으로 태깅하면
  → P279 체인에서 "politician의 하위"임을 확인
  → 코드북에 자동 추가 또는 상위어로 매핑
```

### 적응형 코드북 (v0.4+)

```
사용자 쿼리 패턴 분석:
  "한국 정치인" 쿼리 빈도 높음
  → "politician" subtype을 더 세분화
  → politician → [head_of_state, legislator, diplomat, minister, ...]
  → 해당 subtype만 재태깅

자주 안 쓰는 분류는 합치고, 자주 쓰는 분류는 쪼갬.
코드북이 사용 패턴에 적응.
```

---

## 9. 벡터 임베딩 대비 SIDX의 장점 요약

```
| 특성 | 벡터 임베딩 | SIDX 태깅 |
|------|-----------|----------|
| 인코딩 결과 | 384~4096 float | 1개 uint64 |
| 크기 (1억건) | 150GB~1.6TB | 864MB |
| 해석 가능성 | 블랙박스 | 화이트박스 (필드 값 읽힘) |
| 에러 검출 | 불가능 | 유효값 체크로 즉시 |
| 에러 수정 | 재임베딩 | 태그 1개 수정 |
| 부분 수정 | 불가능 (전체 재임베딩) | 영향받는 타입만 재태깅 |
| 검색 설명 | "벡터가 가까워서" | "type=X AND region=Y" |
| 감사(audit) | 불가능 | 태그 = 감사 로그 |
| 검색 속도 | ANN ~50ms | SIMD ~10ms |
| 필터링 방식 | 검색 후 필터 (비효율) | 필터가 곧 검색 |
| 코드북 수정 | 모델 재학습 | yaml 수정 + 부분 재태깅 |
| 커스텀 필드 | 메타데이터 별도 관리 | 비트에 직접 인코딩 |
| 도메인 적응 | 파인튜닝 필요 | yaml에 필드 추가 |
```

---

## 10. 설계 철학

```
코드북을 "설계"할 필요 없다.
위키데이터 상위 분류를 기계적으로 나누기만 해도 된다.
차원 4개면 1억이 천 건 아래로 떨어진다.
천 건이면 20B LLM이 100ms에 전수 검사한다.

코드북 품질이 0.7이어도 현업 RAG의 11배.
코드북 품질이 0.5여도 현업 RAG의 8배.
아키텍처가 부품 정밀도를 압도한다.

대충 시작해서, 쓰면서 좋아지는 구조.
이것이 SIDX 인코딩의 설계 철학이다.
```
