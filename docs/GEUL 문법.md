# GEUL 통합 문법 명세서 v0.2

**작성일:** 2026-01-26  
**상태:** 표준 초안 (DRAFT)  
**개정:** 참여자 16개 표준화, Edge 기반 구조 통일, 시간 역할 분리  
**목적:** GEUL(General Embedding Unified Language)의 완전한 구조적 정의

---

## 1. 개요

### 1.1 GEUL이란

GEUL은 자연어의 모호성을 보존하면서도 AI가 명시적으로 계산 가능한 형태로 변환하는 **구조화 언어**이다.

**핵심 목표:**
- 환각(Hallucination) 제거
- 추론 과정 추적 가능
- 인간-AI 상호 이해성 극대화
- 지식의 출처/신뢰도 명시

GEUL은 단순히 자연어를 "번역"하는 것이 아니라, 자연어가 내포한 **모든 의미적 정보를 명시적이고 계산 가능한 형태로 외부화(Externalization)**한다.

### 1.2 설계 원칙

**1. 서술 중심 (Claim-based)**
- "사실"이 아닌 "서술"을 저장
- 모든 진술은 관점(Context) 내에서만 의미를 가짐
- "진실"이 아니라 "진실에 대한 진술"을 다룸

**2. 의미 중첩 (Superposition)**
- 자연어 모호성을 정보 손실 없이 보존
- 여러 해석을 병렬로 표현
- 확률적 가중치 부여

**3. 의미정렬 (Semantic-Aligned)**
- 식별자 자체가 의미 내포
- 상위 비트 = 중요 정보
- 우아한 열화 (Graceful Degradation) 구현

**4. MRS + 참여자 기반**
- Minimal Recursion Semantics를 토대로
- 논리적 범위 명확화
- 평탄한 그래프 구조 유지
- 참여자(Participant) Edge로 의미역 명시

---

## 2. 기본 구조

### 2.1 단위

**WORD:**
- 16비트 (2바이트)
- GEUL의 최소 원자 단위
- 2^16 = 65,536개 가능한 값

**SIDX (Semantic-aligned Index):**
- 기본: 4 WORD = 64비트 (8바이트)
- 의미정렬 식별자
- 확장 시: 16 WORD = 256비트 (32바이트)
- 위키데이터 11.3억 개체 수용 가능

**패킷 (Packet):**
- 평균 4 WORD
- 노드 또는 엣지 1개 표현
- 자연어 단어 1개 ≈ GEUL 패킷 1개

**토큰 밀도:**
- 영어: 단어 1개 ≈ GPT 토큰 3개
- GEUL: 개념 1개 ≈ 4 WORD (1 패킷)
- 거의 동일한 정보 밀도 → GPT 컨텍스트 효율적 활용

### 2.2 스트림 구조

```
[메타 헤더] (1 WORD)
  ↓ 
[노드 패킷들] (각 4 WORD)
  - Entity 노드들
  - Verb 노드들
  - Context 노드들
  - Quantifier 노드들
  ↓
[엣지 패킷들] (각 4 WORD)
  - PARTICIPANT 엣지들
  - MOD 엣지들
  - CONTEXT 엣지들
  - 기타 관계 엣지들
```

**메타 헤더 구조 (1 WORD):**
```
bit 1-4:   버전 정보
bit 5-8:   인코딩 플래그
bit 9-16:  스트림 타입
```

---

## 3. 노드 명세

### 3.1 노드 종류

| 노드 타입 | 설명 | 식별자 기반 |
|-----------|------|-------------|
| **Entity** | 사람, 장소, 사물, 조직, 개념 | QID / Synset |
| **Verb** | 행위, 상태, 관계 | Synset |
| **Context** | 서술의 귀속 범위 (WMS 전용) | 내부 ID |
| **Claim** | 진술의 최소 단위 | 내부 ID |
| **Quantifier** | every, some, most 등 | 표준 ID |

**Note:** Participant는 노드가 아닌 **Edge**로 표현한다.

### 3.2 Entity 식별자

#### 3.2.1 상위 분류 (4비트)

Entity의 SIDX bit 5-8은 16개 상위 분류를 인코딩한다:

| ID | 코드 | 분류 | 예시 |
|----|------|------|------|
| 0x0 | HUM | Human (인간) | 아인슈타인, 손흥민 |
| 0x1 | ORG | Organization (조직) | Apple Inc., UN |
| 0x2 | LOC | Location (장소) | 서울, 에펠탑 |
| 0x3 | EVT | Event (사건) | 월드컵, 지진 |
| 0x4 | WRK | Work (창작물) | 해리포터, 모나리자 |
| 0x5 | PRD | Product (제품) | iPhone, 코카콜라 |
| 0x6 | SPE | Species (생물종) | 호랑이, 장미 |
| 0x7 | SUB | Substance (물질) | 물, 철, 산소 |
| 0x8 | CON | Concept (추상개념) | 민주주의, 사랑 |
| 0x9 | QTY | Quantity (수량) | 3개, 50% |
| 0xA | TIM | Time (시간) | 2024년, 3시간 |
| 0xB | UNT | Unit (단위) | 킬로그램, 달러 |
| 0xC | ATR | Attribute (속성) | 빨강, 크다 |
| 0xD | ACT | Activity (활동) | 축구, 요리 |
| 0xE | STT | State (상태) | 행복, 고장 |
| 0xF | RSV | Reserved (예약) | 확장용 |

#### 3.2.2 SIDX 구조 (64비트)

```
bit 1:     Lane (0=Standard, 1=Extension)
bit 2:     Type (0=Node, 1=Edge)
bit 3-4:   Group (00=Entity/Verb, 01=Context/Claim, 10=Meta, 11=Reserved)
bit 5-8:   상위 분류 (16개 타입)
bit 9-32:  속성 플래그 (24비트)
bit 33-64: 로컬 ID (32비트, Q-ID 또는 Synset ID)
```

**속성 플래그 (bit 9-32):**
```
bit 9-12:  하위 분류 (16개)
bit 13-16: 지리적 범위 (대륙/국가)
bit 17-20: 시대 구분
bit 21-32: 도메인별 확장
```

#### 3.2.3 고유 개체 vs 범주

| 구분 | 식별자 | 예시 |
|------|--------|------|
| 고유 개체 (Instance) | Q-ID | Q312 (Apple Inc.) |
| 범주 (Category) | Synset | apple.n.01 (과일 사과) |

GEUL은 둘을 명확히 구분하며, 필요시 인스턴스 → 범주 변환으로 우아한 열화 구현.

### 3.3 Verb 식별자

워드넷 Synset-ID를 필수로 사용한다.

```
예: release.v.01 = 출시하다
    run.v.01 = 달리다
    think.v.01 = 생각하다
```

#### 3.3.1 SIDX 구조 (64비트)

```
bit 1-4:   타입 플래그
bit 5-32:  동사 한정자 영역 (28비트)
bit 33-64: Verb Synset ID (32비트)
```

#### 3.3.2 동사 한정자 비트 레이아웃 (bit 5-32)

| 한정자 | 비트 범위 | 비트 수 | 인코딩 | 설명 |
|--------|-----------|---------|--------|------|
| Tense (시제) | 5-8 | 4 | Float | -1.0=과거, 0.0=현재, +1.0=미래 |
| Aspect (상) | 9-11 | 3 | Bitmask | 1=진행, 2=완료, 4=결과 |
| Polarity (극성) | 12-15 | 4 | Float | -1.0=부정, +1.0=긍정 |
| Evidentiality (증거성) | 16-19 | 4 | Float | -1.0=추론, 0.0=직접, +1.0=전언 |
| Mood (서법) | 20-23 | 4 | Float | -1.0=가정, 0.0=서술, +1.0=명령 |
| Volitionality (의도성) | 24-26 | 3 | Float | -1.0=비의도, +1.0=의도 |
| Confidence (확신성) | 27-29 | 3 | Float | -1.0=추측, +1.0=확신 |
| Politeness (공손) | 30-32 | 3 | Float | -1.0=반말, +1.0=존대 |

**총 28비트 사용.**

#### 3.3.3 Float 양자화

