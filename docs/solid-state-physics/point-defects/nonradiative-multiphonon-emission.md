---
title: "3.2. Point defects: Nonradiative multiphonon emission"
description: deep defect의 nonradiative carrier capture를 electron–phonon coupling, Fermi golden rule과 first-principles 계산 절차로 설명
status: verified
last_verified: 2026-08-05
---

# 3.2. Point defects: Nonradiative multiphonon emission

Nonradiative multiphonon emission (NMP)은 전자나 정공이 deep defect에 포획되거나 결함에서 방출될 때, 전이 에너지를 광자 대신 여러 lattice vibration에 전달하는 과정이다. Shockley–Read–Hall recombination의 capture coefficient를 미시적으로 계산하려면 전자 상태 변화와 그에 따른 원자 재배열을 함께 다뤄야 한다.[1,2]

이 글은 희석된 국소 결함, Born–Oppenheimer potential-energy surface, 조화 진동자와 static-coupling 근사를 사용하는 first-principles NMP 정식화를 다룬다. 산화막 신뢰성의 다중 상태 phenomenological model이나 특정 시뮬레이터 사용법은 별개의 모형 계층이므로 중심 범위에서 제외한다.

## 1. SRH rate equation과 NMP의 역할

### (1) 거시적 포획 계수

Electron capture를 예로 들면 단위 부피당 capture rate는

$$
R_n=C_n\,N_D^+\,n
$$

으로 정의한다.[1,2] $n$은 자유전자 농도, $N_D^+$는 electron capture가 가능한 결함의 농도, $C_n$은 electron capture coefficient이며 3차원에서 단위는 부피/시간이다. 결함 하나의 capture rate는 $r_n=C_n n$이다. Hole capture는 $R_p=C_pN_A^-p$로 같은 방식으로 정의한다.

Capture coefficient는 단순한 결함의 기하학적 면적이 아니다. Electron–phonon coupling, 초기·최종 vibrational state의 overlap, 전하 상태의 long-range Coulomb interaction과 온도를 모두 포함한다.[1,8]

### (2) SRH 식에서 결함 점유율 제거

전통적인 Shockley–Read–Hall (SRH) 모형은 한 결함 준위와 두 전하 상태 사이에서 일어나는 네 가지 기본 과정을 세는 정상상태 rate equation이다. $N_t$를 전체 결함 농도, $f_t$를 결함이 전자 하나로 점유될 확률이라 하면 각 과정의 단위 부피당 전이율은

$$
\begin{aligned}
r_{n,\mathrm{cap}}&=C_n nN_t(1-f_t),&
r_{n,\mathrm{em}}&=e_nN_tf_t,\\
r_{p,\mathrm{cap}}&=C_p pN_tf_t,&
r_{p,\mathrm{em}}&=e_pN_t(1-f_t)
\end{aligned}
$$

이다.[6,7] Electron capture와 hole emission은 결함의 전자 점유를 늘리고, electron emission과 hole capture는 점유를 줄인다. 따라서 정상상태 조건은

$$
\frac{df_t}{dt}
=C_n n(1-f_t)+e_p(1-f_t)-e_nf_t-C_p p f_t
=0
$$

이며, 이 식에서

$$
f_t
=\frac{C_n n+e_p}
{C_n n+e_n+C_p p+e_p}
$$

를 얻는다. 순 재결합률은 전자 쪽과 정공 쪽에서 동일해야 하므로

$$
\begin{aligned}
U
&=r_{n,\mathrm{cap}}-r_{n,\mathrm{em}}\\
&=r_{p,\mathrm{cap}}-r_{p,\mathrm{em}}\\
&=
N_t
\frac{C_nC_pnp-e_ne_p}
{C_n n+e_n+C_p p+e_p}
\end{aligned}
$$

가 된다.[6,7]

열평형 detailed balance를 같은 축퇴도 규약으로 적용하여

