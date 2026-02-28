# GEUL SIDX 코드북 현황

GEUL SIDX 아키텍처가 사용하는 코드북 작업 상태.

---

## 동사 코드북 — 완성

WordNet 13,767개 동사 synset → 16비트 의미정렬 코드북.

| 항목 | 수치 |
|------|------|
| 총 동사 | 13,767 |
| 고유 16비트 코드 | 13,767 (충돌 0) |
| 분류 체계 | 10 Primitive → 68 Sub-primitive → 559 Root → 13,767 Leaf |
| 인코딩 | Huffman 유사 가변길이 (4~8비트 prefix + DFS index) |
| 최종 산출물 | `wordnet/json/verb_bits.json` |

### 분류 체계

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

### Graceful Degradation

```
bit[1-4]:   Primitive 수준 (10종)
bit[1-8]:   Sub-primitive 수준 (68종)
bit[1-16]:  개별 동사 (13,767종)
```

### SIDX 타입 매핑

SIDX 비트 분기(`SIDX.md` 참조)에서 동사 코드북은 다음 Proposal Prefix에 대응:

| Prefix | 비트 | SIDX 타입 |
|--------|------|-----------|
| `0001 1` | 5 | Tiny Verb Edge (고빈도 2워드) |
| `0001 01` | 6 | Verb Edge (일반 3~5워드) |

---

## 엔티티 코드북 — 진행 중

Wikidata 108.8M 개체 → Entity Node (Prefix 7b + Mode 3b + EntityType 6b + Attributes 32b = 48비트).

| 항목 | 수치 |
|------|------|
| SIDX 대상 | 108,854,572 (Wikimedia 내부 제외) |
| EntityType | 64종 (6비트) |
| Mode | 8종 (3비트): 등록/특정단수/특정소수/특정다수/전칭/존재/불특정/예약 |
| Attributes | 타입별 가변 스키마 (32비트) |
| SIDX 생성 | 108,878,520 (100%) |
| 속성 인코딩 | 17,442,999 (16.0%) |

### Entity Node 구조 (v0.3)

```
1st WORD (16비트)
┌─────────┬──────┬────────────┐
│ Prefix  │ Mode │ EntityType │
│  7bit   │ 3bit │   6bit     │
└─────────┴──────┴────────────┘

2nd WORD (16비트)
┌─────────────────────────────┐
│     Attributes 상위 16비트   │
└─────────────────────────────┘

3rd WORD (16비트)
┌─────────────────────────────┐
│     Attributes 하위 16비트   │
└─────────────────────────────┘

Proposal Prefix: 0001 001 (7비트)
```

### 타입별 진행

| 타입 | 이름 | 개체 수 | 속성 인코딩 | 비율 |
|------|------|---------|-------------|------|
| 0x00 | Human | 12,553,670 | 12,182,686 | 97.0% |
| 0x03 | Taxon | 3,904,250 | 3,531,305 | 90.5% |
| 0x08 | Star | 4,843,949 | 1,729,008 | 35.7% |
| 0x16 | Document | 45,000,000 | 24,478 | 3.5% |
| 0x3F | Unknown | 19,678,178 | 0 | 0.0% |

### 잔여 과제

**긴급 — 62.2% 분류 실패 해소:**
- Q6256(Country), Q3624078(Sovereign State) → `entity/references/primary_mapping.json` 추가
- Q5864(G-type Star) → Star(0x08) 매핑 추가
- Q55983715(Common Name Taxon) → Taxon(0x03) 매핑 추가
- P279 체인 탐색 구현 (최대 5홉)

**중기 — 스키마 정제:**
- 과도한 세분화 타입 통합 (Settlement/Village/Hamlet 등)
- 누락 타입 추가 (Country, City, University 등)
- 속성 인코딩률 16.0% → 70%+ 개선

### 검색 아키텍처 (설계 완료)

```
사전 구축: ~35,000 leaf entries (~1MB, L2 캐시 적재)
  ("Human", "country", "Korea") → { mask: 0x..., value: 0x... }

쿼리 파이프라인:
  사용자 쿼리 → 소형 LLM (의미 파싱) → Dictionary (마스크 조립) → SIMD 스캔
```

### 참조 데이터

| 파일 | 크기 | 용도 |
|------|------|------|
| `entity/references/entity_types_64.json` | 11.7KB | 64개 타입 정의 + QID 매핑 |
| `entity/references/type_schemas.json` | 83KB | 48비트 속성 스키마 |
| `entity/references/codebooks_full.json` | 283KB | QID → 코드 매핑 |
| `entity/references/type_mapping.json` | 7.7KB | 하위타입 → 64타입 매핑 |

---

## GEUL SIDX 인코딩에서의 활용

### 비트 분기와 코드북

```
SIDX Proposal Prefix (0001) 내부 분기:

  0001 1      → Tiny Verb Edge: verb_bits.json 상위 코드 (2워드)
  0001 01     → Verb Edge: verb_bits.json 전체 16비트 코드 (3~5워드)
  0001 001    → Entity Node: EntityType 6b + Attributes 32b (3워드)
```

### 인코딩 흐름

```
동사:
  verb_bits.json (16비트, 즉시 사용 가능)
  → Primitive 4비트로 잘라 쓰면 Tiny Verb Edge
  → 전체 16비트 쓰면 Verb Edge

엔티티:
  sidx.yaml 코드북 정의 → LLM 배치 태깅 → 유효성 검증 → 비트 조립
  → EntityType 6비트 + Attributes 32비트 = 38비트 의미정렬
```

### 검색

```
Entity Node SIMD 검색:
  64비트 배열에서 (sidx & mask) == pattern 인 엔티티만 통과
  → 1.08억건 → 수백~수천건으로 축소 (밀리초 단위)
  → 후보군에 LLM 전수 검사

예시 — "한국 정치인":
  mask:    EntityType=Human AND Attributes.country=Korea AND Attributes.subtype=Politician
  pattern: 해당 비트 패턴
  결과:    ~1,962건
```

### 관련 문서

| 문서 | 내용 |
|------|------|
| `docs/SIDX.md` | 64비트 최상위 비트 분기 구조 |
| `docs/Entity Node.md` | Entity Node 상세 (v0.3) |
| `docs/SIDX인코딩방법.md` | sidx.yaml 코드북 → LLM 태깅 → 비트 조립 파이프라인 |
| `docs/entity-sidx-다음단계.md` | 현재 상태 및 로드맵 |
