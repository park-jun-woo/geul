# Context Edge 명세서

**버전:** v0.2  
**작성일:** 2026-01-29  
**목적:** GEUL 지식/서술의 세계관, 출처, 관점(Perspective) 표현

---

## 1. 개요

Context Edge는 **"어느 세계관/맥락에서 이 Claim이 참인가"**를 표현한다.

**핵심 개념:**
- Context = **진리의 조건** (Modal Logic의 가능 세계)
- 같은 Subject에 대해 세계관마다 다른 사실 존재 가능
- 출처(Source), 세계관(Worldview), 시점(Perspective) 모두 표현

**예시:**
```
Context "현실":        (지구, 나이, 46억년)
Context "젊은지구론":   (지구, 나이, 6000년)
Context "해리포터":     (마법, exists, true)
Context "빌런시점":     (빌런, is_a, 정의)
```

---

## 2. Prefix

`SIDX.md` 참조

| 항목 | 값 |
|------|-----|
| Standard | `0 000 100` (7비트) |
| Proposal | `1100 000 100` (10비트) |
| 1st 워드 나머지 | 6비트 (Context Type) |

---

## 3. 패킷 구조 (3워드, 48비트)

### 3.1 레이아웃

```
1st WORD (16비트):
┌─────────────────────┬─────────────────┐
│       Prefix        │  Context Type   │
│       10비트        │     6비트       │
└─────────────────────┴─────────────────┘
 [1100 000 100]        [TTTTTT]

2nd WORD: Context TID (16비트) - 이 Context의 고유 ID
3rd WORD: Target TID (16비트) - 이 Context에서 참인 Claim

총: 3워드 (48비트)
```

### 3.2 필드 설명

| 필드 | 비트 | 위치 | 설명 |
|------|------|------|------|
| Prefix | 10 | 1st[15:6] | `1100 000 100` |
| Context Type | 6 | 1st[5:0] | 0=미지정, 1~62=타입, 63=확장(예약) |
| Context TID | 16 | 2nd | 이 Context의 고유 식별자 |
| Target TID | 16 | 3rd | 대상 Claim (Triple/Verb/Event6/Clause TID) |

---

## 4. Context Type (6비트 = 64개)

### 4.0 특수 코드

| Code | 타입 | 설명 |
|------|------|------|
| 0 | UNSPECIFIED | 타입 미지정 (Triple로 상세 정의) |
| 63 | EXTENDED | 확장 모드 (예약, 미사용) |

### 4.1 출처 (Source) - Code 1~20

| Code | 타입 | 설명 | 예시 |
|------|------|------|------|
| 1 | SYSTEM | 시스템 자동 생성 | 위키데이터 동기화 |
| 2 | USER | 사용자 직접 입력 | 수동 작성 |
| 3 | DOCUMENT | 일반 문서 | PDF, Word |
| 4 | NEWS | 뉴스 기사 | 로이터, AP |
| 5 | ACADEMIC | 학술 논문 | arXiv, Nature |
| 6 | GOVERNMENT | 정부/공공 기관 | SEC, 통계청 |
| 7 | WIKI | 위키피디아/위키데이터 | Q42, P31 |
| 8 | API | 외부 API | 금융, 날씨 |
| 9 | ORG | 기관/조직 발표 | 기업 IR |
| 10 | BOOK | 서적 | ISBN 기반 |
| 11 | INTERVIEW | 인터뷰/증언 | 직접 인용 |
| 12 | DATASET | 데이터셋 | Kaggle |
| 13 | SOCIAL | 소셜 미디어 | Twitter |
| 14 | LEGAL | 법률/판례 | 법원 판결 |
| 15 | ARCHIVE | 아카이브 | archive.org |
| 16 | MULTIMEDIA | 영상/음성 | YouTube |
| 17 | DATABASE | 데이터베이스 | IMDB, Freebase |
| 18 | ENCYCLOPEDIA | 백과사전 | 브리태니커 |
| 19 | MANUAL | 매뉴얼/가이드 | 기술 문서 |
| 20 | STANDARD | 표준 문서 | ISO, RFC |

### 4.2 파생/추론 (Derived) - Code 21~30

