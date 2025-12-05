# Rule컴파일.md  
버전: 0.1  
작성일: 2024-12-05  
대상: GWMS L2 Rule 레이어 설계

---

## 1. 개요

### 1.1 목적

이 문서는 **GWMS(World Management System)** 에서:

- **룰(Rule)을 그래프/GEUL 데이터로 저장**하면서도  
- **실행 시에는 최대한 빠르게 평가**하기 위해

룰을 **“정의 시점에는 데이터, 실행 시점에는 코드”** 로 다루는  
**Rule 컴파일 파이프라인**을 정의한다.

핵심 철학:

> **Rule = 데이터로서의 그래프(편집/버전 관리)  
> + 코드로서의 바이트코드(실행 / 고속 평가)**

---

## 2. 레이어 구조에서 Rule의 위치

GWMS는 대략 다음과 같은 세계 모델 레이어를 가진다고 가정한다.

- **L3: 서술 레이어 (Narrative)**
  - Event6 / Triple / 발화 / 로그 / 뉴스 / 소설 문장
- **L2: Rule 레이어 (Rule / Contract / Law)**
  - “이런 상황에서는 이렇게 처리해야 한다”는 규칙
  - 법, 사규, 게임 룰, 비즈니스 로직 등
- **L1: 월드 레이어 (World State)**
  - 현재 시점의 상태값: 잔고, HP, 재고, 관계, 플래그 등

**Rule 컴파일**은 L2 내부의 메커니즘이다:

- **입력:** 그래프로 정의된 Rule (GEUL 기반)
- **출력:** VM이 바로 실행할 수 있는 **컴파일된 룰(바이트코드/IR)**

---

## 3. Rule의 이중성: 데이터이자 코드

### 3.1 왜 Rule도 데이터여야 하는가

Rule은 다음과 같은 이유로 **그래프 데이터**로 저장되어야 한다.

- 버전 관리: `Rule_Tax@v1`, `Rule_Tax@v2` …
- 출처 기록: “어떤 문서 / 계약 / 법률에서 왔는가”
- 적용 범위: 어떤 월드/컨텍스트/기간에 유효한가
- 휴먼/AI 편집 가능: 자연어 → GEUL → Rule 그래프

따라서 Rule은 기본적으로 **Node + Edge**로 표현된다.

예시(개념):

- `Node: Rule_Murder@v3`
- `Edge: [Rule_Murder] —(appliesToWorld)→ [RealWorld]`
- `Edge: [Rule_Murder] —(triggeredByVerb)→ [Verb_Kill]`
- `Edge: [Rule_Murder] —(penaltyFormula)→ {수식 노드들}`

### 3.2 왜 Rule은 코드이기도 해야 하는가

하지만 L3 서술이 초당 수백~수천 개 들어올 때마다:

- 룰 그래프를 매번 해석(interpret)하면 **느림**
- Rule 수가 늘어날수록 연산량이 급증

따라서 Rule은:

- 정의/수정 시점에는 **그래프 기반 IR**
- 실행 시점에는 **이미 컴파일된(번역된) 코드**

형태로 다뤄야 한다.

---

## 4. 전체 플로우: 정의 → 컴파일 → 실행

### 4.1 Rule 라이프사이클

1. **정의(Define)**
   - Rule을 GEUL/그래프로 정의하거나 수정한다.
   - 예: “`Kill` 동사가 RealWorld에서 발생하면, 살인죄 검토”

2. **검증(Validate)**
   - 정적 체크:
     - 참조 유효성 (존재하지 않는 엔티티/속성 참조 여부)
     - 타입 일관성 (수식 타입, 비교 연산자 타입 등)
     - 무한 루프 가능성 (자기 참조 Rule 등)

3. **컴파일(Compile)**
   - Rule 그래프 → 내부 IR → 바이트코드
   - 타겟: 경량 Rule VM (또는 Go로 생성된 함수)

4. **등록(Register)**
   - `RuleVersionID → {bytecode, 메타데이터}` 를 캐시에 등록
   - 상태: `DRAFT → ACTIVE` 전환

5. **실행(Execute)**
   - L3에서 Event 발생
   - L2에서 관련 Rule 탐색
   - **이미 컴파일된 Rule 바이트코드**를 VM에서 실행
   - L1 월드 상태 업데이트

