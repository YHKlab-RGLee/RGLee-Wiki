---
description: 전자구조와 electron–phonon coupling에서 저전계 carrier mobility를 계산하는 Boltzmann transport workflow, 근사 계층과 mean free path 해석
---

# Carrier mobility from first principles

**Carrier mobility** $\boldsymbol{\mu}$는 약한 전기장에 대한 운반자 drift velocity 또는 전류의 선형 응답을 나타낸다. 전자구조 계산은 band energy, group velocity와 유효 질량을 주지만, 절대 mobility를 정하려면 평형 분포가 산란으로 어떻게 이완되는지도 알아야 한다. 이상적인 결정에서 온도 의존 mobility를 예측할 때는 보통 density functional theory (DFT)와 density-functional perturbation theory (DFPT)로 전자–포논 결합을 계산하고, 그 결과를 선형화한 Boltzmann transport equation (BTE)에 넣는다.[1–4]

이 글은 균일한 bulk 또는 2차원 결정의 저전계 band transport를 중심으로, constant relaxation time approximation (CRTA)부터 electron–phonon coupling (EPC)을 포함한 반복 BTE까지를 하나의 계층으로 정리한다. 열린 소자의 비탄성 전류와 국소 발열은 [Electron–phonon coupling](electron-phonon-coupling.md)에서, 접촉과 유한 길이를 명시한 탄도 수송은 [NEGF formalism](negf-formalism.md)에서 다룬다.

## 1. Mobility의 정의와 계산 대상

### (1) Conductivity와 drift mobility

균일한 물질에 충분히 약한 전기장 $\mathbf E$를 가하면 전류 밀도는

$$
J_\alpha=\sum_\beta \sigma_{\alpha\beta}E_\beta
$$

로 쓸 수 있다. 한 종류의 운반자가 우세하고 그 농도를 $n_c$라 하면 drift mobility tensor는

$$
\mu_{\alpha\beta}=\frac{\sigma_{\alpha\beta}}{|q|n_c}
$$

로 정의한다. $q=-e$인 전자와 $q=+e$인 정공을 구분하되, mobility의 크기에는 $|q|=e$를 사용한다. 전도대 전자를 예로 들면 단위 부피당 농도는

$$
n_c=\frac{g_s}{V_{\mathrm{cell}}N_k}
\sum_{n\mathbf k\in\mathrm{CB}} f^0_{n\mathbf k}
$$

이다. $g_s$는 계산에 이미 포함되지 않은 spin degeneracy, $V_{\mathrm{cell}}$은 primitive-cell 부피, $N_k$는 Brillouin zone 표본 수, $f^0$는 Fermi–Dirac 분포이다. 정공 농도는 valence band의 $1-f^0$를 합한다. 2차원 재료에서는 임의의 vacuum 두께가 들어간 3차원 부피 대신 면적과 sheet carrier density를 사용해야 하며, 보고 단위도 $\mathrm{cm^2\,V^{-1}\,s^{-1}}$인지 sheet conductance에서 유도한 값인지 밝혀야 한다.[1,2,4,5]

각 Bloch 상태의 group velocity는

$$
v_{n\mathbf k,\alpha}
=\frac{1}{\hbar}\frac{\partial\varepsilon_{n\mathbf k}}{\partial k_\alpha}
$$

이다. 따라서 mobility는 band curvature만의 성질이 아니라, Fermi window 안의 상태별 속도와 산란에 의해 만들어진 비평형 분포를 함께 평균한 수송 계수이다.[1,2,4,5]

### (2) Drude 식의 위치

등방성 포물선 band, 하나의 유효 질량 $m^*$, 에너지와 방향에 무관한 relaxation time $\tau$를 가정하면

$$
\mu=\frac{e\tau}{m^*}
$$

를 얻는다. 이 식은 가벼운 band와 긴 lifetime이 mobility에 유리하다는 직관을 주지만, 다중 valley, nonparabolic band, anisotropic scattering과 inelastic intervalley scattering을 하나의 $m^*$와 $\tau$로 축약한다. 실제 first-principles 계산에서 상태별 $\tau_{n\mathbf k}$를 먼저 구한 뒤 위 식을 다시 사용하기보다, conductivity tensor를 직접 적분하는 편이 일반적이다.[1,2,5,6]

