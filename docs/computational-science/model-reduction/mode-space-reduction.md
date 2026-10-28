---
description: Full-band mode-space reduction의 기저 구성, Hamiltonian과 hopping의 투영, spurious-band 제거 및 비주기적 소자로의 확장을 단계별로 설명한다.
---

# Mode-space reduction

**Mode-space reduction (MSR)**은 양자 수송 계산에서 관심 에너지 범위의 전자 상태를 적은 수의 기저 함수(mode)로 표현하여 Hamiltonian의 차원을 줄이는 방법이다. 소자를 수송 방향으로 여러 cell 또는 slice로 나누면 각 cell에 많은 atomic orbitals가 들어갈 수 있다. 이때 필요한 수송 상태를 작은 부분공간으로 표현할 수 있다면, Green's function을 계산하는 행렬의 크기도 줄일 수 있다.[1–3]

## 1. Basic idea

### (1) 축소 기저로 상태 표현

핵심은 원래의 상태 계수 $c_i\in\mathbb C^N$를 작은 좌표 $\xi_i\in\mathbb C^m$로 근사하는 것이다.

$$
\boxed{c_i\simeq U\xi_i,\qquad
U\in\mathbb C^{N\times m},\quad m<N.}
$$

$U$의 **각 열이 하나의 축소 기저벡터(mode)**이며, 원래 $N$개 orbital의 선형결합으로 구성된다. 어떤 $U$를 선택하는지가 정확도를 결정한다. 단순히 Hamiltonian을 잘라서 작은 행렬을 만드는 것과는 다르다.

### (2) Conventional과 atomistic full-band 방식

전통적인 **conventional mode-space**에서는 수송 방향 $x$와 횡방향 $\mathbf r_\perp=(y,z)$를 구분하고, 횡방향 양자 구속 Hamiltonian의 eigenmodes를 계산한다.[1,2]

$$
H_\perp(x)\chi_\alpha(\mathbf r_\perp;x)
=\epsilon_\alpha(x)\chi_\alpha(\mathbf r_\perp;x),
\qquad
\Psi(x,\mathbf r_\perp)
=\sum_\alpha F_\alpha(x)\chi_\alpha(\mathbf r_\perp;x).
$$

$\epsilon_\alpha$는 횡방향 subband 에너지다. 관심 에너지에 도달할 수 있는 낮은 subband를 우선 포함하고, mode 수를 늘리며 전류와 전하밀도의 수렴을 검사한다. 실제 전류 기여는 barrier·tunneling·mode coupling에도 좌우되므로 에너지 순서만으로 최종 mode 수를 결정할 수는 없다. 횡방향 모드 사이의 결합을 유지하면 *coupled mode-space*, 이를 추가로 무시하면 *uncoupled mode-space* 근사가 된다.[1,2]

반면 **atomistic full-band mode-space**는 횡방향 유효질량 모형을 먼저 구성하지 않는다. 원래 tight-binding 또는 DFT Hamiltonian의 **Bloch eigenvectors를 여러 $k$에서 수집**하고, 관심 band들을 표현할 공통 cell basis $U$를 찾는다.[2–4] 두 방식은 축소 기저를 얻는 방법이 다르지만, 이후 Hamiltonian을 투영한다는 원리는 같다.

### (3) Wannierization과의 비교

[Wannierization](wannierization.md)도 Bloch 상태를 조합하여 관심 상태를 표현할 기저를 만든다는 점에서 full-band mode-space와 유사하다. 다만 여기서 설명하는 full-band 방식은 여러 $k$의 cell 계수벡터를 담을 작은 공통 기저 $U$를 구성하는 데 초점을 둔다.[2,3] Wannierization은 각 $k$에서 Bloch 상태의 위상과 혼합을 정한 뒤 Fourier 변환하여 실공간에 국소화된 기저를 구성한다.[5,6]

차원 축소와 국소화는 구분해야 한다. 고정된 고립 band 집합 안에서 unitary 변환과 Fourier 변환만 수행하면 그 공간의 차원과 정보는 보존된다. Wannier 모형에서 차원을 줄이는 것은 관심 band를 선택하거나, 더 큰 후보 공간에서 작은 부분공간을 고르는 disentanglement 단계이다.[5,6]

