---
description: 특이값 절단의 최적 오차와 수치적 랭크, QR 근사, 계산 비용을 설명하고 표본 압축과 연산자 근사의 적용 범위를 구분한다.
---

# Low-rank approximation

Low-rank approximation은 행렬이 수행하는 선형 사상을 적은 수의 독립 방향으로 표현하는 근사이다. 행렬의 행과 열 개수는 유지하면서 인수 사이의 내부 차원을 줄인다. Singular value decomposition (SVD)을 절단하면 spectral norm과 Frobenius norm에서 가장 작은 오차를 얻을 수 있다. 그러나 그 최적성은 지정한 행렬과 노름에 관한 것이며, 행렬에 담기지 않은 상태나 별도로 푸는 방정식의 정확도까지 뜻하지 않는다.[1,2]

기저변환, 부분공간 제한과 축소 모형의 구분은 [Model reduction fundamentals](fundamentals.md)를 따른다. 여기서는 유한차원 행렬의 근사 문제를 다루며, 특이값의 감소가 오차·저장량·계산량으로 어떻게 연결되는지 설명한다. $\dagger$는 켤레전치이고 실수에서는 전치이다. 별도 언급이 없으면 Euclidean 내적을 사용하며, SVD의 오른쪽 인수를 $V_s$로 써서 상태 축소 기저 $V$와 구별한다.

## 1. SVD와 특이값 절단

### (1) 입력 방향과 출력 방향

$M\in\mathbb C^{n\times k}$와 $p=\min(n,k)$를 정하자. 이 문서에서 thin SVD는 0인 특이값도 포함하여 $p$개의 방향을 보관하는 다음 분해이다. $I_p$는 $p$차원 항등행렬이다.[1,2]

$$
M=U_s\Sigma V_s^\dagger,\qquad
U_s^\dagger U_s=V_s^\dagger V_s=I_p,
\qquad \Sigma=\operatorname{diag}(\sigma_1,\ldots,\sigma_p).
$$

$U_s\in\mathbb C^{n\times p}$와 $V_s\in\mathbb C^{k\times p}$의 열은 각각 왼쪽·오른쪽 singular vector이다. 특이값은 실수이며 다음 순서를 따른다. 정확히 양수인 특이값의 수 $q$가 행렬의 대수적 rank이다.[1,2]

$$
\sigma_1\ge\sigma_2\ge\cdots\ge\sigma_p\ge0,
\qquad q=\operatorname{rank}(M)=\#\{i:\sigma_i>0\}.
$$

$u_i$와 $v_i$를 각 인수의 $i$번째 열이라 하면, $M$은 입력 방향 $v_i$를 출력 방향 $u_i$로 보내면서 길이를 $\sigma_i$배 한다. 일반적인 직사각형 행렬에도 성립하는 관계이며, 두 방향이 같아야 하는 고유벡터 관계와 구별된다.[1,2]

$$
Mv_i=\sigma_i u_i,\qquad
M^\dagger u_i=\sigma_i v_i.
$$

따라서 특이값은 이 내적에서 측정한 사상의 세기이다. 양의 특이값에 대응하는 $v_i$들은 입력 중 실제로 전달되는 성분을, $u_i$들은 그 성분이 도달하는 열공간을 나타낸다. 입력과 출력의 좌표계가 같다는 가정도, $M$이 Hermitian이라는 가정도 필요하지 않다. 복소수에서는 위상 선택이 달라져도 대응하는 $u_iv_i^\dagger$가 같을 수 있으므로, 개별 벡터의 성분을 비교할 때는 부호·위상 자유도를 고려해야 한다.[1,2]

| 인수 | 크기 | 담고 있는 정보 |
| --- | --- | --- |
| $U_s$ | $n\times p$ | 출력 공간의 정규직교 방향 |
| $\Sigma$ | $p\times p$ | 각 방향의 비음수 전달 크기 |
| $V_s$ | $k\times p$ | 입력 공간의 정규직교 방향 |
| $q$ | 정수 | 정확히 0이 아닌 전달 방향의 수 |

### (2) Rank-one 성분과 절단

SVD를 열별로 전개하면 서로 직교하는 방향의 rank-one 사상들을 더한 형태가 된다. 원하는 차원 $0\le r\le p$를 정하고 앞의 $r$개 성분만 남긴 행렬을 $M_r$라 한다. $r=0$일 때 합은 0이다.[1,2]

$$
M=\sum_{i=1}^{p}\sigma_i u_iv_i^\dagger,
\qquad
M_r=\sum_{i=1}^{r}\sigma_i u_iv_i^\dagger
=U_{s,r}\Sigma_rV_{s,r}^\dagger.
$$

여기서 $U_{s,r}$와 $V_{s,r}$는 앞의 $r$개 열, $\Sigma_r$는 해당 특이값만 보관한 대각행렬이다. $r\le q$이면 $M_r$의 rank는 $r$이고, $r\ge q$이면 $M_r=M$이다. 근사 후에도 $M_r$의 외부 크기는 $n\times k$이다. 큰 배열을 다시 만들지 않고 세 인수로 저장할 때 내부 차원 $r$의 이점이 생긴다.[1,2]

주어진 입력 $z\in\mathbb C^k$에 대한 계산 순서는 먼저 $V_{s,r}^\dagger z$로 $r$개 계수를 얻고, 특이값을 곱한 뒤 $U_{s,r}$로 출력 공간에 복원하는 것이다. 버려진 입력 방향은 더 이상 출력에 기여하지 않는다.[1,2]

