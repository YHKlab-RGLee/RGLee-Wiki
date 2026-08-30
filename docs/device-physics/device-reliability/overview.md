---
description: 소자 열화와 고장을 구분하고 스트레스 시험, 수명 분포와 가속 모형의 공통 규약을 설명
---

# Device reliability: Overview

**Device reliability**는 정해진 사용 조건과 기간 동안 소자가 요구 기능을 유지할 확률적 능력을 다룬다. 성능 열화는 문턱전압이나 저항처럼 연속적인 물리량의 변화이고, 고장은 그 변화가 미리 정한 기능 한계를 넘은 사건이다. 따라서 신뢰성 평가는 물리적 열화 메커니즘, 측정 가능한 열화량, 고장 판정 기준과 사용 조건의 시간 이력을 함께 명시해야 한다.[1–4]

이 문서는 bias temperature instability (BTI), hot-carrier degradation (HCD), time-dependent dielectric breakdown (TDDB)과 [interconnect reliability](interconnect-reliability.md)의 공통 개념과 통계 규약을 정의한다. 각 현상의 세부 내용은 [BTI](bias-temperature-instability.md), [HCD](hot-carrier-degradation.md), [TDDB](time-dependent-dielectric-breakdown.md) 문서에서 다루며, 수명 자료의 적합과 사용 조건으로의 외삽은 [reliability modeling](reliability-modeling.md)에서 이어서 설명한다.

이 공통 규약을 먼저 고정하면 개별 문서의 열화량과 고장 기준을 같은 의미로 비교할 수 있으며, 마지막에는 각 메커니즘에서 얻은 수명 자료를 동일한 통계·외삽 절차에 연결할 수 있다.

## 1. 열화, 고장과 수명

### (1) 열화량과 고장 기준

열화량 $D(t)$는 초기 상태로부터의 변화를 수치화한 값이다. Metal-oxide-semiconductor field-effect transistor (MOSFET)에서는 $\Delta V_T$, $\Delta g_m$, $\Delta I_\mathrm{D}$를, 배선에서는 $\Delta R/R_0$를 사용할 수 있다. 수명 $t_f$는 시험 전에 정한 임계값 $D_\mathrm{crit}$에 처음 도달한 시간으로 정의한다.[1–4]

$$
t_f=\inf\{t:D(t)\ge D_\mathrm{crit}\}
$$

같은 시편과 스트레스에서도 $D_\mathrm{crit}$를 바꾸면 보고되는 수명이 달라진다. 파괴가 일어나기 전의 매개변수 이동을 고장으로 판정할 수도 있고, 절연막의 전기적 breakdown처럼 불연속 사건을 직접 판정할 수도 있다. 그러므로 “수명”에는 열화량, 기준값, 판독 바이어스와 측정 지연을 반드시 붙여야 한다.[1–4]

### (2) 확률 변수로서의 수명

결함의 위치와 수, 미세구조와 공정 변동 때문에 동일 조건의 소자도 서로 다른 $t_f$를 갖는다. 누적 고장 확률 $F(t)$와 생존 확률 $R(t)$는

$$
F(t)=P(t_f\le t), \qquad R(t)=1-F(t)
$$

로 정의한다. Hazard rate $h(t)$는 시간 $t$까지 살아남은 표본이 직후에 고장날 조건부 비율이다.[1,2,5,6]

$$
h(t)=\frac{f(t)}{R(t)}
$$

$f(t)=dF/dt$이다. 평균 수명 하나만으로는 분포의 폭이나 초기 꼬리를 알 수 없으므로, 고장 확률 또는 분위수와 함께 보고한다.[1,2,5,6]

## 2. 스트레스와 사용 조건

### (1) Mission profile

**Mission profile**은 시간에 따른 전압, 전류, 온도, 듀티비와 동작 상태의 집합이다. 열화 속도는 이 변수들에 비선형적으로 의존할 수 있으므로 평균 전압이나 평균 온도만으로 실제 이력을 대체하면 오차가 생긴다. 회복이 있는 BTI, 전류 방향이 바뀌는 배선, 자가 발열이 큰 트랜지스터에서는 스트레스 순서와 지속 시간도 중요하다.[1,3,4,7,8]

