---
description: Büttiker probe의 fictitious terminal, 영전류 조건, voltage·dephasing probe의 차이와 NEGF 구현·검증 절차를 설명
---

# NEGF: Büttiker probe method

**Büttiker probe method**는 위상 결맞음 수송 영역에 가상의 reservoir를 연결하고, 그 reservoir로 흐르는 전류가 0이 되도록 분포를 조정하여 dephasing과 에너지 완화를 현상론적으로 모사하는 방법이다. Probe로 들어간 전자는 위상 정보를 잃은 다른 전자로 재주입되므로 간섭은 약해지지만 전하는 누설되지 않는다.[1–6]

이 글은 정상 상태의 비상호작용 또는 유효 단일입자 전자 수송을 다룬다. 기본 Green's function, 전극 self-energy와 전류 식은 [NEGF formalism](negf-formalism.md)을 따른다. Phonon용 self-consistent reservoir, microscopic electron–phonon self-energy와 특정 소프트웨어 입력 형식은 범위에서 제외한다.

## 1. 가상 단자와 영전류 조건

### (1) 흡수와 재주입

왼쪽·오른쪽 물리 전극에 probe 집합 $\mathcal P$를 추가하자. 모든 단자를 포함한 retarded Green's function은

$$
G^R(E)=
\left[
(E+i0^+)I-H_D-\Sigma_L^R-\Sigma_R^R
-\sum_{p\in\mathcal P}\Sigma_p^R
\right]^{-1}
$$

이다. Probe $p$의 broadening은

$$
\Gamma_p(E)=i\left[\Sigma_p^R(E)-\Sigma_p^A(E)\right]
$$

로 정의한다. $\operatorname{Im}\Sigma_p^R$만 추가하면 전자가 소자에서 사라지는 흡수 경로만 생긴다. Büttiker probe에서는 lesser self-energy

$$
\Sigma_p^<(E)=if_p(E)\Gamma_p(E)
$$

를 함께 두고 $f_p$를 영전류 조건으로 결정한다. 이 재주입 조건이 전하 보존을 회복하며, 들어간 전자와 나온 전자 사이의 위상 관계는 보존하지 않는다.[2–6]

### (2) 다단자 전류

$T_{q\leftarrow p}$를 단자 $p$에서 $q$로 전달될 확률로 정의하면 Caroli 식은

$$
T_{q\leftarrow p}(E)
=\operatorname{Tr}\!\left[
\Gamma_qG^R\Gamma_pG^A
\right]
$$

이다. Spin degeneracy를 $g_s$로 쓰면 단자 $p$에서 소자로 나가는 에너지별 전류는

$$
i_p(E)=\frac{g_se}{h}
\sum_{q\ne p}
\left[
T_{q\leftarrow p}(E)f_p(E)
-T_{p\leftarrow q}(E)f_q(E)
\right]
$$

이고, 전체 전류는

$$
I_p=\int_{-\infty}^{\infty}i_p(E)\,dE
$$

이다. 자기장이 없고 time-reversal symmetry가 성립하면 $T_{q\leftarrow p}=T_{p\leftarrow q}$이므로 익숙한 $T_{pq}(f_p-f_q)$ 형태로 줄어든다. 자기장이나 비가역적 유효 모형에서는 방향이 있는 두 transmission을 임의로 같게 두면 안 된다.[1,4–7]

## 2. Probe 모형의 구분

영전류를 어느 수준에서 부과하는지가 probe의 물리적 의미를 결정한다.[4–6]

| 모형 | Probe 분포 | 보존 조건 | 모사하는 효과 |
|---|---|---|---|
| Dephasing probe | 에너지별 비평형 $f_p(E)$ | 모든 에너지에서 $i_p(E)=0$ | 에너지 보존 dephasing |
| Voltage probe | $f_{\mathrm{FD}}(E;\mu_p,T_p)$ | 적분 전하 전류 $I_p=0$ | 위상 소실과 에너지 완화 |
| Voltage–temperature probe | $f_{\mathrm{FD}}(E;\mu_p,T_p)$ | $I_p=0$, $J_p=0$ | 전하·열의 순유출이 없는 국소 평형 |

### (1) Dephasing probe

Dephasing probe는

$$
i_p(E)=0
\qquad \text{for every }E
$$

를 부과한다. Reciprocal transmission을 가정하고 probe가 하나뿐이면

$$
f_p(E)=
\frac{\sum_{a\in\{L,R\}}T_{pa}(E)f_a(E)}
{\sum_{a\in\{L,R\}}T_{pa}(E)}
$$

