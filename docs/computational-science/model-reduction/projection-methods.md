---
description: Trial·test 공간의 잔차 조건으로 선형계·동역학·고유값 문제를 축소하고 가중 내적, 안정성, 전체 잔차와 기저 보강을 구분한다.
---

# Projection methods

Projection method는 해를 작은 trial space에서 찾으면서, 원래 방정식의 잔차가 선택한 test space에 직교하도록 정하는 방법이다. Trial space는 표현할 수 있는 상태를, test space는 반드시 만족시킬 방정식의 조합을 결정한다. 두 공간이 같으면 Galerkin, 다르면 Petrov–Galerkin이라 한다. 축소 방정식을 정확히 풀어도 원래 방정식의 잔차 전체가 사라지는 것은 아니다.[1,2]

기저변환과 차원 축소의 차이는 [Model reduction fundamentals](fundamentals.md), 표본으로부터 작은 공간을 얻는 문제는 [Low-rank approximation](low-rank-approximation.md)을 따른다. 여기서는 기저를 이미 정했다고 가정하고, 그 기저로 어떤 방정식을 만들며 언제 해석을 신뢰할 수 있는지 설명한다. 유한차원 선형계, 시간에 무관한 선형 동역학, Hermitian 일반화 고유값 문제가 범위이다. 비선형 잔차 최소화나 특정 기저 생성 알고리즘은 다루지 않는다.

## 1. Trial space와 test space

### (1) 상태 제한과 잔차 조건

원래 상태를 $x\in\mathbb C^n$, 축소 차원을 $r<n$이라 하자. 열독립 행렬 $V,W\in\mathbb C^{n\times r}$가 각각 trial basis와 test basis이고, $a\in\mathbb C^r$는 계산할 축소 좌표이다. $\dagger$는 켤레전치이며 실수에서는 전치이다. 먼저 Euclidean 내적을 사용한다. 근사 상태 $\widetilde x$, 두 부분공간 $\mathcal V,\mathcal W$와 잔차 벡터 $\rho\in\mathbb C^n$의 관계는 다음과 같다.[1,2]

$$
\widetilde x=Va\in\mathcal V=\operatorname{range}(V),\qquad
\mathcal W=\operatorname{range}(W),\qquad W^\dagger\rho=0.
$$

첫 조건은 미지수 수를 $n$에서 $r$로 줄인다. 마지막 조건은 $r$개의 방정식을 부여한다. 잔차의 정의는 원래 문제에 따라 달라지지만, 모든 test vector $w\in\mathcal W$에 대해 $w^\dagger\rho=0$이라는 의미는 같다. $W$가 열독립이어도 잔차가 축소 좌표에 의존하는 방식에 따라 축소 방정식이 특이해질 수 있다. 따라서 두 기저의 열 개수를 맞추는 것만으로 해의 존재와 유일성을 확보하지는 못한다.[1,2]

예를 들어 원래 좌표마다 하나씩 방정식이 있다면, $W^\dagger$의 각 행은 원방정식들의 가중 조합을 만든다. 선택한 $r$개 조합에서 잔차가 상쇄되어도 나머지 조합에는 불일치가 남을 수 있다. 이 설명은 잔차를 작게 만드는 알고리즘의 성능 가정이 아니라 위 직교 조건 자체의 의미이다.[1,2]

### (2) 기저와 공간의 구별

Galerkin의 본질은 $\mathcal W=\mathcal V$이며, 계산에서는 보통 $W=V$로 둔다. 서로 다른 행렬이라도 같은 열공간을 가지면 같은 잔차 조건을 표현할 수 있다. 가역 행렬 $T_v,T_w\in\mathbb C^{r\times r}$로 기저를 바꾸었을 때 다음 관계가 성립한다.[1,2]

$$
V'=VT_v,\qquad W'=WT_w,\qquad
Va=V'a',\quad a'=T_v^{-1}a,\qquad
W'^\dagger\rho=T_w^\dagger W^\dagger\rho.
$$

따라서 위 식에서 정확한 산술의 복원 상태와 잔차 조건이 기저 좌표변환에 불변임을 알 수 있다.[1,2] 반면 행렬의 조건수와 반올림 오차는 기저 선택의 영향을 받는다. 거의 같은 snapshot을 그대로 열로 넣으면 공간의 유효 차원에 비해 좌표 표현이 불안정해질 수 있으므로, 공간 선택과 기저의 수치적 정리를 구분한다.[1,3]

| 선택 | trial space | test space | 직접 강제하는 내용 |
| --- | --- | --- | --- |
| Galerkin | $\mathcal V$ | $\mathcal V$ | 잔차가 해를 찾는 공간에 직교 |
| Petrov–Galerkin | $\mathcal V$ | 별도로 정한 $\mathcal W$ | 잔차가 지정한 제약 공간에 직교 |
| 전체 차원의 가역 기저 | 원공간 전체 | 원공간 전체 | 잔차 전체가 0 |

마지막 행은 비교를 위한 $r=n$의 극한이다. 전체 차원에서는 열독립 $W$가 가역이므로 $W^\dagger\rho=0$에서 $\rho=0$이 따라온다. 실제 축소에서는 이 추론을 사용할 수 없다.[1,2]

## 2. 선형계의 축소와 최적성

### (1) 축소 연산자와 가역성

가역 행렬 $K\in\mathbb C^{n\times n}$와 우변 $b\in\mathbb C^n$에 대한 정적 문제 $Kx=b$를 고려한다. 정적 잔차는 $\rho=b-KVa$로 정의한다. Petrov–Galerkin 조건을 대입하면 작은 선형계를 얻는다.[1,2]

$$
K_r a=b_r,\qquad K_r=W^\dagger KV,\qquad b_r=W^\dagger b.
$$

