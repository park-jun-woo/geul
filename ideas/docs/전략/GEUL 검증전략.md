# GEUL 검증 전략: 자가 진화형 하이브리드 검증 시스템

**버전:** v0.1  
**작성일:** 2026-01-26  
**목적:** GEUL 출력의 오류를 자동으로 탐지하고, 시스템이 스스로 진화하는 검증 전략

---

## 1. 핵심 철학

> **"구조가 있으면 검증 가능하고, 검증이 가능하면 환각을 방지할 수 있다"**

### 자연어 vs GEUL 검증

| 항목 | 자연어 (GPT/RAG) | GEUL |
|------|------------------|------|
| 자동 검증 | 불가능 (0%) | 가능 (85-90%) |
| 검증 방법 | 인간 육안 필수 | 5단계 자동 파이프라인 |
| 대규모 처리 | 불가능 | 가능 |
| 오류 패턴화 | 불가능 | 규칙으로 축적 가능 |

### 예시

**자연어:**
```
GPT 출력: "Apple acquired Tesla in 2025 for $500B"
→ 문법 완벽, 의미 명확
→ 하지만 사실 오류 (실제로 일어나지 않음)
→ 프로그램 검증 불가
→ 인간이 직접 팩트체크 필요
```

**GEUL:**
```
GEUL 출력: Event6(Q312, acquire.v.01, Q478214, $500B, 2025-03-15)
→ SIDX 검증: Q312(Apple), Q478214(Tesla) 존재 확인 ✓
→ 타입 검증: acquire.v.01(기업, 기업) 타입 일치 ✓
→ 시간 검증: 2025-03-15 포맷 유효 ✓
→ 사실 검증: DB에 해당 이벤트 없음 ✗
→ 자동 거부
```

---

## 2. 3단계 하이브리드 파이프라인

```
입력: GPT/Gemini가 생성한 GEUL
  ↓
┌─────────────────────────────────────────┐
│ Stage 1: 심볼릭 검증 (CPU)             │
│ - 90% 오류 차단                         │
│ - 비용: $0.00002/건                    │
│ - 속도: 1-10ms                          │
└─────────────────────────────────────────┘
  ↓ (10% 통과)
┌─────────────────────────────────────────┐
│ Stage 2: LLM 2차 검증                   │
│ - 5% 추가 오류 차단                     │
│ - 비용: $0.0002/건                     │
│ - 속도: 100-500ms                       │
└─────────────────────────────────────────┘
  ↓ (5% 통과)
┌─────────────────────────────────────────┐
│ Stage 3: 인간 최종 검수                 │
│ - 남은 5%만 처리                        │
│ - 비용: $1/건                           │
│ - 속도: 1분                             │
└─────────────────────────────────────────┘
  ↓
출력: 검증된 GEUL
```

---

## 3. Stage 1: 심볼릭 검증 (5계층)

### 3.1 형식 검증 (Syntactic Validation)
```
목표: 비트 구조 유효성
- 64비트 SIDX 포맷 확인
- 필수 슬롯 존재 (Event6: subject, verb)
- 워드 시퀀스 완결성
- 예약 비트 범위 준수

커버리지: ~30%
비용: $0.000005/건
```

**예시:**
```python
def validate_syntax(geul):
    # 비트 구조 체크
    if not is_valid_64bit(geul.sidx):
        return Error("Invalid SIDX format")
    
    # 필수 슬롯
    if geul.type == "Event6" and not geul.subject:
        return Error("Missing subject")
    
    return OK
```

---

### 3.2 참조 무결성 (Reference Integrity)
```
목표: 모든 식별자가 실제로 존재하는지 확인
- SIDX → DB 조회
- Q-ID 유효성 (Wikidata)
- synset 유효성 (WordNet)
- P-ID 관계 타입 존재

커버리지: +40% (누적 70%)
비용: $0.00001/건
```

**예시:**
```python
def validate_reference(geul):
    # SIDX 존재 확인
    if not db.exists(geul.subject):
        return Error(f"Unknown SIDX: {geul.subject}")
    
    # 관계 타입 확인
    if not ontology.has_relation(geul.verb):
        return Error(f"Unknown verb: {geul.verb}")
    
    return OK
```

---

### 3.3 타입 검증 (Type Safety)
```
목표: 의미적 타입 일치 확인
- 동사 선택 제약 (eat.v.01의 agent는 생물)
- 참여자 타입 (CEO는 인물)
- 속성 범위 (나이는 양수)
- 단위 일치 (거리는 length 단위)

커버리지: +10% (누적 80%)
비용: $0.000005/건
```

**예시:**
```prolog
% eat의 agent는 생물이어야 함
validate_type(Event) :-
    Event.verb = eat.v.01,
    Event.agent = X,
    instance_of(X, living_thing).

% CEO는 사람
validate_type(Event) :-
    Event.role = CEO,
    Event.person = X,
    instance_of(X, human).
```

---

