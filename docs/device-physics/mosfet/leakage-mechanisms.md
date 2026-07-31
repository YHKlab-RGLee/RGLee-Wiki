---
title: "(1) MOSFET: Leakage Current"
description: MOSFET leakage current를 terminal current와 physical path별로 분해하고 measurement signature와 metric으로 설명
status: verified
last_verified: 2026-07-31
---

# (1) MOSFET: Leakage Current

metal-oxide-semiconductor field-effect transistor (MOSFET)의 leakage current는 하나의 physical mechanism이 아니다. 같은 off-state drain current에도 thermionic subthreshold transport, gate-dielectric tunneling, reverse-biased junction leakage, gate-induced drain leakage, punch-through가 동시에 기여할 수 있다.[1–3] 소자가 극단적으로 짧아지거나 전기적 stress를 받으면 direct source-to-drain tunneling과 stress-induced leakage current까지 추가된다.[5,8,9,19–21]

따라서 “어느 leakage가 큰가?”를 답하려면 먼저 **어느 terminal에서**, **어떤 bias와 temperature에서**, **어떤 geometry normalization으로** 측정했는지를 선언해야 한다. 그 다음 terminal current, bias dependence, temperature dependence와 area·perimeter·width·length scaling을 함께 사용해 physical path를 분리한다.[1,3,4]

<figure markdown="span">
  ![planar n-channel MOSFET의 주요 leakage-current component: gate leakage, subthreshold leakage, hot-carrier injection, GIDL, junction leakage와 punch-through](images/leakage-current-overview.png)
  <figcaption>
    그림 1. planar n-channel MOSFET의 주요 leakage-current component map. 이 그림은 gate leakage, subthreshold leakage, hot-carrier injection, GIDL, junction leakage와 punch-through를 한 소자에 표시한다. GISL, gate-current terminal partition, TAT/SILC와 direct source-to-drain tunneling은 본문의 확장 taxonomy에서 별도로 다룬다.
    출처: E. Shauly, “CMOS Leakage and Power Reduction in Transistors and Circuits: Process and Layout Considerations,” <i>Journal of Low Power Electronics and Applications</i> <b>2</b>, Figure 2 (2012),
    <a href="https://doi.org/10.3390/jlpea2010001">DOI</a>,
    <a href="https://creativecommons.org/licenses/by/3.0/">CC BY 3.0</a>, 수정 없음.[2]
  </figcaption>
</figure>

## 1. Scope and Conventions

기본 대상은 enhancement-mode planar bulk n-channel MOSFET (nMOS)이다. 별도 표기가 없으면 direct current (DC), $V_S=V_B=0$을 가정한다. 전압은 $V_{XY}=V_X-V_Y$로 정의하고, terminal current는 방향 혼동을 피하기 위해 부호를 포함한 $I_G$, $I_D$, $I_S$, $I_B$ 또는 크기 $|I_X|$로 표시한다.

- off-state current ($I_\mathrm{OFF}$)는 미리 선언한 off-state bias에서 읽은 $|I_D|$이다. 흔한 조건은 $V_G=0$, $V_D=V_\mathrm{DD}$이지만 보편적 정의는 아니므로 supply voltage와 body bias를 함께 적는다.
- threshold voltage ($V_T$)는 모든 비교 곡선에서 같은 extraction method를 사용한다. 이 문서의 기본 규약은 지정한 reference current에 대응하는 gate voltage를 읽는 constant-current method이다.[3,5,6]
- 전류는 physical path에 따라 effective gate width $W$, gate area $A_G$, junction bottom area $A_\mathrm{junc}$, isolation-edge perimeter $P_\mathrm{iso}$ 또는 gate-edge width로 normalize한다. 서로 다른 normalization을 직접 비교하지 않는다.[3,4]
- “dominant”는 정해진 bias·temperature·geometry에서 가장 큰 measured contribution이라는 뜻이다. process node 전체에 영구적으로 붙는 mechanism label이 아니다.[1,2]

!!! warning "[Reproducibility]"
    $I_\mathrm{OFF}$ 한 값만으로는 결과를 재현할 수 없다. $V_G$, $V_D$, $V_S$, $V_B$, temperature, device width·length, junction geometry, normalization, sweep direction, delay와 integration time을 함께 기록한다.[14,15]

## 2. Component Map and Terminal Accounting

### (1) Path Taxonomy

