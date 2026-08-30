---
description: 전자–포논 결합의 수송 Hamiltonian과 SCBA, LOE, Büttiker probe, MD–Landauer의 물리적 의미·근사·검증 기준을 비교
---

# Quantum transport: Electron–phonon coupling

**Electron–phonon coupling (EPC)**은 원자 변위가 전자 Hamiltonian을 바꾸는 상호작용이다. 열린 소자에서는 이 상호작용이 phonon emission·absorption, 전자 위상 완화, 비탄성 전류, 국소 발열과 phonon-limited resistance를 만든다. 그러나 이를 다루는 방법들은 같은 이론의 정확도 순서가 아니다. Self-consistent Born approximation (SCBA)과 lowest order expansion (LOE)은 mode-resolved EPC 행렬을 쓰는 미시적 nonequilibrium Green's function (NEGF) 근사이고, Büttiker probe는 가상 reservoir를 이용한 현상론적 모형이며, molecular dynamics–Landauer (MD–Landauer)는 열적으로 변위된 원자 구조에서 탄성 transmission을 표본 평균하는 adiabatic 접근이다.[1–9]

이 글은 전자 수송에 미치는 phonon의 효과를 다룬다. 격자 자체의 열전도인 **phonon transport**와는 대상 전류가 다르다. 전극 self-energy, Green's function과 탄도 전류의 규약은 [NEGF formalism](negf-formalism.md)을 따른다.

## 1. 수송 Hamiltonian과 관측량

### (1) 선형 Electron–phonon coupling

평형 원자 위치 주변의 작은 변위와 harmonic normal mode를 가정하고, 직교 전자 기저에서 Hamiltonian을

$$
H=H_e+H_{ph}+H_{e\text{-}ph}
$$

로 나눈다. 각 항은

$$
H_e=\sum_{ij}H_{ij}^{0}c_i^\dagger c_j,
$$

$$
H_{ph}=\sum_\lambda \hbar\omega_\lambda
\left(b_\lambda^\dagger b_\lambda+\frac12\right),
$$

$$
H_{e\text{-}ph}
=\sum_{ij\lambda}M_{ij}^{\lambda}c_i^\dagger c_j
\left(b_\lambda+b_\lambda^\dagger\right)
$$

로 쓸 수 있다. $c_i^\dagger$와 $b_\lambda^\dagger$는 각각 전자 상태 $i$와 phonon mode $\lambda$의 생성 연산자이고, $\omega_\lambda$는 mode 진동수이다. 질량으로 정규화하지 않은 Cartesian 변위를 사용하면 coupling matrix는

$$
M_{ij}^{\lambda}
=\sum_{I\alpha}
\left\langle i\left|
\frac{\partial H_e}{\partial R_{I\alpha}}
\right|j\right\rangle
e_{I\alpha}^{\lambda}
\sqrt{\frac{\hbar}{2M_I\omega_\lambda}}
$$

이다. $I$, $\alpha$, $M_I$와 $e_{I\alpha}^{\lambda}$는 각각 원자, Cartesian 방향, 원자 질량과 정규화된 mode eigenvector 성분이다. 비직교 원자 궤도에서는 $H$의 미분만으로 끝나지 않고 overlap 미분과 기저 이동에 따른 항을 동일한 규약으로 처리해야 한다.[1,2,9]

이 선형화는 EPC가 약하다는 가정과 동일하지 않다. 이는 먼저 원자 변위에 대한 전자 Hamiltonian을 1차까지 전개한 것이다. SCBA와 LOE의 결합 차수, harmonic phonon 가정과 phonon 점유 가정은 그 다음 단계에서 별도로 정해진다.[1,2,9]

### (2) 비탄성 문턱과 관측량

전자가 mode $\lambda$를 방출하거나 흡수하면 전자 에너지는

$$
E_f=E_i\mp\hbar\omega_\lambda
$$

로 바뀐다. 낮은 온도에서 bias window가 $\hbar\omega_\lambda$보다 작으면 자발적 emission의 위상 공간이 막힌다. 따라서 약결합 접합에서는

$$
|eV|\simeq\hbar\omega_\lambda
$$