$K_r$는 $r\times r$이지만 $K$의 일부 행과 열을 단순히 잘라낸 행렬일 필요는 없다. Trial vector에 대한 $K$의 작용을 test vector로 읽어 얻은 행렬이다. $K_r$가 가역이면 $a$가 유일하며, 실제 계산에서는 역행렬을 만들기보다 작은 선형계를 푼다. 특정 기준 상태 $x_{\mathrm{ref}}$ 주위의 보정만 구한다면 $\widetilde x=x_{\mathrm{ref}}+Va$로 바꾸고 우변을 $W^\dagger(b-Kx_{\mathrm{ref}})$로 대체한다.[1,2]

위 축소식만으로 원래 $K$의 가역성에서 $K_r$의 가역성을 추론할 수는 없다. 다음 무차원 행렬을 직접 대입하면 이를 확인할 수 있다. 이 반례에서는 $K$의 determinant가 $-1$이지만, 첫 좌표만 남기는 Galerkin 행렬은 0이다. 이는 기저 수가 부족해서 생기는 오차 이전에, 축소 방정식이 해를 결정하지 못하는 경우이다.[1,2]

$$
K=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
V=W=\begin{pmatrix}1\\0\end{pmatrix},\qquad K_r=0.
$$

위 축소식의 영공간을 살펴보면 가역성 조건을 직접 유도할 수 있다. 기하학적으로는 $K\mathcal V$ 안에 $\mathcal W$에 직교하는 비영 벡터가 있으면 test 조건이 그 방향의 계수를 결정하지 못한다. 열독립 $V,W$와 가역 $K$에 대해 다음 조건이 정확히 대응한다.[1,2]

$$
K_r\text{가 가역}\quad\Longleftrightarrow\quad
K\mathcal V\cap\mathcal W^\perp=\{0\}.
$$

여기서 $K\mathcal V=\{Kv:v\in\mathcal V\}$이다. $K_rc=0$인 $c\ne0$가 있으면 $V$의 열독립성과 $K$의 가역성으로 $KVc\ne0$이며, $W^\dagger KVc=0$이므로 그 벡터가 교집합에 속한다. 역으로 교집합의 비영 벡터를 $KVc$로 쓰면 $c\ne0$이고 $K_rc=0$이다. 따라서 양쪽의 특이성 조건이 서로 동치이다.[1,2]

교집합이 정확히 0이어도 두 공간의 배치가 거의 특이한 경우에는 수치적 민감도가 크다. 같은 축소식에 대한 역연산 민감도를 적용하면 다음 해석을 얻는다. 기저들을 각각 Euclidean 정규직교화한 상태에서 $\sigma_{\min}(W^\dagger KV)$가 작으면, 축소 우변의 오차가 큰 좌표 오차로 증폭될 수 있다. 기저를 임의로 스케일한 경우에는 이 특이값의 크기만으로 공간의 양호함을 비교하지 않는다.[1,2]

### (2) Galerkin의 에너지 최적성

$K=K^\dagger\succ0$인 Hermitian positive definite 문제에서는 $W=V$가 특별한 보장을 준다. $\succ0$는 모든 비영 벡터에 대한 이차형식이 양수라는 뜻이다. 열독립성으로 $Va\ne0$이므로 축소 행렬도 양의 정부호이다.[1,3]

$$
a^\dagger K_r a=(Va)^\dagger K(Va)>0\qquad(a\ne0).
$$

상태 오차를 $e=x-Va$, 에너지 노름을 $\|z\|_K=(z^\dagger Kz)^{1/2}$라 하자. $Ke=\rho$와 Galerkin 조건을 결합하면 $V^\dagger Ke=0$이다. 따라서 해 오차는 $K$가 정의하는 내적에서 trial space와 직교한다. 임의의 다른 좌표 $c\in\mathbb C^r$에 대해 다음 분해가 성립한다.[1,3]

$$
\|x-Vc\|_K^2
=\|x-Va\|_K^2+\|V(a-c)\|_K^2,
\qquad
\|x-Va\|_K=\min_c\|x-Vc\|_K.
$$

이는 선택한 공간에서 가능한 최선의 에너지 오차를 얻는다는 뜻이다. Euclidean 상태 오차, 잔차의 Euclidean 노름, 특정 출력 오차를 동시에 최소화한다는 뜻은 아니다. 특히 $K$가 양의 정부호가 아니면 위 제곱근은 노름이 아닐 수 있어, 같은 논증을 옮길 수 없다.[1,3]

잔차의 Euclidean 노름을 최소화하려면 다른 test space가 자연스럽다. $K$가 가역일 때 $KV$도 열독립이고, $b$를 $K\mathcal V$에 직교 투영하는 최소제곱 조건은 다음과 같다. 이 식은 앞의 직교 투영 성질을 잔차 문제에 적용해 얻는다.[1,3]

$$
a\in\operatorname*{arg\,min}_c\|b-KVc\|_2
\quad\Longleftrightarrow\quad
(KV)^\dagger(b-KVa)=0.
$$

이를 직접 확인하려면 $\rho=b-KVa$와 임의의 좌표 변화 $d\in\mathbb C^r$를 사용한다. $\|\rho-KVd\|_2^2$를 전개하면 교차항은 $-2\operatorname{Re}(d^\dagger(KV)^\dagger\rho)$이다. 최소점에서는 모든 방향의 일차 변화가 0이므로 $(KV)^\dagger\rho=0$이다. 반대로 이 조건이면 변화 뒤의 잔차 제곱은 $\|\rho\|_2^2+\|KVd\|_2^2$이므로 더 작아질 수 없다. 이는 해당 직교 투영의 최적성을 대수적으로 확인한 것이다.[1,3]

즉 $W=KV$를 선택한 Petrov–Galerkin은 이 정적 선형 문제의 잔차 최소제곱과 일치한다. 그러나 임의의 $W$를 사용하는 모든 Petrov–Galerkin이 최소제곱법인 것은 아니다. 이 잔차 최소화도 상태 오차를 최소화하는 것은 아니다. 잔차를 상태 오차로 바꾸는 역연산의 영향을 함께 고려해야 한다.[1,3]

## 3. 가중 내적과 overlap

### (1) 알려진 벡터의 직교 투영

