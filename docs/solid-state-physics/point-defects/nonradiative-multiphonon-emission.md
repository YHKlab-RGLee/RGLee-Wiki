---
title: "3.2. Point defects: Nonradiative multiphonon emission"
description: deep defect의 nonradiative carrier capture를 electron–phonon coupling, Fermi golden rule과 first-principles 계산 절차로 설명
status: verified
last_verified: 2026-08-05
---

# 3.2. Point defects: Nonradiative multiphonon emission

Nonradiative multiphonon emission (NMP)은 전자나 정공이 deep defect에 포획되거나 결함에서 방출될 때, 전이 에너지를 광자 대신 여러 lattice vibration에 전달하는 과정이다. Shockley–Read–Hall recombination의 capture coefficient를 미시적으로 계산하려면 전자 상태 변화와 그에 따른 원자 재배열을 함께 다뤄야 한다.[1,2]

이 글은 희석된 국소 결함, Born–Oppenheimer potential-energy surface, 조화 진동자와 static-coupling 근사를 사용하는 first-principles NMP 정식화를 다룬다. 산화막 신뢰성의 다중 상태 phenomenological model이나 특정 시뮬레이터 사용법은 별개의 모형 계층이므로 중심 범위에서 제외한다.

## 1. NMP 포획과 SRH 재결합

### (1) 운반자 포획 주기와 capture coefficient

예를 들어 electron capture의 단위 부피당 capture rate는

$$
R_n=C_n\,N_D^+\,n
$$

으로 정의한다.[1,2] $n$은 자유전자 농도, $N_D^+$는 electron capture가 가능한 결함의 농도, $C_n$은 electron capture coefficient이며 3차원에서 단위는 부피/시간이다. 결함 하나의 capture rate는 $r_n=C_n n$이다. Hole capture는 $R_p=C_pN_A^-p$로 같은 방식으로 정의한다.

Shockley–Read–Hall (SRH) 재결합은 한 종류의 운반자가 결함에 포획된 뒤 반대 종류의 운반자가 같은 결함에 포획되는 두 단계의 주기이다. 각 포획 단계에서 전자 에너지와 결함의 평형 구조가 달라지며, NMP는 이 에너지 차이를 여러 격자 진동으로 전달하는 미시적 전이 과정이다.[1,4] 따라서 capture coefficient는 단순한 결함의 기하학적 면적이 아니라 electron–phonon coupling, 초기·최종 진동 상태의 겹침, 장거리 Coulomb 상호작용과 온도를 포함하는 전이 확률이다.[1,2]

### (2) 단일준위 SRH의 정상상태 재결합률

한 결함 준위와 두 전하 상태만 고려하면 electron capture·emission과 hole capture·emission의 네 과정이 결함 점유를 정한다. $N_t$를 전체 결함 농도, $f_t$를 결함이 전자로 점유될 확률이라 하면 정상상태 조건은

$$
\frac{df_t}{dt}
=C_n n(1-f_t)+e_p(1-f_t)-e_nf_t-C_p p f_t
=0
$$

이며,

$$
f_t
=\frac{C_n n+e_p}
{C_n n+e_n+C_p p+e_p}
$$

를 얻는다. 이때 $e_n$과 $e_p$는 각각 electron emission rate와 hole emission rate이다. 전자와 정공에 대해 같은 순 재결합률을 요구하면

$$
U
=
N_t
\frac{C_nC_pnp-e_ne_p}
{C_n n+e_n+C_p p+e_p}
$$

가 된다.[6,7] 여기서 $f_t$를 소거하는 것은 유도의 한 단계일 뿐이며, 물리적 결과는 두 포획 단계와 두 방출 단계가 함께 정하는 정상상태 재결합률이다.

열평형 detailed balance를 같은 축퇴도 규약으로 적용하여

$$
e_n=C_n n_1,\qquad
e_p=C_p p_1,\qquad
n_1p_1=n_i^2
$$

