---
title: "4.5. Device reliability: Interconnect reliability"
description: Electromigration의 원자 flux, void·hillock 형성, Black 모형, Blech criterion과 배선 수명 측정을 설명
status: verified
last_verified: 2026-08-12
---

# 4.5. Device reliability: Interconnect reliability

Interconnect reliability는 금속 배선과 via가 사용 기간 동안 요구 전류를 전달하는 능력을 다룬다. 이 문서의 중심은 높은 전류 밀도에서 전자와 금속 원자 사이의 운동량 전달로 물질이 재분포하는 electromigration (EM)이다. EM은 원자 flux의 발산 위치에서 void 또는 hillock을 만들며, 각각 저항 증가·open과 인접선 short로 이어질 수 있다.[1–6]

## 1. Electromigration의 구동력

전기장 속 금속 이온에는 직접 electrostatic force와 전자가 전달하는 electron-wind force가 작용한다. 일반적인 금속 배선에서는 유효 전하수 $Z^*$로 두 효과를 합쳐 원자당 전기적 구동력을

$$
F_\mathrm{EM}=Z^*e\rho J
$$

로 나타낼 수 있다. $e$는 기본전하, $\rho$는 비저항, $J$는 conventional current density이다. $Z^*$의 부호와 좌표 규약에 따라 flux 식의 부호가 달라지므로, 실험에서는 전자 흐름과 conventional current 방향을 함께 표시한다.[1–6]

<figure markdown="span">
  ![금속 배선에서 전기장, 전자 흐름, electron-wind force와 금속 이온 이동](images/electromigration-electron-wind.png)
  <figcaption markdown="1">
    그림 1. 금속 배선에서 전기장, 전자 흐름과 electron-wind force에 의한 금속 이온 이동의 개념도. 그림의 방향은 conventional current와 전자 흐름을 구분해 읽어야 한다.
    출처: P. Cheng et al., “Electromigration Failures in Integrated Circuits: A Review of Physics-Based Models and Analytical Methods,” Figure 2 (2025),
    <a href="https://doi.org/10.3390/electronics14153151">DOI</a>,
    <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>, 수정 없음.[6]
  </figcaption>
</figure>

## 2. 원자 flux와 응력

등온 1차원 근사에서 원자 flux $J_a$는 전기적 구동력과 hydrostatic stress $\sigma$의 기울기를 포함하여

$$
J_a
=-\frac{DC}{kT}
\left(
Z^*e\rho J-\Omega\frac{\partial\sigma}{\partial x}
\right)
$$

처럼 쓸 수 있다. $D$는 유효 확산계수, $C$는 이동 가능한 원자 농도, $\Omega$는 원자 부피이다. 첫 항은 EM을 구동하고, 둘째 항은 물질 축적·고갈로 생긴 back stress가 flux에 대항하는 효과를 나타낸다.[2–6]

국소적인 원자 수 변화는 flux divergence에 의해 정해진다.

$$
\frac{\partial C}{\partial t}=-\nabla\cdot J_a
$$

Flux가 공간적으로 일정하면 원자가 이동하더라도 그 구간에 즉시 void가 생기지 않는다. 재료 경계, via, line-width 변화, grain boundary와 온도 구배처럼 flux가 불연속적으로 변하는 위치가 void nucleation과 물질 축적의 취약점이 된다.[2–6]

### (1) 확산 경로와 형상

유효 확산계수는 lattice, grain boundary, 계면과 표면 경로의 기여를 포함한다. 어느 경로가 지배하는지는 금속 재료, 결정립 크기, liner·cap 계면과 온도에 따라 달라진다. 따라서 한 재료에서 얻은 활성화 에너지를 다른 배선 적층이나 선폭에 그대로 적용할 수 없다.[2–6]

Current crowding은 via 모서리와 폭이 급변하는 구간에서 국소 $J$를 평균값보다 크게 만든다. Joule heating은 동시에 국소 온도를 높여 확산을 빠르게 하므로, 설계 전류를 단면적으로 나눈 값과 chuck 온도만으로 수명을 계산하면 위험 지점을 놓칠 수 있다.[2–6]

## 3. Black 모형과 Blech criterion

Black’s equation은 일정한 전류 밀도와 온도에서 평균 또는 characteristic failure time을

$$
t_f=AJ^{-n}\exp\left(\frac{E_a}{kT}\right)
$$

로 나타내는 경험 모형이다. $A$는 재료·형상·고장 기준을 포함한 계수, $n$은 current exponent, $E_a$는 유효 활성화 에너지이다. 이 식은 시험 범위의 축약적 상관관계이며 void nucleation 위치, 응력 경계와 짧은 배선 효과를 명시적으로 풀지 않는다.[1,2,5,6]

짧고 기계적으로 구속된 배선에서는 원자 이동이 만든 back stress가 EM 구동력과 균형을 이룰 수 있다. 이상화한 Blech criterion은

$$
|J|L\le (JL)_\mathrm{crit}
\approx\frac{\Omega\,\Delta\sigma_\mathrm{crit}}
{|Z^*|e\rho}
$$

처럼 나타낸다. $L$은 유효 배선 길이, $\Delta\sigma_\mathrm{crit}$는 void nucleation 또는 재료 항복 전에 허용되는 응력 차이다. 임계 $JL$ 아래에서 “완전한 면역”이라고 단정하려면 blocking boundary와 균일한 재료라는 가정을 확인해야 한다.[3–6]

