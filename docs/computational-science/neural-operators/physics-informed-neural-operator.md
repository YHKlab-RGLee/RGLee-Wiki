---
description: PINO의 함수군별 물리 제약, 데이터와 잔차의 해상도 분리, Fourier 미분과 정규화, 경계 조건 및 일반화 평가를 설명한다.
---

# Physics-informed neural operator

Physics-informed neural operator (PINO)는 **입력 함수에서 해 함수로 가는 연산자를 학습하면서, 예측한 해가 지배 방정식을 얼마나 만족하는지도 학습 목적에 포함하는 방법**이다. 정답 해와 예측 해의 차이를 측정하는 data loss에 지배 방정식의 residual을 측정하는 physics loss를 결합하거나, 정답 해 없이 물리 제약만으로 모형을 학습할 수 있다. 원 PINO는 Fourier neural operator (FNO)를 바탕으로 제안되었으며, 독립 후속 연구에서도 같은 FNO에 데이터와 물리 제약을 조합하여 학습한다.[1,2]

이 문서는 알려진 partial differential equation (PDE)의 해 연산자를 근사하는 순방향 문제를 다룬다. 원 PINO의 FNO 기반 구현을 중심으로 설명하되, 물리 제약을 연산자 학습에 쓰는 원리와 특정 network 구조를 구분한다. Fourier 층 자체는 [FNO의 기본 구조](fourier-neural-operator.md#1-fno)를, branch–trunk 방식의 대안은 [Physics-informed DeepONet](deeponet.md#6-physics-informed-deeponet)을 참고한다. 아래에서는 입력장을 $a$, 해를 $u$, 학습 매개변수를 $\theta$로 통일한다.

## 1. 함수군에 대한 물리 제약

PINO는 특정 초기 조건 하나의 해만 계산하는 대신, 초기 조건이나 PDE의 계수·외력이 달라질 때 각각의 입력에 대응하는 해가 어떻게 변하는지를 나타내는 연산자를 근사한다. 방정식과 경계 조건이 정해져 있고 허용 입력마다 유일한 해가 존재한다고 가정하여, 입력 함수 공간 $\mathcal A$에서 해 공간 $\mathcal U$로 가는 연산자를 정의한다.[1,3]

$$
\mathcal G:\mathcal A\to\mathcal U,
\qquad a\mapsto u=\mathcal G[a].
$$

Network의 예측은 $u_\theta[a]=\mathcal G_\theta[a]$이다. 예를 들어 열전도 문제에서 $a$를 초기 온도 분포로 정하면 출력은 이후 시공간 온도장이다. 입력을 열전도 계수로 정하는 경우에는 다른 해 연산자가 된다. 무엇을 입력에 포함하고 무엇을 고정하는지 명시해야 “새로운 문제를 푼다”는 표현의 범위가 정해진다.[1,3]

### (1) 방정식 잔차의 연산자화

공간 영역을 $D$, 시간 구간을 $[0,T]$, 시공간 영역을 $\Omega=D\times(0,T)$라 하자. $\mathcal P_a$는 입력 $a$에 의존하는 PDE 연산자이며, 내부 방정식은 $\mathcal P_a[u]=0$이다. 예측 해를 대입하여 만든 내부 잔차는 다음과 같다.[1,3]

$$
r_\theta[a](x,t)
=\mathcal P_a[\mathcal G_\theta[a]](x,t).
$$

PDE residual은 예측값과 정답값 사이의 오차가 아니다. 예측장을 지배 방정식에 대입했을 때 그 방정식을 얼마나 만족하지 못하는지를 나타내는 값이다. 이를 해 오차와 연결하려면 방정식의 안정성과 초기·경계 조건이 추가로 필요하다. 따라서 정답 해가 없는 경우에도 잔차를 계산할 수 있지만, 그 값 하나로 해 정확도를 확정할 수는 없다.[1,4]

입력 함수의 분포를 확률측도 $\mu$로 나타내자. 한 입력의 잔차 norm을 최소화하는 대신 입력 분포 전체에서 평균한 loss를 사용하면 물리 제약이 연산자 학습의 목적이 된다. $\|\cdot\|_{\Omega,\mathrm{av}}$는 영역 평균을 사용하는 norm이며 다음 절에서 정의한다.[1,3]

$$
\mathcal J_r(\theta)
=\mathbb E_{a\sim\mu}
\left[\|r_\theta[a]\|_{\Omega,\mathrm{av}}^2\right].
$$

이 식에는 함수 표본 $a$와 공간·시간 좌표라는 두 종류의 변수가 있다. 잔차 평가점만 늘리면 특정 입력 함수에 대한 예측 해가 방정식을 만족하는지 더 촘촘히 검사하게 된다. 반면 입력 함수의 수를 늘리면 동일한 network 매개변수가 더 다양한 입력 조건에서도 방정식을 만족하도록 학습해야 한다.[3,5]

### (2) PINN 및 DeepONet과의 관계

기본적인 physics-informed neural network (PINN)는 하나의 고정된 문제에서 좌표 $(x,t)$를 입력받아 해 $u_\theta(x,t)$를 나타낸다. 입력 함수가 달라지는 연산자 학습에서는 $a$도 모형의 입력이며 여러 $a$에 대해 매개변수를 공유한다. 이 구분은 기본 설정에 대한 것이므로, 매개변수 입력이나 연산자 구조를 추가한 모든 확장 PINN까지 단일 문제에 한정한다는 뜻은 아니다.[1,3,5]

| 방법 | 학습으로 정하는 대상 | 물리 제약의 평가 범위 |
| --- | --- | --- |
| 기본 PINN | 고정된 문제의 해 함수 | 그 문제의 좌표 집합 |
| 지도 학습 FNO | 입력 함수에서 해로 가는 대응 | 기본 data loss에는 잔차 항 없음 |
| FNO 기반 PINO | 같은 종류의 함수 간 대응 | 여러 입력 함수와 좌표 |
| Physics-informed DeepONet | Branch–trunk로 표현한 대응 | 여러 입력 함수와 trunk 좌표 |

Physics-informed DeepONet도 함수군에 걸쳐 PDE 제약을 적용한다. 두 방법을 구별하는 핵심은 물리 제약의 유무가 아니라, 예측 해를 어떤 network 구조로 표현하고 그 해의 좌표 미분을 어떻게 계산하는지에 있다. DeepONet은 고정된 입력 표본을 처리하는 branch와 좌표를 처리하는 trunk를 결합하므로 trunk의 좌표 미분을 사용할 수 있다. 격자 배열을 출력하는 FNO에서는 어떤 연속 표현이나 수치 미분을 사용할지 별도로 정해야 한다. 독립 분석도 두 구조의 physics-informed 근사를 함께 다루며, 둘 사이의 보편적 성능 순서를 보장하지 않는다.[3,5]

## 2. 복합 목적 함수와 표본화

물리 제약은 내부 PDE뿐 아니라 문제를 식별하는 초기·경계 조건을 포함해야 한다. 여기에 정답 해가 있으면 data loss를 더한다. 각 항의 단위와 적분 영역이 다르므로, 먼저 항별 의미를 정하고 정규화한 뒤 가중치를 선택한다.[1,3]

### (1) 내부·초기·경계 잔차

입력 $a$에 대응하는 초기 함수를 $u_{0,a}$, 경계 조건 연산자를 $\mathcal B_a$, 경계 자료를 $g_a$라 하자. 초기 잔차 $i_\theta$와 경계 잔차 $b_\theta$를 다음처럼 정의한다. $\Gamma=\partial D\times(0,T)$는 시공간 경계이다.[1,3]

$$
i_\theta[a](x)=u_\theta[a](x,0)-u_{0,a}(x),
\qquad
b_\theta[a]=\mathcal B_a[u_\theta[a]]-g_a.
$$

Dirichlet 조건에서는 $\mathcal B_a$가 경계에서의 값이고, Neumann 조건에서는 법선 방향 미분 또는 문제에서 정의한 flux이다. 따라서 두 경우의 $b_\theta$는 단위도 다를 수 있다. 시간에 무관한 정상 문제에서는 초기 잔차 항을 사용하지 않는다. 경계와 내부의 잔차를 하나의 배열에 합쳐 동일하게 평균하면 표면과 체적에서 각각 정의한 적분의 의미를 구분할 수 없다. 따라서 두 residual loss는 별도로 정의한다.[1,4]

유한한 양의 측도 $|A|$를 가진 영역 $A$에 대해 이 문서의 평균제곱 norm은 다음과 같다. 벡터장의 절댓값은 성분의 Euclidean norm이며, 경계에서는 체적 대신 표면 측도를 쓴다.[1,4]

$$
\|v\|_{A,\mathrm{av}}^2
=\frac{1}{|A|}\int_A |v(z)|^2\,dz.
$$

평균 norm을 쓰면 단위는 $v$의 단위와 같다. 반면 적분 자체를 norm 제곱으로 쓰는 규약은 영역 크기의 인자를 포함한다. 아래 식은 원문의 적분 loss를 영역 평균 및 물리 척도로 바꾸어 표현한 정의이며, 모든 PINO 구현이 같은 정규화를 쓴다는 진술은 아니다.[1,4]

정답 해를 $u[a]$, 해와 잔차의 양의 대표 척도를 각각 $s_u,s_r,s_i,s_b$라 하자. 무차원화한 네 loss를 다음처럼 정의한다.[1,3]

$$
\mathcal J_d
=\mathbb E_a\left[
\left\|\frac{u_\theta[a]-u[a]}{s_u}\right\|_{\Omega,\mathrm{av}}^2\right],
\qquad
\mathcal J_r^*
=\mathbb E_a\left[
\left\|\frac{r_\theta[a]}{s_r}\right\|_{\Omega,\mathrm{av}}^2\right].
$$

$$
\mathcal J_i
=\mathbb E_a\left[
\left\|\frac{i_\theta[a]}{s_i}\right\|_{D,\mathrm{av}}^2\right],
\qquad
\mathcal J_b
=\mathbb E_a\left[
\left\|\frac{b_\theta[a]}{s_b}\right\|_{\Gamma,\mathrm{av}}^2\right].
$$

별표는 정규화 전의 $\mathcal J_r$와 구별하는 표식이다. 단위가 다른 여러 PDE 성분을 다루면 성분마다 척도를 정한다. 무차원 가중치 $\lambda_d,\lambda_r,\lambda_i,\lambda_b\ge0$를 사용한 전체 목적 함수는 다음과 같다.[1,3]

$$
\mathcal J(\theta)
=\lambda_d\mathcal J_d
+\lambda_r\mathcal J_r^*
+\lambda_i\mathcal J_i
+\lambda_b\mathcal J_b.
$$

척도와 가중치는 다른 역할을 한다. 척도는 물리 단위와 대표 크기를 맞추고, 가중치는 맞춰진 항들 사이의 학습 비중을 정한다. 같은 잔차를 단위만 바꾸어 수치적으로 크게 만들면 정규화하지 않은 전체 loss의 상대 비중도 바뀐다는 것은 위 정의의 직접적인 결과이다. 최종 비교에는 가중합뿐 아니라 각 항과 사용한 척도를 함께 기록해야 한다.[1,3]

### (2) 함수 표본과 좌표 표본

$M$개의 입력 함수 $a_m$과 각 함수의 잔차 평가점 $z_{mj}=(x_{mj},t_{mj})$를 사용하자. 함수마다 $Q_m$개 점을 두고, 양의 quadrature 가중치가 $\sum_jw_{mj}=1$을 만족하면 내부 잔차의 empirical loss는 다음과 같다.[3,4,5]

$$
\widehat{\mathcal J}_r^*
=\frac1M\sum_{m=1}^{M}
\sum_{j=1}^{Q_m}w_{mj}
\left|\frac{r_\theta[a_m](z_{mj})}{s_r}\right|^2.
$$

같은 영역을 균일하게 대표하는 점에는 동일 가중치를 쓸 수 있다. 비균일 격자에서는 단순 평균이 어떤 공간 측도를 근사하는지 확인해야 한다. 예를 들어 경계 근처 점을 많이 추가한 뒤 모든 점에 같은 가중치를 주면, 경계 근처가 더 크게 반영되는 새 목적 함수를 만들 수 있다. 이러한 가중치 변경이 반드시 잘못은 아니지만, 원래 의도한 공간 평균과 다른 적분 목표를 정의하므로 그 선택을 명시해야 한다.[4,5]

정답 해가 없는 입력에서도 PDE 계수, 외력, 초기·경계 자료를 알면 잔차를 계산할 수 있다. 따라서 data loss에 사용하는 입력 집합과 physics loss에 사용하는 입력 집합은 같을 필요가 없다. 그러나 “label-free”는 입력 함수와 지배 방정식도 필요 없다는 뜻이 아니다. 새 입력을 표본화하는 절차와 그 입력에서 잔차를 계산하는 절차는 여전히 필요하다.[1,2]

## 3. 데이터 격자와 잔차 격자

원 PINO의 중요한 설정은 정답 해가 있는 격자와 PDE를 평가하는 격자를 분리하는 것이다. 거친 정답 데이터로 관측된 해의 모양을 제한하고, 더 촘촘한 격자의 물리 제약으로 그 사이에서도 방정식을 만족하도록 학습한다. 데이터 위치와 collocation 위치의 분리는 physics-informed DeepONet에서도 구성할 수 있지만, 원 PINO는 이를 FNO의 해상도 변경과 결합한다.[1,3]

### (1) 두 해상도의 역할

Data loss의 격자 간격을 $h_d$, residual loss의 간격을 $h_r$라 하자. 연속 함수의 격자 표본화 연산자를 $S_h$, network의 해당 격자 구현을 $\mathcal G_{\theta,h}$로 쓴다. 다음은 동일한 입력을 두 격자에서 다루는 계산 흐름의 정의이다.[1,3,5]

$$
a_{h_d}=S_{h_d}a,
\qquad a_{h_r}=S_{h_r}a,
\qquad
u_{\theta,h}=\mathcal G_{\theta,h}[a_h].
$$

$u_{\theta,h}$는 격자 위의 출력 배열이며 연속 함수 $u_\theta[a]$와 구별한다. Data loss는 $u_{\theta,h_d}$와 $S_{h_d}u$를 비교하고, residual loss는 $u_{\theta,h_r}$에 이산 PDE 연산자 $\mathcal P_{a,h_r}$를 적용한다.[1,3]

$$
r_{\theta,h_r}
=\mathcal P_{a,h_r}[u_{\theta,h_r}],
\qquad h_r<h_d\ \text{인 설정을 사용할 수 있다}.
$$

| 대상 | 필요한 정보 | 주된 역할 |
| --- | --- | --- |
| Data 격자 | 입력과 정답 해의 표본 | 관측된 해와 예측의 차이 평가 |
| Residual 격자 | 입력, 계수·외력, 예측 해 | PDE와 조건의 위반 평가 |
| Test 격자 | 독립 기준 해 또는 검증 잔차 | 최종 해 정확도와 격자 의존성 확인 |

더 촘촘한 격자를 사용하려면 입력 $a$와 계수·외력을 그 위치에서도 평가할 수 있어야 한다. 거친 입력 표본만 있다면 보간 또는 다른 재구성이 추가된다. 그러나 보간하거나 재구성한 입력값을 해당 위치에서 실제로 관측한 고해상도 입력값과 동일하다고 가정할 수는 없다. 이는 연속 입력을 이산 표현으로 바꾸는 과정에서 따르는 제한이며, 잔차 평가점을 늘리는 행위가 입력 정보를 새로 측정하는 것은 아니다.[1,5]

### (2) 해상도 변경과 정보의 범위

격자를 세분화하면 PDE residual의 공간적 평가와 수치 미분을 개선할 여지가 있지만, 정확도를 자동으로 보장하지 않는다. 특히 FNO의 학습된 Fourier multiplier 수, 입력 표현, 최적화 결과가 그대로라면 이 조건들도 계속 영향을 준다. 격자를 세분화했을 때 이산 구현이 일정한 연속 연산자로 수렴하는지와, 그 연속 연산자가 실제 해 연산자를 정확히 근사하는지는 별도로 판단해야 한다.[1,5]

연속 미분을 사용하는 잔차 $\mathcal P_a[v]$와 이산 잔차 사이의 차이를 다음처럼 정의하자. $v$는 평가할 만큼 매끄러운 시험 함수이다.[1,6]

$$
\delta_h[v]
=\mathcal P_{a,h}[S_hv]-S_h\mathcal P_a[v].
$$

$\delta_h$에는 미분·곱셈·입력 표본화에 따른 이산화 차이가 들어간다. 따라서 이산 격자에서 residual이 작다는 결과로부터 연속 방정식의 residual도 작다고 판단하려면, 두 residual 사이의 이산화 차이 $\delta_h$를 충분히 작게 제어해야 한다. 이 식은 오차 원인을 분리하기 위한 정의이며, 임의의 입력과 grid에 대해 $\delta_h\to0$을 주장하는 수렴 정리가 아니다.[1,6]

실험에서는 data 격자를 고정하고 residual 격자만 바꾸는 비교와, 학습을 고정하고 test 격자만 바꾸는 비교를 구별한다. 전자는 물리 제약의 해상도가 학습에 미치는 영향을, 후자는 학습된 모형의 해상도 전이를 조사한다. 새로운 입력 함수 분포로 옮겨 가는 시험은 둘과 별개이다.[1,5]

## 4. 공간 미분과 정규화

PINO 구현에서 중요한 선택은 **어떤 함수의 미분을 계산하는가**이다. 출력 배열을 Fourier 보간한 함수를 좌표에 대해 미분하는 것과, 별도로 정의한 연속 query 함수를 미분하는 것은 서로 다른 연산이다. 또한 학습을 위해 loss를 network 매개변수로 미분하는 것만으로는 PDE에 필요한 공간·시간 미분을 얻을 수 없다.[1,3]

### (1) Fourier 미분

주기적 구간 $[0,L)$에서 유한 Fourier 표현을 가진 스칼라 함수 $v$를 생각하자. 유지 mode 집합은 $\mathcal K\subset\mathbb Z$, 복소 계수는 $\widehat v_k$, 물리적 파수는 $q_k=2\pi k/L$이다. 이 문서는 정방향 변환의 지수에 음의 부호를, 복원에 양의 부호를 사용한다.[6,7]

$$
v(x)=\sum_{k\in\mathcal K}\widehat v_k e^{iq_kx},
\qquad q_k=\frac{2\pi k}{L}.
$$

유한 합을 항별 미분하면 다음을 정확히 얻는다.[6,7]

$$
\partial_xv
=\sum_{k\in\mathcal K}(iq_k)\widehat v_k e^{iq_kx},
\qquad
\partial_{xx}v
=\sum_{k\in\mathcal K}(-q_k^2)\widehat v_k e^{iq_kx}.
$$

첫 미분은 파수에 비례하고 두 번째 미분은 음의 파수 제곱에 비례한다. 이 등식은 표현된 유한 Fourier 함수에 대한 것이다. 원래 연속장이 그 표현으로 충분히 근사되는지, 주기적 연결이 매끄러운지, 표본화가 mode를 구분할 만큼 촘촘한지는 별도로 확인한다. 미분은 높은 파수의 오차에도 더 큰 인자를 곱하므로 값의 오차가 작다는 사실만으로 미분 정확도를 판단할 수 없다.[1,6,7]

격자 값에서 계수를 구하고 파수 인자를 곱한 뒤 복원할 때 fast Fourier transform (FFT)을 사용할 수 있다. 그러나 비선형 곱은 기존에 없던 높은 mode를 만들 수 있으며, 제한된 grid에서 이것이 낮은 mode로 접히는 aliasing이 발생할 수 있다. Residual 계산에 $u\partial_xu$ 같은 항이 있으면 각 미분만이 아니라 곱의 해상도와 aliasing도 검토해야 한다.[1,6]

### (2) 출력 projection의 chain rule

원 PINO는 마지막 latent field를 미분한 뒤 출력 projection에 chain rule을 적용하는 방법도 설명한다. 이를 명확히 하기 위해 $v(x)\in\mathbb R^c$가 미분 가능한 유한 Fourier 함수이고, 출력 $u(x)=Q(v(x))$에서 $Q:\mathbb R^c\to\mathbb R$가 두 번 연속 미분 가능하다고 제한하자. $DQ$와 $D^2Q$는 각각 Jacobian과 Hessian이다.[1,3]

$$
\partial_xu=DQ(v)\,\partial_xv.
$$

$$
\partial_{xx}u
=DQ(v)\,\partial_{xx}v
+(\partial_xv)^{\mathsf T}D^2Q(v)(\partial_xv).
$$

이는 명시한 합성 함수의 정확한 chain rule이다. Projection이 비선형이면 두 번째 항이 필요하다. 채널이 하나일 때 익숙한 $Q'(v)v''+Q''(v)(v')^2$가 되지만, 여러 채널에서는 Hessian을 통한 교차항이 존재한다. 실제 마지막 층에 좌표 의존 skip 경로 등이 남아 있다면 그 경로의 미분도 포함해야 한다.[1,3]

