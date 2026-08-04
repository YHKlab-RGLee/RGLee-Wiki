---
title: "(7) Memory Device: SRAM Advance"
description: SRAM의 공정 변동성·수율, 저전압 assist, 고급 bitcell 구조와 신뢰성 불량 분석을 beginner 관점에서 설명
status: verified
last_verified: 2026-08-04
---

# (7) Memory Device: SRAM Advance

[Memory Device: SRAM Basic](sram.md)에서는 conventional 6T bitcell의 hold·read·write, static noise margin (SNM)과 기본적인 $V_\mathrm{min}$을 설명했다. 이 글은 그 기준 셀을 실제 대규모 array와 advanced technology에 적용할 때 생기는 네 가지 질문을 다룬다.

1. 제조 편차가 셀마다 다를 때 모든 셀이 동작하는가?
2. 공급전압을 낮추면 어떤 margin이 먼저 무너지고, assist 회로는 무엇을 보완하는가?
3. 6T보다 transistor를 더 추가한 cell이 언제 유리하며, 면적 비용은 무엇인가?
4. 제작 직후의 불량, 방사선에 의한 일시 오류와 장시간 사용에 따른 열화를 어떻게 구별하는가?

여기서 **cell**은 1 bit를 저장하는 최소 반복 회로, **array**는 cell을 행과 열로 반복한 구조, **macro**는 array와 decoder·precharge·sense amplifier·입출력 회로를 포함한 메모리 블록이다. 이후의 margin과 failure는 별도 표기가 없으면 single-port SRAM을 기준으로 하며, 실제 수율은 cell뿐 아니라 bit line, sense amplifier, timing과 repair 정책까지 포함한다.[1–4]

## 1. PVT 변동과 수율

SRAM은 같은 회로를 매우 많이 반복하므로, 평균적인 셀 하나보다 드물게 약한 **tail cell**이 더 중요하다. 예를 들어 대부분의 셀이 정상이어도 한 셀이 read 중 뒤집히거나 write 시간 안에 상태를 바꾸지 못하면 전체 macro는 불량으로 판정될 수 있다. 따라서 이 절의 핵심은 “대표 셀의 성능”을 “분포의 끝부분과 array 수율”로 확장하는 것이다.

<figure markdown="span">
  ![행과 열로 반복된 memory cell array와 row decoder, sense amplifier, column decoder의 개념도](images/memory-cell-array.svg)
  <figcaption markdown="1">
    그림 1. Memory array를 행 선택, 열 선택, 판독 회로의 결합으로 보는 개념도. 작은 셀 배열을 여러 행·열로 반복하면 하나의 약한 셀도 전체 동작 결과에 영향을 줄 수 있다. 원본은 HandigeHarry, “DRAM,” Wikimedia Commons, public domain이며, 원본에서 array·decoder·sense-amplifier 관계를 설명하는 영역을 발췌해 사용했다. 이 글에서는 SRAM macro에도 공통인 개념도로만 사용하며, 특정 SRAM 제품의 실제 layout이나 회로 timing을 나타내지 않는다.[20]
  </figcaption>
</figure>

그림 1의 셀 하나를 실제 transistor의 집합으로 확대하면, 공정 편차는 $V_\mathrm{th}$, 구동 전류, 누설 전류, bit-line discharge 속도와 sense-amplifier 입력 차이를 동시에 바꾼다. 이 변화가 서로 같은 방향으로 움직이는지, 셀마다 독립적인지 구분하는 것이 PVT 분석의 시작이다.[2–7]

### (1) PVT와 공정 변동의 출처

**Process, voltage, temperature (PVT)**는 회로를 평가하는 세 조건이다. Process는 wafer·die 전체의 공정 model과 설계 parameter가 설계값에서 벗어나는 조건, voltage는 공급전압 $V_\mathrm{DD}$의 변화, temperature는 동작 온도이다. PVT corner는 이 세 축에서 선택한 대표 조합이며, 모든 가능한 칩을 직접 측정한다는 뜻이 아니라 검증할 경계 조건을 정한 것이다.[2,7]

공정 변동은 한 종류가 아니다. 같은 회로 안에서 독립적으로 나타나는 작은 차이와 die 전체에 함께 나타나는 큰 흐름이 서로 다른 통계 성분을 만든다.

| 변동 원인 | 소자에서 달라지는 것 | SRAM에서 보이는 결과 |
| --- | --- | --- |
| **Random dopant fluctuation (RDF)** | channel과 source·drain 주변의 불순물 원자 수와 위치 | $V_\mathrm{th}$와 구동 전류가 달라져 inverter의 균형과 writeability가 변한다. |
| **Line-edge roughness (LER)** | gate 또는 fin의 가장자리와 유효 길이·폭 | 유효 channel 치수, $V_\mathrm{th}$, subthreshold slope와 drive current가 달라진다. |
| **Work-function variation (WFV)** | metal gate의 유효 work function | 같은 구조의 transistor도 $V_\mathrm{th}$가 달라져 pull-up·pull-down·access strength의 상대비가 바뀐다. |
| **Fin 또는 nanosheet dimension variation** | fin 폭·높이, nanosheet 폭·두께와 gate length | 유효 channel 면적, 전류, capacitance와 cell 간 속도 차이가 변한다. |

RDF는 채널에 포함되는 원자 수가 작아질수록 개별 원자의 통계성이 커진다는 관점으로 이해할 수 있다. FinFET처럼 channel을 비교적 lightly doped로 만드는 구조에서는 RDF가 줄어들 수 있지만, LER·fin 치수·oxide와 metal-gate grain에 의한 WFV가 사라지는 것은 아니다. 어떤 항이 지배적인지는 technology, gate stack, geometry와 model calibration에 따라 달라지므로 “FinFET에서는 항상 WFV 하나가 지배한다”와 같이 일반화하면 안 된다.[5–8]

두 transistor의 문턱전압 차이를

$$
\Delta V_\mathrm{th}=V_{\mathrm{th},1}-V_{\mathrm{th},2}
$$

로 쓰면, 이것이 **$V_\mathrm{th}$ mismatch**이다. 6T 셀에서는 두 inverter의 pull-up·pull-down transistor와 두 access transistor가 이상적으로 같아야 하지만, 실제로는 이 mismatch가 positive feedback의 균형을 흔든다. 그러면 SNM, write-trip point, read current와 access time의 분포가 넓어진다.[2,3,5]

작은 planar MOSFET 쌍을 설명할 때 자주 쓰는 Pelgrom 형태의 근사식은

