
# GEUL 비트 명세서 (GEUL Bit Layout Specification)

- 문서명: GEUL-비트명세서.md  
- 버전: v0.1  
- 단위: 64비트 GEUL Word (MID/TID용 의미정렬 ID)  
- 비트 번호 규칙:  
  - **1비트 = 최상위(MSB)**  
  - **64비트 = 최하위(LSB)**

---

## 1. 최상위 구조 개요

GEUL 64비트 워드는 최상위 비트로 두 계층을 나눈다.

```text
bit1: GEUL Standard 플래그
  0 = GEUL Standard (월드 내부 노드/엣지용 ID)
  1 = GEUL Extension (Issuer / 자유 / 차세대 용도)
````

* **bit1 = 0 (Standard)** 인 경우:
  → bit2를 **Kind (노드/엣지)** 로 해석한다.
* **bit1 = 1 (Extension)** 인 경우:
  → bit2는 Kind가 아니며, **Extension Class** 로 별도 해석한다.

---

## 2. GEUL Standard (bit1 = 0)

### 2.1 Kind (bit2)

```text
bit1 = 0 (Standard)일 때만 유효

bit2: Kind
  0 = 노드(Node)
  1 = 엣지(Edge)
```

---

## 3. Standard Node (bit1=0, bit2=0)

Node는 bit3에서 다시 두 갈래로 나뉜다.

```text
bit3:
  0 = 개체 / 동사 / 컨텍스트 노드
  1 = 물리량 노드
```

### 3.1 개체 / 동사 / 컨텍스트 그룹 (bit3 = 0)

여기서 bit4, bit5로 다시 세분화한다.

```text
bit1 = 0 (Standard)
bit2 = 0 (Node)
bit3 = 0 (개체/동사/컨텍스트 그룹)

bit4:
  0 = 개체(Entity) 노드
  1 = 동사/컨텍스트 노드 그룹

if bit4 == 1:
  bit5:
    0 = 동사(Verb) 노드
    1 = 컨텍스트(Context) 노드
```

#### 3.1.1 개체 노드 (Entity Node)

```text
bit1 = 0
bit2 = 0 (Node)
bit3 = 0 (Entity/Verb/Context 그룹)
bit4 = 0 (Entity)

bit5..56  : 속성 약식 표현 비트 (52비트)
bit57..64 : 중복방지용 로컬 ID (8비트)
```

* **bit5..56 (52비트)**

  * 개체의 상위 분류, 타입, 플래그, 상태 등을 compact하게 표현하는 용도.
  * 예: PERSON/ORG/PLACE/WORK, alive/dead, player/NPC, 주요 캐릭터 플래그 등.
* **bit57..64 (8비트)**

  * 동일한 속성 패턴을 가진 개체가 여러 개 존재할 때 중복 방지용 local suffix.

#### 3.1.2 동사 노드 (Verb Node)

```text
bit1 = 0
bit2 = 0 (Node)
bit3 = 0
bit4 = 1 (Verb/Context 그룹)
bit5 = 0 (Verb)

