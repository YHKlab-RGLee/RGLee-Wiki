---
title: "(1) MOSFET: Leakage Current"
description: MOSFET의 대표 누설 전류를 물리 기작, 단자별 실험 분리법, 정량 metric으로 설명
status: verified
last_verified: 2026-07-31
---

# (1) MOSFET: Leakage Current

MOSFET의 “누설 전류”는 하나의 전류가 아니다. 꺼진 채널을 넘는 열방출, 게이트 절연막을 통과하는 터널링, 역바이어스 접합의 생성·터널링, drain-edge의 GIDL, source–drain punch-through가 서로 다른 단자와 바이어스에서 합쳐진 결과이다. 따라서 한 개의 $I_D$ 값만으로 원인을 단정하지 않고, 네 단자 전류와 온도·면적·채널 길이 의존성을 함께 보아야 한다.[1–3]

<figure markdown="span">
  ![nMOS에서 게이트 누설과 subthreshold 누설이 흐르는 대표 경로](images/leakage-current-overview.png)
  <figcaption>
    그림 1. nMOS에서 게이트 누설과 subthreshold 누설의 대표 경로. 전체 여섯 경로를 한 소자에 표시한 고전적 schematic은 Roy 등의
    <a href="https://dvdtang.nl/joomla/images/Roy11_S5.pdf">Fig. 3</a>에서 볼 수 있다.
    출처: Tosaka, “Leakage Current (2 models),” Wikimedia Commons,
    <a href="https://commons.wikimedia.org/wiki/File:Leakage_Current_(2_models).PNG">CC BY-SA 3.0</a>, 수정 없음.[14]
  </figcaption>
</figure>

## 1. Scope and Conventions

기본 대상은 enhancement-mode planar bulk nMOS이며, 별도 표기가 없으면 DC와 실온을 가정한다. 전압은 $V_{XY}=V_X-V_Y$, 기준 바이어스는 $V_S=V_B=0$이다. 전류의 방향을 혼동하지 않도록 본문과 표에서는 단자전류의 **크기** $|I_G|$, $|I_D|$, $|I_S|$, $|I_B|$를 사용한다.

- $I_\mathrm{OFF}$는 선언한 off bias에서 측정한 $|I_D|$이다. 예를 들어 $V_G=0$, $V_D=V_\mathrm{DD}$이며, 비교할 때에는 A/$\mu$m처럼 유효 폭으로 정규화한다.
- 단자전류를 동시에 측정하면 정상상태에서 부호를 포함한 Kirchhoff current law, $\sum_X I_X\approx0$, 을 데이터 품질 검사에 쓸 수 있다.
- $V_T$는 모든 곡선에 동일한 추출법을 사용한다. 이 문서에서는 지정한 기준전류의 constant-current method를 기본으로 하며, 기준전류와 $V_D$를 결과와 함께 기록한다.[2,8]

!!! warning "숫자 하나만으로는 재현되지 않는다"
    “$I_\mathrm{OFF}=1\ \mathrm{nA}$”만으로는 부족하다. $V_G$, $V_D$, $V_S$, $V_B$, 온도, 소자 폭·길이, 폭 정규화 방식, sweep 방향, integration time을 함께 기록해야 한다.[8–10]

## 2. Common Measurement Setup

Gate, drain, source, body에 각각 SMU를 연결하여 네 단자전류를 동시에 읽는 구성이 가장 직접적이다. 저전류 측정에서는 케이블·프로버·척의 누설이 소자 전류와 같은 크기가 될 수 있으므로 triax guarding, 차폐와 암상태, 충분한 settling/integration, current compliance가 필요하다. 빈 패드 또는 open 구조를 같은 배선으로 측정하면 시스템 바닥 전류를 확인할 수 있다.[7,9,10]

측정 순서는 다음처럼 통일할 수 있다.

1. 낮은 $V_D$와 높은 $V_D$에서 반로그 $I_D$–$V_G$를 양방향 sweep한다.
2. 같은 sweep에서 $I_G$, $I_S$, $I_B$도 저장하고 $\sum I_X$를 확인한다.
3. off-state $I_D$–$V_D$와 $I_G$–$V_G$를 별도로 측정한다.
4. 길이, 폭, 접합 면적·둘레가 다른 split과 온도 sweep을 반복한다.
5. 예상치 못한 hysteresis 또는 stress drift가 보이면 sweep 범위를 줄이고 fresh device로 재현한다.[7,9,10]

