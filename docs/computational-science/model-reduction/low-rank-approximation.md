---
description: 전자구조 상태의 스냅샷에서 SVD와 POD로 축소 기저를 구성하고, 비직교 내적·차원 선택·표본 밖 고유값 정확도와 QR 근사의 한계를 설명한다.
---

# Low-rank approximation

Low-rank approximation을 전자구조 상태에 적용하면 여러 계산에서 얻은 파동함수를 적은 수의 공통 방향으로 표현할 수 있다. 이때 압축할 행렬은 Hamiltonian일 필요가 없다. 관심 상태의 계수벡터를 열로 모은 **snapshot 행렬**을 압축하여 기저 $V$를 얻고, 그 뒤 Hamiltonian을 투영하여 reduced-order model (ROM)을 구성한다. 표본 압축의 최적성과 새 조건에서 푸는 축소 방정식의 정확도는 별도로 확인한다.[1,2]

원래 orbital 수 $M$, 축소 차원 $r$, $c\simeq Va$의 의미는 [Model reduction fundamentals](fundamentals.md)를 따른다. 이 글은 “이미 계산한 상태들로부터 $V$를 어떻게 구하는가”를 다룬다. $\dagger$는 켤레전치이고, 처음에는 고정된 직교 orbital basis와 Euclidean 내적을 가정한다. 비직교 basis의 overlap $S$는 3절에서 포함한다.

## 1. 전자구조 상태와 snapshot 행렬

### (1) 표본의 구성

조건 $\mu$에서 정규화한 고유상태 $c_n(\mu)\in\mathbb C^M$를 얻었다고 하자. $n$은 상태 번호이며 $\mu$는 onsite potential, 외부장 등 계산 조건이다. 총 $N_s$개 상태를 선택하여 다음 행렬을 만든다. 열 하나가 한 조건의 한 상태이고, 행 하나가 고정된 orbital의 계수이다. 아래부터 선택된 $j$번째 열을 간단히 $c_j$라 쓴다. 일반적인 매개변수 해의 POD 표본 구성을 고유상태에 적용한 형태이다.[1,2]

$$
X=[c_{n_1}(\mu_1)\ \cdots\ c_{n_{N_s}}(\mu_{N_s})]
\in\mathbb C^{M\times N_s},\qquad c_j^\dagger c_j=1.
$$

예를 들어 세 조건에서 각각 낮은 두 상태를 모으면 $X=[c_1(\mu_1),c_2(\mu_1),c_1(\mu_2),c_2(\mu_2),c_1(\mu_3),c_2(\mu_3)]$이다. $M$이 수만이어도 열은 여섯 개이며, 이 여섯 상태가 공유하는 공간을 찾는 것이 첫 과제이다. 실제로 몇 방향이면 충분한지는 상태들의 선형독립성과 허용오차에 달려 있다. 표본 수가 많다는 사실만으로 새로운 방향이 많이 추가되는 것은 아니다.[1–4]

Energy window를 사용한다면 $\epsilon_n(\mu)\in[E_{\min},E_{\max}]$인 상태를 선택하며, 에너지 기준과 경계 상태 처리 규칙도 함께 정한다. 특정 band 번호를 선택하는 방법은 이와 다른 표본 규칙이다. 예제에서는 에너지 순서상 낮은 두 상태를 선택한다. 어느 규칙을 쓰든 필요한 상태를 먼저 정하고, 그 상태들의 표현 오차를 줄이는 방향을 나중에 구한다. 이 순서는 POD의 표본 의존성을 전자구조 계산에 적용한 것이다.[1,2]

### (2) 표현과 정규화

서로 다른 계산의 열을 쌓으려면 행 좌표의 뜻이 같아야 한다. Orbital 순서, 원자 대응, basis 종류와 정규화가 다르면 같은 행 번호가 같은 방향을 뜻하지 않을 수 있다. 구조나 격자가 달라진 계산에는 공통 기준 공간으로의 사상이 먼저 필요하다. 사상으로 생긴 보간·표현 오차도 별도로 남긴다. 이는 모든 snapshot이 하나의 내적 공간에 속한다는 POD 가정의 직접적인 적용 조건이다.[1,2]

여러 $k$점의 Bloch 계수를 사용할 때에도 어떤 공통 좌표를 비교하는지 명시한다. 예를 들어 고정 tight-binding orbital 계수 공간에서 $H(k)$의 고유벡터를 모으는 구성은 가능하지만, 서로 다른 Bloch 경계조건의 실공간 함수를 아무 설명 없이 같은 벡터로 쌓는 것은 그 구성을 정의하지 못한다. $k$마다 overlap도 변하면 아래의 고정-$S$ 공식을 그대로 사용할 수 없다. 공통 cell basis를 구성하는 적용은 [Mode-space reduction](mode-space-reduction.md)에서 다룬다.[1,2]

정규화하지 않은 표본은 계수 크기 자체로 최적화에 가중치를 준다. 반면 정규화한 상태를 동일 가중치로 넣으면 각 상태를 같은 제곱오차 기준으로 평가한다. 이 글에서는 평균을 빼지 않는다. 목표는 원점을 지나는 선형 공간에서 $c\simeq Va$를 표현하는 것이며, 평균을 뺀 뒤 복원하는 $c\simeq\bar c+Va$는 affine 공간의 다른 문제이다. 특히 고유벡터의 임의 위상 때문에 상태 평균은 물리적 기준 상태로 자동 결정되지 않는다.[1,2]

## 2. SVD와 singular vector

### (1) 상태 방향과 표본 조합

