---
description: Classical MD와 ab initio MD의 원리, statistical ensemble, 시간 간격·총 계산 시간 및 평형 판정 기준을 설명한 입문 문서
---

# Molecular dynamics: Overview

Molecular dynamics simulation (MD)은 상호작용하는 원자 또는 입자의 운동 방정식을 시간에 따라 적분하여 위상공간 궤적을 만드는 계산 방법이다. 궤적 자체는 한 초기조건의 결정론적 또는 확률론적 시간 발달이지만, 충분히 표본화된 궤적에서 얻은 시간 평균은 선택한 statistical ensemble의 평형 평균을 추정하는 데 쓰인다.[1,2] 따라서 좋은 MD 계산에는 세 조건이 동시에 필요하다. 힘을 주는 모형이 연구 질문에 적합해야 하고, 수치 적분이 안정적이어야 하며, 궤적이 관심 관측량에 필요한 상태를 충분히 방문해야 한다.[1,3]

이 문서는 classical MD와 ground-state ab initio molecular dynamics (AIMD)를 다룬다. Classical MD에서는 미리 정한 force field 또는 interatomic potential로 힘을 계산하며, AIMD에서는 전자구조 계산으로 힘을 매 시간 단계에서 구한다. 핵의 양자성, 비단열 전자 동역학, enhanced sampling, 반응 경로 탐색과 machine-learning interatomic potential (MLIP)은 범위에서 제외한다.

## 1. 궤적과 평형 평균

### (1) 위상공간의 시간 발달

$N$개 고전 입자의 위치와 운동량을 각각 $\mathbf r=\{\mathbf r_i\}$, $\mathbf p=\{\mathbf p_i\}$라 두면, 시간에 무관한 기본 Hamiltonian은 다음과 같다.

$$
H(\mathbf r,\mathbf p)
=K(\mathbf p)+U(\mathbf r)
=\sum_{i=1}^{N}\frac{\mathbf p_i^2}{2m_i}+U(\mathbf r).
$$

$m_i$는 입자 $i$의 질량, $K$는 운동에너지, $U$는 위치에 따른 potential energy이다. Hamilton 방정식은 Newton 방정식과 동등하다.

$$
\dot{\mathbf r}_i=\frac{\mathbf p_i}{m_i},
\qquad
\dot{\mathbf p}_i=\mathbf F_i=-\nabla_i U(\mathbf r).
$$

즉 MD의 핵심 입력은 현재 구조에서의 힘 $\mathbf F_i$이다. Classical MD와 AIMD의 가장 중요한 차이는 원자핵을 이동시키는 식이 아니라 $U$와 $\mathbf F_i$를 얻는 방법에 있다.[1,4]

연속 운동 방정식은 컴퓨터에서 유한한 시간 간격 $\Delta t$로 이산화된다. 널리 쓰이는 velocity Verlet 적분은 다음 순서로 속도 반 단계, 위치 한 단계, 속도 반 단계를 갱신한다.[3,5]

$$
\begin{aligned}
\mathbf v_i\left(t+\frac{\Delta t}{2}\right)
&=\mathbf v_i(t)+\frac{\Delta t}{2m_i}\mathbf F_i(t),\\
\mathbf r_i(t+\Delta t)
&=\mathbf r_i(t)+\Delta t\,\mathbf v_i\left(t+\frac{\Delta t}{2}\right),\\
\mathbf v_i(t+\Delta t)
&=\mathbf v_i\left(t+\frac{\Delta t}{2}\right)
+\frac{\Delta t}{2m_i}\mathbf F_i(t+\Delta t).
\end{aligned}
$$

이 적분기는 시간 가역적인 2차 symplectic 방법이다. 유한한 $\Delta t$에서는 정확한 $H$가 아니라 가까운 shadow Hamiltonian을 따른다는 점이 중요하다. 따라서 순간 총에너지가 완전히 일정할 필요는 없지만, 안정적인 NVE 계산에서 에너지 오차는 제한된 범위에서 진동해야 하며 $\Delta t$를 줄일 때 체계적으로 감소해야 한다.[3,6]

### (2) 시간 평균과 ergodicity

관측량 $A(\mathbf r,\mathbf p)$의 궤적 평균은 평형화 이후의 $M$개 frame에 대해 다음처럼 계산한다.