상태의 각 성분이 다른 물리적 가중치를 갖거나 원래 좌표 기저가 비직교이면, Euclidean 내적 대신 양의 정부호 행렬 $S=S^\dagger\succ0$가 정하는 내적을 사용할 수 있다. 이 절의 $S$는 $n\times n$ 원공간 행렬이다. 두 벡터 $z_1,z_2$와 상태의 노름을 다음처럼 정한다.[1,3]

$$
\langle z_1,z_2\rangle_S=z_1^\dagger Sz_2,\qquad
\|z_1\|_S^2=z_1^\dagger Sz_1,\qquad S_r=V^\dagger SV.
$$

$S_r$는 $r\times r$ 축소 overlap이며 $V$의 열독립성 때문에 양의 정부호이다. 선행 fundamentals 문서의 $S=V^\dagger V$는 그 문서에서만 쓰는 축소 overlap 기호이다. 이 문서에서는 원공간 $S=I_n$을 대입한 $S_r=V^\dagger V$가 그 행렬에 해당한다. 동역학의 질량 행렬 $E$와도 기호를 구별하며, 물리적 정의가 같다고 확인한 경우에만 두 행렬을 동일시한다.[1,3]

이미 알려진 상태 $x$에 가장 가까운 $Va$를 $S$-norm에서 찾으면 $V^\dagger S(x-Va)=0$이다. 최적 좌표 $a_{\mathrm{best}}$와 원공간 투영 연산자 $P_S$는 다음과 같다.[1,3]

$$
a_{\mathrm{best}}=S_r^{-1}V^\dagger Sx,\qquad
P_S=VS_r^{-1}V^\dagger S,\qquad x_{\mathrm{best}}=P_Sx.
$$

이 식은 알려진 벡터를 작은 공간으로 옮기는 식이다. 원래 해 $x$를 모르는 상황에서 축소 방정식의 해 $Va$를 계산하는 절차와는 다르다. 정적 Galerkin 해의 최적 노름이 $K$-norm이었던 사실도 이 구별을 보여 준다. 표현에 쓰는 내적 $S$와 방정식에서 생기는 에너지 내적 $K$가 같아야 하는 것은 아니다.[1,3]

가중 직교 투영은 다음 성질을 갖는다. 첫 식은 두 번 투영해도 달라지지 않음을, 두 번째 식은 $S$ 내적에서 자기수반임을 뜻한다. Euclidean 좌표의 행렬 자체가 Hermitian일 필요는 없다.[1,3]

$$
P_S^2=P_S,\qquad P_S^\dagger S=SP_S,\qquad
V^\dagger S(I_n-P_S)x=0.
$$

$S_r=I_r$인 $S$-정규직교 기저에서도 $P_S=VV^\dagger S$이다. 마지막 $S$를 빠뜨리면 다른 내적의 투영이 된다. 반대로 비직교 기저를 그대로 사용할 때 $S_r^{-1}$를 빠뜨리면 기저 길이와 중복에 대한 보정이 사라진다.[1,3]

### (2) Test 조건에 포함되는 내적

벡터 잔차 $\rho$를 $S$ 내적에서 trial space에 직교시키는 조건은 $V^\dagger S\rho=0$이다. 이 조건을 앞의 Euclidean 행렬 형식으로 쓰면 $W=SV$인 Petrov–Galerkin과 같다. 따라서 Galerkin인지 판단할 때에는 내적까지 명시해야 한다.[1,3]

$$
\langle Vc,\rho\rangle_S=0\quad\text{for all }c
\quad\Longleftrightarrow\quad
V^\dagger S\rho=0=(SV)^\dagger\rho.
$$

그러나 이미 weak form으로 조립한 방정식의 왼쪽에 언제나 $S$를 추가하는 것은 아니다. Weak form은 시험함수와 연산자 작용을 짝지어 행렬 원소를 만든 표현이다. 그 행렬에 내적 정보가 이미 들어 있다면, 이를 좌표 벡터에 작용하는 연산자와 구별해야 한다. 뒤의 일반화 고유값 절에서 두 표현이 어떻게 같은 식을 만드는지 확인한다.[1,3]

기저를 정리하려면 $S_r=L_rL_r^\dagger$인 Cholesky factor $L_r$을 구하고, $Q=VL_r^{-\dagger}$로 바꿀 수 있다. 여기서 $L_r^{-\dagger}=(L_r^\dagger)^{-1}$이다. 다음 식은 같은 공간에서 $S$-정규직교 기저를 얻음을 보여 준다.[1,3]

$$
Q^\dagger SQ=L_r^{-1}S_rL_r^{-\dagger}=I_r,
\qquad \operatorname{range}(Q)=\operatorname{range}(V).
$$

이는 정확한 산술의 관계이다. $S_r$가 매우 나쁘게 조건화되어 있으면 이미 거의 종속인 열들이 있다는 신호일 수 있으므로, 작은 고유값을 무조건 역수로 바꾸지 않는다. 열의 제거 여부와 허용오차를 정하고 기저 rank를 확인한 뒤 직교화를 수행한다. 이 처리는 수치적 표현을 개선하지만, 선택 공간 밖의 물리적 방향을 새로 추가하지는 않는다.[1,3]

## 4. 선형 동역학과 입출력

### (1) 질량 행렬을 포함한 축소 모형

시간 $t$에 대해 $x(t)$가 상태, $u(t)\in\mathbb C^m$가 입력, $y(t)\in\mathbb C^p$가 출력인 선형 모형을 정하자. $E,A\in\mathbb C^{n\times n}$, $B\in\mathbb C^{n\times m}$, $C\in\mathbb C^{p\times n}$는 시간에 무관하다. 이 절은 $E$가 가역인 경우만 다루며, 직접 전달항이 없는 출력 $Cx$를 사용한다.[2,4]

$$
E\dot x=Ax+Bu,\qquad y=Cx,\qquad x(0)=x_0.
$$

