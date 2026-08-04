---
title: "2.4. Memory device: DRAM basic"
description: DRAM의 1T1C 셀, charge sharing, sense amplifier, refresh, array 계층과 셀 공정의 기초를 beginner 관점에서 설명
status: verified
last_verified: 2026-08-04
---

# 2.4. Memory device: DRAM basic

[Memory device: Overview](basics.md)에서는 메모리 계층과 공통적인 cell array·word line·bit line·peripheral circuit의 관계를 설명했다. [Memory Device: SRAM Basic](sram.md)에서는 6T SRAM이 두 개의 안정 상태를 회로의 positive feedback으로 유지하는 방식을 다뤘다. 이 글에서는 그와 대비되는 **dynamic random-access memory (DRAM)**를 다룬다.

DRAM은 대규모 데이터를 비교적 작은 면적에 저장하기 위해, 보통 한 bit를 **access transistor 하나와 storage capacitor 하나**로 구성한다. 이 셀은 capacitor의 전하를 읽어 논리값을 판정하고, 읽기 과정에서 약해진 전하를 다시 채워 넣는다. 시간이 지나면 전하가 새어 나가므로 외부 접근이 없더라도 주기적인 **refresh**가 필요하다.[1–5]

이 글에서 다루는 기본 동작은 conventional 1T1C DRAM과 differential bit-line, $V_\mathrm{DD}/2$ precharge, cross-coupled latch형 sense amplifier를 기준으로 한다. 실제 DDR·LPDDR·HBM 제품은 명령 부호, burst, bank 구성, I/O timing과 refresh 정책이 서로 다를 수 있으므로, 아래의 회로 설명과 제품 data sheet의 protocol 정의를 구분한다.[3–5]

## 1. DRAM의 역할과 전체 구조

### (1) 메모리 계층에서 DRAM이 맡는 일

그림 1에서 보듯 register와 cache는 프로세서에 가깝고 작지만 빠른 저장 수준이며, main memory는 더 큰 작업 집합을 담는다. DRAM은 일반적으로 main memory를 구현하는 대표 기술이다. NAND Flash는 전원이 제거되어도 전하 또는 threshold-voltage 상태를 유지하므로 storage에 적합하지만, program·erase 단위와 쓰기 지연·endurance 제약이 DRAM과 다르다.[3,4]

<figure markdown="span">
  ![register, cache, main memory와 storage로 이어지는 시스템 메모리 계층](images/computer-memory-hierarchy.svg)
  <figcaption markdown="1">
    그림 1. 시스템 관점의 메모리 계층. DRAM은 보통 main memory를, SRAM은 cache를, NAND Flash는 storage를 구현하는 데 사용되지만, 시스템 역할과 물리 기술은 일대일 대응이 아니다. 출처: G. Heiser, “Caches,” <i>COMP9242 2025 T3 W03 Part 1: HW Considerations</i>, slide 5, UNSW Sydney, CC BY 4.0. 원본의 계층 흐름을 발췌하여 사용했으며 수정 없음.[21]
  </figcaption>
</figure>

SRAM과 DRAM의 차이는 단순히 “transistor 수가 많고 적다”에 그치지 않는다. SRAM은 전원이 공급되는 동안 feedback loop가 상태를 유지하므로 읽기가 원칙적으로 비파괴적이다. DRAM은 capacitor의 아날로그 전하를 bit-line과 공유하여 읽으므로 읽기 뒤 저장 상태를 복원해야 한다. 이 구조 차이가 밀도·속도·전력·refresh의 차이로 이어진다.[2–5]

| 항목 | SRAM | DRAM | NAND Flash |
| --- | --- | --- | --- |
| 대표 셀 | 보통 6T | 보통 1T1C | floating-gate 또는 charge-trap transistor array |
| 정보 저장 | 두 inverter의 bistable state | capacitor의 전하 | transistor의 비휘발성 charge 또는 threshold 상태 |
| 읽기 | 원칙적으로 비파괴적 | charge sharing 뒤 restore 필요 | sensing 뒤에도 상태가 유지되지만 read/program 조건이 다름 |
| Refresh | 전원이 유지되면 별도 refresh 불필요 | 필요 | 정상 동작 중 주기적 refresh 불필요 |
| 장점 | 짧은 access path, 빠른 sensing | 높은 bit density, 큰 용량 | 전원 제거 뒤에도 보존 |
| 주요 비용 | 셀 면적과 bit당 transistor 수 | refresh, sense와 긴 bit-line 지연 | program·erase 지연, endurance와 block 관리 |

위 표의 속도 비교는 셀 하나의 고유 switching speed를 순위화한 것이 아니다. 실제 latency와 energy는 셀, bit-line, sense amplifier, decoder, I/O와 controller를 포함한 측정 경계에 따라 달라진다. DRAM은 셀은 작지만 한 번의 접근에서 row를 열고, 작은 전압차를 증폭하고, 필요한 column만 외부로 전달해야 하므로 cell access와 chip-level latency가 다르다.[3–5]

### (2) DRAM chip의 기능 블록

DRAM chip을 “capacitor가 빽빽하게 있는 영역”으로만 이해하면 읽기와 timing을 설명할 수 없다. 다음 블록들이 저장 셀과 외부 interface 사이를 연결한다.[2–5]

| 블록 | 초보자를 위한 역할 |
| --- | --- |
| **Cell array** | 1T1C 셀을 행과 열로 반복하여 실제 전하를 저장한다. |
| **Subarray 또는 mat** | 긴 word line과 bit line을 짧게 나눈 작은 어레이 단위이다. |
| **Bank** | 여러 subarray와 local·global 주변회로를 묶은 독립 동작 단위이다. |
| **Row decoder** | row address를 받아 하나의 word line을 선택한다. |
| **Column decoder·column multiplexer** | 열린 row에서 외부로 보낼 column을 선택한다. |
| **Sense amplifier** | bit-line의 작은 전압차를 full-swing 논리값으로 증폭하고 셀을 restore한다. |
| **Global data line** | local sense amplifier 또는 row buffer에서 global sense amplifier·I/O로 선택 데이터를 전달한다. |
| **I/O circuit** | chip 내부 데이터와 외부 DQ·data strobe의 전기적·timing interface를 담당한다. |
| **Refresh controller 또는 refresh logic** | row를 일정 주기로 activate하여 capacitor 전하를 다시 채운다. |

그림 2의 일반적인 array 개념도에서 파란 영역은 셀 반복, 왼쪽은 row 선택, 열 방향의 판독 회로는 sense amplifier, 아래쪽은 column 선택을 나타낸다. 실제 DRAM에서는 sense amplifier가 array의 가장자리나 두 subarray 사이에 반복되고, 그 자체가 열린 row의 row buffer 역할을 한다.[4,5]

<figure markdown="span">
  ![행과 열로 배열된 memory cell, row decoder, sense amplifier와 column decoder의 개념도](images/memory-cell-array.svg)
  <figcaption markdown="1">
    그림 2. DRAM chip을 cell array와 행·열 주변회로의 결합으로 보는 개념도. 원본은 HandigeHarry, “DRAM,” Wikimedia Commons, public domain이며, array·decoder·sense-amplifier 관계를 설명하는 영역을 발췌해 사용했다. 이 그림은 특정 제품의 실제 layout이나 subarray 수를 나타내지 않는다.[22]
  </figcaption>
</figure>

### (3) Cell에서 bank까지의 포함 관계

**Cell**은 한 bit를 저장하는 최소 반복 단위이다. 같은 word line에 연결된 cell들의 모임은 한 row가 되고, 한 row를 감지해 임시로 보관하는 sense-amplifier 집합이 row buffer가 된다. 외부 read/write가 한 번에 row 전체를 꺼내는 것은 아니며, column decoder가 row buffer에서 일부 열을 선택해 global data line과 I/O circuit으로 전달한다.[4,5]

큰 어레이를 하나로 만들면 word line과 bit line의 저항·정전용량이 커진다. 그래서 여러 subarray를 bank로 나누고, 각 subarray에 local decoder·precharge·sense amplifier를 배치한다. 이 분할은 속도와 energy에 유리하지만, decoder와 sense amplifier를 복제해야 하므로 area overhead가 생긴다. 즉, 긴 bit line을 줄이는 것은 항상 공짜인 최적화가 아니다.[3–5]

## 2. 1T1C DRAM 셀과 stored charge

### (1) Access transistor, storage capacitor와 세 단자

1T1C DRAM 셀은 하나의 **access transistor**와 하나의 **storage capacitor**로 구성된다. 여기서는 access transistor를 n-channel metal–oxide–semiconductor field-effect transistor (nMOSFET)으로 설명한다. transistor의 gate는 **word line (WL)**, 한쪽 단자는 **bit line (BL)**, 다른 쪽 단자는 capacitor의 storage node에 연결된다. capacitor의 반대쪽 plate는 보통 공통 plate 전위에 연결된다.[1,2]