$$
\overline A=\frac{1}{M}\sum_{n=1}^{M}A_n.
$$

이 값이 ensemble 평균 $\langle A\rangle$에 접근하려면 궤적이 관련 위상공간을 충분히 방문해야 한다. 에너지 장벽 때문에 한 metastable basin에 갇히면 에너지나 온도가 평탄해 보여도 구조 분포는 수렴하지 않을 수 있다. 단일 관측량의 평탄화는 필요한 조건일 수 있으나 평형을 증명하는 충분조건은 아니다.[2,7]

## 2. Classical molecular dynamics

### (1) Force field와 상호작용 모형

Classical MD는 $U(\mathbf r)$를 분석적인 함수로 정한다. 분자용 fixed-topology force field는 일반적으로 결합 길이, 결합각, dihedral과 같은 bonded term에 electrostatic 및 van der Waals nonbonded term을 더한다. 재료 모형에서는 pair, many-body 또는 반응성 interatomic potential을 사용할 수 있다. 어떤 형식을 쓰든 parameterization에 포함된 화학 조성, 상, 온도·압력과 구조 환경이 모형의 유효 범위를 정한다.[1,8]

미리 정한 potential을 평가하므로 classical MD는 전자구조를 매 단계 푸는 AIMD보다 큰 원자 수와 긴 시간을 다루기 쉽다. 반면 일반적인 fixed-topology force field는 결합의 생성·절단, 전하 이동과 전자 여기 상태를 스스로 기술하지 못한다. 반응성 empirical potential은 결합 변화 일부를 다룰 수 있지만, 별도의 함수형과 parameter 검증이 필요한 classical model이지 AIMD와 동등하지 않다.[1,4]

주기적 경계조건은 bulk 환경을 근사하지만 무한계 그 자체는 아니다. 계산 cell, cutoff, 장거리 electrostatics와 분산력 보정은 potential 정의의 일부로 취급해야 한다. 원자 수를 늘리거나 cutoff만 바꾸었을 때 관심 관측량이 변하지 않는지 확인하지 않으면 finite-size artifact와 상호작용 절단 오차를 물리적 결과로 오인할 수 있다.[1,3]

### (2) 강점과 한계

Classical MD는 같은 모형에서 많은 독립 궤적을 만들고 느린 완화 현상을 표본화하는 데 유리하다. 그러나 긴 궤적은 정확한 궤적을 뜻하지 않는다. Force field의 systematic error, 부적절한 경계조건, 잘못된 thermostat 또는 큰 $\Delta t$는 계산 시간을 늘려도 사라지지 않는다.[3,8]

또한 고전 핵 근사는 zero-point motion과 tunneling을 포함하지 않는다. 가벼운 원소의 높은 진동수, 낮은 온도 또는 proton transfer처럼 핵 양자 효과가 핵심인 문제에서는 classical MD와 통상적인 AIMD 모두 적용 범위를 벗어날 수 있다.[4,9]

## 3. Ab initio molecular dynamics

### (1) Born–Oppenheimer molecular dynamics

Born–Oppenheimer molecular dynamics (BOMD)는 각 핵 배치 $\mathbf R$에서 전자구조 문제를 풀어 ground-state energy $E_0(\mathbf R)$를 구하고, 그 기울기로 핵에 작용하는 힘을 계산한다.

$$
M_I\ddot{\mathbf R}_I
=-\nabla_I E_0(\mathbf R).
$$

$M_I$와 $\mathbf R_I$는 핵 $I$의 질량과 위치이다. 실무에서는 density functional theory (DFT)가 흔하지만, BOMD는 특정 전자구조 방법 하나와 동의어가 아니다. 각 단계의 self-consistent field (SCF) 수렴 오차가 힘에 남으면 NVE 에너지 drift를 만들 수 있으므로 energy cutoff, basis, $k$-point, smearing과 SCF tolerance를 정적 에너지뿐 아니라 force 및 에너지 보존 관점에서도 수렴시켜야 한다.[4,10]