### (3) Drift mobility와 Hall mobility

자기장이 없는 선형 BTE에서 얻는 값은 drift mobility이다. Hall mobility는 약한 자기장에 대한 분포의 1차 보정과 Hall coefficient를 추가로 계산해야 하며,

$$
\mu_{\mathrm H}=r_{\mathrm H}\mu_{\mathrm d}
$$

에서 Hall factor $r_{\mathrm H}$가 일반적으로 1이라고 가정할 수 없다. 실험의 Hall mobility와 계산의 phonon-limited drift mobility를 직접 비교하려면 mobility 종류, 운반자 농도, 온도와 포함한 산란원을 먼저 맞춰야 한다.[1,2]

## 2. 전자구조에서 transport kernel까지

### (1) 선형화한 Boltzmann transport equation

전기장에 의한 작은 분포 변화는 다음 규약으로 쓸 수 있다.

$$
f_{n\mathbf k}=f^0_{n\mathbf k}
-q\sum_\beta E_\beta F_{n\mathbf k,\beta}
\left(-\frac{\partial f^0}{\partial\varepsilon}\right)_{n\mathbf k}.
$$

$\mathbf F_{n\mathbf k}$는 길이 차원의 mean free displacement vector이며, 충돌 적분을 포함한 선형 BTE의 해이다. 이 규약을 conductivity에 대입하면

$$
\sigma_{\alpha\beta}
=\frac{g_sq^2}{V_{\mathrm{cell}}N_k}
\sum_{n\mathbf k}
v_{n\mathbf k,\alpha}F_{n\mathbf k,\beta}
\left(-\frac{\partial f^0}{\partial\varepsilon}\right)_{n\mathbf k}
$$

를 얻는다. $-\partial f^0/\partial\varepsilon$는 chemical potential 주변에서 실제로 전류에 참여하는 에너지 창을 정하고, $\mathbf F$는 각 상태가 산란되기 전에 전류 방향으로 기여하는 정도를 정한다.[1,2,7]

### (2) CRTA와 band-only screening

CRTA에서는 모든 상태에 같은 $\tau_0$를 두어

$$
\mathbf F_{n\mathbf k}^{\mathrm{CRTA}}
=\mathbf v_{n\mathbf k}\tau_0
$$

로 놓는다. 이때 전자구조만으로 직접 정해지는 것은 $\boldsymbol\sigma/\tau_0$이고, 절대 conductivity나 mobility에는 외부에서 정한 $\tau_0$가 필요하다. 따라서 CRTA는 band anisotropy, doping에 따른 transport distribution과 Seebeck coefficient를 빠르게 살피는 데 유용하지만, 서로 다른 재료의 절대 mobility를 매개변수 없이 예측하는 방법은 아니다.[1,5,6]

| 계산 수준 | 산란 입력 | 직접 얻는 양 | 적합한 용도 | 잃는 정보 |
|---|---|---|---|---|
| Band curvature | 없음 | $m^*$, $\mathbf v_{n\mathbf k}$ | valley와 anisotropy의 1차 판별 | lifetime과 산란 선택 규칙 |
| CRTA | 단일 $\tau_0$ | $\boldsymbol\sigma/\tau_0$, 가정한 $\tau_0$의 $\boldsymbol\mu$ | 빠른 전자구조 screening | 온도·상태·mode별 산란 |
| 모형 scattering | 변형 퍼텐셜, 유전율, 불순물 농도 등 | 상태별 rate와 mobility | 많은 재료의 효율적 비교 | 완전한 mode-resolved EPC |
| DFPT–BTE | $g_{mn\nu}(\mathbf k,\mathbf q)$와 phonon | phonon-limited $\boldsymbol\mu(T,n_c)$ | 이상 결정의 정량 예측 | 계산에 넣지 않은 extrinsic scattering |

이 표의 단계들은 단순히 정밀도만 다른 것이 아니다. 각 단계가 요구하는 입력과 검증 가능한 관측량이 다르므로, CRTA 결과에 경험적 $\tau$를 곱한 값과 DFPT–BTE 결과를 모두 `first-principles mobility`라고 부르면 계산의 예측 범위가 흐려진다.[1,5,6]