Singular value decomposition (SVD)은 직사각형 $X$를 정규직교 방향과 비음수 크기로 분해한다. $p=\min(M,N_s)$라 하고, 0인 특이값도 포함하는 thin SVD를 다음과 같이 쓴다. 오른쪽 인수를 $R_s$로 표기하여 축소 기저 $V$와 구별한다.[3,4]

$$
X=U_s\Sigma R_s^\dagger,\qquad
U_s^\dagger U_s=R_s^\dagger R_s=I_p,
\qquad\Sigma=\operatorname{diag}(\sigma_1,\ldots,\sigma_p).
$$

$$
\sigma_1\ge\sigma_2\ge\cdots\ge\sigma_p\ge0,
\qquad q=\operatorname{rank}(X)=\#\{i:\sigma_i>0\}.
$$

| 인수 | 크기 | 이 문제에서의 의미 |
| --- | --- | --- |
| $U_s$ | $M\times p$ | 원래 orbital 계수 공간의 상태 방향 |
| $\Sigma$ | $p\times p$ | 각 방향이 표본 집합에 나타나는 크기 |
| $R_s$ | $N_s\times p$ | 저장된 표본들을 조합하는 방향 |
| $V=U_s[:,1:r]$ | $M\times r$ | 보존할 상태 방향으로 만든 축소 기저 |

$u_i$와 $z_i$를 각각 $U_s,R_s$의 $i$번째 열이라 하자. $z_i$는 $M$개 orbital에 대한 파동함수가 아니라 $N_s$개 snapshot의 조합 계수이다. 양의 $\sigma_i$에 대해 다음 관계를 얻는다.[3,4]

$$
Xz_i=\sigma_i u_i,\qquad
X^\dagger u_i=\sigma_i z_i,\qquad
u_i=\frac{1}{\sigma_i}\sum_{j=1}^{N_s}c_j(z_i)_j.
$$

따라서 왼쪽 singular vector를 $V$로 사용하는 이유는 크기만의 문제가 아니다. 그 열이 실제 상태를 복원할 $M$차원 공간에 있기 때문이다. 오른쪽 singular vector는 어떤 표본 조합이 그 방향을 만드는지 알려 준다. $j$번째 표본에서 방향 $u_i$의 좌표는 $u_i^\dagger c_j=\sigma_i(R_s)_{ji}^*$이다. 이 좌표는 이후 새 Hamiltonian을 풀어 구할 ROM 고유벡터의 좌표와 구별한다.[1,3,4]

### (2) Rank-one 성분과 절단

$0\le r\le p$를 택하고 앞의 $r$개 방향을 남긴다. $U_{s,r},R_{s,r}$는 해당 열들, $\Sigma_r$는 앞부분 대각행렬이다. $\sigma_i>0$인 항은 rank-one 행렬이고, $\sigma_i=0$인 항은 0행렬이다. 절단 후에도 snapshot 근사 $X_r$의 외부 크기는 $M\times N_s$이다.[3,4]

$$
X=\sum_{i=1}^{p}\sigma_i u_i z_i^\dagger,
\qquad X_r=\sum_{i=1}^{r}\sigma_i u_i z_i^\dagger
=U_{s,r}\Sigma_r R_{s,r}^\dagger.
$$

$$
V=U_{s,r},\qquad A=V^\dagger X=\Sigma_rR_{s,r}^\dagger,
\qquad X_r=VA=VV^\dagger X.
$$

$A\in\mathbb C^{r\times N_s}$는 이미 저장된 표본의 축소 좌표이다. 기저를 정한 뒤 원래 $M$성분 상태를 $r$개 숫자로 표현한다는 뜻이 이 인수분해에 드러난다. $r\ge q$이면 정확한 산술에서 $X_r=X$이지만, 새로운 조건의 상태까지 같은 공간에 있다는 결론은 나오지 않는다. 또한 $V,A$만 저장할 때의 압축과 $X_r$ 전체 배열을 다시 만드는 일은 저장 비용이 다르다.[1–4]

## 3. POD basis와 축소 방정식

### (1) 표본 제곱오차의 최소화

Proper orthogonal decomposition (POD)은 지정한 내적에서 표본의 투영 오차 제곱합을 최소화하는 공간을 구한다. 지금의 Euclidean 내적에서는 $V=U_{s,r}$가 그 해이다. $\|\cdot\|_F$는 모든 행렬 원소의 절댓값 제곱합의 제곱근인 Frobenius norm이다.[1,2]

$$
\min_{V^\dagger V=I_r}\|X-VV^\dagger X\|_F^2
=\min_{V^\dagger V=I_r}\sum_{j=1}^{N_s}\|c_j-VV^\dagger c_j\|_2^2
=\sum_{i=r+1}^{p}\sigma_i^2.
$$

평균 제곱오차를 원하면 양변을 $N_s$로 나눈다. 최적 공간은 변하지 않는다. 이 목적은 표본 오차의 합에 관한 것이므로 일부 표본의 큰 오차가 나머지 작은 오차에 가려질 수 있다. 최악 조건이 중요하면 평균뿐 아니라 표본별 최대 오차도 검사한다.[1,2]

기저를 얻은 뒤 새 조건에서 조립한 Hamiltonian $H(\mu)$를 투영한다. 원래 문제를 $Hc=\epsilon Sc$라 하면, 복원 상태 $\widetilde c_n=Va_n$에 대한 Galerkin 방정식은 다음과 같다. $H$는 orbital 사이 Hamiltonian 행렬 원소이며, $S$는 overlap이다.[1,5]

$$
H_r=V^\dagger HV,\qquad S_r=V^\dagger SV,
\qquad H_ra_n=\theta_nS_ra_n,\qquad\widetilde c_n=Va_n.
$$

