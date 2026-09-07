---
description: 전자 Boltzmann transport equation의 이동·충돌항과 선형 응답을 정식화하고 전자구조·포논·산란 파라미터의 수집 및 검증 방법을 설명
---

# BTE: Formulation and parameters

Boltzmann transport equation (BTE)은 전자의 상태별 점유가 공간 이동, 외부 힘과 산란에 의해 어떻게 변하는지 기술하는 반고전적 운동 방정식이다. Band energy만으로 전류를 정할 수 없으며, 충돌 연산자와 구동 조건을 함께 주어 비평형 분포를 풀어야 한다. 이 글은 결정의 전자 수송을 대상으로 하며, 격자 열전도를 계산하는 phonon BTE와는 구별한다.[1,2]

[Electronic transport regimes](transport-regimes.md)를 배경으로 정식화와 입력 자료의 확보 방법을 설명한다. 이를 저전계 물질 계수로 계산하는 응용은 [BTE: Carrier mobility from first principles](carrier-mobility.md), 열린 양자계의 정식화는 [NEGF: Formulation](negf-formalism.md)으로 이어진다.

## 1. 분포 함수와 수송 방정식

### (1) 이동항과 외부 힘

Band 지표 $n$, 결정 파수 $\mathbf k$, 위치 $\mathbf r$, 시간 $t$에서 전자 상태의 점유 확률을 $f_{n\mathbf k}(\mathbf r,t)$라 한다. 스핀을 포함한 개별 상태에서 $0\le f\le1$이다. 자기장과 Berry curvature 보정을 제외하고 전기장 $\mathbf E$만 가하면 BTE는

$$
\frac{\partial f_{n\mathbf k}}{\partial t}
+\mathbf v_{n\mathbf k}\cdot\nabla_{\mathbf r}f_{n\mathbf k}
+\frac{q\mathbf E}{\hbar}\cdot\nabla_{\mathbf k}f_{n\mathbf k}
=C_{n\mathbf k}[f]
$$

이다. $q=-e$는 전자의 부호 있는 전하이고 $e>0$이다. $\hbar$는 reduced Planck constant, $\mathbf v$는 group velocity, $C[f]$는 단위 시간당 점유를 변화시키는 충돌항이다. 각 항의 단위는 $\mathrm{s^{-1}}$이다. 왼쪽은 상태가 실공간과 파수 공간을 이동하면서 생기는 분포 변화이고 오른쪽은 서로 다른 상태 사이의 점유 재분배이다.[1,2]

전자 에너지 $\varepsilon_{n\mathbf k}$에 대해 반고전적 운동은

$$
\dot{\mathbf r}=\mathbf v_{n\mathbf k}
=\frac{1}{\hbar}\nabla_{\mathbf k}\varepsilon_{n\mathbf k},
\qquad \hbar\dot{\mathbf k}=q\mathbf E
$$

로 주어진다. 여기서 $\mathbf k$는 $\mathrm{m^{-1}}$의 Cartesian 파수이다. Reciprocal-lattice 좌표로 저장한 band 자료는 격자 벡터와 $2\pi$ 규약을 반영하여 미분해야 한다. 위 식은 상태별 band energy가 정의되는 quasiparticle 그림을 사용하며, 상태 사이의 위상 간섭을 직접 전파하는 식은 아니다.[1–3]

### (2) 평형 분포와 문제의 조건

온도 $T$, chemical potential $\zeta$, Boltzmann constant $k_B$에 대해 평형 전자 분포는

$$
f^0_{n\mathbf k}
=\frac{1}{\exp[(\varepsilon_{n\mathbf k}-\zeta)/(k_BT)]+1}
$$

이다. BTE라는 이름이 Maxwell–Boltzmann 통계를 강제하는 것은 아니다. 전자에는 Fermi–Dirac 점유와 Pauli blocking을 사용한다. 균일한 정상 상태에서는 시간·공간 미분이 사라져

