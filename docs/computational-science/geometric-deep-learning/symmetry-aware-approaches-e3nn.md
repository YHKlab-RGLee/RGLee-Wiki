---
title: "1.3. Geometric deep learning: Symmetry-aware approaches — (1) e3nn"
description: 일반 GNN의 공간 대칭성 한계와 e3nn의 E(3)-equivariant formalism을 설명
status: verified
last_verified: 2026-08-13
---

# 1.3. Geometric deep learning: Symmetry-aware approaches — (1) e3nn

[Graph neural networks](graph-neural-networks.md)에서 설명한 message passing은 node index의 재배열을 일관되게 처리하지만, 이것만으로 3차원 좌표의 rotation과 reflection에 대한 feature의 변환 법칙까지 정해지지는 않는다. 거리와 scalar feature만 사용하는 GNN은 scalar 출력을 공간 변환에 invariant하게 만들 수 있지만, 방향 성분을 일반 channel처럼 독립적으로 섞거나 비선형 변환하면 vector와 higher-order tensor가 좌표계 변화에 맞게 변환한다는 보장이 없다.[1,3,4]

`e3nn` formalism은 feature 공간을 $O(3)$ irreducible representation (irrep)의 direct sum으로 구성하고, 허용되는 연산을 이 표현과 교환하는 map으로 제한한다. Spherical harmonics가 상대 방향을 irrep feature로 바꾸고, Clebsch–Gordan tensor product가 입력 feature와 방향 feature를 허용된 출력 irrep로 결합한다. 이 구조는 scalar·vector·higher-order tensor의 변환 법칙을 각 층에서 보존한다.[1–4]

## 1. $E(3)$ 대칭과 equivariance

### (1) Euclidean transformation

3차원 Euclidean group $E(3)$의 원소를 $g=(R,\mathbf t)$로 쓰면 좌표에 대한 작용은

$$
\mathbf r_i
\longmapsto
g\mathbf r_i
=R\mathbf r_i+\mathbf t,
\qquad R\in O(3)
$$

이다. $O(3)$에는 $\det R=+1$인 proper rotation과 $\det R=-1$인 reflection·inversion이 함께 들어간다. 군 구조는

$$
E(3)\cong \mathbb R^3\rtimes O(3)
$$

로 나타낸다.[1,3]

입력 feature 공간의 표현을 $D_{\mathrm{in}}(g)$, 출력 표현을 $D_{\mathrm{out}}(g)$라 할 때 모형 $F$가

$$
F\!\left(D_{\mathrm{in}}(g)x\right)
=D_{\mathrm{out}}(g)F(x)
$$

를 모든 $g$에 대해 만족하면 equivariant라고 한다.[1–3] 출력 표현이 항등 표현이면

$$
F\!\left(D_{\mathrm{in}}(g)x\right)=F(x)
$$

가 되어 invariant가 된다. 예를 들어 에너지는 좌표계를 회전해도 값이 바뀌지 않는 invariant이고, 위치에 대한 에너지 기울기에서 얻은 힘은 회전·반전에 따라 극성 벡터로 변환한다. 이 차이가 scalar 출력과 vector 출력에 서로 다른 표현을 지정해야 하는 이유이다.[1,4]

### (2) Translational symmetry

원자계 그래프에서는 절대 좌표 대신 상대 벡터

$$
\mathbf r_{ij}=\mathbf r_j-\mathbf r_i
$$

를 사용하면 전역 병진이 소거된다. 주기계에서는 lattice vector $\mathbf a_{ij}$를 포함해

$$
\mathbf r_{ij}
=\mathbf r_j-\mathbf r_i+\mathbf a_{ij}
$$

로 이웃 image의 실제 변위를 정한다.[2,4] 이 벡터는 회전하면 $R\mathbf r_{ij}$가 되므로 이후 $O(3)$ 표현론으로 방향 의존성을 처리할 수 있다.

## 2. $O(3)$ irreducible representation

### (1) $l$, $m$과 parity

