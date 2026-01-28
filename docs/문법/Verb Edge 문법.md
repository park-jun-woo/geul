# Verb Edge 문법

**버전:** v0.5  
**작성일:** 2026-01-29  
**목적:** GEUL 서술문 표현을 위한 Verb Edge 패킷 구조 정의

---

## 1. 개요

Verb Edge는 사건/행위를 표현하는 핵심 Edge 타입이다.

두 가지 변형을 제공:
- **Short Verb Edge:** 3워드 (48비트) - 빈번한 간단 서술용
- **Verb Edge:** 5워드 (80비트) - 복잡한 정밀 서술용

Root/Inner를 Target참여자 필드로 통합하여 단일 구조로 운용한다.

---

## 2. Short Verb Edge (3워드 = 48비트)

### 2.1 구조

```
48비트 (3워드)
┌─────────┬──────────┬──────────┬───────────────┬──────────────┐
│ Prefix  │ 동사본문  │  한정자   │  참여자플래그  │ Target참여자 │
│  5비트  │  16비트   │  12비트  │    10비트     │    5비트     │
└─────────┴──────────┴──────────┴───────────────┴──────────────┘
```

| 필드 | 비트 | 설명 |
|------|------|------|
| Prefix | 5 | `1100 1` (표준 제안) |
| 동사본문 | 16 | 동사 ID (단순 나열, 65,536개) |
| 한정자 | 12 | 핵심 한정자만 |
| 참여자플래그 | 10 | 핵심 참여자 10개 |
| Target참여자 | 5 | 0=Root, 1-17=Inner |

### 2.2 한정자 (12비트)

| 비트 | 필드 | 크기 | 설명 |
|------|------|------|------|
| 0-1 | Tense | 2 | 시제 |
| 2-4 | Aspect | 3 | 상 |
| 5-6 | Polarity | 2 | 긍정/부정 |
| 7-8 | Mood | 2 | 서법 |
| 9-10 | Modality | 2 | 양태 |
| 11 | 예약 | 1 | - |

### 2.3 참여자 (10개)

| 비트 | 코드 | 역할 | 설명 |
|------|------|------|------|
| 0 | AGT | Agent | 의도적 행위자 |
| 1 | PAT | Patient | 피영향자 |
| 2 | THM | Theme | 대상 |
| 3 | RCP | Recipient | 수혜자 |
| 4 | LOC | Location | 장소 |
| 5 | SRC | Source | 출발점 |
| 6 | DST | Destination | 목적지 |
| 7 | INS | Instrument | 도구 |
| 8 | MNR | Manner | 방식 |
| 9 | CAU | Cause | 원인 |

### 2.4 용도

- 간단한 서술: "비가 온다", "철수가 뛴다"
- 로그/이벤트 스트림
- 경량/빈번 처리

---

## 3. Verb Edge (5워드 = 80비트)

### 3.1 구조

```
80비트 (5워드)
┌─────────┬──────────┬──────────┬───────────────┬──────────────┬───────┬────────┐
│ Prefix  │ 동사본문  │  한정자   │  참여자플래그  │ Target참여자 │ Voice │  예약  │
│  7비트  │  22비트   │  25비트  │    17비트     │    5비트     │ 2비트 │ 2비트  │
└─────────┴──────────┴──────────┴───────────────┴──────────────┴───────┴────────┘
```

| 필드 | 비트 | 설명 |
|------|------|------|
| Prefix | 7 | `1100 001` (표준 제안) |
| 동사본문 | 22 | 동사 ID (우아한 열화 구조) |
| 한정자 | 25 | 완전 한정자 |
| 참여자플래그 | 17 | 전체 참여자 17개 |
| Target참여자 | 5 | 0=Root, 1-17=Inner |
| Voice | 2 | 태 (능동/피동/사동/중간) |
| 예약 | 2 | 미래 확장용 |

### 3.2 동사본문 (22비트) - 우아한 열화

```
┌───────────┬───────────────┬───────────┬───────────┐
│ Primitive │ Sub_primitive │ Verb_idx  │ Desc_idx  │
│  가변     │    가변       │   가변    │   가변    │
└───────────┴───────────────┴───────────┴───────────┘
```

**Primitive (10개):**

| 코드 | Primitive | 비트 | 하위동사 |
|------|-----------|------|----------|
| 10 | CAUSE | 2 | 4,463 |
| 11 | CHANGE | 2 | 3,290 |
| 010 | MOVE | 3 | 2,152 |
| 011 | BE | 3 | 800 |
| 0010 | THINK | 4 | 729 |
| 0011 | COMMUNICATE | 4 | 552 |
| 00010 | TRANSFER | 5 | 508 |
| 00011 | SOCIAL | 5 | 355 |
| 00001 | PERCEIVE | 5 | 194 |
| 00000 | FEEL | 5 | 165 |

**열화 단계:**
1. 전체 일치: 정확한 동사
2. Desc_idx 손실: 유사 동사
3. Verb_idx 손실: 상위 동사
4. Sub_primitive 손실: Primitive만
5. 최소: Primitive만

