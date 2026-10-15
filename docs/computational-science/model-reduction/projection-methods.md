---
description: 전자구조 고유값 문제의 Galerkin·Rayleigh–Ritz 투영에서 출발하여 비직교 overlap, Ritz 오차, 기저 보강, resolvent와 일반 Petrov–Galerkin 모형을 설명한다.
---

# Projection methods

Projection method는 상태를 작은 공간에서 찾고, 그 공간에 맞는 방정식을 만드는 방법이다. 전자구조에서는 원래 문제 $Hc=\epsilon Sc$의 상태를 $c\simeq Va$로 제한한 뒤 작은 고유값 문제를 푼다. 이때 어떤 상태를 표현할 수 있는지와 원래 방정식을 얼마나 만족하는지는 서로 다른 질문이다.[1,2]

원래 orbital 수 $M$, 축소 차원 $r$, 기저 $V\in\mathbb C^{M\times r}$의 물리적 뜻은 [Model reduction fundamentals](fundamentals.md)를 따른다. Snapshot으로 $V$를 만드는 과정은 [Low-rank approximation](low-rank-approximation.md)에 설명되어 있다. 여기서는 $V$를 정한 다음의 방정식 구성과 검증을 다룬다. $H=H^\dagger$는 조립된 Hamiltonian, $S=S^\dagger>0$는 원래 orbital overlap이며 $\dagger$는 켤레전치이다. $V$의 열은 선형독립이라고 가정한다.

## 1. Trial space와 축소 고유값 문제

Galerkin 투영의 결과는 다음 일반화 고유값 문제이다. $a\in\mathbb C^r$는 축소 좌표, $H_r,S_r\in\mathbb C^{r\times r}$는 축소 Hamiltonian과 overlap이다. 첫 식의 $\epsilon$은 이 작은 문제에서 구하는 에너지이며, 이후 원래 고유값과 구별할 때에는 **Ritz value** $\theta$로 쓴다.[1,2]

$$
H_ra=\epsilon S_ra,\qquad
H_r=V^\dagger HV,\qquad S_r=V^\dagger SV.
$$

$H_r$의 원소는 선택한 새 orbital 사이의 Hamiltonian 행렬 원소이다. 따라서 단순히 낮은 에너지 숫자 몇 개를 저장하는 것이 아니라, 선택 공간 안에서 상태가 섞이는 방정식을 보존한다. $r<M$이면 그 공간 밖의 상태 성분에 대해서는 별도의 정확도 검증이 필요하다.[1,2]

### (1) 상태 제한과 residual

원래 atomic orbital (AO)을 $\phi_\alpha$, $V$의 열을 $v_j$라 하자. 새 orbital $\chi_j$와 근사 상태 $\widetilde\psi$는 다음과 같다. **Trial space**는 이 $\chi_j$들의 모든 선형결합이며, 계수 공간에서는 $\mathcal V=\operatorname{range}(V)$에 해당한다.[1,2,3]

$$
|\chi_j\rangle=\sum_{\alpha=1}^{M}|\phi_\alpha\rangle V_{\alpha j},
\qquad |\widetilde\psi\rangle=\sum_{j=1}^{r}|\chi_j\rangle a_j,
\qquad \widetilde c=Va.
$$

예를 들어 $V=[e_1,e_2]$이면 처음 두 AO로만 상태를 만든다. 반면 $V$의 열이 여러 AO를 섞은 벡터이면 새 orbital 하나에도 세 번째 AO 성분이 들어갈 수 있다. 두 경우 모두 $r=2$이지만 표현하는 물리적 공간은 다르다. 축소 차원만으로 공간의 내용을 판단할 수 없는 이유이다.[1,2]

후보 에너지 $\theta$와 상태 $Va$를 원래 방정식에 넣어 **전체 residual**을 정의한다. $H$와 $\theta$를 eV로 쓰고 정규화한 orbital을 사용하면 아래 잔차 성분도 eV 단위를 갖는다.[1,2]

$$
\rho=HVa-\theta SVa\in\mathbb C^M.
$$

$\rho=0$이면 복원 상태가 원래 이산 고유값 문제의 정확한 해이다. 그러나 $r$개의 좌표로 $M$개의 잔차 성분을 모두 0으로 만들 수 있다고 가정할 수는 없다. 투영법은 그중 어떤 방정식 조합을 만족시킬 것인지를 정한다.[1,2]

### (2) Galerkin 조건과 Rayleigh–Ritz

**Test space**는 잔차를 검사하는 함수들의 공간이다. 그 계수 기저를 $Z\in\mathbb C^{M\times r}$로 쓰면 $Z^\dagger\rho=0$은 모든 test orbital에 대해 방정식의 불일치를 0으로 만드는 조건이다. 이 문서의 $Z$는 상태를 복원하는 기저 $V$와 역할이 다르며, hopping에 사용하는 $W$와도 구별한다.[1,2,4]

Galerkin은 물리적 trial space와 test space를 같게 선택하며 보통 $Z=V$로 구현한다. 위 잔차를 대입하면 도입부의 축소식을 바로 얻는다.[1,2]

$$
V^\dagger\rho=0
\quad\Longleftrightarrow\quad
V^\dagger HVa=\theta V^\dagger SVa.
$$

Hermitian 문제에서 이렇게 얻은 작은 고유값 문제를 푸는 절차가 **Rayleigh–Ritz** 방법이다. $(\theta,a)$를 구한 뒤 원래 공간으로 복원한 $Va$가 Ritz vector이다. 작은 행렬의 좌표 $a$ 자체를 원래 orbital 계수와 혼동하지 않는다. $H_r$는 Hermitian이고 $S_r>0$이므로 Ritz value는 실수이며 서로 다른 Ritz vector를 $S$ 내적에서 정규직교하게 선택할 수 있다.[1,2]

투영된 잔차가 0이라는 것은 전체 잔차가 선택 공간에 보이지 않는다는 뜻이다. 좌표 선택 $V=[e_1,e_2]$에서는 첫 두 방정식만 맞고 세 번째 방정식에 잔차가 남을 수 있다. 이 누락된 방정식이 수치 예제에서 세 번째 orbital과의 coupling을 검출한다.[1,2]

