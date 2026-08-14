---
title: "5.4. Device reliability: Time-dependent dielectric breakdown"
description: 게이트 절연막의 운반자 주입, 결함 축적과 percolation, progressive breakdown, Weibull 통계와 수명 외삽을 설명
status: verified
last_verified: 2026-08-13
---

# 5.4. Device reliability: Time-dependent dielectric breakdown

Time-dependent dielectric breakdown (TDDB)은 항복 전압보다 낮은 전기적 스트레스에서도 절연막 내부 결함이 시간에 따라 축적되고, 끝내 전극을 잇는 전도 경로가 형성되어 절연 기능을 잃는 wear-out 현상이다. 순간적인 breakdown voltage 측정과 달리, TDDB는 정해진 전압·전류·온도에서 고장 시간 $t_\mathrm{BD}$의 분포를 측정하고 사용 조건으로 외삽한다.[1–5]

공통 스트레스·고장·mission profile 규약은 [Device reliability: Overview](overview.md)를 따르며, censored data와 가속 모형의 공통 적합 절차는 [Device reliability: Reliability modeling](reliability-modeling.md)에서 다룬다. 이 글은 MOS 게이트 절연막의 **운반자 전도 → 결함 생성 → percolation → breakdown 성장 → 회로 고장** 연결에 초점을 둔다.

## 1. 결함 축적과 percolation

절연막에 전압을 인가하면 전자 또는 정공이 기존 장벽을 터널링하거나 트랩을 거쳐 이동한다. 이 운반자는 에너지를 격자에 전달해 구조적·전자적 결함을 생성하거나 활성화할 수 있다. 다만 정상 터널링 전류 자체는 breakdown이 아니며, 스트레스 전·후의 낮은 전기장 전류를 비교해 새로 생긴 경로를 분리해야 한다.[1,2,5]

결함이 절연막 두께 방향의 임계적인 공간 연결성을 이루면 한쪽 전극에서 다른 쪽 전극으로 이어지는 국소 전도 경로가 생긴다. 이 percolation 사건이 최초 breakdown의 물리적 기준이다. 결함의 위치와 생성 시간이 확률적이므로 같은 조건의 소자도 $t_\mathrm{BD}$가 넓게 분포하며, 면적이 커질수록 가장 먼저 연결되는 약한 부위를 포함할 확률이 높아진다.[1–5]

결함 생성의 세부 과정과 전압 가속 모형에는 서로 다른 설명이 존재한다. Anode hole injection, thermochemical bond breaking과 전압 구동 defect generation 등은 특정 두께·재료·전기장 범위에서 제안된 모형이다. Percolation 통계가 관측된다는 사실만으로 결함 생성의 미시 원인이나 전기장 외삽식을 하나로 정할 수는 없다.[1–4]

태생적 wear-out은 스트레스 중 생성된 결함이 주도하는 분포이다. 반면 extrinsic breakdown은 오염, 국소 두께 감소, 입자와 공정 손상 같은 기존 약점에서 조기에 나타날 수 있다. Weibull plot의 휘어짐이나 두 기울기는 혼합 모집단의 단서이지만, 그 모양만으로 extrinsic 원인을 확정하지 않고 물리적 고장 분석과 결합한다.[1,2,5]

| 단계 | 절연막 상태 | 전기적 관측 | 해석 경계 |
| --- | --- | --- | --- |
| 초기 상태 | 공정으로 정해진 기존 결함 | 정상 터널링 전류, $I_G$–$V_G$ | 초기 누설이 낮아도 장기 수명이 자동으로 보장되지 않음 |
| Wear-out | 스트레스 유발 트랩 증가 | SILC, 전류 drift·noise | SILC는 결함 지표이지 연결 경로의 충분조건이 아님 |
| 최초 breakdown | 임계 percolation path 형성 | 전류 step, noise 증가, 매개변수 급변 | 최초 이상 신호와 회로 수명 종료는 다를 수 있음 |
| Post-breakdown | 국소 전도 경로의 안정·성장·추가 형성 | soft, progressive 또는 hard breakdown | 전류 제한·직렬저항·회로 상태가 성장을 변경 |

