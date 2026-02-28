# GEUL 프로젝트 할일 목록

**작성일:** 2026-01-30  
**최종 검토:** 2026-01-30 (Context_Edge.md 완료 확인)  
**기준:** 프로젝트 문서 22개 분석 완료  
**목표:** 실행 가능한 단계별 로드맵  
**Phase 0 진행률:** 70% 완료 ✅ (모든 핵심 문서 작성 완료!)

---

## 📋 Phase 0: 이론/명세 완성 (4주)

**진행률: 약 70% 완료** ✅ (24개 핵심 문서 모두 작성 완료!)

### 문서 정리 및 보완
- [x] **Context_Edge.md 작성 완료** ✅ (11KB, v0.2)
- [x] GEUL_개요서.md 작성 완료 (19KB, v1.0)
- [x] GEUL-설계철학.md 작성 완료 (15KB)
- [x] 용어.md 작성 완료 (22KB)
- [ ] 용어.md 검토 및 통일성 확인
- [ ] 전체 문서 간 용어 일관성 점검
- [x] SIDX.md 작성 완료 (12KB, v0.9, Big Endian 규칙 포함)
- [x] Stream_Format.md 작성 완료 (9KB, v0.1)
- [ ] SIDX.md와 Stream_Format.md 크로스 레퍼런스 검증
- [x] Pronunciation_Rules.md 작성 완료 (6KB)

### 핵심 명세 검증
- [x] Entity_Node.md 작성 완료 (13KB)
- [x] Quantity_Node.md 작성 완료 (20KB)
- [x] Meta_Node.md 작성 완료 (12KB)
- [ ] Entity_Node.md + Quantity_Node.md + Meta_Node.md 통합성 검증
- [x] Verb_Edge.md 작성 완료 (12KB)
- [x] Event6_Edge.md 작성 완료 (13KB)
- [x] Triple_Edge.md 작성 완료 (11KB)
- [x] Context_Edge.md 작성 완료 (11KB, v0.2) ✅
- [ ] Verb_Edge.md + Event6_Edge.md + Triple_Edge.md + Context_Edge.md 관계 정리
- [x] Faber_Edge.md 작성 완료 (18KB, 코드/AST 표현)
- [x] Clause_Edge.md 작성 완료 (12KB)
- [x] Group_Edge.md 작성 완료 (12KB)
- [ ] Faber_Edge.md + Clause_Edge.md + Group_Edge.md 적용 사례 명확화
- [x] 동사_상위_분류.md 작성 완료 (13KB)
- [x] 개체_상위_분류.md 작성 완료 (11KB)
- [ ] 동사_상위_분류.md와 개체_상위_분류.md SIDX 매핑표 완성

### 아키텍처 문서화
- [x] SEGLAM_전체_데이터_흐름.md 기본 작성 완료 (4KB)
- [ ] SEGLAM 전체 데이터 흐름 상세화 (현재 간략, 확장 필요)
  - [ ] 심상관리 GPT 동작 상세
  - [ ] 쿼리 생성 GPT 알고리즘
  - [ ] WMS 쿼리 최적화 전략
  - [ ] 추론 GPT 체이닝
- [ ] WMS 인터페이스 명세 작성
  - [ ] 쿼리 API 명세
  - [ ] 저장 API 명세
  - [ ] 검색 알고리즘 (1-hop, N-hop)
  - [ ] 인덱싱 전략
- [ ] GEUL-C (캐시) 구조 명세
  - [ ] 캐시 키 구조
  - [ ] TTL 정책
  - [ ] 업데이트 전략
- [ ] GEUL-Agent 각 타입별 동작 명세
  - [ ] Consistency Agent
  - [ ] Calibration Agent
  - [ ] Relation Miner Agent
  - [ ] Pattern Miner Agent
  - [ ] Sememe Candidate Agent

### 데모 문서 (참고용, 이미 작성 완료)
- [x] GEUL데모1.md 완료 (10KB - Knowledge Graph Explorer)
- [x] GEUL데모2.md 완료 (19KB - GoGEUL Code Generator)
- [x] GEUL데모3.md 완료 (26KB - Software Pattern Library)

---

## 🔨 Phase 1: 핵심 인프라 구축 (12주)

