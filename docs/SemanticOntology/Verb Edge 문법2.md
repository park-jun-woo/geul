# Verb Edge 명세서

**버전:** v0.2  
**작성일:** 2026-01-27  
**목적:** GEUL 서술문 표현을 위한 Verb Edge 패킷 구조 정의

---

## 1. 개요

Verb Edge는 사건/행위를 표현하는 핵심 Edge 타입이다. 64비트 고정 구조에 동사, 한정자, 참여자 플래그를 모두 포함하여 효율적인 서술을 가능하게 한다.

---

## 2. 64비트 Verb Edge 구조

```
64비트 (4워드)
┌─────────┬──────────────┬──────────────┬───────────────┐
│ Prefix  │   동사본문    │    한정자     │  참여자플래그  │
│  5비트  │    22비트     │    22비트    │    15비트     │
└─────────┴──────────────┴──────────────┴───────────────┘
```

| 필드 | 비트 | 설명 |
|------|------|------|
| Prefix | 5 | Verb Edge 타입 식별 |
| 동사본문 | 22 | Primitive + Sub_prim + Verb_idx + Desc_idx |
| 한정자 | 22 | 시제, 상, 서법, 양태 등 |
| 참여자플래그 | 15 | 참여자 존재 비트마스크 |

---

## 3. 동사본문 구조 (22비트)

### 3.1 비트 할당 (제안2 기준)

```
동사본문 22비트
├── Primitive: 2~5비트 (빈도 기반 가변)
├── Sub_primitive: 2~4비트
├── Verb_index: 1~5비트
└── Descendant_index: 0~11비트
```

### 3.2 Primitive 비트 할당

| Primitive | 코드 | 비트 | 하위동사 |
|-----------|------|------|----------|
| CAUSE | 10 | 2 | 4,463 |
| CHANGE | 11 | 2 | 3,290 |
| MOVE | 010 | 3 | 2,152 |
| BE | 011 | 3 | 800 |
| THINK | 0010 | 4 | 729 |
| COMMUNICATE | 0011 | 4 | 552 |
| TRANSFER | 00010 | 5 | 508 |
| SOCIAL | 00011 | 5 | 355 |
| PERCEIVE | 00001 | 5 | 194 |
| FEEL | 00000 | 5 | 165 |

### 3.3 비트 길이 통계

- 평균: 25.9비트 (여유 6.1비트)
- 최대: 30비트 (여유 2비트)
- 총 동사: 13,767개

---

## 4. 한정자 구조 (22비트)

| 비트 | 필드 | 크기 | 설명 |
|------|------|------|------|
| 0-1 | Evidentiality | 2 | 증거성 (추론/직접/전언) |
| 2-3 | Mood | 2 | 서법 (가정/서술/명령) |
| 4-5 | Modality | 2 | 양태 (의지 정도) |
| 6-7 | Tense | 2 | 시제 (과거/현재/미래) |
| 8-10 | Aspect | 3 | 상 (진행/완료/결과) |
| 11-12 | Politeness | 2 | 공손 (반말/중립/존대) |
| 13-14 | Polarity | 2 | 긍정/부정 |
| 15-16 | Volitionality | 2 | 의도성 |
| 17-18 | Confidence | 2 | 확신성 |
| 19-21 | Iterativity | 3 | 반복성 (0-7) |

### 4.1 양자화 (2비트 → 4단계)

| 값 | 의미 | 수치 |
|----|------|------|
| 00 | 강한 부정 | -1.0 |
| 01 | 약한 부정 | -0.3 |
| 10 | 약한 긍정 | +0.3 |
| 11 | 강한 긍정 | +1.0 |

---

## 5. 참여자 플래그 (15비트)

플래그 비트 위치 = 참여자 ID. 켜진 순서대로 TID가 뒤따름.

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

**Note:** ATR(Attribute)는 Triple-GEUL로 처리.

---

## 6. 패킷 구조

### 6.1 Verb Edge Packet

| 순서 | 필드 | 크기 | 설명 |
|------|------|------|------|
| 1 | Verb Edge | 4워드 (64비트) | 동사 + 한정자 + 참여자플래그 |
| 2 | Edge TID | 1워드 (16비트) | 이 Edge의 TID 선언 |
| 3+ | 참여자 TID | 각 1워드 | 플래그 순서대로 가변 |

### 6.2 패킷 길이 계산

```
패킷 길이 = 5 + popcount(참여자 플래그)
```

| 참여자 수 | 패킷 길이 | 예시 |
|-----------|-----------|------|
| 0 | 5워드 | 날씨 ("비가 온다") |
| 1 | 6워드 | 자동사 ("철수가 뛴다") |
| 2 | 7워드 | 타동사 ("철수가 공을 찬다") |
| 3 | 8워드 | 수여동사 ("철수가 영희에게 책을 줬다") |

---

## 7. Verb Inner Edge

서술 내부에서 참여자를 수식하는 Edge 타입.

### 7.1 용도

