---
title: "1.5. MOSFET: CMOS"
description: CMOS inverter의 정적 전달 특성, noise margin, switching delay와 전력에서 기본 논리 게이트와 소자–회로 연결 지표까지 설명
status: verified
last_verified: 2026-08-14
---

# 1.5. MOSFET: CMOS

Complementary metal-oxide-semiconductor (CMOS)는 nMOS pull-down network (PDN)와 pMOS pull-up network (PUN)를 상보적으로 구성하는 집적회로 방식이다. 정적 CMOS 논리에서는 정상적인 논리 상태에서 출력이 전원선 또는 접지선에 저저항 경로로 연결되며, 이상적인 소자라면 두 전원선 사이의 직류 경로는 끊어진다. 따라서 rail-to-rail 출력과 큰 noise margin을 얻으면서 정지 상태 전력을 작게 만들 수 있다. 실제 회로에는 subthreshold·gate·junction leakage가 있으므로 “정적 전력이 0”이라는 표현은 이상적 스위치 모형에만 해당한다.[1,2]

이 글은 정적 CMOS inverter를 기준 회로로 삼아 voltage transfer characteristic (VTC), noise margin, propagation delay와 전력의 정의를 유도하고, 이를 NAND·NOR 게이트와 소자 지표에 연결한다. MOSFET의 바이어스와 전류식은 [MOSFET: Overview](basic-operation.md), 누설 경로는 [MOSFET: Leakage current](leakage-mechanisms.md), 짧은 채널에서 장채널식이 무너지는 원인은 [MOSFET: Short-channel effects](short-channel-effects.md), FinFET·GAA를 포함한 구조 변화는 [MOSFET: Architecture evolution](architecture-evolution.md)를 따른다. 아날로그 CMOS, 순차회로, HDL·논리합성, 배치·배선과 일반적인 design–technology co-optimization (DTCO)은 범위에서 제외한다.

별도 설명이 없으면 nMOS 바디는 $0\ \mathrm{V}$, pMOS 바디는 $V_{DD}$에 연결하고, 입력과 출력은 각각 $V_\mathrm{in}$과 $V_\mathrm{out}$으로 쓴다. pMOS 전류는 전원에서 출력으로 흐르는 양의 크기 $I_p$로 정의하고, nMOS 전류 $I_n$은 출력에서 접지로 흐르는 양의 크기로 정의한다.

## 1. CMOS inverter

CMOS inverter는 입력을 공유하는 pMOS와 nMOS의 드레인을 출력에 연결한 가장 작은 상보 논리 회로이다. 입력이 낮으면 pMOS가 출력을 충전하고, 입력이 높으면 nMOS가 출력을 방전한다. 이 한 회로에 논리 레벨 복원, 전압 이득, 정전용량 충·방전과 누설이라는 정적 CMOS의 핵심 물리가 모두 들어 있다.[1,2]

<figure markdown="span">
  ![위쪽 pMOS와 아래쪽 nMOS의 게이트를 입력 A에, 두 드레인을 출력 Q에 연결한 CMOS inverter 회로도](images/cmos-inverter.svg)
  <figcaption markdown="1">
    그림 1. CMOS inverter의 상보 연결. 위쪽 pMOS는 $V_{DD}$에서 출력을 충전하고 아래쪽 nMOS는 $V_{SS}$로 출력을 방전하며, 공통 입력 $A$에 대해 출력 $Q=\overline{A}$를 만든다.
    출처: Inductiveload, “CMOS Inverter,” Wikimedia Commons (2006),
    <a href="https://commons.wikimedia.org/wiki/File:CMOS_Inverter.svg">public domain</a>, 수정 없음.[10]
  </figcaption>
</figure>

### (1) 정적 논리 상태

이상적인 스위치 관점의 두 끝 상태는 다음과 같다. 전환 구간에서는 두 소자가 동시에 부분적으로 켜지므로 단순한 ON/OFF 표만으로 VTC나 전력을 계산할 수 없다.[1,2]

