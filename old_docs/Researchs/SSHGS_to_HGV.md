## SSHGS to HGV 변환 파이프라인: PyG HGTConv 활용 가이드

이 문서는 GEUL 아키텍처의 파일럿 구현체인 \*\*SSHGS(의미 중첩 이종 그래프)\*\*를 입력받아, 최종 추론 엔진(GAT/GPT)을 위한 \*\*2880차원의 HGV(Heterogeneous Graph Vector)\*\*를 생성하는 전체 과정을 기술합니다. 이 파이프라인의 핵심은 PyTorch Geometric(PyG)의 `HGTConv` 레이어를 활용하여, 그래프의 구조적/의미적 정보를 고차원 벡터 공간으로 손실 없이 압축하는 것입니다.

이 과정은 GEUL의 핵심 철학인 \*\*'분업화된 지능(Division of Intelligence)'\*\*을 구현합니다. HGT는 복잡한 그래프를 분석하는 **'의미 구조 분석 전문가'** 역할을 수행하여, 최종 추론기가 더 높은 수준의 '생각'에만 집중할 수 있도록 최고급으로 손질된 지식 재료(HGV)를 제공합니다.

-----

### 1단계: SSHGS 입력 및 파싱 (YAML → `HeteroData`)

모든 과정은 인간이 읽을 수 있는 **SSHGS YAML** 포맷(개발 및 디버깅용) 또는 기계에 최적화된 **SSHG 바이트 스트림**(운영용)을 입력받는 것에서 시작합니다.

\*\*GEUL 파서(Parser)\*\*는 이 입력 데이터를 PyTorch Geometric이 즉시 사용할 수 있는 **`HeteroData` 객체**로 변환합니다.

  * **역할**: 파서는 YAML 또는 바이트 스트림의 노드, 엣지, 속성을 읽어, PyG의 표준 그래프 자료구조로 변환합니다.
  * **프로세스**:
    1.  YAML의 `nodes` 리스트를 순회하며 노드 타입(`Concept`, `Pronoun` 등)별로 그룹화합니다.
    2.  YAML의 `edges` 리스트를 순회하며 엣지 타입(`['Pronoun', 'nsubj', 'Concept']` 등)별로 출발-도착 노드 인덱스를 정리합니다.
    3.  의미 중첩을 표현하는 `probability`, `confidence` 같은 엣지 속성을 `edge_attr`로 저장합니다.

**구현 예시:**

```python
import torch
from torch_geometric.data import HeteroData
import yaml

# SSHG YAML 데이터를 불러옵니다.
ss transcriptome_yaml = """
SSHG_Object:
  # ... (이전 예시와 동일한 YAML 내용) ...
"""

# YAML 파싱
data_yaml = yaml.safe_load(ss transcriptome_yaml)['SSHG_Object']
data = HeteroData()

# 노드 ID를 내부 인덱스로 매핑
node_mapping = {node['id']: i for i, node in enumerate(data_yaml['nodes'])}

# 노드 타입별 그룹화 (x는 초기 특징 벡터)
for n_type in {'Pronoun', 'Concept', 'Determiner', 'Relationship'}:
    nodes_of_type = [node for node in data_yaml['nodes'] if node['type'] == n_type]
    data[n_type].x = torch.randn(len(nodes_of_type), 128) # 예시: 128차원 초기 벡터

# 엣지 타입별 그룹화
for edge in data_yaml['edges']:
    e_type = tuple(edge['relation_type'])
    source_idx = node_mapping[edge['source']]
    target_idx = node_mapping[edge['target']]
    
    # edge_index에 추가
    if e_type not in data:
        data[e_type].edge_index = torch.tensor([[source_idx], [target_idx]])
    else:
        # ... (기존 엣지에 연결 정보 추가) ...

    # 엣지 속성 추가
    if 'attributes' in edge:
        attrs = edge['attributes']
        # ... (edge_attr에 확률, 확신도 정보 추가) ...
```

-----

### 2단계: HGT 모델 아키텍처 정의 (2880차원 HGV 출력)

