---
title: "(1) MOSFET: Basic Operation"
description: nMOS의 게이트 제어, 동작 영역, 대표 DC 특성과 이 위키에서 공통으로 사용하는 기호·추출 규약
status: verified
last_verified: 2026-08-01
---

# (1) MOSFET: Basic Operation

Metal-oxide-semiconductor field-effect transistor (MOSFET)는 절연된 게이트가 반도체 표면의 전하를 조절하여 소스와 드레인 사이의 전류를 제어하는 네 단자 소자이다. 이 글은 이후의 [MOSFET: Leakage Current](leakage-mechanisms.md)와 [MOSFET: Short-Channel Effects](short-channel-effects.md)에 공통으로 필요한 nMOS 동작, 기호와 direct current (DC) 추출 규약만 정리한다.[1,2]

## 1. 게이트가 만드는 반전 채널

Enhancement-mode n-channel MOSFET (nMOS)는 p-type 바디 안의 n-type 소스·드레인, 게이트 절연막과 게이트 전극으로 이루어진다. 양의 $V_{GS}$가 표면전위를 충분히 높이면 게이트 아래에 전자 반전층이 형성되고, 이 층이 소스와 드레인을 잇는 전도 채널이 된다. 바디 전압은 문턱전압과 접합 바이어스를 바꾸므로 MOSFET는 본질적으로 게이트·드레인·소스·바디의 네 단자 소자이다.[1,2]

장채널 charge-sheet model에서 채널 위치 $x$의 반전 전하밀도는 강한 반전 동안

$$
Q_\mathrm{inv}(x)
\approx
-C_\mathrm{ox}\left[V_{GS}-V_T-V(x)\right]
$$

로 쓸 수 있다. $C_\mathrm{ox}$는 단위 면적당 게이트 절연막 정전용량, $V_T$는 문턱전압, $V(x)$는 소스를 기준으로 한 국소 채널 전위이다. 이 식은 게이트가 채널 전하를 늘리고 드레인 전압이 드레인 쪽 반전 전하를 줄이는 기본 관계를 보여준다.[1,2]

## 2. 세 동작 영역과 장채널 기준식

바디를 소스에 연결한 nMOS의 가장 단순한 동작 영역은 다음과 같다.[1,2]

| 동작 영역 | 장채널 경계 | 채널 상태 | 대표 관측 |
| --- | --- | --- | --- |
| 약한 반전·꺼짐 | $V_{GS}<V_T$ | 강한 반전 채널이 없으며 열전자 전류가 지수적으로 변함 | 반로그 전달 특성 |
| 선형 영역 | $V_{GS}>V_T$, $0<V_{DS}<V_{GS}-V_T$ | 소스부터 드레인까지 반전 채널이 이어짐 | 작은 $V_{DS}$에서 저항성 전도 |
| 포화 영역 | $V_{GS}>V_T$, $V_{DS}\ge V_{GS}-V_T$ | 드레인 쪽 반전 전하가 소진되어 pinch-off가 형성됨 | 이상 모형에서 전류 포화 |

일정한 이동도 $\mu_n$, 점진 채널 근사와 준정적 동작을 가정하면 선형 영역 전류는

$$
I_D
\approx
\mu_n C_\mathrm{ox}\frac{W}{L}
\left[
(V_{GS}-V_T)V_{DS}
-\frac{V_{DS}^2}{2}
\right]
$$

이고, 포화 경계 이후에는

$$
I_{D,\mathrm{sat}}
\approx
\frac{1}{2}\mu_n C_\mathrm{ox}\frac{W}{L}
(V_{GS}-V_T)^2
$$

로 쓸 수 있다.[1,2] 이 식들은 기준 모형이다. 실제 단채널 소자에서는 mobility degradation, velocity saturation, channel-length modulation (CLM), 직렬저항과 short-channel effects (SCE) 때문에 경계와 전압 의존성이 달라진다.[2,3]

## 3. 대표 DC 특성과 미분량

전달 특성은 $V_D$를 고정하고 $I_D$–$V_G$를 측정한 곡선이며, 문턱전압 아래 전류, $V_T$, 켜짐 전류와 transconductance $g_m$을 드러낸다. 출력 특성은 여러 $V_G$에서 얻은 $I_D$–$V_D$ 곡선이며, 선형–포화 전이와 output conductance $g_{ds}$를 드러낸다.[1–3]

$$
g_m
=
\left.\frac{\partial I_D}{\partial V_G}\right|_{V_D,V_B},
\qquad
g_{ds}
=
\left.\frac{\partial I_D}{\partial V_D}\right|_{V_G,V_B},
\qquad
r_o=\frac{1}{g_{ds}}.
$$

