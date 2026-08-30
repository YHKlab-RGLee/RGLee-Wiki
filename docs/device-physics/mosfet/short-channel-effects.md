---
description: MOSFET의 short-channel effects를 장채널 기준, 물리적 기원, 개별 현상, 측정법과 정량 지표의 순서로 설명
---

# MOSFET: Short-channel effects

Metal-oxide-semiconductor field-effect transistor (MOSFET)의 short-channel effects (SCE)는 채널 길이를 줄일 때 장채널 모형의 전위 제어와 전류–전압 관계가 무너지는 현상군이다. 이 글은 먼저 장채널 기준을 세운 뒤, 그 기준을 깨뜨리는 물리적 기원을 분류하고 각 단채널 효과를 같은 순서로 설명한다. 별도 표기가 없으면 [MOSFET: Basic operation](basic-operation.md)의 nMOS 바이어스와 $V_T$, $I_\mathrm{OFF}$, subthreshold swing (SS) 추출 규약을 따른다.[1–3]

## 1. 장채널 MOSFET 기준

### (1) 1차원 게이트 제어

장채널 MOSFET에서는 유효 채널 길이 $L_\mathrm{eff}$가 소스·드레인 공핍 폭과 정전기적 특성 길이보다 충분히 크다. 채널 중앙의 전위는 주로 게이트에 수직인 방향으로 변하며, 채널 방향의 소스·드레인 경계조건은 소스 쪽 주입 장벽에 거의 도달하지 않는다. 이때 gradual-channel approximation은 전위 $\psi(x,y)$에 대해

$$
\left|\frac{\partial^2\psi}{\partial x^2}\right|
\ll
\left|\frac{\partial^2\psi}{\partial y^2}\right|
$$

을 가정한다. $x$는 소스에서 드레인으로 향하는 채널 좌표이고 $y$는 게이트에 수직인 좌표이다. 이 근사 아래에서 게이트는 수직 전기장을 통해 반전 전하를 정하고, 드레인은 채널을 따라 전하를 운반하는 수평 전기장을 제공한다. 따라서 낮은 $V_D$에서 추출한 $V_T$는 채널 길이와 드레인 전압에 거의 무관한 기준값 $V_{T,\mathrm{long}}$으로 수렴한다.[1–3]

### (2) 장채널 전류와 포화

강한 반전, 낮은 수평 전기장과 일정한 이동도 $\mu$를 가정한 장채널 charge-sheet model은 선형 영역과 포화 영역의 드레인 전류를 각각

$$
I_D
\approx
\mu C_\mathrm{ox}\frac{W}{L_\mathrm{eff}}
\left[(V_G-V_T)V_D-\frac{V_D^2}{2}\right],
\qquad
0\le V_D<V_G-V_T,
$$

$$
I_{D,\mathrm{sat}}
\approx
\frac{1}{2}\mu C_\mathrm{ox}\frac{W}{L_\mathrm{eff}}(V_G-V_T)^2,
\qquad
V_{D,\mathrm{sat}}\approx V_G-V_T
$$

로 준다. $C_\mathrm{ox}$는 단위 면적당 게이트 절연막 정전용량이고 $W$는 채널 폭이다. 포화는 드레인 끝의 반전 전하가 사라지는 pinch-off로 시작하며, 이상적인 장채널 기준에서는 포화 뒤 $I_D$가 $V_D$에 거의 무관하다. 또한 운반자 속도는 $v=\mu E_x$에 비례한다고 본다. 뒤에서 다루는 $V_T$의 길이·드레인 전압 의존성, SS 증가, 조기 전류 포화와 유한 출력 컨덕턴스는 모두 이 기준에서 벗어난 정도로 정의한다.[1–3]

!!! warning "[Interpretation Caveat]"
    이 장채널 식은 비교 기준이지 짧은 소자의 fitting 식이 아니다. 이동도 저하, 직렬저항, channel-length modulation (CLM), velocity saturation과 이차원 전위 결합을 무시하므로, 이 항들이 유의한 자료에 제곱 법칙을 강제로 맞추지 않는다.[1–4]

## 2. 단채널 효과의 도입과 물리적 기원

채널이 짧아지면 하나의 원인이 모든 비이상성을 만드는 것이 아니다. 먼저 **전위 제어**, **수송**, **포화 경계의 이동**, **운반자 에너지와 열화**를 분리해야 한다. 좁은 의미의 SCE는 소스 장벽에 대한 게이트 제어가 약해지는 정전기적 효과를 가리킨다. 이 글은 교과서에서 함께 다루는 짧은 채널의 수송·출력·신뢰성 효과까지 넓은 의미의 단채널 효과로 포함하되, 아래 표처럼 물리적 기원을 섞지 않는다.[1–4,8–15]