$O(3)$의 실수 irreducible representation (irrep)은 angular momentum degree $l=0,1,2,\ldots$와 inversion parity $p\in\{+1,-1\}$로 표시한다. `e3nn` 표기에서는 $p=+1$을 `e`, $p=-1$을 `o`로 쓴다. 한 irrep의 차원은

$$
\dim(l,p)=2l+1
$$

이다.[1,2,4] $m=-l,\ldots,l$은 한 irrep 안의 $2l+1$개 성분을 구분한다. 이 성분들은 서로 독립된 channel이 아니라, rotation을 적용하면 함께 섞이는 하나의 feature이다.

$P=-I$를 공간 inversion이라 하고 $g=P^kR$를 $R\in SO(3)$와 $k\in\{0,1\}$로 분해하면 $(l,p)$ feature의 변환은

$$
D^{(l,p)}(g)
=p^kD^{(l)}(R)
$$

로 쓸 수 있다. 따라서 `e` feature는 inversion에서 부호가 유지되고, `o` feature는 부호가 바뀐다. $D^{(l)}(R)$은 선택한 실수 기저의 Wigner $D$ matrix이며, 같은 물리적 feature도 기저에 따라 각 성분의 배열은 달라질 수 있다.[1,2,4]

대표적인 irrep와 물리적 변환 법칙의 대응은 다음과 같다.[1–4]

| `e3nn` 표기 | $l$ | 차원 | inversion | 물리적 예 |
| --- | ---: | ---: | --- | --- |
| `0e` | 0 | 1 | 부호 유지 | 에너지와 같은 scalar |
| `1o` | 1 | 3 | 부호 반전 | 위치·힘과 같은 polar vector |
| `2e` | 2 | 5 | 부호 유지 | symmetric traceless rank-2 tensor |
| `1e` | 1 | 3 | 부호 유지 | angular momentum·magnetic field·두 polar vector의 cross product와 같은 axial vector |
| `0o` | 0 | 1 | 부호 반전 | 세 polar vector의 scalar triple product와 같은 pseudoscalar |

일반 Cartesian tensor 하나는 여러 irrep로 분해될 수 있다. 예를 들어 symmetric rank-2 tensor는 trace인 `0e`와 traceless component인 `2e`의 direct sum이다. 따라서 배열의 축 개수만 보고 하나의 irrep를 지정할 수 없다.[1–3]

### (2) Direct sum과 multiplicity

신경망의 한 층은 여러 종류와 여러 사본의 irrep를 함께 가진다.

$$
\mathcal V
=\bigoplus_{a}
m_a\,\mathcal V^{(l_a,p_a)}
$$

여기서 $m_a$는 같은 irrep의 channel 수인 multiplicity이다. 예를 들어 `16x0e + 8x1o`는 scalar 16개와 polar vector 8개를 가지며 전체 성분 수는 $16+8\times3=40$이다.

| 표기 요소 | 의미 | `8x1o`에서의 값 |
| --- | --- | --- |
| `8x` | multiplicity, 즉 같은 irrep의 사본 수 | polar-vector feature 8개 |
| `1` | angular momentum degree $l$ | 각 사본마다 성분 3개 |
| `o` | inversion parity $p=-1$ | inversion에서 각 사본의 부호 반전 |

`+`는 서로 다른 feature space의 direct sum을 뜻한다. Multiplicity가 1이면 `1x`를 생략할 수 있으므로 `2x0e + 1o + 2e`의 전체 성분 수는 $2+3+5=10$이다.[1,2,4]

`16x0e + 8x1o`에서 rotation은 각 `1o` 사본의 세 $m$ 성분을 같은 $D^{(1)}(R)$로 섞지만, 8개 사본 자체는 같은 방식으로 변환한다. 따라서 equivariant linear map은 `1o`의 세 성분에 임의의 서로 다른 가중치를 주는 대신, multiplicity 축에서 8개 사본을 학습 가능한 scalar matrix로 섞을 수 있다. $l$과 $p$가 다른 feature 사이의 변환에는 다음 절의 tensor product처럼 변환 법칙을 보존하는 별도 연산이 필요하다.[1–3]