세 접근의 기저 구성과 목적을 간략히 비교하면 다음과 같다.

| 접근 | 기저 구성 | 주된 목적·차원 축소 |
| --- | --- | --- |
| Conventional mode-space | 횡방향 양자 구속 Hamiltonian의 eigenmodes | 필요한 transverse modes를 남겨 수송 문제 축소[1,2] |
| Atomistic full-band mode-space | 여러 $k$의 Bloch eigenvectors로 공통 cell basis $U$ 구성 | 관심 band를 재현하는 작은 기저로 수송 문제 축소[2,3] |
| Wannierization | Bloch 상태의 위상·혼합 조정 후 Fourier 변환 | 실공간 국소 기저 구성; 차원 축소는 band·부분공간 선택에서 발생[5,6] |

이하에서는 원자 수준의 tight-binding·DFT Hamiltonian을 사용하는 **atomistic full-band mode-space**를 기준으로 설명한다. 여러 $k$의 Bloch eigenvector로 기저를 구성하고 onsite·hopping을 투영한 뒤, spurious band에 따른 기저 보강, 비주기적 소자 연결, NEGF 수송 검증을 다룬다.

## 2. Cell Hamiltonian과 Bloch band

식을 단순하게 하기 위해 2–6절에서는 **직교 orbital basis ($S=I$)**를 가정한다. SIESTA처럼 비직교 basis를 사용하는 경우는 7절에서 다룬다.

### (1) Onsite와 intercell hopping

수송 방향으로 동일한 cell이 간격 $a$로 반복된다고 하자. 각 cell에 $N$개의 orbital이 있고, 이웃 cell 사이의 hopping까지만 포함한다.

- $H_0\in\mathbb C^{N\times N}$: 한 cell 내부의 onsite Hamiltonian block
- $H_1\in\mathbb C^{N\times N}$: cell $i$에서 오른쪽 cell $i+1$로 향하는 hopping block
- $H_1^\dagger$: 반대 방향의 hopping

따라서 수송 방향으로 여러 cell을 연결한 Hamiltonian은

$$
H_{\mathrm{chain}}=
\begin{pmatrix}
H_0&H_1&0&\cdots\\
H_1^\dagger&H_0&H_1&\cdots\\
0&H_1^\dagger&H_0&\ddots\\
\vdots&\vdots&\ddots&\ddots
\end{pmatrix}.
$$

여기서 $H_0$와 $H_1$은 숫자 하나가 아니라 **cell당 orbital 수 $N$에 대응하는 행렬**이다. 원래 Hamiltonian이 두 번째 이웃 이상의 cell을 연결한다면 $H_2,H_3,\ldots$도 필요하다. 아래에서는 원리를 설명하기 위해 nearest-cell 형태만 사용한다.

### (2) Bloch Hamiltonian과 band dispersion

주기적 기준계에서 $c_i=e^{ikia}\phi_{nk}$를 대입하면, 무한한 chain의 고유값 문제를 한 cell의 문제로 표현할 수 있다.

$$
\boxed{
H(k)=H_0+H_1e^{ika}+H_1^\dagger e^{-ika},
}
$$

$$
H(k)\phi_{nk}=\epsilon_n(k)\phi_{nk},
\qquad \phi_{nk}\in\mathbb C^N.
$$

여기서 $\phi_{nk}$는 **$k$에서 $n$번째 Bloch 상태의 한 cell 내 orbital expansion coefficients**다. 실공간 전체 wavefunction과 구별해야 한다. 각 $k$에서 이 방정식을 풀면 $\epsilon_n(k)$라는 band dispersion뿐 아니라, 그 band의 orbital composition을 담은 $\phi_{nk}$를 얻는다.[2,3]

Full-band mode-space는 이 **eigenvalue 자체가 아니라 eigenvector $\phi_{nk}$**를 이용해 기저를 만든다. 서로 다른 $k$에서 같은 band의 orbital 조성이 달라질 수 있기 때문이다.[2,3]

## 3. 초기 축소 기저 $U$ 구성

### (1) 관심 에너지 범위

모든 band를 정확히 재현하는 것이 목적은 아니다. 계산하려는 소자의 전류, tunneling 및 전하에 필요한 에너지 구간을 먼저 정한다.[2,3]

