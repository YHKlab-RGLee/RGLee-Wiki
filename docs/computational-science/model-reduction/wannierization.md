---
description: Bloch 공간의 무손실 기저변환과 부분공간 선택을 구분하고, 초기 투영·최대 국소화·Wannier Hamiltonian 보간을 전자구조 차원 축소에 연결한다.
---

# Wannier functions and wannierization

**Wannierization**은 결정 전체에 퍼진 Bloch 상태로부터 격자 주변에 국소적인 Wannier 기저를 구성하는 과정이다. Bloch 표현은 band energy를 읽기에 편하고, 국소 표현은 원자·결합의 성격과 격자 사이의 hopping을 분석하기에 편하다. 또한 작은 Wannier Hamiltonian을 여러 파수에서 재사용하면 매번 큰 전자구조 문제를 풀지 않고 관심 band를 보간할 수 있다.[1][2]

그러나 **국소화 자체가 차원 축소인 것은 아니다.** 고정한 $J$개 band 공간 안의 unitary 회전은 정보를 보존한다. 더 큰 후보 공간에서 $J$차원을 고르는 disentanglement는 표현할 공간을 제한한다. 실공간 hopping을 짧은 범위에서 자르는 일도 별도의 근사이다. 이 세 구분을 바탕으로, 먼저 무손실 변환을 이해한 뒤 초기 기저·공간 선택·최대 국소화·보간 순서로 진행한다.[1][2]

주기적인 단일입자 Hamiltonian을 전제로 한다. [Model reduction fundamentals](fundamentals.md)의 차원 구분과 [Projection methods](projection-methods.md)의 $H_r=V^\dagger HV$, $S_r=V^\dagger SV$를 알고 있으면 충분하다. [Density functional theory](../../computational-materials-science/electronic-structure/density-functional-theory.md)의 Kohn–Sham 상태도 입력으로 사용할 수 있지만, Wannierization이 원래 전자구조 근사 자체를 개선하는 것은 아니다.[1][2]

## 1. Bloch 표현과 국소 표현

### (1) 정규화와 Fourier 쌍

Brillouin zone (BZ)을 균일한 $N_k$개 점으로 나누고, 이에 대응하는 Born–von Kármán 초격자를 사용한다. $\mathbf k$는 파수, $m$은 band 지표, $\varepsilon_{m\mathbf k}$는 고유에너지이다. 계산에 필요한 입력은 다음 고유값 문제의 해이다.[1][2]

$$
\hat H\lvert\psi_{m\mathbf k}\rangle
=\varepsilon_{m\mathbf k}\lvert\psi_{m\mathbf k}\rangle.
$$

이 문서에서는 Bloch 함수 $\psi$를 초격자에서, 주기 부분 $u$를 단위격자에서 정규화한다. 위치를 $\mathbf r$, 격자벡터를 $\mathbf R$이라 하면 두 함수의 관계는 다음과 같다.[1][3]

$$
\psi_{m\mathbf k}(\mathbf r)
=\frac{1}{\sqrt{N_k}}e^{i\mathbf k\cdot\mathbf r}u_{m\mathbf k}(\mathbf r),
\qquad u_{m\mathbf k}(\mathbf r+\mathbf R)=u_{m\mathbf k}(\mathbf r).
$$

