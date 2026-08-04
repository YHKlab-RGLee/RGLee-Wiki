---
title: "2.2. Many-body perturbation theory: RGF and NEGF scheme"
description: 초심자를 위한 open quantum system의 NEGF 수식 전개, surface Green function 알고리즘, RGF, observables와 Poisson self-consistent procedure를 설명
status: verified
last_verified: 2026-08-04
---

# 2.2. Many-body perturbation theory: RGF and NEGF scheme

Nonequilibrium Green's function (NEGF)은 반무한 전극에 연결된 유한 소자의 정상 상태 quantum transport를 기술하는 정식화이다. 이 글은 유효 단일입자 Hamiltonian, phase coherence와 정상 직류 조건을 기준으로 삼는다. Datta의 단일 준위 모형에서는 접촉이 한 준위에서 전자를 빼내는 경로와 전자를 공급하는 경로를 함께 제공한다. NEGF는 이 그림의 에너지와 결합 세기를 행렬로 확장한 것이다.[1,2,6,7]

Recursive Green's function (RGF)은 NEGF와 다른 물리 이론이 아니라, 국소 결합 Hamiltonian의 block-tridiagonal structure를 이용해 필요한 Green's function 블록만 계산하는 수치 방법이다. 따라서 먼저 open boundary와 occupation을 정의한 뒤 RGF와 Poisson self-consistent calculation을 연결해야 한다.[2,3]

초심자는 NEGF를 하나의 긴 공식으로 외우기보다 다음 네 질문을 분리하면 전체 계산을 이해하기 쉽다.

| 질문 | 답하는 양 | 계산에서의 역할 |
| --- | --- | --- |
| 에너지 $E$의 외란이 소자 안에서 어떻게 전파되는가? | $G^R(E)$ | 상태와 전파 경로를 계산 |
| 반무한 전극을 유한 행렬에 어떻게 포함하는가? | $g_\alpha^R(E)$, $\Sigma_\alpha^R(E)$ | open boundary를 구성 |
| 각 전극이 상태를 얼마나 채우는가? | $f_\alpha(E)$, $G^<(E)$ | 비평형 점유와 전하를 계산 |
| 어느 정도가 반대편 전극에 도달하는가? | $T(E)$ | 단자 전류를 계산 |

이 글은 먼저 한 개 준위에서 이 네 양의 관계를 보인 뒤 일반 행렬식을 유도한다. 그 다음 전극의 surface Green's function, 소자 내부의 RGF, Poisson–NEGF 반복 순서로 확장한다.

## 1. 단일 준위로 보는 NEGF

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

이다. 즉, Green's function은 “한 지점에 단위 source를 넣었을 때 다른 지점에서 얻는 응답”을 주는 역연산자이다. $+i\eta$는 시간 영역에서 원인보다 결과가 먼저 나타나지 않는 retarded boundary condition을 선택한다.[1,2]

$E$가 $\varepsilon_0$에 가까우면 응답이 커진다. 고립된 유한 소자에서는 가능한 에너지가 이처럼 날카로운 이산 준위로 나타난다. 그러나 실제 수송 소자는 전자를 무한히 멀리 운반할 전극과 연결되어 있으므로, 고립된 $G_0^R$만으로는 전류를 정의할 수 없다.[1,2]

### (2) 전극 연결이 준위에 만드는 변화

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

가 된다. $\Delta_\alpha$는 공명 위치를 이동시키고, $\Gamma_\alpha\ge0$는 전자가 전극 $\alpha$로 빠져나갈 수 있어 생기는 에너지 폭을 나타낸다. 날카로운 고립 준위가 폭을 가진 공명으로 바뀌는 것이다.[1,2,6,7]

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

이다. $A(E)/(2\pi)$는 단위 에너지당 이용 가능한 상태의 무게를 나타낸다. $G^R$와 $A$는 **어떤 상태가 있는가**에는 답하지만, 그 상태가 실제로 채워졌는지는 아직 말하지 않는다.[1,2]

