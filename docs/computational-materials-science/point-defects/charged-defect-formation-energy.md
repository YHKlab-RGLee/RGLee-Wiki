---
description: charged defect formation energy의 열역학적 정의, charge-transition level, finite-size correction과 농도 계산을 설명
---

# Point defects: Charged defect formation energy

Charged defect formation energy는 결정이 원자와 전자를 외부 reservoir와 교환하여 전하 상태 $q$의 point defect $D^q$를 만들 때의 열역학적 비용이다. 이 값은 atomic chemical potential과 Fermi level에 따라 달라지며, 서로 다른 전하 상태의 안정성, thermodynamic charge-transition level과 dilute-limit equilibrium concentration을 연결한다.[1,2]

주기적 supercell 계산에서는 charged defect, 그 주기적 image와 neutralizing background 사이에 인공적인 electrostatic interaction이 생긴다. 따라서 정정하지 않은 total-energy difference만으로 formation energy를 정의할 수 없으며, 선택한 부호·energy reference와 finite-size correction을 함께 명시해야 한다.[1,3]

## 1. Charged defect formation energy의 주 방정식

### (1) 주 방정식과 grand-canonical 의미

0 K supercell 총에너지를 사용하는 근사에서 charged defect formation energy의 주 방정식은

$$
\Delta E_f(D^q;E_F,\{\mu_i\})
=E_{\mathrm{tot}}(D^q)
-E_{\mathrm{tot}}(\mathrm{bulk})
-\sum_i n_i\mu_i
+q\left(E_{\mathrm{VBM}}+E_F\right)
+E_{\mathrm{corr}}^q
$$

이다.[1,2] 이 식은 완전 결정에서 결함 구조를 만드는 내부 에너지 변화뿐 아니라, 그 과정에서 원자 reservoir 및 electron reservoir와 교환한 에너지와 주기적 supercell의 인공 상호작용을 함께 센다. 따라서 $\Delta E_f$는 결함 supercell의 total-energy difference 하나가 아니라 grand-canonical quantity이다.[1,2]

각 항의 물리적 의미는 다음과 같다.

| 항 | 의미 |
| --- | --- |
| $E_{\mathrm{tot}}(D^q)$ | 전하 상태 $q$로 완화한 결함 supercell의 총에너지 |
| $E_{\mathrm{tot}}(\mathrm{bulk})$ | 같은 계산 조건을 쓴 완전 결정 supercell의 총에너지 |
| $-\sum_i n_i\mu_i$ | atomic reservoir와 주고받은 원자의 에너지 |
| $q(E_{\mathrm{VBM}}+E_F)$ | electron reservoir와 전자를 교환한 에너지 |
| $E_{\mathrm{corr}}^q$ | 주기적 전하 계산의 finite-size correction |

첫 두 항은 같은 계산 조건에서 얻은 결함 cell과 완전 결정 cell의 내부 에너지 차이이다. $-\sum_i n_i\mu_i$는 원자 조성이 바뀌는 비용, $q(E_{\mathrm{VBM}}+E_F)$는 전하 상태를 만들기 위해 전자를 주고받는 비용, $E_{\mathrm{corr}}^q$는 유한한 주기 cell을 고립 결함 한계에 연결하는 보정이다. 뒤의 세 항은 각각 2절의 atomic chemical potential, 3절의 Fermi level, 4절의 finite-size correction에서 확장한다.

실제 결과를 비교할 때에는 주 방정식의 항을 한 숫자로 합치기 전에 다음처럼 출처와 수렴 조건을 분리해 기록한다.[1,2,7]

| 입력 항 | 같은 기준으로 고정할 조건 | 별도로 검사할 변화량 |
| --- | --- | --- |
| $E_{\mathrm{tot}}(D^q)-E_{\mathrm{tot}}(\mathrm{bulk})$ | functional, pseudopotential, cutoff, $k$-점과 spin 설정 | 구조의 국소 최저점과 supercell 크기 |
| $-\sum_i n_i\mu_i$ | 원소상·host·competing phase의 에너지 기준 | chemical-potential 꼭짓점과 온도·압력 |
| $q(E_{\mathrm{VBM}}+E_F)$ | bulk VBM과 전하 부호 규약 | band-edge 오차와 charge-neutrality 해 |
| $E_{\mathrm{corr}}^q$ | model charge, dielectric response와 potential 규약 | far-field 잔차와 cell 크기·형상 |

### (2) 부호와 에너지 기준

이 글에서는 완전 결정에 원자종 $i$를 **추가**하면 $n_i>0$, 제거하면 $n_i<0$로 둔다. 결함이 전자를 잃으면 $q>0$, 전자를 얻으면 $q<0$이다. 따라서 원자를 추가할 때 reservoir에서 가져온 에너지 $n_i\mu_i$를 빼고, 전자를 $q$개 잃어 electron reservoir로 보낼 때 $q(E_{\mathrm{VBM}}+E_F)$를 더한다.[1,2]

Electron Fermi level $E_F$는 완전 결정의 valence-band maximum (VBM)을 0으로 두고 측정한다. $E_{\mathrm{VBM}}$은 absolute vacuum level이 아니라 계산된 완전 결정의 VBM을 electron chemical potential의 기준으로 사용하는 항이다. $E_F$는 보통 계산된 band gap 안에서 주사하지만, 실제 평형값은 charge-neutrality condition으로 결정해야 한다.[1,2]