| 입력 | pMOS | nMOS | 출력의 정상 상태 | 이상적인 전원–접지 직류 경로 |
| --- | --- | --- | --- | --- |
| $V_\mathrm{in}=0$ | 켜짐 | 꺼짐 | $V_\mathrm{out}=V_{OH}\simeq V_{DD}$ | 없음 |
| $V_\mathrm{in}=V_{DD}$ | 꺼짐 | 켜짐 | $V_\mathrm{out}=V_{OL}\simeq0$ | 없음 |
| 전환 구간 | 부분적으로 켜짐 | 부분적으로 켜짐 | 부하와 두 소자의 전류 평형으로 결정 | 일시적으로 존재 |

입력 단자는 이상적으로 전도 전류를 받지 않지만 게이트 정전용량을 충·방전해야 한다. 출력도 전압원 자체가 아니라 유한한 출력 저항을 가진 MOSFET가 부하 정전용량을 충·방전하여 논리 레벨을 만든다. 따라서 정적 입력 전류가 작다는 사실과 동적 구동 비용이 작다는 주장은 서로 다르다.[1,2]

### (2) VTC와 전류 평형

직류 VTC는 $V_\mathrm{in}$을 $0$에서 $V_{DD}$까지 천천히 주사할 때의 $V_\mathrm{out}(V_\mathrm{in})$이다. 출력 노드에 외부 직류 부하가 없으면 정상 상태의 Kirchhoff current law는

$$
I_p(V_\mathrm{in},V_\mathrm{out})
=
I_n(V_\mathrm{in},V_\mathrm{out})
$$

이다. 낮은 입력에서는 pMOS가 linear region, nMOS가 cutoff에 가깝고, 높은 입력에서는 그 반대이다. 중간 전환 구간에서는 두 소자의 동작 영역이 입력과 출력에 따라 바뀌며, 양쪽이 saturation region에 놓이는 구간에서 큰 음의 전압 이득이 나타난다.[1,2]

작은 신호 관점에서 출력 노드의 증분 전류를 선형화하면 전환 구간의 이득은 대략

$$
A_v
=
\frac{dV_\mathrm{out}}{dV_\mathrm{in}}
\simeq
-\frac{g_{mn}+g_{mp}}{g_{dsn}+g_{dsp}}
$$

로 쓸 수 있다. $g_m$은 입력 전압이 드레인 전류를 바꾸는 정도이고 $g_{ds}$는 유한한 출력 conductance이다. 큰 $g_m/g_{ds}$는 가파른 VTC에 유리하지만, 이 식은 각 소자의 바디 효과, 기생 저항과 출력에 연결된 다른 직류 경로를 생략한 국소 선형화이다.[1,2]

## 2. Logic threshold와 noise margin

논리 회로에서 중요한 값은 MOSFET 하나의 threshold voltage $V_T$만이 아니다. Inverter switching point $V_M$, 입력 판정 경계 $V_{IL}$·$V_{IH}$, 출력 레벨 $V_{OL}$·$V_{OH}$가 함께 다음 단계가 잡음을 제거하고 논리값을 복원할 수 있는 범위를 정한다.[1,2]

### (1) 장채널 switching point 근사

$V_M$은 VTC와 $V_\mathrm{out}=V_\mathrm{in}$ 직선의 교점으로 정의한다. $V_\mathrm{in}=V_\mathrm{out}=V_M$에서 두 소자가 장채널 saturation region에 있고 channel-length modulation을 무시한다고 가정하자. 다음과 같이

$$
\beta_n=\mu_n C_\mathrm{ox}\frac{W_n}{L_n},
\qquad
\beta_p=\mu_p C_\mathrm{ox}\frac{W_p}{L_p}
$$

를 정의하면 전류 평형은

$$
\frac{\beta_n}{2}(V_M-V_{Tn})^2
=
\frac{\beta_p}{2}(V_{DD}-V_M-|V_{Tp}|)^2
$$

이고, 양의 overdrive 해는

$$
V_M
=
\frac{V_{Tn}+\sqrt{\beta_p/\beta_n}\,(V_{DD}-|V_{Tp}|)}
{1+\sqrt{\beta_p/\beta_n}}
$$

