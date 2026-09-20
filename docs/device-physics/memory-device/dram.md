---
description: 1T1C DRAM의 저장 전하와 판독 여유, Precharge–Activate–Sense–Restore–Column access, write·refresh와 기본 timing을 설명
---

# Memory device: DRAM basic

Dynamic random-access memory (DRAM)는 capacitor에 저장한 전하로 1 bit를 나타내는 휘발성 메모리이다. Conventional DRAM의 기본 셀은 access transistor 하나와 storage capacitor 하나로 이루어진 **1T1C cell**이다. 저장 전하는 시간이 지나면 변하기 때문에 주기적인 **refresh**가 필요하고, 읽을 때에는 bit line과 전하를 나누기 때문에 읽은 값의 **restore**가 필요하다.[1–3,6]

이 글은 [Memory device: Overview](basics.md)의 array·word line·bit line 개념을 바탕으로, conventional 1T1C cell과 differential sense amplifier의 기본 동작만 다룬다. 핵심 순서는 다음과 같다.

> **Precharge → Activate → Sense → Restore → Column access → Precharge**

여기서 `ACTIVATE`는 row를 열면서 내부적으로 **charge sharing, Sense, Restore**를 시작하는 명령이고, `READ`와 `WRITE`는 열린 row에서 column을 선택하는 명령이다. 이 두 층을 구분해야 DRAM의 동작 순서와 timing을 혼동하지 않는다.[1,2]

## 1. 1T1C cell과 array의 기준 모형

### (1) Cell: 전하로 1 bit 저장

1T1C cell에서 access transistor의 gate는 **word line (WL)**에, 한쪽 전류 단자는 **bit line (BL)**에, 다른 쪽 단자는 storage capacitor의 **storage node (SN)**에 연결된다. $WL$이 낮으면 transistor가 꺼져 cell이 $BL$에서 분리되고, $WL$이 높으면 transistor가 켜져 $SN$과 $BL$ 사이로 전하가 이동한다.[1,2]

| 구성 요소 | 역할 |
| --- | --- |
| Storage capacitor | $SN$의 전하로 한 bit를 저장한다. |
| Access transistor | $WL$에 따라 $SN$과 $BL$의 연결을 제어한다. |
| Word line | 같은 row의 access transistor들을 선택한다. |
| Bit line | 같은 column의 여러 cell이 공유하는 전하 이동 경로이다. |
| Sense amplifier | $BL$ 쌍의 작은 전압차를 판정·증폭하고 cell을 restore한다. |

Storage-node 전압을 $V_\mathrm{SN}$, capacitor의 반대쪽 plate 전압을 $V_\mathrm{plate}$로 두면 선형 capacitor 근사에서 저장 전하는

$$
Q_\mathrm{cell}
=
C_\mathrm{cell}
\left(V_\mathrm{SN}-V_\mathrm{plate}\right)
$$

이다. $C_\mathrm{cell}$은 cell capacitance이다. 이 글에서는 높은 $V_\mathrm{SN}$을 논리 1, 낮은 $V_\mathrm{SN}$을 논리 0으로 부른다. 실제 제품에서는 내부 polarity와 data scrambling 때문에 외부 data bit와 물리적인 $SN$ 전압의 대응이 반대일 수 있다.[1,2]

전압 자체만으로 셀 상태를 정의하는 것은 충분하지 않다. 판독 직전에 남은 전하가 bit line에 만드는 전압 변화가 sense-amplifier offset과 noise를 이겨야 한다. 따라서 DRAM의 물리적 상태는 “충전·방전된 capacitor”에서 끝나지 않고, **저장 전하 → bit-line 신호 → sense-amplifier 판정**의 연쇄로 정의해야 한다.[1,2,6]

### (2) Array의 row·column 선택

같은 $WL$에 연결된 cell들은 한 **row**를 이루고, 각 cell은 서로 다른 $BL$을 통해 sense amplifier에 연결된다. Row decoder가 하나의 $WL$을 선택하면 그 row의 cell들이 각자의 $BL$과 동시에 전하를 공유한다. Sense amplifier 집합은 이 작은 신호를 판정해 row 전체를 보유하므로 **row buffer** 역할도 한다.[1,2]