$$
\mathcal W=[E_{\min},E_{\max}].
$$

예를 들어 전도대 가장자리 부근의 수송을 계산한다면 해당 전도대와 bias·potential 변화로 접근 가능한 상태들을 포함하도록 $\mathcal W$를 설정한다. 따라서 *Fermi energy에 가장 가까운 band만 선택한다*는 보편적인 규칙은 없다.[2,3]

### (2) Bloch eigenvectors 수집

Brillouin zone에서 여러 $k$-point를 선택한다. 각 점에서 $\epsilon_n(k)\in\mathcal W$를 만족하는 eigenvectors를 수집하고, 열 방향으로 쌓는다.[2,3]

$$
\boxed{
\Phi=[\phi_{n_1k_1},\,\phi_{n_2k_1},\,\ldots,\,
\phi_{n_pk_{N_k}}]\in\mathbb C^{N\times P}.
}
$$

- $N$: 한 cell의 **원래 orbital 수**
- $N_k$: 수집에 사용한 **$k$-point 수**
- $P$: 모든 $k$에서 수집한 **eigenvector의 총개수**
- $m$: 앞으로 선택할 **축소 mode 수** (아직 결정되지 않음)

각 $k$에서 항상 같은 개수의 band를 선택할 필요는 없다. 예를 들어 $N=1000$이고 50개의 $k$-point에서 20개씩 선택했다면 $\Phi$는 $1000\times1000$이다. 100개의 $k$-point에서 같은 상태를 선택하면 $\Phi$는 $1000\times2000$이 될 수 있다. **$\Phi$의 열 수를 늘리는 것과 최종 mode 수 $m$을 늘리는 것은 다른 일**이다.

또한 서로 다른 $k$의 전체 Bloch wavefunction이 서로 직교하더라도, $\Phi$에 저장한 **cell 계수벡터**들이 모두 직교한다는 뜻은 아니다. 따라서 많은 벡터를 수집해도 서로 거의 중복되는 방향이 포함될 수 있다.[2,3]

### (3) 직교화와 SVD

이제 목표는 $P$개의 snapshot을 충분히 표현하면서도 열 수가 작은 $U$를 구성하는 것이다. 한 가지 대표적인 방법이 singular value decomposition (SVD)이다.[3,7,8]

$$
\boxed{
\underbrace{\Phi}_{N\times P}
=\underbrace{L}_{N\times q}
\underbrace{\Sigma}_{q\times q}
\underbrace{V^\dagger}_{q\times P},
\qquad q=\min(N,P).
}
$$

위 식은 *thin SVD*이다. $L$은 cell orbital 공간의 직교 방향을 담고, $\Sigma=\operatorname{diag}(\sigma_1,\ldots,\sigma_q)$의 singular values는 snapshot에 포함된 각 방향의 크기를 나타낸다. 가장 중요한 $m$개 열을 선택하면

$$
\boxed{
U=[L_1,\ldots,L_m]\in\mathbb C^{N\times m},
\qquad U^\dagger U=I_m.
}
$$

예를 들어 다음과 같다.

| 구분 | 예시 크기 | 의미 |
| --- | --- | --- |
| $H(k)$ | $1000\times1000$ | 원래 orbital 1000개 |
| $\Phi$ | $1000\times1000$ | 여러 $k$에서 수집한 1000개 상태 |
| $L$ | $1000\times1000$ | Snapshot으로부터 얻은 직교 방향 |
| $U$ | $1000\times100$ | 처음 선택한 mode 100개 |
| $\widetilde H(k)$ | $100\times100$ | 축소된 Hamiltonian |

여기서 **100은 예시일 뿐이며 초기 mode 수가 정해져 있지 않다.** SVD의 앞쪽 열을 택하면 *주어진 snapshot 집합의 재구성 오차*를 작게 할 수 있지만, 그것만으로 모든 $k$에서 band 정확도가 보장되지는 않는다.[3,7,8] 실제 Mil'nikov–Huang 계열에서는 Bloch 상태를 수집한 뒤 직교화하는 것이 핵심이며, **SVD가 반드시 사용되어야 하는 특정 단계는 아니다**.[2,3]

### (4) 공통 기저 $U$의 적용 범위

