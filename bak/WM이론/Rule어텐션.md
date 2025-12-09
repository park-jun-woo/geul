# Rule어텐션.md

**WMS L2 Rule Attention 모델 설계**

---

## 0. 목적

이 문서는 WMS의 **L2 Rule 레이어**가

* 모든 룰을 매번 전수조사하는 느린 구조가 아니라,
* **“지금 들어온 사건(L3 서술)에 주목해야 할 룰만 골라내는 어텐션 엔진”**
  으로 동작하도록 설계하기 위한 스펙이다.

핵심 키워드:

* **Rule-as-Data**: 룰도 결국 그래프 위의 노드/엣지다.
* **Symbolic Attention**: Q–K–V 구조를 심볼릭/그래프 레벨에서 구현.
* **Hard Filter + Soft Score**: 1차 기호 필터 → 2차 SLT 스코어링.

---

## 1. 개념 요약

### 1.1 Q–K–V 대응 관계

Transformer 어텐션의 Q/K/V를 WMS에 매핑하면:

| 역할        | Transformer | WMS                                |
| --------- | ----------- | ----------------------------------- |
| Q (Query) | 현재 토큰       | **현재 들어온 사건(Event / Triple)**       |
| K (Key)   | 컨텍스트 토큰     | **각 Rule의 트리거 패턴(조건)**              |
| V (Value) | 의미 벡터       | **Rule의 실행 로직(컴파일된 바이트코드) + 메타데이터** |

**아이디어:**
L3에서 사건이 들어올 때마다,

* 이 사건을 Q로 보고
* 그래프에서 “이 Q에 반응해야 할 K(룰)”를 빠르게 찾고
* 그 중에서 SLT로 스코어링해서
* 실제로 실행할 V(룰 실행 로직)를 선택한다.

단, 수학적으로 Transformer의 softmax 어텐션을 그대로 구현하는 것은 아니고,
**구조적으로 유사한 “룰 선택 메커니즘”**으로 이해한다.

---

## 2. 룰의 그래프 표현 (Rule-as-Graph)

### 2.1 Rule 노드

각 Rule은 하나의 노드로 표현:

```text
Node: RULE_MURDER
  kind: Rule
  scope: RealWorld
  priority: 90
  strict_threshold: 0.8   // 이 이상이면 적용(APPLIED)
  soft_threshold:   0.4   // 이 이상이면 의심(SUSPECT)
  effect_ref: <bytecode_id>
```

**핵심 필드:**

* `scope`: 적용 가능한 월드/컨텍스트 (예: RealWorld, CompanyX, DreamWorld 등)
* `priority`: 룰 간 충돌 시 우선순위
* `strict_threshold`: 이 스코어 이상이면 실제 world-state를 변경
* `soft_threshold`: 이 스코어 이상이면 “의심 상태”로 기록

### 2.2 Trigger 엣지 (역색인)

어떤 사건이 이 룰을 “깨우는지”를 **역색인(Trigger Edge)**로 저장:

```text
[Ctx: SYSTEM] [Subj: VERB_KILL] [Prop: TRIGGERS] [Obj: RULE_MURDER]
[Ctx: SYSTEM] [Subj: VERB_STAB] [Prop: TRIGGERS] [Obj: RULE_ASSAULT]
[Ctx: SYSTEM] [Subj: EVENT_TYPE_NOISE] [Prop: TRIGGERS] [Obj: RULE_DISTURBANCE]
```

의미:

* `VERB_KILL`이라는 동사가 관련된 사건이 들어오면 → `RULE_MURDER` 후보로 불러옴
* `VERB_STAB`이면 → `RULE_ASSAULT`
* `EVENT_TYPE_NOISE`면 → `RULE_DISTURBANCE`

**장점:**

* 룰이 1개든 1억 개든,
  **현재 사건과 관련 있는 몇 개만** CSR/인덱스로 O(1)에 가까운 비용으로 찾을 수 있음.

---

## 3. 실행 흐름: L3 사건 → L2 Rule 어텐션 → L1 월드 변환

### 3.1 전체 플로우

1. **L3: 사건 입력**

   * 입력: `Event6` 또는 `Triple`
     예: `철수가 회의실에서 책상을 쾅 쳤다`

2. **1차: Hard Filter (기호적 필터)**

   * 동사, 이벤트 타입, 타겟 엔티티, 컨텍스트 등으로
     관련 있을 법한 룰 후보를 **그래프 쿼리로 빠르게 추출**.
   * 예: `TRIGGERS(VERB_HIT)`에 연결된 Rule만 가져오기.

