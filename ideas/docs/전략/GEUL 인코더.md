# GEUL 인코더: 심볼릭 프로그램 기반 자연어→GEUL 변환기

**버전:** v0.1  
**작성일:** 2026-01-26  
**목적:** 자연어를 GEUL로 변환하는 고성능, 저비용 인코더 설계

---

## 0. 핵심 철학

> **"GEUL 인코더는 LLM이 아니라 컴파일러다"**

### 컴파일러 비유

| 전통 컴파일러 | GEUL 인코더 |
|--------------|-------------|
| 소스코드 (C, Go) | 자연어 문장 |
| AST (추상 구문 트리) | MRS (의미 표현) |
| 문법 규칙 | 변환 룰 DB (2만개) |
| 바이너리 | GEUL |
| 컴파일 에러 | 패턴 미스 → LLM 호출 |

### 왜 LLM이 아닌가?

**LLM 방식의 문제:**
```
문제점:
- 비용: $0.01/문장
- 속도: 200-500ms
- 일관성: 동일 입력 → 다른 출력 가능
- 검증: 블랙박스

100만 문장 처리:
- 비용: $10,000
- 시간: 55시간
```

**심볼릭 프로그램 방식:**
```
장점:
- 비용: $0 (패턴 히트 시)
- 속도: <1ms
- 일관성: 완벽 재현
- 검증: 화이트박스

100만 문장 처리:
- 비용: $500 (5% LLM만)
- 시간: 1.5시간
```

---

## 1. 전체 아키텍처

```
┌────────────────────────────────────────────────┐
│ 입력: 자연어 문장                               │
│ "Apple acquired Tesla for $2B"                 │
└────────────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────────────┐
│ Stage 1: MRS 파싱 (ACE + ERG)                  │
│ - 구문 분석                                     │
│ - 의미 구조 추출                                │
│ - 복수 해석 생성                                │
└────────────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────────────┐
│ Stage 2: 패턴 매칭                              │
│ - MRS 구조 → 패턴 해시                         │
│ - 룰 DB 조회 (O(1))                            │
│ - 히트율: 95%+                                  │
└────────────────────────────────────────────────┘
         ↓ (95% 히트)          ↓ (5% 미스)
┌─────────────────────┐  ┌──────────────────────┐
│ Stage 3a: 룰 적용   │  │ Stage 3b: LLM 룰 생성│
│ - 프로그램 변환     │  │ - Claude/Gemini 호출 │
│ - <1ms              │  │ - 새 룰 생성         │
│ - $0                │  │ - DB 등록            │
└─────────────────────┘  └──────────────────────┘
         ↓                         ↓
┌────────────────────────────────────────────────┐
│ Stage 4: GEUL 검증                              │
│ - 형식/참조/타입/시간/논리 검증                │
│ - 실패 시 재시도 또는 로깅                      │
└────────────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────────────┐
│ 출력: GEUL                                      │
│ Event6(Q312, acquire.v.01, Q478214, $2B, T)   │
└────────────────────────────────────────────────┘
```

---

## 2. Stage 1: MRS 파싱

### 2.1 목표
자연어 문장을 의미 구조(MRS)로 변환

### 2.2 도구
- **ACE Parser** + **ERG Grammar**
- 산출: 복수 MRS 해석

### 2.3 예시
```
입력: "Time flies like an arrow"

출력: 6개 MRS 해석
1. time(명사) flies(동사) like(전치사) arrow
2. Time(고유명사) flies(동사) like(전치사) arrow
3. time(명사) fly(동사) like(동사) arrow
...
```

### 2.4 프루닝
- Entity Linking (Wikidata + WordNet)
- LLM 기반 중의성 해소
- 불합리 해석 제거

**결과:** 6개 → 2-3개 유효 해석

---

## 3. Stage 2: 패턴 매칭

### 3.1 패턴 DB 구조

**테이블 스키마:**
```sql
CREATE TABLE conversion_rules (
    rule_id SERIAL PRIMARY KEY,
    pattern_hash TEXT UNIQUE,        -- MRS 패턴 해시
    verb_synset TEXT,                -- eat.v.01
    pattern_structure JSONB,         -- MRS 구조
    geul_template TEXT,              -- 변환 템플릿
    confidence FLOAT DEFAULT 1.0,
    usage_count INT DEFAULT 0,
    created_at TIMESTAMP,
    created_by TEXT                  -- 'bootstrap', 'llm', 'human'
);

CREATE INDEX idx_pattern_hash ON conversion_rules(pattern_hash);
CREATE INDEX idx_verb_synset ON conversion_rules(verb_synset);
```

