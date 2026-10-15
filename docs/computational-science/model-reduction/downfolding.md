---
description: 전자구조의 block Hamiltonian에서 제거법을 유도하고 projection, 에너지 의존 유효 Hamiltonian, 비직교 기저와 contact self-energy의 차이를 설명한다.
---

# Downfolding and effective Hamiltonians

**Downfolding**은 남길 자유도에 대한 방정식을 만들면서 나머지 자유도의 영향을 유효 항에 포함하는 방법이다. 이 문서에서는 이 용어를 block 방정식의 정확한 제거와 그 근사라는 뜻으로 사용한다. 남기지 않은 계수를 처음부터 0으로 제한하는 coordinate projection과 달리, 제거법은 그 계수를 남긴 계수의 함수로 풀어 원래 방정식에 대입한다. 그 결과 행렬 크기는 작아지지만 에너지 의존성이 생긴다.[1,2]

선행 문서 [Model reduction fundamentals](fundamentals.md)와 [Projection methods](projection-methods.md)의 $Hc=\epsilon Sc$를 출발점으로 삼는다. 여기서는 미지 고유에너지와 시험 에너지를 함께 다루므로 $\epsilon$ 대신 $E$를 쓴다. 처음에는 직교 기저 $S=I_M$와 유한 Hermitian Hamiltonian $H=H^\dagger$를 가정하고, 뒤에서 양의 정부호 overlap $S$와 복소 에너지 $z$로 확장한다. 전자 상관의 many-body self-energy를 유도하는 문서는 아니며, 아래 self-energy는 제거한 일전자 자유도에서 생긴 항이다.[1–4]

## 1. Active space와 제거할 공간

### (1) Block Hamiltonian

전체 $M$개 orbital을 남길 $r$개 orbital의 집합 $A$와 제거할 $M-r$개 orbital의 집합 $B$로 나눈다. 여기서 **active space**는 $A$가 생성하는 공간이고, 관심 상태가 주로 표현되기를 기대하는 공간이다. $B$가 관심 에너지에서 멀리 있는가는 근사를 할 때 필요한 판단이며, 정확한 제거의 정의 자체에 포함된 조건은 아니다.[1,2]

계수 벡터 $c$와 Hamiltonian을 같은 순서로 나누면 다음과 같다. $H_{AB}$는 $B$ 계수에서 $A$ 방정식으로 작용하는 coupling이고, Hermitian 조건으로 $H_{BA}=H_{AB}^\dagger$이다.[1,2]

$$
H=\begin{pmatrix}H_{AA}&H_{AB}\\H_{BA}&H_{BB}\end{pmatrix},
\qquad c=\begin{pmatrix}c_A\\c_B\end{pmatrix}.
$$

$Hc=Ec$는 서로 연결된 두 방정식이다.[1,2]

$$
H_{AA}c_A+H_{AB}c_B=Ec_A,
\qquad
H_{BA}c_A+H_{BB}c_B=Ec_B.
$$

대각 block은 각 공간 내부의 운동을, 비대각 block은 두 공간의 혼합을 나타낸다. 관심 상태가 $A$에 주로 놓여 있어도 $H_{BA}c_A$가 0이 아니면 $B$ 성분이 일반적으로 필요하다. 따라서 orbital의 개수가 많고 적다는 사실과 그 orbital을 무시할 수 있다는 판단은 구별해야 한다. 예를 들어 높은 onsite energy를 가진 orbital도 낮은 에너지 orbital과 결합하면 낮은 상태의 에너지와 계수에 영향을 준다.[1,2]

### (2) Projection의 누락 항

좌표를 선택하는 축소 기저 $V=\begin{pmatrix}I_r&0\end{pmatrix}^{\mathsf T}$를 택하면 $c\simeq Va=(a,0)^{\mathsf T}$이다. 이때 $a$는 축소 좌표이며, [Galerkin projection](projection-methods.md)으로 얻는 행렬은 단순히 $H_{AA}$이다. 다음 관계는 위 block 식에 $c_B=0$을 넣어 직접 확인할 수 있다.[1,2]

$$
H_r=V^\dagger HV=H_{AA},
\qquad H_{AA}a=\theta a.
$$

$\theta$는 projection의 Ritz value이다. 축소 방정식을 정확히 풀어도 원래 공간의 residual $\rho=HVa-\theta Va$에는 제거 방향의 성분이 남는다.[1,2]

$$
\rho=\begin{pmatrix}0\\H_{BA}a\end{pmatrix}.
$$

이 식은 projection이 어떤 정보를 버렸는지 보여준다. $A$ 방향의 방정식은 만족하지만, $B$ 방향의 방정식은 일반적으로 만족하지 않는다. 반면 $H_{BA}a=0$인 특별한 상태는 $B$ 성분 없이도 정확할 수 있다. 모든 coupling이 0인 경우와 특정 상태에서 coupling의 작용만 0인 경우도 구별한다. 이 절의 비교는 동일한 좌표 집합 $A$를 사용하는 projection에 관한 것으로, 전체 고유상태를 이미 포함하도록 잘 구성한 일반적인 축소 공간까지 부정하는 설명은 아니다.[1,2]

## 2. Schur complement와 유효 Hamiltonian

### (1) 제거와 역대입

정확한 제거의 핵심 관계는 다음과 같다. $EI_B-H_{BB}$가 가역이면, 두 번째 block 방정식으로부터 $c_B$를 풀 수 있다. $I_B$는 $B$ 공간의 항등행렬이다.[1,2]

