---
title: "(2) MOSFET: Short-Channel Effects"
description: MOSFET short-channel effects를 long-channel baseline, electrostatic origin, measurement와 metric의 순서로 설명
status: verified
last_verified: 2026-07-31
---

# (2) MOSFET: Short-Channel Effects

metal-oxide-semiconductor field-effect transistor (MOSFET)의 channel length가 짧아지면 source와 drain의 potential이 channel 안쪽까지 침투하여 gate의 barrier control을 약화한다. 이 electrostatic coupling에서 threshold-voltage roll-off, drain-induced barrier lowering (DIBL), subthreshold-swing degradation과 punch-through가 발생하며, 이들을 short-channel effects (SCE)라고 한다. channel-length scaling과 함께 중요해지는 channel-length modulation (CLM), velocity saturation과 hot-carrier degradation은 related phenomena이지만 physical origin이 다르므로 SCE와 구분한다.[1–4]

<figure markdown="span">
  ![channel length가 짧아질수록 source와 channel 사이의 energy barrier가 낮아지는 개념도](images/barrier-lowering-length.svg)
  <figcaption>
    그림 1. channel length가 짧아질수록 drain potential이 source-side barrier를 낮추는 electrostatic coupling.
    출처: Sjoerd Terlouw, “Barrier lowering length,” Wikimedia Commons,
    <a href="https://commons.wikimedia.org/wiki/File:Barrier_lowering_length.svg">CC BY-SA 4.0</a>, 수정 없음.
    정량적 해석은 본문의 문헌 [1–3]을 따른다.[13]
  </figcaption>
</figure>

## 1. Scope and Conventions

기본 대상은 planar bulk n-channel MOSFET (nMOS)이며, $V_S=V_B=0$인 direct current (DC) measurement를 가정한다. drain current는 크기 $|I_D|$를 사용하고, 서로 다른 width의 device는 $I_D/W$로 비교한다. channel-length device split은 가능하면 같은 wafer, width, crystal orientation과 process condition에서 선택한다.

- threshold voltage ($V_T$)는 지정한 reference current의 constant-current method로 추출한다. 모든 비교에서 reference current, width normalization, drain voltage, 온도와 sweep direction을 고정한다.[1,5]
- off-state current ($I_\mathrm{OFF}$)는 선언한 off-state bias에서 측정한 $|I_D|$이며, 비교할 때에는 width로 normalize한다.
- subthreshold swing (SS)은 semilog $I_D$–$V_G$의 지정한 current window에서 추출한다.
- 이 문서의 DIBL은 drain-voltage 증가에 따른 $V_T$ 감소가 양의 값으로 표시되도록 정의한다.
- 문헌의 부호, 전압 기준 또는 $V_T$ 추출법이 다르면 이 규약으로 변환한 뒤 비교한다.

SCE와 related phenomena의 범주는 다음처럼 구분한다.

| Category | Included Phenomena | Common Physics |
| --- | --- | --- |
| electrostatic SCE | $V_T$ roll-off, DIBL, SS degradation, punch-through | weakened gate control of the source barrier |
| related output·transport·reliability phenomena | CLM, velocity saturation, impact ionization, hot-carrier degradation | drain-side high field, nonequilibrium transport, or defect generation |

## 2. Long-Channel Baseline and Electrostatic Origin

### (1) Long-Channel MOSFET Baseline

long-channel device에서는 source와 충분히 떨어진 drain potential이 source-side injection barrier에 미치는 영향이 작다. gate voltage는 dielectric을 통해 surface potential과 inversion charge를 주로 제어하며, subthreshold current는 source–channel barrier height에 지수적으로 의존한다. 이때 $V_T$는 channel length에 거의 무관하고, 낮은 drain voltage와 높은 drain voltage에서 얻은 transfer curve의 horizontal shift도 작다.[1–3]

subthreshold current의 기본 관계는

$$
I_D\propto
\exp\left(\frac{V_G-V_T}{nU_T}\right),
\qquad U_T=\frac{kT}{q}
$$

로 쓸 수 있다. $n$은 게이트 전압이 표면 장벽을 얼마나 효율적으로 바꾸는지를 나타내며, 장채널 벌크 MOSFET에서는 산화막·공핍층·계면 트랩 정전용량의 결합으로 결정된다.[1–3]

