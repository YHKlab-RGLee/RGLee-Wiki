---
description: 전자 밀도의 변분 원리에서 Kohn–Sham 방정식을 유도하고 교환·상관 근사, 자기일관 계산과 에너지 해석의 한계를 설명한다.
---

# Density functional theory

Density functional theory (DFT)는 전자 밀도를 기본 변수로 하여 상호작용하는 전자계의 바닥상태 에너지와 밀도를 구하는 이론이다. 핵심은 다전자 파동함수를 단순히 생략하는 데 있지 않고, 그 파동함수의 최적화 문제를 밀도에 대한 에너지 범함수의 최소화로 바꾸는 데 있다. Kohn–Sham (KS) 구성에서는 같은 밀도를 갖는 비상호작용 보조계를 도입하고, 보조계가 직접 표현하지 못하는 에너지 성분을 exchange–correlation (XC) 범함수로 모은다. 이 구성 자체는 형식적으로 정확하며, 실제 계산의 핵심 근사는 알지 못하는 XC 범함수의 선택에서 들어간다.[1,2]

[Hartree–Fock method](hartree-fock-method.md)의 Slater determinant, 변분 원리와 자기일관성 개념을 선행 지식으로 삼는다. 이하에서는 고정 핵의 비상대론적 Coulomb 전자계, 영온 바닥상태와 외부의 국소 스칼라 potential을 기준으로 한다. 수식은 유한계에서 전개하고 먼저 spin 비편극 공간 궤도함수로 설명한 뒤 spin 분극을 구분한다. 주기계의 구현 세부, 시간에 따른 응답과 들뜬상태 전체의 계산은 이 문서의 범위 밖이다.[1,2]

## 1. 전자 밀도와 변분 원리

DFT의 기본 문제는 **주어진 외부 potential에서 에너지를 최소로 만드는 허용 가능한 전자 밀도를 찾는 것**이다. 밀도를 지정하면 외부 potential 에너지는 즉시 계산할 수 있지만, 운동에너지와 전자 상호작용은 밀도 전체에 의존하는 범함수로 남는다. 이 구분이 보편적인 내부 에너지와 계마다 다른 외부 환경을 분리한다.[1,2]

### (1) 전자 Hamiltonian과 밀도

Hartree 원자단위계인 $\hbar=m_e=e=4\pi\varepsilon_0=1$을 사용한다. $m_e$는 전자 질량, $e$는 기본 전하의 양의 크기, $\varepsilon_0$는 진공 유전율이다. 길이와 에너지 단위는 각각 Bohr radius와 Hartree이다. 전자 수를 $N$, 전자 위치를 $\mathbf r_i$, 전자의 외부 potential energy를 $v_{\mathrm{ext}}(\mathbf r)$라 하면 전자 Hamiltonian은 다음과 같다.[1,2]

$$
\hat H=\hat T+\hat W+\hat V_{\mathrm{ext}}
=-\frac12\sum_{i=1}^{N}\nabla_i^2
+\sum_{i<j}\frac{1}{|\mathbf r_i-\mathbf r_j|}
+\sum_{i=1}^{N}v_{\mathrm{ext}}(\mathbf r_i).
$$

$\hat T$는 운동에너지, $\hat W$는 전자–전자 반발, $\hat V_{\mathrm{ext}}$는 외부 potential 에너지 연산자이다. 핵의 위치와 전하가 만드는 인력은 $v_{\mathrm{ext}}$에 들어간다. 이 문서의 $v$는 전압 자체가 아니라 전자 한 개의 에너지이며, 핵–핵 반발 에너지 $E_{\mathrm{NN}}$는 전자 Hamiltonian 밖에 둔다. 고정한 핵 배치에서 $E_{\mathrm{NN}}$는 밀도 변분에 영향을 주지 않지만, 서로 다른 핵 배치의 총에너지를 비교할 때에는 포함해야 한다.[1,2]

정규화된 반대칭 파동함수를 $\Psi(x_1,\ldots,x_N)$, 공간·spin 좌표를 $x=(\mathbf r,\sigma)$로 쓴다. $dx$는 공간 적분과 spin 합을 함께 뜻한다. Spin을 합한 **전자 수밀도** $n$은

$$
n(\mathbf r)=N\sum_{\sigma}\int
|\Psi(\mathbf r,\sigma,x_2,\ldots,x_N)|^2\,dx_2\cdots dx_N,
\qquad \int n(\mathbf r)\,d\mathbf r=N
$$

으로 정의한다. 밀도의 차원은 길이의 역세제곱이며 전하밀도와 부호가 다르다. $n(\mathbf r)d\mathbf r$는 작은 부피 안의 평균 전자 수이다. 다전자 파동함수와 달리 밀도는 공간점 하나의 함수이지만, 이 단순한 변수로 에너지를 계산하는 법까지 알려진 것은 아니다. 범함수 $F[n]$는 밀도 함수 전체를 입력받아 하나의 에너지 값을 내는 규칙이다.[1,2]

### (2) Hohenberg–Kohn 정리와 constrained search

Hohenberg–Kohn (HK) 정리의 비축퇴 바닥상태 형태에서는 $n_0(\mathbf r)$가 $v_{\mathrm{ext}}$를 가산 상수까지 결정한다. 전자 수와 전자 사이의 상호작용을 고정했을 때, 같은 바닥상태 밀도를 만드는 서로 다른 스칼라 potential은 상수 차이를 제외하면 존재하지 않는다. 따라서 바닥상태의 성질은 원리적으로 밀도의 범함수이다. 이는 밀도에서 모든 관측량을 계산하는 명시적 공식을 제공한다는 뜻은 아니다.[1,2]