$$
(EI_B-H_{BB})c_B=H_{BA}c_A,
\qquad
c_B=(EI_B-H_{BB})^{-1}H_{BA}c_A.
$$

이를 첫 번째 식에 넣으면 **effective Hamiltonian** $H_{\mathrm{eff}}(E)$가 나온다.[1,2]

$$
H_{\mathrm{eff}}(E)c_A=Ec_A,
\qquad
H_{\mathrm{eff}}(E)=H_{AA}+\Sigma_B(E),
$$

$$
\Sigma_B(E)=H_{AB}(EI_B-H_{BB})^{-1}H_{BA}.
$$

$\Sigma_B$는 제거한 $B$가 $A$ 방정식에 주는 보정이다. 행렬 곱을 오른쪽부터 읽으면 $A$에서 $B$로 coupling이 작용하고, $B$ 내부의 응답을 거쳐 다시 $A$로 돌아오는 구조이다. $H_{AA}$만 남긴 projection에서는 이 항이 빠진다. Hamiltonian과 $E$가 에너지 단위이면 역행렬은 에너지의 역수 단위이므로 $\Sigma_B$도 에너지 단위이다. 여기까지는 coupling이 작다는 전개를 하지 않은 정확한 식이다.[1,2]

이 식은 **Schur complement**와 같은 block 제거 구조이다. 엄밀히 말하면 $EI_M-H$에서 $B$를 제거한 Schur complement는 $EI_A-H_{\mathrm{eff}}(E)$이다. $H_{\mathrm{eff}}$라는 이름 때문에 이를 원래 Hamiltonian의 단순한 부분행렬로 생각해서는 안 된다. 보정 항은 $H_{BB}$와 두 coupling block을 모두 알아야 계산할 수 있다.[1,2]

역방향도 중요하다. $H_{\mathrm{eff}}(E)c_A=Ec_A$의 해를 얻은 뒤 위 식으로 $c_B$를 **역대입**하면 전체 $c$가 원래 고유값 방정식을 만족한다. 이 동치는 $EI_B-H_{BB}$가 가역인 에너지에서 성립하며, $c_A$를 얻었다는 사실만으로 전체 상태의 정규화까지 끝난 것은 아니다.[1,2]

### (2) 에너지 의존성과 pole

$H_{\mathrm{eff}}$에는 구하려는 $E$가 들어간다. 따라서 임의의 $E_0$에서 행렬을 한 번 대각화한 값은 일반적으로 원래 문제의 고유값이 아니다. $H_{\mathrm{eff}}(E)$의 $j$번째 고유값 가지를 $\nu_j(E)$라 쓰면 실제로 풀어야 할 조건은 다음과 같다.[1,2]

$$
\nu_j(E)-E=0.
$$

이는 에너지에 대한 **nonlinear eigenvalue problem**이다. 작은 $r\times r$ 행렬의 각 시험 에너지에서 고유값은 $r$개이지만, 에너지를 움직이며 찾는 전체 근의 개수를 $r$개로 제한할 수는 없다. 뒤의 $r=2$ 예제에서는 서로 다른 에너지에서 세 근을 구한다. 이 성질 때문에 정확한 제거는 곧바로 두 상태만 남기는 근사와 같지 않다.[1,2]

$H_{BB}$의 정규직교 고유벡터를 $u_\beta$, 고유값을 $\varepsilon_\beta$라 쓰고 $g_\beta=H_{AB}u_\beta$를 정의하면 보정의 구조가 더 분명해진다. 다음 식은 위 resolvent의 spectral decomposition이다.[1,2]

$$
\Sigma_B(E)=\sum_\beta
\frac{g_\beta g_\beta^\dagger}{E-\varepsilon_\beta}.
$$

분모가 작으면 해당 $B$ 상태의 영향이 커질 수 있다. $\varepsilon_\beta$는 제거한 block의 고유값이며, 전체 결합계의 고유값과 같다고 단정할 수 없다. $g_\beta\ne0$이면 $\Sigma_B$에 pole이 나타나고, $g_\beta=0$이면 그 보정의 residue는 0이다. 그러나 후자의 경우에도 원래 역행렬식은 $E=\varepsilon_\beta$에서 정의되지 않는다. 이 지점의 해는 원래 block 방정식에서 따로 확인한다.[1,2]

예를 들어 $H_{BB}u_\beta=\varepsilon_\beta u_\beta$와 $H_{AB}u_\beta=0$이면 $(0,u_\beta)^{\mathsf T}$는 전체 고유상태이다. $A$ 성분이 0인 이런 상태를 $c_A\ne0$의 축소 방정식만 풀어 찾을 수는 없다. 이는 제거법의 적용 조건을 벗어난 상태가 존재할 수 있다는 뜻이다. Pole을 건너뛰었다는 이유만으로 모든 고유상태를 확보했다고 보고해서도 안 된다.[1,2]

유한 행렬에서는 block determinant 항등식으로도 같은 조건을 확인한다. 아래는 두 block 방정식에 대응하는 직접적인 선형대수 결과이며, $E\notin\operatorname{spec}(H_{BB})$에서 쓴다.[1,2]

$$
\det(EI_M-H)=\det(EI_B-H_{BB})
\det\!\left(EI_A-H_{\mathrm{eff}}(E)\right).
$$

오른쪽 두 인자를 pole에서 각각 평가해 $0\times\infty$로 계산할 수는 없다. 분모를 곱해 다항식으로 정리한 경우에도 원래 정의역과 특이점의 해를 다시 확인해야 한다. 수치적으로는 pole 사이 구간을 나누어 근을 찾고, 얻은 근에서 전체 방정식의 residual을 확인하는 편이 해석을 분명하게 한다.[1,2]