`HeteroData` 객체를 입력받아 2880차원의 HGV를 출력하는 HGT 모델을 PyG를 사용하여 설계합니다. 이 모델은 \*\*자기지도학습(링크 예측)\*\*을 통해 SSHGS의 구조적 문법을 미리 학습한 상태여야 합니다.

  * **핵심 컴포넌트**: `HGTConv` 레이어
  * **아키텍처**:
    1.  여러 개의 `HGTConv` 레이어를 순차적으로 쌓아, 그래프의 지역적/전역적 정보를 점진적으로 학습합니다.
    2.  **마지막 `HGTConv` 레이어**의 `out_channels` 파라미터를 **2880**으로 설정하여 최종 출력 벡터의 차원을 지정합니다.

**구현 예시:**

```python
from torch_geometric.nn import HGTConv, Linear

class SSHG_Processor(torch.nn.Module):
    def __init__(self, hidden_channels, num_heads, metadata):
        super().__init__()
        
        # 첫 번째 레이어: 초기 특징 벡터를 hidden_channels로 변환
        self.conv1 = HGTConv(-1, hidden_channels, metadata, heads=num_heads)
        
        # 두 번째 레이어: 그래프 문맥을 더 깊이 학습
        self.conv2 = HGTConv(hidden_channels, hidden_channels, metadata, heads=num_heads)
        
        # 최종 출력 레이어: HGV를 2880차원으로 변환
        self.final_conv = HGTConv(hidden_channels, 2880, metadata, heads=1)

    def forward(self, x_dict, edge_index_dict):
        # HGT 레이어를 순차적으로 통과
        x_dict = self.conv1(x_dict, edge_index_dict).relu()
        x_dict = self.conv2(x_dict, edge_index_dict).relu()
        
        # 최종 2880차원 HGV 출력
        hgv_dict = self.final_conv(x_dict, edge_index_dict)
        
        return hgv_dict

# 모델 초기화
# metadata는 HeteroData 객체로부터 얻은 노드 타입과 엣지 타입 정보입니다.
# metadata = (['Pronoun', 'Concept', ...], [('Pronoun', 'nsubj', 'Concept'), ...])
model = SSHG_Processor(hidden_channels=768, num_heads=8, metadata=data.metadata())
```

-----

### 3단계: HGV 생성 실행

정의된 파서와 모델을 사용하여 최종 HGV를 생성합니다.

1.  SSHGS YAML(또는 스트림)을 `HeteroData` 객체로 파싱합니다.
2.  `HeteroData` 객체를 미리 훈련된 HGT 모델에 입력으로 전달합니다.
3.  모델은 각 노드 타입에 대한 2880차원의 HGV 벡터 묶음을 딕셔너리 형태로 출력합니다.

**실행 예시:**

```python
# 1단계에서 파싱한 'data' 객체를 사용
x_dict = {node_type: data[node_type].x for node_type in data.node_types}
edge_index_dict = {edge_type: data[edge_type].edge_index for edge_type in data.edge_types}

# 훈련된 모델을 사용하여 HGV 생성
with torch.no_grad():
    hgv_output_dict = model(x_dict, edge_index_dict)

# 결과 확인
print(hgv_output_dict)
```

**출력 결과:**

```
{
  'Pronoun': tensor([[...], ...]),      # [num_pronoun_nodes, 2880] 크기의 텐서
  'Concept': tensor([[...], ...]),      # [num_concept_nodes, 2880] 크기의 텐서
  'Determiner': tensor([[...], ...]),   # [num_determiner_nodes, 2880] 크기의 텐서
  'Relationship': tensor([[...], ...]) # [num_relationship_nodes, 2880] 크기의 텐서
}
```

이 출력된 `hgv_output_dict`의 벡터들이 바로 **최종 추론 엔진(GAT/GPT)의 입력으로 사용될, 문장의 모든 구조와 의미가 응축된 HGV**입니다. 이 벡터 시퀀스를 GPT에 입력하면, 모델은 문법 분석과 같은 저수준 작업을 생략하고 곧바로 고차원적인 추론 및 생성 작업을 시작할 수 있습니다.