$E$는 질량 또는 저장 항의 계수를 나타내는 행렬이다. 수학적으로 $E^{-1}A$를 사용해 표준형으로 바꿀 수 있지만, 실제 계산에서 큰 역행렬을 명시적으로 만들 필요는 없다. 또한 원래 $E$가 가역이라는 조건과 축소된 질량 행렬이 가역이라는 조건은 별개이다.[2,4]

고정된 $V$에 $\widetilde x=Va$를 대입하고, 동적 잔차를 $\rho_t=AVa+Bu-EV\dot a$로 정한다. $W^\dagger\rho_t=0$을 적용하면 reduced-order model (ROM)을 얻는다.[2,4]

$$
E_r\dot a=A_ra+B_ru,\qquad \widetilde y=C_ra,
\qquad
E_r=W^\dagger EV,\quad A_r=W^\dagger AV,\quad
B_r=W^\dagger B,\quad C_r=CV.
$$

출력은 근사 상태를 원래 관측 연산자에 넣어 구하므로 왼쪽에 $W^\dagger$가 붙지 않는다. 입력과 출력의 개수 $m,p$도 그대로이다. 줄어드는 것은 내부 상태 좌표이며, 출력 정의를 함께 축소하거나 바꾸는 것이 아니다. $E_r$가 가역일 때 축소 초기값 문제를 보통 미분방정식으로 풀 수 있고, 특이하다면 아래 해석의 적용 조건을 벗어난다.[2,4]

| 원래 행렬 | 축소 행렬 | 크기 | 확인할 내용 |
| --- | --- | --- | --- |
| $E$ | $W^\dagger EV$ | $r\times r$ | 가역성과 질량 항의 의미 |
| $A$ | $W^\dagger AV$ | $r\times r$ | 시간 변화와 안정성 |
| $B$ | $W^\dagger B$ | $r\times m$ | 원래 입력 채널의 유지 |
| $C$ | $CV$ | $p\times r$ | 원래 출력과 같은 관측량 |

초기조건은 방정식 투영과 별도로 지정한다. 상태의 초기 표현 오차를 $S$-norm에서 최소화하려면 다음 값을 사용한다. $x_0\in\mathcal V$이면 정확한 초기 상태를 복원하고, 그렇지 않으면 초기 오차가 남는다.[2,3]

$$
a(0)=S_r^{-1}V^\dagger Sx_0,\qquad
x_0-Va(0)=(I_n-P_S)x_0.
$$

$E_r=I_r$를 가정할 수 있는지도 기저에 달려 있다. 예를 들어 $E=I_n$, $W=V$라도 $V^\dagger V\ne I_r$이면 $E_r$가 남는다. 기저 길이를 바꾸면서 질량 행렬을 버리면 물리적 시간 척도까지 달라질 수 있다. 고정 행렬에서는 네 축소 행렬을 사전 계산할 수 있지만, 매개변수가 바뀌면 해당 연산자와 유효 기저를 다시 평가해야 한다.[2,4]

### (2) 안정성 보존의 조건과 한계

안정적인 원래 동역학이 항상 안정적인 ROM을 주는 것은 아니다. 이 문서에서 점근 안정성은 입력을 0으로 두었을 때 모든 초기 상태가 장시간 뒤 0으로 수렴한다는 뜻이다. 가역 $E$를 갖는 유한차원 선형 모형에서는 $E^{-1}A$의 모든 고유값의 실수부가 음수인 조건과 같다. 일반 Galerkin 투영만으로 이 조건이 보존되지는 않는다.[4,5]

반면 $E=E^\dagger\succ0$, $A+A^\dagger\prec0$, $W=V$이면 모든 열독립 $V$에 대해 안정성을 보존한다. $\prec0$는 음의 정부호를 뜻한다. 무입력 축소해의 에너지 $\mathcal E_r=\tfrac12a^\dagger E_ra$를 미분하면 다음 관계를 얻는다.[4,5]

$$
E_r=V^\dagger EV\succ0,\qquad
\frac{d\mathcal E_r}{dt}
=\frac12a^\dagger V^\dagger(A+A^\dagger)Va<0
\quad(a\ne0).
$$

즉 에너지가 모든 비영 방향에서 엄격히 감소하는 구조가 부분공간에서도 유지된다. 이 조건은 충분조건이다. 고유값이 안정 영역에 있다는 정보만으로 $A+A^\dagger\prec0$가 따라오지는 않으며, 특정 내적에서 감소하는 에너지가 있다는 사실을 다른 내적의 Galerkin에 그대로 적용할 수도 없다.[4,5]

다음은 그 차이를 보여 주도록 구성한 무차원 반례이다. $E=I_2$이고 원행렬의 고유값은 삼각형 구조로부터 $-1,-2$이다. 그러나 표시한 하나의 정규화된 방향에 Galerkin 투영하면 양의 성장률을 얻는다.[4,5]

$$
A=\begin{pmatrix}-1&4\\0&-2\end{pmatrix},\qquad
V=W=\frac1{\sqrt2}\begin{pmatrix}1\\1\end{pmatrix},\qquad
E_r=1,\quad A_r=\frac12.
$$

따라서 이 ROM의 무입력 응답은 $a(t)=a(0)\exp(t/2)$로 증가한다. 이는 실험적 관찰이 아니라 위 행렬의 직접 계산 결과이다. 안정성이 중요한 문제에서는 기저의 표본 표현 오차와 함께 축소 행렬쌍의 고유값이나 에너지 구조를 검사해야 한다. 단지 $r$을 늘리는 것으로 모든 중간 차원의 안정성이 보장되지는 않는다.[4,5]

## 5. 일반화 고유값 문제와 Rayleigh–Ritz

### (1) 두 행렬의 일관된 축소

Hermitian 행렬 $H=H^\dagger$와 양의 정부호 overlap $S$로 이루어진 문제 $H\psi=\lambda S\psi$를 고려한다. $\psi\in\mathbb C^n$는 고유벡터, $\lambda$는 정확한 고유값이다. Ritz vector를 $\widetilde\psi=Vz$로 두고, $z\in\mathbb C^r$와 Ritz value $\theta$를 함께 구한다. 잔차 $\rho_\lambda=HVz-\theta SVz$에 Galerkin 조건을 적용하면 다음 작은 일반화 고유값 문제를 얻는다.[6,7]