한편 완성된 출력 $Q(v)$를 grid에서 읽어 FFT로 미분하면, grid가 정의한 출력 보간 함수를 미분하게 된다. 비선형 $Q$는 $v$의 유지 mode 밖 성분도 만들 수 있으므로, 이 계산과 위 chain rule은 유한 해상도에서 같다고 가정할 수 없다. 이 차이는 원 논문의 explicit differentiation 구성과 Fourier aliasing 원리에서 도출된다.[1,6]

| 미분 방식 | 실제 미분 대상 | 확인할 조건 |
| --- | --- | --- |
| Finite difference | 이웃 grid 값 | 간격·차수·경계 stencil |
| Fourier 미분 | Fourier로 표현된 함수 | 주기성·매끄러움·해상도 |
| 좌표 automatic differentiation | 좌표가 연결된 연속 query 함수 | 계산 그래프의 좌표 의존성 |
| Latent field와 chain rule | 명시한 latent–projection 합성 | 모든 경로와 고차 chain rule |

Automatic differentiation은 주어진 계산 그래프의 미분을 계산한다. 입력 배열 성분 $a_j$에 대한 $\partial u_i/\partial a_j$는 입력값 민감도이며, 출력 위치에 대한 $\partial_xu$와 다르다. 격자 FNO에 좌표 채널이 있다는 이유만으로 특정 채널에 대한 gradient를 물리적 공간 미분과 동일시해서는 안 된다. 어떤 연속 query 함수가 정의되어 있는지 먼저 확인한다.[1,3]

