# GEUL 데모 2: GoGEUL - AI 코드 생성의 새로운 패러다임

**Verifiable, Accumulative, Transparent Code Generation**

---

## 0. 한 줄 요약

LLM이 Go 코드를 GEUL AST로 생성하고, Transpiler가 실제 Go 코드로 변환하여, 문법 오류 제로, 축적 가능, Git-style diff 지원하는 AI 코딩 시스템

---

## 1. 핵심 가치 제안

### 문제: 현재 AI 코딩의 4가지 치명적 결함

```
문제 1: 휘발성
Claude: "HTTP 서버 만들어줘" → 코드 생성
사용자: "인증 추가해줘" → 처음부터 전체 재생성
→ 이전 버전 비교 불가
→ 변경사항 추적 불가

문제 2: 검증 불가능
Claude: [코드 생성]
→ Syntax error 있어도 모름
→ 실행해봐야 알 수 있음
→ 사용자가 복붙-테스트-피드백 반복

문제 3: 축적 불가능
어제 만든 함수를 오늘 재사용?
→ 불가능
→ 다시 설명해야 함
→ WMS에 저장 안 됨

문제 4: 추적 불가능
"왜 이렇게 코딩했어?"
→ 설명 불가능
→ 블랙박스
```

### 해결: GoGEUL 워크플로우

```
새로운 흐름:

사용자: "HTTP 서버 만들어줘"

LLM → Faber Edge (GEUL AST) 생성
   FuncDecl: main
   FuncDecl: handleRequest
   CallExpr: http.ListenAndServe
   
Transpiler → Go 코드 변환
   → go build
   → 실행 파일

WMS → GEUL AST 저장
   "2026-01-30, HTTP 서버, v1.0"

---

사용자: "인증 추가해줘"

LLM → 기존 AST 로드
   → 증분 변경(Δ)만 생성
   + FuncDecl: authenticate
   ~ CallExpr: handleRequest 내부 수정

Transpiler → 업데이트된 Go 코드

WMS → Δ 저장 (Git-style)
   "2026-01-30, 인증 추가, v1.1"
```

**결과:**
- 문법 오류: 원천 차단 (AST 검증)
- 축적: 모든 코드 WMS에 영구 저장
- 추적: 변경 이력 완전 추적
- 재사용: "이전 HTTP 서버" 즉시 로드

---

## 2. 데모 시나리오

### 시나리오 1: 웹 서비스 개발 (증분)

```
[Step 1]
User: "Go로 HTTP 서버 만들어줘. port 8080"

System:
→ GEUL AST 생성 (2초)
→ Go 코드 변환 (0.1초)
→ go build (1초)
→ 실행 파일 생성 ✓

생성된 파일:
- main.go (25 lines)
- go.mod

실행:
$ ./server
Server running on :8080

---

[Step 2]
User: "이제 /hello 엔드포인트 추가해줘"

System:
→ 기존 AST 로드
→ Δ 생성 (FuncDecl: handleHello 추가)
→ 변환 & 빌드

Diff 시각화:
+ func handleHello(w http.ResponseWriter, r *http.Request)
~ func main() { http.HandleFunc("/hello", handleHello) }

실행:
$ curl localhost:8080/hello
Hello World

---

[Step 3]
User: "JWT 인증 추가해줘"

System:
→ WMS 쿼리: "JWT authentication pattern Go"
→ 패턴 로드 (데모 3 연동)
→ AST에 통합
→ 변환 & 빌드

추가된 구성요소:
+ middleware/auth.go
+ models/user.go
+ security/jwt.go
~ main.go (middleware 적용)

실행:
$ curl -H "Authorization: Bearer <token>" localhost:8080/hello
Hello, authenticated user!
```

### 시나리오 2: 레거시 리팩토링

```
User: "이 Go 코드 리팩토링해줘"
[500줄 레거시 코드 업로드]

System:
→ Go 코드 → GEUL AST (파싱)
→ 분석:
  - 3개 god function (200+ lines)
  - 중복 코드 12곳
  - error handling 불일치
  
→ 리팩토링 제안:
  1. Extract methods (god function 분해)
  2. DRY (중복 제거)
  3. 표준 error handling
  
User: "실행"

System:
→ AST 변환
→ 새 코드 생성

결과:
- 500 lines → 320 lines (36% 감소)
- 함수 3개 → 15개 (책임 분리)
- Cyclomatic complexity: 45 → 18

Side-by-side diff:
[Before]  [After]
500 lines | 320 lines
3 funcs   | 15 funcs
복잡도 45  | 복잡도 18
```