$$
M_rz=U_{s,r}\bigl[\Sigma_r(V_{s,r}^\dagger z)\bigr].
$$

이 절단은 작은 특이값을 0으로 바꾸는 수학적 선택이다. 원래 SVD를 계산하는 과정에서 생기는 반올림 오차와 절단으로 의도적으로 버리는 오차는 다르다. 이후의 정확한 오차식은 정확한 $M_r$에 관한 것이므로, 실제 구현에서는 인수의 재구성 오차와 직교성도 함께 확인한다.[1,2,3]

## 2. 노름별 최적 오차

### (1) 최악 입력과 전체 성분 오차

Spectral norm은 단위 입력 중 가장 크게 증폭되는 방향을 측정한다. Frobenius norm은 행렬의 모든 성분 오차를 제곱하여 합한다. 성분을 $M_{ab}$라 쓰면 정의와 SVD 표현은 다음과 같다.[1,2,3]

$$
\|M\|_2=\max_{\|z\|_2=1}\|Mz\|_2=\sigma_1,
\qquad
\|M\|_F^2=\sum_{a=1}^{n}\sum_{b=1}^{k}|M_{ab}|^2
=\sum_{i=1}^{p}\sigma_i^2.
$$

두 노름 모두 unitary 좌표변환에 불변이므로, $M-M_r$의 크기는 버린 특이값만으로 계산된다. 아래 식에서 $r=p$이면 오차를 0으로 정하고 $\sigma_{p+1}=0$으로 둔다.[1,2]

$$
\|M-M_r\|_2=\sigma_{r+1},\qquad
\|M-M_r\|_F=\left(\sum_{i=r+1}^{p}\sigma_i^2\right)^{1/2}.
$$

첫 식은 가장 큰 누락 방향 하나가 최악 입력을 결정한다는 뜻이다. 둘째 식은 작은 누락 성분이 많이 모이면 전체 오차가 커질 수 있음을 보여 준다. 따라서 $\sigma_{r+1}$만 작다고 해서 Frobenius 오차도 같은 크기라고 보고할 수 없다. $r<p$일 때 각 꼬리 특이값이 $\sigma_{r+1}$ 이하라는 사실에서 다음 범위를 얻는다.[1,2]

$$
\sigma_{r+1}\le\|M-M_r\|_F
\le\sqrt{p-r}\,\sigma_{r+1}.
$$

$M\ne0$인 경우 상대 오차를 계산할 때에도 분모를 해당 노름으로 고정한다. 아래의 $e_2(r)$와 $e_F(r)$는 서로 다른 평가 지표이며, 0행렬에서는 절대 오차를 사용한다.[1,2]

$$
e_2(r)=\frac{\sigma_{r+1}}{\sigma_1},\qquad
e_F(r)=\left(\frac{\sum_{i=r+1}^{p}\sigma_i^2}
{\sum_{i=1}^{p}\sigma_i^2}\right)^{1/2}.
$$

### (2) Eckart–Young–Mirsky 정리

Eckart–Young–Mirsky 정리는 위 절단 오차가 단지 계산하기 쉬운 값이 아니라, rank가 $r$ 이하인 모든 행렬 중 가능한 최솟값임을 말한다. 여기서 비교 행렬 $B$는 $M$과 같은 크기이며, 특정 원소·희소 구조·보존 법칙 등을 추가로 고정하지 않는다.[1,2]

$$
\min_{\operatorname{rank}(B)\le r}\|M-B\|_2=\sigma_{r+1},
\qquad
\min_{\operatorname{rank}(B)\le r}\|M-B\|_F
=\left(\sum_{i=r+1}^{p}\sigma_i^2\right)^{1/2}.
$$

Spectral norm의 하한은 차원으로 이해할 수 있다. Rank가 $r$ 이하인 $B$는 $r+1$개 오른쪽 singular vector가 만드는 공간에서 어떤 0이 아닌 방향을 소거한다. 그 방향을 단위벡터 $z$로 정하면 $Bz=0$이고 $\|Mz\|_2\ge\sigma_{r+1}$이다. 따라서 다른 rank-$r$ 행렬을 고르더라도 이 최악 방향의 오차보다 작아질 수 없다. SVD 절단은 바로 그 하한에 도달한다.[1,2,3]

Frobenius norm의 의미는 열공간 투영으로도 드러난다. Rank-$r$ 후보의 열공간에 대한 직교 투영을 $P$라 하면, $M-B$를 그 공간 안팎의 성분으로 나누어 다음 항등식을 얻는다. 두 항의 직교성은 Frobenius 내적에 관한 것이다.[1,2]

$$
\|M-B\|_F^2=\|(I-P)M\|_F^2+\|PM-B\|_F^2.
$$

고정된 공간에서는 $B=PM$이 가장 좋고, 다음 과제는 $\|PM\|_F^2$를 최대화하는 $r$차원 공간을 고르는 것이다. 각 $u_i$에 배분되는 투영의 크기는 0과 1 사이이고 총합은 $r$ 이하이므로, 큰 $\sigma_i^2$부터 보존하는 것이 최선이다. 이 설명은 Frobenius 최적성이 전체 제곱오차의 배분 문제라는 점과, 왜 앞의 왼쪽 singular vector를 사용하는지를 연결한다.[1,2]

