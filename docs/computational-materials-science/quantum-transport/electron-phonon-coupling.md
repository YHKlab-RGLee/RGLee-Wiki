---
description: 전자–포논 비탄성 수송의 self-energy, deformation potential, SCBA·LOE와 thermal-displacement 방법을 의존 순서로 설명
---

# NEGF: Inelastic electron–phonon scattering

**Electron–phonon coupling (EPC)**은 원자 변위가 전자 Hamiltonian을 바꾸는 상호작용이다. 열린 소자에서는 이 상호작용이 phonon emission·absorption, 전자 위상 완화, 비탄성 전류, 국소 발열과 phonon-limited resistance를 만든다. 계산은 `원자 변위 → coupling matrix → scattering self-energy → Green's function → 전류`의 순서로 이어진다. 각 단계가 무엇을 근사하는지 구분해야 서로 다른 방법을 같은 이론의 정확도 순서로 잘못 배열하지 않는다.[1,2,9]

이 글은 전자 수송에 미치는 phonon의 효과를 다룬다. 격자 자체의 열전도인 **phonon transport**와는 대상 전류가 다르다. Mode-resolved self-consistent Born approximation (SCBA)·lowest order expansion (LOE), deformation potential model, Büttiker probe, molecular dynamics–Landauer (MD–Landauer)와 special thermal displacement (STD)를 다루며, 전극 self-energy, Green's function과 탄도 전류의 규약은 [NEGF formalism](negf-formalism.md)을 따른다.

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

| 단계 | 핵심 양 | 답하는 질문 |
|---|---|---|
| 원자 진동 | $\omega_\lambda$, $e_{I\alpha}^{\lambda}$ | 어떤 원자가 어떤 위상으로 움직이는가? |
| EPC 입력 | $M^\lambda$ 또는 근사한 deformation potential | 그 움직임이 어떤 전자 상태를 연결하는가? |
| 산란 환경 | $\Sigma_{e\text{-}ph}^{R,</>}$ | 준위·점유·수명이 어떻게 바뀌는가? |
| 열린 소자 | $G^{R,</>}$ | 전극과 산란을 동시에 포함한 상태는 무엇인가? |
| 관측량 | $I$, $P_\lambda$, $d^2I/dV^2$ | 전류, 발열과 진동 신호가 어떻게 나타나는가? |

### (2) Deformation potential 근사

**Deformation potential (DP)**은 strain이 band energy를 얼마나 바꾸는지로 long-wavelength acoustic EPC를 압축한 모형이다. Strain tensor를 $u_{\alpha\beta}$로 쓰면 band $n$ 상태의 deformation-potential tensor는

$$
\Xi_{n,\alpha\beta}
=\frac{\partial\varepsilon_n}{\partial u_{\alpha\beta}}
$$

이다. $\varepsilon_n$은 기준 band edge 또는 관심 전자 상태의 에너지이고 $\Xi$의 단위는 energy이다. 등방적 단일 band와 longitudinal acoustic (LA) mode만 남기면 국소 산란 potential을

$$
\delta H_{\mathrm{DP}}(\mathbf r)
=\Xi_d\,\nabla\!\cdot\!\mathbf u(\mathbf r)
$$

로 단순화할 수 있다. $\mathbf u(\mathbf r)$는 변위장이고 $\Xi_d$는 dilation deformation potential이다. 이 strain wave를 양자화하면 normalization domain의 질량을 $\rho_d\Omega_d$로 쓴 경우

$$
g_{\mathrm{DP}}(\mathbf q)
=\Xi_d |\mathbf q|
\sqrt{\frac{\hbar}{2\rho_d\Omega_d\omega_{\mathbf q}}}
$$

