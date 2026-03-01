# 과업 4: Faber_Edge + Clause_Edge + Group_Edge 적용 사례 명확화

**작성일:** 2026-01-30  
**대상:** Faber_Edge.md, Clause_Edge.md, Group_Edge.md  
**목적:** 세 Edge 타입의 구체적 적용 사례 및 시나리오 명확화

---

## 1. 세 Edge 개요

| Edge | Prefix (Proposal) | 역할 | 상태 |
|------|-------------------|------|------|
| **Clause Edge** | `1100 000 010` | 논리적/담화적 관계 | v0.4 |
| **Faber Edge** | `1100 000 110` | 코드/AST 표현 | v0.1 |
| **Group Edge** | `1100 000 111 000` | 집합/그룹 | v0.1 |

---

## 2. Clause Edge 적용 사례

### 2.1 역할 요약

**RST(Rhetorical Structure Theory) 기반 담화 관계 표현**

| 코드 | 타입 | 용도 |
|------|------|------|
| 0000 | CAUSE | 원인→결과 |
| 0001 | RESULT | 결과←원인 |
| 0010 | CONDITION | 조건→귀결 |
| 0011 | PURPOSE | 목적 |
| 0100 | SEQUENCE | 시간순 |
| 0101 | PARALLEL | 동시/병렬 |
| 0110 | CONTRAST | 대조 |
| 0111 | CONCESSION | 양보 |
| 1000 | ELABORATION | 상세화 |
| 1001 | BACKGROUND | 배경 정보 |
| 1010 | EVIDENCE | 증거 제시 |
| 1011 | EVALUATION | 평가 |
| 1100 | SOLUTIONHOOD | 문제→해결 |
| 1101 | ALTERNATIVE | 선택/대안 |
| 1110 | MEANS | 수단 |

---

### 2.2 적용 사례 1: 인과관계

**문장:** "비가 와서 집에 있었다"

```
구조:
  Verb Edge E01: rain(비)          TID=0x0001
  Verb Edge E02: stay(나, 집)      TID=0x0002
  
  Clause Edge:
    Type: CAUSE (0000)
    Edge TID: 0x0100
    TID1: 0x0001 (원인: 비가 옴)
    TID2: 0x0002 (결과: 집에 있음)

패킷:
  1st: [1100 000 010] [0000] [00]
  2nd: [0x0100]
  3rd: [0x0001]
  4th: [0x0002]
```

---

### 2.3 적용 사례 2: 조건문

**문장:** "비가 오면 안 간다"

```
구조:
  Verb Edge E01: rain(비)                    TID=0x0001
  Verb Edge E02: go(나) [Polarity=부정]      TID=0x0002
  
  Clause Edge:
    Type: CONDITION (0010)
    Edge TID: 0x0100
    TID1: 0x0001 (조건)
    TID2: 0x0002 (귀결)

패킷:
  1st: [1100 000 010] [0010] [00]
  2nd: [0x0100]
  3rd: [0x0001]
  4th: [0x0002]
```

---

### 2.4 적용 사례 3: Event6 연결

**문장:** "Apple이 Tesla를 인수해서 주가가 올랐다"

```
구조:
  Event6 E01: (Apple, acquire, Tesla)   TID=0x0020
  Verb Edge E02: rise(주가)             TID=0x0002
  
  Clause Edge:
    Type: CAUSE (0000)
    Edge TID: 0x0100
    TID1: 0x0020 (Event6 참조!)
    TID2: 0x0002
```

**핵심:** Clause Edge는 Verb Edge뿐 아니라 **Event6, Triple, 다른 Clause도 연결** 가능

---

### 2.5 적용 사례 4: 중첩 Clause

**문장:** "비가 와서 집에 있었고, 그래서 공부했다"

```
구조:
  Verb Edge E01: rain(비)         TID=0x0001
  Verb Edge E02: stay(나, 집)     TID=0x0002
  Verb Edge E03: study(나)        TID=0x0003
  
  Clause Edge C01:
    Type: CAUSE
    TID1: 0x0001
    TID2: 0x0002
    Edge TID: 0x0100
  
  Clause Edge C02:
    Type: RESULT
    TID1: 0x0100 (C01 참조!)
    TID2: 0x0003
    Edge TID: 0x0101

그래프:
  E01 ──CAUSE──► E02
         │
         └──C01──RESULT──► E03
```

---

### 2.6 적용 시나리오 매트릭스