### (3) 점유와 전류가 추가로 필요한 이유

전극 $\alpha$의 Fermi–Dirac distribution을 $f_\alpha(E)$라 하면, 단일 준위의 에너지별 점유 무게는

$$
-iG^<(E)
=|G^R(E)|^2
\left[f_L(E)\Gamma_L(E)+f_R(E)\Gamma_R(E)\right]
$$

이다. 결합과 self-energy의 에너지 의존성을 무시하는 넓은 띠 근사에서는 준위의 유효 점유를

$$
f_{\mathrm{eff}}(E)
=
\frac{\Gamma_Lf_L+\Gamma_Rf_R}
{\Gamma_L+\Gamma_R}
$$

로 읽을 수 있다. 이는 두 전극의 Fermi 함수를 단순 평균한 값이 아니라, 각 전극과의 결합 세기로 가중한 값이다.[1,2,6]

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

이다. 따라서 전류가 흐르려면 다음 세 조건이 동시에 필요하다.

1. $A(E)$가 커서 전달에 사용할 소자 상태가 있어야 한다.
2. $\Gamma_L$과 $\Gamma_R$이 모두 0이 아니어서 두 전극에 연결되어야 한다.
3. $f_L(E)-f_R(E)$가 0이 아니어서 순방향 점유 차이가 있어야 한다.

이 단일 준위의 스칼라 $\varepsilon_0$, $\Delta_\alpha$, $\Gamma_\alpha$와 $G$를 여러 궤도의 행렬로 바꾸면 다음 절의 일반 NEGF 식이 된다.[1,2,6,7]

## 2. Open boundary와 retarded Green's function

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

로 쓸 수 있다. $H_D$는 명시적으로 계산할 유한 영역, $H_\alpha$는 반무한 전극, $V_{D\alpha}=V_{\alpha D}^{\dagger}$는 경계 결합이다. 전극끼리 직접 결합하지 않는 분할을 가정한다.

이 분할 뒤에는 서로 다른 두 질문을 구분해야 한다. retarded Green's function $G^R$는 주어진 에너지에서 소자에 이용 가능한 상태와 그 상태가 전극으로 빠져나갈 수 있는지를 정한다. 반면 어느 전극이 그 상태를 얼마나 채우는지는 $G^<$가 정한다. 따라서 $[(E+i\eta)I-H_D]^{-1}$만 계산하면 **고립된** 소자의 이산 준위만 얻을 뿐, 접촉에 의한 준위 폭이나 두 전극의 서로 다른 점유를 포함할 수 없다.[1,2,6,7]

### (2) 전극이 self-energy로 바뀌는 이유

고정된 에너지 $E$에서 $E^+=E+i\eta$와 $\eta\rightarrow0^+$를 두고, 전체 retarded Green's function 방정식

$$
\left(E^+I-H\right)G^R=I
$$

의 소자 열만 쓴다. 이 열은 소자 안에서 시작한 단위 외란에 대한 응답을 뜻한다. 소자 행과 두 전극 행은 각각

$$
\left(E^+I_D-H_D\right)G^R_{DD}
-V_{DL}G^R_{LD}-V_{DR}G^R_{RD}=I_D,
$$

$$
\left(E^+I_\alpha-H_\alpha\right)G^R_{\alpha D}
-V_{\alpha D}G^R_{DD}=0
\qquad (\alpha=L,R)
$$

가 된다. 둘째 식은 “소자에서 전극으로 나간 진폭이 전극 안에서 어떻게 응답하는가”를 말한다. 분리된 전극의 표면 Green's function을

$$
g_\alpha^R(E)=
\left[(E+i\eta)I-H_\alpha\right]^{-1}_{\mathrm{surface}}
$$

로 쓰면

$$
G^R_{\alpha D}=g_\alpha^R V_{\alpha D}G^R_{DD}
$$

이다. 이 식을 첫째 식에 대입하면

