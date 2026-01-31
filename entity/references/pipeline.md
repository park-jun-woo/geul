# Entity SIDX 비트할당 파이프라인 상세

## Stage 1: 타입별 속성 추출

### 목표
각 EntityType에 속한 개체들이 실제로 어떤 Property를 갖는지 통계 추출.

### 절차

1. P31(instance of) 기준 EntityType 매핑 테이블 생성
   - 현재 후보: Human(Q5), Taxon(Q16521), Star(Q523), Galaxy(Q318), Chemical(Q113145171) 등
   - 매핑은 geul_work.entity_type_map 테이블에 저장

2. 타입별 모든 Property 수집, 다음 통계 계산:
   - **커버리지**: 해당 타입 개체 중 이 속성을 가진 비율 (%)
   - **카디널리티**: 고유값 수
   - **엔트로피**: -Σ p(x) log2 p(x)) — 변별력 지표

3. 결과 저장: `geul_work.property_stats(entity_type, property_id, coverage, cardinality, entropy)`

4. **필터**: 커버리지 10% 미만 속성은 후보에서 제외

### 출력
타입별 속성 후보 목록 (커버리지 내림차순 + 엔트로피 내림차순)

---

## Stage 2: 계층 의존성 탐지

### 목표
속성 간 종속 관계를 자동 탐지하여 DAG 생성.

### 방법: 조건부 엔트로피

속성 A, B에 대해:
- H(B|A) = A를 알 때 B의 불확실성
- H(A|B) = B를 알 때 A의 불확실성
- I(A;B) = H(B) - H(B|A) = 상호정보량

**종속 판별 기준:**
- I(A;B) / min(H(A), H(B)) > 0.3 이면 종속으로 판정
- H(B|A) < H(A|B) 이면 A → B (A가 B를 결정)

### 절차

1. Stage 1에서 커버리지 상위 15개 속성 선택 (타입별)
2. 15C2 = 105쌍에 대해 조건부 엔트로피 계산
   - 대용량이면 10만 개체 샘플링
3. 종속 관계 간선 생성
4. 사이클 제거: 약한 간선(I가 낮은 것)부터 제거
5. DAG 확정

### 출력
- `geul_work.dependency_dag(entity_type, parent_prop, child_prop, mutual_info)`
- 타입별 DAG 시각화 (mermaid 또는 graphviz)

---

## Stage 3: 비트 할당 최적화

### 목표
48비트에 속성을 배치하여 충돌(동일 SIDX를 갖는 서로 다른 개체 쌍) 최소화.

### 3-A: 속성 순서 결정

DAG를 위상 정렬한다.
- 독립 속성(부모 없는 노드) 중 엔트로피 높은 것을 먼저 배치
- 종속 속성은 부모 뒤에 배치
- 보편 속성(성별 등 카디널리티 낮고 커버리지 높은 것)은 상위 우선

### 3-B: 각 필드 비트수 결정

탐욕적 할당:
```
budget = 48
for prop in sorted_properties:
    if prop is independent:
        bits = ceil(log2(cardinality))
    else:
        # 부모 값별 최대 카디널리티
        max_child_card = max(cardinality_per_parent_value)
        bits = ceil(log2(max_child_card))
    
    # 최소 2비트, 최대 12비트 제한
    bits = clamp(bits, 2, 12)
    
    if budget >= bits:
        assign(prop, bits)
        budget -= bits
    else:
        # 예산 부족: 비트수 축소하여 양자화
        assign(prop, budget)
        break
```

### 3-C: 잔여/초과 처리
- 잔여: 가장 양자화 손실 큰 필드에 비트 추가, 또는 Reserved
- 초과: 엔트로피 최저 속성부터 제거

### 3-D: 충돌률 계산

전체 개체를 인코딩한 뒤:
```sql
SELECT count(*) as collisions
FROM (
    SELECT sidx_48bit, count(*) as cnt 
    FROM encoded_entities 
    WHERE entity_type = ?
    GROUP BY sidx_48bit 
    HAVING count(*) > 1
) t;
```

### 충돌률 목표

| 타입 | 개체수 | 목표 충돌률 |
|------|--------|------------|
| Human | 12.5M | < 1% |
| Star | 3.6M | < 5% |
| Taxon | 3.8M | < 3% |
| Settlement | 580K | < 0.1% |
| 기타 < 500K | 다양 | < 1% |

### 출력
- `geul_work.bit_allocation(entity_type, prop_id, bit_offset, bit_width, parent_prop)`
- `geul_work.collision_stats(entity_type, total_entities, unique_sidx, collision_rate)`

---

## Stage 4: 코드북 생성

### 목표
계층적 코드 테이블 생성. 특히 부모 값에 따라 달라지는 자식 코드북.

### 절차

1. 독립 필드 코드북: 고유값을 빈도 내림차순으로 코드 부여
   ```
   성별: Male=01, Female=10, Other=11, Unknown=00
   ```

2. 종속 필드 코드북: 부모 값별로 별도 코드 테이블 생성
   ```
   Era=Ancient:  Polity: Egypt=001, Rome=010, Persia=011, ...
   Era=Medieval: Polity: Goryeo=001, Tang=010, Abbasid=011, ...
   Era=Current:  Polity: Korea=001, USA=010, Japan=011, ...
   ```

3. 코드 할당 원칙:
   - 빈도 내림차순 = 낮은 코드 번호
   - 0x00은 항상 "Unknown/Unspecified"
   - 코드 공간의 마지막 10%는 Reserved

4. **LLM 상식 검증**: 생성된 코드북을 Claude API에 보내서 이상 탐지
   - "Ancient 시대에 미국이 있다" → 오류
   - "Prehistoric 시대에 정치인 직업" → 오류

### 출력
- `geul_work.codebook(entity_type, field_name, parent_value, code, label, frequency)`
- `output/codebooks/` 디렉토리에 타입별 마크다운

---

## Stage 5: 검증

### 5-A: 충돌률 테스트
Stage 3-D의 충돌률이 목표 이내인지 최종 확인.

### 5-B: 추상 표현 테스트

부분 채움 SIDX로 범위 쿼리:
```
"어떤 한국 남성 정치인" 
= Mode=5, Type=Human, 성별=Male, 국적=Korea, 소분류=Politician
→ 나머지 비트 마스크 무시하고 SIMD 필터
→ 결과에 한국 남성 정치인만 포함되는지 확인
```

10개 이상의 추상 표현 테스트 케이스를 자동 생성하여 검증.

### 5-C: 인코딩 일관성 테스트

같은 개체를 다시 인코딩했을 때 같은 SIDX가 나오는지 (결정론적 인코딩).

### 5-D: 열화 테스트

비트를 뒤에서부터 하나씩 지워가며 상위 개념으로 자연스럽게 수렴하는지:
```
이순신(전체 48bit) → 한국 남성 군인 → 한국 남성 → 한국인 → 인간 → (EntityType만)
```

### 출력
- `output/stage5_report.md`: 전체 검증 결과
- [REVIEW] 태그로 사람 확인 필요 항목 표시