부근에 $dI/dV$의 step 또는 peak–dip 구조가 생기고, $d^2I/dV^2$의 특징으로 inelastic electron tunneling spectroscopy (IETS)를 해석한다. 새 비탄성 통로가 열려도 탄성 진폭의 renormalization과 간섭 항이 함께 변하므로 conductance가 반드시 증가하는 것은 아니다.[1,2,5]

| 목표 관측량 | 필요한 정보 | 대표적인 해석 |
|---|---|---|
| $I(V)$, $dI/dV$ | 비평형 점유와 전자 self-energy | 비탄성 통로와 탄성 renormalization의 합 |
| $d^2I/dV^2$ | mode-resolved $M^\lambda$, 충분한 에너지 해상도 | 진동 mode의 문턱과 line shape |
| $P_\lambda$, $n_\lambda$ | 전자–phonon power balance와 phonon damping | 국소 발열과 nonequilibrium phonon |
| $\rho(T)$, $\mu(T)$ | 길이·온도별 산란 또는 transmission | phonon-limited resistivity와 mobility |
| Phase-coherence length | 간섭 감쇠 또는 보정된 probe coupling | 환경에 의한 dephasing의 유효 척도 |

## 2. Microscopic NEGF 구조

### (1) Scattering self-energy

EPC를 포함한 device Green's function은

$$
G^R(E)=
\left[
(E+i0^+)S-H_D-\Sigma_L^R-\Sigma_R^R-\Sigma_{e\text{-}ph}^R
\right]^{-1}
$$

이고, 점유는

$$
G^<(E)=G^R(E)
\left(\Sigma_L^<+\Sigma_R^<+\Sigma_{e\text{-}ph}^<\right)
G^A(E)
$$

로 정한다. $\Sigma_{e\text{-}ph}^R$는 전자 준위의 이동과 유한 수명을, $\Sigma_{e\text{-}ph}^{</>}$는 phonon을 흡수·방출하며 상태로 들어오고 나가는 산란을 기술한다. Retarded 성분만 임의의 허수 폭으로 추가하면 점유 재주입과 energy redistribution이 빠지므로 완전한 비탄성 NEGF가 아니다.[1,2]

Mode $\lambda$의 Fock self-energy를 Keldysh convolution으로 쓰면

$$
\Sigma_{\lambda}^{</>}(E)
=i\int\frac{d\varepsilon}{2\pi}
M^\lambda D_\lambda^{</>}(E-\varepsilon)
G^{</>}(\varepsilon)M^\lambda
$$

이다. $D_\lambda$는 phonon Green's function이다. 평형 harmonic phonon을 사용하면 이 convolution은 $G(E-\hbar\omega_\lambda)$와 $G(E+\hbar\omega_\lambda)$를 연결하고, Bose–Einstein occupation

$$
n_B(\hbar\omega_\lambda,T)
=\frac{1}{\exp(\hbar\omega_\lambda/k_BT)-1}
$$

이 absorption과 emission의 상대 가중치를 정한다.[1,2,9]

### (2) 보존 법칙과 phonon 점유

정상 상태에서 일관된 scattering self-energy는 전자 충돌 적분의 총합이 0이 되게 해야 한다.

$$
\int\frac{dE}{2\pi}
\operatorname{Tr}\!\left[
\Sigma_{e\text{-}ph}^<(E)G^>(E)
-\Sigma_{e\text{-}ph}^>(E)G^<(E)
\right]=0
$$

이는 EPC가 소자 안에서 전자의 에너지와 위상은 바꾸더라도 전하를 만들거나 없애지 않는다는 뜻이다. Phonon을 평형 bath에 고정하지 않으면 mode별 점유도

$$
\frac{dn_\lambda}{dt}
=\frac{P_\lambda}{\hbar\omega_\lambda}
-\gamma_{\lambda}^{\mathrm{bath}}
\left[n_\lambda-n_B(\hbar\omega_\lambda,T_{\mathrm{bath}})\right]
$$

