# GEUL 비트 명세서 (GEUL Bit Layout Specification)

- 문서명: GEUL 비트명세.md  
- 버전: **v0.2**  
- 단위: 64비트 GEUL Word (SIDX/TID용 의미정렬 ID)  
- 비트 번호 규칙:  
  - **bit1 = 최상위(MSB)**  
  - **bit64 = 최하위(LSB)**

> 본 문서는 v0.1 구조를 바탕으로,  
> **‘표준 제안(Standard Proposal)’ 레인을 Issuer Namespace가 아닌 자유(Free) 영역에 배치**하는 개정안을 정의한다.  
> 사용자는 **표준 제안 노드/엣지의 상위 4비트가 `1100`으로 시작**하도록 생성하며,  
> **bit4부터는 GEUL Standard와 동일한 구조로 해석**한다.  
> (즉, Proposal은 “표준과 동일한 형태의 실험/후보 트랙”이다.) :contentReference[oaicite:0]{index=0}

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

bit5..32  : 속성 약식 표현 비트 (28비트)
bit33..64 : 중복방지용 로컬 ID (32비트)
```

#### 3.1.2 동사 노드 (Verb Node)

```text
bit1 = 0
bit2 = 0 (Node)
bit3 = 0
bit4 = 1
bit5 = 0 (Verb)

bit6..27  : 동사 의미 한정사(modifiers)
bit28..64 : Verb ID
```

#### 3.1.3 컨텍스트 노드 (Context Node)

```text
bit1 = 0
bit2 = 0 (Node)
bit3 = 0
bit4 = 1
bit5 = 1 (Context)

bit6..64 : 컨텍스트 약식 표현 비트 (59비트)
```

---

### 3.2 물리량 노드 (bit3 = 1)

```text
bit1 = 0
bit2 = 0 (Node)
bit3 = 1 (물리량)

bit4: Unsigned 플래그
bit5: Value Type
bit6: 확장 여부
bit7..16 : Unit Type
bit17..64: 값/헤더 (타입별 스펙)
```

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

## 5.1 등록기관 네임스페이스 (bit2 = 0)

> v0.2에서는 Issuer Namespace 내부 비트 구조를
> v0.1 해석(엄격/최소 심사 분기)과 **동일하게 유지**한다.
> ‘표준 제안’ 레인은 **Issuer가 아니라 자유 영역에서 제공**한다.

```text
bit1 = 1
bit2 = 0 (Issuer Namespace)

bit3:
  0 = 엄격 심사 Issuer
  1 = 최소 심사 Issuer
```

### 5.1.1 엄격 심사 Issuer (bit3 = 0)

```text
bit1 = 1
bit2 = 0
bit3 = 0

bit4..16 : Issuer ID (13비트 → 최대 8192개)
bit17..64: Issuer 내부 용도
```

### 5.1.2 최소 심사 Issuer (bit3 = 1)

```text
bit1 = 1
bit2 = 0
bit3 = 1

bit4..32 : Issuer ID (29비트 → 약 5억 3천만개)
bit33..64: Issuer 내부 용도
```

---

## 5.2 자유 / 미래 영역 (bit2 = 1)

```text
bit1 = 1
bit2 = 1

bit3:
  0 = 자유(Free) 영역
  1 = 미래(Future, Next Gen) 예약 영역
```

---

## 5.2.1 자유(Free) 영역 (bit3 = 0)

### 5.2.1.1 일반 자유 영역

```text
bit1 = 1
bit2 = 1
bit3 = 0

bit4:
  0 = 표준 제안(Standard Proposal) 레인
  1 = 일반 자유(Free) 레인
```

> **이 문서의 핵심 개정 사항**은
> 자유 영역 내부에 1비트를 추가하여
> **표준 제안 레인을 별도로 정의**하는 것이다.
> 따라서 **표준 제안 노드/엣지는 상위 4비트가 `1100`으로 시작한다.**

---

### 5.2.1.2 표준 제안(Standard Proposal) 레인

```text
bit1 = 1
bit2 = 1
bit3 = 0
bit4 = 0  // Standard Proposal

bit5..64 : "GEUL Standard와 동일한 구조로 해석"
          (단, 상위 비트의 구분만 Extension Proposal임)