## 3. Leakage Components

대표 누설 성분은 다음 지도와 개별 기작으로 구분한다.

### (1) Component Map

| 성분 | 주된 물리 | 우선 관찰 단자·sweep | 대표 metric |
| --- | --- | --- | --- |
| Subthreshold leakage | source 장벽을 넘는 열방출·확산 | 반로그 $I_D$–$V_G$ | $I_\mathrm{OFF}/W$, SS, DIBL |
| Gate dielectric tunneling | 절연막 장벽의 양자 터널링 | $I_G$–$V_G$, 단자별 partition | $J_G$, edge current/$W$ |
| Reverse junction leakage | 생성·확산, 고전계 BTBT | drain–body diode $I$–$V$ | 면적·둘레 전류밀도, 활성화 에너지 |
| GIDL | gate–drain overlap 부근 BTBT/TAT | 음의/낮은 $V_G$, 높은 $V_D$ | $I_\mathrm{GIDL}/W$, onset, field slope |
| Punch-through | source–drain 공핍영역 결합 | off-state $I_D$–$V_D$, length split | $V_\mathrm{PT}$, $g_{ds,\mathrm{off}}$ |

### (2) Subthreshold Leakage

Gate 전압이 $V_T$보다 낮아도 source에서 channel로 넘어가는 에너지 장벽은 유한하다. 약한 반전에서 channel 전하는 $V_G$에 지수적으로 변하고, drain 방향으로 확산하여 subthreshold current를 만든다. 짧은 채널에서는 drain이 source-side 장벽을 낮추는 DIBL이 같은 전류를 더 키운다.[1–3]

<figure markdown="span">
  ![게이트가 꺼진 nMOS에서 drain으로 흐르는 subthreshold leakage](images/fet-subthreshold-leakage.png)
  <figcaption>
    그림 2. $V_G=0$인 nMOS의 subthreshold leakage 경로 예시.
    출처: Fadeaway919, “FET subthreshold leakage,” Wikimedia Commons,
    <a href="https://commons.wikimedia.org/wiki/File:FET_subthreshold_leakage.png">CC BY-SA 3.0</a>, 수정 없음.[15]
  </figcaption>
</figure>

일반적인 약한 반전 근사식은 다음처럼 쓸 수 있다.

$$
I_\mathrm{sub}\approx I_0\frac{W}{L}
\exp\left(\frac{V_{GS}-V_T+\eta_DV_{DS}}{nU_T}\right)
\left[1-\exp\left(-\frac{V_{DS}}{U_T}\right)\right],
$$

여기서 $U_T=kT/q$, $n$은 subthreshold slope factor, $\eta_D$는 drain-induced barrier lowering을 나타내는 계수이다. $I_0$의 정의는 compact model마다 다르므로 절대 전류를 이 식 하나로 피팅하기보다, 측정 곡선의 국소 기울기와 바이어스 이동을 추출하는 편이 명확하다.[1–3]

Subthreshold swing(SS)은

$$
\mathrm{SS}
=\left(\frac{d\log_{10}|I_D|}{dV_G}\right)^{-1}
=\ln(10)\,n\frac{kT}{q}
$$

로 정의하며 단위는 mV/dec이다. $n=1$인 이상적인 열전자 한계는 300 K에서 약 $59.6\ \mathrm{mV/dec}$이지만, 실제 $n$은 depletion 및 interface-trap capacitance 때문에 1보다 크다.[1–3]

**실험과 metric.** 낮은 $V_D$와 동작 전압에 가까운 높은 $V_D$에서 반로그 $I_D$–$V_G$를 측정한다. SS는 지정한 전류 window에서 국소 미분 또는 선형회귀로 추출하고, window와 온도를 함께 기록한다. $I_\mathrm{OFF}/W$는 지정 off bias에서 읽는다. 이때 $I_G$가 $I_D$와 비슷하거나 $I_B$가 크게 증가하면 순수한 subthreshold current라고 해석하지 않는다.[1,2,7]

### (3) Gate Dielectric Tunneling