3. **2차: Soft Scoring (SLT)**

   * 후보 Rule마다 `score = SLT(event, rule_trigger_pattern)` 계산.
   * 0.0 ~ 1.0 사이 연속값.

4. **3차: Policy 적용 (상태 결정)**

   * `score >= strict_threshold` → **APPLIED**
   * `soft_threshold <= score < strict_threshold` → **SUSPECT**
   * `score < soft_threshold` → 무시

5. **4차: L1 World에 Delta 반영**

   * APPLIED인 Rule만 실제 world-state를 바꾸는 엣지/노드로 반영.
   * SUSPECT 상태는 별도 “추론/의심 레이어”에 기록.

### 3.2 예시: “김 대리가 책상을 쾅 쳤다”

1. **Event:**

   ```text
   WHO: 김대리
   WHAT: 책상을 쾅 침
   WHERE: 회의실
   WHEN: 2024-12-05
   CONTEXT: 회사 RealWorld
   ```

2. **Hard Filter 결과 (후보 룰):**

   * `RULE_ASSAULT`        (폭행)
   * `RULE_PROPERTY_DAMAGE`(기물 파손)
   * `RULE_DISTURBANCE`    (업무 방해/소란)

3. **SLT 스코어링:**

   * `event` vs `RULE_ASSAULT.trigger` → 0.15  (사람을 친 건 아님)
   * `event` vs `RULE_PROPERTY_DAMAGE.trigger` → 0.35 (부서졌는지 불확실)
   * `event` vs `RULE_DISTURBANCE.trigger` → 0.92 (회의 중 큰 소음, 높은 적합도)

4. **Policy 적용 (각 Rule 메타데이터):**

   * `RULE_ASSAULT`: strict=0.8, soft=0.5 → 0.15 < 0.5 → 무시
   * `RULE_PROPERTY_DAMAGE`: strict=0.7, soft=0.4 → 0.35 < 0.4 → 무시
   * `RULE_DISTURBANCE`: strict=0.8, soft=0.3 → 0.92 ≥ 0.8 → **APPLIED**

5. **L1 World Delta:**

   * `김대리`에 `RULE_DISTURBANCE` 위반 기록 추가
   * 혹은 `Event_Violation_X` 노드를 만들고 김대리/회사/시간과 연결

---

## 4. 스코어의 해석: 월드 상태는 이산, 스코어는 신뢰도

### 4.1 “Weighted Delta”는 피한다

* **하지 말 것:**
  `벌점 = 10 * score` 같이 Rule의 효과를 실수 배율로 곱해 적용
  → 법/규정/ERP/기업 시스템에서는 현실성이 떨어짐.

* **할 것:**
  스코어는 **"이 Rule이 맞을 가능성"**을 나타내는 **메타데이터**로 쓰고,
  실제 상태는 `APPLIED / SUSPECT / NONE`처럼 **이산 값**으로 관리.

### 4.2 SUSPECT의 의미

* `SUSPECT`는 “월드에 바로 확정 반영 X,
  추후 증거/사건이 더 들어올 때 재평가 대상”이라는 의미.
* 예: 책상이 나중에 진짜 부러져 있는 게 발견되면,
  이전의 SUSPECT였던 `Rule_PROPERTY_DAMAGE`를

  * 다시 평가하거나
  * `APPLIED`로 격상.

---

## 5. 구현 관점 설계

### 5.1 핵심 컴포넌트

```go
// L3 사건
type Event struct {
    Ctx    SIDX
    Who    SIDX
    What   SIDX
    Whom   SIDX
    When   Time
    Where  SIDX
    Why    SIDX
    RawNL  string // 원문(선택)
}

// Rule 메타데이터
type RuleMeta struct {
    RuleMID         MID
    Scope           ScopeSpec
    Priority        int
    StrictThreshold float64
    SoftThreshold   float64
    EffectID        RuleEffectID // 컴파일된 바이트코드 참조
}

// 스코어 결과
type RuleEval struct {
    Rule   RuleMeta
    Score  float64
    Status RuleStatus // APPLIED / SUSPECT / IGNORED
}
```

### 5.2 하드 필터 단계 (심볼릭)

