# GEUL 통합 문법 명세서 v1.1

**작성일:** 2026-01-26  
**상태:** 표준 초안 (DRAFT)  
**개정:** ARG 구조 → 참여자 명시 구조로 전환  
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

GEUL은 단순히 자연어를 "번역"하는 것이 아니라, 자연어가 내포한 **모든 의미적 정보를 명시적이고 계산 가능한 형태로 외부화(Externalization)**한다. 이를 통해 AI는 추측이 아닌 **계산**으로 언어를 처리할 수 있게 된다.

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
- 참여자(Participant) 구조로 의미역 명시

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
  - Participant 노드들
  - Context 노드들
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

**Entity (개체):**
- 사람, 장소, 사물, 조직, 개념
- QID (위키데이터) 또는 Synset (워드넷) 기반
- 구체적 실체와 추상 개념 모두 포함

**Verb (동사):**
- 행위, 상태, 관계
- Synset 기반 의미 식별
- 동사 프레임 정보 포함

**Participant (참여자):**
- 사건/상태에 관여하는 개체의 역할 정보
- EntityRef + SemanticRole + 메타데이터
- 의미역 명시화의 핵심

**Context (관점):**
- 서술의 귀속 범위
- 다중 관점 지원
- WMS 전용 노드

**Claim (서술):**
- 진술의 최소 단위
- Context에 귀속
- 출처/신뢰도 메타데이터 포함

**Quantifier (한정자):**
- every, some, most 등
- 논리적 범위 정의
- 한정사 의미 명시

### 3.2 식별자 규칙

#### 3.2.1 Entity 식별자

**고유 개체 (Instance):**

위키데이터 Q-ID를 표준으로 사용한다.

```
예: Q312 = Apple Inc.
    Q2766 = iPhone
    Q19837 = Steve Jobs

SIDX 구조 (64비트):
bit 1:     0 (GEUL Standard)
bit 2:     0 (Node)
bit 3:     0 (개체/동사/컨텍스트 그룹)
bit 4:     0 (Entity)
bit 5-32:  속성 약식 표현 (28비트)
           - is_human, is_organization, is_living 등
bit 33-64: 로컬 ID (32비트)
           - Q-ID 번호 직접 인코딩
```

**속성 약식 표현 (bit 5-32):**

의미정렬의 핵심 부분으로, 상위 비트부터 중요도 순으로 배치:
- bit 5: is_human (인간 여부)
- bit 6: is_organization (조직 여부)
- bit 7: is_living (생물 여부)
- bit 8: is_physical (물리적 실체 여부)
- bit 9-12: 지리적 위치 상위 분류
- bit 13-20: 시간적 범위 (역사적 시기)
- bit 21-28: 도메인별 특수 속성

이 설계로 SIMD 비트마스크 쿼리 시:
```
"인간이면서 조직의 리더인 개체"
→ (SIDX & 0x1800000000000000) == 0x1800000000000000
```
와 같은 고속 필터링 가능.

**범주 개념 (Category):**

워드넷 Synset-ID를 사용한다.

```
예: apple.n.01 = 과일 사과
    person.n.01 = 사람 (범주)
    scientist.n.01 = 과학자

SIDX 구조:
bit 1-4:   0001 (범주 타입)
bit 5-32:  Synset 메타 정보
bit 33-64: Synset ID 인코딩
```

**범주와 인스턴스 관계:**
- 범주: "사과(과일)"
- 인스턴스: "이 빨간 사과" (특정 개체)

GEUL은 둘을 명확히 구분하며, 필요시 인스턴스 → 범주 변환으로 우아한 열화 구현.

#### 3.2.2 Verb 식별자

워드넷 Synset-ID를 필수로 사용한다.

```
예: release.v.01 = 출시하다
    run.v.01 = 달리다
    think.v.01 = 생각하다

SIDX 구조 (64비트):
bit 1-4:   타입 플래그
bit 5-32:  동사 한정사 (modifiers)
           - 시제, 상, 양태 정보
bit 33-64: Verb Synset ID
```

**동사 한정사 (bit 5-32):**
- bit 5-8: 시제 (과거/현재/미래)
- bit 9-12: 상 (완료/진행/단순)
- bit 13-16: 양태 (가능/의무/추측)
- bit 17-24: 부정 플래그 및 강도
- bit 25-32: 기타 문법 범주

**VerbNet 프레임 매핑:**

동사 Synset은 가능한 경우 VerbNet 프레임과 매핑된다:
```
release.v.01 → VerbNet class 10.2
  기본 프레임: Agent releases Theme
  
give.v.01 → VerbNet class 13.1
  기본 프레임: Agent gives Theme to Recipient
```

이 매핑 정보는 참여자 의미역 자동 판단에 활용된다.

#### 3.2.3 대명사 처리

대명사는 GEUL의 핵심 도전 과제 중 하나다. 자연어의 대명사는 문맥에 따라 참조 대상이 달라지는데, GEUL은 이를 명시적으로 해소(Resolution)해야 한다.

**원칙:**
1. 모든 대명사는 참조 대상을 명시
2. TID (Temporary ID) 사용
3. 타입 정보 병기

**예시:**

```
자연어: "Steve Jobs founded Apple. He was a visionary."

GEUL:
[Entity: Q19837, "Steve Jobs"]
[Entity: Q312, "Apple"]
[Verb: found.v.01]
[Participant: P1]
  EntityRef: Q19837
  Role: Agent
  
[Verb: be.v.01]
[Participant: P2]
  EntityRef: TID_001 → Q19837  // "He" 해소
  Role: Theme
  Type: person.n.01  // 타입 명시
```

**대명사 해소 전략:**
1. MRS 파싱 단계에서 후보 추출
2. GPT가 문맥 기반 해소
3. 타입 불일치 검증 (he → 인간만 가능)
4. 거리 기반 우선순위 (가까운 것 우선)