이다. 여러 probe에서는 각 $f_p(E)$가 다른 probe 분포에도 의존하므로, 에너지마다

$$
A_{pp}(E)=\sum_{q\ne p}T_{pq}(E),
\qquad
A_{pq}(E)=-T_{pq}(E)
$$

와

$$
b_p(E)=\sum_{a\in\{L,R\}}T_{pa}(E)f_a(E)
$$

를 구성해

$$
A(E)\mathbf f_{\mathcal P}(E)=\mathbf b(E)
$$

를 푼다. 결과 $f_p(E)$는 일반적으로 Fermi–Dirac distribution이 아니다. 따라서 이 모형은 에너지마다 입자 수를 보존하지만 probe 내부의 열평형을 가정하지 않는다.[4–6]

### (2) Voltage probe

Voltage probe에서는 온도 $T_p$를 지정하고

$$
f_p(E)=
\left[1+\exp\left(\frac{E-\mu_p}{k_BT_p}\right)\right]^{-1}
$$

로 둔다. 미지의 chemical potential $\mu_p$는

$$
I_p(\mu_1,\ldots,\mu_{N_p})=0
$$

을 모든 probe에서 동시에 만족하도록 정한다. 조건이 에너지 적분 뒤에 적용되므로 한 에너지에서 들어온 전자가 다른 에너지에서 나올 수 있다. Probe의 열전류를

$$
J_p=\frac{g_s}{h}\int dE\,(E-\mu_p)
\sum_{q\ne p}
\left[T_{q\leftarrow p}f_p-T_{p\leftarrow q}f_q\right]
$$

로 정의하면 voltage probe에서는 일반적으로 $J_p\ne0$이다. 따라서 이는 dissipative inelastic scattering의 현상론적 모형이다.[4–6]

Voltage–temperature probe는 $\mu_p$와 $T_p$를 모두 미지수로 두고

$$
I_p=0,
\qquad
J_p=0
$$

을 함께 푼다. 이는 일반 voltage probe와 다른 경계조건이며, 세 모형의 결과를 같은 `dephasing strength`만으로 직접 비교해서는 안 된다.[4–6]

!!! warning "[Interpretation Caveat]"
    Dephasing probe와 voltage probe는 낮은 온도·작은 bias의 선형 응답에서는 유사한 conductance를 줄 수 있지만, 유한 bias에서는 에너지 보존 조건이 달라 서로 다른 전류–전압 특성을 낼 수 있다. 두 모형의 저전압 일치를 일반적인 등가성으로 해석하면 안 된다.[5,6]

## 3. 선형 응답과 probe 제거

### (1) Conductance 행렬

공통 평형 분포 $f_0$ 근처의 선형 응답에서 reciprocal transmission을 가정하면 단자 사이 계수는

$$
\mathcal G_{ab}
=\frac{g_se^2}{h}\int dE
\left(-\frac{\partial f_0}{\partial E}\right)T_{ab}(E)
$$

이다. 전류식을

$$
I_a=\sum_bK_{ab}V_b
$$

로 쓰기 위해

$$
K_{aa}=\sum_{b\ne a}\mathcal G_{ab},
\qquad
K_{ab}=-\mathcal G_{ab}\quad(a\ne b)
$$

를 정의한다. $K$의 각 행 합은 0이므로 모든 전압에 같은 상수를 더해도 전류는 변하지 않는다.[1,3,4]

### (2) Schur complement

물리 단자를 $P$, probe를 $\phi$로 묶으면

$$
\begin{pmatrix}
\mathbf I_P\\
\mathbf 0
\end{pmatrix}
=
\begin{pmatrix}
K_{PP}&K_{P\phi}\\
K_{\phi P}&K_{\phi\phi}
\end{pmatrix}
\begin{pmatrix}
\mathbf V_P\\
\mathbf V_\phi
\end{pmatrix}
$$

이다. 기준 전압을 하나 고정한 뒤 $K_{\phi\phi}$가 가역이면

$$
\mathbf V_\phi
=-K_{\phi\phi}^{-1}K_{\phi P}\mathbf V_P
$$

이고, 물리 단자만의 유효 conductance 행렬은

$$
K_{\mathrm{eff}}
=K_{PP}-K_{P\phi}K_{\phi\phi}^{-1}K_{\phi P}
$$

