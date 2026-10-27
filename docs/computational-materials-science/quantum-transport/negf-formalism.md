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

이 식의 $H_{D\alpha},S_{D\alpha}$는 소자와 전극 표면 기저 사이의 블록이고, $\dagger$는 켤레전치이다. Overlap 항은 비직교 기저의 일반화된 고유값 방정식 $Hc=ESc$에서 나온다. **$\Sigma_\alpha^r$는 소자 orbital 공간의 행렬**이며, 크기는 $H_D$와 같다.[3,4]

Self-energy가 나타나는 과정을 짧게 살펴보자. 전체 Green's function에서 전극 표면의 행과 소자의 열을 선택한 블록을 $G_{\alpha D}^r$라 하자. 전체 방정식 $[(E+i0^+)S_{\mathrm{full}}-H_{\mathrm{full}}]G_{\mathrm{full}}^r=I$의 전극 행을 풀면 다음 관계를 얻는다. $0^+$는 retarded 경계조건을 선택하는 양의 무한소이며, 아래 식은 실수 에너지축에서 그 극한을 취한 것이다.[2–4]

$$
G_{\alpha D}^r=g_\alpha^r\tau_{D\alpha}^{\dagger}G^r.
$$

소자 행의 방정식은 $[(E+i0^+)S_D-H_D]G^r-\sum_\alpha\tau_{D\alpha}G_{\alpha D}^r=I_D$이다. 여기에 방금 구한 전극 블록을 대입하면

$$
\left[(E+i0^+)S_D-H_D
-\sum_{\alpha=L,R}\tau_{D\alpha}g_\alpha^r\tau_{D\alpha}^{\dagger}\right]G^r=I_D
$$

가 된다. $I_D$는 소자 orbital 공간의 단위행렬이다. 이렇게 전극의 미지수를 소거하면 그 영향이 $\tau_{D\alpha}g_\alpha^r\tau_{D\alpha}^{\dagger}=\Sigma_\alpha^r$로 남는다. 전극을 고립 소자로부터 단순히 삭제하는 대신, 전극으로 전파되었다가 소자로 돌아오는 효과를 포함하는 것이다. Surface Green's function의 실제 계산은 [Surface Green's function](surface-greens-function.md)에서 다룬다.[2–4]

### (2) 소자의 응답과 준위 폭

Green's function과 고유상태의 관계는 전극에 연결하기 전의 소자에서 먼저 확인할 수 있다. 고유에너지 $\varepsilon_m$과 전개계수 벡터 $\mathbf c_m$은 $H_D\mathbf c_m=\varepsilon_m S_D\mathbf c_m$을 만족하며, $\mathbf c_m^\dagger S_D\mathbf c_n=\delta_{mn}$으로 정규화한다. 여기서 $m,n$은 고유상태 번호이다. 이 유한 기저의 모든 고유상태를 합하면 고립 소자의 Green's function은 다음과 같다.[2,4]

$$
G_0^r(E)=[(E+i0^+)S_D-H_D]^{-1}
=\sum_m\frac{\mathbf c_m\mathbf c_m^\dagger}
{E-\varepsilon_m+i0^+}.
$$

분모는 응답이 나타나는 고유에너지를 정하고, 분자의 바깥곱은 그 고유상태가 각 orbital에 어떻게 분포하는지 나타낸다. 따라서 $G^r_{0,\mu\nu}$는 고유상태들의 기여를 orbital $\mu,\nu$ 사이에서 합한 결과이다.

전극에 연결하면 앞에서 구한 self-energy를 포함하여

$$
G^r(E)=
\left[(E+i0^+)S_D-H_D
-\Sigma_L^r(E)-\Sigma_R^r(E)\right]^{-1}
$$

를 얻는다. $G^r$는 주어진 에너지에서 소자의 orbital들이 어떻게 응답하고 서로 연결되는지를 나타낸다. 전극과의 결합을 제거하면 고립 소자의 $G_0^r$로 돌아간다. 여기서 $G^r$는 비직교 기저의 **전개계수 표현**이며, 아래의 density kernel에도 같은 표현을 사용한다.[3,4]