| 이름 | 회로에서 하는 일 | 직관적 비유 |
| --- | --- | --- |
| WL | access transistor를 켜고 끈다 | 셀로 들어가는 문을 여는 신호 |
| BL | 전하를 쓰고 읽는 공통 데이터선 | 여러 셀이 공유하는 통로 |
| Storage node | 한 셀의 전하가 직접 놓이는 node | 현재 bit를 나타내는 작은 저장 용기 |
| Cell capacitor | 전하를 저장한다 | 물이 조금 담긴 작은 컵 |
| Access transistor | BL과 storage node의 연결을 제어한다 | 컵과 관 사이의 밸브 |

비유에서 컵이 아무리 작아도 물이 새면 시간이 지나 수위가 내려간다. DRAM의 refresh는 수위가 판정 기준 아래로 내려가기 전에 셀을 다시 읽고 충분한 전하를 채우는 과정이다. 이 비유는 전하의 방향과 전압 의존성을 단순화하지만, “작은 capacitor와 leakage·sensing의 균형”이라는 핵심은 잘 보여준다.[1–5]

### (2) 논리 0과 1을 전하로 나타내기

저장 capacitor 양단의 전압을 $V_\mathrm{cell}$이라 정의하면, 저장된 전하의 크기는 이상적인 선형 capacitor 근사에서

$$
Q_\mathrm{cell}=C_\mathrm{cell}V_\mathrm{cell}
$$

이다. $C_\mathrm{cell}$은 cell capacitance, $V_\mathrm{cell}$은 storage node와 plate 사이의 전압차이다. 이 글에서는 저장 전하의 절댓값을 중심으로 설명하므로, 전하의 부호는 선택한 plate 기준에 따라 달라질 수 있다.[1,2]

쓰기 과정에서 storage node를 높은 전압으로 충전한 상태를 논리 1, 낮은 전압으로 방전한 상태를 논리 0으로 부를 수 있다. 실제 DRAM은 내부 plate bias, 데이터 scrambling, bit-line polarity에 따라 외부 DQ의 0·1과 storage node의 높고 낮음이 직접 일치하지 않을 수 있다. 따라서 “높은 node가 항상 외부 논리 1”이라고 일반화하지 않고, 여기서는 이해를 위해 높은 전하 상태를 1로 부른다.[2,3]

DRAM에서 $C_\mathrm{cell}$은 단순히 저장 용량만 결정하지 않는다.

- $C_\mathrm{cell}$이 크면 같은 leakage current에서 전압 변화가 느려져 retention에 유리하다.
- $C_\mathrm{cell}$이 크면 bit-line과 charge sharing할 때 더 큰 sensing signal을 만들 수 있다.
- 그러나 큰 면적의 capacitor는 cell pitch 안에 넣기 어렵고, 높이·공정 복잡도·기생 성분이 증가한다.

따라서 DRAM cell 설계는 “무조건 큰 capacitor”가 아니라, 제한된 면적에서 충분한 $C_\mathrm{cell}$과 낮은 leakage, 낮은 parasitic capacitance를 동시에 얻는 문제이다.[2,14,15]

### (3) Folded bit-line과 open bit-line

DRAM sense amplifier는 한 bit-line의 절대 전압보다 두 선 사이의 작은 차이를 판정하는 differential circuit이다. 그래서 실제 어레이는 target bit-line과 reference bit-line을 어떻게 배치할지 정해야 한다.

| 구조 | reference 선의 위치 | 장점 | 비용 또는 주의점 |
| --- | --- | --- | --- |
| **Folded bit-line** | 같은 array 안에서 pair로 함께 배선 | 두 선이 가까워 공통 noise와 word-line coupling을 잘 상쇄할 수 있다. | cell layout과 sense-amplifier pitch가 커질 수 있다. |
| **Open bit-line** | 인접한 두 array에서 각각 한 선을 가져옴 | 더 작은 cell geometry와 높은 density에 유리할 수 있다. | 두 선의 환경이 달라 noise와 imbalance 관리가 어렵다. |

Folded 구조에서는 true와 complement bit-line이 가까이 있어 common-mode noise rejection에 유리하지만, layout area가 커질 수 있다. Open 구조는 cell density에 유리할 수 있으나, 서로 다른 array의 coupling과 mismatch가 sense margin에 영향을 줄 수 있다. 어떤 구조가 최선인지는 cell pitch, sense-amplifier pitch, noise, process와 technology generation을 함께 놓고 판단한다.[2,6,7]

### (4) 1T1C 이외의 DRAM cell 개념

1T1C는 discrete capacitor를 사용하지만, DRAM이라는 동작 원리를 다른 물리 상태에 구현하려는 cell도 있다.

| 개념 | 저장하는 것 | 기대하는 점 | 어려운 점 |
| --- | --- | --- | --- |
| **Gain cell** | transistor gate capacitance 또는 내부 storage node의 전하 | logic 공정과 capacitorless 구조로 통합하기 쉽다. | 작은 유효 capacitance와 transistor leakage 때문에 retention과 sensing margin이 제한된다. |
| **Capacitorless 1T DRAM** | SOI transistor의 floating-body charge | 별도 capacitor를 없애 cell 또는 3D integration을 단순화할 수 있다. | body charge를 재현성 있게 쓰고 읽는 방법, retention, variation이 어렵다. |
| **Floating-body memory** | 전하가 고립된 body의 potential 변화 | body effect를 sensing signal로 이용할 수 있다. | body가 완전히 고립되지 않으면 charge loss와 history dependence가 생긴다. |

이 구조들은 conventional commodity DRAM의 1T1C를 단순히 대체했다고 보면 안 된다. 각각 저장 상태, write mechanism, sensing quantity와 refresh 조건이 다르며, embedded memory나 3D integration 같은 특정 목표에서 평가된다.[17–20]

## 3. DRAM Write 동작

### (1) Bit line이 storage capacitor를 정하는 과정

Write에서는 먼저 write driver가 원하는 데이터를 BL에 인가한다. 그 다음 WL을 활성화하여 access transistor를 켜면 BL과 storage node가 연결되고, capacitor가 BL의 전압을 따라 충전 또는 방전된다. 충분한 시간 뒤 WL을 끄면 storage node가 다시 고립되어 전하를 보존한다.[1–3]

쓰기 순서를 시간 순서로 쓰면 다음과 같다.

1. 선택할 bank와 row·column 주소를 준비한다.
2. 쓰기 대상 BL 또는 differential pair에 입력 데이터에 대응하는 전압을 구동한다.
3. WL을 높여 access transistor를 켠다.
4. BL과 storage capacitor 사이에 전하가 이동하도록 충분한 write time을 둔다.
5. WL을 끄고 BL을 다음 cycle의 precharge 또는 idle 상태로 돌린다.

논리 1을 쓸 때에는 storage node를 높은 전위로 충전하고, 논리 0을 쓸 때에는 낮은 전위로 방전한다고 생각하면 된다. 하지만 access transistor가 nMOS pass transistor이면 높은 전압을 전달할 때 threshold-voltage loss가 생긴다. 이 때문에 “BL에 높은 전압을 걸었다”와 “storage node가 같은 높은 전압까지 충전되었다”는 같은 말이 아니다.[1,2]

### (2) Threshold-voltage loss와 boosted word line

nMOS access transistor가 켜져 있어도 gate-to-source 전압이 문턱전압보다 작아지면 전류가 급격히 줄어든다. 단순한 pass-transistor 관점에서 high level을 전달할 때 storage node의 최종 전압은 다음보다 높아지기 어렵다.

$$
V_\mathrm{storage}
\lesssim
V_\mathrm{WL}-V_\mathrm{th}
$$

따라서 $V_\mathrm{WL}=V_\mathrm{DD}$만 사용하면 storage node가 충분히 높은 전압에 도달하지 못할 수 있다. DRAM은 charge pump나 bootstrap을 사용해 선택된 WL을 내부 boosted voltage $V_\mathrm{PP}$로 올리는 방법을 사용한다.

$$
V_\mathrm{PP}>V_\mathrm{DD}+V_\mathrm{th}
$$

라는 표현은 full high level을 전달하기 위한 개념적 조건이다. 실제 회로에서는 body effect, transient $V_\mathrm{th}$, series resistance, boosted voltage의 rise·fall time과 oxide reliability를 함께 고려한다. WL boost는 writeability를 개선하지만, unselected cell의 gate stress와 leakage·power·전원 생성 회로를 추가한다.[2,3]

### (3) Write 성능을 어떻게 판단하는가