$$
H_rz=\theta S_rz,\qquad
H_r=V^\dagger HV,\qquad S_r=V^\dagger SV,\qquad
z^\dagger S_rz=1.
$$

마지막 식은 $\widetilde\psi^\dagger S\widetilde\psi=1$이라는 원래 정규화의 축소 표현이다. $H_r$는 Hermitian이고 $S_r$는 양의 정부호이므로 Ritz value는 실수이다. $S_r=I_r$인 기저를 사용하면 표준 Hermitian 문제로 단순해진다. $V$가 Euclidean 정규직교라는 사실만으로 $S_r=I_r$라고 둘 수는 없다.[6,7]

이 절의 $H$를 weak form의 행렬로 해석하면 $H_{ij}$는 원래 기저함수 사이에서 연산자를 평가한 행렬 원소이다. 상태의 좌표 벡터에 직접 작용하는 연산자는 $\mathcal L=S^{-1}H$이다. 그 벡터 잔차에 $S$-Galerkin을 적용하는 과정은 다음과 같다.[6,7]

$$
V^\dagger S(\mathcal LVz-\theta Vz)=0
\quad\Longleftrightarrow\quad
V^\dagger HVz=\theta V^\dagger SVz.
$$

이 유도에서 $S$는 한 번만 들어간다. 이미 $H\psi=\lambda S\psi$ 형태인 weak-form 행렬쌍에 $V^\dagger S$를 다시 곱하면 보통 다른 축소 문제를 만든다. 가중 벡터 투영식의 $S$와 weak-form 행렬의 내적을 중복 적용하지 않는 것이 핵심이다. 행렬 이름이 Hamiltonian이나 stiffness matrix라는 이유만으로 표현을 추정하지 말고, 원소 정의를 확인한다.[6,7]

### (2) Ritz value와 전체 잔차

축소 고유값 식에 $z^\dagger$를 곱하면 Rayleigh quotient를 얻는다. 정규화하지 않은 비영 $z$에도 분모를 유지하면 다음 식이 성립한다.[6,7]

$$
\theta=\frac{z^\dagger H_rz}{z^\dagger S_rz}
=\frac{(Vz)^\dagger H(Vz)}{(Vz)^\dagger S(Vz)}.
$$

이 비는 선택한 공간에서 얻은 고유상태 후보의 값이다. 작은 행렬의 고유값 계산이 잘 수렴했다는 사실과 원문제의 고유벡터를 잘 찾았다는 사실은 다르다. $V^\dagger\rho_\lambda=0$은 축소 공간 안에서의 조건이며, $\rho_\lambda$ 전체의 크기는 여전히 검사해야 한다.[6,7]

$S=L_SL_S^\dagger$로 두면 원문제는 Hermitian 표준형으로 바뀐다. $\phi=L_S^\dagger\widetilde\psi$와 $\widehat H=L_S^{-1}HL_S^{-\dagger}$를 정의할 때 잔차도 함께 변환된다.[6,7]

$$
\widehat H\phi-\theta\phi=L_S^{-1}\rho_\lambda,
\qquad
\|L_S^{-1}\rho_\lambda\|_2^2
=\rho_\lambda^\dagger S^{-1}\rho_\lambda.
$$

따라서 $S$-정규화된 고유벡터를 평가할 때에는 $S^{-1}$ 가중 잔차가 표준 Hermitian 문제의 잔차에 대응한다. Euclidean 잔차를 쓰는 것도 가능하지만 좌표 스케일과 $S$의 조건을 함께 밝혀야 한다. 또 가까운 고유값들이 모여 있으면 개별 고유벡터의 정확도는 고유값 간격에 민감하므로, 작은 잔차만 보고 특정 벡터의 성분까지 확정하지 않는다.[6,7]

| 구별할 대상 | 올바른 형태 | 흔한 혼동 |
| --- | --- | --- |
| 알려진 상태의 $S$-직교 투영 | $VS_r^{-1}V^\dagger Sx$ | $VV^\dagger x$로 대체 |
| weak-form 고유값 축소 | $V^\dagger HV$, $V^\dagger SV$ | 왼쪽에 $S$를 추가 적용 |
| 고유벡터 정규화 | $z^\dagger S_rz=1$ | 항상 $z^\dagger z=1$로 처리 |
| 전체 고유값 잔차 | $HVz-\theta SVz$ | 축소 잔차만 확인 |

## 6. 잔차 검증과 기저 보강

### (1) 방정식 오차와 상태·출력 오차

축소 문제의 정확한 해에서는 projected residual $W^\dagger\rho$가 0이다. 따라서 이것만을 정확도 지표로 쓰면 기저가 놓친 방향을 검출하지 못한다. 정적 문제의 원공간 잔차 $\rho=b-KVa$와 상태 오차 $e=x-Va$는 다음 관계를 만족한다. $\|\cdot\|_2$는 벡터의 Euclidean norm과 그 유도 행렬 노름이다.[1,3]

$$
Ke=\rho,\qquad
\|e\|_2\le\|K^{-1}\|_2\|\rho\|_2,
\qquad
\|y-\widetilde y\|_2\le\|CK^{-1}\|_2\|\rho\|_2.
$$

이 식은 전체 잔차도 역연산의 민감도와 함께 해석해야 함을 보여 준다. 동일한 크기의 잔차라도 그 방향과 출력 $C$에 따라 관측량 오차가 달라진다. 원해가 없을 때 잔차는 유용한 진단량이지만, 실제로 계산하거나 제한하지 않은 $\|K^{-1}\|$를 생략하고 엄밀한 오차 보증이라고 부르지는 않는다.[1,3]

동적 문제에서는 오차 $e(t)=x(t)-Va(t)$가 잔차에 의해 계속 구동된다. 앞의 잔차 부호 규약으로 두 방정식을 빼면 다음 정확한 오차 방정식을 얻는다.[2,3]