### (2) Channel-Length Scaling and Two-Dimensional Coupling

채널 길이가 소스·드레인 공핍영역의 크기와 소자의 정전기적 특성 길이에 가까워지면 전위 분포는 더 이상 게이트에 수직인 1차원 문제로 볼 수 없다. 소스와 드레인의 전기장이 채널 방향으로 침투하면서 게이트, 소스와 드레인이 채널 장벽을 함께 결정한다. 산화막이 얇고 바디가 얇으며 접합이 얕을수록 게이트 결합은 강해지고 드레인 결합은 약해진다.[1–3]

고전적인 charge-sharing model에서는 source·drain depletion region이 channel depletion charge의 일부를 지탱한다. 따라서 gate가 같은 surface condition을 만들기 위해 공급해야 하는 charge와 voltage가 감소한다. energy-barrier picture에서는 drain potential이 source-side conduction-band barrier를 직접 낮춘다. 두 설명은 각각 $V_T$ roll-off와 DIBL을 이해하는 상보적인 관점이다.[1–3]

## 3. Electrostatic Short-Channel Effects

### (1) Threshold-Voltage Roll-Off

threshold-voltage roll-off는 channel length가 감소할수록 nMOS의 $V_T$가 long-channel value보다 낮아지는 현상이다. charge sharing과 two-dimensional barrier coupling 때문에 gate가 inversion condition을 만드는 데 필요한 voltage가 줄어들며, 결과적으로 같은 $V_G$에서 subthreshold current가 증가한다.[1–3]

이 문서에서는 채널 길이 $L$의 저하량을

$$
\Delta V_{T,\mathrm{roll}}(L)
=V_T(L)-V_T(L_\mathrm{ref})
$$

로 정의한다. $L_\mathrm{ref}$는 $V_T$가 length에 거의 무관한 long-channel reference device이다. 이 sign convention에서 정상적인 nMOS의 threshold-voltage roll-off는 음수이다.[1,2,5]

!!! info "[Measurement]"
    낮은 $V_D$에서 여러 channel length의 $I_D$–$V_G$를 측정하고, 모든 curve에 같은 constant-current criterion을 적용한다. 동일 wafer의 device split을 사용하여 width, series resistance와 process variation의 영향을 줄인다.[1–3,5]

!!! abstract "[Metric]"
    $V_T$–$L$과 $\Delta V_{T,\mathrm{roll}}$–$L$을 함께 제시한다. $L_\mathrm{ref}$, 기준전류, $V_D$, 온도와 폭 정규화를 기록한다.[1,2,5]

!!! warning "[Interpretation Caveat]"
    halo implant와 channel-doping nonuniformity는 short channel에서 $V_T$가 오히려 증가하는 reverse short-channel effect를 만들 수 있다. 따라서 monotonic decrease를 가정하지 말고 process condition이 같은 device끼리 비교한다.[1–3]

### (2) Drain-Induced Barrier Lowering

DIBL은 drain-voltage 증가가 source–channel energy barrier를 낮추어 같은 drain current에 필요한 gate voltage를 감소시키는 현상이다. 그림 1처럼 높은 $V_D$에서 transfer curve가 낮은 $V_G$ 방향으로 이동하고 off-state current가 증가한다. channel length가 짧고 gate control이 약할수록 shift가 커진다.[1–3]

양의 값으로 정의한 DIBL은

$$
\mathrm{DIBL}
=\frac{V_T(V_{D,\mathrm{low}})-V_T(V_{D,\mathrm{high}})}
{V_{D,\mathrm{high}}-V_{D,\mathrm{low}}}
$$

이다. 단위는 V/V 또는 mV/V이다. $\Delta V_T/\Delta V_D$를 그대로 사용하는 문헌에서는 같은 현상이 음의 값으로 표시될 수 있다.[1,2]

!!! info "[Measurement]"
    동일 소자의 낮은·높은 $V_D$에서 $I_D$–$V_G$를 측정하고 같은 기준전류로 $V_T$를 추출한다. 가능하면 두 점뿐 아니라 여러 $V_D$에서 장벽 이동의 선형성을 확인한다.[1,2,5]