!!! warning "[Interpretation Caveat]"
    문헌은 $n_i$의 부호를 반대로 정의하기도 한다. 이 경우 chemical-potential term의 부호도 함께 바뀐다. 또한 Freysoldt–Neugebauer–Van de Walle (FNV) 계열 correction에서 far-field potential alignment는 $E_{\mathrm{corr}}^q$의 일부이다. $q\Delta V$를 별도 항으로 더하면서 같은 alignment를 correction에 다시 포함하면 이중 계산이 된다.[1,3]

## 2. Atomic chemical potential과 상안정성

### (1) Host 평형과 competing-phase 부등식

$\mu_i$는 결함 형성 과정에서 원자가 출입하는 reservoir의 chemical potential이다. 원소 기준을 $\mu_i=\mu_i^0+\Delta\mu_i$로 분리하면, 원소상이 석출하지 않는 조건은 일반적으로 $\Delta\mu_i\le 0$이다. $N$성분 host $H$의 화학량론 계수를 $h_i$라 할 때 host와 reservoir의 평형 조건은

$$
\sum_i h_i\Delta\mu_i
=\Delta H_f(H)
$$

로 쓸 수 있다. 여기서 $\Delta H_f(H)$는 같은 원소 기준으로 계산한 host의 formation enthalpy이다. 반면 화학량론 계수가 $p_i$인 competing phase $P$가 석출하지 않으려면

$$
\sum_i p_i\Delta\mu_i
\le \Delta H_f(P)
$$

를 만족해야 한다. 이 부등식을 위반하면 선택한 chemical potential에서 host만 유지하는 것보다 $P$를 형성하는 편이 열역학적으로 유리하다. 따라서 competing phase는 부수적인 수치 보정이 아니라 **host가 존재할 수 있는 chemical potential의 허용 범위 자체를 정의하는 상**이다.[1,2,6]

### (2) 상안정성 영역과 경계

Host 평형식은 $N$개의 $\Delta\mu_i$ 가운데 하나를 종속 변수로 만들고, 각 competing phase는 남은 공간을 자르는 하나의 반공간을 만든다. 모든 부등식의 교집합이 host의 chemical-potential stability region이다. 이 영역은 이성분계에서는 선분, 삼성분계에서는 다각형, 더 많은 성분에서는 고차원 convex polytope가 된다.[1,6,9]

모든 후보상이 최종 경계를 직접 결정하는 것은 아니다. 어떤 부등식은 다른 부등식보다 느슨하여 허용 영역을 실제로 자르지 않는다. 반대로 경계를 이루는 **bordering phase**는 host와 공존할 수 있는 limiting phase이며, 그 경계가 빠지면 허용되지 않는 chemical potential까지 안정한 조건으로 잘못 포함된다. 꼭짓점은 host와 여러 limiting phase가 동시에 평형인 극한 조건이다.[6–9]

모든 competing-phase 부등식을 행렬 $A$와 벡터 $\mathbf b$로 모으면 허용 영역 $\mathcal P$를

$$
\mathcal P
=
\left\{
\Delta\boldsymbol\mu:
A\Delta\boldsymbol\mu\le\mathbf b,
\ \mathbf h^{\mathsf T}\Delta\boldsymbol\mu=\Delta H_f(H),
\ \Delta\boldsymbol\mu\le0
\right\}
$$

로 쓸 수 있다. 각 행은 한 competing phase 또는 원소 석출 조건이고, host 평형식은 equality constraint이다. 이 표현은 후보상을 단순 목록으로 보는 대신 어떤 부등식이 실제 경계를 이루는지 계산하게 한다.[1,6–9]

따라서 “A-rich”와 “A-poor”는 원소 기준값을 임의로 선택한 조건이 아니라, 상안정성 영역 안에서 $\Delta\mu_A$가 각각 최대와 최소가 되는 경계 또는 꼭짓점이다. 다성분계에서는 같은 A-rich 경계 위에서도 다른 원소의 chemical potential이 달라질 수 있으므로, 결과를 보고할 때에는 A-rich라는 이름만 쓰지 않고 전체 $\{\Delta\mu_i\}$ 벡터와 limiting phase를 함께 제시해야 한다.[1,6–9]

원소 $X$의 rich·poor 한계는 각각

$$
\Delta\mu_X^{\mathrm{rich}}
=\max_{\Delta\boldsymbol\mu\in\mathcal P}\Delta\mu_X,
\qquad
\Delta\mu_X^{\mathrm{poor}}
=\min_{\Delta\boldsymbol\mu\in\mathcal P}\Delta\mu_X
$$

라는 선형 최적화 문제이다. 최댓값이나 최솟값만 보고하지 않고 그 해에서 활성화된 limiting phase와 전체 $\Delta\boldsymbol\mu$를 함께 남겨야 다른 결함 조성에도 같은 성장 조건을 재현할 수 있다.[6–9]

Chemical potential을 바꾸면 결함 형성에너지의 원자 저장고 항은

$$
\delta E_f(D^q)
=-\sum_i n_i\delta\mu_i
$$

