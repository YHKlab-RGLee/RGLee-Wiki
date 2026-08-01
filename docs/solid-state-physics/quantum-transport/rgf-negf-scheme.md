---
title: "(1) Quantum Transport: RGF and NEGF Scheme"
description: open quantum system의 NEGF formalism, recursive Green's function 계산, observables와 Poisson self-consistent procedure를 설명
status: verified
last_verified: 2026-08-01
---

# (1) Quantum Transport: RGF and NEGF Scheme

Nonequilibrium Green's function (NEGF)은 반무한 전극에 연결된 유한 소자의 정상 상태 quantum transport를 기술하는 정식화이다. 이 글은 유효 단일입자 Hamiltonian, phase coherence와 정상 직류 조건을 기준으로 삼는다. 전극은 열평형 저장고이지만 서로 다른 electrochemical potential을 가질 수 있으며, open boundary는 전극 self-energy로 표현한다.[1,2]

Recursive Green's function (RGF)은 NEGF와 다른 물리 이론이 아니라, 국소 결합 Hamiltonian의 block-tridiagonal structure를 이용해 필요한 Green's function 블록만 계산하는 수치 방법이다. 따라서 먼저 open boundary와 occupation을 정의한 뒤 RGF와 Poisson self-consistent calculation을 연결해야 한다.[2,3]

## 1. Open Boundary와 Retarded Green's Function

### (1) Device–Lead Partition

전체 단일입자 공간을 왼쪽 전극 $L$, 소자 $D$, 오른쪽 전극 $R$로 나누면 직교 기저의 Hamiltonian은

$$
H =
\begin{pmatrix}
H_L & V_{LD} & 0 \\
V_{DL} & H_D & V_{DR} \\
0 & V_{RD} & H_R
\end{pmatrix}
$$

로 쓸 수 있다. $H_D$는 명시적으로 계산할 유한 영역, $H_\alpha$는 반무한 전극, $V_{D\alpha}=V_{\alpha D}^{\dagger}$는 경계 결합이다. 전극끼리 직접 결합하지 않는 분할을 가정한다.

전체 역행렬에서 전극 자유도를 Schur complement로 제거하면 소자 영역의 retarded Green's function은

$$
G^R(E)=
\left[
(E+i\eta)I-H_D-\Sigma_L^R(E)-\Sigma_R^R(E)
\right]^{-1},
\qquad \eta\rightarrow 0^+
$$

가 된다.[1,2] 여기서 $\eta$는 retarded 경계 조건을 정하며, 전극 self-energy는

$$
\Sigma_\alpha^R(E)
=V_{D\alpha}\,g_\alpha^R(E)\,V_{\alpha D},
\qquad
g_\alpha^R(E)=
\left[(E+i\eta)I-H_\alpha\right]^{-1}_{\mathrm{surface}}
$$

이다. $g_\alpha^R$는 전극 전체 역행렬이 아니라 소자와 맞닿은 표면 블록이다. 따라서 전극의 밴드 구조와 경계 결합이 모두 $\Sigma_\alpha^R$에 들어간다.[1,2]

### (2) Level Shift와 Broadening

Self-energy의 Hermitian 부분은 소자 준위를 이동시키고 anti-Hermitian 부분은 전극으로 빠져나갈 수 있는 상태의 폭을 만든다. 전극 $\alpha$의 broadening 행렬은

$$
\Gamma_\alpha(E)
=i\left[\Sigma_\alpha^R(E)-\Sigma_\alpha^A(E)\right]
=-2\,\operatorname{Im}\Sigma_\alpha^R(E)
$$

로 정의한다. 여기서 $\Sigma_\alpha^A=(\Sigma_\alpha^R)^\dagger$이다. $\Gamma_\alpha$는 단순한 수명 상수가 아니라 에너지와 경계 궤도에 의존하는 양의 준정부호 행렬이다.[1,2]

Retarded Green's function으로부터 전체 spectral function을

$$
A(E)=i\left[G^R(E)-G^A(E)\right]
$$

로 정의한다. 탄도 두 전극 문제에서 별도의 속박 상태가 없다면

$$
A(E)=G^R(E)\left[\Gamma_L(E)+\Gamma_R(E)\right]G^A(E)
$$

가 성립한다. 이 등식은 self-energy와 역행렬 구현을 점검하는 중요한 항등식이다.[1,2]

## 2. Nonequilibrium Occupation과 Observables

### (1) Lesser Green's Function과 Density Matrix