## 3. 방향 기저와 tensor product

### (1) Spherical harmonics

단위 상대 방향 $\hat{\mathbf r}=\mathbf r/\|\mathbf r\|$의 spherical harmonics를 실수 벡터

$$
\mathbf Y^{(l)}(\hat{\mathbf r})
=
\left(
Y_{-l}^{(l)},\ldots,Y_l^{(l)}
\right)
$$

로 모으면

$$
\mathbf Y^{(l)}(R\hat{\mathbf r})
=D^{(l)}(R)
\mathbf Y^{(l)}(\hat{\mathbf r})
$$

가 성립한다.[1–3] 또한 $\mathbf Y^{(l)}(-\hat{\mathbf r})=(-1)^l\mathbf Y^{(l)}(\hat{\mathbf r})$이므로 polar vector인 위치 방향에서 만든 spherical harmonics의 natural parity는 짝수 $l$에서 `e`, 홀수 $l$에서 `o`이다.[1–3] 따라서 $Y^{(0)}$, $Y^{(1)}$, $Y^{(2)}$는 각각 `0e`, `1o`, `2e` 방향 feature가 된다.

거리 $r=\|\mathbf r\|$는 rotation과 inversion에 invariant이므로 radial basis $B_k(r)$와 그 값을 입력받는 multilayer perceptron (MLP)은 scalar weight를 만들 수 있다. 방향은 $\mathbf Y^{(l)}$, 거리는 radial network로 분리하면 변환 법칙을 보존하면서 각도와 거리 의존성을 모두 표현한다.[1,2,4]

### (2) Clebsch–Gordan coefficient와 equivariant tensor product

두 irrep feature $\mathbf x^{(l_1,p_1)}$와 $\mathbf y^{(l_2,p_2)}$의 모든 성분 곱을 모은 raw tensor product는 차원이 $(2l_1+1)(2l_2+1)$인 reducible representation이다. Clebsch–Gordan coefficient는 이 공간의 기저를 바꾸어, 서로 독립적으로 변환하는 출력 irrep block으로 분해한다. 출력 $(l_3,p_3)$에 대한 projection은

$$
z_{m_3}^{(l_3,p_3)}
=
\sum_{m_1,m_2}
C_{l_1m_1,l_2m_2}^{l_3m_3}
x_{m_1}^{(l_1,p_1)}
y_{m_2}^{(l_2,p_2)}
$$

로 쓴다.[1–3] 허용되는 coupling path는

$$
|l_1-l_2|
\le l_3
\le l_1+l_2,
\qquad
p_3=p_1p_2
$$

를 만족한다. 첫 조건은 angular momentum coupling의 triangle rule이고 둘째는 inversion parity 보존이다.[1–3]

Clebsch–Gordan coefficient가 rotation equivariance를 보장하는 핵심은 다음 intertwiner identity이다.

$$
\sum_{m_1,m_2}
C_{l_1m_1,l_2m_2}^{l_3m_3}
D_{m_1n_1}^{(l_1)}(R)
D_{m_2n_2}^{(l_2)}(R)
=
\sum_{n_3}
D_{m_3n_3}^{(l_3)}(R)
C_{l_1n_1,l_2n_2}^{l_3n_3}.
$$

입력에 먼저 rotation을 적용한 뒤 coupling하면

$$
\begin{aligned}
z_{m_3}' &=
\sum_{m_1,m_2}
C_{l_1m_1,l_2m_2}^{l_3m_3}
x_{m_1}'y_{m_2}' \\
&=
\sum_{n_3}
D_{m_3n_3}^{(l_3)}(R)
z_{n_3}
\end{aligned}
$$

가 된다. 즉 “두 입력에 각각 rotation을 적용한 뒤 결합”한 결과와 “먼저 결합한 출력에 $l_3$ representation의 rotation을 적용”한 결과가 같다. 이것이 tensor product layer가 만족하는 rotation equivariance이다.[1–3]