bit6..64 : 동사 종류 ID + 동사 한정사 11종
```

동사 한정사(verb modifiers)는 다음과 같이 22비트 사용:

| 항목                  | 비트 수 | 설명                  |
| ------------------- | ---: | ------------------- |
| 증거성(Evidentiality)  |  2비트 | 정보 출처               |
| 서법(Mood)            |  2비트 | 서술/명령/가정            |
| 양태(Modality)        |  2비트 | 화자의 의지 강도           |
| 시제(Tense)           |  2비트 | 과거/현재/미래            |
| 상(Aspect)           |  3비트 | 진행/완료/결과 중심 (비트마스크) |
| 기간/시점(Period/Point) |  1비트 | 시점 vs 기간            |
| 공손(Politeness)      |  2비트 | 반말/존대 등             |
| 긍/부정(Polarity)      |  2비트 | 긍정/부정               |
| 의도성(Volitionality)  |  2비트 | 의도적/비의도적            |
| 확신성(Confidence)     |  2비트 | 추측/확신               |
| 반복성(Iterativity)    |  2비트 | 반복 정도               |

합계: **22비트**

따라서:

```text
bit6..(6+21) = bit6..27 : 동사 한정사(22비트)
bit28..64             : 동사 종류 ID (37비트)
```

37비트 동사 ID 공간 → 약 1,37e11 개 (사실상 충분히 넉넉한 동사 타입 수).

각 한정사의 코드는 다음과 같이 정의한다.

##### (1) 증거성 (Evidentiality, 2비트)

```text
00 = 직접경험
01 = 전언/보고
11 = 추론
10 = 알 수 없음
```

##### (2) 서법 (Mood, 2비트)

```text
00 = 서술(진술)
01 = 명령
11 = 가정/가정법
10 = 알 수 없음
```

##### (3) 양태 (Modality, 2비트, 화자의 의지)

```text
00 = 중립
01 = 강한 의지
11 = 의지 없음
10 = 알 수 없음
```

##### (4) 시제 (Tense, 2비트)

```text
00 = 현재
01 = 미래
11 = 과거
10 = 알 수 없음
```

##### (5) 상 (Aspect, 3비트, 비트마스크)

```text
bitA1 (LSB) = 진행(Progressive)
bitA2       = 완료(Perfective)
bitA3       = 결과 중심(Resultative)

000 = 사용 안 함 / 없음
001 = 진행
010 = 완료
100 = 결과 중심
…   = 조합 가능 (예: 011 = 진행 + 완료)
```

##### (6) 기간/시점 (Period/Point, 1비트)

```text
0 = Point (한 시점)
1 = Period (기간)
```

##### (7) 공손 (Politeness, 2비트)

```text
00 = 중립
01 = 존대 / 높임
11 = 반말 / 낮춤
10 = 알 수 없음
```

##### (8) 긍정/부정 (Polarity, 2비트)

```text
00 = 중립 / 명시 안 함
01 = 긍정
11 = 부정
10 = 알 수 없음
```

##### (9) 의도성 (Volitionality, 2비트)

```text
00 = 중립 / 명시 안 함
01 = 의도적
11 = 비의도적
10 = 알 수 없음
```

##### (10) 확신성 (Confidence, 2비트)

```text
00 = 중립 / 보통
01 = 확신
11 = 추측 / 낮은 확신
10 = 알 수 없음
```

##### (11) 반복성 (Iterativity, 2비트)

```text
00 = 알 수 없음
01 = 1회
10 = 많음 (여러 번)
11 = 무한 / 습관적
```

> 구현 시 실제 비트순서는 고정된 스펙으로 별도 표를 두고,
> `bit6..64` 안에 (한정사 → 동사ID) 순으로 packing 한다.

#### 3.1.3 컨텍스트 노드 (Context Node)

```text
bit1 = 0
bit2 = 0 (Node)
bit3 = 0
bit4 = 1
bit5 = 1 (Context)

bit6..64 : 컨텍스트 약식 표현 비트 (59비트)
```

* 이 비트들은 **Context 노드의 타입과 메타정보를 compact하게 표현**하는 용도.
* 예시로 들어갈 수 있는 것들:

  * World ID 구역 (RealWorld / MCU / 소설World 등)
  * Time Bucket (연도/연대/시대 구간)
  * POV 타입 (1인칭/3인칭/신 등)
  * Modality (현실/가상/꿈/기억/시뮬레이션)
* 상세 구조는 별도의 “컨텍스트 비트명세서” 서브 문서에서 정의 가능.
  이 상위 스펙에서는 “59비트 컨텍스트 압축 표현 슬롯”까지만 고정.

---

### 3.2 물리량 노드 (bit3 = 1)

```text
bit1 = 0
bit2 = 0 (Node)
bit3 = 1 (물리량)
```

#### 3.2.1 공통 헤더

```text
bit4: Unsigned 플래그
  0 = signed
  1 = unsigned

bit5: Value Type
  0 = 정수(integer)
  1 = 부동소수점(float)

bit6: 확장 여부
  0 = 기본 물리량 (4워드 내에서 값까지 표현)
  1 = 확장 물리량 (추가 워드 사용)