!!! abstract "[Metric]"
    위 식의 DIBL과 함께 $V_{D,\mathrm{low}}$, $V_{D,\mathrm{high}}$, $V_T$ 추출법, 기준전류와 온도를 보고한다. 채널 길이별 DIBL을 제시하면 정전기적 제어의 길이 의존성을 비교할 수 있다.[1,2,5]

!!! warning "[Interpretation Caveat]"
    gate-induced drain leakage (GIDL)나 gate current가 높은 $V_D$ 곡선의 current floor를 올리면, constant-current crossing이 barrier shift가 아닌 다른 leakage를 반영할 수 있다. $I_B$와 $I_G$를 함께 확인한다.[1,6,7]

### (3) Subthreshold-Swing Degradation

SS는

$$
\mathrm{SS}
=\left(\frac{d\log_{10}|I_D|}{dV_G}\right)^{-1}
=\ln(10)\,n\frac{kT}{q}
$$

로 정의된다. 짧은 채널에서 소스 장벽에 대한 게이트 결합이 약해지고 드레인 결합이 커지면, 같은 전류 변화를 만드는 데 더 큰 게이트 전압 변화가 필요하여 SS가 증가할 수 있다. 계면 트랩과 공핍 정전용량도 SS를 악화하므로 길이 의존성만으로 원인을 확정할 수는 없다.[1–3]

!!! info "[Measurement]"
    낮은·높은 $V_D$의 반로그 $I_D$–$V_G$에서 계측기 바닥보다 충분히 높은 동일 전류 구간을 선택한다. 한 점의 수치 미분 대신 지정 구간의 국소 선형회귀를 사용하고 온도와 채널 길이를 함께 변화시킨다.[1–3,6,7]

!!! abstract "[Metric]"
    최소 SS와 지정 전류 구간의 평균 SS를 mV/dec로 보고한다. 온도, $V_D$, 전류 구간과 회귀 방법을 함께 기록한다. 300 K의 약 $59.6\ \mathrm{mV/dec}$은 $n=1$인 열전자 수송의 이상 기준이다.[1–3]

### (4) Punch-Through

punch-through는 source와 drain depletion region이 deep body에서 강하게 결합하여 potential saddle point를 낮추고, gate가 꺼져 있어도 source–drain current path를 여는 현상이다. 일반적인 DIBL보다 electrostatic control loss가 심한 상태이며, 전류가 surface보다 gate에서 먼 bulk path를 따라 흐를 수 있다.[1,8,9]

!!! info "[Measurement]"
    $V_G$를 꺼짐 바이어스에 고정하고 여러 채널 길이에서 $I_D$–$V_D$를 측정한다. 바디 전압과 온도를 함께 변화시키며 $I_B$와 $I_G$를 동시에 읽어 GIDL과 접합 항복을 분리한다.[1,8,9]

!!! abstract "[Metric]"
    punch-through voltage ($V_\mathrm{PT}$)는 지정한 $I_D/W$에 도달하는 $V_D$로 정의한다. off-state output conductance $g_{ds,\mathrm{off}}$의 증가도 secondary metric으로 사용한다. reference current와 모든 terminal bias를 함께 명시한다.[1,8,9]

## 4. Related High-Field, Transport, and Reliability Phenomena

다음 현상은 channel length가 짧을수록 두드러질 수 있지만, source barrier에 대한 gate-control loss만으로 정의되는 SCE는 아니다. 별도의 physics와 metric으로 평가해야 한다.[1–4]

### (1) Channel-Length Modulation

channel-length modulation (CLM)은 saturation 이후 $V_D$가 증가할 때 drain-side pinch-off point가 source 방향으로 이동하여 effective channel length가 감소하는 현상이다. 이상적인 flat saturation과 달리 $I_D$가 계속 증가하며, short channel에서는 같은 length change가 차지하는 비율이 커질 수 있다.[1,2,4]

<figure markdown="span">
  ![n-channel MOSFET의 saturation region에서 drain-side pinch-off가 형성된 개념도](images/mosfet-saturation.svg)
  <figcaption>
    그림 2. n-channel MOSFET saturation region의 drain-side pinch-off.
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