Inversion에서는 두 입력이 각각 $p_1$, $p_2$만큼 부호를 얻으므로 출력은 $p_1p_2$만큼 변한다. 출력 경로를 $p_3=p_1p_2$로 제한하면 inversion에 대해서도 같은 교환 관계가 성립한다. Rotation에 대한 intertwiner identity와 이 parity rule을 함께 적용하면 tensor product는 $O(3)$-equivariant가 된다.[1–3]

Clebsch–Gordan coefficient 자체는 학습되는 parameter가 아니다. 선택한 irrep basis와 normalization convention이 정해지면 고정되는 수이며, 학습 가능한 가중치는 이 고정된 coupling tensor 위에서 multiplicity와 radial dependence를 조절한다.[1–4]

가장 중요한 예는 두 polar vector의 결합이다.

$$
\mathtt{1o}\otimes\mathtt{1o}
=
\mathtt{0e}\oplus\mathtt{1e}\oplus\mathtt{2e}.
$$

| 출력 경로 | Cartesian 관점 | 해석 |
| --- | --- | --- |
| `0e` | $\mathbf a\cdot\mathbf b$ | rotation과 inversion에 invariant인 scalar |
| `1e` | $\mathbf a\times\mathbf b$ | inversion에서 부호가 유지되는 axial vector |
| `2e` | $\frac12(\mathbf a\mathbf b^\mathsf T+\mathbf b\mathbf a^\mathsf T)-\frac13(\mathbf a\cdot\mathbf b)I$ | symmetric traceless rank-2 feature |

세 출력 차원의 합은 $1+3+5=9$로 raw tensor product의 $3\times3$ 성분과 일치한다. 동일한 vector를 두 번 넣은 $\mathbf a\otimes\mathbf a$에서는 antisymmetric `1e` 경로가 0이지만, 서로 다른 vector를 결합하면 `1e`도 남는다.[1–4]

## 4. 원자계 equivariant convolution

### (1) Spherical harmonics와 tensor product의 결합

원자 $i$의 입력 feature를 $\mathbf x_i$라 하면 이웃 $j$가 보내는 메시지는 개념적으로

$$
\mathbf m_{ij}^{(l_{\mathrm{out}},p_{\mathrm{out}})}
=
\sum_{\text{allowed paths}}
w_{\mathrm{path}}(r_{ij})
\left[
\mathbf x_j^{(l_{\mathrm{in}},p_{\mathrm{in}})}
\otimes
\mathbf Y^{(l_f,p_f)}(\hat{\mathbf r}_{ij})
\right]^{(l_{\mathrm{out}},p_{\mathrm{out}})}
$$

로 쓸 수 있다.[1–3] $w_{\mathrm{path}}(r_{ij})$는 거리의 radial basis를 입력받아 계산한 invariant 스칼라이고, 대괄호는 허용된 출력 irrep로 사영한 tensor product이다. 이웃 합

$$
\mathbf x_i'
=
\frac{1}{\sqrt{z}}
\sum_{j\in\mathcal N(i)}
\mathbf m_{ij}
$$

도 같은 종류의 irrep끼리 더하므로 equivariant이다. $z$는 평균 이웃 수에 따른 크기 변화를 조절하는 정규화 상수이며, 정확한 정규화 규약은 모형마다 다를 수 있다.[2,4]

구체적인 feature 흐름은 다음과 같이 읽을 수 있다.

1. 이웃의 scalar feature `0e`와 결합 방향 $Y^{(1)}(\hat{\mathbf r}_{ij})$인 `1o`를 tensor product하면 `1o` vector message가 된다.
2. 이웃의 `1o` feature와 같은 `1o` 방향을 결합하면 `0e`, `1e`, `2e` message를 만들 수 있다.
3. 각 경로의 radial weight $w_{\mathrm{path}}(r_{ij})$는 `0e` scalar이므로 출력 irrep의 변환 법칙을 바꾸지 않는다.
4. 같은 출력 irrep끼리 이웃 합을 취하면 원자 $i$의 updated feature도 같은 방식으로 변환한다.[1–4]