Write가 성공했다는 것은 BL이 목표 전압에 도달했다는 뜻이 아니라, 정해진 pulse가 끝났을 때 storage node가 다음 read에서 원하는 상태로 판정될 만큼 충분히 변했다는 뜻이다. 온도와 process가 바뀌면 $V_\mathrm{th}$와 on-current가 달라져 같은 WL pulse도 다른 결과를 낸다.

!!! info "[Measurement]"
    선택된 cell에 데이터 0과 1을 각각 쓰면서 $V_\mathrm{BL}$, $V_\mathrm{WL}$, $V_\mathrm{storage}$를 동시에 기록한다. write time은 지정한 storage-node 판정 전압 $V_\mathrm{trip}$을 처음 통과하는 시점으로 정의할 수 있다.

    $$
    t_\mathrm{write}
    =
    t\left(V_\mathrm{storage}=V_\mathrm{trip}\right)
    -t_\mathrm{WL,50\%}
    $$

    보고할 때에는 어느 방향의 write인지, $V_\mathrm{trip}$을 어떤 inverter 또는 sense 기준으로 정했는지, WL boost의 크기와 pulse width, $V_\mathrm{DD}$·온도·bit-line load를 함께 적는다. `write success`는 pulse 종료 시점의 상태가 판정 기준을 통과하는지로 별도 집계한다.[2,3]

!!! warning "[Interpretation Caveat]"
    높은 $V_\mathrm{PP}$가 항상 좋은 write assist는 아니다. 더 강한 access transistor는 write에는 유리하지만, gate oxide stress와 standby leakage, half-selected cell disturbance를 키울 수 있다. write time을 줄인 결과를 retention과 reliability를 포함한 전체 동작 개선으로 해석하지 않는다.[2,3]

## 4. DRAM Read와 charge sharing

DRAM read의 핵심은 capacitor에 저장된 전하를 직접 digital level로 읽는 것이 아니라, 훨씬 큰 bit-line capacitance와 잠깐 charge sharing하여 작은 voltage perturbation을 만드는 것이다. sense amplifier는 이 작은 차이를 증폭한다.[2,4,5]

### (1) Bit line을 $V_\mathrm{DD}/2$로 precharge하는 이유

읽기 전에는 BL과 보수 bit-line $\overline{\mathrm{BL}}$을 보통 $V_\mathrm{pre}=V_\mathrm{DD}/2$에 맞추고 equalize한다. 이렇게 하면 cell이 높은 전하 상태이든 낮은 전하 상태이든 한 방향으로만 큰 전압을 전달하지 않고, 어느 쪽으로도 작은 차이를 만들 수 있다.

이 초기화가 끝나면 precharge transistor를 끄고 BL을 부유시킨다. 이후 WL을 켜면 선택된 cell capacitor와 BL capacitance 사이에 전하가 공유된다. 다른 reference bit-line은 $V_\mathrm{pre}$ 근처에 남아 target line과 비교 기준을 제공한다.[2,5]

### (2) Charge-sharing 식의 유도

단순 모델에서 bit-line capacitance를 $C_\mathrm{BL}$, cell capacitance를 $C_\mathrm{cell}$, precharge 전압을 $V_\mathrm{pre}$, cell capacitor의 초기 전압을 $V_\mathrm{cell}$이라 하자. WL을 켠 직후 leakage와 sense-amplifier loading을 무시하면 charge conservation으로

$$
C_\mathrm{BL}V_\mathrm{pre}
+C_\mathrm{cell}V_\mathrm{cell}
=
\left(C_\mathrm{BL}+C_\mathrm{cell}\right)V_\mathrm{BL}'
$$

이다. 따라서 charge sharing 뒤의 BL 전압은

$$
V_\mathrm{BL}'
=
\frac{C_\mathrm{BL}V_\mathrm{pre}+C_\mathrm{cell}V_\mathrm{cell}}
{C_\mathrm{BL}+C_\mathrm{cell}}
$$

가 된다. precharge 상태에서 변한 sensing signal은

$$
\Delta V_\mathrm{BL}
=
V_\mathrm{BL}'-V_\mathrm{pre}
=
\frac{C_\mathrm{cell}}
{C_\mathrm{BL}+C_\mathrm{cell}}
\left(V_\mathrm{cell}-V_\mathrm{pre}\right)
$$

이다.[2,4,5]

이 식에서 가장 중요한 비율은 $C_\mathrm{cell}/C_\mathrm{BL}$이다. 보통 $C_\mathrm{BL}\gg C_\mathrm{cell}$이므로 cell이 $V_\mathrm{DD}$ 또는 0 V에 가까운 상태여도 BL 변화는 작다. 예를 들어 cell capacitance를 키우거나 bit line을 짧게 하여 $C_\mathrm{BL}$을 줄이면 signal이 커지지만, capacitor 면적 또는 peripheral circuit 수가 증가한다.[2,4,5]

### (3) 작은 signal과 sensing margin

실제 sense amplifier 입력은 이상식의 $\Delta V_\mathrm{BL}$만 받지 않는다. bit-line leakage, adjacent-line coupling, WL coupling, precharge imbalance, sense-amplifier offset과 thermal·supply noise가 함께 들어온다. 따라서 판정에 필요한 최소 신호를 $\Delta V_\mathrm{req}$라 하면 개념적으로

$$
|\Delta V_\mathrm{BL}|
>
|V_\mathrm{OS}|+V_\mathrm{noise}+\Delta V_\mathrm{margin}
$$

을 만족해야 한다. $V_\mathrm{OS}$는 두 입력이 같아도 실제 mismatch 때문에 sense amplifier가 한쪽을 먼저 선택하는 입력 offset이다. 이 부등식은 특정 제품의 보편적 spec 식이 아니라, 왜 cell capacitance·bit-line capacitance·offset을 함께 봐야 하는지 보여주는 1차 설계 기준이다.[5,6]

### (4) Destructive read와 restore

WL을 켜면 cell capacitor의 전하가 BL과 공유되므로, 읽기 뒤 cell의 원래 전압은 그대로 남지 않는다. 이를 **destructive read**라고 한다. Sense amplifier가 한쪽 BL을 0 V, 다른 쪽을 $V_\mathrm{DD}$로 재생(regenerate)하면 access transistor가 켜진 동안 그 full-swing 전압이 storage capacitor로 되돌아간다. 이 단계가 **restore**이다.[1–5]

따라서 DRAM의 read는 다음 세 동작을 하나의 연속 과정으로 봐야 한다.

1. cell 전하가 BL에 작은 차이를 만든다.
2. sense amplifier가 작은 차이를 full-swing으로 증폭한다.
3. 증폭된 값이 cell capacitor에 다시 저장된다.

restore가 끝나기 전에 WL을 끄거나 precharge를 시작하면, row의 일부 cell이 충분히 충전되지 않아 read 직후 데이터가 약해질 수 있다. 이것이 row activation 뒤 precharge까지 최소 시간을 두는 물리적 이유 중 하나이다.[2–5]

!!! info "[Measurement]"
    같은 read waveform에서 (i) precharge·equalization 종료, (ii) WL의 50% crossing, (iii) BL과 $\overline{\mathrm{BL}}$의 차전압 형성, (iv) sense-amplifier enable, (v) full-swing 완료, (vi) WL deactivation과 restore 완료를 표시한다. 대표 정량 지표는

    $$
    \Delta V_\mathrm{BL}(t)
    =
    V_\mathrm{BL}(t)-V_{\overline{\mathrm{BL}}}(t),
    \qquad
    t_\mathrm{sense}
    =
    t_{\mathrm{SA,out},50\%}-t_{\mathrm{WL},50\%}
    $$

    로 둘 수 있다. $V_\mathrm{OS}$, bit-line load, cell data polarity, sense-amplifier enable timing, $V_\mathrm{DD}$와 온도를 고정해 sensing failure와 cell retention failure를 분리한다.[2,5,6]

## 5. Sense amplifier, restore와 precharge

### (1) Cross-coupled latch형 sense amplifier

DRAM의 대표적인 bit-line sense amplifier (BLSA)는 두 bit-line에 연결된 cross-coupled nMOS·pMOS latch로 이해할 수 있다. 두 입력이 모두 $V_\mathrm{DD}/2$일 때는 어느 쪽도 강하게 선택하지 않지만, charge sharing으로 작은 차이가 생긴 뒤 sense-enable signal을 넣으면 positive feedback이 그 차이를 빠르게 키운다.[2,5]

일반적인 순서는 다음과 같다.

1. 두 bit-line을 $V_\mathrm{DD}/2$로 precharge하고 equalize한다.
2. precharge 회로를 끄고 WL을 켠다.
3. cell과 target BL이 charge sharing하여 작은 차이를 만든다.
4. n-sense amplifier를 먼저 켜 낮은 쪽을 더 낮춘다.
5. p-sense amplifier를 켜 높은 쪽을 $V_\mathrm{DD}$로 올린다.
6. full-swing BL이 cell capacitor를 restore한다.