| 범주 | 기록할 조건 | 대표적인 혼동 요인 |
| --- | --- | --- |
| 전기적 스트레스 | 각 단자 전압, 전류 밀도, 파형, 듀티비 | 기생 저항, overshoot, 전류 집중 |
| 열적 스트레스 | 소자 온도, 주변 온도, 열 천이 시간 | chuck 온도와 실제 접합 온도의 차이 |
| 시간 조건 | 스트레스·회복·판독 시간 | 측정 지연 중의 회복 또는 추가 열화 |
| 시편 조건 | 면적, 형상, 공정 소자군, 표본 수 | 면적 효과, 공정·웨이퍼 내 상관 |

### (2) 가속 수명 시험

Accelerated life test (ALT)는 사용 조건보다 높은 스트레스에서 관측 시간을 줄인 뒤, 가속 모형과 수명 분포를 함께 적합하여 사용 조건의 분포를 추정하는 시험이다. 유효한 ALT는 여러 스트레스 셀을 포함하고, 시험 범위에서 같은 지배 고장 메커니즘이 유지되어야 한다.[1,2,5]

Acceleration factor (AF)는 두 조건에서 같은 수명 분위수의 비로 정의할 수 있다.

$$
AF(S_1,S_2)=\frac{t_p(S_1)}{t_p(S_2)}
$$

$S$는 스트레스 조건, $t_p$는 누적 고장 확률 $p$에 해당하는 수명이다. 이 비가 분위수와 무관하다는 가정은 분포의 모양이 스트레스에 따라 바뀌지 않는 가속 모형에서만 성립한다.[1,2,5,6]

!!! warning "[Interpretation Caveat]"
    스트레스를 높여 새로운 고장 메커니즘을 활성화하면 짧아진 시험 시간은 사용 조건의 수명을 대표하지 않는다. 각 스트레스 셀에서 물리적 고장 분석, 열화 신호와 분포 모양을 비교하고, 메커니즘이 달라진 자료는 하나의 가속식으로 합치지 않는다.[1,2,5]

## 3. 고장 메커니즘의 분리

서로 다른 메커니즘은 발생 위치, 구동력과 관측 신호가 다르다. 아래 분류는 측정 계획의 출발점이며, 실제 소자에서는 둘 이상의 메커니즘이 동시에 기여할 수 있다.[1,3,4,7,8]

| 메커니즘 | 주된 위치와 구동 조건 | 대표 관측량 | 이 문서군의 핵심 모형 |
| --- | --- | --- | --- |
| BTI | 게이트 절연막·계면, 게이트 바이어스와 온도 | $\Delta V_T$, $\Delta I_D$ | 트랩 점유·생성과 회복 |
| HCD | 드레인 쪽 고전계 영역, $V_G$–$V_D$ 조합 | $\Delta I_D$, $\Delta g_m$, $\Delta V_T$ | 고에너지 운반자에 의한 결함 생성 |
| TDDB | 게이트 절연막, 높은 산화막 전기장 | 누설 증가, soft·hard breakdown | 결함 축적과 percolation |
| Electromigration | 금속 배선과 via, 전류 밀도와 온도 | $\Delta R$, open·short | 원자 flux와 back stress |

하나의 단자 신호가 하나의 원인을 뜻하지는 않는다. 예를 들어 $\Delta V_T$는 BTI와 HCD 모두에서 나타날 수 있고, 게이트 전류 증가는 정상 터널링, stress-induced leakage current (SILC) 또는 breakdown의 결과일 수 있다. 바이어스, 공간적 위치, 온도와 시간 의존성을 함께 사용하여 원인을 분리해야 한다.[1,3,4,8]

## 4. 측정 설계와 보고

### (1) 시험 행렬과 대조군