### (3) 특이값 중복과 유일성

최소 오차가 정해져 있다는 사실과 그 오차를 달성하는 행렬이 하나뿐이라는 사실은 다르다. $0<r<q$에서 $\sigma_r>\sigma_{r+1}$이면 Frobenius 최적 근사 $M_r$는 유일하다. 앞의 투영 설명에서 경계 특이값 사이에 간격이 있으면 더 작은 성분과 바꾸는 순간 보존되는 제곱합이 감소하기 때문이다. 이 유일성은 행렬에 대한 것이며, 그 행렬을 표현하는 기저의 부호·위상까지 고정하지는 않는다.[1,2]

$\sigma_r=\sigma_{r+1}>0$인 경계에서 절단하면 동등한 세기의 방향 중 일부만 남기게 된다. 중복 특이값 공간 안에서 함께 회전한 왼쪽·오른쪽 벡터도 같은 원행렬을 표현하지만, 그중 어떤 부분을 남기는가에 따라 서로 다른 최적 근사가 생긴다. 예를 들어 $M=\operatorname{diag}(3,1,1)$의 rank-2 절단에서 둘째와 셋째 좌표 중 어느 쪽을 버려도 Frobenius 오차는 1이다. 이는 일반 정리와 대각행렬에서 직접 계산한 예이다.[1,2]

반면 spectral norm에서는 경계에 간격이 있어도 최적 행렬이 유일하다고 할 수 없다. 다음은 이를 검산할 수 있는 별도의 무차원 반례이다. 실수 $c$가 $1\le c\le3$이면 $B_c$의 rank는 1이다.[1,2]

$$
M=\begin{pmatrix}2&0\\0&1\end{pmatrix},\qquad
B_c=\begin{pmatrix}c&0\\0&0\end{pmatrix},\qquad
\|M-B_c\|_2=\max(|2-c|,1)=1.
$$

특이값 간격은 $2>1$이지만 이 모든 $B_c$가 spectral 최적값 1을 달성한다. Frobenius 오차는 $\sqrt{(2-c)^2+1}$이므로 $c=2$에서만 최소이다. 따라서 “SVD가 유일하다”, “선택한 부분공간이 유일하다”, “노름 최소화의 해가 유일하다”를 같은 주장으로 사용해서는 안 된다.

## 3. 수치적 랭크와 절단 기준

### (1) 허용오차에 따른 랭크

대수적 rank는 특이값이 정확히 0인지에 따라 정해진다. Numerical rank는 허용오차 안에서 무시할 수 있는 방향을 제외한 수이다. 이 문서에서는 절대 spectral 허용오차 $\tau\ge0$에 대해 다음처럼 정의한다. 등호에 걸리는 특이값은 버리는 규약이다.[1,3]

$$
r_\tau=\#\{i:\sigma_i>\tau\}
=\min\{r:\|M-M_r\|_2\le\tau\}.
$$

따라서 numerical rank를 보고할 때는 $r_\tau$만 아니라 $\tau$, 노름, 원행렬의 크기와 스케일도 함께 남겨야 한다. 모든 특이값이 양수인 행렬도 작은 $r_\tau$를 가질 수 있다. 반대로 “소수점 아래 몇 자리부터 0으로 취급한다”는 규칙은 단위와 정규화를 바꾸면 판정을 바꾸므로 보편적인 물성이나 모형 차원으로 해석할 수 없다.[1,3]

상대 허용오차 $\varepsilon_2$를 택하면 $\tau=\varepsilon_2\sigma_1$로 바꿀 수 있다. Frobenius 상대 허용오차 $\varepsilon_F$에서는 특이값 하나가 아니라 꼬리 전체를 검사해야 한다. 두 경우 필요한 최소 차원은 다음 조건을 만족하는 가장 작은 $r$이다.[1,2,3]

$$
\sigma_{r+1}\le\varepsilon_2\sigma_1,
\qquad\text{또는}\qquad
\sum_{i=r+1}^{p}\sigma_i^2\le
\varepsilon_F^2\sum_{i=1}^{p}\sigma_i^2.
$$

보존된 제곱합의 비율을 $\eta_r$라 정의하면 Frobenius 기준을 다른 형태로 쓸 수 있다. 이 비율을 문헌에서 “energy”라고 부르기도 하지만, 해당 내적이 물리적 에너지를 나타내도록 정의되어 있지 않으면 단순한 행렬 제곱노름의 비율이다.[1,2,3]

$$
\eta_r=\frac{\sum_{i=1}^{r}\sigma_i^2}{\sum_{i=1}^{p}\sigma_i^2},
\qquad e_F(r)=\sqrt{1-\eta_r}.
$$

예를 들어 $\eta_r=0.99$는 Frobenius 상대 오차가 1%라는 뜻이 아니라 10%라는 뜻이다. 이 수치는 위 정의의 직접 계산이며, spectral 상대 오차에 대한 동일한 백분율을 뜻하지도 않는다. 오차 자체의 허용값과 오차 제곱의 허용값을 코드와 보고서에서 일치시켜야 한다.

### (2) 잡음과 경계 특이값

측정 또는 계산으로 얻은 행렬을 $M_{\mathrm{obs}}=M_\star+E$라 하자. $M_\star$는 알 수 없는 기준 행렬, $E$는 잡음·계산 오차이고 $\|E\|_2\le\delta$를 안다고 가정한다. 정리의 spectral 최적값과 삼각부등식을 두 행렬에 번갈아 적용하면 다음 특이값 변동 상한을 얻는다. 이는 앞의 최적 근사 관계에서 도출한 결과이다.[1,2,3]