<figure markdown="span">
  ![행과 열로 배열된 memory cell, row decoder, sense amplifier와 column decoder의 관계](images/memory-cell-array.svg)
  <figcaption markdown="1">
    그림 1. DRAM array의 기본 정보 흐름. Row decoder가 한 row를 열면 sense amplifier들이 그 row를 판정·보유하고, column decoder가 필요한 일부 column만 입출력 경로에 연결한다. 원본은 HandigeHarry, “DRAM,” Wikimedia Commons, public domain이며 array·decoder·sense-amplifier 관계를 설명하는 영역을 발췌해 사용했다. 특정 제품의 실제 layout을 나타내지 않는다.[4]
  </figcaption>
</figure>

큰 array는 긴 $WL$과 $BL$의 저항·정전용량 때문에 여러 **subarray**와 **bank**로 나뉜다. 기본 포함 관계는 `cell → row/column → subarray → bank → chip`이다. Basic 동작에서는 cell–bit line–sense amplifier의 관계가 핵심이며, 세부 배선과 cell 구조의 발전은 [Memory device: DRAM advance](dram-advance.md)에서 다룬다.[1,2]

### (3) 차동 판독과 판독 여유

Conventional differential sensing에서 sense amplifier는 선택 cell이 연결된 $BL$과 기준 신호를 제공하는 $\overline{BL}$의 차이를 읽는다. Precharge 단계에서 두 선을 같은 $V_\mathrm{pre}$로 맞춘 뒤 cell을 연결하면, 선택 cell이 만든 작은 부호 신호만 두 입력의 차이로 남는다. Cross-coupled sense amplifier의 positive feedback은 이 차이를 두 개의 안정한 full-swing 상태 중 하나로 만든다.[1,2,6]

이상적인 입력 신호를 $\Delta V_\mathrm{BL}$, sense amplifier의 입력 환산 offset을 $V_\mathrm{OS}$, coupling·thermal noise의 최악 방향 크기를 $V_\mathrm{noise}$로 두면 개념적 판독 여유를

$$
M_\mathrm{sense}
=
\left|\Delta V_\mathrm{BL}\right|
-\left|V_\mathrm{OS}\right|
-V_\mathrm{noise}
$$

로 나타낼 수 있다. $M_\mathrm{sense}>0$이면 이 정적 오차 모형에서 최악 방향의 offset·noise 합보다 신호가 크지만, 실제 동적 판독의 충분조건은 아니다. 반대로 $M_\mathrm{sense}\le0$은 최악 조건의 여유가 없다는 뜻이며 모든 판독이 반드시 실패한다는 뜻은 아니다. 실제 판정은 sense-enable 시점, transistor mismatch, 공급 전압, 온도와 시간에 따른 신호 발달에도 의존한다. 이 식은 제품의 고정 합격 기준이 아니라, cell 신호가 줄거나 offset·noise가 커질 때 오판 가능성이 증가하는 방향을 보이는 근사이다.[1,6]

## 2. 동작 과정

DRAM 접근은 명령과 내부 회로 동작을 다음처럼 대응시키면 가장 명확하다.[1,2]

| 세부 단계 | 명령 순서 | 내부 동작 순서 |
| --- | --- | --- |
| Read 단계 | `ACTIVATE → READ → PRECHARGE` | Precharge 상태 → Charge sharing → Sense → Restore와 data output → Close |
| Write 단계 | `ACTIVATE → WRITE → PRECHARGE` | Precharge 상태 → Charge sharing → Sense → Overwrite → Restore → Close |
| Refresh 단계 | `REFRESH` | 내부 row 선택 → Activate → Sense → Restore → Close |

### (1) Read 단계

**1. Precharge.** 접근 전에는 $BL$과 보수 bit line $\overline{BL}$을 같은 기준 전압 $V_\mathrm{pre}$로 맞추고 두 선의 잔류 차이를 제거한다. Conventional differential sensing에서는 보통 $V_\mathrm{pre}=V_\mathrm{DD}/2$를 사용한다. 이 상태에서 두 선은 논리 0과 1 어느 방향의 작은 변화도 받아들일 수 있다.[1,2]

**2. Activate.** `ACTIVATE`가 row address를 선택하면 $WL$이 올라가 access transistor가 켜진다. 선택된 cell의 $SN$과 $BL$이 연결되고 두 capacitance 사이에 **charge sharing**이 일어난다. $BL$이 기준 전압보다 어느 방향으로 움직이는지가 저장 bit를 나타낸다.[1,2]

Charge sharing 직전의 bit-line capacitance와 전압을 $C_\mathrm{BL}$, $V_\mathrm{pre}$로 두고, cell의 초기 storage-node 전압을 $V_\mathrm{SN,0}$로 두자. $V_\mathrm{plate}$가 일정하고 leakage, 배선 저항과 sense-amplifier loading을 무시하면 전하 보존으로

