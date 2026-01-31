# GEUL Entity SIDX 비트할당 자동 설계

## 프로젝트
GEUL(Grand Encoding for Universal Language) Entity Node의 48비트 속성 스키마를 위키데이터 실데이터 기반으로 자동 설계한다.

## DB
- **geuldev**: `postgresql://geul_reader:test1224@localhost:5432/geuldev` (READ ONLY)
- **geul_work**: `postgresql://geul_writer:test1224@localhost:5432/geulwork` (READ/WRITE)

- 절대 geuldev DB에 INSERT/UPDATE/DELETE 하지 않는다. 모든 분석 결과는 geul_work에 저장한다.
- 위키데이터 및 워드넷 데이터는 geuldev에 있다.

## Entity SIDX 구조 (확정)

```
1st WORD (16비트): Prefix(7) + Mode(3) + EntityType(6)
2nd WORD (16비트): Attributes 상위
3rd WORD (16비트): Attributes 중위  
4th WORD (16비트): Attributes 하위
총 64비트 = 4워드 고정
```

- Mode 8가지: 0=등록, 1=특정단수, 2=특정소수, 3=특정다수, 4=전칭, 5=존재, 6=불특정, 7=총칭
- EntityType 6비트: 이진 트리 (우아한 열화 지원)
- Attrs 48비트: 타입별 완전 독립 스키마, 계층적 해석

## 핵심 설계 원칙

1. **타입별 완전 독립**: 각 EntityType마다 48비트 해석이 완전히 다름
2. **계층적 해석**: 상위 필드 값이 하위 필드의 코드 테이블을 결정 (예: Era → Polity)
3. **우아한 열화**: 비트를 덜 채울수록 추상적 표현 ("어떤 한국 남성 정치인")
4. **SIMD 최적화**: 비트 마스크로 범위 필터링 가능해야 함
5. **기계적 할당**: LLM이 자연어에서 자동으로 SIDX 생성 가능해야 함
6. **UID 없음**: 외부 ID(Q-ID 등)는 Triple로 분리, 48비트 전부 의미정렬

## 작업 파이프라인

5단계 순서대로 실행한다. 상세 방법론은 `references/pipeline.md` 참조.

### Stage 1: 타입별 속성 추출
위키데이터에서 각 EntityType의 속성 분포 분석. 커버리지, 카디널리티, 엔트로피 계산.

### Stage 2: 계층 의존성 탐지  
속성 간 조건부 엔트로피로 종속 관계 DAG 생성.

### Stage 3: 비트 할당 최적화
48비트에 속성 배치. 충돌 최소화. DAG 순서 준수.

### Stage 4: 코드북 생성
Era별 Polity 테이블, 직업 테이블 등 계층적 코드북 자동 생성. LLM으로 상식 검증.

### Stage 5: 검증
전체 개체 인코딩 후 충돌률 측정. 추상 표현 SIMD 쿼리 테스트.

## 출력 규칙

- 모든 분석 결과는 `geul_work` DB에 테이블로 저장
- 최종 스키마 문서는 `output/` 디렉토리에 마크다운으로 출력
- 각 Stage 완료 시 `output/stage{N}_report.md`에 요약 보고서 작성
- 사람이 검토할 항목은 보고서에 `[REVIEW]` 태그로 표시

## 캐시 파일

- `cache/db_schema.md`: DB 스키마 전체 (테이블, 컬럼, 인덱스, 행 수 추정치, 유용한 쿼리 패턴)

## 주의사항

- **현재 폴더(`entity/`)를 벗어난 경로의 파일/폴더를 생성, 수정, 삭제하지 않는다**
- 대용량 쿼리 시 LIMIT으로 샘플 먼저 확인 후 전체 실행
- 중간 결과를 geul_work에 저장하여 재실행 시 처음부터 안 해도 되게