| 용도 | 예시 |
|------|------|
| 동반 상태 | "창을 든 채로" |
| 동시 행위 | "웃으면서 떠났다" |
| 방식 | "뛰어서 갔다" |
| 조건 | "술 취한 상태로 운전" |

### 7.2 구조

```
Verb Inner Edge: 4워드 (64비트)
├── Prefix: 5비트 (Inner 타입)
├── 관계타입: 3비트 (동반/동시/방식/조건)
├── 동사본문: 22비트
├── 한정자: 22비트
└── 대상참여자: 12비트

Inner TID: 1워드
Parent Edge TID: 1워드
[참여자 TID...]
```

### 7.3 예시

**"창을 든 네안데르탈인이 맘모스를 쫓아간다":**

```
Entity 선언:
  네안데르탈인: T01
  맘모스: T02
  창: T03

Verb Edge (E01):
  chase.v.01 | AGT+PAT | TID=E01
  Agent: T01 (네안데르탈인)
  Patient: T02 (맘모스)

Verb Inner Edge:
  hold.v.01 | Parent=E01 | Target=AGT
  Patient: T03 (창)
```

### 7.4 Triple 승격

반복 패턴 발견 시 자동 승격:

```python
if inner_edge_count(entity, verb, object) > threshold:
    # Verb Inner → Entity Triple로 승격
    create_triple(entity, "typically_" + verb, object)
```

---

## 8. Context Edge

서술의 맥락(출처, 시간, 신뢰도)은 별도 Edge로 처리.

### 8.1 이유

- 64비트 Verb Edge 이미 꽉 참
- 같은 맥락 여러 서술에서 재사용
- 필요할 때만 첨부

### 8.2 연결 방식

**Triple-GEUL로 연결:**
```
Triple(VerbEdge_TID, P:context, Context_TID)
Triple(Context_TID, P:source, "Reuters")
Triple(Context_TID, P:time, "2025-03-15")
Triple(Context_TID, P:confidence, 0.9)
```

---

## 9. 예시

### 9.1 "철수가 영희에게 책을 줬다"

**Entity 선언:**
```
철수: [SIDX 4워드][TID T01] = 5워드
영희: [SIDX 4워드][TID T02] = 5워드
책:   [SIDX 4워드][TID T03] = 5워드
소계: 15워드
```

**Verb Edge:**
```
[Verb Edge 4워드]
  Prefix: 동사
  동사: give.v.01
  한정자: 과거|긍정|완료
  참여자플래그: AGT|THM|RCP

[Edge TID: E01] = 1워드
[Agent: T01] = 1워드 (철수)
[Theme: T03] = 1워드 (책)
[Recipient: T02] = 1워드 (영희)
소계: 8워드
```

**총: 23워드 (368비트)**

### 9.2 "비가 온다"

```
Entity: 비 [T01] = 5워드

Verb Edge:
  rain.v.01 | 현재|진행 | THM
  [Edge TID: E01] = 1워드
  [Theme: T01] = 1워드
소계: 6워드

총: 11워드 (176비트)
```

### 9.3 "창을 든 네안데르탈인이 맘모스를 쫓아갔다"

```
Entity: 
  네안데르탈인 [T01] = 5워드
  맘모스 [T02] = 5워드
  창 [T03] = 5워드
소계: 15워드

Verb Edge (E01):
  chase.v.01 | 과거|완료 | AGT+PAT
  [Edge TID: E01] = 1워드
  [Agent: T01] = 1워드
  [Patient: T02] = 1워드
소계: 7워드

Verb Inner Edge:
  hold.v.01 | Parent=E01 | Target=AGT
  [Inner TID: I01] = 1워드
  [Parent: E01] = 1워드
  [Patient: T03] = 1워드
소계: 7워드

총: 29워드 (464비트)
```

---

## 10. 이전 버전 대비

| 항목 | v0.1 | v0.2 |
|------|------|------|
| Edge SIDX | 2워드 | 통합 |
| Verb SIDX | 4워드 | 통합 |
| 한정자 | 별도 2워드 | 통합 22비트 |
| 총 고정부 | 7워드 | **4워드** |
| Prefix | 8비트 | **5비트** |
| 참여자 | 16개 | **15개** |
| Inner Edge | 없음 | **추가** |

---

## 11. 설계 근거

### 11.1 64비트 통합 이유

- 캐시 라인 친화적
- 원자적 읽기/쓰기
- SIMD 처리 용이

### 11.2 참여자 15개 이유

- 64비트 맞춤 (5+22+22+15=64)
- ATR은 Triple로 대체 가능
- 핵심 의미역 모두 포함

### 11.3 Verb Inner Edge 이유

- Entity 속성 vs 서술 내 상태 구분
- 자동 승격 (귀납 추론) 지원
- 복합 서술 표현

---

## 12. 향후 과제

- [ ] Prefix 5비트 코드 확정
- [ ] Verb Inner Edge 관계타입 정의
- [ ] Context Edge 상세 설계
- [ ] WMS 저장 구조 최적화

---

**문서 종료**