$$
E\dot e=Ae+\rho_t,\qquad e(0)=x_0-Va(0).
$$

초기 오차와 시간 동안 쌓이는 잔차가 모두 중요하다는 뜻이다. 한 시점의 작은 잔차나 작은 초기 표현 오차만으로 전체 시간 구간의 상태 오차를 결정할 수 없다. 실제 평가에서는 같은 입력과 시간 구간을 사용하고, 원모형과 ROM의 시간 적분 오차를 축소 오차보다 충분히 작게 관리한다.[2,3]

기저에 사용하지 않은 검증 사례 $j=1,\ldots,N_{\mathrm{val}}$를 정하고, 동일한 우변·출력 정의에서 다음 지표를 비교할 수 있다. 아래의 $\epsilon_y$는 여러 검증 사례 중 최대 출력 절대 오차이며, 특정 보장 정리가 아니라 이 문서에서 선택한 평가 규약이다.[1,2,3]

$$
\eta_\rho^{(j)}=\|b^{(j)}-K^{(j)}Va^{(j)}\|_2,\qquad
\epsilon_y=\max_j\|y^{(j)}-C^{(j)}Va^{(j)}\|_2.
$$

출력이 0에 가까우면 상대 오차의 분모가 불안정하므로 절대 오차 또는 사전에 정한 출력 척도를 사용한다. 동역학에서는 검증 사례에 초기조건과 입력 이력을 포함하고 시간 표본별 최대값도 함께 정한다. 고유값 문제에서는 벡터의 정규화와 전체 잔차의 노름을 기록한다. 어느 경우든 검증 사례에서 확인한 결과와 전체 매개변수 영역에 대한 보장을 구분한다.[2,3,7]

### (2) 보강 방향과 중단 기준

기저 보강은 기존 공간이 표현하지 못하는 방향을 추가하는 일이다. 새 원모형 상태 $x_{\mathrm{new}}$를 얻었다면, 이미 포함된 성분을 제거한 뒤 남은 방향을 확인할 수 있다. 아래의 $q_{\mathrm{new}}$는 이 문서의 $S$-직교 투영으로 계산한 보강 후보이다.[1,3]

$$
q_{\mathrm{new}}=(I_n-P_S)x_{\mathrm{new}},\qquad
V_{\mathrm{new}}=
\left[V\ \frac{q_{\mathrm{new}}}{\|q_{\mathrm{new}}\|_S}\right]
\quad(\|q_{\mathrm{new}}\|_S>0).
$$

정확히 0이면 같은 공간을 다시 표현한 것이므로 새 자유도가 생기지 않는다. 수치적으로 매우 작다면 정한 rank 허용오차와 비교한다. 잔차가 큰 사례를 다음 원모형 계산 대상으로 고르는 방법도 가능하지만, 어떤 사례를 고를지와 그 사례에서 어느 방향을 얻을지는 구별해야 한다. 일반 비대칭 문제에서는 잔차 벡터를 그대로 더하는 것이 모든 출력에 가장 좋은 보강이라는 보장은 없다.[1,2,3]

동일한 양의 정부호 $K$와 우변에서 중첩 공간 $\mathcal V_r\subset\mathcal V_{r+1}$을 사용하면 Galerkin의 에너지 최적성으로 다음 단조성이 따라온다. $\widetilde x_r,\widetilde x_{r+1}$는 각 공간에서 구한 해이다.[1,3]

$$
\|x-\widetilde x_{r+1}\|_K
\le\|x-\widetilde x_r\|_K.
$$

이 결론은 임의의 Petrov–Galerkin 출력 오차나 모든 동역학의 안정성으로 확장되지 않는다. 공간을 보강한 뒤에도 test space의 적절성, 축소 질량 행렬의 가역성, 전체 잔차와 목표 출력을 다시 검사한다. 허용오차를 만족하면 중단하고, 개선이 멈추면 기저 차원뿐 아니라 검증 범위와 원모형의 수치 오차를 확인한다.[1,2,3]

| 관찰 | 다음 확인 | 해석 범위 |
| --- | --- | --- |
| 투영된 잔차만 작음 | 전체 잔차와 별도 검증 해 | 축소 방정식 계산의 정확성 |
| 전체 잔차가 작지만 출력 오차가 큼 | 역연산 민감도와 출력 방향 | 잔차에서 출력으로의 전달 |
| 기저 열 추가 후 조건수가 악화됨 | 열독립성, overlap, test 조건 | 좌표 표현 또는 공간 배치 |
| 상태 표본은 잘 맞지만 동역학이 발산함 | 축소 행렬쌍의 안정성 | 표현 오차와 시간 진화의 구별 |

### (3) 제거법과의 차이

Projection과 elimination-based downfolding은 모두 작은 행렬을 만들 수 있지만 출발점이 다르다. 여기의 투영법은 $x\approx Va$라는 표현 제한과 test 조건을 먼저 정한다.[1,2] 블록 제거법은 버릴 변수에 대한 원방정식을 풀어 남길 변수의 방정식에 대입한다. 가역인 제거 블록에 대한 Schur complement를 정확히 계산하고 역대입하면 원래 선형계의 해를 복구할 수 있다.[1,8]

따라서 특정 좌표를 0으로 놓고 대응하는 행과 열만 남기는 조작은, 그 좌표의 영향을 대입으로 반영한 제거법과 일반적으로 같지 않다. 둘을 동일하게 해석하려면 선택한 공간이나 유효 연산자 사이의 관계를 별도로 증명해야 한다. 이 문서의 $V^\dagger HV$만으로 제거된 상태의 효과까지 자동으로 포함했다고 주장할 수는 없다. 여기서는 이 차이만 구별하며 에너지 의존 유효 Hamiltonian의 구성은 다루지 않는다.[1,2,8]

## 7. 세 좌표 선형계의 재현 예제

### (1) Galerkin과 Petrov–Galerkin의 비교

