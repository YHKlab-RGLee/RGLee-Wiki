---
title: "(2) MOSFET: Short-Channel Effects"
description: MOSFET의 단채널 효과와 동반 고전계 효과를 물리 기작, 실험 절차, 정량 metric으로 설명
status: verified
last_verified: 2026-07-31
---

# (2) MOSFET: Short-Channel Effects

MOSFET의 channel length가 source/drain 공핍영역과 gate가 제어하는 electrostatic length에 가까워지면, channel potential을 gate 혼자 결정한다는 long-channel 가정이 무너진다. 그 결과 $V_T$ roll-off, drain-induced barrier lowering(DIBL), subthreshold swing 악화, punch-through가 나타난다. 짧은 채널에서 함께 두드러지는 channel-length modulation, velocity saturation, impact ionization과 hot-carrier degradation은 중요하지만, 엄밀히는 각각 출력 electrostatics, 비평형 수송, 신뢰성 효과이므로 좁은 의미의 electrostatic SCE와 구분한다.[1–4]

<figure markdown="span">
  ![채널 길이가 짧아질수록 source-channel 에너지 장벽이 낮아지는 schematic](images/barrier-lowering-length.svg)
  <figcaption>
    그림 1. 채널 길이가 짧아질수록 drain의 영향으로 source-side 장벽이 낮아지는 개념도.
    출처: Sjoerd Terlouw, “Barrier lowering length,” Wikimedia Commons,
    <a href="https://commons.wikimedia.org/wiki/File:Barrier_lowering_length.svg">CC BY-SA 4.0</a>, 수정 없음.
    정량 관계는 본문의 문헌 [1–3]을 따른다.[13]
  </figcaption>
</figure>

## 1. Scope and Conventions

기본 대상은 planar bulk nMOS, $V_S=V_B=0$인 DC 측정이다. 전류는 크기 $|I_D|$를 쓰며, 폭 정규화 값을 병기한다. 모든 length split은 가능하면 같은 wafer, 같은 폭, 같은 orientation과 공정 조건에서 비교한다.

이 문서의 분류는 다음과 같다.

- **엄밀한 electrostatic SCE:** $V_T$ roll-off, DIBL, SS degradation, punch-through
- **함께 평가할 출력·수송·신뢰성 효과:** channel-length modulation(CLM), velocity saturation, impact ionization/hot-carrier effect

BSIM 계열 compact model도 threshold roll-off, DIBL, subthreshold effect, velocity saturation, CLM 등을 서로 다른 물리 항으로 취급한다. 따라서 “짧은 소자에서 보인다”는 이유만으로 모든 현상을 하나의 SCE metric으로 합치지 않는다.[1,4]

## 2. Measurement Design and Metrics

가장 작은 측정 세트는 여러 channel length의 $I_D$–$V_G$를 낮은 $V_D$와 높은 $V_D$에서 측정하고, 각 $V_G$에서 $I_D$–$V_D$를 추가하는 것이다. Body current와 gate current를 함께 읽으면 impact ionization, GIDL, gate leakage가 $I_D$ 추출을 오염시키는지 확인할 수 있다. 저전류 영역은 guarding, 차폐, settling과 sweep history를 관리해야 한다.[5–7]

| 현상 | 핵심 sweep | 대표 metric |
| --- | --- | --- |
| $V_T$ roll-off | length split의 낮은-$V_D$ $I_D$–$V_G$ | $\Delta V_{T,\mathrm{roll}}(L)$ |
| DIBL | 같은 소자의 낮은/높은-$V_D$ $I_D$–$V_G$ | mV/V |
| SS degradation | 반로그 $I_D$–$V_G$ | SS (mV/dec), 전류 window |
| Punch-through | off-state $I_D$–$V_D$, length split | $V_\mathrm{PT}$, $g_{ds,\mathrm{off}}$ |
| CLM | saturation 영역 $I_D$–$V_D$ | $g_{ds}$, $r_o$, $\lambda_\mathrm{CLM}$ |
| Velocity saturation | $I_D$–$V_G$, $I_D$–$V_D$, $g_m$ | $V_{DS,\mathrm{sat}}$, $g_m$, current exponent |
| Hot-carrier effect | stress 전후 transfer/output curve | $I_B/I_D$, $\Delta V_T$, $\Delta g_m$, lifetime |

