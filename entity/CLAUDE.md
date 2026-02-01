# GEUL Entity SIDX 비트할당 자동 설계

## 프로젝트
GEUL(Grand Encoding for Universal Language) Entity Node의 48비트 속성 스키마를 위키데이터 실데이터 기반으로 자동 설계한다.

## 현재 상태 (2026-02-01)

| 항목 | 수치 |
|------|------|
| **위키데이터 전체 개체** | 117,419,925 |
| **Wikimedia 내부 (제외)** | 8,565,353 (7.3%) |
| **SIDX 대상** | 108,854,572 (92.7%) |
| **64개 타입 직접 커버** | 36,295,074 (33.3%) |
| **하위 타입 흡수** | 71,842,429 (66.0%) |
| **Other 폴백** | 717,069 (0.7%) |
| **최종 커버리지** | **100%** |
| **충돌률** | < 0.01% |

### Phase 상태
- [x] Phase 1: 준비 (스크립트 수정)
- [x] Phase 2: 파일럿 실행 (5개 타입)
- [x] Phase 2.5: 최적화 (OPT-1~4)
- [x] Phase 4: 전체 타입 확장 ← **완료**
- [x] 커버리지 갭 분석 ← **완료** (references/uncovered_types_analysis.md)
- [ ] Phase 5: 코드북 상세 생성
- [ ] Phase 6: 인코더 프로토타입

## DB

### 연결 정보
- **geuldev**: `postgresql://geul_reader:test1224@localhost:5432/geuldev` (READ ONLY)
- **geulwork**: `postgresql://geul_writer:test1224@localhost:5432/geulwork` (READ/WRITE)

### DB 접속 방법

**중요**: `psql` 명령어는 WSL 환경에서 작동하지 않음. **Python psycopg2 사용 필수**.

```python
# .venv 활성화 후 실행
import psycopg2

# 읽기 전용 (geuldev)
conn = psycopg2.connect(
    host="localhost", port=5432, dbname="geuldev",
    user="geul_reader", password="test1224"
)

# 쓰기 가능 (geulwork)
conn = psycopg2.connect(
    host="localhost", port=5432, dbname="geulwork",
    user="geul_writer", password="test1224"
)
```

```bash
# 가상환경 활성화 후 인라인 쿼리
source .venv/bin/activate
python3 -c "
import psycopg2
conn = psycopg2.connect('postgresql://geul_reader:test1224@localhost:5432/geuldev')
cur = conn.cursor()
cur.execute('SELECT COUNT(*) FROM entities')
print(cur.fetchone()[0])
conn.close()
"
```

### 주요 테이블 (geuldev)

| 테이블 | 행 수 | 용도 |
|--------|-------|------|
| entities | 117M | 위키데이터 Q-ID |
| triples | 1.7B | subject-property-object |
| entity_labels | 725M | 언어별 레이블 |
| property_usage_stats | 12K | 속성 사용 통계 |

- 절대 geuldev DB에 INSERT/UPDATE/DELETE 하지 않는다
- 모든 분석 결과는 geulwork에 저장한다

## Entity SIDX 구조 (확정)

```
1st WORD (16비트): Prefix(7) + Mode(3) + EntityType(6)
2nd WORD (16비트): Attributes 상위
3rd WORD (16비트): Attributes 중위
4th WORD (16비트): Attributes 하위
총 64비트 = 4워드 고정
```

- Mode 8가지: 0=등록, 1=특정단수, 2=특정소수, 3=특정다수, 4=전칭, 5=존재, 6=불특정, 7=총칭
- EntityType 6비트: 64개 타입 (우아한 열화 지원)
- Attrs 48비트: 타입별 완전 독립 스키마, 계층적 해석

## 핵심 설계 원칙

1. **타입별 완전 독립**: 각 EntityType마다 48비트 해석이 완전히 다름
2. **계층적 해석**: 상위 필드 값이 하위 필드의 코드 테이블을 결정 (예: Era → Polity)
3. **우아한 열화**: 비트를 덜 채울수록 추상적 표현 ("어떤 한국 남성 정치인")
4. **SIMD 최적화**: 비트 마스크로 범위 필터링 가능해야 함
5. **기계적 할당**: LLM이 자연어에서 자동으로 SIDX 생성 가능해야 함
6. **UID 없음**: 외부 ID(Q-ID 등)는 Triple로 분리, 48비트 전부 의미정렬

## 파일 구조

```
entity/
├── CLAUDE.md                    # 본 문서
├── references/
│   ├── entity_types_64.json     # 64개 EntityType 정의
│   ├── type_schemas.json        # 타입별 48비트 스키마 (v1.0 완료)
│   ├── type_mapping.json        # 하위 타입 → 64개 타입 매핑 ★ NEW
│   ├── uncovered_types_analysis.md  # 미분류 타입 분석 ★ NEW
│   ├── category_templates.json  # 9개 카테고리 템플릿
│   └── pipeline.md              # 파이프라인 상세
├── scripts/
│   └── validate_all_schemas.py  # 스키마 검증
├── output/
│   └── phase4_final_report.md   # Phase 4 최종 보고서
├── plans/                       # 각 Phase 계획서
├── finished/                    # 완료된 Phase 아카이브
└── cache/
    └── db_schema.md             # DB 스키마 캐시
```

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

- 모든 분석 결과는 `geulwork` DB에 테이블로 저장
- 최종 스키마 문서는 `output/` 디렉토리에 마크다운으로 출력
- 각 Stage 완료 시 `output/stage{N}_report.md`에 요약 보고서 작성
- 사람이 검토할 항목은 보고서에 `[REVIEW]` 태그로 표시

## 주의사항

- **현재 폴더(`entity/`)를 벗어난 경로의 파일/폴더를 생성, 수정, 삭제하지 않는다**
- 대용량 쿼리 시 LIMIT으로 샘플 먼저 확인 후 전체 실행
- 중간 결과를 geulwork에 저장하여 재실행 시 처음부터 안 해도 되게
- **psql 사용 불가** - Python psycopg2 사용 (.venv 활성화 필요)

## 다음 단계 (TODO)

1. ~~**커버리지 갭 분석**: 미분류 34M 개체가 어떤 타입인지 DB 쿼리로 확인~~ ✅ 완료
2. **Phase 5 코드북 상세 생성**: 64개 타입 각 필드의 상세 코드북
3. **Phase 6 인코더 프로토타입**: 자연어 → SIDX 변환 LLM 프롬프트 개발
4. **type_mapping.json 활용**: 인코더에서 하위 타입 매핑 로직 구현
