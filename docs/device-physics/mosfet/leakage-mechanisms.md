---
title: "(1) MOSFET: Leakage Current"
description: MOSFET의 대표 누설 전류를 전류 경로별 물리 기작, 측정 방법과 정량 지표로 설명
status: verified
last_verified: 2026-07-31
---

# (1) MOSFET: Leakage Current

금속-산화막-반도체 전계효과 트랜지스터(metal-oxide-semiconductor field-effect transistor, MOSFET)의 누설 전류는 하나의 물리 기작이 아니다. 꺼짐 상태(off-state)에서 측정한 드레인 전류에는 채널 장벽을 넘는 전류, 게이트 절연막을 통과하는 전류, 역바이어스 접합 전류, 드레인 가장자리의 고전계 전류와 벌크 관통 전류가 함께 포함될 수 있다. 따라서 총 누설 전류를 먼저 정의한 뒤 전류가 흐르는 경로와 단자별 바이어스를 따라 각 성분을 분리해야 한다.[1–3]

<figure markdown="span">
  ![n채널 MOSFET에서 게이트 누설과 문턱아래 누설이 흐르는 대표 경로](images/leakage-current-overview.png)
  <figcaption>
    그림 1. n채널 MOSFET에서 게이트 누설과 문턱아래 누설이 흐르는 대표 경로. 주요 누설 경로를 한 소자에 함께 표시한 그림은 Roy 등의
    <a href="https://dvdtang.nl/joomla/images/Roy11_S5.pdf">Fig. 3</a>에서 볼 수 있다.
    출처: Tosaka, “Leakage Current (2 models),” Wikimedia Commons,
    <a href="https://commons.wikimedia.org/wiki/File:Leakage_Current_(2_models).PNG">CC BY-SA 3.0</a>, 수정 없음.[14]
  </figcaption>
</figure>

## 1. 범위와 공통 규약

기본 대상은 증가형 평면 벌크 n채널 MOSFET(n-channel MOSFET, nMOS)이다. 별도 표기가 없으면 직류(direct current, DC), 실온, $V_S=V_B=0$을 가정한다. 전압은 $V_{XY}=V_X-V_Y$로 정의하고, 단자전류는 방향 혼동을 피하기 위해 크기 $|I_G|$, $|I_D|$, $|I_S|$, $|I_B|$로 표시한다.

- 꺼짐 전류(off-state current, $I_\mathrm{OFF}$)는 미리 선언한 꺼짐 바이어스에서 측정한 $|I_D|$이다. 대표적인 조건은 $V_G=0$, $V_D=V_\mathrm{DD}$이지만, 전원 전압·온도·소자 치수와 함께 명시해야 한다.
- 문턱전압(threshold voltage, $V_T$)은 모든 비교 곡선에서 동일한 방법으로 추출한다. 이 문서에서는 지정한 기준전류에 대응하는 게이트 전압을 읽는 정전류법(constant-current method)을 기본 규약으로 사용한다.[2,8]
- 전류는 필요에 따라 유효 게이트 폭 $W$, 게이트 면적 $A_G$, 접합 면적 $A_\mathrm{junc}$ 또는 접합 둘레 $P_\mathrm{junc}$로 정규화한다. 서로 다른 정규화값을 직접 비교하지 않는다.

!!! warning "[재현 조건]"
    $I_\mathrm{OFF}$ 한 값만으로는 측정을 재현할 수 없다. $V_G$, $V_D$, $V_S$, $V_B$, 온도, 소자 폭·길이, 정규화 방식, 전압 훑기 방향과 적분 시간을 함께 기록한다.[8–10]

## 2. 꺼짐 전류의 구성

장채널 MOSFET의 이상적인 꺼짐 상태에서도 문턱전압 아래의 열적 전류와 역바이어스 접합 전류는 0이 아니다. 소자를 축소하면 게이트 절연막 터널링, 드레인 가장자리의 고전계 터널링과 소스–드레인 정전기적 결합도 중요해진다. 이 때문에 $I_\mathrm{OFF}$는 특정 기작의 지표가 아니라 여러 성분을 합한 회로 수준의 결과값이다.[1–3]

