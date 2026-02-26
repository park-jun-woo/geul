# GEUL (General Embedding vector Unified Language)

AI 시대를 위한 의미정렬 인공 언어이자 데이터 스트림 포맷.
인간과 AI가 모호성 없이 소통하기 위해 설계된 2바이트(65,536종) 기반 언어 체계.

**Author:** 박준우 (mail@parkjunwoo.com)
**License:** MIT

---

## 웹사이트 (geul.org)

Hugo 정적 사이트. 12개 언어, S3+CloudFront 배포.

### Languages (12)

en(기본, URL prefix 없음), ko, zh, es, ar(**RTL**), pt, id, ru, ja, fr, de, he(**RTL**)

### Hugo 구조

```
hugo/
├── hugo.toml / Makefile
├── content/{en,ko,zh,es,ar,pt,id,ru,ja,fr,de,he}/
│   ├── _index.md                    # 홈
│   └── why/                         # "왜?" 시리즈 (16글)
│       ├── 16-bit.md / cache-reasoning-as-code.md / claims-not-facts.md
│       ├── semantically-aligned-index.md / structured-memory.md
│       ├── artificial-language/     # 인공언어 (3글)
│       └── context-engineering/     # 컨텍스트 엔지니어링 (7글)
├── layouts/                         # 외부 테마 없음
│   ├── index.html                   # 홈
│   ├── _default/{baseof,single,list,languages}.html
│   ├── _default/_markup/render-link.html  # 링크 렌더러 (noopener)
│   ├── partials/{head,header,footer,schema}.html
│   ├── why/list.html
│   ├── robots.txt / 404.html
├── assets/css/main.css              # 라이트 테마, Noto Serif, RTL, 반응형
├── static/images/                   # WebP OG 이미지
├── deployments/terraform/
└── public/                          # Hugo 출력
```

### Front Matter

```yaml
---
title: "Title"
date: 2026-02-26T12:00:00+09:00
lastmod: 2026-02-26T12:00:00+09:00
tags: ["tag1", "tag2"]
summary: "Meta description용 1문단 요약 (한글 ~80자, 영문 ~155자)"
author: "박준우"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---
```

### Commands

Hugo 경로: `/home/parkjunwoo/bin/hugo`

```bash
make serve     # hugo server -D
make build     # hugo --minify → public/
make clean     # rm -rf public/
make deploy    # build + S3 sync + XML content-type fix + CF invalidation + IndexNow
```

배포 시 `CF_DIST_ID=E2Z17ZOR6DJTRZ make deploy`

### AWS Deployment

```
Route53 (geul.org, www) → CloudFront (E2Z17ZOR6DJTRZ) → S3 (geul-org-public) via OAC
```

| 서비스 | 리소스 | 비고 |
|--------|--------|------|
| S3 | `geul-org-public` / `geul-logs` | 사이트 호스팅 (OAC) / 로그 (90일) |
| CloudFront | `E2Z17ZOR6DJTRZ` | HTTPS redirect, CachingOptimized, 압축 |
| CF Function | `geul-public-router` | 언어 감지(cookie→Accept-Language) + clean URL |
| ACM | `www.geul.org` + SAN `geul.org` | us-east-1 |
| Route53 | `geul.org` zone (`Z09654152WX7070IWCD4A`) | A×2(apex+www→CF) |
| IAM | `geul-deployer` | S3 sync + CF invalidation |

**Terraform** (`hugo/deployments/terraform/`): Region ap-northeast-2 / us-east-1(CF,ACM)

### IndexNow

Makefile에 `INDEXNOW_KEY` 미설정 (TODO). 설정 후 `make deploy` 시 자동 제출.

### URL Convention

`/why/natural-language-hallucination/` (en) · `/{lang}/why/natural-language-hallucination/` (기타)

슬러그: 영문 소문자 하이픈, 관사 제거, 3~5단어, 모든 언어 동일 파일명

### Cross-linking

geul.org ↔ parkjunwoo.com 상호 백링크 (SEO)
- footer → `parkjunwoo.com/1/en/about/` · GitHub

### Google Search Console

- GCP: `claribot-488401` | SA: `claude-code@claribot-488401.iam.gserviceaccount.com`
- SA 키: `~/.config/gcloud/claude-code-sa-key.json`
- 사이트: `sc-domain:geul.org` (SA 권한 미등록 — 수동 추가 필요)

```bash
# SA 활성화
gcloud auth activate-service-account claude-code@claribot-488401.iam.gserviceaccount.com \
  --key-file=~/.config/gcloud/claude-code-sa-key.json
# 검색 실적 조회
curl -s -X POST -H "Authorization: Bearer $(gcloud auth print-access-token --scopes=https://www.googleapis.com/auth/webmasters)" \
  -H "Content-Type: application/json" \
  -d '{"startDate":"2026-02-01","endDate":"2026-02-26","dimensions":["query"],"rowLimit":10}' \
  "https://searchconsole.googleapis.com/webmasters/v3/sites/sc-domain%3Ageul.org/searchAnalytics/query"
```

