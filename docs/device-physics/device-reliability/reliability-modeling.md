---
title: "4.6. Device reliability: Reliability modeling"
description: Censored likelihood, 수명 분포, 가속 모형, competing risk와 불확실성을 결합한 신뢰성 예측 절차를 설명
status: verified
last_verified: 2026-08-13
---

# 4.6. Device reliability: Reliability modeling

Reliability modeling은 가속 시험에서 얻은 열화·고장 자료를 확률 분포와 물리 기반 가속식으로 표현하고, 정해진 사용 조건의 수명 또는 고장 확률을 추정하는 과정이다. 공통 열화량과 고장 기준은 [Device reliability: Overview](overview.md)를 따른다. 이 문서에서는 **관측·censoring 정의 → 수명 분포 → 스트레스 가속 → 적합·검증 → mission profile 예측**의 순서로 모형을 구성한다.[1–5,10,11]

아래에서는 bias temperature instability (BTI), hot-carrier degradation (HCD), time-dependent dielectric breakdown (TDDB)과 electromigration을 서로 다른 물리 모형으로 구분한다. 모든 메커니즘을 하나의 경험식으로 합치거나, 시험 자료에 가장 잘 맞는 분포만 골라 물리적 검증 없이 사용 조건으로 외삽하지 않는다.[1–4,10,11]

## 1. 모델링 대상

### (1) 열화 궤적과 고장 시간

열화 자료는 시간에 따른 연속량 $D(t)$이고, 수명 자료는 임계값에 도달한 시간 $t_f$이다. 전자는 속도와 회복을 분석하는 데 유리하고, 후자는 고장 확률을 직접 추정한다. 임계값에 도달하지 않은 시편도 시험 종료 시각 $t_c$까지 생존했다는 정보를 주므로 right-censored 관측값으로 포함해야 한다.[1–4]

| 자료 | 관측값 | 적합 목적 | 주의점 |
| --- | --- | --- | --- |
| 열화 궤적 | $D(t,S)$ | 시간·스트레스 의존성 | 회복, 측정 지연, 시편 간 변동 |
| 고장 시간 | $t_f$ | 수명 분포 | 고장 기준과 시간 영점 |
| Censored 자료 | $t_f>t_c$ | 생존 가능 구간 | 단순 폐기 시 편향 |
| Competing risk | 원인별 $t_{f,i}$ 또는 첫 고장 | 메커니즘별 위험도 | 고장 원인 오분류 |

연속 수명 $T_f$에 대해 누적 고장 확률 $F(t)$, 생존확률 $R(t)$, 확률밀도 $f(t)$와 hazard $h(t)$를

$$
R(t)=P(T_f>t)=1-F(t),
\qquad
h(t)=\frac{f(t)}{R(t)}
$$

로 정의한다. 누적 hazard $H(t)=\int_0^t h(u)\,du$를 사용하면 $R(t)=\exp[-H(t)]$이다. $F(t)$는 시간 $t$까지 고장할 확률이고, $h(t)$는 그때까지 생존한 시편의 조건부 순간 고장률이므로 둘을 같은 양으로 해석하지 않는다.[1–5,10]

### (2) 분포와 가속식의 역할

수명 분포는 같은 스트레스에서 시편 간 산포를 나타내고, 가속식은 스트레스가 분포의 위치 또는 모양을 어떻게 바꾸는지 나타낸다. 두 요소를 동시에 정하지 않으면 높은 스트레스의 산포를 사용 조건의 낮은 고장 확률로 일관되게 옮길 수 없다.[1–4]

### (3) Censored likelihood

시편 $i$의 관측 시각을 $t_i$, 고장이면 $\delta_i=1$, right-censored이면 $\delta_i=0$으로 두면 독립 시편의 likelihood는

$$
L(\theta)
=
\prod_i
f(t_i\mid\theta)^{\delta_i}
R(t_i\mid\theta)^{1-\delta_i}
$$

이다. 즉 정확한 고장 시각은 density로, 시험 종료까지 생존한 시편은 그 시각의 생존확률로 기여한다. 고장이 두 판독 시각 $(t_{L,i},t_{U,i}]$ 사이에서만 알려진 interval-censored 관측은 $F(t_{U,i})-F(t_{L,i})$로 기여한다.[2–5,10,13]