**애매한 경우:**
```
"John told Bill that he was wrong."

GEUL:
[SUPERPOSITION]
  interpretation_1: [0.5]
    he → TID_001 → John
  interpretation_2: [0.5]
    he → TID_002 → Bill
```

의미 중첩으로 두 해석 모두 보존.

### 3.3 Root Type (상위 4비트)

GEUL 개체의 최상위 분류로, 위키데이터 사용 통계 기반 설계.

```
0x0: 추상 개념 (Abstract Concept)
     예: Q7184903(abstract), Q11471(time)
     
0x1: 물리 실체 (Physical Entity)
     예: Q223557(physical object)
     
0x2: 생물 (Biological)
     예: Q729(animal), Q756(plant)
     
0x3: 인간 (Human)
     예: Q5(human)
     
0x4: 조직 (Organization)
     예: Q43229(organization), Q4830453(business)
     
0x5: 장소 (Location)
     예: Q618123(geographical location)
     
0x6: 사건 (Event)
     예: Q1190554(occurrence)
     
0x7: 문헌/정보 (Document/Information)
     예: Q13442814(scholarly article)
     
0x8: 예술/창작물 (Creative Work)
     예: Q838948(work of art)
     
0x9: 인공물 (Artifact)
     예: Q39546(tool), Q811979(architectural structure)
     
0xA: 천체 (Astronomical Object)
     예: Q523(star), Q318(galaxy)
     
0xB: 화학/물질 (Chemical/Substance)
     예: Q11173(chemical element)
     
0xC: 데이터/형식 (Data/Format)
     예: Q1144928(data format)
     
0xD: 사회/역할 (Social Role)
     예: Q28640(profession)
     
0xE: 생태/지형 (Ecology/Geographical Feature)
     예: Q8502(mountain)
     
0xF: 기타/예약 (Reserved)
     예: 향후 확장용
```

**Root Type 활용:**

1. **고속 필터링:**
```
"모든 인간 찾기"
→ SIDX & 0x3000000000000000 == 0x3000000000000000
```

2. **타입 검증:**
```
"하늘을 날다" → Agent는 0x2(생물) 또는 0x9(항공기)만 가능
```

3. **우아한 열화:**
```
정보 손실 시 Root Type은 마지막까지 보존
```

---

## 4. 엣지 명세

### 4.1 WMS 코어 엣지

지식 그래프의 기본 관계를 표현하는 엣지들.

**Triple Edge:**
```
형식: (Subject) --[Property]-- (Object)
용도: 위키데이터 트리플 직접 수용
예: (Q312) --[P127:owned_by]-- (Q95)
    Apple Inc. --소유자--> Tim Cook

비트 구조:
bit 1:     0 (Standard)
bit 2:     1 (Edge)
bit 3-16:  0x0001 (Triple 타입)
bit 17-32: Property ID (위키데이터 P-ID)
bit 33-64: 추가 메타데이터
```

**Event6 Edge:**
```
형식: 6하원칙 다항 관계
필드: Who, What, Whom, When, Where, Why
용도: 복잡한 사건을 단일 엣지로 인코딩

예: "Steve Jobs unveiled iPhone at Macworld 2007"
[Event6]
  Who: Q19837 (Steve Jobs)
  What: Q2766 (iPhone)
  Action: unveil.v.01
  When: Q2024 (2007)
  Where: Q2919643 (Macworld)
  Why: [Context: product launch]
```

**Property Edge:**
```
형식: (Node) --[has_property]-- (Value)
용도: 개별 속성 분리 기술

예: (Q312) --[has_property:color]-- (red)
    (Person_X) --[has_property:age]-- (35)
```

**RELATION:**
```
형식: (Entity) --[관계명]-- (Entity)
용도: 일반적인 관계 연결

예: (Q19837) --[founded]-- (Q312)
    Steve Jobs --설립함--> Apple
```

**CONTEXT_LINK:**
```
형식: (Context) --[링크타입]-- (Context)
용도: 컨텍스트 간 상속/참조

링크 타입:
- inherits_from: 상속
- references: 참조
- contradicts: 모순
- extends: 확장

예: (Context_Fiction) --[extends]-- (Context_RealWorld)
```

### 4.2 MRS 기반 서술 엣지 (개정)

문장의 논리 구조를 표현하는 엣지들. **v1.1에서 ARG 구조를 참여자 구조로 대체.**

#### 4.2.1 PARTICIPANT 엣지 (핵심 개정)

**구 버전 (v1.0):**
```
ARG1, ARG2, ARG3, ARG4로 논항 연결
문제: 의미역이 암시적, 동사마다 다름
```

**신 버전 (v1.1):**
```
PARTICIPANT 엣지로 통합
의미역을 명시적으로 표현
```

**형식:**
```
(Verb) --[PARTICIPANT]-- (Participant_Node)
```

**Participant 노드 구조:**
```json
{
  "EntityRef": "SIDX or TID",     // 필수: 참조 개체
  "SemanticRole": "Agent/Theme/...", // 필수: 의미역
  "Focus": 0.0-1.0,                // 선택: 화용론적 강조
  "QuantifierRef": "SIDX",         // 선택: 한정자 참조
  "GrammaticalRole": "subject/object" // 선택: 문법 역할
}
```

**주요 의미역 (SemanticRole) 목록:**

**핵심 역할:**
- **Agent**: 의도적 행위자
  - 예: "John opened the door" → John = Agent
- **Theme/Patient**: 행위의 대상
  - 예: "John opened the door" → door = Theme
- **Experiencer**: 감정/인지 주체
  - 예: "Mary loves music" → Mary = Experiencer
- **Recipient**: 수취인
  - 예: "John gave Mary a book" → Mary = Recipient