| 시나리오 | 타입 | TID1 | TID2 |
|----------|------|------|------|
| "A이기 때문에 B" | CAUSE | A | B |
| "A이면 B" | CONDITION | A | B |
| "A하고 B" (시간순) | SEQUENCE | A | B |
| "A지만 B" | CONCESSION | A | B |
| "A or B" (선택) | ALTERNATIVE | A | B |
| "A, 즉 B" (부연) | ELABORATION | A | B |

---

## 3. Faber Edge 적용 사례

### 3.1 역할 요약

**프로그래밍 언어 AST를 GEUL 그래프로 표현**

| 분류 | 코드 범위 | 예시 |
|------|-----------|------|
| Declaration | 000xxxxx | FuncDecl, VarDecl, TypeDecl |
| Statement | 001xxxxx | IfStmt, ForStmt, ReturnStmt |
| Expression | 010xxxxx | BinaryExpr, CallExpr, Ident |
| Type | 011xxxxx | PointerType, ArrayType |
| Pattern | 100xxxxx | WildcardPattern, TuplePattern |
| Modifier | 101xxxxx | Public, Private, Async |
| Structure | 110xxxxx | File, Module, Block |
| Language-specific | 111xxxxx | 언어 고유 노드 |

---

### 3.2 적용 사례 1: Go 함수

**코드:**
```go
func Add(a, b int) int {
    return a + b
}
```

**GEUL 표현:**
```
Faber Edge (FuncDecl):
  1st: [1100 000 110] [000100]     - Prefix + Go
  2nd: [000 00000] [00000000]      - FuncDecl + 예약
  3rd: [0x0010]                    - Edge TID
  4th: [0x0011]                    - Name "Add"
  5th: [0x0012]                    - Params
  6th: [0x0013]                    - Results
  7th: [0x0014]                    - Body
  8th: [0x0000]                    - 종결

Faber Edge (Ident) - Name:
  Lang: Go (000100)
  Type: Ident (010 00110)
  TID: 0x0011
  (Quantity Node로 "Add" 문자열 연결)

Faber Edge (BlockStmt) - Body:
  자식: [ReturnStmt TID]
```

---

### 3.3 적용 사례 2: Python 함수

**코드:**
```python
def greet(name: str) -> str:
    return f"Hello, {name}"
```

**GEUL 표현:**
```
Faber Edge (FuncDecl):
  1st: [1100 000 110] [100000]     - Prefix + Python
  2nd: [000 00000] [00000000]      - FuncDecl
  3rd: [0x0020]                    - Edge TID
  4th: [0x0021]                    - Name "greet"
  5th: [0x0022]                    - Params
  6th: [0x0023]                    - Returns
  7th: [0x0024]                    - Body
  8th: [0x0000]                    - 종결
```

---

### 3.4 적용 사례 3: 리프 노드 (식별자)

**코드:**
```go
x
```

**GEUL 표현:**
```
Faber Edge (Ident):
  1st: [1100 000 110] [000100]     - Prefix + Go
  2nd: [010 00110] [00000000]      - Ident
  3rd: [0x0030]                    - Edge TID
  4th: [0x0000]                    - 종결 (자식 없음)
```

---

### 3.5 적용 사례 4: PathGEUL (그래프 탐색)

**용도:** GEUL 그래프 내 패턴 탐색

**언어 코드:** `111110` (PathGEUL)

```
PathGEUL 쿼리: "FuncDecl의 모든 ReturnStmt 찾기"

Faber Edge (Descendant):
  Lang: PathGEUL (111110)
  Type: Descendant (00000010)
  자식: [FilterType: FuncDecl], [FilterType: ReturnStmt]
```

---

### 3.6 언어별 지원 매트릭스

| 언어 코드 | 언어 | 주요 용도 |
|-----------|------|-----------|
| 000000 | Abstract | 공통 AST |
| 000001 | C | 시스템 |
| 000100 | Go | GoGEUL |
| 100000 | Python | PyGEUL |
| 100001 | JavaScript | 웹 |
| 110000 | SQL | 쿼리 분석 |
| 111110 | PathGEUL | 그래프 탐색 |

---

### 3.7 AST 트리 구조 예시

```
FuncDecl (TID=0x0010)
├── Name: Ident "Add" (TID=0x0011)
├── Params: FieldList (TID=0x0012)
│   ├── Field "a" (TID=0x0015)
│   └── Field "b" (TID=0x0016)
├── Results: FieldList (TID=0x0013)
│   └── Field "int" (TID=0x0017)
└── Body: BlockStmt (TID=0x0014)
    └── ReturnStmt (TID=0x0018)
        └── BinaryExpr "+" (TID=0x0019)
            ├── Ident "a" (TID=0x001A)
            └── Ident "b" (TID=0x001B)
```