$$
e_n=C_n n_1,\qquad
e_p=C_p p_1,\qquad
n_1p_1=n_i^2
$$

로 쓰면 익숙한 SRH 식

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

이다.[6,7] 이 유도에서 SRH 식의 분모는 전자 포획 단계와 정공 포획 단계가 직렬로 이어지며, 느린 단계가 전체 재결합 주기를 제한한다는 점을 나타낸다.

### (3) 전통적 SRH와 first-principles NMP의 차이

NMP 이론은 SRH의 점유율 계산을 폐기하는 새로운 거시적 재결합 법칙이 아니다. 한 결함 준위, 두 전하 상태, 서로 독립적인 희석 결함과 정상상태라는 SRH 가정이 유지되면 **최종 식의 꼴은 그대로이고**, NMP 계산이 그 식에 들어가는 $C_n(T)$와 $C_p(T)$를 미시적으로 제공한다.[1,4,8] 이런 의미에서 NMP 결과를 넣은 식을 SRH-like rate equation이라고 부를 수 있다.

| 구분 | 전통적인 SRH 매개변수화 | First-principles NMP를 넣은 SRH-like 식 |
| --- | --- | --- |
| 포획 계수 | 흔히 $C_{n,p}=\langle\sigma_{n,p}v\rangle$로 두고 $\sigma$를 실험 맞춤값이나 상수로 취급 | $C_{n,p}(T)$를 electronic coupling, 진동 파동함수, 에너지 보존, 축퇴도와 장거리 Coulomb factor에서 계산 |
| 온도 의존성 | $v_{\mathrm{th}}(T)$ 또는 경험적인 $\sigma(T)$에 포함 | 초기 진동 상태의 열점유, 양자 터널링, 활성화 장벽, Coulomb factor와 운반자 에너지 평균에서 발생 |
| 결함 에너지의 역할 | $n_1$, $p_1$과 방출률을 정하는 단일 준위 매개변수 | 두 전하 상태의 thermodynamic transition energy뿐 아니라 구조 완화, 두 potential-energy surface와 $W_{if}$를 함께 결정 |
| 결함 전하 | 포획 단면적에 암묵적으로 포함하는 경우가 많음 | 끌림·밀어냄에 따른 장거리 Coulomb 보정을 $f(T)$로 분리해 계산 |
| 방출 과정 | $e_n=C_nn_1$, $e_p=C_pp_1$로 매개변수화 | 같은 미시적 두 상태에 대해 계산한 포획 계수와 detailed balance를 일관된 에너지·축퇴도 규약으로 연결 |

따라서 달라지는 핵심은 분자와 분모의 대수적 구조가 아니라 $C_n$과 $C_p$의 내용이다. 전통적 표기에서 각 $\sigma_{n,p}$에 묶여 있던 결함의 원자 구조, charge-state relaxation, electron–phonon coupling, 여러 phonon을 통한 에너지 일치와 Coulomb focusing이 NMP에서는 계산 가능한 항으로 드러난다.[1,4,8]

반대로 여러 전하 상태나 metastable configuration이 동시에 점유되거나, electronic excited state를 경유하거나, 결함 사이 상호작용과 시간 의존 점유가 중요하면 하나의 $f_t$를 제거해 얻은 위 단일준위 SRH 식으로 축약할 수 없다. 이때에는 각 상태와 전이 경로를 포함한 master equation을 풀어야 하며, 개별 NMP capture coefficient만 계산했다고 해서 단일준위 SRH 식이 자동으로 정당화되지는 않는다.[1,4]

### (4) Born–Oppenheimer 상태

전자 좌표를 $\mathbf r$, 모든 핵 좌표를 $\mathbf R$이라 하면 초기와 최종 vibronic 상태를

$$
\Psi_{im}(\mathbf r,\mathbf R)
=\psi_i(\mathbf r;\mathbf R)\chi_{im}(\mathbf R),
$$