다음은 측정값이 아니라 정적 잔차와 에너지 오차의 차이를 확인하기 위해 구성한 무차원 문제이다. 원행렬은 실수 양의 정부호이며, 출력은 세 번째 상태 성분이다. $e_1,e_2,e_3$는 표준 단위벡터이다.[1,3]

$$
K=\begin{pmatrix}2&1&0\\1&2&1\\0&1&2\end{pmatrix},\qquad
b=\begin{pmatrix}1\\0\\1\end{pmatrix},\qquad
C=\begin{pmatrix}0&0&1\end{pmatrix},\qquad
x=\begin{pmatrix}1\\-1\\1\end{pmatrix}.
$$

먼저 $V=[e_1\ e_2]$로 세 번째 상태를 표현에서 제외한다. Galerkin은 $W=V$를 사용하며 다음 해와 잔차를 얻는다. 이 값들은 작은 선형계를 직접 풀어 계산한다.

$$
a_G=\begin{pmatrix}2/3\\-1/3\end{pmatrix},\qquad
\rho_G=\begin{pmatrix}0\\0\\4/3\end{pmatrix},\qquad
V^\dagger\rho_G=0,\qquad \widetilde y_G=0.
$$

Test space만 $W=KV$로 바꾸면 같은 trial space에서 잔차 최소제곱 해를 얻는다. 이때 좌표는 $a_P=(2/7,1/7)^\mathsf T$이고, 전체 잔차는 $(2/7,-4/7,6/7)^\mathsf T$이다. 출력은 여전히 0이다. 같은 공간에서는 세 번째 좌표를 표현할 수 없으므로, test 조건을 바꾸는 것만으로 이 출력 오차를 없애지는 못한다.[1,3]

마지막으로 $e_3$까지 더하면 전체 공간이 되어 정확한 해를 얻는다. 아래 수치는 다음 코드의 계산 결과를 소수 여섯 자리로 반올림한 값이다. 에너지 오차는 $\sqrt{e^\mathsf TKe}$이며 출력 오차는 $|y-\widetilde y|$이다.

| 방법 | $r$ | 전체 잔차 $\|\rho\|_2$ | 상태 오차 $\|e\|_2$ | 에너지 오차 $\|e\|_K$ | 출력 절대 오차 |
| --- | --- | --- | --- | --- | --- |
| Galerkin | 2 | 1.333333 | 1.247219 | 1.154701 | 1.000000 |
| $W=KV$ | 2 | 1.069045 | 1.678191 | 1.309307 | 1.000000 |
| 전체 공간 | 3 | 0 | 0 | 0 | 0 |

두 축소 해 모두 자기 test space에 대한 잔차는 0이다. 그러나 두 번째 방법은 전체 잔차가 더 작고, 첫 번째 방법은 에너지 오차가 더 작다. 비교 노름을 정하지 않은 채 어느 해가 더 정확한지 말할 수 없는 이유가 이 작은 예제에 드러난다. 여기서 전체 공간까지 늘린 결과는 검산용이며 대규모 문제의 가속률을 보여 주는 자료는 아니다.

### (2) 실행과 수치 검산

아래 Python 3 코드는 외부 패키지 없이 실행한다. 작은 선형계를 부분 피벗 소거법으로 풀고 원공간에서 잔차·상태·출력을 다시 계산한다. 임의 크기의 안정적인 선형대수 라이브러리를 대체하려는 구현이 아니라, 위의 세 좌표 예제를 재현하는 코드이다. 마지막 두 줄은 앞 절의 동역학 반례와 가역성 반례를 독립적으로 확인한다.

```python
from math import sqrt


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def apply(A, x):
    return [dot(row, x) for row in A]


def norm(x):
    return sqrt(dot(x, x))


def solve(A, b):
    n = len(b)
    aug = [list(row) + [rhs] for row, rhs in zip(A, b)]
    for k in range(n):
        pivot = max(range(k, n), key=lambda i: abs(aug[i][k]))
        aug[k], aug[pivot] = aug[pivot], aug[k]
        assert abs(aug[k][k]) > 1e-14
        for i in range(k + 1, n):
            factor = aug[i][k] / aug[k][k]
            for j in range(k, n + 1):
                aug[i][j] -= factor * aug[k][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (aug[i][n] - dot(aug[i][i+1:n], x[i+1:])) / aug[i][i]
    return x


K = [[2., 1., 0.], [1., 2., 1.], [0., 1., 2.]]
b = [1., 0., 1.]
x = solve(K, b)
basis = [[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]]
for label, r, least_squares in (("Galerkin", 2, False),
                               ("Petrov", 2, True),
                               ("full", 3, False)):
    V = basis[:r]  # store basis columns as lists
    KV = [apply(K, v) for v in V]
    W = KV if least_squares else V
    Kr = [[dot(w, kv) for kv in KV] for w in W]
    br = [dot(w, b) for w in W]
    a = solve(Kr, br)
    xr = [sum(a[j] * V[j][i] for j in range(r)) for i in range(3)]
    rho = [bi - ki for bi, ki in zip(b, apply(K, xr))]
    error = [xi - ri for xi, ri in zip(x, xr)]
    projected = norm([dot(w, rho) for w in W])
    energy = sqrt(max(0.0, dot(error, apply(K, error))))
    assert projected < 1e-12
    expected = [2/7, 1/7] if least_squares else [2/3, -1/3]
    if r == 2:
        assert norm([ai - ei for ai, ei in zip(a, expected)]) < 1e-12
    else:
        assert norm(error) < 1e-12
    print(label, *(f"{v:.6f}" for v in
                   (norm(rho), norm(error), energy, abs(error[2]))))

A = [[-1., 4.], [0., -2.]]
v = [1 / sqrt(2)] * 2
ar = dot(v, apply(A, v))
assert abs(ar - 0.5) < 1e-12
K_bad = [[0., 1.], [1., 0.]]
kr_bad = dot([1., 0.], apply(K_bad, [1., 0.]))
assert kr_bad == 0.
print(f"unstable_reduced_rate={ar:.6f}")
print(f"singular_reduced_coefficient={kr_bad:.6f}")
```