BOMD는 결합 변화, 배위 변화와 전하 재배치를 미리 고정한 결합 topology 없이 기술할 수 있다. 그러나 결과는 선택한 exchange-correlation functional, pseudopotential 또는 basis, 분산력 처리와 Born–Oppenheimer approximation에 의존한다. 작은 cell과 짧은 궤적으로 인한 표본화 오차가 전자구조 모형 오차와 별도로 존재한다.[4,9]

### (2) Car–Parrinello molecular dynamics

Car–Parrinello molecular dynamics (CPMD)는 매 단계에서 전자 상태를 완전히 최소화하는 대신 Kohn–Sham orbital에 fictitious mass를 부여하여 핵과 함께 전파하는 extended-Lagrangian 방법이다.[9,11] 전자 자유도가 ground-state surface 가까이에 머물려면 fictitious electronic motion과 ionic motion의 단열 분리가 유지되어야 한다. 이 조건은 CPMD의 $\Delta t$와 fictitious mass를 BOMD와 독립적으로 검증해야 함을 뜻한다.[4,9]

두 AIMD 방식의 차이를 요약하면 다음과 같다.

| 구분 | Classical MD | BOMD | CPMD |
| --- | --- | --- | --- |
| 힘의 근원 | 미리 parameterize한 force field 또는 interatomic potential | 현재 핵 배치의 수렴된 전자 ground state | 핵과 함께 전파하는 fictitious electronic 변수 |
| 결합 변화 | fixed-topology 모형은 일반적으로 불가 | 전자구조 방법의 범위 안에서 가능 | 전자구조 방법과 단열 분리 조건 안에서 가능 |
| 단계당 비용 | 상대적으로 낮음 | 전자구조 반복 수렴 때문에 높음 | 전자 자유도 전파 비용과 작은 시간 간격 필요 |
| 핵심 수치 검사 | 시간 간격, cutoff, constraint와 에너지 보존 | 여기에 SCF·basis·$k$-point·functional 수렴 추가 | 여기에 fictitious mass와 전자-핵 단열 분리 추가 |
| 공통 한계 | 고전 핵, 유한 cell, 유한 시간과 표본화 오차 | 고전 핵, 전자구조 근사, 유한 cell과 표본화 오차 | 고전 핵, 전자구조 근사, fictitious dynamics와 표본화 오차 |

## 4. Statistical ensemble

### (1) Ensemble의 의미

Statistical ensemble은 같은 macroscopic constraint를 만족하는 microstate의 확률분포이다. MD에서 `NVT를 돌린다`는 말은 $T$를 매 순간 정확히 고정한다는 뜻이 아니라, canonical distribution을 생성하도록 열 저장고와 결합한 운동 방정식 또는 확률 과정을 사용한다는 뜻이다. 순간 kinetic temperature와 pressure는 유한계에서 변동하며, 올바른 평균뿐 아니라 올바른 분포 폭을 가져야 한다.[3,12]

$\beta=(k_\mathrm{B}T)^{-1}$라 두면 NVT의 위상공간 확률밀도는 다음에 비례한다.

$$
\rho_{NVT}(\mathbf r,\mathbf p)\propto
\exp[-\beta H(\mathbf r,\mathbf p)].
$$

자유도 수를 $f$라 하면 흔히 출력되는 순간 kinetic temperature는 다음 정의를 사용한다.

$$
T_{\mathrm{inst}}(t)=\frac{2K(t)}{f k_\mathrm B}.
$$

$f$에는 고정한 결합과 제거한 center-of-mass 운동을 반영해야 한다. $T_{\mathrm{inst}}$는 한 frame의 kinetic energy를 온도로 환산한 값이며, 열역학적 $T$는 이 값이 표본화해야 하는 분포를 정하는 parameter이다.[3,12]

반면 이상적인 NVE 궤적은 $N$, $V$, $E$가 일정한 energy shell을 표본화한다. NPT에서는 volume도 확률변수이며 $T$와 외부 압력 $P$가 분포를 정한다. 어떤 ensemble이 더 고급인 것이 아니라, 계산하려는 물리량과 실험 조건에 맞는 constraint를 선택해야 한다.[1,12]

### (2) 주요 ensemble 비교