전극 결합은 소자의 고립 준위를 이동시키고, 전자가 전극으로 빠져나갈 수 있도록 준위에 폭을 만든다. 이를 구분하기 위해

$$
\Sigma_\alpha^r
=\Lambda_\alpha-\frac{i}{2}\Gamma_\alpha,
\qquad
\Gamma_\alpha=i\left[\Sigma_\alpha^r-(\Sigma_\alpha^r)^\dagger\right]
$$

로 쓴다. Hermitian 부분 $\Lambda_\alpha$는 준위 이동과 혼성화를, **broadening matrix** $\Gamma_\alpha$는 전극과의 결합으로 발생하는 준위의 에너지 폭을 기술한다. 둘 다 에너지 단위이다. 일반적인 다중 orbital 소자에서는 두 양 모두 행렬이며, 다음의 단일 준위 예제에서만 수 하나로 표현된다.[1,2]

이 단계까지 계산한 것은 **전극에 열린 소자의 전자 상태**이다. 그 상태에 전자가 얼마나 채워지는지를 구하려면 전극의 Fermi 분포를 결합해야 한다.

## 3. 전자 상태와 점유

### (1) Spectral function

**Spectral function** $A(E)$는 전자 상태의 에너지 분포를 행렬로 나타낸다. Advanced Green's function $G^a=(G^r)^\dagger$를 사용하면 다음과 같이 정의한다.[1,2]

$$
A(E)=i\left[G^r(E)-G^a(E)\right].
$$

$A$와 $G^r$의 단위는 에너지의 역수이다. 정규직교 기저에서 $A_{\mu\mu}/(2\pi)$는 orbital $\mu$에 대한 density of states (DOS)이다. 비직교 기저에서는 전체 행렬을 기저 함수와 결합하여 local density of states (LDOS)를 복원한다.[1–4]

$$
D(\mathbf r,E)=\frac{1}{2\pi}\sum_{\mu\nu}
\phi_\mu(\mathbf r)A_{\mu\nu}(E)\phi_\nu^*(\mathbf r).
$$

합에는 해당 위치의 상태를 표현하는 데 필요한 기저를 포함한다. $D(\mathbf r,E)$는 위치 $\mathbf r$와 에너지 $E$에 존재하는 상태밀도이며, 실제 전자 점유는 다음 절에서 계산한다. 예를 들어 두 전극의 Fermi level보다 높은 에너지에도 spectral peak가 존재할 수 있다.[1–4]

소자 내부에 별도의 산란 self-energy가 없고, 전극 연속체와 연결된 상태를 고려하자. 이 조건의 retarded 극한에서 다음 행렬 항등식으로 spectral function과 전극 broadening을 연결할 수 있다.[1–4]

$$
\begin{aligned}
A&=iG^r\left[(G^a)^{-1}-(G^r)^{-1}\right]G^a\\
 &=G^r(\Gamma_L+\Gamma_R)G^a.
\end{aligned}
$$

첫째 줄은 역행렬의 차이를 이용해 $i(G^r-G^a)$를 다시 쓴 것이다. 둘째 줄에서는 두 역행렬의 $ES_D-H_D$ 항이 상쇄되고, self-energy의 차이가 $\Gamma_L+\Gamma_R$로 남는다. 따라서 전극별 **partial spectral function**을

$$
A_\alpha=G^r\Gamma_\alpha G^a,
\qquad A=A_L+A_R
$$

로 정의할 수 있다. $A_L$과 $A_R$는 각각 왼쪽과 오른쪽 전극에서 입사한 산란상태의 소자 내 기여를 나타낸다. 전극과 완전히 분리된 bound state가 있으면 그 상태의 spectral function과 점유를 별도로 더해야 한다.[1–4]

### (2) 전극별 점유를 합하는 Keldysh 관계