를 얻는다. $\rho_d$는 3차원에서 체적 질량 밀도, 2차원에서 면 질량 밀도이며 $\Omega_d$는 각각 부피 또는 면적이다. $\omega_{\mathbf q}\simeq v_s|\mathbf q|$인 acoustic limit에서 $g_{\mathrm{DP}}\propto\sqrt{|\mathbf q|}$이다.[9–11]

DP는 $M^\lambda$를 생략한 별도의 수송 이론이 아니라, 위 미시적 coupling matrix를 continuum parameter로 바꾸는 **입력 근사**이다. 따라서 $g_{\mathrm{DP}}$를 Golden-rule BTE에 넣을 수도 있고, device basis의 $M_{ij}$로 discretize하여 NEGF self-energy에 넣을 수도 있다. 이때 emission·absorption rate의 기본 구조는

$$
\begin{aligned}
W_{i\rightarrow f}
=\frac{2\pi}{\hbar}|g_{fi}|^2
\big[&(n_{\mathbf q}+1)
\delta(\varepsilon_f-\varepsilon_i+\hbar\omega_{\mathbf q})\\
&+n_{\mathbf q}
\delta(\varepsilon_f-\varepsilon_i-\hbar\omega_{\mathbf q})\big]
\end{aligned}
$$

이다. 첫 항은 phonon emission, 둘째 항은 absorption이며 $n_{\mathbf q}$는 phonon occupation이다. 단일 scalar DP는 long-wavelength intravalley acoustic scattering을 빠르게 가늠하지만, transverse·anisotropic response, intervalley와 optical phonon, piezoelectric·Fröhlich long-range field, screening과 interface mode를 자동으로 포함하지 않는다. 복잡한 band와 저차원 물질에서 band-edge shift 하나로 전체 EPC를 대체하면 산란율을 크게 잘못 평가할 수 있다.[10,11]

### (3) 비탄성 문턱과 관측량

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

위 convolution이 어떤 산란을 뜻하는지 보이기 위해 평형 harmonic mode의 delta-function phonon spectrum을 대입하자. $M^\lambda=(M^\lambda)^\dagger$이고 $n_\lambda=n_B(\hbar\omega_\lambda,T)$인 규약에서 lesser·greater self-energy는

$$
\begin{aligned}
\Sigma_\lambda^<(E)
=M^\lambda\big[&
(n_\lambda+1)G^<(E+\hbar\omega_\lambda)\\
&+n_\lambda G^<(E-\hbar\omega_\lambda)
\big]M^\lambda,
\end{aligned}
$$

$$
\begin{aligned}
\Sigma_\lambda^>(E)
=M^\lambda\big[&
(n_\lambda+1)G^>(E-\hbar\omega_\lambda)\\
&+n_\lambda G^>(E+\hbar\omega_\lambda)
\big]M^\lambda
\end{aligned}
$$

로 풀어 쓸 수 있다. $\Sigma^<(E)$의 첫 항은 $E+\hbar\omega_\lambda$에 있던 전자가 phonon을 방출하여 $E$로 들어오는 scattering-in이고, 둘째 항은 $E-\hbar\omega_\lambda$의 전자가 phonon을 흡수하여 $E$로 들어오는 과정이다. $\Sigma^>(E)$는 반대로 $E$의 전자가 나갈 수 있는 빈 상태와 연결된다. 따라서 두 식의 $E\pm\hbar\omega_\lambda$는 단순한 수치 broadening이 아니라 에너지를 주고받는 상태 사이의 연결이다.[1,2,9]

예를 들어 $k_BT\ll\hbar\omega_\lambda$이면 $n_\lambda\simeq0$이므로 absorption 항은 거의 사라진다. 이때도 emission이 일어나려면 초기 점유 상태와 $\hbar\omega_\lambda$ 낮은 빈 최종 상태가 함께 있어야 한다. 저온·저 bias에서 비탄성 전류가 문턱 아래에서 억제되는 이유가 Bose factor뿐 아니라 이 phase space와 Pauli blocking에도 있다.[1,2]