Retarded Green's function은 이용 가능한 상태를 정하지만 어느 전극이 그 상태를 얼마나 채우는지는 정하지 않는다. 전극 $\alpha$의 Fermi–Dirac distribution을

$$
f_\alpha(E)=
\left[
1+\exp\left(\frac{E-\mu_\alpha}{k_BT_\alpha}\right)
\right]^{-1}
$$

로 두면 탄도 조건의 lesser self-energy와 Keldysh 방정식은

$$
\Sigma^<(E)
=i\left[f_L(E)\Gamma_L(E)+f_R(E)\Gamma_R(E)\right],
$$

$$
G^<(E)=G^R(E)\Sigma^<(E)G^A(E)
$$

이다.[1,2] $\mu_\alpha$와 $T_\alpha$는 각 전극의 electrochemical potential과 온도이다.

단일입자 density matrix는

$$
\rho
=-\frac{i}{2\pi}\int_{-\infty}^{\infty}G^<(E)\,dE
$$

로 계산한다.[1,2] $G^<$는 anti-Hermitian이므로 $-iG^<$가 Hermitian이라는 점이 식의 부호와 $i$ 인자를 확인하는 기준이다. 스핀을 명시적으로 Hamiltonian에 포함했다면 $\rho$에 별도의 2배를 곱하지 않는다.

직교 국소 기저에서 궤도 $n$의 local density of states (LDOS)는

$$
\operatorname{LDOS}_n(E)
=-\frac{1}{\pi}\operatorname{Im}G^R_{nn}(E)
$$

이다. 공간 격자나 원자 궤도에서 전하 밀도를 만들 때에는 기저 함수와 스핀 축퇴 규약까지 포함해 $\rho$를 실공간 밀도로 변환해야 한다.[1,2]

### (2) Transmission과 Terminal Current

전극 $L$에서 들어온 상태가 $R$로 전달될 에너지별 transmission probability는 Caroli 식

$$
T(E)
=\operatorname{Tr}\left[
\Gamma_L(E)G^R(E)\Gamma_R(E)G^A(E)
\right]
$$

로 주어진다. 위상 결맞음 탄도 수송에서 전류는

$$
I
=\frac{e}{h}\sum_{\sigma}
\int_{-\infty}^{\infty}
T_\sigma(E)\left[f_L(E)-f_R(E)\right]\,dE
$$

이다.[1,2] $\sigma$는 명시적인 스핀 채널이다. 두 스핀 채널이 축퇴되어 있고 $T(E)$를 한 스핀에 대해 계산했다면 $\sum_\sigma$를 $g_s=2$로 바꿀 수 있다. 스핀 자유도를 이미 행렬에 포함했다면 추가 축퇴 인자를 곱하면 안 된다.

작은 바이어스와 영온 한계에서는

$$
G_{\mathrm{lin}}
=\frac{e^2}{h}\sum_\sigma T_\sigma(E_F)
$$

가 된다. 이 식은 유한 바이어스 전류식을 선형화한 결과이며, 일반적인 비선형 전류를 대신하지 않는다.

## 3. Recursive Green's function

### (1) Block-Tridiagonal Structure

소자 영역을 수송 방향으로 $N$개의 slice로 나누고 최근접 slice끼리만 결합시키면

$$
EI-H_D-\Sigma_L^R-\Sigma_R^R
=
\begin{pmatrix}
A_1 & -V_{12} & 0 & \cdots \\
-V_{21} & A_2 & -V_{23} & \cdots \\
0 & -V_{32} & A_3 & \cdots \\
\vdots & \vdots & \vdots & \ddots
\end{pmatrix}
$$

가 된다. 내부 slice에서 $A_n=(E+i\eta)I-H_{nn}$이고 첫째와 마지막 블록에는 각각 전극 self-energy가 들어간다.

왼쪽에서 $n$번째 slice까지 연결한 Green's function의 끝 블록을 $g^L_{nn}$이라 하면

$$
g^L_{11}=
\left[A_1-\Sigma_L^R\right]^{-1},
$$

$$
g^L_{nn}
=\left[
A_n-V_{n,n-1}g^L_{n-1,n-1}V_{n-1,n}
\right]^{-1}
$$

로 전진 갱신할 수 있다.[2,3,5] 마지막 slice에서는 $A_N$에 $\Sigma_R^R$를 포함한다. 뒤로 되짚는 단계에서는 대각 블록과 인접 블록을 복원하여 LDOS, 밀도와 국소 전류에 필요한 항을 얻는다.