| 전류 경로 | 대표 물리 기작 | 우선 관찰하는 곡선 | 정량 지표 |
| --- | --- | --- | --- |
| 소스 → 채널 → 드레인 | 문턱아래 열방출·확산 | 반로그 $I_D$–$V_G$ | $I_\mathrm{OFF}/W$, 문턱아래 스윙, 드레인 유도 장벽 저하 |
| 게이트 → 절연막 → 채널·소스·드레인 | 직접 또는 Fowler–Nordheim형 터널링 | $I_G$–$V_G$, 단자별 전류 분배 | $J_G$, 가장자리 전류/$W$ |
| 드레인·소스 접합 → 바디 | 생성·확산, 고전계 밴드 간 터널링 | 접합 역방향 $I$–$V$ | 면적·둘레 전류밀도, 겉보기 활성화 에너지 |
| 게이트–드레인 겹침 영역 → 드레인·바디 | 밴드 간 또는 트랩 보조 터널링 | 낮은 $V_G$, 높은 $V_D$의 $I_D$·$I_B$ | 폭 정규화 전류, 발생 전압 |
| 소스 → 깊은 바디 → 드레인 | 소스·드레인 공핍영역 결합 | 꺼짐 $I_D$–$V_D$, 채널 길이 비교 | 펀치스루 전압, 꺼짐 출력 컨덕턴스 |

이 분류는 전류의 지배 경로를 기준으로 한다. 실제 소자에서는 여러 경로가 동시에 열릴 수 있으므로, 한 곡선의 모양만으로 기작을 확정하지 않는다.[1,7]

## 3. 채널 경로: 문턱아래 누설

### (1) 물리적 기원

문턱아래 누설(subthreshold leakage)은 게이트 전압이 $V_T$보다 낮을 때 소스의 캐리어가 유한한 소스–채널 에너지 장벽을 넘어 드레인으로 확산하면서 생긴다. 약한 반전(weak inversion)에서는 표면 캐리어 농도가 게이트 전압에 지수적으로 의존한다. 짧은 채널에서는 드레인 유도 장벽 저하(drain-induced barrier lowering, DIBL)가 소스 쪽 장벽을 추가로 낮춰 같은 게이트 전압에서 전류를 증가시킨다.[1–3]

<figure markdown="span">
  ![게이트가 꺼진 n채널 MOSFET에서 드레인으로 흐르는 문턱아래 누설](images/fet-subthreshold-leakage.png)
  <figcaption>
    그림 2. $V_G=0$인 n채널 MOSFET의 문턱아래 누설 경로.
    출처: Fadeaway919, “FET subthreshold leakage,” Wikimedia Commons,
    <a href="https://commons.wikimedia.org/wiki/File:FET_subthreshold_leakage.png">CC BY-SA 3.0</a>, 수정 없음.[15]
  </figcaption>
</figure>

약한 반전의 대표 근사식은

$$
I_\mathrm{sub}\approx I_0\frac{W}{L}
\exp\left(\frac{V_{GS}-V_T+\eta_DV_{DS}}{nU_T}\right)
\left[1-\exp\left(-\frac{V_{DS}}{U_T}\right)\right]
$$

이다. 여기서 $U_T=kT/q$는 열전압, $n$은 문턱아래 기울기 계수, $\eta_D$는 드레인 결합을 나타내는 계수이다. $I_0$의 정의는 모형마다 다르므로 이 식은 절대 전류의 보편식이 아니라 게이트 전압·온도·드레인 전압에 대한 민감도를 설명하는 근사식으로 사용한다.[1–3]

문턱아래 스윙(subthreshold swing, SS)은 드레인 전류를 한 자릿수 변화시키는 데 필요한 게이트 전압으로 정의한다.

$$
\mathrm{SS}
=\left(\frac{d\log_{10}|I_D|}{dV_G}\right)^{-1}
=\ln(10)\,n\frac{kT}{q}.
$$