Lesser·greater 성분은 산란으로 생긴 spectral broadening과도 연결된다.

$$
\Gamma_{e\text{-}ph}(E)
=i\left[\Sigma_{e\text{-}ph}^>(E)
-\Sigma_{e\text{-}ph}^<(E)\right]
=-2\operatorname{Im}\Sigma_{e\text{-}ph}^R(E)
$$

이므로 retarded self-energy를

$$
\Sigma_{e\text{-}ph}^R(E)
=\Delta_{e\text{-}ph}(E)
-\frac{i}{2}\Gamma_{e\text{-}ph}(E)
$$

로 나누면 $\Delta_{e\text{-}ph}$는 준위 이동과 탄성 진폭의 renormalization을, $\Gamma_{e\text{-}ph}$는 유한 수명과 폭 넓어짐을 나타낸다. 두 성분은 causality에 의해 Hilbert transform으로 연결되므로, $\Delta$ 또는 principal-value 항을 생략하는 구현은 추가 근사임을 밝혀야 한다.[1,2]

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

## 5. Thermal-displacement Landauer

### (1) 열적 원자 분포와 transmission

MD–Landauer와 special thermal displacement (STD)–Landauer는 원자 변위가 만든 static Hamiltonian의 transmission을 계산한다는 점은 같지만, 열적 원자 분포를 표현하는 방식이 다르다. Mass-weighted normal coordinate를 $Q_\lambda$로 쓰면 harmonic phonon의 양자 열분포는 Gaussian이고 그 분산은

$$
\sigma_\lambda^2(T)
=\left\langle Q_\lambda^2\right\rangle_T
=\frac{\hbar}{2\omega_\lambda}
\coth\!\left(\frac{\hbar\omega_\lambda}{2k_BT}\right)
=\frac{\hbar}{2\omega_\lambda}(2n_\lambda+1)
$$

이다. $2n_\lambda+1$의 상수항은 $T=0$에서도 남는 zero-point motion을 뜻한다. 원자 변위는

$$
\Delta R_{I\alpha}
=\sum_\lambda
\frac{e_{I\alpha}^{\lambda}}{\sqrt{M_I}}Q_\lambda
$$

로 복원한다. $e_{I\alpha}^{\lambda}$와 $M_I$는 각각 mode eigenvector와 원자 질량이다. Harmonic·adiabatic 근사에서 transmission의 양자 열평균은

$$
\left\langle T(E)\right\rangle_T
=\prod_\lambda
\int\frac{dQ_\lambda}{\sqrt{2\pi\sigma_\lambda^2}}
\exp\!\left(-\frac{Q_\lambda^2}{2\sigma_\lambda^2}\right)
T(E;\{Q_\lambda\})
$$

이다. 이 식은 모든 normal coordinate의 확률분포를 적분해야 한다는 뜻이며, mode 수가 늘면 직접 적분이나 무작위 표본화의 비용이 급격히 커진다.[12–14]

### (2) MD–Landauer 표본 평균

MD–Landauer는 온도 $T$의 molecular dynamics (MD) trajectory에서 원자 snapshot $s$를 뽑고, 각 snapshot의 coherent Landauer transmission을 계산한다. 원자가 움직이는 영역의 길이를 $L$로 쓰면

$$
T_s(E;T,L)
=\operatorname{Tr}\!\left[
\Gamma_LG_s^R\Gamma_RG_s^A
\right],
\qquad
\overline{T}(E;T,L)
=\frac{1}{N_s}\sum_{s=1}^{N_s}T_s(E;T,L)
$$

이다. $G_s^R$는 snapshot의 고정된 Hamiltonian으로 계산하며 $N_s$는 독립 표본 수이다. 고전 MD의 평균은 위 양자 harmonic Gaussian과 일반적으로 같지 않다. 고온 harmonic limit에서는 대응하지만, 낮은 온도의 Bose–Einstein occupation과 zero-point motion은 빠진다. 반면 사용한 interatomic potential과 sampling이 충분하면 anharmonic thermal disorder를 포함할 수 있다.[3,4,9]