- **Beneficiary**: 수혜자
  - 예: "John bought a gift for Mary" → Mary = Beneficiary

**공간 역할:**
- **Location**: 장소
  - 예: "in Seoul"
- **Source**: 출발지
  - 예: "from Seoul"
- **Destination**: 목적지
  - 예: "to Busan"
- **Path**: 경로
  - 예: "through the tunnel"

**시간 역할:**
- **Time**: 시점
  - 예: "at 3pm"
- **Duration**: 기간
  - 예: "for 3 hours"
- **Frequency**: 빈도
  - 예: "twice a day"

**방법/도구:**
- **Instrument**: 도구
  - 예: "with a knife"
- **Manner**: 방식
  - 예: "carefully"
- **Means**: 수단
  - 예: "by train"

**원인/목적:**
- **Cause**: 원인
  - 예: "because of rain"
- **Purpose**: 목적
  - 예: "to learn"
- **Result**: 결과
  - 예: "resulting in success"

**기타:**
- **Accompaniment**: 동반
  - 예: "with friends"
- **Topic**: 주제
  - 예: "about politics"
- **Attribute**: 속성
  - 예: "as important"

**예시 1: 단순 문장**

```
자연어: "Apple released iPhone in 2007"
동사: release.v.01

GEUL:
[Verb: release.v.01, VID_001]

[Participant: P1]
  EntityRef: Q312 (Apple Inc.)
  SemanticRole: Agent
  Focus: 0.3

[Participant: P2]
  EntityRef: Q2766 (iPhone)
  SemanticRole: Theme
  Focus: 0.9

[Participant: P3]
  EntityRef: Q2024 (2007)
  SemanticRole: Time
  Focus: 0.2

[PARTICIPANT: VID_001 → P1]
[PARTICIPANT: VID_001 → P2]
[PARTICIPANT: VID_001 → P3]
```

**예시 2: 전치사 의미역**

```
자연어: "서울에서 부산까지 기차로 갔다"
동사: go.v.01

GEUL:
[Verb: go.v.01]

[Participant: P1]
  EntityRef: TID_person (대명사 해소)
  SemanticRole: Agent

[Participant: P2]
  EntityRef: Q8684 (서울)
  SemanticRole: Source  // "에서" → Source

[Participant: P3]
  EntityRef: Q16520 (부산)
  SemanticRole: Destination  // "까지" → Destination

[Participant: P4]
  EntityRef: train.n.01
  SemanticRole: Means  // "로" → Means
```

**예시 3: 복잡한 의미역**

```
자연어: "John gave Mary a book for her birthday"
동사: give.v.01

GEUL:
[Verb: give.v.01]

[Participant: P1]
  EntityRef: John_ID
  SemanticRole: Agent
  
[Participant: P2]
  EntityRef: Mary_ID
  SemanticRole: Recipient
  
[Participant: P3]
  EntityRef: book.n.01
  SemanticRole: Theme
  
[Participant: P4]
  EntityRef: birthday_ID
  SemanticRole: Purpose
```

#### 4.2.2 의미역 자동 판단 전략

**1. VerbNet 기반 매핑 (우선):**
```python
# VerbNet에 동사 프레임 있는 경우
if verb_synset in verbnet_db:
    frame = verbnet_db[verb_synset]
    # give.v.01 → Agent gives Theme to Recipient
    auto_assign_roles(frame)
```

**2. GPT 추론 (폴백):**
```python
prompt = f"""
문장: {sentence}
동사: {verb_synset}
개체: {entities}

각 개체의 의미역을 다음 중 선택:
Agent, Theme, Experiencer, Recipient, Beneficiary,
Location, Source, Destination, Time, Instrument,
Manner, Cause, Purpose

JSON 출력:
"""

# GPT가 의미역 판단
roles = gpt_semantic_role_tagger(prompt)
```

**3. 타입 제약 검증:**
```python
# 타입 불일치 검사
if role == "Agent":
    assert is_animate(entity)  # Agent는 생물이어야
    
if role == "Instrument":
    assert is_physical(entity)  # 도구는 물리적 실체
```

**4. 통계 기반 보정:**
```python
# 코퍼스 통계로 이상한 조합 거부
if (verb, role, entity_type) not in common_patterns:
    flag_for_review()
```

#### 4.2.3 Focus (화용론적 강조)

문장에서 어떤 참여자가 "새로운 정보"인지, "강조"되는지 명시.

```
예: "영희를 사랑하는 사람은 철수다"

[Participant: P1 - 영희]
  Role: Theme
  Focus: 0.2  // 구정보

[Participant: P2 - 철수]
  Role: Experiencer
  Focus: 1.0  // 신정보, 강조됨
```

AI가 답변 생성 시 Focus 값이 높은 참여자를 강조해서 표현.

#### 4.2.4 QuantifierRef (한정자 참조)

논리적 범위를 명시하는 한정자 연결.

```
예: "Every student passed the exam"

[Participant: P1]
  EntityRef: student.n.01
  Role: Agent
  QuantifierRef: every_QID
  
[Quantifier: every_QID]
  Type: universal
  Scope: [pass.v.01]
```

한정자 종류:
- **every**: 전칭 (∀)
- **some**: 존재 (∃)
- **most**: 대다수
- **few**: 소수
- **no**: 부정 전칭 (¬∃)

#### 4.2.5 MOD (Modifier)

수식 관계를 표현.

```
형식: (Modifier) --[MOD]-- (Modified)

예: "red apple"
    "red" --[MOD]-- "apple"
    
예: "run quickly"
    "quickly" --[MOD]-- "run"

비트 구조:
bit 3-16: 0x0010 (MOD 타입)
bit 17-32: 수식 종류 (형용사/부사/관계절)
```

#### 4.2.6 COMPOUND

복합어 내부 결합.

