---
title: "4.4. Device reliability: Time-dependent dielectric breakdown"
description: 게이트 절연막의 결함 축적과 percolation, breakdown 판정, Weibull 통계와 전기장 외삽을 설명
status: verified
last_verified: 2026-08-12
---

# 4.4. Device reliability: Time-dependent dielectric breakdown

Time-dependent dielectric breakdown (TDDB)은 항복 전압보다 낮은 전기적 스트레스에서도 절연막 내부 결함이 시간에 따라 축적되고, 끝내 전극을 잇는 전도 경로가 형성되어 절연 기능을 잃는 wear-out 현상이다. 순간적인 intrinsic breakdown 전압 측정과 달리, TDDB는 일정 전압·전류 스트레스에서 고장 시간의 분포와 사용 조건으로의 외삽을 다룬다.[1–4]

## 1. 결함 축적과 percolation

게이트 절연막을 통과하는 운반자는 구조적·전자적 결함을 생성하거나 활성화할 수 있다. 결함이 임계적인 공간 연결성을 이루면 한쪽 전극에서 다른 쪽 전극으로 이어지는 국소 전도 경로가 생긴다. 이 percolation 관점은 같은 조건의 작은 소자에서도 고장 시간이 넓게 분포하고 면적에 의존하는 이유를 설명한다.[1–4]

결함 생성의 세부 과정과 전압 가속 모형에는 서로 다른 설명이 존재한다. Anode hole injection, thermochemical bond breaking과 전압 구동 defect generation 등은 특정 두께·재료·전기장 범위에서 제안된 모형이다. Percolation 통계가 관측된다는 사실만으로 결함 생성의 미시 원인이나 전기장 외삽식을 하나로 정할 수는 없다.[1–4]

### (1) SILC와 breakdown

Stress-induced leakage current (SILC)는 스트레스가 만든 트랩 보조 경로 때문에 낮은 판독 전기장에서 누설 전류가 증가하는 현상이다. SILC는 결함 축적의 선행 신호가 될 수 있지만, 임계 연결 경로가 완성되었다는 뜻은 아니므로 breakdown 판정과 구분한다.[1–4]

Soft breakdown은 전류가 불연속적으로 증가하지만 외부 회로나 소자 기능이 즉시 완전히 파괴되지 않은 상태이고, hard breakdown은 훨씬 큰 전도와 열적 손상을 수반할 수 있다. 이 구분은 절연막 두께, 소자 면적, 직렬저항, 전류 제한과 측정 대역폭에 의존한다.[1–4]

## 2. 스트레스 시험과 고장 판정

Constant voltage stress (CVS)는 일정 게이트 전압 또는 절연막 전기장을, constant current stress (CCS)는 일정 주입 전류를 인가한다. CVS는 사용 전압과 직접 비교하기 쉽지만 breakdown 직후 전류 폭주를 제한해야 하고, CCS에서는 결함 생성에 따라 필요한 전압이 변한다.[1–4]

!!! info "[Measurement]"
    1. 소자 면적, 유효 절연막 두께, 온도와 모든 단자 바이어스를 기록한다.
    2. 스트레스 전 낮은 전기장의 $I_G$–$V_G$를 측정한다.
    3. 정해진 CVS 또는 CCS를 인가하면서 $I_G(t)$ 또는 $V_G(t)$를 충분한 시간 분해능으로 기록한다.
    4. 미리 정한 전류 급증, 미분 신호, 저전계 누설 증가 또는 회로 기능 기준으로 $t_\mathrm{BD}$를 판정한다.
    5. Soft breakdown과 hard breakdown, 시험 종료까지 고장하지 않은 censored 시편을 구분한다.[1–4]

고장 판정 예시는

$$
t_\mathrm{BD}=\inf\left\{t:
\frac{I_G(t)}{I_{G,\mathrm{base}}(t)}\ge C_I
\right\}
$$

처럼 정의할 수 있다. $I_{G,\mathrm{base}}(t)$는 breakdown 전의 완만한 전류 추세이고 $C_I$는 시험 전에 정한 증가 배수이다. 이 기준은 예시이며, 절대 전류 임계값·전압 step 또는 noise 기준을 사용한다면 대역폭과 compliance까지 밝혀야 한다.[1–4]

!!! warning "[Interpretation Caveat]"
    측정 장비의 전류 compliance, 배선 직렬저항과 sampling interval은 관측되는 breakdown 크기와 시각을 바꿀 수 있다. 서로 다른 실험의 $t_\mathrm{BD}$를 비교할 때는 전기장만 맞추지 말고 판정 알고리즘과 측정 회로도 맞춘다.[1–4]

## 3. Weibull 통계와 면적 효과

두 매개변수 Weibull 분포로 breakdown 시간을 나타내면

$$
F(t)=1-\exp\left[-\left(\frac{t}{\eta}\right)^\beta\right]
$$

이다. $\eta$는 characteristic life, $\beta$는 shape parameter이다. Weibull 좌표의 직선성은 단일 모집단을 점검하는 도구이며, $\beta$의 값만으로 결함 생성 메커니즘을 확정하지 않는다.[1–4]

공간적으로 독립적인 동일 면적 요소가 weakest-link 방식으로 고장한다고 가정하면 기준 면적 $A_0$의 분포로부터 면적 $A$의 분포는