로 쓰면

$$
U_{\mathrm{SRH}}
=
\frac{N_tC_nC_p\left(np-n_i^2\right)}
{C_n(n+n_1)+C_p(p+p_1)}
=
\frac{np-n_i^2}
{\tau_{p0}(n+n_1)+\tau_{n0}(p+p_1)}
$$

을 얻는다. 여기서 $n_1$과 $p_1$은 Fermi level이 해당 결함 준위와 일치할 때의 평형 운반자 농도이고,

$$
\tau_{n0}=\frac{1}{N_tC_n},
\qquad
\tau_{p0}=\frac{1}{N_tC_p}
$$

이다.[6,7] 분모에는 전자와 정공의 포획·방출 시간이 함께 들어가므로, 한 단계가 느리면 전체 재결합 주기가 그 단계에 의해 제한된다.

### (3) SRH 식에서 NMP가 제공하는 물리량

NMP 이론은 SRH 점유 통계를 대체하는 거시적 재결합 법칙이 아니다. 한 결함 준위, 두 전하 상태, 서로 독립적인 희석 결함과 정상상태라는 가정이 유지되면 SRH 식의 꼴은 그대로이고, NMP 계산이 그 식에 들어가는 $C_n(T)$와 $C_p(T)$를 미시적으로 제공한다.[1,2,4]

| 물리량 | SRH에서의 역할 | First-principles NMP에서의 결정 방법 |
| --- | --- | --- |
| $C_n(T)$, $C_p(T)$ | 각 전하 전이의 포획 속도를 정함 | 전자 결합, 진동 상태 겹침, 에너지 보존, 축퇴도와 Coulomb 보정으로 계산 |
| $e_n(T)$, $e_p(T)$ | 결함에서 band로 되돌아가는 방출 속도를 정함 | 같은 에너지·축퇴도 규약에서 capture coefficient와 detailed balance로 연결 |
| $n_1$, $p_1$ | 결함 준위와 band edge 사이의 열평형 통계를 나타냄 | thermodynamic transition level과 band density of states로 결정 |

따라서 NMP가 추가하는 핵심은 새로운 SRH 분모가 아니라 $C_n$과 $C_p$의 미시적 내용이다. 원자 구조 변화, electron–phonon coupling, 여러 phonon을 통한 에너지 일치와 Coulomb 보정이 하나의 경험적 포획 단면적에 숨지 않고 계산 가능한 항으로 분리된다.[1,2,4]

여러 전하 상태, metastable configuration 또는 electronic excited state가 동시에 점유되거나 시간 의존성이 중요하면 단일 $f_t$의 정상상태 식으로 축약할 수 없다. 이 경우에는 상태별 점유 확률과 모든 전이 경로를 포함한 master equation이 필요하며, 개별 NMP capture coefficient는 그 방정식의 전이율 입력값이 된다.[4,8]

## 2. Configuration-coordinate 모형

### (1) 전자 상태와 potential-energy surface

전자 좌표를 $\mathbf r$, 모든 핵 좌표를 $\mathbf R$이라 하면 Born–Oppenheimer 분리에서 초기와 최종 vibronic 상태는

$$
\Psi_{im}(\mathbf r,\mathbf R)
=\psi_i(\mathbf r;\mathbf R)\chi_{im}(\mathbf R),
$$

$$
\Psi_{fn}(\mathbf r,\mathbf R)
=\psi_f(\mathbf r;\mathbf R)\chi_{fn}(\mathbf R)
$$

로 쓴다. $\psi_i$와 $\psi_f$는 각각 band state와 defect state에 해당하는 electron wavefunction이고, $\chi_{im}$과 $\chi_{fn}$은 두 전하 상태의 potential-energy surface 위 nuclear vibrational state이다.[1,3]