$$
V_\mathrm{BL}'
=
\frac{C_\mathrm{BL}V_\mathrm{pre}
+C_\mathrm{cell}V_\mathrm{SN,0}}
{C_\mathrm{BL}+C_\mathrm{cell}}
$$

이고, 기준 전압에서 벗어난 크기는

$$
\Delta V_\mathrm{BL}
=
V_\mathrm{BL}'-V_\mathrm{pre}
=
\frac{C_\mathrm{cell}}
{C_\mathrm{BL}+C_\mathrm{cell}}
\left(V_\mathrm{SN,0}-V_\mathrm{pre}\right)
$$

이다. 예를 들어 긴 $BL$에 많은 cell과 배선의 기생 capacitance가 연결되면 보통 $C_\mathrm{BL}$이 $C_\mathrm{cell}$보다 크다. 이 경우 cell 전압 변화의 일부만 $BL$로 전달되므로 $\Delta V_\mathrm{BL}$은 full-swing 논리 전압보다 훨씬 작고, 직접 외부로 보낼 수 없다.[1,2,6]

**3. Sense.** 충분한 $\Delta V_\mathrm{BL}$이 형성되면 cross-coupled sense amplifier를 켠다. Positive feedback은 더 높은 쪽을 $V_\mathrm{DD}$로, 더 낮은 쪽을 0 V로 밀어 작은 차이를 full-swing 차동 신호로 증폭한다. Sense amplifier가 너무 일찍 켜지면 cell 신호보다 offset과 noise가 판정을 지배할 수 있고, 너무 늦게 켜지면 접근 시간이 길어진다.[1,2]

**4. Restore.** Charge sharing은 $SN$의 원래 전압을 바꾸므로 DRAM read는 **destructive read**이다. 그러나 $WL$이 계속 켜진 상태에서 sense amplifier가 $BL$을 full swing으로 구동하면 그 전압이 $SN$에도 전달되어 원래 bit가 다시 저장된다. 이것이 restore이며, sense amplifier는 판정·증폭뿐 아니라 cell의 재충전도 담당한다.[1,2]

**5. Column access.** Row의 신호가 충분히 판정되면 `READ`가 column address를 선택한다. Column multiplexer는 row buffer의 일부 bit만 global data line과 I/O circuit으로 전달한다. 따라서 `ACTIVATE`는 cell에서 row buffer로 row를 여는 과정이고, `READ`는 열린 row에서 필요한 column을 외부로 내보내는 과정이다.[1,2]

**6. Close.** 다른 row를 열려면 `PRECHARGE`로 현재 row를 닫는다. 먼저 $WL$을 내려 cell을 $BL$에서 분리하고 sense amplifier를 끈 뒤, $BL$과 $\overline{BL}$을 다시 $V_\mathrm{pre}$로 맞춘다. 이 마지막 Precharge가 다음 접근의 첫 Precharge 상태가 된다.[1,2]

!!! note "단계 사이의 겹침"
    위 여섯 이름은 인과관계를 보여주는 순서이다. 실제 파형에서는 Sense와 Restore가 연속적으로 진행되고, cell의 restore가 완전히 끝나기 전에 row buffer의 신호가 column access에 충분한 수준에 도달할 수 있다. 따라서 `Sense → Restore → Column access`를 서로 겹치지 않는 세 구간으로 해석하지 않는다.[1,2]

!!! info "[Measurement]"
    Read 파형에서는 $WL$, $BL$, $\overline{BL}$, sense-enable과 출력 신호를 함께 기록한다. Cell이 만든 차동 입력은

    $$
    \Delta V_\mathrm{BL}(t)
    =
    V_\mathrm{BL}(t)-V_{\overline{\mathrm{BL}}}(t)
    $$

    로 계산한다. $WL$ 상승 뒤 sense amplifier 출력이 판정 기준을 지나는 시간은

    $$
    t_\mathrm{sense}
    =
    t_{\mathrm{SA,out},50\%}-t_{\mathrm{WL},50\%}
    $$

    로 둘 수 있다. $C_\mathrm{BL}$, 초기 $V_\mathrm{SN,0}$, sense-enable 시점, offset, $V_\mathrm{DD}$와 온도를 함께 기록해야 charge-sharing 부족과 sense-amplifier 오판을 구분할 수 있다.[1,2,6]

### (2) Write 단계