### 시나리오 3: 멀티 프로젝트 재사용

```
[프로젝트 A: 2024년]
User: "REST API 서버 만들어줘"
→ GEUL AST 저장 (REST_API_v1.0)

[프로젝트 B: 2025년]
User: "작년에 만든 REST API 기반으로 새 프로젝트"

System:
→ WMS 쿼리: "REST_API_v1.0"
→ AST 로드
→ 프로젝트명만 변경
→ 생성

시간: 10초 (vs 5분 처음부터)

[프로젝트 C: 2026년]
User: "REST API인데 GraphQL 추가"

System:
→ REST_API_v1.0 로드
→ GraphQL 패턴 로드 (데모 3)
→ 통합
→ 생성

결과: REST + GraphQL 듀얼 지원
```

---

## 3. 기술 아키텍처

### 3.1 전체 구조

```
┌─────────────────────────────────────────────┐
│ Input Layer                                 │
├─────────────────────────────────────────────┤
│ 1. Natural Language Prompt                  │
│    "Go로 HTTP 서버 만들어줘"                 │
│                                             │
│ 2. Existing Go Code (optional)              │
│    [파일 업로드]                             │
│                                             │
│ 3. Previous GEUL AST (from WMS)             │
│    "이전에 만든 서버 기반으로..."            │
└─────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────┐
│ LLM Layer (Fine-tuned)                      │
├─────────────────────────────────────────────┤
│ - Prompt → GEUL AST                         │
│ - Go Code → GEUL AST (parsing)              │
│ - AST → AST Δ (incremental)                 │
│                                             │
│ Output: Faber Edge (Go AST in GEUL)         │
└─────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────┐
│ Validation Layer                            │
├─────────────────────────────────────────────┤
│ - Syntax check (AST well-formed)            │
│ - Type check (basic)                        │
│ - Import validation                         │
│ - Naming convention                         │
│                                             │
│ If fail → Retry LLM with error message      │
└─────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────┐
│ Transpiler (GEUL → Go)                      │
├─────────────────────────────────────────────┤
│ - AST → Go source code                      │
│ - go/format (pretty print)                  │
│ - Comment preservation                      │
│ - Idiomatic Go generation                   │
└─────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────┐
│ Build & Run                                 │
├─────────────────────────────────────────────┤
│ - go build                                  │
│ - go test (if tests exist)                 │
│ - Executable output                         │
└─────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────┐
│ WMS Storage                                 │
├─────────────────────────────────────────────┤
│ - GEUL AST permanent storage                │
│ - Version history (Git-style)               │
│ - Searchable by intent/pattern              │
│ - Reusable across projects                  │
└─────────────────────────────────────────────┘
```

### 3.2 Faber Edge 예시

```
프롬프트: "fibonacci 함수 만들어줘"

생성된 GEUL AST:

FaberEdge(FuncDecl):
  Language: Go (0b000100)
  NodeType: FuncDecl (0b00000000)
  EdgeTID: 0x0100
  Children:
    - TID 0x0101: Ident("fibonacci")
    - TID 0x0102: FieldList(Params)
        - Field: n int
    - TID 0x0103: FieldList(Results)
        - Field: int
    - TID 0x0104: BlockStmt(Body)
        - IfStmt:
            - Cond: BinaryExpr(n <= 1)
            - Body: ReturnStmt(n)
            - Else: ReturnStmt(
                BinaryExpr(
                  CallExpr(fibonacci, n-1),
                  +,
                  CallExpr(fibonacci, n-2)
                )
              )

워드 수: 약 50 워드 (100 bytes)
```

### 3.3 Transpiler 로직

```go
// transpiler/gogeul.go

package transpiler

func TranspileToGo(edges []FaberEdge) (string, error) {
    decoder := &GoDecoder{
        edges: edges,
        buf:   &bytes.Buffer{},
    }
    
    // Find top-level nodes (File/Package)
    for _, edge := range edges {
        if edge.NodeType == NodeFile {
            decoder.decodeFile(edge)
        }
    }
    
    // Format with go/format
    formatted, err := format.Source(decoder.buf.Bytes())
    if err != nil {
        return "", fmt.Errorf("format error: %w", err)
    }
    
    return string(formatted), nil
}

func (d *GoDecoder) decodeFuncDecl(edge FaberEdge) {
    d.buf.WriteString("func ")
    
    // Name
    nameEdge := d.edges[edge.Children[0]]
    d.buf.WriteString(nameEdge.Name)
    
    // Params
    d.buf.WriteString("(")
    paramsEdge := d.edges[edge.Children[1]]
    d.decodeFieldList(paramsEdge)
    d.buf.WriteString(")")
    
    // Results
    if len(edge.Children) > 2 {
        d.buf.WriteString(" ")
        resultsEdge := d.edges[edge.Children[2]]
        d.decodeFieldList(resultsEdge)
    }
    
    // Body
    d.buf.WriteString(" {\n")
    bodyEdge := d.edges[edge.Children[3]]
    d.decodeBlockStmt(bodyEdge)
    d.buf.WriteString("}\n")
}
```