전자 전이가 일어나면 결함의 전하와 결합 길이가 바뀌므로 두 surface의 평형 구조도 달라진다. 이 구조 차이가 서로 다른 진동 기저 사이의 overlap을 만들고, 전자 에너지 차이를 여러 진동 양자로 전달할 수 있게 한다.[1,3]

### (2) 1차원 mass-weighted coordinate

완전한 문제는 $3N$차원 nuclear coordinate에 놓이지만, 널리 쓰이는 1차원 근사는 두 relaxed structure를 잇는 mass-weighted displacement를 accepting coordinate로 선택한다. 초기와 최종 구조를 $\mathbf R_i$, $\mathbf R_f$라 하면

$$
(\Delta Q)^2
=\sum_{\alpha}M_\alpha
\left|
\mathbf R_{f,\alpha}-\mathbf R_{i,\alpha}
\right|^2
$$

이다.[1,2] $\alpha$는 원자를 나타내며 $M_\alpha$는 원자 질량이다. 경로상의 무차원 매개변수 $\lambda$를 사용하면

$$
\mathbf R(\lambda)
=\mathbf R_i+\lambda(\mathbf R_f-\mathbf R_i),
\qquad
Q(\lambda)=Q_i+\lambda\Delta Q
$$

로 두 구조를 보간할 수 있다.

조화 근사에서 두 energy surface는

$$
E_i(Q)
=E_i^0+\frac{1}{2}\Omega_i^2(Q-Q_i)^2,
$$

$$
E_f(Q)
=E_f^0+\frac{1}{2}\Omega_f^2(Q-Q_f)^2
$$

로 쓴다.[1,2] $Q$가 mass-weighted coordinate이므로 식에 별도의 effective mass를 다시 곱하지 않는다. $\Omega_i$와 $\Omega_f$는 각 곡선의 curvature로 정한 effective angular frequency이다.

### (3) 구조 완화와 Huang–Rhys factor

두 곡선의 유효 진동수가 같아 $\Omega_i=\Omega_f=\Omega$라고 근사하면 Huang–Rhys factor는

$$
S=\frac{\Omega(\Delta Q)^2}{2\hbar}
$$

이고, 한 surface에서 다른 구조까지 수직으로 이동할 때의 relaxation energy는

$$
\lambda_{\mathrm{rel}}
=S\hbar\Omega
=\frac{1}{2}\Omega^2(\Delta Q)^2
$$

이다.[1,3] $S$는 두 변위된 조화 진동자 상태 사이의 Franck–Condon 분포를 정하는 무차원 결합 척도이다. 이를 모든 조건에서 “실제로 방출되는 평균 포논 수”와 같다고 해석해서는 안 된다. 전이 에너지, 초기 열점유와 서로 다른 두 곡률도 최종 phonon 분포에 영향을 준다.[1,3]

### (4) 다중 phonon 전이의 물리적 의미

Configuration-coordinate diagram에서 두 곡선의 교차점은 고전적인 activation picture를 제공한다. 그러나 양자역학적 capture rate는 교차 장벽만으로 정해지지 않는다. 초기 열점유 상태뿐 아니라 zero-point motion과 진동 파동함수의 tunneling tail도 최종 상태와 겹칠 수 있으므로 저온에서도 전이 확률이 남을 수 있다.[1,3]

여러 phonon이 관여한다는 말은 높은 차수의 electron–phonon perturbation을 phonon 수만큼 반복 적용한다는 뜻이 아니다. 선형 결합을 한 번 적용하더라도 서로 변위된 두 potential-energy surface의 진동 파동함수는 많은 $m\rightarrow n$ 조합에서 유한한 overlap을 갖는다. 이 진동 상태 합이 전자 에너지 차이를 여러 진동 양자의 흡수·방출로 맞춘다.[1,3,5]

## 3. Fermi golden rule capture rate

### (1) 전체 vibronic 전이율