따라서 spherical harmonics가 상대 방향을 정해진 irrep로 변환하고, Clebsch–Gordan coefficient가 입력 feature와 방향 feature를 허용된 출력 irrep로 결합하며, radial network는 그 경로의 세기만 학습한다. Rotation equivariance는 학습 결과에 우연히 나타나는 성질이 아니라 각 연산에 내장된 구조이다.[1–4]

### (2) `e3nn` 핵심 convolution 코드

다음 예제는 `e3nn`의 `spherical_harmonics`와 `FullyConnectedTensorProduct`를 사용해 edge별 equivariant message를 만들고, receiver node에 합산한다. 입력은 네 개의 `0e` scalar channel이고 출력은 네 개의 `0e`와 두 개의 `1o` channel이다. 거리 MLP는 edge마다 tensor-product path의 가중치를 만들며, `shared_weights=False`이므로 weight shape은 `[E, tp.weight_numel]`이다.[1,2,4,5]

```bash
python -m pip install torch e3nn
```

```python
import torch
from torch import nn
from e3nn import o3


irreps_in = o3.Irreps("4x0e")
irreps_sh = o3.Irreps.spherical_harmonics(lmax=2)
irreps_out = o3.Irreps("4x0e + 2x1o")

tensor_product = o3.FullyConnectedTensorProduct(
    irreps_in,
    irreps_sh,
    irreps_out,
    shared_weights=False,
)
radial_mlp = nn.Sequential(
    nn.Linear(1, 32),
    nn.SiLU(),
    nn.Linear(32, tensor_product.weight_numel),
)


def equivariant_convolution(
    node_features: torch.Tensor,
    positions: torch.Tensor,
    edge_index: torch.Tensor,
) -> torch.Tensor:
    senders, receivers = edge_index
    edge_vectors = positions[receivers] - positions[senders]
    edge_lengths = edge_vectors.norm(dim=-1, keepdim=True)

    edge_harmonics = o3.spherical_harmonics(
        irreps_sh,
        edge_vectors,
        normalize=True,
        normalization="component",
    )
    edge_weights = radial_mlp(edge_lengths)
    messages = tensor_product(
        node_features[senders],
        edge_harmonics,
        edge_weights,
    )

    output = messages.new_zeros((node_features.shape[0], irreps_out.dim))
    output.index_add_(0, receivers, messages)
    mean_degree = edge_index.shape[1] / node_features.shape[0]
    return output / mean_degree**0.5


positions = torch.randn(5, 3)
node_features = irreps_in.randn(5, -1)
edge_index = torch.tensor(
    [[0, 1, 2, 3, 4, 0, 2], [1, 2, 3, 4, 0, 3, 0]],
    dtype=torch.long,
)

output = equivariant_convolution(node_features, positions, edge_index)
assert output.shape == (5, irreps_out.dim)
```

코드의 `edge_harmonics`는 $\mathbf Y^{(l_f)}(\hat{\mathbf r}_{ij})$, `edge_weights`는 $w_{\mathrm{path}}(r_{ij})$, `messages`는 $\mathbf m_{ij}$에 대응한다. `index_add_`는 같은 receiver에 들어오는 동일한 출력 irrep를 합한다. 예제는 핵심 연산만 분리하므로 실제 potential에는 smooth radial basis와 cutoff envelope, self-interaction, batch별 graph index, residual connection과 equivariant nonlinearity가 추가로 필요하다.[2,4,5]

### (3) Equivariance 수치 검사

같은 함수에 회전된 좌표와 변환된 입력 feature를 넣은 결과는 원래 출력을 출력 irrep로 변환한 값과 일치해야 한다. 다음 검사는 임의의 proper rotation에 대해 이 교환 관계를 직접 비교한다.[1,2,5]

