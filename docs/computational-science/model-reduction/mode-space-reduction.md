---
description: 소자 양자 수송에서 쓰이는 mode-space reduction의 기본 원리와 conventional transverse modes, atomistic full-band basis, spurious-band 보정, 이종접합 확장을 설명한다.
---

# Mode-space reduction

**Mode-space reduction**은 양자 수송 계산에서 필요한 전자 상태를 더 적은 수의 기저 함수(mode)로 표현하여 Hamiltonian의 차원을 줄이는 방법이다. 수송 방향으로 소자를 여러 cell 또는 slice로 나누었을 때, 각 slice의 원자 궤도 수가 크면 Green's function 계산 비용도 증가한다. 그러나 관심 에너지 범위의 수송에 모든 궤도가 동등하게 중요하지는 않다. 적절한 부분공간만 남겨 같은 수송 문제를 더 작은 행렬로 근사하는 것이 핵심이다.[1–4]

이 문서는 소자 시뮬레이션에서 널리 쓰이는 방법을 다음 순서로 설명한다.

1. **Conventional mode-space:** 횡방향 구속 문제의 고유모드로 수송 상태를 전개한다.
2. **Atomistic full-band mode-space:** 여러 파수의 Bloch 고유벡터로 작은 공통 기저 $U$를 구성한다.
3. **Basis optimization:** 축소 모형에 나타나는 spurious bands를 검사하고 기저를 보완한다.
4. **Heterostructure mode-space:** 결함·계면이 있는 비주기적 영역에 서로 다른 $U_i$를 적용하고 영역 간 coupling까지 축소한다.

이 네 가지는 동등한 네 개의 독립 알고리즘이 아니다. 첫째와 둘째는 **축소 기저를 만드는 대표적인 접근법**이고, 셋째는 특히 atomistic 방법의 **정확도 개선 단계**, 넷째는 그 방법을 **비균일 소자로 확장하는 구성**이다. 처음에는 직교 기저를 가정하고, 마지막에 SIESTA와 같은 비직교 원자 궤도 기저의 처리를 설명한다.

## 1. Conventional mode-space: 횡방향 고유모드

### 1.1 왜 횡방향 문제를 먼저 푸는가?

Nanowire 또는 MOSFET의 수송 방향을 $x$, 횡방향을 $\mathbf r_\perp=(y,z)$라고 하자. 횡방향 양자 구속이 강하면, 주어진 에너지에서 소수의 낮은 subband만 수송에 크게 기여한다. 따라서 전체 $\Psi(x,\mathbf r_\perp)$를 각 $x$ 위치의 횡방향 고유모드 $\chi_\alpha(\mathbf r_\perp;x)$로 전개할 수 있다.[1]

$$
H_\perp(x)\chi_\alpha(\mathbf r_\perp;x)
=\epsilon_\alpha(x)\chi_\alpha(\mathbf r_\perp;x),
$$

$$
\Psi(x,\mathbf r_\perp)
=\sum_\alpha F_\alpha(x)\chi_\alpha(\mathbf r_\perp;x).
$$

여기서 $\chi_\alpha$는 단면의 mode이고, $F_\alpha(x)$는 그 mode가 수송 방향으로 어떻게 전파되는지를 나타내는 계수다. 전체 횡방향 기저 대신 에너지에 관련된 일부 mode만 남기면 계산 차원이 감소한다.

### 1.2 Coupled mode와 uncoupled mode

각 slice에서 선택한 횡방향 고유벡터들을 $U_i$의 열로 모으면, 실제 장치의 Hamiltonian은 $U_i$로 투영된다. 구조 또는 전위가 수송 방향으로 변하면 인접 slice의 모드도 달라져, 서로 다른 mode 사이에 coupling이 발생한다.

**Coupled mode-space (CMS)**는 이러한 mode 간 비대각 결합을 유지한다. **Uncoupled mode-space (UMS)**는 추가 근사로 일부 mode 간 결합을 무시한다. 따라서 *mode 수를 줄이는 것*과 *남겨 둔 mode 사이의 결합을 버리는 것*은 별개의 근사다. 급격한 단면 변화나 강한 비균일 전위에서는 mode coupling이 중요할 수 있다.[1]

