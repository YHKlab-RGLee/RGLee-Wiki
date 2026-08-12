---
title: "4.3. Device reliability: Hot-carrier degradation"
description: 드레인 고전계에서의 hot-carrier 결함 생성, 바이어스 영역, 전기적 열화와 수명 측정법을 설명
status: verified
last_verified: 2026-08-12
---

# 4.3. Device reliability: Hot-carrier degradation

Hot-carrier degradation (HCD)은 채널과 드레인 부근의 높은 전기장에서 에너지를 얻은 운반자가 계면·절연막 결함을 생성하거나 기존 트랩의 전하 상태를 바꾸어 metal-oxide-semiconductor field-effect transistor (MOSFET) 특성을 열화시키는 현상이다. 고전적인 장채널 nMOS에서는 impact ionization과 기판 전류가 중요한 지표였지만, 짧은 채널과 새로운 구조에서는 운반자 에너지 분포, 다단계 결합 파괴와 자가 발열까지 고려해야 한다.[1–5]

## 1. 고전계 운반자와 결함 생성

드레인 전압이 높으면 드레인 쪽 채널의 큰 수평 전기장에서 운반자가 에너지를 얻는다. 일부는 impact ionization을 일으키고, 일부는 Si–H와 같은 계면 결합을 직접 끊거나 여러 번의 낮은 에너지 충돌로 진동 여기 상태를 축적하여 결함을 만들 수 있다. 생성된 interface trap과 oxide trap은 채널 전하와 산란을 바꾼다.[1–4]

고전적인 국소 모형에서는 드레인 근처의 impact-ionization 전류 $I_B$ 또는 gate current를 손상 속도의 대리량으로 사용했다. 그러나 현대의 짧은 채널에서는 결함 생성에 기여하는 운반자와 측정된 기판 전류가 항상 같은 에너지 창을 대표하지 않으며, 낮은 $V_G$에서 생성되는 secondary carrier도 중요할 수 있다.[1–4]

### (1) 단일·다중 입자 과정

Single-particle 과정은 한 운반자가 결합 파괴 장벽을 넘을 만큼 큰 에너지를 전달한다고 본다. Multiple-particle 과정은 여러 운반자가 결합 진동을 단계적으로 여기하여 낮은 개별 에너지에서도 결함을 만들 수 있다고 본다. 실제 예측 모형은 운반자 에너지 분포 함수와 각 과정의 반응 단면적을 결합한다.[2–4]

이 구분은 “hot carrier”를 하나의 유효 온도로 나타내는 단순화의 한계를 보여준다. 비평형 운반자 분포의 높은 에너지 꼬리와 국소 전기장, 산란 경로를 보지 않으면 바이어스에 따른 열화 최대점을 잘못 예측할 수 있다.[2–4]

## 2. 바이어스 영역과 혼합 열화

HCD는 $V_G$와 $V_D$의 조합으로 정해야 한다. 높은 $V_G$와 비교적 낮은 $V_D$에서는 [bias temperature instability (BTI)](bias-temperature-instability.md) 성분이 커질 수 있고, 높은 $V_D$에서는 HCD가 강해진다. 실제 회로 바이어스에는 두 성분이 함께 존재하는 영역이 있다.[3–5]

<figure markdown="span">
  ![VGS와 VDS 바이어스 공간에서 BTI, HCD와 혼합 열화가 지배하는 영역](images/hcd-bias-space.png)
  <figcaption markdown="1">
    그림 1. $V_{GS}$–$V_{DS}$ 바이어스 공간에서 BTI 우세, HCD 우세와 혼합 영역을 구분한 개념도. 영역 경계는 기술과 판정 지표에 따라 달라지므로 정량적인 보편 경계로 사용하지 않는다.
    출처: H. Zhou, “An Overview of Hot Carrier Degradation on Gate-All-Around Nanosheet Transistors,” Figure 4 (2025),
    <a href="https://doi.org/10.3390/mi16030311">DOI</a>,
    <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>, 수정 없음.[5]
  </figcaption>
</figure>

장채널 nMOS의 고전적인 worst-case 조건은 최대 기판 전류 부근으로 정하는 경우가 많았다. 그러나 shortest-channel 소자, pMOS, FinFET과 gate-all-around (GAA) nanosheet에서는 최대 열화가 같은 조건에 놓인다고 가정할 수 없다. 실제 동작 범위를 덮는 $V_G$–$V_D$ 행렬을 측정해야 한다.[1–5]

## 3. 전기적 열화 신호

드레인 쪽에 국소적으로 형성된 interface trap은 선형 영역과 포화 영역의 전류에 서로 다르게 반영될 수 있다. 대표 관측량은 $\Delta V_T$, $\Delta g_m$, 저전압의 $\Delta I_{D,\mathrm{lin}}$와 높은 드레인 전압의 $\Delta I_{D,\mathrm{sat}}$이다.[1–5]

$$
\delta I_{D,\mathrm{lin}}(t)
=\frac{I_{D,\mathrm{lin}}(t)-I_{D,\mathrm{lin},0}}
{|I_{D,\mathrm{lin},0}|}
$$

분모에 초기 전류의 크기를 사용하여 nMOS와 pMOS의 부호 차이를 피한다. 모든 비교에서는 같은 판독 바이어스와 온도를 사용한다.[1,4,5]

