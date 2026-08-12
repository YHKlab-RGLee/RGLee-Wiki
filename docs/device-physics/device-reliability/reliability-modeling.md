---
title: "4.6. Device reliability: Reliability modeling"
description: 수명 분포, censored data, 가속 계수와 메커니즘별 외삽을 이용한 신뢰성 예측 절차를 설명
status: verified
last_verified: 2026-08-12
---

# 4.6. Device reliability: Reliability modeling

Reliability modeling은 가속 시험에서 얻은 열화·고장 자료를 확률 분포와 물리 기반 가속식으로 표현하고, 정해진 사용 조건의 수명 또는 고장 확률을 추정하는 과정이다. 공통 열화량과 고장 기준은 [Device reliability: Overview](overview.md)를 따른다. 이 문서에서는 모든 메커니즘을 하나의 경험식으로 합치지 않고, 수명 분포와 스트레스 의존성을 분리해 적합한 뒤 메커니즘별로 검증하는 절차를 사용한다.[1–4]

아래에서는 bias temperature instability (BTI), hot-carrier degradation (HCD), time-dependent dielectric breakdown (TDDB)과 electromigration을 서로 다른 물리 모형으로 구분한다.

## 1. 모델링 대상

### (1) 열화 궤적과 고장 시간

열화 자료는 시간에 따른 연속량 $D(t)$이고, 수명 자료는 임계값에 도달한 시간 $t_f$이다. 전자는 속도와 회복을 분석하는 데 유리하고, 후자는 고장 확률을 직접 추정한다. 임계값에 도달하지 않은 시편도 시험 종료 시각 $t_c$까지 생존했다는 정보를 주므로 right-censored 관측값으로 포함해야 한다.[1–4]

| 자료 | 관측값 | 적합 목적 | 주의점 |
| --- | --- | --- | --- |
| 열화 궤적 | $D(t,S)$ | 시간·스트레스 의존성 | 회복, 측정 지연, 시편 간 변동 |
| 고장 시간 | $t_f$ | 수명 분포 | 고장 기준과 시간 영점 |
| Censored 자료 | $t_f>t_c$ | 생존 가능 구간 | 단순 폐기 시 편향 |
| Competing risk | 원인별 $t_{f,i}$ 또는 첫 고장 | 메커니즘별 위험도 | 고장 원인 오분류 |

### (2) 분포와 가속식의 역할

수명 분포는 같은 스트레스에서 시편 간 산포를 나타내고, 가속식은 스트레스가 분포의 위치 또는 모양을 어떻게 바꾸는지 나타낸다. 두 요소를 동시에 정하지 않으면 높은 스트레스의 산포를 사용 조건의 낮은 고장 확률로 일관되게 옮길 수 없다.[1–4]

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

!!! info "[Measurement]"
    각 시편에 `(시간, 고장 여부, 고장 원인)`을 기록하고 censored 자료를 포함한 maximum likelihood estimation (MLE)으로 $\eta$와 $\beta$를 적합한다. Median rank로 그린 도표는 진단에 사용할 수 있지만, 작은 표본의 매개변수 추정과 신뢰구간은 censored likelihood 또는 적절한 생존분석 절차로 계산한다.[1,3–5]

## 3. 스트레스 가속 모형

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

### (2) 가속 계수

분포 모양이 스트레스에 따라 유지되는 scale-acceleration 모형에서는 acceleration factor (AF)를

$$
AF(S_1,S_2)=\frac{\eta(S_1)}{\eta(S_2)}
$$

로 놓을 수 있다. Weibull의 $\beta$가 스트레스 셀마다 체계적으로 변한다면 단순한 수평 시간 이동 가정이 맞지 않을 수 있다.[1–5]

## 4. 메커니즘별 모형

아래 식은 각 현상 문서의 세부 가정 아래에서 사용하는 대표 형태이다. 같은 기호 $A$, $n$, $E_a$라도 서로 다른 메커니즘에서 얻은 값은 공유 매개변수가 아니다.[1,6–9]