### SEO 체크리스트

- `<title>` = `{글 제목} — {사이트 제목}` (head.html)
- `<meta name="description">` = frontmatter `summary`
- H1은 템플릿(single.html)에서 자동 생성 → 마크다운에 `#` 사용 금지, `##`부터 시작
- OG: `og:title`, `og:description`, `og:image`(frontmatter `image:`), `og:locale`
- twitter:card: 이미지 있으면 `summary_large_image`, 없으면 `summary`
- Schema.org: Article(headline, date, author, image) + BreadcrumbList
- hreflang: 12개 언어 + `x-default`(en) 자동 생성
- canonical URL 자동
- taxonomy(tags) 페이지: `noindex, follow`
- CSS minify + fingerprint

---

## 프로젝트 구조

```
geul/
├── hugo/                    # 웹사이트 (geul.org)
├── docs/                    # 설계 문서 (현행)
│   ├── GEUL 개요서.md        # 핵심 아키텍처 개요
│   ├── GEUL 마일스톤.md      # 프로젝트 로드맵
│   ├── 문법/                # GEUL 스트림 포맷 문법 명세
│   │   ├── Verb Edge.md     # 동사 엣지 (Tiny/Short/Full)
│   │   ├── Triple Edge.md   # 속성/관계 엣지
│   │   ├── Clause Edge.md   # 담화/논리 엣지
│   │   ├── Event6 Edge.md   # 6하원칙 사건 엣지
│   │   ├── Context Edge.md  # 세계관/출처/맥락 엣지
│   │   ├── Faber Edge.md    # 코드/AST 엣지
│   │   ├── Group Edge.md    # 집합/그룹 엣지
│   │   ├── Meta Node.md     # 스트림 메타데이터 노드
│   │   ├── Quantity Node.md # 물리량/수치 노드
│   │   └── Pronunciation Rules.md  # 바이트→음절 발음 규칙
│   ├── SemanticOntology/    # 의미론 체계
│   │   ├── SIDX.md → entity/references/SIDX.md 참조
│   │   ├── UID.md           # 64비트 통합 식별자
│   │   ├── 동사 상위 분류.md  # 10 Primitive, 68 Sub-primitive
│   │   ├── 개체 상위 분류.md  # 8비트 개체 분류 트리
│   │   ├── 동사 의미 한정자 목록.md  # 시제/상/서법 등 22비트
│   │   └── 참여자.md         # 16개 의미역 (Agent, Patient 등)
│   ├── 전략/                # 전략 문서
│   ├── Papers/              # 연구 논문
│   ├── 오피니언/             # 의견서
│   └── 데모/                # 데모 시나리오
├── entity/                  # Entity SIDX 인코딩 시스템 (별도 CLAUDE.md 있음)
│   ├── CLAUDE.md            # Entity 서브프로젝트 상세 가이드
│   ├── references/          # SIDX 명세, 64개 EntityType, 코드북
│   ├── scripts/             # 인코딩 파이프라인 스크립트
│   ├── templates/           # 프롬프트 템플릿
│   └── cache/               # DB 스키마 캐시
├── geulso/                  # 지식 추출 파이프라인
│   ├── factorize/           # LLM 기반 동사 의미소 분해
│   ├── wordnet/             # WordNet 동사 계층 구축
│   ├── wikidata/            # Wikidata 개체 통합
│   └── ccnews/              # Common Crawl 뉴스 처리
├── sshg/                    # MRS(Minimal Recursion Semantics) 파서
│   └── mrs.py               # ACE→WordNet→Wikidata→LLM 파이프라인
├── note/                    # 연구 일지 (날짜별)
├── bak/                     # 백업/실험 파일
├── old_docs/                # 이전 버전 문서 (참고용)
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
- **64개 EntityType:** Human, Taxon, Gene, Chemical, Star, ... (entity/references/entity_types_64.json)
- **48비트 속성:** 타입별 완전 독립 스키마 (entity/references/type_schemas.json)
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
2. **파일 경로:** entity/ 서브프로젝트는 해당 폴더 내에서만 파일 생성/수정
3. **DB 안전:** geuldev는 절대 쓰기 금지, geulwork만 사용
4. **DB 접속:** psql 사용 불가, Python psycopg2 사용
5. **바이트 오더:** Big Endian (Network Byte Order)
6. **비트 규칙:** bit1 = MSB, bit64 = LSB
7. **설계 원칙:**
   - 우아한 열화 (Graceful Degradation): 비트를 덜 채울수록 더 추상적 표현
   - 지식의 화이트박스화: 모든 정보는 출처/시점/신뢰도 명시
   - 상호 이해성: 인간과 AI 모두 읽고 쓸 수 있는 구조
   - 하위 호환 절대 유지: 한 번 정의된 비트 패턴의 의미는 영구 불변
