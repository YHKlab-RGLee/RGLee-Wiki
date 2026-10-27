---
description: 전극에 연결된 소자의 Hamiltonian에서 출발하여 Green's function, 전자 점유, 밀도와 전류를 계산하는 NEGF의 기본 절차를 설명한다.
---

# NEGF formalism

Nonequilibrium Green's function (NEGF)은 전극과 전자를 주고받는 소자의 전자 상태, 점유와 전류를 계산하는 방법이다. 이 글에서는 두 전극에 연결된 소자를 정의하고, 전극의 영향을 포함한 Green's function을 구한 뒤 전자 밀도와 전류를 계산한다. 마지막에는 같은 절차를 단일 준위에 적용하여 비평형 점유의 의미를 살펴보고, density functional theory (DFT)의 자기일관 계산으로 연결한다.[1–4]

## 1. 계산할 계와 기저

### (1) 두 전극에 연결된 소자

계산 대상은 왼쪽 전극 $L$, 중앙의 소자 $D$, 오른쪽 전극 $R$로 이루어진다. 전극은 소자에 전자를 공급하거나 소자에서 나온 전자를 받아들이는 reservoir이며, 소자는 두 전극 사이의 전달 경로를 제공한다. 각 전극은 반무한하게 이어진다고 가정하고, 접촉 때문에 전하와 전위가 달라지는 부분까지 소자 영역에 포함한다.[3,4]

아래에서는 시간에 따라 변하지 않는 정상 상태와 coherent 단일입자 수송을 다룬다. 소자 안의 정적 장벽과 결함에 의한 탄성 산란은 포함할 수 있지만, 전자–포논 산란처럼 에너지를 교환하는 과정은 별도로 추가해야 한다. Spin 첨자는 생략하고 한 spin 성분의 식을 사용한다. 서로 독립적이고 축퇴된 두 spin을 모두 포함하려면 최종 전자 밀도와 전류를 두 배로 한다.[1,2]

### (2) Localized orbital과 행렬 원소

전자 상태를 원자 주변에 국소화된 기저 함수 $\phi_\mu(\mathbf r)$의 선형결합으로 표현한다. 이를 linear combination of atomic orbitals (LCAO) 표현이라고 한다. **$\mu,\nu$는 기저 orbital의 번호**이다. 원자 하나에 여러 orbital이 있을 수 있으므로 원자 번호와는 구분한다.[3,4]

$$
\psi(\mathbf r)=\sum_\mu c_\mu\phi_\mu(\mathbf r).
$$

Hamiltonian과 overlap의 행렬 원소는 다음과 같이 정의한다.

$$
H_{\mu\nu}=\langle\phi_\mu|\hat H|\phi_\nu\rangle,
\qquad
S_{\mu\nu}=\langle\phi_\mu|\phi_\nu\rangle.
$$

$H_{\mu\nu}$는 두 orbital을 연결하는 에너지 행렬 원소이고, $S_{\mu\nu}$는 두 기저 함수의 겹침이다. 일반적인 LCAO 기저에서는 $S\ne I$이며, $I$는 단위행렬이다. 이 overlap을 유지하면 비직교 기저와 정규직교 기저를 같은 식으로 다룰 수 있으며, 정규직교 기저는 $S=I$인 경우에 해당한다.[3,4]

기저를 $L,D,R$ 순서로 정렬하면 전체 Hamiltonian은 다음 세 영역으로 나뉜다.

$$
H_{\mathrm{full}}=
\begin{pmatrix}
H_L&H_{LD}&0\\
H_{DL}&H_D&H_{DR}\\
0&H_{RD}&H_R
\end{pmatrix}.
$$

대각 블록 $H_L,H_D,H_R$는 각 영역 내부의 Hamiltonian이다. $H_{D\alpha}$는 전극 $\alpha$와 소자 사이의 결합이며, **$\alpha=L,R$는 전극 지표**이다. Overlap 행렬도 동일한 영역으로 나누어 $S_D,S_{D\alpha}$ 등으로 쓴다. 좌우 전극의 직접 결합과 overlap은 0으로 두어 전자 전달이 소자를 통해 이루어지도록 한다.[3,4]