## 3. Projection과 downfolding

### (1) 고정 공간과 에너지 의존 복원

Projection은 정해 둔 $V$로 상태를 $Va$에 제한한다. 정확한 downfolding에서는 $A$ 계수로부터 전체 상태를 복원하는 행렬 자체가 에너지에 의존한다. 이를 $T(E)$라고 정의하면 다음과 같다.[1,2]

$$
c=T(E)c_A,
\qquad
T(E)=\begin{pmatrix}I_A\\(EI_B-H_{BB})^{-1}H_{BA}\end{pmatrix}.
$$

각 열에는 $A$의 좌표 성분뿐 아니라 $B$ 성분이 붙어 있다. 같은 $A$ 좌표라도 서로 다른 고유에너지에서는 다른 $B$ 성분이 복원된다. 따라서 하나의 고정된 $r$차원 공간에 모든 상태를 넣는 projection의 논리를 에너지 의존 $T(E)$에 그대로 적용할 수 없다. 작은 행렬이 전체의 여러 상태를 재현할 수 있는 이유도 이 복원 규칙에 남아 있는 정보 때문이다.[1,2]

전체 상태를 정규화하려면 $c_A^\dagger c_A$만 계산해서는 안 된다. 실수 $E$가 pole 밖에 있을 때 $R_B(E)=(EI_B-H_{BB})^{-1}$를 쓰면, $R_B=R_B^\dagger$이므로 역대입 식에서 다음 정규화가 직접 나온다.[1,2]

$$
1=c^\dagger c
=c_A^\dagger\left[I_A+H_{AB}R_B(E)^2H_{BA}\right]c_A.
$$

이 bracket은 무차원 양의 정부호 행렬이다. $c_A$를 Euclidean norm 1로 선택했다면 복원된 전체 벡터는 일반적으로 norm이 1보다 크다. 전체 벡터를 다시 정규화하거나, 처음부터 bracket을 사용해 $c_A$의 크기를 정한다. 혼합이 강한 상태에서는 이 차이를 무시할 수 없다.[1,2]

같은 사실을 에너지 미분으로도 표현할 수 있다. $\Sigma'_B=d\Sigma_B/dE$라 쓰면 역행렬 미분의 음의 부호에 주의해야 한다. 아래 두 식은 앞의 정확한 복원식으로부터 얻은 관계이다.[1,2]

$$
\Sigma'_B(E)=-H_{AB}R_B(E)^2H_{BA},
\qquad T(E)^\dagger T(E)=I_A-\Sigma'_B(E).
$$

즉, 에너지 의존성을 잃으면 상태의 정규화 정보도 놓칠 수 있다. 이 관계는 여기서 가정한 유한 Hermitian 계의 실수 고유에너지에 관한 것이며, 열린계의 복소 resonance를 같은 양의 norm으로 정규화한다는 뜻은 아니다.[1,2]

상태에 대한 관측량도 같은 복원 규칙을 따라야 한다. 원래 공간에 조립된 Hermitian 관측량 행렬을 $O$라 하면, 전체 정규화까지 포함한 기대값은 다음 직접 대입식으로 계산한다.[1,2]

$$
\langle O\rangle=
\frac{c_A^\dagger T(E)^\dagger O T(E)c_A}
{c_A^\dagger T(E)^\dagger T(E)c_A}.
$$

$O_{AA}$만 사용하면 $B$ 성분과 교차 항의 기여가 빠질 수 있다. 예를 들어 $B$ orbital의 점유 비중을 보고 싶다면 복원한 $c_B$가 필요하다. 에너지 오차가 작다는 사실은 이 모든 기대값의 오차가 작다는 보증이 아니므로, 사용할 관측량을 함께 정해 검증해야 한다.[1,2]

다음 표는 같은 $A$를 출발점으로 하는 세 절차의 차이이다. 정적 근사는 다음 절의 $E_0$ 고정 근사를 뜻한다.[1,2]

| 비교 항목 | Coordinate projection | 정확한 제거 | 정적 근사 |
| --- | --- | --- | --- |
| 행렬 | $H_{AA}$ | $H_{AA}+\Sigma_B(E)$ | $H_{AA}+\Sigma_B(E_0)$ |
| 제거 방향의 상태 | 0으로 제한 | 에너지별 역대입 | 별도 복원·검증 필요 |
| 고유값 문제 | 선형 | 에너지에 대해 비선형 | 선형 |
| 보존되는 정보 | 선택 공간 내부 | 가역성 조건 아래 전체 방정식 | 기준 에너지 부근의 근사 |
| 주요 실패 조건 | 중요한 혼합 누락 | 제거 block의 특이점 | 큰 에너지 변화·가까운 pole |

### (2) 정적 근사와 유효 범위

계산을 단순화하려면 기준 에너지 $E_0$에서 self-energy를 고정할 수 있다. 이때 $H_{\mathrm{stat}}$는 보통의 에너지 독립 Hermitian 행렬이다. 다만 이 단계부터는 정확한 제거와 구별되는 근사가 된다.[1,2]

$$
H_{\mathrm{stat}}=H_{AA}+\Sigma_B(E_0),
\qquad H_{\mathrm{stat}}a=\theta a.
$$