| Code | 타입 | 설명 | 예시 |
|------|------|------|------|
| 21 | MODEL | AI 모델 생성 | GPT, Claude |
| 22 | INFERENCE | 논리적 추론 | 규칙 기반 |
| 23 | AGGREGATION | 집계/통합 | 다중 출처 종합 |
| 24 | CALCULATION | 계산 결과 | 공식 적용 |
| 25 | TRANSLATION | 번역 | 원문→번역 |
| 26 | EXTRACTION | 추출 | NER, RE |
| 27 | CORRECTION | 수정/정정 | 오류 교정 |
| 28 | HEARSAY | 전언/소문 | 미확인 |
| 29 | ESTIMATION | 추정 | 근사값 |
| 30 | PREDICTION | 예측 | 미래 전망 |

### 4.3 세계관/신념 (Worldview) - Code 31~45

| Code | 타입 | 설명 | 예시 |
|------|------|------|------|
| 31 | RELIGION | 종교적 세계관 | 개신교, 불교 |
| 32 | PHILOSOPHY | 철학적 관점 | 실존주의 |
| 33 | SCIENCE | 과학적 합의 | 현대 물리학 |
| 34 | POLITICS | 정치적 관점 | 보수, 진보 |
| 35 | CULTURE | 문화적 관점 | 동양, 서양 |
| 36 | MYTHOLOGY | 신화 체계 | 그리스 신화 |
| 37 | FOLKLORE | 민담/전승 | 지역 설화 |
| 38 | IDEOLOGY | 이념 체계 | 자본주의 |
| 39 | THEORY | 이론 | 상대성이론 |
| 40 | HYPOTHESIS | 가설 | 검증 전 |
| 41 | TRADITION | 전통/관습 | 유교 전통 |
| 42 | CONSENSUS | 합의/통설 | 학계 정설 |
| 43 | MAINSTREAM | 주류 견해 | 다수 의견 |
| 44 | ALTERNATIVE | 대안적 견해 | 소수 의견 |
| 45 | FRINGE | 비주류/이단 | 사이비 |

### 4.4 허구/창작 (Fiction) - Code 46~55

| Code | 타입 | 설명 | 예시 |
|------|------|------|------|
| 46 | NOVEL | 소설 세계관 | 반지의 제왕 |
| 47 | FILM | 영화 세계관 | MCU |
| 48 | GAME | 게임 세계관 | 젤다 |
| 49 | COMICS | 만화 세계관 | DC 유니버스 |
| 50 | ANIMATION | 애니 세계관 | 지브리 |
| 51 | DRAMA | 드라마 세계관 | 왕좌의 게임 |
| 52 | THEATER | 연극 세계관 | 햄릿 |
| 53 | FANFIC | 2차 창작 | 팬픽션 |
| 54 | LEGEND | 전설 | 아서왕 |
| 55 | FAIRYTALE | 동화 | 신데렐라 |

### 4.5 시점/화자 (Perspective) - Code 56~62

| Code | 타입 | 설명 | 예시 |
|------|------|------|------|
| 56 | NARRATOR | 서술자 시점 | 전지적 화자 |
| 57 | PROTAGONIST | 주인공 시점 | 히어로 관점 |
| 58 | ANTAGONIST | 적대자 시점 | 빌런 관점 |
| 59 | AUTHOR | 저자 의도 | 작가 해설 |
| 60 | EXPERT | 전문가 견해 | 학자 의견 |
| 61 | LAYMAN | 일반인 인식 | 대중 인식 |
| 62 | SATIRICAL | 풍자/아이러니 | 반어적 표현 |

---

## 5. Context Type 요약

```
┌─────────────────────────────────────────────┐
│  0:     UNSPECIFIED (미지정)                │
├─────────────────────────────────────────────┤
│  1~20:  출처 (Source)                       │
│         SYSTEM, USER, NEWS, ACADEMIC, ...   │
├─────────────────────────────────────────────┤
│  21~30: 파생/추론 (Derived)                 │
│         MODEL, INFERENCE, PREDICTION, ...   │
├─────────────────────────────────────────────┤
│  31~45: 세계관/신념 (Worldview)             │
│         RELIGION, SCIENCE, THEORY, ...      │
├─────────────────────────────────────────────┤
│  46~55: 허구/창작 (Fiction)                 │
│         NOVEL, FILM, GAME, LEGEND, ...      │
├─────────────────────────────────────────────┤
│  56~62: 시점/화자 (Perspective)             │
│         NARRATOR, PROTAGONIST, EXPERT, ...  │
├─────────────────────────────────────────────┤
│  63:    EXTENDED (확장, 예약)               │
└─────────────────────────────────────────────┘
```

