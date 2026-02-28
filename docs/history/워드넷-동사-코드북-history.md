# 워드넷 동사 의미정렬 코드북 개발 히스토리

WordNet 13,767개 동사 synset을 10 Primitive → 68 Sub-primitive → 559 Root → 13,767 Leaf 체계로 분류하고, 16비트 의미정렬 코드북(verb_bits.json)을 완성하기까지의 전체 과정.

---

## 타임라인 요약

| 날짜 | 마일스톤 | 핵심 산출물 |
|------|----------|-------------|
| 2025-10 초 | WordNet DB 구축 + 동사 의미소 분해(factorize) 파이프라인 | 41,625개 JSON, factorize.py |
| 2025-10-09 | LLM 비교(gpt-oss vs Gemini) + HPA 파싱 테스트 | mrs.py, Gemini 채택 결정 |
| 2025-10-10 | 의미소 분해 데이터 검증 + 자동교정 | validate.py, corrected.py (3,149/3,843 수정) |
| 2025-11-14 | 559 루트 동사 발견 + CRUD v2 설계 돌파 | verbtrees.py, CRUD v2 아키텍처 |
| 2026-01-27 | 32비트 Verb SIDX 체계 확립 + Verb Edge 문법 | sidx559.json, Verb Edge v0.1 |
| 2026-01-29 | 전체 GEUL 스트림 포맷 10개 패킷 명세 완성 | 10비트 Prefix 체계, Stream Format v0.1 |
| 2026-02-27 | **13,767개 동사 16비트 코드북 생성 및 검증 완료** | **verb_bits.json** |

---

## Phase 1: WordNet 데이터 인프라 구축 (2025-10 초)

### 1.1 PostgreSQL 스키마 생성

WordNet 3.1 사전 데이터를 PostgreSQL에 적재.

**스크립트:** `geulso/wordnet/postgres.py`, `wordnet.sql`

```
wordnet_synsets        — synset 정의 (118K+)
wordnet_lemmas         — 어형 매핑
wordnet_synset_relations — synset 간 관계 (hypernym/hyponym 등)
wordnet_verb_frames    — 동사 구문 프레임
wordnet_wikidata_mapping — Wikidata 연결
```

### 1.2 ltree 확장으로 계층 구조 저장

**스크립트:** `geulso/wordnet/ltree.sql`

```sql
CREATE TABLE verb_hypernym_ltree (
    synset_id VARCHAR(100) PRIMARY KEY,
    definition TEXT,
    tree_path LTREE NOT NULL,
    depth INTEGER DEFAULT 0
);
```

PostgreSQL ltree 확장으로 `@>`, `<@` 연산자를 이용한 효율적 트리 탐색 지원.

### 1.3 동사 synset 카운트

**스크립트:** `geulso/wordnet/countv.py`

**결과:** WordNet 동사 synset 총 **13,767개** 확인.

---

## Phase 2: LLM 기반 동사 의미소 분해 (2025-10-03 ~ 10-10)

### 2.1 Factorize 파이프라인 실행

**스크립트:** `geulso/factorize/factorize.py`

Gemini 2.5 Flash API로 각 동사 프레임을 의미소(sememe)로 분해.

```
입력: synset_id, definition, verb_frame, hypernyms, antonyms
출력: {sememes: [{verb_type, verb_property, participants}], qualifiers: {...}}
```

- 비동기 처리 + 재시도 로직 + 중단 시 이어하기(`--skip-existing`)
- **41,625개 JSON 파일** 생성 (~10-20시간 소요)

### 2.2 LLM 모델 비교 (2025-10-09)

| 모델 | 문제점 | 결과 |
|------|--------|------|
| gpt-oss:20b | synset_id 환각, 비일관적 추론, 맥락 외 창작 | **탈락** |
| gemini-2.5-flash | 정확한 후보 선택, 솔직한 NO_CANDIDATE 반환 | **채택** |

**핵심 교훈:** LLM 품질이 의미소 분해 데이터 품질을 직접 결정함.

### 2.3 데이터 검증 및 교정 (2025-10-10)

**스크립트:** `geulso/factorize/validate.py` → `corrected.py`

- 41,625개 파일 전수검사 (15시간 실행)
- **3,843개 오류 파일** 발견 (그 중 777개 NO_CANDIDATE)
- 3단계 synset 후보 탐색: 직접 조회 → 어형 검색 → 정의 키워드 검색
- Gemini로 99% 이상 신뢰도 교정 → **3,149개 자동 교정 성공** (82%)
- 적용된 수정: sememe 2,007건 + participant 1,329건 = 총 3,336건