같은 rate equation 또는 phonon Dyson equation과 함께 풀어야 한다. $P_\lambda$는 전자가 mode에 전달하는 power이고, $\gamma_{\lambda}^{\mathrm{bath}}$는 전극·주변 격자로 빠져나가는 damping이다. `EPC를 포함했다`는 말만으로 phonon heating까지 포함되지는 않으며, $n_\lambda$를 어떻게 정했는지 함께 밝혀야 한다.[1,2]

## 3. SCBA와 LOE

### (1) Self-consistent Born approximation

Self-consistent Born approximation (SCBA)은 $M^\lambda$에 대해 2차인 Hartree·Fock self-energy의 Green's function을 **dressed** $G$로 평가한다. 따라서

$$
G\rightarrow\Sigma_{e\text{-}ph}[G,D]
\rightarrow G
$$

를 전류와 self-energy가 수렴할 때까지 반복한다. 전자 $G$만 반복하고 phonon $D$는 평형값으로 고정하는 구현과, 전자·phonon Green's function을 함께 반복하는 구현은 서로 다른 물리적 문제를 푼다. 후자는 nonequilibrium phonon population과 전자에 의한 phonon renormalization까지 다룰 수 있지만 계산량과 수렴 난도가 더 크다.[1,2]

SCBA는 bare Born approximation보다 repeated scattering과 spectral broadening을 더 일관되게 포함하고, 대응되는 self-energy와 전류식을 함께 사용하면 전하 보존형 근사가 된다. 그러나 crossing diagram, polaron 형성과 강한 vibronic sideband를 모두 합산하는 정확한 강결합 해법은 아니다. 특히 좁은 전자 공명, 약한 electrode coupling과 큰 구조 재배열 에너지가 함께 나타나면 SCBA 결과만으로 strong-coupling physics를 확정하면 안 된다.[1,2]

### (2) Lowest order expansion

Lowest order expansion (LOE)은 탄성 Green's function 주변에서 전류와 power를 EPC의 최저 비영차수인 $O(M^2)$까지 전개한다.

$$
I_{\mathrm{LOE}}(V)
=I_{\mathrm{el}}^{(0)}(V)
+\sum_\lambda\delta I_\lambda^{(2)}(V)
$$

각 $\delta I_\lambda^{(2)}$에는 실제 phonon emission·absorption 항과 가상 phonon 과정이 바꾸는 탄성 항이 함께 들어간다. 원래의 효율적인 LOE는 $E_F$ 주변 약 $\hbar\omega_\lambda$ 범위에서 $G^R(E)$와 electrode self-energy가 천천히 변한다는 wide-band approximation (WBA)을 사용한다. 이 경우 bias와 온도 의존 에너지 적분을 해석적으로 분리하여 한 번의 탄성 계산과 mode별 $M^\lambda$로 IETS를 빠르게 계산할 수 있다.[1,2]

전자 공명이나 band edge가 phonon energy 범위 안에 있으면 WBA-LOE는 line shape와 세기를 잘못 줄 수 있다. Beyond-WBA LOE는 전자 구조의 에너지 의존성을 유지하면서도 $O(M^2)$ 전개를 사용하여 이 범위를 확장한다. 다만 이는 **wide-band** 가정을 완화하는 것이지 weak-coupling 전개 자체를 없애는 것은 아니다.[1,5]

!!! warning "[Interpretation Caveat]"
    `LOE가 SCBA보다 저렴하다`는 사실은 두 방법의 차이를 충분히 설명하지 못한다. LOE는 $O(M^2)$에서 멈추므로 반복 산란에 의한 self-consistent broadening을 만들지 않는다. SCBA도 강결합의 모든 diagram을 포함하지 않으므로, 두 방법의 일치만으로 perturbation theory의 유효성을 일반적으로 증명할 수는 없다.[1,2,5]

## 4. Büttiker probe

### (1) 현상론적 reservoir

Büttiker probe는 device의 선택한 자유도에 fictitious reservoir $p$를 결합한다.

$$
\Gamma_p(E)=i\left[\Sigma_p^R(E)-\Sigma_p^A(E)\right],
\qquad
\Sigma_p^<(E)=if_p(E)\Gamma_p(E)
$$