전통적인 설명은 effective-mass Hamiltonian에 자주 사용되지만, 횡방향 mode를 이용해 수송 문제를 축소한다는 개념 자체가 effective-mass 모형에만 한정되는 것은 아니다.

## 2. Atomistic full-band mode-space: Bloch 상태에서 $U$ 구성

원자 수준의 tight-binding 또는 DFT Hamiltonian에는 단면마다 많은 원자 궤도가 포함된다. 이 경우 단순한 횡방향 유효질량 문제 대신, **원래의 atomistic band structure를 관심 에너지 범위에서 재현하는 축소 기저**를 구성한다.[2,3]

### 2.1 수송 방향 cell Hamiltonian

우선 동일한 cell이 수송 방향 $x$로 주기적으로 반복되는 기준계를 생각하자. 한 cell의 orbital 수를 $N$, cell 간격을 $a$라 두고, $H_0$는 onsite block, $H_1$은 오른쪽 인접 cell과의 hopping block으로 정의한다.

$$
H(k)=H_0+H_1e^{ika}+H_1^\dagger e^{-ika},
\qquad H_0,H_1\in\mathbb C^{N\times N}.
$$

이때 Bloch eigenvalue problem은

$$
H(k)\phi_{nk}=\epsilon_n(k)\phi_{nk},
\qquad \phi_{nk}\in\mathbb C^N
$$

이다. $\phi_{nk}$는 전체 실공간 Bloch 함수가 아니라, **한 cell의 $N$개 원자 궤도에 대한 계수 벡터**다. 원래 모형에 두 번째 이웃 이상의 hopping이 있으면 $H_{\pm2},H_{\pm3},\ldots$도 $H(k)$에 포함해야 한다.

### 2.2 여러 $k$에서 관심 상태를 수집하는 이유

먼저 재현할 에너지 창 $\mathcal W=[E_{\min},E_{\max}]$을 정한다. 각 $k$에서 그 범위에 속하는 고유벡터를 모아 snapshot matrix를 구성한다.

$$
\Phi=
\begin{bmatrix}
\phi_{n_1k_1}&\phi_{n_2k_1}&\cdots&\phi_{n_pk_{N_k}}
\end{bmatrix}
\in\mathbb C^{N\times P}.
$$

여기서 $P$는 **수집된 고유벡터의 총개수**이며, $N$이나 최종 mode 수와 같을 필요가 없다. 예를 들어 한 cell에 1,000개 궤도가 있고, 50개 $k$-point에서 각각 20개 상태를 수집했다면 $N=1000$, $P=1000$이 된다. 에너지 창을 기준으로 고르면 각 $k$에서 수집하는 상태 수는 달라질 수 있다.

여러 $k$를 사용하는 이유는 같은 band라도 $k$에 따라 **cell 내부 orbital 조성**이 변하기 때문이다. 하나의 $k$에서 얻은 몇 개의 고유벡터만으로는 관심 구간의 전체 분산을 표현하기 어려울 수 있다.

### 2.3 SVD로 중복 방향을 정리하는 방법

Snapshot들이 서로 선형 독립일 필요는 없다. 이를 직교화하고 중요한 방향을 선별하는 대표적인 방법이 singular value decomposition (SVD)이다.

$$
\underbrace{\Phi}_{N\times P}
=
\underbrace{L}_{N\times q}
\underbrace{\Sigma}_{q\times q}
\underbrace{V^\dagger}_{q\times P},
\qquad q=\min(N,P).
$$

이는 *thin SVD* 표기다. $L$의 열은 원래 cell orbital 공간에서의 직교 방향이고, $\Sigma$의 대각 원소는 singular values다. 필요한 $m$개 열을 선택하면

$$
\boxed{
U=\begin{bmatrix}L_1&\cdots&L_m\end{bmatrix}
\in\mathbb C^{N\times m},\qquad m<N,\qquad U^\dagger U=I_m.
}
$$

예를 들어 $N=1000$에서 $m=100$을 선택했다면 $U$는 $1000\times100$ 행렬이며, 각 열이 하나의 reduced mode다. 여기서 **100은 미리 정해진 표준값이 아니라** snapshot의 독립성, 목표 에너지 창, band 정확도에 따라 선택한 차원이다.