전자의 점유와 orbital 사이의 상관은 **lesser Green's function** $G^<$로 기술한다. 여기서는 $G^n\equiv-iG^<$를 **electron correlation function**으로 정의한다. $A$가 점유 여부와 무관한 spectral function이라면, $G^n$에는 전자가 실제로 점유한 상태의 정보가 들어간다. 두 함수의 단위는 모두 에너지의 역수이다.[1,2]

열평형인 전극 $\alpha$의 주입 상관은 **lesser self-energy** $\Sigma_\alpha^<=if_\alpha\Gamma_\alpha$로 주어진다. Coherent 정상 상태에서 전극 주입에 의해 결정되는 소자의 lesser Green's function은 다음 **Keldysh 관계**를 만족한다.[1–4]

$$
G^<=G^r\left(\Sigma_L^<+\Sigma_R^<\right)G^a.
$$

전극의 주입 상관에 $G^r$와 $G^a$를 적용하여 소자 내부의 점유 상관을 계산하는 식이다. 여기에 $\Sigma_\alpha^<=if_\alpha\Gamma_\alpha$를 대입하고 $-i$를 곱하면

$$
G^n=G^r\left(f_L\Gamma_L+f_R\Gamma_R\right)G^a
=f_LA_L+f_RA_R
$$

를 얻는다. 마지막 등호에는 앞서 정의한 $A_\alpha=G^r\Gamma_\alpha G^a$를 사용했다. 모든 함수는 같은 에너지 $E$에서 평가한다.[1–4]

이 결과를 orbital 성분으로 쓰면 각 행·열의 의미가 명확해진다.

$$
G^n_{\mu\nu}(E)
=f_L(E)(A_L)_{\mu\nu}(E)
+f_R(E)(A_R)_{\mu\nu}(E).
$$

즉, 같은 orbital 쌍에도 양쪽 전극에서 온 상태가 기여하며 각 기여에 해당 전극의 점유를 곱한다. 평형에서는 $f_L=f_R=f$이므로 $G^n=fA$가 된다. 비평형에서는 $A_L$와 $A_R$를 각자 가중하여 합해야 한다. 이것이 NEGF에서 상태 계산과 점유 계산을 나누는 이유이다.[1–4]

## 4. 전자 밀도와 전류

### (1) 점유 행렬에서 전자 밀도까지

Electron correlation function $G^n$을 에너지에 대해 적분하면 **density kernel** $P$를 얻는다. 이 문서에서는 다음 정규화를 사용한다.[1–4]

$$
P_{\mu\nu}
=\int_{-\infty}^{\infty}\frac{dE}{2\pi}\,G^n_{\mu\nu}(E)
=-i\int_{-\infty}^{\infty}\frac{dE}{2\pi}\,G^<_{\mu\nu}(E).
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

점유식에서 전류식으로 이어지는 과정도 확인할 수 있다. 왼쪽 전극에서 소자로 들어오는 순전자 수송률에 $+e$를 곱한 값을 $I$로 정의하고, $h$를 Planck 상수라 하자. 이 부호 규약에서 접촉 전류는 다음과 같다.[1,2]

$$
I=\frac{e}{h}\int dE\,
\operatorname{Tr}\left[\Gamma_L(f_LA-G^n)\right].
$$

두 항의 차이는 왼쪽 전극의 분포와 소자의 실제 점유 사이의 불균형을 나타낸다. 앞서 구한 $A=A_L+A_R$와 $G^n=f_LA_L+f_RA_R$를 대입하면

$$
\begin{aligned}
f_LA-G^n
 &=f_L(A_L+A_R)-(f_LA_L+f_RA_R)\\
 &=(f_L-f_R)A_R
\end{aligned}
$$

가 된다. 왼쪽 전극에서 입사한 상태의 기여가 상쇄되고 두 전극의 점유 차이만 남는다. 여기에 $A_R=G^r\Gamma_RG^a$를 대입하면 trace가 앞의 $\mathcal T(E)$가 되어 **Landauer 식**을 얻는다.[1,2]

