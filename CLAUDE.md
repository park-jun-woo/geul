# GEUL (General Embedding vector Unified Language)

AI 시대를 위한 의미정렬 인공 언어이자 데이터 스트림 포맷.
인간과 AI가 모호성 없이 소통하기 위해 설계된 2바이트(65,536종) 기반 언어 체계.

**Author:** 박준우 (mail@parkjunwoo.com)
**License:** MIT

---

## 관련 레포

| 레포 | 경로 | 설명 |
|------|------|------|
| **geul-entity** (코드북) | `/mnt/c/Users/mail/git/geul-entity/` | Entity SIDX 48비트 코드북 (Wikidata 기반) |
| **geul-verb** (코드북) | `/mnt/c/Users/mail/git/geul-verb/` | 동사 SIDX 16비트 코드북 (WordNet 기반, 완료) |
| **geul-quantities** (코드북) | `/mnt/c/Users/mail/git/geul-quantities/` | Quantity Node 코드북 (스캐폴드) |
| **geul-ast** (코드북) | `/mnt/c/Users/mail/git/geul-ast/` | Faber Edge 코드북 (스캐폴드) |
| **silk** (하위프로젝트) | `/mnt/c/Users/mail/git/silk/` | SILK (Semantic Interlingua for Linked Knowledge) |
| **geul-org** (웹사이트) | `/mnt/c/Users/mail/git/geul-org/` | geul.org Hugo 정적 사이트. 12개 언어. S3+CloudFront 배포 |
| ~~geul-sidx~~ (아카이브) | `/mnt/c/Users/mail/git/geul-sidx-archived/` | entity/ 이관 후 아카이브. 참고용 |

---

## 프로젝트 구조

```
geul/
├── grammar/                 # GEUL 스트림 포맷 문법 명세 (확정)
│   ├── README.md            # 전체 개요 + Prefix 표 + 외부 레포 링크
│   ├── stream-format.md     # 스트림 포맷 규칙 (v0.2)
│   ├── clause-edge/         # 담화/논리 엣지 (RST 기반 16관계, v0.4)
│   ├── context-edge/        # 세계관/맥락 엣지 (64타입, v0.2)
│   ├── event6-edge/         # 6하원칙 사건 엣지 (가변 3~8워드, v0.2)
│   ├── group-edge/          # 집합/그룹 엣지 (7타입, v0.1)
│   ├── meta-node/           # 스트림 제어 노드 (6타입, v0.1)
│   └── triple-edge/         # 속성/관계 엣지 (Top63+확장, v0.4)
├── workspace/               # "왜?" 시리즈 작업 문서 (geul-org 글의 원고)
├── ideas/                   # 아이디어 및 설계 문서
│   ├── docs/                # 설계 문서 (현행)
│   │   ├── SIDX/            # SIDX 횡단 문서 (인코딩, 쿼리, 검수)
│   │   ├── Papers/          # 논문 초안 (오염방지, 추론분리, 쿼리 등)
│   │   ├── 문법/            # 패킷별 설계 문서 (Entity, Verb, Quantity, Faber)
│   │   ├── 분석/            # 적용 사례 분석
│   │   ├── 전략/            # 검증/공개/부트스트랩/인코더 전략
│   │   ├── 오피니언/         # 의견서 (GEUL 필요성, 7계층 등)
│   │   └── 데모/            # 데모 시나리오
│   ├── old_docs/            # 이전 버전 문서 (참고용)
│   ├── sshg/                # MRS 파서 (ACE→WordNet→Wikidata→LLM)
│   ├── bak/                 # 백업/실험 파일
│   └── geulso/              # 지식 추출 파이프라인 (잔여 파일)
├── draft/                   # 초안 (Meta Node v2, 발음규칙, DFC 논문)
├── notes/                   # 연구 일지 (2025/, 2026/)
├── go.mod                   # Go 모듈 (parkjunwoo.com/geul)
└── .gitignore               # .key, .venv, bak/ 제외
```

---

## 핵심 아키텍처

### SEGLAM (Self-Examination GEUL Architecture Model)

WMS(World Management System)를 중앙 허브로 하는 이중 순환 구조:

- **의식적 흐름 (Online):** 사용자 입력 → Encoder → 심상관리 → 쿼리생성 → WMS 인출 → 추론 → Decoder → 응답
- **무의식적 흐름 (Offline):** 경험 기록 → GEUL-Agent 성찰 → WMS 지식/절차 개선

### GEUL 스트림 포맷

모든 데이터는 16비트(1워드) 단위. Big Endian.

**10비트 Prefix 체계 (Proposal):**

| Prefix | 타입 | 용도 |
|--------|------|------|
| `0001 1` | Tiny Verb Edge | 고빈도 단순 서술 (2워드) |
| `0001 01` | Verb Edge | 일반 서술 (3~5워드) |
| `0001 001` | Entity Node | 개체 정의 (3~5워드) |
| `0001 000 110` | Triple Edge | 속성/관계 |
| `0001 000 101` | Clause Edge | 담화/논리 |
| `0001 000 100` | Event6 Edge | 6하원칙 사건 |
| `0001 000 011` | Context Edge | 세계관/맥락 |
| `0001 000 010` | Quantity Node | 물리량/수치 |
| `0001 000 001` | Faber Edge | 코드/AST |
| `0001 000 111` | Meta Node | 스트림 제어 |
| `0001 000 000 111` | Group Edge | 집합/그룹 |

### SIDX (Semantic-aligned Index)

64비트 전역 의미 식별자. 비트 자체에 의미를 인코딩.