SVD는 수집한 고유벡터의 표현 오차를 작게 만드는 방법이지, band energy를 직접 fitting하는 방법은 아니다. 또한 atomistic MST의 초기 기저를 만드는 데 SVD가 반드시 필요한 것은 아니다. 직교화나 다른 subspace 구성법을 사용할 수도 있다.[2,3]

### 2.4 Onsite와 intercell hopping의 동시 축소

축소된 상태를 원래 cell 계수 $c_i\simeq U\xi_i$로 표현한다면, 같은 $U$로 **onsite뿐 아니라 hopping도** 투영한다.

$$
\boxed{
\widetilde H_0=U^\dagger H_0U,\qquad
\widetilde H_1=U^\dagger H_1U.
}
$$

따라서 축소된 Bloch Hamiltonian은

$$
\widetilde H(k)
=\widetilde H_0+\widetilde H_1e^{ika}
+\widetilde H_1^\dagger e^{-ika}
=U^\dagger H(k)U
$$

가 된다. $\widetilde H_0,\widetilde H_1$은 모두 $m\times m$이고, 이 블록들을 수송 방향으로 연결해 축소된 NEGF 장치를 구성할 수 있다. 먼 이웃 hopping $H_\ell$이 있다면 각각 $\widetilde H_\ell=U^\dagger H_\ell U$로 변환해야 한다.

여기서 **모든 $k$에 동일한 $U$를 적용한다**는 점이 중요하다. 원래 periodic DFT에서의 수송 방향 $k$는 $U$와 hopping을 구성하기 위한 자료이며, 열린 NEGF 장치에서는 수송 방향을 real-space cell들로 연결한다. 횡방향이 주기적이면 그 방향의 $k_\perp$는 별도로 남을 수 있다.

## 3. Basis optimization: Spurious bands를 제거하는 이유

### 3.1 초기 $U$만으로 충분하지 않을 수 있다

SVD로 구성한 $U$가 수집된 wavefunctions를 잘 표현하더라도, 그 기저로 계산한 $\widetilde H(k)$가 모든 $k$에서 관심 band를 정확하게 재현한다는 보장은 없다. 특히 관심 에너지 창에 원래 모형과 대응되지 않는 추가적인 분산 곡선(*spurious bands*)이 나타나거나, 필요한 band가 누락될 수 있다.[2,3]

따라서 초기 기저를 구성한 뒤에는 학습에 쓰지 않은 조밀한 $k$ 격자에서 **band의 에너지·분산뿐 아니라 관심 창 안의 상태 수**를 비교해야 한다. 단순히 몇 개의 eigenvalue가 비슷하다는 것만으로 충분하지 않다.

### 3.2 새로운 basis vector를 추가한다는 의미

문제가 발견되면 기존 $U$의 열공간 밖에서 새 방향 $u_{\mathrm{new}}$를 찾아 기저를 확장한다. 직교 기저에서 그 방향은 다음 조건을 만족하도록 만들 수 있다.

$$
U^\dagger u_{\mathrm{new}}=0,\qquad
u_{\mathrm{new}}^\dagger u_{\mathrm{new}}=1.
$$

기존 $U\in\mathbb C^{1000\times100}$에 한 방향을 추가하면

$$
U_{\mathrm{new}}=
\begin{bmatrix}U&u_{\mathrm{new}}\end{bmatrix}
\in\mathbb C^{1000\times101}
$$

이 된다. 즉 **mode 수를 100개에서 101개로 늘리는 것**이다. 새로운 $k$-point의 Bloch wavefunction을 하나 더 수집하는 행위와는 다르다. 전자는 $U$의 열 수가 증가하는 *basis refinement*이고, 후자는 snapshot matrix $\Phi$의 열 수를 늘리는 *sampling refinement*다.

Mil'nikov 등의 접근에서는 기존 부분공간의 여공간에서 trial vector를 구성하고, 변분적 최적화를 통해 spurious branches를 제거한다. Huang 등의 연구는 이 basis optimization을 더욱 안정적이고 병렬화 가능한 알고리즘으로 발전시켰다.[2,3] 단순히 작은 singular value를 갖는 벡터를 제거하거나 그래프에서 불필요한 band를 삭제하는 절차가 아니다.

따라서 실질적인 순서는 **Bloch 상태 수집 → 초기 $U$ 구성 → band 비교 → 필요한 방향 추가 → 다시 비교**이다. 최종 $m$은 이 검증 과정으로 정해진다.