$n=1$인 열전자 수송의 이상 한계는 300 K에서 약 $59.6\ \mathrm{mV/dec}$이다. 실제 벌크 MOSFET에서는 공핍층과 계면 트랩의 정전용량 때문에 일반적으로 $n>1$이다.[1–3]

!!! info "[측정 방법]"
    낮은 $V_D$와 실제 꺼짐 조건에 가까운 높은 $V_D$에서 반로그 $I_D$–$V_G$를 측정한다. 같은 전압 훑기에서 $I_G$와 $I_B$를 동시에 읽어 드레인 전류 바닥이 다른 누설 성분에 의해 제한되는지 확인한다.[1,2,7]

!!! abstract "[정량 지표]"
    지정한 전류 구간을 선형회귀하여 SS를 구하고, 구간·온도·$V_D$를 함께 기록한다. $I_\mathrm{OFF}/W$는 선언한 꺼짐 바이어스에서 읽는다. DIBL은 동일한 $V_T$ 추출 규약으로 얻은 낮은·높은 $V_D$ 곡선의 수평 이동에서 계산한다.[1,2,8]

!!! warning "[해석 주의]"
    $I_G$ 또는 $I_B$가 $I_D$와 비슷한 크기이면 관측한 전류 바닥을 순수한 문턱아래 누설로 해석할 수 없다. 계측기 누설과 광전류도 먼저 배제해야 한다.[7,9,10]

## 4. 게이트 절연막 경로: 터널링 누설

게이트 절연막 누설(gate-dielectric leakage)은 캐리어가 유한한 절연막 장벽을 양자역학적으로 통과하면서 생긴다. 얇은 절연막의 사다리꼴 장벽에서는 직접 터널링이, 높은 절연막 전기장에서는 Fowler–Nordheim형 터널링이 나타날 수 있다. 게이트–드레인 겹침 가장자리의 직접 터널링은 면적 성분과 다른 단자 분배를 보일 수 있다.[1,2,4]

일차원 Wentzel–Kramers–Brillouin 근사(Wentzel–Kramers–Brillouin approximation, WKB)에서 투과율은

$$
T(E)\approx
\exp\left[
-\frac{2}{\hbar}
\int_{x_1}^{x_2}
\sqrt{2m_\mathrm{ox}^{*}\left(U(x)-E\right)}\,dx
\right]
$$

로 쓸 수 있다. $m_\mathrm{ox}^{*}$는 절연막 유효질량, $U(x)$는 장벽 에너지, $x_1$과 $x_2$는 고전적 회귀점이다. 이 식은 두께와 장벽 모양에 대한 지수 민감도를 보여준다. 실제 전류밀도 계산에는 전극 상태밀도, 밴드 오프셋, 영상힘과 다층 절연막 구조를 추가해야 한다.[2,4,11]

!!! info "[측정 방법]"
    소스와 드레인을 같은 전위로 묶어 채널 방향 전기장을 줄인 뒤 $I_G$–$V_G$를 측정한다. $I_S$와 $I_D$도 함께 읽어 게이트 전류가 어느 단자로 분배되는지 확인한다. 게이트 면적과 겹침 길이가 다른 비교 소자군을 사용하면 면적 성분과 가장자리 성분을 구분할 수 있다.[2,4,7]

!!! abstract "[정량 지표]"
    면적 성분은 $J_G=|I_G|/A_G$, 가장자리 성분은 전류/$W$로 보고한다. 게이트 절연막 두께, 등가 산화막 두께(equivalent oxide thickness, EOT), 전압 극성과 온도를 반드시 병기한다.[2,4,7]

## 5. 접합과 드레인 가장자리 경로

### (1) 역바이어스 소스·드레인 접합 누설