6. **폐기/교체(Retire)**
   - 새로운 버전이 ACTIVE되면 이전 버전은 `DEPRECATED`
   - 히스토리는 남기되, 기본 실행은 새 버전 사용

---

## 5. Rule 정의 모델

### 5.1 Rule Node 기본 구조 (개념)

```text
Node: Rule_<Name>@vN
  - id: MID
  - name: "살인죄 판단 규칙"
  - version: 3
  - priority: 100
  - status: DRAFT / ACTIVE / DEPRECATED
  - kind: EVALUATION / TRANSFORM / ALERT ...
````

### 5.2 Rule 관련 주요 엣지

```text
[Rule] --(appliesToWorld)--> [World]
[Rule] --(appliesToContext)--> [Context 조건]
[Rule] --(triggeredByVerb)--> [Verb_Kill]
[Rule] --(triggeredByEventType)--> [Event_Assault]
[Rule] --(conditionGraph)--> [조건 표현 서브그래프]
[Rule] --(effectGraph)--> [효과 표현 서브그래프]
[Rule] --(sourceDocument)--> [원문 조항/계약 텍스트]
[Rule] --(weight/confidence)--> [신뢰도/우선순위]
```

**핵심 아이디어:**

* Rule의 **“언제, 어디에, 무엇에 반응하는가”** 를 그래프로 표현
* 이 그래프 구조를 기반으로 **컴파일 및 트리거 탐색** 수행

---

## 6. 컴파일 대상: 어떤 Rule을 언제 컴파일할까

### 6.1 컴파일 트리거

다음 이벤트가 발생하면 자동으로 컴파일 파이프라인이 돈다.

1. 새로운 Rule 노드 생성 (`Rule_X@v1`)
2. 기존 Rule 수정 (`Rule_X@v2` 생성, v1은 DEPRECATED)
3. Rule의 조건/효과 서브그래프 변경
4. Rule 상태가 `DRAFT → ACTIVE`로 전환될 때

### 6.2 컴파일 대상/단위

* 최소 단위: **Rule Version**

  * `Rule_Murder@v3` 한 개가 한 컴파일 단위
* 컴파일 결과:

  * `CompiledRule` 구조체로 관리

```go
type CompiledRule struct {
    RuleID       MID        // Rule_Murder
    Version      int        // 3
    Bytecode     []byte     // 또는 IR
    TriggerKey   TriggerKey // Verb/Type 기반 인덱싱 키
    Priority     int
    AppliesTo    RuleScope  // World/Context 제한
}
```

---

## 7. 컴파일 파이프라인 상세

### 7.1 단계 1: 그래프 IR 추출

**입력:** Rule Node + 연관 엣지들
**출력:** 논리적으로 평탄화된 IR (중간 표현)

예시 IR (개념):

```text
IF
  Event.verb IN {KILL, SHOOT, STAB}
  AND Event.target.human == true
  AND Event.context.world == RealWorld
THEN
  mark(Event, Crime_Murder)
  set(Event.penalty, Penalty_Murder_Base)
```

이 IR은 다음 요소를 포함:

* **입력 바인딩**: Event, Actor, Target, Context
* **조건식**: (and/or/not, 비교, in, exists …)
* **효과**: 태그 붙이기, 필드 업데이트, 새로운 Event 생성 등

### 7.2 단계 2: IR → 바이트코드

Rule VM이 실행할 수 있는 **작은 명령어 집합**으로 변환:

예시 (극단적으로 단순화):

```text
LOAD_EVENT          // 현재 Event 바인딩
CHECK_VERB IN {KILL, SHOOT, STAB}
JUMP_IF_FALSE L_end

CHECK_TARGET_TAG "human"
JUMP_IF_FALSE L_end

CHECK_CONTEXT_WORLD "RealWorld"
JUMP_IF_FALSE L_end

APPLY_TAG Event "Crime_Murder"
SET_FIELD Event "penalty" "Penalty_Murder_Base"