| Ensemble | 고정 또는 제어하는 양 | 실제로 변동하는 주요 양 | 필요한 결합 | 대표 용도 | 해석상의 주의점 |
| --- | --- | --- | --- | --- | --- |
| NVE, microcanonical | $N,V,E$ | $T,P$ | 없음 | 보존 동역학, 시간 간격·force 품질 검사, thermostat가 없는 동역학량 | 수치 오차가 있으면 $E$가 drift하며, 초기 에너지가 목표 상태를 결정함 |
| NVT, canonical | $N,V,T$ | $E,P$, 순간 $T$ | thermostat | 고정 부피에서의 평형 구조와 열역학 평균 | 평균 온도만 맞는다고 canonical distribution이 보장되지는 않음 |
| NPT, isothermal–isobaric | $N,P,T$ | $E,V$, 순간 $P,T$ | thermostat와 barostat | 목표 온도·압력에서 평형 밀도, 상 안정성과 구조 | cell 자유도와 barostat가 물리계에 맞아야 하며 작은 계의 부피 변동이 큼 |
| NPH, isoenthalpic–isobaric | $N,P,H$ | $V,T$ | barostat, thermostat 없음 | 일정 외부 압력에서 열 교환 없는 과정의 모델 | 온도는 제어값이 아니며 enthalpy 보존과 cell dynamics를 함께 검사함 |
| $\mu VT$, grand canonical | $\mu,V,T$ | $N,E$ | 열·입자 저장고와 삽입/삭제 규칙 | 흡착, 열린 계와 조성 평형 | 보통의 fixed-$N$ MD만으로 구현되지 않으며 Monte Carlo 혼합 등이 필요함 |

여기서 $H$는 NVE 행에서는 Hamiltonian, NPH 행에서는 thermodynamic enthalpy를 뜻하는 관례적 중복 기호이다. 혼동을 피하려면 실제 보고서에서 enthalpy를 $\mathcal H=E+PV$처럼 별도 표기해도 된다.

### (3) Thermostat와 barostat

Thermostat와 barostat는 단순한 숫자 보정기가 아니라 목표 확률분포를 만드는 sampling algorithm의 일부이다. Andersen과 Langevin thermostat는 확률적 충돌 또는 마찰·잡음을 도입하고, Nosé–Hoover 계열은 extended variable을 이용한다. 방법과 coupling time은 온도 완화 속도, ergodicity 및 실제 시간상관함수에 서로 다른 영향을 준다.[12,13]

Berendsen weak coupling은 목표 평균으로 빠르게 완화시키지만 kinetic energy와 volume fluctuation을 억제하므로 정확한 canonical 또는 isothermal–isobaric ensemble을 생성하지 않는다. 초기 안정화에 제한적으로 사용할 수는 있으나 fluctuation, heat capacity, compressibility 또는 엄밀한 production 평균을 구할 때에는 올바른 분포를 표본화하는 방법으로 전환해야 한다.[3,13]

!!! warning "[Interpretation Caveat]"
    Thermostat를 사용한 궤적에서 평균 온도가 목표값과 일치한다는 사실만으로 올바른 NVT sampling이나 물리적인 kinetics가 보장되지는 않는다. 관심 대상이 diffusion coefficient, vibrational spectrum 또는 반응 속도라면 thermostat 종류와 coupling strength를 바꾸었을 때 결과가 유지되는지 확인하거나, 평형화 뒤 적절한 NVE 구간에서 동역학량을 계산해야 한다.[1,3]

## 5. 계산 시간의 설계

### (1) 시간 간격

시간 간격 $\Delta t$는 가장 빠르게 진동하는 자유도를 충분히 분해해야 한다. 2차 Verlet 계열의 시작점으로 가장 짧은 진동 주기 $\tau_{\min}$의 약 1/10 이하를 사용할 수 있지만, 이는 안정성 보증이 아니라 시험값이다.[1,6]

$$
\Delta t_{\mathrm{start}}\lesssim\frac{\tau_{\min}}{10}.
$$

