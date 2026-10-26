---
description: 반도체 박막 증착의 공급·표면 반응 원리와 주요 증착법, 에피택시의 결정학적 관계 및 두께·피복성 평가를 설명한다.
---

# 박막 증착 (Thin-film deposition)

박막 증착은 기판 위에 원하는 재료층을 형성하는 공정이다. 반도체 공정에서는 금속 배선, 절연막, 반도체층 등을 증착하며, 같은 재료라도 두께·조성·결정 구조·불순물과 피복 상태에 따라 공정의 결과가 달라진다. 따라서 증착법을 선택할 때는 성장 속도뿐 아니라 **어떤 물질을 어떻게 공급하고, 표면에서 어떤 과정을 거쳐 막으로 만드는지**를 함께 살펴야 한다.[1,2]

이 문서는 physical vapor deposition (PVD), chemical vapor deposition (CVD), atomic layer deposition (ALD)의 공급·반응 원리를 설명하고, CVD의 한 종류인 metal–organic chemical vapor deposition (MOCVD)와 에피택셜 성장을 연결한다. 전기화학 증착과 용액 기반 코팅의 상세 공정은 범위에 포함하지 않는다.

## 1. 성장 과정과 박막 평가의 기준

### (1) 공급 방식과 결정학적 관계

PVD는 고체 또는 액체인 응축상 공급원에서 물질을 물리적으로 방출하여 기판에 도달시키는 방법이다. 대표적으로 evaporation과 sputtering이 있다. Evaporation에서는 가열 중 공급원이 녹을 수 있으므로 PVD 전체를 ‘고체 공급원을 사용하는 공정’으로 한정하지 않는다.[3,4]

CVD에서는 기체 전구체를 수송하고 화학반응으로 고체 막을 만든다. ALD는 기판의 각 위치가 반응물에 순차적으로 노출되도록 하고, 각 단계의 표면 반응이 포화되는 성질을 이용한다. 반응물을 시간적으로 나누는 temporal ALD뿐 아니라 공간적으로 분리하는 spatial ALD도 있으므로, 반응기 전체에서 가스를 연속 공급하는지 여부만으로 CVD와 ALD를 구분할 수 없다.[1,5,6]

**Epitaxy는 증착 장비의 종류가 아니라 박막과 기판 사이의 결정학적 방향 관계를 나타낸다.** 같은 물질의 단결정 위에 성장하면 homoepitaxy, 다른 물질의 결정 위에 성장하면 heteroepitaxy로 구분한다.[2,7] 에피택셜 층은 CVD 계열이나 molecular beam epitaxy (MBE) 등 서로 다른 공급 방식으로 성장시킬 수 있다.[8,9]

아래 표는 서로 다른 분류 기준을 구별한다. 뒤의 공정 비교에서도 공급 방식과 결정 구조를 따로 판단해야 한다.

| 구분 | 분류 기준 | 이 문서의 대표 사례 |
| --- | --- | --- |
| PVD | 응축상 공급원의 물리적 방출 | 가열에 의한 evaporation, 이온 충돌에 의한 sputtering[3,4,10,11] |
| CVD | 기체 전구체의 화학반응 | 열적 CVD, 플라즈마를 이용하는 CVD[1,12] |
| ALD | 분리된 순차 표면 반응의 포화 | Temporal ALD, spatial ALD[5,6,13] |
| Epitaxy | 기판과 성장 결정의 방향 관계 | Si 위의 Si, 화합물 반도체의 이종 에피택셜 층[2,8,9] |

### (2) 표면에서의 흡착과 성장

표면에 도달한 원자나 분자가 모두 박막에 남는 것은 아니다. 입자는 흡착한 뒤 표면을 이동하거나, 다른 종과 반응하여 결정에 편입되거나, 다시 탈착할 수 있다. 따라서 공급원의 방출량과 최종 막의 성장량을 동일시해서는 안 된다. 기판 온도와 표면 상태는 이러한 과정의 상대적인 속도에 영향을 준다.[3,8]

예를 들어 기판 온도를 조절하면 흡착종의 표면 이동과 탈착 조건이 함께 달라진다. 표면에서 충분히 이동하여 결합할 수 있는 조건과 표면에 머물지 못하는 조건은 구별해야 한다. 따라서 공급량을 일정하게 유지해도 기판의 조건이 달라지면 같은 성장 결과를 기대할 수 없다.[3,8]

후속 절의 단순 CVD 모델은 이 복잡한 표면 과정을 하나의 유효 반응 계수로 묶는다. ALD에서는 표면의 반응 가능한 자리가 소모되면 같은 반응물을 더 공급해도 추가 반응이 제한된다. 따라서 CVD의 연속 성장률과 ALD의 사이클당 성장량은 서로 다른 방식으로 해석해야 한다.[1,13,14]

### (3) 두께, 균일도와 단차 피복성

막 두께를 $d$, 공정 시간을 $\tau$로 나타내면, 두 시점 사이의 평균 증착률 $\overline{R}_\mathrm{dep}$은 다음과 같이 정의할 수 있다. 두께를 nm, 시간을 s로 입력하면 결과는 nm/s이다. 이는 측정 구간의 평균이며, 성장 전 과정에서 속도가 일정하다는 가정은 포함하지 않는다.[1,13]

