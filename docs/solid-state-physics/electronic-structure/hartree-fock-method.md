---
title: "1.1. Electronic structure: Hartree–Fock method"
description: Slater determinant의 반대칭성과 축약밀도행렬에서 Coulomb·exchange 에너지와 Fock equation을 유도하고 SCF 계산 및 근사 한계를 설명
status: verified
last_verified: 2026-08-13
---

# 1.1. Electronic structure: Hartree–Fock method

Hartree–Fock (HF) method는 반대칭인 $N$전자 파동함수를 하나의 Slater determinant로 제한하고, 그 다양체 위에서 에너지 기대값을 변분 최소화하는 mean-field 전자구조 방법이다. 전자–전자 Coulomb 반발의 direct 성분은 점유 궤도함수가 만드는 평균장으로 바뀌고, 행렬식의 반대칭성은 같은 스핀 전자의 exchange를 정확히 생성한다. 그러나 하나의 determinant로 나타낼 수 없는 전자 상관은 포함하지 않는다.[1–3,5]

이 글은 고정된 핵, 비상대론적 전자 Hamiltonian과 원자 단위계를 사용한다. 먼저 spin orbital을 이용해 일반식을 유도하고, 실제 분자 계산에서 널리 쓰는 closed-shell restricted Hartree–Fock (RHF)와 유한 basis의 Roothaan–Hall equation으로 내려간다. 주기적 고체의 $k$-point 구현과 post-HF 방법의 상세 유도는 범위에서 제외한다.

## 1. 전자 문제와 변분 공간

### (1) Born–Oppenheimer 전자 Hamiltonian

핵 위치 ${\mathbf R_A\}$를 고정하면 $N$전자 Hamiltonian은

$$
\hat H_{\mathrm e}
=
\sum_{i=1}^{N}\hat h(i)
+\sum_{i<j}^{N}\frac{1}{r_{ij}},
$$

$$
\hat h(i)
=-\frac{1}{2}\nabla_i^2
-\sum_A\frac{Z_A}{|\mathbf r_i-\mathbf R_A|}
$$

로 쓴다. $\hat h$는 전자 운동에너지와 전자–핵 인력을 포함하는 one-electron operator이고, $r_{ij}=|\mathbf r_i-\mathbf r_j|$이다. 핵–핵 반발

$$
E_{\mathrm{NN}}
=\sum_{A<B}\frac{Z_AZ_B}{|\mathbf R_A-\mathbf R_B|}
$$

은 고정된 구조에서 상수이므로 전자 변분 문제를 푼 뒤 더한다.[1–3]

따라서 한 구조에서 SCF가 최소화하는 양은 $E_{\mathrm{HF}}$이지만, 서로 다른 핵 배치의 에너지를 비교할 때 사용하는 Born–Oppenheimer potential energy는

$$
E_{\mathrm{tot}}(\{\mathbf R_A\})
=E_{\mathrm{HF}}(\{\mathbf R_A\})+E_{\mathrm{NN}}(\{\mathbf R_A\})
$$

이다. $E_{\mathrm{NN}}$은 한 번의 전자 SCF 순환 안에서는 변하지 않지만 핵 좌표를 바꾸면 달라진다. 그러므로 결합 길이, 구조 안정성 또는 힘을 비교하면서 전자에너지와 총에너지를 혼용하면 안 된다. HF 근사와 basis 선택은 전자 항에 들어가고, 핵–핵 항은 같은 원자 단위계의 고전적 Coulomb 항으로 정확히 계산한다.[1–3]

정확한 $N$전자 파동함수는 전자 좌표 $x_i=(\mathbf r_i,\omega_i)$를 교환하면 부호가 바뀌어야 한다. 여기서 $\omega_i$는 spin 좌표이고, 적분 $dx_i$는 공간 적분과 spin 합을 함께 뜻한다. 전치 연산자 $\hat P_{ij}$에 대해 fermion 파동함수는

$$
\hat P_{ij}\Psi(\ldots,x_i,\ldots,x_j,\ldots)
=-\Psi(\ldots,x_i,\ldots,x_j,\ldots)
$$

를 만족해야 한다. HF method는 이 조건을 만족시키면서 계산 가능한 가장 단순한 변분 공간으로 단일 Slater determinant를 선택한다.[1–3,5]

### (2) Slater determinant

서로 직교 정규화된 spin orbital $\{\chi_i(x)\}_{i=1}^{N}$의 Hartree product에 반대칭화 연산자

$$
\hat{\mathcal A}
=\frac{1}{N!}
\sum_{P\in S_N}(-1)^P\hat P
$$