$$
\left[
E^+I_D-H_D
-V_{DL}g_L^R V_{LD}
-V_{DR}g_R^R V_{RD}
\right]G^R_{DD}=I_D.
$$

여기서

$$
\Sigma_\alpha^R(E)
=V_{D\alpha}\,g_\alpha^R(E)\,V_{\alpha D}
$$

를 전극 $\alpha$의 retarded self-energy라고 정의한다. 즉, self-energy는 전극을 삭제한 보정항이 아니라 **소자 → 전극 표면 → 반무한 전극 내부 → 소자 경계**의 응답을 소자 행렬에 되돌려 놓은 항이다. 소자와 직접 결합하는 것은 전극 표면 궤도뿐이므로 반무한 전극 전체의 조밀한 역행렬이 아니라 이 표면 블록만 계산하면 된다.[1,2,6]

따라서 소자–소자 블록 $G^R_{DD}$를 이후 $G^R$로 간단히 쓰면

$$
G^R(E)=
\left[
(E+i\eta)I-H_D-\Sigma_L^R(E)-\Sigma_R^R(E)
\right]^{-1},
\qquad \eta\rightarrow 0^+
$$

가 된다. 선형대수에서 위의 대입은 전극 블록에 대한 Schur complement라고 부른다. 그러나 NEGF에서 먼저 필요한 것은 이 이름보다, 전극의 propagation을 $g_\alpha^R$로 계산해 소자 경계에 $\Sigma_\alpha^R$로 되돌린다는 물리적 순서이다. 이 소거는 주어진 단일입자 Hamiltonian과 전극 모형 안에서는 정확하며, 추가 근사는 $H_D$, 전극 또는 상호작용 self-energy를 선택할 때 들어간다.[1,2,6]

### (3) Level shift와 broadening

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

## 3. Nonequilibrium occupation과 observables

### (1) Lesser Green's function과 density matrix

앞 절의 $\Gamma_\alpha$는 소자 상태가 전극 $\alpha$로 빠져나갈 수 있는 결합을 나타내지만, 그 전극이 어떤 에너지에서 전자를 공급하는지는 말해 주지 않는다. 전극 $\alpha$가 열평형이고 Fermi–Dirac distribution이 $f_\alpha(E)$이면,

$$
f_\alpha(E)=
\left[
1+\exp\left(\frac{E-\mu_\alpha}{k_BT_\alpha}\right)
\right]^{-1}
$$

로 둔다. 탄도 조건에서 $\Sigma_\alpha^<(E)=if_\alpha(E)\Gamma_\alpha(E)$는 전극 $\alpha$가 소자에 주입하는 상관을 나타낸다. 따라서 lesser self-energy와 Keldysh 방정식은

$$
\Sigma^<(E)
=i\left[f_L(E)\Gamma_L(E)+f_R(E)\Gamma_R(E)\right],
$$

$$
G^<(E)=G^R(E)\Sigma^<(E)G^A(E)
$$

이다.[1,2,6] $\mu_\alpha$와 $T_\alpha$는 각 전극의 electrochemical potential과 온도이다. 이는 전극이 주입한 성분이 $G^R$로 소자 안을 전파하고 $G^A$로 짝지어져 소자 점유에 기여한다는 식이다.

전극별 partial spectral function을

$$
A_\alpha(E)=G^R(E)\Gamma_\alpha(E)G^A(E)
$$

로 정의하면, 탄도 두 전극 문제에서는

$$
-iG^<(E)=f_L(E)A_L(E)+f_R(E)A_R(E)
$$

로 쓸 수 있다. 즉, $G^R$가 정한 같은 소자 상태라도 왼쪽과 오른쪽 전극의 Fermi 분포가 다르면 서로 다른 비율로 채워진다. 단일 준위에서는 이 식이 접촉 결합 세기로 가중한 점유라는 Datta의 그림으로 줄어들지만, 일반 행렬에서는 $A_L$과 $A_R$가 궤도별·에너지별로 달라 단순한 하나의 평균 Fermi 함수로 바꿀 수 없다.[1,2,6]

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