$S=I$이고 $V^\dagger V=I_r$이면 $S_r=I_r$이다. 이 단계에서 $\theta_n$과 $a_n$을 계산해야 ROM의 고유상태가 나온다. SVD의 $\sigma_i$는 에너지 고유값이 아니며 $A$의 열도 새 조건의 해가 아니다. 조립 Hamiltonian 투영에 $S$를 하나 더 곱하여 $V^\dagger SHV$로 바꾸지 않는다. 내적 가중치는 상태의 직교성과 $S_r$에 들어가며, 조립 행렬의 정의와 함께 일관되게 사용한다.[1,5]

### (2) 비직교 basis의 가중 내적

이제 모든 표본이 같은 Hermitian positive-definite overlap $S$를 공유한다고 하자. 물리적 정규화는 $c^\dagger Sc=1$이고, 상태 오차는 $\|e\|_S^2=e^\dagger Se$로 잰다. 일반 내적 공간의 POD를 좌표로 쓰면 다음 최적화가 된다. $\|E\|_{S,F}^2=\operatorname{tr}(E^\dagger SE)$는 열별 $S$-norm 제곱합이다.[1,2]

$$
\min_{V^\dagger SV=I_r}\|X-VV^\dagger SX\|_{S,F}^2.
$$

가역 행렬 $T$를 $S=T^\dagger T$가 되도록 정한다. 양의 정부호 square root로 $T=S^{1/2}$를 쓰거나, Cholesky 분해 $S=LL^\dagger$에서 $T=L^\dagger$를 쓸 수 있다. $Y=TX$에 보통 SVD를 적용하면 가중 오차를 Euclidean 오차로 바꿀 수 있다. 다음은 앞의 POD 정리를 좌표변환한 직접 유도이다.[1,2,5]

$$
Y=TX=\widehat U_s\widehat\Sigma\widehat R_s^\dagger,
\qquad V=T^{-1}\widehat U_{s,r},\qquad V^\dagger SV=I_r.
$$

$$
a_{\rm proj}=V^\dagger Sc,\qquad P_S=VV^\dagger S,
\qquad\|X-P_SX\|_{S,F}^2=\sum_{i>r}\widehat\sigma_i^2.
$$

$P_S$는 $S$-내적에서의 직교 투영이다. 보통 Euclidean 내적에서는 Hermitian일 필요가 없으므로 $VV^\dagger$로 대체하면 다른 최적화가 된다. 구현에서는 $T^{-1}$을 명시적으로 만들기보다 선형계를 풀어 $V$를 구한다. 코드의 Cholesky 예제는 $L$ 대신 $L^\dagger$를 snapshot에 곱해야 한다는 순서까지 확인한다.[1,2,5]

조건마다 $S(\mu)$가 다르면 각각 $S(\mu)^{1/2}$를 곱한 벡터가 자동으로 하나의 공통 물리 공간에 놓이는 것은 아니다. 기준 표현으로의 사상과 그 내적을 먼저 정하거나, 조건별 가중 오차를 포함하는 별도 최적화를 정의해야 한다. 같은 계수 좌표에서 고정 기준 metric으로 $V$를 구하는 선택은 가능하지만, 이때 각 조건의 $S_r(\mu)=V^\dagger S(\mu)V$가 항등행렬이라고 가정하지 않는다. 이는 고정-$S$ 유도의 적용 범위에서 도출되는 제한이다.[1,2,5]

## 4. Singular value와 축소 차원

### (1) 꼬리 오차와 numerical rank

Spectral norm $\|X\|_2$는 단위 표본 조합을 입력했을 때 출력 상태의 최대 크기이다. Frobenius norm은 모든 표본의 제곱합을 센다. $r=p$일 때 $\sigma_{p+1}=0$으로 정하면 다음 식이 성립한다.[3,4]

$$
\|X\|_2=\sigma_1,\qquad\|X\|_F^2=\sum_i\sigma_i^2,
\qquad\|X-X_r\|_2=\sigma_{r+1},
\qquad\|X-X_r\|_F^2=\sum_{i>r}\sigma_i^2.
$$

$X\ne0$에서 차원 선택에 쓰는 상대 오차를 각각 정의한다. 작은 특이값이 많이 모이면 꼬리 제곱합이 커질 수 있으므로 두 기준은 같은 $r$을 요구하지 않을 수 있다.[3,4]

$$
e_2(r)=\frac{\sigma_{r+1}}{\sigma_1},\qquad
e_F(r)=\sqrt{\frac{\sum_{i>r}\sigma_i^2}{\sum_i\sigma_i^2}},
\qquad f_r=1-e_F(r)^2.
$$

POD 문헌에서 $f_r$를 보존된 “energy”의 비율이라고 부르기도 한다. 여기서는 상태 norm 제곱의 비율이며 전자 에너지, 점유수 또는 total energy의 비율이 아니다. 정규화한 $N_s$개 상태의 동일 가중치 표본이면 $\sum_i\sigma_i^2=N_s$이다. 따라서 $f_r$가 커도 그 숫자만으로 eV 단위 band 오차를 판정할 수 없다.[1,2]

절대 spectral 허용오차 $\tau\ge0$에 대한 numerical rank를 다음처럼 정의할 수 있다. 등호에 걸린 특이값은 버리는 규약이다.[3,4]

$$
r_\tau=\#\{i:\sigma_i>\tau\}
=\min\{r:\|X-X_r\|_2\le\tau\}.
$$