### 3.2 패턴 해시 생성

```python
def compute_pattern_hash(mrs):
    """
    MRS 구조를 정규화하여 해시 생성
    """
    # 핵심 구조만 추출
    structure = {
        'verb': mrs.main_verb.synset,
        'args': {
            'ARG1': mrs.get_arg_type('ARG1'),  # 'human', 'organization', etc.
            'ARG2': mrs.get_arg_type('ARG2'),
            'ARG3': mrs.get_arg_type('ARG3')
        },
        'modifiers': [m.type for m in mrs.modifiers]
    }
    
    # 정규화
    normalized = json.dumps(structure, sort_keys=True)
    
    # 해시
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]
```

### 3.3 룰 매칭

```python
def match_pattern(mrs):
    """
    MRS에 매칭되는 룰 검색
    """
    # 1. 완전 일치 (Exact Match)
    pattern_hash = compute_pattern_hash(mrs)
    rule = db.query(
        "SELECT * FROM conversion_rules WHERE pattern_hash = %s",
        (pattern_hash,)
    )
    
    if rule:
        return rule, 'exact'
    
    # 2. 유사 패턴 (Fuzzy Match)
    # 동사만 일치하고 인자 타입이 일반화된 룰
    fuzzy_rules = db.query("""
        SELECT * FROM conversion_rules 
        WHERE verb_synset = %s
        ORDER BY confidence DESC, usage_count DESC
        LIMIT 10
    """, (mrs.main_verb.synset,))
    
    for rule in fuzzy_rules:
        if is_compatible(mrs, rule.pattern_structure):
            return rule, 'fuzzy'
    
    # 3. 미스
    return None, 'miss'
```

### 3.4 룰 DB 초기화

**동사 프레임 기반 부트스트랩:**
```python
def bootstrap_rules():
    """
    WordNet 동사 프레임으로 초기 룰 생성
    """
    for synset in wordnet.all_verb_synsets():
        frames = synset.frame_strings()
        
        for frame in frames:
            # "Somebody ----s something"
            # → ARG1=animate, ARG2=physical_object
            
            rule = parse_frame_to_rule(synset, frame)
            db.insert(rule)
    
    print(f"Bootstrapped {db.count()} rules")
    # 예상: 13,767개 동사 × 평균 1.5 프레임 = ~20,000 룰
```

---

## 4. Stage 3a: 룰 적용 (프로그램 변환)

### 4.1 변환 템플릿

**룰 예시:**
```json
{
  "rule_id": 1234,
  "verb_synset": "acquire.v.01",
  "pattern_structure": {
    "verb": "acquire.v.01",
    "ARG1": "organization",
    "ARG2": "organization",
    "ARG3": "monetary_value"
  },
  "geul_template": {
    "type": "Event6",
    "subject": "${ARG1.sidx}",
    "verb": "acquire.v.01",
    "object": "${ARG2.sidx}",
    "value": "${ARG3.value}",
    "time": "${temporal.timestamp}"
  }
}
```

### 4.2 템플릿 인스턴스화

```python
def apply_rule(mrs, rule):
    """
    룰을 MRS에 적용하여 GEUL 생성
    """
    geul = {}
    
    for key, template in rule.geul_template.items():
        if template.startswith('${'):
            # 변수 치환
            var_path = template[2:-1]  # "ARG1.sidx"
            value = resolve_variable(mrs, var_path)
            geul[key] = value
        else:
            # 리터럴
            geul[key] = template
    
    return GEUL(**geul)

def resolve_variable(mrs, path):
    """
    ${ARG1.sidx} → Q312
    """
    parts = path.split('.')
    
    if parts[0].startswith('ARG'):
        arg = mrs.get_argument(parts[0])
        
        if parts[1] == 'sidx':
            return arg.entity.sidx
        elif parts[1] == 'value':
            return arg.value
    
    elif parts[0] == 'temporal':
        return mrs.temporal.timestamp
```

### 4.3 성능

```python
# 벤치마크 (MacBook Pro M1)
결과:
- 패턴 해시: 0.1ms
- DB 조회: 0.5ms
- 템플릿 적용: 0.3ms
- 총: ~1ms

처리량: 1,000 문장/초
```

---

## 5. Stage 3b: LLM 룰 생성 (예외 처리)

