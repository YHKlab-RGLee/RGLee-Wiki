---
description: MOS capacitor의 전하–표면전위 관계를 유도하고 pristine C–V와 결함의 정적 이동·주파수 분산·손실을 구분하여 정량적으로 해석한다.
---

# MOS capacitor

Metal–oxide–semiconductor (MOS) capacitor는 gate 전압을 산화막 전압과 반도체의 band bending으로 나누는 구조이다. 그 capacitance–voltage (C–V) 특성은 전하의 양뿐 아니라 **측정 시간 안에 어떤 전하가 변할 수 있는가**에 의해 결정된다. 따라서 결함을 해석하려면 먼저 결함이 없는 반도체의 전기정역학을 풀고, 그 위에 결함 전하와 유한한 응답 시간을 추가해야 한다.[1,2,3]

소자 동작의 전체 맥락은 [Overview](basic-operation.md)를 따른다. 이 문서는 균일하게 도핑된 평면 p-type Si를 기준으로 Poisson–Boltzmann 전하식, 저주파·고주파 C–V, interface trap과 border trap의 응답, 결함 밀도 추출의 성립 조건을 다룬다. 여기서 **pristine 기준**은 산화막·계면 결함 전하가 없는 계산 모형이다. 실제 실험에서 stress 이전 시료를 pristine이라고 부르더라도, 그 명칭만으로 초기 결함 밀도가 0이라는 뜻은 아니다. 후자의 비교에서는 절대 결함량과 stress에 의한 변화량을 구분한다.[3,4]

## 1. Gate 전압과 전하 분배

Gate 전압 $V_G$는 접지된 반도체 bulk에 대한 전압이며, 표면전위 $\psi_s$는 계면과 bulk 사이의 정전위 차이다. 산화막 두께를 $t_{ox}$, 절대 유전율을 $\varepsilon_{ox}$, 단위 면적당 산화막 capacitance를 $c_{ox}$라 하면, pristine 구조의 중심 관계는 다음과 같다.[1,2]

$$
c_{ox}=\frac{\varepsilon_{ox}}{t_{ox}},
\qquad
V_G=\phi_{ms}+\psi_s-\frac{Q_s(\psi_s)}{c_{ox}}.
$$

$\phi_{ms}=(\Phi_m-\Phi_s)/q$는 gate와 반도체의 work function 차이를 전압으로 나타낸 값이다. $\Phi_m,\Phi_s$는 에너지, $q>0$는 기본 전하량이며, $Q_s$는 반도체의 부호 있는 면전하이다. 산화막을 가로지르는 전압은 $V_{ox}=-Q_s/c_{ox}$이다. 전압은 gate에서 정의하고 전하는 반대쪽 반도체에서 세기 때문에 음의 부호가 필요하다. 결함이 없어도 $\phi_{ms}\ne0$이면 flat-band voltage는 0이 아니다.[1,2]

### (1) 좌표와 정규화

반도체 좌표 $x$는 계면 $x=0$에서 bulk 방향으로 증가하고, $\psi(\infty)=0$으로 둔다. 전기장 $\mathcal E=-d\psi/dx$와 반도체 절대 유전율 $\varepsilon_s$에 대해 $Q_s=-\varepsilon_s\mathcal E(0)$이다. $\psi_s>0$이면 반도체 표면의 전자 에너지 준위는 bulk보다 $q\psi_s$만큼 낮아진다. p-type에서는 정공이 줄고 전자가 증가하므로 depletion과 inversion 방향이다.[1,2,5]

이하의 정규화는 표 1과 같다. 특히 총 capacitance와 면적 정규화 capacitance를 섞으면 결함 밀도에 면적 인자가 중복되거나 빠진다.[3,4]

표 1. 전하·응답량의 표기와 단위.

| 기호 | 정의 | 단위 |
| --- | --- | --- |
| $A$ | 전기적으로 측정되는 gate 면적 | $\mathrm{m^2}$ |
| $Q_s,Q_{it},Q_f$ | 반도체·interface trap·고정 전하의 면밀도 | $\mathrm{C\,m^{-2}}$ |
| $c=C/A$ | 단위 면적당 capacitance | $\mathrm{F\,m^{-2}}$ |
| $y=Y/A=g+j\omega c$ | 단위 면적당 admittance | $\mathrm{S\,m^{-2}}$ |
| $D_{it,J}$ | 면적·joule당 interface trap 상태 밀도 | $\mathrm{m^{-2}\,J^{-1}}$ |
| $N_{bt,J}$ | 부피·joule당 border trap 상태 밀도 | $\mathrm{m^{-3}\,J^{-1}}$ |

$Y$는 총 admittance, $G=\operatorname{Re}Y$는 총 conductance, $j^2=-1$, $\omega=2\pi f$이며 시간 의존성은 $e^{j\omega t}$를 사용한다. 이후 $c_m,g_m$는 계측기의 병렬 등가 표현, $c_s,c_{it}$는 모형 안의 내부 응답량을 나타낸다. 계측기에 표시되는 $c_m$를 내부 $c_{it}$와 직접 동일시하지 않는다.[3,4]

### (2) 기준 모형의 가정

기준 모형은 일정한 온도 $T$, 완전히 이온화된 균일 acceptor 농도 $N_A$, 비축퇴 carrier 통계, 반무한 bulk, 무시할 수 있는 gate 누설을 가정한다. 금속 gate와 균일한 선형 유전체를 사용하고 lateral edge 효과를 제외한다. 이 조건에서 먼저 평형 전하를 계산한 뒤 소신호 응답을 구한다. 양자 구속과 낮은 반도체 density of states (DOS), 불완전 이온화가 중요하면 carrier 밀도와 전위의 관계부터 바뀌므로, 고전 모형과의 차이를 모두 결함으로 환산해서는 안 된다.[1,4,5]

이 구분은 advanced C–V 해석의 출발점이다. 산화막이 얇아지거나 반도체의 전하 수용 능력이 작아지면 결함이 없어도 semiconductor capacitance가 무한대가 아니며, 측정 accumulation capacitance가 $c_{ox}$보다 작을 수 있다. 따라서 pristine은 특정 곡선 모양을 뜻하는 말이 아니라, 동일한 물질·구조·측정 조건에서 결함 항만 제외한 기준을 뜻한다.[1,4]

## 2. Poisson–Boltzmann 전하–표면전위 관계

반도체 전하는 surface potential의 선형 함수가 아니다. 정공과 전자의 지수적인 밀도 변화와 이온화 불순물의 고정 전하를 함께 적분해야 accumulation부터 inversion까지 연속적인 $Q_s(\psi_s)$를 얻는다. 아래 식은 depletion approximation을 사용하지 않은 **고전적 평형 모형 안의 정확한 적분 관계**이며, 실제 소자의 모든 물리를 포함하는 정확식이라는 뜻은 아니다.[2,5]

### (1) 전하 밀도와 Poisson 방정식

Boltzmann 상수를 $k_B$, thermal voltage를 $U_T=k_BT/q$, 무차원 전위를 $u=\psi/U_T$라 한다. Bulk 전자·정공 농도 $n_0,p_0$와 intrinsic carrier 농도 $n_i$는 $p_0-n_0=N_A$, $p_0n_0=n_i^2$를 만족한다. 그러면 다음과 같다.[2,5]

$$
p(\psi)=p_0e^{-u},\qquad n(\psi)=n_0e^u,
$$