신뢰성 시험은 한 개의 높은 스트레스 조건에서 수명을 얻는 절차가 아니라, 사용 조건으로의 외삽에 필요한 모형을 식별하는 실험 설계이다. 최소한 스트레스를 받지 않은 대조군, 서로 다른 크기의 가속 스트레스 셀과 사용 조건에 가까운 검증 셀을 구분한다. 각 셀에는 시편 수만 배정하지 말고 wafer·lot·소자 형상이 한 스트레스에 치우치지 않도록 무작위화하거나 block으로 기록한다. 그렇지 않으면 공정 차이를 전압 또는 온도 효과로 잘못 적합할 수 있다.[1,2,5]

| 시험 셀 | 주된 목적 | 필요한 비교 | 판정할 수 없는 내용 |
| --- | --- | --- | --- |
| 대조군 | 장비 drift와 보관 중 변화 확인 | 시험 전·후의 동일 판독 조건 | 가속식의 기울기 |
| 복수 가속 셀 | 전압·전류·온도 의존성 식별 | 셀 사이의 고장 모드와 분포 모양 | 사용 조건의 직접 수명 |
| 근사용 검증 셀 | 외삽식의 중간 구간 예측 검사 | 적합에서 제외한 예측값과 관측값 | 관측 범위 밖의 장기 꼬리 |
| 구조·공정 대조군 | 형상과 공정 변동 분리 | 같은 스트레스의 wafer·lot·구조 | 다른 메커니즘의 가속 계수 |

스트레스 변수는 가능한 한 독립적으로 바꾸되, 실제 소자 온도를 함께 측정한다. 전압을 높이면 누설 전류와 자가 발열도 변하므로 외부 전압만으로 전기적 가속과 열적 가속을 분리할 수 없는 경우가 있다. 전압–온도 행렬과 저전력 대조 조건을 두면 두 효과의 상호작용을 검사할 수 있다. 시험 셀마다 고장 위치, 전류 파형과 분포 모양이 유지되는지도 확인해야 하며, 다른 고장 모드가 나타난 셀은 하나의 가속식에 강제로 합치지 않는다.[1,2,5]

표본 수는 목표 고장 확률, 예상 산포, censored 비율과 추정할 매개변수 수에 맞춰 정한다. 고장이 거의 없는 셀은 사용 조건에 가까운 생존 정보를 주지만 그 셀만으로 분포의 모양을 정할 수 없다. 반대로 모든 시편이 시험 초기에 고장나는 셀은 지나치게 강한 스트레스이거나 판독 간격이 부족할 수 있다. 두 경우 모두 단순히 시험 시간을 늘리거나 줄이는 대신 시험 행렬이 필요한 시간 범위와 고장 수를 실제로 덮는지 사전 모의와 중간 점검으로 확인한다.[2,5,6]

### (2) 시편별 자료와 추적 가능성

분포와 가속 모형은 평균 곡선이 아니라 시편별 관측으로 적합한다. 각 시편의 최소 자료 단위를

$$
z_i=\left(t_{L,i},t_{U,i},\delta_i,S_i,\boldsymbol{x}_i,m_i\right)
$$

로 둘 수 있다. $t_{L,i}$와 $t_{U,i}$는 고장 시각의 관측 하한과 상한, $\delta_i$는 고장 또는 censoring 표시, $S_i$는 전압·전류·온도와 파형을 포함한 스트레스 이력, $\boldsymbol{x}_i$는 형상·wafer·lot 같은 공변량, $m_i$는 물리적으로 판정한 고장 모드이다. 연속 측정으로 정확한 고장 시각을 얻으면 $t_{L,i}=t_{U,i}$로 두고, 시험 종료까지 고장하지 않았으면 $t_{U,i}$를 열어 둔다. 이 구분을 보존해야 interval-censored 자료와 right-censored 자료가 적합에 서로 다르게 기여한다.[1,2,5,6]