L_end:
RETURN
```

실제 구현에서는:

* 레지스터/스택 기반 미니 VM
* 분기, 비교, 필드 접근, 함수 호출 정도만 있으면 충분

### 7.3 단계 3: 최적화 (선택)

* Constant Folding (상수 접기)
* Dead Branch 제거
* 공통 서브식 제거 (CSE)
* 단순 룰 병합(옵션)

MVP 단계에서는 **단순한 직렬화 수준**으로도 충분하고,
나중에 성능 이슈가 보이면 여기에 최적화를 추가해도 된다.

---

## 8. 실행 시 룰 탐색과 적용

### 8.1 실행 플로우 요약

1. L3에서 **Event**가 들어온다.
2. L2에서 **트리거 기반**으로 관련 Rule만 찾는다.
3. 찾은 Rule들 중 **현재 Context에 실제로 적용 가능한 것만 남긴다.**
4. 남은 Rule의 **컴파일된 바이트코드를 VM에서 순차 실행**한다.
5. 결과를 L1 월드 상태에 반영한다.

### 8.2 트리거 인덱스 (Rule-as-Graph + Index)

Rule을 저장할 때, 다음과 같은 인덱스를 유지한다:

```text
TriggerKey = (VerbID, EventTypeID, WorldID, ContextTag 등)
TriggerKey → [CompiledRuleID...]
```

실행 시:

```go
func GetTriggeredRules(evt Event) []CompiledRule {
    key := BuildTriggerKey(evt)
    return ruleIndex.Lookup(key) // O(1) 또는 매우 작음
}
```

> 룰이 1만 개든 1억 개든,
> 실제로 각 Event가 검사하는 룰은 **“해당 동사/타입에 연결된 것”만**.

---

## 9. Dev 모드 vs Prod 모드

### 9.1 Dev 모드 (개발/디버깅용)

* 인터프리터/IR 인터랙티브 실행 허용
* **Rule 그래프 ↔ IR ↔ 실행 로그**를 잘 보여주는 모드
* 느려도 괜찮음 (사람이 직접 테스트하는 환경)
* 예:

  * “이 Rule이 왜 이렇게 판정했는지” 추적용

### 9.2 Prod 모드 (실전 서비스용)

* **반드시 컴파일된 Rule만 실행**
* 인터프리터는 비활성화 (또는 디버그 플래그 아래에서만)
* 룰 수정 시:

  * 새 버전 컴파일 완료 + 검증 끝난 뒤에만 `ACTIVE` 전환
* 목표:

  * 초당 수천~수만 Event도 감당 가능하게

---

## 10. 오류 처리 및 안전장치

### 10.1 컴파일 시 오류

* 타입 불일치
* 존재하지 않는 필드/노드 참조
* 순환 참조 등

→ Rule 상태를 `INVALID`로 표시하고, 실행 대상에서 제외
→ UI/로그에 원인을 명시 (어떤 노드/엣지에서 실패했는지)

### 10.2 실행 시 오류

* 예상치 못한 null 값
* 외부 자원 접근 실패 (예: 외부 서비스)

→ 해당 Rule의 실행만 실패로 마킹
→ 전체 시스템은 중단되지 않고,
실패한 Rule ID + Event ID를 로그로 남김.

---

## 11. 성능 관점 요약

* **Rule 수 증가 ≠ 실행 성능 저하**

  * Event마다 **관련 Rule만 인덱스를 통해 O(1)에 찾아** 적용
* **그래프 해석(파싱) 비용은 정의/수정 시에만**

  * 실행 시에는 오직 바이트코드 해석 비용만 부담
* **멀티코어/멀티노드 확장 용이**

  * Event 수준으로 쉽게 병렬화 가능

---

## 12. 앞으로 확장 아이디어

* **JIT (Just-In-Time) 컴파일**

  * 자주 실행되는 Rule을 Go 코드/네이티브 코드로 JIT
* **Rule 프로파일링**

  * Rule별 실행 횟수, 평균 비용, 실패율 통계
* **Rule A/B 테스트**

  * `Rule_Pricing@v3` vs `@v4` 동시에 적용 후 비교
* **자기 수정 Rule**

  * L3 서술/피드백(“이 Rule 오판했어”)을 반영하여 Rule 업데이트

---

## 13. 한 줄 결론

> **Rule은 그래프 데이터로 정의·버전 관리되지만,
> 실행 시에는 반드시 미리 컴파일된 코드로 돌린다.**
>
> 이게 **GWMS L2 Rule 레이어의 기본 원칙**이다.
