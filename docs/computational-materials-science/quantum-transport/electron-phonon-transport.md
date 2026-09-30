---
description: 전자–포논 SCBA 계산에서 전류와 에너지 보존을 확인하고 포논 가열, IETS와 약결합 근사의 적용 범위를 설명
---

# NEGF: Electron–phonon coupling (2)

**Non-equilibrium Green's function (NEGF)** 계산에서 **electron–phonon coupling (EPC)**의 효과는 산란 self-energy를 얻는 데서 끝나지 않는다. 산란으로 달라진 전자 상태와 점유를 다시 구한 뒤, 그 해가 양쪽 단자의 전류와 포논으로 전달되는 에너지를 일관되게 설명하는지 확인해야 한다. 이 글은 **self-consistent Born approximation (SCBA)**의 계산 절차에서 출발하여 전류, 에너지 전달, 진동 신호의 순서로 관측량을 연결한다.[1,2]

결합 행렬과 흡수·방출 self-energy의 유도는 [NEGF: Electron–phonon coupling (1)](electron-phonon-coupling.md)을 따른다. 정상 상태, 직교 전자 기저, 조화 진동과 변위에 선형인 EPC를 가정한다. 전극은 $L,R$이며, 모든 spin 상태를 행렬 trace에 한 번씩 포함한다. 전자 전하는 $-e$ ($e>0$), $h=2\pi\hbar$이다. $I_\alpha$는 전극 $\alpha$에서 소자로 들어오는 순 전자 입자 흐름에 $e$를 곱한 값으로 정의한다. 따라서 $I_L>0$은 왼쪽 전극에서 소자로의 전자 유입을 뜻한다. 문헌마다 전류 방향과 spin 인자가 다르므로 이 규약으로 변환하여 비교한다.[1,2]

## 1. SCBA의 자기일관 계산

### (1) 상태와 점유의 동시 갱신

SCBA는 결합 행렬 $M^\lambda$에 대해 2차인 self-energy 안에 **산란까지 포함한 전자 Green's function**을 사용한다. 모드 $\lambda$의 진동수 $\omega_\lambda$와 점유 $n_\lambda$를 고정해도, 전자 점유가 바뀌면 산란으로 들어오고 나가는 전자의 양이 바뀐다. 같은 $G$가 self-energy의 입력이자 출력이 되어야 하므로 반복 계산이 필요하다.[1,2]

$$
G^{R,</>}
\longrightarrow\Sigma_{e\text{-}ph}^{R,</>}[G]
\longrightarrow G^{R,</>}.
$$

전자 Hamiltonian을 $H_D$, 단위행렬을 $\mathbf 1$, 전극 self-energy를 $\Sigma_{L,R}$라 하자. 한 반복에서 retarded 성분은 Dyson 식으로 갱신한다.[1,2]

$$
G^R(E)=\left[(E+i0^+)\mathbf 1-H_D
-\Sigma_L^R(E)-\Sigma_R^R(E)
-\Sigma_{e\text{-}ph}^R(E)\right]^{-1},
\qquad G^A=(G^R)^\dagger.
$$

$0^+$는 retarded 경계조건이다. 실제 계산에서 이를 유한한 수로 두면 인공적인 선폭이 생기므로 그 영향도 수렴시켜야 한다. EPC의 정적인 Hartree 이동을 별도로 계산하는지, 기준 Hamiltonian에 반영하고 동적인 Fock 항을 반복하는지는 첫 편의 규약에 맞춘다. 두 곳에 같은 정적 이동을 중복해서 넣지 않는다.[1,2]

Lesser와 greater 성분은 전체 self-energy를 사용한 Keldysh 식으로 얻는다. 여기서 $\Sigma_{\rm tot}$는 전극 두 개와 EPC 기여의 합이다.[1,2]

$$
G^{</>}=G^R\Sigma_{\rm tot}^{</>}G^A,
\qquad
\Sigma_{\rm tot}^{</>}=\Sigma_L^{</>}+\Sigma_R^{</>}
+\Sigma_{e\text{-}ph}^{</>}.
$$

이 식에서 EPC 항이 필요한 이유는 다른 에너지에서 산란해 들어온 전자도 해당 에너지의 점유에 기여하기 때문이다. 포논은 전자 저장고가 아니며, 전자가 포논을 주고받으면서 서로 다른 에너지 사이를 이동한다. Retarded 성분에 EPC를 넣으면서 lesser 성분에는 전극만 넣으면 상태의 변화와 점유의 변화를 서로 다른 모형으로 계산하게 된다.[1,2]