Snapshot을 여러 $k$에서 얻었다고 해서 $U(k)$를 매번 따로 만드는 것은 아니다. 최종 $U$는 **하나의 공통 cell 부분공간**을 나타낸다. 그 기저로 모든 $H(k)$를 투영해야 일관된 실공간 onsite·hopping block을 얻어 소자를 연결할 수 있다.[2,3]

각 $k$에서 고유벡터 몇 개만 남겨 $\epsilon_n(k)$를 저장하면 band 데이터는 압축할 수 있지만, 그것만으로 **서로 연결된 cell의 수송 Hamiltonian**이 구성되는 것은 아니다.[2,3]

## 4. 축소된 onsite·hopping을 이용한 소자 구성

### (1) Hamiltonian block의 투영

각 cell의 원래 상태를 $c_i\simeq U\xi_i$로 근사하여 원래 방정식에 대입하면 다음처럼 onsite와 hopping을 함께 투영한다.[2,3]

$$
\boxed{
\widetilde H_0=U^\dagger H_0U,\qquad
\widetilde H_1=U^\dagger H_1U.
}
$$

$N\times N$였던 두 행렬은 모두 $m\times m$이 된다. **Onsite만 축소하고 hopping을 원래 크기로 남기는 것이 아니다.** 두 행렬이 동일한 reduced basis에서 정의되어야 한다.

이때

$$
\widetilde H(k)
=\widetilde H_0+\widetilde H_1e^{ika}
+\widetilde H_1^\dagger e^{-ika}
=U^\dagger H(k)U
$$

가 성립한다. 따라서 축소 후에도 원래와 같은 형태의 band 문제를 풀 수 있다. 다만 $\widetilde H(k)$의 eigenvalues가 $\epsilon_n(k)$와 정확히 같다는 뜻은 아니다. **작게 만든 기저가 얼마나 정확한지**가 다음 단계의 검증 대상이다.

### (2) 축소된 cell의 연결

$L$개의 cell로 된 장치에 동일한 $U$를 적용하면 축소된 장치 Hamiltonian은

$$
\widetilde H_{\mathrm{device}}=
\begin{pmatrix}
\widetilde H_0&\widetilde H_1&0&\cdots\\
\widetilde H_1^\dagger&\widetilde H_0&\widetilde H_1&\cdots\\
0&\widetilde H_1^\dagger&\widetilde H_0&\ddots\\
\vdots&\vdots&\ddots&\ddots
\end{pmatrix}.
$$

수송 방향이 열린 NEGF device에서는 **각 cell을 real space로 연결하고 수송 방향 $k_x$를 별도로 적분하지 않는다.** 대신 전극의 진행·감쇠 모드는 electrode self-energy에 반영한다. 횡방향이 주기적이면 그 방향의 $k_\perp$ sampling은 별도로 수행할 수 있다.[9,10]

장치의 위치별 전위 $\Delta_i$가 있다면 $H_{ii}=H_0+\Delta_i$이므로 $\widetilde H_{ii}=\widetilde H_0+U^\dagger\Delta_iU$처럼 전위도 같은 기저에서 표현해야 한다. Mode 사이의 전위 결합을 임의로 버리면 추가 근사가 된다.[2,3]

## 5. Spurious bands 제거와 mode 수 결정

### (1) 초기 기저 $U$의 band 검증

초기 $U$를 구했다면 원래 $H(k)$와 축소된 $\widetilde H(k)$의 band structures를 **기저 구성에 사용하지 않은 조밀한 $k$ 격자**에서 비교한다. 관심 energy window에서 다음을 확인해야 한다.[2,3,11]

- 원래 물리적 bands의 에너지, extrema 및 dispersion을 재현하는가?
- 관심 구간에 **원래 band와 대응되지 않는 spurious branches**가 나타나는가?
- 필요한 band가 누락되지는 않았는가?

SVD로 snapshot을 매우 잘 표현하더라도 projection된 Hamiltonian이 만드는 spectrum에는 spurious bands가 나타날 수 있다. 이는 eigensolver 오류가 아니라 **선택된 reduced subspace가 충분하지 않은 문제**다.[2,3,11]

### (2) 기저 방향의 보강

예를 들어 처음의 $U$가 $1000\times100$이라면, 이미 선택한 공간 밖에서 새로운 벡터 $u_{\mathrm{new}}\in\mathbb C^{1000}$을 구해