**4비트 (16단계):**
```
0: -1.000    4: -0.467    8:  +0.067   12: +0.600
1: -0.867    5: -0.333    9:  +0.200   13: +0.733
2: -0.733    6: -0.200   10:  +0.333   14: +0.867
3: -0.600    7: -0.067   11:  +0.467   15: +1.000
```

**3비트 (8단계):**
```
0: -1.000    2: -0.429    4: +0.143    6: +0.714
1: -0.714    3: -0.143    5: +0.429    7: +1.000
```

#### 3.3.4 한정자 예시

**"먹었대" (들은 말로 과거에 먹었다)**
```
Verb: eat.v.01
Tense: -0.8 (과거)
Aspect: 2 (완료)
Polarity: +1.0 (긍정)
Evidentiality: +1.0 (전언)
Mood: 0.0 (서술)
```

**"반드시 가라"**
```
Verb: go.v.01
Tense: +0.8 (미래)
Aspect: 0 (단순)
Polarity: +1.0 (긍정)
Mood: +1.0 (명령)
Confidence: +1.0 (확신)
```

#### 3.3.5 별도 노드로 표현되는 동사 메타데이터

비트에 담기 어려운 복잡한 정보:

**Modality (양태):**
```
[Modality Node]
  Type: can | may | must | should | will
  Strength: 0.0~1.0
  → Verb SIDX
  
예: "먹을 수 있다" → Type: can, Strength: 0.8
```

**Iterativity (반복성):**
```
[Iterativity Node]
  Count: Integer
    0: 미지정
    1: 1회
    >1: 실제 횟수
    MAX-1: 많음
    MAX: 무한
  → Verb SIDX
```

**Period/Point (기간/시점):**
```
[Temporal Node]
  Type: point | period
  Value: ISO8601 또는 Duration
  → Verb SIDX

예: "3시간 동안" → Type: period, Value: PT3H
    "2024년 1월 1일에" → Type: point, Value: 2024-01-01
```

---

## 4. 엣지 명세

### 4.1 엣지 종류

| 엣지 타입 | 설명 | Source → Target |
|-----------|------|-----------------|
| **PARTICIPANT** | 사건 참여자 역할 | Verb → Entity |
| **MOD** | 수식/한정 관계 | Any → Any |
| **CONTEXT** | 관점 귀속 | Claim → Context |
| **RSTR** | 한정자 제한 범위 | Quantifier → Entity |
| **BODY** | 한정자 본체 범위 | Quantifier → Verb |
| **PROPERTY** | 속성 관계 | Entity → Entity |

### 4.2 PARTICIPANT Edge (핵심)

#### 4.2.1 구조

```
PARTICIPANT Edge {
  source:     Verb SIDX        // 동사 노드
  target:     Entity SIDX      // 개체 노드
  role:       4-bit            // 의미역 (0x0~0xF)
  gram_role:  2-bit            // 문법적 역할 (선택)
  focus:      4-bit            // 강조도 (선택)
  quant_ref:  16-bit TID       // 한정자 참조 (선택)
}
```

#### 4.2.2 의미역 목록 (16개)

| ID | 코드 | 역할 | 정의 | 예시 |
|----|------|------|------|------|
| 0x0 | AGT | Agent | 의도적 행위자 | "**철수가** 찼다" |
| 0x1 | EXP | Experiencer | 경험/인지 주체 | "**영희가** 슬펐다" |
| 0x2 | THM | Theme | 이동/기술 대상 | "**공을** 찼다" |
| 0x3 | PAT | Patient | 상태 변화 대상 | "**유리가** 깨졌다" |
| 0x4 | RCP | Recipient | 수령자 | "**영희에게** 줬다" |
| 0x5 | BNF | Beneficiary | 수익자 | "**아이를 위해**" |
| 0x6 | INS | Instrument | 도구 | "**망치로** 박았다" |
| 0x7 | MNR | Manner | 방식 | "**빠르게** 달렸다" |
| 0x8 | LOC | Location | 장소 | "**서울에서** 살았다" |
| 0x9 | SRC | Source | 출발점 | "**집에서** 출발" |
| 0xA | DST | Destination | 목적지 | "**학교로** 갔다" |
| 0xB | PTH | Path | 경로 | "**공원을 지나**" |
| 0xC | CAU | Cause | 원인 | "**비 때문에**" |
| 0xD | PRP | Purpose | 목적 | "**운동하러**" |
| 0xE | COM | Comitative | 동반 | "**친구와** 함께" |
| 0xF | ATR | Attribute | 속성 | "하늘이 **파랗다**" |