이다. $\beta_n=\beta_p$이고 $V_{Tn}=|V_{Tp}|$이면 $V_M=V_{DD}/2$가 된다. 정공 이동도가 일반적으로 전자 이동도보다 작으므로 같은 채널 길이에서 대칭에 가까운 구동력을 얻으려면 pMOS의 유효 폭을 더 크게 선택하는 경우가 많다.[1,2]

이 식은 설계 방향을 보여 주지만 현대 짧은 채널 소자의 정량식은 아니다. Velocity saturation과 이동도 저하가 강하면 포화 전류의 gate overdrive 의존성이 제곱보다 약해진다. Alpha-power law는 이를 $(V_{GS}-V_T)^\alpha$ 형태로 근사하지만, 실제 $V_M$과 VTC는 compact model을 사용한 전류 평형으로 구해야 한다.[3,4]

### (2) Unity-gain 경계와 noise margin

VTC에서 기울기가 $-1$인 낮은 쪽과 높은 쪽 입력을 각각 $V_{IL}$과 $V_{IH}$로 정의한다.

$$
\left.\frac{dV_\mathrm{out}}{dV_\mathrm{in}}\right|_{V_{IL}}
=
\left.\frac{dV_\mathrm{out}}{dV_\mathrm{in}}\right|_{V_{IH}}
=-1
$$

낮은 입력과 높은 입력에 허용되는 직류 잡음의 크기는

$$
NM_L=V_{IL}-V_{OL},
\qquad
NM_H=V_{OH}-V_{IH}
$$

로 정의한다. $V_M$만 $V_{DD}/2$에 맞추어도 두 noise margin이 자동으로 같아지는 것은 아니다. VTC의 전체 모양, 출력 conductance, 전원 전압, 부하와 process–voltage–temperature (PVT) 변동을 함께 확인해야 한다.[1,2]

## 3. 스위칭 동역학

정적 VTC는 최종 논리값을 정하지만 출력이 그 값에 도달하는 시간을 정하지 않는다. 출력 노드의 총 부하 정전용량 $C_L$에는 다음 단계의 게이트 정전용량, 현재 게이트의 drain junction·overlap 정전용량과 배선 정전용량이 포함된다. 이 성분들은 전압 의존적일 수 있으므로 하나의 상수 $C_L$은 1차 근사이다.[1,2]

### (1) 출력 노드의 과도 방정식

출력 노드의 전하 보존식은

$$
C_L(V_\mathrm{out})\frac{dV_\mathrm{out}}{dt}
=
I_p(V_\mathrm{in},V_\mathrm{out})
-
I_n(V_\mathrm{in},V_\mathrm{out})
$$

이다. 출력이 낮아질 때에는 nMOS 방전 전류가, 높아질 때에는 pMOS 충전 전류가 지배한다. 구동 소자는 전환 동안 saturation과 linear region을 지나므로 하나의 일정한 ON current나 저항으로 전체 파형을 정확히 표현할 수 없다.[1,2,4]

### (2) Propagation delay와 근사 모형

입력과 출력의 50% $V_{DD}$ 교차점을 기준으로, 출력이 high-to-low로 바뀌는 지연을 $t_{pHL}$, low-to-high로 바뀌는 지연을 $t_{pLH}$로 정의한다. 평균 propagation delay는

$$
t_p=\frac{t_{pHL}+t_{pLH}}{2}
$$

이다. 유효 저항 모형과 유효 전류 모형은 각각

$$
t_{pHL}\approx0.69R_{n,\mathrm{eq}}C_L,
\qquad
t_{pLH}\approx0.69R_{p,\mathrm{eq}}C_L,
$$

$$
t_{pHL}\sim\frac{C_LV_{DD}}{2I_{n,\mathrm{eff}}},
\qquad
t_{pLH}\sim\frac{C_LV_{DD}}{2I_{p,\mathrm{eff}}}
$$