### (1) SILC와 breakdown

Stress-induced leakage current (SILC)는 스트레스가 만든 트랩 보조 경로 때문에 낮은 판독 전기장에서 누설 전류가 증가하는 현상이다. SILC는 결함 축적의 선행 신호가 될 수 있지만, 임계 연결 경로가 완성되었다는 뜻은 아니므로 breakdown 판정과 구분한다.[1–4]

Soft breakdown은 전류가 불연속적으로 증가하지만 외부 회로나 소자 기능이 즉시 완전히 파괴되지 않은 상태이고, hard breakdown은 훨씬 큰 전도와 열적 손상을 수반할 수 있다. **Progressive breakdown**은 최초 breakdown 후 국소 전도 경로의 누설이 시간에 따라 성장하는 구간이다. 최초 $t_\mathrm{BD}$와 회로의 허용 누설을 넘는 시각 $t_\mathrm{fail}$ 사이에 잔여 수명이 존재할 수 있다.[1,2,5,6]

스트레스 중의 breakdown-spot 전류를 $I_\mathrm{BD}(t)$로 두면 제한된 구간에서 progressive growth를

$$
I_\mathrm{BD}(t)
=
I_\mathrm{BD}(0)
\exp\left(\frac{t-t_\mathrm{BD}}{\tau_\mathrm{PBD}}\right),
\qquad t\ge t_\mathrm{BD}
$$

로 적합할 수 있다. $\tau_\mathrm{PBD}$는 해당 전압·온도·전류 제한에서의 성장 시간 상수이다. 이 거동이 모든 breakdown path에 보편적으로 적용되는 것은 아니다. 최초 filament가 안정하거나 추가 경로가 독립적으로 생기면 단일 지수식과 다른 파형이 나타날 수 있다.[5,6]

Soft·progressive·hard breakdown은 순수하게 절연막 속성만으로 나뉘는 절대 등급이 아니다. 절연막 두께, 소자 면적, 판독 전압, 직렬저항, 전류 compliance, 저장된 에너지와 측정 대역폭이 최초 사건의 크기와 후속 손상을 바꾸므로, 파형과 함께 조건을 보고한다.[1,2,5,6]

## 2. 스트레스 시험과 고장 판정

Constant voltage stress (CVS)는 일정 게이트 전압 또는 절연막 전기장을, constant current stress (CCS)는 일정 주입 전류를 인가한다. CVS는 사용 전압과 직접 비교하기 쉽지만 breakdown 직후 전류 폭주를 제한해야 하고, CCS에서는 결함 생성에 따라 필요한 전압이 변한다.[1–4]

| 시험 방식 | 제어량 | 주 관측량 | 해석할 때 주의할 점 |
| --- | --- | --- | --- |
| CVS | $V_G$ 또는 $V_\mathrm{ox}$ | $I_G(t)$, $t_\mathrm{BD}$ | Breakdown 뒤 전류 폭주와 국소 발열을 compliance로 제한해야 함 |
| CCS | $I_G$ 또는 전류 밀도 $J_G$ | $V_G(t)$, voltage collapse | 열화 중 전기장이 변하므로 CVS의 전압 가속 계수를 직접 적용할 수 없음 |
| Ramp voltage stress | 전압 상승률 | breakdown voltage | 짧은 선별 시험이며 장시간 CVS의 $t_\mathrm{BD}$와 같은 통계량이 아님 |
| 저전계 판독 | 작은 판독 전압 | SILC, $I_G$–$V_G$ | 판독 자체가 추가 손상을 만들지 않는지 확인해야 함 |