Numerical rank는 행렬의 대수적 rank와 달리 허용오차·스케일·내적에 의존한다. 표본 오차나 반올림 수준 아래의 작은 특이값에 물리적 의미를 부여하지 않는다. 실제 차원은 꼬리 오차로 후보를 정한 뒤 새 조건의 고유값과 잔차를 검사하여 결정한다. $S\ne I$이면 위 기준의 특이값은 $X$가 아니라 $TX$에서 계산한 $\widehat\sigma_i$이다.[1–4]

### (2) 표본 가중치와 축퇴

표본마다 양의 무차원 가중치 $w_j$를 줄 때는 $D_w=\operatorname{diag}(\sqrt{w_1},\ldots,\sqrt{w_{N_s}})$를 사용한다. 다음 식은 열별 제곱오차에 가중치를 주는 목적을 표준 POD로 변환한다. $D_w$는 상태 공간의 overlap $S$와 역할이 다르다.[1,2]

$$
X_w=XD_w,\qquad
\sum_jw_j\|c_j-P_Sc_j\|_S^2
=\|T(X-P_SX)D_w\|_F^2.
$$

표본을 중복 저장하는 것도 해당 조건의 가중치를 늘린다. 특정 band만 더 중요하게 다룰 수 있지만, 그러면 얻은 공간의 최적성도 그 선택에 대한 것이다. 수치적 편의를 위한 정규화, 물리적인 점유 가중치와 조건 적분을 위한 quadrature 가중치를 혼동하지 않는다. 이들은 다른 오차 목적을 정의한다.[1,2]

고유벡터의 개별 위상을 바꾸어도 동일 가중치의 비중심화 POD 공간은 바뀌지 않는다. 대각 unitary 행렬 $D_\phi$에 대해 다음 관계가 성립하기 때문이다. 같은 가중치로 완전하게 포함한 축퇴 상태 block 안의 unitary 회전에도 같은 논리가 적용된다.[1,2,4]

$$
(XD_\phi)(XD_\phi)^\dagger=XX^\dagger.
$$

다만 절단 경계에서 $\sigma_r=\sigma_{r+1}>0$이면 어떤 동등한 방향을 남길지 유일하지 않다. 거의 같은 특이값에서는 작은 표본 변화로 개별 singular vector가 크게 달라질 수도 있으므로, 열의 부호나 성분만 비교하기보다 보존한 공간과 오차를 비교한다. 전체 축퇴 block 대신 일부 상태만 선택하거나 가중치를 다르게 주면 그 선택의 회전 불변성도 별도로 확인해야 한다.[2,4]

## 5. Snapshot 근사와 Hamiltonian 근사

### (1) 근사 대상과 energy window

$X$의 SVD는 관심 상태의 표현 문제를 푼다. $H$의 SVD는 Hamiltonian의 행렬 작용을 근사한다. $S=I$인 Hermitian $H$를 정확한 unitary 고유기저 $C$로 분해하면 다음 대수적 관계를 얻는다.[3–5]

$$
H=C\operatorname{diag}(\epsilon_n)C^\dagger,\qquad
H^\dagger H=C\operatorname{diag}(\epsilon_n^2)C^\dagger,
\qquad\sigma(H)=\{|\epsilon_n|\}\ \text{내림차순}.
$$

즉 큰 singular value를 남기는 $H$의 절단은 절댓값이 큰 에너지 방향을 남긴다. 가장 낮은 에너지나 Fermi level 근처 상태를 선택하는 규칙과 다르다. 예를 들어 $H=\operatorname{diag}(-1,0.2,4)\ \mathrm{eV}$의 rank-one SVD는 4 eV 방향을 남긴다. 관심 상태가 앞의 두 방향이라면 그 상태들을 $X$에 넣는 편이 목적에 맞다. 이 예는 위 관계에 대각 원소를 대입한 계산이다.[3–5]

에너지 원점을 $\alpha$만큼 바꾸어 $H'=H-\alpha I$로 만들면 고유벡터는 같지만 singular value 순서는 $|\epsilon_n-\alpha|$에 따라 달라진다. 비직교 조립 행렬에서는 같은 이동이 $H'=H-\alpha S$이다. 또한 $H$ 자체의 Euclidean SVD는 일반화 고유값 $\epsilon_n$의 절댓값과 곧바로 같지 않다. 고정 $S$에서는 $S^{-1/2}HS^{-1/2}$를 Hermitian 표준 문제로 바꾼 뒤 앞의 논의를 적용한다.[3–5]

| 압축 대상 | 큰 특이값의 의미 | 추가로 필요한 검증 |
| --- | --- | --- |
| 정규화한 상태의 $X$ | 선택 표본의 공통 방향 | 새 상태의 표현과 축소 고유쌍 |
| Hermitian $H$, $S=I$ | 큰 $\lvert\epsilon\rvert$의 행렬 작용 | 원하는 energy window의 보존 |
| 가역 선형계 행렬 $K$ | 큰 입력–출력 증폭 방향 | 역문제의 가역성과 해 오차 |

마지막 행의 주의점도 SVD에서 직접 나온다. $K$가 정방 가역이어도 rank-$r$ 절단에서 $r<M$이면 절단 행렬은 특이해진다. 작은 행렬 오차가 가역성을 보존하지 않으며, pseudoinverse로 푸는 것은 버린 방향을 제외하는 다른 문제이다. 반면 $V^\dagger KV$는 차원이 작은 별도 방정식이다. 이 둘의 구분은 Hamiltonian의 행렬 압축과 상태 공간 축소에도 그대로 필요하다.[3,4]

### (2) 새로운 조건의 검증