각 slice의 궤도 수가 $M$이고 $N$에 무관하다고 하면 조밀한 블록 역행렬의 계산량은 대략 $\mathcal{O}(NM^3)$이다. 전체 $NM$ 차원 행렬을 직접 역산하는 $\mathcal{O}((NM)^3)$보다 길이 방향 확장성이 좋지만, 단면이 커져 $M$이 증가하면 비용은 여전히 빠르게 커진다.[2,3,5]

### (2) Lead Surface Green's Function

주기 전극은 한 principal layer의 온사이트 블록과 인접 층 결합으로 표현한다. 표면 Green's function은 전달 행렬의 evanescent 해를 선택하거나, 층을 반복적으로 decimation하는 López Sancho 방법 등으로 구할 수 있다.[2,4] 계산된 $g_\alpha^R$는 다음 조건을 만족해야 한다.

- 전극의 전파 상태가 없는 에너지에서 $\Gamma_\alpha$가 사라지는가
- 전극 단위층을 한 층 늘려도 self-energy가 변하지 않는가
- 동일한 전극과 완전 결정 채널을 연결했을 때 불필요한 경계 반사가 없는가

이 검사는 표면 반복법의 수렴뿐 아니라 principal layer가 충분히 두꺼워 결합 범위를 모두 포함하는지도 확인한다.

## 4. Poisson–NEGF Self-Consistent Calculation

### (1) Electrostatic Potential과 Charge

게이트가 있는 소자에서는 운반자 밀도가 electrostatic potential을 바꾸고, 바뀐 potential이 다시 $H_D$와 운반자 밀도를 바꾼다. Electrostatic potential을 $\phi(\mathbf r)$, 전자 전하량의 크기를 $e>0$로 두면

$$
\nabla\cdot
\left[
\epsilon(\mathbf r)\nabla\phi(\mathbf r)
\right]
=-\rho_{\mathrm{tot}}(\mathbf r),
$$

$$
\rho_{\mathrm{tot}}
=e\left[p-n+N_D^+-N_A^-\right]+\rho_{\mathrm{fixed}}
$$

로 쓸 수 있다. 전자의 potential energy는 $-e\phi$이므로 local approximation에서는 $H_D=H_{D,0}-e\phi$로 갱신한다. 다른 sign convention을 사용한다면 Poisson equation, charge density와 Hamiltonian 갱신의 세 부호를 함께 바꿔야 한다.[2,5]

### (2) Iteration과 Convergence

Self-consistent calculation은 다음 순서로 진행한다.

1. 경계 바이어스와 초기 $\phi^{(0)}$를 정한다.
2. $H_D[\phi^{(k)}]$와 전극 self-energy로 $G^R$, $G^<$를 구한다.
3. 에너지 적분으로 $\rho$와 $n(\mathbf r)$을 계산한다.
4. Poisson 방정식을 풀어 $\phi_{\mathrm{out}}^{(k)}$를 얻는다.
5. 선형 혼합이나 Newton 계열 방법으로 $\phi^{(k+1)}$를 만들고 반복한다.

!!! info "[Measurement]"
    수치 결과에는 전극의 $\mu_\alpha$와 온도, spin 처리, energy-integration range와 adaptive criterion, 공간 격자 또는 basis, 전극 principal layer, potential-mixing method와 convergence criterion을 함께 기록한다. 대표 residual은

    $$
    R_\phi^{(k)}
    =\max_{\mathbf r}
    \left|
    \phi^{(k+1)}(\mathbf r)-\phi^{(k)}(\mathbf r)
    \right|
    $$

    이며, 이 값만으로 충분하지 않다. 마지막 반복에서 전하 변화와 두 단자의 전류 불일치도 함께 확인해야 한다.[2,5]

에너지 격자는 물질과 소자에 따라 달라진다. 좁은 공명은 촘촘한 실수축 적분을 요구하고, 평형 성분은 복소 contour 적분으로 효율화할 수 있다. 따라서 보편적인 고정 에너지 간격이나 고정 절점 수를 제시하기보다, 전하와 전류가 적분 세분화에 대해 수렴했음을 보고해야 한다.[2,5]

## 5. 검증과 적용 범위

### (1) 구현 검증

다음 검사는 서로 다른 오류를 찾으므로 함께 수행한다.