### (2) Transmission과 terminal current

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

NEGF의 계산 의존성은 다음 순서로 요약된다. 뒤의 양을 먼저 정해서 앞의 양을 구할 수는 없다.

$$
\left(H_\alpha,V_\alpha\right)
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

여기서 $g_\alpha^R$를 얻는 단계가 다음 절의 surface Green function 문제이고, 큰 소자에서 $G^R$의 필요한 블록을 효율적으로 얻는 단계가 그 다음 절의 RGF 문제이다.

## 4. Surface Green function 알고리즘

### (1) Principal layer와 비선형 표면 방정식

반무한 주기 전극을 층 $n=0,1,2,\ldots$로 나누고, 한 층의 Hamiltonian을 $H_0$, 오른쪽 인접 층으로의 결합을 $V=H_{n,n+1}$로 쓰자. **principal layer**는 이 층보다 멀리 떨어진 층 사이의 직접 결합이 없도록 선택한 최소 반복 블록이다. 원래 모형에 더 먼 이웃 결합이 있으면 여러 원자층을 하나의 principal layer로 묶어 block-tridiagonal form을 만들어야 한다.[2,5,8]

표면은 $n=0$ 층이다. $n=1$부터 시작하는 나머지 반무한 전극은 원래 전극과 동일하므로, 직교 기저에서 retarded surface Green's function $g_s^R$는 자기일관적인 행렬 방정식

$$
g_s^R(E)
=
\left[
zI-H_0-Vg_s^R(E)V^\dagger
\right]^{-1},
\qquad
z=E+i\eta,\quad \eta>0
$$

을 만족한다. 가운데의 $Vg_s^RV^\dagger$는 표면에서 한 층 안쪽으로 갔다가 반무한 내부를 전파하고 되돌아오는 모든 경로를 합친 self-energy이다. 소자–전극 결합을 $\tau_\alpha$라 하면 최종 전극 self-energy는

$$
\Sigma_\alpha^R(E)
=\tau_\alpha g_{\alpha,s}^R(E)\tau_\alpha^\dagger
$$

로 얻는다.[1,2,5,8]

이 식에서 $g_s^R$가 식의 양쪽에 모두 있으므로 단순한 한 번의 역행렬로 끝나지 않는다. 고유 mode를 풀어 전극 안쪽으로 진행하거나 감쇠하는 해를 고르는 방법과, 내부 층을 반복적으로 제거하는 decimation 방법이 대표적이다. 아래에서는 구현 순서가 명확한 López Sancho repeated-doubling 방법을 사용한다.[2,4,8]

### (2) 단일 궤도 사슬의 해

먼저 각 층에 궤도가 하나이고 $H_0=\varepsilon$, $V=t$인 반무한 사슬을 보자. 표면 방정식은

$$
g_s^R
=
\frac{1}{z-\varepsilon-|t|^2g_s^R}
$$

이고, 이를 정리하면

$$
|t|^2(g_s^R)^2-(z-\varepsilon)g_s^R+1=0
$$

이다. 따라서 두 대수적 해 가운데

$$
g_s^R(E)
=
\frac{
z-\varepsilon
-\sqrt{(z-\varepsilon)^2-4|t|^2}
}{
2|t|^2
}
$$

를 retarded branch로 선택한다. 여기서 제곱근의 가지는 $\operatorname{Im}g_s^R\le0$이고 $|z|\rightarrow\infty$에서 $g_s^R\sim1/z$가 되도록 고른다. 다른 근은 전극 안쪽으로 갈수록 발산하는 해 또는 advanced boundary condition에 해당할 수 있다.[2,5]

이 예는 surface Green function 계산이 단순히 “반무한 행렬을 크게 잘라 역산하는 일”이 아님을 보여준다. 핵심은 반무한성에 맞는 해의 가지를 고르는 것이다. 다중 궤도에서는 스칼라 이차방정식 대신 행렬 방정식을 풀어야 하므로 repeated doubling이 유용하다.