### 2.4 구조 검증 및 DB 적재

**스크립트:** `geulso/factorize/check.py` → `postgres.py`

- qualifier 명세 일치 여부, 필수 키 존재, synset 유효성 최종 검사
- `wordnet_factorized_sememes` (~33K rows), `wordnet_factorized_qualifiers`, `wordnet_factorized_participants` 테이블 적재

---

## Phase 3: 559 루트 동사 발견과 분류 (2025-11-14)

### 3.1 동사 hypernym 트리 구축

**스크립트:** `geulso/wordnet/verbtree.py`

- 모든 동사 synset의 hypernym 관계를 BFS로 탐색
- DAG → Tree 변환 (다중 부모 노드는 첫 번째 경로 선택)
- **559개 루트 동사** 발견 (hypernym이 없는 최상위 노드)
- 최대 깊이 ~15레벨

### 3.2 559 루트 동사 추출

**스크립트:** `geulso/wordnet/verbtop559.py`

**산출물:** `verbtop559.json` — 559개 루트 동사의 synset_id, definition, descendant_count

### 3.3 10 Primitive 수동 분류

559개 루트 동사를 10가지 의미 원형(Primitive)으로 분류:

```
BE(99)        — 상태 유지 (exist, have, remain)
PERCEIVE(38)  — 지각 (see, hear, feel)
FEEL(56)      — 감정 (love, hate, fear)
THINK(51)     — 사고 (think, know, believe)
CHANGE(96)    — 상태 변화 (become, die, begin)
CAUSE(277)    — 사역/행위 (make, do, put)
MOVE(49)      — 이동 (go, come, travel)
COMMUNICATE(48) — 소통 (say, tell, speak)
TRANSFER(33)  — 전달/이전 (give, receive, send)
SOCIAL(52)    — 사회적 (meet, join, follow)
```

### 3.4 68 Sub-primitive 분류

각 Primitive 내부를 세부 분류:

| Primitive | Sub-primitives | 예시 |
|-----------|----------------|------|
| BE (8) | EXIST, HAVE, LOCATE, EQUAL, RELATE, APPEAR, REMAIN, ABLE | |
| CAUSE (14) | USE, MAKE, ADD, REMOVE, CONTROL, MODIFY, HARM, DESTROY, EMIT, DETERMINE, PROTECT, REFRAIN, PHYSIO, ACQUIRE | |
| CHANGE (10) | TRANSFORM, BEGIN, END, VANISH, SUCCEED, FAIL, SHIFT, CONNECT... | |
| MOVE (6) | GO, COME, DISPLACE, FALL, LEAVE, FOLLOW | |
| TRANSFER (3) | GIVE, GET, RELEASE, TRADE | |
| PERCEIVE (4) | SEE, SENSE, FIND, MISS | |
| COMMUNICATE (6) | SAY, SHOW, AGREE, DENY, HIDE, ACCUSE | |
| THINK (6) | REASON, KNOW, FORGET, LEARN, REMEMBER, PLAN | |
| FEEL (6) | AFFECT, LIKE, DISLIKE, WANT, FEAR, ANGER | |
| SOCIAL (5) | WORK, COMPETE, BELONG, PART, MEET, COMPLY | |

**산출물:** `geulso/wordnet/classified/*.json` (10개 파일)

### 3.5 CRUD v2 설계 돌파

v1 모델의 11.5% 예외(4,777 파일)를 분석한 결과, **CRUD 4연산 모델**이 모든 예외를 해소:

```
v2 = {Operator} + {Property} + {Pattern}
  Operator: CREATE, READ, UPDATE, DELETE
  Property: 의미 속성 (location, sight, emotion 등)
  Pattern: 시간 형태 (single, iterative, continuous)
```

**핵심 통찰:** WordNet 13,767개 동사는 "언어" 자체가 아니라 **"표준 라이브러리"**. CRUD v2가 소스코드(AST) 수준이며, GEUL은 존재하지 않는 동사도 동적 생성 가능.

---

## Phase 4: 32비트 Verb SIDX 체계 확립 (2026-01-27)

### 4.1 Huffman 유사 비트코드 할당

