---
title: "(1) MOSFET: Basic Operation"
description: MOSFET의 네 단자 구조, nMOS와 pMOS, enhancement mode와 depletion mode, 채널 형성과 기본 전류–전압 특성
status: verified
last_verified: 2026-08-01
---

# (1) MOSFET: Basic Operation

Metal-oxide-semiconductor field-effect transistor (MOSFET)는 게이트 전기장으로 반도체 표면의 전하를 바꾸어 소스와 드레인 사이의 전류를 제어하는 소자이다. 가장 단순하게는 전압으로 여닫는 스위치로 볼 수 있지만, 실제 동작을 이해하려면 채널 종류, 0 V에서의 채널 유무, 바디 바이어스와 드레인 전압을 함께 보아야 한다.[1,2]

이 글은 MOSFET 자체의 기본 구조와 동작을 설명한다. 누설 메커니즘은 [MOSFET: Leakage Current](leakage-mechanisms.md), 채널이 짧아질 때 달라지는 정전기와 수송은 [MOSFET: Short-Channel Effects](short-channel-effects.md)에서 이어서 다룬다.

## 1. 네 단자와 기본 구조

MOSFET는 게이트(gate), 소스(source), 드레인(drain), 바디(body)의 네 단자로 이루어진다. 회로도에서는 바디를 소스와 연결해 세 단자처럼 그리기도 하지만, 바디 전압은 threshold voltage와 소스·드레인 접합의 바이어스를 바꾸므로 독립된 제어 단자로 보아야 한다.[1–3]

| 단자 | 역할 | 기본 동작에서 확인할 점 |
| --- | --- | --- |
| 게이트 $G$ | 절연막을 사이에 두고 채널 전하를 제어한다. | 정상적인 DC 동작에서는 절연막을 가로지르는 전류가 매우 작지만, 실제 절연막에는 누설과 정전용량이 존재한다. |
| 소스 $S$ | 채널에 주 운반자를 공급한다. | 모든 게이트·드레인 바이어스는 보통 소스를 기준으로 쓴다. |
| 드레인 $D$ | 채널을 지난 운반자를 받아들이며, 채널 방향의 전기장을 만든다. | $V_{DS}$가 채널 전하 분포와 동작 영역을 바꾼다. |
| 바디 $B$ | 채널이 형성되는 반도체 영역이며 소스·드레인과 pn 접합을 이룬다. | $V_{BS}$ 또는 $V_{SB}$가 body effect와 접합 바이어스를 정한다. |

n-channel MOSFET (nMOS)는 보통 p-type 바디 안에 n-type 소스와 드레인을 둔다. 채널이 켜지면 전자가 주 운반자가 된다. p-channel MOSFET (pMOS)는 반대로 n-type 바디 안에 p-type 소스와 드레인을 두며, 정공이 주 운반자가 된다. CMOS 회로에서는 nMOS 바디를 가장 낮은 전위에, pMOS 바디를 가장 높은 전위에 연결하여 소스·드레인–바디 접합이 순방향으로 켜지지 않게 하는 것이 기본이다.[1,2,4]

## 2. MOSFET을 나누는 두 기준

nMOS/pMOS와 enhancement/depletion mode는 서로 다른 분류이다. 앞의 구분은 **채널의 주 운반자와 전압 극성**을, 뒤의 구분은 **$V_{GS}=0$일 때 채널이 이미 존재하는지**를 나타낸다.[1,2,5,6]

### (1) 채널 종류: nMOS와 pMOS

nMOS는 $V_{GS}$를 양의 방향으로 올릴수록 전자 채널이 강해진다. pMOS는 극성이 반대이므로 $V_{GS}$를 음의 방향으로 내리거나, 같은 뜻으로 $V_{SG}=V_S-V_G$를 양의 방향으로 올릴수록 정공 채널이 강해진다. 따라서 nMOS와 pMOS의 켜짐 조건을 비교할 때에는 전압의 부호를 생략하면 안 된다.[1,2,4]

### (2) 동작 모드: enhancement mode와 depletion mode

Enhancement-mode MOSFET은 $V_{GS}=0$에서 전도 채널이 없는 normally-off 소자이다. 게이트 전압으로 채널을 새로 형성해야 켜진다. Depletion-mode MOSFET은 $V_{GS}=0$에서도 채널이 존재하는 normally-on 소자이며, 채널의 주 운반자를 밀어내는 방향의 게이트 전압을 걸어야 꺼진다.[5,6]