로 변한다. 여기서 $\delta\mu_i$는 성장 조건을 바꿀 때의 chemical potential 변화량이다. 조성이 다른 vacancy, interstitial과 antisite는 서로 다른 $n_i$를 가지므로 같은 성장 조건 변화에도 형성에너지가 서로 다르게 이동한다. 반면 같은 결함의 두 전하 상태 사이에서는 atomic-reservoir term이 상쇄되므로 thermodynamic charge-transition level 자체는 chemical potential에 의존하지 않는다. 그러나 결함 농도는 formation energy에 지수적으로 의존하므로 어떤 꼭짓점이나 내부 조건을 택했는지는 농도와 지배적인 보상 결함을 크게 바꿀 수 있다.[1,2,6]

### (3) `doped`를 사용한 실제 계산 절차

`doped`의 competing-phase workflow는 위 부등식에서 실제 경계를 만드는 상을 찾고, 그 상들의 일관된 DFT 에너지로 chemical-potential limits를 계산하는 절차이다. 개념적으로는 다음 순서로 읽을 수 있다.[7–9]

1. **후보상 수집:** `CompetingPhases`는 host의 chemical system에서 Materials Project 항목을 가져오고, host에 인접하거나 설정한 에너지 허용오차 안에서 인접상이 될 수 있는 구조를 후보로 고른다. Extrinsic dopant가 있으면 dopant–host 원소를 포함하는 추가 chemical system도 조사해야 한다.
2. **동일한 에너지 기준으로 재계산:** 데이터베이스 에너지를 defect formation energy 식에 그대로 섞지 않고, 선택한 host·원소상·competing phase를 호환되는 functional, pseudopotential, 원자가 구성과 수렴 기준으로 다시 계산한다. 후보 선별에는 데이터베이스를 사용할 수 있지만 최종 부등식에는 서로 일관된 에너지가 필요하다.
3. **경계와 꼭짓점 계산:** `CompetingPhasesAnalyzer`는 계산 결과를 읽어 host stability region의 꼭짓점별 $\{\Delta\mu_i\}$와 해당 limiting phase를 구한다. 이 결과가 `DefectThermodynamics`에서 성장 조건별 결함 형성에너지를 평가하는 chemical-potential 입력이 된다.
4. **Extrinsic limit 확인:** Dopant chemical potential의 상한은 순수 dopant 원소상보다 dopant-containing compound가 더 엄격하게 제한할 수 있다. 따라서 substitutional dopant 하나만 계산하고 dopant-containing competing phase를 누락하면 dopant solubility와 보상 결함 농도를 과대평가할 수 있다.[1,2,7,8]

`energy_above_hull`은 열역학적 상수가 아니라 데이터베이스 에너지의 오차와 누락 가능성을 고려하여 후보상을 얼마나 넓게 포함할지 정하는 선별 허용오차이다. `doped` 3.1.0 문서는 기본값을 0.05 eV/atom으로 제시하지만, 2024년 JOSS 논문은 당시 기본값을 0.1 eV/atom으로 기술한다. 따라서 재현 가능한 계산에서는 `doped` 버전, 실제 허용오차와 수동으로 추가·제외한 상을 기록해야 한다.[7,8]

!!! warning "[Interpretation Caveat]"
    Materials Project에 실험적으로 알려진 상이나 올바른 저에너지 polymorph가 없을 수 있고, database 수준의 상대 에너지 순서가 사용자가 선택한 DFT 설정에서 바뀔 수도 있다. 특히 transition metal, mixed oxidation state, van der Waals 결합과 큰 spin–orbit coupling이 있는 계에서는 후보 목록을 문헌과 실험 상자료로 교차확인한다. 또한 위 경계는 열역학적 평형 조건이다. 실제 성장에서는 핵생성과 확산의 kinetic barrier 때문에 metastable 조건이 나타날 수 있으므로, 계산된 상안정성 영역을 모든 합성 조건의 절대 경계로 해석하지 않는다.[1,2,8]

총에너지를 0 K 값으로 쓸지, 진동·기체·압력 기여를 포함한 유한 온도 자유에너지를 쓸지도 구분해야 한다. 특히 기체 저장고가 들어가면 온도와 분압이 $\mu_i$에 직접 영향을 준다.[1,2]

## 3. Fermi level과 charge transition

### (1) Formation-energy line의 기울기

Atomic chemical potential을 고정하면

$$
\frac{\partial \Delta E_f(D^q)}{\partial E_F}=q
$$

이므로 formation energy–$E_F$ 선의 기울기는 전하 상태이다. $q>0$인 결함은 $E_F$가 올라갈수록 불리해지고, $q<0$인 결함은 유리해진다. 각 $E_F$에서 가장 낮은 선이 열역학적으로 안정한 전하 상태를 정한다.[1,2]

예를 들어 $q=+1$인 선은 $E_F$가 증가할 때 기울기 $+1$로 올라가고, $q=-1$인 선은 기울기 $-1$로 내려간다. 두 선의 교차점은 두 전하 상태의 에너지가 같아지는 후보 지점이다. 실제 안정 전하 상태의 전이인지 판단하려면 다른 전하 상태까지 함께 비교해야 한다.[1,10]