Probe로 흡수된 전자는 위상 또는 에너지 정보를 잃은 분포 $f_p$로 재주입되며, $f_p$는 probe가 전하를 순유출하지 않도록 정한다. Dephasing probe는

$$
i_p(E)=0\quad\text{for every }E
$$

를 부과하여 에너지별 입자 수를 보존하고, voltage probe는

$$
I_p=\int i_p(E)\,dE=0
$$

만 부과하여 probe 안에서 에너지가 재분배될 수 있게 한다. Voltage–temperature probe는 추가로 열전류 $J_p=0$을 만족하는 $\mu_p$와 $T_p$를 함께 구한다. 세 모형의 식과 구현은 [Büttiker probe method](buttiker-probe-method.md)에서 자세히 다룬다.[6–8]

### (2) Electron–phonon 모사의 범위

Probe coupling $\Gamma_p$ 또는 $\gamma_p$를 phonon-limited lifetime이나 mean free path에 맞추면 EPC가 만든 dephasing·relaxation의 수송 결과를 낮은 비용으로 근사할 수 있다. 긴 구조에서 tunneling–hopping crossover나 위상 결맞음 소실의 민감도를 조사할 때 특히 유용하다.[7,8]

그러나 dephasing probe는 에너지를 바꾸지 않으므로 phonon emission·absorption의 모형이 아니다. Voltage probe는 에너지를 완화할 수 있지만 $M^\lambda$, $\omega_\lambda$와 Bose occupation에서 산란율을 유도하지 않으므로 mode-resolved IETS 문턱을 예측하지 않는다. 따라서 보정하지 않은 probe strength를 실제 EPC 상수로 해석하거나, probe 결과를 SCBA의 저비용 극한으로 부르면 안 된다.[1,2,7,8]

## 5. MD–Landauer

### (1) 열적 구조 평균

MD–Landauer approach는 온도 $T$에서 molecular dynamics (MD)로 얻은 원자 snapshot $s$마다 coherent Landauer transmission을 계산한다. 원자가 움직이는 MD 영역의 길이를 $L$로 쓰면

$$
T_s(E;T,L)
=\operatorname{Tr}\!\left[
\Gamma_LG_s^R\Gamma_RG_s^A
\right]
$$

이다. $G_s^R$는 snapshot의 고정된 Hamiltonian으로 계산한다. 독립 표본 수를 $N_s$로 쓰면 transmission 평균은

$$
\overline{T}(E;T,L)
=\frac{1}{N_s}\sum_{s=1}^{N_s}T_s(E;T,L)
$$

이고, spin degeneracy를 $g_s$로 쓴 선형 conductance는

$$
G(T,L)=\frac{g_se^2}{h}
\int dE\left(-\frac{\partial f}{\partial E}\right)
\overline{T}(E;T,L)
$$

에서 얻는다. 여러 길이에 대해 diffusive 구간이 확인되면

$$
R(T,L)=R_c(T)+\rho_{1\mathrm D}(T)L
$$

의 기울기로 1차원 resistivity를 추출하고, 단면적 $A$가 명확하면 $\rho_{3\mathrm D}=A\rho_{1\mathrm D}$로 바꾼다. Carrier density $n$이 별도로 정의된 경우 mobility는

$$
\mu(T)=\frac{1}{|q|n\rho_{3\mathrm D}(T)}
$$

로 계산한다. 여기서 $q$는 운반자 전하이며, 전자에는 $|q|=e$를 사용한다. 이 절차와 유사한 thermal-disorder scattering 방법은 결정뿐 아니라 결함·무정형 구조에도 적용할 수 있다.[3,4]

### (2) Adiabatic 근사와 한계

MD–Landauer는 전자가 짧은 MD 영역을 지나는 동안 핵 위치가 사실상 고정되어 있다는 Born–Oppenheimer 시간척도 분리를 사용한다. 각 snapshot의 열적 무질서가 전자를 산란시키므로, 사용한 interatomic potential과 MD가 허용하는 anharmonic displacement를 자연스럽게 반영하고 전자 Hamiltonian의 변위 의존성을 snapshot마다 비선형으로 계산할 수 있다.[3,4]