Write도 닫힌 row의 cell을 곧바로 구동하지 않는다. 먼저 `ACTIVATE`로 대상 row를 row buffer에 연 뒤, `WRITE`로 선택한 column의 기존 상태를 새 data로 덮어쓴다.[1,2]

**1. Activate.** 대상 row를 열어 sense amplifier가 현재 값을 판정한다.

**2. Column select.** Column decoder가 바꿀 bit를 local sense amplifier와 write driver 사이에 연결한다.

**3. Overwrite.** Write driver가 선택한 $BL$ 쌍을 새 data polarity로 강하게 구동하여 sense amplifier의 기존 상태를 뒤집거나 유지한다.

**4. Restore.** $WL$이 켜져 있으므로 새 $BL$ 전압이 선택 cell의 $SN$을 충전하거나 방전한다. Write recovery가 끝나기 전에 row를 닫으면 cell에 충분한 전하가 저장되지 않을 수 있다.

**5. Close.** `PRECHARGE`가 $WL$을 내리고 $BL$ 쌍을 $V_\mathrm{pre}$로 되돌린다.

즉, read와 write는 row를 여는 앞부분을 공유한다. 차이는 read가 row buffer의 선택 data를 외부로 전달하는 반면, write는 외부 data로 row buffer와 cell의 선택 column을 덮어쓴다는 점이다.[1,2]

!!! info "[Measurement]"
    Write 검증에서는 선택 bit의 쓰기 data가 관측 지점에 유효하게 들어온 시각을 $t_0$로 정하고, 그 뒤 $SN$이 목표 전압 범위에 처음 도달할 때까지의 경과 시간을 측정한다. 관측 지점이 외부 I/O인지 내부 write-driver 입력인지도 함께 기록한다. 논리 1의 최소 허용 전압을 $V_\mathrm{SN,min}^{(1)}$, 논리 0의 최대 허용 전압을 $V_\mathrm{SN,max}^{(0)}$로 두면

    $$
    t_\mathrm{write}^{(1)}
    =
    \inf\{t\ge t_0:V_\mathrm{SN}(t)\ge V_\mathrm{SN,min}^{(1)}\}-t_0
    $$

    $$
    t_\mathrm{write}^{(0)}
    =
    \inf\{t\ge t_0:V_\mathrm{SN}(t)\le V_\mathrm{SN,max}^{(0)}\}-t_0
    $$

    로 각 polarity의 첫 도달 시간을 따로 정의할 수 있다. 같은 값을 다시 쓸 때 $t_0$에서 이미 조건을 만족하면 이 지표는 0이며, 관측 종료까지 도달하지 않으면 미도달로 기록한다. 첫 도달만으로 저장 완료를 보장하지는 않는다. Write driver 크기, $WL$·$BL$ 파형, $C_\mathrm{cell}$, 공급 전압과 온도를 같이 기록하고, 후속 read의 오류 여부로 충분한 저장 전하가 남았는지 확인한다.[1,2,6] 이 셀 수준 지표는 4절의 $t_\mathrm{WR}$와 구분한다. $t_\mathrm{WR}$는 마지막 write data 이후 precharge까지 확보해야 하는 recovery 구간이며, 단일 $SN$의 임의 전압 기준 첫 도달 시간과 같은 정의가 아니다.[1,2]

### (3) Refresh 단계

Refresh는 새로운 data를 입출력하지 않고 기존 row를 **Select → Activate → Sense → Restore → Close**하는 내부 접근이다. Row를 선택·활성화해 남아 있는 작은 전압차를 sense amplifier가 판정하고, full-swing 전압으로 cell을 다시 충전한 다음 row를 닫는다. 그러므로 refresh는 각 cell에 전원만 다시 공급하는 동작이 아니라, row 단위의 read-and-restore 과정이다.[2,3]

`Auto-refresh`에서는 memory controller가 refresh 명령을 보내고 DRAM 내부 counter가 대상 row를 정한다. `Self-refresh`에서는 저전력 상태에서 DRAM 내부 timing 회로가 refresh를 계속한다. 구체적인 command encoding과 한 번에 처리하는 bank·row 범위는 DRAM 세대와 제품 규격에 따라 달라진다.[2,3,5]

## 3. Retention과 refresh

### (1) Retention time