### 1.1 WMS 기본 구조 (Week 1-4)
- [ ] Go 프로젝트 초기화 (모듈 구조, 패키지 설계)
- [ ] SIDX 저장/검색 기본 구조
  - [ ] 메모리 인덱스 구현
  - [ ] 디스크 저장 포맷 설계
  - [ ] 기본 CRUD 연산
- [ ] Node/Edge 타입별 구조체 정의
  - [ ] Entity, Quantity, Meta Node
  - [ ] Triple, Event6, Verb Edge
- [ ] 기본 쿼리 엔진 (1-hop)

### 1.2 GEUL Stream 파서/생성기 (Week 5-6)
- [ ] 16-bit 워드 기반 파서 구현
- [ ] 패킷 타입별 역직렬화
- [ ] 스트림 생성기 (구조체 → GEUL)
- [ ] TID 관리 시스템
- [ ] 유닛 테스트 (100개 샘플)

### 1.3 부트스트랩 파이프라인 (Week 7-12)
- [ ] MRS 파서 통합 (기존 오픈소스 활용)
- [ ] GPT-4o API 연동
  - [ ] Entity ID Pruning 프롬프트
  - [ ] 의미역 판단 프롬프트
  - [ ] 동사 한정사 추출 프롬프트
- [ ] 병렬 처리 워커 (100 concurrent)
- [ ] 비용 추적 시스템
- [ ] **목표:** 10만 문장 → GEUL 변환

---

## 🧪 Phase 2: 검증 시스템 구축 (8주)

### 2.1 Stage 1: 심볼릭 검증 (Week 13-16)
- [ ] Layer 1: 형식 검증 (비트 구조)
- [ ] Layer 2: SIDX 존재 검증
- [ ] Layer 3: 타입 일치 검증
- [ ] Layer 4: 시간/단위 검증
- [ ] Layer 5: 그래프 일관성 검증
- [ ] 성능 최적화 (<10ms/건)

### 2.2 Stage 2: LLM 검증 (Week 17-18)
- [ ] GPT-4o 검증 프롬프트 설계
- [ ] 의미론적 모순 탐지
- [ ] 도메인 지식 검증
- [ ] 오류 패턴 로깅

### 2.3 Stage 3: 인간 검수 UI (Week 19-20)
- [ ] 웹 기반 검수 인터페이스
- [ ] GEUL 시각화 (그래프 뷰)
- [ ] 승인/거부/수정 워크플로우
- [ ] 검수자 통계 대시보드

---

## 🎯 Phase 3: Demo 구축 (각 10-12주)

### Demo 1: Knowledge Graph Explorer (10주)
**Week 21-30**

#### 데이터 수집
- [ ] Wikidata 크롤러 (우선순위 Entity)
  - [ ] 정치인, 기업인, 학자 (10만 명)
  - [ ] 대학, 기업, 도시 (1만 개)
  - [ ] P69, P108, P26, P39 등 핵심 관계
- [ ] Entity → GEUL 변환 파이프라인
- [ ] Triple → WMS 저장

#### CC News 처리
- [ ] 뉴스 크롤러 (1천만 기사)
- [ ] Event6 자동 추출 (GPT 기반)
- [ ] 규칙 필터 (10만 건)
- [ ] 인간 검수 (1만 골든셋)
- [ ] Event6 → WMS 저장

#### N-hop 쿼리 엔진
- [ ] 3-hop 쿼리 최적화 (<10ms)
- [ ] 5-hop 쿼리 구현 (<100ms)
- [ ] 시간 범위 필터
- [ ] 집계 연산 (COUNT, GROUP BY)

#### UI 구축
- [ ] 자연어 쿼리 → GEUL 변환
- [ ] D3.js 그래프 시각화
- [ ] 시간 슬라이더
- [ ] 출처 추적 기능

### Demo 2: GoGEUL Code Generator (12주)
**Week 31-42**

#### Go AST → GEUL
- [ ] go/ast 패키지 통합
- [ ] 기본 노드 타입 인코딩
  - [ ] FuncDecl, VarDecl
  - [ ] IfStmt, ForStmt, AssignStmt
  - [ ] CallExpr, BinaryExpr
- [ ] 전체 Go 문법 커버리지 80%