와 같이 쓸 수 있다. 첫 식의 $0.69$는 단일 RC 지수 응답이 50%에 도달하는 시간이고, 둘째 식의 계수는 $I_\mathrm{eff}$의 정의에 의존한다. 따라서 이 식들은 scaling과 민감도 해석에는 유용하지만 서로 다른 라이브러리나 공정을 비교할 때에는 입력 slew, 출력 부하, 전원, 온도와 지연 추출 기준을 고정해야 한다.[1,2,4]

Fanout-of-4 (FO4) inverter delay는 동일한 inverter 네 개의 입력 정전용량을 구동하는 inverter의 지연으로, 공정과 회로 세대 사이의 대략적인 속도 정규화에 쓰인다. 그러나 실제 경로가 배선 저항·정전용량, diffusion capacitance 또는 복잡한 게이트에 지배되면 FO4 하나가 그 경로의 지연을 대표하지 못한다.[2,5]

## 4. 에너지와 전력

CMOS의 에너지 비용은 출력과 내부 노드의 충·방전, 입력 전환 중의 전원–접지 단락 전류, 그리고 정상 상태의 누설 전류로 나뉜다. 세 항은 전원 전압과 동작률에 대한 의존성이 다르므로 측정에서도 분리해 해석해야 한다.[1,2,6]

### (1) 정전용량 충·방전

이상적인 전압원 $V_{DD}$가 처음에 방전된 $C_L$을 $V_{DD}$까지 충전할 때 공급하는 에너지는

$$
E_\mathrm{supply}=C_LV_{DD}^2
$$

이다. 그중 $C_LV_{DD}^2/2$는 정전용량에 저장되고 나머지는 pMOS 경로에서 열로 소모된다. 이후 방전할 때 저장 에너지가 nMOS 경로에서 소모되므로 한 번의 완전한 $0\rightarrow1\rightarrow0$ 주기에서 회로가 소모하는 에너지는 $C_LV_{DD}^2$이다.[1,2]

한 클록 주기당 평균 $0\rightarrow1$ 전이 횟수를 activity factor $\alpha_{0\rightarrow1}$로 정의하면 switching power는

$$
P_\mathrm{sw}
=
\alpha_{0\rightarrow1}C_\mathrm{eff}V_{DD}^2f
$$

이다. 문헌에 따라 $\alpha$를 모든 toggle의 확률로 정의하고 $1/2$을 따로 붙이기도 하므로, 수치 비교에서는 activity convention을 반드시 명시해야 한다. $C_\mathrm{eff}$는 외부 부하뿐 아니라 실제로 전환하는 내부 노드와 배선의 등가 정전용량까지 포함한다.[1,2]

### (2) Short-circuit current와 leakage

입력이 유한한 시간에 전환하면 nMOS와 pMOS가 동시에 켜지는 구간이 생겨 $V_{DD}$에서 접지로 short-circuit current가 흐른다. 그 에너지는 입력 slew, 두 소자의 구동력, 출력 부하와 $V_{DD}-V_{Tn}-|V_{Tp}|$의 여유에 민감하다. 출력 부하가 커질수록 출력 전환은 느려지지만 short-circuit energy가 항상 같은 비율로 증가하는 것은 아니므로, 정전용량 전력에 고정된 백분율을 더하는 방식은 일반식이 아니다.[2,6]

총평균 전력을 1차적으로 분해하면

$$
P_\mathrm{total}
=
P_\mathrm{sw}+P_\mathrm{sc}+P_\mathrm{leak},
\qquad
P_\mathrm{leak}=V_{DD}I_\mathrm{leak}
$$

로 쓸 수 있다. $I_\mathrm{leak}$에는 입력 벡터에 따른 subthreshold leakage, gate tunneling과 역바이어스 접합 누설 등이 포함된다. 온도와 $V_T$ 변동에 매우 민감하므로 단일 트랜지스터의 $I_\mathrm{OFF}$만으로 큰 논리 블록의 대기 전력을 결정할 수 없다.[2,7]

## 5. 정적 CMOS logic network

