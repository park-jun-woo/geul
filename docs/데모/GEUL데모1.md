# GEUL 데모 1: 지식 그래프 초고속 탐색

**Knowledge Graph with N-hop Query Engine**

---

## 0. 한 줄 요약

Wikidata와 CC News를 GEUL로 변환하여 "트럼프 대통령의 지인들이 졸업한 대학교별 통계" 같은 복잡한 N-hop 쿼리를 0.1초 만에 답하는 시스템

---

## 1. 핵심 가치 제안

### 문제: 기존 LLM의 한계

```
사용자: "트럼프 지인들의 대학 통계를 보여줘"

GPT-4:
→ 트럼프 지인 243명을 하나씩 추론
→ 각 사람의 학력을 추론
→ 통계 계산
→ 시간: 30초
→ 비용: $1.50
→ 정확도: 60% (환각 포함)
→ 출처: 불명확
```

### 해결: GEUL + WMS

```
사용자: "트럼프 지인들의 대학 통계를 보여줘"

GEUL/WMS:
→ WMS 쿼리 (3-hop graph traversal)
→ 시간: 0.08초
→ 비용: $0.001
→ 정확도: 95% (구조화된 데이터)
→ 출처: 각 사실마다 명시 (Wikidata QID, 기사 링크)
```

**차이:**
- 속도: 375배 빠름
- 비용: 1,500배 저렴
- 정확도: 35%p 향상
- 투명성: 완전 추적 가능

---

## 2. 데모 시나리오

### 시나리오 1: 정치 네트워크 분석

```
Query: "트럼프 내각의 아이비리그 네트워크"

결과:
Stanford University: 37명
├─ Elon Musk (알려진 지인)
├─ [35명 더]
└─ 출처: Wikidata Q123, CC News 2024-01-15

Harvard University: 31명
├─ [31명]
└─ 출처: Wikidata Q456, CC News 2024-11-20

Yale University: 23명
...

시각화:
[인터랙티브 그래프]
- 노드: 사람, 대학
- 엣지: knows, educated_at
- 필터: 시간 슬라이더 (2020-2025)
```

### 시나리오 2: 기업 투자 네트워크

```
Query: "OpenAI 투자자들이 투자한 다른 AI 스타트업"

결과:
Microsoft → [OpenAI, Anthropic, Inflection]
a16z → [OpenAI, Character.AI, Hugging Face]
Sequoia → [OpenAI, Runway, Perplexity]

교집합 분석:
- OpenAI + Anthropic 동시 투자자: 12개
- 투자 라운드 시기 분석
- 투자 금액 트렌드
```

### 시나리오 3: 학술 영향력 추적

```
Query: "Geoffrey Hinton의 제자들이 창업한 회사"

결과:
Ilya Sutskever → OpenAI
Oriol Vinyals → Google DeepMind
Alex Graves → Google DeepMind
...

2세대 영향력:
Ilya → Greg Brockman → OpenAI
Ilya → Wojciech Zaremba → OpenAI
```

---

## 3. 기술 아키텍처

### 3.1 전체 구조

```
┌─────────────────────────────────────────────┐
│ Data Sources                                │
├─────────────────────────────────────────────┤
│ 1. Wikidata (구조화된 지식)                  │
│    - 1억+ entities                          │
│    - 10억+ relations                        │
│    → GEUL: Entity Node + Triple Edge        │
│                                             │
│ 2. CC News (비구조화된 사건)                 │
│    - 수억 건 뉴스 기사                       │
│    - 2005-2024                              │
│    → GEUL: Event6 Edge                      │
└─────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────┐
│ GEUL Conversion Layer                       │
├─────────────────────────────────────────────┤
│ - Wikidata API → Entity/Triple              │
│ - LLM Extraction → Event6                   │
│ - Quality Filtering                         │
│ - Deduplication                             │
└─────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────┐
│ WMS (World Management System)               │
├─────────────────────────────────────────────┤
│ Storage: 3GB (10M entities, 100M triples)   │
│ Index: Hash + B-tree + Temporal             │
│ Query: N-hop BFS/DFS, SIMD-optimized        │
│ Cache: LRU, hot-path optimization           │
└─────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────┐
│ Query API & Web UI                          │
├─────────────────────────────────────────────┤
│ - Natural language → Structured query       │
│ - Real-time graph traversal                 │
│ - Interactive visualization (D3.js)         │
│ - Source attribution                        │
└─────────────────────────────────────────────┘
```

### 3.2 GEUL 변환 예시

**Wikidata → GEUL:**

```
Q6 (Donald Trump):
  
Entity Node:
  SIDX: 0x0000_0000_0000_0006
  Label: "Donald Trump"
  Type: Q5 (Human)
  
Triple Edge (educated_at):
  Subject: Q6
  Predicate: P69
  Object: Q1329269 (Wharton)
  Start: 1968
  Source: Wikidata
  Confidence: 1.0
  
Triple Edge (spouse):
  Subject: Q6
  Predicate: P26
  Object: Q432473 (Melania)
  Start: 2005-01-22
  Source: Wikidata
  Confidence: 1.0
```

**CC News → GEUL:**

