# SIDX-LLM 탐색 아키텍처

## 1. 전체 구조

SIDX-LLM 탐색은 두 단계로 구성된다.

```
SIDX 필터링 (심볼릭) → LLM 전수 검사 (뉴럴)

1억건 → SIDX 필터 → 10건 → LLM 판정 → 결과
```

SIDX 필터링이 후보를 극단적으로 줄이고, LLM이 남은 후보를 전수 검사한다. 벡터 유사도 검색(ANN)을 사용하지 않는다. 비트 AND 연산만으로 필터링하고, LLM이 분류한다.

---

## 2. SIDX 물리 구조

하나의 SIDX는 64비트 정수다.

```
64비트 레이아웃 (Entity Node 예시):

Proposal Prefix(7b) + Mode(3b) + EntityType(6b) + Attributes(48b)

[0001001 | Mode 3b | EntityType 6b | Attributes 48b ]
 Prefix    양화      타입(64종)      타입별 독립 스키마

타입별 Prefix (SIDX.md 참조):
  0001 1       = Tiny Verb Edge (고빈도 동사, 2워드)
  0001 01      = Verb Edge (일반 동사, 3~5워드)
  0001 001     = Entity Node (개체, 4워드)
  0001 000 110 = Triple Edge (속성/관계)
  0001 000 111 = Meta Node (스트림 제어)
  ...

Entity Node 48비트 Attributes (타입별 완전 독립):
  Human:  subclass(5) + occupation(6) + country(8) + era(4) + ...
  Star:   constellation(7) + spectral_type(4) + luminosity(3) + ...
  Film:   country(8) + year(7) + language(6) + genre(6) + ...
```

하나의 uint64 안에 타입 판별(Prefix+EntityType), 의미 필터링(Attributes 48비트)이 전부 들어있다. 외부 ID(Q-ID)는 별도 Triple로 분리되어 48비트 전부가 의미정렬에 사용된다.

---

## 3. Multi-SIDX

하나의 문서에 여러 개의 SIDX가 붙는다.

```
뉴스 기사 "삼성·엔비디아·현대차 총수 회동":

SIDX[0]: Entity(0x31 Document)  news / east_asia / current        문서 메타
SIDX[1]: Entity(0x2C Org)       media / east_asia / current       조선일보
SIDX[2]: Entity(0x00 Human)     business / east_asia / current    이재용
SIDX[3]: Entity(0x2D Business)  company / east_asia / current     삼성전자
SIDX[4]: Entity(0x00 Human)     business / n_america / current    젠슨황
SIDX[5]: Entity(0x2D Business)  company / n_america / current     엔비디아
SIDX[6]: Entity(0x00 Human)     business / east_asia / current    정의선
SIDX[7]: Entity(0x2D Business)  company / east_asia / current     현대차
SIDX[8]: Entity(0x2D Business)  restaurant / east_asia / current  깐부치킨
SIDX[9]: Verb Edge              SOCIAL-MEET                       회동
```

각 SIDX의 Q-ID 연결은 별도 Triple로 저장:
```
Triple(SIDX[2], P-Wikidata, "Q484523")  이재용
Triple(SIDX[3], P-Wikidata, "Q81965")   삼성전자
...
```

3계층으로 구분된다:
- Layer 1 — 문서 메타: 이 문서가 무엇인가 (EntityType=Document)
- Layer 2 — 출처: 누가 만들었나 (EntityType=Organization 등)
- Layer 3 — 콘텐츠: 무엇에 대한 내용인가 (Human, Business, Verb Edge 등)

전부 같은 64비트 SIDX 형식. 같은 인덱스에 저장. 같은 SIMD로 검색.

---

## 4. 인덱스 구조

### 기본: flat 배열

```
문서마다 SIDX 배열을 이어붙이면 그게 인덱스.

index.geul:  [SIDX][SIDX][SIDX][SIDX][SIDX][SIDX]...
offset.geul: [0, 5, 8, 15, 19, ...]  (각 문서의 시작 위치)

파일 2개. 이게 전부.
```

