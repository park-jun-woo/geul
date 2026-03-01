# 과업 3: Verb_Edge + Event6_Edge + Triple_Edge 관계 정리

**작성일:** 2026-01-30  
**대상:** Verb_Edge.md, Event6_Edge.md, Triple_Edge.md  
**목적:** 세 Edge 타입의 역할 구분, 상호 관계, 사용 시나리오 명확화

---

## 1. 세 Edge의 핵심 역할

### 1.1 한 줄 정의

| Edge | 역할 | 핵심 질문 |
|------|------|-----------|
| **Verb Edge** | 서술 표현 | "어떻게 말했는가?" |
| **Event6 Edge** | 사건 기록 | "무슨 일이 있었는가?" |
| **Triple Edge** | 관계/속성 | "무엇이 어떠한가?" |

---

### 1.2 상세 비교

| 항목 | Verb Edge | Event6 Edge | Triple Edge |
|------|-----------|-------------|-------------|
| **본질** | 서술 (문장/발화) | 사건 (기록) | 관계 (지식) |
| **시간성** | 한정자로 표현 | When 필드 | 없음 (영속) |
| **참여자** | 의미역 기반 | 6하원칙 | S-P-O |
| **워드** | 2~5 | 3~8 | 4~5 |
| **빈도** | 최고빈도 | 중빈도 | 고빈도 |
| **Prefix** | `0 1` / `0 01` | `0 000 011` | `0 000 001` |

---

## 2. 계층 관계

### 2.1 추상화 수준

```
높음 ────────────────────────────────────────────────► 낮음
(추상)                                              (구체)

┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Triple Edge │ ◄── │ Event6 Edge │ ◄── │  Verb Edge  │
│  (지식/관계) │     │  (사건/기록) │     │  (서술/문장) │
└─────────────┘     └─────────────┘     └─────────────┘
      │                   │                   │
      ▼                   ▼                   ▼
  "X는 Y이다"       "X가 Y를 했다"      "~했다/~한다"
  정적 관계          완결된 사건          동적 서술
```

### 2.2 포함 관계

```
┌─────────────────────────────────────────────────────┐
│                    Event6 Edge                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │   Who    │ │   What   │ │   Whom   │ ...        │
│  │ (Entity) │ │(Verb Edge)│ │ (Entity) │            │
│  └──────────┘ └──────────┘ └──────────┘            │
└─────────────────────────────────────────────────────┘
         │              │              │
         │              │              │
         └──────────────┼──────────────┘
                        ▼
              Triple Edge로 속성 기술
```

**핵심:** Event6의 **What은 Verb Edge를 참조**한다.

---

## 3. 각 Edge의 상세 역할

### 3.1 Verb Edge: 서술의 정밀 표현

**목적:** 동사/서술의 문법적·의미적 정보를 **최대한 풍부하게** 보존

**표현 요소:**
- 동사 본문 (16비트 코드)
- 참여자 패턴 (의미역: AGT, PAT, THM, RCP, LOC 등)
- 한정자 (시제, 상, 극성, 양태, 공손, 의도성 등)
- Target (Root/Inner 구분)

**모드:**

| 모드 | 워드 | 커버율 | 용도 |
|------|------|--------|------|
| Tiny | 2 | ~90% | 고빈도 단순 서술 |
| Short | 3 | ~7% | 일반 서술 |
| Full | 5 | ~3% | 정밀 서술 |

**예시:**
```
"철수가 영희에게 책을 줬다"

Verb Edge (Short):
  동사: give
  참여자: AGT+RCP+THM
  한정자: 과거, 완료, 긍정
```

---

### 3.2 Event6 Edge: 6하원칙 사건 기록

**목적:** 뉴스, 역사, 일상 **사건을 구조화된 형태로 저장**

**6하원칙:**

| 요소 | 영문 | 참조 대상 |
|------|------|-----------|
| Who | Agent | Entity TID |
| What | Action | **Verb Edge TID** |
| Whom | Patient | Entity TID |
| When | Time | Quantity/Entity TID |
| Where | Location | Entity TID |
| Why | Reason | Clause/Entity TID |

**핵심 설계:**
- **What = Verb Edge TID**: 한정자 정보를 Verb Edge에 위임
- **가변 길이**: Presence 비트로 필요한 요소만 포함

**예시:**
```
"Apple이 2025년에 Tesla를 인수했다"

Event6 Edge:
  Who:   Apple (Entity TID 0x0001)
  What:  acquire (Verb Edge TID 0x0100)
  Whom:  Tesla (Entity TID 0x0002)
  When:  2025 (Entity TID 0x0003)
```

---

### 3.3 Triple Edge: 정적 관계/속성

**목적:** 위키데이터 스타일의 **(Subject, Property, Object)** 관계 표현

**특징:**
- **영속적**: 시제/상 없음 ("X는 Y이다")
- **이중 모드**: 기본 4워드 (Top 63) + 확장 5워드 (전체 P-ID)
- **Top 63 속성**: 고빈도 속성 빠른 접근

**Property 분류:**

| 범위 | 분류 | 예시 |
|------|------|------|
| 0~7 | 분류/타입 | instance of, subclass of |
| 8~15 | 공간/위치 | country, location |
| 16~23 | 시간 | date of birth, inception |
| 24~31 | 인물 기본 | place of birth, gender |
| 32~39 | 관계/소속 | father, mother, spouse |
| 40~47 | 직업/활동 | occupation, educated at |
| 48~55 | 미디어/식별 | image, website |
| 56~62 | 작품/창작 | author, director |
| 63 | 확장 | 전체 P-ID |

**예시:**
```
"Apple은 회사이다"

Triple Edge (기본):
  Subject: Apple (TID 0x0010)
  Property: instance of (PropCode 0)
  Object: company (TID 0x0020)
```