```
기사: "Trump appointed Elon Musk to lead DOGE on 2024-12-01"

Event6 Edge:
  Who: Q6 (Trump)
  What: appoint.v.01
  Whom: Q317521 (Musk)
  When: 2024-12-01
  Where: Q61 (Washington DC)
  Why: Context_Appointment_DOGE
  Source: Reuters_2024_12_01
  Confidence: 0.95
```

### 3.3 WMS 쿼리 엔진

```go
// N-hop 쿼리 예시

query := WMSQuery{
    Start: Q6, // Trump
    Pattern: []Hop{
        {Relation: "knows", Direction: OUT},
        {Relation: "educated_at", Direction: OUT},
    },
    Aggregation: GroupByCount{Field: "university"},
}

results := wms.Execute(query)
// Results: [(Stanford, 37), (Harvard, 31), ...]
```

---

## 4. 구현 계획

### Week 1-2: Wikidata → GEUL

**목표:** 1,000만 Entity + 1억 Triple

**작업:**
1. Wikidata API 연동
2. QID → SIDX 매핑 테이블 생성
3. Priority entities 추출:
   - Q5 (Human): 정치인, 기업인
   - Q3918 (University)
   - Q4830453 (Business)
4. Priority relations:
   - P69 (educated_at)
   - P108 (employer)
   - P102 (political party)
   - P39 (position held)
5. 병렬 변환 (32 workers)
6. WMS 저장 및 인덱싱

**검증:**
```bash
$ geul-stats data/world.gwms
Entities: 10,247,893
Triples: 103,492,847
Storage: 2.3 GB
Index: 450 MB
```

### Week 3-5: CC News → Event6

**Week 3: 필터링 (10M → 1M)**
- 정치/경제/기술 카테고리 선별
- Named Entity Recognition
- 시간 정보 명확한 기사만

**Week 4: 추출 (1M → 100K)**
- LLM으로 Event6 추출
- 규칙 기반 검증:
  - Entity가 Wikidata에 존재
  - 시간 정보 명확 (day precision)
  - 대명사 없음
- Confidence 0.8 이상만

**Week 5: 검수 (1만 골든셋)**
- 인간 검수자 3명
- 각 1만 건 검토
- 합의 기반 골든셋 생성
- 자동 검증 규칙 학습

### Week 6-7: WMS 최적화

**최적화 항목:**
1. SIMD 비트마스크 쿼리
2. 병렬 N-hop 탐색
3. LRU 캐시 (hot queries)
4. 메모리 맵 파일
5. 인덱스 압축

**벤치마크 목표:**
- 1-hop: <1ms
- 3-hop: <10ms
- 5-hop: <100ms

### Week 8: UI 개발

**기술 스택:**
- React + TypeScript
- D3.js (graph visualization)
- TailwindCSS

**주요 화면:**
1. 검색 인터페이스
2. 쿼리 분해 시각화
3. 결과 테이블
4. 인터랙티브 그래프
5. 시간 필터 슬라이더

### Week 9: 통합 테스트

**테스트 시나리오:**
1. "트럼프 지인 대학" ✓
2. "OpenAI 투자자 포트폴리오" ✓
3. "Hinton 제자 창업" ✓
4. 5-hop 쿼리 성능 ✓
5. 동시 사용자 100명 ✓

### Week 10: 공개 준비

1. 문서 작성
2. 데모 비디오 (3분)
3. HN/Reddit 포스트 작성
4. GitHub 저장소 정리
5. 런칭

---

## 5. 예상 결과

### 정량 지표

**데이터:**
- Entities: 10M+
- Triples: 100M+
- Events: 1M+
- Storage: 3 GB

**성능:**
- 1-hop: <1ms ✓
- 3-hop: <10ms ✓
- 5-hop: <100ms ✓

**정확도:**
- Triple: 95%+ (Wikidata)
- Event6: 85%+ (LLM+filter+review)

### 정성 반응 (예상)

**학계:**
"실제 작동하는 지식 그래프. 게다가 시간 추적까지."

**언론:**
"트럼프 내각 아이비리그 분석" → 바이럴 가능

**빅테크:**
"우리 Knowledge Graph 통합 가능성?"

**투자자:**
"명확한 ROI, 확장 가능"

---

## 6. 리스크 및 대응

| 리스크 | 영향 | 대응 |
|--------|------|------|
| Wikidata 일관성 | 중 | Top 100 relation만 우선 |
| Event6 품질 | 고 | 3단계 필터 + 골든셋 |
| 성능 목표 미달성 | 중 | SIMD 최적화, 캐싱 |
| 법적 이슈 | 저 | CC0/Fair use 확인 |

---

## 7. 성공 기준

- [ ] 10M Entity 변환 완료
- [ ] 1M Event6 추출 완료
- [ ] "트럼프 대학" 쿼리 <100ms
- [ ] UI 작동
- [ ] GitHub 100+ stars (첫 주)
- [ ] HN 첫 페이지
- [ ] 언론 보도 10+

---

**예산:** $5,000 (LLM API, 서버)  
**팀:** 2-3명  
**기간:** 10주  
**시작:** 2026-02-01  
**완료:** 2026-04-15