관심 에너지 구간이 좁고 $H_{BB}$의 spectrum에서 충분히 떨어져 있으면 $\Sigma_B(E)$의 변화가 작을 수 있다. 기준 에너지를 관심 상태들 부근에 놓는 이유이다. 높은 에너지 orbital을 제거했다는 말만으로 충분하지 않으며, 실제 coupling의 크기와 구간 전체에서의 분모를 함께 봐야 한다.[1,2]

그 판단을 정량화하기 위해 spectral norm $\|\cdot\|_2$를 사용한다. $v=\|H_{AB}\|_2$, $\Delta=\operatorname{dist}(E_0,\operatorname{spec}H_{BB})$라 정의한다. $v$와 $\Delta$는 에너지 단위이고, $|E-E_0|\le w<\Delta$인 구간을 고려한다. 아래 평가는 문헌의 resolvent 표현에 항등식을 적용해 여기서 유도한 보수적인 bound이다.[1,2]

$$
R_B(E)-R_B(E_0)=(E_0-E)R_B(E)R_B(E_0).
$$

Hermitian $H_{BB}$에 대해 $\|R_B(E_0)\|_2=1/\Delta$이고, 구간 안에서는 $\|R_B(E)\|_2\le1/(\Delta-w)$이다. 따라서 정적 행렬이 버린 항은 다음을 만족한다.[1,2]

$$
\|\Sigma_B(E)-\Sigma_B(E_0)\|_2
\le\frac{v^2w}{\Delta(\Delta-w)}.
$$

이 값은 에너지 단위의 **행렬 보정 오차 상한**이며, 특정 순번의 고유값 오차나 모든 관측량의 오차를 그대로 뜻하지 않는다. 실제 근이 가정한 구간 안에 있는지도 확인해야 한다. $w$가 $\Delta$에 접근하면 bound가 커져 이 정적 근사를 정당화하지 못한다. 중요한 $B$ 상태를 $A$에 포함해 partition을 바꾸거나 에너지 의존성을 유지하는 것이 그때의 선택지이다.[1,2]

에너지 의존성을 조금 더 남기는 방법은 $E_0$ 주위의 일차 전개이다. 이는 pole을 포함하지 않는 근방에서만 사용하며, $\Sigma_0=\Sigma_B(E_0)$와 $\Sigma'_0=\Sigma'_B(E_0)$로 쓰면 다음 근사식을 얻는다.[1,2]

$$
\Sigma_B(E)\simeq\Sigma_0+(E-E_0)\Sigma'_0,
$$