$g_{ds}$는 output conductance, $r_o$는 output resistance이다. $\lambda_\mathrm{CLM}$은 제한된 bias window에서 $I_D\approx I_{D0}(1+\lambda V_D)$로 근사할 때의 local CLM coefficient이며 단위는 V$^{-1}$이다.[1,2]

!!! info "[Measurement]"
    여러 $V_G$에서 $I_D$–$V_D$를 측정한다. 항복, 자기 가열과 직렬저항 지배를 피한 포화 구간을 정하고 그 구간을 선형회귀한다.[1,2,4]

!!! abstract "[Metric]"
    $g_{ds}$, $r_o$와 $\lambda_\mathrm{CLM}$을 보고한다. 소자 비교 기준을 같은 $V_G$, 같은 과구동 전압 또는 같은 전류밀도 가운데 하나로 정해 유지한다.[1,2,4]

### (2) Velocity Saturation

velocity saturation은 channel-direction electric field가 커질 때 carrier drift velocity가 더 이상 $v=\mu E$로 선형 증가하지 않고 effective saturation velocity에 접근하는 현상이다. short channel은 비교적 작은 $V_D$에서도 average electric field가 커지므로 long-channel square law보다 이른 current saturation과 낮은 overdrive exponent를 보일 수 있다.[1–3,10]

대표적인 경험식은

$$
v(E)\approx\frac{\mu E}{1+E/E_\mathrm{sat}}
$$

이다. 낮은 전기장에서는 $v\approx\mu E$, 높은 전기장에서는 $v\approx\mu E_\mathrm{sat}$에 접근한다. 실제 실리콘의 속도–전기장 관계는 온도, 결정 방향과 비국소 수송에 의존하므로 $E_\mathrm{sat}$을 보편적 재료상수로 해석하지 않는다.[3,10]

!!! info "[Measurement]"
    여러 channel length에서 $I_D$–$V_D$, $I_D$–$V_G$와 transconductance $g_m$을 측정한다. 온도 또는 external series-resistance 비교를 추가하면 mobility degradation과 series resistance의 영향을 분리하는 데 도움이 된다.[1–3,10]

!!! abstract "[Metric]"
    saturation drain voltage $V_{DS,\mathrm{sat}}$, maximum $g_m$과 $I_{D,\mathrm{sat}}\propto(V_G-V_T)^\alpha$의 local exponent $\alpha$를 함께 보고한다. fitting window를 명시하고, $\alpha$만으로 velocity saturation을 단정하지 않는다.[1–3,10]

### (3) Impact Ionization and Hot-Carrier Degradation

impact ionization은 drain 부근의 큰 electric field에서 에너지를 얻은 carrier가 electron–hole pair를 만드는 과정이다. nMOS에서는 생성된 hole 일부가 body current가 된다. hot-carrier degradation은 high-energy carrier가 dielectric 또는 interface에 defect와 trapped charge를 만들어 $V_T$, $g_m$과 $I_D$를 시간에 따라 변화시키는 reliability phenomenon이다.[1,11,12]

!!! info "[Measurement]"
    초기 전달·출력 곡선을 저장한 뒤 지정한 $(V_G,V_D,V_B,T)$에서 소자를 스트레스한다. 일정한 간격마다 동일한 낮은 전압 판독 조건으로 특성을 다시 측정하고, 스트레스 중 $I_B$와 $I_D$를 기록한다.[7,11,12]

!!! abstract "[Metric]"
    $I_B/I_D$, $\Delta V_T$, $\Delta g_m/g_m$, $\Delta I_D/I_D$와 수명을 사용한다. 수명에는 열화 판정 기준, 듀티비와 스트레스 조건에서 사용 조건으로의 외삽 모형을 함께 기록한다.[7,11,12]

## 5. Suppression Principles

SCE를 줄이는 핵심은 drain-to-channel coupling보다 gate-to-channel coupling을 강하게 만드는 것이다. 특정 process prescription보다 다음 electrostatic principle이 먼저이다.[1–3]