Inverter를 여러 입력 논리로 확장할 때에는 출력에서 접지까지의 PDN이 출력이 0이어야 하는 입력 조합에서만 도통하도록 nMOS를 연결한다. PUN은 그 부울 조건의 보수에서 도통하는 pMOS dual network이다. 올바른 정적 CMOS 게이트에서는 정상 입력마다 PUN과 PDN 가운데 하나만 출력에 저저항 경로를 제공한다.[2,8,9]

### (1) PUN–PDN duality와 기본 게이트

nMOS network에서 직렬 연결은 논리 AND, 병렬 연결은 논리 OR의 도통 조건을 만든다. pMOS network는 입력이 낮을 때 켜지므로 PDN의 직렬과 병렬을 서로 바꾼 De Morgan dual로 구성한다.[2,8,9]

<figure markdown="span">
  ![두 pMOS가 병렬 pull-up network를 이루고 두 nMOS가 직렬 pull-down network를 이루는 2-input CMOS NAND 회로도](images/cmos-nand.svg)
  <figcaption markdown="1">
    그림 2. 2-input CMOS NAND의 transistor network. 입력 $A$와 $B$가 모두 높을 때만 직렬 nMOS PDN이 출력을 낮추며, 하나라도 낮으면 병렬 pMOS PUN 가운데 적어도 한 경로가 출력을 높인다.
    출처: Biezl, “Cmos nand,” Wikimedia Commons (2008),
    <a href="https://commons.wikimedia.org/wiki/File:Cmos_nand.svg">public domain</a>, 시각적 변경 없이 비시각 metadata만 제거.[11]
  </figcaption>
</figure>

| 게이트 | 출력 함수 | nMOS PDN | pMOS PUN | 트랜지스터 수 |
| --- | --- | --- | --- | --- |
| Inverter | $Y=\overline{A}$ | $A$ 한 개 | $A$ 한 개 | 2 |
| 2-input NAND | $Y=\overline{AB}$ | $A$, $B$ 직렬 | $A$, $B$ 병렬 | 4 |
| 2-input NOR | $Y=\overline{A+B}$ | $A$, $B$ 병렬 | $A$, $B$ 직렬 | 4 |

복합 게이트도 먼저 $Y=0$이 되는 조건을 PDN으로 구현한 뒤 dual PUN을 만들 수 있다. 다만 부울식이 같다는 사실은 지연과 에너지가 같다는 뜻이 아니다. 직렬 stack의 내부 노드, 입력 순서, 확산 영역 공유와 각 입력의 도착 시간이 과도 응답과 glitch energy를 바꾼다.[2,8]

### (2) Stack, sizing과 fan-in

직렬 트랜지스터 수가 늘면 등가 저항이 커지고 내부 노드 정전용량이 추가된다. 이를 보상하려고 폭을 키우면 구동 저항은 줄지만 입력과 확산 정전용량이 증가하여 앞 단계와 현재 단계의 에너지·지연을 다시 악화시킨다. 특히 NOR의 직렬 pMOS stack은 낮은 정공 이동도까지 겹치므로 큰 fan-in에서 불리할 수 있다.[2,8]

Fan-out은 현재 출력이 구동하는 다음 단계의 입력 부하를 나타내지만, 게이트 개수만으로 충분하지 않다. 각 수신 게이트의 크기, 배선과 branch가 실제 $C_L$을 정한다. 그러므로 논리 단계의 최적 크기는 한 게이트의 $R_\mathrm{eq}$ 최소화가 아니라 전체 경로의 effort와 부하 분배 문제이다. Standard cell에서 이러한 선택은 셀 높이, 금속 핀, 배선 혼잡도와도 결합되지만, 이는 CMOS 동작 원리와 구별되는 물리 구현 계층이다.[2,5,8]

## 6. 소자–회로 성능 연결

소자 성능을 회로 성능으로 옮길 때에는 “큰 $I_\mathrm{ON}$이면 빠르다”와 같은 단일 지표 대응을 피해야 한다. $I_\mathrm{ON}$이 커져도 $C_{gg}$, junction capacitance 또는 배선 부하가 함께 커지면 지연 개선이 줄어들 수 있고, 낮은 $V_T$는 구동 전류와 누설을 동시에 늘릴 수 있다. 짧은 채널의 DIBL, 유한한 output conductance와 변동성은 정적 VTC, 지연, 대기 전력에 서로 다른 방식으로 나타난다.[3,4,7]