먼저 전자와 핵 진동을 아직 분리하지 않은 식을 쓴다. Electron–phonon perturbation을 $\Delta\hat H_{\mathrm{e-ph}}$라 할 때, 1차 섭동 이론 안에서 초기 vibronic state $\Psi_{im}$에서 최종 state $\Psi_{fn}$으로 가는 한 결함의 전이율은

$$
r_{i\rightarrow f}
=\frac{2\pi}{\hbar}\,g
\sum_m w_m(T)
\sum_n
\left|
\left\langle
\Psi_{fn}
\middle|
\Delta\hat H_{\mathrm{e-ph}}
\middle|
\Psi_{im}
\right\rangle
\right|^2
\delta(E_{im}-E_{fn})
$$

이다.[1,2,5] 여기서 “전체”라는 말은 Fermi golden rule을 적용하기 전의 정확한 many-body dynamics라는 뜻이 아니라, **이 golden-rule 식 안에서 electronic 부분과 vibrational 부분을 아직 인수분해하지 않았다**는 뜻이다.

각 항의 물리적 의미는 다음과 같다.

| 항 | 물리적 의미 |
| --- | --- |
| $2\pi/\hbar$ | 1차 시간 의존 섭동 이론의 golden-rule prefactor |
| $g$ | 같은 에너지를 갖는 동등한 최종 전자·원자 배치의 수 |
| $m,n$ | 각각 초기와 최종 potential-energy surface 위의 핵 진동 양자상태 |
| $w_m(T)=e^{-\mathcal E_{im}/k_BT}/Z_i$ | 포획 직전 초기 진동 상태의 열점유 확률 |
| $\langle\Psi_{fn}|\Delta\hat H_{\mathrm{e-ph}}|\Psi_{im}\rangle$ | 원자 변위가 전자 상태를 band state에서 defect state로 바꾸는 전체 vibronic 전이 진폭 |
| $\delta(E_{im}-E_{fn})$ | 전자 에너지 차이와 모든 흡수·방출 phonon energy를 합친 전체 에너지 보존 |

정확한 용어는 **vibronic**이다. 이는 electronic state와 nuclear vibrational state가 결합된 상태를 뜻한다. 행렬원소의 절댓값 제곱은 전이가 얼마나 강한지를 정하고, delta 함수는 그 전이가 에너지상 허용되는지를 정하므로 둘 중 하나만으로 capture rate를 판단할 수 없다.[1,2,5]

### (2) Static-coupling 분해

Static-coupling 접근은 고정된 기준 구조 $\mathbf Q_0$에서

$$
\Delta\hat H_{\mathrm{e-ph}}
=
\hat H(\mathbf Q)-\hat H(\mathbf Q_0)
$$

로 섭동을 정의하고, 각 phonon coordinate $Q_k$에 대해 1차로 전개한다. 그러면 전체 vibronic 행렬원소는

$$
\left\langle
\Psi_{fn}
\middle|
\Delta\hat H_{\mathrm{e-ph}}
\middle|
\Psi_{im}
\right\rangle
\simeq
\sum_k
W_{if}^{(k)}
\left\langle
\chi_{fn}
\middle|
Q_k-Q_{0,k}
\middle|
\chi_{im}
\right\rangle
$$

로 분해되며,

$$
W_{if}^{(k)}
=
\left\langle
\psi_i
\left|
\frac{\partial \hat h}{\partial Q_k}
\right|
\psi_f
\right\rangle_{\mathbf Q_0}
$$

이다.[1,5] $W_{if}^{(k)}$가 electronic factor이고, 핵 좌표 행렬원소가 vibronic factor의 진동 부분이다. 전자는 원자 변위가 Hamiltonian과 band–defect wavefunction overlap을 얼마나 강하게 섞는지를 나타내고, 후자는 초기 구조의 진동 파동함수가 최종 구조의 에너지 보존 상태와 얼마나 겹치는지를 나타낸다.

1차원 accepting coordinate만 남기면