아래 표는 전통적인 short-channel MOSFET leakage 분류를 terminal-level subcomponent까지 펼치고, defect, source-side symmetry와 ultrascaled-device extension을 더한 점검용 taxonomy다.[1,2,4]

| Physical Region | Current Component | Representative Path | Strong Control Variable | Primary Terminal Signature |
| --- | --- | --- | --- | --- |
| surface channel | subthreshold leakage | source → inversion/depletion surface → drain | $V_G$, $V_D$, $T$, $L$ | $I_D\approx-I_S$ |
| deep body | punch-through | source → subsurface saddle point → drain | $V_D$, $V_B$, $L$, body doping | $I_D\approx-I_S$ |
| channel barrier | direct source-to-drain tunneling | source wavefunction → channel barrier → drain | barrier length·height, $V_G$, $V_D$ | weak-$T$ channel current |
| gate dielectric over channel | gate-to-channel tunneling | gate → channel, then partition to source and drain | oxide field, EOT, gate area | $I_G$, $I_{gcs}$, $I_{gcd}$ |
| gate dielectric over body | gate-to-body tunneling | gate → substrate/body | oxide field, accumulation/inversion | $I_G$ paired with $I_B$ |
| source/drain overlap | overlap direct tunneling | gate → source/drain extension | overlap field·length | $I_{gs}$ or $I_{gd}$ |
| drain-side gate edge | edge direct tunneling (EDT) | gate edge → drain extension | $V_{GD}$, oxide thickness, edge geometry | $I_G$ paired with $I_D$ |
| gate dielectric defects | trap-assisted tunneling (TAT) | electrode → oxide trap(s) → electrode | trap population, field, $T$ | excess $I_G$ |
| stressed gate dielectric | stress-induced leakage current (SILC) | stress-generated trap-assisted path | stress history, injected charge | post-stress low-field $I_G$ |
| drain–body junction | diffusion·generation | neutral region/depletion region → junction | reverse bias, $T$, area·perimeter | $I_D$ paired with $I_B$ |
| drain–body high-field junction | BTBT·TAT·avalanche | valence band/trap → conduction band | local junction field, traps | $I_D$ and $I_B$ |
| gate–drain overlap | gate-induced drain leakage (GIDL) | drain-edge BTBT/TAT | low $V_G$, high $V_D$, $V_B$ | $I_D$ paired with $I_B$ |
| gate–source overlap | gate-induced source leakage (GISL) | source-edge BTBT/TAT | low $V_G$, high $V_S$, $V_B$ | $I_S$ paired with $I_B$ |
| drain-side high field | hot-carrier injection (HCI) | channel carrier → oxide/gate or substrate | $V_G$, $V_D$, lateral field | $I_G$ and/or $I_B$ |

“junction leakage”와 “gate leakage”는 각각 하나의 기작이 아니라 위치 또는 terminal로 묶은 상위 범주다. 예를 들어 reverse-biased junction current에는 neutral-region diffusion, depletion-region generation, junction band-to-band tunneling (BTBT), trap-assisted tunneling (TAT), isolation-edge current가 포함될 수 있다. gate current도 gate-to-body, gate-to-channel, overlap와 edge component로 분할된다.[1,3,4]

### (2) Measured Terminal Current Is Not a Unique Mechanism

steady-state 네 단자 측정에서는 Kirchhoff’s current law (KCL)에 따라

$$
I_G+I_D+I_S+I_B\approx 0
$$

이어야 한다. 그러나 이 식은 current conservation check이지 mechanism separation equation은 아니다. 예를 들어 drain ammeter가 읽는 $I_D$에는 channel current, drain-side gate-tunneling partition, drain-junction current와 GIDL이 모두 들어갈 수 있다.[1,4,7]

compact model의 gate-current accounting을 따르면

$$
I_G=I_{gb}+I_{gc}+I_{gs}+I_{gd},
\qquad
I_{gc}=I_{gcs}+I_{gcd}
$$

로 쓸 수 있다. $I_{gb}$는 gate-to-body, $I_{gc}$는 gate-to-channel, $I_{gs}$와 $I_{gd}$는 source·drain overlap component이고, channel에 주입된 $I_{gc}$는 $I_{gcs}$와 $I_{gcd}$로 source와 drain에 partition된다. 실제 계측기의 terminal current는 이 component들의 부호 있는 합이므로 $|I_G|$와 $|I_D|$를 단순히 더하면 double counting이 생길 수 있다.[1,4,7]