점유와 비점유 성분은 $G^n=-iG^<$, $G^p=iG^>$로 쓰며, spectral function은 $A=G^n+G^p=i(G^R-G^A)$이다. 마찬가지로 $\Sigma^{\rm in}=-i\Sigma^<$, $\Sigma^{\rm out}=i\Sigma^>$를 정의한다. 그러면 전자 갱신은 다음처럼 점유·비점유의 의미가 드러나는 형태로도 쓸 수 있다.[1,2]

$$
G^n=G^R\Sigma_{\rm tot}^{\rm in}G^A,
\qquad
G^p=G^R\Sigma_{\rm tot}^{\rm out}G^A.
$$

$G$의 단위는 에너지의 역수, $\Sigma$의 단위는 에너지이다. $G^n$ 자체는 무차원 점유 확률이 아니라 에너지별 점유된 상태의 무게이다. 다중 궤도 문제에서는 일반적으로 하나의 Fermi 함수만으로 행렬 $G^n$을 표현할 수 없다.[1,2]

### (2) 반복 순서와 계산 입력

다음 절차는 포논 점유를 고정한 전자 SCBA이다. 에너지 격자 전체의 $G$를 준비한 뒤, 첫 편의 $E\pm\hbar\omega_\lambda$에서 평가하는 산란 식을 적용한다. 한 에너지에서만 Dyson 식을 반복하는 방식으로는 서로 다른 에너지의 점유가 연결되는 문제를 닫을 수 없다.[1,2]

| 단계 | 계산 내용 | 확인할 값 |
|---|---|---|
| 입력 | $H_D$, 전극, $M^\lambda$, $\omega_\lambda$, $n_\lambda$ 준비 | 기저·에너지 기준·spin 규약 |
| 초기화 | EPC를 뺀 탄성 해 $G_0$ 계산 | 전극이 정하는 상태와 점유 |
| 산란 갱신 | 현재 $G$로 모드별 lesser/greater self-energy 계산 | 이동된 에너지의 상태와 점유 |
| 인과성 복원 | 같은 산란 항에서 retarded 성분 계산 | 선폭과 실수 에너지 이동 |
| 전자 갱신 | Dyson·Keldysh 식 재계산 | 새 $G^R,G^n,G^p$ |
| 종료 판단 | 반복 잔차와 관측량 비교 | 양쪽 전류·에너지 전달·보존 잔차 |

반복을 안정화하려고 새 값과 이전 값을 섞을 수 있다. 예를 들어 $k$를 반복 번호, $\widehat\Sigma[G^{(k)}]$를 현재 $G$에서 직접 계산한 새 self-energy라 하고, 무차원 혼합 계수 $0<a\leq1$을 정하면

$$
\Sigma^{(k+1)}=(1-a)\Sigma^{(k)}
+a\widehat\Sigma[G^{(k)}]
$$

로 갱신한다. 이는 물리 법칙을 추가하는 식이 아니라 고정점 방정식을 푸는 수치적 선택이다. 같은 계열의 성분을 일관되게 섞고 retarded 관계를 유지해야 한다. 작은 $a$를 사용해 연속 반복의 차이가 작아져도 원래 방정식의 잔차가 작다는 뜻은 아니므로, 종료 판단에는 $\widehat\Sigma[G]-\Sigma$도 사용한다.

전하 밀도에 따라 $H_D$가 달라지는 계산은 정전위도 갱신해야 한다. 포논 점유를 구하려면 여기에 진동의 에너지 수지까지 더해진다. 따라서 결과에 “자기일관 계산”이라고만 쓰기보다 아래의 어느 미지수를 갱신했는지 밝히는 편이 정확하다.[1,2]

| 반복 대상 | 미지수 | 추가로 필요한 관계 |
|---|---|---|
| 전자 산란 | $G$와 $\Sigma_{e\text{-}ph}$ | Dyson·Keldysh·선택한 산란 근사 |
| 전하와 정전위 | 밀도와 $H_D$ | 사용하는 정전위 또는 전자구조 모형 |
| 포논 점유 | $n_\lambda$ | 전자 에너지 전달과 포논 완화 |

## 2. 단자 전류와 전하 보존

### (1) 유입과 유출의 차이

전류를 정하는 것은 전극에서 들어오는 전자와 전극으로 빠져나가는 전자의 차이이다. 에너지별 순유입을 나타내는 무차원 충돌 항 $C_\alpha$를 정의하면 단자 전류는 다음과 같다.[1,2]

$$
\begin{aligned}
C_\alpha(E)&=\operatorname{Tr}
[\Sigma_\alpha^<G^>-\Sigma_\alpha^>G^<]\\
&=\operatorname{Tr}
[\Sigma_\alpha^{\rm in}G^p-\Sigma_\alpha^{\rm out}G^n],\\
I_\alpha&=\frac{e}{h}\int_{-\infty}^{\infty}dE\,C_\alpha(E).
\end{aligned}
$$