절연막이 얇아지면 gate의 전자가 유한한 oxide barrier를 양자역학적으로 투과한다. 장벽이 사다리꼴에 가까운 직접 터널링과 높은 oxide field에서의 Fowler–Nordheim형 터널링을 구분할 수 있으며, gate–drain overlap edge의 직접 터널링도 별도 성분이 될 수 있다. 전류는 절연막 두께와 barrier profile에 지수적으로 민감하다.[1,2,4]

일차원 WKB 근사에서 투과율은

$$
T(E)\approx
\exp\left[
-\frac{2}{\hbar}
\int_{x_1}^{x_2}
\sqrt{2m_\mathrm{ox}^{*}\left(U(x)-E\right)}\,dx
\right]
$$

이다. $m_\mathrm{ox}^{*}$는 절연막 유효질량, $U(x)$는 barrier energy, $x_1,x_2$는 고전적 turning point이다. 이 식은 두께와 전기장에 대한 지수 민감도를 보여주지만, 실제 $J_G$ 계산에는 전극 상태밀도, band offset, image-force 및 다층 dielectric을 포함한 모델이 필요하다.[2,4,11]

**실험과 metric.** Source와 drain을 같은 전위로 묶어 channel lateral field를 줄인 뒤 $I_G$–$V_G$를 측정하고, $I_S$와 $I_D$로 gate current partition을 확인한다. 면적이 다른 소자의 $I_G$가 gate area에 비례하면 면적 성분, 폭 또는 overlap 길이에 더 민감하면 edge 성분을 의심한다. 보고값은 $J_G=|I_G|/A_G$와 edge current/$W$를 분리하고, oxide thickness, equivalent oxide thickness(EOT), 온도, 극성을 함께 적는다.[2,4,7]

### (4) Reverse-Biased Source/Drain Junction Leakage

Drain–body와 source–body pn 접합은 off-state에서 역바이어스된다. 낮거나 중간 전계에서는 depletion-region generation과 중성영역의 minority-carrier diffusion이, 높은 전계와 고농도 접합에서는 band-to-band tunneling(BTBT)이 중요해질 수 있다. 접합 바닥 면적과 isolation edge 둘레가 서로 다른 결함 밀도와 전기장을 갖기 때문에 면적 성분과 둘레 성분을 분리해야 한다.[1,2,11]

$$
|I_\mathrm{junc}|
\approx J_A A_\mathrm{junc}+J_P P_\mathrm{junc},
$$

여기서 $A_\mathrm{junc}$는 접합 면적, $P_\mathrm{junc}$는 접합 둘레, $J_A$와 $J_P$는 각각 A/area와 A/length 단위의 계수이다. 이는 기작 자체의 법칙이라기보다 geometry split으로 성분을 분리하는 실험 모델이다.[7,11]

**실험과 metric.** 가장 깔끔한 방법은 공정 모니터의 독립 drain/body diode에서 reverse $I$–$V$와 온도 sweep을 측정하는 것이다. 트랜지스터에서는 gate와 source를 body에 두어 channel을 끄되, drain-edge field가 GIDL을 만들지 않는 범위를 먼저 확인한다. 여러 면적·둘레 구조를 동시에 회귀하여 $J_A$, $J_P$를 얻고, Arrhenius plot의 기울기에서 apparent activation energy를 추출한다. 약한 온도의존성과 급격한 field dependence는 단순 generation보다 BTBT 가능성을 높이지만, 이 한 가지 특징만으로 기작을 확정하지 않는다.[1,7,11]

### (5) Gate-Induced Drain Leakage

Gate-induced drain leakage(GIDL)는 낮거나 음의 gate bias와 높은 drain bias에서 gate–drain overlap 부근의 surface band bending이 커질 때 나타난다. 강한 국소 전기장이 drain 쪽 valence band와 conduction band 사이의 BTBT를 만들며, oxide/interface trap이 있으면 trap-assisted tunneling(TAT) 또는 저전계 방출 성분이 섞일 수 있다.[1,5,6]

직접 BTBT의 전계 민감도는 단순화하면

$$
J_\mathrm{BTBT}\propto F^2\exp\left(-\frac{B}{F}\right)
$$