```python
rotation = o3.rand_matrix()
input_transform = irreps_in.D_from_matrix(rotation)
output_transform = irreps_out.D_from_matrix(rotation)

rotated_input = node_features @ input_transform.T
rotated_positions = positions @ rotation.T

rotate_then_apply = equivariant_convolution(
    rotated_input,
    rotated_positions,
    edge_index,
)
apply_then_rotate = output @ output_transform.T

assert torch.allclose(
    rotate_then_apply,
    apply_then_rotate,
    atol=1e-5,
    rtol=1e-5,
)
```

!!! info "[Measurement]"
    구현의 equivariance는 임의의 입력 $x$와 회전·반전 $g$를 표본화한 뒤, 입력을 먼저 변환한 출력과 출력을 나중에 변환한 결과의 상대 잔차로 시험한다.[1–3]

    $$
    \epsilon_{\mathrm{eq}}(x,g)
    =\frac{\left\|f\!\left(D_{\mathrm{in}}(g)x\right)-D_{\mathrm{out}}(g)f(x)\right\|_2}
    {\max\!\left(\left\|D_{\mathrm{out}}(g)f(x)\right\|_2,\epsilon_0\right)}
    $$

    $D_{\mathrm{in}}$과 $D_{\mathrm{out}}$은 입력·출력 irrep의 표현 행렬이고, $\epsilon_0$는 영벡터 부근의 분모를 안정화하는 작은 양수이다. 여러 $x$와 $g$에서 최대값과 분포를 보고하며, 허용 오차는 자료형과 연산 정밀도에 맞춰 정한다. Rotation만이 아니라 inversion과 원자 순열도 별도 표본으로 검사해야 $E(3)$과 permutation 조건을 함께 검증할 수 있다.[1–3,5]

<figure markdown="span">
  ![이웃 방향의 spherical harmonics, 거리 radial MLP와 tensor product를 결합하는 NequIP의 equivariant convolution](images/nequip-equivariant-convolution.png)
  <figcaption markdown="1">
    그림 1. NequIP equivariant convolution에서 이웃 방향의 spherical harmonics와 거리 기반 radial MLP가 tensor product 가중치로 결합되는 구조.
    출처: S. Batzner et al., “E(3)-equivariant graph neural networks for data-efficient and accurate interatomic potentials,” Figure 1d (2022),
    <a href="https://doi.org/10.1038/s41467-022-29939-5">DOI</a>,
    <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.
    원본 Figure 1에서 panel d만 잘랐으며 내용은 수정하지 않았다.[4]
  </figcaption>
</figure>

## 5. Nonlinearity와 물리적 출력

### (1) Scalar activation과 gate

스칼라 `0e`에는 보통의 원소별 비선형 함수를 적용할 수 있다. 그러나 $l>0$ irrep의 각 성분에 독립적으로 ReLU를 적용하면 회전 뒤 성분 혼합과 양립하지 않아 equivariance가 깨진다.[1–3]

대표적인 해결책은 invariant scalar gate $g$로 전체 irrep를 곱하는 것이다.

$$
\mathbf x^{(l,p)}
\longmapsto
\sigma(g)\,\mathbf x^{(l,p)}
$$

$\sigma(g)$는 invariant이므로 출력은 원래 $\mathbf x^{(l,p)}$와 같은 변환 법칙을 유지한다. Norm activation은 $\|\mathbf x^{(l,p)}\|$ 같은 invariant 크기에서 스케일을 계산해 같은 목적을 달성한다.[1–3]

Parity가 `0o`인 gate에 일반 함수를 적용하면 출력 parity가 달라질 수 있으므로 활성 함수의 짝·홀 성질까지 추적해야 한다. `O(3)` equivariance를 원하면 rotation만 검사하는 것으로 충분하지 않다.

### (2) Energy와 force

원자별 최종 scalar를 합해

$$
E(\{\mathbf r_i\})
=\sum_i \varepsilon_i^{(0e)}
$$

로 에너지를 만들면 원자 순열과 $E(3)$ 변환에 invariant가 된다. 힘은

$$
\mathbf F_i
=-\frac{\partial E}{\partial\mathbf r_i}
$$