첫 항에는 전극의 공급과 소자의 빈 상태가, 둘째 항에는 소자의 점유된 상태와 전극으로의 유출이 곱해진다. 두 항 각각은 클 수 있지만 평형에서는 차이가 0이다. 전류 단위도 이 구조에서 확인된다. $\Sigma G$는 무차원이고 $dE/h$는 시간의 역수이므로 최종 단위는 전하/시간이다.[1,2]

전극의 Fermi 함수를 $f_\alpha(E)$, 전극 결합에 의한 선폭 행렬을 $\Gamma_\alpha=i(\Sigma_\alpha^R-\Sigma_\alpha^A)$라 하면 $\Sigma_\alpha^{\rm in}=f_\alpha\Gamma_\alpha$, $\Sigma_\alpha^{\rm out}=(1-f_\alpha)\Gamma_\alpha$이다. 이를 대입하면 같은 전류를 다음처럼 표현한다.[1,2]

$$
I_\alpha=\frac{e}{h}\int dE\,
\operatorname{Tr}\!\left[\Gamma_\alpha(f_\alpha A-G^n)\right].
$$

이 형태는 전극이 채우려는 양 $f_\alpha A$와 실제 점유 $G^n$의 차이를 보여 준다. 스펙트럼 $A$만으로는 전류가 정해지지 않는다. 전극과의 결합이 강한 상태라도 그 상태가 양쪽에서 어떻게 채워지는지 알아야 순흐름을 구할 수 있다.[1,2]

### (2) 정상 상태의 연속 방정식

EPC 충돌 항 $C_{e\text{-}ph}$도 단자 항과 같은 방식으로 정의한다. Dyson·Keldysh 식과 self-energy 관계를 일관되게 만족하면 정상 상태의 trace 항등식은 다음과 같다.[1,2]

$$
C_L(E)+C_R(E)+C_{e\text{-}ph}(E)=0.
$$

각 에너지에서는 포논 산란이 전자를 가져오거나 내보내므로 $C_L+C_R$만 0일 필요는 없다. 그러나 EPC는 전자를 생성·소멸시키지 않는다. 일관된 SCBA에서 모든 에너지에 대해 합하면 산란에 의한 입자 변화가 상쇄된다.[1,2]

$$
\int dE\,C_{e\text{-}ph}(E)=0
\quad\Longrightarrow\quad I_L+I_R=0.
$$

첫 편의 한 포논 과정으로 보면, 어떤 에너지에서 사라진 전자는 $\hbar\omega_\lambda$만큼 떨어진 다른 에너지에 나타난다. 적분 변수를 그만큼 옮기면 두 기여가 상쇄된다. 이 검산에는 같은 $G$, 같은 이동 규칙, 충분한 적분 범위가 필요하다. 미수렴 반복이나 경계에서 잘린 에너지 격자는 수치적으로 그 상쇄를 깨뜨릴 수 있다.[1,2]

### (3) Landauer 극한과 단일 준위의 점유

$M^\lambda=0$이면 EPC self-energy가 사라진다. 탄성 해 $G_0$에서는 전극별 spectral 기여를 더하여 $A_0$와 $G_0^n$을 구성할 수 있다.[1,2]

$$
\begin{aligned}
A_0&=G_0^R(\Gamma_L+\Gamma_R)G_0^A,\\
G_0^n&=G_0^R(f_L\Gamma_L+f_R\Gamma_R)G_0^A.
\end{aligned}
$$

이를 왼쪽 전류식에 넣으면 같은 전극의 주입·유출이 상쇄되고 두 전극의 점유 차이만 남는다. 그 결과가 coherent Landauer 식이다.[1,2]

$$
I_0=\frac{e}{h}\int dE\,T_0(E)[f_L-f_R],
\qquad
T_0(E)=\operatorname{Tr}[\Gamma_LG_0^R\Gamma_RG_0^A].
$$

EPC가 있을 때 $G_0$를 산란으로 넓어진 $G$로 바꿔 이 식에 넣는 것만으로는 일반적인 상호작용 전류가 되지 않는다. 누락되는 점유 기여를 보기 위해 한 spin의 단일 준위를 생각하자. 이 경우 행렬은 스칼라가 되며 $A>0$인 에너지에서 $f_{\rm eff}=G^n/A$를 정의할 수 있다. $\Gamma_{e\text{-}ph}=\Sigma_{e\text{-}ph}^{\rm in}+\Sigma_{e\text{-}ph}^{\rm out}$라 두면 Keldysh 식으로부터 다음 결과를 직접 얻는다.[1,2]