#### GEUL → Go Transpiler
- [ ] Faber Edge → Go 코드 생성
- [ ] go/format 통합
- [ ] 역변환 검증 (왕복 테스트)

#### LLM Fine-tuning
- [ ] 훈련 데이터 생성 (1만 쌍)
  - [ ] GitHub 크롤링
  - [ ] Go 코드 → GEUL 자동 변환
  - [ ] 프롬프트 역생성
- [ ] GPT-4 Fine-tune
- [ ] 정확도 측정 (>80% 목표)

#### WMS 통합
- [ ] 코드 저장소 구현
- [ ] 검색 기능
- [ ] 의미론적 Diff 계산
- [ ] 버전 관리

#### Demo UI
- [ ] 웹 인터페이스
- [ ] 3패널 뷰 (AST/Code/Result)
- [ ] 증분 업데이트 기능
- [ ] 실시간 컴파일

### Demo 3: Software Pattern Library (8주)
**Week 43-50**

#### Knowledge Extraction
- [ ] 핵심 100개 패턴 수동 큐레이션
  - [ ] 로그인/인증 (10개)
  - [ ] 결제 시스템 (10개)
  - [ ] 데이터베이스 (20개)
  - [ ] API 설계 (20개)
  - [ ] 프론트엔드 (20개)
  - [ ] DevOps (20개)
- [ ] LLM 기반 자동 추출 파이프라인
- [ ] GEUL 구조화

#### 트렌드 데이터
- [ ] StackOverflow Survey 통합
- [ ] GitHub Stars 크롤링
- [ ] npm 다운로드 통계
- [ ] 외부 데이터 교차 검증

#### 검증 시스템
- [ ] 일관성 검사
- [ ] 최신성 검사 (180일)
- [ ] 완전성 검사
- [ ] 신뢰도 계산

#### UI 구축
- [ ] 패턴 검색/필터
- [ ] 기술 비교 테이블
- [ ] 의사결정 트리 (인터랙티브)
- [ ] 코드 템플릿 표시

---

## 📝 Phase 4: 문서화 및 논문 (8주)

### 4.1 학술 논문 (Week 51-54)
- [ ] "GEUL: A Universal Language for AI Reasoning"
  - [ ] Abstract, Introduction
  - [ ] Related Work
  - [ ] GEUL Architecture
  - [ ] Experiments & Results
  - [ ] Conclusion
- [ ] "Bootstrapping GEUL from Natural Language"
  - [ ] 9단계 파이프라인 상세
  - [ ] 비용/시간 분석
  - [ ] 정확도 측정
- [ ] arXiv 제출

### 4.2 기술 문서 (Week 55-56)
- [ ] GEUL Specification v1.0
- [ ] SEGLAM Architecture Guide
- [ ] WMS Implementation Guide
- [ ] API Reference
- [ ] Tutorial (10개 예제)

### 4.3 블로그/칼럼 (Week 57-58)
- [ ] "AI 시대의 새로운 언어" (대중용)
- [ ] "추론 과정을 저장하라" (철학)
- [ ] "창의성 경제가 온다" (비전)
- [ ] Medium, Substack 발행

---

## 🚀 Phase 5: 공개 및 확산 (12주)

### 5.1 오픈소스 공개 (Week 59-60)
- [ ] GitHub 리포지토리 생성
  - [ ] geul-lang/geul-core
  - [ ] geul-lang/seglam
  - [ ] geul-lang/wms
- [ ] MIT License 적용
- [ ] README, CONTRIBUTING, CODE_OF_CONDUCT
- [ ] CI/CD 설정 (GitHub Actions)

### 5.2 커뮤니티 구축 (Week 61-64)
- [ ] Discord 서버 개설
- [ ] 월간 뉴스레터
- [ ] 데모 사이트 배포
- [ ] API 공개 (무료 Tier)

### 5.3 학계 접촉 (Week 65-66)
- [ ] Stanford, MIT, CMU 세미나 신청
- [ ] NeurIPS/ICML 워크숍 제안
- [ ] 공동 연구 제안서

### 5.4 빅테크 접촉 (Week 67-70)
- [ ] Anthropic: PoC 제안
- [ ] OpenAI: 기술 데모
- [ ] Google: Research 협력
- [ ] 파트너십 문서 준비