---

## 4. 구현 계획

### Week 1-2: Go AST → GEUL Encoder

**목표:** Go 코드를 GEUL로 변환

```go
// encoder/go.go

package encoder

import "go/ast"

func EncodeGoFile(filename string) ([]FaberEdge, error) {
    fset := token.NewFileSet()
    file, err := parser.ParseFile(fset, filename, nil, 0)
    if err != nil {
        return nil, err
    }
    
    encoder := &GoEncoder{}
    ast.Walk(encoder, file)
    
    return encoder.edges, nil
}
```

**커버리지 목표:**
- Week 1: 기본 (Func, Var, If, For, Struct)
- Week 2: 고급 (Interface, Method, Defer, Go)

**테스트:**
```bash
$ gogeul encode examples/hello.go -o hello.geul
$ gogeul decode hello.geul -o hello2.go
$ diff hello.go hello2.go
# 동일해야 함
```

### Week 3-4: GEUL → Go Transpiler

**목표:** GEUL AST를 Go 코드로 변환

**품질 기준:**
- go/format 통과 (100%)
- go build 성공 (100%)
- 원본과 의미 동일

**테스트:**
```bash
$ gogeul transcode examples/*.go
Processed 50 files
Success: 50/50 (100%)
Build: 50/50 (100%)
```

### Week 5-6: LLM Fine-tuning

**목표:** GPT가 직접 GEUL AST 생성

**훈련 데이터 생성:**

```python
# training_data_gen.py

# 1. GitHub에서 Go 코드 수집
repos = fetch_go_repos(stars_min=100)  # 1,000개 repo

# 2. Go → GEUL 변환
for repo in repos:
    for file in repo.go_files:
        geul = encode_go_to_geul(file.content)
        
        # 3. 프롬프트 생성
        prompt = generate_prompt_from_code(file.content)
        
        # 4. 훈련 쌍 저장
        training_pairs.append({
            "prompt": prompt,
            "completion": geul.to_json()
        })

# 총 10만 쌍 생성
```

**Fine-tuning:**
```bash
$ openai api fine_tuning.jobs.create \
  -m gpt-4o-2024-08-06 \
  -t training_data.jsonl \
  --suffix "gogeul-v1"
  
# 또는 Anthropic
$ anthropic fine-tune \
  --model claude-3-5-sonnet-20241022 \
  --data training_data.jsonl
```

**검증:**
```python
prompt = "fibonacci 함수를 Go로 만들어줘"
response = finetuned_model.generate(prompt)

# GEUL AST 파싱
ast = parse_geul(response)

# 변환 & 빌드
code = transpile_to_go(ast)
result = subprocess.run(["go", "build"], input=code)

assert result.returncode == 0  # 빌드 성공
```

### Week 7-8: WMS 통합

**기능:**
1. AST 저장
2. 버전 관리
3. 검색 (intent-based)
4. Diff 생성

```go
// wms/code_storage.go

type CodeStorage struct {
    wms *WMS
}

func (cs *CodeStorage) Save(ast []FaberEdge, metadata CodeMetadata) error {
    // GEUL AST를 WMS에 저장
    entityID := cs.wms.CreateEntity(EntityCode)
    
    for _, edge := range ast {
        cs.wms.AddEdge(edge)
    }
    
    // 메타데이터 저장
    cs.wms.AddTriple(Triple{
        Subject:   entityID,
        Predicate: "created_at",
        Object:    metadata.Timestamp,
    })
    cs.wms.AddTriple(Triple{
        Subject:   entityID,
        Predicate: "intent",
        Object:    metadata.Intent,
    })
    
    return nil
}

func (cs *CodeStorage) Search(intent string) ([]CodeVersion, error) {
    // 의도 기반 검색
    query := fmt.Sprintf(`
        MATCH (code:Code)-[:has_intent]->(:Intent {text: "%s"})
        RETURN code
        ORDER BY code.created_at DESC
    `, intent)
    
    return cs.wms.Execute(query)
}
```