다음 표는 두 분류 정의와 pMOS의 전압 극성 반전을 $V_{GS}=V_G-V_S$ 규약으로 조합하여 정리한 것이다.[1,2,4–6]

| 채널과 모드 | $V_{GS}=0$의 상태 | 대표적인 $V_T$ 부호 | 채널을 강하게 하는 방향 | 끄는 방향 |
| --- | --- | --- | --- | --- |
| nMOS, enhancement mode | 꺼짐 | $V_T>0$ | $V_{GS}>V_T$ | $V_{GS}<V_T$ |
| pMOS, enhancement mode | 꺼짐 | $V_T<0$ | $V_{GS}<V_T$, 또는 $V_{SG}>\lvert V_T\rvert$ | $V_{GS}>V_T$ |
| nMOS, depletion mode | 켜짐 | $V_T<0$ | $V_{GS}$를 더 양의 방향으로 인가 | $V_{GS}<V_T$ |
| pMOS, depletion mode | 켜짐 | $V_T>0$ | $V_{GS}$를 더 음의 방향으로 인가 | $V_{GS}>V_T$ |

!!! note "용어 구분"
    Depletion mode는 소자를 $V_{GS}=0$에서 normally-on인지로 분류하는 이름이다. 반면 **depletion region**은 게이트 또는 pn 접합의 전기장 때문에 이동 가능한 운반자가 줄어든 공간을 뜻한다. 두 표현은 이름이 비슷하지만 같은 개념이 아니다.

이후 MOSFET 문서는 별도 설명이 없으면 집적회로에서 가장 일반적인 enhancement-mode nMOS를 기준으로 한다. Depletion-mode MOSFET은 실제로 판매되고 사용되는 소자이지만, 기본 논리 CMOS를 설명할 때의 기준 소자는 아니다.[2,5,6]

## 3. 게이트 전압이 채널을 만드는 과정

### (1) Accumulation, Depletion과 Inversion

p-type 바디를 가진 enhancement-mode nMOS를 생각하자. 게이트 전압을 음의 방향으로 인가하면 정공이 산화막–반도체 계면에 모인다. 이 상태를 accumulation이라고 한다. 게이트 전압을 양의 방향으로 올리면 정공이 계면에서 밀려나 depletion region이 넓어진다. 전압이 충분히 커지면 계면의 전자 농도가 증가하여 p-type 바디 표면에서 inversion이 일어난다. 이때 형성된 inversion layer가 소스와 드레인을 연결하는 채널이다.[1,2]

Threshold voltage $V_T$는 strong inversion이 시작되는 기준 전압으로 사용한다. 그러나 실제 $I_D$–$V_G$ 특성은 weak inversion에서 strong inversion으로 연속적으로 변하므로, 측정에서 얻는 $V_T$는 선택한 추출법과 기준전류에 따라 달라질 수 있다.[2,7,8]

### (2) 채널 전하와 body effect

바디를 소스에 연결한 장채널 nMOS에서, 점진 채널 근사와 강한 반전을 가정하면 위치 $x$의 반전 전하밀도는

$$
Q_\mathrm{inv}(x)
\approx
-C_\mathrm{ox}
\left[
V_{GS}-V_T-V(x)
\right]
$$

로 쓸 수 있다. $C_\mathrm{ox}=\varepsilon_\mathrm{ox}/t_\mathrm{ox}$는 단위 면적당 게이트 절연막 정전용량이고, $V(x)$는 소스를 기준으로 한 국소 채널 전위이다. 게이트 전압은 반전 전하를 늘리지만, 드레인에 가까워져 $V(x)$가 커질수록 같은 게이트 전압에서 채널 전하는 줄어든다.[1,2]

nMOS에서 소스–바디 접합의 역바이어스 $V_{SB}$를 키우면 더 많은 게이트 전압이 바디의 공핍 전하를 지지하는 데 쓰인다. 그 결과 $V_T$가 증가하고 같은 $V_{GS}$에서 채널 전하와 드레인 전류가 감소한다. 이를 body effect라고 한다. 균일하게 도핑된 p-type 바디의 장채널 근사에서는

$$
V_T(V_{SB})
=
V_{T0}
+
\gamma
\left(
\sqrt{2\lvert\phi_F\rvert+V_{SB}}
-
\sqrt{2\lvert\phi_F\rvert}
\right)
$$