| 대상 | 정하는 내용 | 전자구조에서의 의미 |
| --- | --- | --- |
| Trial basis $V$ | 복원 상태 $Va$의 범위 | 사용할 새 orbital 조합 |
| Test basis $Z$ | $Z^\dagger\rho=0$인 방정식 조합 | 잔차를 읽는 orbital 조합 |
| Galerkin $Z=V$ | 같은 공간으로 상태와 잔차 검사 | Hermitian Ritz 문제 |
| 전체 잔차 $\rho$ | 원래 모든 방정식의 불일치 | 선택 공간 밖의 누락 확인 |

## 2. 비직교 basis와 overlap

### (1) $S$-내적과 정규화

AO가 비직교이면 계수의 Euclidean 길이는 물리적 상태의 길이와 다르다. 원래 계수 $c,d$의 내적과 축소 상태의 정규화는 다음과 같다. $\|c\|_S=(c^\dagger Sc)^{1/2}$로 정의한다.[1,2]

$$
\langle c,d\rangle_S=c^\dagger Sd,\qquad
\widetilde c^\dagger S\widetilde c=a^\dagger S_ra=1.
$$

$V^\dagger V=I_r$는 계수 열들의 Euclidean 정규직교성이다. $V^\dagger SV=I_r$는 새 orbital들의 물리적 정규직교성이다. 두 조건은 $S=I_M$일 때 일치하지만 일반적으로 다르다. 원래 AO의 overlap을 무시한 채 $H_r$만 표준 고유값 문제로 풀면 다른 방정식을 계산한다.[1,2]

알려진 상태 $c$를 선택 공간에서 가장 잘 표현하는 문제도 같은 내적으로 정의해야 한다. 축소 Gram 행렬을 $G=V^\dagger SV=S_r$라 하면, $S$-직교 투영 $P_S$와 최적 좌표는 다음과 같다.[1,3]

$$
a_{\mathrm{best}}=G^{-1}V^\dagger Sc,
\qquad P_S=VG^{-1}V^\dagger S,
\qquad c_{\mathrm{best}}=P_Sc.
$$

이는 $\|c-Va\|_S$를 최소화한 결과이다. $V^\dagger S(c-Va_{\mathrm{best}})=0$에서 위 식을 얻는다. 이미 알려진 $c$를 근사하는 이 문제와, 아직 모르는 고유상태를 축소 방정식으로 찾는 문제는 다르다. 특히 Ritz vector가 각 정확한 고유벡터의 $S$-직교 투영과 항상 같지는 않다.[1,2,3]

투영의 멱등성과 직교성은 다음과 같이 표현된다. 좌표 행렬 $P_S$ 자체는 일반적으로 Euclidean Hermitian이 아니지만, $S$ 내적에서는 자기수반이다.[1,3]

$$
P_S^2=P_S,\qquad P_S^\dagger S=SP_S,
\qquad V^\dagger S(I_M-P_S)c=0.
$$

$G=L_rL_r^\dagger$의 Cholesky 분해로 $Q=VL_r^{-\dagger}$를 만들면 같은 공간의 $S$-정규직교 기저를 얻는다. 여기서 $L_r^{-\dagger}=(L_r^\dagger)^{-1}$이다.[1,2,3]

$$
Q^\dagger SQ=L_r^{-1}GL_r^{-\dagger}=I_r,
\qquad \operatorname{range}(Q)=\operatorname{range}(V).
$$

이 변환은 공간 밖의 방향을 추가하지 않는다. 거의 종속인 열 때문에 $G$의 작은 고유값이 발생하면 직교화 전에 수치 rank와 허용오차를 확인해야 한다. 무조건 작은 수의 역수를 취하면 반올림 오차를 증폭시킬 수 있다. 공간 선택과 그 공간을 표현하는 기저의 조건수는 별개의 문제이다.[1,3]

### (2) 조립 행렬과 추가 $S$의 구별

전자구조의 $H_{\alpha\beta}=\langle\phi_\alpha|\hat H|\phi_\beta\rangle$와 $S_{\alpha\beta}=\langle\phi_\alpha|\phi_\beta\rangle$는 이미 bra와 ket을 짝지어 만든 행렬이다. 따라서 새 orbital 사이의 원소를 직접 전개하면 $H_r=V^\dagger HV$이다. 여기에 $S$를 추가로 넣을 이유가 없다. 이는 일반화 고유값의 투영식과 bilinear form의 기저변환을 AO 표기에 적용한 것이다.[1,2,3]

반면 계수 벡터를 계수 벡터로 보내는 연산자 표현은 $\mathcal L=S^{-1}H$이다. 그 **벡터 잔차** $\mathcal LVa-\theta Va=S^{-1}\rho$에 물리적 $S$-Galerkin 조건을 적용하면 다음과 같다.[1,2]

$$
V^\dagger S(\mathcal LVa-\theta Va)=0
\quad\Longleftrightarrow\quad
V^\dagger(HVa-\theta SVa)=0.
$$

따라서 $V^\dagger\rho=0$과 물리적 $S$-직교성은 모순되지 않는다. $\rho$는 AO bra로 평가한 방정식 성분이고, 원래 이산 AO 공간에서 표현한 residual의 계수는 $S^{-1}\rho$이다. 이미 조립된 $H,S$에 $V^\dagger S$를 다시 곱하는 방식은 일반적으로 다른 문제를 만든다. 이 구별은 뒤의 비직교 좌표 예제에서 직접 검산한다.[1,2,3]

| 계산 대상 | 일관된 식 | 필요한 구별 |
| --- | --- | --- |
| 알려진 상태의 투영 | $VG^{-1}V^\dagger Sc$ | 상태 내적의 $S$ 포함 |
| 조립 Hamiltonian 축소 | $V^\dagger HV$ | 추가 $S$ 없음 |
| 조립 overlap 축소 | $V^\dagger SV$ | 원래 공간과 축소 공간 크기 구별 |
| 벡터 연산자 Galerkin | $V^\dagger S\mathcal LV$ | $S\mathcal L=H$ |

## 3. Ritz value와 상태 정확도