!!! info "[Measurement]"
    1. 소자 면적, gate-stack 구성·물리 두께·equivalent oxide thickness (EOT), 온도와 모든 단자 바이어스를 기록한다.
    2. 스트레스 전 낮은 전기장의 $I_G$–$V_G$와 필요한 $C$–$V$를 측정해 누설·전하 포획의 기준을 만든다.
    3. 정해진 CVS 또는 CCS를 인가하면서 $I_G(t)$ 또는 $V_G(t)$를 충분한 시간 분해능으로 기록한다. 전압 램프·overshoot, sampling interval, 대역폭, 직렬저항과 compliance를 함께 저장한다.
    4. 미리 정한 전류 급증, $dI_G/dt$, 저전계 누설 증가 또는 회로 기능 기준으로 최초 $t_\mathrm{BD}$를 판정한다.
    5. 스트레스를 계속할 경우 post-breakdown 누설이 허용 한계 $I_\mathrm{fail}$를 처음 넘는 $t_\mathrm{fail}$도 별도로 기록한다.
    6. Soft·progressive·hard breakdown, 시험 종료까지 고장하지 않은 censored 시편과 extrinsic 시편을 구분한다.[1–6]

고장 판정 예시는

$$
t_\mathrm{BD}=\inf\left\{t:
\frac{I_G(t)}{I_{G,\mathrm{base}}(t)}\ge C_I
\right\}
$$

처럼 정의할 수 있다. $I_{G,\mathrm{base}}(t)$는 breakdown 전의 완만한 전류 추세이고 $C_I$는 시험 전에 정한 증가 배수이다. 이 기준은 예시이며, 절대 전류 임계값·전압 step 또는 noise 기준을 사용한다면 대역폭과 compliance까지 밝혀야 한다.[1–6]

회로 기능 수명을 누설 한계로 정의하면

$$
t_\mathrm{fail}
=
\inf\left\{t:I_\mathrm{BD}(t)\ge I_\mathrm{fail}\right\},
\qquad
t_\mathrm{res}=t_\mathrm{fail}-t_\mathrm{BD}
$$

이다. $t_\mathrm{res}$는 최초 breakdown 후의 잔여 수명이다. $I_\mathrm{fail}$은 보편 상수가 아니며 회로 노드, standby 전력, timing, logic level과 열 제약으로부터 정해야 한다.[5,6]

전하량을 기준으로 비교할 때 charge to breakdown은

$$
Q_\mathrm{BD}
=
\int_0^{t_\mathrm{BD}}\left|J_G(t)\right|\,dt
$$

로 정의된다. $Q_\mathrm{BD}$가 거의 일정하게 보이는 조건에서는 주입 전하와 결함 생성의 상관을 정리하는 데 유용하다. 그러나 주입 에너지 분포, 온도, 전기장과 운반자 종류가 달라지면 같은 전하량이 같은 손상을 뜻하지 않으므로, $Q_\mathrm{BD}$를 재료 고유의 보편 상수로 취급하지 않는다.[1,2,5]

!!! warning "[Interpretation Caveat]"
    측정 장비의 전류 compliance, 배선 직렬저항과 sampling interval은 관측되는 breakdown 크기와 시각을 바꿀 수 있다. 서로 다른 실험의 $t_\mathrm{BD}$를 비교할 때는 전기장만 맞추지 말고 판정 알고리즘과 측정 회로도 맞춘다.[1–4]

## 3. Weibull 통계와 면적 효과

두 매개변수 Weibull 분포로 breakdown 시간을 나타내면

$$
F(t)=1-\exp\left[-\left(\frac{t}{\eta}\right)^\beta\right]
$$

이다. $\eta$는 characteristic life, $\beta$는 shape parameter이다. Weibull 좌표의 직선성은 단일 모집단을 점검하는 도구이며, $\beta$의 값만으로 결함 생성 메커니즘을 확정하지 않는다.[1–4]

누적 고장 확률을