이후 $G^r,A,G^n,P$는 모두 **소자에 포함된 orbital들을 행과 열로 갖는 행렬**이다. 예를 들어 $G^r_{\mu\nu}$의 $\mu,\nu$는 $H_D$의 행·열과 같은 orbital을 가리킨다. 영역을 구분하는 $D,L,R$와 개별 orbital을 구분하는 $\mu,\nu$를 이렇게 분리하면 큰 행렬을 매번 다시 펼칠 필요가 없다.

### (3) 전극의 점유와 인가 전압

전극 $\alpha$의 electrochemical potential을 $\mu_\alpha$, 온도를 $T_\alpha$라 하자. 전극은 내부 평형을 유지하므로 에너지 $E$인 전자 상태의 점유는 Fermi–Dirac 함수로 정해진다.[1–4]

$$
f_\alpha(E)=
\frac{1}{1+\exp[(E-\mu_\alpha)/(k_BT_\alpha)]}.
$$

$k_B$는 Boltzmann 상수이다. **$\mu_L,\mu_R$는 전극의 점유를 정하는 에너지**이며, 기저 번호 $\mu,\nu$와 역할이 다르다. 모든 에너지는 공통 영점을 사용한다. 두 전극의 온도가 같고 $\mu_L=\mu_R$이면 공통 Fermi 함수 하나로 평형 점유를 표현할 수 있다.

전자 전하를 $-e$($e>0$)라 하고, 이 글의 bias 부호를 $eV_b=\mu_L-\mu_R$로 정한다. 영온에서 $\mu_L>\mu_R$이면 $\mu_R<E<\mu_L$ 구간에서 왼쪽 전극은 채워져 있고 오른쪽 전극은 비어 있다. 이 점유 차이가 순전자 흐름의 원인이 된다. 실제 전달량은 다음 단계에서 구하는 전극–소자 결합과 전자 상태에 의해 결정된다.[1,2]

## 2. 전극을 연결한 Green's function

### (1) 전극의 영향을 나타내는 self-energy

반무한 전극의 모든 orbital을 소자와 함께 직접 계산하는 대신, 전극이 소자에 미치는 영향을 **전극 self-energy** $\Sigma_\alpha^r(E)$에 담는다. 위첨자 $r$은 retarded 응답, 즉 원인 이후에 나타나는 응답을 뜻한다.[1–4]

이를 계산하려면 전극의 surface Green's function $g_\alpha^r$가 필요하다. 이 함수는 소자와 맞닿은 전극 표면에서의 응답이며, 그 뒤로 이어지는 반무한 전극의 효과까지 포함한다. 소자와 전극 표면 사이의 결합을 $\tau_{D\alpha}$라 쓰면, 실수 에너지축의 retarded 극한에서 다음 관계를 얻는다.[3,4]

$$
\tau_{D\alpha}(E)=H_{D\alpha}-ES_{D\alpha},
$$

$$
\Sigma_\alpha^r(E)
=\tau_{D\alpha}(E)\,g_\alpha^r(E)\,
\tau_{D\alpha}^{\dagger}(E).
$$

이 식의 $H_{D\alpha},S_{D\alpha}$는 소자와 전극 표면 기저 사이의 블록이고, $\dagger$는 켤레전치이다. Overlap 항은 비직교 기저의 일반화된 고유값 방정식 $Hc=ESc$에서 나온다. Self-energy 식은 소자–전극 결합, 전극 내부의 응답, 전극–소자 결합을 차례로 반영한다. 원래 전체 방정식에서 전극 성분을 풀어 소자 방정식에 대입한 결과이며, **$\Sigma_\alpha^r$는 소자 orbital 공간의 행렬**이다. 전극 표면에 있는 orbital 수와 관계없이 결과의 크기는 $H_D$와 같다. Surface Green's function의 실제 계산은 [Surface Green's function](surface-greens-function.md)에서 다룬다.[3,4]

### (2) 소자의 응답과 준위 폭

전극에 연결된 소자의 retarded Green's function은

$$
G^r(E)=
\left[(E+i0^+)S_D-H_D
-\Sigma_L^r(E)-\Sigma_R^r(E)\right]^{-1}
$$