Access transistor가 꺼져 있어도 junction leakage, transistor의 off-state leakage와 capacitor dielectric leakage 등으로 $SN$의 전하가 변한다. **Retention time** $t_\mathrm{ret}$은 refresh 없이 cell을 두었을 때 저장 bit를 신뢰성 있게 읽을 수 있는 최대 시간이다. 전하가 완전히 0이 되는 시간이 아니라, 남은 cell 신호가 sense amplifier의 판정 조건을 더는 만족하지 못하는 시점이다.[2,3]

누설 전류의 크기를 일정한 $I_\mathrm{leak}$으로 근사하고 허용 가능한 cell 전압 변화를 $\Delta V_\mathrm{allow}$로 두면

$$
t_\mathrm{ret}
\approx
\frac{C_\mathrm{cell}\Delta V_\mathrm{allow}}
{I_\mathrm{leak}}
$$

이다. 이 식은 $C_\mathrm{cell}$이 크고 $I_\mathrm{leak}$이 작을수록 retention이 길어진다는 방향을 보여주는 1차 근사이다. 실제 $I_\mathrm{leak}$은 전압·온도·시간과 cell 상태에 의존하므로, 모든 cell의 retention을 하나의 상수 전류로 정확히 예측할 수는 없다.[2,3]

여기서 $\Delta V_\mathrm{allow}$는 임의로 정한 방전 폭이 아니라 앞 절의 판독 조건과 연결해야 한다. 이를 보기 위해 1절의 offset·noise 합을 $V_\mathrm{req}=|V_\mathrm{OS}|+V_\mathrm{noise}$로 두고, 2절의 이상적 charge-sharing 식을 대입한다. 그 모형에서 양의 판독 여유를 얻으려면 접근 직전 cell 전압은 다음 조건을 만족해야 한다.

$$
\left|V_\mathrm{SN,0}-V_\mathrm{pre}\right|
>\frac{C_\mathrm{BL}+C_\mathrm{cell}}{C_\mathrm{cell}}V_\mathrm{req}
$$

이는 새로운 소자 법칙이 아니라 앞서 정의한 여유식의 재배열이다. 논리 1에서는 $V_\mathrm{pre}$보다 충분히 높은 전압이, 논리 0에서는 충분히 낮은 전압이 남아 있어야 한다. 따라서 같은 누설 전류라도 restore 직후 전압이 목표 rail에 얼마나 가까운지, bit-line 부하가 얼마나 큰지에 따라 허용 가능한 전압 변화가 달라진다. 저장된 전하를 작은 bit-line 신호로 바꾼 뒤 증폭한다는 두 문헌의 설명을 이 기준 모형으로 연결한 것이다.[1,2]

예를 들어 논리 1의 전압이 단조롭게 내려가는 이상화에서는 restore 직후 전압과 위 식의 높은 쪽 경계 사이 간격이 $\Delta V_\mathrm{allow}$가 된다. 시작부터 그 경계보다 낮으면 양의 retention 시간을 이 근사로 확보할 수 없다. 반대로 경계를 넘는 여유가 있어도 유한한 sense 시간과 실제 offset 분포는 별도로 확인해야 한다. 이 때문에 2절의 쓰기 첫 도달 시간만 짧게 만드는 것과, row를 닫은 뒤 다음 접근까지 충분한 전하를 보존하는 것은 서로 다른 검증 항목이다.[1,2]

### (2) Cell 분포와 판정 기준

공정 편차 때문에 cell마다 capacitance와 leakage가 다르며, retention time도 분포를 이룬다. 주변 data pattern이 charge-sharing 조건에 영향을 줄 수 있고, 일부 cell은 시간에 따라 retention 상태가 달라지는 **variable retention time (VRT)**을 보인다. 따라서 평균 cell이 아니라 짧은 retention을 갖는 tail cell까지 정해진 조건에서 올바르게 읽히도록 refresh 조건을 정해야 한다.[2,3]