### (1) Variational bound

Ritz value는 복원 상태의 Rayleigh quotient이다. $(\theta,a)$가 축소 고유쌍이고 $a\ne0$일 때, 분모를 유지하면 정규화 여부에 무관하게 다음 관계가 성립한다.[1,2]

$$
\theta=\frac{a^\dagger H_ra}{a^\dagger S_ra}
=\frac{(Va)^\dagger H(Va)}{(Va)^\dagger S(Va)}.
$$

원래 에너지를 $\epsilon_1\le\cdots\le\epsilon_M$, 축소 에너지를 $\theta_1\le\cdots\le\theta_r$로 정렬한다. 동일한 유한차원 Hermitian $H$, 양의 정부호 $S$와 열독립 $V$를 고정하고, 축소 문제를 정확히 푼다는 조건에서 Rayleigh–Ritz의 min–max 원리는 다음 상한을 준다.[1,5]

$$
\epsilon_i\le\theta_i,\qquad i=1,\ldots,r.
$$

가장 낮은 에너지는 모든 정규화 상태에서 Rayleigh quotient를 최소화한 값이고, 축소에서는 그 후보를 trial space로 제한한다. 후보가 줄어들었으므로 최소값이 더 내려갈 수 없다. 높은 순서의 에너지는 $i$차원 부분공간에 대한 min–max 논리로 같은 결론을 얻는다. $S=L_SL_S^\dagger$로 직교 좌표에 옮기면 일반화 문제에도 그 논리가 그대로 적용된다.[1,2,5]

같은 행렬쌍에 대해 $\mathcal V_r\subset\mathcal V_{r+1}$인 중첩 공간을 쓰면, 공통으로 존재하는 순번에 대해 다음 단조성이 성립한다.[1,5]

$$
\epsilon_i\le\theta_i^{(r+1)}\le\theta_i^{(r)},
\qquad i\le r.
$$

조건을 바꾸어 서로 다른 $H(\mu)$를 비교하거나, 같은 차원의 공간을 완전히 교체하면 이 단조성의 가정이 사라진다. 또한 이 상한은 동일한 이산 Hamiltonian의 정렬된 에너지에 대한 것이다. 특정 orbital 성격으로 추적한 band의 대응, 관측량 오차, 비Hermitian 열린계, 근사적으로 조립한 행렬의 오차에까지 그대로 확장할 수 없다.[1,2,5,6]

### (2) 전체 residual과 spectral gap

작은 문제의 고유값 계산이 수렴했는지는 $H_ra-\theta S_ra$로 알 수 있다. 원래 문제의 정확도를 검사하려면 $\rho=HVa-\theta SVa$를 다시 계산한다. 비직교 좌표에서는 $S$-정규화한 상태에 대해 다음 잔차 척도 $\eta$가 자연스럽다.[1,2]

$$
S=L_SL_S^\dagger,\qquad
\widehat H=L_S^{-1}HL_S^{-\dagger},\qquad
\widehat c=L_S^\dagger Va,
$$

$$
\widehat H\widehat c-\theta\widehat c=L_S^{-1}\rho,
\qquad \eta=\|L_S^{-1}\rho\|_2
=\sqrt{\rho^\dagger S^{-1}\rho}.
$$

$\widehat H$는 Hermitian이고 $\|\widehat c\|_2=1$이므로 $\eta$는 직교 좌표에서의 전체 잔차이다. 원래 Euclidean 잔차 $\|\rho\|_2$도 보고할 수 있지만 그 크기는 AO 좌표의 스케일에 영향을 받는다. 서로 다른 비직교 표현을 비교할 때에는 $S$와 정규화를 함께 밝혀야 한다.[1,2]

정규화와 Hermitian 조건 아래에서는 **어떤** 원래 고유값이 $\theta$로부터 $\eta$ 이내에 있다. 즉 잔차는 가까운 spectrum의 존재를 보장하지만, 그 고유값이 의도한 band인지는 따로 확인해야 한다.[1,2]

$$
\min_j|\epsilon_j-\theta|\le\eta.
$$

개별 고유벡터의 방향에는 spectral gap이 필요하다. 비교할 단순 고유값 $\epsilon_i$의 $S$-정규화 벡터를 $c_i$, 나머지 spectrum과 Ritz value 사이의 거리를 $\delta_i=\min_{j\ne i}|\epsilon_j-\theta|>0$로 두자. 두 상태 사이의 위상 불변 각 $\alpha_i$를 정의하면 다음과 같다.[1,2]

$$
\cos\alpha_i=|c_i^\dagger S\widetilde c|,
\qquad \sin\alpha_i\le\frac{\eta}{\delta_i}.
$$

이 식은 직교 좌표의 고유벡터 전개에서 원하지 않는 성분들이 최소 $\delta_i$만큼 떨어져 있다는 사실을 사용한다. $\delta_i$가 작으면 작은 잔차에서도 상태 방향이 크게 달라질 수 있다. 실제 원래 spectrum을 모르면 $\delta_i$도 바로 계산되지 않으므로, 축소 eigenvalue 간격을 근거 없이 대입하여 엄밀한 보증으로 해석하지 않는다.[1,2]

정확히 축퇴한 상태들은 같은 고유공간 안에서 자유롭게 회전할 수 있다. 이 경우 특정 열벡터의 성분 차이보다 관련 고유공간과 그 공간에 대한 관측량을 비교하는 편이 적절하다. 에너지, 전체 잔차, 상태 대응과 관측량을 함께 기록해야 하는 이유이다.[1,2]

## 4. Davidson·Lanczos와 공간 보강

### (1) 반복 eigensolver

Lanczos와 Davidson도 작은 부분공간에서 Rayleigh–Ritz 문제를 반복해서 푼다. 차이는 trial space를 어떻게 보강하느냐에 있다. $S=I_M$인 Hermitian 문제에서 시작 벡터 $v$로 만드는 $m$차 Krylov space는 다음과 같고, Lanczos는 그 공간의 정규직교 기저를 구성한다.[1,2]

$$
\mathcal K_m(H,v)=\operatorname{span}\{v,Hv,\ldots,H^{m-1}v\}.
$$

