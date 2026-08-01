---
title: "(3) Point Defects: Nonradiative Multiphonon Emission"
description: 심층 결함의 비방사 운반자 포획을 진동 결합, Fermi golden rule과 first-principles 계산 절차로 설명
status: verified
last_verified: 2026-08-01
---

# (3) Point Defects: Nonradiative Multiphonon Emission

Nonradiative multiphonon emission (NMP)은 전자나 정공이 심층 결함에 포획되거나 결함에서 방출될 때, 전이 에너지를 광자 대신 여러 격자 진동에 전달하는 과정이다. 반도체의 Shockley–Read–Hall 재결합에서 포획 계수를 미시적으로 계산하려면 전자 상태 변화와 그에 따른 원자 재배열을 함께 다뤄야 한다.[1,2]

이 글은 희석된 국소 결함, Born–Oppenheimer potential-energy surface, 조화 진동자와 static-coupling 근사를 사용하는 first-principles NMP 정식화를 다룬다. 산화막 신뢰성의 다중 상태 phenomenological model이나 특정 시뮬레이터 사용법은 별개의 모형 계층이므로 중심 범위에서 제외한다.

## 1. 포획률과 진동 결합

### (1) 거시적 포획 계수

전자 포획을 예로 들면 단위 부피당 포획률은

$$
R_n=C_n\,N_D^+\,n
$$

으로 정의한다.[1,2] $n$은 자유전자 농도, $N_D^+$는 전자를 포획할 수 있는 결함 농도, $C_n$은 전자 포획 계수이며 3차원에서 단위는 부피/시간이다. 한 결함의 포획률은 $r_n=C_n n$이다. 정공 포획은 $R_p=C_pN_A^-p$로 같은 방식으로 정의한다.

포획 계수는 단순한 결함의 기하학적 면적이 아니다. 전자–포논 결합, 초기·최종 진동 상태의 중첩, 전하 상태의 장거리 Coulomb 상호작용과 온도를 모두 포함한다.[1,2]

### (2) Born–Oppenheimer 상태

전자 좌표를 $\mathbf r$, 모든 핵 좌표를 $\mathbf R$이라 하면 초기와 최종 vibronic 상태를

$$
\Psi_{im}(\mathbf r,\mathbf R)
=\psi_i(\mathbf r;\mathbf R)\chi_{im}(\mathbf R),
$$

$$
\Psi_{fn}(\mathbf r,\mathbf R)
=\psi_f(\mathbf r;\mathbf R)\chi_{fn}(\mathbf R)
$$

로 분리한다. $\psi_i$와 $\psi_f$는 각각 band 상태와 결함 상태에 해당하는 전자 파동함수이고, $\chi_{im}$과 $\chi_{fn}$은 두 전하 상태의 potential-energy surface 위 핵 진동 상태이다.[1,3]

전자 전이가 일어나면 결함의 전하와 결합 길이가 바뀌므로 두 surface의 평형 구조도 달라진다. 전자 에너지 차이가 한 개의 포논 에너지보다 훨씬 커도 여러 진동 양자의 동시 교환으로 에너지를 보존할 수 있다는 것이 NMP의 핵심이다.[1,3]

## 2. 1차원 configuration coordinate

### (1) 질량 가중 좌표

완전한 문제는 $3N$차원 핵 좌표에 놓이지만, 널리 쓰이는 1차원 근사는 두 완화 구조를 잇는 질량 가중 변위를 accepting coordinate로 선택한다. 초기와 최종 구조를 $\mathbf R_i$, $\mathbf R_f$라 하면

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

로 쓴다.[1,2] $Q$가 질량 가중 좌표이므로 식에 별도의 유효 질량을 다시 곱하지 않는다. $\Omega_i$와 $\Omega_f$는 각 곡선의 곡률로 정한 유효 각진동수이다.

### (2) 이완 에너지와 Huang–Rhys 인자

두 곡선의 유효 진동수가 같아 $\Omega_i=\Omega_f=\Omega$라고 근사하면 Huang–Rhys factor는

$$
S=\frac{\Omega(\Delta Q)^2}{2\hbar}
$$

이고, 한 surface에서 다른 구조까지 수직으로 이동할 때의 이완 에너지는

$$
\lambda_{\mathrm{rel}}
=S\hbar\Omega
=\frac{1}{2}\Omega^2(\Delta Q)^2
$$

이다.[1,3] $S$는 두 변위된 조화 진동자 상태 사이의 Franck–Condon 분포를 정하는 무차원 결합 척도이다. 일반적으로 “실제로 방출되는 평균 포논 수”와 언제나 동일하다고 해석해서는 안 된다. 전이 에너지, 초기 열점유와 서로 다른 두 곡률도 최종 phonon 분포에 영향을 준다.[1,3]