물리적 기원은 다음 네 범주로 구분한다.

| 물리적 기원 | 장채널 기준에서 깨지는 가정 | 직접 변하는 물리량 | 대표 결과 |
| --- | --- | --- | --- |
| 이차원 정전기 결합 | 채널 중앙 전위를 게이트가 독립적으로 제어함 | 소스 장벽 높이, 채널 공핍 전하의 게이트 분담, 깊은 바디의 전위 안장점 | $V_T$ 감소, DIBL, SS 증가, punch-through |
| 포화 경계의 이동 | pinch-off 뒤 유효 채널 길이가 일정함 | pinch-off 위치와 $L_\mathrm{eff}$ | 포화 영역의 유한 $g_{ds}$와 작은 $r_o$ |
| 고전계 수송 | $v=\mu E_x$와 일정한 이동도 | 운반자 표류 속도와 주행 시간 | 장채널 제곱 법칙보다 이른 전류 포화와 $g_m$ 감소 |
| 드레인 고전계와 열화 | 운반자 에너지 분포와 계면 상태가 바이어스 이력에 무관함 | impact-ionization rate, 바디 전류, 계면·절연막 결함 | 스트레스에 따른 $V_T$, $g_m$, $I_D$ 변화 |

이 기원에 대응하는 단채널 효과와 판별 지표는 다음과 같다. 같은 측정 곡선에 여러 효과가 겹칠 수 있으므로 현상 이름은 관측 결과가 아니라 원인–지표의 쌍으로 사용한다.[1–12]

| 단채널 효과 | 물리적 기원 | 대표 관측 결과 | 핵심 정량 지표 |
| --- | --- | --- | --- |
| threshold-voltage roll-off | charge sharing과 이차원 장벽 결합 | 채널이 짧아질수록 $V_T$가 장채널 기준보다 감소 | $V_T(L)-V_T(L_\mathrm{ref})$ |
| drain-induced barrier lowering (DIBL) | 드레인–소스 장벽의 정전기 결합 | 높은 $V_D$에서 전달 곡선이 낮은 $V_G$ 방향으로 이동 | $[V_T(V_{D,\mathrm{low}})-V_T(V_{D,\mathrm{high}})]/\Delta V_D$ |
| subthreshold-swing degradation | 소스 장벽에 대한 게이트 결합 약화 | 같은 전류 decade 변화에 더 큰 $V_G$ 변화가 필요 | $\mathrm{SS}=(d\log_{10}|I_D|/dV_G)^{-1}$ |
| punch-through | 소스·드레인 공핍영역의 깊은 바디 결합 | 꺼짐 바이어스에서도 표면 아래 전류 경로가 열림 | $V_\mathrm{PT}$, $g_{ds,\mathrm{off}}$ |
| channel-length modulation | 포화 뒤 pinch-off 지점의 소스 방향 이동 | 포화 영역에서도 $V_D$에 따라 $I_D$가 증가 | $g_{ds}$, $r_o$, 국소 $\lambda_\mathrm{CLM}$ |
| velocity saturation | 채널의 큰 수평 전기장 | 장채널 기준보다 낮은 $V_D$에서 전류가 포화 | $V_{DS,\mathrm{sat}}$, $g_m$, gate-overdrive 지수 |
| impact ionization·hot-carrier degradation | 드레인 부근 고전계에서의 운반자 가열과 결함 생성 | 바디 전류와 스트레스 후 전기적 특성 변화 | $|I_B/I_D|$, $\Delta V_T$, $\Delta g_m/g_m$ |

### (1) 이차원 정전기 결합

채널 길이가 소스·드레인 공핍영역의 크기와 소자의 정전기적 특성 길이에 가까워지면 전위 분포는 더 이상 게이트에 수직인 1차원 문제로 볼 수 없다. 소스와 드레인의 전기장이 채널 방향으로 침투하면서 게이트, 소스와 드레인이 채널 장벽을 함께 결정한다. 산화막이 얇고 바디가 얇으며 접합이 얕을수록 게이트 결합은 강해지고 드레인 결합은 약해진다.[1–3]

고전적인 charge-sharing model에서는 소스·드레인 공핍영역이 채널 공핍 전하의 일부를 지탱한다. 따라서 게이트가 같은 표면 상태를 만들기 위해 공급해야 하는 전하와 전압이 감소한다. 에너지 장벽 관점에서는 드레인 전위가 소스 쪽 전도대 장벽을 직접 낮춘다. 전자는 $V_T$ roll-off를, 후자는 DIBL을 드러내지만, 둘 다 장채널의 독립적인 게이트 제어가 무너진 결과이다.[1–3]

### (2) Natural length와 정전기적 축척