!!! info "[Measurement]"
    알려진 data pattern을 row에 쓴 뒤 refresh를 정해진 시간 $t_\mathrm{wait}$ 동안 막고 read한다. 각 대기 시간은 동일한 초기 조건으로 다시 써서 시험한다. 연속된 read는 그 자체로 restore를 수반하므로, 한 번 쓴 cell을 여러 번 읽는 파형을 독립적인 retention 시험으로 취급하지 않는다.[1–3] 먼저 오류 확률이 대기 시간에 따라 단조롭게 증가하는 고정 조건의 모형을 생각하면, 허용 기준을 만족하는 시간의 상한은

    $$
    t_\mathrm{ret}
    =
    \sup\left\{
    t_\mathrm{wait}\ge0:
    P_\mathrm{bit\ error}(t_\mathrm{wait})
    \le P_\mathrm{target}
    \right\}
    $$

    로 정의할 수 있다. 여기서 $P_\mathrm{target}$은 시험에서 허용한 bit-error probability이다. 실제로는 유한한 대기 시간 간격과 반복 횟수로 시험하므로, 마지막 통과 시간과 첫 실패 시간을 따로 기록한다. 그 사이를 시험하지 않았다면 둘 중 하나를 정확한 물리적 경계라고 부르지 않는다. 최대 시험 시간까지 모두 통과한 경우에도 측정 범위에서의 하한만 확인한 것이다.

    이 정의의 고정 조건 가정과 실제 VRT를 구별해야 한다. VRT가 있으면 다른 반복에서 관측한 마지막 통과 시간이 같지 않을 수 있고, 한 번의 통과로 미래의 더 긴 보존을 보장할 수 없다.[2,3] 오류 확률을 추정한 cell 집합과 반복 횟수를 밝히고, 단일 cell의 실패 여부와 array 전체 오류 bit 비율도 구분한다. 온도, $V_\mathrm{DD}$, data pattern과 인접 row activity를 함께 기록하며 평균뿐 아니라 하위 percentile과 최악 cell을 보고한다.[2,3]

!!! warning "[Interpretation Caveat]"
    Retention test의 read error만으로 특정 leakage 경로를 확정할 수 없다. 부족한 cell 전하, sense-amplifier offset, bit-line imbalance와 coupling이 같은 출력 오류를 만들 수 있기 때문이다. Leakage 원인을 분리하려면 cell test와 transistor·capacitor 구조의 전기적 측정을 함께 사용해야 한다.[2,3]

## 4. Command와 timing

### (1) Row·column 명령

DRAM command는 기본 동작 순서를 외부 interface에서 제어한다.[1,2]

| Command | 핵심 동작 |
| --- | --- |
| `ACTIVATE` | Row를 선택하고 Charge sharing–Sense–Restore를 시작한다. |
| `READ` | 열린 row buffer에서 선택 column을 외부로 출력한다. |
| `WRITE` | 열린 row buffer와 선택 cell을 입력 data로 갱신한다. |
| `PRECHARGE` | Row를 닫고 bit-line 쌍을 다음 접근의 기준 전압으로 되돌린다. |
| `REFRESH` | 내부에서 row를 선택하여 Activate–Sense–Restore–Close를 수행한다. |

같은 bank에서 이미 열린 row의 다른 column을 읽으면 **row hit**이다. 다른 row가 열려 있으면 먼저 `PRECHARGE`하고 새 row를 `ACTIVATE`해야 하므로 **row conflict**가 된다. 이 때문에 DRAM의 접근 지연은 주소가 무작위라는 사실만으로 일정하지 않고, bank와 현재 열린 row 상태에 따라 달라진다.[1,2]

### (2) 기본 timing parameter

Timing parameter는 임의의 대기 시간이 아니라 앞 절의 전하 이동이 충분히 끝나도록 보장하는 최소 시간이다.[1,2]

| Parameter | 명령 사이의 구간 | 보장하는 내부 과정 |
| --- | --- | --- |
| $t_\mathrm{RCD}$ | `ACTIVATE` → `READ/WRITE` | Charge sharing과 Sense가 column access에 충분한 수준에 도달함 |
| $t_\mathrm{CL}$ | `READ` → 첫 data | 선택 column의 data가 내부 입출력 경로를 거쳐 interface에 나올 때까지의 read latency |
| $t_\mathrm{RAS}$ | `ACTIVATE` → `PRECHARGE` | Sense와 cell Restore가 완료될 최소 active 시간 |
| $t_\mathrm{RP}$ | `PRECHARGE` → 다음 `ACTIVATE` | $BL$ 쌍의 Precharge와 equalization 완료 |
| $t_\mathrm{RC}$ | 같은 bank의 `ACTIVATE` → 다음 `ACTIVATE` | 한 row cycle의 완료이며 기본적으로 $t_\mathrm{RAS}+t_\mathrm{RP}$ |
| $t_\mathrm{WR}$ | 마지막 write data → `PRECHARGE` | 새 data가 cell에 충분히 Restore되는 write recovery |

$t_\mathrm{RCD}$가 지났다는 것은 cell restore가 완전히 끝났다는 뜻이 아니라, 선택 column을 사용할 만큼 sense 결과가 형성되었다는 뜻이다. 반면 $t_\mathrm{RAS}$는 row를 닫기 전에 cell restore까지 확보해야 한다. 이 차이를 알면 `READ`가 Restore 뒤에만 시작된다는 잘못된 직렬 해석을 피할 수 있다.[1,2,5,6]

