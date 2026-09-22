---
description: Bloch 상태의 gauge 선택에서 projection과 Löwdin 직교화, 최대 국소화, disentanglement 및 Wannier 모형 검증까지 설명한다.
---

# Wannier functions and wannierization

Wannier function은 주기적인 결정의 Bloch 상태를 실공간에서 국소화된 정규직교 기저로 표현한 함수이다. **Wannierization**은 사용할 band 부분공간을 정하고, 그 안에서 Bloch 상태의 위상과 혼합을 선택하여 Wannier 기저를 구성하는 과정이다. 같은 부분공간이라도 선택한 gauge에 따라 함수의 모양과 퍼짐이 달라진다. 따라서 Fourier 변환만 수행하는 것과 유용한 국소 기저를 얻는 것은 구별해야 한다.[1][2]

이 문서는 주기적 단일입자 Hamiltonian의 고유상태를 출발점으로 한다. 예를 들어 [Density functional theory](density-functional-theory.md)의 Kohn–Sham 상태를 사용할 수 있지만, 여기서 만드는 기저 변환 자체가 전자 상관 근사를 개선하지는 않는다. Projection으로 초기 기저를 만들고 Löwdin symmetric orthogonalization으로 정규직교화한 뒤, 필요하면 maximally localized Wannier functions (MLWFs)를 구한다. 관심 band가 다른 band와 섞이면 그 앞에 disentanglement를 넣는다. 이 순서와 각 단계가 보존하는 정보가 글의 중심이다.[1][2]

## 1. Bloch–Wannier 변환과 gauge

### (1) 유한 격자의 정규화

Brillouin zone (BZ)의 균일한 $N_k$개 점과 이에 대응하는 Born–von Kármán 초격자를 생각한다. $\mathbf R$은 그 초격자 안의 격자벡터, $m$은 band 지표이다. Bloch 상태 $\psi_{m\mathbf k}$는 초격자에서 정규화하고, 주기 부분 $u_{m\mathbf k}$는 단위격자에서 정규화한다. 이때 두 함수의 관계는 다음과 같다.[1][2]

$$
\psi_{m\mathbf k}(\mathbf r)
=\frac{1}{\sqrt{N_k}}e^{i\mathbf k\cdot\mathbf r}u_{m\mathbf k}(\mathbf r),
\qquad u_{m\mathbf k}(\mathbf r+\mathbf R)=u_{m\mathbf k}(\mathbf r).
$$

따라서 서로 다른 $\mathbf k$의 Bloch 상태 내적과, 같은 $\mathbf k$에서 주기 부분의 내적은 적분 영역을 구별한다.