$$
\sigma_{\Delta V_\mathrm{th}}
\approx
\frac{A_{V_\mathrm{th}}}{\sqrt{W L}}
$$

이다. $W$와 $L$은 transistor의 유효 폭과 길이, $A_{V_\mathrm{th}}$는 공정에서 추출하는 mismatch 계수이다. 이 식은 면적이 작을수록 mismatch 표준편차가 커지는 방향을 보여주는 모델이며, FinFET·nanosheet의 정수 fin 수, 공간 상관과 layout 효과를 자동으로 모두 설명하지는 않는다. 따라서 실제 SRAM 수율 계산에는 PDK의 global·local variation model과 layout-aware parameter를 사용해야 한다.[5–8]

### (2) Local variation과 global variation

**Global variation**은 같은 die 또는 wafer의 많은 transistor가 비슷한 방향으로 변하는 성분이다. 예를 들어 전체적으로 $V_\mathrm{th}$가 높아지면 여러 셀의 전류가 함께 작아질 수 있다. **Local variation**은 서로 가까운 transistor 사이에도 남는 상대적 차이이다. 한 셀의 왼쪽 pull-down만 다른 쪽보다 약해지는 것이 local mismatch의 예이다.[2,5]

| 구분 | 주로 함께 변하는 범위 | SRAM 검증에서 묻는 질문 |
| --- | --- | --- |
| Global | wafer·die·macro의 넓은 영역 | 이 공정·전압·온도 조건에서 macro 전체의 평균 동작점이 허용 범위인가? |
| Local | 같은 cell 또는 인접 device 사이 | 같은 조건에서 상대 strength가 불리하게 어긋난 tail cell이 얼마나 자주 생기는가? |
| Spatially correlated | 거리나 방향에 따라 비슷하게 변하는 영역 | 한 row·column 또는 한 die 쪽에 fail이 몰리는가? |

PVT corner는 보통 global한 조건을 대표하고, Monte Carlo mismatch는 local한 분포를 대표한다. 둘은 대체 관계가 아니다. 예를 들어 `slow process`에서 모든 transistor의 평균 속도가 느려지는 것과, 같은 셀 안에서 pull-down 하나만 약해지는 것은 서로 다른 failure를 만들 수 있다. 실제 검증에서는 global variation, local mismatch, 공간 상관을 동시에 포함할 수 있지만, 각각의 의미를 분리해 보고해야 한다.[2,6,7]

### (3) Monte Carlo simulation과 failure probability

**Monte Carlo simulation**은 한 개의 최악 corner를 고르는 방법이 아니라, 정한 확률 분포에서 소자 parameter를 반복 추출하는 방법이다. 한 번의 표본에서 다음 순서를 수행한다.

1. PVT 조건과 cell·array testbench를 고정한다.
2. global process와 local mismatch parameter를 분포에서 추출한다.
3. DC sweep으로 SNM·write margin을 계산하거나 transient simulation으로 read·write 동작을 실행한다.
4. 정한 기준을 넘지 못하면 해당 표본을 failure로 세고, 모든 표본의 분포를 모은다.

셀 failure probability는 $N_\mathrm{MC}$번 가운데 실패한 표본 수를 $N_\mathrm{fail}$이라 할 때

$$
P_\mathrm{cell}
\approx
\frac{N_\mathrm{fail}}{N_\mathrm{MC}}
$$

로 추정할 수 있다. 여기서 failure는 반드시 “SNM이 음수”라는 뜻은 아니다. read에는 셀 상태가 뒤집히는 read-disturb failure와 sense amplifier가 잘못 판정하는 readability failure를 구분해야 하고, write에는 지정 pulse 안에 내부 노드가 새 상태로 도달하지 못하는 조건을 사용해야 한다. Dynamic failure는 DC margin만으로 검출되지 않을 수 있다.[2,3,6]

드문 failure를 직접 관찰하려면 매우 많은 표본이 필요하다. 따라서 Monte Carlo 표본 수와 신뢰구간, failure criterion, variance-reduction 또는 importance-sampling 사용 여부를 함께 기록해야 한다. “10,000번 시뮬레이션에서 실패가 없었다”는 결과는 0의 실제 확률을 증명하는 것이 아니라, 그 표본 수와 조건에서 관측된 upper bound를 뜻한다.[2,6]

### (4) Array yield와 분포의 tail

각 cell의 failure가 서로 독립이고 cell failure probability가 $P_\mathrm{cell}$이라고 가정하면, $N_\mathrm{cell}$개 셀이 모두 통과할 확률은

$$
P_\mathrm{array,pass}
\approx
\left(1-P_\mathrm{cell}\right)^{N_\mathrm{cell}}
$$

이다. 따라서 array failure probability는

$$
P_\mathrm{array,fail}
\approx
1-
\left(1-P_\mathrm{cell}\right)^{N_\mathrm{cell}}.
$$

셀 불량률이 충분히 작을 때에는

$$
P_\mathrm{array,fail}
\approx
N_\mathrm{cell}P_\mathrm{cell}
$$

로 볼 수 있다. 이 식은 “셀 하나의 평균 성능보다 분포의 tail이 중요하다”는 말을 정량적으로 보여준다. 단, 실제 array에서는 spatial correlation, redundant row·column, ECC, repair와 fail masking이 있으므로 이 식은 독립·무보정 array에 대한 1차 근사이다.[2,4,7]

!!! info "[Measurement]"
    먼저 PVT corner와 $V_\mathrm{DD}$, 온도, read·write pulse, bit-line 부하와 sense-amplifier offset을 고정한다. 각 Monte Carlo 표본에서 `hold`, `read`, `write`, `access-time`을 별도의 pass/fail로 기록하고

    $$
    P_\mathrm{cell,mode}
    =
    \frac{N_{\mathrm{fail,mode}}}{N_\mathrm{MC}}
    $$

    를 계산한다. 그 다음 목표 array 크기와 repair·ECC 정책을 고정해 $P_\mathrm{array,fail}$ 또는 목표 yield를 계산한다. 보고서에는 평균값만 쓰지 말고 SNM, write margin, $\Delta V_\mathrm{BL}$, delay의 평균·표준편차·percentile과 tail failure를 함께 제시한다.