```
예: "ice cream"
    "ice" --[COMPOUND]-- "cream"
    
예: "New York"
    "New" --[COMPOUND]-- "York"
```

#### 4.2.7 RSTR/BODY (한정자 범위)

**RSTR (Restriction):**
한정자가 제한하는 대상.

```
예: "every student"
    "every" --[RSTR]-- "student"
```

**BODY (Scope Body):**
한정자의 논리적 영향 범위.

```
예: "every student passed"
    "every" --[BODY]-- "passed"
    
논리식: ∀x(student(x) → passed(x))
```

#### 4.2.8 QEQ (Quasi-Equality)

느슨한 범위 연결. 의미 중첩 구현의 기술적 토대.

```
용도: 논리적 범위가 명확하지 않을 때
예: "John wants to succeed"
    want.v.01 --[QEQ]-- succeed.v.01
    (want의 범위가 succeed를 포함하지만 엄격하지 않음)
```

#### 4.2.9 CONJ (Conjunction)

대등 연결.

```
예: "John and Mary"
    John --[CONJ]-- Mary
    
예: "read or write"
    read --[CONJ]-- write
```

### 4.3 프로그래밍/제어 엣지

AI의 절차적 지식을 외부화하는 엣지들.

**IF_THEN_ELSE:**
```
용도: 조건부 분기
구조:
  (Condition) --[IF]-- (True_Branch)
              --[ELSE]-- (False_Branch)

예: "만약 비가 오면 우산을 가져가라"
    [IF: is_raining]
      --[THEN]-- [bring_umbrella]
```

**LOOP_FOR / LOOP_WHILE:**
```
용도: 반복 실행

FOR:
  (Variable) --[LOOP_FOR]-- (Range)
             --[BODY]-- (Statements)

WHILE:
  (Condition) --[LOOP_WHILE]-- (Body)

예: "1부터 10까지 출력하라"
    [FOR: i IN range(1,10)]
      --[BODY]-- [print(i)]
```

**SWITCH_CASE:**
```
용도: 다중 조건 분기
구조:
  (Input) --[CASE_1]-- (Branch_1)
          --[CASE_2]-- (Branch_2)
          --[DEFAULT]-- (Branch_Default)
```

**FUNC_DEF / FUNC_CALL:**
```
FUNC_DEF: 함수 정의
  (Function) --[has_param]-- (Param)
             --[has_body]-- (Body)
             --[returns]-- (ReturnType)

FUNC_CALL: 함수 호출
  (Call) --[invokes]-- (Function)
         --[with_args]-- (Args)

예: "factorial(n) = n * factorial(n-1)"
    [FUNC_DEF: factorial]
      --[param]-- n
      --[body]-- [multiply operation]
```

**VAR_DECL / ASSIGN:**
```
VAR_DECL: 변수 선언
  (Variable) --[VAR_DECL]-- (Type)

ASSIGN: 값 할당
  (Variable) --[ASSIGN]-- (Value)

예: "x = 10"
    [VAR: x] --[ASSIGN]-- [Value: 10]
```

**BLOCK:**
```
용도: 스코프 구분
  (Block) --[contains]-- (Statements)
  
예: Python 함수 내부
    [BLOCK: function_body]
      --[contains]-- [statement1]
      --[contains]-- [statement2]
```

**COMPARE:**
```
용도: 비교 연산
타입: LT(<), GT(>), EQ(==), NE(!=), LE(<=), GE(>=)

예: "x > 10"
    [Compare: GT]
      --[left]-- [x]
      --[right]-- [10]
```

### 4.4 메타/성찰 엣지

지식의 출처, 신뢰도, 관계를 관리하는 엣지들.

**IN_CONTEXT:**
```
형식: (Claim) --[IN_CONTEXT]-- (Context)
용도: 서술이 어떤 관점에 귀속되는지 명시

예: (Claim_flat_earth) --[IN_CONTEXT]-- (Context_medieval)
```

**SUPPORTS / CONTRADICTS:**
```
형식: 
  (Claim_A) --[SUPPORTS]-- (Claim_B)
  (Claim_A) --[CONTRADICTS]-- (Claim_C)

용도: 서술 간 논리적 관계

예: 
  (Claim: "날씨 맑음") --[SUPPORTS]-- (Claim: "소풍 가능")
  (Claim: "비 옴") --[CONTRADICTS]-- (Claim: "날씨 맑음")
```

**SOURCE / DERIVES_FROM:**
```
형식:
  (Claim) --[SOURCE]-- (Document/Person)
  (Claim_B) --[DERIVES_FROM]-- (Claim_A)

용도: 출처 추적

예:
  (Claim: "지구는 둥글다") --[SOURCE]-- (Document: NASA_report_2020)
  (Claim: "따라서 항해 가능") --[DERIVES_FROM]-- (Claim: "지구는 둥글다")
```

**CONFIDENCE:**
```
형식: (Claim) --[CONFIDENCE]-- (Score)
용도: 신뢰도 연결
범위: 0.0 ~ 1.0

예: (Claim: "내일 비") --[CONFIDENCE]-- 0.7
```

**HAS_MEMBER:**
```
형식: (PIDX) --[HAS_MEMBER]-- (SIDX)
용도: 패턴 인덱스 멤버십

예: (PIDX: "급등주") --[HAS_MEMBER]-- (SIDX: Tesla_stock)
                    --[HAS_MEMBER]-- (SIDX: NVIDIA_stock)
```

**SEMANTIC_SUPERPOSITION:**
```
형식: (Node) --[SUPERPOSITION]-- [(I1, p1), (I2, p2), ...]
용도: 중의적 해석 병렬 보존
확률: 각 해석에 가중치 부여

예: "The chicken is ready to eat"
    [SUPERPOSITION]
      interpretation_1: [0.5] chicken eats
      interpretation_2: [0.5] eat chicken
```

---