### (3) 좌표와 출력의 단위 변환

공간·시간·해의 척도를 각각 $L,T,U>0$로 두고, 상수 offset $u_c$를 사용하여 좌표와 출력을 다음처럼 표현하자.[1,3]

$$
x=L\xi,\qquad t=T\tau,
\qquad u(x,t)=u_c+U\widetilde u(\xi,\tau).
$$

상수 척도라는 가정 아래 chain rule을 직접 적용하면 다음을 얻는다. 이는 특정 학습 알고리즘의 경험식이 아니라 좌표 변환의 정확한 결과이다.[1,3]

$$
\partial_tu=\frac{U}{T}\partial_\tau\widetilde u,
\qquad
\partial_xu=\frac{U}{L}\partial_\xi\widetilde u,
\qquad
\partial_{xx}u=\frac{U}{L^2}\partial_{\xi\xi}\widetilde u.
$$

물리적 확산계수 $\kappa>0$를 갖는 1차원 열방정식으로 확인할 수 있다. 외력이 없고 계수가 상수이며, 충분히 매끄러운 해를 가정한다.[6,7]

$$
\partial_tu-\kappa\partial_{xx}u=0,
\qquad [\kappa]=\mathrm{length}^2/\mathrm{time}.
$$

앞의 변환을 대입하고 $U/T$로 나누면 무차원 방정식은 다음과 같다.[6,7]