$$
|\sigma_i(M_{\mathrm{obs}})-\sigma_i(M_\star)|\le\delta.
$$

따라서 임계값에서 $\delta$보다 가까운 특이값은 그 정보만으로 같은 쪽에 남는다고 보증할 수 없다. 예를 들어 관측값이 $\tau+\delta$보다 크면 기준 특이값도 $\tau$보다 크지만, $\tau$ 부근에서는 양쪽 판정이 모두 가능하다. 이 상한은 확률적 잡음 모형을 가정하지 않으며, 정확히 0인 특이값이 잡음으로 양수가 될 수 있는 이유도 설명한다. 부동소수점에서 양수로 출력되었다는 사실만으로 독립적인 물리 방향을 발견했다고 결론 내리지 않는다.[1,2,3]

절단 허용오차는 최종 사용 목적과 데이터의 신뢰도에 맞춰 정한다. 잡음 바닥보다 훨씬 작은 성분까지 보존하면 기준 행렬보다 잡음의 세부 구조를 표현할 수 있다. 반대로 약한 방향이 관심 출력에 중요하면 작은 특이값이라는 이유만으로 제거하기 어렵다. 전자는 데이터의 해상도에 관한 판단이고 후자는 어떤 행렬과 노름을 근사해야 하는가에 관한 판단이므로, 하나의 자동 임계값으로 두 문제를 모두 해결할 수 없다.[1,3]

### (3) 스케일과 평가 공간

일반적인 행·열 스케일 변환은 unitary 변환이 아니므로 특이값과 최적 근사 자체를 바꾼다. 양의 대각행렬 $D_o$와 $D_i$를 각각 출력·입력 좌표의 스케일로 정하고 $\widehat M=D_oMD_i$를 근사한다고 하자. 변환 공간의 후보 $\widehat B$를 원래 공간으로 되돌린 행렬은 다음과 같다.[1,2,3]

$$
B=D_o^{-1}\widehat B D_i^{-1},\qquad
\|\widehat M-\widehat B\|_F^2
=\sum_{a,b}(D_o)_{aa}^{2}(D_i)_{bb}^{2}|M_{ab}-B_{ab}|^2.
$$

이 항등식은 스케일을 바꾸는 것이 원래 성분 오차의 가중치를 바꾸는 일임을 보여 준다. 가역 스케일 변환은 대수적 rank를 보존하지만, 원래 Euclidean norm에 대한 최적성을 보존할 필요는 없다. 서로 다른 단위의 물리 변수를 같은 행렬에 넣을 때는 먼저 무차원화 또는 오차 가중치의 근거를 정한다. 위 식은 행·열별로 분리되는 가중치의 경우이며, 임의의 성분별 가중 오차를 보통 SVD 한 번으로 최소화한다는 뜻은 아니다.[1,2,3]

## 4. QR 기반 근사와 랭크 판정

### (1) 열 피벗과 잔여 블록

SVD는 최적 오차의 기준을 제공하지만, 원래 열 중 대표 열을 고르거나 삼각 인수를 사용하고 싶을 때는 rank-revealing QR (RRQR)을 고려할 수 있다. QR은 정규직교 인수 $Q$와 삼각 인수 $R$의 이름이며, 열 피벗은 순열행렬 $\Pi$로 원래 열 순서를 바꾸는 연산이다. 이 절은 근거 문헌과 같은 실수 tall matrix $M\in\mathbb R^{n\times k}$, $n\ge k$를 기준으로 설명한다.[4,5]

$1\le r<k$에서 thin QR의 열과 행을 나누면 다음과 같다. $Q_1$은 $r$개 열, $Q_2$는 나머지 $k-r$개 열을 가지며 $R_{11}$은 $r\times r$이다.[4,5]

$$
M\Pi=[Q_1\ Q_2]
\begin{pmatrix}R_{11}&R_{12}\\0&R_{22}\end{pmatrix}.
$$

아랫부분을 버려 얻는 rank-$r$ 이하 근사를 $M_{\mathrm{QR}}$라 하자. $Q_2$의 열이 정규직교이므로 오차는 잔여 블록의 노름과 정확히 같다. $\nu$는 여기서 두 노름 $2,F$ 중 하나를 나타낸다.[4,5]

$$
M_{\mathrm{QR}}=Q_1[R_{11}\ R_{12}]\Pi^\mathsf T,
\qquad
\|M-M_{\mathrm{QR}}\|_\nu=\|R_{22}\|_\nu.
$$

Column-pivoted QR은 각 단계에서 아직 설명하지 못한 열의 크기를 사용하여 다음 열을 선택한다. 실무에서 유용하지만, 이 탐욕적 선택이 모든 행렬에서 SVD와 비슷한 rank 판정을 보장하지는 않는다. 원문에는 필요한 singular value를 잘 드러내지 못하는 반례가 제시되어 있다. 특히 $|R_{ii}|$는 특이값이 아니며, 대각 원소만 보고 $\|R_{22}\|_2$를 대신했다고 주장할 수 없다.[4,5]

### (2) 잔차와 열 선택의 안정성