$$
f_{\rm eff}(E)=
\frac{\Gamma_Lf_L+\Gamma_Rf_R+\Sigma_{e\text{-}ph}^{\rm in}}
{\Gamma_L+\Gamma_R+\Gamma_{e\text{-}ph}},
\qquad
C_\alpha=\Gamma_\alpha A(f_\alpha-f_{\rm eff}).
$$

분모는 전체 선폭이고 분자는 채워지는 양이다. EPC를 선폭에만 넣으면 분모만 바꾸는 셈이다. 실제로는 $E\pm\hbar\omega_\lambda$에서 오는 $\Sigma^{\rm in}_{e\text{-}ph}$도 분자에 들어간다. 이 식은 단일 준위에서 도출한 설명용 관계이며, 비가환 행렬 문제에서 분자와 분모를 그대로 나누어서는 안 된다.[1,2]

## 3. 에너지 전달과 포논 가열

### (1) 에너지 전류와 국소 전력

전자 수가 보존되어도 전자 에너지는 포논으로 전달될 수 있다. 전극 $\alpha$에서 소자로 들어오는 전자 에너지 전류 $J_\alpha^E$는 입자 흐름에 에너지를 곱해 얻는다. 두 전극과 소자의 $E$는 같은 기준을 사용한다.[1,2]

$$
J_\alpha^E=\frac{1}{h}\int dE\,E C_\alpha(E).
$$

전자계가 정상 상태이고 내부 에너지 교환 경로가 EPC뿐이면, 전자에서 포논으로 전달되는 순전력은 다음과 같다. 양의 $P_{e\to ph}$는 전자가 에너지를 잃고 포논이 얻는 경우이다.[1,2]

$$
P_{e\to ph}=J_L^E+J_R^E
=-\frac{1}{h}\int dE\,E C_{e\text{-}ph}(E).
$$

입자 보존 적분과 달리 여기에는 $E$가 곱해져 있다. 전자가 높은 에너지에서 사라지고 낮은 에너지에 나타나면 입자 수 변화는 0이지만 에너지 차이는 남는다. 한 포논 모드에 대해 방출·흡수 사건 수를 단위 시간당 각각 $R_{\rm em}$, $R_{\rm abs}$로 셀 수 있는 약결합 한 포논 해석에서는

$$
P_{e\to ph}=\hbar\omega(R_{\rm em}-R_{\rm abs})
$$

가 된다. 여기서 $R$은 실제 점유와 Pauli 차단을 포함한 전체 사건률이다. $M^2$이나 $n+1$만을 사건률로 해석해서는 안 된다. 이 관계는 전자 에너지 손실과 포논 생성이 같은 사건의 두 측면임을 보여 준다.[1,2]

### (2) 열전류와 회로 전력의 구별

에너지 전류에는 전자의 이동에 따른 화학적 일도 포함되어 있다. 전극 $\alpha$의 화학 퍼텐셜을 $\mu_\alpha$라 하고 **전극에서 소자로 들어오는** 열전류를 $J_\alpha^Q$로 정의하면

$$
J_\alpha^Q=J_\alpha^E-\mu_\alpha I_\alpha/e
$$

이다. 문헌 [2]의 전극에서 발생하는 열을 양으로 잡는 식과는 방향이 반대이다. 바이어스를 $\mu_L-\mu_R=eV$, 전류를 $I=I_L=-I_R$로 정의하여 두 전극의 식을 합하면 다음 에너지 수지를 얻는다.[1,2]

$$
J_L^Q+J_R^Q=P_{e\to ph}-IV.
$$

따라서 소자의 포논에 전달된 전력과 회로가 공급한 $IV$는 같은 양이 아니다. 예를 들어 탄성 한계에서는 $P_{e\to ph}=0$이어도 전류와 $IV$는 0이 아닐 수 있다. 이때 에너지는 전극의 평형 분포를 유지하는 과정에서 소산된다. 국소 가열을 논할 때에는 어느 영역의 에너지 전달을 계산했는지 먼저 정해야 한다.[1,2]

에너지 영점을 상수 $E_c$만큼 옮기면 각 에너지 전류는 $J_\alpha^E+E_cI_\alpha/e$로 바뀐다. 하지만 전하 보존이 성립하면 두 에너지 전류의 합은 변하지 않는다. 이는 위 식에서 직접 얻는 유용한 검산이며, 잘못된 전류 부호나 전극마다 다른 에너지 기준을 찾는 데 쓸 수 있다.

### (3) 고정된 열저장고와 비평형 포논 점유