$$
\rho(\psi)
=q\left[p_0(e^{-u}-1)-n_0(e^u-1)\right],
\qquad
\frac{d^2\psi}{dx^2}=-\frac{\rho(\psi)}{\varepsilon_s}.
$$

$\rho$는 부피 전하 밀도이다. 두 괄호의 $-1$은 bulk의 이온화 acceptor 전하를 전하 중성 조건으로 제거한 결과이다. 따라서 $u=0$에서 $\rho=0$이 자동으로 보장된다. $p_0\simeq N_A$, $n_0\simeq n_i^2/N_A$는 $N_A\gg n_i$일 때의 추가 근사이며, 위 식을 세울 때부터 두 관계를 정확한 등식으로 혼용하지 않는다.[2,5]

전위가 양으로 증가하면 첫 항은 정공의 결핍 때문에 음수가 되고, 두 번째 항은 전자의 증가 때문에 음수가 된다. Depletion 영역에서 지배적인 음전하는 이동 전자가 아니라 정공이 떠난 자리의 이온화 acceptor이다. Inversion으로 진행하면 전자 항을 더 이상 버릴 수 없다.[1,2,5]

### (2) 첫 적분과 면전하

Poisson 방정식에 $d\psi/dx$를 곱하고 bulk에서 표면까지 적분하면 공간에 대한 2차 미분 방정식이 다음의 전기장 관계로 줄어든다.[2,5]

$$
\mathcal E_s^2
=-\frac{2}{\varepsilon_s}\int_0^{\psi_s}\rho(\psi)\,d\psi.
$$

$\mathcal E_s=\mathcal E(0)$이며 bulk의 전기장을 0으로 둔 경계 조건이 적분 상수를 정한다. $u_s=\psi_s/U_T$, $r=n_0/p_0$와 무차원 함수 $F$를 도입하여 적분을 수행하면 다음 결과를 얻는다.[2,5]

$$
F(u)=e^{-u}+u-1+r(e^u-u-1),
$$

$$
Q_s(\psi_s)
=-\operatorname{sgn}(u_s)
\sqrt{2\varepsilon_s k_BT p_0\,F(u_s)}.
$$

$\operatorname{sgn}$는 부호 함수이며 $Q_s(0)=0$은 연속 극한으로 정의한다. $F$의 정공 항은 accumulation에서, $u$에 비례하는 항은 depletion에서, $r e^u$는 충분히 큰 양의 전위에서 중요해진다. Bulk에서 $r$가 작다는 사실만으로 전체 전위 범위에서 전자 항을 무시할 수는 없다. 작은 계수와 큰 지수의 곱이 strong inversion을 만든다.[2,5]

이 식과 1절의 gate 전압식을 결합하면 $\psi_s$를 매개변수로 한 $(V_G,Q_s)$ 곡선을 얻는다. 먼저 $\psi_s$를 선택하여 $Q_s$를 계산하고 전압 분배식으로 $V_G$를 구하는 방식은, 전압마다 공간 격자를 직접 풀지 않고도 고전 평형 기준선을 만드는 방법이다. 다만 이 곡선의 미분은 평형을 따라가는 응답이며, inversion 전하가 동결된 고주파 응답으로 바로 사용할 수 없다.[1,2,5]

### (3) 미분 capacitance와 flat-band 극한

평형 반도체 capacitance는 $c_s=-dQ_s/d\psi_s>0$으로 정의한다. 위 적분식을 미분한 결과는 $u_s\ne0$에서 다음과 같다.[2,5]

$$
F'(u)=1-e^{-u}+r(e^u-1),
$$