기저 생성과 차원 조정에 사용하지 않은 조건에서 먼저 정확한 상태 $c$의 표현 오차를 잰다. $S$-정규직교 $V$에 대해 최소 거리와 최적 좌표는 다음과 같다.[1,2,5]

$$
\eta_{\rm repr}(c)=\|c-VV^\dagger Sc\|_S,
\qquad a_{\rm proj}=V^\dagger Sc.
$$

그 다음 작은 고유값 문제를 풀어 얻은 $a_n$으로 복원하고 원래 문제의 잔차를 계산한다. $\theta_n$은 Ritz value이다. Galerkin 조건은 잔차의 선택 공간 성분만 0으로 만든다.[1,5]

$$
\rho_n=HV a_n-\theta_nSVa_n,\qquad
V^\dagger\rho_n=0.
$$

따라서 작은 축소계의 잔차만 보고 종료하지 않는다. 상태 표현 오차, 비교 가능한 정확한 고유값과의 차이, 전체 $\|\rho_n\|_2$를 각각 기록한다. 고정 비직교 $S$에서 물리적 내적에 대응하는 잔차 norm은 $\sqrt{\rho_n^\dagger S^{-1}\rho_n}$이다. 이 식은 표준화한 문제의 잔차가 $S^{-1/2}\rho_n$이라는 대입에서 얻는다.[1,5]

표본의 평균 제곱오차가 작아도 새 조건에서 공간 밖 성분이 생길 수 있다. 차원을 늘리는 검사와 표본 조건을 넓히는 검사는 서로 다른 결함을 찾는다. 전자는 현재 표본의 누락 방향, 후자는 학습 집합의 대표성을 시험한다. 유한 시험점에서의 성공을 연속한 모든 조건의 보증으로 해석하지 않으며, 오차를 보고 기저를 다시 조정한 시험점은 이후 최종 시험 집합과 구분한다.[1,2]

## 6. 세 orbital 모형의 POD 검산

### (1) 학습·검증 표본

선행 문서의 교육용 모형을 사용한다. 물질을 fitting한 Hamiltonian은 아니며, $S=I_3$이고 모든 행렬 원소와 $\mu$의 단위는 eV이다. 코드에서는 eV로 나눈 숫자를 저장한다.

$$
H(\mu)=H_0+\operatorname{diag}(0,\mu,0),\qquad
H_0=\begin{pmatrix}0&-1&0.3\\-1&0.5&0.4\\0.3&0.4&4\end{pmatrix}\ \mathrm{eV}.
$$

학습 조건은 $\mu=-0.5,0,0.5\ \mathrm{eV}$이고 각 조건의 낮은 두 정규화 상태를 동일 가중치로 넣는다. 따라서 $X$는 $3\times6$이다. 시험 조건은 학습점과 겹치지 않는 $\mu=-0.75,-0.25,0.25,0.75\ \mathrm{eV}$이다. 중간 두 점은 학습 구간 안에 있고 양 끝 두 점은 밖에 있다. 다음 코드는 표본 구축, SVD, 차원별 projection과 잔차 계산을 모두 수행한다. NumPy의 선형대수 연산을 사용하며 숨긴 입력이나 난수는 없다.

```python
import numpy as np

H0 = np.array([[0., -1., .3], [-1., .5, .4], [.3, .4, 4.]])
def h(mu):
    return H0 + np.diag([0., mu, 0.])

def states(mu):
    e, c = np.linalg.eigh(h(mu))
    return e[:2], c[:, :2]

train = [-.5, 0., .5]
test = [-.75, -.25, .25, .75]
X = np.column_stack([states(mu)[1] for mu in train])
Us, sigma, Rh = np.linalg.svd(X, full_matrices=False)
assert np.allclose(X, (Us * sigma) @ Rh)
print('sigma:', ' '.join(f'{s:.8f}' for s in sigma))
print('r train_rec test_rec eig_eV residual_eV')
for r in (1, 2, 3):
    V = Us[:, :r]
    P = V @ V.conj().T
    fit = np.linalg.norm(X - P @ X, 'fro') / np.linalg.norm(X, 'fro')
    assert np.isclose(fit, np.linalg.norm(sigma[r:]) / np.linalg.norm(sigma))
    errs = []
    for mu in test:
        e, C = states(mu)
        theta, a = np.linalg.eigh(V.conj().T @ h(mu) @ V)
        n = min(2, r)
        Cr = V @ a[:, :n]
        rho = h(mu) @ Cr - Cr * theta[:n]
        assert np.linalg.norm(V.conj().T @ rho) < 1e-12
        errs.append((np.linalg.norm(C - P @ C, 'fro') / np.sqrt(2),
                     np.max(np.abs(theta[:n] - e[:n])),
                     np.max(np.linalg.norm(rho, axis=0))))
    maxima = np.max(errs, axis=0)
    print(r, *(f'{v:.6e}' for v in (fit, *maxima)))
# Same states in nonorthogonal coordinates: y = B c, S = B^H B.
B = np.array([[1., .2, 0.], [0., 1.3, .1], [0., 0., .8]])
S = B.conj().T @ B
Xs = np.linalg.solve(B, X)
L = np.linalg.cholesky(S)             # S = L L^H
Y = L.conj().T @ Xs
Uw, sw, _ = np.linalg.svd(Y, full_matrices=False)
Vw = np.linalg.solve(L.conj().T, Uw[:, :2])
assert np.allclose(Vw.conj().T @ S @ Vw, np.eye(2))
assert np.allclose(sw, sigma)
assert np.allclose(B @ Vw @ Vw.conj().T @ S @ Xs,
                   Us[:, :2] @ Us[:, :2].conj().T @ X)
for mu in test:
    Hs = B.conj().T @ h(mu) @ B
    assert np.allclose(np.linalg.eigvalsh(Vw.conj().T @ Hs @ Vw),
                       np.linalg.eigvalsh(Us[:, :2].conj().T @ h(mu) @ Us[:, :2]))
print('weighted_POD: OK')
```