포논 점유를 Bose 분포에 고정한 계산에서도 전자에서 포논으로 에너지가 전달될 수 있다. 고정된 분포는 외부 열저장고가 그 에너지를 받아 가며 점유를 유지한다는 가정이다. 따라서 $P_{e\to ph}$를 계산했다는 사실만으로 포논 온도 상승까지 계산한 것은 아니다.[1,2]

모드별 점유 변화가 느리고 진동 모드를 구분할 수 있는 약결합 모형에서는 전자에서 모드 $\lambda$로 전달되는 전력 $P_\lambda$와 외부 완화를 다음처럼 연결할 수 있다. $\gamma_\lambda$는 외부 열저장고에 의한 점유 완화율이며 단위는 시간의 역수이다.[1,2]

$$
\frac{dn_\lambda}{dt}
=\frac{P_\lambda(\{n\},V)}{\hbar\omega_\lambda}
-\gamma_\lambda[n_\lambda-n_B(\omega_\lambda,T_b)],
\qquad
n_B=\frac{1}{\exp(\hbar\omega_\lambda/k_BT_b)-1}.
$$

$T_b$는 열저장고 온도, $k_B$는 Boltzmann 상수이다. 첫 항은 전자가 만드는 순 포논 수, 둘째 항은 열저장고 점유로 돌아가려는 완화이다. $P_\lambda$ 안에는 방출과 흡수가 모두 포함된다. 여러 모드에 대해 전자 에너지 수지와 일치하도록 $\sum_\lambda P_\lambda=P_{e\to ph}$를 사용한다. 넓은 진동 스펙트럼이나 강한 모드 혼합에서는 이 단순한 모드별 점유식의 타당성을 별도로 확인해야 한다.[1,2]

$\gamma_\lambda>0$인 정상 상태에서는

$$
n_\lambda=n_B(\omega_\lambda,T_b)
+\frac{P_\lambda(\{n\},V)}
{\hbar\omega_\lambda\gamma_\lambda}
$$

이다. 우변의 $P_\lambda$도 포논 점유에 의존하므로, 고정된 bath에서 계산한 전력을 한 번 대입하는 것만으로 일반적인 가열 문제를 푼 것은 아니다. $n_\lambda$를 바꾸면 전자의 흡수·방출 self-energy가 바뀌고, 다시 전자 해와 전력을 구해야 한다.[1,2]

| 포논 처리 | 고정하는 것 | 계산으로 얻는 것 |
|---|---|---|
| 고정된 Bose 분포 | $T_b$와 $n_\lambda=n_B$ | 주어진 bath로의 에너지 전달 |
| 모드별 점유 방정식 | $T_b$, 외부 완화율과 모드 모형 | 비평형 $n_\lambda$와 전자 해 |
| 포논 Green's function 갱신 | 포논 bath self-energy와 상호작용 근사 | 진동 스펙트럼·점유의 변화 |

서로 다른 모드의 비평형 점유가 하나의 Bose 온도를 공유할 이유는 없다. 따라서 단일한 “소자 온도”를 제시하려면 모드들이 열평형으로 기술될 수 있다는 추가 가정과 그 근거가 필요하다.[1,2]

## 4. IETS와 약결합 근사

### (1) 비탄성 문턱과 신호의 부호

**Inelastic electron tunneling spectroscopy (IETS)**는 전류의 전압 미분에 나타나는 진동 신호를 분석한다. 낮은 온도에서 $\mu_L>\mu_R$이고 한 포논을 방출하는 전자가 왼쪽의 점유 상태에서 오른쪽의 빈 상태로 이동한다고 생각하자. 초기 에너지 $E_i$는 다음 두 조건을 동시에 만족해야 한다.[1,2]

$$
E_i\leq\mu_L,
\qquad E_i-\hbar\omega_\lambda\geq\mu_R
\quad\Longrightarrow\quad
\mu_L-\mu_R\geq\hbar\omega_\lambda.
$$

따라서 대표적인 방출 문턱은 $|eV|\simeq\hbar\omega_\lambda$이다. 이는 전자의 절대 에너지가 아니라 점유된 출발 상태와 빈 도착 상태를 동시에 확보할 수 있는 에너지 구간에 대한 조건이다. 유한 온도에서는 경계가 퍼지고, 이미 점유된 포논의 흡수도 가능하므로 날카로운 문턱이라는 설명은 낮은 온도의 약결합 한계에 해당한다.[1,2]