이다. $0^+$는 retarded 경계조건을 선택하는 양의 무한소이다. $G^r$는 주어진 에너지에서 소자의 orbital들이 어떻게 응답하고 서로 연결되는지를 나타낸다. 전극과의 결합을 제거하면 $(ES_D-H_D)^{-1}$의 retarded 극한으로 돌아간다. 여기서 $G^r$는 비직교 기저의 **전개계수 표현**이며, 아래의 density kernel에도 같은 표현을 사용한다.[3,4]

전극 결합은 소자의 고립 준위를 이동시키고, 전자가 전극으로 빠져나갈 수 있도록 준위에 폭을 만든다. 이를 구분하기 위해

$$
\Sigma_\alpha^r
=\Lambda_\alpha-\frac{i}{2}\Gamma_\alpha,
\qquad
\Gamma_\alpha=i\left[\Sigma_\alpha^r-(\Sigma_\alpha^r)^\dagger\right]
$$

로 쓴다. Hermitian 부분 $\Lambda_\alpha$는 준위 이동과 혼성화를, **broadening 행렬** $\Gamma_\alpha$는 전극과의 결합으로 생기는 폭을 나타낸다. 둘 다 에너지 단위이다. 일반적인 다중 orbital 소자에서는 두 양 모두 행렬이며, 다음의 단일 준위 예제에서만 수 하나로 표현된다.[1,2]

이 단계까지 계산한 것은 **전극에 열린 소자의 전자 상태**이다. 그 상태에 전자가 얼마나 채워지는지를 구하려면 전극의 Fermi 분포를 결합해야 한다.

## 3. 전자 상태와 점유

### (1) Spectral function

Advanced Green's function을 $G^a=(G^r)^\dagger$로 정의하면, 에너지별 상태의 무게를 나타내는 **spectral function**은 다음과 같다.[1,2]

$$
A(E)=i\left[G^r(E)-G^a(E)\right].
$$

$A$와 $G^r$의 단위는 에너지의 역수이다. 정규직교 기저에서 $A_{\mu\mu}/(2\pi)$는 orbital $\mu$에 대한 density of states (DOS)이다. 비직교 기저의 공간 분포는 orbital 곱과 전체 행렬을 사용하여 복원한다. 상태가 존재하는 에너지와 그 상태가 실제로 점유되었는지는 구분해야 한다. 예를 들어 두 전극의 Fermi level보다 훨씬 높은 에너지에도 spectral peak가 존재할 수 있다.[1–4]

두 전극의 기여를 구분하는 **partial spectral function**은

$$
A_\alpha=G^r\Gamma_\alpha G^a,
\qquad A=A_L+A_R
$$

이다. $A_L$은 왼쪽 전극에서 입사한 상태가 소자 안에 만드는 spectral weight이고, $A_R$은 오른쪽 전극의 기여이다. 여기서는 별도의 내부 산란이 없고, 고려하는 상태가 전극 연속체와 연결되어 있다고 가정한다. 전극과 완전히 분리된 bound state에는 추가 spectral weight와 별도의 점유 조건이 필요하다.[1–4]

### (2) 전극별 점유를 합하는 Keldysh 관계

점유된 전자 상태는 **lesser Green's function** $G^<$로 기술한다. 에너지 적분으로 density kernel을 얻기 편하도록 $G^n\equiv-iG^<$를 정의한다. $G^n$은 점유된 상태의 spectral 행렬이고, $A$는 점유 여부와 무관한 전체 spectral 행렬이다.[1,2]

전극 $\alpha$가 주입하는 점유는 $f_\alpha\Gamma_\alpha$로 주어지며, 소자 내 전파를 양쪽에서 곱하면

$$
G^n=G^r\left(f_L\Gamma_L+f_R\Gamma_R\right)G^a
=f_LA_L+f_RA_R
$$

를 얻는다. 이는 $G^<=G^r(\Sigma_L^<+\Sigma_R^<)G^a$와 $\Sigma_\alpha^<=if_\alpha\Gamma_\alpha$를 사용한 **Keldysh 관계**이다. 모든 함수는 같은 에너지 $E$에서 평가한다.[1–4]

이 결과를 orbital 성분으로 쓰면 각 행·열의 의미가 명확해진다.