$$
\partial_\tau\widetilde u
-\frac{\kappa T}{L^2}\partial_{\xi\xi}\widetilde u=0.
$$

따라서 $[0,1)$ 좌표에서 계산한 Fourier 미분에 물리 좌표용 $\kappa$를 그대로 넣는 것만으로 충분하지 않다. 무차원 확산계수 $\kappa T/L^2$를 사용하거나, 미분을 물리 단위로 되돌려야 한다. 위치에 따라 달라지는 평균이나 표준편차로 출력을 정규화한다면 위 상수 척도식도 그대로 적용할 수 없고 그 함수의 미분을 포함해야 한다. 이 결론들은 같은 chain rule에서 직접 따른다.[1,3,6]

## 5. 경계 조건과 해의 식별

PDE residual은 영역 내부의 관계를 검사한다. 원하는 해를 정하려면 초기·경계 자료도 함께 만족해야 한다. 특히 Fourier 연산에 사용하는 주기적 확장 영역과 실제 물리 영역의 경계 조건을 구별해야 한다.[1,4,6]

### (1) 열방정식의 진단 예

앞의 열방정식에 주기 경계 $u(x+L,t)=u(x,t)$를 두고, 정수 $k\ne0$와 실수 진폭 $A\ne0$에 대해 초기 조건을 $a(x)=A\cos(q_kx)$로 정하자. Fourier mode별 열방정식을 풀면 다음 해를 얻는다. 이는 문헌의 열방정식 mode 해법을 주기 cosine 초기 조건에 적용한 계산 예이다.[6,7]