!!! note "$V_T$ 추출 규약"
    Constant-current, transconductance extrapolation 등은 서로 다른 $V_T$를 줄 수 있다. 한 비교 세트에서는 한 방법과 한 기준전류를 고정하고, 기준전류의 폭 정규화, $V_D$, sweep 방향, 온도를 보고해야 한다.[1,5]

## 3. Electrostatic Short-Channel Effects

좁은 의미의 electrostatic SCE는 gate의 channel-potential 제어가 source와 drain의 전기장에 의해 약해지는 현상을 묶는다.

### (1) Threshold-Voltage Roll-Off

Long-channel에서는 gate가 channel depletion charge를 주로 지탱하지만, 채널이 짧아지면 source/drain depletion region이 그 전하의 일부를 공유한다. Gate가 담당해야 할 전하가 줄어들므로 같은 surface condition에 필요한 gate voltage, 즉 nMOS의 $V_T$가 낮아진다. 이 charge sharing이 고전적인 $V_T$ roll-off의 물리적 그림이다.[1–3]

길이 $L$에서의 roll-off를

$$
\Delta V_{T,\mathrm{roll}}(L)
=V_T(L)-V_T(L_\mathrm{ref})
$$

로 정의한다. $L_\mathrm{ref}$는 long-channel plateau에 있는 reference device이다. 이 규약에서 nMOS의 정상적인 roll-off는 음수이며, 문헌이 $|\Delta V_T|$만 보고하는 경우 부호가 다르므로 구분해야 한다.[1,2,5]

**실험과 metric.** 작은 $V_D$에서 length split의 $I_D$–$V_G$를 측정하고 동일한 constant-current criterion으로 $V_T$를 추출한다. $\Delta V_{T,\mathrm{roll}}$–$L$ 또는 $V_T$–$L$을 그리되, series resistance와 width variation을 줄이기 위해 낮은 기준전류를 사용한다. Reverse short-channel effect처럼 halo implant와 공정 비균일성이 $V_T$를 다시 높일 수 있으므로, 단조감소를 미리 가정하지 않고 doping split과 비교한다.[1–3]

### (2) Drain-Induced Barrier Lowering

DIBL은 drain 전압 증가가 source–channel energy barrier를 낮추어, 같은 drain current에 필요한 gate voltage를 감소시키는 현상이다. 이는 그림 1의 수직 장벽 감소에 해당하며, 높은 $V_D$에서 subthreshold current와 $I_\mathrm{OFF}$를 증가시킨다.[1–3]

이 문서에서는 양의 값이 되도록

$$
\mathrm{DIBL}
=\frac{V_T(V_{D,\mathrm{low}})-V_T(V_{D,\mathrm{high}})}
{V_{D,\mathrm{high}}-V_{D,\mathrm{low}}}
$$

로 정의한다. 단위는 V/V 또는 mV/V이다. 일부 문헌은 $\Delta V_T/\Delta V_D$를 그대로 써 음의 값을 보고하므로, 부호 규약을 반드시 확인한다.[1,2]

**실험과 metric.** 동일 소자와 동일 기준전류에서 두 $I_D$–$V_G$ 곡선의 $V_T$를 추출한다. $V_{D,\mathrm{low}}$와 $V_{D,\mathrm{high}}$를 함께 보고하고, 가능하면 두 점 외에도 여러 $V_D$에서 선형성을 확인한다. 높은 $V_D$ 곡선의 바닥이 GIDL 또는 gate current에 의해 올라가면 constant-current crossing이 barrier lowering이 아니라 다른 leakage를 반영할 수 있으므로 $I_B$와 $I_G$를 함께 검사한다.[1,5–7]

### (3) Subthreshold Swing Degradation

Subthreshold swing은

$$
\mathrm{SS}
=\left(\frac{d\log_{10}|I_D|}{dV_G}\right)^{-1}
=\ln(10)\,n\frac{kT}{q}
$$