곡선의 교차점은 고전적인 활성화 그림을 제공하지만, 양자 포획률은 교차 장벽만으로 정해지지 않는다. 저온에서는 진동 파동함수의 터널링 꼬리와 영점 운동도 기여한다.[1,3]

## 3. Fermi golden rule 포획률

### (1) Static-coupling 근사

Static-coupling 접근은 기준 구조 $Q_0$에서 전자 Hamiltonian $\hat h$를 1차로 전개하여 전자–포논 섭동을

$$
\Delta\hat H
\simeq
\left.
\frac{\partial \hat h}{\partial Q}
\right|_{Q_0}
(Q-Q_0)
$$

로 둔다. 이때 전자 결합 행렬 원소는

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

이다.[1,2] $W_{if}$는 전자 상태의 에너지 차이만으로 정해지지 않으며, 파동함수의 공간 중첩과 구조 변화 방향에 대한 Hamiltonian의 민감도를 담는다.

초기 진동 상태 $m$의 열점유를 $w_m(T)$라 하면 한 결함에 대한 전이율은

$$
r_{i\rightarrow f}
=\frac{2\pi}{\hbar}\,g
\sum_m w_m(T)
\sum_n
\left|
W_{if}
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

로 쓸 수 있다.[1,2,5] $g$는 동등한 최종 상태의 축퇴도이다. Dirac delta는 전체 전자–진동 에너지 보존을 나타내며, 진동 중첩과 좌표 행렬 원소가 여러 phonon이 관여하는 세기를 정한다.

### (2) 1차원 환원과 수치 합

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

실제 계산에서 delta 함수를 유한 폭의 Gaussian 등으로 바꾸면 에너지 보존 오차와 포획 계수의 폭 의존성이 생긴다. 진동 준위의 이산 합을 충분히 수렴시키고, broadening을 바꿨을 때 결과가 안정한지 확인해야 한다.[2,4]

## 4. Supercell rate에서 포획 계수로

### (1) 체적 정규화

주기 supercell의 띠 상태는 계산 부피 $\widetilde V$에 정규화되므로 계산된 한 결함 전이율 $\widetilde r$은 $\widetilde V$에 의존한다. 3차원 벌크 포획 계수는

$$
C=\widetilde V\,f\,\widetilde r
$$

로 변환한다.[1,2,4] $f$는 결함과 자유 운반자 사이의 장거리 Coulomb 상호작용을 반영하는 Sommerfeld factor이다. 중성 결함이면 보통 $f=1$로 두지만, 서로 끌어당기는 전하에서는 포획이 강화되고 밀어내는 전하에서는 억제된다.

이 관계는 결함 농도가 낮고, 한 결함의 파동함수가 주기 복제본과 겹치지 않으며, 초기 band 상태가 bulk-like라는 조건을 요구한다. $\widetilde V\,\widetilde r$가 cell 크기에 대해 수렴하는지 확인하지 않으면 포획 계수를 물질 고유량처럼 보고할 수 없다.[1,2]

포획 단면적 $\sigma$를 사용하려면

$$
C(T)=\left\langle \sigma(E,T)v(E)\right\rangle
$$

처럼 운반자 속도 분포에 대한 평균 규약을 밝혀야 한다. $C/v_{\mathrm{th}}$를 단순히 단면적으로 부르는 경우에는 어떤 열속도 정의를 썼는지에 따라 값이 달라진다.

### (2) 포획과 방출

같은 두 전하 상태 사이의 thermal emission rate는 평형 detailed balance로 포획 계수와 연결할 수 있다. 그러나 이를 사용하려면 band-edge 상태 밀도, 결함 축퇴도, 열역학적 전이 에너지와 동일한 에너지 기준을 사용해야 한다.[1,3] 포획에서 계산한 activation energy를 방출 장벽으로 그대로 복사하면 안 된다.

## 5. First-principles 계산 절차

1. 관련 두 전하 상태의 결함 구조를 충분히 큰 supercell에서 각각 완화한다.
2. [Charged Defect Formation Energy](charged-defect-formation-energy.md)의 정전기 정정과 에너지 기준으로 두 상태의 열역학적 에너지 차이를 정한다.
3. 두 평형 구조 사이의 $\Delta Q$를 계산하고 여러 $\lambda$에서 두 전하 상태의 총에너지를 구한다.
4. 각 energy surface의 곡률과 비조화성을 확인해 $\Omega_i$, $\Omega_f$ 또는 수치 potential을 정한다.
5. 기준 구조 부근의 유한 차분이나 wavefunction overlap으로 $W_{if}$를 계산한다.
6. 진동 상태, 열점유와 energy-conserving 합을 수렴시켜 $\widetilde r(T)$를 얻는다.
7. 계산 부피와 Coulomb factor를 적용해 $C(T)$로 바꾸고 supercell, 보간점, broadening과 전자구조 설정에 대한 수렴을 검사한다.[1,2]