---

## 4. 상호 참조 패턴

### 4.1 Event6 → Verb Edge

```
Event6 Edge:
  What: Verb Edge TID
        └───► Verb Edge:
                동사: acquire
                한정자: 과거, 완료
```

**이점:**
- 한정자 정보 중복 제거
- 동일 Verb Edge 여러 Event6에서 재사용

---

### 4.2 Triple Edge → Event6 (간접)

Event6의 참여자에 대한 속성은 Triple Edge로 기술:

```
Event6:
  Who: Apple (TID 0x0001)
  
Triple Edge:
  Subject: 0x0001 (Apple)
  Property: headquarters_location
  Object: Cupertino (TID 0x0030)
```

---

### 4.3 Clause Edge → Event6/Verb Edge

인과관계 등은 Clause Edge로 연결:

```
Event6 #1: Apple acquires Tesla
Event6 #2: Stock price rises

Clause Edge:
  Type: CAUSE
  TID1: Event6 #1
  TID2: Event6 #2
```

---

## 5. 사용 시나리오 가이드

### 5.1 시나리오별 선택

| 시나리오 | 권장 Edge | 이유 |
|----------|-----------|------|
| "철수는 학생이다" | **Triple** | 정적 분류 관계 |
| "철수가 달린다" | **Verb** | 단순 서술 |
| "철수가 어제 학교에서 영희를 만났다" | **Event6** | 시공간 정보 포함 사건 |
| "철수의 키는 180cm" | **Triple** | 속성-값 관계 |
| "빠르게 달리고 있다" | **Verb (Full)** | 정밀 한정자 필요 |
| "비가 와서 집에 있었다" | **Clause + Verb** | 인과관계 |

### 5.2 결정 플로우차트

```
시작
  │
  ▼
정적 관계/속성인가? ───Yes───► Triple Edge
  │                          (X는 Y이다)
  No
  │
  ▼
시공간/이유가 핵심인가? ───Yes───► Event6 Edge
  │                            (6하원칙)
  No
  │
  ▼
한정자가 중요한가? ───Yes───► Verb Edge (Short/Full)
  │                        (정밀 서술)
  No
  │
  ▼
Tiny Verb Edge
(고빈도 단순 서술)
```

---

## 6. 데이터 변환 관계

### 6.1 자연어 → GEUL

| 자연어 | 1차 분석 | 최종 형태 |
|--------|----------|-----------|
| "이순신은 장군이다" | 분류 | Triple Edge |
| "이순신이 싸웠다" | 서술 | Verb Edge |
| "이순신이 1598년 노량에서 전사했다" | 사건 | Event6 Edge |

### 6.2 GEUL → WMS

```
자연어 입력
    │
    ▼
GEUL Encoder
    │
    ├───► Verb Edge (서술층 L3)
    │         │
    │         ▼
    ├───► Event6 Edge (정규화)
    │         │
    │         ▼
    └───► Triple Edge (지식층 L2)
              │
              ▼
         WMS World State
```

---

## 7. Prefix 체계 정리

| Edge | Standard | Proposal | 비트 |
|------|----------|----------|------|
| Tiny Verb | `0 1` | `1100 1` | 2/5 |
| Verb | `0 01` | `1100 01` | 3/6 |
| Triple | `0 000 001` | `1100 000 001` | 7/10 |
| Event6 | `0 000 011` | `1100 000 011` | 7/10 |

**빈도 반영:**
- Tiny Verb: 최단 Prefix (가장 빈번)
- Triple: 7비트 (고빈도)
- Event6: 7비트 (저빈도)

---

## 8. 상호 보완 관계 요약

```
┌─────────────────────────────────────────────────────────────┐
│                        GEUL Edge 생태계                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Verb Edge ────참조───► Event6 Edge                        │
│   (서술 정밀)            (사건 기록)                          │
│       │                      │                              │
│       │                      │                              │
│       └──────────┬───────────┘                              │
│                  │                                          │
│                  ▼                                          │
│            Triple Edge ◄─────── 속성/관계                    │
│            (지식 저장)                                       │
│                  │                                          │
│                  ▼                                          │
│            Clause Edge ◄─────── 논리 관계                    │
│            (담화 연결)                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 9. 권장 사항

### 9.1 문서 개선

| 문서 | 권장 추가 내용 |
|------|----------------|
| Verb_Edge.md | Event6와의 관계 섹션 |
| Event6_Edge.md | What→Verb Edge 상세 설명 강화 |
| Triple_Edge.md | Event6/Verb Edge와 구분 가이드 |

### 9.2 Cross-Reference 강화

각 문서 말미에 "관련 Edge 비교" 섹션 추가 권장:

```markdown
## 관련 Edge 비교

| 항목 | 이 Edge | Verb Edge | Triple Edge |
|------|---------|-----------|-------------|
| 용도 | ... | ... | ... |
| 언제 사용 | ... | ... | ... |
```

---

## 10. 결론

### 10.1 핵심 구분

| Edge | 한 줄 | 키워드 |
|------|-------|--------|
| Verb | "어떻게 서술되었는가" | 동사, 한정자, 의미역 |
| Event6 | "무슨 사건이 있었는가" | 6하원칙, When, Where |
| Triple | "무엇이 어떠한가" | S-P-O, 속성, 관계 |

### 10.2 상호 관계

- **Verb Edge는 Event6의 What을 채움**
- **Triple Edge는 참여자의 속성을 기술**
- **Clause Edge는 Event6/Verb 간 논리 관계**

### 10.3 선택 원칙

1. 정적 관계/분류 → **Triple**
2. 시공간이 핵심인 사건 → **Event6**
3. 서술/문장 분석 → **Verb**
4. 단순 동작 → **Tiny Verb**

---

**문서 종료**