반면 각 전자는 고정된 potential을 탄성적으로 통과한다. 따라서 전자가 $\hbar\omega_\lambda$를 주고받는 유한 에너지 전이, phonon-assisted tunneling과 mode-resolved IETS는 포함하지 않는다. 고전 MD는 phonon occupation을 Maxwell–Boltzmann 통계로 표본화하므로 낮은 온도의 Bose–Einstein occupation과 zero-point motion도 재현하지 못한다. 온도마다 MD 표본을 새로 만들고, snapshot 수·단면적·길이와 선형 $R(L)$ 구간을 각각 수렴시켜야 한다.[3,4,9]

## 6. 방법 선택과 검증

### (1) 같은 비교축으로 본 차이

| 방법 | 기본 입력 | 에너지 교환 | 적합한 질문 | 핵심 한계 |
|---|---|---|---|---|
| SCBA | $M^\lambda$, $\omega_\lambda$, 전자·phonon Green's function | 명시적 emission·absorption | 비탄성 $I$–$V$, broadening, heating | 높은 계산량, 강결합에서 불완전 |
| LOE | 탄성 GF, $M^\lambda$, $\omega_\lambda$ | $O(M^2)$에서 명시적 | 약결합 IETS와 mode 분석 | 반복 산란 없음, WBA 여부 확인 필요 |
| Büttiker probe | Probe 위치·$\Gamma_p$, 영전류 조건 | 모형에 따라 없음 또는 현상론적 완화 | Dephasing 민감도, 큰 계의 유효 산란 | Microscopic mode·문턱을 예측하지 않음 |
| MD–Landauer | 온도별 MD snapshot, 탄성 transmission | 전자에 대해서는 탄성 | $\rho(T)$, $\mu(T)$, 열적 구조 무질서 | 유한 에너지 전이·양자 핵 효과 없음 |

IETS의 mode별 peak와 국소 heating이 목적이면 LOE로 선별한 뒤 필요한 조건에서 SCBA로 검증하는 순서가 합리적이다. 큰 원자계의 온도 의존 resistivity와 anharmonic structural disorder가 중심이면 MD–Landauer가 직접적인 관측량을 준다. 위상 완화가 interference나 tunneling–hopping crossover에 미치는 민감도만 필요하면 Büttiker probe가 효율적이지만, probe strength를 독립적인 lifetime 또는 mean free path에 맞춰야 한다.[1–8]

### (2) 최소 검증 세트

| 검사 | SCBA·LOE | Büttiker probe | MD–Landauer |
|---|---|---|---|
| 기준 극한 | $M^\lambda\to0$에서 탄도 NEGF | $\Gamma_p\to0$에서 coherent limit | $T\to0$ 해석 시 고전 핵 한계 명시 |
| 보존 법칙 | $I_L+I_R=0$, power balance | 모든 $I_p=0$, 전체 전하 보존 | 각 snapshot의 transmission과 접촉 일관성 |
| 수치 수렴 | 에너지 격자, mode·dynamic region, SCBA 반복 | Probe 위치·세기, 에너지 격자, 영전류 잔차 | 독립 snapshot, 단면적, $k$-점, 길이 구간 |
| 물리 비교 | LOE–SCBA 약결합 일치, IETS 문턱 | 보정한 lifetime·mean free path | $R(L)$ 선형성, 온도별 표본 재생성 |

!!! info "[Measurement]"
    계산 보고에는 전자 온도와 phonon bath 온도, bias 규약, 포함한 mode와 dynamic region, phonon occupation의 결정법을 기록한다. SCBA는 전류 보존 잔차와 self-energy 반복 오차를, LOE는 WBA 또는 beyond-WBA 선택을, probe는 모든 영전류 잔차를, MD–Landauer는 snapshot 사이 상관과 $R(L)$ 회귀 구간을 함께 제시한다.

!!! warning "[Interpretation Caveat]"
    네 방법이 비슷한 $I(V)$ 또는 $\rho(T)$를 주더라도 같은 미시적 과정을 포함했다는 뜻은 아니다. 방법 간 일치는 선택한 관측량과 조건에서의 교차검증이며, mode-resolved energy exchange, dephasing, 열적 구조 무질서를 서로 대체 가능하다고 증명하지 않는다.

