# **연결 글오 (Connection GEUL-O)**

## 1\. 정의 (Definition)

\*\*`연결 글오(Connection GEUL-O)`\*\*는 GEUL 아키텍처에서 **'문단(Paragraph)'의 논리적 뼈대**를 구성하는 핵심 객체입니다. `서술 글오`(문장)들이 개별적인 사실을 나타낸다면, `연결 글오`는 이 문장들을 모아 인과, 조건, 순차, 역접 등 다양한 논리적 관계로 엮어주는 역할을 합니다.

`연결 글오`는 GEUL이 단순한 사실의 나열을 넘어, 복잡한 논증, 절차적 지시, 인과 관계 추론 등 고차원적인 의미를 표현할 수 있게 하는 중심축입니다.

## 2\. 핵심 철학

  * **논리의 개체화 (First-class Citizen of Logic)**: `연결 글오`는 `서술 글오` 사이의 관계를 단순한 속성이 아닌, 그 자체로 고유한 정체성을 가진 \*\*'독립된 개체'\*\*로 취급합니다. 이를 통해 관계 자체에 대한 메타데이터(신뢰도, 출처 등)를 부여하고, 관계를 중심으로 한 쿼리 및 추론이 가능해집니다.

  * **의미의 자기 명시 (Self-descriptive Semantics)**: `연결 글오`는 자신의 성격과 목적을 스스로 명시합니다. `연결 타입(ConnectionType)`이라는 핵심 `글소`를 통해, 자신이 세상의 사실 관계를 \*\*기술(Descriptive)\*\*하는지, 아니면 에이전트의 행동을 \*\*지시(Prescriptive)\*\*하는지를 명확히 구분합니다. 이는 시스템이 '알고 있는 것'과 '해야 할 일'을 혼동하지 않도록 보장하는 결정적인 설계 원칙입니다.

## 3\. 구조: 논리의 청사진 (Blueprint of Logic)

`연결 글오`는 논리적 주장을 구성하기 위한 명확한 구조를 가집니다.

### 3.1. 핵심 구성 글소 (Core GEUL-SO Packets)

| 글소(GEUL-SO) 이름 | 핵심 역할 | 바디(Body) 내용 | 비고 |
| :--- | :--- | :--- | :--- |
| **연결 타입**\<br\>(ConnectionType) | 이 연결의 핵심 논리(성격)를 정의합니다. | `인과관계`, `규칙`, `정의`, `순차`, `역접` 등 추상 개념을 가리키는 **벡터 식별자**. | 이 `글소`가 `연결 글오`의 성격을 결정합니다. |
| **전제 목록**\<br\>(PremiseList) | 논리적 연결의 입력/원인/조건이 되는 `서술 글오`들을 지정합니다. | `서술 글오`들을 가리키는 **벡터 식별자 리스트**. | IF / BECAUSE 절에 해당합니다. |
| **결론 목록**\<br\>(ConclusionList) | 논리적 연결의 출력/결과/행동이 되는 `서술 글오`들을 지정합니다. | `서술 글오`들을 가리키는 **벡터 식별자 리스트**. | THEN / THEREFORE 절에 해당합니다. |
| **메타데이터**\<br\>(Metadata) | 이 논리 연결 자체의 부가 정보를 담습니다. | `신뢰도`, `출처`, `타임스탬프` 등 메타 정보 패킷의 집합입니다. | `서술 글오`의 신뢰도와는 별개입니다. |

### 3.2. 연결 타입(ConnectionType)의 종류

`연결 타입`은 크게 두 가지 범주로 나뉩니다.

#### **A. 기술적(Descriptive) 연결 타입**

세상의 사실 관계나 논리적 관계를 서술합니다. (이전의 `접속 글오` 역할)

  * **`인과관계(Causality)_ID`**: 원인과 결과의 관계를 나타냅니다.
  * **`정의(Definition)_ID`**: 어떤 개념을 다른 개념으로 정의하는 관계를 나타냅니다.
  * **`순차(Sequence)_ID`**: 시간적 또는 논리적 순서를 나타냅니다.
  * **`역접(Contrast)_ID`**: 두 서술이 서로 대조되는 관계임을 나타냅니다.

#### **B. 규범적(Prescriptive) 연결 타입**

에이전트(GAT, GEUL-Agent)가 따라야 할 행동이나 절차를 지시합니다. (이전의 `제어 글오` 역할)

  * **`규칙(Rule)_ID`**: "IF-THEN" 형식의 조건부 행동 규칙을 나타냅니다.
  * **`절차(Procedure)_ID`**: 순서가 있는 단계별 행동 지침을 나타냅니다.

## 4\. 종합 예시

### 예시 1: 뉴스 기사의 인과관계 (기술적 연결)

```yaml
ObjectID: Connection_Causality_001_ID
GEUL_O_Type: Connection_GEUL-O

Packets:
  - ConnectionType: "인과관계(Causality)_ID"
  - PremiseList: [ "Statement_ItRained_ID" ]
  - ConclusionList: [ "Statement_RoadSlippery_ID" ]
  - Metadata:
      - Confidence: 0.9
      - Source: "NewsArticle_456_ID"
```

### 예시 2: 시스템의 작동 규칙 (규범적 연결)

```yaml
ObjectID: Connection_Rule_PowerSave_ID
GEUL_O_Type: Connection_GEUL-O

Packets:
  - ConnectionType: "규칙(Rule)_ID"
  - PremiseList: [ "Statement_BatteryLow_ID" ]
  - ConclusionList: [ "Statement_ActivatePowerSave_ID" ]
  - Metadata:
      - Source: "System_Specification_Doc_ID"
```

## 5\. 아키텍처 내에서의 역할

`연결 글오`는 `문서 글오(Document GEUL-O)`의 `내용 목록(ContentList)`에 포함되어, 해당 문서의 논리적 구조를 형성하는 핵심적인 역할을 수행합니다. 이를 통해 GEUL은 단순한 데이터의 집합을 넘어, 진정한 의미의 '지식'과 '논리'를 표현하는 언어로 거듭나게 됩니다.