마지막 검산은 같은 물리 상태 $y$를 비직교 좌표 $c$로 다시 쓰는 $y=Bc$를 사용한다. 따라서 $S=B^\dagger B$, $H_s=B^\dagger HB$, $X_s=B^{-1}X$이다. 새로운 물리 모형을 만든 것이 아니다. 코드의 weighted POD가 같은 특이값, 원래 좌표로 되돌린 같은 투영 상태와 같은 축소 고유값을 주는지 `assert`로 확인한다. Cholesky 방향이나 추가 overlap 곱의 오류를 이 동치성으로 검사할 수 있다.[1,2,5]

### (2) 차원과 spectrum·잔차

계산한 특이값은 $(1.73205081,1.73191265,0.02187664)$이다. 앞의 두 값이 비슷하므로 하나만 남기는 것은 낮은 두 상태를 표현하는 문제에 적절하지 않다. POD는 두 상태를 동일 가중치로 보았으며, 첫 POD 방향이 가장 낮은 에너지 상태를 먼저 근사하도록 최적화하지 않았다. 다음 표의 $r=1$ 고유값 오차는 존재하는 하나의 Ritz value와 가장 낮은 정확한 고유값의 차이이며, 둘째 상태에 대한 결과는 계산할 수 없다.[1,2]

학습 오차는 $\|X-VV^\dagger X\|_F/\|X\|_F$이다. 시험점의 낮은 두 상태를 $C_2=[c_1,c_2]$라 하면 재구성 오차는 $\|(I-VV^\dagger)C_2\|_F/\sqrt2$로 정의한다. 이 값은 두 상태의 위상과 그 둘을 함께 회전하는 선택에 불변이므로 단순 부호 차이를 오차로 세지 않는다. 에너지 오차와 잔차는 $n_r=\min(2,r)$개의 낮은 Ritz pair에 대해 구한다.[1,2,5]

$$
\eta_E(\mu,r)=\max_{1\le n\le n_r}|\theta_n-\epsilon_n|,
\qquad\eta_\rho(\mu,r)=\max_{1\le n\le n_r}\|HVa_n-\theta_nVa_n\|_2.
$$

표의 시험 열은 네 시험점에서 각각 구한 최댓값이며 서로 다른 조건에서 발생할 수 있다. $r=3$ 행의 값은 환경에 따른 반올림 차이를 피하도록 실행값을 보수적으로 묶었다.

| $r$ | 학습 상대 재구성 오차 | 시험 상대 재구성 오차 | 시험 $\eta_E$ (eV) | 시험 $\eta_\rho$ (eV) |
| --- | --- | --- | --- | --- |
| 1 | $7.071068\times10^{-1}$ | $7.071068\times10^{-1}$ | $6.620153\times10^{-1}$ | $9.630652\times10^{-1}$ |
| 2 | $8.931100\times10^{-3}$ | $1.943603\times10^{-2}$ | $1.598581\times10^{-3}$ | $6.032054\times10^{-2}$ |
| 3 | $<10^{-14}$ | $<10^{-14}$ | $<10^{-14}$ | $<10^{-14}$ |

$r=2$에서는 약 0.89%의 학습 재구성 오차보다 시험 재구성 오차가 크다. 에너지 오차는 약 1.60 meV이지만 전체 잔차는 약 60.3 meV이다. 이 숫자들은 다른 양을 측정하므로 서로 대체하지 않는다. $r=3$은 원래 전체 공간이므로 이 작은 모형에서 압축이 사라지고 반올림 수준으로 정확해진다. 이 예제는 속도 향상을 측정하는 benchmark가 아니라 상태 압축에서 작은 고유값 문제까지 이어지는 검산이다.

낮은 두 상태를 모든 조건에서 정확히 두 방향으로 나타낼 수 있었다면 셋째 특이값이 0이었을 것이다. 여기서는 작지만 양수이므로 학습 상태들의 합집합이 세 번째 방향도 포함한다. “조건마다 상태 두 개를 선택했다”는 사실과 “모든 조건을 정확히 표현하는 공통 공간의 차원이 2이다”라는 주장이 다른 이유이다.[1–4]

## 7. 최적 근사와 QR 심화

### (1) Eckart–Young–Mirsky와 유일성

앞의 POD 최적성은 더 일반적인 행렬 근사 정리와 연결된다. Eckart–Young–Mirsky 정리는 같은 크기의 모든 rank-$r$ 이하 행렬 $F$ 중 SVD 절단이 spectral·Frobenius norm 오차를 최소화함을 말한다. 원소의 부호, 희소성, 특정 orbital 선택 등 추가 제약은 없는 문제이다.[3,4]

$$
\min_{\operatorname{rank}(F)\le r}\|X-F\|_2=\sigma_{r+1},
\qquad\min_{\operatorname{rank}(F)\le r}\|X-F\|_F^2=\sum_{i>r}\sigma_i^2.
$$

Frobenius 최적성이 열공간 선택과 연결되는 이유도 확인할 수 있다. 후보 $F$의 열공간에 대한 직교 projector를 $P$라 하면 두 직교 성분으로 나뉜다.[3,4]

$$
\|X-F\|_F^2=\|(I-P)X\|_F^2+\|PX-F\|_F^2.
$$