처럼 표현할 수 있다. $F$는 drain-edge의 국소 전기장이고 $B$는 bandgap과 유효질량에 의존하는 계수이다. 외부 전압을 $F$로 곧바로 치환하면 overlap geometry와 doping 효과를 잃으므로, 이 식은 field trend를 보는 데만 사용한다.[5,6,11]

**실험과 metric.** nMOS에서 $V_S=V_B=0$, $V_D>0$으로 두고 $V_G$를 0에서 음의 방향으로 sweep하거나, 여러 $V_G$에서 $I_D$–$V_D$를 측정한다. $|V_{DG}|$가 커질수록 나타나는 drain current와 대응하는 body current를 함께 보면 electron–hole pair generation을 확인하는 데 도움이 된다. $I_G$도 동시에 측정하여 gate tunneling의 terminal partition이 $I_D$로 들어오는 경우를 배제한다. $I_\mathrm{GIDL}/W$는 반드시 $(V_G,V_D,V_B,T)$와 함께 보고하며, 정한 기준전류의 onset voltage 또는 $\log I$ 대 $1/F_\mathrm{proxy}$ 기울기를 공정 비교 metric으로 쓸 수 있다.[1,5–7]

### (6) Punch-Through Leakage

채널이 짧거나 body doping이 낮으면 source와 drain 공핍영역이 깊은 body 안에서 서로 접근한다. 두 공핍영역 사이의 potential saddle이 충분히 낮아지면 gate가 꺼져 있어도 source에서 drain으로 bulk path가 열리며, drain 전압에 민감한 큰 off-current가 흐른다. 이는 surface barrier가 drain에 의해 낮아지는 DIBL의 극단적 2차원 electrostatic failure로 볼 수 있지만, 전류 경로는 surface subthreshold path와 구별될 수 있다.[2,12,13]

**실험과 metric.** $V_G$를 off bias에 고정하고 여러 channel length에서 $I_D$–$V_D$를 측정한다. 길이가 짧을수록 나타나는 급격한 $I_D$ 증가와 큰 $g_{ds,\mathrm{off}}=\partial I_D/\partial V_D$를 찾고, body bias와 온도 의존성을 함께 본다. Punch-through voltage $V_\mathrm{PT}$는 “지정한 폭 정규화 전류에 도달하는 $V_D$”처럼 재현 가능한 기준으로 정의해야 하며, 기준전류를 반드시 병기한다. 단순한 GIDL과 접합 breakdown도 높은 $V_D$에서 증가하므로 $I_B$, $I_G$와 length split 없이 $V_\mathrm{PT}$를 지정하지 않는다.[2,12,13]

## 4. Diagnostic Workflow

| 관측 | 다음 확인 | 우선 해석 |
| --- | --- | --- |
| 낮은 $V_D$에서도 반로그 $I_D$–$V_G$가 직선 | SS와 온도의존성 | Subthreshold |
| 높은 $V_D$에서 $I_D$–$V_G$가 수평 이동 | 동일 방법으로 $V_T$ 추출 | DIBL-enhanced subthreshold |
| $\lvert I_G\rvert$가 크고 area에 비례 | $I_S$, $I_D$ partition | Gate tunneling |
| Gate와 무관한 $I_B$ 또는 diode current | 면적·둘레 split, 온도 sweep | Junction leakage |
| 낮은/음의 $V_G$에서 $\lvert V_{DG}\rvert$에 급민감 | $I_B$ 동시 증가, $I_G$ 배제 | GIDL |
| 짧은 $L$에서 off $I_D$–$V_D$가 급증 | length/body-bias split | Punch-through |

이 표는 결정 트리가 아니라 최소 진단 순서이다. 실제 off-current는 여러 성분의 합이며, stress와 self-heating이 있으면 sweep 순서 자체가 결과를 바꿀 수 있다.[1,7,9]

## 5. Summary

- $I_\mathrm{OFF}$는 총량 metric이며, 원인 규명에는 네 단자전류와 bias·온도·geometry split이 필요하다.
- Subthreshold leakage는 SS와 DIBL, gate tunneling은 $J_G$와 terminal partition으로 정량화한다.
- Junction leakage는 면적·둘레 성분, GIDL은 drain-edge field와 body current, punch-through는 length-dependent off $I_D$–$V_D$로 분리한다.
- 모든 metric에는 바이어스, 온도, 정규화, 추출 기준을 포함해야 비교가 재현된다.