$$
U_{\mathrm{new}}=[U,u_{\mathrm{new}}]
\in\mathbb C^{1000\times101}
$$

로 확장할 수 있다. 따라서 **mode 수가 100에서 101로 증가한다.** 새로운 Bloch eigenvector를 sampling해서 $\Phi$의 열 하나를 늘리는 것과 구별해야 한다.

새 방향은 기존 $U$에 직교하도록 만든다. 직교 basis에서 여공간 projector는

$$
Q_\perp=I-UU^\dagger
$$

이다. 예를 들어 Mil'nikov 계열 알고리즘의 trial subspace는 기존 mode-space 기저에 Hamiltonian을 작용시킨 뒤 이 여공간에 투영하는 아이디어를 사용한다.[2,3,11] Nearest-cell·직교 모형에서 Huang 등이 사용한 trial-vector 생성은 다음과 같다.[3]

$$
X_{\mathrm{trial}}=
\big[Q_\perp H(0)U,\;
Q_\perp H(\pi/a)U\big].
$$

$X_{\mathrm{trial}}$의 열들을 직교화하여 trial basis $\Xi$를 구성한 다음,

$$
u_{\mathrm{new}}=\Xi d
$$

의 계수 $d$를 최적화해 문제가 되는 spurious branches를 관심 에너지 구간 밖으로 이동시키는 방향을 구한다. 이 식은 **새로운 기저 방향을 찾는 방법의 구조를 설명**한다. 실제 Mil'nikov/Huang 알고리즘에는 에너지·$k$ 표본을 사용하는 목적함수, spurious-band 탐지 및 반복 정지 조건이 추가된다.[2,3,11]

### (3) 기저 보강의 종료 기준

기저를 한 개 또는 여러 개씩 보강하고, $\widetilde H_0,\widetilde H_1$을 다시 투영한 후 band를 비교한다. 관심 window에서 필요한 물리적 bands가 재현되고 spurious branches가 허용 가능한 수준으로 제거될 때까지 반복한다.

즉, 최종 mode 수 $m$은 **처음부터 정한 숫자가 아니라 정확도 요구를 만족하도록 조정한 결과**다. 그러나 band 재현은 필요조건일 뿐, 열린 소자의 실제 transmission 정확도까지 자동으로 보장하지는 않는다.[3,4]

## 6. 비주기적 접합으로의 확장

### (1) 공통 기저 $U$의 한계

지금까지는 모든 cell이 같은 결정 구조의 반복이라고 가정했다. 그러나 heterojunction, vacancy, surface roughness 또는 amorphous 영역에서는 각 cell의 orbital 수, 결합 환경 및 국소 상태가 다를 수 있다. 하나의 ideal bulk 기준계에서 만든 $U$가 접합부의 interface states까지 정확하게 표현할 것이라고 기대할 수는 없다.[4,11]

대표적인 확장은 **cell별로 다른 축소 기저**를 허용하는 것이다.[4,11]

$$
U_i\in\mathbb C^{N_i\times m_i},\qquad
U_{\mathrm{device}}=\operatorname{diag}(U_1,\ldots,U_L).
$$

여기서 $m_i$는 cell마다 달라도 된다. 예를 들어 왼쪽 재료의 $U_i$와 오른쪽 재료의 $U_j$가 서로 다른 Bloch band 특성을 반영하게 만들 수 있다.

### (2) Onsite와 접합부 hopping의 변화

Cell $i$의 onsite block과 cell $i,j$ 사이의 coupling은 각각

$$
\boxed{
\widetilde H_{ii}=U_i^\dagger H_{ii}U_i,\qquad
\widetilde H_{ij}=U_i^\dagger H_{ij}U_j.
}
$$

로 축소한다. 특히 $\widetilde H_{ij}$의 크기는 $m_i\times m_j$이다. **인접한 두 cell의 축소 기저를 양쪽에서 함께 적용**해야 하며, $m_i=m_j$일 필요도 없다. 원래 $H_{ji}=H_{ij}^\dagger$라면 축소 후에도 Hermiticity가 유지된다.[4,11]