인덱스를 "구축"하는 게 아니라 "모으는" 것. cat 속도로 생성.

### 엔트리 단위

```
(SIDX 8바이트, ptr 4바이트) = 12바이트 pair

ptr이 가리키는 것:
  위키데이터 → 행 번호
  GDELT     → 이벤트 번호
  기업 문서  → 파일 오프셋
  PostgreSQL → row ctid
  S3         → 객체 인덱스

뭘 가리키든 4바이트. SIDX 옆에 붙어서 같이 정렬, 같이 탐색, 같이 읽힘.
```

### 크기

```
| 규모 | SIDX 수 | 인덱스 크기 |
|------|---------|-----------|
| 위키데이터 1.08억 엔티티 | 5.4억 (×5 Multi) | 6.5GB |
| GDELT 10억 이벤트 | 70억 (×7 Multi) | 84GB |
| 대규모 100억 문서 | 1000억 (×10 Multi) | 1.2TB |
| 구글급 1조 | 1조 | 12TB |

벡터 DB 대비:
  벡터 384dim: 1.08억 × 384 × 4B = 150GB
  SIDX:        1.08억 × 5 × 12B  = 6.5GB
  23배 작음. 100M 스케일.

  벡터 384dim: 1조 × 384 × 4B = 1.5PB
  SIDX:        1조 × 12B       = 12TB
  125배 작음. 1조 스케일.
```

---

## 5. 탐색 0단계: 전수 스캔 (SIMD)

가장 단순한 방법. 인덱스를 처음부터 끝까지 비트 AND로 스캔한다.

### 원리

```
mask    = 0xFFFF000000000000  (검사할 비트 위치)
pattern = 0x04A1000000000000  (기대하는 값)

for entry in index:
    if (entry.SIDX & mask) == pattern:
        results.add(entry.ptr)
```

AVX-512는 한 번에 64바이트 = 8개 uint64를 동시 비교한다.

### 성능

```
단일 SIDX (1억건, 800MB):
  AVX-512 연산: 800MB / 64B × 1사이클 = 1250만 사이클 = 4.2ms
  메모리 대역폭: 800MB / 50GB/s DDR5 = 16ms
  병목: 메모리. 실제 시간: ~16ms.

Multi-SIDX (1억건 × 10, 8GB):
  메모리 대역폭: 8GB / 50GB/s = 160ms
  32코어 병렬: 160ms / 32 = 5ms
```

비트 AND는 CPU가 할 수 있는 가장 싼 연산이다. 사이클 1-2개. 병목은 항상 메모리에서 데이터를 가져오는 시간이고, 비교 1번이든 7번이든 메모리 읽는 김에 같이 처리된다.

### Multi-SIDX 복합 조건

```
같은 doc_id에 다음 SIDX가 전부 존재하는 문서:

조건 A: EntityType=Document AND attrs.subtype=news
조건 B: EntityType=Human AND attrs.subclass=business AND attrs.country=USA
조건 C: EntityType=Human AND attrs.subclass=business AND attrs.country=Korea
조건 D: Verb Edge AND sub_primitive=SOCIAL-MEET

각 조건별 SIMD 스캔 (병렬, 각 40ms)
→ doc_id 교집합: A ∩ B ∩ C ∩ D

1억건:
  A (뉴스):                       1000만건
  A ∩ B (미국 기업인 뉴스):         50만건
  A ∩ B ∩ C (+ 한국 기업인):        5000건
  A ∩ B ∩ C ∩ D (+ SOCIAL-MEET):  12건

1억건 → 12건. 조건 4개로.
```

### 분할 스캔

SIDX 전수 스캔은 임의 분할이 가능하다.

```
벡터 DB HNSW: 그래프 전체가 메모리에 있어야 함. 분할 = 파괴.
SIDX: 각 엔트리가 독립. 분할 = 작은 배열 여러 개.
부분의 합이 전체와 같다 (집합 연산이므로).

서버 1대 (64GB RAM)로 8TB 스캔:
  60GB 청크 × 134번 = 110분. 결과 동일.

라즈베리파이 (4GB RAM)로 8TB 스캔:
  4GB 청크 × 2000번 = 5시간. 결과 동일.
```