이 식은 공간의 정의이며, 실제 구현에서 큰 행렬 거듭제곱을 명시적으로 만들라는 뜻은 아니다. 행렬–벡터 곱과 직교화로 다음 방향을 생성한다. Davidson 계열은 현재 Ritz pair의 잔차에 preconditioner 또는 근사 correction equation을 적용하여 공간을 보강한다. 일반 비직교 문제에는 $S$와 정규화에 맞는 정식화가 필요하다.[1,2]

한 번의 대규모 고유값 문제에서 원하는 몇 상태를 수렴시키는 반복 eigensolver와, 여러 $\mu$에서 재사용하는 reduced-order model (ROM)은 목적이 다르다. 전자는 현재 원문제의 잔차를 줄이는 것이 목표이고, 후자는 정해진 조건 영역에서 같은 작은 공간의 표현력을 유지하는 것이 목표이다. 둘 다 Rayleigh–Ritz를 사용한다는 이유만으로 비용과 오차 검증이 같아지지는 않는다.[1,2,6]

### (2) 재사용할 공간과 검증

새 조건의 상태 $c_{\mathrm{new}}$를 얻으면 이미 표현되는 성분을 제거하여 보강 후보 $q$를 만들 수 있다. $P_S$는 2절의 투영이며, 고정된 원래 좌표와 overlap에서 다음 식을 사용한다.[1,3,6]

$$
q=(I_M-P_S)c_{\mathrm{new}},\qquad
V_{\mathrm{new}}=\left[V\ \frac{q}{\|q\|_S}\right]
\quad(\|q\|_S>0).
$$

$q=0$이면 같은 공간을 다시 표현할 뿐 자유도가 늘지 않는다. 수치적으로 작은 경우에는 rank 허용오차와 비교한다. 기존 열을 모두 유지하여 공간이 중첩되면 동일한 $H,S$에서 Ritz 에너지의 단조성은 적용되지만, 모든 상태 성분이나 응답 오차가 단조 감소한다고 결론 내리지는 않는다.[1,3,6]

재사용 기저는 학습에 쓰지 않은 조건에서도 확인한다. 예를 들어 $H(\mu)$의 관심 에너지와 잔차를 별도 $\mu$에서 검사하고, 실패한 조건의 상태를 다음 snapshot으로 포함할 수 있다. 큰 잔차를 발견하는 것과 그 방향을 가장 효율적으로 보정하는 것은 다른 일이며, preconditioner의 적합성과 목표 관측량도 고려해야 한다.[1,3,6]

| 계산 목적 | 공간 갱신의 계기 | 완료 판단 |
| --- | --- | --- |
| 현재 고유값 문제 | 현재 Ritz residual | 원하는 상태의 전체 잔차와 대응 |
| 여러 조건의 ROM | 표본 밖 조건의 오차 | 지정 영역의 별도 검증 |
| 응답 함수 근사 | 관심 에너지·입력에서의 오차 | 해당 응답과 출력의 일치 |

기저 구축, $HV$ 계산, 직교화와 전체 잔차 평가에는 여전히 원래 차원의 연산이 들어간다. 작은 고유값 문제의 크기만 보고 전체 가속률을 추정할 수 없다. 반복 질의에서 구축 비용을 얼마나 재사용하는지까지 포함하는 비용 논의는 fundamentals의 offline·online 구분을 따른다.[1,3,6]

## 5. 선형계와 Green's function

### (1) Resolvent projection

고유상태 대신 주어진 source에 대한 응답을 구할 수도 있다. 복소 에너지 $z$와 조립된 우변 $b\in\mathbb C^M$에 대해 $(zS-H)x=b$를 고려한다. 역행렬이 존재하는 $z$에서 **resolvent의 역행렬 표현**을 $\mathcal G(z)=(zS-H)^{-1}$로 정의하면 $x=\mathcal G(z)b$이다. 일반 선형계 투영과 전달함수의 역행렬 표현을 전자구조 행렬쌍에 적용한 것이다.[4,6]

Galerkin으로 $x\simeq Va(z)$를 대입하면 다음을 얻는다. 아래 역행렬 표현에는 $zS_r-H_r$도 가역이라는 조건이 별도로 필요하다. 따라서 원래 spectrum와 Ritz spectrum을 모두 피하는 $z$를 사용한다. 원래 $zS-H$가 가역이어도 축소 행렬의 가역성은 자동으로 보장되지 않는다. 입력의 투영 $V^\dagger b$까지 포함해야 같은 source에 대한 응답을 비교할 수 있다.[4,6]

$$
(zS_r-H_r)a(z)=V^\dagger b,\qquad
\widetilde x(z)=V(zS_r-H_r)^{-1}V^\dagger b.
$$

따라서 축소 좌표의 작은 Green's function은 $(zS_r-H_r)^{-1}$이고, 우변에서 원래 계수로 가는 근사 행렬은 다음과 같다. 작은 역행렬을 원래 $M\times M$ 행렬과 바로 비교하지 말고 양쪽의 복원·입력 사상을 붙인다.[4,6]

$$
\widetilde{\mathcal G}(z)=V(zS_r-H_r)^{-1}V^\dagger.
$$

여기서 $\mathcal G$는 조립된 우변을 계수로 보내는 규약이다. $\mathcal L=S^{-1}H$의 계수 연산자 resolvent는 $(zI_M-\mathcal L)^{-1}=\mathcal G(z)S$이며, 이산 AO 공간 안에서 두 AO 사이의 bra·ket으로 평가한 resolvent 행렬은 $S\mathcal G(z)S$이다. 마지막 관계는 AO source의 조립 우변이 $S$의 해당 열이고 bra 평가에도 $S$가 들어간다는 사실로 유도된다. 따라서 비직교 기저에서는 모두를 같은 행렬 원소라고 부르지 않는다.[1,2,4,6]

출력 행렬 $C$로 $y=Cx$를 읽는다면 근사 응답은 $\widetilde y=C\widetilde{\mathcal G}(z)b$이다. 상태의 일부 에너지가 잘 맞아도 source와 출력이 선택 공간 밖의 성분에 민감하면 응답은 부정확할 수 있다. 특히 pole 근처에서는 역연산의 민감도가 커지므로 관심 $z$, 입력과 출력에서 직접 검증한다.[4,6]

