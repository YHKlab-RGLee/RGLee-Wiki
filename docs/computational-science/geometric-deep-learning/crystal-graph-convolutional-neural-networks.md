---
title: "1.2. Geometric deep learning: Crystal graph convolutional neural networks"
description: CGCNN의 주기 결정 그래프, gated convolution, pooling, PyTorch 구현과 재현 규약을 설명
status: verified
last_verified: 2026-08-13
---

# 1.2. Geometric deep learning: Crystal graph convolutional neural networks

Crystal graph convolutional neural network (CGCNN)는 결정 구조를 주기 multigraph로 바꾸고, 원자와 결합 feature에서 결정 물성을 학습하는 message-passing architecture이다. 일반적인 node·edge·aggregation 표기는 [Graph neural networks](graph-neural-networks.md)를 따른다. 이 글은 CGCNN에 고유한 결정 그래프, gated convolution, pooling과 구현 계약을 분리해 설명한다.[1,2]

CGCNN의 핵심은 원자 $i$, 이웃 원자 $j$와 둘 사이의 bond feature를 결합한 뒤, sigmoid gate와 nonlinear content의 원소별 곱을 이웃에 대해 합하는 것이다. 원 논문의 공개 구현도 이 연산을 `ConvLayer`로 구현하고, 여러 층 뒤의 원자 feature를 결정별로 평균하여 property decoder에 전달한다.[1,3,4]

## 1. 결정 그래프와 입력 feature

### (1) 주기 multigraph

기준 cell의 원자를 node로 두고, 원자 $j$의 lattice image에서 원자 $i$로 향하는 연결을 directed edge $(j,\mathbf n)\to i$로 나타낸다. 기준 cell의 Cartesian 좌표를 $\mathbf r_i$, lattice matrix를 $L$, image shift를 $\mathbf n\in\mathbb Z^3$라 하면 변위와 거리는

$$
\mathbf d_{ij\mathbf n}
=\mathbf r_j+L\mathbf n-\mathbf r_i,
\qquad
r_{ij\mathbf n}=\|\mathbf d_{ij\mathbf n}\|_2
$$

이다. 같은 $i$와 $j$라도 서로 다른 $\mathbf n$이 이웃 목록에 들어오면 edge가 여러 개 생긴다. CGCNN이 단순 그래프가 아니라 multigraph를 사용하는 이유는 이 periodic image의 구분을 보존하기 위해서이다.[1,2]

이웃 규칙이 거리 cutoff $r_c$라면 edge multiset을

$$
E=
\left\{
(j,\mathbf n)\to i:
0<r_{ij\mathbf n}\le r_c
\right\}
$$

로 정의할 수 있다. 원 공개 구현은 고정된 최대 이웃 수를 가진 dense tensor를 사용하며, 후속 분석은 원형 CGCNN의 12-nearest-neighbor 선택이 결정에 따라 서로 다른 coordination shell을 섞을 수 있음을 지적한다.[3,4] 따라서 `CGCNN`이라는 이름만 기록해서는 그래프 입력을 재현할 수 없고 cutoff, 최대 이웃 수, periodic image와 동률 거리 처리까지 함께 고정해야 한다.[2,3]

### (2) 원자와 bond feature

초기 원자 feature $\mathbf x_i$는 원소 종류를 표현하는 vector이고, encoder가 hidden state를

$$
\mathbf h_i^{(0)}
=W_{\mathrm{emb}}\mathbf x_i+\mathbf b_{\mathrm{emb}}
$$

로 만든다. Bond feature는 원자 사이 거리 $r_{ij\mathbf n}$를 Gaussian basis로 펼쳐 구성할 수 있다.[1,2]

$$
e_{ij\mathbf n,q}
=
\exp\!\left[
-\gamma
\left(r_{ij\mathbf n}-\mu_q\right)^2
\right],
\qquad q=1,\ldots,Q
$$