### 3.4 시간 일관성 (Temporal Consistency)
```
목표: 시간 관계의 모순 탐지
- 시간순 위반 (사망 후 활동)
- 날짜 포맷 유효성
- 생애 구간 (birth < death)
- 동시성 제약 (한 곳에만 존재)

커버리지: +5% (누적 85%)
비용: $0.000005/건
```

**예시:**
```prolog
% 사망 후 활동 불가
temporal_error(X, E) :-
    death(X, T1),
    event(X, E, T2),
    T2 > T1.

% 생애 구간
temporal_error(X) :-
    birth(X, T1),
    death(X, T2),
    T2 < T1.
```

---

### 3.5 논리 규칙 (Domain Logic)
```
목표: 도메인별 제약 사항
- 존재론적 제약 (한 시간에 한 장소)
- 인과 제약 (원인 → 결과)
- 물리 제약 (무게 > 0)
- 도메인 규칙 (CEO 중복 불가)

커버리지: +5% (누적 90%)
비용: $0.000005/건
```

**예시:**
```prolog
% 존재론적: 한 시간에 한 장소만
location_error(X, T) :-
    location(X, L1, T),
    location(X, L2, T),
    L1 \= L2.

% CEO 중복 재임 불가
ceo_error(C, T) :-
    ceo(X, C, T1, T2),
    ceo(Y, C, T3, T4),
    X \= Y,
    overlap(T1-T2, T3-T4).

% 물리: 양수 제약
physical_error(X) :-
    weight(X, W),
    W =< 0.
```

---

## 4. Stage 2: LLM 2차 검증

**목표:** 심볼릭으로 잡지 못한 미묘한 오류 탐지

### 4.1 프롬프트 설계
```
You are a fact checker for structured knowledge.

Input GEUL:
Event6(Q312, acquire.v.01, Q478214, $500B, 2025-03-15)

Task:
1. Check if this event is plausible
2. Identify any factual errors
3. Check for logical inconsistencies

Output format (JSON):
{
  "valid": true/false,
  "confidence": 0.0-1.0,
  "errors": ["error1", "error2"],
  "suggestion": "correction if needed"
}
```

### 4.2 처리 전략
```python
def llm_validate(geul_list):
    # 배치 처리 (비용 절감)
    batch_size = 20
    
    for batch in chunk(geul_list, batch_size):
        results = llm.validate(batch)
        
        for geul, result in zip(batch, results):
            if not result.valid:
                # 오류 패턴 저장
                log_error(geul, result.errors)
                
                # 규칙 생성 요청
                new_rule = llm.generate_rule(result.errors)
                add_symbolic_rule(new_rule)
```

### 4.3 비용 최적화
- 심볼릭 통과분만 처리 (10%)
- 배치 처리로 API 호출 최소화
- 캐시 활용 (동일 패턴)

---

## 5. Stage 3: 인간 최종 검수

**범위:** LLM도 통과한 5%만

### 5.1 UI 설계
```
┌──────────────────────────────────────┐
│ GEUL Review Queue                    │
├──────────────────────────────────────┤
│ Event6(Q312, acquire.v.01, ...)     │
│ Status: Pending Review               │
│                                      │
│ Context:                             │
│ - Source: Reuters, 2025-03-15       │
│ - Confidence: 0.85                  │
│                                      │
│ Actions:                             │
│ [✓ Approve] [✗ Reject] [Edit]      │
└──────────────────────────────────────┘
```

### 5.2 피드백 루프
```python
def human_review(geul):
    decision = ui.show_review(geul)
    
    if decision == "reject":
        # 오류 패턴 분석
        error_pattern = analyze_error(geul, decision.reason)
        
        # Claude에게 규칙 생성 요청
        prompt = f"Generate validation rule for: {error_pattern}"
        new_rule = claude.generate_rule(prompt)
        
        # 자동 추가
        add_symbolic_rule(new_rule)
        
        # 검증률 향상
        log_improvement(error_pattern, new_rule)
```

---

## 6. 자가 진화 메커니즘

### 6.1 순환 개선 프로세스
```
Week 0: 검증률 90%
  ↓
발견: "동시 CEO 불가" 패턴 5건
  ↓
Claude: 규칙 생성
  ↓
Week 1: 검증률 92%
  ↓
발견: "물리 법칙 위반" 패턴 3건
  ↓
Claude: 규칙 생성
  ↓
Week 10: 검증률 95%
  ↓
...
  ↓
Week 100: 검증률 98%
```

### 6.2 규칙 DB 관리
```sql
CREATE TABLE validation_rules (
    rule_id SERIAL PRIMARY KEY,
    rule_code TEXT,
    error_pattern TEXT,
    created_at TIMESTAMP,
    author TEXT, -- 'claude', 'human', 'auto'
    activation_count INT DEFAULT 0,
    false_positive_rate FLOAT
);

-- 규칙 성능 추적
CREATE TABLE rule_performance (
    rule_id INT,
    date DATE,
    true_positive INT,
    false_positive INT,
    false_negative INT
);
```