로 나타낼 수 있다. $V_{T0}$는 $V_{SB}=0$일 때의 $V_T$, $\phi_F$는 바디의 Fermi potential, $\gamma$는 body-effect parameter이다. 실제 도핑 분포가 균일하지 않으면 이 식의 단순한 제곱근 의존성에서 벗어날 수 있다.[2,3]

## 4. nMOS의 기본 동작 영역

바디를 소스에 연결한 enhancement-mode 장채널 nMOS는 이상적인 기준 모형에서 cutoff, linear region과 saturation region으로 나눌 수 있다.[1–3]

| 동작 영역 | 장채널 경계 | 채널 상태 | 전류 특성 |
| --- | --- | --- | --- |
| cutoff·weak inversion | $V_{GS}<V_T$ | strong inversion channel이 형성되지 않음 | 이상적인 스위치 모형에서는 0이지만 실제 전류는 지수적으로 변한다. |
| linear region | $V_{GS}>V_T$, $0<V_{DS}<V_{GS}-V_T$ | 소스에서 드레인까지 inversion channel이 이어짐 | 작은 $V_{DS}$에서 전압으로 제어되는 저항처럼 동작한다. |
| saturation region | $V_{GS}>V_T$, $V_{DS}\ge V_{GS}-V_T$ | 드레인 쪽 채널이 pinch-off에 도달함 | 이상적인 장채널 모형에서는 $I_D$가 $V_{DS}$에 거의 무관하다. |

일정한 전자 이동도 $\mu_n$, gradual-channel approximation, 준정적 동작과 $V_{SB}=0$을 가정하면 linear-region current는

$$
I_D
\approx
\mu_n C_\mathrm{ox}\frac{W}{L}
\left[
(V_{GS}-V_T)V_{DS}
-\frac{V_{DS}^2}{2}
\right]
$$

이다. $W$와 $L$은 각각 채널 폭과 길이이다. $V_{DS}\ll V_{GS}-V_T$이면

$$
I_D
\approx
\mu_n C_\mathrm{ox}\frac{W}{L}
(V_{GS}-V_T)V_{DS}
$$

이므로 $I_D$가 $V_{DS}$에 거의 비례한다.[1,2]

$V_{DS}=V_{GS}-V_T$에서 드레인 끝의 inversion charge가 장채널 근사상 0에 도달하며 pinch-off가 시작된다. 그 이후의 이상적인 saturation current는

$$
I_{D,\mathrm{sat}}
\approx
\frac{1}{2}
\mu_n C_\mathrm{ox}\frac{W}{L}
(V_{GS}-V_T)^2
$$

로 쓸 수 있다.[1–3]

!!! warning "[Interpretation Caveat]"
    Pinch-off는 드레인 전류가 끊긴다는 뜻이 아니다. 드레인 쪽의 짧은 고전계 영역을 통해 운반자가 계속 이동한다. 실제 소자에서는 channel-length modulation (CLM), mobility degradation, velocity saturation, 직렬저항과 short-channel effects (SCE) 때문에 전류가 이상적인 제곱 법칙과 평탄한 포화에서 벗어난다.[2,3]

## 5. pMOS의 전압과 전류

pMOS는 nMOS와 같은 전계효과 원리로 동작하지만 전압과 전류의 극성이 반대이다. Enhancement-mode pMOS에서는 소스를 높은 전위에 두고 게이트 전압을 소스보다 낮추어 $V_{SG}>0$으로 만들면 정공 채널이 형성된다. 계산과 그래프에서는 부호 혼동을 줄이기 위해 $V_{SG}$, $V_{SD}$와 $\lvert I_D\rvert$를 자주 사용한다.[1,2,4]

| 비교 항목 | enhancement-mode nMOS | enhancement-mode pMOS |
| --- | --- | --- |
| 주 운반자 | 전자 | 정공 |
| 일반적인 바디 | p-type | n-type |
| 켜짐 조건 | $V_{GS}>V_{Tn}>0$ | $V_{SG}>\lvert V_{Tp}\rvert$, 즉 $V_{GS}<V_{Tp}<0$ |
| 일반적인 드레인 바이어스 | $V_{DS}>0$ | $V_{SD}>0$ |
| CMOS에서의 기본 바디 전위 | 가장 낮은 전위 | 가장 높은 전위 |