$$
\Psi_{fn}(\mathbf r,\mathbf R)
=\psi_f(\mathbf r;\mathbf R)\chi_{fn}(\mathbf R)
$$

로 분리한다. $\psi_i$와 $\psi_f$는 각각 band state와 defect state에 해당하는 electron wavefunction이고, $\chi_{im}$과 $\chi_{fn}$은 두 전하 상태의 potential-energy surface 위 nuclear vibrational state이다.[1,3]

전자 전이가 일어나면 결함의 전하와 결합 길이가 바뀌므로 두 surface의 평형 구조도 달라진다. 전자 에너지 차이가 한 개의 포논 에너지보다 훨씬 커도 여러 진동 양자의 동시 교환으로 에너지를 보존할 수 있다는 것이 NMP의 핵심이다.[1,3]

## 2. 1차원 configuration coordinate

### (1) Mass-Weighted Coordinate

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

조화 근사에서 두 adiabatic energy surface는

$$
E_i(Q)
=E_i^0+\frac{1}{2}\Omega_i^2(Q-Q_i)^2,
$$

$$
E_f(Q)
=E_f^0+\frac{1}{2}\Omega_f^2(Q-Q_f)^2
$$

로 쓴다.[1,2] $Q$가 mass-weighted coordinate이므로 식에 별도의 effective mass를 다시 곱하지 않는다. $\Omega_i$와 $\Omega_f$는 각 곡선의 curvature로 정한 effective angular frequency이다.

### (2) Relaxation Energy와 Huang–Rhys Factor

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

이다.[1,3] $S$는 두 변위된 조화 진동자 상태 사이의 Franck–Condon 분포를 정하는 무차원 결합 척도이다. 일반적으로 “실제로 방출되는 평균 포논 수”와 언제나 동일하다고 해석해서는 안 된다. 전이 에너지, 초기 열점유와 서로 다른 두 곡률도 최종 phonon 분포에 영향을 준다.[1,3]

곡선의 교차점은 고전적인 activation picture를 제공하지만, quantum capture rate는 crossing barrier만으로 정해지지 않는다. 저온에서는 vibrational wavefunction의 tunneling tail과 zero-point motion도 기여한다.[1,3]

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

이다.[1,5,8] 여기서 “전체”라는 말은 Fermi golden rule을 적용하기 전의 정확한 many-body dynamics라는 뜻이 아니라, **이 golden-rule 식 안에서 electronic 부분과 vibrational 부분을 아직 인수분해하지 않았다**는 뜻이다.

각 항의 물리적 의미는 다음과 같다.

| 항 | 물리적 의미 |
| --- | --- |
| $2\pi/\hbar$ | 1차 시간 의존 섭동 이론의 golden-rule prefactor |
| $g$ | 같은 에너지를 갖는 동등한 최종 전자·원자 배치의 수 |
| $m,n$ | 각각 초기와 최종 potential-energy surface 위의 핵 진동 양자상태 |
| $w_m(T)=e^{-\mathcal E_{im}/k_BT}/Z_i$ | 포획 직전 초기 진동 상태의 열점유 확률 |
| $\langle\Psi_{fn}|\Delta\hat H_{\mathrm{e-ph}}|\Psi_{im}\rangle$ | 원자 변위가 전자 상태를 band state에서 defect state로 바꾸는 전체 vibronic 전이 진폭 |
| $\delta(E_{im}-E_{fn})$ | 전자 에너지 차이와 모든 흡수·방출 phonon energy를 합친 전체 에너지 보존 |

정확한 용어는 **vibronic**이다. 이는 electronic state와 nuclear vibrational state가 결합된 상태를 뜻한다. 행렬원소의 절댓값 제곱은 전이가 얼마나 강한지를 정하고, delta 함수는 그 전이가 에너지상 허용되는지를 정하므로 둘 중 하나만으로 capture rate를 판단할 수 없다.[1,5,8]

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