RRQR에서 확인할 대상은 서로 보완적이다. $R_{22}$가 작아야 버린 열 성분의 오차가 작고, $R_{11}$의 최소 특이값이 너무 작지 않아야 선택한 열들이 거의 종속인 조합을 피한다. 보장이 있는 알고리즘은 이 블록들의 특이값을 원행렬의 특이값과 크기 의존 인자 이내에서 연결한다. 단순한 열 피벗, 추가 열 교환을 쓰는 hybrid 알고리즘, strong RRQR은 보장 수준을 구별하여 사용해야 한다.[4,5]

이 차이는 열 보간식에서 더 구체적으로 보인다. $R_{11}$이 가역이고 $C$가 $M\Pi$의 앞 $r$개 열이면 $C=Q_1R_{11}$이다. 나머지 열을 선택한 열의 선형결합으로 표현하는 계수 $T_c$는 삼각 선형계로 구한다.[4,5]

$$
R_{11}T_c=R_{12},\qquad
M\Pi\approx C[I_r\ T_c],\qquad
\|T_c\|_2\le\frac{\|R_{12}\|_2}{\sigma_{\min}(R_{11})}.
$$

마지막 부등식은 역행렬 노름을 이용해 직접 얻은 상한이다. 작은 잔차만으로 계수의 크기까지 제한되지는 않는다는 점을 보여 준다. Strong RRQR을 포함한 보장 있는 분해를 평가할 때는 이러한 보간 계수도 함께 확인한다. 여기서는 개별 알고리즘의 상수를 동일시하지 않으며, 사용할 구현이 실제로 어떤 블록 오차와 계수 제한을 제공하는지 확인해야 한다. QR이라는 이름이나 피벗 옵션만으로 strong RRQR의 보장을 부여할 수 없다.[4,5]

| 확인할 양 | 작은 값 또는 큰 값의 의미 | 단독으로 보장하지 않는 것 |
| --- | --- | --- |
| $\|R_{22}\|$가 작음 | 선택 공간 밖의 행렬 오차가 작음 | 선택 열의 양호한 조건수 |
| $\sigma_{\min}(R_{11})$가 충분히 큼 | 선택 열의 종속성이 제한됨 | 잔여 블록의 작은 오차 |
| 보간 계수 $T_c$가 제한됨 | 대표 열의 조합이 과도하게 커지지 않음 | SVD와 동일한 최솟값 |
| $|R_{ii}|$의 감소 | 피벗 과정의 진단 정보 | 특이값 스펙트럼과의 동일성 |

## 5. 저장량과 계산 비용

저랭크 근사의 이점은 인수 형태를 유지할 때 발생한다. 대각 $\Sigma_r$를 별도 저장하면 필요한 스칼라 수는 $(n+k)r+r$개이다. $L=U_{s,r}\Sigma_r$, $R=V_{s,r}$로 흡수하면 $M_r=LR^\dagger$이며 $(n+k)r$개를 저장한다. 아래 비교는 희소 인덱스나 프로그램의 부가 메모리를 제외한 조밀 배열의 원소 수이다.[2,3]

$$
N_{\mathrm{dense}}=nk,\qquad
N_{\mathrm{factor}}=(n+k)r,\qquad
N_{\mathrm{factor}}<N_{\mathrm{dense}}\iff
r<\frac{nk}{n+k}.
$$

Rank가 조금 줄었다는 사실만으로 항상 저장량이 줄지는 않는다. 특히 작은 행렬에서는 두 인수를 저장하는 편이 더 클 수 있다. 정방행렬에서 위 기준은 $r<n/2$이지만, 이는 이 저장 형식의 원소 수 기준이다. 행렬의 실제 구조를 이용하는 다른 표현이나 실행 시간의 손익분기점과 같지 않다.[2,3]

벡터 하나에 작용할 때는 $R^\dagger z$와 $L(R^\dagger z)$를 차례로 계산한다. 조밀 행렬의 직접 곱이 $O(nk)$인 데 비해 이 두 곱의 연산 수는 $O((n+k)r)$이다. 다만 $M_r$를 명시적으로 전개하면 $n\times k$ 저장량이 다시 필요하므로, 후속 알고리즘도 인수로 작용을 계산할 수 있어야 압축의 이점이 유지된다.[2,3]

| 작업 | 조밀 행렬 기준 규모 | 조건과 비용 해석 |
| --- | --- | --- |
| 전체 SVD 구성 | $O(nkp)$ | $p=\min(n,k)$; 필요한 인수의 종류에 따라 상수 차이 |
| 절단 후 인수 저장 | $O((n+k)r)$ | 특이값을 한 인수에 흡수 |
| 입력 벡터에 작용 | $O((n+k)r)$ | 원행렬을 재구성하지 않음 |
| 전체 근사 행렬 재구성 | $O(nkr)$ | 결과 저장은 다시 $O(nk)$ |

전체 SVD를 계산한 뒤 절단하는 접근은 작은 문제의 기준해를 만드는 데 적합하지만, 전체 분해 비용을 이미 지불한다. 큰 문제에서 소수의 방향만 필요하면 partial factorization을 고려한다. 희소성이나 빠른 행렬–벡터 곱을 이용할 수 있는 방법도 있지만, 수렴·직교화·데이터 접근 비용과 목표 오차를 함께 비교해야 한다. 동일한 $r$이 모든 알고리즘에서 같은 작업량이나 같은 근사 오차를 뜻하지 않는다.[2,3]