$$
u_k(x,t)
=Ae^{-\kappa q_k^2t}\cos(q_kx).
$$

시간 미분과 공간 두 번 미분을 직접 대입하면 두 항이 상쇄된다. 그러나 $\bar u(x,t)=0$ 역시 내부 PDE residual은 0이다. 두 함수의 차이는 초기 조건에 나타난다.[1,7]

$$
\mathcal P[\bar u]=0,
\qquad
\bar u(x,0)-a(x)=-A\cos(q_kx).
$$

한 주기에서 cosine 제곱의 평균이 $1/2$이므로, 2절의 평균 norm에서 초기 오차는 다음과 같다.[6,7]

$$
\|\bar u(\cdot,0)-a\|_{D,\mathrm{av}}^2
=\frac{A^2}{2}.
$$

이 예는 PINO가 실제 학습에서 언제나 영함수로 수렴한다는 주장이 아니다. 내부 잔차만으로 초기값 문제의 정답을 구별할 수 없음을 보여 주는 정확한 반례이다. Initial loss의 가중치를 지나치게 작게 잡거나 평가에서 초기 시각을 제외하면, 내부 PDE residual이 작더라도 잘못된 해를 발견하지 못할 수 있다는 점을 보여 준다.[1,4]

### (2) 물리 경계와 계산 영역