#### 4.2.3 문법적 역할 (선택, 2비트)

| 값 | 역할 |
|----|------|
| 0 | 미지정 |
| 1 | 주어 (Subject) |
| 2 | 목적어 (Object) |
| 3 | 보어 (Complement) |

**용도:** 능동/수동 변환 시 원문 구조 보존

#### 4.2.4 Focus (강조도, 4비트)

```
0x0: 0.0 (배경 정보)
0x7: 0.5 (보통)
0xF: 1.0 (핵심 강조)
```

**예:** "영희를 사랑하는 사람은 **철수**다" → 철수의 Focus = 0xF

#### 4.2.5 비트 레이아웃 (1 WORD = 16비트)

```
[ role:4 | gram_role:2 | focus:4 | reserved:6 ]
```

전체 PARTICIPANT Edge 패킷 (4 WORD):
```
WORD 0: Edge 타입 + 플래그
WORD 1: Source TID (Verb)
WORD 2: Target TID (Entity)
WORD 3: role | gram_role | focus | reserved
```

### 4.3 MOD Edge

수식/한정 관계:

```
MOD Edge {
  source: 수식어 SIDX
  target: 피수식어 SIDX
  mod_type: 4-bit (degree, temporal, manner, etc.)
}
```

**예:**
```
"매우 중요하다"
[MOD: very → important.a.01]
  mod_type: degree
```

### 4.4 CONTEXT/CLAIM Edge

Context-Claim 체계 (WMS 연동):

```
[CONTEXT Edge]
  source: Claim SIDX
  target: Context SIDX

용도: "이 서술이 누구의 관점인가"
```

---

## 5. 화용 정보 분리

### 5.1 원칙

| 정보 유형 | 소속 | 위치 |
|-----------|------|------|
| 사건 참여자 (Agent, Theme...) | Event | PARTICIPANT Edge |
| 시간 (When) | Event | 동사 한정자 + Temporal Node |
| 발화 주체 (Speaker) | Meta | Context/Claim |
| 청자 (Listener) | Meta | Context/Claim |
| 정보 출처 (Source) | Meta | Context/Claim |

### 5.2 Speaker/Listener/Source

**이들은 참여자가 아니다.** Context 또는 Claim 레벨에서 처리:

```
[Claim]
  id: claim_001
  speaker: Q12345 (화자)
  listener: Q67890 (청자, nullable)
  source: [doc_001, person_002] (정보 출처)
  content: [Event...]
```

### 5.3 시간 처리

| 시간 유형 | 처리 위치 |
|-----------|----------|
| 문법적 시제 | 동사 한정자 Tense (비트) |
| 구체적 시점 | Temporal Node (별도) |
| 기간 | Temporal Node (별도) |
| 빈도 | Iterativity Node (별도) |

**Note:** Time은 참여자 의미역에서 **제외**됨.

---

## 6. TID (Temporary ID)

### 6.1 정의

스트림 내 임시 참조 ID. 대명사 해소 등에 사용.

```
TID 구조 (16비트):
bit 1-4:   타입 (entity, verb, participant, etc.)
bit 5-16:  스트림 내 순번
```

### 6.2 용도

**1. 스트림 내 참조:**
```
[Entity: TID=0x01] // Apple
[Entity: TID=0x02] // iPhone
[Verb: TID=0x10]   // release
[PARTICIPANT: 0x10 → 0x01, role=AGT]
[PARTICIPANT: 0x10 → 0x02, role=THM]
```

**2. 대명사 해소:**
```
"철수가 그의 책을 읽었다"

[Entity: TID=0x01] // 철수
[Entity: TID=0x02] // 책
[PROPERTY: 0x02.owner = 0x01] // 그의 → 철수
```

**3. 한정자 참조:**
```
[Quantifier: TID=0x20] // every
[PARTICIPANT: role=AGT, quant_ref=0x20]
```

---