$Q$의 단위가 $\sqrt{\text{질량}}\times\text{길이}$이면 $W_{if}$의 단위는 에너지/$Q$이다. 따라서 $W_{if}\langle\chi_{fn}|Q-Q_0|\chi_{im}\rangle$는 에너지 단위의 전이 행렬원소가 되고, delta 함수의 역에너지 단위와 $2\pi/\hbar$를 합하면 $r$은 시간의 역수 단위가 된다. 주기 supercell에서 바로 사용하는 최종 1차원 식은

$$
C(T)
=
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
$$

이다.[1,2,8] $\widetilde V$는 delocalized band state의 정규화 부피이고, $f(T)$는 장거리 Coulomb 상호작용과 유한 supercell의 band-state 왜곡을 보정하는 factor이다. 따라서 $C$는 3차원에서 부피/시간 단위를 갖는다.

조화 1차원 모형에서 $E_{im}=E_i^0+\mathcal E_{im}$, $E_{fn}=E_f^0+\mathcal E_{fn}$로 쓰면 delta 함수는

$$
\delta\!\left(
\Delta E+\mathcal E_{im}-\mathcal E_{fn}
\right)
$$

로 쓸 수 있다. $\Delta E=E_i^0-E_f^0$의 부호는 초기·최종 상태 정의에 따라 달라질 수 있으므로, 실제 계산에서는 configuration-coordinate diagram과 같은 convention을 끝까지 사용해야 한다.

### (3) 전자 결합 항의 실제 계산

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

로 평가한다.[1,2] 실제 절차는 다음과 같다.

위 식은 $\epsilon_f-\epsilon_i$를 사용하는 규약이다. Bra와 ket의 순서를 반대로 잡으면 문헌에 따라 전체 부호가 바뀔 수 있지만, 전이율에는 $|W_{if}|^2$가 들어가므로 일관된 규약 안에서는 결과가 같다.[1,2]

1. $Q_0$ 부근에 작은 양·음의 변위를 갖는 여러 구조를 만든다.
2. 기준 구조의 band-like state $\psi_i(Q_0)$와 각 변위 구조의 defect state $\psi_f(Q)$를 상태의 성격과 파동함수 overlap으로 추적한다.
3. $\langle\psi_i(Q_0)|\psi_f(Q)\rangle$ 또는 PAW 일반화 overlap을 $Q$에 대해 선형 맞춤하여 기울기를 구한다.
4. 그 기울기에 $\epsilon_f-\epsilon_i$를 곱하고, 변위 간격·맞춤 구간·파동함수 위상·band index·$k$-point·supercell 크기에 대한 수렴을 확인한다.[1,2,4]

이 계산은 파동함수의 임의 위상과 band crossing에 민감하므로, eigenvalue 순서만 보고 defect state를 선택해서는 안 된다. 여러 band state가 기여하면 각 상태의 $W_{if}$와 점유를 계산해 운반자 에너지 분포에 대해 평균해야 한다. Band-edge 또는 열속도를 대표하는 한 상태만 쓰는 것은 추가 근사이다.[1,4]

### (4) 진동 항의 실제 계산

1차원 모형에서는 각 곡선의 Schrödinger 방정식

$$
\left[
-\frac{\hbar^2}{2}\frac{d^2}{dQ^2}
+E_s(Q)
\right]\chi_{s\nu}(Q)
=\mathcal E_{s\nu}\chi_{s\nu}(Q),
\qquad s\in\{i,f\}
$$

을 풀어 진동 에너지와 파동함수를 얻는다. 조화 포물선이면 해석적 진동자 상태를 사용할 수 있지만, 계산된 energy surface가 비조화적이면 $E_s(Q)$를 직접 넣어 수치적으로 풀 수 있다.[1,2,5]

Vibronic factor는 다음 순서로 계산한다.