```

#### 해석 규칙(중요)

* **bit5부터는 표준과 동일한 문법을 사용**한다.
* 즉, Proposal 레인 내부에서의 “Kind/Node/Edge/세부 하위 분기”는
  **Standard와 1:1로 매핑되는 가상-표준 트랙**이다.

이를 명시적으로 표현하면:

```text
[Proposal Prefix]
  1100

[Standard Mirror]
  bit5.. = (Standard의 bit2..에 대응)
```

##### 예시 1) 표준 제안 노드

* Prefix: `1100`
* 이후(비트5부터) 표준 Node 문법을 그대로 사용

> 해석상 “표준 제안 노드”는
> **‘표준과 같은 구조를 갖지만 아직 표준이 아닌 후보 ID’**이다.

##### 예시 2) 표준 제안 엣지

* Prefix: `1100`
* 이후(비트5부터) 표준 Edge 문법을 그대로 사용

---

### 5.2.1.3 일반 자유(Free) 레인

```text
bit1 = 1
bit2 = 1
bit3 = 0
bit4 = 1  // General Free

bit5..64 : 완전 자유
```

* GEUL Core가 해석/검증하지 않는 영역.
* 연구용, 실험용, 조직 내부 전용 포맷 등 임의 사용 가능.

---

## 5.2.2 미래(Next Generation) 영역 (bit3 = 1)

```text
bit1 = 1
bit2 = 1
bit3 = 1

bit4..64 : GEUL NEXT GENERATION 예약
```

---

## 6. 요약 트리 (v0.2)

```pseudo
if bit1 == 0:  // GEUL Standard
    if bit2 == 0:  // Node
        // Standard Node 규칙
    else:
        // Standard Edge 규칙

else:  // bit1 == 1: GEUL Extension
    if bit2 == 0:  // Issuer Namespace
        if bit3 == 0:
            // Strict Issuer
        else:
            // Loose Issuer

    else:  // bit2 == 1: Free/Future
        if bit3 == 1:
            // Next Generation (Reserved)
        else:  // bit3 == 0: Free
            if bit4 == 0:
                // Standard Proposal Lane
                // bit5.. = Standard grammar mirror
            else:
                // General Free Lane
                // bit5..64 free
```

---

## 7. 설계 의도 및 효과

### 7.1 왜 Issuer가 아니라 Free에 두는가

* 표준 후보의 상위 문법을
  특정 기관 네임스페이스와 묶지 않고
  **“공개 표준 후보의 공용 레인”**으로 제공하기 위함.
* 표준화 과정에서
  “기관 권위”보다
  “공개 제안/공개 검증”의 경로를 우선할 수 있다.

### 7.2 ‘표준과 동일 구조’의 의미

* Proposal 레인은
  **표준의 미래 버전 호환성을 테스트하는 샌드박스**다.
* 표준 채택 전까지는

  * 충돌 가능성을 인정하고
  * 레지스트리/커뮤니티 합의로

    * 채택/수정/반려를 관리한다.

---

## 8. 구현 시 유의사항

1. **파서 분기**

* `1100` Prefix를 만나면
  **“Proposal Standard Mirror”**로 해석해야 한다.

2. **정전적 채택 금지**

* Proposal은 어디까지나 후보 상태다.
* WMS/도메인 엔진은

  * Proposal을 기본적으로 “선택적/실험적” 의미로 다루고,
  * 채택 여부는 레지스트리 정책에 따르도록 구현한다.

3. **문서/레지스트리 동반**

* Proposal의 의미소/타입 정의는
  **정의 문서 + 테스트 벡터 + 충돌/대안 기술**을 권장한다.

---

## 9. 결론

v0.2는 다음을 달성한다.

* **표준 후보 레인을 개인/기관 임의 영역에서 분리**
* **`1100` Prefix로 시작하는 ‘표준 제안’ 트랙 제공**
* **bit4(Proposal 레인 구분) 이후는 표준 문법을 그대로 미러링**

따라서 GEUL은

* “닫힌 개인 규격”이 아니라
* **공개 표준 후보의 실험 구역을 구조적으로 보장하는 언어**로 전진한다. 