이다. Long-channel bulk MOSFET에서는 depletion 및 interface-trap capacitance가 $n$을 결정한다. 채널이 짧아지면 source barrier에 대한 gate control이 약해지고 drain coupling이 커져, 같은 전류 decade를 바꾸는 데 더 큰 $\Delta V_G$가 필요해질 수 있다.[1–3]

**실험과 metric.** 반로그 $I_D$–$V_G$에서 최소 한 점의 numerical derivative만 보고하지 않고, 지정한 current-decade window의 국소 회귀와 minimum SS를 함께 저장한다. 온도와 $V_D$를 명시하고 $L$에 대해 비교한다. 300 K에서 이상적인 thermionic limit 약 $59.6\ \mathrm{mV/dec}$은 $n=1$ 가정의 기준이지 모든 소자에서 반드시 얻어야 하는 보정값은 아니다.[1–3]

### (4) Punch-Through

Punch-through는 source와 drain depletion region이 body 깊은 곳에서 강하게 결합하여 potential saddle을 낮추고, gate가 꺼진 상태에서도 source–drain 경로를 여는 현상이다. 일반적인 DIBL보다 심한 electrostatic failure이며, surface subthreshold path와 다른 깊이의 current path가 지배할 수 있다.[1,8,9]

**실험과 metric.** $V_G$를 off bias에 고정하여 여러 $L$에서 $I_D$–$V_D$를 측정한다. $V_\mathrm{PT}$는 지정한 $I_D/W$에 도달하는 $V_D$ 또는 지정한 $g_{ds,\mathrm{off}}$의 onset으로 정의한다. Body bias dependence와 length dependence가 중요하며, 높은 drain field에서 함께 나타나는 GIDL·junction breakdown을 $I_B$, $I_G$로 분리해야 한다.[1,8,9]

## 4. High-Field, Transport, and Reliability Effects

다음 현상은 짧은 소자에서 함께 중요해지지만, source barrier에 대한 gate control 저하와는 다른 물리와 metric을 갖는다.

### (1) Channel-Length Modulation

Saturation 이후 $V_D$가 증가하면 drain-side pinch-off point가 source 쪽으로 이동하여 유효 채널 길이가 감소한다. 그 결과 이상적인 flat saturation과 달리 $I_D$가 계속 증가한다. 짧은 채널일수록 상대적인 길이 변화가 커지기 쉬우나, 이는 source barrier control의 붕괴와는 다른 출력 특성 효과이다.[1,2,4]

<figure markdown="span">
  ![nMOS 포화 영역에서 drain-side pinch-off가 형성된 schematic](images/mosfet-saturation.svg)
  <figcaption>
    그림 2. nMOS 포화 영역의 drain-side pinch-off 개념도.
    출처: Cyril Buttay; current correction by Cepheiden, “Mosfet saturation,” Wikimedia Commons,
    <a href="https://commons.wikimedia.org/wiki/File:Mosfet_saturation.svg">CC BY-SA 3.0</a>, 수정 없음.[14]
  </figcaption>
</figure>

$$
g_{ds}=\left.\frac{\partial I_D}{\partial V_D}\right|_{V_G},
\qquad
r_o=\frac{1}{g_{ds}},
\qquad
\lambda_\mathrm{CLM}\approx\frac{g_{ds}}{I_D}.
$$

$\lambda_\mathrm{CLM}$의 단위는 V$^{-1}$이며, 제한된 bias window에서 $I_D\approx I_{D0}(1+\lambda V_D)$로 근사할 때의 국소 값이다.[1,2]

**실험과 metric.** 여러 $V_G$의 $I_D$–$V_D$를 측정하고, breakdown·self-heating·series-resistance domination을 피한 saturation window에서 선형회귀하여 $g_{ds}$를 구한다. $r_o$와 $g_mr_o$를 analog 관점 metric으로 사용할 수 있다. 같은 $V_G$가 아니라 같은 overdrive 또는 같은 current density에서 비교할지 미리 정해야 한다.[1,2,4]

### (2) Velocity Saturation