!!! warning "[Interpretation Caveat]"
    physical mechanism, geometrical path와 measured terminal current를 같은 이름으로 쓰지 않는다. “$I_D$가 증가했다”는 관측이고, “GIDL의 BTBT component가 증가했다”는 추가 증거가 필요한 해석이다.[1,3]

## 3. Channel and Bulk Paths

### (1) Thermionic Subthreshold Leakage

subthreshold leakage는 $V_G<V_T$에서 source carrier가 유한한 source–channel energy barrier를 넘어 drain으로 이동해 생긴다. weak inversion의 surface carrier concentration은 gate voltage에 지수적으로 의존하며, long-channel limit에서는 diffusion-dominated transport로 설명할 수 있다. short-channel device에서는 drain-induced barrier lowering (DIBL)이 source-side barrier를 낮춰 같은 $V_G$에서 current를 증가시킨다.[1,3,5]

<figure markdown="span">
  ![gate가 꺼진 n-channel MOSFET에서 drain으로 흐르는 subthreshold leakage](images/fet-subthreshold-leakage.png)
  <figcaption>
    그림 2. $V_G=0$인 n-channel MOSFET의 대표적인 subthreshold leakage path.
    출처: Fadeaway919, “FET subthreshold leakage,” Wikimedia Commons,
    <a href="https://commons.wikimedia.org/wiki/File:FET_subthreshold_leakage.png">CC BY-SA 3.0</a>, 수정 없음.[22]
  </figcaption>
</figure>

weak inversion의 대표 근사식은

$$
I_\mathrm{sub}\approx
I_0\frac{W}{L}
\exp\left(\frac{V_{GS}-V_T+\eta_DV_{DS}}{nU_T}\right)
\left[1-\exp\left(-\frac{V_{DS}}{U_T}\right)\right]
$$

이다. $U_T=kT/q$는 thermal voltage, $n$은 subthreshold slope factor, $\eta_D$는 drain coupling coefficient이다. 이 식은 model-dependent prefactor $I_0$ 때문에 absolute-current universal law가 아니라 $V_G$, $V_D$와 $T$에 대한 민감도를 보여주는 compact approximation으로 사용한다.[1,3]

subthreshold swing (SS)은

$$
\mathrm{SS}
=\left(\frac{d\log_{10}|I_D|}{dV_G}\right)^{-1}
=\ln(10)\,n\frac{kT}{q}
$$

로 정의한다. $n=1$인 thermionic limit은 300 K에서 약 $59.6\ \mathrm{mV/dec}$이다. 실제 bulk MOSFET에서는 depletion capacitance와 interface-trap capacitance 때문에 일반적으로 $n>1$이다.[1,3,5]

!!! info "[Measurement]"
    낮은 $V_D$와 실제 off-state 조건의 높은 $V_D$에서 semilog $I_D$–$V_G$를 측정한다. 같은 sweep에서 $I_G$와 $I_B$를 동시에 읽어 current floor가 gate 또는 junction path에 의해 제한되는지 확인한다.[1,4]

!!! abstract "[Metric]"
    지정한 current window를 regression하여 SS를 구하고 window·$T$·$V_D$를 기록한다. DIBL은 같은 $V_T$ extraction convention으로 얻은 낮은·높은 $V_D$ 곡선의 horizontal shift로 계산한다. $I_\mathrm{OFF}/W$에는 off-state bias를 붙인다.[3,5,6]

### (2) Punch-Through and Subsurface Leakage

punch-through는 channel이 짧거나 body doping이 낮을 때 source와 drain depletion region이 deep body에서 강하게 결합해 subsurface potential saddle point를 낮추는 현상이다. gate가 surface를 꺼도 source carrier가 deep-body path를 통해 drain에 도달할 수 있다. DIBL과 같은 short-channel electrostatics에 연결되지만, surface subthreshold current와 지배 경로가 다를 수 있다.[1,2,17,18]

!!! info "[Measurement]"
    $V_G$를 off bias에 고정하고 여러 channel length에서 $I_D$–$V_D$를 측정한다. $V_B$와 $T$도 바꾸고 $I_G$, $I_B$를 동시에 읽어 GIDL과 junction breakdown을 배제한다.[1,17,18]

!!! abstract "[Metric]"
    punch-through voltage ($V_\mathrm{PT}$)는 지정한 width-normalized reference current에 도달하는 $V_D$로 정의한다. off-state output conductance $g_{ds,\mathrm{off}}=\partial I_D/\partial V_D$도 보조 metric이다. reference current, $V_G$, $V_B$, $T$와 $L$을 함께 보고한다.[17,18]