$\mu_q$는 basis center, $\gamma$는 폭을 정하는 양수이다. 거리만 사용하는 bond feature는 전역 병진·회전에 invariant이지만, 결합각과 방향은 명시적으로 보존하지 않는다. 여러 convolution을 쌓으면 이웃을 통한 간접적인 many-body 문맥은 생길 수 있으나, 한 층의 message에는 pairwise 입력만 직접 들어간다.[1–3]

입력 tensor의 최소 계약은 다음과 같다.

| 기호 또는 코드 | shape | 의미 |
| --- | --- | --- |
| `atom_features` | $[N,F_a]$ | batch 전체의 원자 hidden feature |
| `neighbor_features` | $[N,M,F_b]$ | 각 원자의 $M$개 bond feature |
| `neighbor_indices` | $[N,M]$ | 각 receiver 원자에 대응하는 sender index |
| $N$ | scalar | batch에 포함된 전체 원자 수 |
| $M$ | scalar | padding을 포함한 원자당 최대 이웃 수 |

### (3) 거리 basis와 이웃 tensor

`neighbor_indices[i, k]`와 `neighbor_features[i, k]`는 동일한 periodic edge를 가리켜야 한다. 이웃 탐색기가 $(j,\mathbf n)$을 반환하면 sender index $j$는 `neighbor_indices`에, 거리 $r_{ij\mathbf n}$의 basis vector는 같은 위치의 `neighbor_features`에 둔다. 서로 다른 $\mathbf n$이 같은 $i,j$를 연결하더라도 두 항을 합치거나 제거하지 않는다. 두 periodic image는 sender index가 같아도 거리와 변위가 다른 별도 edge이기 때문이다.[1–3]

균일한 Gaussian center는 거리 구간 $[r_{\min},r_{\max}]$에서

$$
\mu_q=r_{\min}+q\,\Delta r,
\qquad
\Delta r=\frac{r_{\max}-r_{\min}}{Q-1},
\qquad q=0,\ldots,Q-1
$$

로 만들 수 있다. 다음 함수는 이미 계산된 distance tensor의 마지막 축에 $Q$개 basis channel을 추가한다. 이 연산은 neighbor list를 만들지 않으므로 lattice, periodic boundary condition과 cutoff 처리는 앞 단계의 구조 parser가 책임진다.[1,2,4]

```python
import torch


def gaussian_distance(
    distances: torch.Tensor,
    start: float,
    stop: float,
    step: float,
) -> torch.Tensor:
    centers = torch.arange(
        start,
        stop + 0.5 * step,
        step,
        device=distances.device,
        dtype=distances.dtype,
    )
    width = step
    return torch.exp(-((distances[..., None] - centers) / width) ** 2)


distances = torch.tensor([[1.8, 2.1], [2.4, 2.7]])
bond_features = gaussian_distance(
    distances,
    start=0.0,
    stop=5.0,
    step=0.5,
)

assert bond_features.shape == (2, 2, 11)
```

이웃 수가 원자마다 다르면 `[N,M]` tensor로 맞추기 위해 padding이 필요하다. Padding edge를 실제 원자 index `0`으로만 채우고 mask 없이 합산하면 가짜 message가 생긴다. 안전한 구현은 유효 edge만 flat edge list로 보관하거나, `neighbor_mask`를 gate–content 곱에 적용한 뒤 합산한다. 원 공개 코드의 고정 이웃 tensor를 다른 이웃 규칙에 재사용할 때 이 padding 계약을 명시적으로 다시 설계해야 한다.[2–4]

## 2. Gated crystal convolution

### (1) Gate와 content

$t$번째 층에서 receiver $i$, sender $j$와 $k$번째 periodic bond의 결합 vector를

$$
\mathbf z_{(i,j)_k}^{(t)}
=
\mathbf h_i^{(t)}
\mathbin\Vert
\mathbf h_j^{(t)}
\mathbin\Vert
\mathbf e_{(i,j)_k}
$$

로 정의한다. $\Vert$는 마지막 feature 축의 concatenation이다. 한 선형 변환을 $2F_a$개 channel로 만든 뒤 절반은 gate logit, 나머지 절반은 content logit으로 나눌 수 있다.[1,3,4]