여기서 중요한 제약은 $H_{ij}$가 **이미 물리적으로 정의되어 있어야 한다**는 점이다. 서로 다른 bulk의 $H_0$를 연결하는 것만으로 새로운 계면의 화학결합과 hopping을 결정할 수는 없다. 계면 자체가 포함된 Hamiltonian이나 별도로 검증된 coupling 정보가 필요하다.[4,11]

### (3) 비주기적 영역의 기저 $U_i$ 구성

주기적 물질 각각에서 만든 $U$만 반복 사용하면 국소 결함 상태를 놓칠 수 있다. 이 문제에 대한 대표적인 연구가 Shin(2021)의 **heterostructure mode-space method**다.[4]

그 핵심적인 구성 방향은 다음과 같다.

1. **접합·결함이 들어간 구조를 포함하는 기준 supercell**을 만든다. 필요하면 완충 cell을 두어 벌크와 접합부의 환경을 함께 표현한다.
2. 해당 기준 구조의 관심 에너지 범위 eigenstates를 구한다. 주기적 supercell 표현이 가능한 경우 여러 Bloch $k$의 상태를 수집한다.
3. 수집된 상태의 계수를 **각 cell 또는 구조 영역별 성분으로 분할**하여 $U_i$를 구성·직교화한다.
4. 영역별 basis를 보완하고 모든 $\widetilde H_{ij}$를 계산한 뒤 transmission과 local density of states를 원래 모형과 비교한다.

이 절차의 목적은 이상적인 bulk band뿐 아니라 **비주기적인 접합부에 고유한 전자 상태도 축소 공간에 포함**하는 것이다. 신민철 교수의 2021년 연구는 GaSb/InAs tunnel FET, MoTe$_2$/SnS$_2$ 수직 FET, 결함이 있는 InAs nanowire, surface roughness가 있는 Si nanowire 등의 예를 제시했다.[4]

### (4) 비축소 영역을 남기는 hybrid 방식

모든 영역을 반드시 mode space로 줄일 필요는 없다. 예를 들어 전극은 축소하고 복잡한 interface는 원래 atomic-orbital basis에 남길 수 있다. 원래 공간을 유지하는 영역에서는 $U_j=I_{N_j}$로 놓으면

$$
\widetilde H_{ij}=U_i^\dagger H_{ij}
$$

이다. Ducry *et al.* (2020)의 **hybrid mode-space/real-space** 방법은 이러한 설계를 DFT 기반 비균일 소자에 적용한 사례다.[12] 경계의 한쪽 기저를 항등행렬로 두는 관계는 다른 cell별 투영 구성에서도 도출된다.[4,11]

따라서 Shin의 heterostructure MST와 hybrid mode-/real-space 방법은 동일한 구현은 아니지만, 모두 **영역의 특성에 맞게 기저를 구성하고 경계 coupling을 일관되게 투영한다**는 원칙을 따른다.

## 7. SIESTA Hamiltonian과 NEGF 적용

### (1) 비직교 overlap의 축소

SIESTA의 numerical atomic orbitals는 일반적으로 비직교이므로, 출발점은

$$
H(k)c_{nk}=\epsilon_n(k)S(k)c_{nk}
$$

이다. 따라서 Hamiltonian만 축소하면 안 되고, **overlap의 onsite 및 intercell block도 같은 $U_i$로 투영**해야 한다.[4,9,10,13]

$$
\boxed{
\widetilde H_{ij}=U_i^\dagger H_{ij}U_j,\qquad
\widetilde S_{ij}=U_i^\dagger S_{ij}U_j.
}
$$

이는 앞에서 설명한 heterostructure 공식을 그대로 일반화한 것이다. 해당 블록의 NEGF inverse Green's function에는 $E\widetilde S_{ij}-\widetilde H_{ij}$가 등장한다. $\widetilde S_{ii}=I$로 정규화해도, 인접 cell의 $\widetilde S_{ij}$가 0인 것은 아니다.[9,10]

또한 $S(k)$가 $k$에 의존할 때에는 Bloch 계수를 그대로 Euclidean SVD하는 것이 물리적인 내적을 자동으로 보장하지 않는다. **공통 직교 표현에서 상태를 수집하거나 overlap metric과 일관된 기저 구성 방법**을 정의해야 한다. 이는 별도의 수학적 주의 사항이며, 단순히 $U^\dagger U=I$만 확인하고 넘어가서는 안 된다.[4,7,8] 관련 기초는 [Projection methods](projection-methods.md)에서 다룬다.