## 3. Electron–phonon scattering

### (1) DFPT coupling matrix

Harmonic phonon과 전자 퍼텐셜의 1차 변화를 사용하는 질량 정규화 규약에서 EPC matrix element는

$$
g_{mn\nu}(\mathbf k,\mathbf q)
=\sqrt{\frac{\hbar}{2\omega_{\mathbf q\nu}}}
\left\langle\psi_{m,\mathbf k+\mathbf q}\middle|
\Delta_{\mathbf q\nu}V_{\mathrm{KS}}
\middle|\psi_{n\mathbf k}\right\rangle
$$

로 쓸 수 있다. $\Delta_{\mathbf q\nu}V_{\mathrm{KS}}$에는 원자 질량으로 정규화한 phonon eigenvector와 Kohn–Sham potential의 변위 미분이 들어가며, $\nu$는 phonon branch이다. 다른 코드가 원자 질량과 $\sqrt{\hbar/(2\omega)}$를 perturbation 또는 $g$에 배치하는 방식은 달라도 최종 scattering probability $|g|^2$의 규약은 일관되어야 한다.[3,4,7,8]

EPC는 전자 상태 $(n,\mathbf k)$를 $(m,\mathbf k+\mathbf q)$로 옮기면서 phonon을 흡수하거나 방출한다. Pauli blocking을 충돌 적분에서 별도로 적용하는 규약으로 Golden-rule transition rate를 쓰면

$$
W_{n\mathbf k\rightarrow m,\mathbf k+\mathbf q}^{\nu,\mathrm{em}}
=\frac{2\pi}{\hbar}|g_{mn\nu}(\mathbf k,\mathbf q)|^2
(N_{\mathbf q\nu}+1)
\delta\!\left(
\varepsilon_{n\mathbf k}-\varepsilon_{m,\mathbf k+\mathbf q}
-\hbar\omega_{\mathbf q\nu}
\right),
$$

$$
W_{n\mathbf k\rightarrow m,\mathbf k+\mathbf q}^{\nu,\mathrm{abs}}
=\frac{2\pi}{\hbar}|g_{mn\nu}(\mathbf k,\mathbf q)|^2
N_{\mathbf q\nu}
\delta\!\left(
\varepsilon_{n\mathbf k}-\varepsilon_{m,\mathbf k+\mathbf q}
+\hbar\omega_{\mathbf q\nu}
\right)
$$

이다. Bose occupation은

$$
N_{\mathbf q\nu}
=\frac{1}{\exp(\hbar\omega_{\mathbf q\nu}/k_BT)-1}
$$

이다. Emission에는 spontaneous emission을 포함한 $N+1$, absorption에는 $N$이 곱해지고, 충돌 적분에는 최종 전자 상태의 $1-f$가 추가된다. 이 식은 acoustic·optical, intravalley·intervalley 산란을 동일한 상태 합으로 다루며, 가능한 전이의 에너지 보존과 mode별 결합 세기를 함께 반영한다.[1–4,7]

### (2) SERTA와 반복 BTE

Self-energy relaxation time approximation (SERTA)에서는 상태 밖으로 나가는 전체 rate로

$$
\tau_{n\mathbf k}^{-1}
=\sum_{m\nu\mathbf q,\pm}
W_{n\mathbf k\rightarrow m,\mathbf k+\mathbf q}^{\nu,\pm}
$$

를 만들고 $\mathbf F_{n\mathbf k}=\mathbf v_{n\mathbf k}\tau_{n\mathbf k}$로 둔다. 구현에 따라 equilibrium Fermi factor와 detailed-balance 항이 $W$ 또는 충돌 연산자에 배치되므로, 코드 간 lifetime을 비교할 때 정의를 확인해야 한다.[1,2,7]

반복 BTE는 산란되어 들어오는 상태의 비평형 분포까지 남겨 다음 형태의 선형계를 푼다.

$$
\mathbf F_{n\mathbf k}
=\mathbf v_{n\mathbf k}\tau_{n\mathbf k}
+\tau_{n\mathbf k}
\sum_{m\nu\mathbf q,\pm}
\widetilde W_{n\mathbf k,m\mathbf k+\mathbf q}^{\nu,\pm}
\mathbf F_{m,\mathbf k+\mathbf q}.
$$