고정한 공간에서는 $F=PX$가 최선이다. 그 다음 어느 공간이 표본의 제곱합을 가장 많이 보존하는지 선택하면 앞의 POD 문제가 된다. Spectral 오차에서는 rank-$r$ 행렬이 앞의 $r+1$개 오른쪽 singular vector가 만드는 공간에서 적어도 한 방향을 소거하므로, 그 방향의 누락량 $\sigma_{r+1}$보다 작은 최악 오차를 얻을 수 없다.[3,4]

$0<r<q$에서 $\sigma_r>\sigma_{r+1}$이면 Frobenius 최적 행렬은 유일하다. 경계 특이값이 같으면 동등한 방향 중 무엇을 남기는지에 따라 여러 최적 행렬이 생길 수 있다. 행렬의 유일성과 기저 열의 부호·위상 선택의 유일성은 다르다.[2,4]

Spectral norm에서는 경계 간격이 있어도 최적 행렬이 유일하지 않을 수 있다. 직접적인 무차원 반례로 $F_t=\operatorname{diag}(t,0)$, $1\le t\le3$을 생각하자.[3,4]

$$
X=\operatorname{diag}(2,1),\qquad
\|X-F_t\|_2=\max(|2-t|,1)=1,
\qquad\|X-F_t\|_F=\sqrt{(2-t)^2+1}.
$$

모든 $F_t$가 rank one이며 같은 spectral 최적값을 달성하지만 Frobenius 오차는 $t=2$에서만 최소이다. 따라서 “최적 기저”라는 표현에는 어떤 행렬·내적·오차 목적을 최적화했는지 반드시 붙여야 한다.

### (2) QR·RRQR과 열 선택

SVD 기저는 보통 여러 snapshot의 조합이다. 실제 표본 열을 선택하여 공간을 만들고 싶다면 column-pivoted QR이 유용하다. $\Pi$는 열 순열, $Q=[Q_1,Q_2]$는 unitary 행렬이고, $Q_1$의 열은 정규직교하며 선택된 앞의 $r$개 열공간을 포함하는 공간을 생성한다. 선택 열들이 선형독립, 즉 $R_{11}$이 가역일 때 두 공간이 같아져 $Q_1$이 선택 열공간의 기저가 된다. 아래는 $r\le\min(M,N_s)$에서의 block 표현이다.[3,6]

$$
X\Pi=[Q_1\ Q_2]
\begin{pmatrix}R_{11}&R_{12}\\0&R_{22}\end{pmatrix},
\qquad X_{\rm QR}=Q_1[R_{11}\ R_{12}]\Pi^\dagger.
$$

$$
\|X-X_{\rm QR}\|_2=\|R_{22}\|_2,
\qquad\|X-X_{\rm QR}\|_F=\|R_{22}\|_F.
$$

선택한 실제 열을 $C=X\Pi[:,1:r]=Q_1R_{11}$이라 하자. $R_{11}$이 가역일 때 나머지 열을 이 열들의 조합으로 표현할 수 있다. 이는 SVD와 달리 선택된 열의 정체성을 보존하는 interpolative 형태이다.[3,6]

$$
X\Pi\simeq C[I_r\ R_{11}^{-1}R_{12}].
$$

작은 $R_{22}$만으로 선택 열의 조건이 좋다고 할 수는 없다. $R_{11}$이 거의 특이하거나 $R_{11}^{-1}R_{12}$가 크면 계수 해석과 안정성에 문제가 생길 수 있다. Rank-revealing QR (RRQR)은 작은 잔여 block과 적절한 선행 block을 함께 요구하며, strong RRQR은 보간 계수도 제한한다. 보통의 열 피벗 QR이 모든 행렬에서 strong RRQR의 보장을 갖는 것은 아니다.[3,6]

따라서 구현 결과에서는 잔여 block의 norm, 선택 열의 선형독립성과 보간 계수를 따로 확인한다. 비직교 상태 norm이 목적이라면 $TX$에서 선택·직교화를 수행하고 좌표를 되돌리는 방식으로 내적도 맞춘다. 원래 $X$에 Euclidean QR을 적용하고 같은 물리적 최적성을 주장하지 않는다.[1–3,6]

### (3) 비용과 적용 한계

밀집 $M\times N_s$ 행렬의 전체 SVD 비용은 대표적으로 $O(MN_s\min(M,N_s))$이다. $r$이 작을 때 partial factorization이나 randomized range approximation으로 비용을 줄일 수 있지만, 최종 근사의 실제 잔차를 확인해야 한다. 행렬의 희소성, matrix–vector product 접근과 메모리 이동 비용에 따라 유리한 알고리즘이 달라진다.[3,4]

두 인수 $V,A$를 저장하면 원소 수는 $r(M+N_s)$이고 원래 snapshot 저장량은 $MN_s$이다. 작은 $r$이라는 말만으로 충분하지 않으며 다음 부등식이 성립해야 인수 저장 자체가 이득이다.[3,4]

$$
r(M+N_s)<MN_s.
$$

$N_s\ll M$이면 $X^\dagger X$의 작은 고유값 문제로 오른쪽 방향을 구한 뒤 $u_i=Xz_i/\sigma_i$로 복원하는 method of snapshots도 가능하다. 가중 문제에서는 $X^\dagger SX$를 사용한다. 양의 특이값에 대해 Gram 행렬의 고유값은 $\sigma_i^2$이므로, 아주 작은 방향을 식별할 때의 수치적 정밀도는 직접 SVD와 구분해야 한다. 이 관계는 Gram 기반 POD와 SVD의 대수적 연결에서 나온다.[2–4]