---

## 6. 연결 대상 (Target)

Context Edge는 모든 Claim Edge에 연결 가능.

| Target 타입 | 설명 |
|-------------|------|
| Triple Edge | 속성/관계 |
| Verb Edge | 서술 |
| Event6 Edge | 6하원칙 사건 |
| Clause Edge | 절 관계 |
| Context Edge | 중첩 Context |

---

## 7. 메타데이터 확장 (Triple 활용)

Context 자체에 추가 정보는 **Triple로 표현**.

### 7.1 출처 상세

```
(Context TID, P:source_entity, Reuters_Entity)  - 출처 기관
(Context TID, P:url, "https://...")             - 원본 링크
(Context TID, P:author, 저자_Entity)            - 저자
(Context TID, P:publication_date, 2026-01-29)   - 발행일
```

### 7.2 신뢰도/유효성

```
(Context TID, P:confidence, 0.95)               - 신뢰도
(Context TID, P:valid_until, 2026-12-31)        - 유효 기한
(Context TID, P:peer_reviewed, true)            - 검증 여부
```

### 7.3 세계관 상세

```
(Context TID, P:universe_name, "해리포터")       - 세계관 이름
(Context TID, P:canon_level, "primary")          - 정전성
(Context TID, P:timeline, "본편")                - 타임라인
```

### 7.4 시점 상세

```
(Context TID, P:perspective_holder, 빌런_Entity)  - 시점 주체
(Context TID, P:reliability, "unreliable")        - 신뢰성
```

---

## 8. 예시

### 8.1 출처: "로이터 보도"

```
Context Edge:
  1st: [1100 000 100] + [000100]  - NEWS (4)
  2nd: [0x0300]                   - Context TID
  3rd: [0x0001]                   - Target: Triple "Apple acquired Tesla"

추가 Triple:
  (0x0300, P:source_entity, Reuters)
  (0x0300, P:date, 2026-01-29)
```

### 8.2 세계관: "개신교 창조론"

```
Context Edge:
  1st: [1100 000 100] + [011111]  - RELIGION (31)
  2nd: [0x0301]                   - Context TID
  3rd: [0x0002]                   - Target: Triple "지구 나이 = 6000년"

추가 Triple:
  (0x0301, P:name, "젊은지구창조론")
  (0x0301, P:tradition, "개신교 근본주의")
```

### 8.3 허구: "해리포터 세계관"

```
Context Edge:
  1st: [1100 000 100] + [101110]  - NOVEL (46)
  2nd: [0x0302]                   - Context TID
  3rd: [0x0003]                   - Target: Triple "호그와트 is_a 학교"

추가 Triple:
  (0x0302, P:universe_name, "해리포터")
  (0x0302, P:author, J.K.롤링)
```

### 8.4 시점: "빌런의 관점"

```
Context Edge:
  1st: [1100 000 100] + [111010]  - ANTAGONIST (58)
  2nd: [0x0303]                   - Context TID
  3rd: [0x0004]                   - Target: Triple "타노스 is_a 구원자"

추가 Triple:
  (0x0303, P:perspective_holder, 타노스_Entity)
  (0x0303, P:universe, MCU)
```

### 8.5 AI 추론: "Claude가 추론"

```
Context Edge:
  1st: [1100 000 100] + [010101]  - MODEL (21)
  2nd: [0x0304]                   - Context TID
  3rd: [0x0005]                   - Target: Triple "X causes Y"

추가 Triple:
  (0x0304, P:model, Claude_Entity)
  (0x0304, P:confidence, 0.75)
```

### 8.6 다중 Context (같은 Claim, 여러 세계관)

```
Triple T01: (우주, origin, 빅뱅) | TID=0x0001

Context 1: SCIENCE (33)
  (0x0310, Context, T01)

Context 2: RELIGION (31) - 다른 세계관에서는 다른 주장
  다른 Triple: (우주, origin, 창조) | TID=0x0002
  (0x0311, Context, 0x0002)
```

---

## 9. 파싱/인코딩

### 9.1 파싱