### (3) López Sancho repeated-doubling

직교 기저에서 다음 네 행렬로 반복을 시작한다.

$$
\varepsilon_s^{(0)}=H_0,\qquad
\varepsilon^{(0)}=H_0,\qquad
\alpha^{(0)}=V,\qquad
\beta^{(0)}=V^\dagger.
$$

$\varepsilon_s^{(i)}$는 실제 표면층의 유효 onsite block이고, $\varepsilon^{(i)}$는 내부층의 유효 onsite block이다. $\alpha^{(i)}$와 $\beta^{(i)}$는 $i$번 decimation 뒤 남은 유효 순방향·역방향 결합이다. 각 반복에서

$$
g^{(i)}
=
\left[zI-\varepsilon^{(i)}\right]^{-1}
$$

을 계산하고 다음처럼 갱신한다.

$$
\varepsilon_s^{(i+1)}
=
\varepsilon_s^{(i)}
+\alpha^{(i)}g^{(i)}\beta^{(i)},
$$

$$
\varepsilon^{(i+1)}
=
\varepsilon^{(i)}
+\alpha^{(i)}g^{(i)}\beta^{(i)}
+\beta^{(i)}g^{(i)}\alpha^{(i)},
$$

$$
\alpha^{(i+1)}
=
\alpha^{(i)}g^{(i)}\alpha^{(i)},
\qquad
\beta^{(i+1)}
=
\beta^{(i)}g^{(i)}\beta^{(i)}.
$$

한 번의 반복은 홀수 또는 짝수 층을 제거하고, 남은 층 사이의 간격을 두 배로 만든다. 따라서 $i$번 뒤의 유효 결합은 원래 약 $2^i$개 층을 건너뛴 결합을 나타낸다. $\alpha^{(i)}$와 $\beta^{(i)}$가 충분히 작아지면 표면은 더 먼 층과 사실상 분리되고

$$
g_s^R(E)
=
\left[zI-\varepsilon_s^{(\infty)}\right]^{-1}
$$

로 계산한다. 이 갱신식은 López Sancho 방법의 decimation을 onsite block과 유효 hopping으로 쓴 것이며, 실제 NEGF 구현에서 사용하는 에너지 행렬 형태와 동등하다.[2,4,8]

구현 순서는 다음과 같다.

1. 전극 결합 범위를 모두 포함하도록 principal layer를 정하고 $H_0$, $V$를 만든다.
2. 관심 에너지마다 $z=E+i\eta$를 정하고 네 유효 행렬을 초기화한다.
3. $g^{(i)}$를 구한 뒤 $\varepsilon_s$, $\varepsilon$, $\alpha$, $\beta$를 **이전 반복값만 사용해** 동시에 갱신한다.
4. 유효 결합의 상대 norm과 surface equation residual이 모두 허용 오차보다 작아질 때까지 반복한다.
5. $g_s^R$, $\Sigma_\alpha^R$와 $\Gamma_\alpha$를 계산하고 물리·수치 검사를 수행한다.

!!! warning "[Interpretation Caveat]"
    행렬 곱은 교환되지 않는다. $\alpha g\beta$와 $\beta g\alpha$의 순서를 바꾸거나, 같은 반복 안에서 먼저 갱신한 $\alpha^{(i+1)}$를 다른 식에 사용하면 다른 알고리즘이 된다. 왼쪽 전극과 오른쪽 전극은 층 번호가 증가하는 방향이 반대일 수 있으므로 $V$와 $V^\dagger$의 배치도 전극 방향에 맞춰야 한다.[4,8]

### (4) 종료 조건과 수치 검증

유효 결합만 작아졌다고 종료하면 $g_s^R$ 자체의 방정식 오차를 놓칠 수 있다. 예를 들어 Frobenius norm을 사용할 때

$$
r_{\mathrm{hop}}^{(i)}
=
\frac{
\max\left(\|\alpha^{(i)}\|_F,\|\beta^{(i)}\|_F\right)
}{
\max\left(1,\|zI-\varepsilon^{(i)}\|_F\right)
}
$$