## 4. Heterostructure mode-space: 서로 다른 $U_i$와 접합부 연결

### 4.1 비주기적 장치에서 무엇이 달라지는가?

동일한 주기적 cell만으로 이루어진 장치에는 공통 $U$를 사용할 수 있다. 그러나 이종접합, 결함, 표면 거칠기 또는 amorphous 영역에서는 cell마다 원자 수·결합·국소 전위가 달라진다. 이때 모든 cell에 같은 축소 기저를 강제하면 중요한 국소 상태를 잃을 수 있다.

각 cell $i$에 대해

$$
U_i\in\mathbb C^{N_i\times m_i},
\qquad m_i<N_i
$$

를 두면, 전체 변환은 block-diagonal 형태가 된다.

$$
U_{\mathrm{device}}=\operatorname{diag}(U_1,U_2,\ldots,U_L).
$$

### 4.2 서로 다른 축소 기저 사이의 hopping

원래 두 cell 사이의 결합이 $H_{ij}\in\mathbb C^{N_i\times N_j}$라면, 투영한 coupling은

$$
\boxed{
\widetilde H_{ij}=U_i^\dagger H_{ij}U_j
\in\mathbb C^{m_i\times m_j}.
}
$$

즉, **왼쪽 cell의 $U_i$와 오른쪽 cell의 $U_j$를 모두 사용**한다. 두 cell의 mode 수 $m_i,m_j$가 달라도 무방하며, $\widetilde H_{ji}=\widetilde H_{ij}^\dagger$로 Hermiticity가 유지된다. Onsite block은 $\widetilde H_{ii}=U_i^\dagger H_{ii}U_i$이다.

예를 들어 한 영역만 원래 atomic-orbital basis로 남기려면 그 영역의 변환을 $U_j=I$로 두면 된다. 그러면 결합은 $\widetilde H_{ij}=U_i^\dagger H_{ij}$가 된다. 이는 **mode-space/real-space hybrid coupling**의 기본 형태다.[4,5]

다만 서로 다른 물질을 단순히 이어 붙이는 과정에서 알 수 없는 계면 hopping이 자동으로 결정되는 것은 아니다. 원래 $H_{ij}$에 접합부의 실제 화학결합 정보가 있어야 하며, basis와 에너지 기준의 일관성도 필요하다.

### 4.3 실제 연구에서의 구현

Shin(2021)은 주기적으로 동일한 cell 하나만 이용하는 방법을 넘어, 비균일 구조를 포함하는 supercell의 상태를 활용해 cell별 축소 기저를 구성하는 heterostructure MST를 제시했다. GaSb/InAs 이종접합, 2차원 물질 접합, 결함과 표면 거칠기가 있는 nanowire 등의 transmission과 local density of states를 검증했다.[4]

Ducry *et al.* (2020)은 비직교 DFT Hamiltonian의 금속 전극과 주기적 영역을 mode space로 줄이되, 비정질 계면처럼 복잡한 활성 영역은 original real-space basis에 남기는 hybrid 접근을 제안했다.[5] 두 연구는 구현 전략에 차이가 있지만, **영역마다 적절한 기저를 정하고 서로 다른 기저 사이의 coupling을 일관되게 변환한다**는 원리를 공유한다.

## 5. SIESTA처럼 비직교 basis를 사용하는 경우

지금까지는 수식의 의미를 분명히 하기 위해 $S=I$를 가정했다. 그러나 SIESTA의 numerical atomic orbitals는 일반적으로 비직교이므로 원래 고유값 문제는

$$
H(k)c_{nk}=\epsilon_n(k)S(k)c_{nk}
$$

이다. 축소할 때는 Hamiltonian과 overlap을 **같은 변환으로** 투영해야 한다.

$$
\boxed{
\widetilde H_{ij}=U_i^\dagger H_{ij}U_j,\qquad
\widetilde S_{ij}=U_i^\dagger S_{ij}U_j.
}
$$

수송 계산에 등장하는 intercell block은 따라서 $\widetilde H_{ij}-E\widetilde S_{ij}$로 표현된다(반대 부호의 $ES-H$ 관례도 동등하다). 각 cell 내부에서 $\widetilde S_{ii}=I$가 되도록 $U_i$를 선택했더라도, 서로 다른 cell의 $\widetilde S_{ij}$는 일반적으로 0이 아니다.