$$
\Delta\hat H_{\mathrm{e-ph}}
\simeq
\left.
\frac{\partial \hat h}{\partial Q}
\right|_{Q_0}
(Q-Q_0)
$$

이고,

$$
W_{if}
=
\left\langle
\psi_i
\left|
\frac{\partial \hat h}{\partial Q}
\right|
\psi_f
\right\rangle_{Q_0}
$$

를 얻는다. 이 근사에서 한 결함의 전이율은

$$
r_{i\rightarrow f}
=\frac{2\pi}{\hbar}\,g\,|W_{if}|^2
\underbrace{
\sum_m w_m(T)
\sum_n
\left|
\left\langle
\chi_{fn}
\middle|
Q-Q_0
\middle|
\chi_{im}
\right\rangle
\right|^2
\delta(E_{im}-E_{fn})
}_{X_{if}(T)}
$$

처럼 전자 결합 항 $|W_{if}|^2$와 진동 lineshape 항 $X_{if}(T)$로 나뉜다.[1,2,4] 이 분리는 static-coupling, 선형 결합과 1차원 근사를 적용한 결과이지 처음의 전체 vibronic 식이 본래 두 개의 독립 물리로 정확히 분리된다는 뜻은 아니다.

$Q$의 단위가 $\sqrt{\text{질량}}\times\text{길이}$이면 $W_{if}$의 단위는 에너지/$Q$이다. 따라서 $W_{if}\langle\chi_{fn}|Q-Q_0|\chi_{im}\rangle$는 에너지 단위의 전이 행렬원소가 되고, delta 함수의 역에너지 단위와 $2\pi/\hbar$를 합하면 $r$은 시간의 역수 단위가 된다.

조화 1차원 모형에서 $E_{im}=E_i^0+\mathcal E_{im}$, $E_{fn}=E_f^0+\mathcal E_{fn}$로 쓰면 delta 함수는

$$
\delta\!\left(
\Delta E+\mathcal E_{im}-\mathcal E_{fn}
\right)
$$

로 쓸 수 있다. $\Delta E=E_i^0-E_f^0$의 부호는 초기·최종 상태 정의에 따라 달라질 수 있으므로, 실제 계산에서는 configuration-coordinate diagram과 같은 convention을 끝까지 사용해야 한다.

### (3) 전자 결합 행렬원소

$W_{if}$는 단순한 Kohn–Sham eigenvalue 차이가 아니다. 독립입자 근사에서 $\psi_i$는 결함이 있는 supercell의 band-like state, $\psi_f$는 같은 Hamiltonian의 localized defect state여야 한다. 서로 다른 구조나 서로 다른 Hamiltonian에서 얻은 상태를 그대로 섞으면 위 섭동식의 전제가 깨진다.[1,2,4]

실무에서는 $\partial\hat h/\partial Q$를 직접 구성하는 대신 1차 섭동 이론의 관계

$$
W_{if}
=
(\epsilon_f-\epsilon_i)
\left\langle
\psi_i
\middle|
\frac{\partial\psi_f}{\partial Q}
\right\rangle
$$

를 사용한다. Projector augmented-wave (PAW) 계산에서는 overlap operator $\widetilde S$를 포함하여

$$
W_{if}
=
(\epsilon_f-\epsilon_i)
\left\langle
\widetilde\psi_i
\middle|
\widetilde S
\middle|
\frac{\partial\widetilde\psi_f}{\partial Q}
\right\rangle
$$

로 평가한다.[1,2]

위 식은 $\epsilon_f-\epsilon_i$를 사용하는 규약이다. Bra와 ket의 순서를 반대로 잡으면 문헌에 따라 전체 부호가 바뀔 수 있지만, 전이율에는 $|W_{if}|^2$가 들어가므로 일관된 규약 안에서는 결과가 같다.[1,2]