!!! warning "[Interpretation Caveat]"
    $P_\mathrm{array,pass}\approx(1-P_\mathrm{cell})^{N_\mathrm{cell}}$는 독립 셀과 동일한 failure criterion을 가정한다. 인접 셀이 같은 lithography 변동을 공유하거나 spare·ECC가 오류를 가리면 실제 macro yield는 이 식과 달라진다. 그렇더라도 array 크기가 커질수록 작은 셀 failure probability가 중요해진다는 방향은 유지된다.[2,4]

## 2. 저전압 동작과 SRAM Assist

SRAM의 저전압 동작은 전원을 단순히 낮추는 문제가 아니다. $V_\mathrm{DD}$가 줄어들면 내부 inverter의 복원력, access transistor의 전류, bit-line 차전압과 sense-amplifier가 사용할 신호가 함께 작아진다. 변동성의 상대적인 영향도 커지므로, nominal cell이 동작해도 tail cell의 read·write failure가 먼저 증가할 수 있다.[3,6,9]

### (1) $V_\mathrm{min}$의 정의와 저전압 failure

$V_\mathrm{min}$은 SRAM의 고유한 상수가 아니라 **정한 macro, timing, PVT, failure probability와 yield 목표를 만족하는 최저 공급전압**이다. Hold에서는 positive feedback이 데이터를 보존할 수 있어야 하고, read에서는 셀이 뒤집히지 않으면서 sense amplifier가 bit-line 신호를 판정해야 하며, write에서는 driver가 셀의 feedback을 이겨야 한다.[2,6,9]

| 저전압에서 줄어드는 여유 | 먼저 나타나는 문제 | 측정할 지표 |
| --- | --- | --- |
| inverter 복원력 | hold 또는 read 중 저장 노드가 교란에 취약해짐 | HSNM, RSNM, dynamic read-failure probability |
| access·pull-down 전류 | bit line 차전압이 늦게 형성됨 | $\Delta V_\mathrm{BL}$, read delay, sensing margin |
| write-driver와 access의 구동력 | 셀 내부 상태를 pulse 안에 뒤집지 못함 | write margin, write time, write-failure probability |
| noise·mismatch 대비 신호 | 공정 편차가 분포의 tail을 넓힘 | Monte Carlo margin과 array yield |

**Sensing margin**은 sense amplifier가 입력 offset·noise를 이기고 ‘0’과 ‘1’을 판정할 수 있는 여유이다. RSNM은 read 중 셀 내부 상태가 유지되는지를 묻는 지표이므로, RSNM이 충분해도 $\Delta V_\mathrm{BL}$이 작거나 sense-amplifier offset이 크면 read가 실패할 수 있다. 반대로 bit-line 차가 빨라도 셀 내부 노드가 뒤집히면 올바른 read가 아니다.[3,6]

### (2) Read assist

**Read assist**는 read 동안 access 경로가 저장 노드를 흔드는 효과를 줄이거나, sense amplifier가 읽을 신호를 더 빨리 만드는 회로 기법이다. 대표적인 방법은 다음과 같다.

| 방법 | 동작 원리 | 좋아지는 점 | 함께 치러야 하는 비용 |
| --- | --- | --- | --- |
| **WL underdrive (WLUD)** | 선택된 $WL$을 정상 $V_\mathrm{DD}$보다 낮춰 access transistor를 약하게 한다. | precharge된 bit line이 저장된 ‘0’ 노드를 올리는 read disturb를 줄여 RSNM을 개선한다. | read current와 $\Delta V_\mathrm{BL}$이 줄어 read time과 sensing margin이 나빠질 수 있다. |
| **Cell $V_\mathrm{DD}$ boost** | read 동안 셀의 내부 supply를 일시적으로 높여 inverter 복원력을 키운다. | 내부 저장 노드의 안정성과 경우에 따라 bit-line 신호 형성을 돕는다. | 추가 전원선·boost 회로·면적·동적 에너지와 oxide stress가 생길 수 있다. |
| **Suppressed bit line** | bit line을 바로 $V_\mathrm{DD}$까지 precharge하지 않고 더 낮은 초기 전압으로 둔다. | 저장 노드로 전달되는 charge sharing을 줄이고 read energy를 낮출 수 있다. | bit-line 신호 크기와 precharge timing을 함께 다시 설계해야 한다. |

WLUD의 방향은 “access를 약하게 해 안정성을 얻는 대신 read를 느리게 한다”로 기억하면 된다. 반면 cell $V_\mathrm{DD}$ boost는 셀 feedback을 강하게 하는 방향이므로, 목표가 RSNM인지 read delay인지에 따라 이득이 다르다. Assist의 이름만 보고 모든 cell topology에서 같은 효과가 난다고 가정해서는 안 된다.[6,7]

### (3) Write assist

**Write assist**는 write 순간에 셀의 복원 feedback을 약하게 하거나 write driver의 입력을 강하게 한다. 6T cell의 PU가 너무 강하면 access transistor가 내부 노드를 충분히 낮추지 못하므로, read assist와 반대 방향의 바이어스가 필요할 수 있다.

| 방법 | write 중 바꾸는 신호 | 직관적인 효과 | 주의할 점 |
| --- | --- | --- | --- |
| **Negative bit line (NBL)** | ‘0’을 쓸 bit line을 잠시 ground 아래로 내린다. | access transistor를 통한 pull-down을 강화하여 feedback을 이긴다. | coupling capacitor·전압 생성 회로, gate-oxide stress와 추가 write energy가 필요하다. |
| **WL boost** | 선택된 $WL$을 정상 $V_\mathrm{DD}$보다 높게 올린다. | access transistor의 gate overdrive를 키워 write current를 늘린다. | level shifter·charge pump와 높은 전압에 의한 reliability 부담이 생긴다. |
| **Cell $V_\mathrm{DD}$ collapse** | write 동안 셀 supply를 일시적으로 낮춘다. | PU의 복원력을 약하게 하여 내부 상태를 뒤집기 쉽게 한다. | half-select cell, hold stability, supply noise와 data retention을 함께 점검해야 한다. |

NBL과 WL boost는 writeability에 유리하지만, access gate나 junction에 정상 동작보다 큰 전압을 만들 수 있다. Cell $V_\mathrm{DD}$ collapse는 셀 자체를 약하게 만들기 때문에 같은 column이나 row의 half-select cell을 교란하지 않는 회로가 필요하다. 그래서 assist는 bitcell 하나의 write margin만 높이는 기능이 아니라, pulse 생성·분배·복원까지 포함한 macro 설계 문제이다.[6,7,9]

### (4) Near-threshold와 subthreshold SRAM