**스크립트:** `geulso/wordnet/sub_primitive_count.py`

고빈도 sub-primitive에 짧은 코드를 할당하는 가변 길이 인코딩:

```
CHANGE-TRANSFORM (3,049개) → 4비트 "0000"
CAUSE-USE (1,358개)        → 4비트 "0001"
MOVE-DISPLACE (1,025개)    → 4비트 "0010"
...
PERCEIVE-FIND (소수)       → 8비트 "11000000"
```

**산출물:** `geulso/wordnet/json/primitive-map.json` (68 sub-primitive → 가변길이 코드)

### 4.2 559 루트 Flat Index 할당

**스크립트:** `geulso/wordnet/valid_flat.py`

각 루트 동사에 sub-primitive 코드 + 로컬 인덱스 할당:

```json
{
  "synset_id": "abandon.v.02",
  "primitive": "TRANSFER",
  "sub_primitive": "GIVE",
  "flat": "110000101110100",
  "flat_index": "110000101110100000"
}
```

**산출물:**
- `geulso/wordnet/json/flat-verbs.json` — 559개 루트의 flat_index
- `geulso/wordnet/verbtop559/sidx559.json` — 559개 SIDX 확정

### 4.3 32비트 Verb SIDX 구조

```
[1100]    Proposal Prefix (4비트)
[0010]    Verb Node 마커 (4비트)
[xxx]     Primitive (3~5비트)
[xxxx]    Sub-primitive (2~4비트)
[xxxxx]   Verb Index (1~5비트)
[0...0]   Reserved (나머지)
───────────────────────────────
총 32비트
```

### 4.4 32비트 동사 한정자(Modifier) 설계

```
Evidentiality (2b) + Mood (2b) + Modality (2b) + Tense (2b)
+ Aspect (3b) + Politeness (2b) + Polarity (2b) + Volitionality (2b)
+ Confidence (2b) + Iterativity (4b) + Reserved (9b)
= 32비트
```

양자화: 2비트 = 4단계 (-1.0, -0.3, +0.3, +1.0)

---

## Phase 5: 13,767개 동사 16비트 코드북 생성 (2026-02-27)

### 5.1 DFS Pre-order 코드 할당

**스크립트:** `geulso/wordnet/verbtrees_bit.py`

559개 트리 파일을 순서대로 DFS 전위 순회하며 16비트 코드 할당:

```
16비트 = sub_primitive_prefix (4~8비트 Huffman) + DFS_index (8~12비트)
```

**알고리즘:**
1. 559개 verbtree JSON을 번호순 로드
2. 각 트리의 루트 → primitive-map.json에서 코드 조회
3. 남은 비트 = 16 - len(primitive_code)
4. DFS 전위 순회로 순차 코드 할당
5. 중복 synset 건너뛰기 (DAG→Tree 변환 잔여)

### 5.2 검증 통과

**스크립트:** `geulso/wordnet/valid_verb_bits.py`

```
검증 항목                결과
──────────────────────────
총 동사 수              13,767 ✓
고유 synset_id          13,767 ✓ (중복 없음)
고유 16비트 코드        13,767 ✓ (충돌 없음)
오류                    0 ✓
경고                    0 ✓
```

### 5.3 용량 분석

| Prefix 길이 | Sub-primitive 수 | 최대 슬롯 | 사용률 |
|-------------|-------------------|-----------|--------|
| 4비트 | 4개 | 4,096 | 23~75% |
| 5비트 | 4개 | 2,048 | 22~37% |
| 6비트 | 8개 | 1,024 | 17~40% |
| 7비트 | 16개 | 512 | 12~29% |
| 8비트 | 36개 | 256 | 1~22% |

**모든 sub-primitive에 10~40% 확장 여유** — 다국어/신조어 수용 가능.

### 5.4 Graceful Degradation 분석

```
bit[1-4]:  Primitive 수준 (10종: BE, CAUSE, CHANGE, ...)
bit[1-8]:  Sub-primitive 수준 (68종)
bit[1-16]: 개별 동사 (13,767종)
```

WordNet 트리 기반 Huffman 인코딩은 기각됨:
- change.v.01의 직접 자식만 401개 → 첫 분기에 9비트 필요
- 42.2% 동사가 16비트 초과
- 최대 경로 40비트 (예산의 2.5배)
- **결론:** Primitive → Sub-primitive 2단계 degradation이 실용적 한계

---