1. 두 전하 상태를 각각 완화하여 $\mathbf R_i$, $\mathbf R_f$와 $\Delta Q$를 구한다.
2. 두 구조 사이 여러 $Q$에서 각 전하 상태의 총에너지를 계산하여 $E_i(Q)$와 $E_f(Q)$를 만든다.
3. 포물선 맞춤 또는 수치 potential로 $\chi_{s\nu}(Q)$와 $\mathcal E_{s\nu}$를 구한다.
4. 각 온도에서 $w_m(T)$를 정규화하고, $\langle\chi_{fn}|Q-Q_0|\chi_{im}\rangle$를 해석적 displaced-oscillator 식이나 수치 적분으로 계산한다.
5. 에너지 보존 조건을 만족하는 $m,n$ 쌍을 합하여 $X_{if}(T)$를 얻는다.[1,2,4,5]

여러 phonon이 관여한다는 의미는 perturbation Hamiltonian을 높은 차수로 여러 번 적용한다는 뜻이 아니다. 선형 electronic coupling을 한 번 적용해도, 서로 크게 변위된 두 potential-energy surface의 진동 파동함수는 많은 $m\rightarrow n$ 조합에서 유한한 overlap을 가지므로 여러 진동 양자를 동시에 교환할 수 있다.[1,3,5]

실제 계산에서 delta 함수를 유한 폭의 Gaussian으로 바꾸면 energy-conservation error와 capture coefficient의 폭 의존성이 생길 수 있다. 진동 준위의 이산 합과 열점유 cutoff를 충분히 수렴시키고, broadening을 바꿨을 때 결과가 안정한지 확인하거나 진동 lineshape 보간법을 사용해야 한다.[2,4]

## 4. Supercell Rate에서 Capture Coefficient로

### (1) Volume Normalization

주기 supercell의 band state는 계산 부피 $\widetilde V$에 정규화되므로, 결함 하나에 대해 계산한 transition rate $\widetilde r$은 $\widetilde V$에 의존한다. 3차원 bulk capture coefficient는

$$
C=\widetilde V\,f\,\widetilde r
$$

로 변환한다.[1,2,4] $f$는 결함과 자유 운반자 사이의 장거리 Coulomb 상호작용을 반영하는 Sommerfeld factor이다. 중성 결함이면 보통 $f=1$로 두지만, 서로 끌어당기는 전하에서는 포획이 강화되고 밀어내는 전하에서는 억제된다.

이 관계는 결함 농도가 낮고, 한 결함의 wavefunction이 periodic image와 겹치지 않으며, 초기 band state가 bulk-like라는 조건을 요구한다. $\widetilde V\,\widetilde r$가 cell 크기에 대해 수렴하는지 확인하지 않으면 capture coefficient를 물질 고유량처럼 보고할 수 없다.[1,2]

포획 단면적 $\sigma$를 사용하려면

$$
C(T)=\left\langle \sigma(E,T)v(E)\right\rangle
$$

처럼 운반자 속도 분포에 대한 평균 규약을 밝혀야 한다. $C/v_{\mathrm{th}}$를 단순히 단면적으로 부르는 경우에는 어떤 열속도 정의를 썼는지에 따라 값이 달라진다.

### (2) Capture와 Emission

같은 두 전하 상태 사이의 thermal emission rate는 평형 detailed balance로 capture coefficient와 연결할 수 있다. 그러나 이를 사용하려면 band-edge density of states, defect degeneracy, thermodynamic transition energy와 동일한 energy reference를 사용해야 한다.[1,3] Capture에서 계산한 activation energy를 emission barrier로 그대로 사용하면 안 된다.

## 5. First-principles 계산 절차