Censoring을 고장으로 바꾸거나 censored 시편을 버리면 likelihood가 달라져 수명과 분포 폭이 편향될 수 있다. 다만 censoring 시각이 잠재 수명과 독립이라는 non-informative censoring 가정이 필요하다. 누설이 큰 시편만 장비 한계로 조기 종료하는 것처럼 종료 규칙이 열화 상태에 의존하면 그 규칙을 관측 모형에 포함해야 한다.[2–5,10,13]

## 2. Weibull 수명 분포

두 매개변수 Weibull 분포의 누적 고장 확률은

$$
F(t)=1-\exp\left[-\left(\frac{t}{\eta}\right)^\beta\right],\qquad t\ge0
$$

이다. $\eta$는 $F(\eta)=1-e^{-1}\approx0.632$가 되는 characteristic life이고, $\beta$는 분포 모양을 정하는 shape parameter이다.[1,3,5]

Hazard rate는

$$
h(t)=\frac{\beta}{\eta}\left(\frac{t}{\eta}\right)^{\beta-1}
$$

이다. 이 식에서 $\beta<1$, $\beta=1$, $\beta>1$은 각각 감소, 일정, 증가하는 hazard를 뜻한다. 다만 $\beta$만으로 미시적 고장 원인을 확정할 수는 없으며, 고장 분석과 스트레스 의존성이 함께 필요하다.[1,3,5]

Weibull 좌표에서는

$$
Y=\ln[-\ln(1-F)]=\beta\ln t-\beta\ln\eta
$$

이므로 단일 Weibull 모집단은 직선에 가깝게 나타난다. 휘어짐이나 기울기 변화는 혼합 모집단, 서로 다른 메커니즘, 임계시간 또는 부적절한 분포를 의심할 신호이지 자동적인 결론은 아니다.[1,3–5]

누적 고장 확률 $p$에 대응하는 Weibull 분위수는

$$
t_p
=
\eta\left[-\ln(1-p)\right]^{1/\beta}
$$

이다. 제품 요구가 작은 $p$의 early-life failure에 놓이면 평균이나 $t_{50}$보다 $t_p$가 직접적인 정량 지표이다. 그러나 관측된 가장 이른 고장보다 훨씬 작은 $p$로 갈수록 분포 선택과 $\beta$의 작은 오차가 크게 증폭되므로 신뢰구간과 모형 간 예측 차이를 함께 제시한다.[1–5,10,11]

Weibull만이 유일한 수명 분포는 아니다. Lognormal은 $\ln T_f$가 정규분포일 때 적합하고, exponential은 시간에 무관한 hazard를 가정한다. 분포는 확률도표의 직선성 하나가 아니라 고장 메커니즘, censored likelihood, 잔차와 관심 분위수의 예측 안정성을 함께 보고 선택한다.[1–5,10]

| 분포 | 핵심 가정 또는 형태 | 적합한 정량 지표 | 주요 진단 |
| --- | --- | --- | --- |
| Weibull | $h(t)\propto t^{\beta-1}$ | $\beta$, $\eta$, $t_p$ | Weibull 도표, shape의 스트레스 의존성 |
| Lognormal | $\ln T_f$가 정규분포 | log-scale 위치·폭, $t_p$ | Lognormal 도표, 꼬리의 비대칭 |
| Exponential | $h(t)=\lambda$ | $\lambda$, mean time | 시간에 따른 hazard 변화 |
| Mixture | 둘 이상의 잠재 모집단 | 성분별 분포와 혼합비 | 휘어짐, 고장 위치·원인의 분리 가능성 |

!!! info "[Measurement]"
    각 시편에 `(시간, 고장 여부, 고장 원인)`을 기록하고 censored 자료를 포함한 maximum likelihood estimation (MLE)으로 $\eta$와 $\beta$를 적합한다. Median rank로 그린 도표는 진단에 사용할 수 있지만, 작은 표본의 매개변수 추정과 신뢰구간은 censored likelihood 또는 적절한 생존분석 절차로 계산한다.[1,3–5]