### 3.3 한정자 (25비트)

| 비트 | 필드 | 크기 | 설명 |
|------|------|------|------|
| 0-1 | Evidentiality | 2 | 증거성 |
| 2-3 | Mood | 2 | 서법 |
| 4-5 | Modality | 2 | 양태 |
| 6-7 | Tense | 2 | 시제 |
| 8-10 | Aspect | 3 | 상 |
| 11-12 | Politeness | 2 | 공손 |
| 13-14 | Polarity | 2 | 긍정/부정 |
| 15-16 | Volitionality | 2 | 의도성 |
| 17-18 | Confidence | 2 | 확신성 |
| 19-21 | Iterativity | 3 | 반복성 |
| 22-24 | Intensity | 3 | 정도 |

#### 3.3.1 Intensity (3비트)

| 값 | 의미 | 예시 |
|----|------|------|
| 000 | 명시안함 | (기본) |
| 001 | 아주약함 | "살짝" |
| 010 | 약함 | "조금" |
| 011 | 보통 | "적당히" |
| 100 | 강함 | "꽤" |
| 101 | 아주강함 | "매우" |
| 110 | 극강 | "엄청" |
| 111 | 무한대강함 | "완전", "극도로" |

#### 3.3.2 양자화 (2비트 필드)

| 값 | 의미 | 수치 |
|----|------|------|
| 00 | 강한 부정 | -1.0 |
| 01 | 약한 부정 | -0.3 |
| 10 | 약한 긍정 | +0.3 |
| 11 | 강한 긍정 | +1.0 |

### 3.4 참여자플래그 (17비트)

| 비트 | 코드 | 역할 | 설명 |
|------|------|------|------|
| 0 | AGT | Agent | 의도적 행위자 |
| 1 | EXP | Experiencer | 경험자 |
| 2 | THM | Theme | 대상 |
| 3 | PAT | Patient | 피영향자 |
| 4 | RCP | Recipient | 수혜자 |
| 5 | BNF | Beneficiary | 수익자 |
| 6 | INS | Instrument | 도구 |
| 7 | MNR | Manner | 방식 |
| 8 | LOC | Location | 장소 |
| 9 | SRC | Source | 출발점 |
| 10 | DST | Destination | 목적지 |
| 11 | PTH | Path | 경로 |
| 12 | CAU | Cause | 원인 |
| 13 | PRP | Purpose | 목적 |
| 14 | COM | Comitative | 동반 |
| 15 | ATR | Attribute | 속성 |
| 16 | THN | Than | 비교기준 |

플래그가 켜진 순서대로 TID가 뒤따름.

### 3.5 Voice (2비트)

자연어 변환 시 표면 형태 힌트 제공:

| 값 | 의미 | 설명 | 예시 |
|----|------|------|------|
| 00 | 능동 (Active) | 주어가 행위 수행 | "철수가 책을 읽었다" |
| 01 | 피동 (Passive) | 주어가 행위 대상 | "책이 읽혔다" |
| 10 | 사동 (Causative) | 주어가 행위 유발 | "철수가 영희에게 책을 읽혔다" |
| 11 | 중간/재귀 (Middle) | 주어=대상 | "옷이 잘 입힌다" |

**설계 근거:**
- GEUL은 의미 구조 표현 → Voice로 의미 변화 없음
- 참여자(AGT/PAT)가 의미 결정
- Voice는 GEUL→자연어 변환 시 표면 형태 힌트
- 의미 동일, 표현 다름

**예시:**
```
read(AGT=철수, PAT=책)

Voice=00: "철수가 책을 읽었다"
Voice=01: "책이 철수에 의해 읽혔다"
```

---

## 4. Target참여자 (5비트)

Root/Inner 구분 및 수식 대상 지정 (Short/정식 공통):

| 값 | 의미 |
|----|------|
| 0 | Root Verb Edge (일반 서술) |
| 1 | Inner: AGT 수식 |
| 2 | Inner: EXP 수식 |
| 3 | Inner: THM 수식 |
| 4 | Inner: PAT 수식 |
| 5 | Inner: RCP 수식 |
| 6 | Inner: BNF 수식 |
| 7 | Inner: INS 수식 |
| 8 | Inner: MNR 수식 |
| 9 | Inner: LOC 수식 |
| 10 | Inner: SRC 수식 |
| 11 | Inner: DST 수식 |
| 12 | Inner: PTH 수식 |
| 13 | Inner: CAU 수식 |
| 14 | Inner: PRP 수식 |
| 15 | Inner: COM 수식 |
| 16 | Inner: ATR 수식 |
| 17 | Inner: THN 수식 |
| 18-31 | 예약 |

**Short Verb Edge가 Verb Edge를 수식할 수 있으므로 5비트(17개 커버) 필요.**

---

## 5. 패킷 구조

### 5.1 Short Verb Edge Root (Target=0)