실제 회로는 두 latch를 반드시 이 순서로만 켜는 것은 아니며, sense timing과 voltage swing을 줄이는 회로도 존재한다. beginner가 기억할 핵심은 sense amplifier가 단순한 출력 buffer가 아니라 **판정·증폭·restore**를 동시에 담당한다는 점이다.[2,3]

### (2) Reference bit line과 differential sensing

Target BL 하나의 절대 전압만 읽으면 공급전압, 온도, leakage와 global noise 변화에 취약하다. 그래서 complementary BL, dummy cell 또는 reference circuit을 사용해 “현재 cell이 precharge 기준보다 어느 방향으로 얼마나 벗어났는가”를 비교한다. Folded bit-line에서는 pair의 양쪽 선이 가까이 있어 공통으로 들어오는 disturbance를 상쇄하기 쉽고, open bit-line에서는 인접 array의 선이 reference 역할을 하므로 구조적 imbalance를 보정해야 한다.[2,6,7]

여기서 reference bit line은 실제 데이터를 저장하지 않는다고 단정하면 안 된다. 어떤 array에서는 반대쪽 bit-line도 다른 cell들을 연결한 실제 배선이고, 어떤 구조에서는 dummy 또는 reference 회로가 사용된다. 문헌의 `reference line`이라는 표현은 회로 topology를 확인하면서 해석해야 한다.[2,6]

### (3) Sense-amplifier enable timing과 offset

Sense amplifier를 너무 일찍 켜면 cell signal보다 $V_\mathrm{OS}$와 noise가 커서 잘못된 방향으로 latch될 수 있다. 너무 늦게 켜면 sensing latency와 leakage·dynamic energy가 증가한다. 또한 input pair transistor의 $V_\mathrm{th}$ mismatch, layout asymmetry와 parasitic capacitance imbalance가 offset을 만든다.[5,6]

따라서 DRAM scaling에서 sense amplifier는 cell이 작아지는 문제와 별개로 중요하다. cell에서 만들어지는 signal은 작아지고, pair transistor도 작아져 mismatch가 커질 수 있기 때문이다. “cell capacitor를 더 크게 만들면 offset 문제가 모두 해결된다”가 아니라, cell signal과 sense-amplifier offset의 **분포**를 함께 검증해야 한다.[5,6]

### (4) Precharge와 equalization

한 row의 동작이 끝나면 다음 row activation을 위해 BL과 $\overline{\mathrm{BL}}$을 다시 기준 전압으로 되돌린다. 이 초기화가 precharge이고, differential pair 사이의 잔류 차이를 줄이는 동작이 equalization이다. 보통 precharge transistor와 equalization transistor, $V_\mathrm{DD}/2$ bias 회로가 함께 동작한다.[2,3]

Residual bit-line imbalance가 남아 있으면 다음 read에서 cell이 만든 $\Delta V_\mathrm{BL}$에 offset이 더해진다. 예를 들어 precharge가 끝났다고 생각했지만 $V_\mathrm{BL}=V_\mathrm{pre}+\epsilon$인 상태라면, 실제 sense amplifier 입력은 cell signal과 $\epsilon$의 합이다. $\epsilon$이 data polarity에 따라 유리하거나 불리할 수 있으므로, precharge time과 equalization time도 sensing margin의 일부이다.[2,5]

!!! warning "[Interpretation Caveat]"
    “sense amplifier가 full swing을 만들었다”는 것은 내부 latch가 한 논리 상태를 선택했다는 뜻이지, 처음 cell 데이터가 반드시 맞았다는 뜻은 아니다. offset이 큰 상태에서 너무 이르게 enable하면 full-swing **오판**도 빠르게 만들어질 수 있다. sensing correctness는 enable 전 입력 신호와 reference, offset을 함께 확인해야 한다.[5,6]

## 6. Refresh와 retention time

### (1) 왜 refresh가 필요한가

DRAM capacitor는 완벽한 절연체가 아니다. access transistor가 꺼져 있어도 storage node의 전하는 여러 경로로 변한다. 대표적인 경로는 다음과 같다.[2,4,8–10]

| 누설 경로 | 물리적 설명 | 영향을 크게 받는 조건 |
| --- | --- | --- |
| **Junction leakage** | storage node와 access transistor의 source·drain junction을 통한 누설 | junction 면적·둘레, defect, reverse bias, 온도 |
| **Subthreshold leakage** | WL이 꺼져도 access transistor channel에 흐르는 약한 반전 전류 | $V_\mathrm{th}$, WL bias, $V_\mathrm{DD}$, 온도 |
| **Gate-induced drain leakage (GIDL)** | gate·drain 가장자리의 큰 전기장에서 생기는 band-to-band 또는 defect-assisted tunneling | gate bias, drain voltage, edge field, trap |
| **Dielectric leakage** | storage capacitor dielectric을 통한 직접 또는 결함 보조 수송 | dielectric thickness, field, defect, temperature |
| **Trap-assisted tunneling (TAT)** | dielectric 또는 interface trap을 중간 상태로 이용하는 tunneling | trap density, field, stress history |

저장 1과 0은 leakage 경로가 완전히 대칭이 아닐 수 있다. 예를 들어 cell plate 전위, WL의 negative bias, storage node의 polarity에 따라 access transistor의 off-state $V_\mathrm{GS}$와 drain field가 달라진다. 그래서 retention은 데이터 패턴, 인접 WL·BL과 온도에 의존할 수 있다.[2,8–10]

### (2) Retention time의 정의와 1차 근사

**Retention time** $t_\mathrm{ret}$은 refresh 없이 저장된 데이터가 정해진 판정 기준을 만족하는 최대 시간이다. “전하가 0이 되는 시간”이 아니라, charge sharing 뒤 sense amplifier가 데이터를 더 이상 신뢰성 있게 구별하지 못하는 시점으로 정의해야 한다.[8]

누설 전류의 크기를 일정한 $I_\mathrm{leak}$으로 근사하고 허용 가능한 전하 변화량을 $\Delta Q_\mathrm{allow}=C_\mathrm{cell}\Delta V_\mathrm{allow}$로 두면

$$
t_\mathrm{ret}
\approx
\frac{C_\mathrm{cell}\Delta V_\mathrm{allow}}
{I_\mathrm{leak}}
$$

이다. 실제로는 leakage가 voltage·temperature·time에 따라 변하므로

$$
C_\mathrm{cell}\frac{dV_\mathrm{cell}}{dt}
=
-I_\mathrm{leak}(V_\mathrm{cell},T,t)
$$

를 풀어야 한다. 첫 식은 capacitor가 크고 leakage가 작을수록 retention이 길어진다는 방향을 보여주는 근사식이고, 모든 DRAM cell의 retention을 정확히 예측하는 보편식은 아니다.[2,8–10]

### (3) Auto-refresh, self-refresh와 refresh scheduling

외부 memory controller가 **auto-refresh** command를 주기적으로 보내면 DRAM 내부 refresh counter가 대상 row를 정하고, 해당 row를 activate·sense·restore한다. **Self-refresh**에서는 외부 clock 또는 명령 활동이 줄어든 저전력 상태에서 DRAM 내부 oscillator와 counter가 refresh를 계속한다. 현대 SDRAM interface에서는 refresh command가 일정한 평균 간격 $t_\mathrm{REFI}$로 발행되고, refresh operation이 점유하는 시간은 $t_\mathrm{RFC}$로 제한된다.[2,3,11]

Refresh를 구현하는 방법을 동작 범위로 나누면 다음과 같다.

| 방식 | 핵심 아이디어 | 장점과 비용 |
| --- | --- | --- |
| **Distributed refresh** | 각 refresh command에서 일부 row를 처리하고 전체 row를 시간에 걸쳐 분산 | 순간 정지 시간을 줄이지만 controller와 timing 관리가 계속 필요하다. |
| **Burst refresh** | 여러 row 또는 여러 refresh 동작을 한 구간에 몰아서 수행 | 한동안 refresh 간섭을 줄일 수 있지만 refresh 구간의 blocking이 커질 수 있다. |
| **Auto-refresh** | controller가 명령을 보내고 DRAM 내부 counter가 row 순서를 관리 | 외부가 개별 row 주소를 관리하지 않아도 되지만 interface가 정한 간격을 지켜야 한다. |
| **Self-refresh** | DRAM 내부 timing·counter가 저전력 상태에서 refresh | 대기 전력은 낮출 수 있지만 내부 oscillator와 온도 조건을 관리해야 한다. |

