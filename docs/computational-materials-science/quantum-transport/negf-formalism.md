---
description: 열린 양자계의 전극 self-energy, 비평형 점유, density matrix와 전류를 단일 준위부터 행렬식까지 설명
---

# NEGF: Formulation

Nonequilibrium Green's function (NEGF)은 반무한 전극에 연결된 유한 소자의 정상 상태 quantum transport를 기술하는 정식화이다. 이 글은 유효 단일입자 Hamiltonian, phase coherence와 정상 직류 조건을 기준으로 삼는다. 접촉이 소자 상태에서 전자를 빼내는 경로와 전자를 공급하는 경로를 함께 제공한다는 단일 준위 그림에서 출발해, 이를 여러 궤도의 행렬식으로 확장한다.[1–4]

여기서 단일 준위는 실제 소자의 모든 자유도를 대신하는 모형이 아니라, 전파·전극 결합·점유·전류의 역할을 분리해 보여 주는 최소 학술적 예시이다. 행렬식으로 확장한 뒤에도 이 네 역할의 구분은 그대로 유지된다.[1–4]

NEGF 계산에서는 다음 네 질문을 구분해야 한다.

| 질문 | 답하는 양 | 계산에서의 역할 |
| --- | --- | --- |
| 에너지 $E$의 외란이 소자 안에서 어떻게 전파되는가? | $G^R(E)$ | 상태와 전파 경로를 계산 |
| 반무한 전극을 유한 행렬에 어떻게 포함하는가? | $g_\alpha^R(E)$, $\Sigma_\alpha^R(E)$ | 열린 경계를 구성 |
| 각 전극이 상태를 얼마나 채우는가? | $f_\alpha(E)$, $G^<(E)$ | 비평형 점유와 전하를 계산 |
| 어느 정도가 반대편 전극에 도달하는가? | $T(E)$ | 단자 전류를 계산 |

Retarded Green's function만으로는 점유나 전류를 정할 수 없다. 전극의 상태, 소자–전극 결합, 전극별 Fermi 분포를 차례로 결합해야 $G^<$와 전류까지 얻는다.[1–4]

## 1. 단일 준위 열린 양자계

### (1) 고립된 준위의 Green's function

소자에 에너지 $\varepsilon_0$인 궤도 하나만 있다고 하자. 정상 Schrödinger 방정식에 에너지 $E$를 가진 외부 source $s$를 더하면

$$
(E-\varepsilon_0)\psi=s
$$

이고, 응답은

$$
\psi=G_0^R(E)s,
\qquad
G_0^R(E)=\frac{1}{E-\varepsilon_0+i\eta},
\qquad
\eta\rightarrow0^+
$$

이다. Green's function은 주어진 외부원에 대한 선형 응답을 주는 역연산자이다. $+i\eta$는 시간 영역에서 원인보다 결과가 먼저 나타나지 않는 retarded 경계조건과 전극에서 바깥으로 나가는 파동을 선택한다.[1,2]

$E$가 $\varepsilon_0$에 가까우면 응답이 커진다. 고립된 유한 소자의 가능한 에너지는 이처럼 날카로운 이산 준위로 나타난다. 그러나 실제 수송 소자는 운반자를 공급하고 멀리 운반하는 전극과 연결되어 있으므로, 고립된 $G_0^R$만으로는 정상 상태 전류를 정의할 수 없다.[1–3]

### (2) 전극 결합과 공명의 폭

왼쪽과 오른쪽 전극의 효과를 retarded self-energy

$$
\Sigma_\alpha^R(E)
=\Delta_\alpha(E)-\frac{i}{2}\Gamma_\alpha(E),
\qquad \alpha=L,R
$$

로 쓰면 연결된 준위의 Green's function은

$$
G^R(E)=
\frac{1}{
E-\varepsilon_0-\Delta_L-\Delta_R
+i(\Gamma_L+\Gamma_R)/2
}
$$