1. **게이트 절연막의 전기적 두께를 줄인다.** 더 큰 게이트 정전용량은 표면전위 제어를 강화한다. 물리적으로 지나치게 얇은 SiO$_2$는 터널링 누설을 증가시키므로, 고유전율 절연막으로 물리 두께와 전기적 두께를 분리한다.[1–3]
2. **공핍영역과 접합 깊이를 줄인다.** 얕은 소스·드레인 접합과 적절한 바디 도핑은 드레인 전기장의 침투를 줄인다. 높은 도핑은 이동도·접합 누설과 변동성을 악화할 수 있으므로 상충관계를 평가해야 한다.[1–3]
3. **게이트에서 먼 전류 경로를 제거한다.** 얇은 바디와 다중 게이트 구조는 채널 내부의 최악 전류 경로도 게이트 가까이에 두어 장벽 제어를 강화한다.[1–3]

억제 효과는 하나의 DIBL 값만으로 판단하지 않는다. $V_T$–$L$, DIBL–$L$, SS–$L$과 $I_\mathrm{OFF}$를 함께 비교해야 공정 변화가 전체 꺼짐 특성을 개선했는지 확인할 수 있다.[1–3,5]

## 6. Measurement Design and Diagnosis

가장 작은 measurement set은 여러 channel length에 대한 낮은·높은 $V_D$의 transfer characteristics와 여러 $V_G$의 output characteristics이다. $I_G$와 $I_B$를 함께 읽으면 GIDL, gate leakage와 impact ionization이 $I_D$ 기반 extraction을 오염시키는지 확인할 수 있다. low-current region에서는 guarding, shielding, settling time과 sweep history를 관리한다.[5–7]

| Phenomenon | Measurement | Metric | Primary Confounder |
| --- | --- | --- | --- |
| threshold-voltage roll-off | 낮은 $V_D$, 여러 channel length의 $I_D$–$V_G$ | $\Delta V_{T,\mathrm{roll}}(L)$ | reverse SCE, process variation |
| DIBL | 같은 device의 낮은·높은 $V_D$ transfer curve | mV/V | GIDL, gate current |
| SS degradation | semilog $I_D$–$V_G$ | SS와 current extraction window | instrument floor, interface trap |
| punch-through | off-state $I_D$–$V_D$, channel-length split | $V_\mathrm{PT}$, $g_{ds,\mathrm{off}}$ | junction breakdown, GIDL |
| CLM | saturation-region $I_D$–$V_D$ | $g_{ds}$, $r_o$, $\lambda_\mathrm{CLM}$ | self-heating, breakdown |
| velocity saturation | $I_D$–$V_G$, $I_D$–$V_D$, $g_m$ | $V_{DS,\mathrm{sat}}$, $g_m$, $\alpha$ | mobility degradation, series resistance |
| hot-carrier degradation | transfer·output curve before and after stress | $I_B/I_D$, $\Delta V_T$, $\Delta g_m$, lifetime | read stress, extrapolation model |

!!! note "Threshold-Voltage Extraction Consistency"
    constant-current method와 transconductance-extrapolation method는 서로 다른 $V_T$를 줄 수 있다. 하나의 comparison set에서는 extraction method와 reference current를 바꾸지 않으며, reference-current width normalization, $V_D$, 온도와 sweep direction을 함께 보고한다.[1,5]

!!! warning "[Interpretation Caveat]"
    높은 $V_D$에서 current floor가 올라갔다고 모두 DIBL로 해석하지 않는다. transfer-curve horizontal shift와 $I_B$, $I_G$를 함께 본다. 또한 $g_m$ 감소는 velocity saturation뿐 아니라 mobility degradation과 series resistance로도 생기며, saturation-region $I_D$ slope는 CLM뿐 아니라 self-heating과 breakdown의 영향을 받을 수 있다.[1–3,6,7]

## 7. Summary

- SCE의 공통 원인은 source barrier에 대한 gate control이 약해지고 drain coupling이 커지는 two-dimensional electrostatics이다.
- threshold-voltage roll-off, DIBL, SS degradation과 punch-through는 서로 연관되지만 각각 definition과 extraction method가 다르다.
- CLM, velocity saturation과 hot-carrier degradation은 short channel에서 중요하지만 별도의 output·transport·reliability phenomenon이다.
- SCE suppression의 핵심은 gate coupling 강화, drain coupling 약화와 gate에서 먼 current path 제거이다.
- 재현 가능한 비교에는 $V_T$ extraction method, 두 drain voltage, SS extraction window, channel length, 온도와 normalization 기준이 필요하다.

## 8. References

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