$$
Y
=
\ln\!\left[-\ln(1-F)\right]
=
\beta\ln t-\beta\ln\eta
$$

로 변환하면 단일 Weibull 모집단은 $\ln t$에 대해 기울기 $\beta$인 직선이 된다. 확률 $p$에서의 수명은

$$
t_p
=
\eta\left[-\ln(1-p)\right]^{1/\beta}
$$

이다. 제품 예측에 필요한 작은 $p$는 시험 표본이 실제로 관측한 확률 범위보다 훨씬 낮을 수 있으므로, $t_p$에는 적합 오차뿐 아니라 분포 모형과 면적 scaling의 불확실성도 포함한다.[1–4]

공간적으로 독립적인 동일 면적 요소가 weakest-link 방식으로 고장한다고 가정하면 기준 면적 $A_0$의 분포로부터 면적 $A$의 분포는

$$
F_A(t)=1-\left[1-F_{A_0}(t)\right]^{A/A_0}
$$

가 된다. 같은 $F$에서 큰 면적일수록 더 짧은 시간이 예측된다. 이 식은 전기장이 면적 전체에 균일하고 결함이 독립적이며 가장 약한 국소 경로가 전체 고장을 정한다는 가정에 제한된다.[1–4]

$A_0$와 $A$에서 같은 $\beta$를 유지한다면 characteristic life는

$$
\eta(A)
=
\eta(A_0)
\left(\frac{A_0}{A}\right)^{1/\beta}
$$

로 변환된다. 가장자리 전기장 집중, 서로 다른 산화막 두께 영역, 공간적으로 상관된 공정 결함 또는 여러 고장 모집단이 있으면 단순 면적 비 대신 각 영역의 전기장과 분포를 따로 모델링해야 한다.[1–5]

!!! note "[Metric]"
    표본별 $(t_\mathrm{BD},\text{고장 여부})$와 면적을 보존하고 censored maximum likelihood estimation으로 $\eta$와 $\beta$를 구한다. 보고할 수명은 평균만이 아니라 $t_{p}$처럼 지정한 누적 고장 확률의 분위수와 신뢰구간으로 제시한다.[1–4]

| 보고 지표 | 정의 또는 단위 | 답하는 질문 |
| --- | --- | --- |
| $t_\mathrm{BD}$ | 최초 breakdown까지의 시간, s | 임계 경로가 언제 처음 형성되는가? |
| $Q_\mathrm{BD}$ | breakdown까지의 면적당 누적 전하, C/cm$^2$ | 주입 전하 기준의 손상량은 얼마인가? |
| $\beta$, $\eta$ | Weibull shape와 characteristic life | 분포의 폭과 기준 수명은 무엇인가? |
| $t_p$ | 누적 고장 확률 $p$의 분위수, s | 요구 불량률에서 수명은 얼마인가? |
| $t_\mathrm{res}$ | $t_\mathrm{fail}-t_\mathrm{BD}$, s | 최초 breakdown 뒤 회로 허용 한계까지 얼마나 남는가? |

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

식의 $E_\mathrm{ox}$는 외부 게이트 전압을 단순히 EOT로 나눈 값과 항상 같지 않다. 반도체의 표면전위와 전극의 일함수 차이를 제외한 실제 절연막 전압을 구하고, 동일한 전압 정의를 시험과 사용 조건에 적용해야 한다. 특히 계면층과 high-$k$ 층이 직렬로 놓인 적층 구조에서 자유 계면 전하를 무시하면

$$
D=\varepsilon_i E_i,
\qquad
V_\mathrm{ox}=\sum_i E_i t_i
$$

이므로 각 층의 전기장 $E_i$는 유전율 $\varepsilon_i$와 물리 두께 $t_i$에 따라 다르다. EOT가 같아도 각 층의 전기장, trap density와 결함 생성률이 같다는 뜻은 아니다.[2,5,7,8]