진동 모드가 존재한다고 모두 강한 IETS 신호를 만드는 것은 아니다. $M^\lambda$가 실제 수송 상태를 연결해야 한다. 또한 비탄성 경로가 열리는 기여와 탄성 전파 진폭의 보정이 함께 전류를 바꾼다. 따라서 문턱에서 전도도가 증가하거나 감소할 수 있고, 이차 미분에는 peak, dip 또는 비대칭 구조가 나타날 수 있다. 진동 에너지 목록만 맞추는 검증으로는 신호의 크기와 부호를 설명할 수 없다.[1,2]

!!! info "[Measurement]"
    전극 온도와 접합 구조를 고정하고 바이어스 $V$를 주사하여 $I(V)$를 구한다. 계산은 각 전압에서 같은 수렴 기준을 사용한다. 미분 전도도 $\mathcal G$와 비정규화 IETS 신호 $\mathcal S$는

    $$
    \mathcal G(V)=\frac{dI}{dV},
    \qquad \mathcal S(V)=\frac{d^2I}{dV^2}
    $$

    로 정의하며 단위는 각각 A/V, A/V$^2$이다. 문턱 위치는 $\hbar\omega_\lambda/e$와 비교하고, 세기·부호는 결합 행렬을 포함한 전체 전류로 해석한다. 온도, 전압 간격, 미분 구간, 실험의 변조 전압을 함께 보고한다. 측정 곡선과 비교할 때에는 열적 퍼짐과 측정의 에너지 분해능도 맞춰야 한다.[1,2]

### (2) LOE의 전개 차수와 에너지 의존성

**Lowest order expansion (LOE)**은 탄성 해 주변에서 전류를 EPC의 최저 비영차수인 2차까지 전개한다. 무차원 매개변수 $s$로 모든 결합을 $M^\lambda\mapsto sM^\lambda$로 바꾸면, 고정된 기준 구조와 포논 bath에 대한 약결합 전개는 다음처럼 표현할 수 있다.[1,2]

$$
I(s)=I_0+s^2\delta I^{(2)}+O(s^4).
$$

$\delta I^{(2)}$에는 실제 포논 교환뿐 아니라 같은 차수의 탄성 보정도 포함한다. SCBA의 첫 반복에서 self-energy를 얻었다고 곧바로 전류를 엄밀하게 2차까지만 전개한 것과 같지는 않다. 그 self-energy를 Dyson 역행렬에 그대로 넣으면 일부 고차 항도 포함되기 때문이다. 비교할 때는 self-energy의 차수와 최종 전류의 차수를 구별해야 한다.[1,2]

널리 쓰이는 효율적인 LOE는 이 전개에 더하여 관련 에너지 구간에서 $G_0^R$와 전극 self-energy가 천천히 변한다고 가정한다. 이때 전자 행렬을 기준 에너지에서 평가하고 Fermi·Bose 함수의 에너지 적분을 별도로 처리할 수 있다. 약한 결합과 느린 에너지 의존성은 서로 다른 조건이다.[1,3]

단일 준위로 두 번째 조건을 구체화할 수 있다. 준위 에너지를 $\varepsilon_0$, 에너지에 무관한 전극 선폭을 $\Gamma=\Gamma_L+\Gamma_R>0$라 하면

$$
G_0^R(E)=\frac{1}{E-\varepsilon_0+i\Gamma/2},
\qquad
\left|\frac{\delta G_0^R}{G_0^R}\right|
\simeq\frac{|\delta E|}
{\sqrt{(E-\varepsilon_0)^2+(\Gamma/2)^2}}.
$$

오른쪽은 작은 에너지 변화 $\delta E$에 대한 미분으로 얻은 추정이다. 포논 에너지와 바이어스·열적 구간을 움직였을 때 이 비가 작아야 상수 $G_0$ 근사가 자연스럽다. 공명에서 멀면 분모는 준위까지의 에너지 차이가, 공명 부근에서는 선폭이 정한다. 따라서 매우 좁은 공명은 EPC가 작아도 상수 전자 행렬을 사용하는 LOE에 불리하다. 이 비는 해당 스칼라 모형의 진단이며 다중 준위 접합의 보편적 오차 한계는 아니다.[1–3]

### (3) SCBA의 물리적 적용 범위

SCBA의 반복 수렴은 선택한 근사 방정식의 해를 얻었다는 뜻이다. 모든 고차 산란이나 vertex 보정까지 정확히 포함했다는 뜻은 아니다. 전극과의 결합이 약하여 전자가 준위에 오래 머물고 진동 결합이 큰 경우, 구조의 재배열이나 강한 전자–진동 상관은 이 근사의 범위를 벗어날 수 있다.[1,2]