$$
G^n_{\mu\nu}(E)
=f_L(E)(A_L)_{\mu\nu}(E)
+f_R(E)(A_R)_{\mu\nu}(E).
$$

즉, 같은 orbital 쌍에도 양쪽 전극에서 온 상태가 기여하며 각 기여에 해당 전극의 점유를 곱한다. 평형에서는 $f_L=f_R=f$이므로 $G^n=fA$가 된다. 비평형에서는 $A_L$와 $A_R$를 각자 가중하여 합해야 한다. 이것이 NEGF에서 상태 계산과 점유 계산을 나누는 이유이다.[1–4]

## 4. 전자 밀도와 전류

### (1) 점유 행렬에서 전자 밀도까지

점유된 spectral 행렬을 에너지에 대해 적분하면 **density kernel** $P$를 얻는다. 이 문서에서는 다음 정규화를 사용한다.[1–4]

$$
P_{\mu\nu}
=\int_{-\infty}^{\infty}\frac{dE}{2\pi}\,
G^n_{\mu\nu}(E).
$$

$P$는 무차원이다. 정규직교 기저의 대각 성분 $P_{\mu\mu}$는 해당 orbital의 점유수이며, 비대각 성분은 orbital 사이의 coherence를 포함한다. 비직교 LCAO에서는 density kernel 전체를 기저 함수와 결합하여 전자 수 밀도를 구한다.[3,4]

$$
n(\mathbf r)=\sum_{\mu\nu}
\phi_\mu(\mathbf r)P_{\mu\nu}\phi_\nu^*(\mathbf r).
$$

밀도 전체를 표현하는 유한 기저에 대해 이를 공간 적분하면 $N=\operatorname{Tr}(PS)$이다. Overlap이 단위행렬일 때에만 $N=\operatorname{Tr}P$로 단순화된다. 열린 소자 경계의 실제 밀도를 복원할 때에는 그 위치까지 뻗어 있는 전극 기저와 경계 교차항도 포함해야 한다.[3,4]

### (2) Transmission에서 전류까지

밀도는 소자에 **얼마나 많은 전자가 분포하는지**를 나타내고, 전류는 양쪽 전극 사이에서 **얼마나 많은 전자가 순이동하는지**를 나타낸다. Coherent 수송에서 에너지별 transmission은 Caroli 식으로 계산한다.[1–4]

$$
\mathcal T(E)=
\operatorname{Tr}\left[
\Gamma_LG^r\Gamma_RG^a
\right].
$$

$\mathcal T$는 전달 확률을 채널별로 합한 무차원량이다. Trace는 소자 orbital 공간의 대각 성분을 합하는 연산이다. $G^r$가 소자 내부의 전파를, 양쪽의 $\Gamma_L,\Gamma_R$가 전극과의 연결을 포함하므로, 한쪽 전극에만 연결된 상태는 반대쪽으로 전류를 전달하지 못한다.

전류는 이 transmission에 두 전극의 점유 차이를 곱하여 적분한 **Landauer 식**으로 주어진다.[1,2]

$$
I=\frac{e}{h}\int_{-\infty}^{\infty}
\mathcal T(E)\,[f_L(E)-f_R(E)]\,dE.
$$

$h$는 Planck 상수이다. 여기서는 왼쪽에서 오른쪽으로 향하는 순전자 수송률에 $+e$를 곱한 값을 양의 $I$로 정의한다. 한 spin 성분에 대한 식이므로 독립적인 두 spin이 축퇴되어 있으면 결과를 두 배로 한다. 영온에서 $\mu_L>\mu_R$이면 적분 범위는 bias window $[\mu_R,\mu_L]$로 줄어든다. 반면 전자 밀도 계산에는 그보다 낮은 에너지에 이미 채워진 상태도 포함해야 한다.[1–4]

지금까지의 계산 순서는 다음과 같다. 각 단계에서 앞 단계의 결과를 그대로 사용한다.