주어진 $E_F$에서 실제 열역학적 상태는 계산한 모든 전하 상태의 lower envelope

$$
\Delta E_f^{\mathrm{stable}}(D;E_F)
=\min_q\Delta E_f(D^q;E_F)
$$

로 정한다. 따라서 교차점에서 두 선이 lower envelope 위에서 만나고, 그 양쪽에서 안정 전하 상태가 바뀌는지 확인해야 한다. 다른 전하 상태가 교차점보다 낮으면 그 교차는 안정한 charge-transition level이 아니다.[1,10]

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

### (2) Thermodynamic level과 optical level

위 식은 각 전하 상태를 그 상태의 평형 구조까지 완화한 뒤 비교하는 thermodynamic level이다. 원자핵이 움직이지 않는 vertical transition을 나타내는 optical ionization energy와 같지 않다. 두 값을 구분하지 않으면 lattice-relaxation energy를 전자 준위 위치로 잘못 해석할 수 있다.[1,2]

안정한 전하 상태를 건너뛰는 negative-$U$ 거동이 있으면 인접 정수 전하 사이의 모든 교차점이 안정 구간을 갖지 않는다. 이 경우에도 formation-energy lower envelope를 기준으로 실제 전이 쌍을 판정해야 한다.[1,2]

같은 $E_F$와 chemical potential에서 중간 전하 상태 $q$의 유효 상호작용을

$$
U_{\mathrm{eff}}(q)
=
\Delta E_f(D^{q+1})
+\Delta E_f(D^{q-1})
-2\Delta E_f(D^q)
$$

로 정의하면 $U_{\mathrm{eff}}<0$일 때 동일한 $q$ 상태 결함 두 개보다 $q+1$ 상태와 $q-1$ 상태 결함 하나씩의 조합이 에너지상 유리하다. 즉 총전하 $2q$를 보존하는 $2D^q\rightarrow D^{q+1}+D^{q-1}$의 에너지 차이가 위 식이다. 이는 희석 한계에서 서로 떨어진 결함들의 전하 재분배를 비교하며, 결함들이 결합한 complex의 에너지를 뜻하지 않는다.[1,10] 이 판정에는 각 전하 상태의 완화 구조와 correction이 모두 들어가며, 계산하지 않은 중간 상태를 임의로 제외해서는 안 된다.[1,2,7]

### (3) Lower envelope의 계산 예제

교차점과 안정한 전이의 차이를 보기 위해 동일한 결함 조성에 대해 다음 세 형성 에너지를 가정하자. $E_F$와 에너지는 eV 단위이며, $0\le E_F\le2\,\mathrm{eV}$인 가상의 gap을 고려한다. 절편은 각 상태의 구조 완화와 correction까지 반영한 모형 입력이다. 특정 물질에서 계산하거나 측정한 값은 아니다.

| 전하 상태 | $\Delta E_f(E_F)$ | $E_F=1\,\mathrm{eV}$에서의 값 |
| --- | --- | --- |
| $+1$ | $1\,\mathrm{eV}+E_F$ | $2\,\mathrm{eV}$ |
| $0$ | $2.2\,\mathrm{eV}$ | $2.2\,\mathrm{eV}$ |
| $-1$ | $3\,\mathrm{eV}-E_F$ | $2\,\mathrm{eV}$ |

앞의 전이 준위 식을 각 쌍에 적용하면

$$
\epsilon(+/0)=1.2\,\mathrm{eV},\qquad
\epsilon(0/-)=0.8\,\mathrm{eV},\qquad
\epsilon(+/-)=1.0\,\mathrm{eV}
$$

이다. $+/0$ 교차점에서는 음전하 상태가 더 낮고, $0/-$ 교차점에서는 양전하 상태가 더 낮다. 따라서 실제 lower envelope는 $E_F<1\,\mathrm{eV}$에서 $+1$, 그보다 위에서 $-1$이며, 중성 상태가 가장 낮아지는 구간은 없다. 세 교차점을 모두 안정한 전이 준위로 표기하면 이 결론을 놓친다. 이는 앞의 최소화 정의를 모형 입력에 직접 적용한 예제이다.[1,10]

같은 입력으로 계산한 유효 상호작용은

$$
U_{\mathrm{eff}}(0)
=(1+3-2\times2.2)\,\mathrm{eV}
=-0.4\,\mathrm{eV}
$$

이다. $E_F$ 항은 $+E_F-E_F=0$으로 상쇄된다. 중성 결함 두 개가 서로 떨어진 양·음전하 결함으로 전하를 재분배하면 총전하를 바꾸지 않으면서 이 모형에서는 에너지가 낮아진다는 뜻이다. 이 열역학적 비교는 전이 속도나 장벽이 없다는 뜻은 아니며, 광학 전이 에너지를 정하지도 않는다.[1,10]

중성 상태가 lower envelope에 없다는 사실은 유한 온도의 점유 확률이 항상 정확히 0이라는 뜻도 아니다. 동일한 축퇴도를 가정하고 진동 등의 자유에너지 차이를 생략한 채 $E_F=1\,\mathrm{eV}$에 두자. $k_B$를 Boltzmann 상수, $T$를 절대온도, $w_q$를 전하 상태 $q$의 정규화 전 Boltzmann weight라 하면 그 비는