$$
\mathbf a_{(i,j)_k}^{(t)}
=W_f^{(t)}\mathbf z_{(i,j)_k}^{(t)}+\mathbf b_f^{(t)}
$$

$$
\mathbf c_{(i,j)_k}^{(t)}
=W_s^{(t)}\mathbf z_{(i,j)_k}^{(t)}+\mathbf b_s^{(t)}
$$

Gate와 content를 각각 sigmoid와 softplus로 변환하면 edge message는

$$
\mathbf m_{(i,j)_k}^{(t+1)}
=
\sigma\!\left(\mathbf a_{(i,j)_k}^{(t)}\right)
\odot
\operatorname{softplus}\!\left(\mathbf c_{(i,j)_k}^{(t)}\right)
$$

이다. $\odot$는 원소별 곱이다. Receiver $i$의 모든 periodic edge를 합해

$$
\overline{\mathbf m}_i^{(t+1)}
=\sum_{j,k}\mathbf m_{(i,j)_k}^{(t+1)}
$$

를 만들고 residual update를

$$
\mathbf h_i^{(t+1)}
=
\operatorname{softplus}\!\left(
\mathbf h_i^{(t)}
+\overline{\mathbf m}_i^{(t+1)}
\right)
$$

로 적용한다. 원 공개 구현은 선형 변환 뒤와 이웃 합 뒤에 batch normalization을 추가한다. 이 normalization은 CGCNN의 학습 구현에 포함되지만, gate–content 곱과 residual 합이라는 message-passing 구조 자체와는 구분해야 한다.[1,3,4]

### (2) PyTorch 핵심 구현

다음 코드는 원 공개 구현의 tensor 계약과 gated convolution을 현대적인 PyTorch 표기로 축약한 예제이다. Padding 이웃은 이미 유효한 index와 feature로 정리되었다고 가정한다. 실제 dataset loader에서는 padding mask를 두거나, 모든 원자가 정확히 $M$개 이웃을 갖도록 생성 규약을 고정해야 한다.[1,3,4]

```bash
python -m pip install torch
```

```python
import torch
from torch import nn


class CGCNNLayer(nn.Module):
    def __init__(self, atom_channels: int, bond_channels: int):
        super().__init__()
        input_channels = 2 * atom_channels + bond_channels
        self.atom_channels = atom_channels
        self.gated_linear = nn.Linear(input_channels, 2 * atom_channels)
        self.edge_norm = nn.BatchNorm1d(2 * atom_channels)
        self.message_norm = nn.BatchNorm1d(atom_channels)
        self.softplus = nn.Softplus()

    def forward(
        self,
        atom_features: torch.Tensor,
        neighbor_features: torch.Tensor,
        neighbor_indices: torch.Tensor,
    ) -> torch.Tensor:
        num_atoms, max_neighbors = neighbor_indices.shape
        neighbor_atoms = atom_features[neighbor_indices]
        center_atoms = atom_features[:, None, :].expand(
            num_atoms,
            max_neighbors,
            self.atom_channels,
        )

        edge_input = torch.cat(
            [center_atoms, neighbor_atoms, neighbor_features],
            dim=-1,
        )
        gated = self.gated_linear(edge_input)
        gated = self.edge_norm(gated.flatten(0, 1)).view(
            num_atoms,
            max_neighbors,
            2 * self.atom_channels,
        )

        gate_logits, content_logits = gated.chunk(2, dim=-1)
        messages = torch.sigmoid(gate_logits) * self.softplus(content_logits)
        aggregated = self.message_norm(messages.sum(dim=1))
        return self.softplus(atom_features + aggregated)


num_atoms, max_neighbors = 5, 4
atom_channels, bond_channels = 16, 8

atom_features = torch.randn(num_atoms, atom_channels)
neighbor_features = torch.randn(num_atoms, max_neighbors, bond_channels)
neighbor_indices = torch.randint(
    low=0,
    high=num_atoms,
    size=(num_atoms, max_neighbors),
)

layer = CGCNNLayer(atom_channels, bond_channels)
updated_atoms = layer(atom_features, neighbor_features, neighbor_indices)

assert updated_atoms.shape == atom_features.shape
```