## 5. 문법 규칙

### 5.1 패킷 구조

**노드 패킷:**
```
[SIDX: 4 WORD = 64비트]
  bit 1:     Standard(0) / Extension(1)
  bit 2:     Node(0) / Edge(1)
  bit 3-4:   노드 타입 (Entity/Verb/...)
  bit 5-32:  속성/메타데이터
  bit 33-64: 고유 ID
```

**엣지 패킷:**
```
[Edge Header: 1 WORD]
  bit 1:     Standard(0) / Extension(1)
  bit 2:     Kind = Edge(1)
  bit 3-16:  Edge Type (14비트)
  
[Source SIDX: 4 WORD]
[Target SIDX: 4 WORD]

전체: 9 WORD = 18바이트
```

**Participant 노드 패킷:**
```
[Participant Header: 1 WORD]
  bit 1-8:   Participant 타입
  bit 9-16:  메타 플래그

[EntityRef: 4 WORD]
[SemanticRole: 2 WORD]
  - 의미역 SIDX 또는 표준 코드
  
[Focus: 1 WORD]
  - FP16 인코딩 (0.0~1.0)
  
[QuantifierRef: 4 WORD (선택)]

전체: 최소 8 WORD, 최대 12 WORD
```

### 5.2 스트림 예시

#### 예시 1: 단순 문장

```
입력: "Apple released iPhone in 2007"

GEUL 스트림:
[HEADER: 0x0001]  // 버전 1

// 노드들
[Entity: Q312]           // Apple Inc. (4 WORD)
[Entity: Q2766]          // iPhone (4 WORD)
[Entity: Q2024]          // 2007 (4 WORD)
[Verb: release.v.01]     // released (4 WORD)

// Participant 노드들
[Participant: P1]        // (8 WORD)
  EntityRef: Q312
  Role: Agent
  Focus: 0.3
  
[Participant: P2]        // (8 WORD)
  EntityRef: Q2766
  Role: Theme
  Focus: 0.9
  
[Participant: P3]        // (8 WORD)
  EntityRef: Q2024
  Role: Time
  Focus: 0.2

// 엣지들
[PARTICIPANT: release.v.01 → P1]  // (9 WORD)
[PARTICIPANT: release.v.01 → P2]  // (9 WORD)
[PARTICIPANT: release.v.01 → P3]  // (9 WORD)

총: 1 + 16 + 24 + 27 = 68 WORD = 136바이트
```

#### 예시 2: 복잡한 문장

```
입력: "Every student who studied hard passed the difficult exam"

GEUL 스트림:
// 한정자
[Quantifier: every_QID]

// 개체들
[Entity: student.n.01]
[Entity: exam.n.01]

// 동사들
[Verb: study.v.01]
[Verb: pass.v.01]

// 수식
[Adj: hard]
[Adj: difficult]

// Participants for "study"
[Participant: PS1]
  EntityRef: student.n.01
  Role: Agent
  QuantifierRef: every_QID
  
// Participants for "pass"
[Participant: PP1]
  EntityRef: student.n.01
  Role: Agent
  
[Participant: PP2]
  EntityRef: exam.n.01
  Role: Theme

// 엣지들
[PARTICIPANT: study.v.01 → PS1]
[PARTICIPANT: pass.v.01 → PP1]
[PARTICIPANT: pass.v.01 → PP2]
[MOD: hard → study.v.01]
[MOD: difficult → exam.n.01]
[RSTR: every_QID → student.n.01]
[BODY: every_QID → pass.v.01]
```

### 5.3 의미 중첩 표현

```
입력: "I saw the man with the telescope"

해석 1 (60%): 망원경으로 (도구)
  with --[MOD]-- saw
  telescope --[Participant:Instrument]-- saw

해석 2 (40%): 망원경을 가진 (소유)
  with --[MOD]-- man
  telescope --[Participant:Possession]-- man

GEUL:
[Entity: I]
[Entity: man]
[Entity: telescope]
[Verb: see.v.01]
[Preposition: with]

[SUPERPOSITION_NODE]
  interpretations: [
    {
      probability: 0.6,
      structure: [
        [Participant: P1]
          EntityRef: telescope
          Role: Instrument
          
        [PARTICIPANT: see.v.01 → P1]
        [MOD: with → see.v.01]
      ]
    },
    {
      probability: 0.4,
      structure: [
        [Participant: P2]
          EntityRef: telescope
          Role: Possession
          
        [PARTICIPANT: man → P2]
        [MOD: with → man]
      ]
    }
  ]
```

---

## 6. 구현 전략 (MVP)

### 6.1 파이프라인

```
[입력] 자연어 문장
  ↓
[Stage 1] MRS 파싱
  - ERG/ACE 파서 사용
  - 초기 그래프 뼈대 생성
  - 의존 구조 추출
  ↓
[Stage 2] ID 후보 리스팅
  - 명사 → 위키데이터 Q-ID 후보 20개
  - 동사 → 워드넷 Synset 후보 20개
  - 대명사 → 참조 후보 추출
  ↓
[Stage 3] GPT Pruning (가지치기)
  - 문맥상 불가능한 조합 제거
  - 타입 제약 검증
  - 20개 → 평균 1.2개로 축소
  ↓
[Stage 4] 의미역 판단 (신규)
  - VerbNet 프레임 조회 (우선)
  - GPT 기반 의미역 추론 (폴백)
  - Agent, Theme 등 자동 판정
  ↓
[Stage 5] Participant 노드 생성 (신규)
  - EntityRef 할당
  - SemanticRole 할당
  - Focus 계산 (선택)
  - QuantifierRef 연결 (선택)
  ↓
[Stage 6] 의미 중첩 표기
  - 남은 유효 해석들 병렬 보존
  - 확률 가중치 부여
  ↓
[출력] GEUL 스트림
```