### (2) 제거법과의 차이

고정 trial space의 투영은 상태를 $Va$로 제한한다. 반면 [elimination-based downfolding](downfolding.md)은 제거할 변수의 원방정식을 풀어 남길 변수의 방정식에 대입한다. 제거 블록이 가역이면 Schur complement와 역대입으로 원래 선형계의 해를 복원할 수 있다. 따라서 좌표를 0으로 놓고 행·열을 남기는 것과 제거 좌표의 영향을 대입하는 것은 일반적으로 다르다.[4,7]

예를 들어 좌표 선택으로 얻은 $H_r$에는 남긴 좌표들 사이의 원래 행렬 원소만 들어 있다. 제거 공간을 거쳐 되돌아오는 응답은 고정된 이 행렬에 자동으로 더해지지 않는다. 또한 일반적으로 “역행렬을 만든 뒤 일부를 취하기”와 “일부를 취한 뒤 역행렬 만들기”는 같지 않다. 이 차이는 Schur complement의 block inverse 식에서 확인된다.[4,7]

여기서는 projection의 역할을 분명히 하는 데 필요한 구별만 사용한다. 에너지 의존 유효 Hamiltonian의 구성과 제거 블록 pole의 처리는 별도의 문제이다. Green's function을 투영했다는 사실만으로 정확한 제거 효과까지 포함했다고 해석하지 않는다.[4,7]

## 6. Petrov–Galerkin과 일반 동역학

### (1) Trial·test 공간과 가역성

전자구조에서 사용한 잔차 조건은 일반 선형계에도 적용된다. 이 절에서는 원래 차원을 $n$, 상태를 $x\in\mathbb C^n$, 가역 행렬을 $K\in\mathbb C^{n\times n}$, 우변을 $b$로 쓴다. $V,Z\in\mathbb C^{n\times r}$는 열독립이며, 정적 잔차는 $\rho_b=b-KVa$로 정의한다. Trial과 test space가 다르면 **Petrov–Galerkin**이다.[4,6]

$$
Z^\dagger\rho_b=0
\quad\Longleftrightarrow\quad
K_ra=b_r,\qquad K_r=Z^\dagger KV,\qquad b_r=Z^\dagger b.
$$

$K_r$가 가역이면 축소 좌표가 유일하다. 원래 $K$가 가역이어도 이 조건은 자동이 아니다. $K\operatorname{range}(V)$ 안에 test space에 직교하는 비영 방향이 있으면 그 방향의 계수가 결정되지 않는다. 이는 $K_ra=0$의 영공간 조건을 풀어 쓴 것이다.[4,6]

$$
K_r\text{가 가역}
\quad\Longleftrightarrow\quad
K\operatorname{range}(V)\cap\operatorname{range}(Z)^\perp=\{0\}.
$$

직접 만든 반례로 $K=\begin{pmatrix}0&1\\1&0\end{pmatrix}$, $V=Z=e_1$을 택하면 $\det K=-1$이지만 $K_r=0$이다. 공간 배치가 거의 이 경우에 가까우면 정확히 가역이어도 수치적으로 민감할 수 있다. 기저들을 정규직교화한 상태에서 작은 축소 singular value와 조건수를 확인하되, 임의 기저 스케일 차이를 공간 자체의 결함으로 오인하지 않는다.[3,4]

같은 공간의 기저를 가역 행렬 $T_v,T_z$로 바꾸어도 물리적 상태와 잔차 조건은 변하지 않는다. 다음 관계는 공간의 선택과 좌표 표현을 구별한다.[4,6]

$$
V'=VT_v,\qquad Z'=ZT_z,\qquad
Va=V'a',\quad a'=T_v^{-1}a,\qquad
Z'^\dagger\rho_b=T_z^\dagger Z^\dagger\rho_b.
$$

### (2) 최소제곱·에너지 최적성

$K=K^\dagger>0$이고 $Z=V$이면 $K_r>0$이며 축소 해가 존재하고 유일하다. 상태 오차 $e=x-Va$에 대해 $Ke=\rho_b$, $V^\dagger Ke=0$이다. 에너지 노름 $\|w\|_K=(w^\dagger Kw)^{1/2}$에서 이 직교성은 다음 최적성을 준다.[3,4]

$$
\|x-Vd\|_K^2
=\|x-Va\|_K^2+\|V(a-d)\|_K^2,
\qquad
\|x-Va\|_K=\min_d\|x-Vd\|_K.
$$

여기서 $d\in\mathbb C^r$는 임의의 비교 좌표이다. 두 번째 항이 음수가 될 수 없으므로 Galerkin 해가 선택 공간 안에서 최선의 에너지 오차를 준다. 이 결과는 Euclidean 상태 오차, 전체 잔차, 특정 출력 오차를 동시에 최소화한다는 뜻은 아니다. 부정부호 $K$에서는 위 제곱근이 노름이 아니므로 같은 증명을 사용할 수 없다.[3,4]

전체 잔차의 Euclidean 최소제곱은 $Z=KV$로 얻는다. $KV$가 열독립인 현재 조건에서 일차 최적 조건과 다음 제곱합 분해가 동치이다.[4,7]

$$
(KV)^\dagger(b-KVa)=0,
\qquad
\|b-KV(a+d)\|_2^2=\|\rho_b\|_2^2+\|KVd\|_2^2.
$$

따라서 이 선택의 Petrov–Galerkin은 잔차를 최소화한다. 임의의 $Z$에는 이 성질이 없다. 계산에서는 위 식이 normal equation의 구조임을 이해하되, 조건수가 나쁜 큰 문제의 구현은 QR 등 안정적인 최소제곱 알고리즘을 고려한다.[4,7]

잔차와 상태·출력 오차의 차이는 역연산으로 표현된다. $y=Cx$, $\widetilde y=CVa$이고 $\|\cdot\|_2$가 Euclidean 및 유도 행렬 노름이면 다음은 정확한 관계와 그 상계이다.[3,4]