$\widetilde W$는 선형화와 detailed balance에 맞춘 scattering-in kernel이다. 두 번째 항을 버리면 SERTA가 된다. 특히 전자의 진행 방향을 거의 바꾸지 않는 forward scattering은 lifetime을 짧게 만들 수 있어도 전류를 같은 비율로 이완시키지 않으므로, 상태 lifetime과 transport relaxation을 구분해야 한다. 반복 BTE는 이 angular redistribution을 명시적으로 복원한다.[1,2,7,8]

| 해법 | 유지하는 정보 | 장점 | 주의점 |
|---|---|---|---|
| CRTA | band velocity와 단일 $\tau_0$ | 가장 저렴하고 해석이 단순함 | 절대 mobility가 $\tau_0$에 비례함 |
| SERTA/RTA | 상태·mode별 scattering-out | phonon energy와 선택 규칙을 포함함 | scattering-in과 vertex-like 보정을 버림 |
| Iterative BTE | 상태 사이의 선형화한 충돌 연산자 | 방향 재분포와 transport lifetime을 복원함 | 매우 조밀한 $k/q$ 격자와 반복 수렴이 필요함 |

## 4. First-principles 계산 workflow

### (1) Coarse grid에서 interpolation까지

실제 계산은 다음 의존 순서를 따른다.[1–5,8]

```text
구조·DFT 수렴
  → band energy와 wavefunction
  → DFPT phonon과 coarse-grid EPC
  → Wannier 또는 동등한 interpolation
  → dense k/q grid의 velocity·g matrix
  → 온도·carrier density별 chemical potential
  → SERTA 또는 iterative BTE
  → conductivity, drift mobility, mean-free-path spectrum
```

EPC가 Fermi window 안에서 급격히 변하고 energy-conserving surface가 얇기 때문에, 전자 총에너지에 충분한 $k$ 격자보다 훨씬 조밀한 transport용 $k/q$ 격자가 필요할 수 있다. Wannier interpolation은 coarse-grid DFPT 결과를 실공간의 국소화된 표현으로 옮긴 뒤 dense grid로 복원하여 이 비용을 줄인다. Polar material에서는 장거리 Fröhlich 성분, 필요할 때 dynamical quadrupole과 piezoelectric 성분을 단거리 interpolation과 일관되게 분리해야 한다.[1–5,8]

### (2) 수렴과 계산 조건

Mobility는 band edge 부근의 작은 에너지 오차, 속도, phonon frequency와 $|g|^2$에 동시에 민감하다. 그러므로 cutoff와 ground-state $k$ 격자만 수렴시키는 것으로 충분하지 않다. 다음 항목을 mobility 자체에 대해 점검한다.[1,2,4,5,8]

| 수렴 변수 | 바뀌는 물리량 | 최소 확인 방법 |
|---|---|---|
| 전자 $k$와 phonon $q$ 격자 | energy-conserving 전이의 위상 공간 | 격자를 독립적으로 늘려 tensor 성분 비교 |
| Delta function 폭 또는 적분법 | 산란율의 energy conservation | 폭을 줄이거나 tetrahedron/adaptive scheme과 비교 |
| Wannier window와 gauge | velocity와 interpolation된 $g$ | 원래 coarse grid와 band·coupling 재현 확인 |
| DFT functional, SOC, band correction | 유효 질량, valley splitting, 산란 통로 | 목표 band edge와 실험·고수준 계산 비교 |
| 온도와 carrier density | phonon 점유와 Fermi window | 각 조건에서 chemical potential을 다시 결정 |
| Polar long-range correction | 작은 $q$의 coupling | 작은-$q$ 수렴과 analytic/nonanalytic 분할 확인 |

!!! info "[Measurement]"
    계산 보고에는 결정 구조와 dimensional normalization, exchange–correlation functional, pseudopotential, spin–orbit coupling 여부, 전자·phonon coarse grid, 최종 $k/q$ grid, interpolation window, delta-function 처리법을 기록한다. 결과마다 온도, electron 또는 hole density, chemical potential, 포함한 scattering mechanism, SERTA 또는 iterative solver, conductivity와 mobility tensor를 함께 제시한다. Hall 값을 보고한다면 자기장에 대한 BTE 차수와 Hall factor도 별도로 기록한다.