$$
\overline{R}_\mathrm{dep}
=\frac{d(\tau_2)-d(\tau_1)}{\tau_2-\tau_1}.
$$

웨이퍼 내 uniformity는 서로 다른 평탄한 위치에서 두께가 얼마나 일정한지를 뜻한다. 반면 conformality는 단차를 따라 윗면·측벽·바닥에도 유사한 두께가 형성되는지를 나타낸다. 평탄한 웨이퍼에서 두께가 균일하더라도 깊은 홀의 내부는 제대로 덮이지 않을 수 있다.[1,5]

이 문서에서는 step coverage (SC), 즉 단차 피복성을 비교하기 위해 윗면 두께 $d_\mathrm{top}$을 기준으로 측벽과 바닥의 두께를 각각 정규화한다. 구조의 깊이 $h$와 입구 폭 $w$로 aspect ratio (AR)를 정의한다. 모든 길이를 같은 단위로 넣으면 아래 값들은 무차원이다. 두께는 각 위치의 표면에 수직인 방향으로 측정한다.[1,5]

$$
\begin{aligned}
SC_\mathrm{side}&=\frac{d_\mathrm{side}}{d_\mathrm{top}},\qquad
SC_\mathrm{bottom}=\frac{d_\mathrm{bottom}}{d_\mathrm{top}},\\
AR&=\frac{h}{w}.
\end{aligned}
$$

두 피복 비율이 1에 가까우면 선택한 측정 위치의 두께가 윗면과 비슷하다는 뜻이다. 그러나 한 위치의 비율만으로 전체 측벽을 대표할 수는 없다. 따라서 피복 비율을 보고할 때에는 측정 위치를 함께 제시한다.[1,5]

!!! info "[Measurement]"
    공정 시간을 달리한 시편에서 두께를 측정하고 위의 차분식으로 평균 증착률을 구한다. 웨이퍼의 위치별 두께 분포와 구조 내부의 단면 두께는 별도로 기록한다. 단면의 윗면·측벽·바닥 두께로 피복 비율을 계산할 때에는 측벽 측정 깊이와 구조의 폭·깊이도 함께 보고한다. 단면 관찰과 두께 분포의 예시는 Cremers 등의 원문 §III에서 확인할 수 있다.[1,5]

## 2. PVD: 물리적 방출과 기하학적 수송

### (1) Evaporation

Evaporation은 공급원을 가열하여 기화시킨 뒤 기판에 응축시키는 방법이다. 저항 가열은 보트나 필라멘트 등을 사용하고, electron-beam evaporation은 전자빔으로 공급원을 국소적으로 가열한다. 전자빔 가열에서는 도가니 전체의 온도를 올리는 방식과 다른 열적 조건으로 공급원을 증발시킬 수 있다.[3,4]

공급원의 온도는 증기압과 방출률에 영향을 준다. 하지만 기판에서 얻는 두께는 방출률만으로 결정되지 않는다. 공급원과 기판의 거리, 상대적인 방향 및 표면에 남는 비율도 필요하다. 방출원을 기준으로 여러 방향으로 퍼져 나간 입자 가운데 기판에 입사한 부분만 막 형성에 기여하기 때문이다.[3,4]

잔류 기체와의 충돌을 무시할 만큼 평균 자유 경로가 길면, 공급원에서 기판까지의 수송은 직선 경로로 근사할 수 있다. 이 조건에서 돌출부나 홀의 입구가 경로를 가리면 shadowing이 생긴다.[2,4]

따라서 평탄한 금속막에 적합한 증발 조건을 깊은 구조에 그대로 적용해서는 안 된다. 공급원과 기판의 기하학적 관계를 바꾸면 입사 조건이 바뀌므로, 표면별 두께를 확인하면서 원하는 방향성과 피복성을 갖추었는지 판단한다.[2,4]

### (2) Sputtering

Sputtering은 이온 등의 고에너지 입자가 고체 target에 충돌하여 target 원자를 방출시키는 과정이다. 대표적인 증착 구성에서는 플라즈마의 Ar 이온을 target 쪽으로 가속하고, 방출된 물질이 기판에 쌓이도록 한다. Evaporation과 달리 방출의 직접 원인은 공급원의 가열에 의한 기화가 아니라 충돌에 따른 운동량 전달이다.[10,11]

입사 이온 수를 $N_\mathrm{ion}$, 그 충돌로 target에서 방출된 원자 수를 $N_\mathrm{ejected}$라 하면 sputtering yield $Y$는 다음과 같이 정의한다. 이는 이온 한 개당 방출 원자 수라는 무차원 평균이며, 기판에 도달한 원자 수를 뜻하지 않는다.[10,11]

$$
Y=\frac{N_\mathrm{ejected}}{N_\mathrm{ion}}.
$$

Yield는 입사 이온의 에너지에 의존한다. 이온 에너지를 바꾸면 단순히 가열 온도만 달라지는 것이 아니라 충돌에 의한 방출 조건이 변한다. 또한 target에서 방출된 뒤의 기체 충돌과 입사 방향 분포가 막의 피복에 영향을 주므로, 높은 yield가 곧 높은 바닥 피복 비율을 의미하지는 않는다.[10,11]