가 된다. $\Delta_\alpha$는 공명 위치를 이동시키고, $\Gamma_\alpha\ge0$는 전자가 전극 $\alpha$로 빠져나갈 수 있어 생기는 에너지 폭을 나타낸다. 날카로운 고립 준위가 유한한 수명을 가진 공명으로 바뀌는 것이다.[1–4]

이 준위의 spectral function은

$$
A(E)
=-2\,\operatorname{Im}G^R(E)
=
\frac{\Gamma_L+\Gamma_R}{
\left(E-\varepsilon_0-\Delta_L-\Delta_R\right)^2
+(\Gamma_L+\Gamma_R)^2/4
}
$$

이다. $A(E)/(2\pi)$는 단위 에너지당 이용 가능한 상태의 무게를 나타낸다. $G^R$와 $A$는 **어떤 상태가 있는가**에는 답하지만, 그 상태가 실제로 채워졌는지는 말하지 않는다.[1–4]

### (3) 점유와 전달의 분리

전극 $\alpha$의 Fermi–Dirac distribution을 $f_\alpha(E)$라 하면, 단일 준위의 에너지별 점유 무게는

$$
-iG^<(E)
=|G^R(E)|^2
\left[f_L(E)\Gamma_L(E)+f_R(E)\Gamma_R(E)\right]
$$

이다. 결합과 self-energy의 에너지 의존성을 무시하는 넓은 띠 근사에서는 유효 점유를

$$
f_{\mathrm{eff}}(E)
=
\frac{\Gamma_Lf_L+\Gamma_Rf_R}
{\Gamma_L+\Gamma_R}
$$

로 읽을 수 있다. 이는 두 전극의 Fermi 함수를 단순 평균한 값이 아니라 각 전극과의 결합 세기로 가중한 값이다.[1,3,4]

같은 모형의 transmission은

$$
T(E)
=
\Gamma_L\Gamma_R|G^R(E)|^2
=
\frac{\Gamma_L\Gamma_R}{
\left(E-\varepsilon_0-\Delta_L-\Delta_R\right)^2
+(\Gamma_L+\Gamma_R)^2/4
}
$$

이다. 전류가 흐르려면 전달에 사용할 상태가 있고, 그 상태가 양쪽 전극에 연결되며, 두 전극 사이에 점유 차이가 있어야 한다. 이 세 조건은 각각 $A(E)$, $\Gamma_L\Gamma_R$와 $f_L-f_R$에 나타난다.[1–4]

## 2. 전극 self-energy

### (1) Device–lead partition

전체 단일입자 공간을 왼쪽 전극 $L$, 소자 $D$, 오른쪽 전극 $R$로 나누면 직교 기저의 Hamiltonian은

$$
H =
\begin{pmatrix}
H_L & V_{LD} & 0 \\
V_{DL} & H_D & V_{DR} \\
0 & V_{RD} & H_R
\end{pmatrix}
$$

로 쓸 수 있다. $H_D$는 명시적으로 계산할 유한 영역, $H_\alpha$는 반무한 전극, $V_{D\alpha}=V_{\alpha D}^{\dagger}$는 경계 결합이다. 전극끼리 직접 결합하지 않는 분할을 가정한다.[1–3]

Retarded Green's function $G^R$는 주어진 에너지에서 소자에 이용 가능한 상태와 전극으로 빠져나가는 경로를 정한다. 어느 전극이 그 상태를 얼마나 채우는지는 $G^<$가 정한다. 따라서 $[(E+i\eta)I-H_D]^{-1}$만 계산하면 고립된 소자의 이산 준위만 얻을 뿐, 접촉에 의한 준위 폭이나 서로 다른 전극 점유를 포함할 수 없다.[1–4]

### (2) Schur complement와 전극 self-energy

고정된 에너지 $E$에서 $E^+=E+i\eta$와 $\eta\rightarrow0^+$를 두고, 전체 방정식

$$
\left(E^+I-H\right)G^R=I
$$

의 소자 열만 쓴다. 소자 행과 두 전극 행은

$$
\left(E^+I_D-H_D\right)G^R_{DD}
-V_{DL}G^R_{LD}-V_{DR}G^R_{RD}=I_D,
$$