### (3) 도구를 선택하는 기준

BoltzTraP2 같은 band interpolation 도구는 $\boldsymbol\sigma/\tau$와 CRTA 경향을 얻는 데 적합하다. AMSET 계열의 접근은 전자구조에 acoustic deformation potential, polar optical phonon, piezoelectric과 ionized-impurity 모형을 결합하여 완전한 DFPT EPC보다 낮은 비용으로 상태별 산란을 추정한다. EPW와 Perturbo 계열은 DFPT EPC를 dense grid로 interpolation하여 SERTA 또는 iterative BTE를 푼다. 도구 이름보다 실제로 제공한 산란 입력과 푼 충돌 방정식을 기준으로 결과 수준을 구분해야 한다.[1,4–6,8]

## 5. Scattering length scale와 유한 크기

### (1) Mean free path는 BTE 해에서 나온다

RTA에서는 상태별 mean free displacement가

$$
\boldsymbol\Lambda_{n\mathbf k}^{\mathrm{RTA}}
=\mathbf v_{n\mathbf k}\tau_{n\mathbf k}
$$

이다. 반복 BTE에서는 $\mathbf F_{n\mathbf k}$가 다른 상태의 scattering-in 기여까지 포함하므로 $\mathbf v\tau$와 같지 않다. 수송 방향의 유효 scalar mean free path는

$$
\Lambda_{n\mathbf k}
=\frac{\mathbf F_{n\mathbf k}\cdot\mathbf v_{n\mathbf k}}
{|\mathbf v_{n\mathbf k}|}
$$

처럼 투영하여 정의할 수 있다. 따라서 scattering length scale은 mobility에 나중에 곱하는 독립 보정 인자가 아니라, 동일한 collision problem에서 얻은 상태별 속도와 relaxation의 공간 척도이다.[1,2,7]

상태별 기여를 mean free path로 누적하면

$$
\sigma_{\alpha\beta}^{\mathrm{acc}}(\Lambda_0)
=\frac{g_sq^2}{V_{\mathrm{cell}}N_k}
\sum_{n\mathbf k}
v_{n\mathbf k,\alpha}F_{n\mathbf k,\beta}
\left(-\frac{\partial f^0}{\partial\varepsilon}\right)
\Theta(\Lambda_0-\Lambda_{n\mathbf k})
$$

의 accumulation spectrum을 만들 수 있다. 이 양은 어느 길이 이하의 운반자가 bulk conductivity에 얼마나 기여하는지를 보여 주므로, grain size나 channel length와 비교할 때 단일 평균 mean free path보다 정보가 많다.[7,9]

### (2) 물질 mobility와 소자 길이의 구분

Bulk BTE mobility는 공간적으로 균일한 전기장과 충돌 적분을 가정한 물질 계수이다. 대표 소자 길이 $L$과 운반자의 $\Lambda$를 비교하면 다음 수송 영역을 구분할 수 있다.[7,9,10]

| 길이 관계 | 지배적인 설명 | Mobility 해석 |
|---|---|---|
| $L\gg\Lambda$ | 많은 산란을 거친 diffusive transport | bulk $\sigma$와 $\mu$가 직접적인 구성 관계가 됨 |
| $L\sim\Lambda$ | quasi-ballistic crossover | 접촉과 길이 의존 transmission을 함께 다뤄야 함 |
| $L\ll\Lambda$ | ballistic transport | bulk mobility만으로 conductance를 정할 수 없음 |

경계, grain과 interface는 intrinsic phonon BTE에 자동으로 포함되지 않는다. 그 길이 효과를 다루려면 경계 산란을 collision operator에 물리적으로 추가하거나, 실제 길이와 접촉을 갖는 Landauer 또는 NEGF 문제를 풀어야 한다. 여러 길이의 transmission에서 diffusive 구간이 확인되면

$$
R(L)=R_c+\rho L/A
$$

의 기울기로 bulk resistivity를 추출하고