### 6.2 Pruning 전략

#### Stage 3: ID 가지치기

```python
prompt_template = """
문장: {sentence}

명사 후보:
{noun_candidates}

동사 후보:
{verb_candidates}

지시사항:
1. 문맥상 불가능한 조합을 제거하세요
2. 가장 자연스러운 해석을 우선하세요
3. 드문 의미는 제외하세요

JSON 출력:
{{
  "entities": {{"단어": "QID", ...}},
  "verbs": {{"단어": "Synset", ...}}
}}
"""

# GPT 호출
result = gpt_4o_mini(prompt_template.format(...))

# 비용: ~$0.001/문장
```

#### Stage 4: 의미역 판단 (신규)

```python
semantic_role_prompt = """
문장: {sentence}
동사: {verb_synset}
개체들: {entities}

각 개체의 의미역을 판단하세요.

의미역 종류:
- Agent: 의도적 행위자
- Theme/Patient: 행위 대상
- Experiencer: 경험 주체
- Recipient: 수취인
- Beneficiary: 수혜자
- Location: 장소
- Source: 출발지
- Destination: 목적지
- Time: 시간
- Instrument: 도구
- Manner: 방식
- Cause: 원인
- Purpose: 목적

JSON 출력:
{{
  "participants": [
    {{"entity": "QID", "role": "Agent"}},
    {{"entity": "QID", "role": "Theme"}},
    ...
  ]
}}
"""

# GPT 호출
roles = gpt_sonnet_4_5(semantic_role_prompt.format(...))

# 비용: ~$0.0075/문장
```

**검증 로직:**
```python
def validate_semantic_role(entity_type, role):
    """타입 제약 검증"""
    if role == "Agent":
        return entity_type in ["Human", "Organization", "Biological"]
    if role == "Instrument":
        return entity_type in ["Artifact", "Physical"]
    if role == "Time":
        return entity_type in ["Event", "Abstract"]
    # ... 기타 제약
    return True
```

### 6.3 데이터셋 구축

**Phase 1: 10만 골든셋 (현재 진행)**

목표: 인간 검수 완료된 고품질 데이터

```
단계:
1. MRS 파싱 (자동)
2. ID 리스팅 (자동)
3. GPT Pruning (자동, $100)
4. 의미역 판단 (자동, $750)  // 신규
5. 샘플 검수 (인간, 1000개)
6. 전수 검증 (자동 + 인간)

총 비용: ~$850 + 인건비
기간: 2개월
```

**샘플 데이터:**
```json
{
  "natural": "Apple released iPhone in 2007",
  "geul": {
    "nodes": [
      {"type": "Entity", "id": "Q312", "label": "Apple Inc."},
      {"type": "Entity", "id": "Q2766", "label": "iPhone"},
      {"type": "Entity", "id": "Q2024", "label": "2007"},
      {"type": "Verb", "id": "release.v.01"},
      {
        "type": "Participant",
        "id": "P1",
        "EntityRef": "Q312",
        "SemanticRole": "Agent",
        "Focus": 0.3
      },
      {
        "type": "Participant",
        "id": "P2",
        "EntityRef": "Q2766",
        "SemanticRole": "Theme",
        "Focus": 0.9
      },
      {
        "type": "Participant",
        "id": "P3",
        "EntityRef": "Q2024",
        "SemanticRole": "Time",
        "Focus": 0.2
      }
    ],
    "edges": [
      {"type": "PARTICIPANT", "from": "release.v.01", "to": "P1"},
      {"type": "PARTICIPANT", "from": "release.v.01", "to": "P2"},
      {"type": "PARTICIPANT", "from": "release.v.01", "to": "P3"}
    ]
  }
}
```

**Phase 2: 1000만 자동생성셋**

```
데이터 소스:
- 위키피디아 문장
- 뉴스 기사 (CC News)
- 학술 논문 초록
- 오픈 도메인 대화

생성 방법:
- 전체 자동 파이프라인
- 인간 검수 없음
- 실험/연구용

총 비용: ~$85,000
기간: 3개월 (병렬 처리)
```

**Phase 3: 커뮤니티 확장**

```
플랫폼: GEULpedia (위키 하위 프로젝트)
기여 방식:
- 자연어 → GEUL 변환 검증
- 오류 수정
- 도메인별 특화 데이터

보상:
- 기여자 랭킹
- 논문 공저자 자격
- 컨퍼런스 초대
```

---

## 7. 확장성

### 7.1 Proposal 레인 (`1100`)

표준 후보를 실험하는 공간.

```
비트 구조:
bit 1-4: 1100 (Proposal prefix)
bit 5-:  표준 문법 미러링

용도:
- 새로운 의미역 제안
- 새로운 엣지 타입 실험
- 도메인 특화 확장

승격 경로:
1. 커뮤니티 제안 (GitHub Issue)
2. 6개월 실험 (Proposal 레인 사용)
3. 충돌 검증 (자동 테스트)
4. RFC 투표 (커뮤니티 2/3 찬성)
5. Standard 승격 (010x prefix)
```

**예시: 새 의미역 제안**

```
제안: "Co-Agent" (공동 행위자)
예: "John and Mary built the house together"

Proposal 단계:
- 비트: 1100xxxx (Proposal)
- 실험 기간: 6개월
- 사용 통계 수집

Standard 승격 시:
- 비트: 010xxxxx (Standard)
- 공식 문서 추가
- Encoder/Decoder 업데이트
```

### 7.2 Extension 영역

기관별/도메인별 확장.

```
bit 1: 1 (Extension)
bit 2: 0 (Issuer) / 1 (Free)

Issuer 예시:
- 의료 기관: Medical 전용 의미역
- 법률 기관: Legal 전용 관계
- 기업: 내부 프로세스 표현

Free 예시:
- 개인 연구
- 프로토타입
- 임시 실험
```