이를 변분 문제로 표현하는 방법이 constrained search이다. 주어진 밀도 $n$을 만드는 정규화된 반대칭 파동함수들 가운데 내부 에너지가 최소인 것을 선택하여

$$
F[n]=\min_{\Psi\to n}\langle\Psi|\hat T+\hat W|\Psi\rangle
$$

를 정의한다. $\Psi\to n$은 위의 밀도 정의를 만족한다는 제약이다. 탐색 영역은 유한한 운동에너지를 갖는 허용 가능한 전자 상태로 제한한다. 이 정의에는 $v_{\mathrm{ext}}$가 없으므로, 같은 운동에너지 연산자와 Coulomb 상호작용을 사용하는 계들은 동일한 $F$를 공유한다. 여기서 보편적이라는 말은 어떤 상대론적 이론이나 다른 입자 상호작용에도 같은 범함수를 사용한다는 뜻이 아니다.[1,2]

외부 potential을 지정한 전자 에너지 범함수는

$$
E_v[n]=F[n]+\int v_{\mathrm{ext}}(\mathbf r)n(\mathbf r)\,d\mathbf r
$$

이며, 정확한 바닥상태 밀도 $n_0$와 전자 에너지 $E_0$는

$$
E_0=E_v[n_0]=\min_{n\to N}E_v[n],
\qquad E_v[n]\ge E_0
$$

를 만족한다. $n\to N$은 단순한 적분값 제약에 더해 앞서 정한 허용 가능한 밀도 영역을 뜻한다. 첫 최소화는 같은 밀도를 만드는 파동함수 사이의 탐색이고, 두 번째는 밀도 자체 사이의 탐색이다. 두 탐색을 합하면 원래 다전자 변분 문제를 얻는다. 이 부등식은 정확한 $F$에 대한 명제이므로, 근사 범함수의 에너지를 정확한 에너지의 상한으로 보장하지 않는다.[1,2]

축퇴가 있으면 하나의 밀도에서 개별 바닥상태 파동함수 하나를 유일하게 복원한다는 표현을 그대로 사용할 수 없다. 에너지 최소화와 ensemble을 통한 정식화를 구분해야 한다. 또한 전자 상태에서 나올 수 있는 밀도인 $N$-representable density와, 어떤 국소 potential의 바닥상태 밀도인 $v$-representable density는 다른 조건이다. 후자의 일의성 정리가 모든 임의의 양함수에 대응 potential의 존재를 보장하지는 않는다.[1,2]

### (3) 밀도에 대한 정상 조건

범함수 미분은 밀도의 작은 변화에 대한 에너지의 일차 응답이다. $\delta n$을 작은 밀도 변화라 하면, 미분 가능한 방향에서

$$
\delta F=\int\frac{\delta F[n]}{\delta n(\mathbf r)}
\delta n(\mathbf r)\,d\mathbf r
$$

로 정의한다. 전자 수 보존 제약을 Lagrange multiplier $\mu$로 부과하면, 정상 밀도에서의 Euler 조건은

$$
\frac{\delta F[n]}{\delta n(\mathbf r)}+v_{\mathrm{ext}}(\mathbf r)=\mu
$$

이다. 각 항의 차원은 에너지이다. 이 식은 입자 수를 유지하며 밀도를 옮겼을 때 더 이상 일차 에너지 이득이 없다는 뜻이다. 그러나 $F$의 구체적인 형태를 모르므로 이 식만으로 계산은 닫히지 않는다. 정수 전자 수를 넘어서는 미분에는 좌우 미분의 차이가 있을 수 있으며, 이 문제는 뒤의 기본 gap 해석에서 다시 다룬다.[1,2]

## 2. Kohn–Sham 보조계와 에너지 분해

KS 구성은 전자 밀도를 재현하는 비상호작용 궤도함수로 운동에너지의 큰 부분을 계산하고, 남은 차이를 XC 에너지에 포함한다. **실제 전자가 서로 상호작용하지 않는다는 근사는 아니다.** 보조계와 실제 계 사이에서 일치시킬 대상은 밀도이며, 파동함수와 각 에너지 성분까지 같게 만드는 것은 아니다.[1–3]

### (1) 비상호작용 운동에너지

밀도 $n$을 재현하는 Slater determinant를 $\Phi$라 하면, determinant로 표현 가능한 범위에서 비상호작용 운동에너지 범함수는

$$
T_s[n]=\min_{\Phi\to n}\langle\Phi|\hat T|\Phi\rangle
$$

이다. 아래에서는 해당 밀도를 비상호작용 바닥상태로 재현하는 KS potential이 존재하는 경우를 다룬다. 단일 determinant로 충분하지 않은 밀도에는 ensemble 일반화가 필요할 수 있으며, HK 정리와 이 비상호작용 표현 가능성은 서로 다른 문제이다.[1,2]

직교 정규화된 공간 궤도함수를 $\phi_i$, 점유수를 $f_i$라 하면

$$
n(\mathbf r)=\sum_i f_i|\phi_i(\mathbf r)|^2,
\qquad \langle\phi_i|\phi_j\rangle=\delta_{ij},
\qquad \sum_i f_i=N
$$

이다. $\delta_{ij}$는 Kronecker delta이다. Spin 비편극 closed-shell의 영온 비축퇴 기준에서는 점유 공간 궤도함수의 $f_i=2$, 비점유 궤도함수의 $f_i=0$이다. Ensemble 또는 분수 점유를 허용하면 공간 궤도함수의 $0\le f_i\le2$를 사용하며, spin별 궤도함수로 바꿀 때에는 상한이 1이다. 이 차이를 놓치면 밀도와 운동에너지에 인자 2의 오류가 생긴다.[1,2,4]