유한 차분에서는 $Q_0$ 부근의 $\langle\widetilde\psi_i(Q_0)|\widetilde S(Q_0)|\widetilde\psi_f(Q)\rangle$ 기울기를 구한다. 이 계산은 파동함수의 임의 위상과 band crossing에 민감하므로, 변위마다 overlap으로 같은 defect state를 추적해야 한다. 여러 band state가 기여하면 각 상태의 $W_{if}$와 점유를 운반자 에너지 분포에 대해 평균해야 하며, band edge의 한 상태만 쓰는 것은 추가 근사이다.[1,2,4]

### (4) 진동 lineshape

1차원 모형에서는 각 곡선의 Schrödinger 방정식

$$
\left[
-\frac{\hbar^2}{2}\frac{d^2}{dQ^2}
+E_s(Q)
\right]\chi_{s\nu}(Q)
=\mathcal E_{s\nu}\chi_{s\nu}(Q),
\qquad s\in\{i,f\}
$$

을 풀어 진동 에너지와 파동함수를 얻는다. 조화 포물선이면 해석적 진동자 상태를 사용할 수 있지만, 계산된 energy surface가 비조화적이면 $E_s(Q)$를 직접 넣어 수치적으로 풀 수 있다. 각 온도의 $w_m(T)$와 진동 행렬원소를 에너지 보존 조건에 따라 합하면 $X_{if}(T)$를 얻는다.[1,2,5]

실제 계산에서 delta 함수를 유한 폭의 Gaussian으로 바꾸면 energy-conservation error와 capture coefficient의 폭 의존성이 생길 수 있다. 진동 준위의 이산 합과 열점유 cutoff를 충분히 수렴시키고, broadening을 바꿨을 때 결과가 안정한지 확인하거나 진동 lineshape 보간법을 사용해야 한다.[2,4]

## 4. Supercell 전이율과 capture coefficient

### (1) 부피 정규화와 Coulomb 보정

주기 supercell의 band state는 계산 부피 $\widetilde V$에 정규화되므로, 결함 하나에 대해 계산한 transition rate $\widetilde r$은 $\widetilde V$에 의존한다. 3차원 bulk capture coefficient는

$$
\begin{aligned}
C(T)
&=\widetilde V f(T)\widetilde r(T)\\
&=
f(T)\widetilde V
\frac{2\pi}{\hbar}\,g\,|W_{if}|^2
\sum_m w_m(T)
\sum_n
\left|
\left\langle
\chi_{fn}
\middle|
Q-Q_0
\middle|
\chi_{im}
\right\rangle
\right|^2
\delta(E_{im}-E_{fn})
\end{aligned}
$$

로 변환한다.[1,2,4] $\widetilde V$는 delocalized band state의 정규화 부피이고, $f(T)$는 장거리 Coulomb 상호작용과 유한 supercell의 band-state 왜곡을 보정하는 factor이다. 중성 결함이면 보통 $f=1$로 두지만, 서로 끌어당기는 전하에서는 포획이 강화되고 밀어내는 전하에서는 억제된다. 따라서 $C$는 3차원에서 부피/시간 단위를 갖는다.

이 관계는 결함 농도가 낮고, 한 결함의 wavefunction이 periodic image와 겹치지 않으며, 초기 band state가 bulk-like라는 조건을 요구한다. $\widetilde V\,\widetilde r$가 cell 크기에 대해 수렴하는지 확인하지 않으면 capture coefficient를 물질 고유량처럼 보고할 수 없다.[1,2]

포획 단면적 $\sigma$를 사용하려면

$$
C(T)=\left\langle \sigma(E,T)v(E)\right\rangle
$$

처럼 운반자 속도 분포에 대한 평균 규약을 밝혀야 한다. $C/v_{\mathrm{th}}$를 단순히 단면적으로 부르는 경우에는 어떤 열속도 정의를 썼는지에 따라 값이 달라진다.

### (2) Capture와 emission의 detailed balance