**Near-threshold operation**은 공급전압이 transistor의 threshold voltage와 비슷한 영역에서 동작하는 경우이고, **subthreshold operation**은 주요 transistor가 강한 inversion 아래의 약한 inversion 전류로 동작하는 경우이다. Subthreshold 전류는 $V_\mathrm{GS}$와 $V_\mathrm{th}$의 작은 차이에 매우 민감하므로, 동일한 절대 $V_\mathrm{th}$ 변화도 낮은 전압에서는 상대적으로 큰 성능 차이를 만든다.[7,9]

저전압 SRAM의 설계 선택은 보통 다음 세 방향 사이의 절충이다.

- 6T: 셀 면적과 주변회로 부담이 작지만 read disturb와 writeability가 같은 access path에서 충돌한다.
- 8T·10T: read path를 분리하거나 feedback을 제어하여 저전압 margin을 개선할 수 있지만 transistor·배선·누설·면적이 늘어난다.
- Assist 추가: 기존 6T의 동작 전압을 낮출 수 있지만 boost/collapse 회로와 timing 검증 비용이 늘어난다.

따라서 “$V_\mathrm{min}$이 낮다”는 결과만으로 더 좋은 SRAM이라고 할 수 없다. cell area, leakage, read·write energy, access time, assist generator의 면적과 reliability를 같은 macro 경계에서 비교해야 한다.[6,7,9]

!!! info "[Measurement]"
    $V_\mathrm{DD}$를 높은 전압에서 낮은 전압으로 주사하면서 각 전압에서 hold·read·write를 별도의 transient test로 수행한다. 예를 들어 목표 cell failure probability를 $P_\mathrm{target}$이라 정하면

    $$
    V_\mathrm{min}
    =
    \min\left\{V_\mathrm{DD}:P_\mathrm{fail,all\ modes}\le P_\mathrm{target}\right\}
    $$

    로 정의할 수 있다. 실제 보고에서는 $P_\mathrm{target}$, array 크기, pulse width, sense-amplifier enable 시점, assist waveform, PVT와 Monte Carlo 표본 수를 함께 명시해야 한다. 이 조건이 바뀌면 같은 cell도 다른 $V_\mathrm{min}$을 갖는다.

!!! warning "[Interpretation Caveat]"
    Assist가 한 failure mode를 개선해도 다른 mode를 악화할 수 있다. 예를 들어 WLUD는 read disturb를 줄이지만 read current를 낮출 수 있고, NBL은 write를 쉽게 만들지만 전압 stress와 energy를 늘릴 수 있다. 그러므로 SNM 하나 또는 nominal transient 하나만으로 assist의 성공을 판정하지 않는다.[6,7]

## 3. Advanced SRAM Cell

6T는 저장 feedback과 read·write access를 최소 transistor 수로 구현하는 기준 셀이다. 그러나 같은 access transistor가 read와 write를 모두 담당하기 때문에, read stability와 writeability를 동시에 최적화하기 어렵다. Advanced cell은 이 충돌을 풀기 위해 읽기 경로, 쓰기 경로 또는 feedback 제어를 분리한다.[3,7,9]

<figure markdown="span">
  ![두 cross-coupled inverter와 두 access transistor로 이루어진 conventional 6T SRAM cell](images/sram-6t-cell.svg)
  <figcaption markdown="1">
    그림 2. Advanced cell을 비교할 때 기준으로 삼는 conventional 6T SRAM cell. $Q$와 $\overline{Q}$를 저장하는 두 inverter와 두 access transistor가 read·write 경로를 함께 공유한다. 원본은 Inductiveload, “SRAM Cell (6 Transistors),” Wikimedia Commons, public domain, 수정 없음이다.[21]
  </figcaption>
</figure>

### (1) 8T·10T와 read-decoupled cell

**Read-decoupled cell**은 read bit line이 저장 노드 $Q$ 또는 $\overline{Q}$에 직접 연결되지 않도록 별도의 transistor 경로를 두는 셀이다. 대표적인 8T cell은 6T 저장 latch에 두 개의 read transistor를 더해 read port를 분리한다. 읽는 동안 storage node가 bit line을 직접 충전·방전하지 않으므로, 6T의 read disturb와 cell-sizing 충돌을 줄일 수 있다.[7,9]

10T cell은 여기에 feedback control, stacking, power gating 또는 single-ended read path를 더하는 식으로 설계된다. “8T는 항상 6T보다 안정적”이라는 뜻은 아니다. 어떤 노드를 읽는지, read transistor의 stack과 leakage가 어떤지, reference를 어떻게 만드는지에 따라 stability·speed·energy가 달라진다.[7,9]

| 구조 | 읽기 경로 | 기대하는 이점 | 추가로 확인할 항목 |
| --- | --- | --- | --- |
| 6T differential | 저장 latch와 access transistor를 통해 $BL/\overline{BL}$ 차를 만든다. | 가장 작은 기본 cell, differential sensing과 높은 집적도 | read disturb와 writeability의 상충, mismatch |
| 8T read-decoupled | 저장 latch와 분리된 read port가 read bit line을 구동한다. | read 중 저장 노드 교란을 줄이고 read stability를 독립적으로 조정 | 두 transistor와 read WL, 누설, cell 면적 |
| 10T read/write separated | read·write path를 더 분리하고 feedback 또는 supply를 제어한다. | 저전압·subthreshold에서 read/write를 각각 최적화할 여지 | 추가 control, dynamic power, routing과 layout 면적 |

### (2) Single-ended와 differential cell

**Differential cell**은 $BL$과 $\overline{BL}$ 두 선의 차이를 sense amplifier가 판정한다. 두 선에 공통으로 들어오는 일부 noise를 차동 입력이 억제할 수 있고 reference를 별도로 만들지 않아도 되지만, 두 bit line의 precharge·equalize와 두 선의 matching이 필요하다.

**Single-ended cell**은 한 개의 read bit line과 reference 또는 기준 timing을 사용한다. 배선과 일부 주변회로를 줄일 수 있지만, bit-line leakage·reference variation·noise를 판정 기준과 함께 관리해야 한다. Single-ended가 곧 저전력 또는 high density를 보장하는 것이 아니며, sense amplifier와 column organization까지 포함해 비교해야 한다.[7,9]

### (3) High-density cell과 high-performance cell