```
[Short Verb Edge 3워드]
[Edge TID 1워드]
[참여자 TID × N]
───────────────────
총: 4 + N 워드
```

### 5.2 Short Verb Edge Inner (Target=1~17)

```
[Short Verb Edge 3워드]
[Edge TID 1워드]
[Parent Edge TID 1워드]
[참여자 TID × N]
───────────────────
총: 5 + N 워드
```

### 5.3 Verb Edge Root (Target=0)

```
[Verb Edge 5워드]
[Edge TID 1워드]
[참여자 TID × N]
───────────────────
총: 6 + N 워드
```

### 5.4 Verb Edge Inner (Target=1~17)

```
[Verb Edge 5워드]
[Edge TID 1워드]
[Parent Edge TID 1워드]
[참여자 TID × N]
───────────────────
총: 7 + N 워드
```

---

## 6. 혼용 예시

### 6.1 Short Root + Short Inner

**"웃으며 뛴다"**

```
V1 (Short Root): run
    AGT = E1
    Target = 0

V2 (Short Inner): smile
    Target = 1 (V1의 AGT 수식)
    Parent = V1
```

### 6.2 Verb Root + Short Inner

**"창을 든 네안데르탈인이 맘모스를 쫓았다"**

```
V1 (Verb Root): chase
    AGT = E1 (네안데르탈인)
    PAT = E2 (맘모스)
    한정자: 과거|완료
    Target = 0

V2 (Short Inner): hold
    PAT = E3 (창)
    Target = 1 (V1의 AGT 수식)
    Parent = V1
```

### 6.3 비교문

**"철수가 영희보다 빠르다"**

```
V1 (Verb Root): faster
    THM = E1 (철수)
    THN = E2 (영희)
    Target = 0
```

### 6.4 복합 수식

**"창을 든 네안데르탈인들이 창에 맞아 피를 흘리는 맘모스를 쫓았다"**

```
Entity:
  E1: 네안데르탈인들
  E2: 맘모스
  E3: 창
  E4: 피

V1 (Verb Root): chase
    AGT = E1
    PAT = E2
    Target = 0

V2 (Short Inner): hold
    PAT = E3
    Target = 1 (V1.AGT)
    Parent = V1

V3 (Short Inner): hit
    PAT = E2
    INS = E3
    Target = 4 (V1.PAT)
    Parent = V1

V4 (Short Inner): bleed
    AGT = E2
    THM = E4
    Target = 4 (V1.PAT)
    Parent = V1

Clause Edge:
  C1: CAUSE(V3, V4)
```

---

## 7. Prefix 할당 체계

| 타입 | Prefix | 비트 | 워드 |
|------|--------|------|------|
| Short Verb Edge | `1100 1` | 5 | 3 |
| Entity | `1100 01` | 6 | 4 |
| Verb Edge | `1100 001` | 7 | 5 |
| Triple Edge | `1100 0001` | 8 | 2 |
| Clause Edge | `1100 00001` | 9 | 1 |
| Event6 Edge | `1100 000001` | 10 | 1 |
| Context Edge | `1100 0000001` | 11 | 1 |
| Reserved | `1100 0000000` | 11 | - |

---

## 8. 선택 가이드

| 상황 | 선택 |
|------|------|
| 간단한 서술 (참여자 ≤3) | Short |
| 비교/복잡 서술 | Verb |
| 정밀 한정자 필요 | Verb |
| 대량 로그/스트림 | Short |
| Inner 수식 (간단) | Short |
| Inner 수식 (복잡) | Verb |

---

## 9. 설계 근거

### 9.1 Short/Verb 분리 이유

| | Short | Verb |
|--|-------|------|
| 빈도 | 80%+ | 20%- |
| 복잡도 | 낮음 | 높음 |
| 워드 | 3 | 5 |
| 평균 절감 | - | 40% |

**파레토 원리:** 80% 서술은 간단 → Short로 처리

### 9.2 Target 5비트 통합 이유

- Root/Inner 단일 구조
- Short ↔ Verb 혼용 지원
- 정식 Verb 17개 참여자 모두 수식 가능

### 9.3 ATR + THN 유지 이유

- ATR: Triple 대체 가능하나 편의상 유지
- THN: 비교 표현 필수

---

## 10. 향후 과제

- [ ] 동사 ID 할당 테이블 정의
- [ ] 우아한 열화 구조 상세 설계
- [ ] WMS 저장/인덱싱 최적화
- [ ] Short ↔ Verb 자동 승격/강등 규칙

---

## 11. 버전 이력

| 버전 | 일자 | 변경 |
|------|------|------|
| v0.1 | 2026-01-27 | 초안 |
| v0.2 | 2026-01-27 | 64비트 통합 |
| v0.3 | 2026-01-28 | Inner 통합, Target 5비트 |
| v0.4 | 2026-01-29 | Short/Verb 분리, 17개 참여자, Intensity 3비트 |
| v0.5 | 2026-01-29 | Voice 2비트 추가 (예약 4→2비트) |

---

**문서 종료**