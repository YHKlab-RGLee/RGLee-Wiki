---
description: 주기적 원자 Hamiltonian에서 Bloch 상태를 골라 작은 cell 기저를 만들고, 이를 NEGF 수송에 적용해 검증하는 절차를 설명한다.
---

# NEGF: Mode-space reduction

**Mode-space reduction**은 지정한 에너지 범위의 수송을 설명하는 데 필요한 cell 내부 상태만 남겨 Hamiltonian의 block 크기를 줄이는 방법이다. 이 글의 출발점은 이미 정해진 주기적 원자 Hamiltonian이다. 먼저 그 Hamiltonian의 band를 풀고, 여러 파수의 Bloch 상태를 하나의 작은 cell 기저로 모은다. 그 기저에 Hamiltonian을 투영한 뒤 band를 다시 확인하고, 마지막으로 열린 소자의 [nonequilibrium Green's function (NEGF)](negf-formalism.md) 계산에 적용한다. 작은 기저를 쓴 결과는 원래 원자 기저의 계산과 비교해야 한다.[1–3]

여기서는 수송축으로 같은 cell이 반복되는 직교 원자 궤도 모형과 이웃 cell까지만 결합하는 ballistic 문제를 기본 사례로 삼는다. Cell당 원자 궤도 수를 $M$, 남길 기저 벡터 수를 $m<M$, 반복 간격을 $a$라 한다. 복잡한 접합, 산란, 비직교 궤도는 기본 절차를 이해한 뒤 7절에서 다룬다. 에너지의 기준과 Hamiltonian의 전위 부호는 입력 모형에서 정한 것을 그대로 유지한다.[1–3]

## 1. 주기적 기준 Hamiltonian

### (1) Cell block과 Bloch 문제

$H_0\in\mathbb C^{M\times M}$은 한 cell의 Hamiltonian, $W\in\mathbb C^{M\times M}$는 cell $j$에서 $j+1$로 가는 결합으로 정의한다. 그러면 주기적 기준계의 block은

$$
H_{jj}=H_0,\qquad H_{j,j+1}=W,\qquad H_{j+1,j}=W^\dagger
$$

이다. 이 정의에서 $H_0$은 Hermitian이고, 반대 방향 결합은 $W^\dagger$이다. Bloch 형태 $c_j=e^{ikja}\psi_{nk}$를 대입하면 cell 내부 벡터 $\psi_{nk}\in\mathbb C^M$가 푸는 행렬은

$$
H(k)=H_0+We^{ika}+W^\dagger e^{-ika}
$$

이고 고유값 문제는

$$
H(k)\psi_{nk}=\varepsilon_n(k)\psi_{nk},\qquad
\psi_{nk}^\dagger\psi_{nk}=1
$$

이다. $k$는 길이의 역수, $ka$는 무차원 위상, $\varepsilon_n(k)$는 에너지이다. 여기서 **band**는 $k$에 따른 $\varepsilon_n(k)$의 곡선이며, **Bloch eigenvector** $\psi_{nk}$는 그 상태의 한 cell 안 궤도 진폭이다. $k$마다 풀어 얻는 벡터는 서로 같을 필요가 없다. 따라서 한 $k$의 몇 벡터만으로 전체 관심 band를 표현할 수 있다고 가정하지 않는다.[1–4]

Cell을 길게 잡아 이웃 cell 밖의 결합을 cell 내부 또는 바로 다음 cell 결합으로 포함할 수 있다. 그러한 재분할을 하지 않은 장거리 결합 모형에는 $H(k)$에 더 먼 cell의 Fourier 항도 넣어야 한다. 이하의 식은 위 이웃 cell 규약을 따른다.[1,3]

### (2) 관심 에너지 범위

관찰하거나 계산할 에너지 구간을 $\mathcal W=[E_-,E_+]$로 먼저 정한다. 예를 들어 전도대 가장자리의 수송을 본다면 해당 가장자리와 계산할 주입·터널링 에너지가 구간 안에 있어야 한다. 구간 밖 band까지 모두 재현하려고 하면 작은 기저라는 목적이 약해진다. 반대로 구간이 너무 좁으면 소자의 바이어스나 전위 변화가 접근시키는 상태가 빠진다. 이 범위 선택은 적용할 소자와 관측량의 조건부 입력이지, 재료만으로 정해지는 상수가 아니다.[1–3]

$$
\mathcal B_{\mathcal W}(k)=\{n:\varepsilon_n(k)\in\mathcal W\}
$$

이 집합은 파수 $k$에서 관심 에너지에 든 band 번호를 뜻한다. 표본 $k_1,\ldots,k_{N_k}$는 Brillouin zone에 걸쳐 놓고, 각 점에서 $n\in\mathcal B_{\mathcal W}(k_l)$인 벡터를 수집한다. Band 끝점이나 valley 주변처럼 곡선의 성격이 달라지는 곳은 표본을 더 촘촘하게 둔다. 표본이 일부 파수만 대표하므로, 나중에 더 조밀한 $k$ 격자에서 원래 band와 비교한다.[1–3]

## 2. Bloch 표본과 공통 cell 기저

### (1) 표본 행렬과 독립 방향

선택한 Bloch eigenvector를 열로 이은 행렬을 $\Phi_0$라 한다. 선택한 열의 총수가 $p$이면

$$
\Phi_0=[\psi_{n_1k_1},\psi_{n_2k_1},\ldots,\psi_{n_pk_{N_k}}]
\in\mathbb C^{M\times p}
$$

이다. 서로 다른 $k$의 벡터는 각각 정규화되어도 열 전체가 서로 직교하지 않는다. 같은 물리적 방향을 여러 번 수집했을 수도 있다. 따라서 $p$가 곧 retained dimension은 아니다. 직교 원자 궤도에서는 singular value decomposition (SVD)

$$
\Phi_0=L\,\operatorname{diag}(\sigma_1,\sigma_2,\ldots)R^\dagger
$$

으로 선형 독립 방향을 정리하고, 충분히 작은 $\sigma_\alpha$에 해당하는 방향을 제외한다. 남은 $m$개 왼쪽 singular vector를 모아

$$
U=L_{[:,1:m]}\in\mathbb C^{M\times m},\qquad U^\dagger U=I_m
$$

로 둔다. $U$의 열은 원래 cell 궤도 공간에 놓인 직교 단위벡터이다. SVD 경계값은 수치적 중복을 정리하는 선택이며 물리적 정답을 자동으로 정하지 않는다. 낮은 singular value 방향을 버렸을 때 target band나 수송이 달라지면 표본 또는 $m$을 다시 정한다.[1–3]

중요한 점은 **각 $k$에서 서로 다른 $U(k)$를 쓰는 과정이 아니라는 것**이다. $k$별 고유벡터는 기저를 만들기 위한 표본이고, 완성한 $U$는 해당 주기적 기준 cell에 공통으로 쓰는 하나의 $k$ 독립 행렬이다. 따라서 원래 band와 줄인 band를 같은 $k$의 Hamiltonian에 대해 직접 비교할 수 있으며, 같은 종류의 cell이 반복되는 장치에도 같은 $U$를 적용할 수 있다. 기저 선택을 바꾸거나 물질·단면이 달라지면 이 전제가 다시 검토되어야 한다.[1–3]

장치의 $j$번째 cell 파동함수 계수를 $c_j\in\mathbb C^M$, 줄인 계수를 $\xi_j\in\mathbb C^m$라고 하면 실제 축소 가정은

$$
c_j\approx U\xi_j,\qquad \xi_j=U^\dagger c_j
$$

이다. 첫 관계는 $m$개 열벡터의 선형결합으로 cell 상태를 표현한다는 뜻이다. 두 번째 관계는 주어진 원래 상태의 retained 성분을 추출한다. 두 식을 합치면 $UU^\dagger c_j$만 남으므로, 버린 공간의 진폭은 이 표현에서 복원되지 않는다. 이 때문에 $U$의 직교성만 확인해서 정확도를 판정할 수 없고, 대상 band와 장치 관측량을 따로 검사한다.[1–3]

### (2) 차원 예

다음은 실제 재료의 계산값이 아니라 행렬 크기를 보여 주는 예이다. Cell에 네 궤도가 있고, 세 $k$점에서 관심 band 두 개씩 골랐다고 하자. 그러면 $\Phi_0$는 $4\times6$이다. 여섯 열이 두 개의 독립 방향에 충분히 가깝고 그 두 방향을 남기기로 검증했다면 $U$는 $4\times2$이다. 이 조건은 항상 성립하는 물리 법칙이 아니며, 실제 $m$은 표본과 정확도 검사를 거쳐 결정한다.

| 단계 | 이 예의 크기 | 역할 |
| --- | --- | --- |
| 원래 cell $H_0,W$ | 각각 $4\times4$ | 네 원자 궤도의 에너지와 cell 결합 |
| 수집 행렬 $\Phi_0$ | $4\times6$ | 세 $k$점의 두 Bloch 상태씩 저장 |
| 공통 기저 $U$ | $4\times2$ | 중복 방향을 정리한 두 cell 방향 |
| 줄인 cell block | 각각 $2\times2$ | 같은 두 방향에서 전파를 계산 |

열 개 cell로 만든 장치라면 원래 궤도 공간의 차원은 $40$, 같은 $U$를 cell마다 적용한 공간은 $20$이다. 이 숫자는 차원 축소만 말한다. 실제 전류나 계산 시간의 오차·이득은 이 비율만으로 정해지지 않는다. 특히 선택한 두 방향이 장치 전위에 의해 버린 방향과 강하게 섞이면 더 많은 mode가 필요하다.[1–3]

## 3. Cell Hamiltonian의 투영과 band 검사

### (1) Cell block 투영

주기적 기준 cell의 두 block을 모두 $U$로 투영한다.

$$
h_0=U^\dagger H_0U\in\mathbb C^{m\times m}
$$

$$
w=U^\dagger WU\in\mathbb C^{m\times m}
$$

줄인 Bloch Hamiltonian은

$$
h(k)=h_0+we^{ika}+w^\dagger e^{-ika}=U^\dagger H(k)U
$$

이다. 마지막 등식은 **같은 $U$를 모든 $k$에 사용했기 때문에** 성립한다. $h(k)$를 대각화해 얻은 $\widetilde\varepsilon_\mu(k)$를 원래 $\varepsilon_n(k)$와 비교한다. 이 과정은 $m<M$일 때 원래 전체 Hamiltonian과 동등한 정확한 좌표 변환이 아니라 retained subspace에 대한 투영 근사이다. 비교는 반드시 정한 $\mathcal W$에서 수행한다.[1–3]

표본 상태가 $U$의 열공간에 정확히 들어간다면, 그 표본 벡터는 그 $k$에서 투영 고유값 문제에도 포함된다. 그러나 **표본점의 재현**이 **표본 사이 모든 band의 재현**을 보장하지 않는다. 원자 Hamiltonian에서는 관심 구간에 원래 모형에 없는 spurious branch가 나타날 수 있다. 원래 band와 줄인 band를 촘촘한 $k$에서 겹쳐 보고, 관심 구간의 빠진 branch와 추가 branch를 모두 찾는다.[1–3]

$$
r_{nk}=\left\|(I_M-UU^\dagger)\psi_{nk}\right\|_2
$$

$r_{nk}$는 원래 고유벡터가 retained 공간 밖에 남기는 비율을 나타내는 차원 없는 진단량이다. $r_{nk}=0$이면 그 벡터가 기저 안에 있고, 큰 값이면 빠진 방향이 있다. 다만 $r_{nk}$가 작은 sampled state만 검사해서는 추가 branch를 발견할 수 없으므로 band 그림과 branch 수를 함께 확인한다.[1–3]

| 비교 대상 | 확인할 질문 | 불일치가 뜻하는 일 |
| --- | --- | --- |
| 원래와 축소 band | $\mathcal W$ 안의 곡선과 극값이 맞는가? | 관심 분산 관계가 바뀜 |
| Band branch 수 | 빠지거나 새로 생긴 branch가 있는가? | 누락 상태 또는 spurious state |
| 표본 사이 파수 | 표본점 사이에서 차이가 생기는가? | $k$ 표본 또는 기저 보완 필요 |

### (2) 완전성과 버린 공간

$U$가 정사각 단위행렬이면 $h(k)$는 단순한 기저 변환이므로 전체 spectrum이 같다. $m<M$이면 버린 공간과의 결합 때문에 정확성이 조건부가 된다. 이를 이해하려면 전체 공간을 retained 공간 $P=UU^\dagger$와 그 여공간 $Q=I_M-P$로 나눈다. 원래 resolvent의 retained 부분에는 버린 공간을 거쳐 돌아오는 효과가 들어간다.

$$
K_{\mathrm{eff}}(z)=K_{PP}(z)-K_{PQ}(z)K_{QQ}^{-1}(z)K_{QP}(z)
$$

여기서 $K(z)=zI-H$, $z=E+i0^+$이며 $K_{AB}$는 $A,B\in\{P,Q\}$ 사이의 block이다. $K_{QQ}$가 가역인 에너지에서 이 식은 정확한 Schur complement이다. 보통의 mode-space 투영은 두 번째 항을 따로 만들지 않으므로 버린 방향의 영향을 band와 열린 장치 결과로 확인해야 한다. 이 식은 계산 절차의 첫 단계가 아니라 왜 검증이 필요한지를 설명한다.[4,5]

## 4. 열린 소자의 NEGF 적용

### (1) 장치 block과 contact

장치에 $N$개 cell이 있고, 각 cell의 전위·구조 효과를 $V_i$라 하자. 주기적 기준과 같은 궤도 배열과 결합 범위를 가진 기본 사례에서 장치 block을 $H_{ii}=H_0+V_i$, $H_{i,i+1}=W$로 쓴다. 같은 $U$를 모든 cell에 적용하면

$$
\mathcal U=\operatorname{diag}(U,U,\ldots,U)
$$

이고 줄인 장치 block은

$$
h_{ii}=U^\dagger(H_0+V_i)U,\qquad h_{i,i+1}=U^\dagger WU=w
$$

이다. $V_i$는 에너지 단위의 연산자이며 단순한 cell 전체의 상수 전위일 필요는 없다. 전위가 cell 내부 궤도마다 다르면 $U^\dagger V_iU$에 mode 사이의 결합이 생길 수 있다. 그 원소를 임의로 지우지 않고 사용한다. Lead도 같은 cell 기준으로 축소하면 그 lead의 surface Green's function과 lead–device 결합을 줄인 공간에서 일관되게 구성한다. 원래 lead의 self-energy가 이미 계산되어 있다면 장치 경계의 $U$로 투영하는 경로도 가능하지만, 두 구성은 버린 lead 상태의 영향을 동일하게 처리하는지 비교해야 한다.[1,3,4]

일반적인 열린 장치의 retarded Green's function은 $h_D=\mathcal U^\dagger H_D\mathcal U$와 양쪽 접촉 self-energy $\Sigma_{L,r}^R,\Sigma_{R,r}^R$로

$$
G_r^R(E)=\left[(E+i0^+)I-h_D-\Sigma_{L,r}^R(E)-\Sigma_{R,r}^R(E)\right]^{-1}
$$

으로 정한다. 아래첨자 $r$은 축소 공간을 뜻한다. 여기서는 위상 결맞음 ballistic 수송이므로 산란 self-energy를 넣지 않았다. 접촉의 broadening 행렬과 advanced Green's function은

$$
\Gamma_{\alpha,r}=i(\Sigma_{\alpha,r}^R-\Sigma_{\alpha,r}^{R\dagger}),\quad
G_r^A=G_r^{R\dagger},\quad \alpha\in\{L,R\}
$$

이다. $\Gamma_{\alpha,r}$는 접촉 $\alpha$가 장치 상태를 열어 주는 정도를 나타내며 $G_r^R$와 같은 축소 공간에서 정의한다.[4,5]

### (2) Transmission과 기준 비교

에너지별 transmission은

$$
T_r(E)=\operatorname{Tr}\!\left[\Gamma_{L,r}G_r^R\Gamma_{R,r}G_r^A\right]
$$

이다. 이 trace는 두 접촉 사이의 전달 확률을 모든 보유 채널에 대해 합한 무차원 값이다. 원래 Hamiltonian과 접촉으로 구한 $T_f(E)$가 기준이다. 두 곡선은 동일한 장치 구조, 전위, 접촉 조건, 에너지 격자에서 비교한다. 선형 눈금만 보면 작은 누설 영역의 차이가 가려질 수 있으므로, 응용에서 작은 transmission이 중요하면 로그 눈금도 본다. 실제 연구는 band 재현 뒤에도 full-space transmission과 전류를 별도로 대조하였다.[1–3,5]

유한 폭의 비교 구간 $\mathcal W_T$와 비음수 가중 함수 $g(E)$를 먼저 정한다. $0<\int_{\mathcal W_T}g(E)\,dE<\infty$이고 아래 분자와 분모의 적분이 모두 유한할 때, 한 가지 요약 오차는

$$
\epsilon_T=\frac{\int_{\mathcal W_T}g(E)|T_r(E)-T_f(E)|\,dE}
{\int_{\mathcal W_T}g(E)\max\{T_f(E),T_0\}\,dE}
$$

이다. $T_0>0$은 $T_f(E)$가 거의 0인 영역의 기준값으로 분석자가 정한다. 위 조건이면 분모는 $T_0\int_{\mathcal W_T}g(E)\,dE$ 이상이므로 양수이다. 이 식은 문헌의 보편 표준이 아니라 곡선 비교를 재현 가능하게 기록하기 위한 이 글의 정의이다. 공명 peak 위치나 터널링 문턱이 핵심이면 적분 오차 하나에 더해 그 위치 차이도 보고한다. Band만 맞거나 한 바이어스의 전류만 맞는다고 모든 바이어스의 $T(E)$가 맞는 것은 아니다.[1–3]

| 검증 단계 | 원래 공간과 축소 공간에서 맞출 입력 | 주로 보는 결과 |
| --- | --- | --- |
| 주기적 기준 | 같은 $H_0,W,a,\mathcal W$와 $k$ 격자 | Band 에너지, 빠진·추가 branch |
| 열린 장치 | 같은 $H_D$, 전위, contact, energy grid | $T_f(E)$와 $T_r(E)$ |
| 필요한 관측량 | 같은 bias와 점유 조건 | 전류, 전하, local density of states |

Transmission이 맞지 않으면 먼저 관심 에너지와 lead 주입 상태가 기저에 들어갔는지 확인한다. 이어 표본 $k$와 $m$을 늘리고, band의 추가 branch 및 장치 전위가 만드는 혼합을 살핀다. Band 검사와 열린 장치 검사를 별도로 하는 이유는 주기적 기준계에 없는 전위·접촉·결함이 장치에 들어가기 때문이다.[1–4]

## 5. 계산 이득의 범위

Cell마다 $M$개 궤도를 가진 $N$-cell 장치에서 block recursive Green's function (RGF)의 조밀한 block 분해 비용은 대표적으로

$$
C_f\sim\mathcal O(NM^3),\qquad C_r\sim\mathcal O(Nm^3)
$$

이다. 이는 **전파 단계의 block 연산**을 비교하는 조건부 scaling이며 wall time의 등식이 아니다. 기저 표본 계산, SVD, 투영, contact 처리, 에너지 적분, self-consistent 전위 계산의 비용은 따로 든다. $m$이 $M$보다 훨씬 작고 축소 block이 조밀하더라도 충분히 작을 때 이득이 커진다. 반대로 관심 에너지에 많은 band가 필요하거나 장치의 공간 변화가 강해 $m$을 늘려야 하면 이득이 줄어든다.[1,3,4]

$$
\text{cell block storage: }\mathcal O(M^2)\longrightarrow\mathcal O(m^2)
$$

이 저장량 관계도 같은 수의 조밀한 block을 보관한다는 가정에서 나온다. RGF는 길이 방향의 소거 알고리즘이고 mode-space reduction은 각 block의 기저 차원을 줄이는 단계이므로, 둘을 이어서 쓸 수 있다. 실제 계산 보고에는 원래·축소 차원, 기저 구성 시간, 전파 시간과 전체 시간을 따로 적는 편이 계산 이득의 원인을 보여 준다.[1,3,4,5]

## 6. 재현 가능한 기본 절차

처음 적용할 때는 다음 순서가 핵심이다. 각 단계의 출력이 다음 단계의 입력이 되므로 band가 확인되기 전에 장치 결과만으로 기저를 승인하지 않는다.[1–3]

| 순서 | 입력과 수행 | 남길 기록 |
| --- | --- | --- |
| 1 | 주기적 $H_0,W$, cell 간격 $a$, 궤도·에너지 규약을 확정 | 원래 block 차원 $M$과 결합 범위 |
| 2 | 대상 장치와 관측량으로 $\mathcal W$를 설정 | $E_-,E_+$와 선택 이유 |
| 3 | $H(k)$를 풀고 여러 $k$의 관심 Bloch 벡터를 수집 | $k$ 표본, 선택 band, $\Phi_0$의 열 수 |
| 4 | SVD 등으로 중복 방향을 제거해 공통 $U$ 구성 | $m$, rank 경계값, $U^\dagger U$ 오차 |
| 5 | $H_0,W$를 투영하고 촘촘한 $k$에서 band 비교 | 빠진·추가 branch, band 오차 |
| 6 | 장치와 contact를 일관되게 축소해 NEGF 계산 | $T_r(E)$, 같은 입력의 $T_f(E)$ 및 허용 오차 |

이 절차의 종료 조건은 특정 mode 수가 아니다. 연구자가 선언한 에너지·바이어스 범위에서 band와 필요한 열린 장치 관측량이 mode 수, $k$ 표본, window 변경에 대해 충분히 안정해야 한다. 실패하면 그 원인이 window 누락인지, 표본 부족인지, 추가 branch인지, 장치의 국소 혼합인지 나눠 확인한다.[1–3]

## 7. 확장과 한계

### (1) Spurious band와 기저 보완

표본으로 넣은 물리적 Bloch 상태를 보존하면서도 축소 band 안에 원래 모형에 없는 branch가 생길 수 있다. Atomistic full-band 계산에서는 단순히 표본을 늘리는 것만으로 해결되지 않을 수 있어, 현재 $U$의 여공간에서 보완 벡터를 더해 관심 window의 spurious branch를 밀어내는 방법이 쓰인다. 보완 뒤에는 전체 window의 band를 다시 검사한다. 이는 첫 기저를 만들기 전에 수행하는 독립 작업이 아니라 초기 band 검사에서 실패를 발견했을 때의 정리 단계이다.[1–3]

$$
Q=I_M-UU^\dagger
$$

$Q$는 직교 궤도 규약에서 현재 기저가 버린 방향으로의 projector이다. 보완 후보는 이 공간에서 만들지만, 어떤 후보가 적절한지는 band 검사로 결정한다. 원래 물리 band까지 지우는 방식으로 겉모양만 맞추면 안 된다.[1–3]

### (2) 위치별 기저와 mode 결합

물질·단면·결함 때문에 모든 cell을 한 주기적 기준으로 대표할 수 없으면 cell마다 $U_i\in\mathbb C^{M_i\times m_i}$를 만들 수 있다. 이때 인접 block은

$$
h_{i,i+1}=U_i^\dagger H_{i,i+1}U_{i+1}
$$

로 계산하며 크기는 $m_i\times m_{i+1}$일 수 있다. 이 block의 서로 다른 mode 사이 원소가 공간 변화에 따른 혼합을 담는다. Coupled mode space (CMS)는 이를 유지하고, uncoupled mode space (UMS)는 mode 또는 group 사이 결합을 추가로 무시한다. 후자는 기저 축소와 별개의 근사이므로 급격한 구조 변화나 disorder에서는 CMS 및 원래 공간과 대조한다.[3,4,6]

### (3) 산란과 비직교 궤도

전자–phonon 산란을 넣으면 줄인 $H$만으로 끝나지 않는다. 상호작용 연산자와 관련 self-energy도 같은 기저 규약에서 구성해야 하며, 산란은 서로 다른 mode와 에너지를 연결할 수 있다. Ballistic $T(E)$가 맞아도 산란을 켠 전류가 자동으로 맞는 것은 아니다. 산란 모형, 에너지 범위와 mode 수에 대한 수렴 검사를 다시 해야 한다.[2,7]

원래 원자 궤도가 비직교이고 overlap $S$가 있다면 $H\psi=ES\psi$의 generalized eigenproblem을 쓴다. 축소 문제에서도

$$
S_r=\mathcal U^\dagger S\mathcal U,\qquad H_r=\mathcal U^\dagger H\mathcal U
$$

를 함께 유지한다. Euclidean 직교화 $U^\dagger U=I$만으로 $S_r=I$라고 둘 수 없다. Overlap metric, lead 결합과 density 해석을 같은 규약으로 맞추는 일은 별도 확장 단계이다.[3,8]

## 8. 요약

- 지정된 주기적 $H_0,W$와 관심 에너지 window에서 출발해 $H(k)$의 Bloch 상태를 여러 $k$에서 모은다.
- 수집한 상태의 중복 방향을 정리한 $k$ 독립 cell 기저 $U$로 모든 관련 block을 투영한다.
- 축소 band의 빠진·추가 branch를 확인한 뒤, 같은 조건의 원래 공간과 축소 공간에서 장치 transmission을 비교한다.
- Spurious band 보완, 위치별 기저, mode 결합, 산란과 비직교 overlap은 기본 절차 뒤에 각각 검증하는 확장이다.

## 9. 참고문헌

1. J. Z. Huang, H. Ilatikhameneh, M. Povolotskyi, and G. Klimeck, “Robust Mode Space Approach for Atomistic Modeling of Realistically Large Nanowire Transistors,” *Journal of Applied Physics* **123**, 044303 (2018). [DOI: 10.1063/1.5010238](https://doi.org/10.1063/1.5010238). [arXiv:1710.08064](https://arxiv.org/abs/1710.08064).
2. G. Mil’nikov, N. Mori, and Y. Kamakura, “Low-dimensional Quantum Transport Models in Atomistic Device Simulations,” *2011 International Conference on Simulation of Semiconductor Processes and Devices (SISPAD)*, 315–318 (2011). [DOI: 10.1109/SISPAD.2011.6035033](https://doi.org/10.1109/SISPAD.2011.6035033). [Full text](https://in4.iue.tuwien.ac.at/pdfs/sispad2011/pdf/11-5.pdf).
3. M. Shin, “Hetero-structure mode space method for efficient device simulations,” *Journal of Applied Physics* **130**, 104303 (2021). [DOI: 10.1063/5.0064314](https://doi.org/10.1063/5.0064314). [arXiv:2107.10511](https://arxiv.org/abs/2107.10511).
4. R. Grassi, A. Gnudi, I. Imperiale, E. Gnani, S. Reggiani, and G. Baccarani, “Mode space approach for tight-binding transport simulations in graphene nanoribbon field-effect transistors including phonon scattering,” *Journal of Applied Physics* **113**, 144506 (2013). [DOI: 10.1063/1.4800900](https://doi.org/10.1063/1.4800900). [arXiv:1302.0694](https://arxiv.org/abs/1302.0694).
5. C. H. Lewenkopf and E. R. Mucciolo, “The recursive Green’s function method for graphene,” *Journal of Computational Electronics* **12**, 203–231 (2013). [DOI: 10.1007/s10825-013-0458-7](https://doi.org/10.1007/s10825-013-0458-7). [arXiv:1304.3934](https://arxiv.org/abs/1304.3934).
6. M. Luisier, A. Schenk, and W. Fichtner, “Quantum transport in two- and three-dimensional nanoscale transistors: Coupled mode effects in the nonequilibrium Green’s function formalism,” *Journal of Applied Physics* **100**, 043713 (2006). [DOI: 10.1063/1.2244522](https://doi.org/10.1063/1.2244522). [Author-hosted full text](https://iis-people.ee.ethz.ch/~schenk/JApplPhys_100_043713.pdf).
7. D. A. Lemus, J. Charles, and T. Kubis, “Mode-space-compatible inelastic scattering in atomistic nonequilibrium Green’s function implementations,” *Journal of Computational Electronics* **19**, 1389–1398 (2020). [DOI: 10.1007/s10825-020-01549-8](https://doi.org/10.1007/s10825-020-01549-8). [arXiv:2003.09536](https://arxiv.org/abs/2003.09536).
8. T. Ozaki, K. Nishio, and H. Kino, “Efficient implementation of the nonequilibrium Green function method for electronic transport calculations,” *Physical Review B* **81**, 035116 (2010). [DOI: 10.1103/PhysRevB.81.035116](https://doi.org/10.1103/PhysRevB.81.035116). [arXiv:0908.4142](https://arxiv.org/abs/0908.4142).