전역적인 공정 corner는 nMOS와 pMOS의 평균 구동력을 함께 이동시키고, 국소 mismatch는 같은 셀 안의 두 소자를 서로 다르게 이동시킬 수 있다. 전자는 여러 corner의 VTC와 지연으로, 후자는 통계적 compact-model parameter를 사용한 Monte Carlo 분석으로 구분하는 것이 원칙이다. 평균 $V_M$이 목표값에 맞더라도 분포의 꼬리에서 noise margin이나 지연 규격이 실패할 수 있으므로 평균값과 worst-case 또는 수율 지표를 함께 보고해야 한다.[2,4]

| 소자·구조 지표 | 주로 연결되는 회로량 | 단순 대응이 실패하는 이유 |
| --- | --- | --- |
| $I_\mathrm{ON}$, $g_m$, 유효 구동 전류 | $t_{pHL}$, $t_{pLH}$, slew | $C_L$, 출력 전압에 따른 전류와 입력 slew가 함께 작용한다. |
| $I_\mathrm{OFF}$와 gate·junction leakage | 대기 전력 | 입력 벡터, stack effect, 온도와 회로 상태가 총누설을 바꾼다. |
| $C_{gg}$, overlap·junction capacitance | 동적 전력과 지연 | 구동력 향상을 위한 폭 증가가 정전용량도 늘린다. |
| $V_T$, DIBL, SS | $V_M$, noise margin, 누설, 저전압 동작 | nMOS/pMOS의 비대칭과 PVT 변동이 함께 작용한다. |
| 배선·접촉 저항과 정전용량 | 경로 지연과 에너지 | 트랜지스터 자체보다 interconnect가 지배할 수 있다. |

!!! info "[Measurement]"
    정적 특성은 지정한 $(V_{DD},T)$와 공정 corner에서 $V_\mathrm{in}$을 $0$부터 $V_{DD}$까지 직류 주사하여 VTC를 얻는다. $V_\mathrm{out}=V_\mathrm{in}$ 교점에서 $V_M$을 구하고, 수치 미분한 기울기가 $-1$인 두 점에서 $V_{IL}$과 $V_{IH}$를 추출한 뒤 $NM_L$과 $NM_H$를 계산한다. 과도 특성은 입력 slew와 $C_L$을 명시하고 입력·출력의 $0.5V_{DD}$ 교차점으로 $t_{pHL}$과 $t_{pLH}$를 구한다. 전력은 충분한 주기 동안 전원 전류를 적분하여

    $$
    E_\mathrm{cycle}
    =
    \int_{t_0}^{t_0+T}V_{DD}I_{DD}(t)\,dt,
    \qquad
    P_\mathrm{avg}=\frac{E_\mathrm{cycle}}{T}
    $$

    로 보고한다. 입력 벡터, activity convention, 부하, 배선 포함 여부, 초기 상태와 PVT 조건을 함께 기록해야 VTC·지연·전력의 비교가 재현 가능하다.[1,2]

!!! warning "[Interpretation Caveat]"
    장채널 square-law와 단일 $R_\mathrm{eq}C_L$ 모형은 물리적 경향과 손계산을 위한 기준이다. FinFET·GAA를 포함한 현대 CMOS의 정량 예측에는 검증된 compact model, 기생 성분 추출, 입력 slew와 배선을 포함한 회로 시뮬레이션이 필요하다. 소자 단면의 향상이 곧바로 표준 셀 면적이나 시스템 전력 개선을 뜻하지 않으며, 그 변환에는 셀 구조·배선·전원망과 workload가 개입한다.[3–5]

## 7. 요약