제품별 refresh command와 granularity는 DDR 세대와 density에 따라 다르다. 예를 들어 DDR5에서는 all-bank refresh와 same-bank refresh가 구분되고, 대상 bank가 idle이어야 하며 refresh 동안 정해진 recovery time이 필요하다. 이 사실은 “refresh는 항상 전체 chip을 완전히 멈춘다”는 단순화가 모든 interface에 그대로 적용되지 않음을 보여준다.[11]

### (4) Data-pattern dependence, VRT와 retention tail

DRAM cell의 retention time은 모든 cell에서 같은 값이 아니다. 제조 variation으로 access transistor와 capacitor leakage가 cell마다 달라지고, 인접 bit-line·word-line coupling 때문에 저장된 주변 data pattern에 따라서도 sense noise가 달라질 수 있다. 또한 trap의 charge state가 바뀌면 같은 cell의 leakage가 시간에 따라 여러 상태를 오가는 **variable retention time (VRT)**가 나타날 수 있다.[8–10]

따라서 retention-time distribution은 중심 부분만 보고 판단하면 안 된다. 대부분의 cell이 오래 버텨도, 작은 확률의 high-leakage tail cell이 전체 refresh interval을 결정할 수 있다. 실제 제품은 이 tail과 온도 상승, voltage 변화, data pattern, refresh timing margin을 함께 고려해 보수적인 refresh 조건을 정한다.[8–10]

!!! info "[Measurement]"
    먼저 한 row에 정해진 data pattern을 쓰고, 일정 시간 동안 refresh를 막은 뒤 read하여 오류가 처음 나타나는 시간을 측정한다. `retention failure`는 sense amplifier 출력이 기대값과 달라지는 시점으로 정의할 수 있다. cell 또는 row별 결과에서

    $$
    t_\mathrm{ret}
    =
    \max\left\{t:
    P_\mathrm{bit\ error}(t)\le P_\mathrm{target}
    \right\}
    $$

    를 사용할 수 있다. 온도, $V_\mathrm{DD}$, data pattern, 인접 row activity, refresh interval과 read 판정 기준을 함께 기록하고 평균·percentile·최악 tail을 따로 보고한다.

!!! warning "[Interpretation Caveat]"
    retention failure가 관찰되었다고 해서 곧바로 capacitor dielectric leakage라고 결론내리지 않는다. access transistor의 subthreshold leakage·GIDL, junction defect, bit-line coupling, sense offset, precharge imbalance와 측정 장비의 noise도 같은 read error를 만들 수 있다. 저장 node 전류, gate·junction 전류, temperature dependence와 구조별 소자 test를 함께 사용해 경로를 분리해야 한다.[8–10]

## 7. DRAM 명령과 timing parameters

### (1) ACTIVATE, READ, WRITE와 PRECHARGE

현대 SDRAM의 기본 명령은 셀 하나를 바로 선택하는 명령이 아니라, row를 열고 그 안에서 column을 고르는 단계로 나뉜다.[2–5,11]

| 명령 | 내부 동작 | beginner가 기억할 핵심 |
| --- | --- | --- |
| **ACTIVATE** | bank에서 row address의 WL을 켜고 charge sharing·sensing·restore 수행 | row를 row buffer로 연다. |
| **READ** | 열린 row의 row buffer에서 column을 선택해 외부로 출력 | 이미 열린 row라면 column access만 수행할 수 있다. |
| **WRITE** | 열린 row의 선택 column에 입력 데이터를 전달하고 row buffer·cell을 갱신 | write driver가 sense/row-buffer 경로를 덮어쓴다. |
| **PRECHARGE** | 열린 row를 닫고 BL pair를 다음 access 기준 전압으로 초기화 | 다른 row를 열 수 있게 bit-line을 준비한다. |

구형 asynchronous DRAM에서는 row address와 column address를 같은 address pin에 시간차로 넣고 **Row Address Strobe (RAS)**와 **Column Address Strobe (CAS)**로 각각 latch하는 address multiplexing이 핵심이었다. 현대 synchronous DDR interface에서는 `ACTIVATE`, `READ`, `WRITE`, `PRECHARGE`가 clocked command encoding으로 전달되지만, 이름에 남은 RAS·CAS·WE가 가리키는 row·column·write 기능의 역사적 관계를 이해하면 timing table을 읽기 쉽다.[2,3,12]

### (2) Row buffer와 row hit·miss·conflict

ACTIVATE가 끝나면 한 row의 데이터가 sense amplifier에 latch된다. 이 sense amplifier 집합을 **row buffer**라고 한다. 같은 bank에서 연속된 column access가 현재 열린 row를 다시 요청하면 **row hit**이고, 추가 ACTIVATE 없이 row buffer에서 column만 선택할 수 있다. 열린 row가 없으면 row closed 상태이며, 다른 row가 이미 열려 있는데 새 row를 요청하면 기존 row를 PRECHARGE한 뒤 새 row를 ACTIVATE해야 하므로 **row conflict**가 된다.[4,5]

| 접근 상태 | 필요한 동작 | 상대적 지연의 물리적 이유 |
| --- | --- | --- |
| Row hit | 열린 row에서 column 선택 | charge sharing·sense·restore를 반복하지 않아 작다. |
| Row closed | ACTIVATE 후 column 접근 | 새 row를 읽어 row buffer에 넣는 시간이 필요하다. |
| Row conflict | 기존 row PRECHARGE → 새 row ACTIVATE → column 접근 | bit-line 초기화와 새 charge sharing·sensing을 모두 수행한다. |

그러므로 DRAM의 “random access”는 SRAM처럼 어느 cell이든 동일한 짧은 내부 경로를 갖는다는 뜻이 아니다. 주소가 어느 bank와 row에 매핑되는지, 직전 access와 같은 row인지에 따라 물리 sequence와 latency가 달라진다. Memory controller는 bank 병렬성과 row hit, queue order, refresh를 함께 고려해 scheduling한다.[4,5]

### (3) 주요 timing parameter의 물리적 의미

제품 data sheet의 timing 이름은 interface마다 조금씩 다르지만, 다음 정의를 기본 연결 고리로 사용할 수 있다.[3–5,11]

| Parameter | 의미 | 대응하는 물리 과정 |
| --- | --- | --- |
| $t_\mathrm{RCD}$ | ACTIVATE 뒤 READ/WRITE를 발행하기까지의 row-to-column delay | WL rise, charge sharing, sense와 row-buffer latch가 충분히 끝나는 시간 |
| $t_\mathrm{CL}$ | READ command에서 첫 data가 출력되기까지의 CAS latency | 열린 row의 column 선택, global path와 I/O pipeline |
| $t_\mathrm{RAS}$ | ACTIVATE 뒤 PRECHARGE가 허용되기 전 row active 최소 시간 | sense-amplifier restore가 cell에 완료될 시간 |
| $t_\mathrm{RP}$ | PRECHARGE command 뒤 다음 ACTIVATE까지 필요한 시간 | BL discharge·equalization·precharge 완료 |
| $t_\mathrm{RC}$ | 같은 bank에서 한 row cycle의 시간 | 대략 $t_\mathrm{RAS}+t_\mathrm{RP}$ |
| $t_\mathrm{WR}$ | WRITE data가 들어간 뒤 PRECHARGE까지 필요한 write recovery | write 데이터가 cell에 확정되고 restore될 시간 |
| $t_\mathrm{RFC}$ | REFRESH command가 bank를 점유하고 회복하는 시간 | 여러 row의 sensing·restore 및 내부 refresh sequence |
| $t_\mathrm{REFI}$ | refresh command 사이의 평균 간격 | retention 조건을 만족하도록 row들을 순환하는 schedule |

특히 $t_\mathrm{CL}$은 cell 내부 sensing 시간과 같지 않다. command가 clocked interface에 들어온 뒤 column mux, global sense amplifier, output register, burst와 data strobe timing이 더해진 결과이다. 반대로 $t_\mathrm{RCD}$도 단순히 WL propagation delay 하나가 아니라, row activation에서 column command가 안전해질 때까지의 interface 규약이다.[2–5]

대략적인 row cycle 관계는

$$
t_\mathrm{RC}
\approx
t_\mathrm{RAS}+t_\mathrm{RP}
$$

로 생각할 수 있다. 실제 data sheet에서는 bank group, read-to-precharge, write-to-read, burst length와 command granularity에 따른 추가 제약이 함께 있으므로 이 식을 모든 timing parameter의 완전한 정의로 사용하면 안 된다.[3,11]