## 6. References

1. K. Roy, S. Mukhopadhyay, and H. Mahmoodi-Meimand, “Leakage Current Mechanisms and Leakage Reduction Techniques in Deep-Submicrometer CMOS Circuits,” *Proceedings of the IEEE* **91**, 305–327 (2003). [DOI: 10.1109/JPROC.2002.808156](https://doi.org/10.1109/JPROC.2002.808156).
2. C. Hu, *Modern Semiconductor Devices for Integrated Circuits*, Chapter 7, Pearson (2010). [저자 제공 PDF](https://www.chu.berkeley.edu/wp-content/uploads/2020/01/Chenming-Hu_ch7.pdf).
3. D. J. Frank et al., “Device Scaling Limits of Si MOSFETs and Their Application Dependencies,” *Proceedings of the IEEE* **89**, 259–288 (2001). [DOI: 10.1109/5.915374](https://doi.org/10.1109/5.915374).
4. K. N. Yang et al., “Characterization and Modeling of Edge Direct Tunneling (EDT) Leakage in Ultrathin Gate Oxide MOSFETs,” *IEEE Transactions on Electron Devices* **48**, 1159–1164 (2001). [DOI: 10.1109/16.925242](https://doi.org/10.1109/16.925242).
5. L. Huang, P. T. Lai, J. P. Xu, and Y. C. Cheng, “Mechanism Analysis of Gate-Induced Drain Leakage in Off-State n-MOSFET,” *Microelectronics Reliability* **38**, 1425–1431 (1998). [DOI: 10.1016/S0026-2714(98)00044-4](https://doi.org/10.1016/S0026-2714(98)00044-4).
6. H.-F. Chen et al., “Investigation of the Characteristics of GIDL Current in 90 nm CMOS Technology,” *Chinese Physics* **15**, 645–648 (2006). [DOI: 10.1088/1009-1963/15/3/034](https://doi.org/10.1088/1009-1963/15/3/034).
7. D. K. Schroder, *Semiconductor Material and Device Characterization*, 3rd ed., Wiley (2006). [DOI: 10.1002/0471749095](https://doi.org/10.1002/0471749095).
8. A. Ortiz-Conde et al., “Revisiting MOSFET Threshold Voltage Extraction Methods,” *Microelectronics Reliability* **53**, 90–104 (2013). [DOI: 10.1016/j.microrel.2012.09.015](https://doi.org/10.1016/j.microrel.2012.09.015).
9. Keysight Technologies, “DC MOSFET Characterization at the Wafer Level,” Application Note 5990-5547EN (2019). [공식 문서](https://www.keysight.com/my/en/assets/7018-02489/application-notes/5990-5547.pdf).
10. Tektronix/Keithley, *Low Level Measurements Handbook*, 7th ed. [공식 문서](https://www.tek.com/en/documents/product-article/keithley-low-level-measurements-handbook---7th-edition) (접속일: 2026-07-31).
11. S. M. Sze and K. K. Ng, *Physics of Semiconductor Devices*, 3rd ed., Wiley (2006). [DOI: 10.1002/0470068329](https://doi.org/10.1002/0470068329).
12. N. Kotani and S. Kawazu, “Computer Analysis of Punch-Through in MOSFETs,” *Solid-State Electronics* **22**, 63–70 (1979). [DOI: 10.1016/0038-1101(79)90172-2](https://doi.org/10.1016/0038-1101(79)90172-2).
13. J. J. Barnes, K. Shimohigashi, and R. W. Dutton, “Short-Channel MOSFET’s in the Punchthrough Current Mode,” *IEEE Transactions on Electron Devices* **26**, 446–453 (1979). [DOI: 10.1109/T-ED.1979.19447](https://doi.org/10.1109/T-ED.1979.19447).
14. Tosaka, “Leakage Current (2 models),” Wikimedia Commons (2008), CC BY-SA 3.0. [파일 설명과 라이선스](https://commons.wikimedia.org/wiki/File:Leakage_Current_(2_models).PNG).
15. Fadeaway919, “FET subthreshold leakage,” Wikimedia Commons (2015), CC BY-SA 3.0. [파일 설명과 라이선스](https://commons.wikimedia.org/wiki/File:FET_subthreshold_leakage.png).
