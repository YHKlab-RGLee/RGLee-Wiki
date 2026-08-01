---
title: "(2) Point Defects: Charged Defect Formation Energy"
description: charged defect formation energy의 열역학적 정의, charge-transition level, finite-size correction과 농도 계산을 설명
status: verified
last_verified: 2026-08-01
---

# (2) Point Defects: Charged Defect Formation Energy

Charged defect formation energy는 결정이 원자와 전자를 외부 reservoir와 교환하여 전하 상태 $q$의 point defect $D^q$를 만들 때의 열역학적 비용이다. 이 값은 atomic chemical potential과 Fermi level에 따라 달라지며, 서로 다른 전하 상태의 안정성, thermodynamic charge-transition level과 dilute-limit equilibrium concentration을 연결한다.[1,2]

주기적 supercell 계산에서는 charged defect, 그 주기적 image와 neutralizing background 사이에 인공적인 electrostatic interaction이 생긴다. 따라서 정정하지 않은 total-energy difference만으로 formation energy를 정의할 수 없으며, 선택한 부호·energy reference와 finite-size correction을 함께 명시해야 한다.[1,3]

## 1. Grand-Canonical Formation Energy

### (1) 부호와 기준

이 글에서는 완전 결정에 원자종 $i$를 **추가**하면 $n_i>0$, 제거하면 $n_i<0$로 둔다. 결함이 전자를 잃으면 $q>0$, 전자를 얻으면 $q<0$이다. Electron Fermi level $E_F$는 완전 결정의 valence-band maximum (VBM)을 0으로 두고 측정한다.

이 규약에서 formation energy는

$$
\Delta E_f(D^q;E_F,\{\mu_i\})
=E_{\mathrm{tot}}(D^q)
-E_{\mathrm{tot}}(\mathrm{bulk})
-\sum_i n_i\mu_i
+q\left(E_{\mathrm{VBM}}+E_F\right)
+E_{\mathrm{corr}}^q
$$

이다.[1,2] 각 항의 역할은 다음과 같다.

| 항 | 의미 |
| --- | --- |
| $E_{\mathrm{tot}}(D^q)$ | 전하 상태 $q$로 완화한 결함 supercell의 총에너지 |
| $E_{\mathrm{tot}}(\mathrm{bulk})$ | 같은 계산 조건을 쓴 완전 결정 supercell의 총에너지 |
| $-\sum_i n_i\mu_i$ | atomic reservoir와 주고받은 원자의 에너지 |
| $q(E_{\mathrm{VBM}}+E_F)$ | electron reservoir와 전자를 교환한 에너지 |
| $E_{\mathrm{corr}}^q$ | 주기적 전하 계산의 finite-size correction |

$E_{\mathrm{VBM}}$은 계산의 absolute vacuum level이 아니라 완전 결정 계산에서 Fermi energy reference를 연결하는 항이다. $E_F$는 보통 계산된 band gap 안에서 주사하지만, 실제 평형값은 charge-neutrality condition으로 결정해야 한다.[1,2]

!!! warning "[Interpretation Caveat]"
    문헌은 $n_i$의 부호를 반대로 정의하기도 한다. 이 경우 chemical-potential term의 부호도 함께 바뀐다. 또한 Freysoldt–Neugebauer–Van de Walle (FNV) 계열 correction에서 far-field potential alignment는 $E_{\mathrm{corr}}^q$의 일부이다. $q\Delta V$를 별도 항으로 더하면서 같은 alignment를 correction에 다시 포함하면 이중 계산이 된다.[1,3]

### (2) Atomic Chemical Potential

$\mu_i$는 결함 형성 과정에서 원자가 출입하는 reservoir의 chemical potential이다. 화합물 $A_xB_y$가 모상과 평형이면

$$
x\mu_A+y\mu_B
=\mu_{A_xB_y}^{\mathrm{bulk}}
$$

를 만족한다. 동시에 원소상이나 경쟁 화합물이 석출하지 않도록 각 상에 대한 부등식도 만족해야 한다. 예를 들어 원소 기준 $\mu_i=\mu_i^0+\Delta\mu_i$를 쓰면 일반적으로 $\Delta\mu_i\le 0$이고, 경쟁상 $A_aB_b$에 대해