$$
\frac{w_0}{w_+}=\frac{w_0}{w_-}
=\exp\!\left[-\frac{0.2\,\mathrm{eV}}{k_BT}\right]
$$

이다. 따라서 낮은 온도에서 중성 상태가 억제되는 정도와, 안정한 0 K 전하 상태를 고르는 판정은 구별해야 한다. 이 비는 동일 결함 종의 상대 점유만 정한다. 총 결함 농도를 얻으려면 형성 자유에너지와 site 수를 사용하거나, 동결된 종별 총농도를 별도로 지정해야 한다.[1,10]

## 4. Periodic charge의 finite-size correction

### (1) 인공 상호작용의 기원

3차원 주기 경계에서 순전하를 갖는 cell의 Coulomb 에너지는 그대로는 발산한다. 평면파 전자구조 코드는 보통 균일한 중화 배경을 도입해 계산을 유한하게 만들지만, 그 결과는 고립 결함이 아니라 결함의 주기 배열과 배경 전하가 만드는 에너지를 포함한다.[1,3]

국소화된 전하와 충분히 큰 3차원 supercell에서는 가장 큰 image-charge 오차가 대략 $q^2/(\epsilon L)$로 감소한다. Makov–Payne 전개는 입방 셀, 등방 유전 응답과 국소화된 전하 분포를 기준으로 이 항과 고차 다중극 항을 전개한다.[1,4] 비입방 셀, 이방성 유전체와 복잡한 결함 전하에서는 이 단순식의 가정이 약해진다.[3,5]

이 절의 Coulomb 식은 원자 단위계($e=\hbar=4\pi\epsilon_0=1$)를 사용한다. 따라서 정수 $q$는 기본 전하 단위의 전하량, 길이는 bohr, 에너지는 hartree이며 $\epsilon$은 무차원 상대 유전율이다. 입방 cell과 등방 유전 상수 $\epsilon$에 대한 leading point-charge correction은

$$
E_{\mathrm{PC}}
=\frac{q^2\alpha}{2\epsilon L}
$$

이다. $\alpha$는 위 양의 correction 식에 맞춘 Madelung constant의 양의 크기이고 $L$은 cell의 선형 크기이다. SI 길이와 에너지를 사용하려면 위 식에 $e^2/(4\pi\epsilon_0)$를 복원해야 한다. 이 식은 $L^{-1}$ 장거리 항만 정정하며, cell 형상과 유전 이방성을 평균값 하나로 축약하면 오차가 커질 수 있다.[4,5]

같은 입방·등방·국소 전하 조건에서 Makov–Payne 전개를 $L^{-3}$까지 쓰면

$$
E_{\mathrm{MP}}
=E_{\mathrm{PC}}
-\frac{2\pi qQ}{3\epsilon L^3}
+\frac{2\pi|\mathbf p|^2}{3\epsilon L^3}
+O(L^{-5})
$$

이다. $\mathbf p$와 $Q$는 defect-induced charge의 dipole moment와 second radial moment이다. 결정에서는 screening charge와 defect charge를 유일하게 분리하기 어려우므로 이 고차항을 무비판적으로 계산하기보다 FNV/eFNV residual과 여러 cell의 수렴으로 검사한다.[4,5]

### (2) FNV와 eFNV

FNV 방법은 결함 계산과 완전 결정 계산의 long-range potential difference를 유전 매질 안의 model-charge potential과 비교한다. 모형의 주기적 self-energy를 고립 한계로 바꾸는 image-charge 항과, model potential을 제거한 뒤 남는 far-field constant difference를 함께 정정한다.[1,3]

원래 FNV 구현은 planar-averaged potential과 isotropic dielectric constant를 사용한다. 따라서 원자 위치에서 potential fluctuation이 크거나 dielectric response가 anisotropic인 계에서는 plateau를 판정하기 어렵다. Extended FNV (eFNV)는 원자 위치의 potential을 표본으로 사용하고 dielectric tensor를 포함해 이러한 경우를 다룬다.[3,5]

부호를 고정하기 위해 $V$를 양의 시험 전하에 대한 electrostatic potential로 정의한다. 결함과 bulk의 차이에서 같은 전하 $q$의 주기적 model potential을 뺀 far-field 잔차를 $\Delta V_{\mathrm{far}}=[V_{\mathrm{defect}}-V_{\mathrm{bulk}}-V_{\mathrm{per}}^{\mathrm{model}}]_{\mathrm{far}}$로 둔다. 이 규약에서 정정은

$$
E_{\mathrm{corr}}^q
=E_{\mathrm{iso}}^{\mathrm{model}}
-E_{\mathrm{per}}^{\mathrm{model}}
-q\,\Delta V_{\mathrm{far}}
$$

로 나타낼 수 있다. 앞의 두 항은 동일한 model charge의 고립·주기 경계 조건 에너지 차이이다. 전자의 potential energy를 출력하는 코드는 위 electrostatic potential과 부호가 반대이므로, residual도 같은 규약으로 변환한 뒤 적용해야 한다. 원자 단위계에서는 $q\Delta V$가 에너지이며, potential을 volt로 읽어 SI 에너지로 계산할 때에는 정수 $q$에 기본 전하 $e$를 곱한다. Potential 기준과 model subtraction을 함께 맞추고 별도의 alignment를 중복해서 더하지 않는다.[1,3,5]