### 스케일별 전수 스캔

```
| 규모 | 크기 | 단일 서버 | 10대 | 100대 |
|------|------|---------|------|-------|
| 1억 | 800MB | 16ms | - | - |
| 10억 | 8GB | 160ms | 16ms | - |
| 100억 | 80GB | 1.6초 | 160ms | 16ms |
| 1000억 | 800GB | 16초 | 1.6초 | 160ms |
| 1조 | 8TB | 불가(단일) | 16초 | 1.6초 |
```

AWS 스팟 인스턴스 200대 동원 시 1조 전수 스캔 800ms, 비용 $0.87.

---

## 6. 탐색 1단계: 디렉토리 파티셔닝

SIDX 상위 비트가 의미의 대분류이므로, 비트를 디렉토리로 펼치면 파일 시스템 자체가 인덱스가 된다.

### 원리

```
SIDX 비트: [Prefix 7][EntityType 6][Attributes 상위...]
디렉토리:  /prefix/entity_type/attr_field1/

파일을 여는 행위 = 비트 AND N번 실행한 것과 동일한 결과.
하지만 비트 연산 0번. OS가 파일 열어준 것뿐.
```

### 디렉토리 구조

```
index/
├── entity/
│   ├── human/
│   │   ├── politician/
│   │   │   ├── korea.geul
│   │   │   ├── usa.geul
│   │   │   └── ...
│   │   ├── military/
│   │   │   ├── korea.geul
│   │   │   └── ...
│   │   └── ...
│   ├── business/
│   ├── star/
│   └── ...
├── verb/
│   ├── social-meet/
│   │   └── all.geul
│   ├── move-go/
│   └── ...
├── triple/
└── meta/
```

### 파티셔닝 깊이별 효과

```
| 깊이 | 기준 | 파일 수 | 파일 크기 (1조 기준) | 라즈베리파이 |
|------|------|--------|-------------------|------------|
| 0 | 없음 | 1 | 8TB | 5시간 |
| 1 | Prefix (타입 분기) | ~10 | 800GB | 50분 |
| 2 | + EntityType 6비트 | 640 | 12.5GB | 50초 |
| 3 | + 속성 상위 5비트 | 20,480 | 390MB | 1.5초 |
| 4 | + 속성 차상위 5비트 | 655,360 | 12MB | 50ms |
```

### 쿼리 예시

```
"미중 정상 외교 회담":

파일 3개만 열면 됨:
  index/entity/human/politician/usa.geul    (72MB)
  index/entity/human/politician/china.geul  (96MB)
  index/verb/social-meet/all.geul           (800MB)

비트 AND: 0번.
읽는 데이터: 968MB (8TB의 0.012%)
라즈베리파이: 2초.
```

### 핵심 원리

비트 상위→하위 순서가 의미의 대분류→소분류 순서이고, 디렉토리 깊이와 일치한다. 벡터 임베딩은 상위 비트에 의미가 없으므로 이 최적화가 원천적으로 불가능하다.

---

## 7. 탐색 2단계: 정렬 + 이진 탐색

디렉토리 파티셔닝으로 도달한 파일 내부에서, SIDX가 정렬되어 있으면 전수 스캔 대신 이진 탐색이 가능하다.

### 원리

```
파일: noun/person/head_of_state/north_america.geul
내용: 900만 (SIDX, ptr) pair

정렬 안 됨: 900만건 전수 스캔 → 72MB 읽기 → 144ms
정렬됨: 이진 탐색 log2(900만) = 23번 비교 → 184바이트 읽기 → 0.002ms
```

### 파일 내부 구조