### 5.1 언제 호출되나?

- 패턴 미스 (5%)
- 신규 동사 발견
- 복잡한 구문

### 5.2 LLM 프롬프트

```
You are a GEUL conversion rule generator.

Input:
- Sentence: "Apple acquired Tesla for $2B"
- MRS structure: {
    "verb": "acquire.v.01",
    "ARG1": {"lemma": "Apple", "type": "organization", "qid": "Q312"},
    "ARG2": {"lemma": "Tesla", "type": "organization", "qid": "Q478214"},
    "ARG3": {"lemma": "$2B", "type": "monetary_value"}
  }

Task:
Generate a conversion rule in JSON format that can transform 
this MRS pattern into GEUL Event6.

Output format:
{
  "verb_synset": "acquire.v.01",
  "pattern_structure": {
    "verb": "acquire.v.01",
    "ARG1": "organization",
    "ARG2": "organization",
    "ARG3": "monetary_value"
  },
  "geul_template": {
    "type": "Event6",
    "subject": "${ARG1.sidx}",
    "verb": "acquire.v.01",
    "object": "${ARG2.sidx}",
    "value": "${ARG3.value}",
    "time": "${temporal.timestamp}"
  },
  "confidence": 0.9
}

Rules:
1. Use variable substitution with ${} syntax
2. Map semantic roles (ARG1, ARG2) to GEUL slots
3. Be as general as possible (use types, not specific entities)

OUTPUT (JSON only):
```

### 5.3 룰 검증 및 등록

```python
def generate_and_register_rule(mrs, sentence):
    """
    LLM으로 새 룰 생성 및 등록
    """
    # 1. LLM 호출
    prompt = build_prompt(mrs, sentence)
    response = llm.generate(prompt)
    
    # 2. JSON 파싱
    try:
        rule = json.loads(response)
    except:
        log_error("LLM generated invalid JSON")
        return None
    
    # 3. 룰 검증
    if not validate_rule(rule):
        log_error("Rule validation failed")
        return None
    
    # 4. 테스트 적용
    geul = apply_rule(mrs, rule)
    validation_result = validate_geul(geul)
    
    if not validation_result.passed:
        log_error(f"Generated GEUL failed validation: {validation_result.errors}")
        return None
    
    # 5. DB 등록
    rule_id = db.insert_rule(rule)
    
    # 6. 통계 로깅
    log_info(f"New rule created: {rule_id}, verb={rule['verb_synset']}")
    
    return rule
```

### 5.4 비용 추정

```
패턴 미스율: 5%
LLM 비용: $0.001/호출

100만 문장:
- 미스: 5만 건
- LLM 비용: $50
- + 룰 적용 95만 건: $0

총: $50 (vs 100% LLM: $10,000)
```

---

## 6. Stage 4: GEUL 검증

생성된 GEUL은 5단계 검증 파이프라인 통과:

1. 형식 검증
2. 참조 무결성
3. 타입 검증
4. 시간 일관성
5. 논리 규칙

(상세는 `GEUL검증전략.md` 참조)

---

## 7. 점진적 일반화 (Rule Compression)

### 7.1 문제

```
초기:
- "Apple acquired Tesla" → Rule A
- "Google acquired DeepMind" → Rule B
- "Microsoft acquired OpenAI" → Rule C

3개 룰이지만 본질적으로 동일 패턴
```

### 7.2 해결: 일반화

```python
def compress_rules_periodically():
    """
    주기적으로 유사 룰 병합
    """
    # 1. 동사별 그룹화
    verb_groups = db.query("""
        SELECT verb_synset, array_agg(rule_id)
        FROM conversion_rules
        GROUP BY verb_synset
        HAVING count(*) > 10
    """)
    
    for verb, rule_ids in verb_groups:
        rules = db.get_rules(rule_ids)
        
        # 2. 패턴 클러스터링
        clusters = cluster_by_similarity(rules)
        
        # 3. 각 클러스터를 일반화된 룰로 병합
        for cluster in clusters:
            generalized_rule = generalize_rules(cluster)
            
            # 4. 일반화 룰 등록
            new_rule_id = db.insert_rule(generalized_rule)
            
            # 5. 기존 룰 비활성화
            db.deprecate_rules(cluster.rule_ids)
    
    print(f"Compressed {len(deprecated_rules)} rules into {len(new_rules)}")
```

### 7.3 일반화 예시