!!! info "[Measurement]"
    전하 정정을 적용할 때에는 다음 자료를 함께 남긴다.

    1. supercell 형상·부피와 결함 사이 최소 거리
    2. 전하 상태, 유전 상수 또는 유전 텐서와 그 계산 조건
    3. model charge, sampled potential과 far-field region의 선택
    4. correction을 적용하기 전의 formation energy, $E_{\mathrm{corr}}^q$와 적용 후 값
    5. 적어도 두 supercell 크기에서의 잔여 크기 의존성

    $N_{\mathrm{far}}$개 표본에서 model potential을 뺀 far-field 값이 $\Delta V_i$라면 plateau의 산포를

    $$
    \sigma_{\mathrm{far}}
    =
    \sqrt{
    \frac{1}{N_{\mathrm{far}}}
    \sum_{i=1}^{N_{\mathrm{far}}}
    \left(\Delta V_i-\overline{\Delta V}_{\mathrm{far}}\right)^2
    }
    $$

    로 기록할 수 있다. 작은 $\sigma_{\mathrm{far}}$는 표본 영역에서 plateau가 형성되었는지를 검사하지만, charge localization이나 크기 수렴을 대신하지 않는다.[3,5,7]

    가장 큰 cell $L_{\max}$을 내부 기준으로 삼으면 corrected formation energy의 잔여 크기 의존성은

    $$
    \delta_{\mathrm{size}}
    =
    \max_{L<L_{\max}}
    \left|
    \Delta E_f^{\mathrm{corr}}(L)
    -\Delta E_f^{\mathrm{corr}}(L_{\max})
    \right|
    $$

    로 비교할 수 있다. 허용 오차는 목표 transition level과 농도 민감도에 맞춰 미리 정하며, cell 크기뿐 아니라 형상도 바꾸어 correction의 이방성 민감도를 확인한다.[1,5,7]

    구조를 완화한 정적 전하 상태에는 전자와 이온 응답을 포함한 정적 유전 응답이 보통 대응하고, 고정 이온 수직 과정에는 전자 유전 응답이 대응한다. 어떤 응답을 썼는지 명시해야 한다.[3,5]

### (3) Correction 적용 범위

Correction이 크다고 해서 결과를 자동으로 신뢰할 수 있는 것은 아니다. Defect-induced charge가 cell boundary까지 퍼지거나 host band state와 강하게 섞이면 localized model charge라는 전제가 무너진다. Far-field potential residual이 일정해지는지, defect state와 charge density가 국소화되는지, correction 후 size convergence가 개선되는지를 함께 확인해야 한다.[1,3,5]

2차원 물질, slab와 계면은 진공 방향의 주기 상호작용과 경계 조건이 3차원 bulk와 다르다. 이 글의 3차원 bulk FNV/eFNV 절차를 그대로 적용할 수 없다.

## 5. Equilibrium concentration과 charge neutrality

### (1) Dilute-limit concentration

결함들이 서로 독립적인 희석 한계에서 전하 상태 $q$의 평형 농도는

$$
c(D^q)
=N_{\mathrm{site}}\,g_q
\exp\left[
-\frac{\Delta G_f(D^q;E_F,T)}{k_BT}
\right]
$$

로 쓸 수 있다.[1,2] $N_{\mathrm{site}}$는 단위 부피당 가능한 site 수, $g_q$는 배향·스핀 등의 축퇴도, $\Delta G_f$는 유한 온도에서 고립 결함 하나의 형성 자유에너지이며, 결함을 여러 site에 배치하는 configurational entropy는 위 농도 식을 얻는 과정에서 별도로 처리한다. 또한 앞에 곱한 $g_q$의 축퇴 엔트로피 $k_B\ln g_q$는 이 $\Delta G_f$에 다시 포함하지 않는다. 이를 이미 포함한 자유에너지를 사용한다면 해당 축퇴도 인자는 1로 두어야 한다.[1,10] 0 K DFT의 $\Delta E_f$를 $\Delta G_f$ 대신 쓰면 진동 엔트로피와 저장고의 유한 온도 기여를 생략한 근사임을 밝혀야 한다.

전기적으로 중성인 벌크의 평형 $E_F$를 구하려면 결함 전하뿐 아니라 자유 전자와 정공의 농도도 필요하다. 이들은 각각

$$
n(E_F,T)
=
\int_{E_C}^{\infty}
g(E)f(E;E_F,T)\,dE
$$

과

$$
p(E_F,T)
=
\int_{-\infty}^{E_V}
g(E)\left[1-f(E;E_F,T)\right]dE
$$

로 계산한다. 여기서 $g(E)$는 단위 부피·에너지당 band 상태 밀도, $f$는 Fermi–Dirac distribution이며 $E_C$, $E_V$는 conduction-band minimum과 valence-band maximum이다. 이 적분의 $E$, $E_C$, $E_V$도 $E_F$와 같은 VBM 기준으로 놓는다. Effective-density-of-states 식을 쓰는 경우에는 포물선 band와 nondegenerate carrier라는 추가 근사를 밝혀야 한다.[1,2]