$$
F_A(t)=1-\left[1-F_{A_0}(t)\right]^{A/A_0}
$$

가 된다. 같은 $F$에서 큰 면적일수록 더 짧은 시간이 예측된다. 이 식은 전기장이 면적 전체에 균일하고 결함이 독립적이며 가장 약한 국소 경로가 전체 고장을 정한다는 가정에 제한된다.[1–4]

!!! note "[Metric]"
    표본별 $(t_\mathrm{BD},\text{고장 여부})$와 면적을 보존하고 censored maximum likelihood estimation으로 $\eta$와 $\beta$를 구한다. 보고할 수명은 평균만이 아니라 $t_{p}$처럼 지정한 누적 고장 확률의 분위수와 신뢰구간으로 제시한다.[1–4]

## 4. 전압과 온도 외삽

시험 전기장 $E_\mathrm{ox}$에서 사용 전기장으로 외삽하기 위해 대표적으로

$$
t_\mathrm{BD}=A\exp(-\gamma E_\mathrm{ox}),
\qquad
t_\mathrm{BD}=A\exp\left(\frac{G}{E_\mathrm{ox}}\right),
\qquad
t_\mathrm{BD}=AE_\mathrm{ox}^{-n}
$$

과 같은 $E$, $1/E$, power-law 형태가 사용되어 왔다. $\gamma$, $G$, $n$은 해당 소자·온도·전기장 구간의 적합 매개변수이다. 높은 전기장의 짧은 시험만으로 세 후보 중 사용 조건의 장기 예측을 유일하게 고르기 어려울 수 있다.[1–4]

온도 의존성도 단일 Arrhenius 식에서 벗어날 수 있다. 터널링 전류, defect generation과 국소 발열의 온도 의존성이 함께 들어가므로, 고정한 게이트 전압과 고정한 절연막 전기장 시험이 동일한 열 가속을 준다고 가정하지 않는다.[1–4]

### (1) 외삽 검증

여러 전기장과 온도에서 Weibull 기울기, 고장 신호와 사후 전기 특성을 비교한다. 고장 모드가 유지되는 구간만 공동 적합하고, 중간 스트레스 셀을 적합에서 제외한 뒤 예측하는 방식으로 모형을 교차 검증한다.[1–4]

매우 낮은 고장 확률과 긴 사용 시간의 예측에는 통계적 신뢰구간 외에 가속식 선택의 불확실성이 지배할 수 있다. 후보 모형이 시험 자료에서 구분되지 않으면 하나의 숫자보다 각 모형의 예측 범위와 검증 한계를 보고한다.[1–4]

## 5. 회로 해석의 경계

Soft breakdown 뒤에도 단일 트랜지스터가 계속 동작할 수 있지만, 증가한 게이트 전류와 잡음은 회로 상태와 민감한 노드에 따라 기능 오류를 일으킬 수 있다. 반대로 단일 소자의 전류 step을 곧바로 칩 고장으로 등치하면 회로의 여유와 redundancy를 무시하게 된다.[1,2,4]

고유전율 절연막과 적층 구조에서는 결함 위치, 전도 경로와 breakdown 신호가 SiO$_2$의 단일층 모형과 다를 수 있다. 재료나 물리 두께가 바뀌면 기존의 Weibull 매개변수와 전압 가속 계수를 그대로 이전하지 않고 구조별로 재검증한다.[1,2,4]

## 6. 요약

- TDDB는 절연막 결함의 시간적 축적과 임계 percolation 경로 형성으로 나타나는 wear-out 고장이다.
- SILC, soft breakdown과 hard breakdown을 구분하고 측정 회로·판정 기준을 수명 정의에 포함한다.
- Weibull 분포와 weakest-link 면적 scaling은 명시된 독립성·균일 전기장 가정에서 사용한다.
- $E$, $1/E$와 power-law 외삽식은 경쟁 모형이며, 고전계 적합만으로 사용 조건의 장기 수명을 확정하지 않는다.

## 7. 참고문헌

1. J. H. Stathis, “Physical and Predictive Models of Ultrathin Oxide Reliability in CMOS Devices and Circuits,” *IEEE Transactions on Device and Materials Reliability* **1**, 43–59 (2001). [DOI](https://doi.org/10.1109/7298.946459)
2. J. S. Suehle, “Ultrathin Gate Oxide Reliability: Physical Models, Statistics, and Characterization,” *IEEE Transactions on Electron Devices* **49**, 958–971 (2002). [DOI](https://doi.org/10.1109/TED.2002.1003712)
3. R. Degraeve, G. Groeseneken, R. Bellens, J. L. Ogier, M. Depas, P. J. Roussel, and H. E. Maes, “New Insights in the Relation Between Electron Trap Generation and the Statistical Properties of Oxide Breakdown,” *IEEE Transactions on Electron Devices* **45**, 904–911 (1998). [DOI](https://doi.org/10.1109/16.662800)
4. M. White and J. B. Bernstein, *Microelectronics Reliability: Physics-of-Failure Based Modeling and Lifetime Evaluation*, JPL Publication 08-5, Jet Propulsion Laboratory (2008). [PDF](https://nepp.nasa.gov/files/16365/08_102_4_%20JPL_White.pdf)