- **평형 검사:** $\mu_L=\mu_R$와 같은 온도에서 순전류가 수치 오차 안에서 0인가
- **전류 보존:** 탄도 정상 상태에서 왼쪽과 오른쪽 단자 전류의 크기가 일치하는가
- **스펙트럼 항등식:** $A=i(G^R-G^A)$와 $G^R(\Gamma_L+\Gamma_R)G^A$가 일치하는가
- **균일 전극 검사:** 소자와 전극이 같은 주기계일 때 허위 반사가 나타나지 않는가
- **분할 독립성:** slice 경계와 명시적 소자 길이를 바꿔도 관심 관측량이 수렴하는가
- **적분 수렴:** 에너지 구간과 격자를 세분화해도 전하와 전류가 허용 오차 안에서 유지되는가

### (2) Non-Orthogonal Basis와 Interactions

원자 궤도처럼 overlap 행렬 $S$가 있는 non-orthogonal basis에서는 단순히 $I$를 $S_D$로 바꾸는 것만으로 충분하지 않다. 소자 역행렬은

$$
G^R(E)=
\left[
(E+i\eta)S_D-H_D-\Sigma_L^R-\Sigma_R^R
\right]^{-1}
$$

가 되고, 경계 결합에도 $H_{D\alpha}-ES_{D\alpha}$ 조합이 들어간다. 밀도와 전하도 overlap을 고려한 일관된 규약으로 계산해야 한다.[2,5] 직교식과 비직교식을 한 구현 안에서 섞으면 전하 수와 전류 보존이 깨질 수 있다.

!!! warning "[Interpretation Caveat]"
    이 글의 $\Sigma^<=i\sum_\alpha f_\alpha\Gamma_\alpha$는 전극만이 nonequilibrium occupation을 공급하는 유효 단일입자 ballistic transport 문제에 해당한다. Phonon, impurity 또는 electron–electron scattering을 넣으면 scattering self-energy와 그에 대응하는 $G^<$를 self-consistently 계산해야 한다. Strong correlation, time-dependent driving, superconducting Nambu space와 photon coupling은 각각 추가 formalism을 요구하며 현재 식을 그대로 적용할 수 없다.[2,5]

## 6. 요약

1. 전극 self-energy는 반무한 open boundary를 유한 소자 Green's function에 포함하며, $\Gamma_\alpha$는 전극과 결합된 상태의 폭을 나타낸다.
2. $G^<$는 상태의 nonequilibrium occupation을 담고, density matrix는 $\rho=-i(2\pi)^{-1}\int G^<dE$로 계산한다.
3. Caroli transmission과 Landauer current에서 spin을 행렬에 포함했는지 별도 degeneracy factor로 셌는지 명시해야 한다.
4. RGF는 block-tridiagonal structure를 이용해 길이에 선형인 계산량으로 필요한 Green's function 블록을 얻는다.
5. 실제 소자 계산은 Poisson–NEGF 반복과 평형, 전류 보존, 스펙트럼 항등식, 적분·분할 수렴 검사를 함께 요구한다.

## 7. 참고문헌

1. M. Paulsson, "Non Equilibrium Green's Functions for Dummies: Introduction to the One Particle NEGF equations," *arXiv:cond-mat/0210519v2* (2006). [arXiv](https://arxiv.org/abs/cond-mat/0210519).
2. X. Waintal, M. Wimmer, A. Akhmerov, C. Groth, B. K. Nikolić, M. Istas, T. Ö. Rosdahl, and D. Varjas, "Computational quantum transport: A scattering approach perspective," *arXiv:2407.16257v2* (2026). [arXiv](https://arxiv.org/abs/2407.16257).
3. S. Kazymyrenko and X. Waintal, "Knack of using Green's functions in numerical quantum transport calculations," *Physical Review B* **77**, 115119 (2008). [DOI](https://doi.org/10.1103/PhysRevB.77.115119).
4. M. P. López Sancho, J. M. López Sancho, and J. Rubio, "Quick iterative scheme for the calculation of transfer matrices: Application to Mo (100)," *Journal of Physics F: Metal Physics* **14**, 1205–1215 (1984). [DOI](https://doi.org/10.1088/0305-4608/14/5/016).
5. R. Lake, G. Klimeck, R. C. Bowen, and D. Jovanovic, "Single and multiband modeling of quantum electron transport through layered semiconductor devices," *Journal of Applied Physics* **81**, 7845–7869 (1997). [DOI](https://doi.org/10.1063/1.365394).