### (3) Direct Source-to-Drain Tunneling

direct source-to-drain tunneling (DSDT 또는 S/D tunneling)은 carrier가 channel barrier를 열적으로 넘지 않고 양자역학적으로 관통하는 path다. conventional planar bulk MOSFET의 일반적인 leakage floor로 가정해서는 안 되지만, barrier가 매우 짧은 ultrascaled FDSOI, double-gate SOI, FinFET과 유사 구조에서는 thermionic subthreshold current와 별도로 고려해야 한다.[5,19–21]

!!! warning "[Interpretation Caveat]"
    낮은 온도에서 subthreshold current의 temperature dependence가 약해졌다는 사실만으로 DSDT를 확정하지 않는다. contact, series resistance, trap-assisted path와 instrument floor를 배제하고, barrier-length scaling 또는 quantum-transport simulation과 교차검증한다.[19–21]

## 4. Gate-Dielectric Paths

### (1) Direct and Fowler–Nordheim Tunneling

gate-dielectric leakage는 carrier가 finite dielectric barrier를 통과해 생긴다. 얇은 dielectric의 trapezoidal barrier에서는 direct tunneling (DT)이, 충분히 높은 dielectric field에서 triangular barrier에 가까워지면 Fowler–Nordheim (FN) tunneling이 나타날 수 있다. high-$k$ stack에서는 equivalent oxide thickness (EOT)만 같아도 physical thickness와 band offset이 다르므로 single-layer SiO$_2$ 식을 그대로 적용할 수 없다.[1,3,4]

일차원 Wentzel–Kramers–Brillouin approximation (WKB)의 transmission probability는

$$
T(E)\approx
\exp\left[
-\frac{2}{\hbar}
\int_{x_1}^{x_2}
\sqrt{2m_\mathrm{ox}^{*}\left(U(x)-E\right)}\,dx
\right]
$$

이다. $m_\mathrm{ox}^{*}$는 dielectric effective mass, $U(x)$는 barrier-energy profile, $x_1$과 $x_2$는 classical turning point다. 이 식은 thickness와 barrier shape에 대한 지수 민감도를 보여주지만, quantitative current에는 electrode density of states, band offset, image-force lowering와 multilayer stack을 포함해야 한다.[3,4]

### (2) Gate-Current Partition and Edge Direct Tunneling

gate-to-channel current $I_{gc}$는 channel에서 source와 drain 쪽으로 $I_{gcs}$와 $I_{gcd}$로 나뉜다. gate-to-body $I_{gb}$와 source·drain overlap current $I_{gs}$, $I_{gd}$는 별도 path다. 따라서 $I_G$–$V_G$ 하나만으로 gate dielectric의 위치별 current density를 복원할 수 없고, 네 terminal current와 geometry split이 필요하다.[1,4,7]

edge direct tunneling (EDT)은 off-state의 ultrathin-oxide MOSFET에서 gate edge와 drain extension 사이로 흐르는 gate-to-drain tunneling이다. gate-to-substrate area tunneling, junction BTBT와 conventional GIDL이 공유하는 terminal current에 섞일 수 있으며, width scaling과 overlap geometry dependence로 분리하는 것이 유용하다.[1,7]

!!! info "[Measurement]"
    source와 drain을 같은 전위로 묶어 lateral field를 줄인 $I_G$–$V_G$ 측정과 실제 off-state의 비대칭 bias 측정을 비교한다. $I_S$, $I_D$, $I_B$를 동시에 읽고 gate area와 overlap length가 다른 device split을 사용한다.[4,7]

!!! abstract "[Metric]"
    gate-area component는 $J_G=|I_G|/A_G$, overlap·edge component는 current/$W$로 보고한다. dielectric stack, physical thickness, EOT, voltage polarity와 $T$를 병기한다.[3,4,7]

### (3) Trap-Assisted Tunneling and Stress-Induced Leakage Current

trap-assisted tunneling (TAT)은 carrier가 dielectric defect state를 경유해 barrier를 통과하는 transport다. stress-induced leakage current (SILC)는 high-field electrical stress 뒤 low-field gate leakage가 증가한 **degradation signature**이며, fresh-device의 intrinsic direct tunneling과 같은 항으로 취급하면 안 된다. 여러 SILC model은 stress로 생성된 trap을 통한 one-step 또는 multi-step inelastic TAT로 이 증가분을 설명한다.[8,9]