와 surface equation residual

$$
r_s
=
\frac{
\left\|
\left[zI-H_0-Vg_s^RV^\dagger\right]g_s^R-I
\right\|_F
}{
\|I\|_F
}
$$

을 함께 확인할 수 있다. 허용 오차는 부동소수점 정밀도와 뒤에서 필요한 transmission·전하의 정확도에 맞춰 정하고, 한 개의 보편적인 숫자로 고정하지 않는다.

$\eta$는 retarded branch를 선택하고 역행렬의 특이성을 완화하지만, 실제 스펙트럼에 인공적인 폭도 더한다. 너무 크면 band edge와 좁은 구조가 퍼지고, 너무 작으면 band edge 또는 표면 상태 근처에서 역행렬의 조건수가 나빠질 수 있다. 그러므로 $\eta$를 줄였을 때 $\Gamma_\alpha$, $T(E)$와 적분된 전하·전류가 수렴하는지 확인해야 한다.[2,8]

!!! info "[Measurement]"
    Surface Green function 구현은 에너지마다 다음 양을 저장해 검증한다.

    $$
    r_s(E),\qquad
    r_{\mathrm{hop}}(E),\qquad
    \delta_\Sigma(E)
    =
    \frac{
    \|\Sigma_\alpha^R(E;\eta)-\Sigma_\alpha^R(E;\eta/2)\|_F
    }{
    \max(1,\|\Sigma_\alpha^R(E;\eta/2)\|_F)
    }.
    $$

    또한 $\operatorname{Im}g_s^R$가 양의 준정부호가 아닌 음의 준정부호인지, $\Gamma_\alpha=i(\Sigma_\alpha^R-\Sigma_\alpha^A)$가 양의 준정부호인지 확인한다. 전파 mode가 없는 band gap에서는 $\eta\rightarrow0^+$에 따라 $\Gamma_\alpha$가 0으로 수렴해야 한다. 동일한 주기 전극을 소자와 양쪽 전극에 사용한 완전 결정 시험에서는 열려 있는 각 mode가 불필요한 경계 반사 없이 전달되어야 한다.[2,4,5,8]

비직교 기저에서는 초기 energy matrix를

$$
e_s^{(0)}=e^{(0)}=zS_{00}-H_{00},
$$

$$
\alpha^{(0)}=H_{01}-zS_{01},
\qquad
\beta^{(0)}=H_{10}-zS_{10}
$$

로 구성한다. 이어서

$$
a^{(i)}=\left[e^{(i)}\right]^{-1}\alpha^{(i)},
\qquad
b^{(i)}=\left[e^{(i)}\right]^{-1}\beta^{(i)}
$$

를 구하고

$$
e_s^{(i+1)}
=e_s^{(i)}-\alpha^{(i)}b^{(i)},
$$

$$
e^{(i+1)}
=e^{(i)}-\beta^{(i)}a^{(i)}-\alpha^{(i)}b^{(i)},
$$

$$
\alpha^{(i+1)}=\alpha^{(i)}a^{(i)},
\qquad
\beta^{(i+1)}=\beta^{(i)}b^{(i)}
$$

로 energy matrix 자체를 decimation한다. 수렴 뒤에는 $g_s^R=\lim_i[e_s^{(i)}]^{-1}$이다. 이 식은 앞의 onsite 갱신식과 같은 소거를 $zS-H$ 규약으로 표현한 것이다. 직교 기저용 $zI-H$와 비직교 기저용 $zS-H$를 한 반복 안에서 섞어서는 안 된다.[5,8]

## 5. Recursive Green's function

### (1) Block-tridiagonal structure

RGF는 앞 절에서 전극에 적용한 소거를 소자 내부 slice에 반복하는 방법이다. 왼쪽 부분을 하나의 묶음으로 보아 제거할 때마다 그 효과가 다음 slice에 에너지 의존 self-energy로 남는다. 따라서 RGF의 재귀식은 Schur complement의 별도 근사가 아니라, 필요한 Green's function 블록만 남기도록 정렬한 Gaussian elimination이다.[2,3,5]