!!! warning "[Interpretation Caveat]"
    Maximum likelihood estimation의 큰 표본 근사는 고장 수가 매우 적을 때 부정확할 수 있다. Wald interval 하나에 의존하지 말고 profile likelihood 또는 적절한 bootstrap interval을 비교하며, 고장이 하나도 없는 셀에서는 분포 모양을 그 셀만으로 추정할 수 없음을 밝힌다.[2–5,10,13]

## 3. 스트레스 가속 모형

Accelerated failure time (AFT) 모형은 스트레스가 수명 축을 늘이거나 줄인다고 보고

$$
\ln T_f
=
\mu(S)+\sigma\varepsilon
$$

로 나타낸다. $\mu(S)$는 스트레스 $S$에 따른 log-life의 위치, $\sigma$는 분포 폭, $\varepsilon$은 선택한 표준 분포의 확률변수이다. Weibull에서 공통 $\beta$를 두는 scale-acceleration은 이러한 AFT 가정의 한 형태이다. 스트레스 셀마다 $\sigma$나 $\beta$가 체계적으로 달라지면 단순 시간축 이동이 성립하지 않을 수 있다.[2–5,10,11]

### (1) 온도와 전압

열 활성화 속도에 대한 Arrhenius 형태를 수명으로 쓰면

$$
t_f(T)=A\exp\left(\frac{E_a}{kT}\right)
$$

이다. $E_a$는 적합한 활성화 에너지, $k$는 Boltzmann 상수, $T$는 절대온도이다. 이 식은 하나의 속도 제한 과정이 시험 범위에서 유지될 때의 모형이며, 온도가 바뀌어 다른 확산 경로나 반응이 지배하면 한 개의 $E_a$로 외삽할 수 없다.[1–4]

전기적 스트레스 $S$에는 대표적으로

$$
t_f=A\exp(-\gamma S),\qquad
t_f=A\exp\left(\frac{G}{S}\right),\qquad
t_f=AS^{-n}
$$

과 같은 exponential, reciprocal, power-law 형태가 사용된다. 어느 식도 모든 메커니즘에 보편적이지 않다. 예를 들어 TDDB의 전기장 외삽과 electromigration의 전류 밀도 항은 물리적 대상과 매개변수의 의미가 다르다.[1–4]

온도와 전기적 스트레스를 동시에 바꿀 때에는 단순 곱 모형을 자동으로 가정하지 않는다. 예를 들어

$$
\mu(S,T)
=
a_0+a_1g(S)+\frac{a_2}{kT}+a_3\frac{g(S)}{kT}
$$

에서 $g(S)$는 선택한 전압·전기장·전류 변환이고, $a_3$는 상호작용을 나타낸다. $a_3=0$인 분리 가능한 모형은 더 단순하지만, 전기적 스트레스가 유효 활성화 에너지나 우세 메커니즘을 바꾸면 성립하지 않는다. 시험 설계에는 상호작용과 곡률을 식별할 수 있는 여러 스트레스 셀이 필요하다.[1–4,10,11]

### (2) 가속 계수

분포 모양이 스트레스에 따라 유지되는 scale-acceleration 모형에서는 acceleration factor (AF)를

$$
AF(S_1,S_2)=\frac{\eta(S_1)}{\eta(S_2)}
$$

로 놓을 수 있다. Weibull의 $\beta$가 스트레스 셀마다 체계적으로 변한다면 단순한 수평 시간 이동 가정이 맞지 않을 수 있다.[1–5]

$AF$의 방향은 문헌마다 반대로 정의되기도 한다. 이 문서에서는 $AF(S_1,S_2)>1$이면 $S_1$의 characteristic life가 $S_2$보다 길다는 규약을 사용한다. 수치만 보고하지 말고 분자·분모의 스트레스 조건과 수명 정량 지표를 함께 쓴다.[2–5,10]

## 4. 메커니즘별 모형

아래 식은 각 현상 문서의 세부 가정 아래에서 사용하는 대표 형태이다. 같은 기호 $A$, $n$, $E_a$라도 서로 다른 메커니즘에서 얻은 값은 공유 매개변수가 아니다.[1,6–9]

