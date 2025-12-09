# **GEUL 쿼리 → 1-레이어(단일 블록) 트랜스포머로 컴파일**

## 1) 개념 요약

- **GEUL 쿼리 = 연산 그래프(IR)**
    
    필터(WHERE/ε-열화 허용), 가중치(확률/신뢰도), 시간·참조 제약, 집계(COUNT/AVG…).
    
- **실행 코어 = 1블록 트랜스포머**
    
    Attn(Q,K,V)=softmax(QK⊤/d+M) V\text{Attn}(Q,K,V)=\text{softmax}(QK^\top/\sqrt{d}+M)\,V
    
    여기서 **Q**는 쿼리에서 생성, **K,V**는 WMS 인덱스(사전 전처리), **M**은 필터·시간·확률 마스크.
    

한마디로, **쿼리를 가중치/마스크로 변환해 단일 어텐션으로 Top-k와 집계를 뽑는다**.

---

## 2) 컴파일 파이프라인

1. **GEUL 쿼리 파싱 → IR**
    - 조건(의미소·시간·확률)
    - 열화 허용도 ϵ\epsilon
    - 조인/참조 홉 수 hh
    - 집계 함수들( count/sum/avg … )
2. **하이퍼네트/LoRA 생성(경량 가중치)**
    - 기본 블록 가중치 W0W^0 고정.
    - 쿼리 qq로부터 **저랭크 어댑터** ΔW(q)=A(q)B(q)⊤\Delta W(q)=A(q)B(q)^\top 생성.
    - 최종 W=W0+ΔW(q)W = W^0 + \Delta W(q) → **1회 추론 동안만 유효한 “쿼리 전용 레이어”**.
3. **키/값 메모리(K,V) 준비**
    - WMS가 오브젝트별 **키 Ki∈RdK_i\in\mathbb{R}^d**, **값 ViV_i**, 메타(시간, 신뢰도, 태그) 제공.
    - 저장 단계에서 **8비트 양자화 인덱스**·**16비트 차원압축(PQ/LSH)** 적용 → GPU 상주.
4. **마스크/바이어스 MM 합성**
    - 시간 커널: mitime=κ(Δti)m^{time}_i = \kappa(\Delta t_i)
    - 확률/신뢰도: miconf=α⋅(pi−τ)m^{conf}_i = \alpha\cdot (p_i-\tau)
    - 의미 유사/열화 허용: misem=β⋅simϵ(Ki,q)m^{sem}_i = \beta\cdot \text{sim}_\epsilon(K_i, q)
    - 조합: Mi=mitime+miconf+misem+maskfiltersM_i = m^{time}_i + m^{conf}_i + m^{sem}_i + \text{mask}_{filters}
5. **단일 패스 실행 (Flash-Attention)**
    - softmax((QK⊤)/d+M)V\text{softmax}\big((QK^\top)/\sqrt d + M\big)V
    - **Top-k** 선택 + 선택된 VV로 **집계 헤드**(선형/간단 MLP) 수행.

---

## 3) 무엇이 가능한가

- **근사 최근접/의미 검색**: 쿼리-조건을 **Q, M**으로 변환 → 한 번의 어텐션으로 상위 결과.
- **시간/확률 필터**: 로짓에 직접 가중(마스크) → 재스코어링 불필요.
- **집계(Count/Sum/Avg/Weighted)**: 어텐션 가중치로 자연스럽게 구현.
- **다중 참조(코리퍼런스)**: 한 홉은 1패스. **다홉 조인**은 **스테이지드 1-패스 × h회**로 파이프라인 처리.
- **우아한 열화**: ϵ\epsilon을 올리면 상위 개념으로 자동 확장(리콜↑, 프리시전↓ 조절).

---

## 4) 성능/비용 포인트

- **연산 복잡도**: 기본은 O(Nd)O(Nd)이지만, IVF/PQ/LSH로 **후보 N′≪NN'\ll N** 만 GPU로 당겨서 계산.
- **INT8/FP16 친화**: 키/값 양자화 + Flash-Attention → **LLM 대비 10^1–10^2배 저렴**한 질의 경로.
- **캐시**: 인기 쿼리의 (Q,M)(Q,M) 캐시, 결과 Top-k/집계 캐시를 WMS와 공유.

---

## 5) 한계와 대처

- **복잡 조인/재귀**: 단일 블록 한 번으로는 무리 → **스텝드 실행 계획**(쿼리 플래너가 1-블록 호출을 여러 번).
- **정확 집계/정합성**: 근사 검색과 정확 집계를 분리. Top-k 후보를 뽑고, 필요 시 2단계 정확 검증.
- **권한/행 레벨 보안**: 마스크 MM에 **RBAC/ABAC**를 강제 주입(로짓 무한대 음수 마스킹).

---

## 6) 미니 수식 예 (요지)

- 로짓: ℓi=QKi⊤d+λ1mitime+λ2miconf+λ3misem+maskfilters,i\ell_i = \frac{QK_i^\top}{\sqrt d} + \lambda_1 m^{time}_i + \lambda_2 m^{conf}_i + \lambda_3 m^{sem}_i + \text{mask}_{filters,i}
- 가중치: ai=softmax(ℓ)ia_i = \text{softmax}(\ell)_i
- 응답: y=∑iaiViy = \sum_i a_i V_i, Top-k = 상위 kk의 ℓi\ell_i 인덱스
- 집계: count≈∑i1[ℓi>τ]\text{count} \approx \sum_i \mathbf{1}[\ell_i>\tau], avg(f)≈∑iaif(Vi)\text{avg}(f) \approx \sum_i a_i f(V_i)

---

## 7) 구현 체크리스트

- [ ]  **GEUL-쿼리 → IR 컴파일러**(EBNF/타입시스템/ε-열화 파라미터 포함)
- [ ]  **하이퍼네트/LoRA 생성기**(쿼리→ΔW)
- [ ]  **GPU 인덱스**: IVF-PQ(16b), INT8 키-값, Flash-Attn 커널
- [ ]  **집계 헤드**와 **다홉 실행 플래너**
- [ ]  **정확성 검증 루프**(근사 Top-k → 정확 재평가 옵션)