| 계산 조건 | 보수적인 시작 범위 | 범위가 달라지는 이유 | 반드시 할 검증 |
| --- | ---: | --- | --- |
| 수소를 포함하고 고주파 결합을 제약하지 않은 classical all-atom MD | $0.5$–$1.0\ \mathrm{fs}$ | X–H stretching이 가장 빠른 운동인 경우가 많음 | NVE energy drift와 $\Delta t/2$ 결과 비교 |
| X–H 결합 등 고주파 자유도에 정확한 constraint를 둔 classical MD | 흔히 $2\ \mathrm{fs}$부터 시험 | 제거된 진동이 시간 간격의 상한을 더 이상 정하지 않음 | constraint 오차, 에너지와 관심 관측량의 시간 간격 의존성 |
| 수소를 포함한 BOMD | 흔히 $0.5$–$1.0\ \mathrm{fs}$부터 시험 | 핵 진동과 함께 매 단계 force의 전자 수렴 오차가 존재함 | NVE drift, SCF 수렴, force 및 관측량의 $\Delta t/2$ 비교 |
| 무거운 원소 중심의 완만한 진동 | 더 큰 값이 가능하나 고정값 없음 | 최고 진동수가 낮을 수 있음 | phonon 또는 velocity spectrum과 NVE 비교로 결정 |
| CPMD | BOMD보다 작은 값이 필요할 수 있음 | fictitious electronic frequency도 분해해야 함 | ionic energy, fictitious kinetic energy와 단열 분리 검사 |

표의 수치는 출발점일 뿐이다. 질량을 인위적으로 늘리면 더 큰 $\Delta t$가 가능하지만 실제 질량에 의존하는 diffusion과 vibrational dynamics가 바뀐다. 마찬가지로 thermostat가 에너지 증가를 숨길 수 있으므로 시간 간격 검증은 짧은 NVE 구간에서 수행한다.[1,14]

!!! info "[Measurement]"
    같은 초기구조와 force 설정으로 $\Delta t$, $\Delta t/2$, 필요하면 $\Delta t/4$의 짧은 NVE 궤적을 만든다. 각 궤적에서 총에너지 $E(t)$를 선형 적합하여 drift $b_E=dE/dt$를 구하고, 원자 수 또는 자유도당 값으로 함께 보고한다. 2차 symplectic 적분기에서는 시간 간격을 줄일 때 에너지 fluctuation이 대체로 $\mathcal O(\Delta t^2)$로 감소해야 한다. Drift만 작고 fluctuation 수렴이 없으면 cutoff 불연속, 부정확한 constraint, 낮은 수치 정밀도 또는 AIMD의 불충분한 SCF 수렴도 조사한다.[3,6]

### (2) 총 계산 시간

총 시간은 $t_{\mathrm{run}}=N_{\mathrm{step}}\Delta t$이지만, step 수 자체는 표본화 품질을 나타내지 않는다. 서로 인접한 frame은 강하게 상관되어 있으므로 production 길이는 가장 느린 관심 관측량의 상관시간과 요구 uncertainty로 정해야 한다.[2,7]

저장 간격을 $\delta t_s$라 하고 관측량 $A$의 정규화 autocorrelation을 $\rho_A(k)$라 하면 statistical inefficiency $g_A$와 유효 표본 수 $N_{\mathrm{eff},A}$를 다음처럼 정의할 수 있다.

$$
g_A=1+2\sum_{k=1}^{\infty}\rho_A(k),
\qquad
N_{\mathrm{eff},A}\approx\frac{M}{g_A}.
$$

Integrated autocorrelation time을 $\tau_{\mathrm{int},A}=g_A\delta t_s/2$로 정의하면 $M$개 frame의 production 시간은 대략 $t_{\mathrm{prod}}=M\delta t_s$이다. 목표 유효 표본 수 $N_{\mathrm{eff}}^*$를 먼저 정하면 필요한 시간의 1차 추정은 다음과 같다.

$$
t_{\mathrm{prod}}\gtrsim
N_{\mathrm{eff}}^*g_A\delta t_s
=2N_{\mathrm{eff}}^*\tau_{\mathrm{int},A}.
$$

예를 들어 $10\ \mathrm{fs}$마다 저장한 자료에서 $g_A=200$이면 독립 표본 하나에 해당하는 간격은 약 $2\ \mathrm{ps}$이다. 이 관측량에 대해 100개의 유효 표본을 목표로 하면 production 시간의 시작 추정은 약 $200\ \mathrm{ps}$이다. 이는 예시 계산이지 모든 계에 적용되는 권장 시간이 아니다. 구조 전이처럼 더 느린 관측량이 있다면 그 상관시간이 전체 시간을 정한다.