| 메커니즘 | 대표 응답 또는 수명식 | 반드시 확인할 조건 |
| --- | --- | --- |
| [BTI](bias-temperature-instability.md) | $\Delta V_T=A|V_\mathrm{ov}|^m t^n\exp(-E_a/kT)$ | stress/recovery 파형, 판독 지연, 결함군 |
| [HCD](hot-carrier-degradation.md) | $\Delta X=A(V_G,V_D,T)t^n$ | 바이어스 영역, 운반자 에너지 분포, 자가 발열 |
| [TDDB](time-dependent-dielectric-breakdown.md) | Weibull $F(t)$와 전기장 가속식 | 면적, breakdown 판정, soft·hard 구분 |
| [Electromigration](interconnect-reliability.md) | $t_f=AJ^{-n}\exp(E_a/kT)$ | 실제 금속 온도, 전류 집중, 길이와 back stress |

BTI와 HCD의 거듭제곱 시간식은 제한된 시간 창의 경험적 요약일 수 있다. TDDB의 Weibull 분포는 결함 percolation과 연결되지만, 전압 가속 형태까지 자동으로 정하지는 않는다. Black’s equation도 배선 형상과 응력 경계 조건을 생략한 축약식이다.[1,6–9]

## 5. 적합과 검증 절차

!!! info "[Measurement]"
    1. 사용 조건, 예측 기간 $t_\mathrm{use}$와 요구 정량 지표 $F(t_\mathrm{use})$, $R(t_\mathrm{use})$ 또는 $t_p$를 먼저 고정한다.
    2. 같은 메커니즘을 유지하면서 가속식의 기울기·곡률·상호작용을 식별할 여러 전압·전류·온도 셀과 대조군을 설계한다. 시편·wafer·lot 배정을 무작위화하거나 block으로 기록한다.
    3. 시편별 `(관측 하한, 관측 상한, 고장 여부, 고장 원인, 스트레스 이력)`을 보존한다. Right-censored 관측은 상한을 열어 두고, 정확한 고장은 사건 시각으로 별도 표시하며, interval-censored 관측은 서로 다른 하한과 상한을 기록한다.
    4. 후보 수명 분포와 가속식을 원자료 likelihood로 공동 적합한다. 매개변수 추정값과 covariance, profile likelihood 또는 bootstrap interval을 계산한다.
    5. 확률도표, censored residual, 스트레스 셀별 shape와 물리적 고장 위치를 확인한다. 적합에 쓰지 않은 중간 스트레스 셀로 예측을 검증한다.
    6. 검증된 범위에서 사용 조건과 mission profile을 적용하고, 분위수 또는 고장 확률의 confidence interval과 prediction interval을 구분해 보고한다.[1–5,10,11,13]

서로 다른 스트레스 셀의 자료를 먼저 각각 직선화한 뒤 기울기만 비교하면 censored 자료와 공통 매개변수의 불확실성을 제대로 전달하지 못할 수 있다. 가능한 경우 원자료 likelihood를 사용해 분포와 가속 계수를 공동 추정하고, 시편·웨이퍼·lot의 계층적 변동도 시험 설계에 반영한다.[1–5]

| 검증 질문 | 사용할 진단 | 실패할 때의 해석 |
| --- | --- | --- |
| 한 분포가 각 셀을 설명하는가? | 확률도표, likelihood residual | 분포 꼬리 또는 혼합 모집단 재검토 |
| 공통 shape가 유지되는가? | 셀별 $\beta$·$\sigma$, 제한 모형 비교 | 단순 scale-acceleration 기각 가능 |
| 가속식이 충분한가? | 중간 셀 예측 오차, 곡률·상호작용 | 다른 변환 또는 메커니즘 전환 조사 |
| 고장 모드가 같은가? | 전기적 신호, 사후 물리 분석 | 모드별 자료 분리와 competing risk 필요 |
| 제조 변동이 독립적인가? | wafer·lot별 잔차와 random effect | 유효 표본 수와 신뢰구간 재평가 |

적합도 검정에서 모형을 기각하지 못했다는 사실은 그 모형이 참임을 뜻하지 않는다. 특히 censored 자료와 작은 고장 수에서는 서로 다른 분포·가속식이 모두 관측 구간을 설명할 수 있으므로, 관심 있는 early-tail 예측과 holdout 자료에서 후보 모형을 비교한다.[2–5,10,11]