## 7. 의미 중첩 (Superposition)

### 7.1 정의

자연어의 모호성을 정보 손실 없이 표현:

```
[SUPERPOSITION]
  interpretation_1: [weight]
    ...GEUL 구조...
  interpretation_2: [weight]
    ...GEUL 구조...
```

### 7.2 예시

**"The chicken is ready to eat"**

```
[Entity: chicken.n.01]
[Verb: ready.v.01]
[Verb: eat.v.01]

[SUPERPOSITION]
  interpretation_1: [0.5]
    // 닭이 (무언가를) 먹을 준비가 됨
    [PARTICIPANT: eat.v.01 → chicken, role=AGT]
    
  interpretation_2: [0.5]
    // (누군가가) 닭을 먹을 준비가 됨
    [PARTICIPANT: eat.v.01 → chicken, role=THM]
```

### 7.3 한정자 범위 모호성

**"Every professor taught a course"**

```
해석 1: ∀p ∃c (teach(p,c))
  "각 교수가 (각자 다른) 어떤 과목을 가르쳤다"
  
해석 2: ∃c ∀p (teach(p,c))
  "어떤 (같은) 과목을 모든 교수가 가르쳤다"

[SUPERPOSITION]
  interpretation_1: [0.7]
    [BODY: Q_every → Q_some]
  interpretation_2: [0.3]
    [BODY: Q_some → Q_every]
```

---

## 8. 우아한 열화 (Graceful Degradation)

### 8.1 Entity 열화

정보 손실 시 상위 개념으로 대체:

```
100%: Q39930 (푸들)
 75%: Q144 (개)
 50%: Q7377 (포유류)
 25%: Q729 (동물)
```

### 8.2 참여자 열화

**핵심: 개체 정보는 손실돼도 의미역은 보존**

```
완전 정보:
[PARTICIPANT: verb → Q39930(푸들), role=AGT]

열화 후:
[PARTICIPANT: verb → Q729(동물), role=AGT]
              ↑ 상위 개념       ↑ 역할 보존
```

### 8.3 동사 열화

```
100%: acquire.v.01 (인수하다)
 50%: get.v.01 (얻다)
 25%: act.v.01 (행하다)
```

---

## 9. 사용 예시

### 9.1 단순 문장

**"Paris is the capital of France"**

```
[Entity: Q90 (Paris)]
[Entity: Q142 (France)]
[Verb: be.v.01]
[Entity: capital.n.01]

[PARTICIPANT: be.v.01 → Q90, role=THM]
[PARTICIPANT: be.v.01 → capital.n.01, role=ATR]
[PROPERTY: Q90, P1376:capital_of, Q142]
```

### 9.2 복합 문장

**"철수가 영희에게 책을 줬다"**

```
[Entity: TID=0x01] // 철수
[Entity: TID=0x02] // 영희
[Entity: TID=0x03] // 책
[Verb: give.v.01, Tense=-0.8, Aspect=2]

[PARTICIPANT: give.v.01 → 철수, role=AGT]
[PARTICIPANT: give.v.01 → 책, role=THM]
[PARTICIPANT: give.v.01 → 영희, role=RCP]
```

### 9.3 복잡한 전치사 구문

**"비 때문에 친구와 함께 집에서 학교로 빠르게 뛰어갔다"**

```
[Entity: TID=0x01] // 화자 (생략된 주어)
[Entity: TID=0x02] // 비
[Entity: TID=0x03] // 친구
[Entity: TID=0x04] // 집
[Entity: TID=0x05] // 학교
[Verb: run.v.01, Tense=-0.8, Aspect=2]

[PARTICIPANT: run.v.01 → 0x01, role=AGT]
[PARTICIPANT: run.v.01 → 0x02, role=CAU]  // 비 때문에
[PARTICIPANT: run.v.01 → 0x03, role=COM]  // 친구와
[PARTICIPANT: run.v.01 → 0x04, role=SRC]  // 집에서
[PARTICIPANT: run.v.01 → 0x05, role=DST]  // 학교로
[PARTICIPANT: run.v.01 → quickly, role=MNR]  // 빠르게
```

### 9.4 상태 서술

**"하늘이 매우 파랗다"**