로 계산한다.[1,4] invariant scalar의 좌표 기울기는 `1o` 극성 벡터로 변환하며, 동시에 하나의 미분 가능한 에너지에서 유도되므로 에너지–힘 일관성을 가진다.

다만 자동 미분으로 힘을 만들었다는 사실만으로 학습된 potential이 정확하거나 장거리 물리를 포함한다는 뜻은 아니다. cutoff, 이웃 목록, 원자 종류 embedding과 학습 자료가 물리적 적용 범위를 정한다.[2,4]

## 6. 근사와 적용 범위

!!! warning "[Interpretation Caveat]"
    - **각운동량 절단:** 유한한 $l_{\max}$는 angular resolution과 계산량의 절충이다. 필요한 $l_{\max}$는 물성과 자료에 따라 검증해야 하며 보편적인 값은 없다.[1,4]
    - **국소 cutoff:** 유한 이웃 반경의 message passing은 전하 이동, 장거리 정전기와 분산 상호작용을 자동으로 재현하지 않는다. 별도 장거리 항이나 전역 상호작용이 필요할 수 있다.[2,4]
    - **Parity 선택:** 반전 대칭을 강제한 모형은 실제 외부장, 표면 법선이나 chiral 환경이 제공하는 symmetry-breaking 입력을 명시적으로 받아야 한다.
    - **이웃 목록 불연속:** hard cutoff에서 이웃이 출입하면 에너지나 고차 미분이 매끄럽지 않을 수 있으므로 radial envelope의 연속성을 확인해야 한다.

## 7. 요약

1. Equivariance는 입력과 출력이 각자의 군 표현에 따라 변환하면서 모형 연산과 군 작용이 교환한다는 조건이다.
2. `e3nn` feature는 차수 $l$, parity $p$와 multiplicity로 구성된 $O(3)$ irrep의 direct sum이다.
3. Spherical harmonics는 이웃 방향을 irrep로 바꾸고, Clebsch–Gordan coefficient는 tensor product를 허용된 출력 irrep로 분해한다. 이 coefficient의 intertwiner identity가 rotation equivariance를 보장한다.
4. 거리 기반 스칼라 가중치, tensor product와 같은 irrep의 이웃 합으로 equivariant convolution을 만든다.
5. 스칼라 gate는 고차 feature에 비선형성을 주며, invariant 에너지의 기울기는 equivariant 힘을 만든다.
6. 유한한 $l_{\max}$와 국소 cutoff는 formalism의 실제 표현 범위를 제한하며, parity는 문제의 물리적 대칭성과 일치하게 선택해야 한다.

## 8. 참고문헌

1. M. Geiger and T. Smidt, "e3nn: Euclidean neural networks," *arXiv:2207.09453* (2022). [DOI](https://doi.org/10.48550/arXiv.2207.09453).
2. e3nn developers, "e3nn Documentation," official documentation. [Irreducible Representations](https://docs.e3nn.org/en/stable/api/o3/o3_irreps.html), [Tensor Product](https://docs.e3nn.org/en/stable/api/o3/o3_tp.html), [Spherical Harmonics](https://docs.e3nn.org/en/stable/api/o3/o3_sh.html).
3. N. Thomas, T. Smidt, S. Kearnes, L. Yang, L. Li, K. Kohlhoff, and P. Riley, "Tensor field networks: Rotation- and translation-equivariant neural networks for 3D point clouds," *arXiv:1802.08219* (2018). [DOI](https://doi.org/10.48550/arXiv.1802.08219).
4. S. Batzner, A. Musaelian, L. Sun, M. Geiger, J. P. Mailoa, M. Kornbluth, N. Molinari, T. Smidt, and B. Kozinsky, "E(3)-equivariant graph neural networks for data-efficient and accurate interatomic potentials," *Nature Communications* **13**, 2453 (2022). [DOI](https://doi.org/10.1038/s41467-022-29939-5).
5. e3nn developers, "Convolution," official guide (2026년 확인). [Documentation](https://docs.e3nn.org/en/stable/guide/convolution.html).