## 최종 산출물 목록

### 핵심 데이터 파일

| 파일 | 규모 | 용도 |
|------|------|------|
| `geulso/wordnet/json/verb_bits.json` | **13,767개** (110,211줄) | **최종 동사 코드북** |
| `geulso/wordnet/json/verb559.json` | 559개 (3,918줄) | 루트 동사 + 분류 정보 |
| `geulso/wordnet/json/primitive-map.json` | 68개 (69줄) | Sub-primitive → 비트코드 매핑 |
| `geulso/wordnet/json/flat-verbs.json` | 559개 (3,763줄) | Sub-primitive별 동사 그룹 |
| `geulso/wordnet/json/sub_primitive_flats.json` | 68개 | 대안 인코딩 매핑 |
| `geulso/wordnet/verbtop559/sidx559.json` | 559개 | 루트 동사 확장 SIDX |
| `geulso/wordnet/verbtop559/verbclassified559.json` | 559개 | 전체 분류 메타데이터 |
| `geulso/wordnet/classified/*.json` | 10 파일 | Primitive별 그룹 |
| `geulso/wordnet/verbtrees/*.json` | 559 파일 | 개별 hyponym 트리 |

### 처리 스크립트

| 스크립트 | 역할 | Phase |
|----------|------|-------|
| `postgres.py` + `wordnet.sql` | WordNet DB 적재 | 1 |
| `ltree.sql` | hypernym 트리 스키마 | 1 |
| `countv.py` | 동사 synset 카운트 → 13,767 | 1 |
| `factorize/factorize.py` | LLM 의미소 분해 (41K JSON) | 2 |
| `factorize/validate.py` | synset 참조 검증 + LLM 교정 | 2 |
| `factorize/corrected.py` | 교정 적용 | 2 |
| `factorize/check.py` | 구조 검증 + 통계 | 2 |
| `verbtree.py` | hypernym 트리 구축 → 559 루트 발견 | 3 |
| `verbtop559.py` | 559 루트 추출 | 3 |
| `verbtop-primitive.py` | Primitive별 필터링 | 3 |
| `verbtrees.py` | 559 개별 트리 생성 | 4 |
| `sub_primitive_count.py` | 분포 집계 | 4 |
| `verbtrees_bit.py` | **16비트 코드 할당** | 5 |
| `valid_verb_bits.py` | **코드북 검증** | 5 |
| `valid_flat.py` | flat 일관성 검증 | 5 |

### DB 테이블

| 테이블 (geuldev) | 행 수 | 용도 |
|------------------|-------|------|
| `verb_hypernym_ltree` | 13,767 | 동사 계층 트리 |
| `wordnet_factorized_sememes` | ~33K | 동사 의미소 |
| `wordnet_factorized_qualifiers` | ~41K | 동사 한정자 |
| `wordnet_factorized_participants` | ~66K+ | 참여자 역할 |

---

## 핵심 설계 결정 기록

### 1. LLM 선택: Gemini > gpt-oss
- gpt-oss:20b는 synset 환각, 비일관적 추론 → Gemini 2.5 Flash 채택
- 의미소 분해 품질이 전체 파이프라인 품질을 좌우

### 2. 분류 체계: 2단계 (Primitive → Sub-primitive)
- WordNet 전체 트리 인코딩은 비현실적 (최대 40비트)
- 10 Primitive × 68 Sub-primitive가 실용적 granularity의 최적점

### 3. 코드 할당: Huffman 유사 가변길이
- 고빈도 sub-primitive에 짧은 prefix → 평균 코드 길이 최소화
- CHANGE-TRANSFORM(3,049개) = 4비트, PERCEIVE-FIND(소수) = 8비트

### 4. 트리 순회: DFS Pre-order
- 부모-자식 관계가 인접 코드로 표현됨
- 단, 의미적 유사도와 코드 근접성이 완벽히 일치하지는 않음 (알파벳순 × DFS)

### 5. CRUD v2: 예외 없는 의미소 모델
- v1의 monolithic `verb_type`이 11.5% 예외 원인
- {Operator, Property, Pattern} 3요소 분해로 모든 동사 표현 가능

### 6. Graceful Degradation: 2단계 제한 수용
- bit[1-8]까지만 의미적 degradation 가능 (68 sub-primitive 수준)
- bit[9-16]의 DFS index는 의미적 의미 없음 → 수용 가능한 트레이드오프