```
[Entity: sky.n.01]
[Verb: be.v.01]
[Entity: blue.a.01]

[PARTICIPANT: be.v.01 → sky.n.01, role=THM]
[PARTICIPANT: be.v.01 → blue.a.01, role=ATR, focus=0xF]
[MOD: very → blue.a.01, mod_type=degree]
```

### 9.5 내포문

**"대부분의 과학자들이 그 이론이 매우 중요하다고 생각했다"**

```
// 외부 서술
[Verb: think.v.01, Tense=-0.8]
[Quantifier: most, TID=0x20]

[PARTICIPANT: think.v.01 → scientist.n.01, role=EXP, quant_ref=0x20, focus=0x3]
[PARTICIPANT: think.v.01 → Statement_002, role=THM, focus=0xE]

// 내포된 서술 (Statement_002)
[Verb: be.v.01]
[PARTICIPANT: be.v.01 → theory.n.01, role=THM]
[PARTICIPANT: be.v.01 → important.a.01, role=ATR, focus=0xF]
[MOD: very → important.a.01]
```

### 9.6 수동태

**"The book was given to Mary by John"**

```
[Entity: book.n.01]
[Entity: Mary (Q...)]
[Entity: John (Q...)]
[Verb: give.v.01, Tense=-0.8]

// 의미역은 능동태와 동일
[PARTICIPANT: give.v.01 → John, role=AGT, gram_role=0]  // 전치사구
[PARTICIPANT: give.v.01 → book, role=THM, gram_role=1]  // 문법적 주어
[PARTICIPANT: give.v.01 → Mary, role=RCP, gram_role=2]  // 간접목적어
```

**핵심:** 문법적 역할(gram_role)과 의미역(role)을 분리하여 수동태/능동태 변환에 강건.

---

## 10. RuleDB 연동

### 10.1 패턴 구조

GEUL 인코더의 RuleDB에서 사용하는 패턴:

```json
{
  "verb_synset": "give.v.01",
  "participants": [
    {"role": "AGT", "type_mask": "0x0..."},  // Human
    {"role": "THM", "type_mask": "0x4..."},  // Work/Product
    {"role": "RCP", "type_mask": "0x0..."}   // Human
  ]
}
```

### 10.2 SIDX 기반 매칭

```
패턴 해시 = verb_sidx[0:32] | role_bitmap[0:16] | type_masks[0:16]

매칭:
  (entity.sidx & pattern.type_mask) == pattern.type_mask
```

### 10.3 능동/수동 정규화

MRS 파싱 단계에서 의미역 정규화 → RuleDB는 동일 패턴으로 처리

| 표면형 | Agent | Theme | Recipient |
|--------|-------|-------|-----------|
| "John gave Mary a book" | John | book | Mary |
| "A book was given to Mary by John" | John | book | Mary |

---

## 11. 다국어 지원

### 11.1 원칙

- SIDX는 언어 중립적
- QID/Synset도 언어 독립적
- 의미역 체계 공유

### 11.2 예시

```
"사과를 먹다" (한국어)
→ [Entity: Q89 (apple)]
  [Verb: eat.v.01]
  [PARTICIPANT: eat.v.01 → Q89, role=THM]

"eat an apple" (영어)
→ 동일한 GEUL 구조
```

### 11.3 파서 계획

| 언어 | 파서 | 상태 |
|------|------|------|
| 영어 | ERG + ACE | v1.0 |
| 한국어 | Korean Resource Grammar | v1.5 계획 |
| 중국어 | Chinese MRS Parser | v1.5 계획 |
| 일본어 | JACY Grammar | v1.5 계획 |

---

## 12. 구현 체크리스트

### 12.1 MVP (6개월)

**기반:**
- [ ] MRS 파서 통합 (ERG/ACE)
- [ ] QID/Synset 통합 DB
- [ ] 16개 의미역 인코딩

**파이프라인:**
- [ ] ID 후보 리스팅
- [ ] GPT Pruning
- [ ] PARTICIPANT Edge 생성

**검증:**
- [ ] 10만 골든셋
- [ ] 의미역 정확도 90%+

### 12.2 v1.0 (1년)