| 단계 | 계산할 양 | 얻는 정보 |
| --- | --- | --- |
| 전극 연결 | $\Sigma_L^r,\Sigma_R^r$ | 반무한 전극이 소자에 미치는 영향 |
| 상태 계산 | $G^r$, $A_L$, $A_R$ | 열린 소자의 전파와 전극별 spectral weight |
| 점유 계산 | $G^n=f_LA_L+f_RA_R$ | 실제로 점유된 상태 |
| 밀도 계산 | $P$, $n(\mathbf r)$ | 전자 수와 공간 분포 |
| 전류 계산 | $\mathcal T(E)$, $I$ | 전극 사이의 순전자 전달 |

## 5. 단일 준위에서 확인하는 비평형 점유

### (1) 하나의 상태를 갖는 소자

이제 위 절차를 가장 작은 모형에 적용한다. 소자에는 정규화된 상태 $|d\rangle$ 하나만 있고, 한 spin 성분만 고려한다. 따라서 소자 Hamiltonian과 overlap은 각각 $1\times1$ 행렬이며, 모든 소자 행렬은 scalar가 된다. 이 모형은 실제로 한 상태만 있는 계의 모형이거나, 관심 에너지 구간을 하나의 공명이 지배한다고 보는 근사이다. 여러 orbital이 결합한 원래 행렬에서 대각 원소 하나만 떼어 내는 연산과는 구별한다.[1,2]

전극에 의한 실수 에너지 이동을 포함한 준위 에너지를 $\varepsilon_d$라 하고, 좌우 전극이 만드는 폭을 $\gamma_L,\gamma_R$라 하자. 여기서는 **scalar 폭에는 소문자 $\gamma_\alpha$**, 앞의 **broadening 행렬에는 대문자 $\Gamma_\alpha$**를 사용한다. Wide-band approximation에서 이 에너지와 폭을 관심 구간의 상수로 놓으면, $\gamma=\gamma_L+\gamma_R>0$에 대해[1,2]

$$
G_d^r(E)=\frac{1}{E-\varepsilon_d+i\gamma/2}
$$

이다. 같은 Green's function에서 상태와 transmission을 차례로 계산하면

$$
A_{\alpha,d}=\gamma_\alpha|G_d^r|^2,
\qquad
A_d=\gamma|G_d^r|^2,
\qquad
\mathcal T_d=\gamma_L\gamma_R|G_d^r|^2
$$

를 얻는다. $A_d$는 중심이 $\varepsilon_d$이고 반치전폭이 $\gamma$인 Lorentzian이다. 공명 중심의 transmission은 $4\gamma_L\gamma_R/\gamma^2$이며, 두 전극의 결합이 같을 때 1에 도달한다. 이는 위 scalar 식에 $E=\varepsilon_d$를 대입한 결과이다.

### (2) Effective occupation과 두 chemical potential

점유도 같은 순서로 계산한다. 전극별 spectral function에 Fermi 함수를 곱하면

$$
G_d^n=|G_d^r|^2(\gamma_Lf_L+\gamma_Rf_R)
=A_df_{\mathrm{eff}},
$$

$$
f_{\mathrm{eff}}(E)=
\frac{\gamma_Lf_L(E)+\gamma_Rf_R(E)}
{\gamma_L+\gamma_R}
$$

이다. $f_{\mathrm{eff}}$는 **에너지별 점유 가중치**이다. 왼쪽 전극과 더 강하게 결합하면 왼쪽에서 주입되는 전자의 비중이 커진다. 이 가중 평균은 두 전극의 주입을 합한 결과이며, 소자에 새로운 reservoir를 도입한 것이 아니다.[1,2]

영온에서 $\mu_L>\mu_R$인 경우를 보면 하나의 chemical potential로 표현하기 어려운 이유가 드러난다.

| 에너지 구간 | $f_L$ | $f_R$ | $f_{\mathrm{eff}}$ |
| --- | --- | --- | --- |
| $E<\mu_R$ | 1 | 1 | 1 |
| $\mu_R<E<\mu_L$ | 1 | 0 | $\gamma_L/\gamma$ |
| $E>\mu_L$ | 0 | 0 | 0 |