소자 영역을 수송 방향으로 $N$개의 slice로 나누고 최근접 slice끼리만 결합시키면

$$
EI-H_D-\Sigma_L^R-\Sigma_R^R
=
\begin{pmatrix}
A_1-\Sigma_L^R & -V_{12} & 0 & \cdots \\
-V_{21} & A_2 & -V_{23} & \cdots \\
0 & -V_{32} & A_3 & \cdots \\
\vdots & \vdots & \vdots & \ddots
\end{pmatrix}
$$

가 된다. 마지막 대각 블록은 $A_N-\Sigma_R^R$이며, 내부 slice에서 $A_n=(E+i\eta)I-H_{nn}$이다. 첫째와 마지막 slice에만 각각 전극 self-energy가 들어간다.

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

로 전진 갱신할 수 있다. 여기서 $V_{n,n-1}g^L_{n-1,n-1}V_{n-1,n}$는 이미 제거한 왼쪽 slice들의 self-energy이다. 마지막 slice에서는

$$
G^R_{NN}
=\left[
A_N-\Sigma_R^R
-V_{N,N-1}g^L_{N-1,N-1}V_{N-1,N}
\right]^{-1}
$$

로 오른쪽 전극 self-energy까지 포함한다.[2,3,5] 뒤로 되짚는 단계에서는 대각 블록과 인접 블록을 복원하여 LDOS, 밀도와 국소 전류에 필요한 항을 얻는다.

각 slice의 궤도 수가 $M$이고 $N$에 무관하다고 하면 조밀한 블록 역행렬의 계산량은 대략 $\mathcal{O}(NM^3)$이다. 전체 $NM$ 차원 행렬을 직접 역산하는 $\mathcal{O}((NM)^3)$보다 길이 방향 확장성이 좋지만, 단면이 커져 $M$이 증가하면 비용은 여전히 빠르게 커진다.[2,3,5]

### (2) 전진 소거와 후진 복원

전진 단계는 마지막 slice의 Green's function만 계산하는 절차가 아니다. Transmission만 필요하면 경계 사이의 일부 블록으로 충분할 수 있지만, LDOS와 전하 밀도에는 모든 대각 블록이 필요하고 국소 전류에는 인접한 비대각 블록도 필요하다. 따라서 원하는 관측량을 먼저 정하고 전진 단계에서 후진 복원에 필요한 $g^L_{nn}$과 결합 블록을 저장해야 한다.[2,3,5]

전진 소거가 끝난 뒤 오른쪽에서 왼쪽으로 Dyson equation을 적용하면 완전히 연결된 $G^R_{nn}$과 $G^R_{n,n+1}$을 복원할 수 있다. 이 과정에서도 전체 역행렬을 만들지 않고 필요한 블록만 얻는다. RGF의 이점은 물리식을 바꾸는 데 있지 않고, 같은 Schur complement를 block-tridiagonal 연결 순서에 맞게 수행하는 데 있다.[2,3,5]

## 6. Poisson–NEGF self-consistent calculation

### (1) Electrostatic potential과 charge

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

### (2) Iteration과 convergence

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

## 7. 검증과 적용 범위

### (1) 구현 검증

다음 검사는 서로 다른 오류를 찾으므로 함께 수행한다.

- **평형 검사:** $\mu_L=\mu_R$와 같은 온도에서 순전류가 수치 오차 안에서 0인가
- **전류 보존:** 탄도 정상 상태에서 왼쪽과 오른쪽 단자 전류의 크기가 일치하는가
- **스펙트럼 항등식:** $A=i(G^R-G^A)$와 $G^R(\Gamma_L+\Gamma_R)G^A$가 일치하는가
- **균일 전극 검사:** 소자와 전극이 같은 주기계일 때 허위 반사가 나타나지 않는가
- **분할 독립성:** slice 경계와 명시적 소자 길이를 바꿔도 관심 관측량이 수렴하는가
- **적분 수렴:** 에너지 구간과 격자를 세분화해도 전하와 전류가 허용 오차 안에서 유지되는가