이다. 둘째 항은 probe로 들어갔다가 비결맞게 재주입되는 경로를 포함한다. 단순한 imaginary potential 계산에는 이 항이 없으므로 두 계산은 전하 보존 측면에서 같지 않다.[2–4]

## 4. 결합 모형과 계산 절차

### (1) Wide-band probe

국소 궤도 $|n\rangle$에 wide-band probe를 붙이는 최소 모형은

$$
\Sigma_p^R=-\frac{i}{2}\gamma_p|n\rangle\langle n|,
\qquad
\Gamma_p=\gamma_p|n\rangle\langle n|
$$

이다. 이때 $\gamma_p$는 probe 결합에 의한 에너지 폭이다. 단순한 단일 준위 수명 해석에서는

$$
\tau_p\sim\frac{\hbar}{\gamma_p}
$$

로 대응시킬 수 있지만, 실제 phase-relaxation length나 microscopic electron–phonon 결합과의 관계는 probe 배치, mode velocity와 momentum randomization 방식에 의존한다.[3,6,7]

모든 원자 궤도에 독립적인 국소 probe를 붙이면 위상뿐 아니라 운동량도 완화할 수 있다. 순수한 forward dephasing이나 momentum-conserving scattering이 필요하면 probe가 결합하는 mode와 self-energy 구조를 별도로 설계해야 한다.[4,7]

### (2) 수치 순서

실제 계산은 다음 순서로 수행한다.[3,5–7]

1. 물리 전극과 probe의 $\Sigma^R$, $\Gamma$를 정의하고 probe 위치·결합 행렬을 기록한다.
2. 각 에너지에서 $G^R$와 모든 필요한 $T_{q\leftarrow p}$를 계산한다.
3. Dephasing probe이면 에너지별 선형계를 풀고, voltage probe이면 모든 $I_p=0$을 만족하는 $\mu_p$를 비선형 반복으로 구한다.
4. 결정된 $\Sigma_p^<$를 넣어 $G^<$, density matrix와 물리 단자 전류를 계산한다.
5. 전하가 Hamiltonian을 바꾸는 Poisson–NEGF 문제에서는 probe 해를 각 전하 반복 안에서 다시 수렴시킨다.

Voltage probe의 비선형 반복에서는 정규화한 최대 잔차

$$
r_{\mathrm{probe}}
=\frac{\max_{p\in\mathcal P}|I_p|}
{\max(I_{\mathrm{scale}},|I_L|,|I_R|)}
$$

를 사용한다. $I_{\mathrm{scale}}$은 평형 근처에서 분모가 0이 되는 것을 막기 위해 미리 선언한 기준 전류이다. Dephasing probe에서는 적분 잔차만 보지 말고

$$
r_E=
\max_{p,E}
\frac{|i_p(E)|}{\max(i_{\mathrm{scale}}(E),|i_L(E)|,|i_R(E)|)}
$$

도 확인해야 한다.

## 5. 검증과 적용 한계

### (1) 보존 법칙과 수렴

다음 검사는 probe 계산의 최소 검증 세트이다.[3–7]

| 검사 | 계산량 | 실패가 뜻하는 것 |
|---|---|---|
| 평형 | $\mu_L=\mu_R$에서 모든 $I_a$ | 분포·부호 또는 에너지 적분 오류 |
| Probe 영전류 | $r_{\mathrm{probe}}$, dephasing의 $r_E$ | self-consistency 미수렴 |
| 전체 전하 보존 | $\sum_a I_a$ | terminal 누락 또는 transmission 방향 오류 |
| Coherent limit | $\gamma_p\rightarrow0$ | probe 제거 또는 기준 계산 불일치 |
| 에너지 격자 | 격자 세분화 전후의 전류 | 좁은 공명과 Fermi window 해상도 부족 |
| 대칭성 | 적용 가능한 경우 Onsager–Casimir 관계 | 자기장·terminal convention 처리 오류 |

전체 전하 보존 잔차는

$$
r_Q=
\frac{\left|\sum_{a\in\{L,R,\mathcal P\}}I_a\right|}
{\max(I_{\mathrm{scale}},\sum_a|I_a|)}
$$

로 기록할 수 있다. 에너지 격자 $\mathcal E$와 세분화한 격자 $\mathcal E'$의 전류 차이는