SILC 확인에는 같은 소자의 pre-stress와 post-stress $I_G$–$V_G$가 필요하다. stress voltage, stress time, injected charge 또는 fluence, recovery delay와 sensing field를 기록하고, 새 소자의 process variation과 구분한다.[8,9]

!!! warning "[Interpretation Caveat]"
    TAT는 GIDL 영역의 interface/bulk trap, reverse junction의 depletion-region trap, gate dielectric trap에 모두 등장할 수 있다. “TAT”라는 transport label만으로 defect location이 정해지지 않는다.[4,8,12]

### (4) Hot-Carrier Injection

hot-carrier injection (HCI)은 drain-side lateral field에서 에너지를 얻은 carrier가 gate dielectric으로 주입되거나 impact ionization을 일으켜 gate/body current와 장기적 parameter shift를 만드는 high-field phenomenon이다. 전통적인 leakage taxonomy에는 포함되지만, $V_G=0$의 정상 off-state에서 항상 존재하는 baseline component로 간주해서는 안 된다. on-state, transition 또는 stress bias에서 별도로 평가한다.[1,2,4]

## 5. Junction, Overlap, and Isolation-Edge Paths

### (1) Reverse-Biased Junction Diffusion and Generation

off-state drain–body와 source–body pn junction에는 reverse bias가 걸린다. 낮거나 중간 field에서는 neutral-region minority-carrier diffusion과 depletion-region Shockley–Read–Hall generation이 기여한다. isolation edge와 gate edge는 bulk bottom area와 defect density·stress·electric field가 달라 별도 perimeter component를 가질 수 있다.[1,3,4,10,16]

geometry split의 first-order decomposition은

$$
|I_\mathrm{junc}|
\approx
J_AA_\mathrm{bottom}
+J_\mathrm{iso}P_\mathrm{iso}
+J_\mathrm{gate}W_\mathrm{gate-edge}
$$

로 쓸 수 있다. $J_A$는 junction-bottom area current density, $J_\mathrm{iso}$는 isolation-edge line current, $J_\mathrm{gate}$는 gate-edge line current다. 이는 단일 mechanism의 지배 방정식이 아니라 spatial component를 회귀하기 위한 experimental model이다.[4,10]

### (2) Junction BTBT, TAT, and Avalanche

highly doped 또는 고전계 reverse junction에서는 direct BTBT와 trap-assisted tunneling이 증가할 수 있다. 더 높은 bias에서 impact-ionization avalanche multiplication이 시작되면 pre-breakdown leakage와 breakdown regime을 분리해야 한다. BTBT, TAT와 avalanche는 모두 reverse current를 키우지만 field·temperature dependence와 발생 위치가 같지 않다.[1,3,10,12]

!!! info "[Measurement]"
    독립 drain–body diode structure에서 reverse $I$–$V$와 $T$ dependence를 먼저 측정한다. bottom area, STI perimeter와 gate-edge length가 독립적으로 변하는 구조를 함께 회귀하고, transistor에서는 channel과 overlap field를 최소화한 bias와 비교한다.[4,10]

!!! abstract "[Metric]"
    $J_A$, $J_\mathrm{iso}$와 $J_\mathrm{gate}$를 geometry regression으로 추출하고, Arrhenius plot의 apparent activation energy를 bias별로 보고한다. activation energy 하나만으로 diffusion, generation 또는 tunneling을 확정하지 않는다.[3,10]

### (3) GIDL and GISL

gate-induced drain leakage (GIDL)는 nMOS의 낮거나 음의 gate voltage와 높은 drain voltage가 gate–drain overlap 부근의 band bending과 local electric field를 키울 때 나타난다. high-field에서는 direct BTBT가 중요하고, trap이 있으면 lower-field 영역에 TAT가 더해질 수 있다. gate-induced source leakage (GISL)는 source-side bias를 반전한 대응 component이며, asymmetric source/drain structure에서는 두 current가 같다고 가정할 수 없다.[1,4,11–13]

direct BTBT의 field dependence는 단순화하면

$$
J_\mathrm{BTBT}\propto F^2\exp\left(-\frac{B}{F}\right)
$$

로 나타낼 수 있다. $F$는 local electric field, $B$는 bandgap과 effective mass 등에 의존하는 coefficient다. 외부 단자전압을 $F$와 동일시하면 doping gradient, overlap geometry와 field crowding을 잃으므로 정성적 경향 또는 calibrated field model에만 사용한다.[3,11,12]