Command 전송과 자료 burst의 세부를 무시하고 **각 순서의 첫 명령을 즉시 발행할 수 있다면**, precharge가 완료된 bank에서 첫 data까지의 핵심 지연은 약 $t_\mathrm{RCD}+t_\mathrm{CL}$, row hit에서는 약 $t_\mathrm{CL}$이다. Row conflict는 기존 row를 닫는 $t_\mathrm{RP}$가 먼저 필요하므로 약 $t_\mathrm{RP}+t_\mathrm{RCD}+t_\mathrm{CL}$이 된다. 이 합은 물리적 순서를 비교하는 근사이며, 실제 controller 지연에는 command bus 대기, bank 상태, burst, queueing과 세대별 timing 제약이 추가된다.[1,2,6]

| 접근 상태 | 필요한 핵심 순서 | 첫 data까지의 개념적 지연 |
| --- | --- | --- |
| Row hit | `READ` | $t_\mathrm{CL}$ |
| Closed bank | `ACTIVATE → READ` | $t_\mathrm{RCD}+t_\mathrm{CL}$ |
| Row conflict | `PRECHARGE → ACTIVATE → READ` | $t_\mathrm{RP}+t_\mathrm{RCD}+t_\mathrm{CL}$ |

특히 row conflict라는 주소 관계만으로 `PRECHARGE`를 즉시 발행할 수 있는 것은 아니다. 기존 row의 restore가 진행 중이면 최소 active 시간을 채워야 하고, 직전에 write했다면 write recovery도 만족해야 한다. Wang은 같은 bank의 다른 row 접근에서도 이전 row의 활성화 시각에 따라 추가 대기가 달라짐을 설명한다. Lee의 내부 동작 설명에서도 cell restore가 끝나기 전에 row를 닫으면 충분한 전하를 남길 수 없다.[1,2]

이 두 제약만 분리해서 살펴보자. 요청 도착 시각을 $t_\mathrm{req}$, 기존 row의 활성화 시각을 $t_\mathrm{ACT,old}$, 마지막 write data의 끝 시각을 $t_\mathrm{data,end}$로 두면, precharge 발행 시각은 최소한

$$
t_\mathrm{PRE}\ge
\max\left(t_\mathrm{req},\;
t_\mathrm{ACT,old}+t_\mathrm{RAS},\;
t_\mathrm{data,end}+t_\mathrm{WR}\right)
$$

를 만족해야 한다. Write가 없으면 마지막 항은 제외한다. 이 식은 동시에 만족해야 하는 두 timing 제약을 절대 시각으로 옮긴 것이며, 모든 세대의 명령 제약을 나열한 완전한 controller 모형은 아니다. Read 이후 precharge 제약, command bus 점유와 refresh 등이 있으면 그 조건도 추가해야 한다.[1,2]

따라서 요청부터의 지연을 계산할 때는 먼저 $t_\mathrm{PRE}-t_\mathrm{req}$의 대기를 구하고, 그 뒤에 표의 $t_\mathrm{RP}+t_\mathrm{RCD}+t_\mathrm{CL}$ 구간을 붙인다. $t_\mathrm{RAS}$ 전체를 매번 더하면 이미 경과한 시간을 중복 계산하고, 항상 생략하면 남은 restore 시간을 놓친다. 같은 원리로 row hit의 $t_\mathrm{CL}$도 `READ` 발행 이후의 지연이며 요청 도착부터의 모든 대기를 뜻하지 않는다. 비교 실험에서는 요청 도착·명령 발행·첫 data 중 어느 지점을 시간 원점으로 삼았는지 먼저 고정한다.[1,2]

## 5. Cell signal의 설계 관계

### (1) Capacitance·전하·누설의 trade-off

Charge-sharing 식에서 read signal을 직접 정하는 기본 변수는 $C_\mathrm{cell}$, $C_\mathrm{BL}$과 접근 직전의 $V_\mathrm{SN,0}$이다.

- 큰 $C_\mathrm{cell}$은 sensing signal과 retention에 유리하지만 작은 cell 면적에 구현하기 어렵다.
- 작은 $C_\mathrm{BL}$은 $\Delta V_\mathrm{BL}$과 속도에 유리하지만, bit line을 짧게 나누면 sense amplifier와 decoder의 면적 overhead가 늘어난다.
- 높은 access-transistor on-current는 charge sharing과 write를 빠르게 하지만, 낮은 off-state leakage도 동시에 필요하다.