꺼짐 상태의 드레인–바디와 소스–바디 pn 접합은 역바이어스된다. 낮거나 중간 전기장에서는 공핍영역의 생성 전류와 중성영역의 소수 캐리어 확산이, 높은 전기장과 고농도 접합에서는 밴드 간 터널링(band-to-band tunneling, BTBT)이 중요해질 수 있다. 접합 바닥과 절연 가장자리는 결함 밀도와 전기장이 다르므로 면적 성분과 둘레 성분을 분리해야 한다.[1,2,11]

비교 소자군의 전류는

$$
|I_\mathrm{junc}|
\approx J_A A_\mathrm{junc}+J_P P_\mathrm{junc}
$$

로 분해할 수 있다. $J_A$와 $J_P$는 각각 단위 면적과 단위 길이당 전류이다. 이 식은 단일 기작의 지배 방정식이 아니라 기하학적으로 성분을 분리하는 실험 모형이다.[7,11]

!!! info "[측정 방법]"
    독립된 드레인–바디 다이오드 구조에서 역방향 $I$–$V$와 온도 의존성을 측정하는 것이 가장 명확하다. 트랜지스터에서는 게이트와 소스를 바디 전위에 두어 채널을 끄고, 드레인 가장자리의 고전계 누설이 지배하지 않는 전압 범위를 먼저 확인한다.[1,7,11]

!!! abstract "[정량 지표]"
    접합 면적과 둘레가 다른 구조를 함께 회귀하여 $J_A$와 $J_P$를 추출한다. 온도에 따른 Arrhenius 도표에서는 겉보기 활성화 에너지를 구하되, 그 값 하나만으로 생성 전류와 터널링을 확정하지 않는다.[1,7,11]

### (2) 게이트 유도 드레인 누설

게이트 유도 드레인 누설(gate-induced drain leakage, GIDL)은 nMOS에서 낮거나 음의 게이트 전압과 높은 드레인 전압이 게이트–드레인 겹침 부근의 밴드 굽힘과 국소 전기장을 증가시킬 때 나타난다. 직접 BTBT가 기본 경로이며, 산화막 또는 계면 트랩이 존재하면 트랩 보조 터널링(trap-assisted tunneling, TAT)이 섞일 수 있다.[1,5,6]

직접 BTBT의 전기장 의존성은 단순화하면

$$
J_\mathrm{BTBT}\propto F^2\exp\left(-\frac{B}{F}\right)
$$

로 나타낼 수 있다. $F$는 드레인 가장자리의 국소 전기장이고 $B$는 밴드갭과 유효질량에 의존하는 계수이다. 외부 단자전압을 $F$와 동일시하면 겹침 구조와 도핑의 영향을 잃으므로 이 식은 정성적 전기장 경향에만 사용한다.[5,6,11]

!!! info "[측정 방법]"
    $V_S=V_B=0$, $V_D>0$에서 $V_G$를 0에서 음의 방향으로 변화시키거나, 여러 $V_G$에서 $I_D$–$V_D$를 측정한다. 전자–정공 쌍 생성과 게이트 터널링을 구분하기 위해 $I_B$와 $I_G$를 동시에 읽는다.[1,5–7]

!!! abstract "[정량 지표]"
    $I_\mathrm{GIDL}/W$를 $(V_G,V_D,V_B,T)$와 함께 보고한다. 공정 비교에는 미리 정한 기준전류에 도달하는 발생 전압이나, 국소 전기장의 대용 변수를 사용한 전류 기울기를 쓸 수 있다. 대용 변수와 맞춤 구간을 반드시 명시한다.[1,5–7]

## 6. 벌크 경로: 펀치스루 누설

펀치스루 누설(punch-through leakage)은 채널 길이가 짧거나 바디 도핑이 낮을 때 소스와 드레인의 공핍영역이 깊은 바디에서 강하게 결합하여 발생한다. 두 영역 사이의 전위 안장점이 충분히 낮아지면 게이트가 꺼져 있어도 소스에서 드레인으로 벌크 전류 경로가 열린다. 이는 표면의 장벽 저하와 연속적인 정전기 문제이지만, 지배 전류 경로는 표면의 문턱아래 누설과 다를 수 있다.[1,2,12,13]