$$
\left(H_{AA}+\Sigma_0-E_0\Sigma'_0\right)c_A
\simeq E\left(I_A-\Sigma'_0\right)c_A.
$$

오른쪽의 $I_A-\Sigma'_0$는 에너지 의존성을 일차까지 옮긴 유효 overlap 역할을 한다. 앞 절의 정확한 정규화 행렬을 기준 에너지에서 평가한 것과 같은 형태이다. 단순히 보정 항을 더한 뒤 축소 계수의 Euclidean norm을 물리적 norm으로 취급하면 이런 차이를 놓친다. 일차 전개도 원래의 유리함수를 모든 에너지에서 재현하는 식은 아니며, 이 문서의 수치 비교에서는 더 단순한 상수 $H_{\mathrm{stat}}$를 사용한다.[1,2]

## 4. Green's function과 self-energy

### (1) Active resolvent

고유값을 직접 구하는 대신 **resolvent** $G(z)=(zI_M-H)^{-1}$를 사용할 수도 있다. $z$는 에너지 단위의 복소수이고, 필요한 역행렬이 존재하는 영역에서 논의한다. 같은 block 제거를 적용하면 전체 resolvent의 $AA$ block은 다음과 같다.[1,3,4]

$$
G_{AA}(z)=\left[zI_A-H_{AA}-\Sigma_B(z)\right]^{-1}.
$$

이 식에서 $G_{AA}$는 전체 계를 풀고 나서 $A$ 성분을 취한 정확한 결과이다. 반면 $A$만 projection한 모델의 Green's function은 $(zI_A-H_{AA})^{-1}$이므로 일반적으로 다르다. 전체 역행렬의 부분 block과 부분 block의 역행렬을 혼동하지 않는 것이 중요하다. 두 계산의 차이는 제거된 공간으로 전달되었다가 되돌아오는 응답이다.[1,3,4]

입력이 $B$에도 작용하면 입력도 함께 제거해야 한다. 선형계 $(zI-H)c=f$에서 $f=(f_A,f_B)^{\mathsf T}$를 우변으로 두면 두 번째 방정식으로부터 다음을 얻는다. 여기서 $f$는 정규화된 상태가 아니라 주어진 외부 입력이며, 이 관계는 고유값 문제의 $f=0$보다 일반적인 block 소거이다.[1,3,4]

$$
\left[zI_A-H_{AA}-\Sigma_B(z)\right]c_A
=f_A+H_{AB}(zI_B-H_{BB})^{-1}f_B.
$$

따라서 유효 행렬만 정확히 만들고 입력의 $B$ 성분을 버리면 원래 응답 문제가 되지 않는다. 출력이 $B$ 성분에 의존할 때도 역대입이 필요하다. 이는 고유에너지 재현, active Green's function 재현, 임의 입력에 대한 전체 관측량 재현이 서로 다른 검증 대상임을 보여준다.[1,3,4]

### (2) 유한계 제거와 열린계 경계조건

위에서 사용한 유한 Hermitian $H_{BB}$의 제거는 닫힌 계의 정확한 재표현이다. 실수 $E$가 $H_{BB}$의 spectrum 밖에 있으면 $\Sigma_B(E)$도 Hermitian이다. 행렬을 작게 썼다는 사실만으로 입자가 외부 reservoir로 빠져나가는 열린계가 된 것은 아니다.[1,2]

수송의 **retarded Green's function**에서는 $z=E+i\eta$, $\eta>0$로 접근한 뒤 $\eta\to0^+$의 경계값을 취한다. 제거할 부분이 반무한 lead이면 그 lead의 경계조건을 포함한 surface Green's function $g_B^r(E)$가 필요하다. 직교 기저에서 contact self-energy는 다음 형태이다. $g_B^r$는 접촉하는 lead 자유도에 제한한 Green's function이고, $H_{AB}$도 그 접촉 block에 대한 coupling이다.[3,4]

$$
\Sigma_B^r(E)=H_{AB}g_B^r(E)H_{BA}.
$$

표면 응답은 유한하게 잘라 놓은 고립 cluster의 역행렬과 동일하지 않다. Lead의 연속 spectrum이 연결되는 에너지에서는 retarded self-energy의 반Hermitian 성분이 중앙 영역에서 lead로 전파되는 열린 경계의 효과를 나타낼 수 있다. 반대로 닫힌 작은 행렬에 임의의 $\eta$를 더해 얻은 폭을 곧바로 물리적인 접촉 수명으로 해석해서는 안 된다. 유한 cluster의 이산 pole을 완만하게 표시하는 계산과 무한 lead의 경계값을 구하는 계산은 구별한다.[2–4]

두 경우의 공통점은 block elimination이라는 대수 구조이며, 차이는 제거 대상의 spectrum과 선택한 경계조건이다. 열린계 계산에서는 lead와 중앙 영역의 정의, 접촉 coupling, 사용한 복소 에너지의 부호가 함께 일관되어야 한다. 이 문서의 세 orbital 예제에는 lead도, 입사 전자도, 전류도 없으므로 그 결과를 transmission이나 contact broadening으로 해석하지 않는다.[3,4]

## 5. 비직교 basis의 확장

### (1) $zS-H$의 block 분할

Atomic orbital (AO) 기저가 비직교이면 출발점은 $Hc=ESc$이다. $S=S^\dagger>0$는 원래 AO overlap이며 무차원이다. 이때 $H$만 직교 기저 식처럼 나누면 overlap coupling을 누락한다. 제거해야 할 대상은 **matrix pencil** $K(z)=zS-H$ 전체이다.[3,4]

$$
K(z)=\begin{pmatrix}
K_{AA}(z)&K_{AB}(z)\\K_{BA}(z)&K_{BB}(z)
\end{pmatrix},
\qquad K_{XY}(z)=zS_{XY}-H_{XY}.
$$

$X,Y$는 $A$ 또는 $B$를 뜻한다. $K_{BB}(z)$가 가역인 곳에서 $K(z)c=0$의 두 번째 식을 풀면 다음과 같다.[3,4]

$$
c_B=-K_{BB}(z)^{-1}K_{BA}(z)c_A.
$$

따라서 active 방정식과 coefficient Green's function은 Schur complement $K_{\mathrm{eff}}$로 표현된다. 여기서 $G(z)=(zS-H)^{-1}$라는 행렬 규약을 사용한다.[3,4]

$$
K_{\mathrm{eff}}(z)=K_{AA}(z)
-K_{AB}(z)K_{BB}(z)^{-1}K_{BA}(z),
\qquad G_{AA}(z)=K_{\mathrm{eff}}(z)^{-1}.
$$

직교 기저와 같은 덧셈형 이름을 쓰려면 $\tau_{AB}(z)=H_{AB}-zS_{AB}$, $\tau_{BA}(z)=H_{BA}-zS_{BA}$로 정의한다. 그러면 제거 보정은 아래와 같다.[3,4]

$$
\Sigma_B(z)=\tau_{AB}(z)(zS_{BB}-H_{BB})^{-1}\tau_{BA}(z),
$$

$$
K_{\mathrm{eff}}(z)=zS_{AA}-H_{AA}-\Sigma_B(z).
$$

두 coupling factor에 **같은 $z$**가 들어간다. $H$와 $S$가 Hermitian이어도 복소 $z$에서는 일반적으로 $\tau_{BA}(z)\ne\tau_{AB}(z)^\dagger$이다. 실제 adjoint는 다음과 같기 때문이다.[3,4]

$$
\tau_{AB}(z)^\dagger=H_{BA}-z^*S_{BA},
\qquad \tau_{BA}(z)=\tau_{AB}(z^*)^\dagger.
$$

실수 $E$에서는 이 차이가 없어지지만, retarded 계산의 유한 $\eta$나 복소 contour에서는 없어지지 않는다. 직교 기저의 익숙한 coupling–Green–coupling adjoint 형태를 비직교 기저 코드에 그대로 옮기지 않아야 하는 이유이다. 예를 들어 $S_{AB}\ne0$이면 $H_{AB}=0$이더라도 $K_{AB}(z)$는 0이 아닐 수 있다. 따라서 비직교 좌표의 Hamiltonian 비대각 원소만 보고 공간이 독립이라고 판단할 수 없다.[3,4]

실수 고유에너지에서 상태를 복원한 뒤에는 원래의 $S$로 정규화한다. 다음은 $c^\dagger Sc=1$의 block 전개이며, 마지막 교차 항에는 두 공간 사이의 overlap이 들어간다.[3,4]

$$
1=c_A^\dagger S_{AA}c_A+c_B^\dagger S_{BB}c_B
+2\operatorname{Re}(c_A^\dagger S_{AB}c_B).
$$

이 경우 $\|c_B\|_2^2$를 그대로 물리적인 orbital 점유 확률로 부르는 것은 적절하지 않다. 아래 예제의 $B$ weight를 단순 제곱으로 읽을 수 있는 이유는 그 예제가 $S=I$인 직교 좌표를 사용하기 때문이다. 상태 norm과 orbital별 전하 분할의 정의를 구별하고, 실제 비직교 AO 계산에서는 사용할 전하 분석 규약을 별도로 정해야 한다.[3,4]

### (2) Löwdin 직교화와 partitioning

**Löwdin symmetric orthogonalization**은 비직교 기저를 직교 기저로 바꾸는 전차원 변환이다. 양의 정부호 $S$의 Hermitian inverse square root를 $S^{-1/2}$라 할 때, 원래 orbital을 열로 모은 $\Phi$는 다음과 같이 바뀐다. 이는 $B$ 계수를 풀어 없애는 Löwdin partitioning과 다른 연산이다.[1,2,5,6]

$$
\widetilde\Phi=\Phi S^{-1/2},
\qquad S^{-1/2}SS^{-1/2}=I_M.
$$

같은 물리적 상태 $\Phi c=\widetilde\Phi\widetilde c$의 계수는 $c=S^{-1/2}\widetilde c$이다. 이를 원래 일반화 고유값 방정식에 대입하고 왼쪽에서 $S^{-1/2}$를 곱하면 다음 표준 문제가 나온다. 아래는 직교화의 변환식을 Hamiltonian에 적용한 직접 유도이다.[5,6]

$$
\widetilde H=S^{-1/2}HS^{-1/2},
\qquad \widetilde H\widetilde c=E\widetilde c.
$$

$S$가 가역이고 모든 열을 유지하면 차원은 $M$으로 같으며, 단순한 좌표변환 때문에 고유값이 사라지지 않는다. 이후에 $\widetilde H$를 $A/B$로 나누어 제거하거나 일부 열만 projection할 수 있지만, 그 단계는 직교화 이후의 별도 선택이다. $S^{-1/2}$가 원래 $A/B$ orbital을 섞으면 변환 뒤의 같은 열 번호가 원래와 같은 물리적 active space를 뜻하지 않을 수도 있다.[1,2,5,6]

또한 작은 overlap 고유값을 잘라내어 $S^{-1/2}$를 만드는 절차는 모든 방향을 보존하는 위 식과 다르다. 그 경우에는 어떤 방향을 버렸는지와 그 영향도 검증해야 한다. 이 문서에서는 선형독립 기저, 양의 정부호 $S$, 전차원 inverse square root만 가정하여 직교화와 제거의 차이를 분명히 한다.[5,6]

## 6. 세 orbital 모형의 검산

### (1) Full·projection·downfolding

다음은 실제 물질의 parameter가 아닌 교육용 tight-binding 행렬이다. 선행 문서와 같은 $S=I_3$, $A=\{1,2\}$, $B=\{3\}$을 사용한다. 에너지의 단위는 eV이며, 코드 안에서는 eV를 단위로 한 수치만 저장한다.

$$
H=\begin{pmatrix}
0&-1&0.3\\-1&0.5&0.4\\0.3&0.4&4
\end{pmatrix}\mathrm{eV},
\qquad
b=\begin{pmatrix}0.3\\0.4\end{pmatrix}\mathrm{eV}.
$$

여기서 $H_{AB}=b$이고 제거한 block은 $H_{BB}=4\,\mathrm{eV}$이다. 앞서 유도한 식을 대입하면 보정은 다음과 같다.[1,2]

$$
H_{\mathrm{eff}}(E)=H_{AA}+\frac{bb^\dagger}{E-4\,\mathrm{eV}}.
$$

즉, diagonal onsite만 바뀌는 것이 아니다. $bb^\dagger$의 비대각 원소도 0이 아니므로 두 active orbital 사이의 유효 coupling도 바뀐다. $E<4\,\mathrm{eV}$에서는 이 보정이 음의 준정부호이고, $E>4\,\mathrm{eV}$에서는 양의 준정부호이다. 이는 이 모형의 단일 제거 orbital과 분모의 부호에서 직접 읽을 수 있는 성질이다.[1,2]

상수 근사에는 $E_0=0\,\mathrm{eV}$를 사용한다. 낮은 두 상태를 비교하기 위한 선택이며, $4\,\mathrm{eV}$ 부근이나 전체 세 상태를 한꺼번에 근사하는 선택은 아니다. 아래 표는 뒤의 코드로 계산한 에너지이다. 정확한 제거 열은 full eigenvalue를 식에 넣어 재확인한 값이 아니라, $\nu_j(E)-E$의 근을 독립적으로 찾아 얻은 결과이다.

| 상태 순번 | Full $3\times3$ (eV) | Projection $2\times2$ (eV) | 정확한 제거 (eV) | 정적 근사 (eV) |
| --- | --- | --- | --- | --- |
| 1 | −0.82909176 | −0.78077641 | −0.82909176 | −0.83912597 |
| 2 | 1.27476220 | 1.28077641 | 1.27476220 | 1.27662597 |
| 3 | 4.05432956 | 해당 없음 | 4.05432956 | 해당 없음 |

Projection의 첫 번째 에너지 오차는 약 $0.04831535\,\mathrm{eV}$이고 정적 근사의 오차는 약 $0.01003422\,\mathrm{eV}$이다. 두 번째 상태의 오차도 이 예제에서는 줄어든다. 그러나 상수 보정을 썼다고 항상 모든 상태가 개선된다는 결론은 이 한 예제로 얻을 수 없다. 정확한 제거는 세 근을 재현하지만, 정적 $2\times2$ 행렬은 두 고유값만 준다는 차이가 핵심이다.

근 찾기에서는 고유값 가지를 오름차순 $j=0,1$로 표시한다. 구간과 가지는 각각 $(j,[E_l,E_h])=(0,[-2,0]),(1,[0,2]),(1,[4.0001,6])$로 정한다. 모든 경계값은 eV 단위이고 어떤 구간도 pole인 $E=4$를 가로지르지 않는다. 각 구간에서 함수 부호가 바뀌는지 먼저 확인한 뒤 이분법으로 근을 좁힌다. 이 구간 선택은 이 작은 모형에 맞춘 것으로, 임의 대형 문제의 모든 근을 자동으로 탐색하는 알고리즘은 아니다.

### (2) 상태 복원과 수치적 한계

각 근에서 $H_{\mathrm{eff}}(E)$의 대응 고유벡터 $a$를 구하고 $c_B=b^\dagger a/(E-4\,\mathrm{eV})$를 복원한다. 그 뒤 전체 $c=(a,c_B)^{\mathsf T}$를 정규화한다. 비교할 지표는 전체 residual의 norm과 $B$ weight이다. 이 지표의 식은 앞의 정확한 복원과 정규화 관계를 모형에 적용한 것이다.[1,2]

$$
\eta_{\mathrm{res}}=\|Hc-Ec\|_2,
\qquad p_B=|c_3|^2,\qquad c^\dagger c=1.
$$

$\eta_{\mathrm{res}}$는 에너지 단위이고 $p_B$는 무차원이다. 아래 코드는 NumPy만 사용하며, 전체 대각화는 끝에서 검증에만 사용한다. 실제 큰 block의 구현에서는 명시적인 inverse보다 선형계 solve로 역행렬의 작용을 구할 수 있다. 여기서는 $B$가 한 차원이므로 나눗셈으로 동일한 연산을 수행한다.[1–4]

```python
import numpy as np

H = np.array([[0., -1., .3], [-1., .5, .4], [.3, .4, 4.]])
A, b, d = H[:2, :2], H[:2, 2], H[2, 2]
E0 = 0.0

def heff(E):
    return A + np.outer(b, b) / (E - d)

def branch(E, j):
    return np.linalg.eigvalsh(heff(E))[j] - E

def bisect(j, lo, hi):
    assert not (lo <= d <= hi)
    flo, fhi = branch(lo, j), branch(hi, j)
    assert flo * fhi < 0.0
    for _ in range(100):
        mid = (lo + hi) / 2.0
        if mid == lo or mid == hi:
            return mid
        fm = branch(mid, j)
        if fm == 0.0:
            return mid
        if flo * fm < 0.0:
            hi = mid
        else:
            lo, flo = mid, fm
    return (lo + hi) / 2.0

roots, states = [], []
for j, lo, hi in [(0, -2., 0.), (1, 0., 2.), (1, 4.0001, 6.)]:
    E = bisect(j, lo, hi)
    _, U = np.linalg.eigh(heff(E))
    a = U[:, j]
    c = np.r_[a, (b @ a) / (E - d)]
    c /= np.linalg.norm(c)
    roots.append(E)
    states.append(c)
roots, states = np.array(roots), np.column_stack(states)
res = np.linalg.norm(H @ states - states * roots, axis=0)

full, C = np.linalg.eigh(H)
proj, P = np.linalg.eigh(A)
stat, Q = np.linalg.eigh(heff(E0))
# Static eigenstates use the actual candidate energy for back-substitution.
stat_res = []
for E, a in zip(stat, Q.T):
    c = np.r_[a, (b @ a) / (E - d)]
    c /= np.linalg.norm(c)
    stat_res.append(np.linalg.norm(H @ c - E * c))

assert np.allclose(roots, full, atol=1e-12, rtol=0)
assert np.max(res) < 1e-12
assert np.allclose(states.T @ states, np.eye(3), atol=1e-12)
assert np.allclose(np.abs(C.T @ states), np.eye(3), atol=1e-12)
np.set_printoptions(precision=8, suppress=True)
print("full", full)
print("projection", proj)
print("nonlinear roots", roots)
print("static E0=0", stat)
print("projection residuals", np.abs(b @ P))
print("static restored residuals", np.array(stat_res))
print("B weights", states[2] ** 2)
print("normalized norms", np.linalg.norm(states, axis=0))
print("max exact residual < 1e-12", np.max(res) < 1e-12)
```

이 코드의 결과는 다음과 같다. 전체 고유벡터와 복원 고유벡터의 부호가 달라도 절댓값 overlap 비교에는 영향을 주지 않는다.

```text
full [-0.82909176  1.2747622   4.05432956]
projection [-0.78077641  1.28077641]
nonlinear roots [-0.82909176  1.2747622   4.05432956]
static E0=0 [-0.83912597  1.27662597]
projection residuals [0.48262652 0.13065851]
static restored residuals [0.01043006 0.00743701]
B weights [0.00992203 0.00211403 0.98796394]
normalized norms [1. 1. 1.]
max exact residual < 1e-12 True
```

첫 두 상태의 $B$ weight가 작아도 0은 아니며, projection에서는 그 성분을 아예 버린다. 세 번째 상태는 대부분 $B$에 놓여 있지만 coupling 때문에 $A$ 성분도 있어 $E\ne4\,\mathrm{eV}$의 비선형 근으로 찾을 수 있다. 정확한 제거가 그 상태를 재현하는 사실과, 낮은 두 상태용 정적 모델이 그 상태를 표현하지 않는 사실은 양립한다.

정적 근사의 residual은 그 고유에너지 $\theta$를 사용해 $B$를 역대입한 뒤 계산했다. 그러면 $B$ 방정식은 만족하지만 $A$ 방정식에는 $[\Sigma_B(\theta)-\Sigma_B(E_0)]a$가 남는다. 반대로 복원에도 $E_0$를 사용하면 다른 근사 상태가 되므로 residual도 달라진다. 검증할 때는 에너지뿐 아니라 어떤 복원 규칙으로 상태를 만들었는지 밝혀야 한다.[1,2]

계산 비용도 분리해서 판단한다. 이 예제에서는 제거한 block이 scalar라서 $\Sigma_B$를 만드는 비용이 작다. 일반적인 큰 $B$에서는 각 에너지의 선형계 풀이, nonlinear root 탐색, 필요한 상태의 역대입 비용이 남는다. 작은 effective Hamiltonian을 얻었다는 사실만으로 전체 계산이 빨라졌다고 결론내리지 않는다. 반복 에너지 평가에서 재사용할 구조가 있는지, 필요한 근이 몇 개인지, 어떤 관측량을 복원하는지에 따라 비용을 비교한다.[1–3]

마지막으로 이 검산은 고정된 $H$의 spectrum과 상태만 다룬다. Density functional theory (DFT)의 self-consistent field (SCF) 계산에서는 점유된 상태로부터 밀도를 계산하고, 그 밀도에 의존하는 Hamiltonian을 서로 일관되게 갱신한다. 따라서 좁은 energy window에서 고정 $H$의 몇 고유값이 정확하다는 결과만으로 SCF 수렴, 전체 전하, 힘의 정확성을 인증할 수 없다는 것이 이로부터의 결론이다. 그 목적에는 해당 관측량과 갱신된 조건을 별도로 검증해야 한다.[3,4]

## 7. 요약

- Coordinate projection은 $c_B=0$으로 제한하지만, downfolding은 $c_B$를 풀어 $H_{AB}(EI_B-H_{BB})^{-1}H_{BA}$를 남긴다.
- 정확한 제거는 가역성 조건 아래 원래 고유값 문제와 동치이다. 에너지 의존성, pole, 별도로 확인할 $A$ 성분 0인 상태를 함께 다룬다.
- $r\times r$ effective Hamiltonian도 에너지 의존 nonlinear 문제에서는 $r$개보다 많은 근을 가질 수 있다. 전체 상태의 역대입과 정규화가 필요하다.
- 정적 근사는 관심 에너지 구간과 제거 spectrum의 거리를 확인해 사용한다. 유한계 제거와 반무한 lead의 retarded self-energy는 같은 경계조건을 뜻하지 않는다.
- 비직교 기저에서는 $zS-H$ 전체를 분할하고 두 coupling factor에 같은 $z$를 쓴다. Löwdin 직교화는 전차원 기저변환이며 제거와 별개이다.
- 계산 속도와 전하·힘·SCF 정확도는 작은 행렬의 크기나 일부 에너지의 일치만으로 판단하지 않는다.

## 8. 참고문헌

1. N. Marzari, A. A. Mostofi, J. R. Yates, I. Souza, and D. Vanderbilt, “Maximally localized Wannier functions: Theory and applications,” *Reviews of Modern Physics* **84**, 1419–1475 (2012). [DOI: 10.1103/RevModPhys.84.1419](https://doi.org/10.1103/RevModPhys.84.1419). [Author preprint](https://arxiv.org/pdf/1112.5411), §III.B.2, Eqs. (68)–(72).
2. G. Dusson, I. M. Sigal, and B. Stamm, “The Feshbach-Schur map and perturbation theory,” arXiv:2105.02058 (2021). [Full text](https://arxiv.org/pdf/2105.02058), Theorem 1.2, Corollary 1.3, Eqs. (1.10)–(1.16), Proposition 2.2.
3. T. Ozaki, K. Nishio, and H. Kino, “Efficient implementation of the nonequilibrium Green function method for electronic transport calculations,” arXiv:0908.4142 (2009). [Full text](https://arxiv.org/pdf/0908.4142), §§II.A–D, Eqs. (2)–(8), Appendix B.
4. M. Brandbyge, J.-L. Mozos, P. Ordejón, J. Taylor, and K. Stokbro, “Density-functional method for nonequilibrium electron transport,” *Physical Review B* **65**, 165401 (2002). [DOI: 10.1103/PhysRevB.65.165401](https://doi.org/10.1103/PhysRevB.65.165401). [Author preprint](https://arxiv.org/pdf/cond-mat/0110650), §§II–III, Eqs. (7)–(15), §IV.B, §VI.B.4.
5. A. R. Naidu, “Centrality of Löwdin orthogonalizations,” arXiv:1105.3571 (2011). [Full text](https://arxiv.org/pdf/1105.3571), Eqs. (1)–(7).
6. G. Torun, “Coherence, superposition, and Löwdin symmetric orthogonalization,” arXiv:2209.03746 (2022; revised 2023). [Full text](https://arxiv.org/pdf/2209.03746), §§II.A–B, Eqs. (1), (3)–(5).