이 궤도함수들로 계산하는 운동에너지는

$$
T_s[n]=\sum_i f_i\int\phi_i^*(\mathbf r)
\left(-\frac12\nabla^2\right)\phi_i(\mathbf r)\,d\mathbf r
$$

이다. 적절한 경계조건 아래에서 이는 양의 기울기 제곱 적분으로도 쓸 수 있다. 궤도함수에 대한 표현은 명시적이지만, 궤도함수 자체가 밀도에 의해 정해지므로 밀도의 범함수라는 지위는 유지된다. 실제 상호작용 파동함수의 운동에너지 $T[n]$와 일반적으로 같지 않다.[1,2]

### (2) Hartree 에너지와 XC 에너지

고전적인 평균 전하분포 사이의 Coulomb 에너지를 Hartree 항으로 분리한다.[1,2]

$$
E_{\mathrm H}[n]=\frac12\iint
\frac{n(\mathbf r)n(\mathbf r')}{|\mathbf r-\mathbf r'|}
\,d\mathbf r\,d\mathbf r'.
$$

계수 $1/2$은 같은 쌍을 두 번 세지 않기 위한 것이다. 그러나 이 식은 전자쌍의 실제 공동 확률을 밀도의 곱으로 치환한 구조이며, 자기 Coulomb 항도 포함한다. 반대칭성과 전자 상관이 만드는 차이는 $E_{\mathrm H}$만으로 표현되지 않는다.[1,2]

XC 에너지는 나머지로 **정의**한다.

$$
E_{\mathrm{xc}}[n]=F[n]-T_s[n]-E_{\mathrm H}[n].
$$

따라서 전자 에너지는 다음과 같이 분해된다.[1–3]

$$
\boxed{E_v[n]=T_s[n]+\int v_{\mathrm{ext}}n\,d\mathbf r
+E_{\mathrm H}[n]+E_{\mathrm{xc}}[n]}.
$$

이는 아직 근사식이 아니다. $W[n]=\langle\Psi[n]|\hat W|\Psi[n]\rangle$를 constrained search의 상호작용 에너지라 하면

$$
E_{\mathrm{xc}}[n]
=\bigl(T[n]-T_s[n]\bigr)+\bigl(W[n]-E_{\mathrm H}[n]\bigr)
$$

이다. 즉 XC는 고전적 Coulomb 에너지의 보정뿐 아니라 상호작용에 따른 운동에너지 차이도 포함한다. 예를 들어 같은 밀도를 실제 다전자 상태와 보조 determinant가 모두 만들더라도, 밀도에 드러나지 않는 전자 사이의 공동 운동은 서로 다를 수 있다. 그 차이를 제외하면 KS 에너지 분해는 더 이상 정확하지 않다.[1,2]

### (3) Hartree–Fock과의 관계

Hartree–Fock (HF)은 실제 Hamiltonian의 기대값을 단일 determinant 공간에서 최소화한다. KS-DFT는 밀도와 $T_s$를 얻는 데 determinant를 사용하지만, 에너지는 XC 범함수를 포함한 식으로 계산한다. 정확한 XC를 사용한 KS 에너지를 보조 determinant에 대한 $\langle\Phi|\hat H|\Phi\rangle$와 동일시하면 correlation을 누락한다.[1,2,4]

두 방법의 변분 대상과 교환 처리를 비교하면 다음과 같다.[1,2,4]

| 구분 | HF | KS-DFT |
| --- | --- | --- |
| 최소화하는 에너지 | 실제 Hamiltonian의 determinant 기대값 | $T_s+V_{\mathrm{ext}}+E_{\mathrm H}+E_{\mathrm{xc}}$ |
| 궤도함수의 역할 | 근사 다전자 파동함수 구성 | 보조계의 밀도와 운동에너지 구성 |
| 교환 처리 | 비국소 Fock exchange | 선택한 XC에 따름; 보통의 KS는 곱셈 potential |
| 상관 처리 | 단일 determinant 밖의 correlation 누락 | 정확한 XC에는 포함, 실제 계산에서는 근사 |
| 정확한 에너지의 상한 | 변분 원리로 보장 | 근사 XC에는 일반적 보장 없음 |

Exact exchange도 어느 궤도함수로 계산했는지 구분해야 한다. KS exchange는 KS determinant에서 얻는 Fock 형태의 에너지이고, HF exchange는 HF 궤도함수에서 얻는다. 국소 곱셈 potential에 제약된 exchange-only KS 계산은 일반적인 비국소 HF 계산과 같은 변분 문제가 아니다. 따라서 DFT의 correlation energy를 무조건 $E_0-E_{\mathrm{HF}}$로 정의할 수는 없다.[1,2]

## 3. Kohn–Sham 방정식과 총에너지

KS 방정식은 밀도 변분의 정상 조건을 비상호작용 전자의 고유값 문제로 구현한다. 보통의 KS에서 모든 궤도함수는 같은 국소 유효 potential을 느끼며, 그 potential이 다시 밀도에 의존하므로 전체 문제는 비선형이다.[1,2]

### (1) 유효 potential과 궤도함수

Hartree 항의 범함수 미분은

$$
v_{\mathrm H}[n]\,(\mathbf r)=\frac{\delta E_{\mathrm H}}{\delta n(\mathbf r)}
=\int\frac{n(\mathbf r')}{|\mathbf r-\mathbf r'|}\,d\mathbf r'
$$

이다. 밀도의 곱에서 두 대칭적인 변분 항이 나오므로 에너지의 $1/2$이 potential에는 남지 않는다. XC potential은

$$
v_{\mathrm{xc}}[n]\,(\mathbf r)=\frac{\delta E_{\mathrm{xc}}[n]}{\delta n(\mathbf r)}
$$

로 정의하며, KS potential은

$$
v_s(\mathbf r)=v_{\mathrm{ext}}(\mathbf r)
+v_{\mathrm H}[n]\,(\mathbf r)+v_{\mathrm{xc}}[n]\,(\mathbf r)
$$

이다. 이 세 potential은 모두 전자 한 개의 에너지 차원을 갖는다. $v_{\mathrm{xc}}$는 위치에서 곱하는 국소 potential이지만, 그 위치의 값이 밀도 전체에 의존할 수 있다. 연산자가 국소적이라는 것과 범함수가 한 점의 밀도에만 의존한다는 것은 다른 뜻이다.[1,2]

직교 제약 아래 궤도함수를 변분하고 Lagrange multiplier 행렬을 대각화하면

$$
\boxed{\left[-\frac12\nabla^2+v_s(\mathbf r)\right]\phi_i(\mathbf r)
=\epsilon_i\phi_i(\mathbf r)}
$$

를 얻는다. $\epsilon_i$는 KS 궤도 에너지이다. 주어진 $v_s$에 대해서는 선형 방정식이지만, 해로 만든 $n$이 다시 $v_s$를 바꾸므로 한 번의 대각화로는 풀리지 않는다. 정확한 XC와 적절한 표현 가능성 아래에서 자기일관적인 바닥상태 해는 실제 밀도를 재현하며, 근사 XC를 사용하면 그 근사 에너지의 정상 해를 구한다.[1,2,4]

### (2) 고윳값 합의 보정

점유 궤도함수에 KS 방정식을 곱해 적분하고 점유수를 합하면

$$
\sum_i f_i\epsilon_i
=T_s+\int v_{\mathrm{ext}}n\,d\mathbf r
+2E_{\mathrm H}+\int v_{\mathrm{xc}}n\,d\mathbf r
$$

를 얻는다. Hartree potential의 밀도 적분은 $2E_{\mathrm H}$이고, XC potential의 밀도 적분은 일반적으로 $E_{\mathrm{xc}}$와 같지 않다. 따라서 고윳값의 합에 잘못 포함된 항을 빼고 에너지 범함수의 값을 넣어야 한다.[1,5]

$$
\boxed{E_v[n]=\sum_i f_i\epsilon_i-E_{\mathrm H}[n]
-\int n(\mathbf r)v_{\mathrm{xc}}(\mathbf r)\,d\mathbf r
+E_{\mathrm{xc}}[n]}.
$$

이 식은 같은 자기일관 밀도와 국소 KS potential을 사용한 에너지 재구성식이다. 핵을 포함한 총에너지는 $E_{\mathrm{tot}}=E_v+E_{\mathrm{NN}}$이다. 비국소 exchange 연산자가 들어가는 hybrid에서는 해당 연산자의 기대값까지 반영해야 하므로 이 국소 식을 그대로 전용하지 않는다.[1,4,5]

예를 들어 두 구조의 안정성을 비교할 때 점유 $\epsilon_i$ 합만 비교하면 Hartree와 XC의 보정, 핵 반발을 빠뜨린다. 이 문제는 두 계산을 똑같이 수렴시켜도 없어지지 않는다. 비교할 대상은 선택한 근사와 Hamiltonian에 맞게 계산한 총에너지이며, 궤도 에너지의 개별 이동은 별도의 전자 상태 분석 자료이다.[1,2,5]

## 4. 교환·상관 근사

실용적인 XC 근사는 어떤 정보를 사용하여 $E_{\mathrm{xc}}$를 구성하는지에 따라 구분한다. 밀도만 사용하는 local density approximation (LDA), 밀도 기울기를 더하는 generalized gradient approximation (GGA), 궤도함수 정보까지 사용하는 근사로 확장된다. 더 많은 정보를 사용한다는 사실만으로 모든 물성에서 오차가 단조롭게 줄어드는 것은 아니며, 비교 대상과 조건에 맞는 검증이 필요하다.[1,4]

### (1) LDA와 균일 전자기체

LDA는 각 공간점의 밀도를 같은 밀도의 균일 전자기체에 대응시킨다. $\varepsilon_{\mathrm{xc}}^{\mathrm{unif}}(n)$를 균일 전자기체의 전자 한 개당 XC 에너지라 하면

$$
E_{\mathrm{xc}}^{\mathrm{LDA}}[n]
=\int n(\mathbf r)\varepsilon_{\mathrm{xc}}^{\mathrm{unif}}(n(\mathbf r))\,d\mathbf r
$$

이다. 균일 전자기체에는 전체 전하를 중화하는 배경이 있으며, 실제 비균일 밀도에서는 이 대응이 근사이다. 균일계의 상호작용 정보를 사용하는 것이므로 LDA가 electron correlation을 전혀 포함하지 않는다는 해석은 잘못이다. KS의 궤도함수 운동에너지 $T_s$를 위와 같은 국소 밀도식으로 대체하는 것도 아니다.[1–3]

3차원 spin 비편극 밀도에 대한 LDA exchange는

$$
E_{\mathrm x}^{\mathrm{LDA}}[n]
=-\frac34\left(\frac3\pi\right)^{1/3}\int n(\mathbf r)^{4/3}\,d\mathbf r
$$

이다. 이는 균일 전자기체의 Fock exchange로 계수를 정한 식이며, 음의 부호는 고전적인 Hartree 쌍 에너지에 대한 exchange 감소분을 나타낸다. Correlation 부분은 별도의 균일 전자기체 에너지 자료와 그 매개화가 필요하다.[1,2,4]

LDA potential을 만들 때에는 밀도 인자도 미분한다.

$$
v_{\mathrm{xc}}^{\mathrm{LDA}}(\mathbf r)
=\left[\varepsilon_{\mathrm{xc}}^{\mathrm{unif}}(n)
+n\frac{d\varepsilon_{\mathrm{xc}}^{\mathrm{unif}}(n)}{dn}\right]_{n=n(\mathbf r)}.
$$

따라서 전자 한 개당 에너지 $\varepsilon_{\mathrm{xc}}$를 그대로 potential로 넣으면 안 된다. 문헌이 단위 부피당 에너지 $e_{\mathrm{xc}}=n\varepsilon_{\mathrm{xc}}$를 사용하면 potential은 $de_{\mathrm{xc}}/dn$이다. 두 표기는 동등하지만 밀도 인자의 위치를 확인해야 한다. 이 구분은 계산 코드의 XC 에너지와 미분값을 읽을 때에도 필요하다.[1,2,4]

### (2) GGA와 밀도 기울기

GGA는 밀도 변화에 대한 정보를 포함하기 위해, 단위 부피당 에너지 함수 $g$를 사용하여

$$
E_{\mathrm{xc}}^{\mathrm{GGA}}[n]
=\int g(n(\mathbf r),\nabla n(\mathbf r))\,d\mathbf r
$$

로 쓴다. 이때 $g$는 구체적으로 선택한 근사의 함수이며, 기울기 의존성을 포함한다는 형식만으로 정해지지 않는다. GGA는 밀도가 완만하게 변한다는 전제의 낮은 차수 gradient expansion과 동일한 개념이 아니다. 정확한 제약을 만족시키거나 특정 계의 성질을 재현하도록 더 일반적인 함수 형태를 사용할 수 있다.[1,4]

경계에서 변분의 표면항이 사라지는 조건 아래 부분적분하면

$$
v_{\mathrm{xc}}^{\mathrm{GGA}}
=\frac{\partial g}{\partial n}
-\nabla\cdot\frac{\partial g}{\partial(\nabla n)}
$$

를 얻는다. 둘째 항은 밀도 기울기의 변화가 주변 공간의 에너지에 미치는 영향을 모은 것이다. $\partial g/\partial n$만 사용하면 원래 GGA 에너지의 정상 조건을 풀지 않게 된다. 기울기를 포함해도 이 형태의 KS potential은 여전히 궤도함수에 곱하는 함수이다.[1,4]

### (3) Meta-GGA와 hybrid

Meta-GGA는 밀도와 기울기 외에 kinetic-energy density $\tau$ 또는 밀도의 Laplacian 같은 정보를 사용한다. 이 문서의 양의 운동에너지 밀도 규약은

$$
\tau(\mathbf r)=\frac12\sum_i f_i|\nabla\phi_i(\mathbf r)|^2
$$

이다. 적절한 경계조건에서 $\int\tau\,d\mathbf r=T_s$이며, 원자단위계로 쓴 $\tau$는 에너지/부피에 해당한다. 문헌에 따라 $1/2$을 생략한 양을 같은 기호로 부르므로 식을 옮길 때 규약을 맞춰야 한다. $\tau$ 의존성은 궤도함수를 통해 들어오므로, 이를 직접 궤도함수 변분하면 단순한 곱셈 XC potential보다 일반적인 연산자가 나타난다.[1,4]

Hybrid는 비국소 Fock 형태의 exchange를 밀도 기반 근사와 혼합한다. 한 가지 단순한 global hybrid의 구조는

$$
E_{\mathrm{xc}}^{\mathrm{hyb}}
=aE_{\mathrm x}^{\mathrm{Fock}}+(1-a)E_{\mathrm x}^{\mathrm{GGA}}
+E_{\mathrm c}^{\mathrm{GGA}}
$$

이다. $a$는 선택한 근사가 정하는 무차원 혼합 비율이다. $E_{\mathrm x}^{\mathrm{Fock}}$는 현재 최적화하는 궤도함수로 평가하며, 별도의 HF 계산 에너지를 단순히 더한다는 뜻은 아니다. 위 식은 global hybrid의 예시 형식으로, 모든 hybrid의 정의가 아니다. 전자 간 거리 구간에 따라 exchange를 다르게 혼합하는 range-separated hybrid도 있다.[1,4]

비국소 exchange를 직접 포함하는 궤도함수 방정식은 generalized Kohn–Sham (GKS) 틀로 구분한다. 보통의 국소 KS와 GKS는 사용하는 유효 연산자의 범위가 다르므로, 고윳값과 gap을 해석할 때 어느 틀의 결과인지 명시해야 한다. Hybrid를 사용했다는 사실만으로 correlation과 장거리 상호작용이 모두 정확해지는 것은 아니다.[1,4]

근사별 입력 정보와 확인할 한계를 정리하면 다음과 같다.[1,4]

| 근사 | 사용하는 정보 | 필요한 해석상의 구분 |
| --- | --- | --- |
| LDA | 한 점의 밀도 | 균일 전자기체 에너지와 실제 비균일계의 차이 |
| GGA | 밀도와 그 기울기 | 기울기 의존성과 체계적인 gradient expansion의 차이 |
| Meta-GGA | 밀도·기울기와 $\tau$ 등 | 궤도 의존성과 운동에너지 밀도 규약 |
| Hybrid | 밀도 기반 성분과 Fock exchange | 비국소 연산자, 혼합 비율과 거리 분리 여부 |

### (4) Spin 분극

Collinear spin 계산에서는 $\sigma=\uparrow,\downarrow$에 대한 밀도를 별도 변수로 사용한다.

$$
n_\sigma(\mathbf r)=\sum_i f_{i\sigma}|\phi_{i\sigma}(\mathbf r)|^2,
\qquad n=n_\uparrow+n_\downarrow,
\qquad 0\le f_{i\sigma}\le1.
$$

XC 에너지는 $E_{\mathrm{xc}}[n_\uparrow,n_\downarrow]$가 되고, spin별 XC potential은

$$
v_{\mathrm{xc},\sigma}(\mathbf r)
=\frac{\delta E_{\mathrm{xc}}[n_\uparrow,n_\downarrow]}{\delta n_\sigma(\mathbf r)}
$$

이다. Hartree potential은 전체 밀도로 구성하지만 XC potential과 궤도함수는 spin별로 달라질 수 있다. 비편극 밀도만 허용하는 계산은 spin 분극 해를 탐색할 수 없으므로, 초기 spin과 허용한 대칭성은 계산 모형의 일부이다. 여기서는 spin–orbit coupling과 궤도 자기장 결합을 제외하며, 공간에 따라 spin 방향이 달라지는 경우에는 비공선 일반화가 필요하다.[1,2,4]

## 5. 자기일관 계산과 수렴

Self-consistent field (SCF) 계산은 입력 밀도로 구성한 KS 연산자의 점유 고유함수들이 다시 같은 밀도를 만드는 고정점을 찾는다. SCF 반복의 수렴, 기저와 적분의 수렴, XC 근사의 정확도는 각각 다른 문제이다.[1,4]

### (1) 유한 기저와 SCF 순환

비직교 기저 $\{\chi_\mu\}$에 궤도함수를 전개하면 $\phi_i=\sum_\mu C_{\mu i}\chi_\mu$이다. $\mathbf C$를 전개 계수 행렬, $S_{\mu\nu}=\langle\chi_\mu|\chi_\nu\rangle$를 overlap 행렬, $H^s_{\mu\nu}=\langle\chi_\mu|\hat h_s|\chi_\nu\rangle$를 KS 행렬로 정의하면

$$
\mathbf H_s[n]\mathbf C=\mathbf S\mathbf C\boldsymbol\epsilon,
\qquad \mathbf C^\dagger\mathbf S\mathbf C=\mathbf I
$$

를 푼다. $\hat h_s=-\nabla^2/2+v_s$, $\boldsymbol\epsilon$은 고윳값 대각행렬, $\mathbf I$는 단위행렬이며 $\dagger$는 Hermitian conjugate이다. 행렬의 겉모양은 HF와 같지만 밀도에서 연산자를 구성하는 방법이 다르다. 기저의 선형 종속성이 강하면 overlap 처리도 수치 안정성에 영향을 준다.[1,4]

기본 순환은 다음과 같다.[1,4]

1. 핵 배치, 전자 수, spin 제약, 경계조건, 기저와 XC 근사를 지정한다.
2. 초기 밀도로 $v_{\mathrm H}$와 $v_{\mathrm{xc}}$를 구성한다.
3. KS 방정식을 풀고 지정한 전자 수에 맞게 점유수를 결정한다.
4. 점유 궤도함수에서 출력 밀도와 에너지를 계산한다.
5. 입력·출력 밀도의 차이를 점검하고 갱신한 밀도로 반복한다.

반복 번호를 $k$, 입력·출력 밀도를 $n_{\mathrm{in}}^{(k)}$, $n_{\mathrm{out}}^{(k)}$라 하면 가장 단순한 linear mixing은

$$
n_{\mathrm{in}}^{(k+1)}=(1-\alpha)n_{\mathrm{in}}^{(k)}
+\alpha n_{\mathrm{out}}^{(k)},\qquad 0<\alpha\le1
$$

이다. $\alpha$는 새 출력에 주는 가중치이다. 작게 잡으면 갱신을 완화하지만 모든 문제의 수렴을 보장하지는 않는다. 더 정교한 mixing과 수렴 가속도 고정점 탐색을 돕는 수치 방법이며, 선택한 XC 범함수를 물리적으로 더 정확하게 만드는 보정은 아니다.[1,4]

### (2) 반복 수렴과 계산 조건

!!! info "[Measurement]"
    SCF 반복에서는 에너지 변화와 밀도 잔차를 함께 기록한다. 예를 들어 이 문서에서는 전자 수로 정규화한 잔차를

    $$
    \eta_n^{(k)}=\frac1N\int
    |n_{\mathrm{out}}^{(k)}-n_{\mathrm{in}}^{(k)}|\,d\mathbf r,
    \qquad \Delta E^{(k)}=E^{(k)}-E^{(k-1)}
    $$

    로 정의한다. $\eta_n$은 무차원이며 $\Delta E$는 에너지이다. 이는 밀도와 에너지 수렴을 함께 확인하라는 원칙을 구현한 지표 선택이고, 특정 프로그램의 기본 잔차 정의는 아니다. 실제 보고에는 프로그램이 사용하는 norm과 정규화, 허용 오차, 최대 반복 횟수 및 사용한 에너지의 정의를 남긴다.[1,4]

에너지 변화가 작아도 밀도나 궤도함수가 충분히 자기일관적이지 않을 수 있다. 반대로 SCF 잔차가 작아도 다른 초기 상태에서 더 낮은 에너지 해가 나올 수 있다. 정상점의 안정성은 궤도 회전에 대한 에너지의 이차 변화 등으로 별도 판단하며, 단일 초기값의 수렴을 전역 바닥상태의 증명으로 보지 않는다.[1,4]

유한 기저는 궤도함수를 표현하는 자유도를 제한하고, 수치 적분은 XC 에너지와 행렬 구성에 별도 오차를 만든다. 따라서 SCF 허용 오차를 더 작게 만드는 것만으로 기저나 적분 오차를 줄일 수 없다. 필요한 정확도는 연구 대상의 에너지 차이나 물성 변화에 맞춰 정하고, 동일한 계산 조건에서 설정을 체계적으로 강화해 확인한다.[1,4]

계산 기록에서는 다음 구분을 유지한다.[1,4]

| 점검 대상 | 바꾸거나 비교할 조건 | 확인하는 문제 |
| --- | --- | --- |
| 반복 수렴 | 에너지·밀도 잔차의 허용 오차 | 같은 설정에서의 자기일관성 |
| 공간 표현 | 기저 크기와 수치 적분 격자 | 궤도함수와 에너지 적분의 수치 오차 |
| 전자 상태 | 초기 밀도, spin과 점유 제약 | 다른 정상 해 또는 대칭성에 대한 민감도 |
| 물리 근사 | XC와 명시적인 추가 보정 | 수렴 이후에도 남는 모형 의존성 |

## 6. 결과의 물리적 의미와 한계

DFT 결과는 총에너지·밀도와 보조계의 고윳값을 구분하여 해석해야 한다. 정확한 바닥상태 이론이라는 사실만으로 KS의 모든 고윳값 차이가 실제 전자 제거·추가 또는 광학 여기 에너지가 되는 것은 아니다. 근사 XC의 오차와, 서로 다른 물리량을 비교한 데서 생기는 차이도 나누어야 한다.[1,2,5]

### (1) 전자 추가·제거와 기본 gap

고정한 핵 배치의 유한계에서 $E_0(M)$을 $M$전자 바닥상태 에너지라 하자. 필요한 전하 상태가 결합된 상태로 존재하는 범위에서 수직 ionization energy $I$와 electron affinity $A$는

$$
I=E_0(N-1)-E_0(N),
\qquad A=E_0(N)-E_0(N+1)
$$

이다. 핵을 고정하지만 각 전자 수에서는 전자 상태를 각각 최적화한다. 따라서 이 정의는 궤도함수를 동결한 전자 제거와 다르다. 유한계의 정확한 KS potential을 무한원에서 0으로 정하면 최고 점유 궤도 에너지는 $\epsilon_{\mathrm H}=-I$를 만족한다. 이 관계를 근사 XC의 고윳값에도 정확한 등식으로 적용할 수는 없다.[1,2,5]

Fundamental gap은 전자 추가·제거 에너지의 차이로 정의한다.[1,5]

$$
E_g=I-A=E_0(N+1)+E_0(N-1)-2E_0(N).
$$

한편 같은 $N$전자 KS potential의 최고 점유와 최저 비점유 고윳값을 각각 $\epsilon_{\mathrm H}$, $\epsilon_{\mathrm L}$라 하면, 보통의 정확한 국소 KS에서는

$$
\boxed{E_g=(\epsilon_{\mathrm L}-\epsilon_{\mathrm H})+\Delta_{\mathrm{xc}}}
$$

이다. $\Delta_{\mathrm{xc}}$는 정수 전자 수를 통과할 때 XC potential의 범함수 미분이 갖는 상수 도약인 derivative discontinuity이다. 이 식은 정확한 KS gap조차 일반적으로 기본 gap과 같지 않은 이유를 보여 준다. 실제 LDA·GGA 계산에서는 이 차이와 함께 근사 potential 자체의 오차도 고려해야 한다.[1,5]

전자 수를 연속적으로 다루기 위해서는 분수 전자를 가진 순수 파동함수를 가정하지 않고, 서로 다른 전자 수 상태의 ensemble을 사용한다. 인접 정수 상태가 에너지의 아래쪽 convex hull을 이루는 경우, $0\le\omega\le1$에 대해

$$
E_0(N+\omega)=(1-\omega)E_0(N)+\omega E_0(N+1)
$$

이다. $\omega$는 두 정수 상태 사이의 혼합 가중치이다. 이 구간별 선형성 때문에 정수점에서 왼쪽 기울기는 $-I$, 오른쪽 기울기는 $-A$가 되어 차이가 $E_g$이다. 미분이 매끄러운 밀도 근사로 이 구조를 그대로 재현할 수 있다고 가정하면 전하 이동과 gap 해석에 문제가 생긴다.[2,5,6]

전자 수를 바꾸지 않는 중성 여기와 전자 추가·제거는 다른 과정이다. 따라서 광학 흡수 에너지를 위의 총에너지 차나 KS gap과 곧바로 동일시하지 않는다. 또한 hybrid의 GKS gap에 국소 KS에서 정의한 $\Delta_{\mathrm{xc}}$를 그대로 덧붙이는 것도 정당화되지 않는다. Quasiparticle 관점의 후속 전개는 [GW approximation](../many-body-perturbation/gw-approximation.md)으로 연결한다.[1,4,5]

### (2) 자기상호작용과 상관의 누락

전자 한 개에는 실제 전자–전자 반발이 없지만, 그 밀도로 계산한 $E_{\mathrm H}$는 0이 아니다. 따라서 정확한 XC는 이를 상쇄해야 한다. $n_1$을 한 전자 밀도라 하면

$$
E_{\mathrm x}[n_1]=-E_{\mathrm H}[n_1],
\qquad E_{\mathrm c}[n_1]=0
$$

이다. 흔히 사용하는 국소·반국소 근사가 이 조건을 일반적으로 만족하지 못하는 것이 self-interaction error의 기본 예이다. 이는 정확한 DFT의 한계가 아니라 범함수 근사의 문제이다. 국소화된 전자 상태와 전하 이동을 다룰 때에는 이러한 오차가 관련되는지 검토해야 한다.[1,2,4]

여러 전자배치가 중요해지는 계에서는 익숙한 XC 근사가 필요한 correlation을 충분히 나타내지 못할 수 있다. KS 보조계가 determinant라는 이유만으로 정확한 DFT에 HF와 동일한 단일 determinant 오차가 필연적으로 생긴다고 주장해서는 안 된다. 정확한 이론의 가능성과 실제 사용한 근사의 성능을 분리하는 것이 핵심이다.[1,2]

### (3) 장거리 상호작용과 검증 범위

일반적인 LDA·GGA의 국소·반국소 정보만으로는 멀리 떨어진 부분계 사이의 올바른 장거리 dispersion을 재현하기 어렵다. 이를 다루기 위해 비국소 correlation 또는 별도의 dispersion 보정을 사용할 수 있다. 평형 거리 근처에서 결합 에너지가 우연히 비슷하게 나오는 것과, 장거리 점근 거동을 재현하는 것은 서로 다른 검증이다.[1,4]

결과를 보고할 때에는 최소한 전자 수와 spin, 핵 구조, XC의 정확한 이름, 기저 및 경계조건, 수렴 기준과 추가 보정의 사용 여부를 명시한다. 특정 계에서 얻은 좋은 에너지 차이를 모든 구조·전하·spin 상태에서의 보편적 정확도로 확장하지 않는다. 오차 검토의 기준은 연구에서 실제로 비교하려는 물리량이어야 한다.[1,4]

## 7. 요약

- 밀도 변분은 내부 에너지의 constrained search와 외부 potential 에너지를 결합한다. 정확한 범함수의 변분 원리와 근사 범함수의 정확도는 구분한다.[1,2]
- KS 보조계는 실제 밀도를 재현하도록 구성하며, XC에는 상호작용 에너지뿐 아니라 $T-T_s$도 포함된다.[1,2]
- KS 방정식은 자기일관적으로 풀어야 한다. 총에너지는 고윳값 합에 Hartree·XC 보정과 핵 반발을 반영하여 구한다.[1,4,5]
- LDA, GGA, meta-GGA와 hybrid는 사용하는 정보와 연산자의 범위가 다르며, spin과 점유수 규약도 함께 확인한다.[1,4]
- SCF 수렴, 수치 표현의 수렴과 물리 근사의 검증을 분리하고, KS gap·기본 gap·중성 여기 에너지를 구별한다.[1,4,5]

## 8. 참고문헌

1. K. Capelle, “A Bird's-Eye View of Density-Functional Theory,” *Brazilian Journal of Physics* **36**, 1318–1343 (2006). [DOI: 10.1590/S0103-97332006000700035](https://doi.org/10.1590/S0103-97332006000700035), [Author manuscript](https://arxiv.org/abs/cond-mat/0211443). §§2–5와 §6의 spin 일반화를 참조한다.
2. K. Burke and friends, *The ABC of DFT* (2007). [Author-hosted text](https://dft.uci.edu/doc/g1.pdf). Chapters 6–9와 14의 밀도 변분, KS 구성, LDA, spin 및 discontinuity 설명을 참조한다.
3. W. Kohn and L. J. Sham, “Self-Consistent Equations Including Exchange and Correlation Effects,” *Physical Review* **140**, A1133–A1138 (1965). [DOI: 10.1103/PhysRev.140.A1133](https://doi.org/10.1103/PhysRev.140.A1133), [Publisher full text](https://harvest.aps.org/v2/journals/articles/10.1103/PhysRev.140.A1133/fulltext). §II.A의 에너지 분해와 국소 근사를 참조한다.
4. S. Lehtola, F. Blockhuys, and C. Van Alsenoy, “An Overview of Self-Consistent Field Calculations Within Finite Basis Sets,” *Molecules* **25**, 1218 (2020). [DOI: 10.3390/molecules25051218](https://doi.org/10.3390/molecules25051218), [Author manuscript](https://arxiv.org/html/1912.12029v2). §§II–XI의 기저 전개, 변분, 안정성과 XC 기여를 참조한다.
5. J. P. Perdew and M. Levy, “Physical Content of the Exact Kohn-Sham Orbital Energies: Band Gaps and Derivative Discontinuities,” *Physical Review Letters* **51**, 1884–1887 (1983). [DOI: 10.1103/PhysRevLett.51.1884](https://doi.org/10.1103/PhysRevLett.51.1884), [Publisher full text](https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevLett.51.1884/fulltext). Eqs. (2)–(10)의 총에너지와 gap 관계를 참조한다.
6. J. P. Perdew, R. G. Parr, M. Levy, and J. L. Balduz, Jr., “Density-Functional Theory for Fractional Particle Number: Derivative Discontinuities of the Energy,” *Physical Review Letters* **49**, 1691–1694 (1982). [DOI: 10.1103/PhysRevLett.49.1691](https://doi.org/10.1103/PhysRevLett.49.1691), [Publisher full text](https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevLett.49.1691/fulltext). Eq. (5)와 그 적용 조건인 정수 에너지의 convexity를 참조한다.