---

## 🎯 Phase 6: 표준화 (진행 중)

### 6.1 GEUL Foundation 설립
- [ ] 비영리 재단 등록 (미국)
- [ ] 이사회 구성
- [ ] 거버넌스 문서

### 6.2 표준화 기구 접촉
- [ ] W3C Community Group 신청
- [ ] IETF 관심 그룹
- [ ] ISO/IEC JTC1 제안

### 6.3 Extension 생태계
- [ ] Extension 등록 프로세스
- [ ] Issuer ID 할당 시스템
- [ ] Extension 카탈로그

---

## 📊 핵심 마일스톤

| 주차 | 마일스톤 | 완료 조건 | 진행률 |
|------|----------|-----------|--------|
| 4주 | 명세 완성 | 24개 문서 최종 검토 완료 | **70%** ✅ |
| 12주 | WMS v0.1 | 10만 GEUL 스트림 저장/검색 | 0% |
| 20주 | 검증 시스템 | 90% 자동 검증 달성 | 0% |
| 30주 | Demo 1 완성 | Knowledge Graph 공개 | 0% |
| 42주 | Demo 2 완성 | GoGEUL 공개 | 0% |
| 50주 | Demo 3 완성 | Pattern Library 공개 | 0% |
| 58주 | 논문 제출 | arXiv + 학회 제출 | 0% |
| 70주 | 공개 완료 | 오픈소스 + 커뮤니티 활성화 | 0% |

**현재 위치:** Phase 0 (Week 3-4)
**완료된 주요 문서:**
- ✅ GEUL_개요서 (19KB)
- ✅ SIDX (12KB, v0.9)
- ✅ Stream_Format (9KB)
- ✅ 모든 Node/Edge 타입 문서 완료 (Context Edge 포함!)
- ✅ 3개 데모 문서

**다음 단계:** 문서 검증 및 통일성 확인 → Phase 1 진입

---

## 💰 예산 추정

### 인력
- 핵심 개발자 3명 × 18개월 × $15K/월 = $810K
- 검수자 10명 × 3개월 × $5K/월 = $150K

### 인프라
- GPU 서버 (학습): $50K
- WMS 서버 (3년): $30K
- API 서버 (1년): $20K

### LLM API
- 부트스트랩 (100만 문장): $11K
- 검증 (100만 건): $200
- Fine-tuning: $50K

### 기타
- 법률/재단: $50K
- 마케팅/커뮤니티: $30K

**총 예산: $1.2M (18개월)**

---

## ⚠️ 주요 리스크

### 기술 리스크
1. **문서 간 일관성 문제** (확률: 50%, 현재 상태)
   - 완화: 용어 통일 작업, 크로스 레퍼런스 검증 (이번 주 진행 예정)
   - 영향: 구현 단계에서 혼란, 재작업 필요

2. **LLM Fine-tuning 실패** (확률: 30%)
   - 완화: 대체 접근 (Prompt Engineering)
   - 영향: Demo 2 지연 4주

3. **N-hop 성능 미달** (확률: 20%)
   - 완화: SIMD 최적화, 캐싱 강화
   - 영향: Demo 1 품질 저하

4. **검증 정확도 부족** (확률: 40%)
   - 완화: 인간 검수 비율 증가
   - 영향: 비용 $50K 추가

### 시장 리스크
1. **빅테크 자체 개발** (확률: 60%)
   - 완화: 빠른 공개, 표준 선점
   - 영향: 경쟁 심화

2. **채택 부진** (확률: 40%)
   - 완화: 데모 품질, 커뮤니티 구축
   - 영향: 생태계 지연

### 프로젝트 관리 리스크
1. **Phase 0 지연** (확률: 20%, 위험 감소) ✅
   - 현재 진행률: 70% (Context_Edge 완료)
   - 완화: 문서 검증 작업 병렬화
   - 영향: 전체 일정 1주 지연 가능 (이전 2주에서 개선)

---

## 🎯 즉시 착수 항목 (우선순위)

### 이번 주
1. [x] **Context_Edge.md 작성 완료** ✅ (2026-01-30 완료)
2. [ ] 전체 문서 간 용어 일관성 점검
   - 용어.md 기준으로 통일
   - 각 문서에서 사용된 용어 검증
   - Context_Edge.md 용어 확인