!!! info "[Measurement]"
    계산 결과에는 $C_n$ 또는 $C_p$의 구분과 단위, 온도 범위, $\Delta Q$, $\Omega_i$, $\Omega_f$, 에너지 차이, $W_{if}$, 축퇴도 $g$, Coulomb factor $f$, supercell 부피와 delta 함수 처리법을 함께 보고한다. 가장 직접적인 수치 검사는

    $$
    C(T;\widetilde V)
    =\widetilde V f\widetilde r(T;\widetilde V)
    $$

    가 supercell 크기와 진동 상태 절단에 대해 수렴하는지 확인하는 것이다.[1,2]

## 6. 근사와 해석상의 주의점

!!! warning "[Interpretation Caveat]"
    - **1차원 accepting mode:** 두 최소점을 잇는 직선 좌표가 모든 phonon mode의 Duschinsky 회전과 promoting mode를 담지는 못한다. 여러 mode가 비슷하게 결합하거나 경로가 휘면 다차원 처리가 필요할 수 있다.[2,4]
    - **조화·선형 결합:** 큰 구조 재배열, 결합 파괴와 강한 비조화성에서는 포물선과 $\partial\hat h/\partial Q$의 1차 전개가 약해진다.[1,4]
    - **전자구조 오차:** 포획 계수는 전이 에너지와 wavefunction localization에 매우 민감하다. 띠간격이나 결함 준위를 사후 이동하는 것만으로 $W_{if}$와 구조 이완 오차가 고쳐지지는 않는다.[1,2]
    - **비아디아바틱 근사:** static-coupling Fermi golden rule은 약한 결합의 비아디아바틱 전이에 적합하다. 강한 결합과 surface 교차 부근에서는 adiabaticity를 별도로 평가해야 한다.[3,4]

NMP 계수 하나가 특정 소자의 bias-temperature instability, random telegraph noise 또는 장기 열화를 곧바로 결정하지는 않는다. 소자 수준 예측에는 결함 분포, 전계에 따른 carrier 공급, 여러 구조 상태와 시간 의존 kinetics가 추가로 필요하다.

## 7. 요약

1. NMP 포획은 전자 상태 변화와 서로 다른 전하 상태의 핵 진동 상태 중첩이 결합된 과정이다.
2. 질량 가중 $\Delta Q$와 두 energy surface는 격자 이완을 정량화하며, Huang–Rhys factor는 변위된 조화 진동자의 결합 척도이다.
3. Static-coupling Fermi golden rule에서 $W_{if}$와 진동 행렬 원소가 미시적 전이율을 정한다.
4. 주기 supercell 전이율은 계산 부피와 Coulomb factor를 적용해 포획 계수로 변환해야 한다.
5. 1차원, 조화, 선형 결합과 비아디아바틱 근사의 유효성을 수렴 검사와 다차원 비교로 평가해야 한다.

## 8. 참고문헌

1. A. Alkauskas, Q. Yan, and C. G. Van de Walle, "First-principles theory of nonradiative carrier capture via multiphonon emission," *Physical Review B* **90**, 075202 (2014). [DOI](https://doi.org/10.1103/PhysRevB.90.075202).
2. M. E. Turiansky, A. Alkauskas, C. G. Van de Walle, and J. L. Lyons, "Nonrad: Computing nonradiative capture coefficients from first principles," *Computer Physics Communications* **267**, 108056 (2021). [DOI](https://doi.org/10.1016/j.cpc.2021.108056).
3. K. Huang and A. Rhys, "Theory of light absorption and non-radiative transitions in F-centres," *Proceedings of the Royal Society of London. Series A* **204**, 406–423 (1950). [DOI](https://doi.org/10.1098/rspa.1950.0184).
4. X. Zhang, M. E. Turiansky, L. Razinkovas, M. Maciaszek, P. Broqvist, Q. Yan, J. L. Lyons, C. E. Dreyer, D. Wickramaratne, Á. Gali, A. Pasquarello, and C. G. Van de Walle, "First-principles calculations of defects and electron–phonon interactions: Seminal contributions of Audrius Alkauskas to the understanding of recombination processes," *Journal of Applied Physics* **135**, 150901 (2024). [DOI](https://doi.org/10.1063/5.0205525).
5. G. D. Barmparis, Y. S. Puzyrev, X.-G. Zhang, and S. T. Pantelides, "Theory of inelastic multiphonon scattering and carrier capture by defects in semiconductors," *Physical Review B* **92**, 214111 (2015). [DOI](https://doi.org/10.1103/PhysRevB.92.214111).