같은 두 전하 상태 사이의 thermal emission rate는 평형 detailed balance로 capture coefficient와 연결할 수 있다. 그러나 이를 사용하려면 band-edge density of states, defect degeneracy, thermodynamic transition energy와 동일한 energy reference를 사용해야 한다.[1,3] Capture에서 계산한 activation energy를 emission barrier로 그대로 사용하면 안 된다.

## 5. First-principles 입력량과 수렴 검사

계산은 구조·에너지, 전자 결합, 진동 합, 거시적 정규화의 의존 순서로 진행한다. 각 단계의 출력이 다음 단계의 입력이 되므로, 최종 $C(T)$만 비교해서는 오차의 원인을 구분하기 어렵다.[1,2,4]

| 단계 | 핵심 입력과 출력 | 필수 검사 |
| --- | --- | --- |
| 전하 상태와 에너지 | 두 전하 상태의 완화 구조와 [charged defect formation energy](charged-defect-formation-energy.md)에서 얻은 thermodynamic transition energy | supercell 크기, 정전기 정정, band edge와 에너지 기준 |
| Configuration coordinate | $\Delta Q$, $E_i(Q)$, $E_f(Q)$, $\Omega_i$, $\Omega_f$ 또는 수치 potential | 보간점 수, 구조 완화, 포물선 맞춤과 비조화성 |
| 전자 결합 | 기준 구조와 인접 변위의 상태 overlap에서 얻은 $W_{if}$ | 변위 간격, 선형 맞춤 구간, 파동함수 위상, band index와 $k$-point |
| 진동 합 | $\chi_{s\nu}$, $w_m(T)$와 $X_{if}(T)$에서 얻은 $\widetilde r(T)$ | 진동 준위 cutoff, 온도별 열점유, delta 함수 처리와 lineshape 보간 |
| 거시적 계수 | $\widetilde V$, $f(T)$와 $g$를 적용한 $C_n(T)$ 또는 $C_p(T)$ | $\widetilde V\widetilde r$의 부피 수렴, Coulomb 보정과 축퇴도 규약 |

!!! info "[Measurement]"
    계산 결과에는 $C_n$ 또는 $C_p$의 구분과 단위, 온도 범위, $\Delta Q$, $\Omega_i$, $\Omega_f$, 에너지 차이, $W_{if}$, 축퇴도 $g$, Coulomb factor $f$, supercell 부피와 delta 함수 처리법을 함께 보고한다. 가장 직접적인 수치 검사는

    $$
    C(T;\widetilde V)
    =\widetilde V f\widetilde r(T;\widetilde V)
    $$

    가 supercell 크기와 vibrational-state cutoff에 대해 수렴하는지 확인하는 것이다.[1,2]

## 6. 근사와 해석상의 주의점

!!! warning "[Interpretation Caveat]"
    - **1차원 accepting mode:** 두 최소점을 잇는 직선 좌표가 모든 phonon mode의 Duschinsky 회전과 promoting mode를 담지는 못한다. 여러 mode가 비슷하게 결합하거나 경로가 휘면 다차원 처리가 필요할 수 있다.[2,4]
    - **조화·선형 결합:** 큰 구조 재배열, 결합 파괴와 강한 비조화성에서는 포물선과 $\partial\hat h/\partial Q$의 1차 전개가 약해진다.[1,4]
    - **전자구조 오차:** Capture coefficient는 transition energy와 wavefunction localization에 매우 민감하다. band gap이나 defect level을 사후 이동하는 것만으로 $W_{if}$와 structural-relaxation error가 고쳐지지는 않는다.[1,2]
    - **비아디아바틱 근사:** static-coupling Fermi golden rule은 약한 결합의 비아디아바틱 전이에 적합하다. 강한 결합과 surface 교차 부근에서는 adiabaticity를 별도로 평가해야 한다.[3,4]