Sputtering에서도 입사각의 분포와 shadowing을 고려해야 한다. 압력과 장비 형상에 따라 기판에 도달하는 입자의 방향 분포가 달라지며, 평탄한 표면의 증착률과 좁은 구조 안의 피복성은 별도로 평가한다. 따라서 ‘PVD는 언제나 동일한 피복성을 갖는다’는 비교 대신 실제 증착 조건과 단면 두께를 함께 제시하는 것이 적절하다.[1,11]

## 3. CVD: 기체 수송과 표면 반응

### (1) 일차 반응과 정상상태 모델

CVD의 성장률은 전구체가 기판 가까이 도달하는 속도와, 도달한 전구체가 표면에서 소비되는 속도의 영향을 함께 받는다. 실제로는 흡착, 반응, 부산물 탈착 및 배출이 이어지지만, 다음 모델에서는 기체 전달과 유효 표면 반응의 두 단계로 묶는다. 한 종류의 제한 전구체에 대한 일차 반응을 가정하고, 기상 반응·역반응과 표면 축적을 무시하는 정상상태 근사이다.[1,12]

주 기체 흐름과 표면 바로 위에서의 전구체 수농도를 각각 $C_g$, $C_s$로 두고 단위는 $\mathrm{m^{-3}}$로 정한다. 기체 전달 계수 $h_g$와 일차 표면 반응 계수 $k_s$는 모두 m/s이다. 표면으로 향하는 전달 플럭스 $J_\mathrm{tr}$와 표면에서 소비되는 플럭스 $J_\mathrm{rxn}$의 양의 방향을 기판으로 정하면 다음과 같다.[1,12]

$$
J_\mathrm{tr}=h_g(C_g-C_s),\qquad
J_\mathrm{rxn}=k_sC_s.
$$

두 플럭스의 단위는 $\mathrm{m^{-2}\,s^{-1}}$이며 전구체 입자 수를 센다. 표면에 전구체가 계속 축적되지 않는 정상상태에서는 두 값이 같다. 이를 $J$로 놓고 위의 두 식을 풀면 표면 농도와 순소비 플럭스를 얻는다.[1,12]

$$
\begin{aligned}
C_s&=\frac{h_g}{h_g+k_s}C_g,\\
J&=\frac{h_gk_s}{h_g+k_s}C_g=k_\mathrm{eff}C_g,\\
\frac{1}{k_\mathrm{eff}}&=\frac{1}{h_g}+\frac{1}{k_s}.
\end{aligned}
$$

유효 계수 $k_\mathrm{eff}$ 역시 m/s이다. 이 식은 기체 전달과 표면 반응 중 느린 과정이 전체 공급을 제한한다는 뜻이다. 양의 계수에 대해 $k_\mathrm{eff}$는 $h_g$와 $k_s$ 각각보다 작다. 따라서 전달과 반응의 두 단계가 직렬로 필요한 이 모델에서는 어느 한 단계의 플럭스만으로 전체 성장률을 과대평가할 수 있다.[1,12]

전구체 한 개가 소비될 때 고체에 편입되는 유효 부피를 $\Omega_\mathrm{inc}$로 두면 두께 성장률은 아래와 같이 변환한다. $\Omega_\mathrm{inc}$의 단위는 전구체 한 개당 $\mathrm{m^3}$이며, 화학량론과 고체의 수밀도를 포함한다. 예를 들어 전구체 한 개당 고체 원자 하나가 편입되고 고체 원자 수밀도가 $n_s$이면 $\Omega_\mathrm{inc}=1/n_s$이다.[1,12]

$$
R_\mathrm{dep}=\Omega_\mathrm{inc}J.
$$

이 관계로 얻는 성장률의 단위는 m/s이다. 플럭스가 전구체 분자를 세는지, 고체 원자를 세는지 먼저 정하지 않고 질량밀도나 원자 수밀도로 나누면 단위 또는 화학량론이 어긋난다. 위의 식은 편입 효율과 막 밀도를 주어진 값으로 처리하는 두께 변환이며, 그 값 자체를 수송 모델이 예측하는 것은 아니다.[1,12]

### (2) 반응 제한과 전달 제한

아래 표는 위 모델의 두 극한을 비교한다. ‘제한’은 해당 단계만 존재한다는 뜻이 아니라, 다른 단계보다 전체 성장에 더 큰 저항을 준다는 뜻이다.[1,12]

| 영역 | 계수의 관계와 근사 | 표면 농도와 공정 해석 |
| --- | --- | --- |
| Surface-reaction-limited | $k_s\ll h_g$, $J\approx k_sC_g$ | $C_s\approx C_g$이며 전구체는 공급되지만 반응이 느리다. 온도에 따른 반응 계수 변화가 중요하다. |
| Mass-transport-limited | $h_g\ll k_s$, $J\approx h_gC_g$ | $C_s\ll C_g$이며 빠른 반응이 표면 부근 전구체를 소모한다. 유동과 기체 전달의 균일성이 중요하다. |