!!! info "[Measurement]"
    timing을 측정할 때에는 시작 사건과 종료 사건을 명시한다. 예를 들어 row-open latency는 ACTIVATE command 수락부터 row buffer output이 안정되는 시점까지, column latency는 READ command 수락부터 첫 data-valid crossing까지 정의할 수 있다.

    $$
    t_\mathrm{RCD,meas}
    =
    t_{\mathrm{SA\ latch,valid}}-t_{\mathrm{ACT\ accepted}},
    \qquad
    t_\mathrm{read,meas}
    =
    t_{\mathrm{DQ\ valid}}-t_{\mathrm{READ\ accepted}}
    $$

    같은 bank의 row hit·closed·conflict를 분리하고, burst length, $V_\mathrm{DD}$, 온도, data pattern, I/O load와 refresh 간섭을 함께 보고한다. data sheet parameter와 waveform에서 직접 추출한 소자 내부 시간을 같은 항목으로 섞지 않는다.[3–5]

## 8. DRAM array와 계층 구조

### (1) Cell, subarray, mat, bank와 bank group

DRAM의 계층은 셀의 전기적 동작과 system address를 연결하는 다리이다.

| 계층 | 의미 | 주로 공유하는 회로 |
| --- | --- | --- |
| Cell | 1T1C 한 개 | WL과 BL의 일부 |
| Subarray 또는 mat | 작은 cell array와 local SA 집합 | row decoder, precharge, local data path |
| Bank | 여러 subarray와 bank-level I/O | row buffer와 global data path |
| Bank group | 여러 bank를 timing·I/O 관점에서 묶은 단위 | bank-group command·bandwidth 자원 |
| Rank | 같은 command를 함께 받고 외부 data word를 구성하는 chip 묶음 | command/address와 DQ width |
| Channel | memory controller와 DRAM module 사이의 독립 interface | command, address, data, clock |

`subarray`, `mat`, `bank`의 정확한 경계는 제조사와 제품에 따라 다르지만, 물리적 원리는 비슷하다. local bit-line이 한 subarray의 row buffer에 연결되고, column decoder가 그중 일부를 좁은 global data line으로 보낸다. global sense amplifier와 bank I/O가 이 데이터를 chip 외부 interface로 전달한다.[4,5]

### (2) Local bit line, global bit line과 I/O circuit

Local BL은 많은 cell이 공유하므로 $C_\mathrm{BL}$이 커지고, 그만큼 charge-sharing signal이 작아진다. 그렇다고 local BL을 무한히 짧게 만들면 sense amplifier와 row decoder를 많이 복제해야 한다. 그래서 DRAM은 local array 안에서 row를 병렬로 sensing한 뒤, 필요한 column만 global data line으로 multiplex한다.[4,5]

이 구조에서 한 row의 모든 cell이 ACTIVATE될 수 있지만, 외부 read/write는 그중 좁은 column slice만 사용한다. **Column multiplexer**는 row buffer에서 어느 column group을 global path에 연결할지 선택하고, **global sense amplifier**는 더 긴 global line에서 작은 차이를 다시 증폭한다. **I/O circuit**은 chip 내부의 병렬 data를 DQ pin, burst와 data strobe에 맞춰 serialize·drive한다.[2–5]

### (3) Address multiplexing과 hierarchical word line

많은 row와 column을 직접 외부 pin에 연결하면 package pin 수가 커진다. DRAM은 address bus를 row와 column이 시간적으로 공유하고, 내부 row-address latch와 column-address latch가 각각 보존하는 address multiplexing을 사용해 pin 수를 줄여 왔다. synchronous DDR에서는 command/address protocol이 세대별로 바뀌었지만, 내부에서 row 선택과 column 선택을 분리한다는 물리 구조는 유지된다.[2,3,12]

큰 어레이의 WL은 저항과 정전용량이 크므로 하나의 decoder output이 전체 길이를 직접 구동하지 않는다. predecoder, local decoder, hierarchical word line과 여러 단계의 WL driver를 사용해 분포된 부하를 나눈다. 이때 word-line resistance는 rise·fall time과 access transistor의 실제 gate voltage를 바꾸고, adjacent WL coupling은 retention과 read disturbance에 영향을 줄 수 있다.[2,3,13]

### (4) Redundancy와 memory controller scheduling

제조 중 일부 row·column에 defect가 생길 수 있으므로 spare row·column과 fuse·remap 회로를 두어 불량 위치를 대체한다. 이 redundancy는 raw cell yield를 product yield로 바꾸는 데 도움이 되지만, 주소 mapping과 repair policy가 추가되어 physical cell 수와 logical capacity가 달라진다.[2,3]

Memory controller는 physical address를 channel·rank·bank group·bank·row·column으로 나누고, queue의 여러 요청을 이 구조에 맞춰 배치한다. 같은 bank의 row hit을 늘리면 $t_\mathrm{RCD}$와 $t_\mathrm{RP}$를 줄일 수 있지만, 한 row를 오래 열어 두면 다른 row의 요청이 conflict로 대기할 수 있다. 따라서 row policy는 항상 “row hit만 최대화”하는 단일 목표가 아니라 latency, bandwidth, energy, fairness와 refresh를 함께 고려한다.[4,5]

## 9. DRAM cell capacitor 기술

### (1) 왜 작은 면적에 충분한 capacitance가 필요한가

Charge-sharing 식에서 $C_\mathrm{cell}$이 작아지면 $\Delta V_\mathrm{BL}$이 작아지고, retention 식에서 같은 leakage가 흐를 때 허용 전하량도 줄어든다. 그러나 cell pitch는 lithography와 array routing이 정하므로 capacitor를 평면 방향으로만 키울 수 없다. DRAM capacitor 공정의 핵심은 작은 footprint 위에 큰 유효 면적과 낮은 leakage를 만드는 것이다.[2,14,15]

평행판 capacitor의 1차 근사에서는

$$
C
\approx
\frac{\varepsilon_0\varepsilon_r A}
{t_\mathrm{ox}}
$$

이다. $A$는 두 electrode가 마주 보는 유효 면적, $t_\mathrm{ox}$는 dielectric physical thickness, $\varepsilon_r$는 relative permittivity이다. 실제 3D DRAM capacitor에서는 sidewall·curved surface·fringing field·전극 저항과 interface layer가 포함되므로 이 식은 방향과 설계 trade-off를 보여주는 근사식이다.[14,15]

### (2) Stack capacitor와 trench capacitor

| 구조 | capacitor를 만드는 위치 | scaling 관점 |
| --- | --- | --- |
| **Stack capacitor** | access transistor와 bit line 위쪽에 높은 3D 전극을 쌓음 | 작은 footprint에서 cylinder·pillar 면적을 늘릴 수 있지만 높은 aspect ratio의 deposition과 patterning이 어렵다. |
| **Trench capacitor** | silicon substrate 안쪽으로 깊은 trench를 파서 전극과 dielectric을 형성 | 평면 면적을 덜 차지하지만 deep etch, sidewall defect, fill과 junction isolation이 어렵다. |

Stack 구조의 cylinder와 pillar는 수직 sidewall을 이용해 footprint보다 훨씬 큰 electrode area를 만들고, trench 구조는 substrate 깊이를 이용한다. 1988년 고밀도 DRAM 연구도 작은 cell area 안에 큰 capacitance를 확보하기 위한 trench cell과 open-bit-line architecture를 함께 다뤘다. 이는 capacitor와 array architecture가 서로 독립된 문제가 아니라는 점을 보여준다.[7]

### (3) High-k dielectric, EOT와 재료 trade-off

Dielectric의 $\varepsilon_r$를 높이면 동일한 physical thickness와 footprint에서 capacitance density를 높일 수 있다. 또는 같은 capacitance를 더 두꺼운 physical dielectric으로 만들 수 있어 direct tunneling을 줄일 여지가 생긴다. 이때 **equivalent oxide thickness (EOT)**는 같은 capacitance를 갖는 SiO$_2$ 기준 두께로, 물리적 두께와 같은 개념이 아니다.[14,15]

하지만 high-k가 leakage를 자동으로 없애지는 않는다. 높은 dielectric constant, band offset, defect density, crystallinity, electrode interface와 thermal budget이 함께 결정되며, trap-assisted tunneling·Poole–Frenkel emission·Schottky emission 같은 추가 수송이 나타날 수 있다. 즉, capacitance를 키우는 재료 선택은 leakage·breakdown·reliability와 함께 평가한다.[14,15]

### (4) Aspect ratio, conformality와 capacitor reliability

3D capacitor가 충분한 면적을 가지려면 깊고 좁은 구조에 dielectric과 electrode를 균일하게 입혀야 한다. **Atomic layer deposition (ALD)**는 surface reaction을 cycle 단위로 제어하여 높은 aspect ratio 구조에서 conformal film을 만들 수 있어 DRAM capacitor 재료에 중요하다. 그러나 deposition이 균일하지 않으면 local thickness가 얇은 부분에서 leakage와 electric field가 커진다.[14,15]