예상 출력은 다음과 같다. 각 방법명 뒤의 네 열은 표와 같은 순서이며, test 잔차가 0에 가까운지는 코드의 `assert`로 별도 검사한다. $10^{-12}$는 이 작은 무차원 계산에서 사용한 반올림 허용량이다.

```text
Galerkin 1.333333 1.247219 1.154701 1.000000
Petrov 1.069045 1.678191 1.309307 1.000000
full 0.000000 0.000000 0.000000 0.000000
unstable_reduced_rate=0.500000
singular_reduced_coefficient=0.000000
```

## 8. 요약

- Trial space는 상태의 표현 범위를, test space와 내적은 잔차 제약을 정한다. 투영된 잔차가 0이라는 사실은 원방정식 전체가 만족된다는 뜻이 아니다.
- 양의 정부호 정적 문제의 Galerkin은 에너지 오차를 최소화한다. 일반 Petrov–Galerkin에는 이 최적성이나 가역성이 자동으로 주어지지 않는다.
- 원공간 내적 $S$와 축소 overlap $S_r=V^\dagger SV$를 구별한다. 가중 벡터 투영과 이미 내적이 조립된 weak-form 행렬의 축소에서 $S$를 중복 적용하지 않는다.
- 동역학에서는 질량·입력·출력·초기조건을 함께 축소한다. 원모형의 안정성만으로 ROM의 안정성을 판단할 수 없으며, 보존되는 에너지 구조 또는 축소 행렬쌍을 검사한다.
- 기저 보강의 효과는 전체 잔차와 독립 검증 사례의 목표 출력으로 평가한다. 단조 개선 보장은 성립하는 노름과 문제 조건 안에서만 사용한다.

## 9. 참고문헌

1. Y. Saad, *Iterative Methods for Sparse Linear Systems*, second edition (SIAM, 2003). [DOI: 10.1137/1.9780898718003](https://doi.org/10.1137/1.9780898718003). [Author-hosted full text](https://www-users.cse.umn.edu/~saad/IterMethBook_2ndEd.pdf). §§1.12–1.13, 5.1–5.2, 14.2.
2. P. Benner, S. Gugercin, and K. Willcox, “A Survey of Projection-Based Model Reduction Methods for Parametric Dynamical Systems,” *SIAM Review* **57**(4), 483–531 (2015). [DOI: 10.1137/130932715](https://doi.org/10.1137/130932715). [Author-hosted full text](https://kiwi.oden.utexas.edu/papers/Parametric-model-reduction-survey-Benner-Gugercin-Willcox.pdf). §§2.1–2.4, 3.3–3.4.
3. B. Haasdonk, “Reduced Basis Methods for Parametrized PDEs—A Tutorial Introduction for Stationary and Instationary Problems,” in *Model Reduction and Approximation: Theory and Algorithms*, pp. 65–136 (SIAM, 2017). [DOI: 10.1137/1.9781611974829.ch2](https://doi.org/10.1137/1.9781611974829.ch2). [Author preprint](https://pnp.mathematik.uni-stuttgart.de/ians/haasdonk/data/oberwolfach2014/RBtutorial.pdf). 공개 preprint의 §§2.3, 2.6, 3.3, Proposition 2.46.
4. R. Pulch, “Stability preservation in Galerkin-type projection-based model order reduction,” *Numerical Algebra, Control and Optimization* **9**(1), 23–44 (2019). [DOI: 10.3934/naco.2019003](https://doi.org/10.3934/naco.2019003). [Author preprint](https://arxiv.org/abs/1711.02912). §§2.1–2.3, Theorem 1.
5. I. Kalashnikova, M. F. Barone, S. Arunajatesan, and B. G. van Bloemen Waanders, “Construction of energy-stable projection-based reduced order models,” *Applied Mathematics and Computation* **249**, 569–596 (2014). [DOI: 10.1016/j.amc.2014.10.073](https://doi.org/10.1016/j.amc.2014.10.073). [Author-hosted full text](https://www.sandia.gov/app/uploads/sites/127/2021/10/amc2014.pdf). §§2–3, 5.1.
6. Y. Saad, *Numerical Methods for Large Eigenvalue Problems*, revised edition (SIAM, 2011). [DOI: 10.1137/1.9781611970739](https://doi.org/10.1137/1.9781611970739). [Author-hosted full text](https://www-users.cse.umn.edu/~saad/eig_book_2ndEd.pdf). §§3.2, 4.3.1, 9.2.2, 9.2.5–9.2.6.
7. Z. Bai, J. Demmel, J. Dongarra, A. Ruhe, and H. van der Vorst, eds., *Templates for the Solution of Algebraic Eigenvalue Problems: A Practical Guide* (SIAM, 2000). [DOI: 10.1137/1.9780898719581](https://doi.org/10.1137/1.9780898719581). G. Sleijpen and H. van der Vorst, [§4.7.1, Basic Theory](https://www.netlib.org/utk/people/JackDongarra/etemplates/node137.html), [§5.6, Jacobi-Davidson Methods](https://www.netlib.org/utk/people/JackDongarra/etemplates/node176.html); [§5.2, Transformation to Standard Problem](https://www.netlib.org/utk/people/JackDongarra/etemplates/node163.html); Z. Bai and R. Li, [§5.7.1, Positive Definite B](https://www.netlib.org/utk/people/JackDongarra/etemplates/node178.html), [Residual Vector](https://www.netlib.org/utk/people/JackDongarra/etemplates/node179.html), [Error Bounds for Computed Eigenvectors](https://www.netlib.org/utk/people/JackDongarra/etemplates/node182.html).
8. L. N. Trefethen and D. Bau III, *Numerical Linear Algebra* (SIAM, 1997). [DOI: 10.1137/1.9780898719574](https://doi.org/10.1137/1.9780898719574). [University-hosted full text](https://www.stat.uchicago.edu/~lekheng/courses/309/books/Trefethen-Bau.pdf). Lecture 20, p. 152의 “Solution of $Ax=b$ by LU Factorization”와 p. 154의 Exercise 20.3.