코드에서 `neighbor_atoms`는 $\mathbf h_j^{(t)}$, `center_atoms`는 $\mathbf h_i^{(t)}$, `neighbor_features`는 $\mathbf e_{(i,j)_k}$에 대응한다. `chunk(2)` 뒤의 두 tensor가 gate와 content이고, `sum(dim=1)`이 같은 receiver에 연결된 $M$개 message의 합이다. 원자 index를 함께 재배열하고 `neighbor_indices`도 같은 permutation으로 변환하면 출력도 같은 순서로 재배열되어야 한다.[1,2,4]

## 3. Pooling과 property decoder

### (1) 결정 표현

$R$개의 convolution 뒤 원자 state를 결정 단위로 모아야 한다. 한 결정 $C_b$에 속한 원자 index 집합을 $I_b$라 하면 mean pooling은

$$
\mathbf h_{C_b}^{\mathrm{mean}}
=
\frac{1}{|I_b|}
\sum_{i\in I_b}\mathbf h_i^{(R)}
$$

이다. 반면 sum pooling은

$$
\mathbf h_{C_b}^{\mathrm{sum}}
=
\sum_{i\in I_b}\mathbf h_i^{(R)}
$$

로 계의 크기에 따라 변한다. 원 공개 구현은 결정별 평균을 사용한다.[1,4] 평균은 unit cell을 단순 복제했을 때 같은 국소 환경의 반복 수를 제거하지만, 총에너지처럼 extensive한 목표에는 원자별 기여의 합이나 명시적인 크기 정보가 더 자연스러울 수 있다. Pooling과 목표의 원자당·cell당 정규화를 함께 보고해야 하는 이유이다.[2,5]

Decoder $D_C$가 결정 표현을 scalar property로 보내면

$$
\widehat y_b=D_C\!\left(\mathbf h_{C_b}\right)
$$

이고, 회귀 학습의 mean squared error는

$$
\mathcal L_{\mathrm{MSE}}
=
\frac{1}{B}
\sum_{b=1}^{B}
\left(\widehat y_b-y_b\right)^2
$$

이다. $B$는 batch의 결정 수이다. 이 손실은 목표가 정규화된 방식과 단위를 스스로 정하지 않으므로 dataset의 label 계약이 별도로 필요하다.[1,2]

목표값을 표준화할 때에는 train split에서만 평균과 표준편차를 구하고, validation·test에는 같은 변환을 적용한다. 전체 dataset에서 통계량을 먼저 계산하면 test label의 분포가 학습 절차에 들어가는 자료 누출이 생긴다. 예측을 원래 단위로 되돌린 뒤 MAE와 RMSE를 계산해야 서로 다른 표준화 규약의 결과를 비교할 수 있다. Formation energy처럼 원자당 단위로 학습한 값과 cell total을 섞지 말고, 구조 파일의 원자 수와 label 정규화가 일치하는지도 batch마다 확인해야 한다.[1,2,5]

여러 결정을 하나의 batch로 합칠 때 convolution은 `neighbor_indices`가 batch 전체의 원자 index를 가리키도록 offset을 적용해야 한다. 결정 $b$의 local index를 그대로 연결하면 서로 다른 결정의 원자 사이에 가짜 edge가 생길 수 있다. 반대로 pooling은 `crystal_index`를 사용해 결정 경계를 복원해야 한다. 즉 convolution 단계의 edge offset과 pooling 단계의 graph assignment는 하나의 batch 계약으로 함께 시험해야 한다.[2,4,5]

### (2) Batch별 pooling 코드

다음 함수는 각 원자가 어느 결정에 속하는지를 나타내는 `crystal_index`를 사용해 mean pooling을 수행한다. `index_add_`는 원자 feature의 합을 만들고 `bincount`는 결정별 원자 수를 계산한다.