자유 운반자와 결함 전하를 합한 charge-neutrality equation은

$$
p(E_F,T)-n(E_F,T)
+\sum_{D,q}q\,c(D^q)
+N_D^+(E_F,T)-N_A^-(E_F,T)
=0
$$

이다.[1,2] 여기서 $N_D^+$와 $N_A^-$는 $\sum_{D,q}$에서 제외하고 별도로 모형화한, 각각 한 번 이온화된 donor와 acceptor의 농도이다. 도펀트를 이미 $c(D^q)$에 포함했다면 그 도펀트의 별도 항은 넣지 않는다. 다중 전하를 갖는 도펀트는 $q\,c(D^q)$로 세어야 하며, 모든 결함과 불순물을 합에 포함하면 두 별도 항을 모두 생략한다. 이는 각 전하를 한 번만 합하는 조건이다.[1,11] Formation energy와 농도가 $E_F$에 의존하므로 이 식은 nonlinear self-consistent problem이다.

### (2) Formation temperature와 measurement temperature

고온 성장 중에는 결함의 총수가 평형에 가까울 수 있지만 냉각 중 확산이 멈추면 결함 종의 총농도는 동결될 수 있다. 이후 전하 상태만 측정 온도에서 다시 평형화될 수도 있다. 따라서 formation energy로 계산한 농도는 열적 이력, migration barrier와 평형 가정을 밝히지 않으면 실제 시료 농도와 동일시할 수 없다.[1,2]

결함 종 $D$의 구조적 농도가 형성 온도에서 동결된다고 가정하면

$$
C_D^{\mathrm{frozen}}
=
\sum_q
c(D^q;E_F^{\mathrm{form}},T_{\mathrm{form}})
$$

를 먼저 정한다. 측정 온도에서 전하 상태만 다시 평형화한다면 새 charge-neutrality 해를 구할 때에도

$$
\sum_q
c(D^q;E_F^{\mathrm{meas}},T_{\mathrm{meas}})
=C_D^{\mathrm{frozen}}
$$

라는 종별 보존 조건을 함께 적용한다. 이때 5절 (1)의 완전 평형 농도 식을 측정 온도에 그대로 대입하면 총수가 일반적으로 보존되지 않는다. 대신 전하 상태별 weight를 정규화하여

$$
w_q=g_q\exp\!\left[-\frac{\Delta G_f(D^q;E_F,T)}{k_BT}\right],
\qquad
c(D^q)=C_D^{\mathrm{frozen}}\frac{w_q}{\sum_{q'}w_{q'}}
$$

로 쓴다. 여기서 $E_F=E_F^{\mathrm{meas}}$, $T=T_{\mathrm{meas}}$이며, 동일 결함 종의 모든 전하 상태에 공통인 자유에너지 항은 비율에서 상쇄된다. 정규화된 점유 확률을 동결된 총수에 곱한 것이므로 종별 보존을 만족하면서 charge neutrality로 측정 온도의 $E_F$를 정할 수 있다.[1,10] 이 frozen-defect 모형은 구조 확산은 멈췄지만 전자 포획·방출은 충분히 빠르다는 시간척도 분리를 가정한다.[1,2,7]

## 6. 계산 절차와 불확실성