전체 작업의 비용에는 인수 구성과 이후의 반복 사용이 모두 들어간다. 행렬을 단 한 번 적용하기 위해 비싼 분해를 새로 만드는 경우와, 같은 근사를 수천 번 적용하는 경우의 선택은 달라진다. 데이터가 메모리 밖에 있으면 읽기 횟수도 중요하다. 따라서 위 표는 연산량 모형이며, 장비에서 측정한 속도나 특정 문제의 보장된 가속률로 사용하지 않는다.[2,3]

## 6. 상태 표본과 연산자 근사의 차이

### (1) Snapshot 행렬의 표현 오차

상태 snapshot $x_j\in\mathbb C^n$을 $N_s$개 모아 $X=[x_1\ \cdots\ x_{N_s}]$를 만들자. 이때 $X$의 SVD에서 $V=U_{s,r}$를 상태 trial basis로 선택하면 $X_r=VV^\dagger X$이다. Proper orthogonal decomposition (POD)은 이러한 표본의 제곱 표현 오차를 최소화하는 기저 구성과 연결된다. 아래에서 $P=VV^\dagger$는 Euclidean 직교 투영이다.[6,7]

$$
\|X-PX\|_F^2
=\sum_{j=1}^{N_s}\|x_j-Px_j\|_2^2
=\sum_{i=r+1}^{\min(n,N_s)}\sigma_i(X)^2.
$$

이 식의 목적함수는 수집한 표본의 오차 합이다. 평균 제곱오차를 쓰면 양쪽을 $N_s$로 나누며, 같은 표본과 같은 가중치에서는 최적 공간이 바뀌지 않는다. 표본별 가중치나 상태 내적을 바꾸면 그에 맞는 최적화 문제도 달라진다. 따라서 표본의 위치·횟수·정규화는 분해 전의 단순 전처리가 아니라 어떤 오차를 중요하게 보는가를 결정한다.[6,7]

POD의 최적성은 주어진 표본을 재구성하는 데 관한 것이며, 새 매개변수에서 얻는 축소 방정식의 해 오차를 곧바로 제한하지 않는다. 아직 보지 않은 상태가 선택 공간 밖으로 나갈 수 있고, 축소 방정식이 계산한 좌표가 기존 상태의 최적 투영 좌표와 다를 수도 있다. 이를 분리하기 위해 기저에 사용하지 않은 표본의 표현 오차와 실제 축소 해·출력 오차를 별도로 검사한다.[6,7]

합계 오차가 작다는 사실만으로 모든 표본의 상대 오차가 작아지는 것도 아니다. 크기가 작은 표본 하나의 방향을 완전히 놓쳐도 전체 제곱합에 미치는 영향은 작을 수 있다. 반대로 최대 표본 오차를 직접 제한하는 목적은 평균 제곱오차 최소화와 다르다. 요구 사항이 최악 조건의 정확도라면 오차 합과 함께 표본별 오차를 확인해야 한다.[6,7]

### (2) 연산자 작용과 역문제

$M$이 상태 표본이 아니라 연산자이면 오차의 해석이 달라진다. 같은 입력 $z$에 대한 출력 차이는 spectral norm의 정의로 제한된다. 아래 관계는 임의의 입력에 성립하지만 $Mz$에 대한 상대 오차 상한은 아니다.[1,3]

$$
\|(M-M_r)z\|_2\le\sigma_{r+1}\|z\|_2.
$$

예를 들어 $z=v_{r+1}$이면 원래 출력은 $\sigma_{r+1}u_{r+1}$이고 절단 출력은 0이다. $\sigma_{r+1}>0$일 때 이 방향의 출력 상대 오차는 100%이다. 따라서 작은 $\|M-M_r\|_2/\|M\|_2$는 모든 입력에 대한 작은 출력 상대 오차와 다르다. 이 예는 특정 물리 결과가 아니라 SVD 작용식을 그대로 대입한 계산이다.[1,2]

특히 정방 가역 행렬 $K\in\mathbb C^{n\times n}$를 $r<n$인 $K_r$로 절단하면 $K_r$는 특이행렬이다. $Kx=b$를 풀던 작업에서 $K_r$로 교체하는 것은 작은 좌표계의 가역 방정식을 구성하는 일과 다르다. 일반 우변에 대한 해가 없어지거나 유일하지 않을 수 있으며, pseudoinverse를 사용하면 버린 방향을 제거하는 다른 해 선택 문제가 된다.[1,2]

$K$의 최소 특이값을 $\sigma_n(K)>0$이라 하자. SVD의 역을 취하면 다음 식을 얻으며, $\kappa_2(K)$는 spectral norm으로 정의한 조건수이다. 이 관계는 작은 방향을 역으로 풀 때의 증폭을 나타내며, forward 작용을 압축하기 쉬운 행렬이 역문제에서도 다루기 쉬운 것은 아니라는 점을 설명한다.[1,2]

$$
\|K^{-1}\|_2=\frac{1}{\sigma_n(K)},\qquad
\kappa_2(K)=\frac{\sigma_1(K)}{\sigma_n(K)}.
$$

따라서 행렬 근사 오차만으로 역문제 해의 정확성을 결정하지 않는다. 상태·잔차·출력 오차의 구분은 선행 문서의 검증 절차를 따른다.[1,2]

## 7. 네 방향 행렬의 재현 예제

### (1) 행렬과 두 오차 기준