3. [ ] 핵심 명세 문서 간 크로스 레퍼런스 검증
   - SIDX.md ↔ Stream_Format.md
   - Context_Edge.md ↔ Triple_Edge.md
   - 모든 Edge 타입 간 일관성
4. [ ] WMS Go 프로젝트 초기화
   - 모듈 구조 설계
   - 패키지 구조 설계
   - 기본 디렉토리 생성

### 이번 달
1. SEGLAM 아키텍처 상세화
   - 심상관리 GPT 동작 명세
   - 쿼리 생성 알고리즘
   - WMS 인터페이스 API 명세
2. GEUL Stream 파서 프로토타입
   - 16-bit 워드 기반 파서
   - 패킷 타입별 역직렬화
   - Context Edge 포함 100개 샘플 유닛 테스트
3. 10만 문장 부트스트랩 시작 준비
   - MRS 파서 선정 및 통합
   - GPT-4o API 프롬프트 설계
   - 비용 추적 시스템 기본 설계

### 3개월 내
1. Phase 0 완전 완료
   - 모든 검증 작업 완료
   - 최종 문서 리뷰
2. WMS v0.1 개발 착수
   - SIDX 저장/검색 기본 구조
   - Node/Edge 타입별 구조체 정의 (Context Edge 포함)
   - 기본 CRUD 연산
3. 검증 시스템 Layer 1-3 구현
   - 형식 검증 (비트 구조)
   - SIDX 존재 검증
   - 타입 일치 검증

---

**다음 업데이트:** 매주 월요일  
**진행 상황 추적:** GitHub Projects

---

## 📝 업데이트 히스토리

### 2026-01-30 (v1.2) - Context_Edge 완료! 🎉
**모든 핵심 문서 작성 완료**

**새로 완료된 문서:**
- ✅ Context_Edge.md (11KB, v0.2) - 세계관/출처/맥락 표현

**Phase 0 진행률:** 60% → **70%** ✅

**주요 성과:**
- 모든 Node 타입 완료 (Entity, Quantity, Meta)
- 모든 Edge 타입 완료 (Verb, Event6, Triple, Faber, Clause, Group, Context)
- 핵심 명세 완료 (SIDX, Stream Format)
- 아키텍처 문서 완료 (SEGLAM, GEUL 개요서)

**다음 단계:**
- 문서 간 용어 일관성 점검
- 크로스 레퍼런스 검증
- Phase 0 완료 후 Phase 1 (WMS 개발) 진입

### 2026-01-30 (v1.1)
**프로젝트 파일 검토 완료**

**완료된 문서 (21개):**
- GEUL_개요서.md (19KB)
- GEUL-설계철학.md (15KB)
- SIDX.md (12KB, v0.9)
- Stream_Format.md (9KB, v0.1)
- SEGLAM_전체_데이터_흐름.md (4KB)
- Entity_Node.md (13KB)
- Quantity_Node.md (20KB)
- Meta_Node.md (12KB)
- Verb_Edge.md (12KB)
- Event6_Edge.md (13KB)
- Triple_Edge.md (11KB)
- Faber_Edge.md (18KB)
- Clause_Edge.md (12KB)
- Group_Edge.md (12KB)
- 동사_상위_분류.md (13KB)
- 개체_상위_분류.md (11KB)
- 용어.md (22KB)
- Pronunciation_Rules.md (6KB)
- GEUL데모1.md (10KB)
- GEUL데모2.md (19KB)
- GEUL데모3.md (26KB)

**미완성 문서:**
- Context_Edge.md (0바이트, 비어있음) ⚠️

**Phase 0 진행률:** 60%

**주요 변경:**
- Phase 0 각 항목에 완료/미완료 체크박스 추가
- 문서 크기 정보 추가
- 즉시 착수 항목을 현재 상태에 맞게 재조정
- 핵심 마일스톤에 진행률 추가
- 주요 리스크에 현재 상황 반영
- Context_Edge.md 작성을 최우선 과제로 설정

### 2026-01-30 (v1.0)
- 초기 TODO 작성
- 6단계 Phase 정의
- 70주 로드맵 수립