### (2) 수송 계산의 검증 기준

Mode-space reduction은 Hamiltonian을 작게 만드는 근사이며, 원래 모형을 완전히 동일하게 푸는 것은 아니다. 검증 대상은 다음 단계로 구분한다.[3,4]

| 단계 | 비교할 결과 | 판단할 사항 |
| --- | --- | --- |
| Periodic 기준계 | Band energy, dispersion, 관심 window의 band 수 | $U$가 원래 물리적 상태를 충분히 표현하는가? |
| Open device | Transmission $T(E)$, current, local density of states | 축소 모형이 실제 수송을 재현하는가? |
| Self-consistent 계산 시 | Charge distribution, electrostatic potential, 수렴 결과 | 관심 bias·전위 변화에서도 기저가 유효한가? |

원래 Hamiltonian이 $N$차원이고 축소 기저가 $m$차원이라면, 조밀한 block 선형대수의 대표적인 $O(N^3)$ 연산이 $O(m^3)$ 규모로 작아질 수 있다. 다만 이는 특정 연산의 **점근적 비교**이며 전체 실행 시간의 실제 가속비는 original sparsity, lead 계산, 반복 횟수, 하드웨어, basis 준비 비용에 좌우된다.[1,3]

마지막으로 mode-space는 **이미 주어진 $H$와 $S$를 축소**한다. 새로운 heterointerface의 $H_{ij}$를 DFT 정확도로 생성하거나, 임의의 전압에서 Kohn–Sham Hamiltonian을 자동으로 갱신하는 방법 자체는 아니다.[4,9,11] [Wannierization](wannierization.md)으로 얻은 Hamiltonian에 추가로 적용할 수도 있고, SIESTA에서 이미 얻은 localized AO Hamiltonian을 직접 축소할 수도 있다.[3,4,13]

## 8. 요약

**Atomistic full-band MST의 기본 흐름은 다음과 같다.**

$$
\begin{aligned}
&H_0,H_1
\xrightarrow{\text{Bloch eigenvectors at multiple }k}
\Phi
\xrightarrow{\text{orthogonalization / SVD}}
U_{\mathrm{initial}}\\
&\xrightarrow{\text{band validation / basis optimization}}
U_{\mathrm{final}}
\xrightarrow{\text{projection}}
\widetilde H_0,\widetilde H_1
\xrightarrow{\text{device assembly}}
\text{NEGF}.
\end{aligned}
$$

비주기적 장치에서는 여기에 **cell별 $U_i$ 구성**과 **$\widetilde H_{ij}=U_i^\dagger H_{ij}U_j$**가 추가된다. SIESTA처럼 비직교 basis라면 $S_{ij}$까지 같은 방식으로 변환한다.

이때 최종 판단 기준은 단순히 reduced band가 보기 좋게 재현되는지가 아니라, **관심 에너지·bias 범위에서 원래 device의 전자 수송 결과를 얼마나 정확하게 유지하면서 계산 비용을 줄였는가**이다.

## 9. 참고문헌