관측량이 Gaussian에 가깝고 $N_{\mathrm{eff}}$가 충분하면 평균의 표준오차는 대략 $s_A/\sqrt{N_{\mathrm{eff},A}}$로 감소한다. 따라서 `10 ps AIMD`와 `100 ns classical MD`라는 원시 시간만 비교하지 말고, 각 방법에서 얻은 독립 표본 수와 신뢰구간을 보고해야 한다.[2,7]

!!! warning "[Interpretation Caveat]"
    관측된 궤적만으로 매우 느린 미방문 상태의 존재를 배제할 수 없다. 상관시간 추정치는 궤적이 이미 방문한 상태 사이의 기억만 반영한다. 독립적인 초기구조에서 시작한 여러 궤적이 서로 다른 장기 평균을 보이면 단일 궤적의 작은 오차막대는 kinetic trapping을 숨긴 것이다.[7,15]

## 6. 평형화와 production

### (1) 초기조건과 단계적 평형화

초기 구조에는 원자 중첩, 비현실적인 결합 길이, 잘못된 조성·전하 또는 목표 상태와 맞지 않는 밀도가 없어야 한다. 먼저 energy minimization으로 큰 force를 제거하고, 목표 온도에 맞는 Maxwell–Boltzmann velocity를 배정한 뒤 center-of-mass translation을 제거한다. 이 과정은 평형 sampling을 대신하지 않으며 단지 수치적으로 안전한 시작점을 만든다.[1,8]

일반적인 순서는 `minimization → NVT thermalization → 필요하면 NPT density/cell equilibration → 목표 ensemble의 추가 평형화 → production`이다. 목표 production이 NVE라면 thermostat를 제거한 직후 바로 자료를 모으지 말고 짧은 NVE 구간에서 에너지와 평균 온도가 의도한 상태에 머무는지 확인한다. 고체의 variable-cell NPT에서는 cell shape 자유도가 대칭과 물리적 경계조건에 맞는지도 확인해야 한다.[1,14]

### (2) 평형 판정 기준

평형화 완료 시점은 하나의 고정 시간이나 온도 plateau로 정하지 않는다. 다음 세 층을 모두 통과해야 한다.[1,2]

1. **수치 안정성:** 원자 중첩, SCF 실패, constraint failure와 체계적인 에너지 폭주가 없다.
2. **열역학적 stationarity:** 목표 ensemble에 맞추어 energy, kinetic temperature, pressure, density 또는 cell parameter가 시간에 따른 체계적인 추세 없이 정상 변동 범위에 머문다.
3. **문제 고유의 느린 변수:** radial distribution function, coordination number, order parameter, defect population, molecular conformation 또는 확산 전 상태 분포처럼 결론에 직접 쓰는 관측량도 초기조건에서 멀어지는 추세를 멈춘다.

평형화 절단점 $t_0$를 정량화하는 한 방법은 $t_0$ 이후 자료에서 유효 비상관 표본 수를 최대화하는 것이다.[2,16]

$$
t_0^*=\underset{t_0}{\operatorname{arg\,max}}\;
N_{\mathrm{eff}}(t_0),
\qquad
N_{\mathrm{eff}}(t_0)=\frac{M(t_0)}{g(t_0)}.
$$

초기 transient를 더 버리면 bias는 줄지만 $M$도 감소한다. 위 기준은 이 bias–variance tradeoff를 관측량별로 다룬다. 다만 한 관측량에서 얻은 $t_0^*$가 모든 구조 변수의 평형을 보장하지 않으므로, energy·density와 연구 결론에 직접 연결된 느린 관측량에 각각 적용하고 가장 늦은 절단점을 채택한다.[2,16]

!!! info "[Measurement]"
    1. Energy, temperature, pressure 또는 volume과 최소 하나의 문제 고유 구조 변수를 같은 시간축에 그린다.
    2. 후보 $t_0$마다 이후 구간의 평균 추세와 $g_A(t_0)$를 계산하고 $N_{\mathrm{eff},A}(t_0)$를 구한다.
    3. 각 핵심 관측량의 $t_0^*$ 가운데 가장 늦은 값을 production 시작점으로 선택한다.
    4. Production의 첫 절반과 둘째 절반, 그리고 독립 초기조건의 궤적 사이에서 평균과 분포가 uncertainty 안에서 일치하는지 확인한다.
    5. 불일치하면 평형화 또는 production을 연장한다. 단순히 불리한 궤적을 제외하지 않는다.[2,7]