| 메커니즘 | 대표 응답 또는 수명식 | 반드시 확인할 조건 |
| --- | --- | --- |
| BTI | $\Delta V_T=A|V_\mathrm{ov}|^m t^n\exp(-E_a/kT)$ | stress/recovery 파형, 판독 지연, 결함군 |
| HCD | $\Delta X=A(V_G,V_D,T)t^n$ | 바이어스 영역, 운반자 에너지 분포, 자가 발열 |
| TDDB | Weibull $F(t)$와 전기장 가속식 | 면적, breakdown 판정, soft·hard 구분 |
| Electromigration | $t_f=AJ^{-n}\exp(E_a/kT)$ | 실제 금속 온도, 전류 집중, 길이와 back stress |

BTI와 HCD의 거듭제곱 시간식은 제한된 시간 창의 경험적 요약일 수 있다. TDDB의 Weibull 분포는 결함 percolation과 연결되지만, 전압 가속 형태까지 자동으로 정하지는 않는다. Black’s equation도 배선 형상과 응력 경계 조건을 생략한 축약식이다.[1,6–9]

## 5. 적합과 검증 절차

!!! info "[Measurement]"
    1. 사용 조건과 예측할 정량 지표·분위수·기간을 먼저 고정한다.
    2. 같은 메커니즘을 유지하는 여러 전압·전류·온도 셀과 대조군을 설계한다.
    3. 원자료, censored 관측값과 고장 원인을 보존한다.
    4. 후보 수명 분포와 가속식을 공동 적합하고 잔차, Weibull 도표와 매개변수의 스트레스 의존성을 확인한다.
    5. 적합에 쓰지 않은 중간 스트레스 또는 시간 구간으로 예측 성능을 검증한다.
    6. 사용 조건의 mission profile을 구간별로 적용하고 신뢰구간을 포함해 결과를 보고한다.[1–5]

서로 다른 스트레스 셀의 자료를 먼저 각각 직선화한 뒤 기울기만 비교하면 censored 자료와 공통 매개변수의 불확실성을 제대로 전달하지 못할 수 있다. 가능한 경우 원자료 likelihood를 사용해 분포와 가속 계수를 공동 추정하고, 시편·웨이퍼·lot의 계층적 변동도 시험 설계에 반영한다.[1–5]

## 6. 외삽과 불확실성

사용 조건은 가속 시험보다 훨씬 낮은 스트레스와 긴 시간에 있을 수 있다. 이때 통계적 신뢰구간은 선택한 모형이 옳다는 조건 아래의 불확실성만 표현하고, 잘못된 가속식이나 메커니즘 전환에서 생기는 model-form uncertainty는 포함하지 않는다.[1–5]

!!! warning "[Interpretation Caveat]"
    높은 스트레스에서 좋은 적합도는 장기·저전압 예측의 충분조건이 아니다. 사용 조건에 가까운 저스트레스 셀, 독립 검증 자료, 물리적 고장 분석을 함께 사용하고, 후보 모형들이 모두 자료와 양립하면 한 값을 단정하기보다 예측 범위를 제시한다.[1–5]

독립적인 경쟁 고장 모드의 cause-specific 생존확률을 $R_i(t)$라 하면 전체 생존확률은

$$
R_\mathrm{all}(t)=\prod_i R_i(t)
$$

로 쓸 수 있다. 그러나 공통 온도, 전원 파형이나 앞선 열화가 여러 모드에 영향을 주면 독립 가정이 깨질 수 있다. 회로 수준의 결합은 각 메커니즘의 상태 변수를 유지한 모형으로 검증해야 한다.[1–4]

## 7. 요약

- 수명 분포는 시편 산포를, 가속식은 스트레스 의존성을 나타내며 두 요소를 함께 적합한다.
- Censored 자료를 보존하고 MLE와 신뢰구간으로 Weibull 매개변수를 추정한다.
- Arrhenius, exponential과 power-law 식은 메커니즘과 검증 범위가 붙은 모형이지 보편식이 아니다.
- 사용 조건 외삽에는 통계적 불확실성과 모형 선택·메커니즘 전환의 불확실성을 구분해 제시한다.

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