$$
\mu=\frac{1}{|q|n_c\rho}
$$

로 mobility와 연결할 수 있다. $R_c$는 접촉 저항, $A$는 단면적이다. 이 회귀는 ballistic 접촉항과 길이에 비례하는 저항이 분리되는 구간에서만 의미가 있다.[9,10]

!!! warning "[Interpretation Caveat]"
    `Scattering length를 고려한 mobility`는 두 질문을 구분해야 한다. 무한 결정의 EPC 계산에서는 mean free path가 BTE 해의 결과이고, finite device에서는 $L/\Lambda$가 bulk mobility를 소자 conductance로 바꿔도 되는지를 판정한다. 경험적인 경계 mean free path를 intrinsic $\tau$에 단순히 더하는 Matthiessen 방식은 독립 산란·완화시간 근사가 성립할 때의 모형이며, 원자적 interface와 coherent reflection을 자동으로 설명하지 않는다.[1,7,9,10]

## 6. 추가 산란과 결과 해석

### (1) Phonon-limited mobility의 의미

DFPT–BTE로 EPC만 넣어 얻은 값은 선택한 전자·phonon 이론 안에서의 **phonon-limited mobility**이다. 실제 시료에는 ionized impurity, neutral defect, alloy disorder, grain boundary, interface roughness와 경우에 따라 carrier–carrier scattering이 추가된다. 서로 독립인 약한 산란을 같은 relaxation-time 수준에서 다룰 때는

$$
\tau_{n\mathbf k,\mathrm{tot}}^{-1}
\approx\sum_s\tau_{n\mathbf k,s}^{-1}
$$

로 rate를 합할 수 있지만, scalar mobility에 Matthiessen rule을 적용하는 것은 anisotropic·inelastic scattering의 전체 collision operator를 푸는 것보다 강한 근사이다. 실험값보다 높은 phonon-limited mobility는 곧 계산 실패를 뜻하지 않으며, 반대로 우연한 일치가 누락 산란의 부재를 증명하지도 않는다.[1,2,5,6]

### (2) 전자구조 정확도와 모형 오차

산란율에는 energy-conserving final state와 $|g|^2$가 함께 들어가므로 band gap, valley ordering, effective mass와 spin–orbit splitting의 오차가 mobility에 증폭될 수 있다. Polar semiconductor에서는 작은 $q$의 장거리 coupling을 잘못 interpolation하면 격자를 늘려도 틀린 극한으로 수렴할 수 있다. 또한 harmonic phonon, lowest-order EPC와 semiclassical quasiparticle picture가 무너지는 강한 disorder, polaronic localization 또는 매우 높은 전기장에서는 이 workflow의 적용 범위를 다시 검토해야 한다.[1–5,8]

| 질문 | 권장 최소 모형 | 결과를 부르는 방식 |
|---|---|---|
| Band가 수송에 유리한가? | DFT + velocity/effective mass 또는 CRTA | $m^*$, $\sigma/\tau$; 절대 mobility라고 부르지 않음 |
| 이상 결정의 온도 의존성은? | DFPT EPC + SERTA, 필요하면 iterative BTE | phonon-limited drift mobility |
| 불순물·polar scattering의 경향은? | 검증된 상태별 모형 scattering | 포함한 mechanism을 명시한 mobility |
| Hall 측정과 비교하는가? | 자기장 보정 BTE + 실제 산란원 | Hall mobility와 Hall factor |
| Channel이 mean free path와 비슷한가? | Landauer/NEGF 또는 경계 포함 BTE | 길이 의존 conductance 또는 apparent mobility |

## 7. 요약