온도 의존성도 단일 Arrhenius 식에서 벗어날 수 있다. 터널링 전류, defect generation과 국소 발열의 온도 의존성이 함께 들어가므로, 고정한 게이트 전압과 고정한 절연막 전기장 시험이 동일한 열 가속을 준다고 가정하지 않는다.[1–4]

### (1) 외삽 검증

여러 전기장과 온도에서 Weibull 기울기, 고장 신호와 사후 전기 특성을 비교한다. 고장 모드가 유지되는 구간만 공동 적합하고, 중간 스트레스 셀을 적합에서 제외한 뒤 예측하는 방식으로 모형을 교차 검증한다.[1–4]

최초 breakdown의 wear-out 시간과 post-breakdown 성장 시간은 같은 가속 계수를 공유한다고 가정하지 않는다. 서로 다른 안정·성장 filament가 관측될 수 있고 hard breakdown까지의 가속도 최초 $t_\mathrm{BD}$의 가속과 다를 수 있으므로, $t_\mathrm{BD}$와 $t_\mathrm{res}$를 분리해 전압·온도 의존성을 적합한다.[5,6]

매우 낮은 고장 확률과 긴 사용 시간의 예측에는 통계적 신뢰구간 외에 가속식 선택의 불확실성이 지배할 수 있다. 후보 모형이 시험 자료에서 구분되지 않으면 하나의 숫자보다 각 모형의 예측 범위와 검증 한계를 보고한다.[1–4]

## 5. 적층 gate stack과 회로 해석

High-$k$/metal gate stack은 얇은 SiO$_x$ 계면층과 high-$k$ 층이 직렬로 놓인 복합 절연막이다. 스트레스 중 두 층에서 서로 다른 속도로 결함이 생성되고, 어느 층에 기존 결함이 많은지에 따라 shallow·steep Weibull 구간이나 혼합 분포가 나타날 수 있다. 따라서 단일층 SiO$_2$의 $\beta$와 가속 계수를 EOT만 맞춰 이전하지 않고 층별 전기장과 결함 분포를 포함해 검증한다.[5,7,8]

High-$k$ 적층에서도 bulk trap의 생성과 percolation, soft breakdown 뒤 추가 wear-out이라는 기본 틀은 유용하다. 다만 한 번의 soft breakdown이 넓은 소자의 전체 전류에서 작게 보일 수 있고, 여러 국소 경로의 누설 합이 hard breakdown보다 먼저 응용 회로의 허용 전류를 넘을 수 있다. 검출 한계와 회로 기준을 함께 사용해야 하는 이유이다.[2,7,8]

Soft breakdown 뒤에도 단일 트랜지스터가 계속 동작할 수 있지만, 증가한 게이트 전류와 잡음은 회로 상태와 민감한 노드에 따라 기능 오류를 일으킬 수 있다. 반대로 단일 소자의 전류 step을 곧바로 칩 고장으로 등치하면 회로의 여유와 redundancy를 무시하게 된다.[1,2,5,6]

| 회로 수준 결과 | 연결되는 절연막 관측 | 기능 고장 기준의 예 |
| --- | --- | --- |
| 대기 전력 증가 | 한 개 또는 여러 soft-breakdown path의 누설 합 | 허용 standby current 초과 |
| 저장 노드 교란 | 민감한 노드로 흐르는 국소 게이트 전류 | 보존 시간 또는 logic level 위반 |
| 지연·잡음 증가 | trap·breakdown에 따른 전류 fluctuation과 동작점 변화 | timing 또는 noise margin 위반 |
| 열적 손상·단락 | progressive/hard breakdown의 큰 전류 | 온도·전류·기능 안전 한계 초과 |

!!! warning "[Interpretation Caveat]"
    소자 TDDB 분포를 칩 고장률로 변환하려면 실제 gate area의 합만이 아니라 각 소자의 전압 duty cycle, 온도 이력, 회로 상태별 $I_\mathrm{fail}$과 고장 간 의존성을 반영해야 한다. 이 단계는 단일 소자의 면적 scaling과 동일하지 않다.[1,4–8]