!!! info "[측정 방법]"
    $V_G$를 꺼짐 바이어스에 고정하고 여러 채널 길이에서 $I_D$–$V_D$를 측정한다. 바디 전압과 온도를 추가로 변화시키고, $I_B$와 $I_G$를 함께 읽어 GIDL과 접합 항복을 분리한다.[1,2,12,13]

!!! abstract "[정량 지표]"
    펀치스루 전압(punch-through voltage, $V_\mathrm{PT}$)은 지정한 폭 정규화 전류에 도달하는 $V_D$로 정의한다. 꺼짐 출력 컨덕턴스 $g_{ds,\mathrm{off}}=\partial I_D/\partial V_D$의 증가도 보조 지표로 사용한다. 기준전류, $V_G$, $V_B$, 온도와 채널 길이를 함께 보고한다.[1,2,12,13]

## 7. 성분 분리를 위한 측정 순서

소스 측정 장치(source-measure unit, SMU)를 게이트·드레인·소스·바디에 각각 연결하면 네 단자전류를 동시에 읽을 수 있다. 정상상태에서 부호를 포함한 전류 합이 0에 가까운지 확인하면 배선 오류와 측정 바닥을 찾는 데 도움이 된다. 저전류 측정에서는 삼축 케이블 가딩, 차폐, 암상태, 충분한 안정화 시간과 빈 패드 측정이 필요하다.[7,9,10]

| 관측 결과 | 다음 확인 | 우선 검토할 기작 |
| --- | --- | --- |
| 낮은 $V_D$의 반로그 $I_D$–$V_G$가 일정 기울기를 보임 | SS와 온도 의존성 | 문턱아래 누설 |
| 높은 $V_D$에서 $I_D$–$V_G$가 수평 이동 | 같은 방법의 $V_T$와 DIBL | 장벽 저하가 강화한 문턱아래 누설 |
| $|I_G|$가 크고 게이트 면적에 비례 | $I_S$·$I_D$ 전류 분배 | 게이트 절연막 터널링 |
| 게이트 전압과 무관한 접합 전류 | 면적·둘레와 온도 의존성 | 역바이어스 접합 누설 |
| 낮은 $V_G$와 높은 $V_D$에서 $I_D$·$I_B$ 증가 | $I_G$ 배제, 드레인 가장자리 전기장 | GIDL |
| 짧은 채널에서 꺼짐 $I_D$–$V_D$가 급증 | 채널 길이·바디 전압 의존성 | 펀치스루 |

이 표는 단일 관측으로 결론을 내리는 결정표가 아니다. 다음 순서로 서로 다른 증거를 겹쳐 판단한다.

1. 낮은·높은 $V_D$의 $I_D$–$V_G$에서 채널 장벽 제어를 확인한다.
2. 같은 측정에서 $I_G$, $I_S$, $I_B$와 단자전류 합을 확인한다.
3. 꺼짐 $I_D$–$V_D$와 $I_G$–$V_G$로 전압 민감도를 분리한다.
4. 폭·길이·접합 면적·둘레가 다른 비교 소자군과 온도 의존성을 사용한다.
5. 이력현상이나 시간에 따른 이동이 보이면 전압 범위를 줄이고 새 소자에서 반복한다.[7,9,10]

## 8. 요약

- $I_\mathrm{OFF}$는 여러 누설 경로를 합한 값이므로 단독으로 물리 기작을 특정하지 못한다.
- 채널 경로는 SS와 DIBL, 게이트 절연막 경로는 $J_G$와 단자별 전류 분배로 평가한다.
- 접합 누설은 면적·둘레와 온도 의존성, GIDL은 드레인 가장자리 전기장과 바디 전류로 구분한다.
- 펀치스루는 여러 채널 길이의 꺼짐 $I_D$–$V_D$와 바디 전압 의존성으로 확인한다.
- 모든 정량 지표에는 바이어스, 온도, 정규화 기준과 추출 구간을 함께 기록해야 한다.

## 9. 참고문헌

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