```
Q-ID 기준 정렬:

[Q76,     doc_ids: [102, 203, 501, 892, ...]]       오바마
[Q6279,   doc_ids: [3829, 4011, 4523, 7291, ...]]   바이든
[Q22686,  doc_ids: [1024, 2048, 5012, 5201, ...]]   트럼프
[Q35836,  doc_ids: [8821, 9012, ...]]                부시

바이너리:
[Q-ID 4B | doc_count 4B | doc_id doc_id doc_id ...]
[Q-ID 4B | doc_count 4B | doc_id doc_id doc_id ...]
```

Q-ID 이진 탐색으로 특정 엔티티에 직행. 각 Q-ID 내 doc_id 리스트도 정렬되어 있어 merge join으로 교집합.

### 쿼리 예시: 미중 정상 회담 최종

```
1단계: 파일 경로로 점프 (비트 연산 0번)
  entity/human/politician/usa.geul
  entity/human/politician/china.geul

2단계: 정렬된 파일에서 이진 탐색 (전수 스캔 0번)
  미국: 바이든 Q6279 → 23번 비교 → doc_ids
        트럼프 Q22686 → 23번 비교 → doc_ids
        오바마 Q76    → 23번 비교 → doc_ids
  중국: 시진핑 Q15031 → 23번 비교 → doc_ids
        후진타오 Q8562 → 23번 비교 → doc_ids

3단계: doc_id 교집합 (정렬되어 있으므로 merge join)
  바이든 ∩ 시진핑:   {3829, 4011}
  트럼프 ∩ 시진핑:   {5012, 5201}
  오바마 ∩ 후진타오:  {102, 203}

4단계: verb/social-meet 파일에서 해당 doc_id 확인
  doc 3829 → meeting ✅
  doc 4011 → meeting ✅
  doc 102  → meeting ✅
  doc 203  → summit  ✅

결과: 4건.
```

### 읽은 데이터량

```
이진 탐색 1회: 8B × 23단계 = 184바이트
정상 5명 × 184B = 920바이트
doc_id 리스트: 수천건 × 4B = 수십KB
meeting 확인: 수십건 × 8B = 수백바이트

총: ~100KB. 8TB의 0.0000012%.
```

### 성능

```
| 장비 | 100KB 읽기 | 이진 탐색 + 교집합 | 총 |
|------|-----------|------------------|-----|
| 라즈베리파이 | 0.2ms | 0.8ms | 1ms |
| 노트북 | 0.05ms | 0.05ms | 0.1ms |
| 서버 | 0.002ms | 0.008ms | 0.01ms |
```

---

## 8. 정렬 전략

### 용도별 이중 정렬

```
같은 (SIDX, ptr) pair 데이터를 두 가지로 정렬해 보관:

by_sidx.geul:  SIDX 순 정렬 → "이 조건에 맞는 문서 전부" (검색용)
by_doc.geul:   doc_id 순 정렬 → "이 문서의 태그 전부" (조회용)

같은 데이터, 정렬만 다름.
```

### 정렬 비용

```
1조 엔트리 정렬:
  12TB 외부 정렬 (merge sort)
  SSD 기준: 수 시간. 1회성.

Elasticsearch 역인덱스 구축: 수 시간~수일.
HNSW 그래프 구축: 수 시간~수일.
SIDX 정렬: sort 명령어 한 번. 동급이거나 더 빠름.
```

### 인덱스 구축 = 정렬

```
Elasticsearch: 토크나이징 → 분석 → 역인덱스 구축 → 세그먼트 머지
Pinecone:      임베딩 → HNSW 그래프 구축 → 클러스터링
SIDX:          sort

60년간 최적화된 정렬 알고리즘을 그대로 사용.
B-tree, HNSW, 역인덱스 어느 것도 필요 없다.
```

---

## 9. 5단계 최적화 종합

```
| 단계 | 방법 | 읽는 데이터 (1조) | 라즈베리파이 | 서버 |
|------|------|-----------------|------------|------|
| 0 | 전수 스캔 | 8TB | 5시간 | 140ms |
| 1 | 디렉토리 파티셔닝 | 968MB | 2초 | 20ms |
| 2 | 깊이 4 파티셔닝 | 24MB | 50ms | 0.5ms |
| 3 | + 이진 탐색 | 100KB | 1ms | 0.01ms |
| 4 | + doc_id merge join | 100KB | 1ms | 0.01ms |
```