Lateral field가 커지면 carrier drift velocity는 더 이상 $v=\mu E$로 선형 증가하지 않고 높은 전계의 유효 포화속도에 접근한다. 짧은 채널에서는 비교적 작은 $V_D$에서도 평균 lateral field가 커지므로, square-law보다 이른 current saturation과 약한 overdrive exponent가 나타난다.[1–3,10]

간단한 경험식은

$$
v(E)\approx\frac{\mu E}{1+E/E_\mathrm{sat}}
$$

이며, $E\ll E_\mathrm{sat}$에서는 $\mu E$, $E\gg E_\mathrm{sat}$에서는 $\mu E_\mathrm{sat}$에 접근한다. 실제 silicon의 속도–전기장 관계는 온도, 결정방향, nonlocal transport에 의존하므로 이 식의 $E_\mathrm{sat}$을 보편적 재료상수로 해석하지 않는다.[3,10]

**실험과 metric.** 여러 $L$에서 $I_D$–$V_D$, $I_D$–$V_G$, $g_m$을 측정하고, $V_{DS,\mathrm{sat}}$가 long-channel square-law 예상보다 작아지는지 본다. 일정 bias window에서 $I_{D,\mathrm{sat}}\propto(V_G-V_T)^\alpha$를 피팅하면 $\alpha$가 2에서 1 쪽으로 감소하는 경향을 볼 수 있지만, mobility degradation과 series resistance도 같은 방향으로 작용한다. 따라서 $\alpha$, peak $g_m$, $V_{DS,\mathrm{sat}}$를 함께 보고하고 가능하면 온도·길이 split으로 분리한다.[1–3,10]

### (3) Impact Ionization and Hot-Carrier Degradation

Drain 근처의 큰 lateral field에서 carrier가 충분한 에너지를 얻으면 impact ionization으로 electron–hole pair를 만들 수 있다. nMOS에서는 생성된 hole의 일부가 body로 흘러 substrate/body current가 되고, hot carrier의 일부가 oxide 또는 interface에 포획되면 $V_T$, $g_m$, $I_D$가 시간에 따라 변한다. 이는 순간적인 SCE라기보다 고전계 전류와 신뢰성 열화이다.[1,11,12]

**실험과 metric.** 초기 transfer/output curve를 저장한 뒤 지정한 $(V_G,V_D,V_B,T)$에서 stress하고, 짧은 간격으로 동일한 저전압 read condition에서 $\Delta V_T$, $\Delta g_m/g_m$, $\Delta I_D/I_D$를 측정한다. Stress 중 $I_B/I_D$는 impact-ionization monitor로 유용하다. Lifetime은 열화 criterion, duty cycle, stress와 use bias 간 extrapolation model에 의존하므로 criterion과 모델을 함께 보고한다. 측정 자체가 추가 열화를 만들지 않도록 read bias와 시간도 고정한다.[7,11,12]

## 5. Interpretation Pitfalls

- **DIBL과 GIDL:** 높은 $V_D$의 $I_D$–$V_G$ 바닥 상승을 모두 DIBL로 부르면 안 된다. 곡선의 수평 이동, $I_B$, $I_G$를 함께 본다.[1,6,7]
- **SS와 측정 바닥:** instrumentation leakage 또는 gate current가 $I_D$ 바닥을 만들면 numerical derivative가 거짓으로 커진다.[6,7]
- **Velocity saturation과 series resistance:** 둘 다 $g_m$과 current exponent를 낮춘다. length, temperature, external resistance split이 필요하다.[1–3]
- **CLM과 self-heating:** 높은 $V_D$의 기울기가 항상 CLM은 아니다. forward/reverse sweep과 pulsed measurement로 열적 지연을 확인한다.[1,2,7]
- **Metric 정의:** $V_T$, DIBL, $V_\mathrm{PT}$, SS의 추출 window를 바꾸면 같은 raw data에서도 다른 값이 나온다.[1,5]

## 6. Summary

- 좁은 의미의 electrostatic SCE는 $V_T$ roll-off, DIBL, SS degradation, punch-through이다.
- CLM, velocity saturation, impact ionization/hot-carrier effect는 짧은 소자에서 중요하지만 별도 물리와 metric으로 평가한다.
- 최소 실험 세트는 length split, 낮은/높은 $V_D$의 transfer curve, output curve, 네 단자전류 동시 측정이다.
- 재현 가능한 비교에는 $V_T$ 기준전류, DIBL의 두 drain bias, SS window, 폭 정규화, 온도를 반드시 포함한다.