주기 Fourier 표현은 반대쪽 끝을 이어 놓은 함수를 나타낸다. 비주기 문제에서 padding이나 Fourier continuation으로 계산 영역을 넓힐 수 있지만, 물리적 Dirichlet 또는 Neumann 조건은 원래 영역에서 별도로 확인해야 한다. 원 PINO도 확장 공간을 사용하면서 loss는 원래 영역에서 평가하는 구성을 설명한다.[1,6]

경계 조건을 만족하도록 경계 오차에 penalty loss를 부여할 수도 있고, 조건을 정확히 만족하는 trial function을 출력 표현에 직접 포함할 수도 있다. 예를 들어 무차원 구간 $\xi\in[0,1]$의 정상 문제에서 $u(0)=g_0$, $u(1)=g_1$를 강제하는 다음 trial function을 생각할 수 있다. $v_\theta[a](\xi)$는 끝점에서 유한한 임의의 network 출력이다.[6,8]

$$
u_\theta[a](\xi)
=(1-\xi)g_0+\xi g_1
+\xi(1-\xi)v_\theta[a](\xi).
$$

끝점을 대입하면 마지막 항이 사라지므로 두 경계값이 정확히 나온다. 이는 경계에 맞는 trial function을 구성하는 원리를 직접 적용한 예이며, 기본 PINO가 항상 이 식을 쓴다는 뜻은 아니다. 내부 PDE를 만족하는지는 여전히 학습해야 하고, residual 계산에는 $\xi(1-\xi)$의 미분도 포함한다.[6,8]

| 조건 부과 방식 | 만족을 유도하는 위치 | 남는 확인 사항 |
| --- | --- | --- |
| Boundary penalty | 경계 loss | 최종 경계 오차와 가중치 |
| 조건을 내장한 trial function | 출력 표현 자체 | 미분의 일관성·표현 가능한 해 |
| 주기 Fourier 표현 | 계산상 이어 붙인 영역 | 실제 문제의 주기성과 일치 여부 |
| Padding·continuation | 확장된 계산 영역 | 원래 경계의 조건과 오차 |

## 6. 학습 자료와 추론

PINO는 여러 입력 함수에 대해 하나의 연산자 모형을 학습하고, 학습한 매개변수를 고정한 뒤 보지 않은 입력의 해를 예측한다. 정답 해 없이 physics loss를 계산할 수 있더라도 학습된 모형의 예측이 정확하다는 보장은 없다. 따라서 최종 해의 정확도는 독립적인 시험으로 확인해야 한다.[1,2,3]

### (1) 정답 데이터의 역할

Physics-only 학습에서는 2절의 목적 함수에서 $\lambda_d=0$으로 놓는다. Hybrid 학습에서는 정답 해를 사용할 수 있는 입력에 data loss도 적용한다. 두 설정 모두 입력 함수와 PDE·초기·경계 자료는 필요하며, 정답 해의 사용 여부만 다르다.[1,2]

Physics-only 학습을 선택하면 정답 해를 생성하는 비용을 줄일 수 있다. 그러나 data loss를 제외해도 정답 데이터를 사용하는 학습과 같은 예측 정확도를 얻는다고 보장할 수는 없다. 독립 PINO 실험은 physics-only와 data-plus-physics를 구분하여 비교하고, physics-informed DeepONet 연구도 가중치 선택과 최적화의 어려움을 논의한다. 따라서 두 설정을 비교할 때에는 최종 가중합뿐 아니라 해 오차와 각 residual을 따로 확인한다. 이 문서에서는 그 결과를 모든 PDE에 대한 우열이나 데이터 절감 비율로 일반화하지 않는다.[2,3]

### (2) 고정된 모형의 추론

학습 후의 매개변수를 $\theta_0$, 새로운 입력을 $a_*$라 하면 추론은 다음 연산자 평가이다.[1,3]

$$
u_*=\mathcal G_{\theta_0}[a_*].
$$