### (3) Special thermal displacement

STD는 harmonic normal mode의 root-mean-square amplitude를 하나의 대표 구조에 동시에 담는다.

$$
Q_\lambda^{\mathrm{STD}}(T)
=s_\lambda\sigma_\lambda(T),
\qquad s_\lambda\in\{-1,+1\}
$$

$s_\lambda$는 대규모 주기계에서 서로 다른 mode의 교차항이 최대한 상쇄되도록 선택하는 부호이다. 이 구조의 transmission

$$
T_{\mathrm{STD}}(E,T)
=T\!\left(E;\{Q_\lambda^{\mathrm{STD}}(T)\}\right)
$$

하나로 $\langle T(E)\rangle_T$를 근사하므로, 많은 snapshot을 필요로 하는 직접 표본 평균보다 저렴하다. Quantum occupation과 zero-point amplitude가 $\sigma_\lambda(T)$에 들어가며, displaced Hamiltonian을 직접 풀기 때문에 전자 응답의 변위 의존성을 단순한 $O(M^2)$ 항으로 잘라내지 않는다.[12–14]

그러나 one-shot 정확도는 무조건 보장되지 않는다. 원래의 상쇄 논리는 많은 mode와 반복 단위를 가진 큰 주기계의 thermodynamic limit에서 정당화된다. 작은 소자, 강한 국소 mode, 결함과 비주기 구조에서는 supercell 크기, 부호 집합과 소수 configuration 평균에 대한 수렴을 별도로 확인해야 한다.[12–14]

### (4) Conductance 추출과 adiabatic 한계

Spin degeneracy를 $g_s$로 쓰면 MD 평균 또는 STD transmission의 선형 conductance는

$$
G(T,L)=\frac{g_se^2}{h}
\int dE\left(-\frac{\partial f}{\partial E}\right)
\left\langle T(E;T,L)\right\rangle
$$

에서 얻는다. 여러 길이에서 diffusive 구간이 확인되면

$$
R(T,L)=R_c(T)+\rho_{1\mathrm D}(T)L
$$

의 기울기로 1차원 resistivity를 추출한다. 단면적 $A$가 명확하면 $\rho_{3\mathrm D}=A\rho_{1\mathrm D}$로 바꾸고, carrier density $n$의 규약이 정해졌을 때

$$
\mu(T)=\frac{1}{|q|n\rho_{3\mathrm D}(T)}
$$

로 mobility를 얻는다. $R_c$를 분리하지 않고 한 길이의 resistance만 bulk resistivity로 바꾸면 contact 저항이 mobility에 섞인다.[3,4,12,14]

MD–Landauer와 STD–Landauer는 전자가 산란 영역을 지나는 동안 핵 위치가 고정되어 있다는 Born–Oppenheimer 시간척도 분리를 사용한다. 각 transmission 계산에서 전자는 static potential을 탄성적으로 통과한다. 변위된 구조는 momentum selection을 풀고 phonon-assisted tunneling과 온도 의존 renormalization을 열평균 의미에서 근사할 수 있지만, 특정 전자가 mode $\lambda$에 $\hbar\omega_\lambda$를 주고받는 시간 순서는 추적하지 않는다. 따라서 phonon energy 척도의 IETS line shape, mode-resolved nonequilibrium occupation과 전자–phonon power flow에는 energy-resolved SCBA·LOE가 필요하다.[1–4,12–14]

## 6. 방법 선택과 검증

### (1) 같은 비교축으로 본 차이