6T 대비 transistor를 추가하면 bitcell 면적은 일반적으로 증가하지만, read path를 더 강하게 만들거나 bit line에 연결되는 셀 수를 늘려 주변회로를 공유할 수 있다. 따라서 **cell area**와 **macro density**는 같은 지표가 아니다. 8T 또는 10T cell이 더 넓어도 긴 bit line에서 read signal을 충분히 유지하면 column당 더 많은 셀을 공유할 가능성이 있고, 반대로 주변회로가 복잡해져 macro 전체 면적이 커질 수도 있다.[7,9]

| 비교 기준 | High-density 설계가 우선하는 것 | High-performance·low-voltage 설계가 우선하는 것 |
| --- | --- | --- |
| cell | 최소 transistor와 contact 수, regular layout | read/write path 분리, 강한 read signal, assist 또는 feedback control |
| array | 짧은 bit line보다 cell 반복 수와 주변회로 amortization | 짧은 bit line, 빠른 local sense, 낮은 RC 지연 |
| 전력 | 작은 cell과 적은 precharge·control 회로 | 작은 voltage swing, 짧은 access time, 안정적인 sensing |
| 수율 | layout regularity와 작은 mismatch 민감도 | margin 분리와 tail failure 억제 |

비교할 때에는 같은 PDK, 같은 layout rule, 같은 array 크기·bit-line 길이, 같은 sense criterion을 사용해야 한다. 논문에서 제시한 cell 면적, RSNM 또는 $V_\mathrm{min}$을 서로 다른 공정과 simulation 조건에서 그대로 순위화하면 안 된다.[2,7,9]

### (4) FinFET 및 GAA SRAM

**FinFET**은 gate가 fin channel의 여러 면을 제어하여 짧은 channel에서 electrostatic control을 개선한 transistor 구조이다. SRAM에서는 leakage와 short-channel effect에 유리할 수 있지만, fin의 정수 개수와 폭이 유효 transistor width를 양자화하므로 planar MOSFET처럼 폭을 연속적으로 조절하기 어렵다. 이 제약은 PU·PD·AX strength를 맞추는 cell sizing과 layout에 직접 영향을 준다.[7,8]

**Gate-all-around (GAA)** transistor는 gate가 nanosheet 또는 nanowire channel을 둘러싸는 구조이다. Gate control을 더 강화할 가능성이 있지만, nanosheet 폭·두께, inner spacer, contact와 metal-gate work function의 편차가 SRAM의 $V_\mathrm{th}$와 parasitic capacitance에 영향을 준다. 따라서 GAA SRAM에서도 read·write margin, variability와 contact resistance를 함께 최적화해야 한다.[7,10]

### (5) CFET과 backside power delivery

**Complementary FET (CFET)**은 nFET와 pFET를 수직으로 적층하는 3D 구조이고, **backside power delivery network (BS-PDN)**는 전원·ground 배선을 wafer backside 쪽으로 옮기는 기술이다. 이 조합은 frontside에서 signal과 power가 차지하는 공간을 줄이고, SRAM cell을 더 작게 만들 가능성을 제공한다. 그러나 “수직 적층 = SRAM 면적이 자동으로 감소”라고 말할 수는 없다. nFET·pFET 연결, contact, bit line, word line과 열·공정 수율이 모두 layout을 제한하기 때문이다.[11,12]

CFET SRAM에서 BS-PDN이 바꾸는 주요 설계 변수는 다음과 같다.

| 변수 | frontside power를 사용할 때의 문제 | backside 또는 double-sided routing의 가능성 |
| --- | --- | --- |
| signal·power 혼잡 | 같은 면에서 bit line, word line, $V_\mathrm{DD}$·ground contact가 경쟁한다. | signal routing 공간을 더 확보할 수 있다. |
| IR drop | 긴 전원 경로와 높은 저항이 cell supply를 흔든다. | 전원 경로를 짧게 만들 수 있지만 backside via와 contact 저항을 새로 검증해야 한다. |
| parasitic $R$, $C$ | 인접 wire와 긴 contact가 delay·energy를 키운다. | routing 방향과 위치에 따라 capacitance·delay를 줄일 가능성이 있다. |
| 공정·열 | frontside와 stacked device가 이미 복잡하다. | wafer thinning, backside alignment, thermal budget과 defect가 추가 제약이 된다. |

2025년 CFET SRAM DTCO 연구들은 backside power와 double-sided signal/power routing을 6T·8T array의 parasitic, delay와 power 관점에서 비교하고 있다.[11,12] 여기서 “가능성”은 공정·layout·PDN 모델 아래의 설계 결과이며, 모든 GAA·CFET SRAM에 자동으로 적용되는 보편적 수치가 아니다. 실제 제품 판단에는 cell area뿐 아니라 RSNM, writeability, bit-line IR drop, thermal reliability와 manufacturing yield를 함께 측정해야 한다.

!!! info "[Measurement]"
    서로 다른 cell topology를 비교할 때는 먼저 같은 저장 데이터와 같은 $V_\mathrm{DD}$·온도·PVT를 고정한다. 그 다음 다음 지표를 같은 array 경계에서 추출한다.

    $$
    A_\mathrm{cell},\quad
    \mathrm{RSNM},\quad
    \mathrm{WM},\quad
    t_\mathrm{read},\quad
    t_\mathrm{write},\quad
    E_\mathrm{read},\quad
    E_\mathrm{write},\quad
    I_\mathrm{leak},\quad
    P_\mathrm{array,fail}
    $$

    여기서 $A_\mathrm{cell}$은 layout 면적, WM은 문서에서 정한 write margin, $t$와 $E$는 주변회로 포함 여부를 명시한 지연과 에너지이다. 6T·8T·10T의 transistor 수만 세거나 single cell 결과만 비교해서는 high-density와 high-performance의 차이를 판단할 수 없다.

!!! warning "[Interpretation Caveat]"
    8T·10T, FinFET·GAA와 CFET의 장점은 특정 read path, bias, PDK와 layout에 종속된다. 특히 cell-level RSNM 개선이 macro-level access time·energy·yield 개선으로 바로 이어지지 않을 수 있다.[7,9,11,12]

## 4. 신뢰성과 불량 분석

SRAM의 불량은 “값을 저장하지 못한다”라는 한 문장으로 끝나지 않는다. 언제, 어떤 동작에서, 어느 회로 경로가 실패했는지를 기록해야 원인을 좁힐 수 있다. 제작 직후의 process defect, 일시적인 radiation-induced soft error, 사용 시간에 따른 transistor aging과 contact·interconnect degradation은 서로 다른 시험과 모델을 요구한다.[13–19]

### (1) Read, write, hold와 access-time failure