NMP 계수 하나만으로 특정 소자의 bias-temperature instability, random telegraph noise 또는 장기 열화를 곧바로 결정할 수는 없다. 소자 수준에서 예측하려면 결함 분포뿐 아니라 전기장이 정하는 carrier 공급, 여러 구조 상태와 시간에 따른 kinetics까지 포함해야 한다.

## 7. 요약

1. 단일준위 정상상태에서는 SRH 식의 대수적 꼴이 유지되고, NMP가 그 안의 $C_n(T)$와 $C_p(T)$에 electronic coupling, 원자 재배열, 진동 overlap과 Coulomb 상호작용을 제공한다.
2. 여러 전하·준안정·여기 상태가 관여하면 단일준위 정상상태 SRH 식 대신 상태별 master equation이 필요하다.
3. 전체 golden-rule 식은 vibronic 행렬원소로 시작하며, static-coupling·선형 결합·1차원 근사를 적용한 뒤 $|W_{if}|^2X_{if}(T)$로 분해된다.
4. Mass-weighted $\Delta Q$와 두 energy surface는 lattice relaxation을 정량화하며, Huang–Rhys factor는 displaced harmonic oscillator의 결합 척도이다.
5. 주기 supercell transition rate는 계산 부피와 Coulomb factor를 적용해 capture coefficient로 변환해야 한다.
6. 1차원, 조화, 선형 결합과 비아디아바틱 근사의 유효성을 수렴 검사와 다차원 비교로 평가해야 한다.

## 8. 참고문헌

1. A. Alkauskas, Q. Yan, and C. G. Van de Walle, "First-principles theory of nonradiative carrier capture via multiphonon emission," *Physical Review B* **90**, 075202 (2014). [DOI](https://doi.org/10.1103/PhysRevB.90.075202).
2. M. E. Turiansky, A. Alkauskas, M. Engel, G. Kresse, D. Wickramaratne, J.-X. Shen, C. E. Dreyer, and C. G. Van de Walle, "Nonrad: Computing nonradiative capture coefficients from first principles," *Computer Physics Communications* **267**, 108056 (2021). [DOI](https://doi.org/10.1016/j.cpc.2021.108056).
3. K. Huang and A. Rhys, "Theory of light absorption and non-radiative transitions in F-centres," *Proceedings of the Royal Society of London. Series A* **204**, 406–423 (1950). [DOI](https://doi.org/10.1098/rspa.1950.0184).
4. X. Zhang, M. E. Turiansky, L. Razinkovas, M. Maciaszek, P. Broqvist, Q. Yan, J. L. Lyons, C. E. Dreyer, D. Wickramaratne, Á. Gali, A. Pasquarello, and C. G. Van de Walle, "First-principles calculations of defects and electron–phonon interactions: Seminal contributions of Audrius Alkauskas to the understanding of recombination processes," *Journal of Applied Physics* **135**, 150901 (2024). [DOI](https://doi.org/10.1063/5.0205525).
5. G. D. Barmparis, Y. S. Puzyrev, X.-G. Zhang, and S. T. Pantelides, "Theory of inelastic multiphonon scattering and carrier capture by defects in semiconductors," *Physical Review B* **92**, 214111 (2015). [DOI](https://doi.org/10.1103/PhysRevB.92.214111).
6. W. Shockley and W. T. Read, Jr., "Statistics of the Recombinations of Holes and Electrons," *Physical Review* **87**, 835–842 (1952). [DOI](https://doi.org/10.1103/PhysRev.87.835).
7. R. N. Hall, "Electron-Hole Recombination in Germanium," *Physical Review* **87**, 387 (1952). [DOI](https://doi.org/10.1103/PhysRev.87.387).
8. S. R. Kavanagh, D. O. Scanlon, A. Walsh, and C. Freysoldt, "Impact of metastable defect structures on carrier recombination in solar cells," *Faraday Discussions* **239**, 339–356 (2022). [DOI](https://doi.org/10.1039/D2FD00043A).