$$
I=\frac{e}{h}\int_{-\infty}^{\infty}
\mathcal T(E)\,[f_L(E)-f_R(E)]\,dE.
$$

이는 한 spin 성분에 대한 식이므로 독립적인 두 spin이 축퇴되어 있으면 결과를 두 배로 한다. 영온에서 $\mu_L>\mu_R$이면 적분 범위는 bias window $[\mu_R,\mu_L]$로 줄어든다. 반면 전자 밀도 계산에는 그보다 낮은 에너지에 이미 채워진 상태도 포함해야 한다.[1–4]

지금까지의 계산 순서는 다음과 같다. 각 단계에서 앞 단계의 결과를 그대로 사용한다.

| 단계 | 계산할 양 | 얻는 정보 |
| --- | --- | --- |
| 전극 연결 | $\Sigma_L^r,\Sigma_R^r$ | 반무한 전극이 소자에 미치는 영향 |
| 상태 계산 | $G^r$, $A_L$, $A_R$ | 열린 소자의 응답과 전극별 spectral function |
| 점유 계산 | $G^n=f_LA_L+f_RA_R$ | 전자의 점유와 orbital 사이의 상관 |
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

### (2) Effective distribution function과 두 chemical potential

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

이다. $f_{\mathrm{eff}}(E)$는 단일 준위의 **effective distribution function**, 즉 에너지별 점유를 나타내는 유효 분포 함수이다. 두 Fermi 함수를 평균할 때의 가중계수는 $\gamma_L/\gamma$와 $\gamma_R/\gamma$이며, 결합이 강한 전극의 분포가 더 크게 반영된다. 따라서 분포 함수 $f_{\mathrm{eff}}$와 그것을 구성하는 결합 가중계수를 구분한다.[1,2]

영온에서 $\mu_L>\mu_R$인 경우를 보면 하나의 chemical potential로 표현하기 어려운 이유가 드러난다.

| 에너지 구간 | $f_L$ | $f_R$ | $f_{\mathrm{eff}}$ |
| --- | --- | --- | --- |
| $E<\mu_R$ | 1 | 1 | 1 |
| $\mu_R<E<\mu_L$ | 1 | 0 | $\gamma_L/\gamma$ |
| $E>\mu_L$ | 0 | 0 | 0 |

예를 들어 $\gamma_L:\gamma_R=3:1$이면 bias window 안에서 $f_{\mathrm{eff}}(E)=3/4$이다. 영온의 단일 Fermi 함수는 한 에너지에서 1에서 0으로 바뀌지만, 이 분포에는 두 전극의 chemical potential 사이에 중간 높이의 구간이 존재한다. 따라서 **$f_{\mathrm{eff}}$를 계산했다는 사실만으로 하나의 소자 chemical potential $\mu_D$가 정해지지는 않는다.** 평형에서는 두 전극의 분포가 같아져 $f_{\mathrm{eff}}=f$가 된다.[1,2]

준위의 총점유를 계산하기 전에 상태 수의 정규화를 확인하자. 위 Lorentzian을 전 에너지축에 정의한 wide-band 모형에서는[1,2]

$$
\int_{-\infty}^{\infty}\frac{dE}{2\pi}\,A_d(E)=1
$$

이다. 이는 한 spin 성분에 대해 이용 가능한 상태가 하나라는 뜻이다. 전극 결합은 그 상태의 에너지 분포를 넓히며, 실제로 채워진 전자 수는 $f_{\mathrm{eff}}$까지 포함하여 계산한다. 따라서 준위의 총점유 $n_d$는

$$
n_d=\int\frac{dE}{2\pi}\,A_d(E)f_{\mathrm{eff}}(E),
\qquad 0\le n_d\le1.
$$

로 주어진다. $f_{\mathrm{eff}}(E)$는 특정 에너지에서의 분포이고, $n_d$는 공명의 위치와 폭까지 반영한 적분값이다. 영온의 Fermi 함수는 $E<\mu_\alpha$에서 1이므로, 위 Lorentzian을 각 전극의 chemical potential까지 적분하면 다음 결과를 얻는다.