를 정의한다. 여기서 $S_N$은 $N$개 전자의 순열군이고 $(-1)^P$는 순열의 parity이다. $\hat{\mathcal A}^2=\hat{\mathcal A}$인 projector를 Hartree product에 작용시키고 정규화하면 Slater determinant를 얻는다. 파동함수를 순열 합과 행렬식으로 각각 쓰면

$$
\begin{aligned}
\Phi(x_1,\ldots,x_N)
&=\frac{1}{\sqrt{N!}}
\sum_{P\in S_N}(-1)^P
\prod_{a=1}^{N}\chi_{P(a)}(x_a)\\
&=\frac{1}{\sqrt{N!}}
\begin{vmatrix}
\chi_1(x_1) & \chi_2(x_1) & \cdots & \chi_N(x_1)\\
\chi_1(x_2) & \chi_2(x_2) & \cdots & \chi_N(x_2)\\
\vdots & \vdots & \ddots & \vdots\\
\chi_1(x_N) & \chi_2(x_N) & \cdots & \chi_N(x_N)
\end{vmatrix}
\equiv |\chi_1\chi_2\cdots\chi_N| .
\end{aligned}
$$

두 전자 좌표를 맞바꾸면 행렬식의 두 **행**이 교환되므로 부호가 바뀐다. 반면 두 spin orbital을 맞바꾸면 두 **열**이 교환되어 같은 부호 변화가 생긴다. 두 orbital이 같거나 선형 종속이면 열들이 선형 종속이 되어 determinant 전체가 0이므로 Pauli exclusion principle도 파동함수 수준에서 구현된다.[1–3,5]

일반 orbital overlap matrix를 $S_{ij}=\langle\chi_i|\chi_j\rangle$라 하면 determinant의 norm은 $\langle\Phi|\Phi\rangle=\det\mathbf S$이다. 따라서 앞 식의 $1/\sqrt{N!}$만으로 정규화되려면

$$
\langle\chi_i|\chi_j\rangle=\delta_{ij}
$$

가 필요하다. 여기서 직교성은 전자들이 서로 구별되는 orbital에 붙어 있다는 뜻이 아니다. 행렬식 전개에는 모든 orbital–전자 배정이 같은 크기로 들어가며, 전자 label은 물리적 입자 식별자가 아니라 파동함수의 좌표 자리이다.[1,2,5]

점유 orbital에 unitary rotation $\widetilde\chi_i=\sum_j\chi_jU_{ji}$을 가하면

$$
|\widetilde\chi_1\cdots\widetilde\chi_N|
=(\det\mathbf U)|\chi_1\cdots\chi_N|
$$

이다. $|\det\mathbf U|=1$이므로 점유 공간은 같고 파동함수는 관측할 수 없는 전체 위상만 변한다. 이 불변성 때문에 HF의 물리적 변분 변수는 개별 orbital 모양이 아니라 $N$차원 점유 부분공간이다.[2,5]

HF 에너지는

$$
E_{\mathrm{HF}}
=\min_{\Phi\,\in\,\mathcal D}
\langle\Phi|\hat H_{\mathrm e}|\Phi\rangle
$$

이며, $\mathcal D$는 직교 정규화된 spin orbital로 만든 단일 determinant의 집합이다. 엄밀히 말해 Fock equation은 이 제한 변분 문제의 **정상 조건**을 줄 뿐이고, SCF로 얻은 모든 해가 전역 최솟값인 것은 아니다. 따라서 최소화 문제와 정상 방정식을 구분해야 한다.[1,2,5]

이 제한은 계산 가능성을 주지만, determinant의 개수를 늘리는 것과 basis function의 개수를 늘리는 것을 서로 다른 근사 축으로 만든다. HF에서는 파동함수가 하나의 decomposable antisymmetric product에 머물고, basis를 늘릴 때에는 그 determinant를 구성하는 점유 부분공간만 더 유연해진다.[1,2,5]

### (3) 축약밀도행렬과 pair density

단일 determinant의 one-particle reduced density matrix (1-RDM)를