Capacitor의 주요 reliability 문제는 dielectric breakdown과 time-dependent dielectric breakdown (TDDB)이다. 전기장과 defect가 누적되면 leakage가 증가하고, 결국 storage charge가 refresh interval 안에 유지되지 않을 수 있다. 따라서 capacitor 공정에서 capacitance만 측정하면 부족하며, leakage distribution, breakdown field, stress 뒤의 capacitance·leakage 변화와 cell retention을 함께 봐야 한다.[14,15]

!!! info "[Measurement]"
    capacitor test structure에서 작은 AC 신호로 $C$–$V$를 측정하고, 동일한 electrode area로 leakage $I$–$V$와 breakdown·stress 특성을 측정한다. 저주파 또는 지정 frequency에서 추출한 capacitance density는

    $$
    C_\mathrm{density}
    =
    \frac{C}{A_\mathrm{footprint}}
    $$

    로 계산할 수 있다. DRAM cell에 적용할 때에는 capacitor 단독의 $C$와 leakage를 charge-sharing signal, retention time, bit-line parasitic과 연결해 확인한다. physical thickness, EOT, electrode material, ALD cycle, stress voltage·time과 breakdown criterion을 함께 기록한다.[14,15]

## 10. Access transistor와 DRAM 공정 기술

### (1) Access transistor가 만족해야 할 조건

Access transistor는 쓰기 때는 강하게 켜져야 하고, retention 때는 거의 꺼져 있어야 한다. 따라서 다음 요구가 서로 충돌한다.

| 요구 조건 | 필요한 이유 | 지나치게 강화하면 생기는 문제 |
| --- | --- | --- |
| 높은 on-current | charge sharing, write와 restore를 빠르게 한다. | 큰 device 또는 낮은 $V_\mathrm{th}$는 area·gate leakage·standby leakage를 늘릴 수 있다. |
| 낮은 off-current | storage charge가 새는 속도를 줄인다. | $V_\mathrm{th}$를 높이면 write와 read 속도가 줄어든다. |
| 낮은 junction leakage | storage node의 직접 전하 손실을 줄인다. | junction engineering이 drive와 breakdown에 영향을 준다. |
| 충분한 breakdown voltage | boosted WL과 cell plate bias를 견딘다. | 두꺼운 dielectric·큰 spacing은 area와 parasitic을 늘릴 수 있다. |
| 작은 $V_\mathrm{th}$ variation | cell 간 sensing·write 분포를 줄인다. | 강한 drive와 낮은 variation을 동시에 얻기 어렵다. |

이 trade-off 때문에 access transistor를 강하게 만드는 것이 항상 DRAM 전체 성능을 개선하지는 않는다. on-current가 커지면 write·restore가 빨라지지만, off-state leakage가 커져 refresh energy 또는 retention tail이 나빠질 수 있다.[2,8–10]

### (2) RCAT, BCAT와 buried word line

평면 channel 길이를 짧게 줄이면 source와 drain 전기장이 서로 결합해 short-channel effect가 커진다. DRAM은 array pitch 안에서 충분한 유효 channel length와 on-current를 얻기 위해 channel을 silicon 안으로 파거나 word line을 buried 구조로 넣는 공정 기술을 사용해 왔다.

- **Recessed-channel array transistor (RCAT)**은 channel을 recess 안으로 형성하여 제한된 평면 길이에서 유효 channel path와 gate control을 확보하려는 구조이다.
- **Buried-channel-array transistor (BCAT)**은 channel과 gate의 일부를 silicon 또는 recess 내부에 배치해 short-channel effect와 array pitch 문제를 완화하려는 계열이다.
- **Buried word line (BWL)**은 WL을 cell 구조 안쪽에 배치하여 bit-line·capacitor와의 배선 공간을 줄이고 작은 cell pitch를 목표로 하는 방식이다.
- Fin 또는 vertical access transistor는 channel의 수직 면적과 gate control을 활용하려는 확장 개념이지만, high-aspect-ratio 공정과 variation 관리가 함께 필요하다.

RCAT 연구에서는 channel orientation과 recess 형상이 cell transistor drivability와 retention·write 조건에 영향을 주는 것으로 보고되었고, BCAT 연구에서는 recess depth, junction depth, fin width와 fillet radius의 변동이 $V_\mathrm{th}$, subthreshold swing, on/off ratio와 DIBL을 바꿀 수 있음이 분석되었다. 따라서 구조 이름을 외우는 것보다 **channel을 어디에 만들었고, 그 결과 전기장·누설·기생 성분이 어떻게 바뀌는지**가 중요하다.[18,19]

### (3) Short-channel effect, DIBL과 subthreshold swing

Access transistor가 짧아지면 drain voltage가 source-side barrier에 영향을 주는 **drain-induced barrier lowering (DIBL)**이 커질 수 있다. 그러면 같은 $V_\mathrm{GS}$에서 off-state current가 증가하고, storage node의 retention이 나빠질 수 있다. **Subthreshold swing (SS)**은 off에서 on으로 이동할 때 gate voltage가 current를 몇 decade 바꾸는지 나타내는 지표이다.

!!! info "[Measurement]"
    cell transistor test structure에서 여러 $V_\mathrm{DS}$와 $V_\mathrm{GS}$에 대해 $I_\mathrm{D}$를 측정한다. 일정한 기준 전류에서 추출한 threshold voltage를 $V_\mathrm{th}(V_\mathrm{DS})$라 두면

    $$
    \mathrm{DIBL}
    =
    \frac{V_\mathrm{th}(V_\mathrm{DS,low})
    -V_\mathrm{th}(V_\mathrm{DS,high})}
    {V_\mathrm{DS,high}-V_\mathrm{DS,low}}
    $$

    로 정의할 수 있다. Subthreshold swing은 지정한 subthreshold fitting window에서

    $$
    \mathrm{SS}
    =
    \left(\frac{d\log_{10}|I_\mathrm{D}|}{dV_\mathrm{GS}}\right)^{-1}
    $$

    로 추출한다. $V_\mathrm{DS}$, temperature, reference current, fitting window, access transistor geometry를 고정하여 비교한다.[18,19]

### (4) Word-line resistance와 bit-line parasitics

WL resistance가 크면 선택된 access transistor의 gate voltage가 row 위치에 따라 늦게 오르거나 작아질 수 있다. BL resistance와 capacitance가 크면 cell과 sense amplifier 사이의 charge sharing과 full-swing restore가 느려진다. Contact resistance는 write current와 restore current를 줄이고, interconnect coupling은 reference imbalance와 sensing offset을 키운다.[2–5]

이 효과가 있기 때문에 DRAM의 속도를 cell transistor의 $I_\mathrm{ON}$ 하나로 예측할 수 없다. 같은 transistor라도 bit-line에 연결된 cell 수, local·global data path 길이, contact·via 저항과 sense-amplifier 위치가 달라지면 $t_\mathrm{RCD}$와 $t_\mathrm{RP}$가 달라진다. 짧은 bit-line 구조는 sensing을 빠르게 만들 수 있지만, 더 많은 local peripheral circuit으로 density를 희생할 수 있다.[4,5]

### (5) Cell transistor와 peripheral transistor의 설계 차이

Cell transistor는 작은 pitch, 낮은 off-current, low junction leakage와 retention을 우선한다. 반면 peripheral transistor는 decoder·sense amplifier·I/O에서 높은 speed, 충분한 voltage swing, drive current와 reliability를 우선할 수 있다. DRAM chip이 하나의 transistor type만으로 구성된다고 가정하면 boosted WL, cell plate, sense latch와 I/O driver의 서로 다른 요구를 설명하기 어렵다.[2,3]

!!! warning "[Interpretation Caveat]"
    RCAT·BCAT·BWL이라는 이름만으로 성능 우열을 정하지 않는다. 서로 다른 논문은 cell pitch, capacitor 구조, $V_\mathrm{PP}$, bit-line load, temperature, data pattern과 sensing criterion이 다를 수 있다. 구조 비교는 같은 array organization과 같은 retention·write·read 지표를 사용하고, 공정 variation과 reliability까지 포함해야 한다.[18,19]

## 11. 요약