| 불량 종류 | 실패가 발생하는 동작 | 관측되는 현상 | 1차로 의심할 경로 |
| --- | --- | --- | --- |
| **Hold failure** | $WL=0$인 보존 상태 | 저장 노드가 시간이 지나며 반대 상태로 이동 | feedback strength, low-$V_\mathrm{DD}$ margin, leakage, aging |
| **Read failure** | read pulse와 sensing | cell이 read 중 뒤집히거나 sense amplifier가 반대 값을 출력 | RSNM, $\Delta V_\mathrm{BL}$, sense offset, bit-line leakage |
| **Write failure** | write pulse | 입력 데이터를 써도 내부 노드가 새 stable state에 도달하지 않음 | PU 대 AX strength, write driver, WL/BL timing, assist |
| **Access-time failure** | 기능은 맞지만 제한 시간 안에 완료되어야 할 때 | output이 늦거나 sense amplifier가 enable window를 놓침 | WL·BL RC, contact/interconnect resistance, SA delay, low current |

Read failure와 access-time failure는 구분해야 한다. 충분히 긴 시간을 주면 올바른 값이 나오는 셀도 제품 timing에서는 불량일 수 있다. 반대로 output이 빠르게 나오더라도 read disturb로 셀의 저장값을 바꾸었다면 기능적으로 안전한 read가 아니다.[3,6,13]

!!! info "[Measurement]"
    hold에서는 $WL=0$으로 두고 지정한 시간 동안 $Q$, $\overline{Q}$의 최종 상태를 확인한다. read에서는 precharge, $WL$ pulse, sense-amplifier enable과 output 판정 시점을 기록하여 (i) 내부 node upset, (ii) 잘못된 sense, (iii) 늦은 output을 별도 분류한다. write에서는 양방향 데이터와 모든 relevant half-select 조건을 반복하고, 내부 node가 정의한 logic threshold를 지나는 시간과 output read-back 결과를 함께 기록한다.

### (2) Soft error와 critical charge

**Soft error**는 transistor나 dielectric이 영구적으로 파괴되지 않았는데도, 방사선 입자나 패키지에서 나온 고에너지 입자가 sensitive node에 전하를 만들어 저장 논리를 일시적으로 바꾸는 오류이다. 저장 feedback이 원래 상태로 돌아오면 회복되지만, 교란 전하가 충분히 크면 **single-event upset (SEU)**가 발생해 bit가 반대 상태로 남을 수 있다.[13,16,17]

**Critical charge ($Q_\mathrm{crit}$)**는 특정 bias·저장 상태·입자 strike 위치와 pulse model에서 내부 논리 상태를 뒤집는 데 필요한 최소 수집 전하이다. 간단한 회로 모델에서는 sensitive node에 주입한 전류를 적분해

$$
Q_\mathrm{inj}
 =
\int_0^\infty I_\mathrm{inj}(t)\,dt
$$

로 계산하고, 상태가 뒤집히는 경계의 $Q_\mathrm{inj}$를 $Q_\mathrm{crit}$으로 정의한다. 방사선 전류는 흔히 double-exponential pulse로 모델링한다.

$$
I_\mathrm{inj}(t)
=
\frac{Q_\mathrm{inj}}{\tau_\mathrm{f}-\tau_\mathrm{r}}
\left(
e^{-t/\tau_\mathrm{f}}
-e^{-t/\tau_\mathrm{r}}
\right)
$$

여기서 $\tau_\mathrm{r}$과 $\tau_\mathrm{f}$는 rise·fall time constant이다. $Q_\mathrm{crit}$이 크면 같은 strike 조건에서 soft upset에 더 강한 경향이 있지만, 이것이 실제 soft-error rate (SER)를 단독으로 결정하지는 않는다. 입자 flux, sensitive area, strike 위치, charge sharing, 저장 논리 상태와 동작전압도 함께 작용한다.[13,16,17]

### (3) NBTI·PBTI·HCI·TDDB에 따른 열화

**Negative bias temperature instability (NBTI)**는 주로 pMOS, **positive bias temperature instability (PBTI)**는 주로 nMOS의 bias·temperature stress로 $V_\mathrm{th}$와 구동력이 시간에 따라 변하는 현상이다. SRAM에서는 절대 성능보다 PU·PD·AX transistor의 **상대 strength**가 중요하므로, 한 종류의 transistor만 더 크게 열화되어도 read stability와 writeability가 달라진다. NBTI·PBTI의 effect는 data pattern과 duty cycle에 의존하므로, 한 개의 고정 SNM만으로 수명 전체를 대표할 수 없다.[14,15]

**Hot-carrier injection (HCI)**는 큰 lateral electric field에서 높은 에너지를 얻은 carrier가 interface 또는 dielectric trap을 만들며 transistor 특성을 바꾸는 열화이다. **Time-dependent dielectric breakdown (TDDB)**는 dielectric에 높은 field가 장시간 인가되어 leakage가 증가하고 결국 절연 기능을 잃는 확률적 열화이다. HCI와 TDDB는 transistor drive, gate leakage, 주변회로 timing과 cell margin을 바꾸며, TDDB는 영구적인 hard failure로 이어질 수 있다.[15,16]

| 열화 원인 | SRAM에 먼저 나타날 수 있는 변화 | 시험에서 함께 고정할 것 |
| --- | --- | --- |
| NBTI | pMOS PU의 $V_\mathrm{th}$·drive 변화, read stability 저하 | 저장 데이터, duty cycle, 온도, stress time |
| PBTI | nMOS PD·AX의 drive 변화, read/write balance 변화 | gate bias, stress pattern, 온도 |
| HCI | high-field transistor의 drive·leakage 변화, access delay 증가 | drain bias, switching activity, pulse count |
| TDDB | gate leakage 증가, soft breakdown 또는 hard failure | dielectric stress, voltage, 온도, time-to-failure |
| Contact·interconnect resistance | WL·BL voltage drop, RC delay, sensing margin 감소 | line length, contact chain, current density, 온도 |

Contact 및 interconnect resistance는 저장 latch의 transistor parameter만 바꾸는 것이 아니다. 긴 WL·BL에서 $IR$ drop과 RC 지연을 만들고, 선택 셀에서 생성한 작은 $\Delta V_\mathrm{BL}$을 줄여 access-time failure 또는 sensing failure를 만들 수 있다. 따라서 device parameter와 circuit failure의 상관관계를 보려면 transistor aging simulation만으로 끝내지 말고 extracted parasitic와 실제 array timing을 함께 사용해야 한다.[15,18]