| 자료 층위 | 반드시 보존할 값 | 품질 확인 질문 |
| --- | --- | --- |
| 시편 | 원시 파형, 판독 시각, 고장 여부·모드 | 판독 간격 사이의 고장을 임의의 한 시각으로 바꾸지 않았는가? |
| 시험 셀 | 설정값과 실제 전압·전류·온도, 시편 배정 | 설정 온도와 실제 접합·배선 온도를 구분했는가? |
| 적합 결과 | 후보 분포·가속식, 매개변수와 불확실성 | Censored 시편과 기각한 자료의 이유를 포함했는가? |
| 사용 예측 | mission profile, 요구 분위수·고장 확률 | 시험 범위 밖 외삽과 모형 선택 오차를 구분했는가? |

원시 자료에서 고장 판정값으로 변환하는 규칙도 버전과 함께 고정한다. 전류 급증, 저항 증가율 또는 $\Delta V_T$ 임계값을 나중에 바꾸면 같은 원시 파형에서도 $t_f$가 달라진다. 따라서 원시 파형을 보존하고 판정 알고리즘·평활화·결측 처리·이상치 제외 규칙을 기록해야 재분석과 독립 검증이 가능하다. 고장 모드가 불명확한 시편은 임의의 대표 모드에 넣지 말고 미분류 상태와 민감도 분석을 함께 보고한다.[1–5]

!!! info "[Measurement]"
    1. 초기 전기 특성을 같은 판독 조건에서 측정한다.
    2. 전압·전류·온도·파형과 지속 시간이 정해진 스트레스를 인가한다.
    3. 판독 바이어스로 전환한 뒤 지연 시간 $t_\mathrm{delay}$를 기록하고 열화량 $D(t)$를 측정한다.
    4. 고장하지 않은 시편도 시험 종료 시각과 함께 right-censored 자료로 보존한다.
    5. 고장 시편은 전기적 신호와 물리적 고장 분석으로 메커니즘을 확인한다.

    정규화한 열화량은 일반적으로

    $$
    \delta X(t)=\frac{X(t)-X_0}{X_0}
    $$

    로 정의한다. $X_0$의 부호가 해석을 흐릴 수 있는 전류에는 $|X_0|$를 분모로 쓰고 그 규약을 밝힌다.[1–4]

!!! note "[Metric]"
    보고 항목에는 표본 수, 고장 수, censored 수, 소자 형상·면적, 모든 스트레스와 판독 조건, $D_\mathrm{crit}$, 시간 영점과 측정 지연, 적합한 분포·가속식, 매개변수의 신뢰구간을 포함한다. 평균값만 제시하거나 고장하지 않은 시편을 버리면 수명 분포가 편향될 수 있다.[1,2,5,6]

## 5. 모델의 경계

가속식은 물리 법칙 그 자체가 아니라 제한된 조건에서 확인한 모형이다. Arrhenius 온도 항, 전압의 지수식이나 거듭제곱식은 메커니즘별로 검증해야 한다. 높은 스트레스에서 맞는 식이 사용 전압의 매우 낮은 고장 확률까지 같은 형태를 유지한다는 보장은 없다.[1,2,5]

모형의 적용 범위는 시험에서 실제로 덮은 전압·온도·시간뿐 아니라 소자 형상, 재료 적층, 판독 방법과 고장 기준까지 포함한다. 같은 이름의 BTI나 TDDB 시험이라도 판독 지연이나 breakdown 판정 전류가 다르면 관측 수명은 동일한 확률변수가 아니다. 다른 공정 세대나 구조로 매개변수를 옮기기 전에 원시 열화 신호와 고장 위치가 같은 메커니즘을 가리키는지 확인하고, 적어도 일부 조건에서 독립 자료로 예측 오차를 측정한다.[1–5]

또한 통계적 적합 오차와 모형 형식의 불확실성을 구분한다. 정해진 Weibull–가속식 안에서 계산한 신뢰구간은 그 모형이 맞다는 조건부 결과이며, Weibull과 lognormal 또는 서로 다른 전압 가속식 사이의 차이를 포함하지 않는다. 여러 후보가 관측 범위에서 비슷하게 맞으면 사용 조건 예측을 후보별로 제시하고, 하나의 좁은 오차막대로 합치지 않는다. 낮은 고장 확률로 갈수록 이 모형 선택 차이가 표본 오차보다 커질 수 있다.[2,5,6]