$$
\delta_I=
\frac{|I_L(\mathcal E')-I_L(\mathcal E)|}
{\max(I_{\mathrm{scale}},|I_L(\mathcal E')|)}
$$

로 검사한다. 허용 오차는 선형계 조건수, energy integration과 목표 관측량의 정확도에 맞춰 정하며 보편적인 숫자로 고정하지 않는다.

!!! info "[Measurement]"
    각 bias와 probe coupling에서 $I_L$, $I_R$, 모든 $I_p$, $r_Q$, $r_{\mathrm{probe}}$와 $\delta_I$를 함께 저장한다. Dephasing probe는 $r_E$도 저장한다. Voltage probe에서는 $J_p$를 추가로 보고해야 전하 보존과 에너지 소산을 구분할 수 있다.

### (2) 현상론적 모형의 한계

Büttiker probe는 계산 비용이 낮고 coherent limit에서 비결맞음 수송으로 연속적으로 연결할 수 있지만, $\gamma_p$ 자체가 특정 phonon mode, 온도 의존 scattering rate 또는 microscopic collision integral을 자동으로 제공하지는 않는다. 정량 예측이 목적이면 독립적인 산란 시간·mean free path·mobility 또는 microscopic self-energy와 맞춰 보정해야 한다.[3,6,7]

Probe가 간섭을 약화하므로 destructive interference가 지배하는 구조에서는 전류가 증가할 수 있지만, backscattering이나 공명 폭 증가가 지배하면 전류가 감소할 수 있다. 따라서 `dephasing은 항상 저항을 증가시킨다` 또는 `probe coupling이 클수록 conductance가 단조 감소한다`는 보편 법칙은 성립하지 않는다.[5–7]

## 6. 요약

- Büttiker probe는 fictitious reservoir의 흡수 self-energy와 영전류 재주입 조건을 결합한 현상론적 수송 모형이다.
- Dephasing probe는 에너지마다 $i_p(E)=0$을, voltage probe는 에너지 적분 뒤 $I_p=0$을 부과하므로 에너지 보존 성질이 다르다.
- NEGF에서는 probe의 $\Sigma_p^R$, $\Gamma_p$, $\Sigma_p^<$와 모든 terminal 사이 transmission을 함께 계산해야 한다.
- 선형 응답에서는 probe 전압을 conductance 행렬의 Schur complement로 제거할 수 있고, 유한 bias voltage probe는 결합된 비선형 영전류 조건을 풀어야 한다.
- Probe current, 전체 전하 보존, coherent limit와 에너지 격자 수렴을 확인한 뒤에만 $\gamma_p$ 의존성을 해석해야 한다.
- 이 방법은 microscopic scattering theory가 아니므로 probe coupling은 독립적인 물리량에 맞춰 보정해야 한다.

## 7. 참고문헌

1. M. Büttiker, "Four-Terminal Phase-Coherent Conductance," *Physical Review Letters* **57**, 1761–1764 (1986). [https://doi.org/10.1103/PhysRevLett.57.1761](https://doi.org/10.1103/PhysRevLett.57.1761)
2. M. Büttiker, "Coherent and sequential tunneling in series barriers," *IBM Journal of Research and Development* **32**, 63–75 (1988). [https://doi.org/10.1147/rd.321.0063](https://doi.org/10.1147/rd.321.0063)
3. J. L. D'Amato and H. M. Pastawski, "Conductance of a disordered linear chain including inelastic scattering events," *Physical Review B* **41**, 7411–7420 (1990). [https://doi.org/10.1103/PhysRevB.41.7411](https://doi.org/10.1103/PhysRevB.41.7411)
4. M. Büttiker, "Reversing the sign of current-current correlations," arXiv:cond-mat/0209031 (2002). [https://arxiv.org/abs/cond-mat/0209031](https://arxiv.org/abs/cond-mat/0209031)
5. M. Kilgour and D. Segal, "Charge transport in molecular junctions: From tunneling to hopping with the probe technique," *The Journal of Chemical Physics* **143**, 024111 (2015). [https://doi.org/10.1063/1.4926395](https://doi.org/10.1063/1.4926395)
6. H. Förster, P. Samuelsson, S. Pilgram, and M. Büttiker, "Voltage and dephasing probes in mesoscopic conductors: A study of full-counting statistics," *Physical Review B* **75**, 035340 (2007). [https://doi.org/10.1103/PhysRevB.75.035340](https://doi.org/10.1103/PhysRevB.75.035340)
7. J. Maassen, F. Zahid, and H. Guo, "Effects of dephasing in molecular transport junctions using atomistic first principles," *Physical Review B* **80**, 125423 (2009). [https://doi.org/10.1103/PhysRevB.80.125423](https://doi.org/10.1103/PhysRevB.80.125423)