| 방법 | 기본 입력 | 에너지 교환 | 적합한 질문 | 핵심 한계 |
|---|---|---|---|---|
| SCBA | $M^\lambda$, $\omega_\lambda$, 전자·phonon Green's function | 명시적 emission·absorption | 비탄성 $I$–$V$, broadening, heating | 높은 계산량, 강결합에서 불완전 |
| LOE | 탄성 GF, $M^\lambda$, $\omega_\lambda$ | $O(M^2)$에서 명시적 | 약결합 IETS와 mode 분석 | 반복 산란 없음, WBA 여부 확인 필요 |
| Deformation potential | $\Xi$, elastic constant, acoustic dispersion | 사용하는 solver가 결정 | 장파장 acoustic scattering의 저비용 추정 | 단일 scalar로 anisotropy·다른 mode를 잃기 쉬움 |
| Büttiker probe | Probe 위치·$\Gamma_p$, 영전류 조건 | 모형에 따라 없음 또는 현상론적 완화 | Dephasing 민감도, 큰 계의 유효 산란 | Microscopic mode·문턱을 예측하지 않음 |
| MD–Landauer | 온도별 MD snapshot, 탄성 transmission | 전자에 대해서는 탄성 | $\rho(T)$, $\mu(T)$, 열적 구조 무질서 | 유한 에너지 전이·양자 핵 효과 없음 |
| STD–Landauer | Harmonic mode, quantum thermal amplitude, 특수 변위 구조 | 각 구조에서는 탄성 | 큰 주기 소자의 phonon-assisted tunneling과 열평균 transmission | 작은·국소·비주기계에서 one-shot 수렴 필요 |

IETS의 mode별 peak와 국소 heating이 목적이면 LOE로 선별한 뒤 필요한 조건에서 SCBA로 검증하는 순서가 합리적이다.[1,2,5] 장파장 acoustic scattering이 지배적이라는 근거가 있고 빠른 추정이 목적이면 DP가 유용하지만, full $M^\lambda$의 일부를 압축한 것임을 밝혀야 한다.[9–11] 큰 원자계의 anharmonic structural disorder가 중심이면 MD–Landauer가, harmonic quantum displacement를 포함한 대규모 주기 소자의 열평균이 목적이면 STD–Landauer가 적합하다.[3,4,12–14] 위상 완화의 민감도만 필요하면 Büttiker probe가 효율적이지만, probe strength를 독립적인 lifetime 또는 mean free path에 맞춰야 한다.[6–8]

### (2) 최소 검증 세트

| 검사 | SCBA·LOE·DP 입력 | Büttiker probe | MD·STD–Landauer |
|---|---|---|---|
| 기준 극한 | $M^\lambda\to0$에서 탄도 NEGF; DP는 full EPC와 제한 조건 비교 | $\Gamma_p\to0$에서 coherent limit | 변위 $\to0$에서 coherent Landauer |
| 보존 법칙 | $I_L+I_R=0$, power balance | 모든 $I_p=0$, 전체 전하 보존 | 각 snapshot의 transmission과 접촉 일관성 |
| 수치 수렴 | 에너지 격자, mode·dynamic region, SCBA 반복; DP tensor·branch | Probe 위치·세기, 에너지 격자, 영전류 잔차 | MD snapshot·상관 또는 STD supercell·부호, $k$점과 길이 |
| 물리 비교 | LOE–SCBA 약결합 일치, IETS 문턱, DP–full EPC 산란율 | 보정한 lifetime·mean free path | $R(L)$ 선형성, MD–STD가 공유하는 harmonic 조건 비교 |

!!! info "[Measurement]"
    계산 보고에는 전자 온도와 phonon bath 온도, bias 규약, 포함한 mode와 dynamic region, phonon occupation의 결정법을 기록한다. SCBA는 전류 보존 잔차와 self-energy 반복 오차를, LOE는 WBA 또는 beyond-WBA 선택을 기록한다. DP는 $\Xi$의 tensor/scalar 규약, strain 방향, 포함한 acoustic branch와 screening을 밝힌다. Probe는 모든 영전류 잔차를, MD–Landauer는 snapshot 사이 상관을, STD–Landauer는 supercell과 부호 configuration 수렴을 기록하며 두 thermal-displacement 방법 모두 $R(L)$ 회귀 구간을 제시한다.