$$
\gamma(x,x')
=\sum_{i=1}^{N}\chi_i(x)\chi_i^*(x')
$$

로 정의한다. 이 연산자는 점유 공간으로의 projector이므로

$$
\int \gamma(x,x'')\gamma(x'',x')\,dx''
=\gamma(x,x'),
\qquad
\operatorname{Tr}\gamma=N
$$

을 만족한다. 즉 $\gamma^2=\gamma$인 idempotency가 단일 determinant의 핵심 표지이다. 대각 성분 $\rho(x)=\gamma(x,x)$은 spin까지 분해된 one-particle density이다.[2,5]

이 글에서는 순서 있는 서로 다른 전자쌍을 세도록 two-particle reduced density matrix (2-RDM)를 정규화한다. 단일 determinant에서는

$$
\Gamma(x_1,x_2;x_1',x_2')
=\gamma(x_1,x_1')\gamma(x_2,x_2')
-\gamma(x_1,x_2')\gamma(x_2,x_1')
$$

이고, 대각 pair density는

$$
\boxed{
\rho_2(x_1,x_2)
=\rho(x_1)\rho(x_2)
-|\gamma(x_1,x_2)|^2
}
$$

이다. 첫 항은 독립입자 direct 곱이고 두 번째 항은 반대칭성에서 생긴 exchange 감소량이다. $x_1=x_2$이면 두 항이 정확히 상쇄되어 같은 spin-coordinate에 두 전자가 놓일 확률이 0이 된다. 그러나 반대 spin은 spin 함수의 직교성 때문에 이 exchange 항을 공유하지 않는다.[2,3,5]

첫 전자가 $x_1$에 있다는 조건에서 exchange hole을

$$
\rho_{\mathrm x}(x_2|x_1)
=-\frac{|\gamma(x_1,x_2)|^2}{\rho(x_1)}
$$

로 정의하면 idempotency로부터

$$
\int \rho_{\mathrm x}(x_2|x_1)\,dx_2=-1
$$

을 얻는다. 따라서 exchange hole은 실제로 양전하를 띤 입자가 생긴다는 뜻이 아니라, 기준 전자 주변에서 같은 spin 전자를 찾을 조건부 밀도가 정확히 전자 하나만큼 결손된다는 뜻이다. 이 결손은 공간적으로 퍼져 있으며 이후 exchange energy의 음의 부호와 자기상호작용 상쇄를 동시에 설명한다.[2,5]

## 2. Hartree–Fock 에너지

### (1) Slater–Condon 에너지

One-electron 적분과 two-electron 적분을 각각

$$
h_{ij}=\langle\chi_i|\hat h|\chi_j\rangle,
$$

$$
(ij|kl)
=\iint
\chi_i^*(x_1)\chi_j(x_1)
\frac{1}{r_{12}}
\chi_k^*(x_2)\chi_l(x_2)
\,dx_1dx_2
$$

로 정의한다. 점유 spin orbital $i,j$에 대한 Coulomb 적분과 exchange 적분은

$$
J_{ij}=(ii|jj),
\qquad
K_{ij}=(ij|ji)
$$

이다. Slater–Condon rule을 적용하거나 앞 절의 1-RDM과 pair density를 Hamiltonian에 축약하면 전자 에너지는

$$
\boxed{
E_{\mathrm{HF}}
=\sum_i^{\mathrm{occ}}h_{ii}
+\frac{1}{2}
\sum_{i,j}^{\mathrm{occ}}
\left(J_{ij}-K_{ij}\right)
}
$$

가 된다.[1–3,5] $1/2$은 순서가 반대인 동일한 전자쌍을 두 번 세지 않게 한다. $J_{ij}$는 두 궤도함수 밀도의 고전적 Coulomb 반발에 해당하지만, $K_{ij}$는 bra와 ket에서 orbital label이 교차되는 양자역학적 항이다. Spin 함수가 서로 직교하면 $K_{ij}=0$이므로 exchange는 같은 spin 성분 사이에서만 남는다.[1–3,5]

같은 궤도함수에 대해서는 $J_{ii}=K_{ii}$이다. 따라서 위 식에서 한 전자가 자기 자신의 Coulomb 장과 상호작용하는 항은 orbital별로 정확히 상쇄된다. 이 상쇄는 단일 determinant의 exchange가 수행하는 역할이며, 서로 다른 전자의 순간적인 Coulomb 회피까지 포함한다는 뜻은 아니다.[1–3,5]

### (2) Hartree와 exchange 에너지의 밀도행렬 표현

같은 에너지를 1-RDM으로 쓰면 direct 항과 exchange 항의 구조가 더 명확해진다.

$$
E_{\mathrm{HF}}[\gamma]
=\int h(x,x')\gamma(x',x)\,dx\,dx'
+E_{\mathrm H}[\rho]+E_{\mathrm x}[\gamma],
$$

$$
E_{\mathrm H}[\rho]
=\frac{1}{2}\iint
\frac{\rho(x_1)\rho(x_2)}{r_{12}}\,dx_1dx_2,
$$

$$
\boxed{
E_{\mathrm x}[\gamma]
=-\frac{1}{2}\iint
\frac{|\gamma(x_1,x_2)|^2}{r_{12}}\,dx_1dx_2
} .
$$

$h(x,x')$는 local one-electron operator이면 $\hat h(x)\delta(x-x')$로 줄어든다. $E_{\mathrm H}$는 대각 밀도 $\rho$만 필요하지만, $E_{\mathrm x}$는 서로 다른 두 점을 연결하는 off-diagonal coherence $\gamma(x_1,x_2)$에 의존한다. 그러므로 HF exchange는 일반적으로 local multiplicative potential로 표현할 수 없는 orbital-dependent, nonlocal functional이다.[2,3,5]

Pair-density 식을 이용하면

$$
E_{\mathrm{ee}}^{\mathrm{HF}}
=\frac{1}{2}\iint
\frac{\rho(x_1)\left[\rho(x_2)+\rho_{\mathrm x}(x_2|x_1)\right]}{r_{12}}
\,dx_1dx_2
$$

로도 쓸 수 있다. 따라서 음의 exchange energy는 같은 spin 전자쌍의 조건부 확률이 Coulomb kernel이 큰 가까운 거리에서 줄어든 결과이다. 다만 “exchange force”라는 별도의 고전적 힘이 작용하는 것은 아니며, 전체 효과는 반대칭 파동함수의 확률구조에서 나온다.[2,5]

### (3) Closed-shell 에너지

RHF에서는 $n=N/2$개의 공간 궤도함수 $\{\phi_i(\mathbf r)\}$를 각각 $\alpha$, $\beta$ 전자가 공유한다. 이때

$$
\boxed{
E_{\mathrm{RHF}}
=2\sum_{i=1}^{n}h_{ii}
+\sum_{i,j=1}^{n}
\left(2J_{ij}-K_{ij}\right)
}
$$

이다.[1–3,5] 첫 항의 계수 2는 공간 궤도함수의 이중 점유에서 오고, $2J-K$는 spin 합을 끝낸 결과이다. Spin-orbital 식의 $J-K$와 closed-shell 공간-orbital 식의 $2J-K$를 같은 합 범위에서 섞어 쓰면 계수가 틀린다.

## 3. Fock operator와 정상 조건

### (1) 직교 제약 변분

궤도함수 직교 조건을 Lagrange multiplier $\varepsilon_{ij}$로 부과하면

$$
\mathcal L
=E_{\mathrm{HF}}
-\sum_{ij}\varepsilon_{ij}
\left(\langle\chi_i|\chi_j\rangle-\delta_{ij}\right)
$$

를 얻는다. $\chi_i^*$에 대한 정상 조건 $\delta\mathcal L=0$은

$$
\hat f\chi_i
=\sum_j\varepsilon_{ji}\chi_j
$$

를 준다. 이 식은 각 orbital을 독립적으로 변분한 결과가 아니라, 직교 정규화 제약을 가진 determinant 다양체에서의 Euler–Lagrange equation이다. Fock operator는

$$
\boxed{
\hat f
=\hat h
+\sum_{j}^{\mathrm{occ}}
\left(\hat J_j-\hat K_j\right)
}
$$

이며, 작용은

$$
\hat J_j\chi_i(x_1)
=\left[
\int\frac{|\chi_j(x_2)|^2}{r_{12}}\,dx_2
\right]\chi_i(x_1),
$$

$$
\hat K_j\chi_i(x_1)
=\left[
\int\frac{\chi_j^*(x_2)\chi_i(x_2)}{r_{12}}\,dx_2
\right]\chi_j(x_1)
$$

로 정의한다.[1–3,5] $\hat J_j$는 위치 $x_1$에서 스칼라 Coulomb potential을 곱하지만, $\hat K_j$는 $\chi_i$의 모든 $x_2$ 값과 overlap을 Coulomb kernel로 가중한 뒤 $\chi_j(x_1)$ 방향으로 사영한다. 따라서 $\hat K_j$는 적분연산자이며 곱셈 potential이 아니다.

점유 orbital의 1-RDM을 사용하면 전체 Fock operator의 kernel은 더 간결하게

$$
\boxed{
f(x_1,x_2)
=\left[\hat h(x_1)+v_{\mathrm H}(\mathbf r_1)\right]
\delta(x_1-x_2)
-\frac{\gamma(x_1,x_2)}{r_{12}}
}
$$

로 쓸 수 있다. 여기서

$$
v_{\mathrm H}(\mathbf r_1)
=\int\frac{\rho(x_2)}{r_{12}}\,dx_2
$$

는 local Hartree potential이고, 마지막 항이 nonlocal Fock exchange kernel이다. “Fock term”은 문맥에 따라 전체 $\hat f$를 뜻하기도 하고 exchange 부분 $-\hat K$만을 뜻하기도 한다. 혼동을 피하려면 전체는 **Fock operator**, 마지막 항은 **Fock exchange** 또는 **exchange operator**라고 구분하는 편이 명확하다.[2,3,5]

Hartree potential 안에는 기준 orbital 자신의 밀도도 포함되지만, 동일 orbital의 exchange 작용은

$$
\hat J_i\chi_i=\hat K_i\chi_i
$$

이므로 정확히 소거된다. 반면 $i\neq j$인 같은 spin orbital에서는 $\hat J_j\chi_i$와 $\hat K_j\chi_i$가 같지 않으며, 그 차이가 실제 exchange mean field를 만든다.[1–3,5]

### (2) 점유–비점유 회전과 Brillouin 조건

직교 정규성을 보존하는 orbital 변화는 anti-Hermitian matrix $\boldsymbol\kappa^\dagger=-\boldsymbol\kappa$를 사용해

$$
|\Phi(\boldsymbol\kappa)\rangle
=\exp(\hat\kappa)|\Phi_0\rangle,
\qquad
\hat\kappa
=\sum_{ai}\left(
\kappa_{ai}\hat a_a^\dagger\hat a_i
-\kappa_{ai}^*\hat a_i^\dagger\hat a_a
\right)
$$

로 매개화할 수 있다. $i$와 $a$는 각각 점유·비점유 orbital이다. 점유–점유 회전은 determinant를 위상만 바꾸고, 비점유–비점유 회전은 점유 공간을 바꾸지 않으므로 에너지의 독립적인 1차 변화는 점유–비점유 block에만 있다.[2,5]

에너지의 1차 변화는 상수 배수 규약을 제외하면

$$
\delta E
=2\operatorname{Re}\sum_{ai}F_{ai}\,\delta\kappa_{ai}^*
$$

이므로 HF 정상점에서

$$
\boxed{F_{ai}=\langle\chi_a|\hat f|\chi_i\rangle=0}
$$

이어야 한다. 이는 최적 HF determinant와 모든 singly excited determinant 사이의 Hamiltonian matrix element가 0이라는 Brillouin condition과 같은 내용이다. 그러나 1차 gradient가 0이라는 사실만으로 최소점은 보장되지 않으며, 점유–비점유 회전에 대한 orbital Hessian의 고윳값까지 조사해야 안정성을 판정할 수 있다.[2,5]

### (3) Canonical orbital과 자기일관성

$\varepsilon_{ij}$는 Hermitian matrix이므로 점유 궤도함수 사이의 unitary transformation으로 대각화할 수 있다. 이렇게 선택한 canonical orbital은

$$
\boxed{
\hat f\chi_p=\epsilon_p\chi_p
}
$$

를 만족한다.[1,2] 그러나 $\hat f$ 자체가 점유 궤도함수로 만든 $\hat J_j$와 $\hat K_j$에 의존하므로 이 식은 보통의 선형 고유값 문제가 아니다. 입력 궤도함수로 만든 Fock operator의 고유함수가 다시 같은 점유 공간을 만들 때에만 자기일관적이다.[1–3]

점유 궤도함수끼리의 unitary rotation은 determinant를 전체 위상만큼 바꾸고 one-particle density matrix와 HF 에너지는 보존한다. 따라서 canonical orbital은 편리한 표현이지만 유일한 국소 궤도함수 집합은 아니다.[1,2]

## 4. 유한 basis와 SCF 계산

### (1) Roothaan–Hall equation

분자 궤도함수를 $M$개의 일반적으로 비직교인 basis function $\{\varphi_\mu\}$로

$$
\phi_i(\mathbf r)
=\sum_{\mu=1}^{M}C_{\mu i}\varphi_\mu(\mathbf r)
$$

처럼 전개한다. Fock equation을 basis에 사영하면 closed-shell RHF의 Roothaan–Hall equation

$$
\boxed{
\mathbf F\mathbf C
=\mathbf S\mathbf C\boldsymbol\epsilon
}
$$

을 얻는다. 여기서

$$
F_{\mu\nu}=\langle\varphi_\mu|\hat f|\varphi_\nu\rangle,
\qquad
S_{\mu\nu}=\langle\varphi_\mu|\varphi_\nu\rangle
$$

이다.[1–3] $\mathbf S\neq\mathbf I$이므로 generalized eigenvalue problem이며, $\mathbf X^\dagger\mathbf S\mathbf X=\mathbf I$인 직교화 행렬을 사용하면

$$
\widetilde{\mathbf F}\widetilde{\mathbf C}
=\widetilde{\mathbf C}\boldsymbol\epsilon,
\qquad
\widetilde{\mathbf F}=\mathbf X^\dagger\mathbf F\mathbf X
$$

인 보통의 Hermitian eigenvalue problem으로 바뀐다.[1–3]

Closed-shell density matrix를

$$
P_{\mu\nu}
=2\sum_{i=1}^{n}C_{\mu i}C_{\nu i}^*
$$

로 정의한다. 실수 AO basis와 chemist's notation

$$
(\mu\nu|\lambda\sigma)
=\iint
\varphi_\mu(\mathbf r_1)\varphi_\nu(\mathbf r_1)
\frac{1}{r_{12}}
\varphi_\lambda(\mathbf r_2)\varphi_\sigma(\mathbf r_2)
\,d\mathbf r_1d\mathbf r_2
$$

를 사용하면 RHF Fock matrix는

$$
\boxed{
F_{\mu\nu}[\mathbf P]
=h_{\mu\nu}
+\sum_{\lambda\sigma}P_{\lambda\sigma}
\left[
(\mu\nu|\lambda\sigma)
-\frac{1}{2}(\mu\lambda|\nu\sigma)
\right]
}
$$

이다. 대괄호의 첫 적분 축약은 Coulomb matrix이고 두 번째는 exchange matrix이다. Exchange 앞의 $1/2$은 $\mathbf P$에 이미 공간 orbital의 이중 점유 계수 2가 포함되었기 때문에 생긴다. Complex basis나 다른 전자반발적분 첨자 규약에서는 conjugation과 첨자 순서가 달라질 수 있으므로, 구현식을 옮길 때에는 적분 정의와 density matrix 정의를 함께 확인해야 한다.[1–3,5]

$\mathbf F$가 $\mathbf P$의 함수이고 $\mathbf P$가 다시 점유 generalized eigenvector $\mathbf C$의 함수이므로 Roothaan–Hall equation은 한 번의 대각화로 끝나지 않는다. 계산적으로도 exchange 축약은 AO index를 교차 결합하므로 단순한 local Hartree potential 구성과 구조가 다르다.[1–3,5]

### (2) Self-consistent field 순환

Self-consistent field (SCF) 계산은 다음 순환을 수행한다.[1–3]

1. 원자 밀도의 합이나 core Hamiltonian에서 초기 $\mathbf P^{(0)}$를 만든다.
2. $\mathbf P^{(k)}$로 Coulomb·exchange 적분을 축약하여 $\mathbf F^{(k)}$를 만든다.
3. $\mathbf F^{(k)}\mathbf C^{(k+1)}=\mathbf S\mathbf C^{(k+1)}\boldsymbol\epsilon^{(k+1)}$을 푼다.
4. 점유 궤도함수로 새 $\mathbf P^{(k+1)}$와 에너지를 계산한다.
5. 에너지와 밀도 또는 orbital-gradient residual이 허용 오차보다 작아질 때까지 반복한다.

!!! info "[Measurement]"
    SCF 수렴은 에너지 변화 하나만으로 판정하지 않는다. 대표적으로

    $$
    \Delta E^{(k)}
    =E^{(k)}-E^{(k-1)},
    \qquad
    \Delta\mathbf P^{(k)}
    =\mathbf P^{(k)}-\mathbf P^{(k-1)}
    $$

    와 비직교 basis의 commutator residual

    $$
    \mathbf R^{(k)}
    =\mathbf F^{(k)}\mathbf P^{(k)}\mathbf S
    -\mathbf S\mathbf P^{(k)}\mathbf F^{(k)}
    $$

    의 norm을 함께 확인한다. 보고할 때에는 $|\Delta E|$, density RMS 또는 $\|\mathbf R\|$, 허용 오차, 최대 반복 횟수, 초기 추정과 수렴 가속법을 명시한다.[2,3]

### (3) 수렴과 안정성의 구분

SCF 고정점에 도달했다는 사실은 선택한 변분 공간의 전역 최솟값을 찾았다는 뜻이 아니다. 정상점은 국소 최솟값, saddle point 또는 점유가 다른 해일 수 있다. 점유–비점유 orbital rotation에 대한 에너지의 이차 변화, 즉 orbital Hessian을 검사해야 주어진 HF ansatz 안에서 안정한 해인지 판단할 수 있다.[1–3]

SCF가 진동하거나 발산하면 density mixing, damping, level shifting 또는 direct inversion in the iterative subspace (DIIS)를 사용할 수 있다. 이 기법들은 고정점 탐색을 안정화하지만, basis 불충분·잘못된 spin 상태·강한 다중 determinant 성격 같은 모형 문제를 해결하지는 않는다.[2,3]

## 5. Spin 제약의 선택

같은 HF 변분 원리라도 $\alpha$와 $\beta$ 공간 궤도함수에 어떤 제약을 두는지에 따라 해가 달라진다.[2,3]

| 방법 | 궤도함수 제약 | 적합한 기본 대상 | 주요 주의점 |
| --- | --- | --- | --- |
| RHF | $\phi_i^\alpha=\phi_i^\beta$인 이중 점유 | closed-shell singlet | 결합 해리나 spin polarization에서 지나치게 제한될 수 있음 |
| UHF | $\alpha$, $\beta$ 공간 궤도함수를 독립 최적화 | 일반 open-shell 또는 broken-symmetry 해 | 더 낮은 에너지를 얻을 수 있으나 $\hat S^2$ 고유함수가 아닐 수 있음 |
| ROHF | 이중 점유 궤도함수를 공유하면서 open-shell 점유를 유지 | 명확한 spin multiplicity의 open-shell | Fock operator와 canonical orbital energy의 정의가 UHF보다 덜 단순함 |

RHF보다 UHF의 변분 공간이 더 크므로 같은 basis와 Hamiltonian에서 $E_{\mathrm{UHF}}\le E_{\mathrm{RHF}}$이다. 그러나 낮은 에너지가 곧 원하는 spin 대칭성을 보존한다는 뜻은 아니다. UHF에서는 계산한 $\langle\hat S^2\rangle$를 목표값 $S(S+1)$과 비교하고, spin contamination과 symmetry breaking이 물리적 현상인지 근사의 산물인지 따로 판단해야 한다.[2,3]

## 6. 결과의 해석과 적용 한계

### (1) 변분 상한과 basis-set limit

고정한 Hamiltonian과 허용한 spin·공간 대칭성 아래에서 HF 에너지는 단일 determinant 집합의 최솟값이다. 따라서 정확한 바닥상태 에너지보다 낮아질 수 없지만, 이 명제는 SCF가 실제 최솟값에 수렴하고 수치 적분과 행렬 연산이 충분히 정확하다는 조건을 전제로 한다.[1,2]

유한 basis에서 얻은 값은 basis-set-dependent HF 에너지이다. Basis 공간을 포함 관계로 확장하고 각 단계에서 같은 변분 문제의 최솟값을 찾으면 에너지는 HF basis-set limit를 향해 내려간다. 이는 전자 상관이 복원된다는 뜻이 아니라, 선택한 단일 determinant를 더 유연하게 표현한다는 뜻이다.[1,2,4]

### (2) 단일 determinant 근사

HF는 Pauli 반대칭성에서 생기는 exchange를 포함하지만, 서로 다른 determinant의 중첩이 필요한 correlation은 잃는다. 특히 여러 전자배치가 비슷한 가중치를 가져야 하는 계에서는 한 determinant의 궤도함수를 아무리 최적화해도 필요한 파동함수 구조를 만들 수 없다.[1–3]

| 구분 | HF가 보존하는 정보 | HF가 잃는 정보 또는 위험 |
| --- | --- | --- |
| 반대칭성 | 전자 교환에서 파동함수 부호가 바뀜 | 없음 |
| Exchange | 같은 spin 전자의 비국소 exchange와 자기상호작용 상쇄 | 반대 spin의 동적 상관은 포함하지 않음 |
| 변분 | 단일 determinant 집합 안의 정상점과 최솟값 | 정확한 다중 determinant 바닥상태는 변분 공간 밖에 있을 수 있음 |
| 궤도함수 | 점유 공간과 density matrix를 자기일관적으로 최적화 | Canonical orbital 하나하나를 직접 관측량으로 동일시할 수 없음 |
| Basis | 주어진 basis에서 재현 가능한 최적 determinant | 유한 basis 오차와 선형 의존성 |

### (3) Orbital energy와 총에너지

Canonical HF orbital energy $\epsilon_i$는 수렴한 Fock operator의 고유값이다. Spin-orbital 표기에서 점유 궤도함수의 고유값을 합하면

$$
\sum_i^{\mathrm{occ}}\epsilon_i
=\sum_i^{\mathrm{occ}}h_{ii}
+\sum_{i,j}^{\mathrm{occ}}
\left(J_{ij}-K_{ij}\right)
$$

가 된다. 반면 HF 총 전자에너지는 전자쌍 상호작용을 한 번만 세기 위해 two-electron 항에 $1/2$이 붙는다. 따라서

$$
\boxed{
E_{\mathrm{HF}}
=\sum_i^{\mathrm{occ}}\epsilon_i
-\frac{1}{2}
\sum_{i,j}^{\mathrm{occ}}
\left(J_{ij}-K_{ij}\right)
}
$$

이며, 점유 orbital energy의 단순한 합은 HF 총에너지가 아니다.[1–3] 각 $\epsilon_i$에는 다른 점유 전자가 만드는 평균장이 이미 들어 있으므로 합만 취하면 전자–전자 상호작용을 두 번 센다.

또한 canonical orbital energy는 수렴한 $N$전자 determinant의 Fock operator에서 정의된 Lagrange multiplier이다. 점유 공간 안의 unitary rotation은 density matrix와 총에너지를 보존하지만 개별 orbital의 모양은 바꿀 수 있다. 그러므로 canonical orbital의 순서와 공간 분포는 유용한 분석 자료이지만, 모든 $\epsilon_p$를 독립적인 실제 전자 여기 에너지와 동일시해서는 안 된다. 특히 비점유 orbital은 바닥상태 density matrix를 만들지 않으므로 점유 orbital과 같은 변분적 지위를 갖지 않는다.[1–3]

### (4) 후속 전자구조 방법과의 연결

HF determinant와 orbital은 perturbation theory, configuration interaction, coupled-cluster와 many-body Green's function 방법의 기준 상태로 자주 사용된다. 이 위키의 [GW approximation](../many-body-perturbation/gw-approximation.md)은 독립입자 기준에서 출발해 frequency-dependent self-energy로 quasiparticle energy를 다룬다. 두 방법의 orbital eigenvalue를 같은 물리량으로 간주하지 말고, 각각의 연산자와 근사를 확인해야 한다.

[Electron localization function](electron-localization-function.md)의 원래 유도도 HF 단일 determinant의 같은-spin pair density에서 시작한다. HF에서 exchange hole과 kinetic-energy density가 어떻게 생기는지를 이해하면 ELF가 전자 밀도 자체가 아니라 같은-spin 국소 회피를 정규화한 양이라는 점을 구분하기 쉬워진다.

!!! warning "[Interpretation Caveat]"
    SCF 수렴, basis 수렴과 물리 모형의 정확도는 서로 다른 문제이다. $\Delta E$와 density residual이 작아도 불안정한 HF 정상점일 수 있고, HF basis-set limit에 도달해도 단일 determinant 밖의 correlation은 남는다. Spin 상태, stability, basis와 후속 correlation 방법을 각각 독립적으로 점검해야 한다.[1–4]

## 7. 요약

- Slater determinant는 Hartree product의 반대칭화이며, 점유 공간으로의 idempotent 1-RDM과 정규화가 $-1$인 같은 spin exchange hole을 만든다.
- HF 에너지는 one-electron, Hartree와 exchange 항으로 구성된다. Exchange는 1-RDM의 off-diagonal 성분에 의존하는 비국소 항이며 orbital별 자기 Coulomb 항을 정확히 상쇄한다.
- 직교 제약 변분은 점유–비점유 Fock matrix block $F_{ai}=0$과 $\hat f\chi_p=\epsilon_p\chi_p$를 주지만, Fock operator가 점유 궤도함수에 의존하므로 비선형 자기일관 문제이다.
- 유한 비직교 basis에서는 $\mathbf F\mathbf C=\mathbf S\mathbf C\boldsymbol\epsilon$을 밀도와 함께 반복해 푼다.
- SCF 수렴은 에너지와 density·commutator residual을 함께 확인하고, 수렴 뒤에도 orbital stability를 별도로 검사해야 한다.
- RHF, UHF와 ROHF는 spin 제약이 다르며, 더 낮은 UHF 에너지가 올바른 spin 대칭성을 보장하지 않는다.
- Basis-set limit는 단일 determinant 표현의 완성이지 electron correlation의 복원이 아니다.

## 8. 참고문헌

1. C. C. J. Roothaan, “New Developments in Molecular Orbital Theory,” *Reviews of Modern Physics* **23**, 69–89 (1951). [DOI: 10.1103/RevModPhys.23.69](https://doi.org/10.1103/RevModPhys.23.69).
2. S. Lehtola, F. Blockhuys, and C. Van Alsenoy, “An Overview of Self-Consistent Field Calculations Within Finite Basis Sets,” *Molecules* **25**, 1218 (2020). [DOI: 10.3390/molecules25051218](https://doi.org/10.3390/molecules25051218).
3. Psi4 developers, “HF: Hartree–Fock Theory,” official documentation (2026년 확인). [Documentation](https://psi4.github.io/psi4docs/master/scf.html).
4. S. Shahbazian and M. Zahedi, “Towards a complete basis set limit of Hartree–Fock method: correlation-consistent versus polarized-consistent basis sets,” *Theoretical Chemistry Accounts* **113**, 152–160 (2005). [DOI: 10.1007/s00214-005-0619-2](https://doi.org/10.1007/s00214-005-0619-2).
5. P. Echenique and J. L. Alonso, “A mathematical and computational review of Hartree–Fock SCF methods in quantum chemistry,” *Molecular Physics* **105**, 3057–3098 (2007). [DOI: 10.1080/00268970701757875](https://doi.org/10.1080/00268970701757875).