## 6. 외삽과 불확실성

사용 조건은 가속 시험보다 훨씬 낮은 스트레스와 긴 시간에 있을 수 있다. 이때 통계적 신뢰구간은 선택한 모형이 옳다는 조건 아래의 불확실성만 표현하고, 잘못된 가속식이나 메커니즘 전환에서 생기는 model-form uncertainty는 포함하지 않는다.[1–5]

### (1) Mission profile

사용 스트레스 $S(t)$가 시간에 따라 변할 때, 현재 조건과 시간만으로 hazard가 정해지고 열화 기억효과가 없다는 가정에서는

$$
H(t)
=
\int_0^t h\!\left(u\mid S(u)\right)du,
\qquad
R(t)=\exp[-H(t)]
$$

로 누적할 수 있다. Piecewise-constant mission profile이면 각 구간의 적분을 합한다. 그러나 BTI recovery, progressive breakdown, back stress처럼 내부 상태가 다음 구간의 속도에 영향을 주면 같은 시간·스트레스의 단순 hazard 합으로는 이력을 보존할 수 없다. 이때에는 트랩 점유, breakdown 전류 또는 응력 같은 상태 변수를 시간 순서대로 갱신한다.[1,6–11]

Duty cycle만으로 직류 시간을 선형 축소하는 것도 하나의 누적 손상 가정이다. 주파수·상승 시간·열 시정수 또는 회복 시간이 메커니즘의 상태 변화와 비슷하면 동일 duty cycle의 파형도 다른 수명을 줄 수 있으므로, 대표 파형이나 경계 파형으로 검증한다.[1,6–11]

!!! warning "[Interpretation Caveat]"
    높은 스트레스에서 좋은 적합도는 장기·저전압 예측의 충분조건이 아니다. 사용 조건에 가까운 저스트레스 셀, 독립 검증 자료, 물리적 고장 분석을 함께 사용하고, 후보 모형들이 모두 자료와 양립하면 한 값을 단정하기보다 예측 범위를 제시한다.[1–5]

### (2) Competing risk

독립적인 잠재 고장 시간의 생존확률을 $R_i(t)$라 하면 전체 생존확률은

$$
R_\mathrm{all}(t)=\prod_i R_i(t)
$$

로 쓸 수 있다. 관측 가능한 cause-specific hazard를 $h_i(t)$로 나타내면 원인 $i$의 cumulative incidence function (CIF)은

$$
F_i(t)
=
\int_0^t R_\mathrm{all}(u)h_i(u)\,du
$$

이다. 다른 원인의 고장을 단순 right-censoring한 Kaplan–Meier 곡선의 $1-R_i(t)$는 일반적으로 CIF와 같지 않다. 특정 원인의 절대 고장 확률을 보고할 때에는 다른 원인이 먼저 발생해 그 시편을 위험집단에서 제거한다는 사실을 반영한다.[1–5,10,12]

공통 온도·전원 파형, 제조 결함이나 앞선 열화가 여러 모드에 영향을 주면 잠재 고장 시간이 독립이라는 곱 모형도 깨질 수 있다. 회로 수준의 결합은 공유 covariate, 계층적 변동 또는 각 메커니즘의 상태 변수를 유지한 모형으로 검증한다.[1–4,10,12]

### (3) 불확실성의 구분

| 불확실성 | 예 | 보고 방법 |
| --- | --- | --- |
| 시편 산포 | 같은 셀의 $t_f$ 분포 | 분위수와 prediction interval |
| 매개변수 불확실성 | $\beta$, $E_a$, $n$의 추정 오차 | covariance, profile likelihood·bootstrap interval |
| 모형 형식 | Weibull 대 lognormal, $E$ 대 $1/E$ | 후보별 예측과 검증 범위 |
| 고장 원인 | early·late mode 오분류 | 원인 분류 민감도와 competing-risk 결과 |
| 사용 조건 | 온도·전압·duty cycle의 변동 | mission-profile 시나리오 또는 확률분포 |

Confidence interval은 모집단 매개변수나 그 함수의 추정 불확실성을, prediction interval은 새 시편 또는 미래 관측의 산포까지 포함한다. 둘을 같은 “수명 오차막대”로 합치지 않고, model-form과 mission-profile 불확실성은 통계 적합 구간 밖의 별도 시나리오로 제시한다.[1–5,10,11]