---

## 4. Group Edge 적용 사례

### 4.1 역할 요약

**복수 Node를 하나의 그룹으로 묶어 표현**

| 타입 | 코드 | 의미 | 멤버 수 |
|------|------|------|---------|
| AND | 000 | 논리곱 | 2+ |
| OR | 001 | 논리합 | 2+ |
| XOR | 010 | 배타적 선택 | 2+ |
| LIST | 011 | 순서 있는 목록 | 1+ |
| SET | 100 | 순서 없는 집합 | 1+ |
| RANGE | 101 | 범위 | 2 |
| PAIR | 110 | 순서쌍 | 2 |

---

### 4.2 적용 사례 1: AND 그룹

**문장:** "철수와 영희가 만났다"

```
구조:
  Entity: 철수     TID=0x0001
  Entity: 영희     TID=0x0002
  
  Group Edge (AND):
    Type: AND (000)
    Edge TID: 0x0100
    멤버: [0x0001, 0x0002]
  
  Verb Edge: meet
    Subject: 0x0100 (그룹 참조!)

패킷:
  1st: [1100 000 111 000] [000]
  2nd: [0x0100]
  3rd: [0x0001]    - 철수
  4th: [0x0002]    - 영희
  5th: [0x0000]    - 종결
```

---

### 4.3 적용 사례 2: OR 그룹

**문장:** "커피 또는 차를 주문하세요"

```
구조:
  Entity: 커피     TID=0x0001
  Entity: 차       TID=0x0002
  
  Group Edge (OR):
    Type: OR (001)
    Edge TID: 0x0100
    멤버: [0x0001, 0x0002]
  
  Verb Edge: order
    Object: 0x0100 (OR 그룹)

패킷:
  1st: [1100 000 111 000] [001]
  2nd: [0x0100]
  3rd: [0x0001]
  4th: [0x0002]
  5th: [0x0000]
```

---

### 4.4 적용 사례 3: XOR 그룹

**문장:** "합격 또는 불합격 (둘 중 하나만)"

```
구조:
  Entity: 합격     TID=0x0001
  Entity: 불합격   TID=0x0002
  
  Group Edge (XOR):
    Type: XOR (010)
    Edge TID: 0x0100
    멤버: [0x0001, 0x0002]
```

**OR vs XOR:**
- OR: "A 또는 B (둘 다 가능)"
- XOR: "A 또는 B (정확히 하나)"

---

### 4.5 적용 사례 4: LIST (순서 목록)

**문장:** "1등 철수, 2등 영희, 3등 민수"

```
구조:
  Entity: 철수     TID=0x0001
  Entity: 영희     TID=0x0002
  Entity: 민수     TID=0x0003
  
  Group Edge (LIST):
    Type: LIST (011)
    Edge TID: 0x0100
    멤버: [0x0001, 0x0002, 0x0003]  ← 순서 중요!
```

**SET과 차이:**
- LIST: 순서가 의미 있음 (순위, 시퀀스)
- SET: 순서 무관 (단순 집합)

---

### 4.6 적용 사례 5: RANGE (범위)

**문장:** "1부터 10까지"

```
구조:
  Quantity: 1      TID=0x0001
  Quantity: 10     TID=0x0002
  
  Group Edge (RANGE):
    Type: RANGE (101)
    Edge TID: 0x0100
    멤버: [0x0001, 0x0002]  ← 시작, 끝

의미: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 (사이 값 포함)
```

---

### 4.7 적용 사례 6: PAIR (순서쌍)

**문장:** "좌표 (3, 5)"

```
구조:
  Quantity: 3      TID=0x0001
  Quantity: 5      TID=0x0002
  
  Group Edge (PAIR):
    Type: PAIR (110)
    Edge TID: 0x0100
    멤버: [0x0001, 0x0002]

의미: (3, 5) - 두 값의 쌍, 사이 값 없음
```

**RANGE vs PAIR:**
- RANGE [1, 5] → 1, 2, 3, 4, 5
- PAIR [1, 5] → (1, 5)만

---

### 4.8 적용 사례 7: 복합 주어

**문장:** "철수, 영희, 민수가 학교에서 회의했다"