1. M. Luisier, A. Schenk, and W. Fichtner, “Quantum transport in two- and three-dimensional nanoscale transistors: Coupled mode effects in the nonequilibrium Green's function formalism,” *Journal of Applied Physics* **100**, 043713 (2006). [DOI: 10.1063/1.2244522](https://doi.org/10.1063/1.2244522).
2. G. Mil'nikov, N. Mori, and Y. Kamakura, “Low-dimensional Quantum Transport Models in Atomistic Device Simulations,” *2011 International Conference on Simulation of Semiconductor Processes and Devices (SISPAD)*, 315–318 (2011). [DOI: 10.1109/SISPAD.2011.6035033](https://doi.org/10.1109/SISPAD.2011.6035033). [Full text](https://in4.iue.tuwien.ac.at/pdfs/sispad2011/pdf/11-5.pdf).
3. J. Z. Huang, H. Ilatikhameneh, M. Povolotskyi, and G. Klimeck, “Robust Mode Space Approach for Atomistic Modeling of Realistically Large Nanowire Transistors,” *Journal of Applied Physics* **123**, 044303 (2018). [DOI: 10.1063/1.5010238](https://doi.org/10.1063/1.5010238). [Preprint](https://arxiv.org/abs/1710.08064).
4. M. Shin, “Hetero-structure mode space method for efficient device simulations,” *Journal of Applied Physics* **130**, 104303 (2021). [DOI: 10.1063/5.0064314](https://doi.org/10.1063/5.0064314). [Preprint](https://arxiv.org/abs/2107.10511).
5. N. Marzari, A. A. Mostofi, J. R. Yates, I. Souza, and D. Vanderbilt, “Maximally localized Wannier functions: Theory and applications,” *Reviews of Modern Physics* **84**, 1419–1475 (2012). [DOI: 10.1103/RevModPhys.84.1419](https://doi.org/10.1103/RevModPhys.84.1419). [Full text](https://arxiv.org/pdf/1112.5411).
6. J. Kuneš, “Wannier Functions and Construction of Model Hamiltonians,” in *The LDA+DMFT approach to strongly correlated materials*, E. Pavarini, E. Koch, D. Vollhardt, and A. Lichtenstein (eds.), Modeling and Simulation Vol. 1, Forschungszentrum Jülich (2011), Chapter 4. ISBN 978-3-89336-734-4. [Full text](https://www.cond-mat.de/events/correl11/manuscripts/kunes.pdf).
7. P. Benner, S. Gugercin, and K. Willcox, “A Survey of Projection-Based Model Reduction Methods for Parametric Dynamical Systems,” *SIAM Review* **57**(4), 483–531 (2015). [DOI: 10.1137/130932715](https://doi.org/10.1137/130932715). [Full text](https://kiwi.oden.utexas.edu/papers/Parametric-model-reduction-survey-Benner-Gugercin-Willcox.pdf).
8. B. Haasdonk, “Reduced Basis Methods for Parametrized PDEs—A Tutorial Introduction for Stationary and Instationary Problems,” in *Model Reduction and Approximation: Theory and Algorithms*, 65–136 (SIAM, 2017). [DOI: 10.1137/1.9781611974829.ch2](https://doi.org/10.1137/1.9781611974829.ch2). [Author preprint](https://pnp.mathematik.uni-stuttgart.de/ians/haasdonk/data/oberwolfach2014/RBtutorial.pdf).
9. M. Brandbyge, J.-L. Mozos, P. Ordejón, J. Taylor, and K. Stokbro, “Density-functional method for nonequilibrium electron transport,” *Physical Review B* **65**, 165401 (2002). [DOI: 10.1103/PhysRevB.65.165401](https://doi.org/10.1103/PhysRevB.65.165401). [Author preprint](https://arxiv.org/pdf/cond-mat/0110650).
10. T. Ozaki, K. Nishio, and H. Kino, “Efficient implementation of the nonequilibrium Green function method for electronic transport calculations,” *Physical Review B* **81**, 035116 (2010). [DOI: 10.1103/PhysRevB.81.035116](https://doi.org/10.1103/PhysRevB.81.035116). [Author preprint](https://arxiv.org/pdf/0908.4142).
11. F. Ducry, M. H. Bani-Hashemian, and M. Luisier, “A Hybrid Mode-Space/Real-Space Scheme for DFT+NEGF Device Simulations,” *2019 International Conference on Simulation of Semiconductor Processes and Devices (SISPAD)*, 69–72 (2019). [DOI: 10.1109/SISPAD.2019.8870571](https://doi.org/10.1109/SISPAD.2019.8870571). [Full text](https://in4.iue.tuwien.ac.at/pdfs/sispad2019/SISPAD_4.1.pdf).
12. F. Ducry, M. H. Bani-Hashemian, and M. Luisier, “Hybrid Mode-Space–Real-Space Approximation for First-Principles Quantum Transport Simulation of Inhomogeneous Devices,” *Physical Review Applied* **13**, 044067 (2020). [DOI: 10.1103/PhysRevApplied.13.044067](https://doi.org/10.1103/PhysRevApplied.13.044067).
13. SIESTA Project, *SIESTA 4.1-b4 User’s Guide* (2018). [Official manual](https://siesta.icmab.es/SIESTA_MATERIAL/Docs/Manuals/siesta-4.1-b4.pdf).