| 관측량 | 민감한 변화 | 단독 해석의 한계 |
| --- | --- | --- |
| $\Delta V_T$ | 유효 트랩 전하 | BTI도 같은 변화를 생성 |
| $\Delta g_m$ | 이동도·계면 산란 | 직렬저항과 추출점에 민감 |
| $\Delta I_{D,\mathrm{lin}}$ | 채널 전체의 전도 변화 | $V_T$ 이동과 mobility가 결합 |
| $\Delta I_{D,\mathrm{sat}}$ | 고전계 동작 성능 | 자가 발열과 직렬저항 포함 |
| $I_B$ | impact ionization | 현대 소자의 총 손상률과 일대일 대응 아님 |

## 4. 스트레스와 수명 추출

!!! info "[Measurement]"
    1. 초기 $I_D$–$V_G$, $I_D$–$V_D$, $g_m$과 가능한 경우 $I_B$를 측정한다.
    2. 실제 동작 범위를 포함하는 여러 $(V_{G,\mathrm{str}},V_{D,\mathrm{str}})$와 온도에서 스트레스한다.
    3. 각 스트레스 구간 뒤 같은 낮은 교란의 바이어스에서 $V_T$, $I_{D,\mathrm{lin}}$, $I_{D,\mathrm{sat}}$와 $g_m$을 빠르게 판독한다.
    4. 열화 기준 $|\Delta X/X_0|=D_\mathrm{crit}$에 도달한 시간을 $t_f$로 정한다.
    5. 스트레스 중의 전류와 실제 소자 온도를 기록하여 전기적 가속과 자가 발열을 구분한다.[1–5]

제한된 범위에서 열화는

$$
|\Delta X(t)|=A(V_G,V_D,T)t^n
$$

으로 적합할 수 있다. $A$는 바이어스와 온도를 포함한 속도 계수, $n$은 시간 지수이다. 미시적 결함 생성률이 시간 내내 같은 거듭제곱 법칙을 따른다는 뜻은 아니며, 포화·회복·다른 메커니즘의 개입 여부를 확인해야 한다.[2–5]

!!! note "[Metric]"
    수명 보고에는 $X$와 $D_\mathrm{crit}$, stress/read 바이어스, 온도, 소자 형상, 시간 적합 구간과 censored 시편을 포함한다. 동일한 “10% 전류 감소”라도 선형 전류와 포화 전류는 서로 다른 공간적 민감도를 가지므로 서로 바꾸어 쓰지 않는다.[1,4,5]

## 5. 구조와 온도의 영향

HCD의 온도 의존성은 한 방향의 Arrhenius 항으로만 정리되지 않을 수 있다. 온도 상승은 phonon 산란으로 운반자 에너지 분포를 낮추는 한편, 결합 파괴와 자가 발열 관련 반응을 빠르게 할 수 있다. 측정 온도 범위와 바이어스에 따라 겉보기 활성화 거동이 달라질 수 있다.[2–5]

GAA nanosheet에서는 표면 방향, sheet 폭·두께, 모서리 전기장, inner spacer와 열 제거 경로가 열화의 공간 분포에 영향을 준다. 따라서 평면형 MOSFET에서 보정한 기판 전류 기반 수명식을 구조 매개변수 없이 옮기는 것은 적절하지 않다.[3–5]

!!! warning "[Interpretation Caveat]"
    $I_B$의 최대점, $\Delta V_T$ 또는 하나의 온도 가속 계수만으로 HCD를 판정하지 않는다. BTI 대조 스트레스, 여러 판독량, 바이어스 지도와 실제 접합 온도를 함께 비교한다.[2–5]

## 6. 요약

- HCD는 고전계에서 형성된 비평형 운반자가 계면·절연막 결함을 만들거나 점유 상태를 바꾸는 열화이다.
- Impact ionization은 고전적 지표이지만, 현대 소자의 결함 생성에는 단일·다중 입자 과정과 secondary carrier가 관여할 수 있다.
- HCD와 BTI는 $V_G$–$V_D$ 공간에서 혼합되므로 실제 동작 범위를 덮는 바이어스 행렬이 필요하다.
- 수명은 특정 전기량의 열화 기준, 판독 조건과 실제 소자 온도를 포함하여 정의한다.

## 7. 참고문헌

1. C. Hu, S. C. Tam, F.-C. Hsu, P.-K. Ko, T.-Y. Chan, and K. W. Terrill, “Hot-Electron-Induced MOSFET Degradation—Model, Monitor, and Improvement,” *IEEE Transactions on Electron Devices* **32**, 375–385 (1985). [DOI](https://doi.org/10.1109/T-ED.1985.21952)
2. A. Acovic, G. La Rosa, and Y.-C. Sun, “A Review of Hot-Carrier Degradation Mechanisms in MOSFETs,” *Microelectronics Reliability* **36**, 845–869 (1996). [DOI](https://doi.org/10.1016/0026-2714(96)00022-4)
3. M. Bina et al., “Predictive Hot-Carrier Modeling of n-Channel MOSFETs,” *IEEE Transactions on Electron Devices* **61**, 3103–3110 (2014). [DOI](https://doi.org/10.1109/TED.2014.2340575)
4. S. Tyaginov et al., “Compact Physics Hot-Carrier Degradation Model Valid over a Wide Bias Range,” *Micromachines* **14**, 2018 (2023). [DOI](https://doi.org/10.3390/mi14112018)
5. H. Zhou, “An Overview of Hot Carrier Degradation on Gate-All-Around Nanosheet Transistors,” *Micromachines* **16**, 311 (2025). [DOI](https://doi.org/10.3390/mi16030311)