### 7.3 다국어 확장

```
현재 (v1.0):
- 영어만 지원
- MRS (ERG) 파서

계획 (v1.5):
- 한국어: Korean Resource Grammar
- 중국어: Chinese MRS 파서
- 일본어: JACY Grammar

장점:
- SIDX는 언어 중립적
- QID/Synset도 언어 독립적
- 의미역 체계 공유

예: "사과를 먹다" (한국어)
   → Entity(Q89), Verb(eat.v.01)
   → Participant(Theme=Q89)
   
   "eat an apple" (영어)
   → 동일한 GEUL 구조
```

---

## 8. 참여자 구조 (상세)

### 8.1 참여자 철학

**핵심 원칙:**
- 문장 복잡성을 참여자 단위로 원자화
- 의미역을 명시적으로 외부화
- 문법 역할 ≠ 의미 역할 구분

**예시:**

```
"The book was given to Mary by John"

문법적:
- 주어: The book
- 간접목적어: Mary
- 행위자: John (전치사구)

의미적:
- Agent: John (진짜 행위자)
- Theme: The book (진짜 대상)
- Recipient: Mary (진짜 수취인)
```

GEUL은 **의미적 역할**을 명시함으로써 수동태/능동태 변환에 강건.

### 8.2 우아한 열화와 참여자

정보 손실 시 참여자 구조 활용:

```
완전 정보:
[Participant]
  EntityRef: Q39930 (푸들)
  Role: Agent
  Focus: 0.8

75% 정보:
[Participant]
  EntityRef: Q144 (개)  // 상위 개념
  Role: Agent           // 역할 보존
  Focus: 0.8

50% 정보:
[Participant]
  EntityRef: Q7377 (포유류)
  Role: Agent
  Focus: 0.8

25% 정보:
[Participant]
  EntityRef: Q729 (동물)
  Role: Agent
  Focus: 0.8
```

**핵심:**
- 개체 정보는 손실돼도
- **의미역은 끝까지 보존**
- 추론 가능성 유지

### 8.3 Focus 계산

화용론적 강조도를 자동 계산하는 전략:

**1. 정보 구조 분석:**
```python
def calculate_focus(sentence, entity):
    focus = 0.5  # 기본값
    
    # 문두/문미 위치
    if entity in sentence_start:
        focus += 0.2
    if entity in sentence_end:
        focus += 0.3
        
    # 강조 구문
    if "it is X that" in sentence:
        focus = 1.0
        
    # 대조 접속사
    if "but" in context and entity after "but":
        focus += 0.3
        
    # Wh-질문 초점
    if sentence.startswith("Who"):
        focus = 1.0
        
    return min(focus, 1.0)
```

**2. GPT 추론:**
```python
focus_prompt = """
문장: {sentence}
개체: {entity}

이 개체가 문장에서 얼마나 강조/중요한지 0.0~1.0로 평가:
- 0.0: 배경 정보
- 0.5: 보통
- 1.0: 핵심 초점

출력: {{"focus": 0.X}}
"""
```

### 8.4 한정자와 참여자

논리적 범위를 명시하는 복잡한 구조:

**예: "Every student read some book"**

```
[Quantifier: Q_every]
  Type: universal
  
[Quantifier: Q_some]
  Type: existential

[Participant: P_student]
  EntityRef: student.n.01
  Role: Agent
  QuantifierRef: Q_every
  
[Participant: P_book]
  EntityRef: book.n.01
  Role: Theme
  QuantifierRef: Q_some

[RSTR: Q_every → student.n.01]
[RSTR: Q_some → book.n.01]
[BODY: Q_every → read.v.01]

논리식: ∀s(student(s) → ∃b(book(b) ∧ read(s,b)))
```

**범위 모호성:**

```
"Every professor taught a course"

해석 1: ∀p ∃c (teach(p,c))
  "각 교수가 (각자 다른) 어떤 과목을 가르쳤다"
  
해석 2: ∃c ∀p (teach(p,c))
  "어떤 (같은) 과목을 모든 교수가 가르쳤다"

GEUL:
[SUPERPOSITION]
  interpretation_1: [0.7]
    [BODY: Q_every → Q_some]  // wide scope for every
  interpretation_2: [0.3]
    [BODY: Q_some → Q_every]  // wide scope for some
```

---

## 9. 사용 예시

### 9.1 단순 문장

```
입력: "Paris is the capital of France"

GEUL:
[Entity: Q90]  // Paris
[Entity: Q142]  // France
[Verb: be.v.01]  // is
[Entity: capital.n.01]  // capital

[Participant: P1]
  EntityRef: Q90
  Role: Theme
  
[Participant: P2]
  EntityRef: capital.n.01
  Role: Attribute

[Property: Q90, P1376:capital_of, Q142]
// 위키데이터 트리플도 병행 저장
```

### 9.2 복잡한 문장

```
입력: "대부분의 과학자들이 그 이론이 매우 중요하다고 생각했다"

GEUL:
// 외부 서술
[Verb: think.v.01]
[Participant: P1]
  EntityRef: scientist.n.01
  Role: Experiencer
  QuantifierRef: most_QID
  Focus: 0.2

[Participant: P2]
  EntityRef: Statement_Important_002
  Role: Theme
  Focus: 0.9

// 내포된 서술
[Statement: Statement_Important_002]
  [Verb: be.v.01]
  [Participant: P3]
    EntityRef: theory_ID
    Role: Theme
  [Participant: P4]
    EntityRef: important.a.01
    Role: Attribute
    Focus: 1.0
  [MOD: very → important.a.01]
```

### 9.3 의미 중첩