- **비트 설계:** `1`=먼 미래(50%), `01`=미래(25%), `001`=표준(12.5%), `000`=자유(12.5%)
- **현재 사용:** `0001` Proposal 영역 (자유 영역 내 관례적 사용)
- **설계 헌장:** 1조 년 후에도 사용 가능한 언어, 하위 호환 절대 유지

---

## 기술 스택

| 항목 | 기술 |
|------|------|
| 언어 | Python 3.12 (핵심), Go 1.22 (유틸리티) |
| DB | PostgreSQL (ltree 확장 필수) |
| LLM API | Google Gemini (의미소 분해), Ollama (로컬 추론) |
| NLP | spaCy, NLTK, ACE Parser |
| Python 패키지 | psycopg2, delphin |

---

## 데이터베이스

### 접속 정보

| DB | 용도 | 연결 |
|----|------|------|
| geuldev | 원본 데이터 (READ ONLY) | `postgresql://geul_reader:test1224@localhost:5432/geuldev` |
| geulwork | 분석 결과 (READ/WRITE) | `postgresql://geul_writer:test1224@localhost:5432/geulwork` |

**주의:** WSL 환경에서 `psql` 명령어 사용 불가. 반드시 Python psycopg2 사용.

```python
import psycopg2
conn = psycopg2.connect(
    host="localhost", port=5432, dbname="geuldev",
    user="geul_reader", password="test1224"
)
```

### 주요 테이블 (geuldev)

| 테이블 | 행 수 | 용도 |
|--------|-------|------|
| entities | ~117M | 위키데이터 Q-ID |
| triples | ~1.7B | subject-property-object |
| entity_labels | ~725M | 언어별 레이블 |
| wordnet_synsets | ~118K | WordNet synset |
| verb_hypernym_ltree | 13,767 | 동사 상위어 트리 |
| wordnet_factorized_sememes | ~33K | 동사 의미소 |
| cc_news_sentences | ~12M | 뉴스 문장 |

**절대 규칙:** geuldev에 INSERT/UPDATE/DELETE 하지 않는다. 모든 결과는 geulwork에 저장.

---

## 핵심 데이터 구조

### 동사 체계

- **559개 루트 동사** → 10 Primitive → 68 Sub-primitive → 13,767 WordNet 동사
- **10 Primitive:** BE, PERCEIVE, FEEL, THINK, CHANGE, CAUSE, MOVE, COMMUNICATE, TRANSFER, SOCIAL
- **32비트 Verb SIDX:** Prefix(8) + Primitive(3-5) + Sub-primitive(2-4) + Verb Index(1-5) + Padding
- **32비트 한정자:** Evidentiality(2) + Mood(2) + Modality(2) + Tense(2) + Aspect(3) + Politeness(2) + Polarity(2) + Volitionality(2) + Confidence(2) + Iterativity(4) + Reserved(9)
- **16개 참여자 역할:** Agent, Experiencer, Theme, Patient, Recipient, Beneficiary, Instrument, Manner, Location, Source, Destination, Path, Cause, Purpose, Comitative, Attribute

### Entity 체계

- **64비트 Entity SIDX:** Prefix(7) + Mode(3) + EntityType(6) + Attributes(48)
- **Mode 8가지:** 등록, 특정단수, 특정소수, 특정다수, 전칭, 존재, 불특정, 총칭
- **64개 EntityType:** Human, Taxon, Gene, Chemical, Star, ... (geul-entity/references/entity_types_64.json)
- **48비트 속성:** 타입별 완전 독립 스키마 (geul-entity/references/type_schemas.json)
- **커버리지:** 108.8M 개체 (Wikidata 전체의 92.7%), 충돌률 < 0.01%

---

## 프로젝트 현황

### 완료

- [x] GEUL 개요서 및 핵심 설계 문서
- [x] SIDX 64비트 비트 명세서 (v0.11)
- [x] 동사 SIDX 32비트 체계 (559 루트, 10 Primitive, 68 Sub-primitive)
- [x] Verb Edge 문법 (Tiny/Short/Full 3단계 압축)
- [x] Entity SIDX 가변 워드 구조 (Lane 분기, 3/5워드)
- [x] 10비트 Prefix 체계 확정
- [x] 전체 문법 명세서 초안 (10개 패킷 타입)
- [x] 스트림 포맷 규칙 (TID 4원칙)
- [x] Entity 64개 타입 + 48비트 스키마 설계 완료
- [x] 발음 규칙 (CV 구조, 1바이트=1음절)

### 진행 중 / TODO

- [ ] Phase 5: Entity 코드북 상세 생성
- [ ] Phase 6: Entity 인코더 프로토타입
- [ ] CRUD v2 동사 의미소 검증
- [ ] 인코더/디코더 PoC 구현
- [ ] 실제 문장 GEUL 변환 테스트

---

## 작업 규칙

1. **문서 언어:** 한국어 우선, 기술 용어는 영문 병기
2. **DB 안전:** geuldev는 절대 쓰기 금지, geulwork만 사용
3. **DB 접속:** psql 사용 불가, Python psycopg2 사용
4. **바이트 오더:** Big Endian (Network Byte Order)
5. **비트 규칙:** bit1 = MSB, bit64 = LSB
6. **커밋:** Co-Authored-By 트레일러 넣지 않는다
8. **설계 원칙:**
   - 우아한 열화 (Graceful Degradation): 비트를 덜 채울수록 더 추상적 표현
   - 지식의 화이트박스화: 모든 정보는 출처/시점/신뢰도 명시
   - 상호 이해성: 인간과 AI 모두 읽고 쓸 수 있는 구조
   - 하위 호환 절대 유지: 한 번 정의된 비트 패턴의 의미는 영구 불변