- DRAM은 보통 access transistor와 storage capacitor로 한 bit를 저장하며, capacitor 전하가 leakage로 변하므로 refresh가 필요하다.
- Write는 BL을 구동하고 WL로 access transistor를 켜 capacitor를 충전·방전하는 과정이다. nMOS의 threshold-voltage loss 때문에 boosted WL이 사용될 수 있다.
- Read는 BL을 $V_\mathrm{DD}/2$로 precharge한 뒤 cell과 bit-line capacitance를 charge sharing하여 작은 $\Delta V_\mathrm{BL}$을 만든다.
- Sense amplifier는 작은 differential signal을 full-swing으로 키우고, destructive read 뒤 cell 전하를 restore한다.
- Precharge와 equalization의 잔류 imbalance는 다음 sensing의 offset처럼 작용하므로 read timing의 일부로 관리해야 한다.
- Retention time은 capacitor와 leakage만의 고정 상수가 아니다. access transistor, junction, dielectric, GIDL·TAT, temperature, data pattern, VRT와 tail distribution이 함께 결정한다.
- ACTIVATE는 row를 row buffer에 열고, READ·WRITE는 열린 row의 column을 접근하며, PRECHARGE는 다음 row를 위해 bit-line을 초기화한다.
- $t_\mathrm{RCD}$, $t_\mathrm{CL}$, $t_\mathrm{RAS}$, $t_\mathrm{RP}$와 $t_\mathrm{RFC}$는 각각 charge sharing·sensing·restore·precharge·refresh sequence와 연결된 interface timing이다.
- DRAM의 density와 성능은 cell뿐 아니라 subarray·bank·global data line·I/O·controller scheduling과 redundancy를 포함한 계층 구조의 결과이다.
- capacitor는 작은 footprint에서 큰 유효 면적과 낮은 leakage를 얻어야 하며, access transistor는 높은 on-current와 낮은 off-current를 동시에 요구한다.

## 12. 참고문헌

1. R. H. Dennard, F. H. Gaensslen, H.-N. Yu, V. L. Rideout, E. Bassous, and A. R. LeBlanc, “Field-Effect Transistor Memory,” U.S. Patent 3,387,286 (1968). [Google Patents](https://patents.google.com/patent/US3387286A/en).
2. B. Keeth and R. J. Baker, *DRAM Circuit Design: A Tutorial*, Wiley-IEEE Press (2001), ISBN 0-7803-6014-1. [Google Books](https://books.google.com/books?id=CTVGAQAAIAAJ).
3. B. Keeth, R. J. Baker, B. Johnson, and F. Lin, *DRAM Circuit Design: Fundamental and High-Speed Topics*, 2nd ed., Wiley-IEEE Press (2007), ISBN 978-0-470-18475-2. [Publisher information](https://www.wiley.com/en-us/DRAM+Circuit+Design%3A+Fundamental+and+High-Speed+Topics%2C+2nd+Edition-p-9780470184752).
4. B. L. Jacob, S. W. Ng, and D. T. Wang, *Memory Systems: Cache, DRAM, Disk*, Morgan Kaufmann (2008), ISBN 978-0-12-379751-3. [Publisher information](https://www.sciencedirect.com/book/9780123797513/memory-systems).
5. K. K. Chang, *Understanding and Improving the Latency of DRAM-Based Memory Systems*, Ph.D. dissertation, Carnegie Mellon University (2017). [University repository PDF](https://research.ece.cmu.edu/safari/thesis/kchang_dissertation.pdf).
6. K. M. Koo, W. Y. Chung, S. Y. Lee, G. H. Yoon, and W. Y. Choi, “Modeling of Statistical Variation Effects on DRAM Sense Amplifier Offset Voltage,” *Micromachines* **12**(10), 1145 (2021). [DOI: 10.3390/mi12101145](https://doi.org/10.3390/mi12101145).
7. M. Inoue, T. Yamada, H. Kotani, H. Yamauchi, A. Fujiwara, J. Matsushita, H. Akamatsu, M. Fukumoto, M. Kubota, I. Nakao, N. Aoi, G. Fuse, S.-I. Ogawa, S. Odanaka, A. Ueno, and H. Yamamoto, “A 16-Mbit DRAM with a Relaxed Sense-Amplifier-Pitch Open-Bit-Line Architecture,” *IEEE Journal of Solid-State Circuits* **23**(5), 1104–1112 (1988). [DOI: 10.1109/4.5931](https://doi.org/10.1109/4.5931).
8. J. Liu, B. Jaiyen, Y. Kim, C. Wilkerson, and O. Mutlu, “An Experimental Study of Data Retention Behavior in Modern DRAM Devices: Implications for Retention Time Profiling Mechanisms,” *Proceedings of the 40th Annual International Symposium on Computer Architecture* (ISCA), 60–71 (2013). [DOI: 10.1145/2485922.2485928](https://doi.org/10.1145/2485922.2485928). [Author-provided PDF](https://users.ece.cmu.edu/~omutlu/pub/dram-retention-time-characterization_isca13.pdf).
9. M. K. Bepary, B. M. S. B. Talukder, and M. T. Rahman, “DRAM Retention Behavior with Accelerated Aging in Commercial Chips,” *Applied Sciences* **12**(9), 4332 (2022). [DOI: 10.3390/app12094332](https://doi.org/10.3390/app12094332).
10. A. Weber, A. Birner, and W. Krautschneider, “DRAM Retention Tail Improvement by Trap Passivation,” *Solid-State Electronics* **51**(11–12), 1534–1539 (2007). [DOI: 10.1016/j.sse.2007.09.023](https://doi.org/10.1016/j.sse.2007.09.023).
11. Micron Technology, *Introducing Micron DDR5 SDRAM: New Features*, technical white paper (2019). [Technical paper PDF](https://www.micron.com/content/dam/micron/global/public/products/white-paper/ddr5-new-features-white-paper.pdf).
12. IBM Research, “A 22-ns 1-Mbit CMOS High-Speed DRAM with Address Multiplexing,” *IEEE Journal of Solid-State Circuits* (1988). [Research record](https://research.ibm.com/publications/a-22-ns-1-mbit-cmos-high-speed-dram-with-address-multiplexing).
13. K. Itoh, Y. Nakagome, S. Kimura, and T. Watanabe, “Limitations and Challenges of Multigigabit DRAM Chip Design,” *IEEE Journal of Solid-State Circuits* **32**(5), 624–634 (1997). [IEEE Xplore record](https://doi.org/10.1109/4.568008).
14. W. Jeon, “Recent Advances in the Understanding of High-k Dielectric Materials Deposited by Atomic Layer Deposition for Dynamic Random-Access Memory Capacitor Applications,” *Journal of Materials Research* **35**(7), 775–794 (2020). [DOI: 10.1557/jmr.2019.335](https://doi.org/10.1557/jmr.2019.335).
15. Y. Ohji, S. Iijima, N. Nakanishi, and I. Asano, “Application of High-K Dielectric Material Thin Film to DRAM Capacitors—Issues and a Direction,” *Oyo Buturi* **66**(11), 1210–1214 (1997). [DOI: 10.11470/oubutsu1932.66.1210](https://doi.org/10.11470/oubutsu1932.66.1210).
16. I. G. Kim et al., “Overcoming DRAM Scaling Limitations by Employing Straight Recessed Channel Array Transistors with <100> Uni-Axial and {100} Uni-Plane Channels,” *IEDM Technical Digest*, 319–322 (2005). [DOI: 10.1109/IEDM.2005.1609339](https://doi.org/10.1109/IEDM.2005.1609339).
17. C. Kuo, T. J. King, and C.-M. Hu, “A Capacitorless Double Gate DRAM Technology for Sub-100-nm Embedded and Stand-Alone Memory Applications,” *IEEE Transactions on Electron Devices* **50**(12), 2408–2416 (2003). [DOI: 10.1109/TED.2003.819257](https://doi.org/10.1109/TED.2003.819257).
18. J.-W. Han, S.-W. Ryu, D.-H. Kim, C.-J. Kim, S. Kim, D.-I. Moon, S.-J. Choi, and Y.-K. Choi, “Fully Depleted Polysilicon TFTs for Capacitorless 1T-DRAM,” *IEEE Electron Device Letters* **30**(7), 742–744 (2009). [DOI: 10.1109/LED.2009.2022343](https://doi.org/10.1109/LED.2009.2022343).
19. M. Sun, H. W. Baac, and C. Shin, “Simulation Study: The Impact of Structural Variations on the Characteristics of a Buried-Channel-Array Transistor (BCAT) in DRAM,” *Micromachines* **13**(9), 1476 (2022). [DOI: 10.3390/mi13091476](https://doi.org/10.3390/mi13091476).
20. T. Schloesser et al., “A 6F² Buried Wordline DRAM Cell for 40nm and Beyond,” *IEDM Technical Digest* (2008). [Conference PDF](https://yumilab.ei.gunma-u.ac.jp/analog/IEDM08advprg.pdf).
21. G. Heiser, “Caches,” *COMP9242 2025 T3 W03 Part 1: HW Considerations*, slide 5, UNSW Sydney (2025), CC BY 4.0. [Lecture PDF](https://cgi.cse.unsw.edu.au/~cs9242/25/lectures/03a-hw.pdf).
22. HandigeHarry, “DRAM,” Wikimedia Commons (2008), public domain. [Original file and license](https://commons.wikimedia.org/wiki/File:DRAM.svg).