이때 초기·경계 조건이 새로운 입력의 일부라면 그 정보가 모형 입력과 residual 정의 양쪽에 일관되게 들어가야 한다. 학습에서 고정했던 물리 계수나 영역 형상을 바꾸는 시험은 단순히 새로운 함수 표본을 넣는 것과 같지 않다. 어떤 변화가 학습 분포에 포함되었는지에 따라 별도의 분포 이동 시험으로 다룬다.[1,3,5]

## 7. 오차 해석과 평가

PINO 평가에서는 해의 오차, 방정식 위반, 초기·경계 오차를 나누어야 한다. 학습에 쓰지 않은 함수와 좌표에서 각각을 확인하고, 잔차를 계산하는 수치 연산의 해상도도 기록한다. 해 오차와 physics loss를 함께 제시한 독립 실험과 함수·좌표의 표본 오차를 분리한 분석이 이 평가 틀의 근거이다.[2,3,5]

### (1) 잔차와 해 오차의 연결

작은 잔차에서 작은 해 오차를 추론하려면 PDE의 안정성 조건이 필요하다. 예를 들어 초기·경계 조건을 만족하는 적절한 함수 집합에서 두 함수 $v,u$에 대해 다음 안정성 부등식이 성립한다고 **가정**하자. $X$는 해 오차의 norm 공간이고 $Y$는 residual의 norm 공간이다.[4,8]

$$
\|v-u\|_X
\le C_{\mathrm{stab}}\,
\|\mathcal P_a[v]-\mathcal P_a[u]\|_Y.
$$

정답이 $\mathcal P_a[u]=0$을 만족하므로 오른쪽은 $C_{\mathrm{stab}}\|\mathcal P_a[v]\|_Y$가 된다. 이 조건은 자동으로 주어지는 것이 아니다. $C_{\mathrm{stab}}$은 방정식, 입력과 허용 함수의 norm에 의존할 수 있고, 조건을 정확히 만족하지 않는 함수에는 초기·경계 오차도 포함한 다른 추정이 필요하다. 독립 residual 분석 역시 특정 방정식 종류와 초기·경계 조건의 정확한 만족을 전제로 오차를 제한하므로, 그 결과를 임의의 PINO에 그대로 적용하지 않는다.[4,8]

학습점에서의 residual 평균은 연속 norm의 quadrature 근사이다. 이 근사 차이가 크면 training loss가 작아도 연속 residual은 클 수 있다. 나아가 한 입력의 안정성 결과를 함수군 전체의 보장으로 확장하려면 입력 분포에 걸친 상수와 표본 오차도 통제해야 한다. 이는 고정 문제에 대한 안정성 분석과 독립 연산자 학습의 표본 분석을 구분하여 얻는 조건부 해석이다.[4,5,6]

따라서 training residual의 감소를 해 정확도의 확인으로 대신하지 않는다. 잔차에 의한 오차 추정에는 적용 가능한 안정성 조건과 잔차 평가의 정확도가 필요하며, 실제 모형 비교에서는 독립 기준 해에 대한 오차도 따로 측정한다. 이는 residual 기반 분석의 전제와 독립 PINO 실험의 해·물리 오차 구분을 함께 따른 평가 원칙이다.[2,4,8]

### (2) 정량 지표와 시험 집합

!!! info "[Measurement]"
    학습에 사용하지 않은 입력 함수마다 동일한 시험 좌표에서 기준 해 $u[a]$와 예측 해를 비교한다. $\|u[a]\|_{\Omega,\mathrm{av}}>0$일 때 상대 해 오차는 다음과 같다.[2,3]

    $$
    e_u(a)=
    \frac{\|u_\theta[a]-u[a]\|_{\Omega,\mathrm{av}}}
    {\|u[a]\|_{\Omega,\mathrm{av}}}.
    $$

    정답 norm이 0이거나 매우 작으면 절대 오차와 사용한 기준 척도를 함께 보고한다. 동일한 입력에 대해 독립 평가점에서 물리적 residual의 크기도 측정한다. 다음은 대표 척도로 무차원화한 root-mean-square 지표이다.[2,3,4]

    $$
    e_r(a)=\frac{\|\mathcal P_a[u_\theta[a]]\|_{\Omega,\mathrm{av}}}{s_r},
    \quad
    e_i(a)=\frac{\|i_\theta[a]\|_{D,\mathrm{av}}}{s_i},
    \quad
    e_b(a)=\frac{\|b_\theta[a]\|_{\Gamma,\mathrm{av}}}{s_b}.
    $$

함수별 오차를 먼저 구한 뒤 평균과 산포를 집계하면 일부 입력의 큰 오차를 전체 좌표 평균 속에 숨기는 일을 줄일 수 있다. 같은 함수의 다른 좌표를 시험하는 실험과 보지 않은 함수의 해를 시험하는 실험을 구분하고, 기준 해의 수치해법·격자·시간 간격도 기록한다. 기준 해가 부정확하면 그 차이를 모형 오차만으로 해석할 수 없다는 것은 비교 정의에서 따른다.[3,5]

### (3) 비교 실험과 비용

다음 표는 우월한 방법을 미리 정하는 기준이 아니라, 관찰한 차이의 원인을 분리하는 실험 설계이다. 가능한 한 network 구조와 입력 집합을 고정하고 하나의 요인만 바꾼다.[1,2,3]