예를 들어 $\gamma_L:\gamma_R=3:1$이면 bias window 안의 점유 가중치는 $3/4$이다. 영온의 단일 Fermi 함수는 한 에너지에서 1에서 0으로 바뀌지만, 이 분포에는 두 전극의 chemical potential 사이에 중간 높이의 구간이 존재한다. 따라서 **$f_{\mathrm{eff}}$를 계산했다는 사실만으로 하나의 소자 chemical potential $\mu_D$가 정해지지는 않는다.** 평형에서는 두 전극의 분포가 같아져 $f_{\mathrm{eff}}=f$가 된다.[1,2]

준위의 총점유 $n_d$는 이 분포를 spectral function과 함께 적분하여 계산한다.

$$
n_d=\int\frac{dE}{2\pi}\,A_d(E)f_{\mathrm{eff}}(E),
\qquad 0\le n_d\le1.
$$

특정 에너지에서 $f_{\mathrm{eff}}=3/4$이라고 해서 준위 전체에 전자가 $3/4$개 있는 것은 아니다. 총점유에는 공명의 위치와 폭, 두 chemical potential 아래의 spectral weight가 모두 들어간다. 전류는 같은 모형의 $\mathcal T_d$를 Landauer 식에 넣어 별도로 구한다.

### (3) 여러 orbital이 있는 경우

일반적인 다중 orbital 소자로 돌아가면 점유식은 여전히 $G^n_{\mu\nu}=f_L(A_L)_{\mu\nu}+f_R(A_R)_{\mu\nu}$이다. 그러나 $A_L$와 $A_R$가 각 orbital 쌍에 서로 다른 비율로 기여하므로, 소자 전체에 공통인 scalar $f_{\mathrm{eff}}$로 묶기는 어렵다. 평형이나 $A_L=w(E)A$, $A_R=[1-w(E)]A$처럼 전극 기여가 모든 성분에서 같은 비율인 특수한 경우에는 공통 scalar 분포가 가능하다. 이 조건은 앞의 행렬 점유식에 직접 대입하여 확인할 수 있다.

따라서 일반 LCAO 계산에서는 **$G^n_{\mu\nu}$를 행렬로 계산하고 적분하여 $P_{\mu\nu}$를 얻는다.** 단일 준위의 scalar 폭 $\gamma_\alpha$를 다중 orbital 행렬의 대각 성분으로 대체하여 같은 식을 적용하면 orbital 혼합과 간섭이 빠질 수 있다.[1–4]

## 6. DFT와 연결하는 자기일관 계산

### (1) 밀도에 따른 Hamiltonian 갱신

지금까지는 소자 Hamiltonian $H_D$가 주어졌다고 가정했다. DFT에서는 Kohn–Sham Hamiltonian이 전자 밀도에 의존하므로, NEGF로 얻은 밀도를 사용하여 $H_D$를 갱신해야 한다. 이때 기저와 전극의 점유 조건은 유지하고 다음 과정을 반복한다.[3,4]

1. 입력 밀도 $n(\mathbf r)$로 $H_D[n]$를 구성한다.
2. 전극 self-energy를 포함하여 $G^r$와 $A_L,A_R$를 계산한다.
3. 정해진 $\mu_L,\mu_R$의 Fermi 함수로 $G^n$을 구하고 적분하여 $P$를 얻는다.
4. $P$로 공간 밀도를 복원하고, 입력 밀도와 혼합하여 다음 반복을 시작한다.

소자에 전극 원자층을 충분히 포함하면 바깥 경계의 전극 응답은 bulk 계산 결과로 연결할 수 있다. 밀도·전위가 수렴한 뒤 그 Hamiltonian으로 transmission과 전류를 평가한다. 이 과정은 정적인 전하 재배치를 포함하며, 비탄성 산란을 다루려면 [Inelastic electron transport](inelastic-electron-transport.md)에서 설명하는 추가 self-energy가 필요하다. 동적 다전자 상관도 별도의 근사로 다룬다.[2–4]

### (2) 전자 점유와 정전기 경계조건

전극의 **electrochemical potential $\mu_\alpha$**는 Fermi 점유를 정한다. 반면 **electrostatic potential $\varphi(\mathbf r)$**는 전하 분포와 Poisson 경계조건으로 결정되며, 전자에게 $-e\varphi$의 potential energy를 준다. 따라서 $\mu_L-\mu_R$를 지정하는 것과 소자 내부의 전위 분포를 구하는 것은 서로 연결된 두 작업이다.[1,3,4]