- [ ] 의미 중첩 자동 처리
- [ ] Focus 자동 계산
- [ ] Quantifier 범위 처리
- [ ] Context-Claim WMS 통합

### 12.3 v2.0 (3년)

- [ ] 다국어 지원
- [ ] 실시간 인코딩
- [ ] ISO/W3C 표준화

---

## 부록 A: 용어집

| 용어 | 정의 |
|------|------|
| **SIDX** | Semantic-aligned Index. 64비트 의미정렬 식별자 |
| **TID** | Temporary ID. 스트림 내 임시 참조 |
| **QID** | 위키데이터 Item ID (Q312 = Apple Inc.) |
| **Synset** | 워드넷 동의어 집합 (apple.n.01) |
| **MRS** | Minimal Recursion Semantics |
| **PARTICIPANT** | 사건 참여자를 연결하는 Edge |
| **SemanticRole** | 의미역 (Agent, Theme 등) |
| **Focus** | 화용론적 강조도 (0.0~1.0) |
| **WMS** | World Management System |
| **Context** | 서술의 귀속 범위 |
| **Claim** | 진술의 최소 단위 |

---

## 부록 B: 의미역 전체 목록 (16개)

### B.1 핵심 참여자

| ID | 코드 | 역할 | 정의 |
|----|------|------|------|
| 0x0 | AGT | Agent | 의도적 행위자 |
| 0x1 | EXP | Experiencer | 경험/인지 주체 |
| 0x2 | THM | Theme | 이동/기술 대상 |
| 0x3 | PAT | Patient | 상태 변화 대상 |
| 0x4 | RCP | Recipient | 수령자 |
| 0x5 | BNF | Beneficiary | 수익자 |

### B.2 도구/방식

| ID | 코드 | 역할 | 정의 |
|----|------|------|------|
| 0x6 | INS | Instrument | 도구 |
| 0x7 | MNR | Manner | 방식 |

### B.3 공간

| ID | 코드 | 역할 | 정의 |
|----|------|------|------|
| 0x8 | LOC | Location | 장소 |
| 0x9 | SRC | Source | 출발점 |
| 0xA | DST | Destination | 목적지 |
| 0xB | PTH | Path | 경로 |

### B.4 원인/목적

| ID | 코드 | 역할 | 정의 |
|----|------|------|------|
| 0xC | CAU | Cause | 원인 |
| 0xD | PRP | Purpose | 목적 |

### B.5 기타

| ID | 코드 | 역할 | 정의 |
|----|------|------|------|
| 0xE | COM | Comitative | 동반 |
| 0xF | ATR | Attribute | 속성 |

### B.6 참여자가 아닌 것들

다음은 **참여자 의미역이 아님**:

| 정보 | 처리 위치 |
|------|----------|
| Time (시간) | 동사 한정자 Tense + Temporal Node |
| Duration (기간) | Temporal Node |
| Frequency (빈도) | Iterativity Node |
| Speaker (화자) | Context/Claim |
| Listener (청자) | Context/Claim |
| Source (정보출처) | Context/Claim |

---

## 부록 C: 참고 문서

**핵심 문서:**
- `GEUL_비트명세.md` - 64비트 SIDX 구조 상세
- `참여자.md` - Participant 구조 상세 (v0.2)
- `동사_의미_한정자_목록.md` - 동사 한정자 상세
- `개체_상위_분류.md` - 16개 Entity 타입
- `Context-Claim.md` - WMS Context/Claim 명세
- `GEUL_인코더.md` - 심볼릭 인코더 설계
- `GEUL_부트스트랩_전략.md` - 데이터셋 구축 방법

**관련 연구:**
- VerbNet: 동사 프레임 DB
- FrameNet: 의미 프레임 DB
- PropBank: 의미역 코퍼스
- MRS (Copestake et al.): 논리 의미론

---

**문서 종료**

**버전:** v0.2  
**작성일:** 2026-01-26  
**주요 개정:**
- 참여자 16개 표준화 (부록 B)
- PARTICIPANT를 Edge 기반으로 통일
- 시간 역할을 참여자에서 제거
- Speaker/Listener/Source를 Context/Claim으로 분리
- Entity 상위 분류 16개 통합
- 예시 오류 수정