다음 예제는 실험 자료가 아니라 오차식을 검산하기 위해 구성한 무차원 행렬이다. 정규직교 열을 갖는 실수 행렬 $H$와 서로 다른 네 특이값을 사용한다. $H^\mathsf TH=I_4$이므로 표시한 식 자체가 정확한 SVD이며, 이 예에서는 왼쪽·오른쪽 인수가 같다.[1,2]

$$
H=\frac12\begin{pmatrix}
1&1&1&1\\1&-1&1&-1\\1&1&-1&-1\\1&-1&-1&1
\end{pmatrix},\qquad
M=H\operatorname{diag}(8,2,0.2,0.02)H^\mathsf T.
$$

이 행렬의 대수적 rank는 4이다. 절대 spectral 허용오차 $\tau=0.25$에서 numerical rank는 2이며, 상대 spectral 오차는 2.5%이다. Frobenius 오차를 2% 이하로 요구하면 rank 2로는 부족하고 rank 3이 필요하다. 아래 값은 앞의 정확한 식과 다음 코드로 계산했으며 표시 자릿수만 반올림했다.

| $r$ | Spectral 절대 오차 | Frobenius 절대 오차 | $e_2(r)$ | $e_F(r)$ |
| --- | --- | --- | --- | --- |
| 1 | 2 | 2.010075 | 0.250000 | 0.243685 |
| 2 | 0.2 | 0.200998 | 0.025000 | 0.024367 |
| 3 | 0.02 | 0.020000 | 0.002500 | 0.002425 |
| 4 | 0 | 0 | 0 | 0 |

작은 예제에서는 저장량 절약을 기대하기 어렵다. $M$은 16개 원소이지만 rank-2의 두 인수도 16개 원소를 저장한다. 예제의 역할은 압축 성능 측정이 아니라, rank와 노름을 바꿀 때 어떤 오차가 변하는지 확인하는 데 있다. 실제 압축률은 앞 절의 크기 조건으로 따로 계산한다.

### (2) 표본 밖의 방향

같은 $H$의 열을 $h_i$라 쓰고, 표본으로 $x_1=8h_1$, $x_2=2h_2$만 수집했다고 가정하자. $X=[x_1\ x_2]$의 rank-2 근사는 정확하지만, 새 상태 $x_{\mathrm{new}}=h_3$는 선택 공간에 수직이다. 아래 관계는 이 구성에서 직접 계산된다.[1,2,6,7]

$$
V=[h_1\ h_2],\qquad
\|X-VV^\mathsf TX\|_F=0,\qquad
\|x_{\mathrm{new}}-VV^\mathsf Tx_{\mathrm{new}}\|_2=1.
$$

이는 학습 표본 오차가 0이어도 표본 밖의 상태 오차가 클 수 있음을 보여 주는 반례이다. 한편 원래 $M$을 연산자로 해석하고 입력을 $h_3$로 주면 $Mh_3=0.2h_3$이고 $M_2h_3=0$이다. 행렬 spectral 상대 오차가 2.5%여도 이 입력의 출력 상대 오차는 100%이다. 두 계산은 같은 방향을 버리지만 하나는 상태 집합의 포괄성, 다른 하나는 연산자 오차의 정규화 분모를 시험한다.

### (3) 실행과 검산

아래 Python 3 코드는 외부 패키지 없이 실행한다. 일반 행렬의 SVD 알고리즘을 구현한 것이 아니라, 위에서 이미 구성한 정확한 SVD를 이용해 원행렬과 절단 행렬을 만들고 오차를 확인한다. Spectral 오차는 알려진 singular vector에 대한 작용으로, Frobenius 오차는 모든 성분의 제곱합으로 독립 계산한다. `assert`의 $10^{-12}$는 이 작은 예제의 반올림 허용량이다.

```python
from math import sqrt

H = [[v / 2 for v in row] for row in (
    (1, 1, 1, 1), (1, -1, 1, -1),
    (1, 1, -1, -1), (1, -1, -1, 1))]
sigma = [8.0, 2.0, 0.2, 0.02]
cols = list(zip(*H))


def norm(v):
    return sqrt(sum(x * x for x in v))


def apply(A, v):
    return [sum(a * b for a, b in zip(row, v)) for row in A]


def matrix(r):
    return [[sum(H[i][j] * sigma[j] * H[k][j] for j in range(r))
             for k in range(4)] for i in range(4)]


M = matrix(4)
for r in range(1, 5):
    Mr = matrix(r)
    E = [[M[i][j] - Mr[i][j] for j in range(4)] for i in range(4)]
    spectral = max(norm(apply(E, v)) for v in cols)
    frobenius = sqrt(sum(x * x for row in E for x in row))
    expected_2 = sigma[r] if r < 4 else 0.0
    expected_f = norm(sigma[r:])
    assert abs(spectral - expected_2) < 1e-12
    assert abs(frobenius - expected_f) < 1e-12
    print(r, *(f"{v:.6f}" for v in
               (spectral, frobenius, spectral / sigma[0],
                frobenius / norm(sigma))))


def project(v):
    coeff = [sum(a * b for a, b in zip(v, h)) for h in cols[:2]]
    return [sum(coeff[j] * cols[j][i] for j in range(2))
            for i in range(4)]


for v in (cols[0], cols[1]):
    assert norm([a - b for a, b in zip(v, project(v))]) < 1e-12
new_error = norm([a - b for a, b in zip(cols[2], project(cols[2]))])
y = apply(M, cols[2])
y2 = apply(matrix(2), cols[2])
relative_action_error = norm([a - b for a, b in zip(y, y2)]) / norm(y)
assert abs(new_error - 1.0) < 1e-12
assert abs(relative_action_error - 1.0) < 1e-12
assert sum(s > 0.25 for s in sigma) == 2
print(f"new_state_error={new_error:.6f}")
print(f"relative_action_error={relative_action_error:.6f}")
```