| 방법 | 유지하는 내용 | 별도로 확인할 조건 |
|---|---|---|
| LOE | 탄성 전류와 2차 EPC 보정 | 약결합, 채택한 전자 에너지 의존성 근사 |
| 고정 bath 전자 SCBA | 선택한 2차 self-energy를 dressed $G$로 반복 | 전하 보존, 포논 분포 고정의 타당성 |
| 전자·포논 공동 계산 | 포논 점유나 스펙트럼의 되먹임 | 포논 완화 모형과 상호작용 근사 |

어느 방법이든 조화 진동, 선형 EPC, 전자 Hamiltonian의 정확도라는 공통 전제가 남는다. 더 많은 반복으로 잘못된 기저 모형이나 누락된 물리를 보완할 수는 없다. 결과를 해석할 때는 수치 오차와 물리적 근사 오차를 분리해서 평가한다.[1,2]

## 5. 수치 검증과 결과 보고

### (1) 에너지 격자와 반복 잔차

에너지 격자는 bias window보다 넓어야 한다. $E\pm\hbar\omega_\lambda$의 점유를 읽어야 하고, retarded 실수부의 주값 적분은 더 먼 에너지에도 의존하기 때문이다. 반복 산란에서는 이 연결이 이어지므로 최대 포논 에너지 한 번만큼 격자를 늘렸다는 사실만으로 충분성이 보장되지 않는다. 범위를 실제로 늘려 관측량을 비교해야 한다.[1,2]

수치 시험은 한 번에 한 조건을 바꾸는 것이 해석하기 쉽다. 다음 표는 앞의 방정식에서 직접 얻는 구현 점검 항목이며, 특정 코드에 공통으로 적용되는 고정 허용오차를 제시하는 것은 아니다.

| 변경할 조건 | 비교할 관측량 | 드러나는 문제 |
|---|---|---|
| 에너지 간격 축소 | 전류·전력·공명 형태 | 좁은 상태나 Fermi 경계의 미해상 |
| 적분 범위 확대 | 실수 self-energy·보존 잔차 | 잘린 꼬리와 주값 적분 |
| 에너지 이동 보간 개선 | 문턱 위치·전류 보존 | $E\pm\hbar\omega$ 표본 오차 |
| 반복 기준 강화 | 원래 방정식 잔차·양쪽 전류 | 겉보기 반복 수렴 |
| 전압 간격 변경 | $dI/dV$, $d^2I/dV^2$ | 미분 과정의 오차 증폭 |

반복 오차를 보고하는 한 가지 방법은, 행렬 원소 제곱합의 제곱근인 Frobenius norm $\|\cdot\|_F$로 self-energy의 고정점 잔차를 측정하는 것이다. 성분 $x\in\{R,<,>\}$와 에너지 격자 전체에 대해

$$
r_\Sigma=\max_{E,x}
\frac{\|\widehat\Sigma^x[G](E)-\Sigma^x(E)\|_F}
{\max(\|\Sigma^x(E)\|_F,\Sigma_{\rm floor})}
$$

를 정의할 수 있다. $\Sigma_{\rm floor}>0$는 에너지 단위의 기준값이다. 이는 이 글의 보고용 정의이며 보편적인 수렴 판정식은 아니다. $r_\Sigma$와 함께 전류·전력의 절대 변화를 보고하면 작은 self-energy나 영전류 근처에서도 해석이 가능하다.

### (2) 보존 법칙과 극한 검사

전하 보존의 상대 잔차는 예를 들어 다음처럼 정의한다.

$$
\epsilon_I=
\frac{|I_L+I_R|}
{\max(|I_L|,|I_R|,I_{\rm floor})}.
$$

$I_{\rm floor}>0$는 전류 단위의 보고 기준값이다. 평형처럼 전류가 작은 경우에는 절대 잔차 $|I_L+I_R|$도 함께 기록한다. 에너지 보존은 contact 쪽과 EPC 충돌 적분 쪽을 따로 계산하여 대조한다. 두 방식으로 얻은 전력을 $P_{\rm contacts}$, $P_{\rm collision}$이라 하면

$$
\Delta P=|P_{\rm contacts}-P_{\rm collision}|,
\qquad
P_{\rm contacts}=J_L^E+J_R^E
$$

가 독립적인 구현 경로를 비교하는 잔차이다. 한쪽 전력을 다른 쪽 값으로 정의해 저장한 뒤 비교하면 검사가 되지 않는다. 또한 에너지 영점 이동 검사도 함께 수행하면 전하 잔차가 전력에 섞이는 문제를 확인할 수 있다.