POD의 준비 비용에는 원래 고유상태를 구하는 계산도 포함된다. 축소 후에도 매번 큰 $H(\mu)$를 조립하고 $V^\dagger H(\mu)V$를 계산한다면 전체 차원 비용이 남는다. 밀집 행렬곱의 크기를 세면 이 투영의 비용은 $O(M^2r+Mr^2)$이고, 한 상태의 복원은 $O(Mr)$이다. 따라서 작은 eigenproblem만의 속도를 전체 계산의 speedup으로 보고하지 않는다.[1,2]

이 예제처럼 $H(\mu)=H_0+\mu D$인 경우에는 $V^\dagger H_0V$와 $V^\dagger DV$를 미리 계산할 수 있다. 여기서 $D=\operatorname{diag}(0,1,0)$는 무차원이고 $\mu$는 eV이다. 일반적인 Hamiltonian에서도 적은 수의 분리항이 있으면 같은 offline–online 구성을 사용할 수 있지만, 그 표현의 정확도와 조립 비용은 별도 문제이다.[1,2]

$$
H_r(\mu)=V^\dagger H_0V+\mu V^\dagger DV.
$$

최종적으로 남겨야 할 정보는 표본 조건·상태 선택·내적·가중치, 특이값과 차원 기준, 새 조건의 상태·고유값·잔차 오차, 준비·투영·작은 문제·복원 비용이다. POD는 이 중 기저 구성과 표본 표현 오차를 담당한다. 축소 방정식의 정확도와 물리적 출력까지 검증한 뒤에야 지정 범위에서 사용할 ROM이 된다.[1,2]

## 8. 요약

- $X$의 열은 관심 파동함수의 계수벡터이다. 왼쪽 singular vector는 상태 공간의 방향이고 오른쪽 singular vector는 표본 조합이다.
- POD는 지정한 표본·내적·가중치의 재구성 제곱오차를 최소화한다. $V$를 구한 뒤 $H_r,S_r$를 구성하고 작은 고유값 문제를 푸는 단계가 별도로 필요하다.
- 고정 비직교 overlap에서는 $TX$의 SVD를 구하고 $V=T^{-1}\widehat U_{s,r}$로 되돌린다. 서로 다른 표현이나 변하는 overlap은 공통 공간의 정의부터 확인한다.
- 특이값 꼬리는 학습 오차의 기준이다. Hamiltonian의 큰 singular value, 낮은 에너지 상태와 POD의 보존 “energy”는 서로 다른 양이다.
- 차원별 시험 상태의 표현·고유값·전체 잔차를 비교하고, QR의 열 선택 조건과 준비·조립·복원 비용도 함께 검증한다.

## 9. 참고문헌

1. P. Benner, S. Gugercin, and K. Willcox, “A Survey of Projection-Based Model Reduction Methods for Parametric Dynamical Systems,” *SIAM Review* **57**(4), 483–531 (2015). [DOI: 10.1137/130932715](https://doi.org/10.1137/130932715). [Full text](https://kiwi.oden.utexas.edu/papers/Parametric-model-reduction-survey-Benner-Gugercin-Willcox.pdf). §2, §3.3.1–3.3.2, Eqs. (3.17)–(3.20), weighted-inner-product footnote 4.
2. B. Haasdonk, “Reduced Basis Methods for Parametrized PDEs—A Tutorial Introduction for Stationary and Instationary Problems,” in *Model Reduction and Approximation: Theory and Algorithms*, 65–136 (SIAM, 2017). [DOI: 10.1137/1.9781611974829.ch2](https://doi.org/10.1137/1.9781611974829.ch2). [Author preprint](https://pnp.mathematik.uni-stuttgart.de/ians/haasdonk/data/oberwolfach2014/RBtutorial.pdf). §§2–3, Proposition 3.18–3.19, Eq. (3.12), Remark 3.20; numbering follows the preprint.
3. N. Halko, P. G. Martinsson, and J. A. Tropp, “Finding Structure with Randomness: Probabilistic Algorithms for Constructing Approximate Matrix Decompositions,” *SIAM Review* **53**(2), 217–288 (2011). [DOI: 10.1137/090771806](https://doi.org/10.1137/090771806). [Full text](https://arxiv.org/pdf/0909.4061). §§1.1–1.2, 3.1–3.3.
4. A. Uschmajew and B. Vandereycken, “Geometric Methods on Low-Rank Matrix and Tensor Manifolds,” in *Handbook of Variational Methods for Nonlinear Geometric Data*, 261–313 (Springer, 2020). [DOI: 10.1007/978-3-030-31351-7_9](https://doi.org/10.1007/978-3-030-31351-7_9). [Full text](https://www.unige.ch/math/vandereycken/papers/published_Uschmajew_V_2020_b.pdf). §§9.2–9.2.1, Theorem 9.1.
5. Y. Saad, *Numerical Methods for Large Eigenvalue Problems*, revised edition (2011). [Author-hosted full text](https://www-users.cse.umn.edu/~saad/eig_book_2ndEd.pdf). §§4.3, 9.2; Rayleigh–Ritz Algorithm 4.5 and generalized symmetric problems.
6. M. Gu and S. C. Eisenstat, “Efficient Algorithms for Computing a Strong Rank-Revealing QR Factorization,” *SIAM Journal on Scientific Computing* **17**(4), 848–869 (1996). [DOI: 10.1137/0917055](https://doi.org/10.1137/0917055). [Full text](https://math.berkeley.edu/~mgu/MA273/Strong_RRQR.pdf). §§1.1–1.2, Eqs. (1)–(6).