!!! info "[Measurement]"
    전달 특성은 $(V_D,V_S,V_B,T)$를 고정하고 $V_G$를 주사하며 측정한다. 지정한 기준전류 $I_\mathrm{ref}$를 사용하는 constant-current method에서는

    $$
    V_T
    =
    V_G\ \text{at}\ |I_D|/W=I_\mathrm{ref}
    $$

    로 추출한다. 문턱전압 아래의 지정 구간에서는

    $$
    \mathrm{SS}
    =
    \left(
    \frac{d\log_{10}(|I_D|/W)}{dV_G}
    \right)^{-1}
    $$

    를 회귀하여 subthreshold swing (SS)을 구한다. 출력 특성은 $V_G$를 단계적으로 고정하고 $V_D$를 주사하며 측정하고, 선택한 바이어스점 또는 맞춤 구간에서 위 식의 $g_m$과 $g_{ds}$를 계산한다. $V_T$는 추출법에 따라 값이 달라질 수 있으므로 한 소자군에서는 방법과 $I_\mathrm{ref}$를 바꾸지 않는다.[2–4]

## 4. 이 위키의 공통 규약

이후 MOSFET 글은 별도 표기가 없으면 enhancement-mode 평면형 벌크 nMOS, DC, $V_S=V_B=0$을 기준으로 설명한다. 전압은 $V_{XY}=V_X-V_Y$로 정의한다. 단자 전류의 방향이 핵심이면 부호 있는 $I_G$, $I_D$, $I_S$, $I_B$를 사용하고, 크기나 정규화된 성능을 비교할 때에는 $|I_X|$를 사용한다.

| 양 | 이 위키의 정의 | 함께 기록할 조건 |
| --- | --- | --- |
| $V_T$ | 선언한 $I_\mathrm{ref}$에서 얻은 $V_G$ | 추출법, $I_\mathrm{ref}$, $V_D$, $V_B$, $T$ |
| $I_\mathrm{OFF}$ | 선언한 꺼짐 바이어스에서의 $|I_D|$ | 모든 단자 전압, $T$, $W$, $L$ |
| $I_\mathrm{ON}$ | 선언한 켜짐 바이어스에서의 $|I_D|$ | 모든 단자 전압, $T$, $W$, $L$ |
| SS | $dV_G/d\log_{10}(|I_D|/W)$ | 전류 구간, $V_D$, $T$, 회귀법 |
| $g_m$ | $\partial I_D/\partial V_G$ | 고정한 $V_D$, $V_B$, 바이어스점·구간 |
| $g_{ds}$ | $\partial I_D/\partial V_D$ | 고정한 $V_G$, $V_B$, 바이어스점·구간 |

전류 정규화는 물리적 경로에 맞춘다. 채널 전류는 보통 유효 폭 $W$, 게이트 절연막 전류는 게이트 면적, 접합 전류는 바닥 면적과 둘레 성분으로 나눈다. 따라서 서로 다른 정규화 기준의 수치를 직접 비교하지 않는다.[2,5]

## 5. 요약

- nMOS에서는 양의 게이트 전압이 전자 반전 채널을 만들고 소스–드레인 전류를 제어한다.
- 장채널 기준 모형은 약한 반전, 선형 영역과 포화 영역을 구분하며, 단채널 글의 비교 기준으로 사용한다.
- 전달 특성은 $V_T$, SS와 $g_m$, 출력 특성은 선형–포화 전이와 $g_{ds}$를 드러낸다.
- 이후 글은 별도 표기가 없으면 nMOS, DC, $V_S=V_B=0$과 이 글의 전압·전류·정규화 규약을 따른다.

## 6. 참고문헌

1. J. A. del Alamo, “Lecture 9 — MOSFET (I): MOSFET I–V Characteristics,” MIT OpenCourseWare 6.012, *Microelectronic Devices and Circuits* (2005). [강의 자료 PDF](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2005/resources/lec9/).
2. C. Hu, *Modern Semiconductor Devices for Integrated Circuits*, Chapter 6, Pearson (2010). [저자 제공 PDF](https://www.chu.berkeley.edu/wp-content/uploads/2020/01/Chenming-Hu_ch6-1.pdf).
3. Analog Devices, “Chapter 8: Transistors — Metal-Oxide-Semiconductor Field-Effect Transistor Basics,” *Analog Devices University Program*. [공식 교육 자료](https://wiki.analog.com/university/courses/electronics/text/chapter-8).
4. A. Ortiz-Conde et al., “Revisiting MOSFET Threshold Voltage Extraction Methods,” *Microelectronics Reliability* **53**, 90–104 (2013). [DOI: 10.1016/j.microrel.2012.09.015](https://doi.org/10.1016/j.microrel.2012.09.015).
5. D. K. Schroder, *Semiconductor Material and Device Characterization*, 3rd ed., Wiley (2006). [DOI: 10.1002/0471749095](https://doi.org/10.1002/0471749095).