$$
e=K^{-1}\rho_b,\qquad
\|e\|_2\le\|K^{-1}\|_2\|\rho_b\|_2,
\qquad
\|y-\widetilde y\|_2\le\|CK^{-1}\|_2\|\rho_b\|_2.
$$

동일한 잔차 크기라도 역연산의 민감도와 출력 방향이 다르면 실제 오차가 달라진다. 계산하거나 제한하지 않은 역연산 노름을 생략하고 잔차 자체를 엄밀한 상태 오차 보증이라고 부르지 않는다. 이 논리는 앞 절 resolvent의 pole 부근 검증에도 적용된다.[3,4,6]

### (3) 입출력과 안정성

시간 $t$의 선형 모형을 $E\dot x=Ax+Bu$, $y=Cx$로 두자. $E,A\in\mathbb C^{n\times n}$은 시간에 무관하고, $u\in\mathbb C^m$, $y\in\mathbb C^p$, $B\in\mathbb C^{n\times m}$, $C\in\mathbb C^{p\times n}$이다. 여기서는 $E$가 가역이고 직접 전달항이 없는 경우만 다룬다. 고정된 $V,Z$로 잔차 $\rho_t=AVa+Bu-EV\dot a$를 검사하면 다음 ROM을 얻는다.[6,8]

$$
E_r\dot a=A_ra+B_ru,\qquad \widetilde y=C_ra,
$$

$$
E_r=Z^\dagger EV,\quad A_r=Z^\dagger AV,\quad
B_r=Z^\dagger B,\quad C_r=CV.
$$

출력은 복원 상태를 원래 $C$로 읽으므로 $Z^\dagger$가 붙지 않는다. 입력과 출력의 개수도 그대로이며 내부 상태 차원만 줄어든다. $E_r$가 가역인지 별도로 확인해야 축소 문제를 보통 미분방정식으로 풀 수 있다. 원래 overlap $S$와 여기의 질량·저장 행렬 $E$는 물리적 정의를 확인했을 때에만 동일시한다.[6,8]

초기조건 $x_0$에는 선택한 상태 내적에 대한 투영 좌표를 사용하거나, 초기 표현 오차를 명시한다. 예를 들어 Euclidean 내적을 쓰면 $a(0)=(V^\dagger V)^{-1}V^\dagger x_0$이다. 오차 $e(t)=x(t)-Va(t)$는 다음 식을 만족하므로 초기 오차와 시간 중 발생하는 잔차가 모두 중요하다.[3,6,8]

$$
E\dot e=Ae+\rho_t,\qquad e(0)=x_0-Va(0).
$$

원래 $E^{-1}A$의 모든 고유값 실수부가 음수인 점근 안정성은 임의 투영으로 보존되지 않는다. 무차원 반례 $E=I_2$, $A=\begin{pmatrix}-1&4\\0&-2\end{pmatrix}$의 고유값은 $-1,-2$이다. 그러나 $V=Z=(1,1)^\mathsf T/\sqrt2$로 축소하면 $E_r=1$, $A_r=0.5$이므로 영입력 해가 증가한다. 이는 아래 코드에서 직접 대입하여 검산하는 반례이다.[6,8,9]

명확한 충분조건도 있다. $E=E^\dagger>0$, $A+A^\dagger<0$, $Z=V$라면 $E_r>0$이고 $A_r+A_r^\dagger<0$이다. 영입력에서 축소 에너지의 시간 변화는 다음과 같다.[8,9]

$$
\frac{d}{dt}(a^\dagger E_ra)
=a^\dagger(A_r+A_r^\dagger)a<0\qquad(a\ne0).
$$

이 조건은 축소계의 점근 안정성을 보장한다. 단순히 “원래 eigenvalue가 왼쪽 반평면에 있다”는 조건보다 강하며, nonnormal 행렬에서는 두 조건을 구별해야 한다. 보존되는 에너지 내적 또는 Lyapunov 구조를 이용하는 방법이 있지만, 실제로 적용한 구조와 가정을 확인해야 보장을 사용할 수 있다.[8,9]

## 7. 세 orbital 모형의 수치 검증

### (1) Eigenpair와 residual

다음은 물질 데이터가 아닌 교육용 tight-binding 모형이다. 원래 basis는 직교하여 $S=I_3$이고, $\mu$는 두 번째 onsite energy의 변화량이다. 수치 행렬은 에너지를 eV로 나타낸 값이다. 앞선 두 문서와 같은 $H_0$를 사용한다.

$$
H(\mu)=H_0+\operatorname{diag}(0,\mu,0),\qquad
H_0=\begin{pmatrix}0&-1&0.3\\-1&0.5&0.4\\0.3&0.4&4\end{pmatrix}\ \mathrm{eV}.
$$

$\mu=0$에서 $V_c=[e_1,e_2]$를 쓰면 세 번째 orbital은 복원 상태에 들어갈 수 없다. 이때 $H_r$는 왼쪽 위 $2\times2$ block이고 $S_r=I_2$이다. 그러나 원래 $H_0$를 복원 상태에 작용시키면 세 번째 성분에 $0.3a_1+0.4a_2$가 남는다. 선택 공간 안의 방정식은 만족하지만 밖의 coupling은 사라지지 않는다는 1절의 설명을 직접 확인할 수 있다.[1,2]

비교용 $V_\star$는 $H_0$의 정확한 낮은 두 고유벡터를 열로 둔다. 이 공간은 현재 조건의 해당 invariant subspace이므로 두 에너지와 상태가 수치 정밀도까지 복원된다. 전체 대각화를 이미 수행한 기준이며 저렴한 기저 생성법이나 가속률의 증거는 아니다.[1,2]

| $\mu=0$의 공간 | 낮은 에너지 (eV) | 각 상태의 전체 잔차 (eV) |
| --- | --- | --- |
| 원래 3차원 | $-0.82909176,\ 1.27476220$ | 수치 반올림 수준 |
| $V_c=[e_1,e_2]$ | $-0.78077641,\ 1.28077641$ | $0.48262652,\ 0.13065851$ |
| $V_\star$ | $-0.82909176,\ 1.27476220$ | $10^{-12}$ 미만 |