| 검사 조건 | 만족해야 할 결과 | 의미 |
|---|---|---|
| $M^\lambda=0$ | 같은 $H_D$의 Landauer 전류 | 기본 부호·spin·전극 입력 |
| 공통 $\mu,T$, 같은 온도의 포논 | 순전류와 순 에너지 교환 0 | 상세평형과 흡수·방출 구현 |
| 유한 바이어스 | $I_L+I_R\to0$ | 전자 수 보존 |
| contact와 충돌 적분 비교 | $\Delta P\to0$ | 에너지 전달의 일관성 |
| 결합을 약하게 축소 | 적합한 조건에서 2차 보정으로 접근 | 섭동적 극한 |

이 검사는 앞 절의 방정식과 가정을 코드에 적용한 것이다. 공통 전자 온도만 맞추고 포논 bath를 다른 온도에 두면 열평형 시험이 아니며, 그 경우 에너지 교환이 남는 것은 오류가 아니다. 마찬가지로 전하 보존을 통과해도 실제 사용한 EPC 근사가 강결합 영역에서 정확하다는 결론은 얻을 수 없다.[1,2]

### (3) 미분 신호의 수렴

IETS를 보고하려면 전류보다 작은 진동 보정을 분해해야 한다. 균일한 전압 간격 $\Delta V$에서 중앙 차분을 사용하면

$$
\mathcal S(V)\simeq
\frac{I(V+\Delta V)-2I(V)+I(V-\Delta V)}{(\Delta V)^2}
$$

이다. 세 전류값의 계산 오차가 각각 절댓값 $\delta I$ 이하이면, 이 차분에 들어가는 오차의 상한은 삼각부등식으로 $4\delta I/(\Delta V)^2$이다. 따라서 전압 간격만 줄이면 오히려 수치 잡음이 커질 수 있다. $\Delta V$를 줄이는 동시에 각 전압의 SCBA와 에너지 적분 정확도를 높여야 한다. 이 상한은 계산 오차 전파에 대한 추정이며 실제 물리 신호의 폭을 뜻하지 않는다.

최종 결과에는 $I(V)$만 제시하기보다 사용한 $M^\lambda$와 진동 에너지, 포논 bath 또는 완화 모형, 양쪽 전류의 잔차, 에너지 범위·간격, 전압 간격을 함께 남긴다. 미분 곡선이 조건 변경에도 유지되는지 확인하고 나서 peak와 dip의 물리적 의미를 해석한다.[1,2]

## 6. 요약

- SCBA는 산란 self-energy와 전자 상태·점유를 같은 해에 도달할 때까지 반복한다.
- 단자 전류는 주입과 유출의 차이이며, EPC를 넣은 retarded 성분만으로는 일반적인 전류를 구할 수 없다.
- EPC는 전자 수를 보존하지만 전자 에너지를 포논에 전달할 수 있다. 국소 전달 전력은 회로 전체의 $IV$와 구별한다.
- 포논 온도나 비평형 점유를 구하려면 외부로의 완화와 전자의 되먹임을 추가한다.
- IETS의 부호·세기와 LOE의 타당성은 결합 행렬과 전자 스펙트럼에 의존한다. 보존 법칙, 격자 수렴, 물리적 근사 범위를 각각 확인한다.

## 7. 참고문헌

1. T. Frederiksen, M. Paulsson, M. Brandbyge, and A.-P. Jauho, "Inelastic transport theory from first principles: Methodology and application to nanoscale devices," *Physical Review B* **75**, 205413 (2007). [DOI](https://doi.org/10.1103/PhysRevB.75.205413), [원문](https://arxiv.org/html/cond-mat/0611562). 전류: Secs. III.2–III.3; SCBA와 전력: Sec. III.4; LOE와 진동 신호: Secs. III.5–III.6; 수치 구현: Appendices A–C.
2. M. Galperin, M. A. Ratner, and A. Nitzan, "Molecular transport junctions: Vibrational effects," *Journal of Physics: Condensed Matter* **19**, 103201 (2007). [DOI](https://doi.org/10.1088/0953-8984/19/10/103201), [원문](https://arxiv.org/pdf/cond-mat/0612085). NEGF와 전류: Sec. 3d, Eqs. (23)–(30); SCBA와 IETS: Secs. 5b–5d; 약결합 계산: Sec. 5g; 에너지·열전류와 가열: Sec. 9, Eqs. (93)–(109).
3. J. K. Viljas, J. C. Cuevas, F. Pauly, and M. Häfner, "Electron-vibration interaction in transport through atomic gold wires," *Physical Review B* **72**, 245415 (2005). [DOI](https://doi.org/10.1103/PhysRevB.72.245415), [원문](https://arxiv.org/pdf/cond-mat/0508470). 섭동적 전류: Sec. III C; 전자 에너지 의존성의 근사: Sec. IV; 에너지 의존성을 유지한 출발식: Appendix E.