!!! info "[Measurement]"
    GIDL은 $V_S=V_B=0$, $V_D>0$에서 $V_G$를 낮추며 측정하고, GISL은 drain/source 역할을 바꾼 mirrored bias로 측정한다. $I_B$와 $I_G$를 함께 읽어 generated-hole current와 EDT/gate tunneling을 구분한다.[1,4,7]

!!! abstract "[Metric]"
    $I_\mathrm{GIDL}/W$와 $I_\mathrm{GISL}/W$를 $(V_G,V_D,V_S,V_B,T)$와 함께 보고한다. onset voltage 또는 field-proxy slope를 쓸 때 reference current, proxy definition과 fitting window를 명시한다.[4,11,13]

!!! warning "[Interpretation Caveat]"
    drain-side low-$V_G$ current가 모두 GIDL은 아니다. $I_G$가 함께 증가하면 EDT 또는 overlap gate tunneling, $I_B$만 reverse-junction geometry를 따라 증가하면 junction component, 짧은 $L$에서만 $I_D\approx-I_S$로 증가하면 punch-through를 먼저 확인한다.[1,4,7]

## 6. Measurement Workflow for Component Separation

### (1) Four-Terminal Setup and Data Quality

gate, drain, source와 body에 source-measure unit (SMU)를 각각 연결해 네 terminal current를 동시에 읽는다. low-current measurement에서는 guarded triaxial cabling, shielded dark enclosure, clean high-insulation fixture, 충분한 settling time과 open-pad/background measurement가 중요하다. cable·fixture leakage와 shunt capacitance는 current floor와 settling error를 만들 수 있다.[14,15]

!!! info "[Measurement]"
    각 bias point에서 signed-current KCL residual $|I_G+I_D+I_S+I_B|$를 기록한다. residual이 target component보다 크면 mechanism fitting 전에 wiring, compliance, settling, autorange와 background subtraction을 점검한다.[4,14,15]

### (2) Bias Matrix

| Measurement | Bias Strategy | Most Sensitive Components | Required Cross-Check |
| --- | --- | --- | --- |
| semilog $I_D$–$V_G$ | low and high $V_D$ | subthreshold, DIBL, GIDL floor | simultaneous $I_G$, $I_B$ |
| off-state $I_D$–$V_D$ | fixed low $V_G$, several $L$ and $V_B$ | punch-through, GIDL, junction leakage | $I_S$, $I_B$, channel-length split |
| symmetric $I_G$–$V_G$ | $V_S=V_D$, controlled $V_B$ | gate area tunneling, $I_{gb}$/$I_{gc}$ | source/drain partition |
| asymmetric overlap sweep | vary $V_{GD}$ or $V_{GS}$ | $I_{gd}$/$I_{gs}$, EDT | overlap-length and width split |
| reverse diode $I$–$V$ | isolated S/B or D/B junction | diffusion, generation, BTBT, TAT, avalanche | area·perimeter split, $T$ sweep |
| mirrored edge sweep | swap source and drain bias | GIDL versus GISL | layout/process symmetry |
| pre/post-stress $I_G$–$V_G$ | identical sensing sweep | SILC and dielectric TAT | fresh control device, recovery time |
| cryogenic-to-high-$T$ sweep | identical bias matrix | thermionic versus weak-$T$ path | instrument floor, contact effects |

### (3) Decision Sequence

1. low-$V_D$와 high-$V_D$ $I_D$–$V_G$에서 SS, DIBL과 current floor를 확인한다.
2. 같은 sweep의 $I_G$, $I_S$, $I_B$와 KCL residual로 terminal partition과 measurement integrity를 확인한다.
3. symmetric gate bias와 asymmetric overlap bias를 비교해 gate-area, channel-partition과 edge component를 분리한다.
4. 독립 junction structure와 area·isolation perimeter·gate-edge split으로 junction spatial component를 추출한다.
5. mirrored source/drain sweep으로 GIDL과 GISL, structural asymmetry를 확인한다.
6. channel length와 body bias split으로 punch-through를 확인하고, ultrascaled device에서만 DSDT model을 추가 검토한다.
7. 시간 변화 또는 hysteresis가 있으면 stress를 중단하고 fresh control과 pre/post-stress sequence로 SILC·trapping을 분리한다.[1,4,10,14,15]

!!! warning "[Interpretation Caveat]"
    curve shape 하나나 단일 activation energy만으로 mechanism을 확정하지 않는다. 최소한 terminal correlation, bias signature, temperature dependence와 geometry scaling 중 서로 독립적인 두 종류 이상의 evidence를 요구한다.[3,10,14]