!!! info "[Measurement]"
    time-zero와 aged 조건에서 같은 cell·array testbench를 반복한다. stress 전후의 $V_\mathrm{th}$, leakage, $I_\mathrm{read}$, $\Delta V_\mathrm{BL}$, RSNM, write margin과 read·write delay를 비교하고, failure probability의 시간 변화를 기록한다. HCI·TDDB는 accelerated stress를 사용하더라도 온도·전압 acceleration model과 failure criterion을 명시해야 하며, 실제 사용 조건으로 extrapolation할 때는 별도의 model uncertainty를 보고한다.[14–16]

### (4) SRAM failure bit map

**SRAM failure bit map**은 array의 각 주소에서 pass/fail 또는 logic 0/1 failure를 공간적으로 표시한 지도이다. Single-bit failure는 한 셀의 local defect나 marginal parameter를 암시할 수 있고, 같은 column에 반복되는 pattern은 bit-line·column peripheral 문제를, 같은 row에 반복되는 pattern은 word line·row driver 문제를 의심하게 한다. 여러 셀이 이웃해 실패하면 lithography, contact, power distribution 또는 coupling 문제를 생각할 수 있다.[18,19]

하지만 bit map의 모양만으로 원인을 확정할 수는 없다. 한 failure pattern이 여러 defect 또는 fault mechanism에서 나올 수 있으므로, bitmap을 current signature, PVT dependence, read/write direction과 함께 비교하고 필요하면 FIB/SEM/TEM 같은 physical failure analysis로 확인해야 한다.[18,19]

| 관측 pattern | 가능한 해석 | 추가 확인 |
| --- | --- | --- |
| 고립된 한두 bit | local $V_\mathrm{th}$ mismatch, contact defect, weak cell | 동일 주소의 read/write 방향, 온도·전압 sweep, physical localization |
| 한 column 또는 column group | bit line, column mux, sense amplifier, contact chain | column별 delay·current, SA offset, line resistance |
| 한 row 또는 row group | WL driver, word-line resistance, row decoder | WL waveform·RC, row address 의존성 |
| 넓은 cluster·wafer 위치 의존 | global/spatial process variation, power distribution | wafer map, process monitor, IR drop, neighboring structures |
| 특정 data pattern·동작에서만 발생 | read disturb, writeability, leakage 또는 half-select | 저장 방향을 바꾼 March test, assist on/off, transient waveform |

### (5) 소자 parameter와 회로 불량의 연결

소자·공정 parameter와 회로 failure는 다음 chain으로 연결된다.

$$
\text{RDF/LER/WFV/dimension}
\rightarrow
\Delta V_\mathrm{th},\ \Delta I_\mathrm{on},\ \Delta I_\mathrm{off}
\rightarrow
\text{PU/PD/AX imbalance}
\rightarrow
\text{SNM, write margin, }\Delta V_\mathrm{BL},\text{ delay}
\rightarrow
\text{bit failure or yield loss}.
$$

Contact·interconnect 문제는 이 chain에서 주로 line resistance·capacitance와 supply/bit-line drop을 통해 failure를 만든다. Aging은 time-zero parameter에 drift를 더하고, soft error는 짧은 charge pulse를 추가한다. 따라서 같은 `read failure`라도 (i) time-zero mismatch, (ii) low-$V_\mathrm{DD}$ dynamic sensing, (iii) aged PU/PD balance, (iv) particle strike가 서로 다른 원인일 수 있다.[2,13–19]

!!! warning "[Interpretation Caveat]"
    회로 simulation에서 하나의 parameter를 바꾸어 failure를 재현했다고 해서 silicon의 유일한 원인이 증명되는 것은 아니다. Failure map, PVT·aging·data-pattern dependence, current signature와 physical analysis가 서로 일치하는지 확인해야 한다. 특히 bitmap의 row·column 모양은 원인 후보를 좁히는 진단 단서이지 단독 판정 기준이 아니다.[18,19]

## 5. 요약

- PVT는 process·voltage·temperature의 대표 조건이고, local mismatch는 같은 셀 안 transistor 사이의 상대적 차이이다. RDF, LER, WFV와 fin·nanosheet 치수 변동은 $V_\mathrm{th}$와 구동력 분포를 넓힌다.
- Monte Carlo는 평균 셀이 아니라 SNM, write margin, sensing margin과 delay의 분포를 얻기 위한 절차이다. 대규모 array에서는 작은 $P_\mathrm{cell}$도 $N_\mathrm{cell}$개의 반복 때문에 중요한 $P_\mathrm{array,fail}$로 증폭될 수 있다.
- $V_\mathrm{min}$은 cell 고유 상수가 아니라 array 크기, timing, PVT, failure probability와 yield 목표를 포함한 정의이다. WLUD·cell $V_\mathrm{DD}$ boost는 read를, NBL·WL boost·cell $V_\mathrm{DD}$ collapse는 write를 보조할 수 있지만 전력·면적·stress 비용이 있다.
- 8T·10T와 read-decoupled cell은 read path와 storage node의 충돌을 줄일 수 있지만 transistor·배선·leakage·layout 비용이 증가한다. Single-ended와 differential의 선택도 sense reference와 주변회로까지 포함해 판단해야 한다.
- FinFET·GAA·CFET·BS-PDN은 SRAM scaling의 새로운 자유도를 주지만, quantized geometry, contact, parasitic, thermal budget과 manufacturing yield를 함께 최적화해야 한다.
- Read·write·hold·access-time failure를 분리하고, soft error의 $Q_\mathrm{crit}$, BTI·HCI·TDDB aging, contact·interconnect resistance와 failure bit map을 서로 연결해 분석해야 한다.

## 6. 참고문헌