$$
\left(E^+I_\alpha-H_\alpha\right)G^R_{\alpha D}
-V_{\alpha D}G^R_{DD}=0
\qquad (\alpha=L,R)
$$

가 된다. 분리된 전극에서 소자와 직접 맞닿은 표면의 Green's function을

$$
g_\alpha^R(E)=
\left[(E+i\eta)I-H_\alpha\right]^{-1}_{\mathrm{surface}}
$$

로 쓰면

$$
G^R_{\alpha D}=g_\alpha^R V_{\alpha D}G^R_{DD}
$$

이다. 이를 소자 행에 대입하고

$$
\Sigma_\alpha^R(E)
=V_{D\alpha}\,g_\alpha^R(E)\,V_{\alpha D}
$$

를 정의하면

$$
G^R(E)=
\left[
(E+i\eta)I-H_D-\Sigma_L^R(E)-\Sigma_R^R(E)
\right]^{-1}
$$

을 얻는다. 여기서 $G^R_{DD}$를 $G^R$로 간단히 썼다. 이 소거는 전극 블록에 대한 Schur complement이다. Self-energy는 전극을 단순히 삭제한 보정항이 아니라, 소자에서 전극으로 나간 진폭이 반무한 전극 안에서 전파된 뒤 소자 경계에 미치는 응답을 되돌려 놓은 항이다.[1–3]