위 코드는 다음 출력을 낸다. 앞의 다섯 열은 순서대로 $r$, 두 절대 오차, 두 상대 오차이며, 끝의 두 줄은 표본 밖 상태와 연산자 출력의 검사 결과이다.

```text
1 2.000000 2.010075 0.250000 0.243685
2 0.200000 0.200998 0.025000 0.024367
3 0.020000 0.020000 0.002500 0.002425
4 0.000000 0.000000 0.000000 0.000000
new_state_error=1.000000
relative_action_error=1.000000
```

## 8. 요약

- SVD 절단은 지정한 행렬의 rank 제약 아래 spectral·Frobenius 오차를 최소화한다. 두 노름의 오차는 각각 첫 누락 특이값과 꼬리 제곱합의 제곱근이다.
- 최적 오차와 최적 행렬의 유일성은 구별한다. Frobenius 경계 간격 조건을 spectral norm에 그대로 적용할 수 없다.
- Numerical rank에는 허용오차·노름·스케일이 필요하다. 잡음과 절단 경계가 겹치면 랭크 판정의 신뢰 범위도 제한된다.
- 열 피벗 QR의 편리함과 strong RRQR의 보장은 다르다. 잔여 블록 오차, 선택 열의 조건, 보간 계수를 함께 확인한다.
- 인수 저장과 반복 작용의 비용 절약은 분해 비용 및 행렬 구조와 비교한다. 표본 재구성 오차와 연산자 오차는 새 상태·출력·역문제 해의 오차를 대신하지 않는다.

## 9. 참고문헌

1. L. N. Trefethen and D. Bau III, *Numerical Linear Algebra* (SIAM, 1997). [DOI: 10.1137/1.9780898719574](https://doi.org/10.1137/1.9780898719574). [University-hosted full text](https://www.stat.uchicago.edu/~lekheng/courses/309/books/Trefethen-Bau.pdf). Lectures 4–5, 특히 Theorems 4.1, 5.1–5.9.
2. A. Uschmajew and B. Vandereycken, “Geometric Methods on Low-Rank Matrix and Tensor Manifolds,” in *Handbook of Variational Methods for Nonlinear Geometric Data*, pp. 261–313 (Springer, 2020). [DOI: 10.1007/978-3-030-31351-7_9](https://doi.org/10.1007/978-3-030-31351-7_9). [Author-hosted full text](https://www.unige.ch/math/vandereycken/papers/published_Uschmajew_V_2020_b.pdf). §§9.2–9.2.1, Theorem 9.1.
3. N. Halko, P. G. Martinsson, and J. A. Tropp, “Finding Structure with Randomness: Probabilistic Algorithms for Constructing Approximate Matrix Decompositions,” *SIAM Review* **53**(2), 217–288 (2011). [DOI: 10.1137/090771806](https://doi.org/10.1137/090771806). [Author preprint](https://arxiv.org/abs/0909.4061). §§1.1–1.4, 3.1–3.3.
4. M. Gu and S. C. Eisenstat, “Efficient Algorithms for Computing a Strong Rank-Revealing QR Factorization,” *SIAM Journal on Scientific Computing* **17**(4), 848–869 (1996). [DOI: 10.1137/0917055](https://doi.org/10.1137/0917055). [Author-hosted full text](https://math.berkeley.edu/~mgu/MA273/Strong_RRQR.pdf). §§1–2, 특히 (1)–(6), Algorithm 1과 Example 1.
5. S. Chandrasekaran and I. C. F. Ipsen, “On Rank-Revealing Factorisations,” *SIAM Journal on Matrix Analysis and Applications* **15**(2), 592–622 (1994). [DOI: 10.1137/S0895479891223781](https://doi.org/10.1137/S0895479891223781). [Author-hosted full text](https://scg.ece.ucsb.edu/publications/papers/Chandrasekaran_1994_SIAM_RankRevealingFactorizations.pdf). §§2, 5–11.
6. P. Benner, S. Gugercin, and K. Willcox, “A Survey of Projection-Based Model Reduction Methods for Parametric Dynamical Systems,” *SIAM Review* **57**(4), 483–531 (2015). [DOI: 10.1137/130932715](https://doi.org/10.1137/130932715). [Author-hosted full text](https://kiwi.oden.utexas.edu/papers/Parametric-model-reduction-survey-Benner-Gugercin-Willcox.pdf). §3.3.1, (3.17)–(3.19)와 표본 최적성의 한계.
7. B. Haasdonk, “Reduced Basis Methods for Parametrized PDEs—A Tutorial Introduction for Stationary and Instationary Problems,” in *Model Reduction and Approximation: Theory and Algorithms*, pp. 65–136 (SIAM, 2017). [DOI: 10.1137/1.9781611974829.ch2](https://doi.org/10.1137/1.9781611974829.ch2). [Author preprint](https://pnp.mathematik.uni-stuttgart.de/ians/haasdonk/data/oberwolfach2014/RBtutorial.pdf). 공개 preprint의 Proposition 3.18, (3.12), Remark 3.20.