```

#### 3.2.2 기본 물리량 (bit6 = 0)

```text
bit7..16  : 단위 종류(Unit Type) (10비트 → 최대 1024종)
bit17..64 : 값(Value) (48비트)
```

* Unit Type 예:

  * 0x000 ~ 0x0FF : SI 기본 단위 (m, s, kg, A, K, mol, cd 등)
  * 0x100 ~ …     : 파생 단위 (N, J, W, Pa 등)
  * 0x3FF         : 확장/사용자 정의 단위 예약

48비트 값 공간:

* 정수형: 약 ±1.4 × 10¹⁴ 범위
* 부동소수점형: 48비트 custom float 스펙 정의 가능 (예: 1 sign + 10 exponent + 37 mantissa 등)

#### 3.2.3 확장 물리량 (bit6 = 1)

```text
bit7..64 : 단위/메타 정보 헤더 (Unit Type 또는 별도 코드)
+ 후속 워드들에 실제 값 표현 (길이/형식은 유닛 타입에 따라 정의)
```

* 예:

  * 벡터(3D 좌표), 행렬, 3D 모델 ID, 텍스처 참조 등 복잡 물리량.
  * `Unit Type`가 “3D Position”이라면, 뒤에 x,y,z 값을 3×64비트로 붙이는 식.

---

## 4. Standard Edge (bit1=0, bit2=1)

```text
bit1 = 0
bit2 = 1 (Edge)

bit3..16 : Edge Type (14비트)
           0x0000 ~ 0x3FFE = 정규 엣지 타입
           0x3FFF          = 확장 타입 (추가 워드로 타입 정의)
bit17..64: 엣지 타입별 서브 헤더 / 플래그 / 압축 정보 등
```

* **Edge Type 예시:**

  * 0x0001 : Triple Edge (Context, Subject, Property, Object)
  * 0x0002 : Event6 Edge (6하원칙 사건)
  * 0x0003 : Keyframe Edge
  * 0x0004 : Delta Edge
  * 0x0005 : Scene Edge
  * …
* 실제 항(Ctx, Subj, Obj …) 값들은 GWMS 내부에서 **별도 MID/TID 필드**로 관리하며,
  64비트 MID 자체는 “이 엣지가 어떤 타입/성격인가”를 담는 머리 역할만 한다.

---

## 5. GEUL Extension (bit1 = 1)

Extension 영역은 **네임스페이스/기관/자유/차세대용 메타 영역**으로 사용한다.
여기서는 **bit2를 Kind로 해석하지 않는다.**

```text
bit1 = 1 (GEUL Extension)

bit2: Extension Class
  0 = 등록기관(Issuer) 네임스페이스
  1 = 자유/미래 영역
```

---

### 5.1 등록기관 네임스페이스 (bit2 = 0)

```text
bit1 = 1
bit2 = 0 (Issuer Namespace)

bit3:
  0 = 엄격 심사 Issuer
  1 = 최소 심사 Issuer
```

#### 5.1.1 엄격 심사 Issuer (bit3 = 0)

```text
bit1 = 1
bit2 = 0
bit3 = 0

bit4..16 : Issuer ID (13비트 → 최대 8192개)
bit17..64: Issuer 내부 용도 (버전, 서브도메인, 정책 등)
```

* 엄격 심사: 국제기구, 공신력 있는 재단/표준화 기구 등.
* Issuer ID 8192개면 글로벌 “공식” 기관을 커버하기에 충분.

#### 5.1.2 최소 심사 Issuer (bit3 = 1)

```text
bit1 = 1
bit2 = 0
bit3 = 1

bit4..32 : Issuer ID (29비트 → 약 5억 3천만개)
bit33..64: Issuer 내부 용도
```

* “사업체이기만 하면 등록 가능, 다만 비인도적/비정상 사용시 회수 가능” 같은 정책에 대응하는 계층.
* 전 세계 기업/단체/기관을 식별하기에 충분한 크기.

---

### 5.2 자유 / 미래 영역 (bit2 = 1)

```text
bit1 = 1
bit2 = 1

bit3:
  0 = 자유(Free) 영역
  1 = 미래(Future, Next Gen) 예약 영역