두 극한 사이에서는 어느 하나의 근사식 대신 결합식을 사용한다. 온도가 증가할 때 반응 속도가 기체 전달보다 빠르게 증가하는 공정에서는 반응 제한에서 전달 제한으로 넘어갈 수 있다. 그러므로 온도를 높였는데 성장률 증가가 둔해졌다는 관측은 전달 제한과 일관될 수 있지만, 그 사실만으로 모든 기상·표면 반응을 식별한 것은 아니다.[1,12]

반응기 규모의 전달과 미세 구조 안의 전달도 구분해야 한다. 웨이퍼 위의 주 흐름이 균일하더라도 깊은 구조 안에서는 표면 소모와 제한된 수송 때문에 전구체 농도가 낮아질 수 있다. 위의 단일 $C_s$ 모델은 공간별 농도 분포를 풀지 않으므로, 이 식만으로 단차 피복성을 계산할 수 없다.[1,5]

### (3) 압력과 반응 활성화에 따른 구분

Atmospheric-pressure CVD (APCVD)와 low-pressure CVD (LPCVD)는 주로 압력 조건을 구별하며, plasma-enhanced CVD (PECVD)는 반응 활성화에 플라즈마를 사용하는 방식을 가리킨다. 따라서 압력과 활성화 방법은 서로 다른 분류 축이다.[1,12]

| 방식 | 대표적인 조절 수단 | 공정 해석의 초점 |
| --- | --- | --- |
| APCVD | 대기압 부근의 기체 유동과 기판 온도 | 전달 제한 조건에서는 유동·경계층 변화가 균일도에 영향을 준다.[1,12] |
| LPCVD | 낮은 압력과 열적 반응 | 압력을 낮추면 기체 전달 조건이 달라져 반응 제한으로 운전할 수 있는 범위가 바뀐다.[1,12] |
| PECVD | 플라즈마에 의한 반응종 활성화 | 열만 사용하는 경우보다 낮은 기판 온도에서 필요한 반응을 진행시키는 데 이용한다.[2,12] |

이 명칭들만으로 막의 조성·밀도·응력이나 전기적 특성이 결정되지는 않는다. PECVD로 낮은 온도에서 막을 형성할 수 있다는 사실도, 높은 온도에서 형성한 막과 같은 특성을 보장하지 않는다. 공정 비교에는 성장률뿐 아니라 실제 막의 특성과 기판이 허용하는 열적 조건을 포함해야 한다.[1,2,12]

## 4. MOCVD: 전구체 공급과 화합물 반도체 성장

### (1) 유기금속 전구체와 표면 성장

MOCVD는 유기금속 전구체를 이용하는 CVD 계열의 공정이다. 기체 공급·분해·표면 반응을 제어하면서 화합물 반도체의 조성과 층 두께를 형성한다. 유기금속이라는 명칭이 모든 반응물이 유기금속이어야 한다는 뜻은 아니다.[9,15,16]

GaN 성장의 대표적인 조합은 Ga 공급원인 trimethylgallium (TMGa)과 N 공급원인 암모니아 $\mathrm{NH_3}$이다. 두 반응물의 공급량뿐 아니라 분해되어 실제 성장에 참여하는 정도가 중요하다. 전구체의 투입 몰 유량을 같게 맞추는 것이 곧 GaN 결정에서 필요한 Ga와 N의 편입량을 맞추는 방법은 아니다.[15,16]

가스 공급계에서 정한 양과 성장 표면에 실제 도달하여 반응하는 양 사이에는 수송과 화학반응이 개입한다. MOCVD를 이해할 때는 공급계의 설정값, 표면에 도달한 반응종, 고체에 편입된 양을 나누어 생각해야 한다.[9,15,16]

### (2) V/III 공급비와 해석의 한계

GaN의 TMGa–암모니아 조합에서 입력 V/III ratio를 다음과 같이 정의한다. $\dot n_{\mathrm{NH_3}}$와 $\dot n_{\mathrm{TMGa}}$는 각각 공급되는 전구체의 몰 유량이며, 같은 단위인 mol/s 또는 mol/min으로 환산한다. 이 경우 각 분자는 각각 N 원자와 Ga 원자를 하나씩 포함한다.[15,16]

$$
(V/III)_\mathrm{in}
=\frac{\dot n_{\mathrm{NH_3}}}{\dot n_{\mathrm{TMGa}}}.
$$

이 무차원 비율은 **입력 전구체의 비**이다. 성장 표면에서 반응할 수 있는 활성 N과 Ga 종의 비 또는 완성된 고체의 원자 조성비와는 구별한다. 분해 효율과 기상 부반응, 유동 조건이 개입하기 때문에 서로 다른 반응기에서 같은 입력 V/III 값을 사용했다고 해서 같은 성장 조건을 실현한 것은 아니다.[15,16]

이 구분은 조건을 바꾼 실험을 해석할 때 유용하다. 암모니아 유량을 늘리는 것과 TMGa 유량을 줄이는 것은 모두 입력 V/III를 키우지만, 두 경우의 절대 공급량과 성장률은 같지 않을 수 있다. 따라서 비율 하나만 보고 조건을 옮기지 않고 각 전구체 유량, 온도, 압력과 측정된 성장률을 함께 기록한다.[15,16]