```python
def parse_context_edge(words: list[int]) -> dict:
    """3워드 Context Edge 파싱"""
    
    word1 = words[0]
    prefix = (word1 >> 6) & 0x3FF
    assert prefix == 0b1100000100, "Invalid Context Edge prefix"
    
    context_type = word1 & 0x3F
    context_tid = words[1]
    target_tid = words[2]
    
    TYPE_NAMES = {
        0: "UNSPECIFIED",
        1: "SYSTEM", 2: "USER", 3: "DOCUMENT", 4: "NEWS",
        5: "ACADEMIC", 6: "GOVERNMENT", 7: "WIKI", 8: "API",
        # ... 나머지 타입
        21: "MODEL", 22: "INFERENCE",
        31: "RELIGION", 33: "SCIENCE",
        46: "NOVEL", 47: "FILM",
        56: "NARRATOR", 58: "ANTAGONIST",
        63: "EXTENDED"
    }
    
    return {
        "type": "Context Edge",
        "context_type": TYPE_NAMES.get(context_type, f"Code{context_type}"),
        "context_type_code": context_type,
        "context_tid": context_tid,
        "target_tid": target_tid,
        "word_count": 3
    }
```

### 9.2 인코딩

```python
def encode_context_edge(
    context_type: int,
    context_tid: int,
    target_tid: int
) -> list[int]:
    """Context Edge 인코딩 → 3워드"""
    
    prefix = 0b1100000100  # 10비트
    word1 = (prefix << 6) | (context_type & 0x3F)
    
    return [word1, context_tid, target_tid]

# 사용 예시
NEWS = 4
RELIGION = 31
NOVEL = 46

words = encode_context_edge(NEWS, 0x0300, 0x0001)
# → [0xC104, 0x0300, 0x0001]
```

---

## 10. WMS 저장 구조

### 10.1 테이블

```sql
CREATE TABLE context_edges (
    context_tid INTEGER,              -- Context ID
    context_type SMALLINT NOT NULL,   -- 6비트 (0-63)
    target_tid INTEGER NOT NULL,      -- Claim TID
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (context_tid, target_tid)
);

CREATE INDEX idx_target ON context_edges(target_tid);
CREATE INDEX idx_type ON context_edges(context_type);
CREATE INDEX idx_context ON context_edges(context_tid);
```

### 10.2 쿼리

```sql
-- Claim의 모든 Context
SELECT * FROM context_edges WHERE target_tid = ?;

-- 특정 세계관의 모든 Claim
SELECT target_tid FROM context_edges WHERE context_tid = ?;

-- NEWS 타입의 모든 Context
SELECT * FROM context_edges WHERE context_type = 4;
```

---

## 11. 설계 근거

### 11.1 Context Edge 단독 타입 이유

- **세계관 = 메타 레이어**: Triple/Clause와 다른 레벨
- **Named Graph 대응**: RDF Quad의 G(Graph)에 해당
- **양상논리**: "가능 세계"에서의 진리 조건

### 11.2 6비트 Context Type 이유

- 별도 Triple 없이 **즉시 분류 가능**
- 62개 타입으로 대부분 커버
- 상세 정보는 Triple로 확장

### 11.3 3워드 경량 구조 이유

- Context 연결은 **대량 발생** (모든 Claim에 붙음)
- 최소 크기로 저장 효율
- 메타데이터는 Triple로 분리

---

## 12. GEUL 생태계 내 위치

```
GEUL Edge 체계:

Object Level (사실):
├── Entity Node
├── Triple Edge
├── Verb Edge
├── Event6 Edge
├── Clause Edge
└── Quantity Node

Meta Level (사실의 조건):
└── Context Edge ← 이 문서
        │
        └── "어느 세계관에서 이 사실이 참인가?"
```

---

## 13. 버전 히스토리

| 버전 | 날짜 | 변경 |
|------|------|------|
| v0.1 | 2026-01-29 | 초안: 6비트 Context Type, 3워드 구조 |
| v0.2 | 2026-01-29 | Prefix 표기 수정, SIDX.md 참조로 변경 |

---

## 14. 향후 과제

- [ ] Context 계층 구조 (부모 Context)
- [ ] Context 간 호환성/충돌 표현
- [ ] 시간에 따른 Context 변화
- [ ] 확장 모드 (Code 63) 상세 정의

---

**문서 종료**