```go
// 1차: 심볼릭 필터링 (빠른 그래프 쿼리)
func GetCandidateRules(ev Event, gw *GraphWorld) []RuleMeta {
    // 예: 동사 기반 트리거
    rules := gw.QueryTriggeredRules(ev.What)

    // 컨텍스트 scope 필터링
    filtered := make([]RuleMeta, 0, len(rules))
    for _, r := range rules {
        if r.Scope.Contains(ev.Ctx) {
            filtered = append(filtered, r)
        }
    }
    return filtered
}
```

### 5.3 소프트 스코어(SLT) 단계

```go
// 2차: SLT를 이용한 Soft Scoring
func ScoreRules(ev Event, candidates []RuleMeta, slt SLTEngine) []RuleEval {
    evals := make([]RuleEval, 0, len(candidates))
    for _, r := range candidates {
        s := slt.Score(ev, r) // 0.0 ~ 1.0
        evals = append(evals, RuleEval{
            Rule:  r,
            Score: s,
        })
    }
    return evals
}
```

### 5.4 Policy 적용

```go
func ApplyPolicy(evals []RuleEval) []RuleEval {
    for i, e := range evals {
        switch {
        case e.Score >= e.Rule.StrictThreshold:
            evals[i].Status = RuleStatusApplied
        case e.Score >= e.Rule.SoftThreshold:
            evals[i].Status = RuleStatusSuspect
        default:
            evals[i].Status = RuleStatusIgnored
        }
    }

    // 우선순위/충돌 처리 필요 시 여기서 정렬/해결
    return evals
}
```

### 5.5 전체 파이프라인

```go
func EvaluateRules(ev Event, gw *GraphWorld, slt SLTEngine) []RuleEval {
    // 1. 후보 룰 검색 (Hard Filter)
    candidates := GetCandidateRules(ev, gw)

    if len(candidates) == 0 {
        return nil
    }

    // 2. 소프트 스코어링 (SLT)
    scored := ScoreRules(ev, candidates, slt)

    // 3. Policy 적용 (APPLIED / SUSPECT / IGNORED)
    decided := ApplyPolicy(scored)

    return decided
}
```

---

## 6. 충돌 처리와 우선순위

실제 시스템에서는 여러 Rule이 동시에 APPLIED/SUSPECT 될 수 있고,
서로 상충할 수 있다. 예:

* `Rule_Discount10Percent`
* `Rule_Discount20Percent`
* 둘 다 APPLIED 되면? → 할인폭 충돌.

### 6.1 우선순위 기반

각 RuleMeta에 `Priority` 필드:

```go
// 예: 높은 숫자가 더 우선
sort.Slice(evals, func(i, j int) bool {
    return evals[i].Rule.Priority > evals[j].Rule.Priority
})
```

Policy:

* 동일 영역에 대해 서로 충돌하는 Rule은

  * 우선순위 높은 것만 APPLIED,
  * 나머지는 SUSPECT나 IGNORED로 다운그레이드.

### 6.2 “모순 상태 기록”도 가능

WMS 철학상, 현실이 애매하면:

* “둘 다 기록 + conflict 상태 명시” 도 허용
* 나중에 사람/상위 시스템이 판단하는 구조도 가능.

---

## 7. 요약

1. **Rule도 데이터다.**

   * 룰은 Rule Node + Trigger Edge로 표현된다.
2. **L2는 어텐션 엔진이다.**

   * L3 사건(Event)을 Q로,
   * Rule 트리거를 K로,
   * Rule 실행 로직을 V로 보는 “심볼릭 어텐션” 구조.
3. **두 단계 선택.**

   * Hard Filter: 인덱스/CSR/비트마스크로 후보 Rule만 뽑기.
   * Soft Score: SLT로 상황 적합도 점수 계산.
4. **스코어는 신뢰도, 상태는 이산.**

   * world-state 업데이트는 APPLIED/SUSPECT/NONE으로 관리.
   * 스코어는 추론의 신뢰도/근거로 남기기.
5. **성능과 유연성을 동시에 잡는 구조.**

   * 룰 1억 개여도, 각 사건당 실제로 SLT 돌리는 룰은 수십 개 수준으로 유지 가능.
   * 룰 추가/수정은 그래프 데이터 수정 + Rule 컴파일로 처리.

---

이 문서를 기반으로,

* `Rule컴파일.md`와
* `레이어구조.md`
  와 함께 묶으면 L2 설계 라인은 거의 뼈대가 완성된 상태라고 봐도 됩니다.