$$
a\mu_A+b\mu_B
\le \mu_{A_aB_b}^{\mathrm{bulk}}
$$

가 요구된다.[1,2] 따라서 “A-rich”와 “A-poor”는 임의의 숫자가 아니라 상안정성 영역의 경계 조건이다.

총에너지를 0 K 값으로 쓸지, 진동·기체·압력 기여를 포함한 유한 온도 자유에너지를 쓸지도 구분해야 한다. 특히 기체 저장고가 들어가면 온도와 분압이 $\mu_i$에 직접 영향을 준다.[1,2]

## 2. Fermi Level과 Charge Transition

### (1) Formation-Energy Line의 기울기

Atomic chemical potential을 고정하면

$$
\frac{\partial \Delta E_f(D^q)}{\partial E_F}=q
$$

이므로 formation energy–$E_F$ 선의 기울기는 전하 상태이다. $q>0$인 결함은 $E_F$가 올라갈수록 불리해지고, $q<0$인 결함은 유리해진다. 각 $E_F$에서 가장 낮은 선이 열역학적으로 안정한 전하 상태를 정한다.[1,2]

두 전하 상태 $q$와 $q'$의 formation energy가 같아지는 thermodynamic charge-transition level은

$$
\epsilon(q/q')
=
\frac{
\Delta E_f(D^q;E_F=0)
-\Delta E_f(D^{q'};E_F=0)
}{
q'-q
}
$$

로 정의한다.[1,2] 같은 결함 조성과 같은 chemical potential을 비교하므로 atomic-reservoir term은 상쇄된다. 반면 두 전하 상태의 structural relaxation과 charge correction은 서로 다를 수 있다. 따라서 각 상태를 일관된 조건에서 계산해야 한다.

### (2) Thermodynamic Level과 Optical Level

위 식은 각 전하 상태를 그 상태의 평형 구조까지 완화한 뒤 비교하는 thermodynamic level이다. 원자핵이 움직이지 않는 vertical transition을 나타내는 optical ionization energy와 같지 않다. 두 값을 구분하지 않으면 lattice-relaxation energy를 전자 준위 위치로 잘못 해석할 수 있다.[1,2]

안정한 전하 상태를 건너뛰는 negative-$U$ 거동이 있으면 인접 정수 전하 사이의 모든 교차점이 안정 구간을 갖지 않는다. 이 경우에도 formation-energy lower envelope를 기준으로 실제 전이 쌍을 판정해야 한다.[1,2]

## 3. Finite-Size Correction for Periodic Charges

### (1) 인공 상호작용의 기원

3차원 주기 경계에서 순전하를 갖는 cell의 Coulomb 에너지는 그대로는 발산한다. 평면파 전자구조 코드는 보통 균일한 중화 배경을 도입해 계산을 유한하게 만들지만, 그 결과는 고립 결함이 아니라 결함의 주기 배열과 배경 전하가 만드는 에너지를 포함한다.[1,3]

국소화된 전하와 충분히 큰 3차원 supercell에서는 가장 큰 image-charge 오차가 대략 $q^2/(\epsilon L)$로 감소한다. Makov–Payne 전개는 입방 셀, 등방 유전 응답과 국소화된 전하 분포를 기준으로 이 항과 고차 다중극 항을 전개한다.[1,4] 비입방 셀, 이방성 유전체와 복잡한 결함 전하에서는 이 단순식의 가정이 약해진다.[3,5]

### (2) FNV와 eFNV

FNV 방법은 결함 계산과 완전 결정 계산의 long-range potential difference를 유전 매질 안의 model-charge potential과 비교한다. 모형의 주기적 self-energy를 고립 한계로 바꾸는 image-charge 항과, model potential을 제거한 뒤 남는 far-field constant difference를 함께 정정한다.[1,3]

원래 FNV 구현은 planar-averaged potential과 isotropic dielectric constant를 사용한다. 따라서 원자 위치에서 potential fluctuation이 크거나 dielectric response가 anisotropic인 계에서는 plateau를 판정하기 어렵다. Extended FNV (eFNV)는 원자 위치의 potential을 표본으로 사용하고 dielectric tensor를 포함해 이러한 경우를 다룬다.[3,5]

정정의 개념적 형태는

$$
E_{\mathrm{corr}}^q
=E_{\mathrm{iso}}^{\mathrm{model}}
-E_{\mathrm{per}}^{\mathrm{model}}
-q\,\Delta V_{\mathrm{far}}
$$

로 나타낼 수 있다. 다만 $\Delta V_{\mathrm{far}}$의 부호는 코드가 정의하는 “결함–완전 결정” potential difference와 model potential의 부호에 따라 달라진다. 실제 계산에서는 사용한 구현의 정의를 따라야 하며, 식의 일부만 다른 규약에서 가져오면 안 된다.[1,3,5]

!!! info "[Measurement]"
    전하 정정을 적용할 때에는 다음 자료를 함께 남긴다.

    1. supercell 형상·부피와 결함 사이 최소 거리
    2. 전하 상태, 유전 상수 또는 유전 텐서와 그 계산 조건
    3. model charge, sampled potential과 far-field region의 선택
    4. correction을 적용하기 전의 formation energy, $E_{\mathrm{corr}}^q$와 적용 후 값
    5. 적어도 두 supercell 크기에서의 잔여 크기 의존성

    구조를 완화한 정적 전하 상태에는 전자와 이온 응답을 포함한 정적 유전 응답이 보통 대응하고, 고정 이온 수직 과정에는 전자 유전 응답이 대응한다. 어떤 응답을 썼는지 명시해야 한다.[3,5]

### (3) 적용 가능성 판정

Correction이 크다고 해서 결과를 자동으로 신뢰할 수 있는 것은 아니다. Defect-induced charge가 cell boundary까지 퍼지거나 host band state와 강하게 섞이면 localized model charge라는 전제가 무너진다. Far-field potential residual이 일정해지는지, defect state와 charge density가 국소화되는지, correction 후 size convergence가 개선되는지를 함께 확인해야 한다.[1,3,5]

2차원 물질, slab와 계면은 진공 방향의 주기 상호작용과 경계 조건이 3차원 bulk와 다르다. 이 글의 3차원 bulk FNV/eFNV 절차를 그대로 적용할 수 없다.

## 4. Equilibrium Concentration과 Charge Neutrality

### (1) Dilute-Limit Concentration

결함들이 서로 독립적인 희석 한계에서 전하 상태 $q$의 평형 농도는

$$
c(D^q)
=N_{\mathrm{site}}\,g_q
\exp\left[
-\frac{\Delta G_f(D^q;E_F,T)}{k_BT}
\right]
$$

로 쓸 수 있다.[1,2] $N_{\mathrm{site}}$는 단위 부피당 가능한 site 수, $g_q$는 배향·스핀 등의 축퇴도, $\Delta G_f$는 유한 온도 형성 자유에너지이다. 0 K DFT의 $\Delta E_f$를 $\Delta G_f$ 대신 쓰면 진동 엔트로피와 저장고의 유한 온도 기여를 생략한 근사임을 밝혀야 한다.

$E_F$는 외부에서 임의로 정한 값이 아니라 자유 운반자, 이온화 도펀트와 모든 charged defect를 포함하는 charge-neutrality equation

$$
p(E_F,T)-n(E_F,T)
+\sum_{D,q}q\,c(D^q)
+N_D^+(E_F,T)-N_A^-(E_F,T)
=0
$$

을 풀어 정한다.[1,2] Formation energy와 농도가 $E_F$에 의존하므로 이 식은 nonlinear self-consistent problem이다.

### (2) Formation Temperature와 Measurement Temperature

고온 성장 중에는 결함의 총수가 평형에 가까울 수 있지만 냉각 중 확산이 멈추면 결함 종의 총농도는 동결될 수 있다. 이후 전하 상태만 측정 온도에서 다시 평형화될 수도 있다. 따라서 formation energy로 계산한 농도는 열적 이력, migration barrier와 평형 가정을 밝히지 않으면 실제 시료 농도와 동일시할 수 없다.[1,2]

## 5. 계산 절차와 불확실성

1. 완전 결정의 구조, 띠 가장자리와 유전 응답을 동일한 전자구조 설정에서 수렴시킨다.
2. Chemical potential의 phase-stability region을 competing phase와 함께 정한다.
3. 결함별로 여러 전하 상태와 대칭이 깨진 초기 구조를 탐색해 국소 최저점을 찾는다.
4. 각 전하 상태에 일관된 electrostatic correction을 적용하고 potential residual과 charge localization을 확인한다.
5. Supercell 크기, $k$-점, plane-wave cutoff 또는 local basis에 대한 formation energy와 transition level의 수렴을 검사한다.
6. Formation-energy line의 lower envelope와 $\epsilon(q/q')$를 구한 뒤, 필요하면 charge-neutrality equation을 풀어 농도를 계산한다.

!!! warning "[Interpretation Caveat]"
    띠간격을 과소평가하는 exchange–correlation 근사는 가능한 $E_F$ 구간과 결함–band 혼성을 왜곡할 수 있다. 단순히 실험 띠간격에 맞추어 conduction-band minimum만 이동하는 보정은 결함 상태의 성격과 band-edge alignment를 자동으로 고치지 않는다. 선택한 functional에서 띠 가장자리와 결함 상태가 어떻게 변하는지 별도로 검증해야 한다.[1,2]

정량 결과는 functional, pseudopotential, spin과 spin–orbit coupling 처리, supercell, $k$-점, charge-correction method, dielectric response, chemical potential과 atomic-relaxation criterion에 모두 영향을 받는다. Corrected formation energy 값 하나만으로는 이러한 불확실성이 어디에서 생겼는지 재현할 수 없다.

## 6. 요약

1. Formation energy에는 atomic reservoir 및 electron reservoir와의 에너지 교환과 electrostatic finite-size correction이 포함된다. 따라서 grand-canonical quantity이다.
2. Formation energy–$E_F$ 선의 기울기는 $q$이며, 교차점은 완화된 전하 상태 사이의 thermodynamic charge-transition level을 정한다.
3. FNV/eFNV는 image-charge energy와 far-field potential alignment를 하나의 일관된 correction 안에서 다룬다.
4. Correction의 신뢰성은 charge localization, far-field potential residual과 supercell size convergence로 판단해야 한다.
5. Equilibrium concentration은 formation free energy뿐 아니라 charge neutrality, 온도와 열적 이력에 의존한다.

## 7. 참고문헌

1. C. Freysoldt, B. Grabowski, T. Hickel, J. Neugebauer, G. Kresse, A. Janotti, and C. G. Van de Walle, "First-principles calculations for point defects in solids," *Reviews of Modern Physics* **86**, 253–305 (2014). [DOI](https://doi.org/10.1103/RevModPhys.86.253).
2. C. G. Van de Walle and J. Neugebauer, "First-principles calculations for defects and impurities: Applications to III-nitrides," *Journal of Applied Physics* **95**, 3851–3879 (2004). [DOI](https://doi.org/10.1063/1.1682673).
3. C. Freysoldt, J. Neugebauer, and C. G. Van de Walle, "Fully ab initio finite-size corrections for charged-defect supercell calculations," *Physical Review Letters* **102**, 016402 (2009). [DOI](https://doi.org/10.1103/PhysRevLett.102.016402).
4. G. Makov and M. C. Payne, "Periodic boundary conditions in ab initio calculations," *Physical Review B* **51**, 4014–4022 (1995). [DOI](https://doi.org/10.1103/PhysRevB.51.4014).
5. Y. Kumagai and F. Oba, "Electrostatics-based finite-size corrections for first-principles point defect calculations," *Physical Review B* **89**, 195205 (2014). [DOI](https://doi.org/10.1103/PhysRevB.89.195205).