## 6. 요약

- TDDB는 절연막 결함의 시간적 축적과 임계 percolation 경로 형성으로 나타나는 wear-out 고장이다.
- SILC, 최초 soft breakdown, progressive breakdown과 hard breakdown을 구분하고 측정 회로·판정 기준을 수명 정의에 포함한다.
- $t_\mathrm{BD}$, $Q_\mathrm{BD}$, Weibull 분위수와 $t_\mathrm{res}$는 서로 다른 질문에 답하므로 정의와 단위를 함께 보고한다.
- Weibull 분포와 weakest-link 면적 scaling은 독립 결함·균일 전기장·단일 모집단 가정이 성립하는 범위에서 사용한다.
- $E$, $1/E$와 power-law 외삽식은 경쟁 모형이며, 고전계 적합만으로 사용 조건의 장기 수명을 확정하지 않는다.
- High-$k$ 적층에서는 EOT만으로 층별 전기장을 정할 수 없으며, 최초 breakdown과 회로 기능 고장의 수명도 분리해야 한다.

## 7. 참고문헌

1. J. H. Stathis, “Physical and Predictive Models of Ultrathin Oxide Reliability in CMOS Devices and Circuits,” *IEEE Transactions on Device and Materials Reliability* **1**, 43–59 (2001). [DOI](https://doi.org/10.1109/7298.946459)
2. J. S. Suehle, “Ultrathin Gate Oxide Reliability: Physical Models, Statistics, and Characterization,” *IEEE Transactions on Electron Devices* **49**, 958–971 (2002). [DOI](https://doi.org/10.1109/TED.2002.1003712)
3. R. Degraeve, G. Groeseneken, R. Bellens, J. L. Ogier, M. Depas, P. J. Roussel, and H. E. Maes, “New Insights in the Relation Between Electron Trap Generation and the Statistical Properties of Oxide Breakdown,” *IEEE Transactions on Electron Devices* **45**, 904–911 (1998). [DOI](https://doi.org/10.1109/16.662800)
4. M. White and J. B. Bernstein, *Microelectronics Reliability: Physics-of-Failure Based Modeling and Lifetime Evaluation*, JPL Publication 08-5, Jet Propulsion Laboratory (2008). [PDF](https://nepp.nasa.gov/files/16365/08_102_4_%20JPL_White.pdf)
5. S. Lombardo, J. H. Stathis, B. P. Linder, K. L. Pey, F. Palumbo, and C. H. Tung, “Dielectric Breakdown Mechanisms in Gate Oxides,” *Journal of Applied Physics* **98**, 121301 (2005). [DOI](https://doi.org/10.1063/1.2147714)
6. J. S. Suehle, B. Zhu, Y. Chen, and J. B. Bernstein, “Detailed Study and Projection of Hard Breakdown Evolution in Ultra-Thin Gate Oxides,” *Microelectronics Reliability* **45**, 419–426 (2005). [DOI](https://doi.org/10.1016/j.microrel.2004.10.018)
7. R. Degraeve, M. Aoulaiche, B. Kaczer, P. J. Roussel, T. Kauerauf, S. Sahhaf, and G. Groeseneken, “Review of Reliability Issues in High-$k$/Metal Gate Stacks,” *2008 IEEE International Symposium on the Physical and Failure Analysis of Integrated Circuits*, 1–6 (2008). [DOI](https://doi.org/10.1109/IPFA.2008.4588195)
8. T. Nigam, A. Kerber, and P. Peumans, “Accurate Model for Time-Dependent Dielectric Breakdown of High-$k$ Metal Gate Stacks,” *2009 IEEE International Reliability Physics Symposium*, 523–530 (2009). [DOI](https://doi.org/10.1109/IRPS.2009.5173307)