## 7. Architecture and Model Boundaries

planar bulk, fully depleted silicon-on-insulator (FDSOI), FinFET과 gate-all-around (GAA) device는 body terminal의 접근성, gate perimeter, junction volume와 channel electrostatics가 다르다. 따라서 이 문서의 path taxonomy는 재사용할 수 있지만, 각 component의 terminal visibility와 normalization은 architecture에 맞게 바꿔야 한다. 특히 floating-body SOI에서는 body-generated charge가 terminal current로 즉시 드러나지 않을 수 있고, multi-gate device에서는 width definition과 gate-area normalization을 명시해야 한다.[2,4,20]

compact model component는 계측 가능한 terminal current와 일대일 대응하지 않는다. BSIM-BULK의 $I_{gb}$, $I_{gcs}$, $I_{gcd}$, $I_{gs}$, $I_{gd}$, GIDL/GISL과 junction subcomponents는 charge conservation과 circuit simulation을 위한 model partition이므로, parameter extraction에는 해당 model version, enabled options와 fitting hierarchy를 함께 기록한다.[1,4]

## 8. Summary

- $I_\mathrm{OFF}$는 하나의 mechanism이 아니라 channel, gate dielectric, junction, overlap edge와 bulk path의 signed terminal contribution이 섞인 결과다.
- channel-related leakage에는 thermionic subthreshold, DIBL-enhanced current, punch-through와 ultrascaled DSDT를 구분한다.
- gate leakage는 $I_{gb}$, $I_{gcs}$, $I_{gcd}$, $I_{gs}$, $I_{gd}$로 partition하고 EDT, dielectric TAT와 SILC를 별도 확인한다.
- junction leakage는 bottom-area, isolation-perimeter와 gate-edge component를 나누고 diffusion, generation, BTBT, TAT와 avalanche regime을 구분한다.
- GIDL과 GISL은 mirrored bias, $I_B$·$I_G$ correlation과 edge geometry로 분리한다.
- HCI와 SILC는 정상 off-state baseline과 구분해 operating/stress history를 기록한다.
- 네 terminal current, KCL residual, temperature sweep와 geometry split을 함께 사용해야 mechanism assignment가 가능하다.

## 9. References