$$
\frac{q\mathbf E}{\hbar}\cdot\nabla_{\mathbf k}f_{n\mathbf k}
=C_{n\mathbf k}[f]
$$

만 남는다. 이 단순화가 뒤의 bulk mobility 문제를 정한다. 시간 의존 계산에는 초기 분포가 필요하며, 공간 이동항을 남기는 유한 영역 문제에는 경계에서 들어오는 분포를 별도로 지정해야 한다. 균일한 해에 길이 하나를 곱하는 것만으로 경계 문제를 정의할 수는 없다.[1,2]

## 2. 미시적 충돌 연산자

### (1) 상태 전이와 상세 균형

상태 $i=(n,\mathbf k)$와 $j=(m,\mathbf k')$ 사이의 전이율을 $W_{i\to j}$라 하자. 이 절의 $W$에는 최종 전자 상태의 Pauli 인자를 포함하지 않는다. 동일한 상태 계수 규약 아래 충돌항은

$$
C_i[f]=\sum_j\left[
W_{j\to i}f_j(1-f_i)-W_{i\to j}f_i(1-f_j)
\right]
$$

이다. 첫 항은 scattering-in, 둘째 항은 scattering-out이다. 상태 합에는 사용한 Brillouin zone 격자의 적분 가중치를 포함한다. 전자–포논 산란은 전자를 생성·소멸시키지 않으므로 모든 전자 상태를 같은 규약으로 합하면 $\sum_i C_i=0$이다. 이는 위 식에서 $i,j$를 교환하면 두 항이 상쇄되는 것으로 직접 확인할 수 있다.[1,2]

전자와 포논의 온도가 같고 외부 구동이 없는 평형에서는 detailed balance가

$$
W_{i\to j}f_i^0(1-f_j^0)
=W_{j\to i}f_j^0(1-f_i^0)
$$

를 만족하여 $C[f^0]=0$이 된다. 비탄성 산란에서 두 방향의 $W$ 자체가 같아야 하는 것은 아니다. 에너지 차이에 따른 전자·포논 점유까지 결합한 두 흐름이 같아야 한다.[2,3]

### (2) 포논 흡수와 방출

Phonon 파수 $\mathbf q$, branch $\nu$, 각진동수 $\omega_{\mathbf q\nu}$와 electron–phonon coupling (EPC) 행렬 원소 $g_{mn\nu}(\mathbf k,\mathbf q)$를 정의한다. 열평형 phonon 점유는

$$
N_{\mathbf q\nu}
=\frac{1}{\exp[\hbar\omega_{\mathbf q\nu}/(k_BT)]-1}
$$

이다. 최종 전자 상태를 $j=(m,\mathbf k+\mathbf q)$로 통일하면 Fermi's golden rule의 전이율은

$$
W^{\nu,\mathrm{abs}}_{i\to j}
=\frac{2\pi}{\hbar}|g_{mn\nu}|^2N_{\mathbf q\nu}
\delta(\varepsilon_i-\varepsilon_j+\hbar\omega_{\mathbf q\nu}),
$$

$$
W^{\nu,\mathrm{em}}_{i\to j}
=\frac{2\pi}{\hbar}|g_{mn\nu}|^2(N_{\mathbf q\nu}+1)
\delta(\varepsilon_i-\varepsilon_j-\hbar\omega_{\mathbf q\nu})
$$

이다. 방출항에서는 원래 방출되는 포논의 파수를 $-\mathbf q$로 바꾸어 썼으며, $\omega_{-\mathbf q\nu}=\omega_{\mathbf q\nu}$와 대응하는 결합의 Hermitian 관계를 사용한다. 흡수는 전자의 에너지를 $\hbar\omega$만큼 올리고 방출은 내린다. $N+1$의 1은 spontaneous emission이다. $g$는 에너지 단위이고 Dirac delta는 에너지 역수 단위이므로 전이율은 $\mathrm{s^{-1}}$가 된다.[1–3]

이 식은 harmonic phonon, 변위에 대한 1차 EPC와 약한 산란의 Golden-rule 근사이다. 주어진 상태에서 허용되는 모든 $m,\mathbf q,\nu$를 적분해야 총 산란율을 얻는다. Optical mode 하나의 진동수나 band-edge effective mass만으로 이 상태 합을 대신할 수 없다.[1,2,4]

## 3. 선형 응답과 완화시간 근사

### (1) 분포 보정과 전류

충분히 약한 전기장에서 $f=f^0+\delta f$로 놓고 전기장의 1차 항만 유지한다. 길이 단위의 mean free displacement $\mathbf F_i$를

$$
\delta f_i=q\sum_\beta E_\beta F_{i\beta}D_i,
\qquad
D_i=-\frac{\partial f_i^0}{\partial\varepsilon_i}
=\frac{f_i^0(1-f_i^0)}{k_BT}
$$

로 정의한다. $\beta$는 Cartesian 방향이다. 전자에는 $q=-e$이므로 $\mathbf E\cdot\mathbf F_i>0$인 상태의 점유 보정은 음수이다. 이 부호와 전류의 전하 부호를 함께 적용해야 양의 종방향 conductivity를 얻는다.[1–3]

Relaxation time approximation (RTA)은 충돌항을

$$
C_i[f]\approx-\frac{\delta f_i}{\tau_i}
$$

로 근사한다. 정상 상태 BTE의 왼쪽에 $f^0$를 대입하면

$$
-q\mathbf E\cdot\mathbf v_iD_i
=-\frac{\delta f_i}{\tau_i},
\qquad \mathbf F_i^{\mathrm{RTA}}=\tau_i\mathbf v_i
$$

를 얻는다. 이는 정의한 부호를 확인하는 직접적인 유도이다. $\tau_i$는 초 단위이며 어떤 충돌 연산자를 축약했는지에 따라 의미가 달라진다.[1,2]

단위 셀 부피 $V_{\mathrm{cell}}$, 정규화된 전자 격자 가중치 $w_{\mathbf k}$를 사용하면 전류는

$$
J_\alpha=\frac{q}{V_{\mathrm{cell}}}
\sum_{n\mathbf k}w_{\mathbf k}v_{n\mathbf k,\alpha}\delta f_{n\mathbf k},
\qquad \sum_{\mathbf k}w_{\mathbf k}=1
$$

이고 선형 conductivity는

$$
\sigma_{\alpha\beta}
=\frac{q^2}{V_{\mathrm{cell}}}
\sum_{n\mathbf k}w_{\mathbf k}v_{n\mathbf k,\alpha}F_{n\mathbf k,\beta}D_{n\mathbf k}
$$

이다. 여기서는 $n$에 스핀 상태를 포함한다. 한 스핀의 축퇴 band만 저장했다면 해당 축퇴를 정확히 한 번 적용한다. 3차원 $\sigma$의 단위는 $\mathrm{S\,m^{-1}}$이다. 전도대 전자 농도 $n_c$와 drift mobility는

$$
n_c=\frac{1}{V_{\mathrm{cell}}}\sum_{n\mathbf k\in\mathrm{CB}}
w_{\mathbf k}f^0_{n\mathbf k},
\qquad \mu_{\alpha\beta}=\frac{\sigma_{\alpha\beta}}{en_c}
$$

로 구한다. $\mathrm{CB}$는 conduction band 집합이다. 정공 농도에는 valence band의 $1-f^0$를 사용한다. 2차원 결정에서는 셀 면적과 sheet density로 바꾸어 sheet conductivity를 얻는다. 이때도 mobility의 단위는 $\mathrm{m^2\,V^{-1}\,s^{-1}}$이며, 진공 두께로 정한 3차원 conductivity와 혼합하지 않는다.[1–3,5]

### (2) SERTA와 결합된 상태 응답

Self-energy relaxation time approximation (SERTA)은 선형화한 충돌 연산자의 대각 이완율을 사용하고 다른 상태의 비평형 보정을 생략한다. 균일한 $N_q$개 포논 격자에서는

$$
\begin{aligned}
\tau_i^{-1}
=\frac{2\pi}{\hbar N_q}\sum_{m\mathbf q\nu}|g_{mn\nu}|^2
\big[&(N_{\mathbf q\nu}+1-f_j^0)
\delta(\varepsilon_i-\varepsilon_j-\hbar\omega_{\mathbf q\nu})\\
+&(N_{\mathbf q\nu}+f_j^0)
\delta(\varepsilon_i-\varepsilon_j+\hbar\omega_{\mathbf q\nu})\big]
\end{aligned}
$$

이다. $j=(m,\mathbf k+\mathbf q)$이며 $N_q$는 격자점 수, $N_{\mathbf q\nu}$는 점유이다. 앞 절의 bare $W$와 달리 $f_j^0$를 포함한다. 따라서 $N$과 $N+1$만 있는 전이율을 그대로 합하거나 거기에 $1-f_j^0$만 곱해 SERTA lifetime이라고 부르면 일반적인 축퇴 전자계에서 같은 식이 되지 않는다.[1–3]

반복 BTE는 선형화된 scattering-in kernel $K_{ij}$를 남겨

$$
F_{i\beta}=\tau_i v_{i\beta}+\tau_i\sum_j K_{ij}F_{j\beta}
$$

를 푼다. $K$에는 평형 점유, detailed balance 변환과 격자 가중치가 포함되며 단위는 $\mathrm{s^{-1}}$이다. 다른 상태에서 들어오는 방향성 때문에 $\mathbf F_i$가 항상 $\mathbf v_i$에 평행한 것은 아니다. Forward scattering은 상태 lifetime을 줄여도 전류 방향을 약하게 바꿀 수 있어, lifetime과 transport relaxation을 구분해야 한다.[1–3]

Constant relaxation time approximation (CRTA)은 $\tau_i=\tau_0$까지 가정한다. Band 자료만 확보한 단계에서 얻는 것은 $\sigma/\tau_0$이며, 절대 mobility에는 외부에서 정한 $\tau_0$가 필요하다. 이를 미시적 EPC를 계산한 결과와 같은 의미의 무매개변수 예측으로 해석하지 않는다.[5,6]

## 4. 입력 파라미터의 수집

### (1) 계산 수준별 자료 묶음

BTE의 입력은 몇 개의 보편적인 상수가 아니다. 선택한 충돌 모형에 따라 필요한 배열과 시료 조건이 달라진다. 아래 표는 자료 수집의 범위를 정하는 기준이다.[1,5,6]

| 계산 수준 | 확보할 물질 자료 | 별도로 정할 조건 |
| --- | --- | --- |
| CRTA | 셀, 균일 격자의 $\varepsilon_{n\mathbf k}$와 속도 | $T$, $n_c$ 또는 $\zeta$, 가정한 $\tau_0$ |
| 산란 모형 BTE | 전자구조와 모형별 변형 퍼텐셜·탄성·유전 응답 | 불순물 농도·전하 상태, 포함할 산란원 |
| 미시적 EPC–BTE | 전자 상태, 모든 관련 $\omega_{\mathbf q\nu}$와 고유벡터, $g_{mn\nu}$ | 전자·포논 점유, 수렴된 적분 격자 |

구조 파일과 계산 출력을 함께 보관하고 결정상, 격자, 원자 배치, exchange–correlation functional, pseudopotential, spin–orbit coupling 사용 여부를 기록한다. 서로 다른 구조·전자구조 수준에서 얻은 자료를 결합할 때에는 band ordering과 정규화가 유지되는지 확인한다. 데이터베이스의 유전율 하나를 가져오는 것으로 특정 시료의 산란 문제가 완성되는 것은 아니다.[1,6]

### (2) 전자구조와 점유 조건

Density functional theory (DFT) 계산에서는 수렴된 구조의 균일한 Brillouin zone 격자에서 에너지와 wavefunction을 확보한다. 고대칭 경로의 band plot은 적분 영역 전체를 표본화하지 않으므로 수송 적분의 입력을 대체하지 못한다. 속도는 앞의 band 미분식 또는 보간 Hamiltonian의 미분으로 얻고, 원래 계산점에서 band와 속도를 대조한다.[1,5,7]

예를 들어 고립된 band의 $\alpha$ 방향 수치 미분은

$$
v_{n\mathbf k,\alpha}\approx
\frac{\varepsilon_n(\mathbf k+\Delta k\hat{\mathbf e}_\alpha)
-\varepsilon_n(\mathbf k-\Delta k\hat{\mathbf e}_\alpha)}{2\hbar\Delta k}
$$

이다. $\hat{\mathbf e}_\alpha$는 단위 방향 벡터이다. 이 식은 속도 자료를 독립적으로 점검하기 위한 예시이며, $\Delta k$에 대한 수렴과 동일 band 추적이 필요하다. Band crossing에서 에너지순 번호만 미분하면 다른 상태를 연결할 수 있으므로 보간 Hamiltonian과 상태 정보를 이용한 검증이 필요하다.[1,2]

$T$와 목표 $n_c$는 사용자가 정하거나 비교 실험에서 가져오는 조건이다. 각 온도에서 앞 절의 농도 합이 목표값을 만족하도록 $\zeta$를 구한다. 전자구조를 고정하고 점유만 바꾸면 rigid-band approximation이다. Doping으로 구조나 band가 변하는 문제까지 이 절차가 자동으로 포함하지는 않는다.[3,5]

### (3) 포논과 EPC 행렬

Density-functional perturbation theory (DFPT) 또는 supercell의 finite displacement로 포논 자료를 얻는다. 변위 성분 $u_a,u_b$에 대한 총에너지 $E_{\mathrm{tot}}$의 force constant는

$$
\Phi_{ab}=\frac{\partial^2E_{\mathrm{tot}}}{\partial u_a\partial u_b}
=-\frac{\partial\mathcal F_b}{\partial u_a}
\approx-\frac{\mathcal F_b(+\Delta u_a)-\mathcal F_b(-\Delta u_a)}{2\Delta u_a}
$$

이다. $\mathcal F_b$는 원자에 작용하는 힘으로, mean free displacement $\mathbf F$와 다른 양이다. 원자 질량을 적용하고 Fourier 변환한 dynamical matrix $\mathcal D(\mathbf q)$는

$$
\mathcal D(\mathbf q)\mathbf e_{\mathbf q\nu}
=\omega_{\mathbf q\nu}^{2}\mathbf e_{\mathbf q\nu}
$$

를 만족한다. $\mathbf e_{\mathbf q\nu}$는 질량 가중 좌표의 무차원 정규화 고유벡터이다. Force constant는 에너지/길이 제곱, $\mathcal D$는 $\mathrm{s^{-2}}$ 단위이다. Finite displacement에서는 변위 크기와 supercell 크기, DFPT에서는 응답 계산과 포논 격자를 수렴시킨다.[1,2,4]

포논 에너지만으로 EPC를 알 수는 없다. 원자 $\kappa$의 질량 $M_\kappa$와 Cartesian 성분 $\alpha$에 대해

$$
g_{mn\nu}(\mathbf k,\mathbf q)
=\sum_{\kappa\alpha}\sqrt{\frac{\hbar}{2M_\kappa\omega_{\mathbf q\nu}}}
e_{\kappa\alpha,\nu}(\mathbf q)
\langle\psi_{m,\mathbf k+\mathbf q}|\partial_{\mathbf q\kappa\alpha}V|\psi_{n\mathbf k}\rangle
$$

를 계산해야 한다. $V$는 self-consistent 전자 퍼텐셜, $\partial_{\mathbf q\kappa\alpha}V$는 해당 주기적 원자 변위에 대한 미분이다. 퍼텐셜 미분의 에너지/길이에 영점 진동 진폭의 길이를 곱하여 $g$가 에너지 단위가 된다. 질량이나 진동 진폭을 이미 포함한 출력에 이를 다시 곱하지 않는다.[1,2,4]

실무에서는 coarse 전자·포논 격자의 응답과 Bloch 상태를 확보한 뒤 Wannier 보간 등으로 조밀한 격자의 $g$를 구성한다. 독립적으로 계산한 시험점과 보간 결과를 비교하고, 전자 상태와 EPC의 gauge·band 순서·격자 대응을 함께 확인한다. Polar material의 장거리 전기장 성분은 단거리 성분과 구별하여 처리해야 작은 $\mathbf q$의 결합을 재현할 수 있다.[1,3,4]

### (4) 산란 모형의 물질 상수

변형 퍼텐셜 모형에서는 작은 strain에 대한 band energy 응답을 구한다. 무차원 strain 성분 $s$와 동일한 기준으로 정렬한 에너지 $\widetilde\varepsilon$를 사용하면 한 성분의 추출식은

$$
D_s=\left.\frac{\partial\widetilde\varepsilon}{\partial s}\right|_{s=0}
\approx\frac{\widetilde\varepsilon(+\Delta s)-\widetilde\varepsilon(-\Delta s)}{2\Delta s}
$$

이다. $D_s$는 에너지 단위이다. 압축·인장 구조에서 같은 band 또는 valley를 추적하고, 에너지 기준 정렬과 strain 구간을 보고한다. 여러 작은 strain으로 선형 구간을 확인한다. 이 수집 절차는 장파장 strain 응답을 위한 것이며, 하나의 $D_s$가 전체 mode·intervalley EPC를 대체한다는 뜻은 아니다.[4,6,7]

모형별로 필요한 상수와 확보 경로는 다음과 같다. AMSET 공식 문서는 해당 계산 출력에서 입력 파일을 만드는 구체적인 절차를 제공하며, VASP 공식 문서는 유전·탄성 응답 계산을 설명한다. 명령과 파일 형식은 사용 버전의 문서를 확인한다.[4,6–8]

| 파라미터 | 수집 방법 | 확인할 규약 |
| --- | --- | --- |
| 변형 퍼텐셜 | Strain 전후 band energy 차이 | 에너지 기준, 방향·valley, 에너지 단위 |
| 탄성 tensor | 작은 strain에 대한 응력 또는 총에너지 응답 | 응력 부호, tensor/Voigt 표기, 3차원 압력 단위 |
| 고주파·정적 유전 tensor | 전기장에 대한 전자 및 이온 응답 | 상대 유전율인지, 이온 응답 포함 여부 |
| Piezoelectric tensor | Strain에 대한 분극 응답 | 고정 이온/이완 이온, 축과 tensor 규약 |
| Polar phonon 진동수 | 포논 계산과 극성 mode의 결합 정보 | 각진동수/주파수/에너지, 단일 유효 mode 근사 |

DFPT의 고정 이온 유전 응답은 전자 부분이다. 이를 이온 기여까지 포함한 정적 유전율과 동일시하지 않는다. VASP의 `LEPSILON`이 주는 고정 이온 응답과 Born effective charge를 사용할 때도 이 구분을 확인해야 한다. Polar scattering 모형에서 두 유전 응답이 별도로 등장하기 때문이다.[6–8]

### (5) 시료 의존 입력과 경험적 완화시간

불순물 산란에는 이온화된 산란 중심의 농도 $N_{\mathrm{imp}}$, 전하 상태와 screening 모형이 필요하다. 이 값은 완전 결정의 band 계산으로 정해지지 않는다. 시료의 도핑·보상·이온화 정보를 사용하거나 명시적인 가정 범위를 주어 계산한다. 불순물 하나가 자유 운반자 하나를 공급한다는 조건에서만 $N_{\mathrm{imp}}=n_c$로 둘 수 있다. 보상 도핑과 불완전 이온화에서는 두 농도를 독립적으로 다루어야 한다.[6,9]

!!! info "[Measurement]"
    CRTA를 실험에 맞출 때에는 같은 온도·농도·결정 방향의 conductivity $\sigma_{\alpha\alpha}^{\mathrm{exp}}$와 계산한 $\mathcal B_{\alpha\alpha}=(\sigma/\tau_0)_{\alpha\alpha}$를 사용하여

    $$
    \tau_{\mathrm{fit}}=
    \frac{\sigma_{\alpha\alpha}^{\mathrm{exp}}}{\mathcal B_{\alpha\alpha}}
    $$

    로 초 단위의 유효 완화시간을 추출할 수 있다. 이는 CRTA의 비례 관계에서 유도한 보정값이다. 해당 측정에 포함된 산란을 한 상수로 흡수하므로 phonon lifetime의 직접 측정이나 독립적인 mobility 예측으로 해석하지 않는다. 보정에 사용한 조건과 별도의 검증 조건을 함께 기록한다.[5,6]

## 5. 입력 검증과 적용 한계

물질 파라미터와 수치 설정은 구별해야 한다. 전자·포논 격자, 보간 window와 delta 함수의 폭은 실험에서 수집할 물질 상수가 아니라 적분을 수렴시키는 설정이다. 특히 수치 broadening을 물리적인 $\hbar/\tau$로 간주하여 lifetime을 다시 정하면 계산 목적이 달라진다.[1,2,9]

아래 검증 순서는 앞의 방정식에서 요구하는 일관성을 확인하기 위한 실무 절차이다. 정해진 격자 수 하나를 모든 물질에 공통으로 적용하기보다, 목표 온도·농도의 결과를 기준으로 판단한다.[1,2,9]

| 검사 대상 | 확인 방법 | 실패 시 재검토할 입력 |
| --- | --- | --- |
| 평형 충돌항 | $C[f^0]$가 수치 오차 내에서 소멸하는지 확인 | 흡수·방출 부호, Pauli 인자, 적분 가중치 |
| 전하 보존 | 상태 전체의 충돌항 합 확인 | 상태 window, 역방향 전이, 상태 중복 |
| 전자·포논 보간 | 직접 계산점의 band·mode·결합과 비교 | Gauge, 질량 정규화, 장거리 보정 |
| 적분 수렴 | $k/q$ 격자와 delta 처리법을 바꾸어 tensor 비교 | 최종 상태 표본화와 에너지 window |
| 모형 의존성 | 같은 입력에서 SERTA와 반복 BTE 비교 | 방향 재분배를 생략한 오차 |

예를 들어 연속된 두 설정에서 얻은 양의 종방향 conductivity를 $\sigma^{(a)}$, $\sigma^{(b)}$라 하면

$$
\eta_\sigma=
\frac{|\sigma^{(b)}-\sigma^{(a)}|}{|\sigma^{(b)}|}
$$

를 수렴 지표로 사용할 수 있다. 이는 이 글에서 정의한 무차원 비교 지표이며, 허용 오차는 사용 목적에 맞춰 미리 정한다. 거의 0인 성분에는 상대 오차 대신 절대 오차도 기록한다. 격자 수렴은 선택한 산란 모형의 완전성이나 전자구조 정확도를 보증하지 않는다.[1,2,9]

여기서 유도한 선형 응답은 약한 전기장과 열평형 phonon bath를 전제한다. 높은 전기장에 의한 큰 분포 변화, 비평형 phonon 점유 또는 강한 localization에는 그대로 적용할 수 없다. 또한 semiclassical BTE의 점유와 nonequilibrium Green's function (NEGF)의 양자 상관함수는 같은 입력 배열이 아니다. 두 접근 모두 EPC를 사용할 수 있지만 위상 간섭과 열린 경계를 다루는 방식이 다르므로 $g$와 $\tau$를 전극 self-energy로 단순 치환하지 않는다.[1,3,4]

## 6. 요약

- BTE는 이동·구동과 충돌에 의한 점유 재분배를 함께 풀어 비평형 전자 분포를 정한다.
- Bare 전이율, Pauli blocking을 포함한 충돌항, 선형화된 SERTA lifetime은 서로 구분한다.
- 전자구조와 포논 외에 EPC 또는 명시적인 산란 모형이 있어야 절대 mobility를 계산할 수 있다.
- 물질 응답은 DFT·DFPT·finite displacement로, 온도·농도·불순물 조건은 대상 시료와 계산 목적에 맞춰 확보한다.
- 단위·정규화·상세 균형과 수렴을 확인하고 경험적 보정과 미시적 예측의 범위를 구분한다.

## 7. 참고문헌

1. J.-J. Zhou, J. Park, I.-T. Lu, I. Maliyov, X. Tong, and M. Bernardi, "Perturbo: A software package for ab initio electron–phonon interactions, charge transport and ultrafast dynamics," *Computer Physics Communications* **264**, 107970 (2021). [DOI](https://doi.org/10.1016/j.cpc.2021.107970), [본문](https://arxiv.org/pdf/2002.02045), §2.1–2.2.
2. T. Gunst, T. Markussen, K. Stokbro, and M. Brandbyge, "First-principles method for electron-phonon coupling and electron mobility: Applications to two-dimensional materials," *Physical Review B* **93**, 035414 (2016). [DOI](https://doi.org/10.1103/PhysRevB.93.035414), [본문](https://arxiv.org/pdf/1511.02045), §II.
3. S. Poncé, W. Li, S. Reichardt, and F. Giustino, "First-principles calculations of charge carrier mobility and conductivity in bulk semiconductors and two-dimensional materials," *Reports on Progress in Physics* **83**, 036501 (2020). [DOI](https://doi.org/10.1088/1361-6633/ab6a43), [본문](https://arxiv.org/pdf/1908.01733), §2–3.
4. F. Giustino, "Electron-phonon interactions from first principles," *Reviews of Modern Physics* **89**, 015003 (2017). [DOI](https://doi.org/10.1103/RevModPhys.89.015003), [본문](https://arxiv.org/pdf/1603.06965), §II–III, VI, X.
5. G. K. H. Madsen, J. Carrete, and M. J. Verstraete, "BoltzTraP2, a program for interpolating band structures and calculating semi-classical transport coefficients," *Computer Physics Communications* **231**, 140–145 (2018). [DOI](https://doi.org/10.1016/j.cpc.2018.05.010), [본문](https://arxiv.org/pdf/1712.07946), §2.
6. A. M. Ganose, J. Park, A. Faghaninia, R. Woods-Robinson, K. A. Persson, and A. Jain, "Efficient calculation of carrier scattering rates from first principles," *Nature Communications* **12**, 2222 (2021). [본문](https://www.nature.com/articles/s41467-021-22440-5), Results 및 Discussion.
7. AMSET developers, "Calculation Inputs," *AMSET Documentation*. [공식 문서](https://hackingmaterials.lbl.gov/amset/inputs/), 전자구조·변형 퍼텐셜·탄성·유전 응답 입력 절차.
8. VASP developers, "LEPSILON" and "IBRION," *VASP Wiki*. [LEPSILON](https://vasp.at/wiki/LEPSILON), [IBRION](https://vasp.at/wiki/IBRION), 고정 이온·이온 유전 응답, Born effective charge와 탄성 tensor 계산.
9. J. Leveillee, X. Zhang, E. Kioupakis, and F. Giustino, "Ab initio calculation of carrier mobility in semiconductors including ionized-impurity scattering," *arXiv:2301.02323* (2023). [본문](https://arxiv.org/pdf/2301.02323), §II–III.