pMOS의 장채널 전류 크기는 nMOS 식에서 $(V_{GS},V_{DS},V_T,\mu_n)$을 $(V_{SG},V_{SD},\lvert V_{Tp}\rvert,\mu_p)$로 바꾸어 같은 형태로 쓸 수 있다. 다만 전자와 정공의 이동도가 다르므로 같은 $W/L$과 gate overdrive에서도 두 소자의 전류가 같다고 가정해서는 안 된다.[2,4]

## 6. 대표 전기 특성과 추출량

Transfer characteristics는 $V_D$를 고정하고 얻은 $I_D$–$V_G$ 곡선이다. 이 곡선에서 $I_\mathrm{OFF}$, $V_T$, $I_\mathrm{ON}$과 transconductance $g_m$을 확인한다. Output characteristics는 여러 $V_G$에서 얻은 $I_D$–$V_D$ 곡선이며, linear-to-saturation transition과 output conductance $g_{ds}$를 보여준다.[1,2]

$$
g_m
=
\left.
\frac{\partial I_D}{\partial V_G}
\right|_{V_D,V_B},
\qquad
g_{ds}
=
\left.
\frac{\partial I_D}{\partial V_D}
\right|_{V_G,V_B},
\qquad
r_o=\frac{1}{g_{ds}}.
$$

!!! info "[Measurement]"
    전달 특성은 $(V_D,V_S,V_B,T)$를 고정하고 $V_G$를 주사하여 측정한다. 지정한 기준전류 $I_\mathrm{ref}$를 사용하는 constant-current method에서는

    $$
    V_T
    =
    V_G
    \quad\text{when}\quad
    \frac{\lvert I_D\rvert}{W}=I_\mathrm{ref}
    $$

    로 정한다. 지정한 subthreshold current 구간에서는

    $$
    \mathrm{SS}
    =
    \left(
    \frac{d\log_{10}(\lvert I_D\rvert/W)}{dV_G}
    \right)^{-1}
    $$

    를 회귀하여 subthreshold swing (SS)을 구한다. 출력 특성은 $V_G$를 단계적으로 고정하고 $V_D$를 주사하여 측정한다. $V_T$는 추출법과 $I_\mathrm{ref}$에 의존하므로, 소자 사이를 비교할 때에는 같은 방법과 바이어스를 사용해야 한다.[2,7,8]

## 7. 이 위키의 공통 규약

이후 MOSFET 글은 별도 표기가 없으면 enhancement-mode 평면형 벌크 nMOS, DC, $V_S=V_B=0$을 기준으로 설명한다. 전압은 $V_{XY}=V_X-V_Y$로 정의한다. 단자 전류의 방향이 중요할 때에는 부호 있는 $I_G$, $I_D$, $I_S$, $I_B$를 사용하고, 전류 크기나 정규화된 성능을 비교할 때에는 $\lvert I_X\rvert$를 사용한다.

| 물리량 | 이 위키의 정의 | 함께 기록할 조건 |
| --- | --- | --- |
| $V_T$ | 선언한 $I_\mathrm{ref}$에서 얻은 $V_G$ | 추출법, $I_\mathrm{ref}$, $V_D$, $V_B$, $T$ |
| $I_\mathrm{OFF}$ | 선언한 꺼짐 바이어스에서의 $\lvert I_D\rvert$ | 모든 단자 전압, $T$, $W$, $L$ |
| $I_\mathrm{ON}$ | 선언한 켜짐 바이어스에서의 $\lvert I_D\rvert$ | 모든 단자 전압, $T$, $W$, $L$ |
| SS | $dV_G/d\log_{10}(\lvert I_D\rvert/W)$ | 전류 구간, $V_D$, $T$, 회귀법 |
| $g_m$ | $\partial I_D/\partial V_G$ | 고정한 $V_D$, $V_B$, 바이어스점·구간 |
| $g_{ds}$ | $\partial I_D/\partial V_D$ | 고정한 $V_G$, $V_B$, 바이어스점·구간 |

전류의 정규화 기준은 실제 전류 경로에 맞춘다. 채널 전류는 보통 유효 폭 $W$, 게이트 절연막 전류는 게이트 면적, 접합 전류는 접합의 바닥 면적과 둘레를 기준으로 나눈다. 정규화 기준이 다른 수치는 직접 비교하지 않는다.