## 7. 요약

- EPC 수송의 미시적 출발점은 mode-resolved $M^\lambda$가 전자 상태와 $E\pm\hbar\omega_\lambda$를 연결하는 Hamiltonian이다.
- SCBA는 2차 self-energy를 dressed Green's function으로 반복해 비탄성 산란과 broadening을 다루지만, 일반적인 강결합 정확 해법은 아니다.
- LOE는 $O(M^2)$ 전개로 IETS를 효율적으로 계산하며, 원래 WBA-LOE와 전자 구조의 에너지 의존성을 남기는 beyond-WBA LOE를 구분해야 한다.
- Büttiker probe는 보정 가능한 현상론적 dephasing·relaxation 모형이며, microscopic phonon mode나 emission 문턱을 스스로 예측하지 않는다.
- MD–Landauer는 열적 snapshot의 transmission과 길이 의존 저항을 평균하지만, 유한 electron–phonon energy transfer와 고전 MD 밖의 양자 핵 효과를 포함하지 않는다.
- 방법은 계산량이 아니라 목표 관측량, energy exchange의 필요성, coupling regime와 검증 가능한 기준량에 따라 선택해야 한다.

## 8. 참고문헌

1. T. Frederiksen, M. Paulsson, M. Brandbyge, and A.-P. Jauho, "Inelastic transport theory from first principles: Methodology and application to nanoscale devices," *Physical Review B* **75**, 205413 (2007). [DOI](https://doi.org/10.1103/PhysRevB.75.205413), [arXiv](https://arxiv.org/abs/cond-mat/0611562)
2. M. Galperin, M. A. Ratner, and A. Nitzan, "Molecular transport junctions: Vibrational effects," *Journal of Physics: Condensed Matter* **19**, 103201 (2007). [DOI](https://doi.org/10.1088/0953-8984/19/10/103201), [arXiv](https://arxiv.org/abs/cond-mat/0612085)
3. T. Markussen, M. Palsgaard, D. Stradi, T. Gunst, M. Brandbyge, and K. Stokbro, "Electron-phonon scattering from Green's function transport combined with molecular dynamics: Applications to mobility predictions," *Physical Review B* **95**, 245210 (2017). [DOI](https://doi.org/10.1103/PhysRevB.95.245210), [arXiv](https://arxiv.org/abs/1701.02883)
4. Y. Liu, Z. Yuan, R. J. H. Wesselink, A. A. Starikov, M. van Schilfgaarde, and P. J. Kelly, "Direct method for calculating temperature-dependent transport properties," *Physical Review B* **91**, 220405(R) (2015). [DOI](https://doi.org/10.1103/PhysRevB.91.220405)
5. J.-T. Lü, R. B. Christensen, G. Foti, T. Frederiksen, T. Gunst, and M. Brandbyge, "Efficient calculation of inelastic vibration signals in electron transport: Beyond the wide-band approximation," *Physical Review B* **89**, 081405(R) (2014). [DOI](https://doi.org/10.1103/PhysRevB.89.081405), [arXiv](https://arxiv.org/abs/1312.7625)
6. M. Büttiker, "Four-terminal phase-coherent conductance," *Physical Review Letters* **57**, 1761–1764 (1986). [DOI](https://doi.org/10.1103/PhysRevLett.57.1761)
7. J. L. D'Amato and H. M. Pastawski, "Conductance of a disordered linear chain including inelastic scattering events," *Physical Review B* **41**, 7411–7420 (1990). [DOI](https://doi.org/10.1103/PhysRevB.41.7411)
8. M. Kilgour and D. Segal, "Charge transport in molecular junctions: From tunneling to hopping with the probe technique," *The Journal of Chemical Physics* **143**, 024111 (2015). [DOI](https://doi.org/10.1063/1.4926395), [arXiv](https://arxiv.org/abs/1505.00645)
9. F. Giustino, "Electron-phonon interactions from first principles," *Reviews of Modern Physics* **89**, 015003 (2017). [DOI](https://doi.org/10.1103/RevModPhys.89.015003), [arXiv](https://arxiv.org/abs/1603.06965)