```
구조:
  Entity: 철수     TID=0x0001
  Entity: 영희     TID=0x0002
  Entity: 민수     TID=0x0003
  Entity: 학교     TID=0x0004
  
  Group Edge (AND):
    Edge TID: 0x0100
    멤버: [0x0001, 0x0002, 0x0003]
  
  Verb Edge: meet
    Subject: 0x0100 (AND 그룹)
    Location: 0x0004
```

---

## 5. 세 Edge 간 조합 사례

### 5.1 Clause + Group: "A와 B가 협력하거나 경쟁한다"

```
Entity: A          TID=0x0001
Entity: B          TID=0x0002

Group Edge (AND):  TID=0x0100
  멤버: [0x0001, 0x0002]

Verb Edge: cooperate    TID=0x0201
  Subject: 0x0100
  
Verb Edge: compete      TID=0x0202
  Subject: 0x0100

Clause Edge (ALTERNATIVE):
  TID1: 0x0201
  TID2: 0x0202
```

---

### 5.2 Faber + Group: 함수의 다중 파라미터

```
Faber Edge (ParamDecl) - param a    TID=0x0010
Faber Edge (ParamDecl) - param b    TID=0x0011

Group Edge (LIST):                   TID=0x0100
  멤버: [0x0010, 0x0011]

Faber Edge (FuncDecl):
  Params: 0x0100 (LIST 그룹 참조)
```

---

### 5.3 Clause + Faber: 코드 블록의 실행 순서

```
Faber Edge (AssignStmt) stmt1    TID=0x0020
Faber Edge (CallExpr) stmt2      TID=0x0021
Faber Edge (ReturnStmt) stmt3    TID=0x0022

Clause Edge (SEQUENCE):
  TID1: 0x0020
  TID2: 0x0021
  Edge TID: 0x0100

Clause Edge (SEQUENCE):
  TID1: 0x0100
  TID2: 0x0022
  Edge TID: 0x0101
```

---

## 6. 적용 시나리오 선택 가이드

### 6.1 결정 트리

```
표현하려는 것이?
│
├── 논리적/담화적 관계 ──► Clause Edge
│   │
│   ├── 인과? → CAUSE/RESULT
│   ├── 조건? → CONDITION
│   ├── 대조? → CONTRAST
│   └── 연결? → SEQUENCE/PARALLEL
│
├── 복수 개체의 그룹 ──► Group Edge
│   │
│   ├── 모두 참여? → AND
│   ├── 선택 가능? → OR/XOR
│   ├── 순서 있음? → LIST
│   ├── 순서 없음? → SET
│   └── 범위/쌍? → RANGE/PAIR
│
└── 코드/AST 구조 ──► Faber Edge
    │
    ├── 선언? → Declaration (000xxxxx)
    ├── 문장? → Statement (001xxxxx)
    ├── 표현식? → Expression (010xxxxx)
    └── 타입? → Type (011xxxxx)
```

---

### 6.2 시나리오별 권장

| 시나리오 | Edge | 타입 |
|----------|------|------|
| "A 때문에 B" | Clause | CAUSE |
| "A와 B가 함께" | Group | AND |
| "A 또는 B 선택" | Group | OR/XOR |
| "1부터 10까지" | Group | RANGE |
| "func f() {}" | Faber | FuncDecl |
| "A하고 B하고 C" | Clause | SEQUENCE |
| "(x, y) 좌표" | Group | PAIR |

---

## 7. 결론

### 7.1 역할 요약

| Edge | 핵심 역할 | 연결 대상 |
|------|-----------|-----------|
| **Clause** | 논리/담화 관계 | Verb, Event6, Triple, Clause |
| **Faber** | 코드/AST 표현 | 자식 Faber Edge |
| **Group** | 복수 개체 묶음 | Entity, Quantity, Edge |

### 7.2 상호 보완

```
Group Edge ─────► 복수 참여자 ─────► Verb Edge
                                        │
                                        ▼
                                    Event6 Edge
                                        │
                                        ▼
Clause Edge ◄───────── 인과/논리 ──────┘

Faber Edge ─────► AST 구조 (독립적 도메인)
```

### 7.3 문서 상태

| 문서 | 적용 사례 명확성 | 개선 필요 |
|------|------------------|-----------|
| Clause_Edge.md | ✅ 양호 | 시각적 다이어그램 |
| Faber_Edge.md | ⚠️ 보통 | 언어별 매핑 테이블 |
| Group_Edge.md | ✅ 양호 | 중첩 그룹 예시 |

---

**문서 종료**