!!! warning "[Interpretation Caveat]"
    여러 방법이 비슷한 $I(V)$ 또는 $\rho(T)$를 주더라도 같은 미시적 과정을 포함했다는 뜻은 아니다. 방법 간 일치는 선택한 관측량과 조건에서의 교차검증이며, mode-resolved energy exchange, deformation-potential 입력, dephasing과 thermal-displacement 평균을 서로 대체 가능하다고 증명하지 않는다.

## 7. 요약

- EPC 수송의 미시적 출발점은 mode-resolved $M^\lambda$가 전자 상태와 $E\pm\hbar\omega_\lambda$를 연결하는 Hamiltonian이다.
- Lesser·greater self-energy는 emission과 absorption의 scattering-in/out을 $E\pm\hbar\omega_\lambda$에서 연결하며, retarded 성분의 실수부와 허수부는 각각 준위 renormalization과 spectral broadening을 정한다.
- Deformation potential은 장파장 acoustic EPC를 strain에 대한 band-energy 미분으로 압축한 입력 근사이며, anisotropy·intervalley·optical·long-range coupling을 포함하는 일반적인 $M^\lambda$와 같지 않다.
- SCBA는 2차 self-energy를 dressed Green's function으로 반복하지만 일반적인 강결합 정확 해법은 아니다. LOE는 $O(M^2)$ 전개로 IETS를 효율적으로 계산하며 WBA와 beyond-WBA를 구분해야 한다.
- Büttiker probe는 보정 가능한 현상론적 dephasing·relaxation 모형이며, microscopic phonon mode나 emission 문턱을 스스로 예측하지 않는다.
- MD–Landauer는 여러 열적 snapshot을, STD–Landauer는 harmonic quantum distribution을 대표하는 특수 변위 구조를 사용한다. 둘 다 energy-resolved self-energy 없이 mode별 power flow나 IETS line shape를 주지는 않는다.

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
10. A. M. Ganose, J. Park, A. Faghaninia, R. Woods-Robinson, K. A. Persson, and A. Jain, "Efficient calculation of carrier scattering rates from first principles," *Nature Communications* **12**, 2222 (2021). [DOI](https://doi.org/10.1038/s41467-021-22440-5)
11. K. Kaasbjerg, K. S. Thygesen, and A.-P. Jauho, "Acoustic phonon limited mobility in two-dimensional semiconductors: Deformation potential and piezoelectric scattering in monolayer MoS2 from first principles," *Physical Review B* **85**, 115317 (2012). [DOI](https://doi.org/10.1103/PhysRevB.85.115317), [arXiv](https://arxiv.org/abs/1206.2003)
12. T. Gunst, T. Markussen, M. L. N. Palsgaard, K. Stokbro, and M. Brandbyge, "First-principles electron transport with phonon coupling: Large scale at low cost," *Physical Review B* **96**, 161404(R) (2017). [DOI](https://doi.org/10.1103/PhysRevB.96.161404), [arXiv](https://arxiv.org/abs/1706.09290)
13. M. Zacharias and F. Giustino, "Theory of the special displacement method for electronic structure calculations at finite temperature," *Physical Review Research* **2**, 013357 (2020). [DOI](https://doi.org/10.1103/PhysRevResearch.2.013357), [arXiv](https://arxiv.org/abs/1912.10929)
14. Z. Fan, J. H. Garcia, A. W. Cummings, J. E. Barrios-Vargas, M. Panhans, A. Harju, F. Ortmann, and S. Roche, "Linear scaling quantum transport methodologies," *Physics Reports* **903**, 1–69 (2021). [DOI](https://doi.org/10.1016/j.physrep.2020.12.001)