MOCVD의 목적이 에피택셜 층이라면 막이 생겼다는 사실만으로 성공을 판단할 수 없다. 조성과 두께 외에도 성장 결정과 기판의 관계를 확인해야 한다. 앞의 CVD 모델은 수송과 반응의 경쟁을 이해하는 출발점이지만, 결정 결함이나 격자 변형을 직접 예측하지는 않는다. 이 구분은 6절에서 다룬다.[8,9]

## 5. ALD: 분리된 표면 포화반응

### (1) Temporal ALD와 spatial ALD

ALD의 핵심은 표면이 서로 분리된 반응물에 순차적으로 노출되고, 각 반응 단계가 self-limiting하게 진행된다는 점이다. Temporal ALD에서는 시간에 따라 주입과 제거를 반복한다. Spatial ALD에서는 반응물 영역을 공간적으로 나누고 기판과 공급부를 상대적으로 이동시켜 같은 표면이 각 반응물을 순서대로 만나게 한다.[5,6,13]

아래 표는 두 반응물을 사용하는 temporal ALD 한 사이클의 대표적인 구성이다. Purge는 불활성 기체와 배기 등을 이용하여 남은 기상 반응물과 부산물을 제거하는 단계이며, 이미 형성된 표면 결합을 모두 제거하는 과정이 아니다.[13,14]

| 단계 | 표면과 기체에서의 과정 | 다음 단계에 필요한 조건 |
| --- | --- | --- |
| A 주입 | A가 반응 가능한 표면 자리와 반응한다. | 목표 표면에 충분한 노출을 제공한다. |
| 첫 purge | 남은 A와 기상 부산물을 제거한다. | B와 A의 기상 혼합을 억제한다. |
| B 주입 | B가 A 반응 후의 표면과 반응한다. | 다음 A 반응에 필요한 표면 상태를 만든다. |
| 둘째 purge | 남은 B와 기상 부산물을 제거한다. | 다음 사이클의 A와 분리한다. |

Self-limiting은 충분히 노출된 표면에서 같은 반응물의 추가 공급이 성장량을 계속 늘리지 못한다는 뜻이다. 한 사이클이 반드시 결정학적 원자층 하나를 완성한다는 뜻은 아니다. 실제 성장량은 반응 자리와 표면 화학에 의존하므로 ‘원자층’이라는 이름만으로 사이클 수를 원자층 수로 바꾸어서는 안 된다.[5,13,14]

Spatial ALD에서도 표면의 순차 노출과 반응물 간 분리는 유지되어야 한다. 공간적으로 분리된 공급 영역에 가스가 연속 주입되더라도, 이동하는 표면이 순서대로 포화반응을 겪으면 ALD의 원리에 부합한다. Temporal ALD의 pulse–purge 순서를 모든 ALD 장비의 시간표로 해석하지 않는 이유이다.[5,6]

### (2) 사이클당 성장량과 포화 검증

Growth per cycle (GPC)은 사이클당 두께 증가량이다. 사이클 수 $N_1$, $N_2$에서 측정한 두께를 각각 $d(N_1)$, $d(N_2)$라 하면 선택한 구간의 평균값을 다음과 같이 계산한다. 두께가 nm이면 단위는 nm/cycle이다.[5,13]

$$
\overline{\mathrm{GPC}}
=\frac{d(N_2)-d(N_1)}{N_2-N_1}.
$$

이 식은 두께 자료의 기울기에 대한 정의이다. 사이클 수와 두께가 선형인 구간에서는 일정한 GPC로 두께를 설계할 수 있다. 그러나 선형성만으로 각 반응의 포화를 입증할 수는 없다. A와 B의 공급을 각각 바꾸어 추가 노출에 따른 성장량 변화를 확인해야 하며, 충분한 purge 조건도 별도로 점검해야 한다.[13,14]

Purge가 부족하면 서로 분리해야 할 반응물이 함께 남아 비포화 반응이 기여할 수 있다. 또한 온도를 높이면 전구체의 열분해가 추가 성장에 기여할 수 있다. 이런 경우 두께가 더 빨리 늘었다는 결과를 ALD의 포화 성장량이 커졌다고 바로 해석하면 안 된다.[5,14]

!!! info "[Measurement]"
    먼저 한 반응물의 노출 조건을 고정하고 다른 반응물의 노출량을 늘리며 위 식으로 GPC를 비교한다. A와 B를 바꾸어 같은 확인을 수행한 뒤 purge 조건도 변화시킨다. 이때 온도와 두께 추출 구간을 유지한다. 성장량이 포화되는지와 기상 혼합이 제거되었는지는 별개의 질문이므로, 한 번의 두께 측정으로 두 조건을 동시에 검증했다고 해석하지 않는다.[13,14]

### (3) 고종횡비 구조의 피복 조건