전극의 $g_\alpha^R$를 실제로 구하는 방법은 [Surface Green's function](surface-greens-function.md)에서 다룬다.

### (3) Broadening과 spectral identity

전극 $\alpha$의 broadening 행렬은

$$
\Gamma_\alpha(E)
=i\left[\Sigma_\alpha^R(E)-\Sigma_\alpha^A(E)\right],
\qquad
\Sigma_\alpha^A=(\Sigma_\alpha^R)^\dagger
$$

로 정의한다. $\Gamma_\alpha$는 에너지와 경계 궤도에 의존하는 Hermitian 양의 준정부호 행렬이다. 전파 mode가 없는 에너지에서는 $\eta\rightarrow0^+$에 따라 해당 전극의 $\Gamma_\alpha$가 사라져야 한다.[2,5]

전체 spectral function은

$$
A(E)=i\left[G^R(E)-G^A(E)\right]
$$

이다. 탄도 두 전극 문제에서 별도의 속박 상태가 없다면

$$
A(E)=G^R(E)\left[\Gamma_L(E)+\Gamma_R(E)\right]G^A(E)
$$

가 성립한다. 별도의 속박 상태는 전극 broadening에 나타나지 않을 수 있으므로, 이 항등식을 무조건 적용하면 그 상태의 spectral weight를 누락할 수 있다.[1,2]

## 3. 비평형 점유와 관측량

### (1) Lesser Green's function과 density matrix

열평형 전극 $\alpha$의 Fermi–Dirac distribution은

$$
f_\alpha(E)=
\left[
1+\exp\left(\frac{E-\mu_\alpha}{k_BT_\alpha}\right)
\right]^{-1}
$$

이다. $\mu_\alpha$와 $T_\alpha$는 각 전극의 electrochemical potential과 온도이다. 탄도 조건에서 전극이 소자에 주입하는 상관은

$$
\Sigma_\alpha^<(E)=if_\alpha(E)\Gamma_\alpha(E)
$$

로 주어지며,

$$
\Sigma^<(E)
=i\left[f_L(E)\Gamma_L(E)+f_R(E)\Gamma_R(E)\right],
$$

$$
G^<(E)=G^R(E)\Sigma^<(E)G^A(E)
$$

가 된다.[1–4] 첫 식은 전극이 어느 에너지의 상태를 채우는지 정하고, 둘째 식은 주입된 상관이 소자 내부에서 어떻게 분포하는지 정한다.

전극별 partial spectral function을

$$
A_\alpha(E)=G^R(E)\Gamma_\alpha(E)G^A(E)
$$

로 정의하면

$$
-iG^<(E)=f_L(E)A_L(E)+f_R(E)A_R(E)
$$

이다. 일반 행렬에서는 $A_L$과 $A_R$가 궤도별·에너지별로 다르므로 전체 점유를 하나의 평균 Fermi 함수로 바꿀 수 없다.[1–4]

단일입자 density matrix는

$$
\rho
=-\frac{i}{2\pi}\int_{-\infty}^{\infty}G^<(E)\,dE
$$

로 계산한다. $G^<$는 anti-Hermitian이므로 $-iG^<$와 $\rho$가 Hermitian인지 확인할 수 있다. 스핀을 Hamiltonian에 명시적으로 포함했다면 별도의 축퇴 인자를 곱하지 않는다.[1,3,4]

직교 국소 기저에서 궤도 $n$의 local density of states (LDOS)는

$$
\operatorname{LDOS}_n(E)
=-\frac{1}{\pi}\operatorname{Im}G^R_{nn}(E)
$$

이다. Density matrix와 LDOS는 같은 양이 아니다. 전자는 실제 점유를 포함하고, 후자는 이용 가능한 상태를 나타낸다.[1–3]

### (2) Transmission과 단자 전류

왼쪽 전극에서 들어온 상태가 오른쪽 전극으로 전달될 에너지별 transmission은 Caroli 식

$$
T(E)
=\operatorname{Tr}\left[
\Gamma_L(E)G^R(E)\Gamma_R(E)G^A(E)
\right]
$$

으로 주어진다. 위상 결맞음 탄도 수송에서 왼쪽에서 오른쪽으로 흐르는 전류를 양으로 정하면

$$
I
=\frac{e}{h}\sum_{\sigma}
\int_{-\infty}^{\infty}
T_\sigma(E)\left[f_L(E)-f_R(E)\right]\,dE
$$

이다.[1–4] $\sigma$는 명시적인 스핀 채널이다. 두 스핀 채널이 축퇴되고 $T(E)$를 한 스핀에 대해 계산했다면 합을 2로 바꿀 수 있지만, 스핀 자유도가 이미 행렬에 포함되었다면 추가 인자를 곱하지 않는다.

작은 바이어스와 영온 한계에서는

$$
G_{\mathrm{lin}}
=\frac{e^2}{h}\sum_\sigma T_\sigma(E_F)
$$

가 된다. 이는 유한 바이어스 전류식을 선형화한 결과이며 일반적인 비선형 전류를 대신하지 않는다.[2–4]

### (3) 계산 의존성과 결과 해석

NEGF 계산의 의존성은

$$
\left(H_\alpha,V_{D\alpha}\right)
\longrightarrow
g_\alpha^R
\longrightarrow
\Sigma_\alpha^R,\Gamma_\alpha
\longrightarrow
G^R
\longrightarrow
\begin{cases}
G^<,\rho,\\
T(E),I
\end{cases}
$$

순서이다. $g_\alpha^R$를 얻지 않고 열린 경계를 정할 수 없으며, $G^R$를 얻지 않고 비평형 점유나 transmission을 계산할 수 없다.

!!! info "[Measurement]"
    계산 결과에는 $(\mu_L,\mu_R)$, 전극 온도, 전류의 양의 방향, spin 처리와 에너지 적분 범위를 함께 기록한다. 에너지 격자를 세분화하면서

    $$
    \delta_I
    =
    \frac{|I_{\mathrm{fine}}-I_{\mathrm{coarse}}|}
    {\max(I_{\mathrm{scale}},|I_{\mathrm{fine}}|)}
    $$

    를 평가한다. $I_{\mathrm{scale}}$은 무전류 근처에서 분모가 사라지는 것을 막기 위해 선언한 기준값이다. 같은 방식으로 전하와 주요 spectral peak의 위치도 수렴하는지 확인한다.[3,6]

## 4. 가정과 확장 범위

### (1) 비직교 기저

원자 궤도처럼 overlap 행렬 $S$가 있는 non-orthogonal basis에서는

$$
G^R(E)=
\left[
(E+i\eta)S_D-H_D-\Sigma_L^R-\Sigma_R^R
\right]^{-1}
$$

를 사용한다. 경계 결합에도 $H_{D\alpha}-ES_{D\alpha}$ 조합이 들어간다. 직교식의 $EI-H$와 비직교식의 $ES-H$를 같은 유도나 구현 안에서 섞으면 전하와 전류의 일관성이 깨질 수 있다.[3,6]

### (2) 산란과 상호작용

이 글의

$$
\Sigma^<=i\sum_\alpha f_\alpha\Gamma_\alpha
$$

는 전극만이 비평형 점유를 공급하는 유효 단일입자 탄도 문제에 해당한다. Phonon, impurity 또는 electron–electron scattering을 포함하면 scattering self-energy의 retarded·lesser 성분을 추가하고 $G^R$, $G^<$와 self-energy를 함께 수렴시켜야 한다. Strong correlation, time-dependent driving, superconducting Nambu space와 photon coupling은 각각 추가 정식화를 요구한다.[2,3]

!!! warning "[Interpretation Caveat]"
    NEGF라는 이름만으로 계산에 상호작용과 비탄성 산란이 포함되는 것은 아니다. 실제 적용 범위는 Hamiltonian과 채택한 self-energy가 결정한다. 전극 self-energy만 사용한 결과는 접촉이 열린 경계를 만들더라도 소자 내부에서는 phase-coherent ballistic transport를 가정한다.[2,3]

## 5. 요약

- $G^R$는 이용 가능한 상태와 전극으로 빠져나가는 경로를, $G^<$는 전극별 점유가 만든 비평형 density matrix를 정한다.
- 전극 self-energy는 반무한 전극의 표면 응답을 유한 소자 Green's function에 포함하며, $\Gamma_\alpha$는 전극과 연결된 상태의 폭을 나타낸다.
- 단일 준위에서는 점유가 $\Gamma_\alpha$로 가중된 Fermi 분포로 보이지만, 여러 궤도에서는 전극별 partial spectral function을 사용해야 한다.
- Transmission과 전류는 소자 상태, 양쪽 전극 결합과 점유 차이가 모두 있을 때 생긴다.
- 비직교 기저, 산란과 상호작용을 포함할 때에는 Green's function뿐 아니라 결합, density matrix와 self-energy 규약도 함께 확장해야 한다.

## 6. 참고문헌

1. M. Paulsson, "Non Equilibrium Green's Functions for Dummies: Introduction to the One Particle NEGF equations," *arXiv:cond-mat/0210519v2* (2006). [arXiv](https://arxiv.org/abs/cond-mat/0210519).
2. X. Waintal, M. Wimmer, A. Akhmerov, C. Groth, B. K. Nikolić, M. Istas, T. Ö. Rosdahl, and D. Varjas, "Computational quantum transport: A scattering approach perspective," *arXiv:2407.16257v3* (2026). [arXiv](https://arxiv.org/abs/2407.16257).
3. R. Lake, G. Klimeck, R. C. Bowen, and D. Jovanovic, "Single and multiband modeling of quantum electron transport through layered semiconductor devices," *Journal of Applied Physics* **81**, 7845–7869 (1997). [DOI](https://doi.org/10.1063/1.365394).
4. S. Datta, "Electrical Resistance: An Atomistic View," *Nanotechnology* **15**, S433–S451 (2004). [DOI](https://doi.org/10.1088/0957-4484/15/7/051), [arXiv](https://arxiv.org/abs/cond-mat/0408319).
5. C. H. Lewenkopf and E. R. Mucciolo, "The recursive Green's function method for graphene," *Journal of Computational Electronics* **12**, 203–231 (2013). [DOI](https://doi.org/10.1007/s10825-013-0458-7), [arXiv](https://arxiv.org/abs/1304.3934).
6. T. Ozaki, K. Nishio, and H. Kino, "Efficient implementation of the nonequilibrium Green function method for electronic transport calculations," *Physical Review B* **81**, 035116 (2010). [DOI](https://doi.org/10.1103/PhysRevB.81.035116), [arXiv](https://arxiv.org/abs/0908.4142).