## 7. 요약

- 수명 분포는 시편 산포를, 가속식은 스트레스 의존성을 나타내며 두 요소를 함께 적합한다.
- 고장·right-censored·interval-censored 관측이 likelihood에 기여하는 방식을 구분하고 MLE와 신뢰구간을 계산한다.
- Arrhenius, exponential과 power-law 식은 메커니즘과 검증 범위가 붙은 모형이지 보편식이 아니다.
- 공통 shape와 단순 시간축 이동 가정을 셀별 분포와 holdout 스트레스로 검증한다.
- Mission profile에는 기억효과의 상태 변수를, competing risk에는 다른 원인의 선행 고장을 반영한다.
- 사용 조건 외삽에는 시편 산포, 매개변수, 모형 형식과 사용 조건의 불확실성을 구분해 제시한다.

## 8. 참고문헌

1. M. White and J. B. Bernstein, *Microelectronics Reliability: Physics-of-Failure Based Modeling and Lifetime Evaluation*, JPL Publication 08-5, Jet Propulsion Laboratory (2008). [PDF](https://nepp.nasa.gov/files/16365/08_102_4_%20JPL_White.pdf)
2. NIST/SEMATECH, “Accelerated life tests,” *e-Handbook of Statistical Methods*. [Web](https://www.itl.nist.gov/div898/handbook/apr/section3/apr314.htm)
3. NIST/SEMATECH, “Acceleration models,” *e-Handbook of Statistical Methods*. [Web](https://www.itl.nist.gov/div898/handbook/apr/section1/apr15.htm)
4. NIST/SEMATECH, “How do you project reliability at use conditions?” *e-Handbook of Statistical Methods*. [Web](https://www.itl.nist.gov/div898/handbook/apr/section4/apr43.htm)
5. NIST/SEMATECH, “Weibull distribution,” *e-Handbook of Statistical Methods*. [Web](https://www.itl.nist.gov/div898/handbook/apr/section1/apr162.htm)
6. J. F. Zhang, R. Gao, M. Duan, Z. Ji, W. Zhang, and J. Marsland, “Bias Temperature Instability of MOSFETs: Physical Processes, Models, and Prediction,” *Electronics* **11**, 1420 (2022). [DOI](https://doi.org/10.3390/electronics11091420)
7. S. Tyaginov et al., “Compact Physics Hot-Carrier Degradation Model Valid over a Wide Bias Range,” *Micromachines* **14**, 2018 (2023). [DOI](https://doi.org/10.3390/mi14112018)
8. J. H. Stathis, “Physical and Predictive Models of Ultrathin Oxide Reliability in CMOS Devices and Circuits,” *IEEE Transactions on Device and Materials Reliability* **1**, 43–59 (2001). [DOI](https://doi.org/10.1109/7298.946459)
9. P. Cheng, L.-F. Mao, W.-H. Shen, and Y.-L. Yan, “Electromigration Failures in Integrated Circuits: A Review of Physics-Based Models and Analytical Methods,” *Electronics* **14**, 3151 (2025). [DOI](https://doi.org/10.3390/electronics14153151)
10. W. Q. Meeker and L. A. Escobar, *Statistical Methods for Reliability Data* (Wiley, 1998). [Publisher](https://www.wiley.com/en-us/Statistical+Methods+for+Reliability+Data-p-9780471143284)
11. L. A. Escobar and W. Q. Meeker, “A Review of Accelerated Test Models,” *Statistical Science* **21**, 552–577 (2006). [DOI](https://doi.org/10.1214/088342306000000321)
12. K. J. Coakley et al., “Survival Analysis Approach to Account for Non-Exponential Decay Rate Effects in Lifetime Experiments,” *Nuclear Instruments and Methods in Physics Research A* **813**, 84–95 (2016). [DOI](https://doi.org/10.1016/j.nima.2015.12.064)
13. NIST/SEMATECH, “Maximum likelihood estimation,” *e-Handbook of Statistical Methods*. [Web](https://www.itl.nist.gov/div898/handbook/apr/section4/apr412.htm)