Korhonen 모형은 구속된 배선의 응력 진화를 확산 방정식으로 풀어 시간과 위치에 따른 $\sigma(x,t)$를 예측한다. 이 접근은 Black 모형이 숨긴 길이, 경계 조건과 back-stress 형성을 명시하지만, 재료 매개변수와 void nucleation 기준이 필요하다.[4–6]

## 4. 시험과 고장 판정

!!! info "[Measurement]"
    Kelvin 또는 four-terminal 구조에서 초기 저항 $R_0$를 측정한다. 정해진 전류 파형을 인가하고 실제 금속 온도를 추정하면서 $R(t)$를 주기적으로 판독한다. 고장 시간을

    $$
    t_f=\inf\left\{t:\frac{R(t)-R_0}{R_0}\ge\delta R_\mathrm{crit}\right\}
    $$

    로 정하고 $\delta R_\mathrm{crit}$, 판독 전류, sampling interval과 compliance를 기록한다. 시험 뒤에는 void·hillock 위치와 via open 여부를 물리적으로 확인한다.[1,2,5,6]

여러 $J$와 $T$ 셀에서 얻은 $t_f$ 분포로 $n$과 $E_a$를 적합한다. 전류를 바꿀 때 Joule heating도 바뀌므로, 환경 온도가 아니라 배선의 실제 온도를 사용하거나 열 보정을 별도로 검증해야 한다.[1,2,5,6]

!!! note "[Metric]"
    저항 임계값 수명과 완전 open 수명은 같은 분포가 아닐 수 있다. 평균 time to failure만 보고하지 말고 표본 수, censored 수, Weibull 또는 lognormal 분포 매개변수, 배선 폭·두께·길이, via 수와 전류 방향을 함께 제시한다.[1,2,5,6]

## 5. 실제 배선에서의 해석

직류 가속 시험의 $J$를 회로의 평균 전류로 단순 대체하면 양방향 전류, 듀티비와 recovery를 놓칠 수 있다. 원자 이동의 방향성과 열 시정수를 포함한 파형으로 등가 스트레스를 계산해야 하며, 짧은 펄스가 언제나 평균 전류만큼의 손상을 준다는 가정은 별도 검증이 필요하다.[2,5,6]

!!! warning "[Interpretation Caveat]"
    저항 증가는 EM void 외에도 contact 열화, 계면 반응과 측정 온도 변화에서 생길 수 있다. 반대로 국소 void가 병렬 전류 경로 때문에 초기 저항에 작게 나타날 수도 있다. 전기적 수명 분포와 물리적 고장 위치를 연결한다.[2,5,6]

EM은 배선 신뢰성의 전부가 아니다. Stress migration, thermomigration, time-dependent dielectric breakdown of low-$k$ dielectrics와 package-induced mechanical stress도 배선층 고장을 만들 수 있다. 이 문서의 Black·Blech 식은 그 현상들을 자동으로 포함하지 않는다.[2,5,6]

## 6. 요약

- EM은 전류가 구동하는 원자 이동이며, 고장은 원자 flux 자체보다 flux divergence가 큰 위치에서 시작한다.
- Back stress는 EM flux에 대항하고 짧은 배선의 임계 $JL$ 거동을 만든다.
- Black’s equation은 전류 밀도와 온도의 경험적 수명식이고, Blech·Korhonen 모형은 길이와 응력 경계를 추가한다.
- 수명 시험에는 국소 전류 집중, 실제 금속 온도, 저항 임계값과 물리적 고장 위치를 함께 포함한다.

## 7. 참고문헌

1. J. R. Black, “Electromigration—A Brief Survey and Some Recent Results,” *IEEE Transactions on Electron Devices* **16**, 338–347 (1969). [DOI](https://doi.org/10.1109/T-ED.1969.16754)
2. J. R. Lloyd, “Electromigration in Integrated Circuit Conductors,” *Journal of Physics D: Applied Physics* **32**, R109–R118 (1999). [DOI](https://doi.org/10.1088/0022-3727/32/17/201)
3. I. A. Blech, “Electromigration in Thin Aluminum Films on Titanium Nitride,” *Journal of Applied Physics* **47**, 1203–1208 (1976). [DOI](https://doi.org/10.1063/1.322842)
4. M. A. Korhonen, P. Borgesen, K. N. Tu, and C. Y. Li, “Stress Evolution Due to Electromigration in Confined Metal Lines,” *Journal of Applied Physics* **73**, 3790–3799 (1993). [DOI](https://doi.org/10.1063/1.354073)
5. M. White and J. B. Bernstein, *Microelectronics Reliability: Physics-of-Failure Based Modeling and Lifetime Evaluation*, JPL Publication 08-5, Jet Propulsion Laboratory (2008). [PDF](https://nepp.nasa.gov/files/16365/08_102_4_%20JPL_White.pdf)
6. P. Cheng, L.-F. Mao, W.-H. Shen, and Y.-L. Yan, “Electromigration Failures in Integrated Circuits: A Review of Physics-Based Models and Analytical Methods,” *Electronics* **14**, 3151 (2025). [DOI](https://doi.org/10.3390/electronics14153151)