### (3) Production 종료 기준

Production은 사전에 정한 최소 길이를 채웠다는 이유만으로 종료하지 않는다. 핵심 관측량마다 $N_{\mathrm{eff}}$, block average 또는 bootstrap confidence interval을 갱신하고 목표 정밀도에 도달했는지 판단한다. 최소한 다음을 기록해야 한다.[2,7]

| 기록 항목 | 보고할 내용 | 실패 신호 |
| --- | --- | --- |
| 계산 길이 | $\Delta t$, 전체 step 수, 평형화와 production 시간 | 전체 시간만 있고 버린 구간이 불명확함 |
| 저장 규약 | energy와 좌표의 저장 간격 | 상관시간보다 지나치게 성긴 저장으로 빠른 관측량을 잃음 |
| 평형 절단 | 관측량별 $t_0$와 선택 기준 | 임의로 첫 10%를 버림 |
| 상관 분석 | $g$, $\tau_{\mathrm{int}}$ 또는 block 길이 | frame 수를 독립 표본 수로 사용함 |
| 불확도 | 평균, confidence interval과 계산 방법 | 평균 하나만 보고함 |
| 재현성 | 독립 seed·초기구조의 궤적 수와 일치 여부 | 한 궤적이 한 basin에 갇힘 |

## 7. 해석 한계와 점검표

MD 결과의 오류는 크게 model error, numerical error와 sampling error로 나뉜다. 서로 다른 오류는 같은 진단으로 해결되지 않는다. 더 작은 $\Delta t$는 부정확한 force field를 고치지 못하고, 더 긴 궤적은 잘못된 ensemble을 바로잡지 못하며, 엄격한 SCF 수렴은 작은 cell의 finite-size artifact를 제거하지 못한다.[3,8]

계산 전후에는 다음 질문을 순서대로 확인한다.

- 연구 질문이 평형 평균, 실제 시간동역학 또는 비평형 응답 가운데 무엇인지 정했는가?
- Classical MD의 potential 또는 AIMD의 전자구조 수준이 필요한 결합·전하·상과 상태점을 표현하는가?
- 선택한 ensemble이 실험 또는 이론의 constraint와 일치하는가?
- Thermostat와 barostat가 목표 분포를 생성하며 관심 동역학량을 과도하게 교란하지 않는가?
- $\Delta t/2$ 계산에서 에너지와 최종 관측량이 수렴하는가?
- Cell 크기, cutoff, $k$-point와 장거리 상호작용 처리에 결과가 수렴하는가?
- 온도뿐 아니라 가장 느린 문제 고유 관측량이 평형화되었는가?
- Raw frame 수가 아니라 유효 표본 수와 uncertainty를 보고했는가?
- 독립 초기조건의 결과가 일치하며, 일치하지 않을 때 kinetic trapping을 숨기지 않았는가?

## 8. 요약

- MD는 고전 핵의 운동 방정식을 적분하며, classical MD와 AIMD는 힘을 계산하는 방식에서 구분된다.
- NVE, NVT, NPT와 NPH는 서로 다른 constraint와 확률분포를 나타낸다. 목표 온도·압력은 순간값을 고정한다는 뜻이 아니다.
- 시간 간격은 가장 빠른 운동을 기준으로 보수적으로 시작하고, NVE 에너지와 관심 관측량의 $\Delta t/2$ 수렴으로 확정한다.
- 총 시간은 고정된 ps 또는 ns 규칙이 아니라 가장 느린 핵심 관측량의 상관시간, 목표 유효 표본 수와 uncertainty로 결정한다.
- 평형은 온도 plateau 하나로 판정하지 않는다. 열역학량, 구조 변수, 독립 궤적과 kinetic trapping 가능성을 함께 검사한다.
- MLIP, enhanced sampling, 핵 양자 동역학과 비단열 동역학은 이 문서의 범위 밖이다.