```

#### 5.2.1 자유(Free) 영역 (bit3 = 0)

```text
bit1 = 1
bit2 = 1
bit3 = 0

bit4..64 : 완전 자유
```

* GEUL Core가 해석/검증하지 않는 영역.
* 연구용, 실험용, 특정 조직 내부 전용 포맷 등, 임의 사용 가능.
* 표준과 충돌하지 않는 한에서 자유롭게 사용.

#### 5.2.2 미래(Next Generation) 영역 (bit3 = 1)

```text
bit1 = 1
bit2 = 1
bit3 = 1

bit4..64 : GEUL NEXT GENERATION 예약
```

* GEUL v2/v3 등 차세대 스펙을 위한 예약 공간.
* v1에서는 “사용 금지 / Reserved”로 두고,
  차세대 스펙이 이 영역에서 새로운 규칙을 정의하도록 남겨둔다.

---

## 6. 요약 트리

간단한 의사코드로 전체 분기를 정리하면 다음과 같다.

```pseudo
if bit1 == 0:  // GEUL Standard
    if bit2 == 0:  // Node
        if bit3 == 0:  // Entity / Verb / Context
            if bit4 == 0:  // Entity
                // Entity Node: bit5..56 = 속성, bit57..64 = 중복방지 ID
            else:  // Verb / Context
                if bit5 == 0:  // Verb
                    // Verb Node: bit6..27 = 한정사, bit28..64 = Verb ID
                else:  // Context
                    // Context Node: bit6..64 = 컨텍스트 약식 표현
        else:  // bit3 == 1: Physical
            // Physical Node:
            // bit4 = Unsigned, bit5 = ValueType, bit6 = 확장 여부
            // bit7..16 = UnitType, bit17..64 = 값(또는 헤더)
    else:  // bit2 == 1: Edge
        // Edge:
        // bit3..16 = EdgeType(14bit), bit17..64 = 서브헤더/플래그

else:  // bit1 == 1: GEUL Extension
    if bit2 == 0:  // Issuer Namespace
        if bit3 == 0:
            // Strict Issuer: bit4..16 = Issuer(13bit), bit17..64 = 내부용
        else:
            // Loose Issuer: bit4..32 = Issuer(29bit), bit33..64 = 내부용
    else:  // bit2 == 1: Free / Future
        if bit3 == 0:
            // Free: bit4..64 완전 자유
        else:
            // Next Generation: bit4..64 예약
```

---

## 7. 구현 시 유의사항

1. **비트 번호 일관성**

   * 모든 문서/코드에서 “bit1 = MSB, bit64 = LSB” 규칙을 유지한다.
   * packing/unpacking 시 endian 고려 필요(표현은 비트 위치 기준이므로 구현에서 주의).

2. **Standard vs Extension 구분**

   * Kind(노드/엣지)는 **Standard(bit1=0)** 에서만 의미 있다.
   * Extension(bit1=1)에서는 bit2를 **Extension Class** 로 해석하고, 노드/엣지 의미는 부여하지 않는다.

3. **동사 한정사와 ID의 packing 순서**

   * `bit6..27 = modifiers, bit28..64 = Verb ID` 구조를 고정하고,
   * 별도의 표로 “modifier 비트 오프셋”을 정의해두면 구현/디버깅이 쉬워진다.

4. **물리량 확장 모드**

   * `bit6=1`인 경우, 실제 값 표현은 타입별 별도 스펙을 둔다.
   * 예: UnitType=3D_POSITION이면 뒤에 x,y,z를 3×64비트로 붙이는 규칙 등.

5. **Extension 충돌 방지**

   * Issuer ID(엄격/최소) 할당은 중앙 레지스트리에서 관리한다.
   * Free 영역(bit1=1, bit2=1, bit3=0)은 충돌을 감수하는 영역이라는 점을 명시한다.

---

이 문서는 **64비트 GEUL Word/MID의 상위 비트 구조**에 대한 고정 스펙이다.
구체적인 “속성 비트 매핑(예: Entity bit5..56, Context bit6..64 내부 구조)”은 별도의 세부 명세서로 분리해 관리할 수 있다.