### Week 9-10: UI 개발

**화면 구성:**

```
┌─────────────────────────────────────────────┐
│ GoGEUL Code Generator                       │
├─────────────────────────────────────────────┤
│ Prompt:                                     │
│ > "HTTP 서버 만들어줘. JWT 인증 포함"        │
│                                             │
│ [Generate] [Load Previous]                  │
└─────────────────────────────────────────────┘

결과:

┌─ GEUL AST (트리 뷰) ─────────────────────────┐
│ File: main.go                               │
│ └─ Package: main                            │
│    ├─ Import: net/http                      │
│    ├─ Import: github.com/golang-jwt/jwt     │
│    ├─ FuncDecl: main                        │
│    ├─ FuncDecl: handleRequest               │
│    └─ FuncDecl: authMiddleware              │
│                                             │
│ File: models/user.go                        │
│ └─ StructDecl: User                         │
└─────────────────────────────────────────────┘

┌─ Generated Go Code ─────────────────────────┐
│ [main.go] [models/user.go] [auth.go]        │
│                                             │
│ package main                                │
│                                             │
│ import (                                    │
│     "net/http"                              │
│     jwt "github.com/golang-jwt/jwt/v5"      │
│ )                                           │
│                                             │
│ func authMiddleware(next http.Handler) ... │
│ ...                                         │
└─────────────────────────────────────────────┘

[Build & Run] [Save to WMS] [Download]
```

### Week 11: 고급 기능

**1. 증분 업데이트:**
```
User: "로깅 추가해줘"
→ 기존 AST 로드
→ log 패키지 import 추가
→ 각 함수에 log.Printf 추가
→ Diff 표시
```

**2. 멀티 파일:**
```
프로젝트 구조 자동 생성:
project/
├─ main.go
├─ handlers/
│  ├─ user.go
│  └─ post.go
├─ models/
│  └─ user.go
└─ middleware/
   └─ auth.go
```

**3. 테스트 생성:**
```
User: "테스트 코드도 만들어줘"
→ *_test.go 파일 자동 생성
→ table-driven tests
→ go test 실행
```

### Week 12: 테스트 & 문서

**통합 테스트:**
- [ ] Hello World 생성 & 실행
- [ ] HTTP 서버 생성 & 실행
- [ ] 증분 업데이트 (인증 추가)
- [ ] 레거시 리팩토링
- [ ] 멀티 프로젝트 재사용

**문서:**
- README
- API 문서
- 튜토리얼 (5개 예제)
- 데모 비디오 (5분)

---

## 5. 예상 결과

### 정량 지표

**변환 정확도:**
- Go → GEUL: 98%+
- GEUL → Go: 100% (go build 성공)

**성능:**
- 인코딩: <1초 (100 LOC)
- 디코딩: <0.1초
- LLM 생성: 2-5초

**축적:**
- Week 1: 100개 패턴
- Month 3: 1,000개 패턴
- Month 6: 10,000개 패턴

### 정성 효과

**개발자 생산성:**
- 초기 개발: 5배 빠름
- 리팩토링: 10배 빠름
- 재사용: 20배 빠름

**코드 품질:**
- 문법 오류: 0%
- 컨벤션 준수: 100%
- 테스트 커버리지: 자동 생성

---

## 6. 리스크 및 대응

| 리스크 | 영향 | 대응 |
|--------|------|------|
| LLM이 GEUL 학습 실패 | 고 | Fallback: Go → GEUL 자동 변환 |
| Transpiler 품질 낮음 | 중 | go/format + 인간 검수 |
| 커버리지 부족 | 중 | 단계적 확장 (80% → 95% → 99%) |
| WMS 성능 | 저 | 인덱싱 최적화 |

---

## 7. 성공 기준

- [ ] Hello World 생성 & 빌드 성공
- [ ] HTTP 서버 생성 & 실행 성공
- [ ] 증분 업데이트 작동
- [ ] WMS 저장/로드 작동
- [ ] GitHub 500+ stars
- [ ] Dev.to/HN 첫 페이지

---

**예산:** $10,000 (LLM fine-tuning)  
**팀:** 2-3명  
**기간:** 12주  
**시작:** 2026-04-15  
**완료:** 2026-07-15