$$
c_s=
\frac{\sqrt{2\varepsilon_s k_BT p_0}}{2U_T}
\frac{\operatorname{sgn}(u_s)F'(u_s)}{\sqrt{F(u_s)}}.
$$

Flat band에서 분자와 분모가 함께 0으로 가므로 이 표현에 $u_s=0$을 직접 대입하지 않는다. $F(u)=(1+r)u^2/2+O(u^3)$로 전개하면 Debye screening length $L_D$와 유한한 flat-band capacitance를 얻는다. 아래 극한은 앞선 두 출처의 전하식으로부터 유도한 것이다.[2,5]

$$
L_D=\sqrt{\frac{\varepsilon_s k_BT}{q^2(p_0+n_0)}},
\qquad
c_{s,FB}=\frac{\varepsilon_s}{L_D},
$$

$$
c_{FB}=\left(\frac1{c_{ox}}+\frac{L_D}{\varepsilon_s}\right)^{-1}.
$$

Flat band에서 총 반도체 전하가 0이라는 사실은 미분 전하 응답까지 0이라는 뜻이 아니다. 작은 양·음의 전위 변화가 유한한 screening 길이에 걸쳐 carrier를 재배치하므로 $c_{s,FB}$는 유한하다. Depletion 폭을 무리하게 0으로 보내 $c_{FB}=c_{ox}$라고 처리하면 flat-band voltage 추출에 체계적인 오차가 생긴다.[2,5]

## 3. Pristine C–V와 carrier 응답 시간

Pristine 소자에서도 저주파와 고주파 inversion C–V는 다르다. Gate의 direct current (DC) 바이어스로 정해지는 동작점과 alternating current (AC) 소신호에 대한 응답을 구분해야 한다. 전하가 동작점에 존재한다는 것과 매 주기마다 증감할 수 있다는 것은 별개의 조건이다.[1,3]

### (1) 평형 C–V와 depletion approximation

결함이 없는 구조에서 $Q_G=-Q_s$이고 $dV_G/d\psi_s=1+c_s/c_{ox}$이므로, 평형을 따라가는 gate capacitance $c_g=dQ_G/dV_G$는 다음과 같다.[1,2]

$$
c_g=\frac{c_{ox}c_s}{c_{ox}+c_s},
\qquad
\frac{d\psi_s}{dV_G}=\frac{c_{ox}}{c_{ox}+c_s}.
$$

첫 식은 산화막과 반도체 응답의 직렬 연결이고, 두 번째 식은 gate 전압 중 실제 band bending으로 전달되는 비율이다. Accumulation에서는 정공 응답이 커져 $c_s\gg c_{ox}$이면 $c_g\simeq c_{ox}$이다. Depletion에서는 이동 carrier가 적고 공간전하층이 두꺼워지므로 $c_s$가 작아져 $c_g$가 감소한다.[1,2]

Depletion approximation은 폭 $W_d$ 내부의 전하 밀도를 $-qN_A$, 그 밖을 0으로 둔다. 이동 carrier를 무시할 수 있는 depletion 구간에서 다음을 얻는다.[1,2]

$$
W_d\simeq\sqrt{\frac{2\varepsilon_s\psi_s}{qN_A}},
\qquad
Q_d\simeq-qN_AW_d,
\qquad
c_d\simeq\frac{\varepsilon_s}{W_d}.
$$

$Q_d$는 depletion 전하이고 $c_d=-dQ_d/d\psi_s$이다. $c_d$는 이온화 불순물이 AC에 맞추어 이동한다는 뜻이 아니다. 다수 carrier인 정공이 depletion 경계에서 드나들면서 전기적으로 드러나는 고정 전하 영역의 폭이 바뀌는 것이다. 이 모형은 flat band 근처의 완만한 carrier 분포와 inversion 전하의 증가를 버리므로 두 전이 영역에는 2절의 연속 전하식을 우선한다.[1,2,5]

### (2) Inversion의 저주파·고주파 분기

p-type에서 $\phi_F=U_T\ln(p_0/n_i)>0$라 두면 $\psi_s=2\phi_F$에서 $n_s=p_0$이다. $p_0\simeq N_A$인 통상적인 threshold 정의와 depletion approximation을 함께 적용한 결과는 다음과 같다.[1,2]

$$
V_{T0}\simeq\phi_{ms}+2\phi_F
+\frac{\sqrt{4q\varepsilon_sN_A\phi_F}}{c_{ox}},
\qquad
W_{d,\max}\simeq\sqrt{\frac{4\varepsilon_s\phi_F}{qN_A}}.
$$

$V_{T0}$는 pristine 기준의 threshold voltage이다. Strong inversion에서 전위가 $2\phi_F$ 부근에 머물고 추가 gate 전하가 주로 inversion 전하를 증가시킨다는 근사로부터, low-frequency (LF) 응답은 다시 $c_{ox}$에 접근한다. 실제 $\psi_s$가 정확히 고정되는 것은 아니며, 2절의 전하식에서는 계속 변한다.[1,2]

High-frequency (HF) 응답은 inversion 전하의 **소신호 변화**가 무시되는 경우이다. DC inversion 층은 존재할 수 있고, AC 전하는 주로 depletion 폭의 작은 변동으로 보상된다. 따라서 다음 plateau가 나타난다.[1,3]

$$
c_{\min}\simeq
\left(\frac1{c_{ox}}+\frac{W_{d,\max}}{\varepsilon_s}\right)^{-1}.
$$

단독 MOS capacitor에서는 소수 carrier의 생성·공급이 느릴 수 있지만, source와 drain이 연결된 MOS field-effect transistor (MOSFET)에서는 접촉을 통해 inversion carrier를 공급할 수 있다. 따라서 같은 주파수에서도 단자 구성에 따라 inversion 응답이 달라진다. “몇 Hz 이하면 LF”라는 고정 경계보다, 해당 시료에서 carrier가 실제로 응답하는지 확인하는 것이 먼저이다.[1,3]

### (3) Deep depletion과 두 시간 척도

Deep depletion은 DC 전압 주사 자체가 소수 carrier 공급보다 빠를 때 나타나는 비평형 상태이다. 충분한 inversion 전하가 쌓이기 전에 gate 전압을 높이면 $W_d$가 평형의 $W_{d,\max}$보다 커지고 capacitance가 HF plateau보다 더 낮아질 수 있다. 이는 HF inversion plateau와 동일한 현상이 아니다.[1,3]

표 2. Pristine MOS capacitor의 inversion 조건과 관측 결과.

| 조건 | DC 동작점의 inversion 전하 | AC inversion 전하 변화 | 대표 C–V 결과 |
| --- | --- | --- | --- |
| 충분히 느린 주사와 LF 측정 | 평형에 가까움 | 유효함 | $c_g$가 $c_{ox}$ 쪽으로 증가 |
| 충분히 느린 주사와 HF 측정 | 평형에 가까움 | 무시 가능 | $c_{\min}$ 부근 plateau |
| 소수 carrier 공급보다 빠른 주사 | 평형값보다 부족 | 단순 평형 미분 불가 | Deep depletion으로 추가 감소 |

표 2의 세 조건은 Hu의 [Fig. 5–18과 관련 설명](https://www.chu.berkeley.edu/wp-content/uploads/2020/01/Chenming-Hu_ch5-1.pdf), Stampfer의 [Fig. 5.9](https://www.iue.tuwien.ac.at/phd/stampfer/node-Capacitance-Voltage-Measurements.html)에서 비교할 수 있다. 두 출처의 그림은 원문에서 확인하며 여기에는 복제하지 않는다.[1,3]

!!! abstract "[Measurement]"
    Quasi-static (QS) C–V는 충분히 느린 전압 ramp에서 측정한 총 gate 전류 $I_G$를 전압 변화율로 나누어 얻는다. 누설 전류 $I_{leak}$를 별도로 평가할 수 있으면 면적 정규화 값은 다음과 같다.[1,3]

    $$
    c_{QS}(V_G)=\frac{I_G-I_{leak}}{A\,dV_G/dt}.
    $$

    Ramp를 더 느리게 했을 때 곡선이 수렴하는지 확인한다. Ramp가 느려질수록 변위 전류는 작아지므로 누설이 지배하면 QS 추출이 불안정해진다. QS와 HF의 inversion 차이를 그대로 interface trap capacitance라고 빼서는 안 된다.[1,3]

## 4. 결함 전하에 의한 C–V 이동과 변형

결함은 gate 전압의 분배와 그 미분을 각각 바꾼다. 측정 중 일정한 전하는 주로 전압축 이동을 만들고, 표면전위에 따라 점유가 변하는 전하는 gate 전압 중 일부를 추가로 소모하여 stretch-out을 만든다. AC에도 응답하는 결함은 여기에 추가 capacitance와 손실까지 남긴다. 이 세 효과는 한 시료에 겹쳐 나타날 수 있다.[1,3,4]

### (1) 고정 전하와 flat-band 이동

먼저 산화막 전하를 계면의 등가 면전하 $Q_f$로 나타내고, 가변 interface trap 전하를 $Q_{it}(\psi_s)$로 분리한다. 산화막 내부의 공간 분포를 무시한 이 모형의 gate 관계는 다음과 같다.[1,3]

$$
V_G=\phi_{ms}+\psi_s
-\frac{Q_s(\psi_s)+Q_{it}(\psi_s)+Q_f}{c_{ox}},
$$

$$
V_{FB}=\phi_{ms}-\frac{Q_f+Q_{it}(0)}{c_{ox}}.
$$

Flat band는 반도체의 band bending이 0이라는 뜻이다. 계면에 전하가 있으면 flat band에서도 산화막 전기장이 0일 필요는 없다. $Q_{it}(0)$를 $V_{FB}$에 이미 포함했다면 이후 전압식에는 $\Delta Q_{it}=Q_{it}(\psi_s)-Q_{it}(0)$만 넣어야 한다. 전체 $Q_{it}$를 다시 넣으면 flat-band 전하를 두 번 센다.[1,3]

$$
V_G=V_{FB}+\psi_s
-\frac{Q_s(\psi_s)+\Delta Q_{it}(\psi_s)}{c_{ox}}.
$$

$Q_f$만 증가하고 다른 물리량이 같으면 곡선의 일정한 이동은 $\Delta V_G=-\Delta Q_f/c_{ox}$이다. 양의 전하는 음의 gate 전압 방향, 음의 전하는 양의 방향으로 이동시킨다. 반면 work function 변화나 이미 존재하던 trap의 점유 변화도 전압 이동에 기여하므로, $V_{FB}$ 이동 하나만으로 새 결함의 개수를 정할 수는 없다.[1,3,4]

!!! abstract "[Measurement]"
    동일한 온도·면적·산화막 기준에서 flat-band 위치를 비교한다. Work function과 $c_{ox}$가 유지되고 이동이 등가 고정 전하 변화로 설명되는 경우에 한해 다음을 적용한다.[1,3]

    $$
    \Delta Q_{eff}=-c_{ox}\Delta V_{FB}.
    $$

    $\Delta Q_{eff}$는 전기적으로 환산한 유효 전하 변화이다. 산화막 내부 분포나 계면 점유를 별도로 알지 못하면 이를 특정 종류의 결함 수로 이름 붙이지 않는다. 곡선이 stretch-out까지 보이면 한 점에서 잰 수평 이동을 전 구간의 고정 이동으로 해석하지 않는다.[3,4]

### (2) Interface trap capacitance와 stretch-out

Interface trap은 반도체와 전하를 교환하여 gate 바이어스에 따라 점유가 변하는 계면 상태이다. 정적 응답의 부호를 $c_{it,0}=-dQ_{it}/d\psi_s$로 정의하면, 안정적인 통상적 trap 응답에서 $c_{it,0}\ge0$이다. DC 주사에 대해 trap이 평형에 가까울 때 전압 분배식을 미분하면 다음을 얻는다.[3,4]

$$
\frac{dV_G}{d\psi_s}
=1+\frac{c_s+c_{it,0}}{c_{ox}},
\qquad
\frac{d\psi_s}{dV_G}
=\frac{c_{ox}}{c_{ox}+c_s+c_{it,0}}.
$$

따라서 같은 $\psi_s$ 구간을 지나려면 pristine보다 넓은 gate 전압 범위가 필요하다. 이것이 stretch-out의 전기정역학적 의미이다. Trap이 AC에 너무 느려 직접 측정 capacitance에 보이지 않아도, DC 주사를 따라 점유가 변하면 HF C–V의 전압축 변형은 남는다. HF 측정이 곧 defect-free 측정은 아니다.[3,4]

Trap 밀도를 에너지로 환산할 때는 단위가 중요하다. $D_{it,J}$가 Fermi level 부근의 열적 에너지 폭에서 거의 일정하고 그 상태들이 평형 응답을 할 수 있으면 다음 근사를 쓴다.[3,4,6]

$$
c_{it,0}\simeq q^2D_{it,J}.
$$

실무에서 $D_{it}$를 $\mathrm{cm^{-2}\,eV^{-1}}$로 표시하고 $c_{it,0}$를 $\mathrm{F\,cm^{-2}}$로 표시하면, 통상적인 수치 관계는 $c_{it,0}\simeq qD_{it}$이다. 전자의 $q^2$ 중 한 인자는 점유가 변할 때의 전하이고 다른 한 인자는 전위 변화와 에너지 변화의 변환이다. 에너지 축을 J에서 eV로 바꾸면 두 번째 인자가 단위 변환에 흡수된다. $D_{it}$의 에너지 단위를 확인하지 않은 채 $q$와 $q^2$ 중 하나를 선택해서는 안 된다.[3,4,6]

Trap 분포가 열적 폭 안에서 급격히 변하면 측정값은 한 에너지에서의 정확한 밀도라기보다 주변 점유 변화가 가중된 응답이다. 또한 $Q_{it}$는 점유된 상태의 순전하이고 $D_{it}$는 에너지당 상태 수이므로 서로 다른 물리량이다. 큰 상태 밀도라도 측정 창에서 점유가 변하지 않으면 작은 AC 응답으로 보일 수 있다.[3,4]

### (3) Pristine 대비 관측 패턴

표 3은 서로 독립적인 관측 특징을 분리한 것이다. 각 행은 진단 후보이며 하나의 특징과 한 종류의 결함이 일대일 대응한다는 뜻은 아니다.[1,3,4,6,7]

| 비교 대상 | 주된 변화 | 주파수·시간 의존성 | 해석상 구분 |
| --- | --- | --- | --- |
| Pristine의 carrier 응답 | LF/HF inversion 분기 | 소수 carrier 공급에 의존 | 결함이 없어도 발생 |
| 측정 중 고정된 전하 | C–V의 수평 이동 | 선택한 측정 창에서 거의 일정 | 느린 trap도 고정 전하처럼 보일 수 있음 |
| DC에 응답하고 AC에는 느린 trap | Stretch-out | 주사 시간과 AC 주파수의 상대 관계 | HF 곡선에도 결함 정보가 남음 |
| AC에 응답하는 interface trap | 추가 capacitance와 conductance 손실 | $\omega\tau$ 부근의 분산 | 내부 trap 응답과 단자 응답의 구분 필요 |
| 넓은 시간 분포의 border trap | 넓은 주파수 구간의 분산·이력 | 주파수·대기·주사 조건에 의존 | 단일 relaxation 추출식 적용에 한계 |
| 직렬 저항 | 높은 주파수에서 겉보기 capacitance 감소 | 회로의 $RC$ 시간에 의존 | Trap 손실과 분리 필요 |

결함을 넣은 곡선은 모든 gate 전압에서 pristine보다 위나 아래에 놓이는 것이 아니다. 추가 $c_{it}$는 동일한 표면전위에서 응답을 증가시키지만, 동시에 전압 이동과 stretch-out이 생겨 동일한 $V_G$에서 비교하는 두 시료의 $\psi_s$가 달라진다. 따라서 모형 비교는 동일 $V_G$와 동일 $\psi_s$의 의미를 구분해야 한다.[3,4]

## 5. Interface trap의 동적 admittance

유한한 trap 응답 시간은 저장 성분과 손실 성분을 동시에 만든다. 정적인 $c_{it,0}$ 하나를 모든 주파수에 그대로 더하는 모형으로는 이 둘을 설명할 수 없다. Depletion에서 소수 carrier 응답이 무시되고 반도체 자체 손실이 작다는 조건 아래, trap을 반도체 capacitance와 병렬인 동적 branch로 나타낸다.[3,4]

### (1) 단일 relaxation 모형

하나의 유효 relaxation time $\tau$를 갖는 점유 변화가 평형값으로 1차적으로 완화한다고 가정한다. Trap 전하의 작은 변동 $\delta Q_{it}$와 표면전위 변동 $\delta\psi_s$에 대해 다음 선형식과 응답을 얻는다. 이는 단일 series resistance–capacitance (RC) branch와 동등한 모형이다.[3,4]

$$
\tau\frac{d\delta Q_{it}}{dt}+\delta Q_{it}
=-c_{it,0}\delta\psi_s,
\qquad
\delta Q_{it}=-\frac{c_{it,0}}{1+j\omega\tau}\delta\psi_s.
$$

따라서 반도체 표면 노드에서 보이는 trap admittance $y_{it}$는 다음과 같다.[3,4]

$$
y_{it}=\frac{j\omega c_{it,0}}{1+j\omega\tau}
=g_{it}+j\omega c_{it,p},
$$

$$
c_{it,p}=\frac{c_{it,0}}{1+(\omega\tau)^2},
\qquad
\frac{g_{it}}{\omega}
=\frac{c_{it,0}\omega\tau}{1+(\omega\tau)^2}.
$$

$c_{it,p}$는 주파수 의존 병렬 capacitance 성분이다. $\omega\tau\ll1$이면 trap은 거의 평형적으로 따라가고, $\omega\tau\gg1$이면 AC capacitance 기여가 작아진다. $\omega\tau=1$에서 $g_{it}/\omega$가 최대이며 최대값은 **$c_{it,0}/2$**이다. 이 계수는 위 식을 직접 미분하거나 대입하여 확인할 수 있다. 뒤의 연속 에너지 분포에 대한 2.5 계수와 혼용하지 않는다.[3,4]

손실 피크는 점유가 전압보다 늦게 변하기 때문에 생긴다. 단, 고주파에서 $g_{it}/\omega\to0$이라는 사실을 $g_{it}\to0$이라고 읽으면 틀린다. 이 단일 RC 모형에서 $g_{it}$ 자체는 $c_{it,0}/\tau$에 접근한다. Trap을 단순히 “고주파에서 사라지는 capacitance”로만 그리면 conductance의 정규화 의미를 놓친다.[3,4]

### (2) Gate에서 측정하는 복소 응답

Depletion 영역의 반도체 branch를 $j\omega c_d$, trap branch를 $y_{it}$라 하면 내부 admittance $y_p$와 gate admittance $y_g$는 다음과 같다.[3,4]

$$
y_p=j\omega c_d+y_{it},
\qquad
y_g=\left(\frac1{j\omega c_{ox}}+\frac1{y_p}\right)^{-1}.
$$

기기가 보고하는 병렬 등가 capacitance는 $\operatorname{Im}y_g/\omega$이고 conductance는 $\operatorname{Re}y_g$이다. 따라서 $c_{it,p}$를 $c_{ox}$에 직접 더하는 것이 아니다. 먼저 반도체 노드에서 capacitance와 손실을 결합하고, 산화막을 직렬로 연결해야 한다. 특히 손실이 큰 영역에서는 실수 capacitance들만 직렬 합성하는 식으로 복소 네트워크를 대신할 수 없다.[3,4]

AC 진폭 역시 모형의 일부이다. 위 식은 동작점 근처의 미분 응답이므로 표면전위 진폭이 점유 함수를 크게 가로지르지 않아야 한다. 실제로는 gate AC 진폭을 낮추었을 때 추출 결과가 수렴하는지 확인한다. 진폭이 크면 서로 다른 $\psi_s$와 점유 상태를 평균하게 되므로 small-signal $D_{it}$의 의미가 흐려진다.[3,4]

### (3) 연속 에너지 분포와 손실 피크

실제 계면에는 서로 다른 에너지의 trap이 존재한다. 열적으로 기여하는 구간에서 $D_{it}$와 capture 특성이 거의 일정하고 lateral surface-potential fluctuation이 작다는 전통적 연속 분포 근사에서는, $c_D=q^2D_{it,J}$를 정의하여 다음 식을 사용한다.[3,4]

$$
\frac{g_p}{\omega}
=\frac{c_D}{2\omega\tau}
\ln\!\left[1+(\omega\tau)^2\right].
$$

여기서 $g_p$는 산화막의 직렬 효과를 제거한 내부 병렬 conductance이다. 단일 relaxation 식과 달리 에너지 분포의 점유·시간 응답을 평균한 결과이다. $a=\omega\tau$라 하면 극값 조건은 $2a^2/(1+a^2)=\ln(1+a^2)$이며, $a\simeq1.98$에서 최대값이 약 $0.402c_D$가 된다. 따라서 흔히 쓰는 추출 관계는 다음과 같다.[3,4]

$$
D_{it,J}\simeq\frac{2.5}{q^2}
\left(\frac{g_p}{\omega}\right)_{\max}.
$$

$\mathrm{eV^{-1}}$ 밀도와 같은 면적 단위로 환산할 때는 통상 $D_{it}\simeq(2.5/q)(g_p/\omega)_{\max}$로 쓴다. 총 $G_p$를 쓰면 반드시 면적 $A$로 나누어야 한다. 2.5는 보편적인 기하학 상수가 아니라 이 분포 모형의 피크 모양에서 나온 계수이다. 비대칭 피크, 여러 피크, 넓은 plateau에서는 이 모형의 적합성을 먼저 판단한다.[3,4]

## 6. C–V와 conductance를 이용한 결함 추출

결함 추출은 내부 $c_s$와 $c_{it}$를 단자에서 측정한 $C,G$로부터 분리하는 역문제이다. 서로 다른 방법은 서로 다른 시간 창의 trap을 관측하므로, 같은 시료에서 얻은 밀도가 다르다고 해서 반드시 어느 한 계산이 잘못된 것은 아니다. 다만 비교 전에는 진정한 LF/HF 조건, 반도체 기준선, 면적과 산화막 capacitance를 일치시켜야 한다.[3,4]

### (1) High–low 방법

같은 DC 상태에서 LF에는 trap이 응답하고 HF에는 응답하지 않으며, 두 경우 반도체의 $c_s$가 같다고 가정한다. 손실이 작은 조건에서 산화막 직렬 효과를 역변환한 차이가 $c_{it,0}$이다.[3,4]

!!! abstract "[Measurement]"
    Depletion의 동일 gate 바이어스에서 보정된 $c_{LF},c_{HF}$를 얻고, 양쪽 주파수 극한에 수렴하는지 확인한 뒤 다음을 계산한다.[3,4]

    $$
    c_{it,HL}=
    \frac{c_{ox}c_{LF}}{c_{ox}-c_{LF}}
    -\frac{c_{ox}c_{HF}}{c_{ox}-c_{HF}},
    \qquad
    D_{it,J}\simeq\frac{c_{it,HL}}{q^2}.
    $$

    단순한 $(c_{LF}-c_{HF})/q^2$는 gate 전압 분배를 제거하지 않아 같은 추출식이 아니다. Inversion에서는 반도체의 LF/HF 응답 자체가 달라질 수 있으므로 이 단순 high–low 식의 적용 구간에서 제외한다.[3,4]

어떤 trap은 가장 낮은 측정 주파수에서도 느리고, 어떤 trap은 가장 높은 주파수에서도 빠를 수 있다. 전자는 LF에 누락되고 후자는 HF에도 남아 두 곡선의 차이가 작아진다. 따라서 정해진 두 주파수만 선택하고 모든 trap의 밀도를 얻었다고 주장할 수 없다. 또한 $c_{LF}$가 $c_{ox}$에 접근하면 분모가 작아져 작은 측정 오차나 $c_{ox}$ 오차가 크게 증폭된다.[3,4]

### (2) Surface potential 복원과 Terman 방법

에너지별 $D_{it}$를 보고하려면 gate 전압을 surface potential로 바꾸어야 한다. QS 평형에서 산화막 전압의 미분은 $dV_{ox}=dQ_G/c_{ox}$이므로, $c_{QS}=dQ_G/dV_G$를 사용한 Berglund 적분은 다음과 같다.[3,4]

$$
\psi_s(V_G)-\psi_s(V_0)
=\int_{V_0}^{V_G}
\left[1-\frac{c_{QS}(V)}{c_{ox}}\right]dV.
$$

$V_0$는 기준 gate 전압이며 $\psi_s(V_0)$는 별도로 정해야 하는 적분 상수이다. Accumulation이라고 무조건 $\psi_s=0$으로 놓는 것은 근사이다. 특히 반도체 DOS가 작으면 accumulation에서도 상당한 band bending이 있어 기준값의 오차가 전체 에너지 축을 이동시킨다. 적분은 전위 차이를 제공하며 절대 에너지 원점을 자동으로 보장하지 않는다.[3,4]

Terman 방법은 trap이 DC 주사는 따라가되 AC에는 응답하지 않는 HF C–V를 이용한다. 적절한 pristine $c_{HF}(\psi_s)$와 측정 capacitance를 대응시켜 $\psi_s(V_G)$를 복원한 뒤 4절의 미분 관계로부터 trap capacitance를 구한다.[3,4]

!!! abstract "[Measurement]"
    산화막 capacitance와 도핑을 독립적으로 정하고, HF 곡선이 단조롭게 변해 $c_{HF}\leftrightarrow\psi_s$ 대응이 가능한 구간에서 다음 식을 적용한다.[3,4]

    $$
    c_{it,T}=c_{ox}
    \left(\frac{dV_G}{d\psi_s}-1\right)-c_s,
    \qquad
    D_{it,J}\simeq\frac{c_{it,T}}{q^2}.
    $$

    여기서 $c_s$는 동일 표면전위의 pristine 반도체 응답이다. Pristine이면 $dV_G/d\psi_s=1+c_s/c_{ox}$이므로 결과가 0이 된다. 괄호의 $-1$을 빠뜨리면 결함이 없는 경우에도 가짜 trap capacitance가 남는다.[3,4]

HF plateau에서는 capacitance가 전위에 거의 무관하므로 역변환이 불안정하다. 도핑이나 $c_{ox}$를 잘못 선택해도 이론과 측정 곡선의 차이가 stretch-out으로 환산된다. 느린 산화막 trap의 주사 중 점유 변화도 영향을 주기 때문에 Terman 결과가 순수한 빠른 interface trap 밀도만을 뜻한다고 단정하지 않는다.[3,4]

### (3) Conductance 방법과 측정 창

Conductance 방법은 trap의 지연 응답에 의한 손실을 사용한다. 우선 계측기의 총 $G_m,C_m$를 면적으로 나눈 $g_m,c_m$를 준비하고 직렬 저항 영향을 보정한다. 이상적인 산화막 capacitor를 직렬로 제거하면 내부 손실은 다음과 같다.[3,4]

!!! abstract "[Measurement]"
    고정된 DC 바이어스마다 주파수를 변화시키며 다음 $g_p/\omega$를 계산하고, 충분한 주파수 범위에서 피크 양쪽을 관측한다.[3,4]

    $$
    \frac{g_p}{\omega}
    =\frac{\omega c_{ox}^{\,2}g_m}
    {g_m^2+\omega^2(c_{ox}-c_m)^2}.
    $$

    연속 분포 모형이 맞으면 5절의 2.5 계수로 $D_{it}$를 추출한다. 피크 주파수를 $f_p$라 할 때 그 모형의 시간 상수는 $\tau\simeq1.98/(2\pi f_p)$이다. 단일 relaxation 모형에는 $\tau=1/(2\pi f_p)$와 다른 피크 계수를 사용한다.[3,4]

주파수 창을 벗어난 trap은 피크가 나타나지 않는다. 따라서 피크가 없다는 것은 trap이 없다는 결론과 다르다. 온도를 바꾸면 capture·emission 시간이 바뀌어 관측 가능한 에너지 구간이 달라질 수 있지만, 저온에서 응답이 동결된 상태를 감소한 결함 밀도로 해석해서는 안 된다. 피크 위치를 trap 에너지로 변환하는 데에는 capture 특성에 대한 추가 모형이 필요하다.[3,4]

$D_{it}$가 매우 크면 단자 응답이 산화막에 의해 제한되고 작은 측정 오차가 내부 응답 역변환에 크게 증폭된다. 특히 high-$k$/III–V 계면에서는 비대칭 에너지 분포와 큰 $D_{it}$ 때문에 표준 conductance 피크식이 밀도를 과소평가할 수 있다. 피크 높이만 비교하지 말고 바이어스에 따른 위치 이동, 모양, C–V stretch-out을 함께 확인한다.[3,4]

## 7. Border trap과 넓은 주파수 분산

Border trap은 산화막 안에 있으면서 반도체와 전하를 교환할 수 있는 결함이다. Interface trap이 계면에서 carrier를 주고받는 것과 달리 산화막 깊이에 따른 tunneling 거리가 추가되므로, 같은 에너지의 결함도 서로 다른 시간 척도로 관측될 수 있다. 이 분포는 accumulation에서 넓은 주파수 범위의 capacitance 분산과 손실을 설명하는 데 중요하다.[6,7]

### (1) Tunneling 깊이와 응답 시간

이 절에서는 산화막 좌표 $z$를 계면에서 gate 방향으로 정의한다. $0\le z\le t_{ox}$이며 반도체 좌표 $x$와 반대 방향이다. 단순 tunneling 제한 모형에서 계면의 유효 시간 상수 $\tau_0$와 감쇠 계수 $\kappa>0$를 사용하면 다음과 같다.[6,7]

$$
\tau(z)=\tau_0e^{2\kappa z}.
$$

$\kappa$의 단위는 길이의 역수이다. $\tau_0$는 바이어스·carrier 공급·점유 조건을 포함한 유효 값이므로 모든 온도와 전압에서 일정한 물질 상수로 간주하지 않는다. 이 식은 거리 의존성을 단순화한 모형이고, 실제 capture에 다른 활성화 과정이 중요하면 해당 시간 의존성을 함께 포함해야 한다.[6,7]

$\omega\tau(z)\sim1$인 깊이를 계산하면 주파수에 따른 대략적인 관측 깊이를 얻는다. 아래 식은 위 tunneling 모형을 대수적으로 풀어 얻은 추론이다.[6,7]

$$
z_\omega\simeq\frac{1}{2\kappa}
\ln\!\left(\frac{1}{\omega\tau_0}\right).
$$

이 값이 실제 산화막 안에 있을 때에만 깊이 선택의 직관으로 사용한다. $z_\omega<0$이면 계면에 가까운 해당 모형의 trap도 느린 쪽에 있고, $z_\omega>t_{ox}$이면 깊이 범위 전체가 빠른 쪽에 놓일 수 있다. 응답은 이 깊이에서 불연속적으로 켜지고 꺼지는 것이 아니라 부드럽게 변한다.[6,7]

주파수를 낮추면 더 깊고 느린 결함이 응답에 참여한다. 깊이 분포가 완만하면 일정 주파수 창에서 capacitance가 $\ln(1/\omega)$에 가깝게 변하고 $g/\omega$가 넓은 plateau처럼 보일 수 있다. 그러나 이 거동은 유한한 두께와 시간 창, 전압 분배의 결과이며 모든 border trap 분포의 보편적인 법칙은 아니다.[6,7]

### (2) 분포 회로와 공간 의존 admittance

산화막 내 trap을 모두 계면의 하나의 $c_{it}$로 옮기면 위치에 따른 전압 분배를 잃는다. 이를 보존하려면 산화막을 얇은 층으로 나누어 각 층의 dielectric capacitance와 trap branch를 결합한다. 반도체 쪽을 바라보는 단위 면적당 admittance를 $y(z)$, 단위 깊이당 국소 trap admittance를 $\eta_{bt}(z,\omega)$라 정의한다.[6,7]

$$
\frac{dy}{dz}
=-\frac{y^2}{j\omega\varepsilon_{ox}}
+\eta_{bt}(z,\omega),
\qquad
y(0)=j\omega c_s.
$$

첫 항은 추가된 산화막 두께의 직렬 capacitance, 두 번째 항은 그 위치의 결함 응답이다. 여기의 $c_s$는 해당 accumulation 바이어스에서 독립적으로 정한 반도체 capacitance이다. $dy/dz$와 두 우변 항의 단위는 모두 $\mathrm{S\,m^{-3}}$이다. $y(t_{ox})$가 최종 gate admittance이며, 여기에 전체 $c_{ox}$를 다시 직렬로 더하지 않는다. 이미 미분 방정식 안에서 산화막 전체를 통과했기 때문이다.[6,7]

국소 시간 응답을 한 개의 relaxation으로 대표하는 모형에서는 다음 kernel을 쓴다. $N_{bt,J}$는 열적으로 기여하는 에너지 부근의 부피 상태 밀도이다.[6,7]

$$
\eta_{bt}^{(1)}
=\frac{j\omega q^2N_{bt,J}(z)}{1+j\omega\tau(z)}.
$$

반면 점유와 시간 상수의 에너지 의존성을 연속 분포로 적분하는 모형에는 다음과 같은 logarithmic kernel이 사용된다. 이는 앞 식을 단순히 기호만 바꾼 것이 아니라 국소 에너지 응답을 평균하는 방식이 다른 모형이다.[3,7]

$$
\eta_{bt}^{(dist)}
=\frac{q^2N_{bt,J}(z)}{\tau(z)}
\ln\!\left[1+j\omega\tau(z)\right].
$$

두 번째 식의 실수부를 $\omega$로 나누면 5절의 연속 interface 분포식과 같은 $\ln[1+(\omega\tau)^2]/(2\omega\tau)$ 형태가 나온다. 공간 적분 이전에 이미 에너지 평균이 들어간 셈이다. 따라서 서로 다른 kernel로 얻은 $N_{bt}$와 $\tau_0$를 정의 확인 없이 비교해서는 안 된다. 두 kernel은 저주파에서 모두 $\eta\simeq j\omega q^2N_{bt,J}$가 되지만 중간·고주파 응답은 다르다.[3,6,7]

결함 밀도를 0으로 놓으면 분포 방정식은 반드시 pristine 직렬 관계로 돌아가야 한다. 실제로 $d(1/y)/dz=1/(j\omega\varepsilon_{ox})$를 적분하면 다음을 얻는다.[6,7]

$$
\frac{1}{y(t_{ox})}
=\frac{1}{j\omega c_s}
+\frac{t_{ox}}{j\omega\varepsilon_{ox}}
=\frac{1}{j\omega c_s}+\frac{1}{j\omega c_{ox}}.
$$

이 극한은 좌표 방향, 산화막 직렬 항의 부호, 면적 정규화를 확인하는 유용한 검사이다. 실험적 분산과 분포 회로의 예는 Yuan 등의 [Figs. 1–3](https://web.ece.ucsb.edu/Faculty/rodwell/publications_and_presentations/publications/2011_4_april_yuan_EDL.pdf)에서 확인할 수 있다. 이 실험은 Al₂O₃/InGaAs의 accumulation 사례이며, 동일한 수치나 분산 크기를 Si/SiO₂에 그대로 적용하지 않는다.[6,7]

### (3) Hysteresis와 역문제의 비유일성

전압 주사 중 trap 점유가 평형에서 지연되면 같은 gate 전압에서도 직전의 바이어스와 대기 시간에 따라 전하가 달라진다. 따라서 정방향과 역방향 C–V 사이의 hysteresis는 점유 이력의 정보를 준다. 측정 동안 완전히 동결된 trap은 수평 이동처럼, 더 빠른 trap은 AC 분산처럼 보일 수 있으므로 고정 전하·느린 결함의 구분은 시간 창에 의존한다.[3,7]

!!! abstract "[Measurement]"
    주사 범위·방향·속도·시작 바이어스·대기 시간·온도를 고정하여 양방향 곡선을 얻는다. 두 경로에서 같은 표면 상태를 비교할 수 있고 차이가 등가 전하 이동으로 설명될 때만 다음을 사용한다.[1,3]

    $$
    \Delta Q_{hys,eff}\simeq-c_{ox}\Delta V_{hys}.
    $$

    $\Delta V_{hys}$는 비교 경로 사이의 부호 있는 수평 전압 차이이다. 곡선 모양 자체가 다르면 동일 capacitance가 동일 surface potential을 뜻하지 않을 수 있다. 이때 hysteresis 폭을 전체 산화막 trap 밀도로 환산하지 않는다.[3,4]

분포 모형의 $N_{bt}$, $\tau_0$, $\kappa$, $c_s$는 서로 영향을 주어 제한된 주파수 창의 데이터를 비슷하게 맞출 수 있다. Capacitance만 fitting하면 손실을 잘못 예측하는 해도 남을 수 있으므로 $c(V_G,f)$와 $g(V_G,f)$를 함께 비교하고, 여러 바이어스나 온도에서 같은 매개변수 해석이 유지되는지 검사한다. 맞춘 곡선 하나는 결함의 위치·에너지 분포를 유일하게 결정한 증거가 아니다.[6,7]

## 8. 측정 오차와 적용 범위

결함 해석에서 중요한 것은 pristine와 측정값의 차이를 모두 한 개의 $D_{it}$로 흡수하지 않는 것이다. 전압 이동, 반도체 자체 응답, 직렬 저항, 누설, 시간 이력은 서로 다른 원인인데도 일부 C–V 특징을 공유한다. 내부 전하 모형과 단자 회로 모형을 함께 검토해야 한다.[3,4,6,7]

### (1) 직렬 저항과 누설의 분리

총 series resistance를 $R_s$라 하면 $Z_m=R_s+1/Y_g$이다. 이상적인 총 capacitance $C$만 있는 소자에 직렬 저항이 추가된 경우, 계측기의 병렬 등가 결과는 다음과 같이 유도된다.[4,6]

$$
C_m=\frac{C}{1+(\omega R_sC)^2},
\qquad
G_m=\frac{\omega^2R_sC^2}{1+(\omega R_sC)^2}.
$$

따라서 높은 주파수에서 $C_m$가 감소하고 손실이 나타나는 현상은 결함 없이도 생긴다. 이 절의 식은 총 $C,G,R_s$를 사용한다. 면적 정규화 표현에 그대로 $R_s$를 대입하면 차원이 맞지 않으며, 면적 정규화 impedance에는 $AR_s$가 대응한다.[4,6]

!!! abstract "[Measurement]"
    Trap과 dielectric 손실이 무시되는 강한 accumulation 구간이라면, 실수 impedance로부터 다음 $R_s$ 추정이 가능하다.[4,6]

    $$
    R_s\simeq\operatorname{Re}\frac1{G_m+j\omega C_m}
    =\frac{G_m}{G_m^2+(\omega C_m)^2},
    $$

    $$
    Y_{corr}=\left(\frac1{Y_m}-R_s\right)^{-1}.
    $$

    $Y_m$은 총 측정 admittance이다. 실제 accumulation에 border trap 손실이 있으면 실수 impedance 전체를 $R_s$로 빼는 절차가 결함 신호까지 제거한다. 여러 주파수에서 추정 저항의 일관성을 확인하고, 접촉·배선 또는 독립 측정 정보와 비교한다.[4,6]

누설은 QS 전류와 AC conductance 모두에 영향을 줄 수 있다. 이상적 산화막을 전제로 한 6절의 내부 손실 변환식은 큰 누설이 있는 유전체에 그대로 적용하지 않는다. 누설을 포함한 회로를 세우고 보정이 안정적인 구간만 사용해야 하며, 누설 전류가 변위 전류를 지배하는 조건에서는 QS 자료로 얻은 큰 capacitance를 추가 trap 응답으로 해석하지 않는다.[1,3,4]

### (2) Pristine 모형의 물질 의존성

얇은 산화막에서는 inversion 전하가 계면의 무한히 얇은 sheet가 아니라 반도체 내부에 분포하는 양자역학적 효과가 중요할 수 있다. Poly-Si gate의 depletion도 추가 전압 강하를 만들 수 있다. 이들은 oxide/interface defect와 별개의 이유로 유효 gate capacitance를 줄인다. 해당 구조에서는 1절의 이상적 금속 gate와 고전 carrier 분포 가정을 수정해야 한다.[1,4]

III–V 반도체처럼 conduction-band DOS가 작으면 accumulation에서도 $c_s$가 충분히 크지 않을 수 있고, 비축퇴 Boltzmann 통계가 성립하지 않는 전위 범위가 나타난다. 이때는 실제 band structure와 Fermi–Dirac 통계를 반영한 $Q_s(\psi_s)$를 사용해야 한다. Si용 pristine 곡선의 plateau나 flat-band 비율을 그대로 기준으로 삼으면 intrinsic semiconductor 응답을 결함으로 오인할 수 있다.[4,5]

또한 강한 주파수 분산이 있다고 해서 그것이 곧 계면 화학 구조를 식별하는 것은 아니다. Electrical extraction은 선택한 모형과 시간 창에 대응하는 상태 밀도·시간 상수를 제공한다. 특정 결함의 원자 구조나 전체 산화막 결함 수를 주장하려면 전기적 fitting 이외의 독립적인 정보가 필요하다.[4,7]

### (3) 일관된 비교 절차

표 4는 pristine 계산과 결함 시료를 비교할 때 각 단계에서 확인할 항목이다. 앞 단계의 불확실성을 다음 단계의 결함 밀도로 흡수하지 않도록 순서를 정한다.[1,3,4,6,7]

| 단계 | 확인할 자료 | 다음 해석에 필요한 조건 |
| --- | --- | --- |
| 구조 기준 | 면적·도핑·두께·gate 재료·온도 | 같은 정규화와 올바른 $c_s,c_{ox}$ |
| 동작점 준비 | 주사 방향·속도·대기·단자 연결 | HF inversion과 deep depletion의 구분 |
| 단자 응답 | $C,G$의 주파수·진폭 의존성 | Small-signal 범위와 직렬 저항·누설 평가 |
| 정적 결함 | Flat-band 이동과 stretch-out | 고정 전하와 가변 점유의 분리 |
| 동적 결함 | $g_p/\omega$ 피크와 $c(f)$ | 단일·연속·공간 분포 모형의 선택 |
| 결과 비교 | 에너지 구간·주파수 창·불확실성 | 같은 종류의 밀도와 시간 응답인지 확인 |

권장 결과물은 한 개의 $D_{it}$ 숫자보다, 사용한 에너지·주파수 범위와 피크 모형, $c_{ox}$의 결정법, 주사 이력, 보정 전후 $C,G$를 함께 제시하는 것이다. 특히 가장 낮거나 높은 주파수에서 곡선이 아직 수렴하지 않았다면 미관측 trap의 가능성을 결과의 적용 범위로 남긴다.[3,4,6,7]

## 9. 요약

- Pristine 기준선은 동일한 구조와 측정 조건에서 결함 항을 제외한 모형이다. 고전 평형 $Q_s(\psi_s)$와 HF 소신호 응답은 별도로 계산한다.
- Pristine에도 LF/HF inversion 분기가 있으며, DC carrier 공급이 부족한 deep depletion은 이와 다른 비평형 상태이다.
- 고정 전하의 전압 이동, DC trap 점유에 의한 stretch-out, AC trap 응답에 의한 capacitance·손실을 구분한다.
- High–low, Terman, conductance 방법은 서로 다른 전제와 시간 창을 가진다. $D_{it}$의 J/eV 단위와 단일·연속 분포의 피크 계수를 명시한다.
- Border trap에는 산화막 깊이에 따른 시간 분포와 전압 분배가 필요하다. $C,G$의 공동 해석과 직렬 저항·누설·반도체 기준 모형의 검증 없이는 분산만으로 결함 분포를 유일하게 결정할 수 없다.

## 10. 참고문헌

1. Chenming Hu, *Modern Semiconductor Devices for Integrated Circuits*, Chapter 5, “MOS Capacitor,” §§5.1–5.9, Pearson (2010). [Author-hosted chapter](https://www.chu.berkeley.edu/wp-content/uploads/2020/01/Chenming-Hu_ch5-1.pdf).
2. Matthew J. Gilbert, “Lecture 38: MOS Capacitor I,” *ECE 340*, University of Illinois Urbana-Champaign (November 28, 2011), 특히 pp. 9–16. [Lecture PDF](https://transport.ece.illinois.edu/ece340f11-lectures/ece340lecture38-mos_capi.pdf).
3. Bernhard Stampfer, *Advanced Electrical Characterization of Charge Trapping in MOS Transistors*, §5.2, “Capacitance-Voltage Measurements,” TU Wien (2020), Figs. 5.8–5.10 and Eqs. (5.38)–(5.50). [Dissertation section](https://www.iue.tuwien.ac.at/phd/stampfer/node-Capacitance-Voltage-Measurements.html).
4. Roman Engel-Herbert, Yoontae Hwang, and Susanne Stemmer, “Comparison of methods to quantify interface trap densities at dielectric/III-V semiconductor interfaces,” *Journal of Applied Physics* **108**, 124101 (2010). [DOI: 10.1063/1.3520431](https://doi.org/10.1063/1.3520431); [Author manuscript](https://escholarship.org/content/qt0nf6t24x/qt0nf6t24x.pdf).
5. Philipp Hehenberger, *Advanced Characterization of the Bias Temperature Instability*, Appendix B.1, “Surface Space Charge Region of an n-Type MOS Capacitor,” TU Wien (2011), Eqs. (B.1)–(B.13). [Dissertation appendix](https://www.iue.tuwien.ac.at/phd/hehenberger/dissse52.html).
6. Yu Yuan et al., “A Distributed Model for Border Traps in Al₂O₃–InGaAs MOS Devices,” *IEEE Electron Device Letters* **32**(4), 485–487 (2011). [DOI: 10.1109/LED.2011.2105241](https://doi.org/10.1109/LED.2011.2105241); [Author-hosted PDF](https://web.ece.ucsb.edu/Faculty/rodwell/publications_and_presentations/publications/2011_4_april_yuan_EDL.pdf).
7. Abhitosh Vais, Koen Martens, Dennis Lin, Anda Mocuta, Nadine Collaert, Aaron Thean, and Kristin De Meyer, “An Analytical Model of MOS Admittance for Border Trap Density Extraction in High-k Dielectrics of III–V MOS Devices,” *IEEE Transactions on Electron Devices* **63**(12), 4707–4713 (2016). [DOI: 10.1109/TED.2016.2620603](https://doi.org/10.1109/TED.2016.2620603); [Author-uploaded full text](https://www.researchgate.net/publication/309657100_An_Analytical_Model_of_MOS_Admittance_for_Border_Trap_Density_Extraction_in_High-_k_Dielectrics_of_III-V_MOS_Devices).