1. K. Roy, S. Mukhopadhyay, and H. Mahmoodi-Meimand, “Leakage Current Mechanisms and Leakage Reduction Techniques in Deep-Submicrometer CMOS Circuits,” *Proceedings of the IEEE* **91**, 305–327 (2003). [DOI: 10.1109/JPROC.2002.808156](https://doi.org/10.1109/JPROC.2002.808156).
2. E. Shauly, “CMOS Leakage and Power Reduction in Transistors and Circuits: Process and Layout Considerations,” *Journal of Low Power Electronics and Applications* **2**, 1–29 (2012). [DOI: 10.3390/jlpea2010001](https://doi.org/10.3390/jlpea2010001).
3. C. Hu, *Modern Semiconductor Devices for Integrated Circuits*, Chapter 7, Pearson (2010). [저자 제공 PDF](https://www.chu.berkeley.edu/wp-content/uploads/2020/01/Chenming-Hu_ch7.pdf).
4. BSIM Group, *BSIM-BULK MOSFET Model: Technical Manual*, Version 107.2.1, University of California, Berkeley (2025). [공식 release](https://bsim.berkeley.edu/models/bsimbulk/) (접속일: 2026-07-31).
5. D. J. Frank et al., “Device Scaling Limits of Si MOSFETs and Their Application Dependencies,” *Proceedings of the IEEE* **89**, 259–288 (2001). [DOI: 10.1109/5.915374](https://doi.org/10.1109/5.915374).
6. A. Ortiz-Conde et al., “Revisiting MOSFET Threshold Voltage Extraction Methods,” *Microelectronics Reliability* **53**, 90–104 (2013). [DOI: 10.1016/j.microrel.2012.09.015](https://doi.org/10.1016/j.microrel.2012.09.015).
7. K. N. Yang et al., “Characterization and Modeling of Edge Direct Tunneling (EDT) Leakage in Ultrathin Gate Oxide MOSFETs,” *IEEE Transactions on Electron Devices* **48**, 1159–1164 (2001). [DOI: 10.1109/16.925242](https://doi.org/10.1109/16.925242).
8. L. Larcher, A. Paccagnella, and G. Ghidini, “A Model of the Stress Induced Leakage Current in Gate Oxides,” *IEEE Transactions on Electron Devices* **48**, 285–288 (2001). [DOI: 10.1109/16.902728](https://doi.org/10.1109/16.902728).
9. M. Ossaimee, K. Kirah, W. Fikry, A. Girgis, and O. A. Omar, “Simplified Quantitative Stress-Induced Leakage Current (SILC) Model for MOS Devices,” *Microelectronics Reliability* **46**, 287–292 (2006). [DOI: 10.1016/j.microrel.2005.07.007](https://doi.org/10.1016/j.microrel.2005.07.007).
10. D. K. Schroder, *Semiconductor Material and Device Characterization*, 3rd ed., Wiley (2006). [DOI: 10.1002/0471749095](https://doi.org/10.1002/0471749095).
11. L. Huang, P. T. Lai, J. P. Xu, and Y. C. Cheng, “Mechanism Analysis of Gate-Induced Drain Leakage in Off-State n-MOSFET,” *Microelectronics Reliability* **38**, 1425–1431 (1998). [DOI: 10.1016/S0026-2714(98)00044-4](https://doi.org/10.1016/S0026-2714(98)00044-4).
12. R. Inagaki, N. Sadachika, D. Navarro, M. Miura-Mattausch, and Y. Inoue, “A GIDL-Current Model for Advanced MOSFET Technologies without Binning,” *IPSJ Transactions on System LSI Design Methodology* **2**, 93–102 (2009). [DOI: 10.2197/ipsjtsldm.2.93](https://doi.org/10.2197/ipsjtsldm.2.93).
13. H.-F. Chen et al., “Investigation of the Characteristics of GIDL Current in 90 nm CMOS Technology,” *Chinese Physics* **15**, 645–648 (2006). [DOI: 10.1088/1009-1963/15/3/034](https://doi.org/10.1088/1009-1963/15/3/034).
14. Keysight Technologies, “DC MOSFET Characterization at the Wafer Level,” Application Note 5990-5547EN (2019). [공식 문서](https://www.keysight.com/my/en/assets/7018-02489/application-notes/5990-5547.pdf).
15. Tektronix/Keithley, *Low Level Measurements Handbook*, 7th ed. [공식 PDF](https://download.tek.com/document/LowLevelHandbook_7Ed.pdf) (접속일: 2026-07-31).
16. S. M. Sze and K. K. Ng, *Physics of Semiconductor Devices*, 3rd ed., Wiley (2006). [DOI: 10.1002/0470068329](https://doi.org/10.1002/0470068329).
17. N. Kotani and S. Kawazu, “Computer Analysis of Punch-Through in MOSFETs,” *Solid-State Electronics* **22**, 63–70 (1979). [DOI: 10.1016/0038-1101(79)90172-2](https://doi.org/10.1016/0038-1101(79)90172-2).
18. J. J. Barnes, K. Shimohigashi, and R. W. Dutton, “Short-Channel MOSFET’s in the Punchthrough Current Mode,” *IEEE Transactions on Electron Devices* **26**, 446–453 (1979). [DOI: 10.1109/T-ED.1979.19447](https://doi.org/10.1109/T-ED.1979.19447).
19. H. Kawaura and T. Baba, “Direct Tunneling from Source to Drain in Nanometer-Scale Silicon Transistors,” *Japanese Journal of Applied Physics* **42**, 351–357 (2003). [DOI: 10.1143/JJAP.42.351](https://doi.org/10.1143/JJAP.42.351).
20. C. Medina-Bailon et al., “Multisubband Ensemble Monte Carlo Analysis of Tunneling Leakage Mechanisms in Ultrascaled FDSOI, DGSOI, and FinFET Devices,” *IEEE Transactions on Electron Devices* **66**, 1145–1152 (2019). [DOI: 10.1109/TED.2019.2890985](https://doi.org/10.1109/TED.2019.2890985).
21. C. Medina-Bailon et al., “Self-Consistent Enhanced S/D Tunneling Implementation in a 2D MS-EMC Nanodevice Simulator,” *Micromachines* **12**, 601 (2021). [DOI: 10.3390/mi12060601](https://doi.org/10.3390/mi12060601).
22. Fadeaway919, “FET Subthreshold Leakage,” Wikimedia Commons (2015), CC BY-SA 3.0. [파일 설명과 라이선스](https://commons.wikimedia.org/wiki/File:FET_subthreshold_leakage.png).