- 정적 CMOS inverter는 상보적인 pMOS PUN과 nMOS PDN으로 rail-to-rail 출력을 만들며, 이상적인 끝 상태에서는 전원–접지 직류 경로가 없다.
- VTC는 $I_p=I_n$ 전류 평형으로 정해지고, $V_M$과 $V_{IL}$·$V_{IH}$·$V_{OL}$·$V_{OH}$가 logic threshold와 noise margin을 결정한다.
- 지연은 구동 전류만이 아니라 출력·입력·배선 정전용량과 입력 slew에 의존한다. $RC$식과 유효 전류식은 조건을 고정한 1차 근사이다.
- Switching power는 activity, $C_\mathrm{eff}$, $V_{DD}^2$과 주파수에 비례하며, short-circuit power와 입력 벡터·온도 의존적인 leakage power를 별도로 고려해야 한다.
- NAND와 NOR는 PDN의 도통 조건과 그 dual PUN으로 구성되지만, transistor stack, sizing, 내부 노드와 배선 때문에 부울식만으로 지연·에너지를 판단할 수 없다.
- $I_\mathrm{ON}$, $I_\mathrm{OFF}$, $C_{gg}$, $V_T$와 SCE는 회로 지표의 입력일 뿐이다. 현대 CMOS의 정량 비교에는 compact model, 기생 성분과 PVT 조건을 포함한 VTC·과도·전력 분석이 필요하다.

## 8. 참고문헌

1. J. A. del Alamo, “Lecture 14: The CMOS Inverter,” MIT OpenCourseWare 6.012 *Microelectronic Devices and Circuits* (2005). [강의 자료](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2005/resources/lec14/).
2. N. H. E. Weste and D. M. Harris, *CMOS VLSI Design: A Circuits and Systems Perspective*, 4th ed., Addison-Wesley (2011). [저자 제공 강의 자료](https://pages.hmc.edu/harris/cmosvlsi/4e/lect/index.html).
3. T. Sakurai and A. R. Newton, “Alpha-Power Law MOSFET Model and its Applications to CMOS Inverter Delay and Other Formulas,” *IEEE Journal of Solid-State Circuits* **25**, 584–594 (1990). [DOI: 10.1109/4.52187](https://doi.org/10.1109/4.52187).
4. Y. Taur and T. H. Ning, *Fundamentals of Modern VLSI Devices*, 2nd ed., Cambridge University Press (2009). [DOI: 10.1017/CBO9781139195065](https://doi.org/10.1017/CBO9781139195065).
5. D. Harris, R. Ho, G.-Y. Wei, and M. Horowitz, “The Fanout-of-4 Inverter Delay Metric” (1997). [저자 제공 원고](https://pages.hmc.edu/harris/research/FO4.pdf).
6. H. J. M. Veendrick, “Short-Circuit Dissipation of Static CMOS Circuitry and Its Impact on the Design of Buffer Circuits,” *IEEE Journal of Solid-State Circuits* **19**, 468–473 (1984). [DOI: 10.1109/JSSC.1984.1052168](https://doi.org/10.1109/JSSC.1984.1052168).
7. C. Hu, *Modern Semiconductor Devices for Integrated Circuits*, Pearson (2010). [저자 제공 PDF](https://www.chu.berkeley.edu/wp-content/uploads/2020/01/Chenming-Hu_ch7.pdf).
8. A. Agarwal and J. H. Lang, “Lecture 3: CMOS Gates,” MIT OpenCourseWare 6.884 *Complex Digital Systems* (2005). [강의 자료](https://ocw.mit.edu/courses/6-884-complex-digital-systems-spring-2005/resources/l03_cmos_gates/).
9. A. M. Niknejad, “Lecture 18: CMOS Logic,” EECS 105, University of California, Berkeley (2004). [강의 자료](https://msdnaa.eecs.berkeley.edu/~ee105/sp04/handouts/lectures/Lecture18.pdf).
10. Inductiveload, “CMOS Inverter,” Wikimedia Commons (2006), public domain. [파일 설명과 라이선스](https://commons.wikimedia.org/wiki/File:CMOS_Inverter.svg).
11. Biezl, “Cmos nand,” Wikimedia Commons (2008), public domain. [파일 설명과 라이선스](https://commons.wikimedia.org/wiki/File:Cmos_nand.svg).