```
입력: "The chicken is ready to eat"

GEUL:
[Entity: chicken.n.01]
[Verb: be.v.02]  // ready
[Verb: eat.v.01]

[SUPERPOSITION]
  interpretation_1: [0.5]
    // 닭이 먹을 준비됨
    [Participant: P1]
      EntityRef: chicken.n.01
      Role: Agent
    [PARTICIPANT: eat.v.01 → P1]
    
  interpretation_2: [0.5]
    // 닭을 먹을 준비됨
    [Participant: P2]
      EntityRef: chicken.n.01
      Role: Theme
    [PARTICIPANT: eat.v.01 → P2]
```

### 9.4 복합 전치사

```
입력: "서울에서 부산까지 KTX로 3시간 동안 갔다"

GEUL:
[Verb: go.v.01]

[Participant: P1]
  EntityRef: TID_person
  Role: Agent

[Participant: P2]
  EntityRef: Q8684 (서울)
  Role: Source

[Participant: P3]
  EntityRef: Q16520 (부산)
  Role: Destination

[Participant: P4]
  EntityRef: KTX.n.01
  Role: Means

[Participant: P5]
  EntityRef: duration_3hours
  Role: Duration
```

각 전치사가 명시적 의미역으로 변환됨.

---

## 10. 구현 체크리스트

### 10.1 MVP (6개월)

**기반 구축:**
- [ ] MRS 파서 통합 (ERG/ACE)
- [ ] QID/Synset 통합 DB 구축
- [ ] VerbNet 프레임 DB 구축 (신규)

**파이프라인:**
- [ ] ID 후보 리스팅 엔진
- [ ] GPT Pruning 시스템
- [ ] 의미역 자동 판단 시스템 (신규)
- [ ] Participant 노드 생성기 (신규)

**데이터:**
- [ ] 10만 골든셋 완성
- [ ] 1000개 샘플 인간 검수
- [ ] 의미역 태깅 품질 검증 (신규)

**모델:**
- [ ] GEUL Encoder 학습
- [ ] GEUL Decoder 학습
- [ ] Participant 인식 정확도 90%+ (신규)

### 10.2 v1.0 (1년)

**고급 기능:**
- [ ] 의미 중첩 자동 처리
- [ ] Focus 자동 계산
- [ ] QuantifierRef 자동 연결
- [ ] Context-Claim WMS 통합

**확장:**
- [ ] PIDX 자동 생성
- [ ] 다국어 지원 (한중일)
- [ ] 도메인 특화 (의료/법률)

**생태계:**
- [ ] GEULpedia 위키 통합
- [ ] 커뮤니티 기여 시스템
- [ ] 1000만 자동생성셋 공개

### 10.3 v2.0 (3년)

**혁신 기능:**
- [ ] GEUL-to-Code 트랜스파일러
- [ ] 완전 자율 GEUL 생성
- [ ] 실시간 의미역 추론

**표준화:**
- [ ] ISO 표준 제출
- [ ] W3C 표준 제안
- [ ] 학계 벤치마크 확립

---

## 부록 A: 용어집

**SIDX (Semantic-aligned Index):**
의미정렬 식별자. 64비트(또는 256비트) 정수로 개체/동사를 고유하게 식별하며, 비트 자체에 의미 정보 내포.

**TID (Temporary ID):**
스트림 내 임시 참조 ID. 대명사 해소 등에 사용.

**QID (Q-ID):**
위키데이터 Item ID. 예: Q312 = Apple Inc.

**PID (P-ID):**
위키데이터 Property ID. 예: P127 = owned by

**Synset:**
워드넷의 동의어 집합. 예: apple.n.01 = 과일 사과

**MRS (Minimal Recursion Semantics):**
논리적 범위를 명확히 하는 의미 표현 체계.

**PIDX (Pattern Index):**
고비용 패턴 연산 결과를 저장하는 인덱스.

**WMS (World Management System):**
GEUL 기반 지식 관리 시스템.

**Participant:**
사건/상태에 참여하는 개체의 역할 정보를 담는 노드. v1.1의 핵심 개정.

**SemanticRole:**
참여자의 의미역. Agent, Theme, Experiencer 등.

**Focus:**
화용론적 강조도. 0.0 (배경) ~ 1.0 (핵심).

**QuantifierRef:**
한정자 참조. every, some, most 등.

---

## 부록 B: 참고 문서

**핵심 문서:**
- `GEUL 비트 명세서.md` - 64비트 SIDX 구조 상세
- `Edges.md` - 전체 엣지 타입 목록
- `참여자.md` - Participant 구조 상세 (v1.1 신규)
- `Context-Claim.md` - WMS Context/Claim 명세
- `부트스트랩 전략.md` - 데이터셋 구축 방법

**관련 연구:**
- VerbNet: 동사 프레임 DB
- FrameNet: 의미 프레임 DB
- PropBank: 의미역 코퍼스
- MRS (Copestake et al.): 논리 의미론

**구현 참조:**
- ERG (English Resource Grammar)
- ACE Parser
- spaCy (보조 파서)
- GPT-4o/Sonnet 4.5 (의미역 판단)

---

## 부록 C: 의미역 전체 목록

**핵심 역할 (Core Roles):**
- Agent, Theme, Patient, Experiencer, Stimulus
- Recipient, Beneficiary, Source, Goal

**공간 역할 (Spatial):**
- Location, Source, Destination, Path, Direction

**시간 역할 (Temporal):**
- Time, Duration, Frequency, StartTime, EndTime

**방법/도구 (Manner/Instrument):**
- Instrument, Manner, Means, Method

**원인/결과 (Causal):**
- Cause, Reason, Purpose, Result, Consequence

**동반/속성 (Accompaniment/Attribute):**
- Accompaniment, Comitative, Topic, Attribute, Material

**특수 역할 (Special):**
- Possession, Part, Whole, Container, Content

---

**문서 종료**

**버전:** v1.1  
**총 라인 수:** 1,847줄  
**개정 완료일:** 2026-01-26