## 8. 기준 모형의 한계와 다음 글

이 글의 전류식은 MOSFET의 기본 의존성을 보여주는 장채널 기준식이다. 실제 소자의 정확한 전류를 예측하는 compact model이 아니며, 약한 반전 누설, 양자역학적 터널링, 고전계 이동도, 속도 포화와 2차원 정전기를 모두 포함하지 않는다. 따라서 식과 측정값이 어긋날 때에는 먼저 가정이 맞는지 확인해야 한다.[2,3]

- 꺼짐 상태에서 전류가 생기는 경로는 [MOSFET: Leakage Current](leakage-mechanisms.md)에서 다룬다.
- 채널 길이 감소에 따른 DIBL, $V_T$ roll-off와 SS degradation은 [MOSFET: Short-Channel Effects](short-channel-effects.md)에서 다룬다.
- SOI, FinFET과 GAA 구조에서 게이트 제어가 달라지는 과정은 [MOSFET: Architecture Evolution](architecture-evolution.md)에서 다룬다.

## 9. 요약

- MOSFET는 게이트, 소스, 드레인, 바디로 이루어진 네 단자 소자이며, 바디 전압은 threshold voltage와 접합 바이어스를 바꾼다.
- nMOS/pMOS는 채널의 주 운반자와 전압 극성을, enhancement/depletion mode는 $V_{GS}=0$에서의 채널 유무를 구분한다.
- Enhancement-mode nMOS에서는 양의 $V_{GS}$가 depletion을 거쳐 전자 inversion channel을 형성하며, reverse body bias는 body effect를 통해 $V_T$를 높인다.
- 장채널 기준 모형은 cutoff, linear region과 saturation region을 구분한다. Saturation에서 나타나는 pinch-off는 전류가 끊기는 현상이 아니다.
- Transfer characteristics는 $V_T$, SS와 $g_m$을, output characteristics는 linear-to-saturation transition과 $g_{ds}$를 보여준다.
- 후속 MOSFET 글은 별도 표기가 없으면 enhancement-mode 평면형 벌크 nMOS와 이 글의 전압·전류 규약을 따른다.

## 10. 참고문헌

1. J. A. del Alamo, “Lecture 9 — MOSFET (I): MOSFET I–V Characteristics,” MIT OpenCourseWare 6.012, *Microelectronic Devices and Circuits* (2005). [강의 자료 PDF](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2005/resources/lec9/).
2. C. Hu, *Modern Semiconductor Devices for Integrated Circuits*, Chapter 6, Pearson (2010). [저자 제공 PDF](https://www.chu.berkeley.edu/wp-content/uploads/2020/01/Chenming-Hu_ch6-1.pdf).
3. J. A. del Alamo, “Lecture 10 — MOSFET (II): MOSFET I–V Characteristics (cont.),” MIT OpenCourseWare 6.012, *Microelectronic Devices and Circuits* (2005). [강의 자료 PDF](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2005/resources/lec10/).
4. MIT OpenCourseWare, “6.012 Microelectronic Devices and Circuits, Lecture 12,” Spring 2009. [강의 자료 PDF](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-spring-2009/resources/mit6_012s09_lec12/).
5. B. Chen, “Depletion-Mode MOSFET: The Forgotten FET,” Supertex/Microchip Application Note AN-D66 (2013). [공식 PDF](https://www.microchip.com/content/dam/mchp/documents/OTH/ApplicationNotes/ApplicationNotes/AN-D66.pdf).
6. Infineon Technologies, “Applications for Depletion MOSFETs,” Application Note, Version 1.0 (2018). [공식 PDF](https://www.infineon.com/assets/row/public/documents/24/42/infineon-application-note-applications-for-depletion-mosfets-applicationnotes-en.pdf).
7. A. Ortiz-Conde et al., “Revisiting MOSFET Threshold Voltage Extraction Methods,” *Microelectronics Reliability* **53**, 90–104 (2013). [DOI: 10.1016/j.microrel.2012.09.015](https://doi.org/10.1016/j.microrel.2012.09.015).
8. Keysight Technologies, “MOSFET Threshold Voltage Extraction: How to Get Power Management Right from the Beginning” (2023). [공식 기술 자료](https://www.keysight.com/blogs/en/tech/sim-des/mosfet-threshold-voltage-extraction).