### 6.3 규칙 진화
```python
def evolve_rules():
    # 성능 낮은 규칙 식별
    weak_rules = db.query("""
        SELECT rule_id, false_positive_rate
        FROM validation_rules
        WHERE false_positive_rate > 0.1
    """)
    
    for rule in weak_rules:
        # Claude에게 개선 요청
        improved_rule = claude.improve_rule(
            original=rule.code,
            performance=rule.stats
        )
        
        # A/B 테스트
        test_rule(improved_rule, sample_size=1000)
```

---

## 7. 비용 분석

### 7.1 100만 건 검증 시나리오

**전통적 방법 (100% 신경망):**
```
100만 건 × $0.001/건 = $1,000
시간: 100만 × 200ms = 55시간
```

**GEUL 하이브리드:**
```
Stage 1 (심볼릭):
- 100만 건 × $0.00002 = $20
- 시간: 100만 × 5ms = 1.4시간
- 90만 건 차단

Stage 2 (LLM):
- 10만 건 × $0.0002 = $20
- 시간: 10만 × 200ms = 5.5시간
- 5만 건 추가 차단

Stage 3 (인간):
- 5만 건 × $1 = $50,000
- 시간: 5만 × 1분 = 833시간

총 비용: $50,040
총 시간: 840시간
```

**하지만 인간 검수는 선택적:**
- 고위험(금융/의료): 필수
- 저위험(뉴스 요약): Stage 2까지만

**저위험 시나리오:**
```
총 비용: $40 (vs $1,000)
절감: 96%
시간: 7시간 (vs 55시간)
```

---

## 8. 구현 스택

### 8.1 심볼릭 검증
```
언어: Go (성능) / Python (프로토타입)
규칙 엔진: Datalog / Prolog
DB: PostgreSQL (ltree)
캐시: Redis
```

### 8.2 LLM 검증
```
모델: Gemini 2.5 Flash (저렴)
대안: Claude Haiku (정확)
배치 크기: 20
타임아웃: 30초
```

### 8.3 UI
```
프론트엔드: React
백엔드: FastAPI
DB: PostgreSQL
큐: Redis + Celery
```

---

## 9. 실전 적용 예시

### 9.1 금융 뉴스 처리
```
입력: 10만 뉴스/일
목표: Event6 추출

검증 결과:
- Stage 1: 9만 건 통과 (90%)
- Stage 2: 8.5만 건 통과 (95%)
- Stage 3: 인간 검수 5천 건

비용/일: $4 (심볼릭) + $20 (LLM) = $24
vs 전통: $200
절감: 88%
```

### 9.2 의료 기록 구조화
```
입력: 1만 진료 기록/일
위험: 높음 (인간 검수 필수)

검증 결과:
- Stage 1: 9천 건 통과
- Stage 2: 8.5천 건 통과
- Stage 3: 1.5천 건 검수

비용/일: $2 + $2 + $1,500 = $1,504
vs 전통: $10,000 (100% 인간)
절감: 85%
```

---

## 10. 핵심 메시지

### 10.1 자연어 vs GEUL
```
자연어 (GPT):
→ 검증 불가능
→ 환각 불가피
→ 대규모 불가능

GEUL:
→ 90% 자동 검증
→ 환각 조기 차단
→ 무한 확장 가능
```

### 10.2 자가 진화
```
Week 0: 90% → Week 100: 98%
→ 시스템이 점점 똑똑해짐
→ 도메인 특화 최적화
→ 운영하면서 개선
```

### 10.3 비용 효율
```
심볼릭(저렴) → LLM(중간) → 인간(비쌈)
→ 적재적소 배치
→ 비용 10-100배 절감
```

---

## 11. 논문 기여점

1. **Verifiable Semantic Outputs**
   - 구조 → 검증 가능 → 환각 방지

2. **Hybrid Validation Pipeline**
   - 심볼릭(90%) + LLM(5%) + 인간(5%)
   - 비용 효율 극대화

3. **Self-Evolving System**
   - 오류 발견 → 규칙 생성 → 성능 향상
   - AI가 AI를 검증하고 개선

4. **Production-Ready**
   - 실전 적용 가능
   - ROI 명확

---

## 12. 향후 개선 방향

### 12.1 단기 (6개월)
- [ ] 규칙 자동 생성 파이프라인
- [ ] A/B 테스트 프레임워크
- [ ] 성능 모니터링 대시보드

### 12.2 중기 (1년)
- [ ] 도메인별 규칙 라이브러리
- [ ] 규칙 마켓플레이스
- [ ] 크라우드소싱 검수

### 12.3 장기 (2년+)
- [ ] 강화학습 기반 규칙 최적화
- [ ] 다국어 지원
- [ ] 연합 학습 (federated learning)

---

## 결론

GEUL의 구조적 특성은 검증을 가능하게 하고,  
검증은 환각을 방지하며,  
시스템은 스스로 진화한다.

**"Structure → Verification → Trust"**

이것이 GEUL이 차세대 지식 표현 표준이 되어야 하는 이유다.
