# GEUL (General Embedding vector Unified Language)

AI 시대를 위한 **의미정렬 인공 언어**이자 **데이터 스트림 포맷**.

인간과 AI가 모호성 없이 소통하기 위해 설계된 2바이트(65,536종) 기반 언어 체계입니다.

## Why GEUL?

자연어는 모호합니다. 같은 문장도 문맥에 따라 의미가 달라지고, LLM은 이 모호성 위에서 확률적으로 추론합니다.

GEUL은 **의미 자체를 비트로 인코딩**합니다. 모든 동사, 개체, 관계, 맥락이 고유한 비트 패턴을 가지며, 해석의 여지가 없습니다.

```
자연어: "He broke the record"  →  깨뜨렸다? 기록을 세웠다?
GEUL:   Verb(CHANGE.break) + Entity(record) + Event6(...)  →  하나의 의미
```

## Core Concepts

### SIDX (Semantic-aligned Index)

64비트 전역 의미 식별자. 비트 자체에 의미를 인코딩합니다.

- `1`=먼 미래(50%), `01`=미래(25%), `001`=표준(12.5%), `000`=자유(12.5%)
- 현재 `0001` Proposal 영역 사용
- 설계 헌장: 1조 년 후에도 사용 가능, 하위 호환 절대 유지

### Stream Format

모든 데이터는 16비트(1워드) 단위, Big Endian.

| Prefix | Type | Purpose |
|--------|------|---------|
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

### SEGLAM (Self-Examination GEUL Architecture Model)

WMS(World Management System)를 중앙 허브로 하는 이중 순환 구조:

- **의식적 흐름 (Online):** 사용자 입력 → Encoder → 심상관리 → 쿼리생성 → WMS 인출 → 추론 → Decoder → 응답
- **무의식적 흐름 (Offline):** 경험 기록 → GEUL-Agent 성찰 → WMS 지식/절차 개선

### Verb System

559개 루트 동사 → 10 Primitive → 68 Sub-primitive → 13,767 WordNet 동사

**10 Primitive:** BE, PERCEIVE, FEEL, THINK, CHANGE, CAUSE, MOVE, COMMUNICATE, TRANSFER, SOCIAL

- **32비트 Verb SIDX:** Prefix(8) + Primitive(3-5) + Sub-primitive(2-4) + Verb Index(1-5) + Padding
- **32비트 한정자:** Evidentiality(2) + Mood(2) + Modality(2) + Tense(2) + Aspect(3) + Politeness(2) + Polarity(2) + Volitionality(2) + Confidence(2) + Iterativity(4) + Reserved(9)
- **16개 참여자 역할:** Agent, Experiencer, Theme, Patient, Recipient, Beneficiary, Instrument, Manner, Location, Source, Destination, Path, Cause, Purpose, Comitative, Attribute

### Entity System

64개 EntityType으로 Wikidata 108.8M 개체(92.7%)를 커버합니다.

- **64비트 Entity SIDX:** Prefix(7) + Mode(3) + EntityType(6) + Attributes(48)
- **Mode 8가지:** 등록, 특정단수, 특정소수, 특정다수, 전칭, 존재, 불특정, 총칭
- 충돌률 < 0.01%

## Project Structure

```
geul/
├── grammar/                 # GEUL 스트림 포맷 문법 명세
│   ├── clause-edge/         # 담화/논리 엣지
│   ├── context-edge/        # 세계관/맥락 엣지
│   ├── event6-edge/         # 6하원칙 사건 엣지
│   ├── group-edge/          # 집합/그룹 엣지
│   ├── meta-node/           # 스트림 제어 노드
│   └── triple-edge/         # 속성/관계 엣지
├── ideas/                   # 아이디어 및 설계 문서
├── draft/                   # 초안 (아이디어 이상, 논문 미만)
└── notes/                   # 연구 일지
```

### Related Repositories

| Repository | Type | Description |
|------------|------|-------------|
| [geul-entity](https://github.com/park-jun-woo/geul-entity) | Codebook | Entity SIDX 48비트 코드북 (Wikidata 기반) |
| [geul-verb](https://github.com/park-jun-woo/geul-verb) | Codebook | 동사 SIDX 16비트 코드북 (WordNet 기반, 완료) |
| [geul-quantities](https://github.com/park-jun-woo/geul-quantities) | Codebook | Quantity Node 코드북 (스캐폴드) |
| [geul-ast](https://github.com/park-jun-woo/geul-ast) | Codebook | Faber Edge 코드북 (스캐폴드) |
| [silk](https://github.com/park-jun-woo/silk) | Subproject | SILK (Semantic Interlingua for Linked Knowledge) |
| [geul-org](https://github.com/park-jun-woo/geul-org) | Website | geul.org Hugo 정적 사이트 (12개 언어) |

## Status

### Done

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

### TODO

- [ ] Phase 5: Entity 코드북 상세 생성
- [ ] Phase 6: Entity 인코더 프로토타입
- [ ] CRUD v2 동사 의미소 검증
- [ ] 인코더/디코더 PoC 구현
- [ ] 실제 문장 GEUL 변환 테스트

## Design Principles

- **Graceful Degradation** -- 비트를 덜 채울수록 더 추상적 표현
- **White-box Knowledge** -- 모든 정보는 출처/시점/신뢰도 명시
- **Mutual Intelligibility** -- 인간과 AI 모두 읽고 쓸 수 있는 구조
- **Absolute Backward Compatibility** -- 한 번 정의된 비트 패턴의 의미는 영구 불변

## Website

[geul.org](https://geul.org) -- 12개 언어 지원 ([geul-org](https://github.com/park-jun-woo/geul-org))

## License

[MIT](LICENSE) -- Copyright (c) 2025 Park Jun Woo