두 좌표 Ritz 에너지는 모두 원래 같은 순번의 에너지보다 높다. 반면 $V_c^\dagger\rho$는 수치적으로 0이어도 전체 잔차는 명확히 남는다. 아래 코드는 원래 세 고유값도 출력하고, $\mu=0.8$에서 같은 $V_\star$를 재사용하여 조건 변화 후의 잔차를 다시 검사한다. 한 점에서의 정확성을 새 조건의 정확성으로 대체하지 않는 예이다.

### (2) 비직교 좌표의 동치성

가역 행렬 $T$로 원래 계수를 $c=T c'$라고 표현하자. 이 예제의 $T$는 실수 상삼각 행렬이며, 세 번째 새 orbital에 첫 두 orbital 성분을 섞는다. 같은 물리적 문제의 새 행렬과 같은 trial space의 좌표는 다음과 같다.[1,2,7]

$$
H'=T^\dagger H_0T,\qquad S'=T^\dagger T,\qquad
V'=T^{-1}V_c.
$$

이때 $V'^\dagger H'V'=V_c^\dagger H_0V_c$와 $V'^\dagger S'V'=I_2$가 성립한다. 잔차는 $\rho'=T^\dagger\rho$로 바뀌므로 Euclidean 크기가 달라질 수 있지만 다음 가중 크기는 같다.[1,2]

$$
\rho'^\dagger S'^{-1}\rho'=\rho^\dagger\rho.
$$

아래 Python 3 코드는 NumPy만 사용한다. `eigh_pair`는 Cholesky 변환으로 Hermitian 일반화 문제를 표준형으로 바꾼 뒤 고유벡터를 역변환한다. 명시적 역행렬 대신 `solve`를 사용한다. $10^{-12}$는 이 작은 예제에서 사용하는 수치 검산 허용량이며 대규모 계산의 보편적 수렴 기준은 아니다.[1,2]

```python
import numpy as np


def eigh_pair(H, S):
    L = np.linalg.cholesky(S)
    left = np.linalg.solve(L, H)
    Hhat = np.linalg.solve(L, left.conj().T).conj().T
    energy, U = np.linalg.eigh(Hhat)
    return energy, np.linalg.solve(L.conj().T, U)


def ritz(H, S, V):
    Hr, Sr = V.conj().T @ H @ V, V.conj().T @ S @ V
    energy, a = eigh_pair(Hr, Sr)
    c = V @ a
    rho = H @ c - (S @ c) * energy
    eta = np.linalg.norm(np.linalg.solve(np.linalg.cholesky(S), rho), axis=0)
    assert np.linalg.norm(c.conj().T @ S @ c - np.eye(V.shape[1])) < 1e-12
    assert np.linalg.norm(V.conj().T @ rho) < 1e-12
    return energy, c, rho, eta


np.set_printoptions(precision=8, suppress=True)
H0 = np.array([[0., -1., .3], [-1., .5, .4], [.3, .4, 4.]])
S = np.eye(3)
full, U = eigh_pair(H0, S)
Vc, Vstar = np.eye(3)[:, :2], U[:, :2]
e, c, rho, eta = ritz(H0, S, Vc)
es, cs, rs, etas = ritz(H0, S, Vstar)
print("full energies", full)
print("coordinate energies", e)
print("coordinate residuals", eta)
print("exact-space energies", es)
assert np.all(e >= full[:2] - 1e-12)
assert np.max(etas) < 1e-12

Htest = H0 + np.diag([0., .8, 0.])
et, ct, rt, etat = ritz(Htest, S, Vstar)
print("held-out energy errors", et - np.linalg.eigvalsh(Htest)[:2])
print("held-out residuals", etat)

T = np.array([[1., .2, .1], [0., 1.2, .3], [0., 0., .8]])
Hp, Sp = T.conj().T @ H0 @ T, T.conj().T @ T
Vp = np.linalg.solve(T, Vc)
ep, cp, rp, etap = ritz(Hp, Sp, Vp)
fullp, Up = eigh_pair(Hp, Sp)
assert np.allclose(fullp, full, atol=1e-12, rtol=0)
assert np.allclose(ep, e, atol=1e-12, rtol=0)
assert np.allclose(etap, eta, atol=1e-12, rtol=0)
# Projectors avoid the arbitrary eigenvector phase.
assert np.linalg.norm((T @ cp) @ (T @ cp).conj().T - c @ c.conj().T) < 1e-12
print("nonorthogonal energies", ep)
print("nonorthogonal Euclidean residuals", np.linalg.norm(rp, axis=0))
print("nonorthogonal weighted residuals", etap)
# Extra Sp changes the projected Hamiltonian even for this same physical space.
wrong = Vp.conj().T @ Sp @ Hp @ Vp
right = Vp.conj().T @ Hp @ Vp
assert np.linalg.norm(wrong - right) > 1e-3
A = np.array([[-1., 4.], [0., -2.]])
v = np.ones(2) / np.sqrt(2)
assert np.isclose(v @ A @ v, .5)
print("unstable reduced rate", f"{v @ A @ v:.8f}")
```

실행 결과는 다음과 같다. 고유벡터의 부호·위상은 구현에 따라 달라도 표의 에너지와 잔차, 코드의 projector 비교에는 영향을 주지 않는다.

```text
full energies [-0.82909176  1.2747622   4.05432956]
coordinate energies [-0.78077641  1.28077641]
coordinate residuals [0.48262652 0.13065851]
exact-space energies [-0.82909176  1.2747622 ]
held-out energy errors [0.00030789 0.00207768]
held-out residuals [0.03782945 0.06820681]
nonorthogonal energies [-0.78077641  1.28077641]
nonorthogonal Euclidean residuals [0.38610121 0.10452681]
nonorthogonal weighted residuals [0.48262652 0.13065851]
unstable reduced rate 0.50000000
```

비직교 좌표에서 바뀐 Euclidean 잔차를 물리적 정확도 변화로 해석해서는 안 된다. 가중 잔차와 복원 상태의 공간은 같으며, 추가 $S'$를 넣은 잘못된 축소 행렬은 같지 않다. 이 예제는 좌표 일관성의 검산이고, $S'$의 조건수가 극단적으로 큰 경우의 수치 안정성까지 시험한 것은 아니다.