비직교 기저에서 일정한 전자 potential energy $\Delta_\alpha$를 전극에 더하면, 그 행렬 원소는 $\Delta_\alpha S_{\mu\nu}$이다. 전극 band와 점유를 함께 rigid shift하는 모형에서는

$$
H_\alpha\to H_\alpha+\Delta_\alpha S_\alpha,
\qquad
\mu_\alpha\to\mu_\alpha+\Delta_\alpha
$$

를 일관되게 적용한다. 전극과 연결된 소자 경계의 전위도 같은 기준을 사용해야 한다. 모든 에너지에 공통 상수를 더하는 것은 영점의 변경이고, 두 전극에 서로 다른 이동을 주는 것은 bias의 변경이다. 실제 내부 전위 강하는 자기일관 전하와 screening에 따라 구한다.[3,4]

계산 결과를 확인할 때에는 밀도·전위의 반복 수렴, 에너지 적분 격자, 전극 경계 위치를 따로 점검한다. 정상 상태의 두 전극 전류는 같은 크기로 반대 방향이어야 한다. 전극과 분리된 bound state, 큰 수치적 broadening, 불완전한 경계 밀도 처리는 이 기본 계산에 추가 검토가 필요한 경우이다.[3,4]

## 7. 요약

NEGF의 계산은 **전극을 연결한 상태를 구한 뒤, 각 전극의 분포로 그 상태를 채우는 과정**이다. $H_D,S_D,\Sigma_L^r,\Sigma_R^r$로 $G^r$를 계산하고, $A_L,A_R$에 $f_L,f_R$를 곱해 점유 행렬 $G^n$을 얻는다. 이를 적분하면 density kernel과 전자 밀도가 나오고, 같은 전파·결합 행렬로 transmission과 전류를 계산한다.

$\alpha$는 전극, $\mu,\nu$는 orbital 지표이다. $\mu_\alpha$는 전극의 electrochemical potential이며, 단일 준위의 $f_{\mathrm{eff}}$는 전극별 주입으로부터 얻은 점유 가중치이다. 일반적인 다중 orbital 문제에서는 그 점유를 하나의 chemical potential 대신 행렬로 유지한다.

## 8. 참고문헌

1. S. Datta, “Electrical Resistance: An Atomistic View,” *Nanotechnology* **15**, S433–S451 (2004). [DOI](https://doi.org/10.1088/0957-4484/15/7/051), [Author manuscript](https://arxiv.org/abs/cond-mat/0408319). §§3–4, 8의 단일 준위, broadening, 점유와 행렬 NEGF 관계를 참조한다.
2. D. A. Ryndyk, R. Gutiérrez, B. Song, and G. Cuniberti, “Green function techniques in the treatment of quantum transport at the molecular scale,” *arXiv:0805.0628v2* (2008). [Author manuscript](https://arxiv.org/abs/0805.0628v2). §2.1의 coherent 수송, §3의 Keldysh 관계, §4.2.2의 상호작용이 없는 한계와 Eq. (432)의 단일 준위 분포를 참조한다.
3. M. Brandbyge, J.-L. Mozos, P. Ordejón, J. Taylor, and K. Stokbro, “Density-functional method for nonequilibrium electron transport,” *Physical Review B* **65**, 165401 (2002). [DOI](https://doi.org/10.1103/PhysRevB.65.165401), [Author manuscript](https://arxiv.org/abs/cond-mat/0110650). §§II–IV의 영역 분할, 비직교 기저, 전극별 spectral density 및 정전기 경계조건을 참조한다. 이 논문의 broadening 정의에는 $1/2$가 포함되므로 본문의 $\Gamma=i(\Sigma^r-\Sigma^a)$와 정규화를 구분한다.
4. T. Ozaki, K. Nishio, and H. Kino, “Efficient implementation of the nonequilibrium Green function method for electronic transport calculations,” *Physical Review B* **81**, 035116 (2010). [DOI](https://doi.org/10.1103/PhysRevB.81.035116), [Author manuscript](https://arxiv.org/abs/0908.4142). §§II–III의 overlap을 포함한 Green's function, density kernel, 경계 밀도와 비평형 계산을 참조한다.