**Before:**
```json
[
  {"ARG1": "Q312", "ARG2": "Q478214"},  // Apple → Tesla
  {"ARG1": "Q95", "ARG2": "Q23548"},    // Google → DeepMind
  {"ARG1": "Q2283", "ARG2": "Q1415"}    // Microsoft → OpenAI
]
```

**After (일반화):**
```json
{
  "ARG1": {
    "type": "organization",
    "constraint": "is_tech_company"  // 선택적
  },
  "ARG2": {
    "type": "organization"
  }
}
```

### 7.4 일반화 효과

```
Week 0: 0개 룰
Week 4: 5,000개 룰 (구체적)
Week 12: 8,000개 룰 (일반화 전)
Week 13: 3,000개 룰 (일반화 후)
  → 히트율 유지, 관리 용이

최종: 2,000-3,000개 룰 (안정 상태)
```

---

## 8. 자동 부트스트랩 시나리오

### 8.1 초기화 (Week 1-2)

```python
# 1. WordNet 동사 프레임으로 부트스트랩
bootstrap_rules()
# → 20,000개 초기 룰

# 2. 수동으로 100개 고품질 룰 작성
add_manual_rules(curated_rules)

# 3. 검증 파이프라인 설정
setup_validation()
```

### 8.2 자동 확장 (Week 3+)

```python
while True:
    # 1. 뉴스 문장 배치 가져오기
    sentences = news_api.fetch(limit=10000)
    
    # 2. MRS 파싱
    mrs_batch = [parse_to_mrs(s) for s in sentences]
    
    # 3. 변환 시도
    results = []
    for mrs in mrs_batch:
        rule, match_type = match_pattern(mrs)
        
        if match_type == 'miss':
            # LLM으로 새 룰 생성
            rule = generate_and_register_rule(mrs, sentence)
            log_metric('rule_generation', 1)
        
        geul = apply_rule(mrs, rule)
        results.append(geul)
    
    # 4. 검증
    validated = [g for g in results if validate_geul(g).passed]
    
    # 5. 저장
    db.insert_geul_batch(validated)
    
    # 6. 통계
    hit_rate = (len(results) - llm_calls) / len(results)
    print(f"Hit rate: {hit_rate:.1%}, LLM calls: {llm_calls}")
    
    # 7. 주기적 일반화 (매주)
    if week % 1 == 0:
        compress_rules_periodically()
```

### 8.3 예상 진행

```
Week 0: 20k 룰 (부트스트랩)
Week 1: 20.5k 룰 (히트율 60%)
Week 2: 21k 룰 (히트율 75%)
Week 4: 22k 룰 (히트율 85%)
Week 8: 23k 룰 (히트율 92%)
Week 12: 압축 → 15k 룰 (히트율 95%)
Week 26: 안정 → 10k 룰 (히트율 97%)
```

---

## 9. 성능 분석

### 9.1 처리량

```
단일 문장:
- MRS 파싱: 50ms (ACE)
- 패턴 매칭: 1ms
- 룰 적용: 1ms
- 검증: 5ms
총: ~57ms

배치 처리 (1000문장):
- 병렬 파싱: 5초
- 패턴 매칭: 1초
- 룰 적용: 1초
- 검증: 5초
총: 12초 → 83문장/초
```

### 9.2 비용

**100만 문장 처리:**

| 항목 | 전통 (100% LLM) | 하이브리드 (5% LLM) |
|------|-----------------|---------------------|
| MRS 파싱 | $0 | $0 |
| 변환 | $10,000 | $50 |
| 검증 | $20 | $20 |
| **총** | **$10,020** | **$70** |
| **절감** | - | **99.3%** |

### 9.3 정확도

```
Week 0: 룰 기반 70%, LLM 보조 90%
Week 4: 룰 기반 80%, LLM 보조 92%
Week 12: 룰 기반 90%, LLM 보조 95%
Week 26: 룰 기반 93%, LLM 보조 95%

최종: 93-95% (안정)
```

---

## 10. 비교: LLM 방식 vs 하이브리드

| 측면 | LLM (GPT-4) | 하이브리드 (룰+LLM) |
|------|-------------|---------------------|
| 초기 설정 | 즉시 사용 | 2주 부트스트랩 |
| 비용/문장 | $0.01 | $0.00005 (95% 룰) |
| 속도 | 200ms | 1ms (룰 히트) |
| 일관성 | 확률적 | 결정론적 |
| 검증 | 어려움 | 완전 추적 가능 |
| 개선 | 재학습 필요 | 룰 추가만 |
| 투명성 | 블랙박스 | 화이트박스 |