## 8. 요약

- 상태를 $c\simeq Va$로 제한하고 전체 잔차에 Galerkin 조건을 적용하면 $H_r=V^\dagger HV$, $S_r=V^\dagger SV$인 Rayleigh–Ritz 문제가 나온다.
- 비직교 AO에서는 상태 내적과 정규화에 $S$가 필요하다. 조립된 Hamiltonian 축소에 추가 $S$를 넣는 것은 이 원칙과 다르다.
- Hermitian definite 문제의 Ritz 상한은 같은 행렬쌍과 순번, 중첩 공간 등의 가정 안에서 사용한다. 전체 잔차와 상태의 spectral gap은 에너지와 상태 오차를 구별한다.
- 반복 eigensolver의 공간 보강과 여러 조건에서 재사용하는 ROM은 검증 목적이 다르다. Resolvent에는 입력과 출력, 관심 복소 에너지의 정확성도 필요하다.
- 일반 Petrov–Galerkin의 가역성·최적성·동적 안정성은 자동으로 보장되지 않는다. 성립하는 내적과 연산자 조건을 함께 확인한다.

## 9. 참고문헌

1. Y. Saad, *Numerical Methods for Large Eigenvalue Problems*, revised edition (SIAM, 2011). [DOI: 10.1137/1.9781611970739](https://doi.org/10.1137/1.9781611970739). [Author-hosted full text](https://www-users.cse.umn.edu/~saad/eig_book_2ndEd.pdf). §§3.1–3.2, 4.3, 6.1–6.3, 8.3, 9.2.2, 9.2.5–9.2.6.
2. Z. Bai, J. Demmel, J. Dongarra, A. Ruhe, and H. van der Vorst, eds., *Templates for the Solution of Algebraic Eigenvalue Problems: A Practical Guide* (SIAM, 2000). [DOI: 10.1137/1.9780898719581](https://doi.org/10.1137/1.9780898719581). [§4.7.1, Basic Theory](https://www.netlib.org/utk/people/JackDongarra/etemplates/node137.html); [§5.2, Transformation to Standard Problem](https://www.netlib.org/utk/people/JackDongarra/etemplates/node163.html); [§5.6, Jacobi-Davidson Methods](https://www.netlib.org/utk/people/JackDongarra/etemplates/node176.html); [§5.7.1, Positive Definite B](https://www.netlib.org/utk/people/JackDongarra/etemplates/node178.html), [Residual Vector](https://www.netlib.org/utk/people/JackDongarra/etemplates/node179.html), [Error Bounds for Computed Eigenvalues](https://www.netlib.org/utk/people/JackDongarra/etemplates/node181.html), [Error Bounds for Computed Eigenvectors](https://www.netlib.org/utk/people/JackDongarra/etemplates/node182.html), [Remarks on Clustered Eigenvalues](https://www.netlib.org/utk/people/JackDongarra/etemplates/node183.html).
3. B. Haasdonk, “Reduced Basis Methods for Parametrized PDEs—A Tutorial Introduction for Stationary and Instationary Problems,” in *Model Reduction and Approximation: Theory and Algorithms*, pp. 65–136 (SIAM, 2017). [DOI: 10.1137/1.9781611974829.ch2](https://doi.org/10.1137/1.9781611974829.ch2). [Author preprint](https://pnp.mathematik.uni-stuttgart.de/ians/haasdonk/data/oberwolfach2014/RBtutorial.pdf). §§2.3, 2.6, 3.3, Proposition 2.46, Exercise A.8.
4. Y. Saad, *Iterative Methods for Sparse Linear Systems*, second edition (SIAM, 2003). [DOI: 10.1137/1.9780898718003](https://doi.org/10.1137/1.9780898718003). [Author-hosted full text](https://www-users.cse.umn.edu/~saad/IterMethBook_2ndEd.pdf). §§1.12–1.13, 5.1–5.2, 14.2.
5. J. Demmel, “Notes for Ma221 Lecture 19: Symmetric eigenvalue problems and the SVD,” University of California, Berkeley (October 28, 2010). [Author course notes](https://people.eecs.berkeley.edu/~demmel/ma221_Fall10/Lectures/Lecture_19.html). Rayleigh quotient와 Courant–Fischer minimax theorem의 정리·증명.
6. P. Benner, S. Gugercin, and K. Willcox, “A Survey of Projection-Based Model Reduction Methods for Parametric Dynamical Systems,” *SIAM Review* **57**(4), 483–531 (2015). [DOI: 10.1137/130932715](https://doi.org/10.1137/130932715). [Author-hosted full text](https://kiwi.oden.utexas.edu/papers/Parametric-model-reduction-survey-Benner-Gugercin-Willcox.pdf). §§2.1–2.4, 3.3, 5.4.
7. L. N. Trefethen and D. Bau III, *Numerical Linear Algebra* (SIAM, 1997). [DOI: 10.1137/1.9780898719574](https://doi.org/10.1137/1.9780898719574). [University-hosted full text](https://www.stat.uchicago.edu/~lekheng/courses/309/books/Trefethen-Bau.pdf). Lecture 11, pp. 80–83; Lecture 20, pp. 152–154; Lecture 36, pp. 276–278, 283.
8. R. Pulch, “Stability preservation in Galerkin-type projection-based model order reduction,” *Numerical Algebra, Control and Optimization* **9**(1), 23–44 (2019). [DOI: 10.3934/naco.2019003](https://doi.org/10.3934/naco.2019003). [Author preprint](https://arxiv.org/abs/1711.02912). §§2.1–2.3, Theorem 1.
9. I. Kalashnikova, M. F. Barone, S. Arunajatesan, and B. G. van Bloemen Waanders, “Construction of energy-stable projection-based reduced order models,” *Applied Mathematics and Computation* **249**, 569–596 (2014). [DOI: 10.1016/j.amc.2014.10.073](https://doi.org/10.1016/j.amc.2014.10.073). [Author-hosted full text](https://www.sandia.gov/app/uploads/sites/127/2021/10/amc2014.pdf). §§2–3, 5.1.