Natural length 또는 electrostatic scale length $\lambda$는 소스·드레인 경계에서 생긴 이차원 potential perturbation이 채널 방향으로 감쇠하는 특성 길이이다. Subthreshold에서 mobile charge를 무시하고 이차원 Poisson 또는 Laplace equation을 풀면, 장채널 해에서 벗어난 최저차 potential component $\delta\psi$는 대표적으로

$$
\frac{d^2\delta\psi}{dx^2}
-\frac{\delta\psi}{\lambda^2}=0,
\qquad
\delta\psi(x)
\approx A_S e^{-x/\lambda}
+A_D e^{-(L_\mathrm{eff}-x)/\lambda}
$$

처럼 쓸 수 있다. $x$는 소스에서 드레인으로 향하는 좌표, $L_\mathrm{eff}$는 유효 채널 길이, $A_S$와 $A_D$는 단자 바이어스와 경계조건으로 정해지는 계수이다. 따라서 채널 길이만이 아니라 무차원 비 $L_\mathrm{eff}/\lambda$가 정전기적 SCE의 크기를 결정한다. 같은 $L_\mathrm{eff}$에서도 $\lambda$가 작으면 드레인 전위가 소스 장벽에 도달하기 전에 더 빠르게 감쇠한다.[2,13–15]

Fully depleted single-gate silicon-on-insulator (FD-SOI) MOSFET에서 실리콘 막 내부 전위를 수직 방향의 포물선으로 근사한 대표 모형은

$$
\lambda_\mathrm{FD-SOI}
=
\sqrt{
\frac{\varepsilon_\mathrm{Si}}{\varepsilon_\mathrm{ox}}
t_\mathrm{Si}t_\mathrm{ox}
}
$$

를 준다. $\varepsilon_\mathrm{Si}$와 $\varepsilon_\mathrm{ox}$는 실리콘과 게이트 절연막의 유전율, $t_\mathrm{Si}$와 $t_\mathrm{ox}$는 실리콘 막과 게이트 절연막의 물리적 두께이다. 이 식은 얇은 절연막과 얇은 바디가 $\lambda$를 줄이는 이유를 보여주지만, 모든 MOSFET에 적용하는 보편식은 아니다.[13–15]

평면형 bulk MOSFET에서는 공핍영역 아래 경계가 고정된 평면이 아니며 공핍 깊이와 소스·드레인 접합 형상이 바이어스에 따라 달라진다. 따라서 $t_\mathrm{Si}$ 자리에 임의의 바디 두께를 넣지 않는다. Bulk 구조의 $\lambda$는 게이트 절연막의 물리적 두께와 유전율, 공핍 깊이, 접합 깊이·농도 구배와 경계조건을 포함한 고유값 문제로 구해야 한다. Natural length는 서로 다른 구조의 정전기적 제어를 비교하는 길이 척도이지 재료 하나에 고정된 상수가 아니다.[2,14,15]

| 설계 변화 | $\lambda$의 경향 | 물리적 의미 |
| --- | --- | --- |
| 게이트 절연막을 얇게 함 | 감소 | 게이트가 채널 전위를 더 가까이에서 제어함 |
| 공핍 깊이 또는 바디 두께를 줄임 | 감소 | 게이트에서 먼 전위 경로를 줄임 |
| 게이트가 채널을 여러 면에서 감쌈 | 감소 | 드레인 전기장이 게이트 경계에서 더 잘 종결됨 |
| $L_\mathrm{eff}/\lambda$를 크게 함 | SCE 감소 | 소스와 드레인의 전위 교란이 채널 중앙에서 덜 겹침 |