ALD에서 입구 부근이 먼저 포화되면 이후의 반응물이 더 안쪽의 미반응 표면에 도달할 수 있다. 이것이 복잡한 구조를 균일하게 덮는 데 유리한 이유이다. 그러나 깊은 구조의 모든 위치가 충분히 노출되어야 하므로, 평탄한 시편에서 얻은 포화 조건을 그대로 적용해서 내부 피복을 보장할 수는 없다.[5,13,14]

반응물의 수송, 표면에서 소모되는 정도, 구조의 깊이와 폭은 필요한 노출 조건을 함께 결정한다. 따라서 ALD의 self-limiting 성질은 높은 conformality를 가능하게 하는 원리이며, 모든 형상과 모든 주입 시간에서 완전한 피복을 보장하는 장비 사양은 아니다.[5,13,14]

실제 비교에서는 1절의 피복 비율과 깊이에 따른 두께 분포를 함께 사용한다. 구조가 실제로 어떻게 덮이는지는 [Hausmann 등의 원문 Fig. 4](https://gordon.faculty.chemistry.harvard.edu/sites/g/files/omnuum7801/files/gordon/files/aldhf_3.pdf#page=5)의 단면 사진에서 볼 수 있다. 해당 결과는 그 논문의 전구체·노출·형상 조건에 대한 사례이며, 임의의 ALD 공정에 같은 피복 결과를 부여하는 근거로 사용하지 않는다.[5,14]

## 6. Epitaxy: 결정 관계와 격자 변형

### (1) MOCVD와 MBE의 성장 조건

에피택셜 성장에서는 공급된 종이 기판의 결정학적 질서를 따라 편입될 조건을 마련한다. 예를 들어 Si 위의 Si 성장과 서로 다른 화합물 반도체 사이의 성장은 기판과 막의 재료 관계가 다르지만, 모두 기판과 성장 결정의 방향 관계를 다룬다. 공급 방법을 선택한 뒤에도 표면 상태와 결정 성장 조건을 별도로 조절해야 한다.[2,8,9]

MBE는 초고진공에서 원자·분자 빔을 가열된 결정 기판에 공급하는 대표적인 방법이다. 전형적인 고체 공급원 MBE에서는 effusion cell의 온도로 빔의 공급률을 조절하고 shutter로 공급을 전환한다. MBE라는 이름만으로 모든 공급원이 고체라고 한정할 수는 없으며, 기체 공급원 등을 이용하는 변형도 있다.[8,9,17]

장치 구성은 [University of Texas at Austin의 MBE 설명 §2와 Fig. 2.1](https://lase.ece.utexas.edu/introduction-mbe-growth)에서 확인할 수 있다. 공급원을 향하는 가열 기판, 여러 공급원과 그 앞의 shutter를 구분하여 읽으면, 기체 흐름과 전구체 반응을 중심으로 설명한 MOCVD와의 차이를 이해할 수 있다. 두 방법 모두 층 두께와 조성을 제어하지만 공급의 물리적 조건과 표면 반응은 동일하지 않다.[8,9,17]

### (2) Lattice mismatch와 실제 변형률

Heteroepitaxy에서는 박막과 기판의 자연 격자 주기가 다를 수 있다. 충분히 얇은 층이 기판의 면내 주기에 맞춰 변형되면 coherent 또는 pseudomorphic 상태를 유지할 수 있다. 두께와 불일치가 커지면 변형 에너지와 전위 형성 에너지의 경쟁으로 misfit dislocation을 통한 완화가 가능해진다.[8,18]

여기서는 동일한 면내 방향의 1:1 격자 대응과 두꺼운 기판을 가정한다. 같은 온도에서 무변형 박막과 기판의 격자상수를 각각 $a_f$, $a_s$라 하고, 격자 불일치 $f$의 부호를 다음과 같이 정한다. 두 값은 같은 길이 단위로 사용하므로 $f$는 무차원이다.[8,18]

$$
f=\frac{a_f-a_s}{a_s}.
$$

이 값은 두 물질의 무변형 격자상수 차이이며, 성장한 박막이 실제로 얼마나 늘어나거나 줄었는지를 직접 나타내지 않는다. 성장 후 박막의 면내 격자상수를 $a_\parallel$이라 하면 실제 면내 변형률은 무변형 박막을 기준으로 다음과 같이 정의한다. 완전한 coherent 상태에서 $a_\parallel=a_s$를 대입하면 오른쪽의 관계가 얻어진다.[8,18]

$$
\varepsilon_\parallel
=\frac{a_\parallel-a_f}{a_f},\qquad
\varepsilon_\parallel^\mathrm{coherent}
=-\frac{f}{1+f}.
$$

이는 선택한 두 정의와 coherent 조건의 대수적 결과이다. $a_f>a_s$이면 $f>0$이지만 박막의 실제 면내 변형률은 음수이므로 압축 상태이다. 작은 불일치에서만 $\varepsilon_\parallel^\mathrm{coherent}\approx-f$로 근사할 수 있다. 문헌을 비교할 때에는 mismatch의 부호뿐 아니라 분모가 기판인지 박막인지도 확인해야 한다.[8,18]

위의 coherent 변형률 관계는 박막이 기판의 면내 주기에 맞춰져 있다는 가정을 사용한다. 전위에 의해 완화된 층에는 이 관계를 그대로 적용하지 않고 실제 면내 격자상수를 사용한다.[8,18]

## 7. 공정 선택과 측정 결과의 해석

공정 이름은 출발점이며 목표 막의 모든 특성을 대신하지 않는다. 아래 표는 앞에서 설명한 원리와 실제 확인할 항목을 연결한다. 장비별 처리량이나 막 품질에 대한 보편적인 순위를 제시하는 표는 아니다.

| 목표와 비교 대상 | 우선 확인할 제어 조건 | 함께 확인할 결과 |
| --- | --- | --- |
| PVD로 평탄한 막 형성 | 방출률, 공급원–기판 기하와 입사 분포 | 웨이퍼 위치별 두께와 단차 피복 비율[1,4,11] |
| CVD 성장률과 균일도 조절 | 반응·전달 제한 영역, 온도와 유동 | 두께의 시간 변화와 공간 분포[1,12] |
| MOCVD 화합물 반도체 성장 | 각 전구체의 절대 유량과 입력 비, 온도·압력 | 성장률, 조성·불순물 및 결정 상태[15,16] |
| ALD로 구조 내부 피복 | 각 반응물의 포화 노출과 반응물 분리 | GPC, 깊이에 따른 두께와 바닥 피복 비율[5,13,14] |
| 에피택셜 층 형성 | 기판·막의 결정 관계와 표면 성장 조건 | 격자 변형과 완화 여부[8,18] |

두께 측정은 성장률을 평가하는 데 필요하지만, 두께가 맞는다는 사실만으로 조성이나 결정 품질이 맞는다고 결론내릴 수 없다. 또한 윗면·측벽·바닥의 두께가 비슷한 conformal coating과 빈 공간 전체를 채우는 gap filling은 같은 목표가 아니다. 좁은 공간을 채우다가 입구가 닫히면 내부에 빈 공간이 남을 수 있으므로, 목표가 피복인지 충전인지 먼저 정해야 한다.[1,2]

비교 자료에는 두께의 정의와 측정 위치, 온도·압력, 공급량 또는 사이클 수 및 시편 형상을 함께 적는다. 이는 서로 다른 공정의 숫자를 같은 의미로 비교하기 위한 조건이다. 예를 들어 평탄한 시편의 GPC와 깊은 홀 바닥의 GPC를 구분하지 않으면, 반응 자체의 성장량 차이와 내부 노출 부족을 혼동할 수 있다.[1,5,14]

증착 후의 형상 가공은 [Etching](etching.md)에서 다룬다.

## 8. 핵심 정리

- PVD와 CVD는 물질을 방출·공급하고 막으로 만드는 원리로 구분하며, ALD는 분리된 순차 포화반응을 이용한다. Spatial ALD까지 포함하려면 시간 분리만으로 ALD를 정의하지 않는다.[3,4,5,6]
- CVD의 일차 정상상태 모델에서는 기체 전달과 표면 반응이 함께 플럭스를 제한한다. 이 플럭스를 두께 성장률로 바꿀 때에는 고체 수밀도와 편입 화학량론이 필요하다.[1,12]
- MOCVD의 입력 V/III는 전구체 공급비이며, 표면의 활성종 비나 고체 조성비와 구별한다.[15,16]
- ALD의 포화반응과 충분한 노출은 함께 확인해야 한다. 일정한 GPC나 평탄한 시편의 균일도만으로 깊은 구조의 피복성을 판단할 수 없다.[5,13,14]
- Epitaxy는 기판과 성장 결정의 관계이다. 공급 방식과 별도로 격자 불일치, 실제 변형률과 완화를 구별해야 한다.[8,9,18]

## 9. 참고문헌

1. J. Hoyt, “Lecture 17: Chemical Vapor Deposition,” *6.774 Physics of Microfabrication: Front-End Processing*, MIT OpenCourseWare (2004), transcript, pp. 1–13. [강의 원문](https://ocw.mit.edu/courses/6-774-physics-of-microfabrication-front-end-processing-fall-2004/1sSADV3Iiuifbp51EEBEB0v15lnIZkjBA_transcript.pdf).
2. S. Pennathur, “Lecture 3,” *ME 141B: The MEMS Class*, University of California, Santa Barbara (2010), slides 3, 9–15, 19–24. [강의 원문](https://sites.engineering.ucsb.edu/~sumita/courses/Courses/ME141B/ME141B_lecture_3_F10.pdf).
3. A. G. Andreou, “Film Deposition,” Johns Hopkins University 520/580.495 (2000), including R. B. Darling, *Physical Vapor Deposition*, pp. 7–31. [강의 원문](https://pages.jh.edu/aandreo1/495/Archives/2002/LectureNotes/FilmDeposition.pdf).
4. C. A. Mack, “Evaporation, parts 1–2,” *CHE323/CHE384 Chemical Processes for Micro- and Nanofabrication* (2013), Lectures 20–21. [Lecture 20](https://www.lithoguru.com/scientist/CHE323/Lecture20.pdf), [Lecture 21](https://www.lithoguru.com/scientist/CHE323/Lecture21.pdf).
5. V. Cremers, R. L. Puurunen, and J. Dendooven, “Conformality in Atomic Layer Deposition: Current Status Overview of Analysis and Modelling,” *Applied Physics Reviews* **6**, 021302 (2019), §§I–III, V–VI. [DOI: 10.1063/1.5060967](https://doi.org/10.1063/1.5060967), [저자 기관 원문](https://backoffice.biblio.ugent.be/download/8614054/8614061).
6. P. Poodt, “Spatial Atomic Layer Deposition for Large-Area and Flexible Electronics,” *NEVAC Blad* **58**(2), 29–31 (2020). [기관 저장소 원문](https://pure.tue.nl/ws/portalfiles/portal/151430173/NEVAC_ALD_Issue_2020_Poodt.pdf).
7. X. Klemenschits, *Emulation and Simulation of Microelectronic Fabrication Processes*, TU Wien doctoral thesis (2022), §5.1.2. [기관 원문](https://www.iue.tuwien.ac.at/phd/klemenschits/18.html).
8. Laboratory for Advanced Semiconductor Epitaxy, “An Introduction to MBE Growth,” University of Texas at Austin, §§2, 5–6. [기관 원문](https://lase.ece.utexas.edu/introduction-mbe-growth).
9. C. G. Fonstad, “Lecture 7: Epitaxy Techniques and Considerations,” *6.772 Compound Semiconductor Devices*, MIT OpenCourseWare (2003), slides 3–7, 13–15. [강의 원문](https://ocw.mit.edu/courses/6-772-compound-semiconductor-devices-spring-2003/8c305146942ad5a5ad1c559a6ecae11c_Lecture7v2.pdf).
10. NPTEL, “Lecture 38: Deposition and Fabrication Techniques I,” *Advances in Spintronic Materials, Technology and Devices*, §Sputtering technique. [강의 원문](https://archive.nptel.ac.in/content/storage2/courses/115103039/module16/lec38/6.html).
11. C. A. Mack, “Sputtering, parts 1–2,” *CHE323/CHE384 Chemical Processes for Micro- and Nanofabrication* (2013), Lectures 22–23. [Lecture 22](https://www.lithoguru.com/scientist/CHE323/Lecture22.pdf), [Lecture 23](https://www.lithoguru.com/scientist/CHE323/Lecture23.pdf).
12. C. A. Mack, “Chemical Vapor Deposition, parts 1–2,” *CHE323/CHE384 Chemical Processes for Micro- and Nanofabrication* (2013), Lectures 24–25. [Lecture 24](https://www.lithoguru.com/scientist/CHE323/Lecture24.pdf), [Lecture 25](https://www.lithoguru.com/scientist/CHE323/Lecture25.pdf).
13. S. M. George, “Atomic Layer Deposition: An Overview,” *Chemical Reviews* **110**, 111–131 (2010), pp. 112–114. [DOI: 10.1021/cr900056b](https://doi.org/10.1021/cr900056b), [대학 공개 사본](https://www.seas.upenn.edu/~nanosop/documents/overviewofALD.pdf).
14. D. M. Hausmann, E. Kim, J. Becker, and R. G. Gordon, “Atomic Layer Deposition of Hafnium and Zirconium Oxides Using Metal Amide Precursors,” *Chemistry of Materials* **14**, 4350–4358 (2002), §§II–IV. [DOI: 10.1021/cm020357x](https://doi.org/10.1021/cm020357x), [저자 기관 원문](https://gordon.faculty.chemistry.harvard.edu/sites/g/files/omnuum7801/files/gordon/files/aldhf_3.pdf).
15. T. Ciarkowski *et al.*, “Connection between Carbon Incorporation and Growth Rate for GaN Epitaxial Layers Prepared by OMVPE,” *Materials* **12**, 2455 (2019), §§1–3. [DOI: 10.3390/ma12152455](https://doi.org/10.3390/ma12152455), [공개 원문](https://pmc.ncbi.nlm.nih.gov/articles/PMC6695831/).
16. Y. Zhang, Z. Chen, K. Zhang, Z. Feng, and H. Zhao, “Laser-Assisted Metal–Organic Chemical Vapor Deposition of Gallium Nitride,” *physica status solidi (RRL) – Rapid Research Letters*, 2100202 (2021), §§1–2, 4. [DOI: 10.1002/pssr.202100202](https://doi.org/10.1002/pssr.202100202), [공개 원문](https://d-nb.info/1233639382/34).
17. A. Ptak, “Principles of Molecular Beam Epitaxy,” in *Handbook of Crystal Growth*, 2nd ed., Vol. III, Part A, pp. 161–192 (2015), abstract. [DOI: 10.1016/B978-0-444-63304-0.00004-4](https://doi.org/10.1016/B978-0-444-63304-0.00004-4), [저자 기관 초록](https://research-hub.nlr.gov/en/publications/chapter-4-principles-of-molecular-beam-epitaxy/).
18. S. Smirnov, “Critical Thickness and Dislocations,” §3.1.1, TU Wien doctoral thesis. [기관 원문](https://www.iue.tuwien.ac.at/phd/smirnov/node68.html).