1. 관련 두 전하 상태의 결함 구조를 충분히 큰 supercell에서 각각 완화한다.
2. [Charged Defect Formation Energy](charged-defect-formation-energy.md)의 정전기 정정과 에너지 기준으로 두 상태의 열역학적 에너지 차이를 정한다.
3. 두 평형 구조 사이의 $\Delta Q$를 계산하고 여러 $\lambda$에서 두 전하 상태의 총에너지를 구한다.
4. 각 energy surface의 곡률과 비조화성을 확인해 $\Omega_i$, $\Omega_f$ 또는 수치 potential을 정한다.
5. 기준 구조 부근의 유한 차분이나 wavefunction overlap으로 $W_{if}$를 계산한다.
6. Vibrational state, thermal occupation과 energy-conserving 합을 수렴시켜 $\widetilde r(T)$를 얻는다.
7. 계산 부피와 Coulomb factor를 적용해 $C(T)$로 바꾸고 supercell, 보간점, broadening과 전자구조 설정에 대한 수렴을 검사한다.[1,2]

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
2. 여러 전하·준안정·여기 상태가 관여하면 단일 결함 점유율을 제거한 SRH 식 대신 상태별 master equation이 필요하다.
3. 전체 golden-rule 식은 vibronic 행렬원소로 시작하며, static-coupling·선형 결합·1차원 근사를 적용한 뒤 $|W_{if}|^2X_{if}(T)$로 분해된다.
4. Mass-weighted $\Delta Q$와 두 energy surface는 lattice relaxation을 정량화하며, Huang–Rhys factor는 displaced harmonic oscillator의 결합 척도이다.
5. 주기 supercell transition rate는 계산 부피와 Coulomb factor를 적용해 capture coefficient로 변환해야 한다.
6. 1차원, 조화, 선형 결합과 비아디아바틱 근사의 유효성을 수렴 검사와 다차원 비교로 평가해야 한다.

## 8. 참고문헌

1. A. Alkauskas, Q. Yan, and C. G. Van de Walle, "First-principles theory of nonradiative carrier capture via multiphonon emission," *Physical Review B* **90**, 075202 (2014). [DOI](https://doi.org/10.1103/PhysRevB.90.075202).
2. M. E. Turiansky, A. Alkauskas, C. G. Van de Walle, and J. L. Lyons, "Nonrad: Computing nonradiative capture coefficients from first principles," *Computer Physics Communications* **267**, 108056 (2021). [DOI](https://doi.org/10.1016/j.cpc.2021.108056).
3. K. Huang and A. Rhys, "Theory of light absorption and non-radiative transitions in F-centres," *Proceedings of the Royal Society of London. Series A* **204**, 406–423 (1950). [DOI](https://doi.org/10.1098/rspa.1950.0184).
4. X. Zhang, M. E. Turiansky, L. Razinkovas, M. Maciaszek, P. Broqvist, Q. Yan, J. L. Lyons, C. E. Dreyer, D. Wickramaratne, Á. Gali, A. Pasquarello, and C. G. Van de Walle, "First-principles calculations of defects and electron–phonon interactions: Seminal contributions of Audrius Alkauskas to the understanding of recombination processes," *Journal of Applied Physics* **135**, 150901 (2024). [DOI](https://doi.org/10.1063/5.0205525).
5. G. D. Barmparis, Y. S. Puzyrev, X.-G. Zhang, and S. T. Pantelides, "Theory of inelastic multiphonon scattering and carrier capture by defects in semiconductors," *Physical Review B* **92**, 214111 (2015). [DOI](https://doi.org/10.1103/PhysRevB.92.214111).
6. W. Shockley and W. T. Read, Jr., "Statistics of the Recombinations of Holes and Electrons," *Physical Review* **87**, 835–842 (1952). [DOI](https://doi.org/10.1103/PhysRev.87.835).
7. R. N. Hall, "Electron-Hole Recombination in Germanium," *Physical Review* **87**, 387 (1952). [DOI](https://doi.org/10.1103/PhysRev.87.387).
8. N. Pant and E. Kioupakis, "Increased light-emission efficiency in disordered InGaN through the correlated reduction of recombination rates," *Physical Review Applied* **20**, 064049 (2023). [DOI](https://doi.org/10.1103/PhysRevApplied.20.064049).