$$
\langle\psi_{m\mathbf k}\vert\psi_{n\mathbf k'}\rangle_{\rm sc}
=\delta_{mn}\delta_{\mathbf k\mathbf k'},
\qquad
\langle u_{m\mathbf k}\vert u_{n\mathbf k}\rangle_{\rm cell}=\delta_{mn}.
$$

첨자 $\mathrm{sc}$와 $\mathrm{cell}$은 각각 초격자와 단위격자 적분을 뜻한다. 이후 $\psi$와 trial orbital의 내적은 초격자에서, 이웃 $\mathbf k$점의 $u$ 사이 내적은 같은 단위격자에서 계산한다. 이 구별이 있어야 projection의 정규화와 국소화에 쓰는 중첩을 일관되게 다룰 수 있다.[1][3]

각 $\mathbf k$에서 정규직교하게 선택한 $J$개 Bloch형 상태를 $\psi^{\rm W}_{n\mathbf k}$라 하자. 위첨자 $\rm W$는 Wannier gauge를 뜻하며, 이 상태가 어떻게 정해지는지는 다음 절에서 설명한다. 이 상태들을 Fourier 변환하면 원점 단위격자에 속한 Wannier 함수와 이를 격자벡터 $\mathbf R$만큼 평행이동한 함수들을 얻는다. 함수의 중심은 단위격자 안에서 원자나 결합 위치 등에 놓일 수 있다. 이 정규화에서는 정방향과 역방향에 같은 계수가 붙는다.[1][3]

$$
\lvert w_{n\mathbf R}\rangle
=\frac{1}{\sqrt{N_k}}\sum_{\mathbf k}
 e^{-i\mathbf k\cdot\mathbf R}\lvert\psi^{\rm W}_{n\mathbf k}\rangle.
$$

$$
\lvert\psi^{\rm W}_{n\mathbf k}\rangle
=\frac{1}{\sqrt{N_k}}\sum_{\mathbf R}
 e^{i\mathbf k\cdot\mathbf R}\lvert w_{n\mathbf R}\rangle.
$$

선택 상태들의 정규직교성과 이산 Fourier 변환의 직교관계 때문에 얻어진 함수들은 정규직교한다.[1][3]

$$
\langle w_{m\mathbf R}\vert w_{n\mathbf R'}\rangle
=\delta_{mn}\delta_{\mathbf R\mathbf R'}.
$$

### (2) 차원과 목적

$J$는 만들 Wannier 함수의 수이며 모든 $\mathbf k$에서 같다. 반면 입력에 사용할 band 수 $J_{\mathbf k}$는 에너지 범위를 어떻게 정하는지에 따라 달라질 수 있다. 먼저 관심 상태가 모든 $\mathbf k$에서 다른 band들과 분리된 $J$개 band 집합인지 확인한다. 집합 내부의 교차나 축퇴는 허용한다.[1][2]

| 입력 상태 | 차원 | 필요한 선택 |
| --- | --- | --- |
| 고립된 $J$개 band | $J_{\mathbf k}=J$ | 집합 전체를 유지하고 기저만 바꾼다. |
| 다른 band와 얽힌 관심 상태 | $J_{\mathbf k}\ge J$ | 더 큰 후보 공간에서 $J$차원 공간을 고른다. |

두 번째 경우가 entangled bands이며, 공간을 고르는 과정이 **disentanglement**이다. 여기서 고르는 것은 개별 band 번호 $J$개가 아니라 입력 상태들의 선형결합으로 만드는 공간이다. 예를 들어 관심 orbital 성격이 band 교차와 혼성화 구간에서 여러 고유상태에 나뉘면, 그 성분들을 함께 사용해야 한다. 후보 에너지 범위인 outer window와 반드시 포함할 상태를 정하는 frozen window는 4절에서 다룬다.[1][2][4]

목표 차원은 해석하려는 상태와 에너지 범위에 맞춰 정한다. 적은 수의 함수로 넓은 범위의 모든 band를 재현할 수는 없으며, 후보 band를 충분히 계산했더라도 최종 $J$차원에 무엇을 담을지 결정해야 한다. 따라서 먼저 관심 band의 orbital 성격을 확인하고, 그 성격을 반영하는 trial orbital을 준비한다.[1][2][3]

초격자 전체로 세면 Fourier 변환 전후의 상태 수는 모두 $N_kJ$이다. “단위격자당 $J$개”라는 표현은 무한 결정 전체를 $J$개의 함수로 대체한다는 뜻이 아니다. 한 격자의 $J$개 함수를 모든 격자로 평행이동한 집합이 선택된 Bloch 상태들을 표현한다. 더 큰 atomic orbital (AO) 기저와 비교할 때에야 $J$가 작은 모형의 차원이 될 수 있다.[1][3]

AO도 국소 함수인데 Wannier 기저를 다시 만드는 이유는 선택한 band 공간에 맞춘 정규직교 기저를 얻기 위해서이다. 관심 band에는 여러 원자 orbital의 혼성이 들어 있으므로 Wannier 함수는 원자 orbital 하나와 같을 필요가 없다. 결합 중심의 함수가 될 수도 있고 이웃 원자까지 꼬리를 가질 수도 있다. 따라서 국소적이라는 말은 특정 원자에 완전히 갇혔다는 뜻이 아니며, 남은 꼬리가 Hamiltonian의 먼 hopping에 미치는 영향은 따로 확인한다.[1][2][3]

## 2. Isolated band와 unitary gauge

### (1) 고정 공간의 정보 보존

다른 band와 분리된 $J$개 band 집합을 먼저 생각한다. **Gauge**는 각 $\mathbf k$에서 상태의 위상과 혼합을 정하는 방식이다. 정사각 행렬 $Q(\mathbf k)$가 unitary이면 다음 회전은 동일한 공간의 다른 정규직교 기저를 만든다. $\dagger$는 Hermitian conjugate이며 $I_J$는 $J$차원 단위행렬이다. $J=1$에서는 위상 선택이며, $J>1$에서는 band 사이의 혼합까지 허용한다.[1][2][4]

$$
\lvert\psi^{\rm W}_{n\mathbf k}\rangle
=\sum_{m=1}^{J}\lvert\psi_{m\mathbf k}\rangle Q_{mn}(\mathbf k),
\qquad Q^\dagger Q=QQ^\dagger=I_J.
$$

공간이 유지된다는 말은 projector로 확인할 수 있다. 아래 내적과 ket은 1절의 초격자 정규화를 따른다. $QQ^\dagger=I_J$를 대입하면 회전 전후의 합이 같아진다.[1][4]

$$
\sum_n\lvert\psi^{\rm W}_{n\mathbf k}\rangle
\langle\psi^{\rm W}_{n\mathbf k}\rvert
=\sum_m\lvert\psi_{m\mathbf k}\rangle\langle\psi_{m\mathbf k}\rvert.
$$

입력 에너지를 담은 $J\times J$ 대각행렬을 $E(\mathbf k)$라 하자. 같은 Hamiltonian은 새 기저에서 일반적으로 비대각 행렬이 되지만 고유값 집합은 보존된다.[1][3]

$$
H^{\rm W}(\mathbf k)=Q^\dagger E(\mathbf k)Q,
\qquad \operatorname{spec}H^{\rm W}(\mathbf k)
=\operatorname{spec}E(\mathbf k).
$$

따라서 서로 다른 에너지의 고유상태를 섞어도 계산 결과를 잃지 않는다. 대신 회전한 각 함수는 더 이상 에너지 고유상태가 아니므로, 에너지를 구할 때 $H^{\rm W}$를 다시 대각화한다. 변환된 대각원소 하나를 원래 band energy와 동일시하면 이 차이를 놓친다. $Q$를 고르는 목적은 에너지를 바꾸는 것이 아니라 이웃 $\mathbf k$의 함수들이 매끄럽게 연결되도록 하는 것이다. 점마다 제각각인 위상은 Fourier 합에서 불필요한 진동을 만들고 국소화를 해칠 수 있다.[1][2][3]

다만 이 대수적 정보 보존과 전역적으로 매끄럽고 주기적인 gauge의 존재는 별개의 조건이다. 선택한 공간에 위상적 장애가 있거나 추가 대칭 조건이 국소 기저와 양립하지 않으면 원하는 국소화를 얻지 못할 수 있다. 이후의 표준 절차는 원하는 국소 기저를 허용하는 공간을 대상으로 하며, 고립된 band라는 조건만으로 강한 국소화를 보장하지 않는다.[1][2][3]

### (2) 공통 모형의 회전 예

공통의 세 orbital 교육 모형에서 같은 대수를 검산한다. 행렬 원소와 에너지의 단위는 eV이며 $S=I_3$이다. 이 예에는 위치 연산자나 $\mathbf k$ 격자가 없으므로 **실제 Wannier 함수나 최대 국소화를 구하는 계산이 아니다**. 한 고정 공간에서의 회전과 $3\to2$ 부분공간 선택을 구별하는 검산이다.

$$
H_0=\begin{pmatrix}0&-1&0.3\\-1&0.5&0.4\\0.3&0.4&4\end{pmatrix}\;\mathrm{eV}.
$$

아래 코드는 먼저 $3\times3$ unitary 회전으로 전체 spectrum을 보존한다. 다음으로 정확한 두 저에너지 고유벡터를 열로 갖는 $C_2$를 선택하고 그 안에서 $2\times2$ 회전을 한다. 마지막으로 첫 두 AO 좌표만 남긴 projection과 비교한다. 두 상태를 고른다는 차원만 같아도 선택 공간에 따라 결과가 달라지는 예이다.[1][3][4]

```python
import numpy as np

H0 = np.array([[0., -1., .3], [-1., .5, .4], [.3, .4, 4.]])
e, C = np.linalg.eigh(H0)
theta = 0.37
Q2 = np.array([[np.cos(theta), -np.sin(theta)],
               [np.sin(theta),  np.cos(theta)]])
Q3 = np.eye(3)
Q3[:2, :2] = Q2
C2 = C[:, :2]
V = C2 @ Q2
Vcoord = np.eye(3)[:, :2]
print("full           ", np.linalg.eigvalsh(H0))
print("full rotated   ", np.linalg.eigvalsh(Q3.T @ H0 @ Q3))
print("low two rotated", np.linalg.eigvalsh(V.T @ H0 @ V))
print("two coordinates", np.linalg.eigvalsh(Vcoord.T @ H0 @ Vcoord))
assert np.allclose(np.linalg.eigvalsh(Q3.T @ H0 @ Q3), e)
assert np.allclose(np.linalg.eigvalsh(V.T @ H0 @ V), e[:2])
assert np.allclose(V @ V.T, C2 @ C2.T)
assert np.allclose(V.T @ V, np.eye(2))
assert not np.allclose(V @ V.T, np.eye(3))
```

| 계산 | 행렬 차원 | 고유에너지 (eV) |
| --- | --- | --- |
| 전체 및 전체 회전 | $3\times3$ | $-0.82909176,\ 1.27476220,\ 4.05432956$ |
| 정확한 저에너지 공간 및 내부 회전 | $2\times2$ | $-0.82909176,\ 1.27476220$ |
| 두 AO 좌표만 선택 | $2\times2$ | $-0.78077641,\ 1.28077641$ |

$C_2$ 선택에서 높은 상태 하나가 빠졌으며, 그 뒤의 $Q_2$ 회전은 남은 공간만 보존한다. $VV^\dagger=C_2C_2^\dagger$가 성립해도 이 projector는 $I_3$가 아니다. 또 정확한 저에너지 공간은 전체 문제를 먼저 풀어 얻었으므로 그 자체를 저렴한 해법으로 제시하는 예가 아니다. 실제 Wannierization에서 필요한 매끄러운 공간 선택과 실공간 국소화는 이제 설명할 별도의 단계이다.[1][3][4]

## 3. Trial orbital과 초기 기저

### (1) Trial orbital의 투영

Trial orbital $\lvert g_n\rangle$은 원하는 함수의 중심과 성격을 지정하는 초기 추정이다. 원자 중심의 $d$ orbital이나 결합 중심 함수 등을 사용할 수 있다. Trial orbital이 완성된 Wannier 함수와 정확히 같거나 서로 직교할 필요는 없다. Projection은 이 함수 중 입력 band로 표현할 수 있는 성분을 추출한다.[1][2][3]

각 $\mathbf k$에서 입력 Bloch 상태와 $J$개 trial orbital 사이의 복소 내적을 계산한다. 이를 행렬 $A$에 담으면 행은 입력 band, 열은 trial orbital에 대응한다.[1][3]

$$
A_{mn}(\mathbf k)=\langle\psi_{m\mathbf k}\vert g_n\rangle,
\qquad A(\mathbf k)\in\mathbb C^{J_{\mathbf k}\times J}.
$$

투영된 함수 $\phi_{n\mathbf k}$는 이 계수로 입력 상태들을 합한 것이다.

$$
\lvert\phi_{n\mathbf k}\rangle
=\sum_{m=1}^{J_{\mathbf k}}\lvert\psi_{m\mathbf k}\rangle A_{mn}(\mathbf k).
$$

$A_{mn}$에는 진폭과 위상이 모두 들어 있다. 따라서 orbital 성격을 나타내는 $\lvert A_{mn}\rvert^2$만 저장하면 함수의 선형결합을 복원할 수 없다. 또한 서로 다른 trial orbital을 투영해도 같은 band 성분이 남을 수 있으므로, $\phi$들은 일반적으로 정규직교하지 않다.[1][3]

투영된 함수들의 중첩을 모은 Gram 행렬 $G$는 AO basis의 중첩 $S$와 다른 행렬이며, 다음과 같다.[1][3]

$$
G_{mn}(\mathbf k)=\langle\phi_{m\mathbf k}\vert\phi_{n\mathbf k}\rangle,
\qquad G=A^\dagger A.
$$

각 함수를 자기 norm으로 나누면 대각 성분은 1이 되지만, 서로 다른 함수 사이의 중첩은 남는다. Löwdin symmetric orthogonalization은 이 중첩까지 함께 제거한다.[1][2][3]

### (2) Löwdin symmetric orthogonalization

$A$의 열들이 선형독립이면 $G$의 고유값 $s_a$는 모두 양수이다. 고유벡터를 열로 모은 unitary 행렬을 $Z$라 할 때, $G$와 그 양의 역제곱근은 다음과 같다. 역제곱근은 각 원소에 적용하는 연산이 아니라 고유값에 적용하는 행렬 함수이다.[1][3]

$$
G=Z\,\operatorname{diag}(s_1,\ldots,s_J)Z^\dagger,
\qquad
G^{-1/2}=Z\,\operatorname{diag}(s_1^{-1/2},\ldots,s_J^{-1/2})Z^\dagger.
$$

이 행렬을 곱하면 정규직교 초기 기저 $\zeta_{n\mathbf k}$의 Bloch 계수 $B_0$를 얻는다.[1][3]

$$
B_0=A G^{-1/2},
\qquad
\lvert\zeta_{n\mathbf k}\rangle
=\sum_{m=1}^{J_{\mathbf k}}\lvert\psi_{m\mathbf k}\rangle (B_0)_{mn}(\mathbf k).
$$

정규직교성은 원래 Bloch 상태의 정규직교성과 $G=A^\dagger A$를 대입해 확인할 수 있다.

$$
B_0^\dagger B_0=G^{-1/2}GG^{-1/2}=I_J,
\qquad
\langle\zeta_{m\mathbf k}\vert\zeta_{n\mathbf k}\rangle=\delta_{mn}.
$$

$J_{\mathbf k}=J$이면 $B_0$는 정사각 unitary 행렬이므로 입력 공간 전체를 유지한다. $J_{\mathbf k}>J$이면 $B_0$는 열이 정규직교인 직사각 행렬이며, 더 큰 입력 공간 안의 $J$차원만 선택한다. 이 경우에는 $B_0^\dagger B_0=I_J$여도 $B_0B_0^\dagger$가 입력 공간의 단위행렬이 되지 않는다.[1][3][4]

아래 점검은 역제곱근 식의 직접적인 결과이다. $s_a=0$이면 역제곱근이 존재하지 않고, 매우 작은 $s_a$는 거의 투영되지 않은 성분을 크게 증폭한다. 수치적인 허용 기준은 입력의 정밀도와 필요한 정확도에 맞춰 정해야 한다.[1][3]

| 관찰 | 의미 | 먼저 확인할 항목 |
| --- | --- | --- |
| $J_{\mathbf k}<J$ | 목표 차원만큼 상태가 없다. | 계산한 band 수와 후보 범위 |
| $s_a=0$ | 투영된 함수들이 선형종속이다. | 중복된 trial orbital, 빠진 orbital 성격 |
| 매우 작은 $s_a$ | 어떤 성분이 입력 공간에 거의 없다. | Trial orbital의 위치·방향과 후보 범위 |
| 정규직교하지만 넓게 퍼진 함수 | 직교화는 끝났지만 국소화는 충분하지 않다. | 다음 단계의 공간 선택과 기저 회전 |

여기까지의 출력 $B_0$는 **정규직교 초기 기저**이다. Projection만으로 목적에 맞는 Wannier 함수를 얻는 방법도 있지만, 이 결과가 위치 분산을 최소화했다는 뜻은 아니다. 고립된 band에서는 정사각 $B_0$를 $Q$의 초기값으로 쓰고, entangled bands에서는 먼저 부분공간 선택의 초기값으로 사용한다.[1][2][3]

## 4. Entangled bands와 disentanglement

### (1) Outer·frozen window

Disentanglement는 $J_{\mathbf k}$개 후보 상태에서 $J$차원 공간을 고른다. 선택 행렬 $D(\mathbf k)$의 크기는 $J_{\mathbf k}\times J$이며, 선택된 상태들이 정규직교하도록 열에 조건을 둔다.[2][4][5]

$$
\lvert\psi^{\rm opt}_{n\mathbf k}\rangle
=\sum_{m=1}^{J_{\mathbf k}}\lvert\psi_{m\mathbf k}\rangle D_{mn}(\mathbf k),
\qquad D^\dagger D=I_J.
$$

Outer window는 이 선형결합에 사용할 고유상태의 에너지 범위이다. Frozen window는 후보 중 최종 공간에 반드시 포함할 고유상태를 지정한다. 입력점마다 frozen 상태 수가 $J_f(\mathbf k)$개라면 다음 차원 조건이 필요하다.[4][5]

$$
J_f(\mathbf k)\le J\le J_{\mathbf k}
\qquad\text{모든 입력 }\mathbf k\text{에서}.
$$

Frozen 상태를 포함한다는 것은 그 상태가 최종 기저의 특정 함수 하나와 같다는 뜻이 아니다. $J$개 선택 상태의 선형결합으로 그 고유상태를 정확히 표현할 수 있다는 뜻이다. 따라서 같은 입력 Hamiltonian을 사용하면 해당 고유에너지가 선택 공간의 Hamiltonian에도 남는다.[4][5]

| 에너지 범위 | 공간 선택 조건 | 입력점에서의 의미 |
| --- | --- | --- |
| Frozen window 안 | 해당 고유상태를 반드시 포함 | 해당 고유에너지 보존 |
| Outer 안, frozen 밖 | 필요한 선형결합을 선택 | 개별 band의 정확한 보존은 요구하지 않음 |
| Outer 밖 | 후보에서 제외 | 이 모형이 자동으로 표현하지 않음 |

이 표의 보존은 입력 $\mathbf k$점에서의 조건이다. 아직 계산하지 않은 점은 6절의 Fourier 보간으로 구하므로 별도로 정확도를 확인한다. 또 단순히 $B_0$를 계산했다고 frozen 조건까지 충족되는 것은 아니다. Frozen 상태를 먼저 포함하고 나머지 방향을 선택하는 등, 해당 제약을 만족하도록 초기 공간과 반복 최적화를 구성해야 한다.[4][5]

### (2) 이웃 공간의 연결

선택 기준은 이웃 $\mathbf k$점에서 공간이 가능한 한 매끄럽게 이어지도록 하는 것이다. 비교에는 Bloch 함수 전체가 아니라 단위격자 주기 부분 $u$를 사용한다. $\mathbf b$를 이웃 점으로 향하는 벡터라 하면, 원래 입력 상태들의 중첩은 다음과 같다.[2][5]

$$
M^{\rm B}_{mn}(\mathbf k,\mathbf b)
=\langle u_{m\mathbf k}\vert u_{n,\mathbf k+\mathbf b}\rangle_{\rm cell}.
$$

선택된 주기 부분을 $u^{\rm opt}$라 하고, 그 공간의 projector를 $P_{\mathbf k}$로 정의한다. 이 연산자는 같은 단위격자 함수 공간에서 이웃 점끼리 비교한다.[2][4][5]

$$
P_{\mathbf k}=\sum_{n=1}^{J}
\lvert u^{\rm opt}_{n\mathbf k}\rangle\langle u^{\rm opt}_{n\mathbf k}\rvert.
$$

두 공간이 얼마나 다른지는 다음 trace로 나타낼 수 있다. $\operatorname{Tr}$는 단위격자 함수 공간에서 취한다.[2][5]

$$
\mathcal T_{\mathbf k,\mathbf b}
=\operatorname{Tr}\!\left[P_{\mathbf k}(1-P_{\mathbf k+\mathbf b})\right]
=J-\operatorname{Tr}\!\left[P_{\mathbf k}P_{\mathbf k+\mathbf b}\right].
$$

두 공간이 같으면 $\mathcal T=0$이고, 일치하지 않는 방향이 있으면 양수이다. 표준적인 두 단계 방법은 이 차이를 격자 전체에서 가중 평균한 $\Omega_{\rm I}$를 먼저 줄인다.[2][4][5]

$$
\Omega_{\rm I}^{\rm mesh}
=\frac{1}{N_k}\sum_{\mathbf k,\mathbf b}
 w_{\mathbf b}\mathcal T_{\mathbf k,\mathbf b}.
$$

$w_{\mathbf b}$는 이웃 격자의 기하에 따라 정한 유한차분 가중치이며 길이 제곱의 차원을 갖는다. $\Omega_{\rm I}^{\rm mesh}$는 연속 $\mathbf k$ 공간에서 정의한 spread의 한 성분을 유한 격자로 근사한 값이다. 선택 공간을 나타내는 $D$를 조절하되 frozen 조건은 유지한다.[2][4][5]

이 단계가 끝나면 $J$차원 공간이 정해진다. 그러나 같은 공간 안에서도 개별 기저 함수의 위상과 혼합은 여전히 자유롭다. 따라서 공간을 고정한 뒤, 다음 단계에서 그 자유도를 이용해 함수들을 국소화한다. 고립된 band에서는 이미 공간이 정해져 있으므로 이 절의 최적화를 건너뛴다.[2][4][5]

## 5. Maximally localized Wannier functions

### (1) Spread와 gauge

선택 공간이 정해진 뒤에는 $D$를 고정하고 그 안의 정사각 unitary 행렬 $Q$만 조절한다. 전체 Bloch 계수 변환은 아래와 같다. Isolated $J$-band 집합에서는 $D=I_J$이며, entangled bands에서는 $D$가 직사각 행렬이다.[1][3][4]

$$
T(\mathbf k)=D(\mathbf k)Q(\mathbf k),\qquad
T^\dagger T=I_J,\qquad TT^\dagger=DD^\dagger.
$$

$$
\lvert\psi^{\rm W}_{n\mathbf k}\rangle
=\sum_{m=1}^{J_{\mathbf k}}\lvert\psi_{m\mathbf k}\rangle T_{mn}(\mathbf k).
$$

이 상태를 1절의 Fourier 쌍에 넣어 Wannier 함수를 만든다. 같은 $D$에서도 $Q$에 따라 함수의 중심과 모양은 달라지므로, 어느 gauge를 선택할지 수량적인 기준이 필요하다.[1][2][4]

Maximally localized Wannier functions (MLWFs)는 함수들의 위치 분산 합인 **spread**를 최소화하는 기준으로 구한다. 원점 격자에 있는 함수의 중심을 $\bar{\mathbf r}_n$, 이차 모멘트를 $\langle r^2\rangle_n$이라 쓰면 다음과 같다.[1][2][4]

$$
\bar{\mathbf r}_n=\langle w_{n\mathbf0}\vert\mathbf r\vert w_{n\mathbf0}\rangle,
\qquad
\langle r^2\rangle_n=\langle w_{n\mathbf0}\vert r^2\vert w_{n\mathbf0}\rangle.
$$

$$
\Omega=\sum_{n=1}^{J}
\left(\langle r^2\rangle_n-\lvert\bar{\mathbf r}_n\rvert^2\right).
$$

$\Omega$의 차원은 길이 제곱이다. 함수가 좌표 원점에서 얼마나 멀리 있는지가 아니라 자기 중심 주위에서 얼마나 퍼지는지를 측정한다. 위 실공간 정의는 국소화된 함수의 무한 결정 극한을 기준으로 한다. 유한 격자 계산에서는 주기 경계를 반영한 중첩 식으로 이를 근사한다.[1][2]

Spread는 선택 공간에만 의존하는 $\Omega_{\rm I}$와, 그 공간 안의 기저에 의존하는 $\widetilde\Omega$로 나뉜다.[1][2][4]

$$
\Omega=\Omega_{\rm I}+\widetilde\Omega,
\qquad \widetilde\Omega=\Omega_{\rm D}+\Omega_{\rm OD}.
$$

4절에서 줄인 것은 첫 성분의 격자 근사이다. 이제 $D$를 고정했으므로 $\Omega_{\rm I}$는 변하지 않고, $Q$를 바꿔 $\widetilde\Omega$를 줄인다. $\Omega_{\rm D}$와 $\Omega_{\rm OD}$는 각각 대각 및 비대각 중첩과 관련된 성분이다. 다음 표는 각 단계가 실제로 바꾸는 대상을 정리한 것이다.[1][2][4]

| 단계 | 바꾸는 대상 | 직접 만족시키는 조건 |
| --- | --- | --- |
| Löwdin 직교화 | 투영된 함수들의 혼합 | 정규직교성 |
| Disentanglement | 후보 공간 안의 $J$차원 공간 | Frozen 포함과 이웃 공간의 연결 |
| 최대 국소화 | 고정된 공간 안의 기저 | 위치 spread 감소 |

### (2) 중첩·격자·국소 최솟값

실제로는 Wannier 함수를 매번 실공간에 그리지 않고, 이웃 상태 사이의 중첩으로 중심과 spread를 계산한다. 4절의 입력 중첩 $M^{\rm B}$를 최종 기저로 변환하면 다음과 같다. 왼쪽 변환은 $\mathbf k$, 오른쪽 변환은 이웃 $\mathbf k+\mathbf b$에 속한다.[1][2][4]

$$
M^{\rm W}(\mathbf k,\mathbf b)
=T^\dagger(\mathbf k)M^{\rm B}(\mathbf k,\mathbf b)T(\mathbf k+\mathbf b).
$$

같은 유한차분 규약에서 중심과 spread의 기저 의존 성분은 아래와 같이 근사한다. $\operatorname{Im}\ln M^{\rm W}_{nn}$은 대각 중첩의 위상이며, $\Omega_{\rm D}$와 $\Omega_{\rm OD}$의 정의는 바로 앞 분해식과 대응한다. 가중치는 좌표 성분 $\alpha,\beta$에 대해 $\sum_{\mathbf b}w_{\mathbf b}b_\alpha b_\beta=\delta_{\alpha\beta}$가 되도록 격자 기하에 맞춘다.[1][2][4]

$$
\bar{\mathbf r}_n\simeq-\frac{1}{N_k}
\sum_{\mathbf k,\mathbf b}w_{\mathbf b}\mathbf b\,
\operatorname{Im}\ln M^{\rm W}_{nn}(\mathbf k,\mathbf b).
$$

$$
\Omega_{\rm D}\simeq\frac{1}{N_k}\sum_{\mathbf k,\mathbf b}w_{\mathbf b}
\sum_n\left[\operatorname{Im}\ln M^{\rm W}_{nn}(\mathbf k,\mathbf b)
+\mathbf b\cdot\bar{\mathbf r}_n\right]^2.
$$

$$
\Omega_{\rm OD}\simeq\frac{1}{N_k}\sum_{\mathbf k,\mathbf b}w_{\mathbf b}
\sum_{m\ne n}\lvert M^{\rm W}_{mn}(\mathbf k,\mathbf b)\rvert^2.
$$

첫 성분은 중심 위치로 설명되지 않는 대각 위상 변화를 측정하고, 둘째 성분은 이웃 점에서 서로 다른 함수 지표 사이에 남은 중첩을 측정한다. BZ 경계를 넘는 이웃도 주기 경계에 맞춰 연결하고, 복소 로그의 위상 선택을 일관되게 유지해야 한다. 격자 간격을 줄였을 때 중심과 spread가 수렴하는지도 확인한다.[1][2]

반복 최적화는 unitary 조건을 유지하면서 $Q$를 갱신한다. Spread의 변화가 작아져도 전역 최솟값에 도달했다는 보장은 없다. 초기 trial orbital을 바꾸어 얻은 중심, 함수 모양과 spread를 비교하면 다른 국소 최솟값에 도달했는지 점검할 수 있다. 또한 표준적인 두 단계 방법은 공간과 기저를 차례로 최적화하므로, 둘을 동시에 바꾸는 모든 가능한 해 중 최저 spread를 보장하지 않는다.[1][4]

## 6. Wannier Hamiltonian과 band interpolation

### (1) AO 공간과 선택 공간의 대응

최종 $T$가 정해지면 고유에너지를 Wannier 기저로 변환한다. 입력 band의 에너지 대각행렬을 $E(\mathbf k)$라 하면 다음과 같다.[1][3]

$$
E(\mathbf k)=\operatorname{diag}
(\varepsilon_{1\mathbf k},\ldots,\varepsilon_{J_{\mathbf k}\mathbf k}),
\qquad
H^{\rm W}(\mathbf k)=T^\dagger(\mathbf k)E(\mathbf k)T(\mathbf k).
$$

$H^{\rm W}$는 $J\times J$ Hermitian 행렬이며 에너지 단위를 갖는다. 고립된 band의 정사각 unitary 변환에서는 모든 입력 고유값이 보존된다. 직사각 $T$를 쓰면 더 큰 Hamiltonian을 선택 공간에 제한한 것이므로, frozen 조건으로 포함한 상태 이외의 고유값은 원래 band와 달라질 수 있다.[1][3][4]

이를 원래 AO 공간에서 보면 [Projection methods](projection-methods.md)의 식과 직접 이어진다. 각 $\mathbf k$에서 원래 basis 크기를 $M$, 후보 Bloch 계수 열을 모은 행렬을 $C_B\in\mathbb C^{M\times J_{\mathbf k}}$라 하자. $H$와 $S$는 각각 AO 함수 사이의 Hamiltonian과 중첩을 이미 조립한 행렬이다. $S$가 양의 정부호이며 입력 고유벡터가 $S$-정규직교라면 다음이 성립한다.[3][6]

$$
HC_B=SC_BE,\qquad C_B^\dagger SC_B=I_{J_{\mathbf k}},
\qquad C_B^\dagger HC_B=E.
$$

공통 문서의 reduced basis $V$는 선택과 회전을 모두 AO 계수에 반영한 행렬이다. 따라서 크기는 $M\times J$이며 다음 두 경로가 같은 Hamiltonian을 준다.[1][3][6]

$$
V(\mathbf k)=C_B(\mathbf k)D(\mathbf k)Q(\mathbf k)=C_BT.
$$

$$
H_r=V^\dagger HV=T^\dagger ET=H^{\rm W},
\qquad S_r=V^\dagger SV=T^\dagger T=I_J.
$$

여기서 $S$를 $V^\dagger SHV$처럼 한 번 더 넣지 않는다. 이미 $H_{\alpha\beta}=\langle\chi_{\alpha\mathbf k}|\hat H|\chi_{\beta\mathbf k}\rangle$로 조립한 행렬이므로 양쪽 계수만 변환한다. 반면 내적과 정규화에는 $S_{\alpha\beta}=\langle\chi_{\alpha\mathbf k}|\chi_{\beta\mathbf k}\rangle$가 들어간다. 여기서 $\chi_{\alpha\mathbf k}$는 AO의 Bloch sum이며 $\alpha$는 AO 지표이다.[3][6]

| 행렬 | 크기 | 역할 |
| --- | --- | --- |
| $C_B$ | $M\times J_{\mathbf k}$ | AO에서 후보 Bloch 고유상태를 표현 |
| $D$ | $J_{\mathbf k}\times J$ | 후보 중 표현할 부분공간 선택 |
| $Q$ | $J\times J$ | 고정 공간 안의 unitary gauge |
| $T=DQ$ | $J_{\mathbf k}\times J$ | 최종 Wannier gauge의 Bloch 계수 |
| $V=C_BT$ | $M\times J$ | 공통 projection 식에 넣을 AO 계수 |

예를 들어 $M=30$인 AO basis에서 이미 고립된 두 band만 $C_B$에 넣었다면, $J_{\mathbf k}=J=2$이고 $D=I_2$이다. $Q$는 두 band의 정보를 모두 보존하지만 원래 30차원과 비교한 $V$는 2차원 모형이다. 이 경우 차원 축소는 band를 입력으로 고른 단계에 있고, 그 뒤의 최대 국소화에 있지 않다. 반대로 여섯 후보 band에서 세 함수를 만드는 경우에는 $D$ 자체가 $6\times3$이며 disentanglement도 공간을 줄인다. 이 숫자들은 행렬 크기를 설명하는 가정이며 물질의 계산 결과가 아니다.[1][3][4]

### (2) 실공간 hopping과 보간

실공간 행렬 $H_{mn}(\mathbf R)$는 원점의 $m$번째 함수와 $\mathbf R$ 격자의 $n$번째 함수 사이의 Hamiltonian 행렬원소이다. 대각 성분과 격자 간 hopping을 포함하며, 다음 Fourier 변환으로 계산한다.[1][3]

$$
H_{mn}(\mathbf R)
=\langle w_{m\mathbf0}\vert\hat H\vert w_{n\mathbf R}\rangle
=\frac{1}{N_k}\sum_{\mathbf k}e^{-i\mathbf k\cdot\mathbf R}
H^{\rm W}_{mn}(\mathbf k).
$$

새 파수 $\mathbf q$에서는 반대 부호의 Fourier 합으로 행렬을 구성하고 대각화한다. 여기서는 각 격자 방향의 점 수가 홀수인 $\Gamma$ 포함 균일 mesh와, 원점을 중심으로 $\pm\mathbf R$가 짝을 이루는 완전한 실공간 대표집합을 가정한다. 이 경우 아래 가중치 없는 합이 Hermitian 보간 행렬을 주며, 그 고유값이 보간한 band이다.[1][3]

$$
H^{\rm W}_{\rm int}(\mathbf q)
=\sum_{\mathbf R}e^{i\mathbf q\cdot\mathbf R}H(\mathbf R).
$$

입력 격자와 대응하는 모든 독립 $\mathbf R$ 성분을 유지하면 이산 Fourier 역변환은 입력 $H^{\rm W}$를 복원한다. 반면 새로운 $\mathbf q$에서의 값은 보간 결과이다.[1][3]

Hermitian Hamiltonian과 병진 대칭으로부터 다음 관계도 얻는다. 실공간 데이터를 읽거나 일부 hopping을 절단할 때 확인할 수 있는 조건이다.[1][3]

$$
H_{mn}(\mathbf R)=H_{nm}^{*}(-\mathbf R).
$$

잘 국소화된 기저에서는 먼 격자 사이의 행렬원소가 작아져 짧은 범위의 모형을 만들기 유리하다. 그러나 남길 hopping의 범위를 줄이면 추가 근사가 생긴다. 또한 유한 $\mathbf k$ 격자는 실공간의 초격자 주기와 연결되므로, 함수와 그 주기적 복사본의 중첩이 충분히 작은지 확인해야 한다. 보간 오차는 hopping 범위와 입력 격자를 각각 바꾸어 수렴을 확인한다.[1][3]

유한 mesh의 입력점은 초격자 병진으로 동등한 $\mathbf R$들을 구별하지 못한다. 따라서 임의의 완전한 대표집합으로 입력점을 복원할 수 있다는 사실만으로 새 $\mathbf q$에서의 보간이 유일하거나 Hermitian이라고 결론 내릴 수 없다. 위의 $\pm\mathbf R$ 조건은 hopping 절단 이전부터 필요하다. 짝수 mesh 등에서 경계의 동등한 격자벡터를 함께 쓰는 경우에는, 같은 초격자 병진류의 가중치 합을 1로 하고 conjugate 짝에도 일관된 가중치를 주는 등 경계를 처리해야 한다. 이때 위 단순합은 해당 가중합으로 바뀐다. 이는 Fourier 복원식과 실공간 image 가중 규약에서 얻는 조건이다.[1][3]

특히 hopping을 자를 때는 $\mathbf R$와 $-\mathbf R$의 Hermitian conjugate 관계를 함께 유지한다. 한쪽만 없애면 Hermitian 성질을 잃을 수 있다는 것은 위 관계의 직접적인 결과이다. Gauge를 바꾸면 개별 hopping은 달라질 수 있으므로, 동일한 범위 절단이라도 band 오차는 다시 검증한다. 작아진 spread는 짧은 범위 표현에 유리한 특성이지 특정 cutoff에서의 band 오차에 대한 인증값은 아니다.[1][3][4]

## 7. 차원 축소와 정확도 검증

### (1) 선택·국소화·보간 오차

검증은 초기 기저, 선택 공간, 국소화, Fourier 보간을 나누어 수행한다. 아래 표는 앞의 조건과 변환식에서 얻은 점검 순서이다. 모든 재료에 적용할 오차 기준 하나를 정하기보다, 관심 에너지 범위와 후속 계산에 필요한 정확도를 먼저 정한다.[1][3][4]

| 확인 단계 | 비교할 양 | 불일치 시 우선 점검 |
| --- | --- | --- |
| 초기 기저 | $G$의 고유값, $B_0^\dagger B_0$ | Trial orbital, 후보 band, 정규화 |
| 공간 선택 | 차원 조건과 frozen 상태 포함 | Outer/frozen window, 목표 $J$ |
| 국소화 | 개별 spread, 중심, 함수 모양 | 초기값, 반복 수렴, 격자 간격 |
| 입력점의 고유값 | $T^\dagger ET$와 원래 band | 선택 공간이 관심 상태를 포함하는지 |
| Fourier 역변환 | 입력 $H^{\rm W}$와 복원한 행렬 | 부호, 가중치, hopping 절단 |
| 새 점의 band | 보간값과 별도 직접 계산 | 입력 격자와 실공간 범위 |

특히 **선택 공간에서 생긴 차이와 보간에서 생긴 차이를 구별**해야 한다. 입력점의 $T^\dagger ET$부터 관심 고유값을 재현하지 못하면, 이후 Fourier 변환을 정확하게 수행해도 그 차이는 남는다. 반대로 입력점이 잘 맞아도 그 사이에 급격한 band 변화가 있으면 격자가 충분한지 별도 확인해야 한다.[1][3][4]

Band 비교는 같은 에너지 기준과 같은 비교 대상을 사용한다. 입력에 쓰지 않은 $\mathbf q$점에서 직접 계산한 결과와 비교하면 보간의 정확도를 평가할 수 있다. 교차 부근에서는 단순한 band 번호 대응이 불명확할 수 있으므로, 비교하려는 고유값 집합과 orbital 성격을 함께 확인한다. 이는 선택 공간과 band 재현을 구분한 앞의 원칙을 실제 검증에 적용한 것이다.[1][2][3]

### (2) 관측량·전하·DFT 한계

Wannier 함수 하나의 모양과 hopping 하나의 값은 선택한 공간과 gauge에 의존한다. 따라서 서로 다른 $J$, trial orbital 또는 에너지 범위를 사용한 계산에서 spread 숫자만 비교해 어느 모형이 더 정확하다고 판단할 수 없다. 비교 목적이 band 재현인지, 특정 orbital 성격인지 먼저 정하고 해당 결과를 확인해야 한다.[1][2][3]

Hamiltonian 외의 연산자 행렬이 필요한 후속 계산에서는 그 행렬도 같은 기저로 변환해야 한다. 같은 $\mathbf k$를 보존하는 연산자 $\hat O$의 입력 행렬을 $O^{\rm B}$라 하면 다음과 같다.[1][3]

$$
O^{\rm W}(\mathbf k)=T^\dagger(\mathbf k)O^{\rm B}(\mathbf k)T(\mathbf k).
$$

따라서 band 고유값이 잘 맞는다는 확인만으로 모든 응답의 정확도가 검증되는 것은 아니다. 필요한 행렬원소와 최종 물리량의 수렴도 확인한다.[1][3]

Band 고유값만으로 충분하지 않은 이유는 점유 상태로부터 밀도를 만드는 식에서도 확인할 수 있다. Density functional theory (DFT)의 밀도는 파동함수와 점유수에 의존하고, self-consistent field (SCF) 계산은 그 밀도로 Hamiltonian을 갱신한다. 아래 식은 이를 드러내기 위한 초격자 표기이다. $f_{m\mathbf k}$는 spin 계수까지 포함한 입력 상태의 점유수이며, $\psi$는 1절의 초격자 정규화를 따른다.[6][7]

$$
n(\mathbf r)=\sum_{m,\mathbf k} f_{m\mathbf k}
|\psi_{m\mathbf k}(\mathbf r)|^2.
$$

완전하게 보존한 공간에서 기저를 회전하더라도 점유수 행렬은 함께 변환해야 한다. 같은 $\mathbf k$에서 입력 점유수 행렬을 $F^{\rm B}=\operatorname{diag}(f_{m\mathbf k})$라 하면, 정사각 $Q$에 대해서는 $F^{\rm W}=Q^\dagger F^{\rm B}Q$이다. 입력 함수들을 행벡터 $\Psi$로 모아 쓰면 다음 항등식으로 밀도 기여의 보존을 확인할 수 있다. 이는 연산자 기저변환과 점유상태 밀도식에서 직접 얻는 결론이다.[3][6][7]

$$
(\Psi Q)F^{\rm W}(\Psi Q)^\dagger
=\Psi F^{\rm B}\Psi^\dagger.
$$

모두 같은 점유수를 가진 공간에서는 $F^{\rm B}$가 단위행렬에 비례하므로 단순해진다. 그러나 점유·비점유 상태를 섞거나 부분 점유가 다르면 $F^{\rm W}$를 처음의 대각 점유수와 같다고 둘 수 없다. 직사각 $T$로 공간을 줄인 경우에는 제외한 상태의 밀도 기여까지 이 항등식으로 되살릴 수 없다. 따라서 좁은 energy window의 band가 맞는다는 사실은 전체 점유공간이나 총전하가 정확하다는 뜻이 아니다.[3][6][7]

같은 이유로 고정 $H$에서의 band 보간 검증만으로 total energy, 원자 힘 또는 SCF 수렴의 정확도를 인증할 수 없다는 것이 이 문서의 적용 범위상 결론이다. 총에너지에는 밀도 의존 항이 있고, 힘에는 에너지의 구조 의존성과 기저 변화가 관계한다. 그 용도로 축소 모형을 쓰려면 밀도·점유수·Hamiltonian 갱신과 해당 관측량을 일관되게 구성해 직접 비교해야 한다. 이 문서의 예와 표준 Wannier 보간은 그러한 SCF 축소 알고리즘까지 제공하지 않는다.[6][7]

계산 비용도 준비와 재사용으로 나누어 해석한다. 입력 Bloch 상태의 계산, 중첩 계산, 공간 선택과 국소화에는 준비 비용이 든다. 이후의 이점은 저장한 hopping으로 새 파수에서 $J\times J$ 행렬을 만들고 대각화할 수 있다는 데 있다. 따라서 작은 $J$만 보고 최초 DFT 계산까지 같은 비율로 빨라진다고 해석하지 않는다. 후속 수송 문제에서 기저를 더 줄이는 방법은 [NEGF: Mode-space reduction](mode-space-reduction.md)으로 이어진다.[1][3]

재현 가능한 계산 기록에는 원래 전자구조 계산, $\mathbf k$ 격자, 목표 $J$, trial orbital의 중심과 방향, outer/frozen window, 수렴 기준, 남긴 hopping 범위를 포함한다. 최종 spread와 함께 입력에 쓰지 않은 점의 band 비교도 보관하면, 공간 선택과 보간 중 어느 단계가 결과를 제한하는지 다시 확인할 수 있다.[1][3][4]

## 8. 요약

- 고정된 isolated $J$-band 공간에서 unitary gauge와 Fourier 변환은 정보를 보존한다. 국소화 자체는 차원 축소가 아니다.
- Trial projection과 Gram 행렬 $G$의 Löwdin 직교화는 초기 기저를 만들며, spread 최소화와는 다른 단계이다.
- Entangled bands에서는 $D$가 부분공간을 선택하고, frozen 조건을 유지한 그 공간 안에서 $Q$가 기저를 회전한다.
- AO 공간의 $V=C_BDQ$는 $H_r=V^\dagger HV=T^\dagger ET$, $S_r=I_J$를 주며, 원래 AO 수보다 작은 Wannier 모형의 위치를 분명히 한다.
- 공간 선택, 국소화, hopping 절단과 새 파수의 보간을 각각 검증한다. Band 일치는 전하·총에너지·힘·SCF 정확도를 대신하지 않는다.

## 9. 참고문헌

1. N. Marzari, A. A. Mostofi, J. R. Yates, I. Souza, and D. Vanderbilt, “Maximally localized Wannier functions: Theory and applications,” *Reviews of Modern Physics* **84**, 1419–1475 (2012). [DOI: 10.1103/RevModPhys.84.1419](https://doi.org/10.1103/RevModPhys.84.1419). [Full text: arXiv:1112.5411](https://arxiv.org/pdf/1112.5411).

2. J. Kuneš, “Wannier Functions and Construction of Model Hamiltonians,” in *The LDA+DMFT approach to strongly correlated materials*, E. Pavarini, E. Koch, D. Vollhardt, and A. Lichtenstein (eds.), Modeling and Simulation Vol. 1, Forschungszentrum Jülich (2011), Chapter 4. ISBN 978-3-89336-734-4. [Full text](https://www.cond-mat.de/events/correl11/manuscripts/kunes.pdf).

3. K. Koepernik, O. Janson, Y. Sun, and J. van den Brink, “Symmetry-conserving maximally projected Wannier functions,” *Physical Review B* **107**, 235135 (2023). [DOI: 10.1103/PhysRevB.107.235135](https://doi.org/10.1103/PhysRevB.107.235135). [Inspected preprint: arXiv:2111.09652v1](https://arxiv.org/abs/2111.09652v1) (2021); 본문 근거의 식 번호는 이 preprint를 따른다.

4. A. Damle, A. Levitt, and L. Lin, “Variational Formulation for Wannier Functions with Entangled Band Structure,” *Multiscale Modeling & Simulation* **17**(1), 167–191 (2019). [DOI: 10.1137/18M1167164](https://doi.org/10.1137/18M1167164). [Author-hosted full text](https://math.berkeley.edu/~linlin/publications/VariationWannier.pdf).

5. I. Souza, N. Marzari, and D. Vanderbilt, “Maximally localized Wannier functions for entangled energy bands,” *Physical Review B* **65**, 035109 (2001). [DOI: 10.1103/PhysRevB.65.035109](https://doi.org/10.1103/PhysRevB.65.035109). [Full text](https://arxiv.org/pdf/cond-mat/0108084). 특히 III.A–B와 III.G의 공간 선택·inner window 조건.

6. J. M. Soler et al., “The SIESTA method for ab initio order-N materials simulation,” *Journal of Physics: Condensed Matter* **14**, 2745–2779 (2002). [DOI: 10.1088/0953-8984/14/11/302](https://doi.org/10.1088/0953-8984/14/11/302). [Full text](https://arxiv.org/pdf/cond-mat/0111138). AO·밀도, 총에너지와 힘의 관계.

7. P. Giannozzi et al., “QUANTUM ESPRESSO: a modular and open-source software project for quantum simulations of materials,” *Journal of Physics: Condensed Matter* **21**, 395502 (2009). [DOI: 10.1088/0953-8984/21/39/395502](https://doi.org/10.1088/0953-8984/21/39/395502). [Full text](https://arxiv.org/pdf/0906.2569). Self-consistency와 Appendix A.1–A.2.