```python
def mean_pool_crystals(
    atom_features: torch.Tensor,
    crystal_index: torch.Tensor,
) -> torch.Tensor:
    num_crystals = int(crystal_index.max().item()) + 1
    pooled = atom_features.new_zeros((num_crystals, atom_features.shape[1]))
    pooled.index_add_(0, crystal_index, atom_features)

    counts = torch.bincount(
        crystal_index,
        minlength=num_crystals,
    ).to(atom_features.dtype)
    return pooled / counts[:, None].clamp_min(1)


crystal_index = torch.tensor([0, 0, 1, 1, 1], dtype=torch.long)
crystal_features = mean_pool_crystals(updated_atoms, crystal_index)

assert crystal_features.shape == (2, atom_channels)
```

## 4. 검증과 재현 규약

### (1) 구조적 불변성 검사

CGCNN의 scalar node feature는 좌표 회전에 따라 값이 변하지 않는 거리 feature를 사용한다. 따라서 구현에서 먼저 검사할 구조적 조건은 node relabeling에 대한 equivariance와 pooling 뒤의 permutation invariance이다.[1,2]

$$
F(PH,PE)=P\,F(H,E),
\qquad
R(PH)=R(H)
$$

$P$는 원자 index의 permutation이다. 아래 시험은 한 결정의 원자 순서를 바꾸고 neighbor index를 새 번호로 옮긴 뒤, convolution 결과가 같은 permutation을 따르는지 확인한다. Batch normalization의 running statistics가 바뀌지 않도록 평가 모드에서 비교한다.

```python
layer.eval()

permutation = torch.randperm(num_atoms)
old_to_new = torch.argsort(permutation)

permuted_atoms = atom_features[permutation]
permuted_bonds = neighbor_features[permutation]
permuted_neighbors = old_to_new[neighbor_indices[permutation]]

with torch.no_grad():
    reference = layer(atom_features, neighbor_features, neighbor_indices)
    permuted = layer(permuted_atoms, permuted_bonds, permuted_neighbors)

assert torch.allclose(permuted, reference[permutation], atol=1e-6, rtol=1e-6)
```

### (2) 정량 평가와 보고 항목

!!! info "[Measurement]"
    같은 train/validation/test split과 같은 목표 정규화에서, test crystal $b$의 참값 $y_b$와 예측값 $\widehat y_b$로 mean absolute error (MAE)와 root mean squared error (RMSE)를 계산한다.[1,2]

    $$
    \operatorname{MAE}
    =\frac{1}{B}\sum_{b=1}^{B}
    \left|\widehat y_b-y_b\right|
    $$

    $$
    \operatorname{RMSE}
    =\sqrt{
    \frac{1}{B}\sum_{b=1}^{B}
    \left(\widehat y_b-y_b\right)^2
    }
    $$

    두 값의 단위는 목표 property와 같으며, 원자당 값인지 cell당 값인지 반드시 함께 적는다. Random split은 유사한 조성이나 구조 prototype을 train과 test 양쪽에 둘 수 있으므로, 새로운 화학 조성이나 구조로의 일반화를 주장하려면 group split의 기준과 중복 제거법을 함께 보고해야 한다.[2,5]

재현을 위해 고정하거나 기록할 항목은 다음과 같다.

| 구분 | 필수 기록 | 결과에 영향을 주는 경로 |
| --- | --- | --- |
| 결정 그래프 | cutoff, $M$, periodic image, padding mask | edge multiset과 local environment |
| 원자 입력 | 원소 encoding, embedding 차원 | 초기 화학 정보 |
| Bond 입력 | 거리 범위, $\mu_q$, $\gamma$, basis 수 | 거리 분해능과 cutoff 거동 |
| Convolution | 층 수, hidden 차원, normalization | receptive field와 최적화 |
| Pooling | mean, sum 또는 학습형 readout | 계 크기 scaling |
| 목표 | 단위, 원자당·cell당 정규화 | 손실과 오차의 의미 |
| 자료 분할 | 중복 제거, random·composition·prototype split | 일반화 범위 |