## 7. References

1. C. Hu, *Modern Semiconductor Devices for Integrated Circuits*, Chapters 6–7, Pearson (2010). [Chapter 7 저자 제공 PDF](https://www.chu.berkeley.edu/wp-content/uploads/2020/01/Chenming-Hu_ch7.pdf).
2. Y. Taur and T. H. Ning, *Fundamentals of Modern VLSI Devices*, 2nd ed., Cambridge University Press (2009). [DOI: 10.1017/CBO9781139195065](https://doi.org/10.1017/CBO9781139195065).
3. D. J. Frank et al., “Device Scaling Limits of Si MOSFETs and Their Application Dependencies,” *Proceedings of the IEEE* **89**, 259–288 (2001). [DOI: 10.1109/5.915374](https://doi.org/10.1109/5.915374).
4. BSIM Research Group, “BSIM4,” University of California, Berkeley. [공식 모델 페이지](https://bsim.berkeley.edu/models/bsim4/) (접속일: 2026-07-31).
5. A. Ortiz-Conde et al., “Revisiting MOSFET Threshold Voltage Extraction Methods,” *Microelectronics Reliability* **53**, 90–104 (2013). [DOI: 10.1016/j.microrel.2012.09.015](https://doi.org/10.1016/j.microrel.2012.09.015).
6. Keysight Technologies, “DC MOSFET Characterization at the Wafer Level,” Application Note 5990-5547EN (2019). [공식 문서](https://www.keysight.com/my/en/assets/7018-02489/application-notes/5990-5547.pdf).
7. D. K. Schroder, *Semiconductor Material and Device Characterization*, 3rd ed., Wiley (2006). [DOI: 10.1002/0471749095](https://doi.org/10.1002/0471749095).
8. N. Kotani and S. Kawazu, “Computer Analysis of Punch-Through in MOSFETs,” *Solid-State Electronics* **22**, 63–70 (1979). [DOI: 10.1016/0038-1101(79)90172-2](https://doi.org/10.1016/0038-1101(79)90172-2).
9. J. J. Barnes, K. Shimohigashi, and R. W. Dutton, “Short-Channel MOSFET’s in the Punchthrough Current Mode,” *IEEE Transactions on Electron Devices* **26**, 446–453 (1979). [DOI: 10.1109/T-ED.1979.19447](https://doi.org/10.1109/T-ED.1979.19447).
10. C. Canali, G. Majni, R. Minder, and G. Ottaviani, “Electron and Hole Drift Velocity Measurements in Silicon and Their Empirical Relation to Electric Field and Temperature,” *IEEE Transactions on Electron Devices* **22**, 1045–1047 (1975). [DOI: 10.1109/T-ED.1975.18267](https://doi.org/10.1109/T-ED.1975.18267).
11. C. Hu et al., “Hot-Electron-Induced MOSFET Degradation—Model, Monitor, and Improvement,” *IEEE Transactions on Electron Devices* **32**, 375–385 (1985). [DOI: 10.1109/T-ED.1985.21952](https://doi.org/10.1109/T-ED.1985.21952).
12. A. Acovic, G. La Rosa, and Y.-C. Sun, “A Review of Hot-Carrier Degradation Mechanisms in MOSFETs,” *Microelectronics Reliability* **36**, 845–869 (1996). [DOI: 10.1016/0026-2714(96)00022-4](https://doi.org/10.1016/0026-2714(96)00022-4).
13. Sjoerd Terlouw, “Barrier lowering length,” Wikimedia Commons (2025), CC BY-SA 4.0. [파일 설명과 라이선스](https://commons.wikimedia.org/wiki/File:Barrier_lowering_length.svg).
14. Cyril Buttay and Cepheiden, “Mosfet saturation,” Wikimedia Commons (2008; current correction 2021), CC BY-SA 3.0. [파일 설명과 라이선스](https://commons.wikimedia.org/wiki/File:Mosfet_saturation.svg).
