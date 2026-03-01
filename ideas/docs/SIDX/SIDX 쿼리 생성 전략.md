# SIDX 쿼리 생성 전략

**작성일:** 2026-02-26
**주제:** SIDX 비트마스크 쿼리를 어떻게 생성할 것인가 — LLM vs 알고리즘
**결론:** 하이브리드. 비트 조립은 100% 알고리즘, 자연어 의미 파싱만 LLM 보조.

---

## 1. 핵심 질문

SIDX를 활용해 SIMD 탐색을 하려면, 프롬프트에서 쿼리할 SIDX 비트마스크를 만들어내야 한다.

- LLM 모델이 필요한가?
- 알고리즘으로 가능한가?

---

## 2. 결론: 2단계 분리

```
자연어 쿼리  →  [Stage 1: 의미 추출]  →  구조화된 쿼리  →  [Stage 2: 비트 조립]  →  SIDX 비트마스크
                   ↑ 쟁점                                    ↑ 100% 알고리즘
```

- **Stage 2 (비트 조립)**: 논쟁의 여지 없이 순수 알고리즘. 코드북이 확정되면 `EntityType=Human, 성별=Male, 국적=Korea` → 비트 조립은 비트 연산 함수 하나면 끝.
- **Stage 1 (의미 추출)**: 80-90%는 코드북 사전 룩업 + 규칙 NLU. 나머지 10-20%만 LLM 보조.

---

## 3. 알고리즘으로 커버 가능한 범위 (~80-90%)

| 쿼리 유형 | 방법 | 예시 |
|-----------|------|------|
| 타입 직접 지정 | 사전 매핑 | "사람" → Human(0x00) |
| 속성 직접 지정 | 코드북 룩업 | "한국" → 국적 0x52 |
| 동사 분류 지정 | prefix 매핑 | "이동 동사" → MOVE-* 계열 |
| 한정자 지정 | 비트 플래그 | "과거형 부정" → Tense=past, Polarity=neg |
| 참여자 패턴 | 플래그 조합 | "누가 누구에게" → AGT+RCP |

**SIDX의 모든 비트 위치에 의미가 고정**되어 있으므로, 개념→비트 매핑은 유한한 사전(dictionary)이다.

### 3.1 Verb 쿼리는 거의 100% 알고리즘

68개 sub_primitive가 허프만 코드로 확정되어 있으므로:

```python
# "이동 관련 동사 모두 찾기" → MOVE 계열 6개 sub_primitive의 prefix mask
MOVE_MASKS = [
    (0b0010_000000000000, 0b1111_000000000000),   # MOVE-DISPLACE (4bit)
    (0b0011_000000000000, 0b1111_000000000000),   # MOVE-GO (4bit)
    (0b1000011_000000000, 0b1111111_000000000),   # MOVE-COME (7bit)
    (0b1001101_000000000, 0b1111111_000000000),   # MOVE-LEAVE (7bit)
    (0b10111011_00000000, 0b11111111_00000000),   # MOVE-FALL (8bit)
    (0b11000011_00000000, 0b11111111_00000000),   # MOVE-FOLLOW (8bit)
]
# SIMD에서 OR로 합쳐서 병렬 탐색
```

---

## 4. LLM이 필요한 영역 (~10-20%)

| 쿼리 유형 | 왜 LLM? | 예시 |
|-----------|---------|------|
| **모호성 해소** | 같은 단어가 여러 타입 | "Apple" → Business? Taxon? |
| **함축 추론** | 명시하지 않은 속성 추론 | "위대한 과학자" → 저명도=7? |
| **시대/맥락 추론** | 배경지식 필요 | "나폴레옹 시대 사람" → Era=Early Modern |
| **유사/비유 쿼리** | 직접 매핑 불가 | "물과 관련된 것" → Chemical, River, Lake... |
| **복합 서술 쿼리** | 문장 구조 파싱 | "누군가 어제 서울에서 책을 산 사건" |

---

## 5. 3계층 아키텍처 제안

```
Level 1: 코드북 직접 룩업 (O(1), 알고리즘)
   ↓ 실패 시
Level 2: 규칙 기반 NLU (spaCy + 패턴 매칭)
   ↓ 실패 시
Level 3: LLM 호출 (마지막 수단)
```

**Level 1 — 코드북 룩업:**
```python
ENTITY_TYPE_DICT = {"사람": 0x00, "인간": 0x00, "human": 0x00, "조직": 0x01, ...}
NATIONALITY_DICT = {"한국": 0x52, "미국": 0x01, ...}
GENDER_DICT = {"남자": 0b01, "여자": 0b10, "male": 0b01, ...}
VERB_PRIM_DICT = {"이동": "MOVE", "감정": "FEEL", "사고": "THINK", ...}
```

**Level 2 — 규칙 NLU:**
spaCy 형태소 분석 → 명사구/동사구 추출 → Level 1 사전에 매핑.

**Level 3 — LLM:**
LLM은 SIDX 비트를 직접 생성하지 않는다. 구조화된 JSON까지만 출력하고, 비트 조립은 알고리즘이 담당.

---

## 6. LLM의 역할: 비트 생성이 아닌 의미 파싱

LLM에게 주는 건 **스키마가 고정된 JSON 템플릿**이다:

```json
// Entity 쿼리 스키마
{
  "type": "entity_query",
  "entity_type": null,    // 64개 중 택1 (null = don't care)
  "mode": null,           // 8개 중 택1
  "attrs": {
    "subcategory": null,  // 32개 중 택1
    "occupation": null,   // 64개 중 택1
    "nationality": null,  // 256개 중 택1
    "era": null,          // 16개 중 택1
    "gender": null,       // 4개 중 택1
    "notability": null,   // 8개 중 택1
    "birth_decade": null  // 16개 중 택1
  }
}
```

```json
// Verb 쿼리 스키마
{
  "type": "verb_query",
  "primitive": null,       // 10개 중 택1
  "sub_primitive": null,   // 68개 중 택1
  "participants": [],      // 19개 역할 중 선택
  "qualifiers": {
    "tense": null,
    "aspect": null,
    "polarity": null,
    "mood": null
  }
}
```

LLM은 null을 채우는 것이 전부. 못 채우면 null로 둔다 — 그게 곧 우아한 열화이고, SIMD에서는 don't care 비트가 된다.

이 패턴은 현대 LLM의 **function calling / tool use**와 구조적으로 동일하다.

---

## 7. 우아한 열화가 쿼리 오류 허용도를 높인다

SIDX의 "비트를 덜 채울수록 추상적 표현" 원칙이 쿼리에도 적용된다:

```
"한국 사람" (성별 모름)
→ value: EntityType=Human, 국적=Korea, 성별=00(Unknown)
→ mask:  EntityType=0x3F, 국적=0xFF, 성별=00(don't care)
```

LLM이 확신 없는 필드는 빼면 된다. SIMD가 넓은 범위를 탐색하고 후처리에서 좁힌다.

---

## 8. 과도기 JSON 중간층의 가치

지금 LLM에게 비트를 직접 다루라고 하면 정확도가 보장되지 않는다.
JSON 중간층은 비용이 아니라 투자다:

1. **검증 가능성** — JSON은 사람이 읽고 오류를 바로 잡을 수 있다
2. **디버깅** — 쿼리 오류의 원인을 JSON 단에서 찾을 수 있다
3. **코드북 진화** — 비트 스키마가 바뀌어도 JSON→비트 변환 함수만 고치면 된다
4. **학습 데이터 축적** — (자연어, JSON) 쌍이 쌓이면 미래 GEUL-native 모델 학습 데이터가 된다

---

## 9. Tool Use와 GEUL 쿼리의 구조적 동일성

```
[현재 Tool Use]
사용자: "이 파일에서 TODO 찾아줘"
→ LLM 추론 → Grep(pattern="TODO", path="./src") → 런타임 실행 → 결과

[미래 GEUL Query]
사용자: "세종대왕 시대 학자 찾아줘"
→ LLM 추론 → ENTITY_QUERY(type=Human, sub=Scientist, era=Medieval, nat=Korea) → WMS SIMD 실행 → 결과
```

본질은 동일: **"자연어 의도 → 실행 가능한 구조화 호출"**

GEUL 쿼리는 LLM 입장에서 새로운 tool이 추가되는 것과 같다. Tool use 학습과 동일한 방법론 적용 가능.

---

## 10. GEUL은 Tool Use를 넘어선다

Tool use의 한계:
```
LLM → 구조화 출력(tool call) → 비구조화 결과(텍스트) → LLM이 다시 해석
```

GEUL-native의 차이:
```
LLM → GEUL 쿼리 → WMS → GEUL 결과 → LLM이 GEUL로 직접 이해
      구조화         구조화           구조화
```

입출력 전체가 GEUL이면 자연어 변환 없이 의미가 보존된다.
Tool use는 "자연어 속에서 구조화를 잠깐 빌려 쓰는" 것이고, GEUL-native는 **사고 자체가 구조화**되는 것이다.

이것이 SEGLAM 의식적 흐름의 핵심:
```
입력 → Encoder → GEUL 심상 → WMS 쿼리(GEUL) → WMS 결과(GEUL) → 추론(GEUL) → Decoder → 출력
```

---

## 11. 로드맵

```
Phase 1 (현재)   : 자연어 → JSON → 알고리즘 → SIDX
                   데이터 축적 단계. 코드북 + JSON 중간층 설계.

Phase 2 (단기)   : GEUL을 tool schema로 등록
                   LLM이 tool call처럼 GEUL 쿼리 생성.
                   JSON 대신 GEUL 텍스트 표현 사용.

Phase 3 (중기)   : GEUL 코퍼스로 파인튜닝
                   LLM이 GEUL 문법을 내재화.
                   쿼리뿐 아니라 응답도 GEUL로.

Phase 4 (장기)   : GEUL-native 사전학습
                   내부 추론 자체가 GEUL 기반.
                   자연어는 I/O 인터페이스일 뿐.
```

---

## 12. 요약

| 질문 | 답 |
|------|-----|
| LLM 전용 모델이 필요한가? | 아니다. 별도 파인튜닝까지는 불필요 |
| 순수 알고리즘으로 가능한가? | 80-90%는 가능. 코드북 사전 + 규칙 NLU |
| LLM이 아예 불필요한가? | 아니다. 모호성/함축/복합 쿼리에는 범용 LLM 필요 |
| SIDX 비트를 LLM이 직접 생성해야 하나? | 절대 아니다. LLM은 구조화 쿼리까지만 |
| JSON 중간층이 왜 필요한가? | 과도기 검증 + 미래 학습 데이터 축적 |
| 최종 형태는? | LLM이 GEUL을 tool처럼 직접 사용, 나아가 GEUL-native 사고 |

---

**문서 종료**