따라서 DRAM basic의 핵심 설계 문제는 “capacitor를 크게 만들기” 하나가 아니라, 제한된 cell 면적에서 저장 전하·bit-line 부하·transistor leakage·sense-amplifier 판정 여유를 함께 맞추는 것이다.[1–3,6]

| 설계 변수 | 유리한 방향 | 함께 커지는 부담 |
| --- | --- | --- |
| $C_\mathrm{cell}$ | 큰 저장 전하, 큰 $|\Delta V_\mathrm{BL}|$, 긴 retention | cell 면적과 capacitor 공정 부담 |
| $C_\mathrm{BL}$ | 작을수록 큰 $|\Delta V_\mathrm{BL}|$과 빠른 판독 | 짧은 bit line에 필요한 sense amplifier·decoder 면적 |
| Access-transistor on-current | 빠른 charge sharing과 write | off-state leakage와 disturb를 함께 억제해야 함 |
| Sense-enable 시점 | 빠른 활성화는 latency를 줄임 | $\Delta V_\mathrm{BL}$이 작은 때 켜면 offset·noise 민감도 증가 |
| Restore 시간 | 길수록 후속 retention 여유 증가 | bank 점유 시간과 접근 지연 증가 |

## 6. 요약

- 1T1C DRAM은 access transistor와 storage capacitor로 1 bit를 저장하며, cell은 $WL$로 선택되고 $BL$을 통해 sense amplifier에 연결된다.
- Read의 인과 순서는 **Precharge → Activate/Charge sharing → Sense → Restore → Column access → Precharge**이다.
- `ACTIVATE`는 row를 열어 내부 판정과 restore를 시작하고, `READ`와 `WRITE`는 열린 row의 column을 선택한다.
- Read는 charge sharing으로 cell 전압을 바꾸는 destructive read이므로 sense amplifier가 판정한 값을 반드시 restore해야 한다.
- Refresh는 외부 data transfer 없이 row를 **Select → Activate → Sense → Restore → Close**하는 내부 동작이다.
- $t_\mathrm{RCD}$, $t_\mathrm{CL}$, $t_\mathrm{RAS}$와 $t_\mathrm{RP}$는 각각 판정 가능한 신호 형성, column 출력, cell restore와 bit-line 초기화에 필요한 시간을 나타낸다.

## 7. 참고문헌

1. D. Lee, *Reducing DRAM Latency at Low Cost by Exploiting Heterogeneity*, Ph.D. dissertation, Carnegie Mellon University (2016). [Author manuscript](https://research.ece.cmu.edu/safari/thesis/dlee_dissertation.pdf).
2. D. T. Wang, *Modern DRAM Memory Systems: Performance Analysis and a High Performance, Power-Constrained DRAM Scheduling Algorithm*, Ph.D. dissertation, University of Maryland, College Park (2005). [University record](https://drum.lib.umd.edu/items/b3a2340b-5fe3-4230-b8aa-7d4128baad62).
3. J. Liu, B. Jaiyen, Y. Kim, C. Wilkerson, and O. Mutlu, “An Experimental Study of Data Retention Behavior in Modern DRAM Devices: Implications for Retention Time Profiling Mechanisms,” *Proceedings of the 40th Annual International Symposium on Computer Architecture*, 60–71 (2013). [DOI: 10.1145/2485922.2485928](https://doi.org/10.1145/2485922.2485928).
4. HandigeHarry, “DRAM,” *Wikimedia Commons* (2006), public domain. [파일 설명과 라이선스](https://commons.wikimedia.org/wiki/File:DRAM.svg).
5. Micron Technology, *8Gb: x4, x8, x16 DDR4 SDRAM*, Rev. H, “PRECHARGE Command” and “REFRESH Command” (2021). [제품 data sheet PDF](https://www.micron-electronic.com/pdf-0b/mt40a512m16jy-075e-b.pdf).
6. K. K. Chang et al., “Understanding Reduced-Voltage Operation in Modern DRAM Devices: Experimental Characterization, Analysis, and Mechanisms,” *Proceedings of the ACM on Measurement and Analysis of Computing Systems* **1**(1), Article 11 (2017). [DOI: 10.1145/3078505.3078590](https://doi.org/10.1145/3078505.3078590); [author manuscript](https://arxiv.org/abs/1705.10292).
