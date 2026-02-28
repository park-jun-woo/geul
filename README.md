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

### Verb System

559개 루트 동사 → 10 Primitive → 68 Sub-primitive → 13,767 WordNet 동사

**10 Primitive:** BE, PERCEIVE, FEEL, THINK, CHANGE, CAUSE, MOVE, COMMUNICATE, TRANSFER, SOCIAL

### Entity System

64개 EntityType으로 Wikidata 108.8M 개체(92.7%)를 커버합니다.

- **64비트 Entity SIDX:** Prefix(7) + Mode(3) + EntityType(6) + Attributes(48)
- 충돌률 < 0.01%

## Project Structure

```
geul/
├── docs/           # 설계 문서 및 문법 명세
├── entity/         # Entity SIDX 인코딩 시스템
├── geulso/         # 지식 추출 파이프라인 (WordNet, Wikidata, CCNews)
├── sshg/           # MRS 파서 (ACE → WordNet → Wikidata → LLM)
├── papers/         # 연구 논문
└── note/           # 연구 일지
```

## Design Principles

- **Graceful Degradation** -- 비트를 덜 채울수록 더 추상적 표현
- **White-box Knowledge** -- 모든 정보는 출처/시점/신뢰도 명시
- **Mutual Intelligibility** -- 인간과 AI 모두 읽고 쓸 수 있는 구조
- **Absolute Backward Compatibility** -- 한 번 정의된 비트 패턴의 의미는 영구 불변

## Website

[geul.org](https://geul.org) -- 12개 언어 지원 ([repository](https://github.com/park-jun-woo/geul-org))

## License

[MIT](LICENSE) -- Copyright (c) 2025 Park Jun Woo