검증 자료는 모형 선택에 사용한 자료와 분리한다. 같은 자료로 매개변수를 적합하고 성능까지 평가하면 외삽 오차를 과소평가할 수 있다. 독립 검증 셀이 부족하면 한 스트레스 셀을 제외해 예측한 뒤 관측값과 비교하고, 그 제한을 결과에 명시한다.[2,5]
검증 오차는 사용 조건에서 요구하는 수명 분위수 또는 고장 확률과 같은 정량 지표로 보고한다.

여러 독립 고장 모드가 경쟁하고 각각의 수명 $T_i$가 있을 때 시스템 수준의 첫 고장 시간은

$$
T_\mathrm{first}=\min_i T_i
$$

이다. 그러나 이 관계가 각 메커니즘의 열화량을 서로 더할 수 있다는 뜻은 아니다. BTI의 회복, TDDB의 weakest-link 면적 효과와 electromigration의 back stress처럼 고유한 상태 변수와 경계 조건을 유지한 채 메커니즘별로 예측한 뒤 결합해야 한다.[1–4,7]

## 6. 요약

- 신뢰성 수명은 열화량, 임계값, 판독 조건과 사용 이력이 붙은 확률 변수이다.
- ALT는 같은 고장 메커니즘이 유지되는 여러 스트레스 셀에서 분포와 가속 모형을 함께 추정해야 한다.
- 같은 전기적 변화가 여러 메커니즘에서 나타날 수 있으므로 바이어스·온도·시간 의존성과 고장 분석으로 원인을 분리한다.
- 고장하지 않은 시편과 불확실성을 포함해 보고하고, 검증 범위 밖의 장기·저확률 외삽은 별도로 경고한다.

## 7. 참고문헌

1. M. White and J. B. Bernstein, *Microelectronics Reliability: Physics-of-Failure Based Modeling and Lifetime Evaluation*, JPL Publication 08-5, Jet Propulsion Laboratory (2008). [PDF](https://nepp.nasa.gov/files/16365/08_102_4_%20JPL_White.pdf)
2. NIST/SEMATECH, “Acceleration models,” *e-Handbook of Statistical Methods*. [Web](https://www.itl.nist.gov/div898/handbook/apr/section1/apr15.htm)
3. J. F. Zhang, R. Gao, M. Duan, Z. Ji, W. Zhang, and J. Marsland, “Bias Temperature Instability of MOSFETs: Physical Processes, Models, and Prediction,” *Electronics* **11**, 1420 (2022). [DOI](https://doi.org/10.3390/electronics11091420)
4. J. H. Stathis, “Physical and Predictive Models of Ultrathin Oxide Reliability in CMOS Devices and Circuits,” *IEEE Transactions on Device and Materials Reliability* **1**, 43–59 (2001). [DOI](https://doi.org/10.1109/7298.946459)
5. NIST/SEMATECH, “Accelerated life tests,” *e-Handbook of Statistical Methods*. [Web](https://www.itl.nist.gov/div898/handbook/apr/section3/apr314.htm)
6. NIST/SEMATECH, “Weibull distribution,” *e-Handbook of Statistical Methods*. [Web](https://www.itl.nist.gov/div898/handbook/apr/section1/apr162.htm)
7. P. Cheng, L.-F. Mao, W.-H. Shen, and Y.-L. Yan, “Electromigration Failures in Integrated Circuits: A Review of Physics-Based Models and Analytical Methods,” *Electronics* **14**, 3151 (2025). [DOI](https://doi.org/10.3390/electronics14153151)
8. H. Zhou, “An Overview of Hot Carrier Degradation on Gate-All-Around Nanosheet Transistors,” *Micromachines* **16**, 311 (2025). [DOI](https://doi.org/10.3390/mi16030311)