5시간 → 1ms. 같은 데이터. 같은 하드웨어. 같은 결과.

모든 단계에서 결과는 수학적으로 동일하다. 속도만 다르다. 분할해도 결과 동일. 비트 AND는 순서 무관, 상태 없음, 합산 가능.

---

## 10. 벡터 DB와의 비교

```
| 속성 | SIDX | 벡터 DB (HNSW) |
|------|------|---------------|
| 상위 비트에 의미 | 있음 (대분류) | 없음 |
| 디렉토리 파티셔닝 | 가능 | 불가능 |
| 정렬 후 이진 탐색 | 가능 | 불가능 (벡터 정렬 무의미) |
| 분할 스캔 | 가능 (결과 동일) | 불가능 (그래프 끊김) |
| 콜드 스타트 | 파일 열면 즉시 | 그래프 구축 수 시간 |
| 복합 조건 | 교집합 (정확) | 벡터 1개로 압축 (근사) |
| 인덱스 크기 (1조) | 12TB | 1.5PB |
| 인덱스 구축 | sort | HNSW 구축 수 일 |
| 결과 | 정확 (집합 연산) | 근사 (유사도 순위) |
```

---

## 11. LLM 전수 검사 단계

SIDX 필터링 이후 남은 후보를 LLM이 전수 검사한다.

```
필터링 결과 10건:
  각 문서를 LLM에 입력
  "이 문서가 '미중 정상 외교 회담'에 해당하는가? relevant/irrelevant"
  
  10건 × ~200토큰 = 2000토큰
  처리 시간: ~2ms (배치)
  비용: 거의 $0
```

SIDX가 10건까지 줄였기 때문에 LLM은 가장 쉬운 일만 한다. 이진 분류(relevant/irrelevant). LLM이 가장 잘하는 태스크. 환각할 여지 없음.

```
전체 파이프라인:
  SIDX 필터: 1조 → 10건 (1ms)
  LLM 판정: 10건 → 4건 (2ms)
  총: 3ms
```

---

## 12. 하드웨어별 실현 가능성

```
| 장비 | 비용 | 1조 탐색 시간 | 용도 |
|------|------|-------------|------|
| 라즈베리파이 | $35 | 1ms (최적화) ~ 5시간 (전수) | 연구/학생 |
| 노트북 | $1000 | 0.1ms (최적화) ~ 75분 (전수) | 개인 |
| 서버 1대 | $200/월 | 0.01ms (최적화) ~ 110분 (전수) | 중소기업 |
| AWS 12대 | $2.90/회 | 140ms (전수, 메모리 상주) | 대기업 |
| AWS 200대 스팟 | $0.87/회 | 800ms (전수) | 빅테크 배치 |
| H100 104장 | $400K/월 | 24ms (전수) | 실시간 서비스 |
```

전부 같은 코드. 같은 바이너리. 같은 결과. 장비만 다르다.

---

## 13. 설계 원리 요약

1. **비트 레이아웃 = 디렉토리 구조 = 의미 계층.** 상위 비트가 대분류, 하위 비트가 소분류. 물리적 배치와 의미 구조가 일치한다.

2. **정렬된 uint64 배열이 곧 인덱스.** sort 한 번이 인덱스 구축. B-tree, HNSW, 역인덱스 불필요.

3. **분할해도 결과가 동일.** 비트 AND는 순서 무관, 상태 없음. 라즈베리파이든 H100 100장이든 결과는 같고 시간만 다르다.

4. **파일 여는 행위가 필터링.** 별도 인덱스 자료구조 없이 OS 파일 시스템이 검색 엔진 역할을 한다.

5. **벡터 임베딩은 이 최적화가 원천 불가능.** 벡터 상위 비트에 의미 없음. 정렬 무의미. 파티셔닝 불가. 분할 불가. 항상 전체 그래프 필요.