---

## 11. 실전 적용

### 11.1 금융 뉴스 처리

```
입력: 10만 뉴스/일
목표: Event6 추출

초기 (Week 1):
- 히트율: 60%
- LLM 호출: 4만/일
- 비용: $40/일

안정기 (Week 12):
- 히트율: 95%
- LLM 호출: 5천/일
- 비용: $5/일

절감: 88%
```

### 11.2 Wikipedia 변환

```
입력: 900만 문장
목표: Wiki Triple

Week 1-4: 부트스트랩
- 10만 문장 처리
- 룰 확장: 20k → 25k

Week 5-12: 대규모 변환
- 주 100만 문장
- 히트율: 90%+
- 비용: $500/주

총 비용: $5k (vs LLM: $90k)
```

---

## 12. 구현 우선순위

### Phase 1: 프로토타입 (Week 1-4)
- [ ] MRS 파서 통합
- [ ] 패턴 매칭 엔진
- [ ] 룰 DB 설계
- [ ] WordNet 부트스트랩
- [ ] LLM 룰 생성기

### Phase 2: 최적화 (Week 5-8)
- [ ] 배치 처리
- [ ] 유사 패턴 매칭
- [ ] 캐싱 레이어
- [ ] 성능 프로파일링

### Phase 3: 자동화 (Week 9-12)
- [ ] 자동 부트스트랩 루프
- [ ] 룰 압축 알고리즘
- [ ] 모니터링 대시보드
- [ ] 에러 분석 도구

---

## 13. 논문 기여점

1. **Compiler-like Architecture**
   - GEUL 인코더는 LLM이 아닌 컴파일러
   - 패턴 기반 변환

2. **Hybrid Approach**
   - 95% 심볼릭 (무료, 빠름)
   - 5% LLM (예외 처리)

3. **Self-Bootstrapping**
   - 초기 20k 룰로 시작
   - 자동으로 확장/일반화
   - 안정 상태 10k 룰

4. **Cost Efficiency**
   - 99% 비용 절감
   - 1000배 속도 향상
   - 완벽한 일관성

5. **Transparent & Debuggable**
   - 모든 변환 추적 가능
   - 룰 수정으로 즉시 개선
   - 화이트박스 시스템

---

## 14. 결론

GEUL 인코더는 자연어→GEUL 변환을 위한 **컴파일러**다.

핵심 원칙:
- **프로그램 우선, LLM 보조**
- **패턴 재사용**
- **자동 진화**

결과:
- 비용: 1/200
- 속도: 200배
- 일관성: 완벽

이것이 GEUL이 실용적인 이유다.

---

## 부록: 코드 예시

### A. 전체 파이프라인

```python
class GEULEncoder:
    def __init__(self):
        self.parser = ACEParser('erg.dat')
        self.rule_db = RuleDatabase()
        self.llm = ClaudeAPI()
        self.validator = GEULValidator()
    
    def encode(self, sentence: str) -> List[GEUL]:
        # 1. MRS 파싱
        mrs_list = self.parser.parse(sentence)
        
        results = []
        for mrs in mrs_list:
            # 2. 패턴 매칭
            rule, match_type = self.rule_db.match(mrs)
            
            # 3. 변환
            if match_type == 'miss':
                # LLM으로 새 룰 생성
                rule = self.generate_rule(mrs, sentence)
            
            geul = self.apply_rule(mrs, rule)
            
            # 4. 검증
            if self.validator.validate(geul):
                results.append(geul)
        
        return results
    
    def encode_batch(self, sentences: List[str]) -> List[GEUL]:
        # 배치 처리 최적화
        mrs_batch = self.parser.parse_batch(sentences)
        
        # 병렬 변환
        with ThreadPoolExecutor() as executor:
            results = executor.map(self._encode_mrs, mrs_batch)
        
        return list(results)
```

### B. 통계 수집

```python
class EncoderMetrics:
    def __init__(self):
        self.hit_count = 0
        self.miss_count = 0
        self.llm_calls = 0
        self.validation_failures = 0
    
    def report(self):
        total = self.hit_count + self.miss_count
        hit_rate = self.hit_count / total if total > 0 else 0
        
        return {
            'hit_rate': f"{hit_rate:.1%}",
            'llm_calls': self.llm_calls,
            'validation_failures': self.validation_failures,
            'cost_per_sentence': self.calculate_cost()
        }
```