- 전자구조는 group velocity와 carrier density를 주지만, 절대 mobility에는 산란으로 정해지는 비평형 분포가 추가로 필요하다.
- CRTA는 $\sigma/\tau$를 빠르게 비교하는 방법이며, 임의의 $\tau$ 없이 절대 mobility를 예측하지 않는다.
- 이상 결정의 phonon-limited mobility는 보통 DFPT로 mode-resolved EPC를 구하고, dense $k/q$ grid에서 SERTA 또는 iterative BTE를 풀어 계산한다.
- 반복 BTE는 scattering-in과 방향 재분포를 유지하므로 단일-particle lifetime과 전류를 이완시키는 transport lifetime의 차이를 다룬다.
- Mean free path는 $\mathbf v\tau$ 또는 반복 BTE의 mean free displacement에서 유도된다. 유한 소자에서는 $L/\Lambda$가 diffusive, quasi-ballistic과 ballistic 영역을 나누며, 이때 bulk mobility만으로 conductance를 정할 수 없는 경우가 생긴다.
- 계산값을 실험과 비교할 때는 drift/Hall 구분, 온도·농도·차원 정규화, 포함한 산란원과 전자구조·EPC 수렴 조건을 함께 보고해야 한다.

## 8. 참고문헌

1. S. Poncé, W. Li, S. Reichardt, and F. Giustino, "First-principles calculations of charge carrier mobility and conductivity in bulk semiconductors and two-dimensional materials," *Reports on Progress in Physics* **83**, 036501 (2020). [DOI](https://doi.org/10.1088/1361-6633/ab6a43), [arXiv](https://arxiv.org/abs/1908.01733)
2. S. Poncé, F. Macheda, E. R. Margine, N. Marzari, N. Bonini, and F. Giustino, "First-principles predictions of Hall and drift mobilities in semiconductors," *Physical Review Research* **3**, 043022 (2021). [DOI](https://doi.org/10.1103/PhysRevResearch.3.043022)
3. F. Giustino, "Electron-phonon interactions from first principles," *Reviews of Modern Physics* **89**, 015003 (2017). [DOI](https://doi.org/10.1103/RevModPhys.89.015003), [arXiv](https://arxiv.org/abs/1603.06965)
4. J.-J. Zhou, J. Park, I.-T. Lu, I. Maliyov, X. Tong, and M. Bernardi, "Perturbo: A software package for ab initio electron–phonon interactions, charge transport and ultrafast dynamics," *Computer Physics Communications* **264**, 107970 (2021). [DOI](https://doi.org/10.1016/j.cpc.2021.107970), [arXiv](https://arxiv.org/abs/2002.02045)
5. A. M. Ganose, J. Park, A. Faghaninia, R. Woods-Robinson, K. A. Persson, and A. Jain, "Efficient calculation of carrier scattering rates from first principles," *Nature Communications* **12**, 2222 (2021). [DOI](https://doi.org/10.1038/s41467-021-22440-5)
6. G. K. H. Madsen, J. Carrete, and M. J. Verstraete, "BoltzTraP2, a program for interpolating band structures and calculating semi-classical transport coefficients," *Computer Physics Communications* **231**, 140–145 (2018). [DOI](https://doi.org/10.1016/j.cpc.2018.05.010), [arXiv](https://arxiv.org/abs/1712.07946)
7. T.-H. Liu, J. Zhou, B. Liao, D. J. Singh, and G. Chen, "First-principles mode-by-mode analysis for electron-phonon scattering channels and mean free path spectra in GaAs," *Physical Review B* **95**, 075206 (2017). [DOI](https://doi.org/10.1103/PhysRevB.95.075206), [arXiv](https://arxiv.org/abs/1606.07074)
8. T. Gunst, T. Markussen, K. Stokbro, and M. Brandbyge, "First-principles method for electron-phonon coupling and electron mobility: Applications to two-dimensional materials," *Physical Review B* **93**, 035414 (2016). [DOI](https://doi.org/10.1103/PhysRevB.93.035414), [arXiv](https://arxiv.org/abs/1511.02045)
9. R. Claes, S. Poncé, G.-M. Rignanese, and G. Hautier, "Phonon-limited electronic transport through first principles," *Nature Reviews Physics* **7**, 73–90 (2025). [DOI](https://doi.org/10.1038/s42254-024-00795-0)
10. T. Markussen, M. Palsgaard, D. Stradi, T. Gunst, M. Brandbyge, and K. Stokbro, "Electron-phonon scattering from Green's function transport combined with molecular dynamics: Applications to mobility predictions," *Physical Review B* **95**, 245210 (2017). [DOI](https://doi.org/10.1103/PhysRevB.95.245210), [arXiv](https://arxiv.org/abs/1701.02883)