## 9. 참고문헌

1. E. Braun, J. Gilmer, H. B. Mayes, D. L. Mobley, J. I. Monroe, S. Prasad, and D. M. Zuckerman, “Best Practices for Foundations in Molecular Simulations [Article v1.0],” *Living Journal of Computational Molecular Science* **1**, 5957 (2019). [DOI](https://doi.org/10.33011/livecoms.1.1.5957)
2. A. Grossfield, P. N. Patrone, D. R. Roe, A. J. Schultz, D. W. Siderius, and D. M. Zuckerman, “Best Practices for Quantification of Uncertainty and Sampling Quality in Molecular Simulations [Article v1.0],” *Living Journal of Computational Molecular Science* **1**, 5067 (2018). [DOI](https://doi.org/10.33011/livecoms.1.1.5067)
3. P. T. Merz and M. R. Shirts, “Testing for physical validity in molecular simulations,” *PLOS ONE* **13**, e0202764 (2018). [DOI](https://doi.org/10.1371/journal.pone.0202764)
4. M. E. Tuckerman, “Ab initio molecular dynamics: Basic concepts, current trends and novel applications,” *Journal of Physics: Condensed Matter* **14**, R1297–R1355 (2002). [DOI](https://doi.org/10.1088/0953-8984/14/50/202)
5. L. Verlet, “Computer ‘Experiments’ on Classical Fluids. I. Thermodynamical Properties of Lennard-Jones Molecules,” *Physical Review* **159**, 98–103 (1967). [DOI](https://doi.org/10.1103/PhysRev.159.98)
6. GROMACS Development Team, “Molecular Dynamics,” *GROMACS 2026.3 Documentation*. [공식 문서](https://manual.gromacs.org/current/reference-manual/algorithms/molecular-dynamics.html)
7. K. Wiehe and S. C. Schmidler, “Monitoring Convergence of Molecular Simulations in the Presence of Kinetic Trapping” (2011). [Duke University manuscript](https://www2.stat.duke.edu/~scs/Papers/ConvergeDiagnos_JCTC.pdf)
8. W. F. van Gunsteren et al., “Validation of Molecular Simulation: An Overview of Issues,” *Angewandte Chemie International Edition* **57**, 884–902 (2018). [DOI](https://doi.org/10.1002/anie.201702945)
9. T. D. Kühne, “Second generation Car–Parrinello molecular dynamics,” *WIREs Computational Molecular Science* **4**, 391–406 (2014). [DOI](https://doi.org/10.1002/wcms.1176)
10. J. M. Herbert and M. Head-Gordon, “Accelerated, energy-conserving Born–Oppenheimer molecular dynamics via Fock matrix extrapolation,” *Physical Chemistry Chemical Physics* **7**, 3269–3275 (2005). [DOI](https://doi.org/10.1039/B509494A)
11. R. Car and M. Parrinello, “Unified Approach for Molecular Dynamics and Density-Functional Theory,” *Physical Review Letters* **55**, 2471–2474 (1985). [DOI](https://doi.org/10.1103/PhysRevLett.55.2471)
12. H. C. Andersen, “Molecular dynamics simulations at constant pressure and/or temperature,” *The Journal of Chemical Physics* **72**, 2384–2393 (1980). [DOI](https://doi.org/10.1063/1.439486)
13. G. Bussi, D. Donadio, and M. Parrinello, “Canonical sampling through velocity rescaling,” *The Journal of Chemical Physics* **126**, 014101 (2007). [DOI](https://doi.org/10.1063/1.2408420)
14. VASP Team, “Molecular-dynamics calculations,” *VASP Wiki*. [공식 문서](https://vasp.at/wiki/MD_runs)
15. A. Grossfield and D. M. Zuckerman, “Quantifying uncertainty and sampling quality in biomolecular simulations,” *Annual Reports in Computational Chemistry* **5**, 23–48 (2009). [DOI](https://doi.org/10.1016/S1574-1400(09)00502-7)
16. J. D. Chodera, “A Simple Method for Automated Equilibration Detection in Molecular Simulations,” *Journal of Chemical Theory and Computation* **12**, 1799–1805 (2016). [DOI](https://doi.org/10.1021/acs.jctc.5b00784)