1. 완전 결정의 구조, 띠 가장자리와 유전 응답을 동일한 전자구조 설정에서 수렴시킨다.
2. Host와 원소상, intrinsic·extrinsic competing phase를 같은 에너지 기준으로 계산하고 chemical-potential stability region의 경계와 꼭짓점을 정한다.
3. 결함별로 여러 전하 상태와 대칭이 깨진 초기 구조를 탐색해 국소 최저점을 찾는다.
4. 각 전하 상태에 일관된 electrostatic correction을 적용하고 potential residual과 charge localization을 확인한다.
5. Supercell 크기, $k$-점, plane-wave cutoff 또는 local basis에 대한 formation energy와 transition level의 수렴을 검사한다.
6. Formation-energy line의 lower envelope와 $\epsilon(q/q')$를 구한 뒤, 필요하면 charge-neutrality equation을 풀어 농도를 계산한다.

!!! warning "[Interpretation Caveat]"
    띠간격을 과소평가하는 exchange–correlation 근사는 가능한 $E_F$ 구간과 결함–band 혼성을 왜곡할 수 있다. 단순히 실험 띠간격에 맞추어 conduction-band minimum만 이동하는 보정은 결함 상태의 성격과 band-edge alignment를 자동으로 고치지 않는다. 선택한 functional에서 띠 가장자리와 결함 상태가 어떻게 변하는지 별도로 검증해야 한다.[1,2]

정량 결과는 functional, pseudopotential, spin과 spin–orbit coupling 처리, supercell, $k$-점, charge-correction method, dielectric response, chemical potential과 atomic-relaxation criterion에 모두 영향을 받는다. Corrected formation energy 값 하나만으로는 이러한 불확실성이 어디에서 생겼는지 재현할 수 없다.

최종 결과에는 다음 오차원을 분리해 남긴다.[1,2,5,7]

| 오차원 | 직접 비교할 양 | 실패 시 해석 |
| --- | --- | --- |
| 전자구조 | functional·band edge·spin 설정에 따른 $\Delta E_f$와 $\epsilon(q/q')$ | 결함 준위와 host band의 상대 위치가 불확실함 |
| 유한 크기 | cell 크기·형상에 따른 $\delta_{\mathrm{size}}$와 $\sigma_{\mathrm{far}}$ | 고립 결함 한계와 correction 가정이 충분히 검증되지 않음 |
| 원자 구조 | 서로 다른 초기 왜곡에서 얻은 국소 최저점 | 더 낮은 metastable 또는 symmetry-broken 구조를 놓쳤을 수 있음 |
| 열역학 입력 | competing phase, $\Delta\boldsymbol\mu$, 온도·압력과 축퇴도 | 농도와 지배 결함의 성장 조건 의존성이 불확실함 |
| 통계 모형 | 완전 평형과 frozen-defect 결과의 차이 | 실제 열적 이력과 시간척도가 결론을 바꿀 수 있음 |

이 오차원들은 하나의 합성 오차 막대로 자동 결합되지 않는다. 예를 들어 작은 finite-size residual이 잘못된 band edge나 누락된 구조 최저점을 보상하지 못한다. 따라서 formation energy, transition level과 농도마다 지배적인 오차원을 따로 밝히고, 결론이 바뀌는 입력 범위를 함께 보고한다.

## 7. 요약

1. Formation energy에는 atomic reservoir 및 electron reservoir와의 에너지 교환과 electrostatic finite-size correction이 포함된다. 따라서 grand-canonical quantity이다.
2. Competing phase의 부등식은 host의 chemical-potential stability region을 정의한다. 성장 조건은 전체 chemical-potential 벡터와 limiting phase로 명시해야 한다.
3. Formation energy–$E_F$ 선의 기울기는 $q$이며, lower envelope에서 안정 전하 상태가 바뀌는 교차점이 thermodynamic charge-transition level을 정한다.
4. FNV/eFNV는 image-charge energy와 far-field potential alignment를 하나의 일관된 correction 안에서 다룬다.
5. Correction의 신뢰성은 charge localization, far-field potential residual과 supercell size convergence로 판단해야 한다.
6. Equilibrium concentration은 formation free energy뿐 아니라 charge neutrality, 온도와 열적 이력에 의존한다.

## 8. 참고문헌

1. C. Freysoldt, B. Grabowski, T. Hickel, J. Neugebauer, G. Kresse, A. Janotti, and C. G. Van de Walle, "First-principles calculations for point defects in solids," *Reviews of Modern Physics* **86**, 253–305 (2014). [DOI](https://doi.org/10.1103/RevModPhys.86.253).
2. C. G. Van de Walle and J. Neugebauer, "First-principles calculations for defects and impurities: Applications to III-nitrides," *Journal of Applied Physics* **95**, 3851–3879 (2004). [DOI](https://doi.org/10.1063/1.1682673).
3. C. Freysoldt, J. Neugebauer, and C. G. Van de Walle, "Fully ab initio finite-size corrections for charged-defect supercell calculations," *Physical Review Letters* **102**, 016402 (2009). [DOI](https://doi.org/10.1103/PhysRevLett.102.016402).
4. G. Makov and M. C. Payne, "Periodic boundary conditions in ab initio calculations," *Physical Review B* **51**, 4014–4022 (1995). [DOI](https://doi.org/10.1103/PhysRevB.51.4014).
5. Y. Kumagai and F. Oba, "Electrostatics-based finite-size corrections for first-principles point defect calculations," *Physical Review B* **89**, 195205 (2014). [DOI](https://doi.org/10.1103/PhysRevB.89.195205).
6. E. V. Malyi and A. Zunger, "Understanding Doping of Quantum Materials," *Chemical Reviews* **121**, 3031–3060 (2021). [DOI](https://doi.org/10.1021/acs.chemrev.0c00608).
7. S. R. Kavanagh, A. G. Squires, A. Nicolson, I. Mosquera-Lois, A. M. Ganose, B. Zhu, K. Brlec, A. Walsh, and D. O. Scanlon, "`doped`: Python toolkit for robust and repeatable charged defect supercell calculations," *Journal of Open Source Software* **9**, 6433 (2024). [DOI](https://doi.org/10.21105/joss.06433).
8. `doped` developers, "Competing Phases," `doped` 3.1.0 documentation. [Official documentation](https://doped.readthedocs.io/en/3.1.0/chemical_potentials_tutorial.html).
9. `pymatgen` developers, "ChemicalPotentialDiagram," `pymatgen` documentation. [Official documentation](https://pymatgen.org/pymatgen.analysis.html#pymatgen.analysis.chempot_diagram.ChemicalPotentialDiagram).

10. J. Coutinho, V. P. Markevich, and A. R. Peaker, "Characterisation of negative-U defects in semiconductors," *Journal of Physics: Condensed Matter* **32**, 323001 (2020). [DOI](https://doi.org/10.1088/1361-648X/ab8091).

11. `doped` developers, "Defect Thermodynamics & Doping," `doped` 3.1.0 documentation. [Official documentation](https://doped.readthedocs.io/en/3.1.0/thermodynamics_tutorial.html).