경계조건과 전위 분포를 함께 그린 원문 도식은 Yan et al.의 [Figure 3](https://doi.org/10.1109/16.141237), bulk와 double-gate 구조를 비교한 도식은 Frank et al.의 [Figure 1](https://doi.org/10.1109/55.720194)에서 확인할 수 있다. 두 그림은 재사용 조건이 확인되지 않아 저장소에 복제하지 않는다.[13,14]

!!! warning "[Interpretation Caveat]"
    문헌에서는 `natural length`, `scale length`와 `characteristic length`를 유사한 뜻으로 사용하지만, 구조와 근사법에 따라 정의와 수치 계수가 달라질 수 있다. 서로 다른 식의 $\lambda$를 비교할 때에는 게이트 구조, 절연막 두께의 정의, 바디 또는 공핍영역 경계조건과 유효 채널 길이의 정의를 먼저 맞춘다.[2,14,15]

## 3. Threshold-voltage roll-off 단채널 효과

Threshold-voltage roll-off는 채널 길이가 감소할수록 nMOS의 $V_T$가 장채널 값보다 낮아지는 현상이다. Charge sharing과 이차원 barrier coupling 때문에 게이트가 inversion을 만드는 데 필요한 전압이 줄어들며, 결과적으로 같은 $V_G$에서 subthreshold current가 증가한다.[1–3]

이 글에서는 $V_T$가 길이에 거의 무관한 장채널 소자 $L_\mathrm{ref}$를 기준으로 삼는다. 짧은 nMOS의 $V_T$가 기준값보다 낮으면 $\Delta V_{T,\mathrm{roll}}<0$으로 표시한다.[1,2,5]

!!! info "[Measurement]"
    낮은 $V_D$에서 채널 길이가 다른 여러 소자의 $I_D$–$V_G$를 측정하고, 모든 곡선에 같은 정전류 기준을 적용한다. 동일 웨이퍼의 소자군을 사용하여 폭, 직렬저항과 공정 변동의 영향을 줄인다. 각 길이에서

    $$
    \Delta V_{T,\mathrm{roll}}(L)
    =
    V_T(L)-V_T(L_\mathrm{ref})
    $$

    를 계산하고 $V_T$–$L$과 함께 제시한다. $L_\mathrm{ref}$, 기준전류, $V_D$, 온도와 폭 정규화를 기록한다.[1–3,5]

!!! warning "[Interpretation Caveat]"
    Halo implant와 채널 도핑의 불균일성은 짧은 채널에서 $V_T$가 오히려 증가하는 reverse short-channel effect를 만들 수 있다. 따라서 단조 감소를 가정하지 말고 공정 조건이 같은 소자끼리 비교한다.[1–3]

## 4. DIBL 단채널 효과

DIBL은 드레인 전압 증가가 소스–채널 에너지 장벽을 낮추어 같은 드레인 전류에 필요한 게이트 전압을 감소시키는 현상이다. 높은 $V_D$에서 전달 곡선이 낮은 $V_G$ 방향으로 이동하고 꺼짐 전류가 증가한다. 채널 길이가 짧고 게이트 제어가 약할수록 이동량이 커진다.[1–3]

이 글은 드레인 전압 증가에 따른 $V_T$ 감소를 양의 DIBL로 표시한다. $\Delta V_T/\Delta V_D$를 그대로 사용하는 문헌에서는 같은 현상이 음의 값으로 표시될 수 있다.[1,2]

!!! info "[Measurement]"
    동일 소자의 낮은·높은 $V_D$에서 $I_D$–$V_G$를 측정하고 같은 기준전류로 $V_T$를 추출한다. 양의 값으로 정의한

    $$
    \mathrm{DIBL}
    =
    \frac{V_T(V_{D,\mathrm{low}})-V_T(V_{D,\mathrm{high}})}
    {V_{D,\mathrm{high}}-V_{D,\mathrm{low}}}
    $$

    을 V/V 또는 mV/V로 계산한다. 가능하면 두 점뿐 아니라 여러 $V_D$에서 $V_T$–$V_D$의 선형성을 확인한다. 두 드레인 전압, $V_T$ 추출법, 기준전류, 온도와 채널 길이를 함께 보고한다.[1,2,5]

!!! warning "[Interpretation Caveat]"
    Gate-induced drain leakage (GIDL)나 게이트 전류가 높은 $V_D$ 곡선의 전류 바닥을 올리면, 정전류 교차점이 장벽 이동이 아닌 다른 누설을 반영할 수 있다. $I_B$와 $I_G$를 함께 확인한다.[1,6,7]

## 5. Subthreshold-swing degradation 단채널 효과

짧은 채널에서 소스 장벽에 대한 게이트 결합이 약해지고 드레인 결합이 커지면, 같은 전류 변화를 만드는 데 더 큰 게이트 전압 변화가 필요하여 SS가 증가할 수 있다. 계면 트랩과 공핍 정전용량도 SS를 악화하므로 길이 의존성만으로 원인을 확정할 수는 없다.[1–3]

!!! info "[Measurement]"
    낮은·높은 $V_D$의 반로그 $I_D$–$V_G$에서 계측기 바닥보다 충분히 높은 동일 전류 구간을 선택한다. 한 점의 수치 미분 대신 지정 구간을 국소 선형회귀하여

    $$
    \mathrm{SS}
    =
    \left(
    \frac{d\log_{10}(|I_D|/W)}{dV_G}
    \right)^{-1}
    =
    \ln(10)\,n\frac{kT}{q}
    $$

    를 mV/dec로 추출한다. 최소 SS와 지정 구간의 평균 SS를 구분하고, $T$, $V_D$, $L$, 전류 구간과 회귀법을 기록한다. 300 K의 약 $59.6\ \mathrm{mV/dec}$은 $n=1$인 열전자 수송의 이상 기준이다.[1–3,6,7]

## 6. Punch-through 단채널 효과

Punch-through는 소스와 드레인 공핍영역이 바디 깊은 곳에서 강하게 결합하여 전위 안장점을 낮추고, 게이트가 꺼져 있어도 소스–드레인 전류 경로를 여는 현상이다. 일반적인 DIBL보다 정전기적 제어 손실이 심한 상태이며, 전류가 표면보다 게이트에서 먼 벌크 경로를 따라 흐를 수 있다.[1,8,9]

!!! info "[Measurement]"
    $V_G$를 꺼짐 바이어스에 고정하고 여러 채널 길이에서 $I_D$–$V_D$를 측정한다. 바디 전압과 온도를 함께 변화시키며 $I_B$와 $I_G$를 동시에 읽어 GIDL과 접합 항복을 분리한다. 지정한 기준전류 $I_\mathrm{PT,ref}$에 대해

    $$
    V_\mathrm{PT}
    =
    V_D\ \text{at}\ |I_D|/W=I_\mathrm{PT,ref},
    \qquad
    g_{ds,\mathrm{off}}
    =
    \left.\frac{\partial |I_D|}{\partial V_D}\right|_{V_G=V_{G,\mathrm{off}}}
    $$

    를 추출한다. $I_\mathrm{PT,ref}$와 모든 단자 바이어스, $T$와 $L$을 함께 명시한다.[1,8,9]

## 7. Channel-length modulation 단채널 효과

다음 세 효과는 채널 길이가 짧을수록 두드러지지만, 앞의 네 정전기적 SCE와 물리적 기원이 다르다. 따라서 소스 장벽 제어의 손실로 환원하지 않고 출력 경계, 수송과 신뢰성의 지표를 각각 사용한다.[1–4]

Channel-length modulation (CLM)은 포화 이후 $V_D$가 증가할 때 드레인 쪽 pinch-off 지점이 소스 방향으로 이동하여 유효 채널 길이가 감소하는 현상이다. 이상적인 평탄 포화와 달리 $I_D$가 계속 증가하며, 짧은 채널에서는 같은 길이 변화가 차지하는 비율이 커질 수 있다.[1,2,4]

<figure markdown="span">
  ![n-channel MOSFET의 포화 영역에서 드레인 쪽 pinch-off가 형성된 개념도](images/mosfet-saturation.svg)
  <figcaption markdown="1">
    그림 1. n-channel MOSFET 포화 영역의 드레인 쪽 pinch-off.
    출처: Cyril Buttay; current correction by Cepheiden, “Mosfet saturation,” Wikimedia Commons,
    <a href="https://commons.wikimedia.org/wiki/File:Mosfet_saturation.svg">CC BY-SA 3.0</a>, 수정 없음.[16]
  </figcaption>
</figure>

$g_{ds}$는 출력 컨덕턴스, $r_o$는 출력 저항이다. $\lambda_\mathrm{CLM}$은 제한된 바이어스 구간에서 $I_D\approx I_{D0}(1+\lambda V_D)$로 근사할 때의 국소 CLM 계수이다.[1,2]

!!! info "[Measurement]"
    여러 $V_G$에서 $I_D$–$V_D$를 측정한다. 항복, 자기 가열과 직렬저항 지배를 피한 포화 구간을 정하고 그 구간을 선형회귀하여

    $$
    g_{ds}
    =
    \left.\frac{\partial I_D}{\partial V_D}\right|_{V_G},
    \qquad
    r_o=\frac{1}{g_{ds}},
    \qquad
    \lambda_\mathrm{CLM}
    \approx
    \frac{g_{ds}}{I_D}
    $$

    를 추출한다. $\lambda_\mathrm{CLM}$의 단위는 V$^{-1}$이다. 소자를 비교할 때에는 같은 $V_G$, 같은 gate overdrive 또는 같은 전류밀도 가운데 하나를 기준으로 정해 일관되게 적용한다.[1,2,4]

## 8. Velocity saturation 단채널 효과

Velocity saturation은 채널 방향 전기장이 커질 때 운반자 표류 속도가 더 이상 $v=\mu E$로 선형 증가하지 않고 유효 포화 속도에 접근하는 현상이다. 짧은 채널에서는 비교적 작은 $V_D$에서도 평균 전기장이 커진다. 따라서 전류가 장채널 제곱 법칙보다 일찍 포화되고, $I_D$의 gate-overdrive exponent가 2보다 작아질 수 있다.[1–3,10]

대표적인 경험식은

$$
v(E)\approx\frac{\mu E}{1+E/E_\mathrm{sat}}
$$

이다. 낮은 전기장에서는 $v\approx\mu E$, 높은 전기장에서는 $v\approx\mu E_\mathrm{sat}$에 접근한다. 실제 실리콘의 속도–전기장 관계는 온도, 결정 방향과 비국소 수송에 의존하므로 $E_\mathrm{sat}$을 보편적 재료상수로 해석하지 않는다.[3,10]

!!! info "[Measurement]"
    여러 채널 길이에서 $I_D$–$V_D$, $I_D$–$V_G$와 transconductance $g_m=\partial I_D/\partial V_G$를 측정한다. 출력 곡선에서 정해 둔 전이 기준으로 $V_{DS,\mathrm{sat}}$을 읽고, 지정한 gate-overdrive 구간에서

    $$
    \alpha
    =
    \frac{\partial\ln I_{D,\mathrm{sat}}}
    {\partial\ln(V_G-V_T)}
    $$

    를 회귀한다. $V_{DS,\mathrm{sat}}$, 최대 $g_m$, $\alpha$와 맞춤 구간을 함께 보고한다. 온도 또는 외부 직렬저항 비교로 이동도 저하와 직렬저항을 점검하며, $\alpha$만으로 velocity saturation을 단정하지 않는다.[1–3,10]

## 9. Hot-carrier degradation 단채널 효과

Impact ionization은 드레인 부근의 큰 전기장에서 에너지를 얻은 운반자가 전자–정공 쌍을 만드는 과정이다. nMOS에서는 생성된 정공 일부가 바디 전류가 된다. hot-carrier degradation은 고에너지 운반자가 절연막 또는 계면에 결함과 포획 전하를 만들어 $V_T$, $g_m$과 $I_D$를 시간에 따라 변화시키는 신뢰성 현상이다.[1,11,12]

!!! info "[Measurement]"
    초기 전달·출력 곡선을 저장한 뒤 지정한 $(V_G,V_D,V_B,T)$에서 소자를 스트레스한다. 일정한 간격마다 동일한 낮은 전압 판독 조건으로 특성을 다시 측정하고, 스트레스 중 $I_B$와 $I_D$를 기록한다. 순간 고전계 신호는 $|I_B/I_D|$로, 열화는

    $$
    \Delta V_T=V_T(t)-V_T(0),
    \qquad
    \frac{\Delta g_m}{g_m(0)}
    =
    \frac{g_m(t)-g_m(0)}{g_m(0)},
    \qquad
    \frac{\Delta I_D}{I_D(0)}
    =
    \frac{I_D(t)-I_D(0)}{I_D(0)}
    $$

    로 추출한다. 수명을 보고할 때에는 열화 판정 기준과 듀티비뿐 아니라, 스트레스 조건에서 실제 사용 조건까지 외삽할 때 쓴 모형도 함께 기록한다.[7,11,12]

## 10. 억제 구조와 trade-off

SCE 억제의 공통 목표는 natural length $\lambda$를 줄여 드레인–채널 결합보다 게이트–채널 결합을 강하게 만드는 것이다. 실제 구조에서는 게이트 절연막, 채널·웰, 소스·드레인 확장 영역과 바디 형상을 함께 조절한다. 이 과정에는 켜짐 전류, 누설, 정전용량과 신뢰성 사이의 trade-off가 따른다.[1–3,13–15]

### (1) 게이트 절연막과 Gate Control

작은 EOT는 $C_\mathrm{ox}$를 키우고 게이트의 표면전위 제어를 강화하여 $\lambda$, DIBL과 $V_T$ roll-off를 줄인다. SiO$_2$의 물리적 두께를 계속 줄이면 direct tunneling이 급격히 증가하므로, high-$k$/metal gate는 같은 EOT에서 더 두꺼운 물리적 장벽을 사용한다. 다만 계면층, 고정전하, 계면 트랩과 이동도 저하를 함께 평가해야 한다.[1–3]

### (2) 얕은 접합과 Channel Engineering

얕은 소스·드레인 접합은 드레인 전위가 채널 아래로 침투하는 길이를 줄인다. Retrograde well은 표면의 이동도 저하를 완화하면서 공핍 깊이를 제한하고, halo implant는 소스·드레인 끝 근처의 국소 바디 도핑을 높여 charge sharing, DIBL과 punch-through를 억제한다.[1–3]

그러나 halo가 강하면 짧은 채널에서 양쪽 분포가 겹쳐 reverse short-channel effect를 만들고, 높은 접합 전기장이 BTBT와 GIDL을 늘릴 수 있다. 도핑 증가는 불순물 산란과 통계적 변동성도 키울 수 있으므로 $V_T$–$L$의 평탄화만으로 최적화를 판정하지 않는다.[1–3]

### (3) LDD와 Drain Engineering

Lightly doped drain (LDD)은 고농도 드레인과 채널 사이에 낮은 농도의 확장 영역을 두어 드레인 쪽 전위 강하를 분산하고 첨두 수평 전기장을 낮춘다. 이에 따라 impact ionization과 hot-carrier 생성이 줄고, 특정 설계에서는 punch-through와 $V_T$ roll-off도 완화될 수 있다.[11,17,18]

LDD의 낮은 농도 확장 영역은 동시에 소스·드레인 직렬저항을 늘려 $I_{D,\mathrm{sat}}$과 $g_m$을 낮춘다. Spacer 아래에서 생성된 계면 트랩은 확장 영역의 저항을 더 높여 열화를 만들 수 있다. 주입량을 높이면 직렬저항은 줄지만 전계 완화 효과와 hot-carrier degradation에 대한 여유가 감소한다. 따라서 spacer 길이, 겹침, 확장 영역 농도와 열 공정을 함께 최적화해야 한다.[17,18]

따라서 LDD는 natural length를 직접 줄이는 multigate 구조와 같은 보편적 정전기 해법이 아니다. 주된 역할은 드레인 근처의 **전계 분포를 바꾸는 것**이며, SCE 개선 여부는 DIBL·$V_T$–$L$과 함께 직렬저항, $I_\mathrm{ON}$, 기생 정전용량과 hot-carrier 수명으로 확인한다.[3,17,18]

### (4) Thin-Body와 Multigate 구조

Fully depleted silicon-on-insulator (FD-SOI)의 얇은 바디, FinFET과 gate-all-around (GAA)는 게이트에서 먼 전위 경로를 제거하고 채널을 여러 면에서 제어한다. 같은 $L_\mathrm{eff}$에서 $\lambda$를 줄여 $V_T$ roll-off, DIBL과 SS degradation을 동시에 억제할 수 있으며, 무거운 채널 도핑에 덜 의존할 수 있다.[1–3,13–15]

| 설계 수단 | 직접 바꾸는 물리량 | 주로 개선하는 항목 | 함께 확인할 trade-off |
| --- | --- | --- | --- |
| 작은 EOT, high-$k$/metal gate | $C_\mathrm{ox}$, 게이트 결합 | DIBL, $V_T$ roll-off, SS | gate tunneling, 계면 결함, 이동도 |
| 얕은 접합 | 접합 깊이와 드레인 결합 | DIBL, punch-through | 접촉·직렬저항, 접합 정전용량 |
| halo·retrograde well | 공핍 폭과 charge sharing | $V_T$ roll-off, DIBL, punch-through | reverse SCE, BTBT·GIDL, 변동성 |
| LDD·graded extension | 드레인 첨두 전기장 | hot-carrier, 일부 GIDL·punch-through | 직렬저항, $I_\mathrm{ON}$, 기생 정전용량 |
| thin-body·multigate | $\lambda$, 최악 전류 경로 | DIBL, SS, $V_T$ roll-off | 공정 복잡도, 접촉저항, 폭 정의 |

억제 효과는 하나의 DIBL 값만으로 판단하지 않는다. $V_T$–$L$, DIBL–$L$, SS–$L$, $I_\mathrm{OFF}$와 함께 $I_\mathrm{ON}$, $g_m$, $g_{ds}$, 직렬저항과 신뢰성 지표를 비교해야 한다.[1–3,5,17,18]

## 11. 요약

- 장채널 기준은 1차원 게이트 제어, 저전계 속도 관계와 일정한 포화 채널 길이를 가정한다.
- 단채널 효과의 물리적 기원은 이차원 정전기 결합, 포화 경계의 이동, 고전계 수송과 드레인 고전계에 의한 열화로 구분해야 한다.
- Natural length $\lambda$는 단자 전위 교란의 채널 방향 감쇠 길이이며, $L_\mathrm{eff}/\lambda$가 정전기적 SCE를 비교하는 핵심 비이다.
- Threshold-voltage roll-off, DIBL, SS degradation과 punch-through는 서로 연관되지만 각각 정의와 추출법이 다르다.
- CLM, velocity saturation과 hot-carrier degradation은 넓은 의미의 단채널 효과에 포함할 수 있지만 각각 출력·수송·신뢰성의 지표로 판별해야 한다.
- SCE 억제의 핵심은 게이트 결합 강화, 드레인 결합 약화와 게이트에서 먼 전류 경로 제거이며, LDD는 주로 드레인 첨두 전기장을 완화한다.

## 12. 참고문헌

1. C. Hu, *Modern Semiconductor Devices for Integrated Circuits*, Chapters 6–7, Pearson (2010). [Chapter 7 저자 제공 PDF](https://www.chu.berkeley.edu/wp-content/uploads/2020/01/Chenming-Hu_ch7.pdf).
2. Y. Taur and T. H. Ning, *Fundamentals of Modern VLSI Devices*, 2nd ed., Cambridge University Press (2009), Appendix 10. [Generalized MOSFET Scale Length Model](https://www.cambridge.org/highereducation/books/fundamentals-of-modern-vlsi-devices/FC4BC491DDD2F339A03BE28C6E174169/generalized-mosfet-scale-length-model/94556AB782696F64CBF2DA4389139BA4), [DOI: 10.1017/CBO9781139195065](https://doi.org/10.1017/CBO9781139195065).
3. D. J. Frank et al., “Device Scaling Limits of Si MOSFETs and Their Application Dependencies,” *Proceedings of the IEEE* **89**, 259–288 (2001). [DOI: 10.1109/5.915374](https://doi.org/10.1109/5.915374).
4. BSIM Research Group, “BSIM4,” University of California, Berkeley. [공식 모델 페이지](https://bsim.berkeley.edu/models/bsim4/).
5. A. Ortiz-Conde et al., “Revisiting MOSFET Threshold Voltage Extraction Methods,” *Microelectronics Reliability* **53**, 90–104 (2013). [DOI: 10.1016/j.microrel.2012.09.015](https://doi.org/10.1016/j.microrel.2012.09.015).
6. Keysight Technologies, “DC MOSFET Characterization at the Wafer Level,” Application Note 5990-5547EN (2019). [공식 문서](https://www.keysight.com/my/en/assets/7018-02489/application-notes/5990-5547.pdf).
7. D. K. Schroder, *Semiconductor Material and Device Characterization*, 3rd ed., Wiley (2006). [DOI: 10.1002/0471749095](https://doi.org/10.1002/0471749095).
8. N. Kotani and S. Kawazu, “Computer Analysis of Punch-Through in MOSFETs,” *Solid-State Electronics* **22**, 63–70 (1979). [DOI: 10.1016/0038-1101(79)90172-2](https://doi.org/10.1016/0038-1101(79)90172-2).
9. J. J. Barnes, K. Shimohigashi, and R. W. Dutton, “Short-Channel MOSFET’s in the Punchthrough Current Mode,” *IEEE Transactions on Electron Devices* **26**, 446–453 (1979). [DOI: 10.1109/T-ED.1979.19447](https://doi.org/10.1109/T-ED.1979.19447).
10. C. Canali, G. Majni, R. Minder, and G. Ottaviani, “Electron and Hole Drift Velocity Measurements in Silicon and Their Empirical Relation to Electric Field and Temperature,” *IEEE Transactions on Electron Devices* **22**, 1045–1047 (1975). [DOI: 10.1109/T-ED.1975.18267](https://doi.org/10.1109/T-ED.1975.18267).
11. C. Hu et al., “Hot-Electron-Induced MOSFET Degradation—Model, Monitor, and Improvement,” *IEEE Transactions on Electron Devices* **32**, 375–385 (1985). [DOI: 10.1109/T-ED.1985.21952](https://doi.org/10.1109/T-ED.1985.21952).
12. A. Acovic, G. La Rosa, and Y.-C. Sun, “A Review of Hot-Carrier Degradation Mechanisms in MOSFETs,” *Microelectronics Reliability* **36**, 845–869 (1996). [DOI: 10.1016/0026-2714(96)00022-4](https://doi.org/10.1016/0026-2714(96)00022-4).
13. R.-H. Yan, A. Ourmazd, and K. F. Lee, “Scaling the Si MOSFET: From Bulk to SOI to Bulk,” *IEEE Transactions on Electron Devices* **39**, 1704–1710 (1992). [DOI: 10.1109/16.141237](https://doi.org/10.1109/16.141237).
14. D. J. Frank, Y. Taur, and H.-S. P. Wong, “Generalized Scale Length for Two-Dimensional Effects in MOSFET’s,” *IEEE Electron Device Letters* **19**, 385–387 (1998). [DOI: 10.1109/55.720194](https://doi.org/10.1109/55.720194).
15. H.-S. P. Wong, “Beyond the Conventional Transistor,” *IBM Journal of Research and Development* **46**, 133–168 (2002). [DOI: 10.1147/rd.462.0133](https://doi.org/10.1147/rd.462.0133).
16. Cyril Buttay and Cepheiden, “Mosfet saturation,” Wikimedia Commons (2008; current correction 2021), CC BY-SA 3.0. [파일 설명과 라이선스](https://commons.wikimedia.org/wiki/File:Mosfet_saturation.svg).
17. D. J. Mountain and D. Burnell, “An Evaluation of Conventional and LDD Devices for Submicron Geometries,” *Solid-State Electronics* **33**, 565–570 (1990). [DOI: 10.1016/0038-1101(90)90241-6](https://doi.org/10.1016/0038-1101(90)90241-6).
18. S. S. Chung and J. J. Yang, “A New Approach for Characterizing Structure-Dependent Hot-Carrier Effects in Drain-Engineered MOSFET’s,” *IEEE Transactions on Electron Devices* **46**, 1371–1377 (1999). [DOI: 10.1109/16.772478](https://doi.org/10.1109/16.772478).