한 가지 더 중요한 차이는 **비직교 basis의 Bloch 계수에 보통의 Euclidean SVD를 그대로 적용하면 물리적 내적을 반영하지 못할 수 있다**는 점이다. 따라서 공통의 직교화된 표현을 만들거나 overlap metric을 고려한 기저 구성이 필요하다. 특히 $S(k)$가 $k$에 의존하면 고정된 하나의 $S$를 사용하는 단순 weighted SVD로 모든 $k$의 내적을 동시에 표현할 수 있다고 가정해서는 안 된다. 이 문제는 [Low-rank approximation](low-rank-approximation.md)과 [Projection methods](projection-methods.md)의 일반적인 기저·내적 구분과 연결된다.

## 6. 네 접근법의 관계와 적용 범위

| 구분 | 기저 $U$를 구성하는 원리 | 주된 대상 |
| --- | --- | --- |
| Conventional mode-space | 횡방향 confinement eigenmodes | Effective-mass 기반 MOSFET, nanowire |
| Atomistic full-band mode-space | 여러 $k$의 Bloch eigenstates에서 공통 부분공간 구성 | Tight-binding 및 DFT 기반 atomistic NEGF |
| Basis optimization | 초기 부분공간의 여공간 방향을 보강해 spurious bands 제거 | Atomistic mode-space의 정확도 개선 |
| Heterostructure mode-space | 영역별 $U_i$ 구성 및 $\widetilde H_{ij}=U_i^\dagger H_{ij}U_j$ | 이종접합·결함·비정질 영역 |

실제 소자 계산에서 mode-space 축소가 성공했는지는 **band structure만이 아니라 transmission $T(E)$, local density of states, 전하 분포와 관심 동작 조건**에서 판단해야 한다. 특히 bias 또는 구조 변화에 따라 Hamiltonian이 달라지면, 기존 $U$가 그 변화를 충분히 표현하는지 재검증해야 한다.

또한 mode-space는 이미 주어진 Hamiltonian의 차원을 줄이는 방법이다. 이것만으로 새로운 구조의 DFT Hamiltonian을 생성하거나 self-consistent charge redistribution을 계산하는 것은 아니다. Wannierization이 주로 국소화된 Hamiltonian 표현을 구성한다면, mode-space는 그 위에 적용할 수도 있는 **추가적인 차원 축소**다. 자세한 비교는 [Wannier functions](wannierization.md)를 참고한다.

## 참고문헌

1. M. Luisier, A. Schenk, and W. Fichtner, “Quantum transport in two- and three-dimensional nanoscale transistors: Coupled mode effects in the nonequilibrium Green's function formalism,” *Journal of Applied Physics* **100**, 043713 (2006). [DOI: 10.1063/1.2244522](https://doi.org/10.1063/1.2244522).
2. G. Mil'nikov, N. Mori, and Y. Kamakura, “Equivalent transport models in atomistic quantum wires,” *Physical Review B* **85**, 035317 (2012). [DOI: 10.1103/PhysRevB.85.035317](https://doi.org/10.1103/PhysRevB.85.035317).
3. J. Z. Huang, H. Ilatikhameneh, M. Povolotskyi, and G. Klimeck, “Robust Mode Space Approach for Atomistic Modeling of Realistically Large Nanowire Transistors,” *Journal of Applied Physics* **123**, 044303 (2018). [DOI: 10.1063/1.5010238](https://doi.org/10.1063/1.5010238). [Preprint](https://arxiv.org/abs/1710.08064).
4. M. Shin, “Hetero-structure mode space method for efficient device simulations,” *Journal of Applied Physics* **130**, 104303 (2021). [DOI: 10.1063/5.0064314](https://doi.org/10.1063/5.0064314). [Preprint](https://arxiv.org/abs/2107.10511).
5. F. Ducry, M. H. Bani-Hashemian, and M. Luisier, “Hybrid Mode-Space–Real-Space Approximation for First-Principles Quantum Transport Simulation of Inhomogeneous Devices,” *Physical Review Applied* **13**, 044067 (2020). [DOI: 10.1103/PhysRevApplied.13.044067](https://doi.org/10.1103/PhysRevApplied.13.044067).