### (2) Non-orthogonal basis와 interactions

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

## 8. 요약

1. 단일 준위에서 $G^R$는 공명의 위치와 폭을, $G^<$는 두 전극이 결합 세기에 따라 만든 점유를 나타낸다. 일반 NEGF는 이 관계를 행렬로 확장한다.
2. 전극 self-energy는 소자에서 전극으로 나간 진폭의 응답을 유한 소자 Green's function에 되돌려 놓으며, $\Gamma_\alpha$는 전극과 결합된 상태의 폭을 나타낸다.
3. Surface Green function은 반무한 전극의 마지막 principal layer 응답이다. López Sancho 방법은 내부층을 반복적으로 decimation하여 유효 거리를 두 배씩 늘리고 $g_s^R$를 구한다.
4. $G^R$는 이용 가능한 상태와 탈출 경로를, $G^<$는 전극별 Fermi 분포가 만든 nonequilibrium occupation을 담는다. Density matrix는 $\rho=-i(2\pi)^{-1}\int G^<dE$로 계산한다.
5. RGF는 block-tridiagonal structure에서 slice를 차례로 소거해 내부 self-energy를 만들며, 길이에 선형인 계산량으로 필요한 Green's function 블록을 얻는다.
6. 실제 소자 계산은 Poisson–NEGF 반복과 surface residual, 평형, 전류 보존, 스펙트럼 항등식, 적분·분할 수렴 검사를 함께 요구한다.

## 9. 참고문헌

1. M. Paulsson, "Non Equilibrium Green's Functions for Dummies: Introduction to the One Particle NEGF equations," *arXiv:cond-mat/0210519v2* (2006). [arXiv](https://arxiv.org/abs/cond-mat/0210519).
2. X. Waintal, M. Wimmer, A. Akhmerov, C. Groth, B. K. Nikolić, M. Istas, T. Ö. Rosdahl, and D. Varjas, "Computational quantum transport: A scattering approach perspective," *arXiv:2407.16257v3* (2026). [arXiv](https://arxiv.org/abs/2407.16257).
3. S. Kazymyrenko and X. Waintal, "Knack of using Green's functions in numerical quantum transport calculations," *Physical Review B* **77**, 115119 (2008). [DOI](https://doi.org/10.1103/PhysRevB.77.115119).
4. M. P. López Sancho, J. M. López Sancho, and J. Rubio, "Highly convergent schemes for the calculation of bulk and surface Green functions," *Journal of Physics F: Metal Physics* **15**, 851–858 (1985). [DOI](https://doi.org/10.1088/0305-4608/15/4/009).
5. R. Lake, G. Klimeck, R. C. Bowen, and D. Jovanovic, "Single and multiband modeling of quantum electron transport through layered semiconductor devices," *Journal of Applied Physics* **81**, 7845–7869 (1997). [DOI](https://doi.org/10.1063/1.365394).
6. S. Datta, "Electrical Resistance: An Atomistic View," *Nanotechnology* **15**, S433–S451 (2004). [DOI](https://doi.org/10.1088/0957-4484/15/7/051), [arXiv](https://arxiv.org/abs/cond-mat/0408319).
7. S. Datta, *Quantum Transport: Atom to Transistor*, Chapters 8–11 (Cambridge University Press, 2005). [Chapter 11 DOI](https://doi.org/10.1017/CBO9781139164313.012).
8. T. Ozaki, K. Nishio, and H. Kino, "Efficient implementation of the nonequilibrium Green function method for electronic transport calculations," *Physical Review B* **81**, 035116 (2010). [DOI](https://doi.org/10.1103/PhysRevB.81.035116), [arXiv](https://arxiv.org/abs/0908.4142).