$$
\langle\psi_{m\mathbf k}|\psi_{n\mathbf k'}\rangle_{\rm sc}
=\delta_{mn}\delta_{\mathbf k\mathbf k'},
\qquad
\langle u_{m\mathbf k}|u_{n\mathbf k}\rangle_{\rm cell}=\delta_{mn}.
$$

$\mathrm{sc}$는 초격자, $\mathrm{cell}$은 단위격자이다. 아래에서 $\psi$와 국소 trial orbital 사이의 내적은 초격자에서, 서로 다른 $\mathbf k$의 $u$ 사이 내적은 단위격자에서 계산한다. 이 규약은 양방향 Fourier 변환에 $1/\sqrt{N_k}$를 쓰는 규약이다. Bloch 함수를 단위격자에서 정규화하여 한쪽 변환에 $1/N_k$를 쓰는 문헌과 혼용하지 않는다.[1][2]

### (2) 복합 band의 unitary 자유도

먼저 모든 $\mathbf k$에서 다른 band들과 분리된 $J$개 band 집합을 정한다. 집합 내부의 교차나 축퇴는 허용한다. 각 $\mathbf k$에서 $J\times J$ unitary 행렬 $U(\mathbf k)$로 혼합한 상태를 Wannier gauge의 Bloch 상태라고 부른다.[1][2]

$$
|\psi^{\rm W}_{n\mathbf k}\rangle
=\sum_{m=1}^{J}|\psi_{m\mathbf k}\rangle U_{mn}(\mathbf k),
\qquad U^\dagger U=UU^\dagger=I_J.
$$

$\dagger$는 Hermitian conjugate, $I_J$는 $J$차원 단위행렬이다. $J=1$이면 $U=e^{i\theta(\mathbf k)}$인 위상 선택이며, $J>1$이면 서로 다른 에너지의 상태도 섞을 수 있다. 혼합한 상태는 같은 부분공간을 생성하지만 일반적으로 Hamiltonian 고유상태는 아니다. 보존되는 것은 기저가 생성하는 공간과 그 공간에 제한된 연산자이다.[1][2]

Wannier 함수 $|w_{n\mathbf R}\rangle$와 역변환은 다음과 같다.

$$
|w_{n\mathbf R}\rangle
=\frac{1}{\sqrt{N_k}}\sum_{\mathbf k}
 e^{-i\mathbf k\cdot\mathbf R}|\psi^{\rm W}_{n\mathbf k}\rangle.
$$

$$
|\psi^{\rm W}_{n\mathbf k}\rangle
=\frac{1}{\sqrt{N_k}}\sum_{\mathbf R}
 e^{i\mathbf k\cdot\mathbf R}|w_{n\mathbf R}\rangle.
$$

이 변환은 이산 Fourier 변환이므로 정규직교성과 전체 선택 공간을 보존한다. 실제로 $\mathbf k$ 합의 직교관계를 대입하면 다음 결과를 얻는다.[1][2]

$$
\langle w_{m\mathbf R}|w_{n\mathbf R'}\rangle
=\delta_{mn}\delta_{\mathbf R\mathbf R'},
\qquad
\sum_{n\mathbf R}|w_{n\mathbf R}\rangle\langle w_{n\mathbf R}|
=\sum_{n\mathbf k}|\psi_{n\mathbf k}\rangle\langle\psi_{n\mathbf k}|.
$$

### (3) 매끄러운 gauge와 실공간 국소화

국소화의 핵심은 서로 이웃한 $\mathbf k$에서 함수가 얼마나 매끄럽게 이어지는가이다. Band 계산이 반환한 고유벡터에는 각 점마다 임의의 위상이 붙을 수 있다. 이를 그대로 Fourier 변환하면 에너지가 매끄러워도 Wannier 함수가 넓게 퍼질 수 있다. 반대로 적절한 주기 경계 접합 조건을 만족하는 해석적인 Bloch frame은 지수적으로 국소화된 Wannier 함수와 연결된다. 단순한 연속성만으로 지수 감쇠가 보장되는 것은 아니다.[1][2]

국소화는 정규직교성과 다른 조건이다. 임의의 unitary $U$로 만든 함수도 정규직교하지만, 그 공간적 범위는 좋지 않을 수 있다. 또한 유한 $\mathbf k$ 격자에서 만든 함수에는 대응하는 초격자 주기가 남는다. 이때 국소화는 초격자 안에서의 국소화를 뜻하며, 이미지 사이의 중첩이 무시될 정도인지 격자를 늘려 확인해야 한다.[1][3]

다음 표는 이후에 나오는 세 선택을 구별한다. 이 구별은 spread가 감소했다는 사실만으로 band 모형의 정확성을 판단하지 않게 해 준다.[1][2]

| 선택 단계 | 바꾸는 대상 | 보존하거나 제한하는 것 |
| --- | --- | --- |
| Projection과 Löwdin 직교화 | Trial orbital을 반영한 정규직교 frame | 투영된 함수들의 span; full rank 필요 |
| 최대 국소화 | 고정 부분공간 안의 unitary gauge | 부분공간과 그 안의 연산자 정보 |
| Disentanglement | 더 큰 공간 안의 $J$차원 부분공간 | 지정한 차원과 frozen 상태; 나머지는 근사 |

## 2. Projection과 Löwdin symmetric orthogonalization

### (1) Trial orbital의 투영

Projection은 원자 중심의 $d$ orbital, 결합 중심 함수 등 원하는 Wannier 기저의 중심과 각운동량 성격을 반영한 trial orbital $|g_n\rangle$을 선택하는 방법이다. Trial orbital은 계산된 Wannier 함수 그 자체가 아니며, 원래부터 서로 직교할 필요도 없다. 관심 band 공간에 들어 있는 성분만 남긴 뒤 정규직교화한다.[1][2][3]

각 $\mathbf k$에서 사용할 $J_{\mathbf k}$개 Bloch 상태의 projector를 $P^{\psi}_{\mathbf k}$라 하고, projection 행렬 $A$를 정의한다. 지금은 고립된 집합이면 $J_{\mathbf k}=J$이고, 뒤에서 다룰 큰 후보 공간이면 $J_{\mathbf k}\ge J$이다.

$$
P^{\psi}_{\mathbf k}=\sum_{m=1}^{J_{\mathbf k}}
|\psi_{m\mathbf k}\rangle\langle\psi_{m\mathbf k}|,
\qquad A_{mn}(\mathbf k)=\langle\psi_{m\mathbf k}|g_n\rangle.
$$

$$
|\phi_{n\mathbf k}\rangle=P^{\psi}_{\mathbf k}|g_n\rangle
=\sum_{m=1}^{J_{\mathbf k}}|\psi_{m\mathbf k}\rangle A_{mn}(\mathbf k).
$$

$A$는 $J_{\mathbf k}\times J$ 행렬이다. 열 하나는 trial orbital 하나의 band별 복소 진폭을 담는다. 따라서 $|A_{mn}|^2$만 남겨서는 이 단계의 위상 정보를 복원할 수 없다. 각 $\mathbf k$의 고유상태를 unitary 변환해도 $P^{\psi}_{\mathbf k}$는 같으므로, 같은 trial orbital을 투영한 $\phi$는 원래 고유벡터의 임의 gauge에 의존하지 않는다.[1][3]

투영된 함수들의 Gram 행렬 $S$는 다음과 같다.

$$
S_{mn}(\mathbf k)=\langle\phi_{m\mathbf k}|\phi_{n\mathbf k}\rangle,
\qquad S=A^\dagger A.
$$

$S\ne I_J$인 이유는 projection이 서로 다른 trial orbital을 같은 band 성분으로 보낼 수 있기 때문이다. 각각을 자기 norm으로 나누는 것만으로는 서로 다른 열 사이의 중첩이 없어지지 않는다. 이 상호 중첩까지 제거하는 연산이 Löwdin symmetric orthogonalization이다.[1][3]

### (2) 양의 역제곱근과 정규직교성

모든 $\mathbf k$에서 $A$가 full column rank라고 가정한다. 그러면 $S$는 양의 정부호 Hermitian 행렬이며, 양의 고유값 $s_a$와 unitary 고유벡터 행렬 $Z$로 분해할 수 있다. 양의 역제곱근은 원소별 역제곱근이 아니라 다음 행렬 함수이다.[3][4]

$$
S=Z\,\mathrm{diag}(s_1,\ldots,s_J)Z^\dagger,
\qquad
S^{-1/2}=Z\,\mathrm{diag}(s_1^{-1/2},\ldots,s_J^{-1/2})Z^\dagger.
$$

투영된 함수들을 열로 모은 것을 $\Phi_{\mathbf k}$라 쓰면 Löwdin frame $X_{\mathbf k}$와 Bloch 계수 $Q$는 다음과 같다.

$$
X_{\mathbf k}=\Phi_{\mathbf k}S^{-1/2},
\qquad Q=A(A^\dagger A)^{-1/2}.
$$

이 식은 모든 trial orbital을 같은 행렬 연산으로 동시에 다룬다. 정규직교성은 바로 확인된다.[1][3][4]

$$
X_{\mathbf k}^\dagger X_{\mathbf k}
=S^{-1/2}SS^{-1/2}=I_J,
\qquad Q^\dagger Q=I_J.
$$

$J_{\mathbf k}=J$이면 $Q$는 unitary이고 원래 고립된 band 집합을 그대로 생성한다. $J_{\mathbf k}>J$이면 $Q$는 열만 정규직교인 직사각 행렬이며, $QQ^\dagger$는 후보 band 계수 공간에서 선택된 $J$차원 부분공간의 projector이다. 따라서 직사각 행렬에 $QQ^\dagger=I_{J_{\mathbf k}}$까지 요구하면 안 된다.[1][3][4]

### (3) 최소 변형 성질과 최대 국소화의 차이

Löwdin 직교화는 주어진 입력 함수와의 거리 제곱합을 최소화한다. $X=(|x_1\rangle,\ldots,|x_J\rangle)$를 정규직교 frame이라 하면, full rank인 고정 $\Phi$에 대해 다음 문제의 해가 $\Phi S^{-1/2}$이다. Norm은 Hilbert 공간 norm이며, 행렬로 표현하면 Frobenius norm이다.[3][4]

$$
\min_{X^\dagger X=I_J}\sum_{n=1}^{J}
\|\,|x_n\rangle-|\phi_n\rangle\,\|^2
=\min_{X^\dagger X=I_J}\|X-\Phi\|_F^2.
$$

이 최적화는 위치 연산자 $\mathbf r$를 포함하지 않는다. 따라서 여기서의 최소 변형을 실공간 spread의 최소화와 동일시할 수 없다. 같은 trial orbital에서 출발해도 Löwdin 직교화 뒤에 unitary 회전을 더 적용하면 정규직교성은 유지하면서 spread를 바꿀 수 있다. Projection만으로도 목적에 맞는 기저를 얻을 수 있지만, 이를 MLWF라고 부르려면 별도의 spread 최적화 기준을 만족하는지 구별해야 한다.[1][2][3]

수치적으로는 singular value decomposition (SVD)을 이용해 같은 frame을 구성할 수 있다. Thin SVD를 $A=L\Sigma W^\dagger$라 쓰면 $L^\dagger L=W^\dagger W=I_J$, $\Sigma=\mathrm{diag}(\sigma_a)$이고 다음이 성립한다.[4][3]

$$
Q=LW^\dagger,
\qquad s_a=\sigma_a^2.
$$

이는 위 정의에 SVD를 대입한 결과이다. 작은 $\sigma_a$는 trial orbital들의 어떤 선형결합이 선택 공간에 거의 투영되지 않는다는 뜻이다. 정확히 0이면 필요한 $J$개의 독립 방향이 없으므로 원래의 정규직교화 문제는 성립하지 않는다. Pseudoinverse로 작은 방향을 버릴 수는 있지만, 그 결과는 차원이 줄어든 문제이며 원래 목표를 그대로 해결한 것이 아니다.[1][4]

다음 표처럼 원인을 분리하면 직교화 실패를 단순한 반복 횟수 부족으로 오해하지 않는다. 마지막 열은 위 rank 조건에 따른 점검 방법이다.[1][3][4]

| 관찰 | 수학적 의미 | 점검할 선택 |
| --- | --- | --- |
| $J_{\mathbf k}<J$ | 후보 공간 차원 부족 | 계산한 band 수와 후보 window |
| $\sigma_{\min}=0$ | 투영 열의 선형종속 | Trial orbital 중복과 누락된 성격 |
| 매우 작은 $\sigma_{\min}$ | 거의 잃어버린 방향의 정규화 | 원자·결합 중심, orbital 방향, window |
| 양호한 rank지만 큰 spread | 정규직교성과 국소화의 차이 | Gauge 최적화와 부분공간 적합성 |

이 문서의 Löwdin은 중첩 행렬의 역제곱근을 쓰는 **symmetric orthogonalization**이다. 저에너지 유효 Hamiltonian을 얻기 위한 Löwdin partitioning을 뜻하지 않는다.

## 3. Maximally localized Wannier functions

### (1) Spread functional과 불변 부분

최대 국소화는 고정된 band 부분공간에서 Wannier 함수들의 위치 분산 합을 최소화한다. 원점 격자에 있는 함수 $|w_{n\mathbf0}\rangle$의 중심을 $\bar{\mathbf r}_n$, 이차 모멘트를 $\langle r^2\rangle_n$이라 하면 다음과 같다. 이 실공간 정의는 국소화된 함수의 무한 결정 극한을 기준으로 하며, 실제 유한 격자에서는 아래의 이산식을 사용한다.[1][2]

$$
\bar{\mathbf r}_n=\langle w_{n\mathbf0}|\mathbf r|w_{n\mathbf0}\rangle,
\qquad
\Omega=\sum_{n=1}^{J}
\left(\langle r^2\rangle_n-|\bar{\mathbf r}_n|^2\right).
$$

$\Omega$의 차원은 길이의 제곱이다. 함수가 원점에서 얼마나 멀리 있는지가 아니라 **자기 중심 주위에서 얼마나 퍼지는지**를 측정한다. 따라서 전체 좌표 원점을 옮기거나 함수의 소속 격자를 다시 표시하는 것만으로 spread가 줄어들지 않는다.[1][2]

이 functional은 gauge-invariant 부분 $\Omega_{\rm I}$와 나머지 $\widetilde\Omega$로 나뉜다.

$$
\Omega=\Omega_{\rm I}+\widetilde\Omega,
\qquad \widetilde\Omega=\Omega_{\rm D}+\Omega_{\rm OD}.
$$

$$
\Omega_{\rm I}=\sum_n\left[
\langle r^2\rangle_n-
\sum_{m,\mathbf R}
|\langle w_{m\mathbf R}|\mathbf r|w_{n\mathbf0}\rangle|^2
\right].
$$

여기서 벡터 행렬원소의 절댓값 제곱은 Cartesian 성분들의 절댓값 제곱합이다. $\Omega_{\rm I}$는 선택 공간 자체에 정해져 있어 그 안의 unitary gauge 회전으로 바뀌지 않는다. 반면 $\widetilde\Omega$는 원점의 자기 함수 이외의 Wannier 함수와 연결하는 위치 행렬원소들의 제곱합이다.[1][2]

$$
\widetilde\Omega=
\sum_n\sum_{(m,\mathbf R)\ne(n,\mathbf0)}
|\langle w_{m\mathbf R}|\mathbf r|w_{n\mathbf0}\rangle|^2.
$$

이 표현은 고정 공간에서 줄일 수 있는 부분과 줄일 수 없는 부분을 분리한다. 아래에서 $\Omega_{\rm D}$는 같은 Wannier 지표의 위상 변화와 관련된 항, $\Omega_{\rm OD}$는 서로 다른 지표 사이의 항으로 나타난다. 둘은 모두 $\widetilde\Omega$의 구성 요소이며, $\Omega_{\rm I}$까지 자유롭게 줄이는 것은 부분공간을 바꾸는 다른 문제이다.[1][2]

### (2) 이웃한 k점의 overlap

매 반복마다 실공간 함수를 만들 필요는 없다. 단위격자에서 정규화한 주기 부분 사이의 overlap 행렬 $M$이 국소화에 필요한 $\mathbf k$ 방향 변화를 담는다. $\mathbf b$는 이웃 점까지의 reciprocal-space 벡터이다.[1][2]

$$
M_{mn}^{(\mathbf k,\mathbf b)}
=\langle u_{m\mathbf k}|u_{n,\mathbf k+\mathbf b}\rangle_{\rm cell}.
$$

Gauge를 바꾸면 두 끝점의 행렬을 각각 곱한다. 이는 같은 $\mathbf k$ 안의 similarity transform과 다르다.[1][2]

$$
M^{\rm W}(\mathbf k,\mathbf b)
=U^\dagger(\mathbf k)M(\mathbf k,\mathbf b)U(\mathbf k+\mathbf b).
$$

이산 미분의 기하학적 가중치를 $w_{\mathbf b}$라 하자. 예를 들어 Cartesian 성분 $\alpha,\beta$에 대해 다음 이차 정확도 조건을 만족하도록 이웃 shell과 가중치를 선택한다.[1][2]

$$
\sum_{\mathbf b}w_{\mathbf b}b_\alpha b_\beta=\delta_{\alpha\beta}.
$$

$\mathbf b$의 차원은 길이의 역수, $w_{\mathbf b}$의 차원은 길이의 제곱이다. 같은 이산화에서 중심과 $\Omega_{\rm I}$는 다음과 같이 계산한다. 오른쪽은 유한 격자 추정값이며 격자 수렴을 확인해야 한다.[1][2]

$$
\bar{\mathbf r}_n\simeq
-\frac{1}{N_k}\sum_{\mathbf k,\mathbf b}
 w_{\mathbf b}\mathbf b\,\operatorname{Im}\ln M^{\rm W}_{nn}(\mathbf k,\mathbf b).
$$

$$
\Omega_{\rm I}\simeq\frac{1}{N_k}\sum_{\mathbf k,\mathbf b}
 w_{\mathbf b}\left[J-\sum_{m,n}|M^{\rm W}_{mn}(\mathbf k,\mathbf b)|^2\right].
$$

$\operatorname{Im}\ln M_{nn}$은 이웃 상태 사이의 위상 차이를 사용한다. BZ 경계를 넘는 이웃도 적절한 reciprocal-lattice 접합을 적용하며, 복소 로그의 branch가 일관되어야 한다. 무작위 위상이 붙은 고유벡터를 그대로 쓰기보다 projection으로 비교적 매끄러운 초기 gauge를 만드는 이유가 여기에 있다.[1][2]

Gauge-dependent 항은 같은 overlap으로 분해된다.

$$
\Omega_{\rm D}\simeq\frac{1}{N_k}\sum_{\mathbf k,\mathbf b}w_{\mathbf b}
\sum_n\left[
\operatorname{Im}\ln M^{\rm W}_{nn}(\mathbf k,\mathbf b)
+\mathbf b\cdot\bar{\mathbf r}_n\right]^2.
$$

$$
\Omega_{\rm OD}\simeq\frac{1}{N_k}\sum_{\mathbf k,\mathbf b}w_{\mathbf b}
\sum_{m\ne n}|M^{\rm W}_{mn}(\mathbf k,\mathbf b)|^2.
$$

첫 항은 중심 위치로 설명되지 않는 대각 위상 변화를, 둘째 항은 이웃 점에서 서로 다른 Wannier 지표가 섞이는 정도를 측정한다. 두 식은 동일한 finite-difference 규약에서 사용해야 하며, 서로 다른 이산화의 spread 숫자를 바로 비교해서는 안 된다.[1][2]

### (3) 반복 최적화와 local minimum

실제 최적화에서는 $U(\mathbf k)$의 unitary 조건을 유지하며 $\widetilde\Omega$를 줄인다. 예를 들어 anti-Hermitian 행렬 $K^\dagger=-K$를 쓰는 업데이트는 다음과 같이 표현할 수 있다. 이는 unitary 공간에서의 움직임을 보여 주는 표현이며, 특정 코드의 유일한 업데이트 공식은 아니다.[1][2]

$$
U_{\rm new}(\mathbf k)=U_{\rm old}(\mathbf k)e^{K(\mathbf k)}.
$$

Spread 변화가 작아졌다는 것은 선택한 초기값에서 반복이 멈출 조건을 충족했다는 뜻이다. 모든 초기값에 대해 global minimum에 도달했다는 증명은 아니다. 초기 projection을 달리하여 중심·함수 성격·최종 spread를 비교하면 local minimum과 원하는 기저 사이의 차이를 점검할 수 있다. 대칭을 고정해야 하는 문제에서는 unconstrained spread 최소화와 대칭을 만족하는 기저 구성을 별도로 구분해야 한다.[1][2][3]

## 4. Entangled bands와 disentanglement

### (1) 부분공간 선택과 gauge 선택

Entangled bands는 원하는 orbital 성격을 가진 상태들이 다른 band와 에너지상 겹치거나 혼성화되어 고립된 고정 band 집합으로 잘라내기 어려운 경우이다. Disentanglement는 더 큰 후보 공간에서 매 $\mathbf k$마다 $J$차원 공간을 선택하는 과정이다. 한 개의 band 번호를 교차점 너머로 추적하는 것과 같지 않다.[1][2]

후보 상태가 $J_{\mathbf k}$개일 때 직사각 행렬 $V(\mathbf k)$로 선택한 frame을 만들고, 그 안에서 정사각 unitary $U(\mathbf k)$로 gauge를 최적화한다.

$$
|\psi^{\rm opt}_{n\mathbf k}\rangle
=\sum_{m=1}^{J_{\mathbf k}}|\psi_{m\mathbf k}\rangle V_{mn}(\mathbf k),
\qquad V^\dagger V=I_J.
$$

$$
|\psi^{\rm W}_{n\mathbf k}\rangle
=\sum_{m=1}^{J_{\mathbf k}}|\psi_{m\mathbf k}\rangle T_{mn}(\mathbf k),
\qquad T(\mathbf k)=V(\mathbf k)U(\mathbf k).
$$

$V$를 바꾸면 선택 공간이 달라지고, 고정 $V$에서 $U$만 바꾸면 그 공간은 같다. Disentanglement 뒤의 $J$개 상태는 보통 원래 고유상태의 선형결합이므로, 얻은 모형이 후보 window 안의 모든 원래 band를 정확히 재현할 필요도, 그럴 차원도 없다.[1][2][3]

부분공간의 매끄러움은 주기 부분 $|u^{\rm opt}_{n\mathbf k}\rangle$의 projector $P_{\mathbf k}$로 측정한다. 이것은 앞의 초격자 Bloch projector $P^{\psi}_{\mathbf k}$와 달리 **같은 단위격자 함수 공간**에서 이웃 $\mathbf k$와 비교한다.

$$
P_{\mathbf k}=\sum_{n=1}^{J}
|u^{\rm opt}_{n\mathbf k}\rangle\langle u^{\rm opt}_{n\mathbf k}|.
$$

$$
\mathcal T_{\mathbf k,\mathbf b}
=\operatorname{Tr}[P_{\mathbf k}(1-P_{\mathbf k+\mathbf b})]
=J-\operatorname{Tr}[P_{\mathbf k}P_{\mathbf k+\mathbf b}].
$$

$\operatorname{Tr}$는 단위격자 함수 공간의 trace이다. $\mathcal T$는 이웃 공간이 같으면 0이고, 서로 맞지 않는 방향이 있으면 양수이다. 이 값을 가중 평균한 것이 앞서 정의한 $\Omega_{\rm I}$의 이산 표현이다. 따라서 보통 먼저 $V$를 조절하여 $\Omega_{\rm I}$를 최소화하고, 선택 공간을 고정한 뒤 $U$로 $\widetilde\Omega$를 줄인다. 여기서 gauge-invariant라는 말은 **고정 부분공간 안에서** 불변이라는 뜻이다.[1][2]

### (2) Outer window와 frozen window

Outer window는 부분공간 선택에 사용할 후보 고유상태들의 에너지 범위를 정한다. Frozen 또는 inner window는 그중 최종 부분공간에 반드시 포함할 상태들을 정한다. 각 $\mathbf k$에서 frozen 상태 수를 $J_f(\mathbf k)$라 하면, 필요한 차원 조건은 다음과 같다.[1][5]

$$
J_f(\mathbf k)\le J\le J_{\mathbf k}
\qquad\text{모든 입력 }\mathbf k\text{에서}.
$$

왼쪽 조건을 어기면 보존할 상태를 $J$차원 안에 담을 수 없고, 오른쪽 조건을 어기면 필요한 차원만큼 선택할 수 없다. 두 조건을 만족해도 원하는 orbital 성격이 후보 공간에 빠졌다면 좋은 모형은 얻기 어렵다. 따라서 window는 에너지 숫자만 보고 고르기보다 band 성격과 혼성화 영역을 함께 검토한다.[1][3]

| 범위 | 상태에 대한 조건 | 재현 정확도의 의미 |
| --- | --- | --- |
| Frozen window 안 | 해당 고유상태를 선택 공간에 포함 | 입력 $\mathbf k$에서 해당 고유값 보존 |
| Outer 안, frozen 밖 | 필요한 선형결합을 선택 | 원래 개별 band의 정확한 보존은 보장하지 않음 |
| Outer 밖 | 선택 후보에서 제외 | 이 모형의 검증 범위로 자동 확장할 수 없음 |

위의 정확한 보존은 이상적인 부분공간 포함과 같은 입력 Hamiltonian을 전제로 한다. 입력하지 않은 $\mathbf k$에서의 값은 이후 Fourier interpolation의 결과이므로, frozen window 안이라는 이유만으로 정확해지는 것은 아니다. 실제 계산에서는 부분공간 선택 오차와 보간 오차를 나누어 확인한다.[1][3]

예를 들어 Si의 네 occupied valence band만 표현하는 문제와, valence 및 낮은 conduction 성격을 함께 나타내는 문제는 다른 부분공간 선택이다. 후자는 높은 conduction band와의 연결 때문에 disentanglement가 필요할 수 있다. Wannier90의 Si 예제는 이를 atom-centered $sp^3$ 초기 projection과 inner/outer window로 보여 준다. 원문 band 그림은 [공식 tutorial 3](https://wannier90.readthedocs.io/en/latest/tutorials/tutorial_3/)에서 확인할 수 있다.[1][6]

## 5. Wannier Hamiltonian과 interpolation

### (1) 연산자 변환과 hopping

Wannier 기저의 유용성은 작은 행렬로 band 정보를 다시 계산할 수 있다는 데 있다. 원래 고유값을 대각에 둔 행렬을 $E(\mathbf k)$라 하면, 최종 frame의 Hamiltonian은 다음과 같다. 고립된 band에서는 $T=U$, disentanglement가 있으면 $T=VU$이다.[1][3]

$$
H^{\rm W}(\mathbf k)=T^\dagger(\mathbf k)E(\mathbf k)T(\mathbf k).
$$

정사각 unitary 변환이면 고유값 전체가 보존된다. 직사각 $T$이면 더 큰 Hamiltonian을 선택 공간에 제한한 행렬이며, frozen 조건으로 포함시킨 상태 이외에는 원래 고유값과 차이가 날 수 있다. 이 차이는 Fourier 보간 전에 이미 생길 수 있는 부분공간 오차이다.[1][3]

실공간 행렬원소 $H_{mn}(\mathbf R)$는 원점의 $m$ 함수와 $\mathbf R$ 격자의 $n$ 함수 사이의 hopping을 나타낸다. 이 문서의 Fourier 부호 규약에서는 다음과 같다.

$$
H_{mn}(\mathbf R)=\langle w_{m\mathbf0}|\hat H|w_{n\mathbf R}\rangle
=\frac{1}{N_k}\sum_{\mathbf k}e^{-i\mathbf k\cdot\mathbf R}
H^{\rm W}_{mn}(\mathbf k).
$$

$$
H^{\rm W}_{\rm int}(\mathbf q)=\sum_{\mathbf R}
 e^{i\mathbf q\cdot\mathbf R}H(\mathbf R).
$$

$\mathbf q$는 새로 평가할 파수이다. 대응하는 이산 Fourier 격자의 모든 독립 $\mathbf R$ 성분을 유지하면 입력 격자에서 원래 $H^{\rm W}$를 복원한다. 새로운 점에서는 이를 보간으로 사용한다. 실제 프로그램이 Wigner–Seitz 형태의 실공간 집합을 쓰면 동등한 경계 벡터들의 가중치까지 포함해야 한다.[1][3][7]

잘 국소화된 기저는 먼 격자 사이의 행렬원소를 작게 만들어 실공간 절단에 유리하다. 그러나 작은 spread가 어떤 임의의 hopping cutoff에서도 정확한 band를 보장하지는 않는다. $\mathbf k$ 격자와 실공간 범위가 연결되어 있으므로, cutoff만 늘려도 해결되지 않는 경우에는 입력 격자를 촘촘하게 해야 한다.[1][3]

### (2) 기저 선택과 물리적 해석

Wannier 함수의 원자·결합 성격은 선택한 부분공간과 gauge를 해석하는 데 유용하다. 다만 함수 하나의 모양이나 hopping 하나를 유일하게 정해진 관측량으로 보면 안 된다. 특히 같은 재료에서도 ligand band를 포함하는지에 따라 transition-metal 중심 함수의 ligand 꼬리와 Hamiltonian의 크기가 달라질 수 있다.[1][2]

예를 들어 좁은 antibonding band 집합만 선택하면 원자 성분 사이의 혼성화를 함수의 공간적 꼬리로 담아야 한다. Bonding band까지 포함하면 그 성분을 별도 함수들로 분리할 자유도가 생긴다. 따라서 서로 다른 window와 $J$를 쓴 두 모형의 spread를 비교할 때는, 더 작은 숫자가 같은 물리 모형을 더 잘 최적화했다는 뜻인지 먼저 확인해야 한다.[1][2]

Wannier Hamiltonian은 조밀한 band 계산과 후속 유효 모형의 출발점이지만, 모든 응답이 고유값만으로 정해지는 것은 아니다. 같은 $\mathbf k$를 보존하는 연산자 $\hat O$의 행렬 $O^{\rm B}$가 필요하면 같은 frame으로 변환한다.[1][3]

$$
O^{\rm W}(\mathbf k)=T^\dagger(\mathbf k)O^{\rm B}(\mathbf k)T(\mathbf k).
$$

따라서 band interpolation 검증이 끝났더라도 Spin 등 별도 행렬원소가 필요한 계산은 그 입력과 변환을 추가로 검증한다. 위치 연산자는 서로 다른 $\mathbf k$ 사이의 구조와 $\mathbf k$ 미분을 포함하므로, 위의 같은-$\mathbf k$ 행렬식만으로 처리하지 않는다. 상호작용 모형 역시 선택 기저에 맞는 상호작용 행렬원소와 근사가 별도로 필요하다. Wannierization을 수행했다는 이유만으로 그 모형의 모든 항이 정해지는 것은 아니다.[1][2][3]

## 6. 계산 검증과 적용 한계

### (1) 단계별 검증

실무 검증은 **부분공간, gauge, interpolation**을 분리하여 수행하는 편이 원인 파악에 유리하다. Wannier90처럼 overlap과 projection을 입력받는 도구에서는 $M$, $A$, 고유값과 $\mathbf k$ 순서가 같은 전자구조 계산을 가리켜야 한다. 공식 Si 예제의 `.mmn`, `.amn`, `.eig`는 각각 이 세 종류의 정보를 제공한다. 이는 수학적으로 서로 대응하는 frame과 에너지를 변환해야 한다는 조건의 구현이다.[1][3][6][7]

다음 표는 앞의 식들로부터 구성한 점검 순서이다. 보편적인 합격 오차 한 개를 정하기보다 최종 응용에 필요한 정확도를 먼저 정하고, 그 정확도에 대해 격자와 window 수렴을 기록한다.[1][3]

| 단계 | 확인할 자료 | 실패 시 우선 점검 |
| --- | --- | --- |
| 후보 공간 | 모든 $\mathbf k$의 $J_{\mathbf k}$, orbital 성격 | Band 수와 outer window |
| Projection | $S$ 고유값 또는 $A$의 singular value | Trial orbital 독립성과 성격 |
| 직교화 | $Q^\dagger Q-I_J$의 norm | 정규화, 행렬 순서, 작은 singular value |
| 국소화 | $\Omega$ 성분, 개별 spread, 중심과 함수 모양 | 초기 gauge, 반복 수렴, 대칭 조건 |
| 입력점 재현 | $T^\dagger ET$의 고유값과 원래 band | Frozen 포함과 부분공간 선택 |
| 새 점 재현 | 별도 직접 계산과 interpolated band | $\mathbf k$ 격자와 hopping 범위 |
| 후속 응용 | 필요한 연산자와 최종 물리량의 수렴 | 누락된 행렬원소와 모형 근사 |

특히 입력 $\mathbf k$에서의 일치는 Fourier 변환을 올바르게 구현했다는 확인이 될 수 있지만, 그 사이의 band까지 정확하다는 독립 검증은 아니다. 고대칭 경로뿐 아니라 관심 에너지 영역의 추가 점을 직접 계산하여 비교하면 경로 밖의 오차도 점검할 수 있다. 이는 새 점에서의 interpolation 오차를 평가하라는 원칙을 적용한 검증 절차이다.[1][3]

Band 비교에서는 같은 에너지 기준을 맞추고, 비교 대상 band 또는 부분공간을 먼저 정한다. 교차점에서 단순한 band 번호가 서로 다른 성격을 가리키면 잘못된 대응으로 오차를 과장하거나 숨길 수 있다. 이때 eigenvalue 집합의 일치와 orbital·부분공간의 일치를 별도 질문으로 다룬다.[1][2][3]

### (2) 국소화와 위상적 제약

국소화 실패의 원인이 언제나 trial orbital이나 반복 설정에 있는 것은 아니다. 고립된 2차원 또는 3차원 band 집합의 Chern 불변량이 0이 아니면, 그 집합 전체를 생성하는 정규직교 기저를 모든 방향에서 지수적으로 국소화할 수 없는 위상적 장애가 있다. 이는 유한 격자의 작은 spread 숫자만으로 판정할 문제가 아니다.[1][2]

이 결론을 모든 topological insulator에 일괄 적용하지 않는다. 여기서 명시한 장애는 선택한 부분공간의 비영 Chern 불변량에 관한 것이며, 추가로 특정 대칭을 유지하도록 요구하는 문제와도 구별한다. 부분공간에 band를 더 넣으면 위상적 성격과 Wannier 기저의 존재 조건 자체가 달라질 수 있다.[1][2][3]

또한 spin을 포함한 계산에서 Bloch 상태가 spinor이면 projection과 overlap도 같은 spinor 공간에서 계산해야 한다. Scalar orbital로 가정한 직관을 그대로 적용하기보다, 선택한 trial spinor와 보존할 대칭을 함께 명시한다. 이 문서의 행렬식은 spin 성분을 내적에 포함하면 그대로 사용할 수 있지만, 함수가 실수라는 추가 가정은 하지 않는다.[1][2][3]

### (3) 재현 가능한 기록

재현을 위해서는 최종 spread만 저장하기보다 원래 band 계산, 사용한 $J$, trial orbital의 중심·방향, window, $\mathbf k$ 격자, 수렴 조건과 실공간 절단을 함께 남긴다. 같은 재료에 대한 서로 다른 Wannier 모형을 비교할 때에는 이 항목들이 같은지 먼저 확인한다. 다음 표는 계산 목적별로 특히 보존해야 할 검증 근거를 정리한 것이다.[1][2][3]

| 계산 목적 | 핵심 검증 근거 | 해석상의 제한 |
| --- | --- | --- |
| Orbital·결합 해석 | 중심, 대칭, 함수 모양과 부분공간 | 개별 함수는 gauge에 의존 |
| Band interpolation | 새 $\mathbf k$의 직접 계산과 비교 | 입력점 재현만으로 충분하지 않음 |
| 저에너지 모형 | 대상 에너지 구간과 포함 상태 | 제외 band의 모든 정보를 보존하지 않음 |
| 연산자 기반 응답 | 해당 행렬원소와 최종 응답 수렴 | Band 고유값 일치와 별도 검증 |

## 7. 요약

- Bloch–Wannier 변환은 선택된 공간의 기저 변환이며, 국소화의 품질은 $\mathbf k$에 따른 frame의 매끄러움에 달려 있다.
- Projection은 trial orbital의 성격을 공간에 투영하고, Löwdin 직교화는 full-rank Gram 행렬의 역제곱근으로 가장 가까운 정규직교 frame을 만든다.
- 최대 국소화는 고정 부분공간에서 위치 spread를 최소화한다. Löwdin의 최소 거리 조건과 목적 함수가 다르다.
- Disentanglement는 더 큰 후보 공간에서 $J$차원 부분공간을 고르는 단계이며, frozen window는 반드시 포함할 고유상태를 지정한다.
- 최종 검증은 rank와 spread, 원래 band와의 일치, 새 점에서의 interpolation, 후속 연산자 계산을 나누어 수행한다.

## 8. 참고문헌

1. N. Marzari, A. A. Mostofi, J. R. Yates, I. Souza, and D. Vanderbilt, “Maximally localized Wannier functions: Theory and applications,” *Reviews of Modern Physics* **84**, 1419–1475 (2012). [DOI: 10.1103/RevModPhys.84.1419](https://doi.org/10.1103/RevModPhys.84.1419). [Author-hosted full text](https://www.physics.rutgers.edu/~dhv/pubs/local_copy/mar_rmp.pdf).

2. J. Kuneš, “Wannier Functions and Construction of Model Hamiltonians,” in *The LDA+DMFT approach to strongly correlated materials*, E. Pavarini, E. Koch, D. Vollhardt, and A. Lichtenstein (eds.), Modeling and Simulation Vol. 1, Forschungszentrum Jülich (2011), Chapter 4. ISBN 978-3-89336-734-4. [Full text](https://www.cond-mat.de/events/correl11/manuscripts/kunes.pdf).

3. K. Koepernik, O. Janson, Y. Sun, and J. van den Brink, “Symmetry-conserving maximally projected Wannier functions,” *Physical Review B* **107**, 235135 (2023). [DOI: 10.1103/PhysRevB.107.235135](https://doi.org/10.1103/PhysRevB.107.235135). [Inspected preprint: arXiv:2111.09652v1](https://arxiv.org/abs/2111.09652v1) (2021); 본문에서 인용한 절·식 번호는 이 preprint를 따른다.

4. N. J. Higham, “Computing the Polar Decomposition—with Applications,” *SIAM Journal on Scientific and Statistical Computing* **7**, 1160–1174 (1986). [DOI: 10.1137/0907079](https://doi.org/10.1137/0907079). [Author manuscript](https://eprints.maths.manchester.ac.uk/694/1/high86p.pdf).

5. I. Souza, N. Marzari, and D. Vanderbilt, “Maximally localized Wannier functions for entangled energy bands,” *Physical Review B* **65**, 035109 (2001). [DOI: 10.1103/PhysRevB.65.035109](https://doi.org/10.1103/PhysRevB.65.035109). [Full text](https://arxiv.org/abs/cond-mat/0108084). 특히 §III.G의 inner-window 제약을 따른다.

6. Wannier90 developers, “3: Silicon — Disentangled MLWFs,” *Wannier90 Documentation*. [Tutorial](https://wannier90.readthedocs.io/en/latest/tutorials/tutorial_3/). 열람일: 2026-09-22.

7. Wannier90 developers, “Files,” *Wannier90 Documentation*. [User guide](https://wannier90.readthedocs.io/en/latest/user_guide/wannier90/files/). 열람일: 2026-09-22.