## 5. 한계와 적용 범위

CGCNN은 결정 구조에서 직접 학습 가능한 representation을 만들지만, 원형 architecture의 입력과 message는 모든 물리 정보를 보존하지 않는다.[1–3,5]

| 한계 | 손실되는 정보 또는 위험 | 확인 방법 |
| --- | --- | --- |
| 유한 이웃 목록 | cutoff 밖의 장거리 정전기·분산 상호작용 | cutoff와 장거리 항에 대한 ablation |
| 거리 중심 bond feature | 방향과 결합각의 명시적 표현 | angular 또는 equivariant model과 비교 |
| Pairwise message | 한 층에서 명시적인 three-body correlation 부재 | 각도 feature를 넣은 모형과 비교 |
| 고정 $M$과 padding | 결정별 coordination 차이 왜곡 | neighbor shell과 padding mask 검사 |
| Mean pooling | extensive target의 크기 정보 약화 | sum·atomwise decoder와 단위 비교 |
| 자료 분할 누출 | 유사 조성·구조에 대한 과도한 성능 추정 | composition·prototype group split |

!!! warning "[Interpretation Caveat]"
    Gate 값이 크다는 사실만으로 특정 bond의 물리적 결합 세기나 인과적 중요도가 증명되지는 않는다. Gate는 학습 손실과 전체 network parameterization 안에서 선택된 내부 가중치이다. 화학적 해석에는 독립적인 구조 perturbation, attribution 안정성 또는 별도 물리 계산이 필요하다.[1–3]

## 6. 요약

1. CGCNN은 기준 cell의 원자와 periodic bond를 multigraph로 표현하며, 같은 원자쌍의 서로 다른 lattice image를 별도 edge로 유지한다.
2. 각 edge는 receiver 원자, sender 원자와 bond feature를 결합하고 sigmoid gate와 softplus content의 곱을 message로 만든다.
3. Edge message를 receiver별로 합하고 residual update를 적용하면 한 층의 원자 표현이 완성된다.
4. 여러 convolution 뒤에는 결정별 pooling과 property decoder를 적용하며, pooling은 목표량의 extensive·intensive 성격과 맞아야 한다.
5. 재현에는 이웃 규칙, feature basis, normalization, pooling, 목표 단위와 자료 분할을 함께 기록해야 한다.
6. 원형 CGCNN의 유한 이웃, pairwise 거리 feature와 고정 이웃 수는 장거리·각도·명시적 many-body 정보를 제한한다.

## 7. 참고문헌

1. T. Xie and J. C. Grossman, "Crystal Graph Convolutional Neural Networks for an Accurate and Interpretable Prediction of Material Properties," *Physical Review Letters* **120**, 145301 (2018). [DOI](https://doi.org/10.1103/PhysRevLett.120.145301).
2. P. Reiser, M. Neubert, A. Eberhard, L. Torresi, C. Zhou, C. Shao, H. Metni, C. van Hoesel, H. Schopmans, T. Sommer, and P. Friederich, "Graph neural networks for materials science and chemistry," *Communications Materials* **3**, 93 (2022). [DOI](https://doi.org/10.1038/s43246-022-00315-6).
3. C. W. Park and C. Wolverton, "Developing an improved crystal graph convolutional neural network framework for accelerated materials discovery," *Physical Review Materials* **4**, 063801 (2020). [DOI](https://doi.org/10.1103/PhysRevMaterials.4.063801).
4. T. Xie, "Crystal Graph Convolutional Neural Networks," official source repository. [GitHub](https://github.com/txie-93/cgcnn/blob/master/cgcnn/model.py).
5. C. Chen, W. Ye, Y. Zuo, C. Zheng, and S. P. Ong, "Graph Networks as a Universal Machine Learning Framework for Molecules and Crystals," *Chemistry of Materials* **31**, 3564–3572 (2019). [DOI](https://doi.org/10.1021/acs.chemmater.9b01294).