1. E. Grossar, M. Stucchi, K. Maex, and W. Dehaene, “Read Stability and Write-Ability Analysis of SRAM Cells for Nanometer Technologies,” *IEEE Journal of Solid-State Circuits* **41**, 2577–2588 (2006). [DOI: 10.1109/JSSC.2006.883344](https://doi.org/10.1109/JSSC.2006.883344).
2. K. Agarwal and S. Nassif, “Statistical Analysis of SRAM Cell Stability,” *Proceedings of the 43rd Annual Design Automation Conference*, 57–62 (2006). [DOI: 10.1145/1146909.1146928](https://doi.org/10.1145/1146909.1146928).
3. E. Seevinck, F. J. List, and J. Lohstroh, “Static-Noise Margin Analysis of MOS SRAM Cells,” *IEEE Journal of Solid-State Circuits* **22**, 748–754 (1987). [DOI: 10.1109/JSSC.1987.1052809](https://doi.org/10.1109/JSSC.1987.1052809).
4. R. Joshi et al., “A Universal Hardware-Driven PVT and Layout-Aware Predictive Failure Analytics for SRAM,” *IEEE Transactions on Very Large Scale Integration (VLSI) Systems* **24**, 968–978 (2016). [DOI: 10.1109/TVLSI.2015.2427196](https://doi.org/10.1109/TVLSI.2015.2427196).
5. M. J. M. Pelgrom, A. C. J. Duinmaijer, and A. P. G. Welbers, “Matching Properties of MOS Transistors,” *IEEE Journal of Solid-State Circuits* **24**, 1433–1439 (1989). [DOI: 10.1109/JSSC.1989.572629](https://doi.org/10.1109/JSSC.1989.572629).
6. Y. N. Chen et al., “Impacts of Intrinsic Device Variations on the Stability of FinFET Subthreshold SRAMs,” *2011 IEEE International Conference on Integrated Circuit Design and Technology*, 1–4 (2011). [DOI: 10.1109/ICICDT.2011.5783210](https://doi.org/10.1109/ICICDT.2011.5783210).
7. W. Gul, M. Shams, and D. Al-Khalili, “SRAM Cell Design Challenges in Modern Deep Sub-Micron Technologies: An Overview,” *Micromachines* **13**, 1332 (2022). [DOI: 10.3390/mi13081332](https://doi.org/10.3390/mi13081332). [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
8. K. Endo, S. O’uchi, T. Matsukawa, and Y. Liu, “(Invited) Variability in FinFET SRAM Cells,” *228th ECS Meeting* (2015). [초록](https://ecs.confex.com/ecs/228/webprogram/Paper58600.html).
9. N. Verma and A. P. Chandrakasan, “A 65nm 8T Sub-Vt SRAM Employing Sense-Amplifier Redundancy,” *IEEE International Solid-State Circuits Conference Digest of Technical Papers*, 328–329 (2007). [저자 제공 PDF](https://people.eecs.berkeley.edu/~pister/290Q/Papers/Computation/sub-Vt%20SRAM%20isscc07.pdf).
10. Y. Morita et al., “24.3 A 3nm Gate-All-Around SRAM Featuring an Adaptive Dual-BL and an Adaptive Cell-Power Assist Circuit,” *IEEE International Solid-State Circuits Conference Digest of Technical Papers* (2021). [IEEE Xplore](https://ieeexplore.ieee.org/abstract/document/9365988).
11. Y.-C. Lu, M.-L. Wu, and V. P.-H. Hu, “Design Technology Co-Optimization for CFET SRAM Cells Considering Double-Sided Signal/Power Routing,” *2025 IEEE International Symposium on Circuits and Systems*, 1–5 (2025). [DOI: 10.1109/iscas56072.2025.11043266](https://doi.org/10.1109/iscas56072.2025.11043266).
12. Y.-C. Chen, L.-A. Yu, K.-W. Cheng, and E. R. Hsieh, “Ultra-scale (0.014 μm²) High-efficient 10A 6T CFET-SRAM Cells Combined Backside Power Deliver Networks and Backside Bit-lines,” *2025 International VLSI Symposium on Technology, Systems and Applications*, 1–4 (2025). [DOI: 10.1109/VLSITSA64674.2025.11046769](https://doi.org/10.1109/VLSITSA64674.2025.11046769).
13. A. Pavlov and M. Sachdev, “Soft Errors in SRAMs: Sources, Mechanisms and Mitigation Techniques,” in *CMOS SRAM Circuit Design and Parametric Test in Nano-Scaled Technologies*, chap. 6 (Springer, 2008). [DOI: 10.1007/978-1-4020-8363-1_6](https://doi.org/10.1007/978-1-4020-8363-1_6).
14. A. Bansal, R. Rao, J.-J. Kim, S. Zafar, J. H. Stathis, and C.-T. Chuang, “Impacts of NBTI and PBTI on SRAM Static/Dynamic Noise Margins and Cell Failure Probability,” *Microelectronics Reliability* **49**, 642–649 (2009). [DOI: 10.1016/j.microrel.2009.03.016](https://doi.org/10.1016/j.microrel.2009.03.016).
15. S. Mishra and S. Mahapatra, “On the Impact of Time-Zero Variability, Variable NBTI and Stochastic TDDB on SRAM Cells,” *IEEE Transactions on Electron Devices* **63**, 2764–2770 (2016). [DOI: 10.1109/TED.2016.2558522](https://doi.org/10.1109/TED.2016.2558522).
16. X. Wan, “Device Reliability Challenges in Advanced FinFET Technology,” *EDFA Technical Articles* **21** (4), 30–37 (2019). [DOI: 10.31399/asm.edfa.2019-4.p030](https://doi.org/10.31399/asm.edfa.2019-4.p030).
17. G. Zhang, J. Shao, F. Liang, and D. Bao, “A Novel Single Event Upset Hardened CMOS SRAM Cell,” *IEICE Electronics Express* **9**, 140–145 (2012). [DOI: 10.1587/elex.9.140](https://doi.org/10.1587/elex.9.140).
18. P. Coppens, G. Vanhorebeek, and E. De Backer, “Correlation between Predicted Cause of SRAM Failures and In-Line Defect Data,” *Microelectronics Reliability* **41** (1), 53–57 (2001). [DOI: 10.1016/S0026-2714(00)00105-0](https://doi.org/10.1016/S0026-2714(00)00105-0).
19. M. Schienle, Th. Zanon, and D. Schmitt-Landsiedel, “Improved SRAM Failure Diagnosis for Process Monitoring via Current Signature Analysis,” *Microelectronics Reliability* **39** (6–7), 1009–1014 (1999). [DOI: 10.1016/S0026-2714(99)00139-0](https://doi.org/10.1016/S0026-2714(99)00139-0).
20. HandigeHarry, “DRAM,” *Wikimedia Commons* (2006), public domain. [파일 설명과 라이선스](https://commons.wikimedia.org/wiki/File:DRAM.svg).
21. Inductiveload, “SRAM Cell (6 Transistors),” *Wikimedia Commons* (2009), public domain. [파일 설명과 라이선스](https://commons.wikimedia.org/wiki/File:SRAM_Cell_(6_Transistors).svg).