| 비교 | 고정할 주요 조건 | 확인할 질문 |
| --- | --- | --- |
| Data-only / data-plus-physics | 구조·정답 데이터 | 물리 제약이 해·잔차 오차를 어떻게 바꾸는가 |
| Physics-only / hybrid | PDE·입력 분포·평가점 | 정답 supervision의 역할은 무엇인가 |
| Residual 격자 변경 | Data 격자·구조 | 미분·표본화와 학습 결과가 함께 바뀌는가 |
| Test 격자 변경 | 학습된 매개변수 | 해상도 전이에서 오차가 유지되는가 |
| 분포 내 / 분포 밖 입력 | 오차 정의·평가 해상도 | 어느 입력 변화까지 재사용 가능한가 |

비용은 데이터 생성, 연산자 학습, 반복 추론으로 나누어 기록한다. $N_*$개 문제를 학습된 모형으로 평가할 때의 총시간을 다음처럼 정의할 수 있다. $t_{\mathrm{infer},m}$은 $m$번째 입력의 추론 시간이며, 아래 식은 학습 후 매개변수를 고정하여 평가하는 절차에 대한 것이다.[1,2]

$$
T_{\mathrm{total}}
=T_{\mathrm{data}}+T_{\mathrm{train}}
+\sum_{m=1}^{N_*}t_{\mathrm{infer},m}.
$$

이 식은 정답 데이터 생성, 연산자 모형의 학습 및 여러 입력에 대한 추론에 걸린 시간을 모두 합산하기 위한 정의이다. 특정 하드웨어에서의 추론 시간만 비교하여 전체 계산의 이득으로 해석하지 않는다. 비교에는 동일한 정확도 목표, batch 크기, 하드웨어와 residual 평가 비용을 명시한다. 특히 residual의 해상도나 학습 반복 수가 달라지면 학습 비용도 달라지므로 함께 기록한다.[1,2]

## 8. 요약

- PINO는 입력 함수군에 대한 해 연산자를 학습하며, 예측 해의 PDE·초기·경계 residual을 목적 함수에 포함한다. 원 방법의 backbone은 FNO이다.
- Data 격자와 residual 격자는 역할이 다르다. 잔차 격자를 촘촘히 만드는 것과 새로운 입력 함수를 학습하는 것은 별개이다.
- 공간 미분에는 연속 표현, Fourier 부호·파수, projection의 chain rule 및 좌표·출력 정규화가 일치해야 한다.
- 작은 내부 residual만으로 원하는 해가 식별되지는 않는다. 초기·경계 조건, 수치 미분 오차와 안정성 조건을 함께 확인한다.
- Physics-only와 hybrid 학습을 구분하고, 고정된 모형을 독립 시험 함수에서 평가하여 해·잔차·조건 오차 및 총비용을 함께 보고한다.

## 9. 참고문헌

1. Z. Li, H. Zheng, N. Kovachki, D. Jin, H. Chen, B. Liu, K. Azizzadenesheli, and A. Anandkumar, "Physics-Informed Neural Operator for Learning Partial Differential Equations," arXiv:2111.03794v4 (2023). §§2–3, §4 and Appendix C. [Original paper](https://arxiv.org/abs/2111.03794v4).
2. R. Majumdar, A. Varhade, S. Karande, and L. Vig, "Can Physics Informed Neural Operators Self Improve?" *DLDE-III Workshop, NeurIPS* (2023). §§2–3, Algorithm 1 and Table 1. [arXiv:2311.13885](https://arxiv.org/abs/2311.13885).
3. S. Wang, H. Wang, and P. Perdikaris, "Learning the solution operator of parametric partial differential equations with physics-informed DeepOnets," arXiv:2103.10974v1 (2021). §§2–5. [Original preprint](https://arxiv.org/abs/2103.10974v1).
4. S. Mishra and R. Molinaro, "Estimates on the generalization error of Physics Informed Neural Networks (PINNs) for approximating PDEs," arXiv:2006.16144. §2, Assumption 2.1 and Theorem 2.6. [Original paper](https://arxiv.org/abs/2006.16144).
5. T. De Ryck and S. Mishra, "Generic bounds on the approximation error for physics-informed (and) operator learning," *NeurIPS* **35** (2022). §§2, 3.3–3.4 and 5. [arXiv:2205.11393](https://arxiv.org/abs/2205.11393).
6. J. P. Boyd, *Chebyshev and Fourier Spectral Methods*, Second Edition, online manuscript (2000). §§1.9, 2.2, 2.8, 3.7 (diffusion example, pp. 76–77), 6.5, 9.2–9.5 and 11.2–11.4. [Book PDF](https://depts.washington.edu/ph506/Boyd.pdf).
7. G. Strang, *Computational Science and Engineering*, §4.1, "Fourier Series for Periodic Functions," pp. 317–333, Wellesley-Cambridge Press (2007). Complex Fourier series and heat equation example. [Book section](https://math.mit.edu/~gs/cse/websections/cse41.pdf).

8. S. Liu, X. Huang, and P. Protopapas, "Residual-Based Error Bound for Physics-Informed Neural Networks," *Proceedings of Machine Learning Research* **216**, 1284–1293 (2023). §§2, 5–6. [Original paper](https://proceedings.mlr.press/v216/liu23b.html).