$$
n_d=\frac12+\frac1\pi
\sum_{\alpha=L,R}\frac{\gamma_\alpha}{\gamma}
\arctan\frac{2(\mu_\alpha-\varepsilon_d)}{\gamma}.
$$

예를 들어 $\gamma_L=\gamma_R=\gamma/2$이고 $\mu_L-\varepsilon_d=\varepsilon_d-\mu_R=\gamma/2$이면 두 arctangent 항이 상쇄되어 $n_d=1/2$이다. 같은 모형의 transmission을 Landauer 식에 넣으면 $I=e\gamma\pi/(4h)>0$을 얻는다. 반면 평형에서 $\mu_L=\mu_R=\varepsilon_d$이면 점유는 여전히 $1/2$이지만 전류는 0이다. 이 예는 **총점유와 순전자 흐름이 서로 다른 물리량**임을 보여 준다. 두 결과는 위 식들을 해당 조건에서 직접 적분한 값이다.[1,2]

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

NEGF의 계산은 **전극을 연결한 상태를 구한 뒤, 각 전극의 분포로 그 상태를 채우는 과정**이다. $H_D,S_D,\Sigma_L^r,\Sigma_R^r$로 $G^r$를 계산하고, $A_L,A_R$에 $f_L,f_R$를 곱해 electron correlation function $G^n$을 얻는다. 이를 적분하면 density kernel과 전자 밀도가 나오고, 같은 전파·결합 행렬로 transmission과 전류를 계산한다.

$\alpha$는 전극, $\mu,\nu$는 orbital 지표이다. $\mu_\alpha$는 전극의 electrochemical potential이며, 단일 준위의 $f_{\mathrm{eff}}$는 두 전극의 Fermi 분포를 결합 세기에 따라 평균한 유효 분포 함수이다. 일반적인 다중 orbital 문제에서는 그 점유를 하나의 chemical potential 대신 행렬로 유지한다.

## 8. 참고문헌

1. S. Datta, “Electrical Resistance: An Atomistic View,” *Nanotechnology* **15**, S433–S451 (2004). [DOI](https://doi.org/10.1088/0957-4484/15/7/051), [Author manuscript](https://arxiv.org/abs/cond-mat/0408319). §§3–4, 8의 단일 준위, broadening, 점유와 행렬 NEGF 관계를 참조한다.
2. D. A. Ryndyk, R. Gutiérrez, B. Song, and G. Cuniberti, “Green function techniques in the treatment of quantum transport at the molecular scale,” *arXiv:0805.0628v2* (2008). [Author manuscript](https://arxiv.org/abs/0805.0628v2). §2.1의 coherent 수송, §3의 Keldysh 관계, §4.2.2의 상호작용이 없는 한계와 Eq. (432)의 단일 준위 분포를 참조한다.
3. M. Brandbyge, J.-L. Mozos, P. Ordejón, J. Taylor, and K. Stokbro, “Density-functional method for nonequilibrium electron transport,” *Physical Review B* **65**, 165401 (2002). [DOI](https://doi.org/10.1103/PhysRevB.65.165401), [Author manuscript](https://arxiv.org/abs/cond-mat/0110650). §§II–IV의 영역 분할, 비직교 기저, 전극별 spectral density 및 정전기 경계조건을 참조한다. 이 논문의 broadening 정의에는 $1/2$가 포함되므로 본문의 $\Gamma=i(\Sigma^r-\Sigma^a)$와 정규화를 구분한다.
4. T. Ozaki, K. Nishio, and H. Kino, “Efficient implementation of the nonequilibrium Green function method for electronic transport calculations,” *Physical Review B* **81**, 035116 (2010). [DOI](https://doi.org/10.1103/PhysRevB.81.035116), [Author manuscript](https://arxiv.org/abs/0908.4142). §§II–III의 overlap을 포함한 Green's function, density kernel, 경계 밀도와 비평형 계산을 참조한다.
