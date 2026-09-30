---
description: 주기적 원자 Hamiltonian에서 Bloch 상태를 골라 작은 cell 기저를 만들고, 이를 NEGF 수송에 적용해 검증하는 절차를 설명한다.
---

# NEGF: Mode-space reduction

**Mode-space reduction**은 지정한 에너지 범위의 수송을 설명하는 데 필요한 cell 내부 상태만 남겨 Hamiltonian의 block 크기를 줄이는 방법이다. 이 글의 출발점은 이미 정해진 주기적 원자 Hamiltonian이다. 먼저 그 Hamiltonian의 band를 풀고, 여러 파수의 Bloch 상태를 하나의 작은 cell 기저로 모은다. 그 기저에 Hamiltonian을 투영한 뒤 band를 다시 확인하고, 마지막으로 열린 소자의 [nonequilibrium Green's function (NEGF)](negf-formalism.md) 계산에 적용한다. 작은 기저를 쓴 결과는 원래 원자 기저의 계산과 비교해야 한다.[1–3]

여기서는 수송축으로 같은 cell이 반복되는 직교 원자 궤도 모형과 이웃 cell까지만 결합하는 ballistic 문제를 기본 사례로 삼는다. Cell당 원자 궤도 수를 $M$, 남길 기저 벡터 수를 $m<M$, 반복 간격을 $a$라 한다. 접합, 산란, 비직교 궤도의 추가 조건은 6절에서 다룬다. 에너지의 기준과 Hamiltonian의 전위 부호는 입력 모형에서 정한 것을 그대로 유지한다.[1–3]

전체 과정은 다음과 같다. 앞 단계에서 얻은 기저와 행렬을 다음 단계에 그대로 사용한다.[1–3]

| 순서 | 수행할 일 | 다음 단계에 넘길 결과 |
| --- | --- | --- |
| 1 | 주기적 Hamiltonian과 관심 에너지 범위 설정 | Cell 내부와 이웃 cell 사이의 행렬 |
| 2 | 여러 파수에서 관심 band의 Bloch 상태 수집 | 표본 상태를 열로 모은 행렬 |
| 3 | 중복 방향을 정리하고 공통 기저 구성 | 남길 기저 벡터와 기저 차원 |
| 4 | Hamiltonian 투영과 band 검증 | 원래 band를 재현하는 축소 block |
| 5 | 장치와 접촉의 NEGF 계산 및 기준 비교 | Transmission과 필요한 관측량의 오차 |

## 1. 주기적 기준 Hamiltonian

### (1) Cell block과 Bloch 문제

$H_0\in\mathbb C^{M\times M}$은 한 cell의 Hamiltonian, $W\in\mathbb C^{M\times M}$는 행이 cell $j$, 열이 cell $j+1$에 해당하는 결합 block이다. 그러면 주기적 기준계의 block은

$$
H_{jj}=H_0,\qquad H_{j,j+1}=W,\qquad H_{j+1,j}=W^\dagger
$$

이다. $H_0$은 Hermitian이고, 반대 방향 결합은 $W^\dagger$이다. Cell $j$의 궤도 진폭을 $c_j$라 하면 에너지 $E$인 정상상태는

$$
W^\dagger c_{j-1}+H_0c_j+Wc_{j+1}=Ec_j
$$

를 만족한다. 왼쪽 항부터 이전 cell의 영향, 현재 cell 안의 작용, 다음 cell의 영향을 나타낸다. 이 실공간 식에 Bloch 형태 $c_j=e^{ikja}\psi_{nk}$를 대입하면 cell 내부 벡터 $\psi_{nk}\in\mathbb C^M$가 푸는 행렬은

$$
H(k)=H_0+We^{ika}+W^\dagger e^{-ika}
$$

이고 고유값 문제는

$$
H(k)\psi_{nk}=\varepsilon_n(k)\psi_{nk},\qquad
\psi_{nk}^\dagger\psi_{nk}=1
$$

이다. $k$는 길이의 역수, $ka$는 무차원 위상, $\varepsilon_n(k)$는 에너지이다. 여기서 **band**는 $k$에 따른 $\varepsilon_n(k)$의 곡선이며, **Bloch eigenvector** $\psi_{nk}$는 그 상태의 한 cell 안 궤도 진폭이다. $k$마다 풀어 얻는 벡터는 서로 같을 필요가 없다. 따라서 한 $k$의 몇 벡터만으로 전체 관심 band를 표현할 수 있다고 가정하지 않는다.[1–4]

유한한 결합 범위보다 충분히 긴 cell을 택하면 모든 결합을 cell 내부와 이웃 cell 사이의 block에 담을 수 있다. 그러한 재분할을 하지 않은 장거리 결합 모형에는 $H(k)$에 더 먼 cell의 Fourier 항도 넣어야 한다. 이하의 식은 위 이웃 cell 규약을 따른다.[1,3]

### (2) 관심 에너지 범위

관찰하거나 계산할 에너지 구간을 $\mathcal W=[E_{\min},E_{\max}]$로 먼저 정한다. 예를 들어 전도대 가장자리의 수송을 본다면 해당 가장자리와 계산할 주입·터널링 에너지가 구간 안에 있어야 한다. 구간 밖 band까지 모두 재현하려고 하면 작은 기저라는 목적이 약해진다. 반대로 구간이 너무 좁으면 바이어스나 전위 변화로 수송에 참여하는 상태를 놓친다. 따라서 관심 에너지 범위는 재료의 band뿐 아니라 계산할 소자의 동작 조건을 바탕으로 정한다.[1–3]

$$
\mathcal B_{\mathcal W}(k)=\{n:\varepsilon_n(k)\in\mathcal W\}
$$

이 집합은 파수 $k$에서 관심 에너지 범위에 들어오는 band 번호를 뜻한다. 표본 $k_1,\ldots,k_{N_k}$는 Brillouin zone에 걸쳐 놓고, 각 점에서 $n\in\mathcal B_{\mathcal W}(k_l)$인 벡터를 수집한다. Band 끝점이나 valley 주변처럼 곡선의 성격이 달라지는 곳은 표본을 더 촘촘하게 둔다. 표본이 일부 파수만 대표하므로, 나중에 더 조밀한 $k$ 격자에서 원래 band와 비교한다.[1–3]

## 2. Bloch 표본과 공통 cell 기저

### (1) 표본 행렬과 독립 방향

선택한 Bloch eigenvector를 열로 이은 행렬을 $\Phi_0$라 한다. 선택한 열의 총수가 $p$이면

$$
\Phi_0=[\psi_{n_1q_1},\psi_{n_2q_2},\ldots,\psi_{n_pq_p}]
\in\mathbb C^{M\times p}
$$

이다. 여기서 $(n_s,q_s)$는 $s$번째로 선택한 band와 파수의 쌍이며, $q_s$는 앞서 정한 $k$ 표본 중 하나이다. 같은 파수에서 여러 band를 고르면 그 파수가 열 목록에 여러 번 나타난다. 서로 다른 $k$의 벡터는 각각 정규화되어도 열 전체가 서로 직교하지 않는다. 같은 물리적 방향을 여러 번 수집했을 수도 있다. 따라서 수집한 열의 수 $p$와 최종 기저 차원 $m$은 같지 않을 수 있다. 직교 원자 궤도에서는 singular value decomposition (SVD)

$$
\Phi_0=L\,\operatorname{diag}(\sigma_1,\sigma_2,\ldots)R^\dagger
$$

으로 선형 독립 방향을 정리하고, 충분히 작은 $\sigma_\alpha$에 해당하는 방향을 제외한다. 남은 $m$개 왼쪽 singular vector를 모아

$$
U=[\ell_1,\ldots,\ell_m]\in\mathbb C^{M\times m},\qquad U^\dagger U=I_m
$$

로 둔다. $\ell_\alpha$는 $L$의 $\alpha$번째 열이며, singular value는 큰 값부터 정렬한다. $U$의 열은 원래 cell 궤도 공간에 놓인 직교 단위벡터이다. SVD에서 작은 singular value를 제외하는 기준은 표본의 중복과 근사 수준을 조절한다. 낮은 singular value 방향을 버렸을 때 관심 band나 수송이 달라지면 표본 또는 $m$을 다시 정한다.[1–3]

**완성한 $U$는 $k$와 무관한 공통 cell 기저이다.** 여러 $k$의 고유벡터를 재료로 삼아, 관심 band에 필요한 cell 내부 진폭을 한 행렬에 담는다. SVD로 얻은 각 열은 여러 표본 상태의 선형결합이므로 특정 $k$나 특정 band 하나와 일대일로 대응할 필요가 없다. 따라서 원래 band와 줄인 band를 같은 $k$의 Hamiltonian에 대해 직접 비교할 수 있으며, 같은 종류의 cell이 반복되는 장치에도 같은 $U$를 적용할 수 있다. 물질이나 단면이 다른 cell의 기저는 6절처럼 별도로 구성한다.[1–3]

장치의 $j$번째 cell 파동함수 계수를 $c_j\in\mathbb C^M$, 줄인 계수를 $\xi_j\in\mathbb C^m$라고 하면 실제 축소 가정은

$$
c_j\approx U\xi_j,\qquad \xi_j=U^\dagger c_j
$$

이다. 첫 관계는 $m$개 열벡터의 선형결합으로 cell 상태를 근사한다는 뜻이다. 두 번째 관계는 주어진 원래 상태를 그 기저에 투영한 계수이다. 두 식을 합치면 $UU^\dagger c_j$만 남으므로, 버린 공간의 진폭은 이 표현에서 복원되지 않는다. 이 때문에 $U$의 직교성만 확인해서 정확도를 판정할 수 없고, 대상 band와 장치 관측량을 따로 검사한다.[1–3]

### (2) 행렬 차원의 예

다음은 실제 재료의 계산값이 아니라 행렬 크기를 보여 주는 예이다. Cell에 네 궤도가 있고, 서로 다른 세 $k$점에서 관심 band 두 개씩 골랐다고 하자. 그러면 $\Phi_0$는 $4\times6$이다. 여섯 열이 두 개의 독립 방향에 충분히 가깝고 그 두 방향만으로 관심 band를 재현한다면 $U$는 $4\times2$이다. 벡터 여섯 개를 모아도 필요한 독립 방향은 두 개일 수 있다는 예이다. 실제 $m$은 표본의 선형 독립성과 정확도 검사로 결정한다.

| 단계 | 이 예의 크기 | 역할 |
| --- | --- | --- |
| 원래 cell $H_0,W$ | 각각 $4\times4$ | 네 원자 궤도의 에너지와 cell 결합 |
| 수집 행렬 $\Phi_0$ | $4\times6$ | 세 $k$점의 두 Bloch 상태씩 저장 |
| 공통 기저 $U$ | $4\times2$ | 중복 방향을 정리한 두 기저 벡터 |
| 줄인 cell block | 각각 $2\times2$ | 두 기저 벡터 사이 결합을 계산 |

열 개 cell로 만든 장치라면 원래 궤도 공간의 차원은 $40$, 같은 $U$를 cell마다 적용한 공간은 $20$이다. 이 숫자는 차원 축소만 말한다. 실제 전류나 계산 시간의 오차·이득은 이 비율만으로 정해지지 않는다. 특히 선택한 두 방향이 장치 전위에 의해 버린 방향과 강하게 섞이면 더 많은 mode가 필요하다.[1–3]

## 3. Hamiltonian 투영과 band 검증

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

이다. 마지막 등식은 **같은 $U$를 모든 $k$에 사용했기 때문에** 성립한다. $h(k)$를 대각화해 얻은 $\widetilde\varepsilon_\mu(k)$를 원래 $\varepsilon_n(k)$와 비교한다. 이 과정은 $m<M$일 때 원래 전체 Hamiltonian과 동등한 정확한 좌표 변환이 아니라 선택한 부분공간에 대한 투영 근사이다. 비교는 반드시 정한 $\mathcal W$에서 수행한다.[1–3]

실공간에서도 1절의 식에 $c_j\approx U\xi_j$를 넣고 왼쪽에 $U^\dagger$를 곱하면

$$
w^\dagger\xi_{j-1}+h_0\xi_j+w\xi_{j+1}=E\xi_j
$$

를 얻는다. 원래 식과 cell 사이의 연결 구조는 같고, cell 내부 미지수만 $M$개에서 $m$개로 줄었다. 따라서 기존 block 수송 알고리즘에 축소 행렬을 입력할 수 있다.[1–4]

### (2) Band 검증과 기저 보완

표본 상태가 $U$의 열공간에 정확히 들어간다면, 그 표본 벡터는 그 $k$에서 투영 고유값 문제에도 포함된다. 그러나 **표본점의 재현**이 **표본 사이 모든 band의 재현**을 보장하지 않는다. **축소 Hamiltonian에는 원래 band에 없는 가짜 해가 나타날 수 있다.** 그 해가 이루는 분산 곡선을 spurious branch라 한다. 원래 band와 줄인 band를 촘촘한 $k$에서 겹쳐 보고, 관심 구간에서 누락된 band와 가짜 해가 만든 곡선을 모두 찾는다.[1–3]

$$
r_{nk}=\left\|(I_M-UU^\dagger)\psi_{nk}\right\|_2
$$

$r_{nk}$는 정규화된 원래 고유벡터에서 선택한 부분공간 밖에 남은 성분의 norm이며, 0과 1 사이의 차원 없는 값이다. $r_{nk}=0$이면 그 벡터가 기저 안에 있고, 큰 값이면 빠진 방향이 있다. 다만 $r_{nk}$가 작은 표본 상태만 검사해서는 가짜 해를 발견할 수 없으므로 band 곡선의 모양과 개수도 함께 확인한다.[1–3]

| 비교 대상 | 확인할 질문 | 불일치가 뜻하는 일 |
| --- | --- | --- |
| 원래와 축소 band | $\mathcal W$ 안의 곡선과 극값이 맞는가? | 관심 분산 관계가 바뀜 |
| Band 곡선의 개수 | 빠지거나 새로 생긴 곡선이 있는가? | 상태 누락 또는 가짜 해 |
| 표본 사이 파수 | 표본점 사이에서 차이가 생기는가? | $k$ 표본 또는 기저 보완 필요 |

가짜 해가 남아 있으면 현재 $U$에 직교하는 공간에서 보완 벡터를 찾아 기저에 더한다. 적절한 벡터를 선택하면 이미 표현된 Bloch 상태는 보존하면서 가짜 해의 에너지를 관심 범위 밖으로 옮길 수 있다. 이 최적화는 표본을 무작정 늘리는 것과 다르며, 보완할 때마다 전체 관심 범위의 band를 다시 검사한다. 기저를 보완하면 $m$도 증가하므로, 최종 계산에는 보완을 마친 $U$와 다시 투영한 block을 사용한다.[1–3]

$$
Q=I_M-UU^\dagger
$$

$Q$는 직교 궤도 규약에서 현재 기저가 버린 방향으로의 projector이다. 보완 후보는 이 공간에서 만들지만, 어떤 후보가 적절한지는 band 검사로 결정한다. 따라서 보완의 대상은 기저 행렬 $U$이며, 계산된 band 곡선을 사후에 삭제하는 절차가 아니다.[1–3]

## 4. 열린 소자의 NEGF 적용

### (1) 장치 block과 contact

장치에 $N$개 cell이 있고, 각 cell 내부에 더해지는 전위 에너지 행렬을 $V_i$라 하자. 주기적 기준과 같은 궤도 배열과 결합 범위를 가진 기본 사례에서 장치 block을 $H_{ii}=H_0+V_i$, $H_{i,i+1}=W$로 쓴다. 같은 $U$를 모든 cell에 적용하면

$$
\mathcal U=\operatorname{diag}(U,U,\ldots,U)
$$

이고 줄인 장치 block은

$$
h_{ii}=U^\dagger(H_0+V_i)U,\qquad h_{i,i+1}=U^\dagger WU=w
$$

이다. $V_i$는 cell 전체에 일정한 상수일 수도 있고, 궤도마다 다른 전위 에너지를 가질 수도 있다. 전위가 cell 내부 궤도마다 다르면 $U^\dagger V_iU$에 mode 사이의 결합이 생길 수 있다. 기본 계산에서는 이 결합 원소를 모두 유지한다. 예를 들어 $V_i=v_i I_M$인 일정한 전위는 $U^\dagger V_iU=v_iI_m$이므로 모든 mode의 에너지를 똑같이 옮긴다. 반면 횡방향으로 변하는 전위는 일반적으로 비대각 원소를 만든다. 따라서 기저를 줄이는 단계와 mode 사이 결합을 무시하는 단계는 구분해야 한다.[1,2,4]

Lead도 같은 cell 기준으로 축소하면 그 lead의 surface Green's function과 lead–device 결합을 줄인 공간에서 일관되게 구성한다. 원래 lead의 self-energy가 이미 계산되어 있다면 장치 경계의 $U$로 투영하는 경로도 가능하지만, 두 구성은 버린 lead 상태의 영향을 동일하게 처리하는지 비교해야 한다.[1,3,4]

축소한 열린 장치의 retarded Green's function은 $h_D=\mathcal U^\dagger H_D\mathcal U$와 양쪽 접촉 self-energy $\Sigma_{L,r}^R,\Sigma_{R,r}^R$로

$$
G_r^R(E)=\left[(E+i0^+)I-h_D-\Sigma_{L,r}^R(E)-\Sigma_{R,r}^R(E)\right]^{-1}
$$

으로 정한다. 아래첨자 $r$은 축소 공간을 뜻하며, $I$의 차원은 $Nm$이다. $H_D$는 전체 장치 Hamiltonian, $h_D$는 이를 투영한 행렬이다. 양의 무한소 $0^+$는 retarded 경계 조건을 지정한다. 여기서는 위상 결맞음 ballistic 수송이므로 산란 self-energy를 넣지 않았다. 접촉의 broadening 행렬과 advanced Green's function은

$$
\Gamma_{\alpha,r}=i(\Sigma_{\alpha,r}^R-\Sigma_{\alpha,r}^{R\dagger}),\quad
G_r^A=G_r^{R\dagger},\quad \alpha\in\{L,R\}
$$

이다. $\Gamma_{\alpha,r}$는 접촉 $\alpha$와의 결합으로 생기는 에너지 준위의 폭을 나타내며 $G_r^R$와 같은 축소 공간에서 정의한다.[4,5]

### (2) Transmission과 기준 비교

에너지별 transmission은

$$
T_r(E)=\operatorname{Tr}\!\left[\Gamma_{L,r}G_r^R\Gamma_{R,r}G_r^A\right]
$$

이다. 이 trace는 두 접촉 사이의 전달 확률을 축소 모형의 모든 전도 채널에 대해 합한 무차원 값이다. 원래 Hamiltonian과 접촉으로 구한 $T_f(E)$가 기준이다. 두 곡선은 동일한 장치 구조, 전위, 접촉 조건, 에너지 격자에서 비교한다. 선형 눈금만 보면 작은 누설 영역의 차이가 가려질 수 있으므로, 응용에서 작은 transmission이 중요하면 로그 눈금도 본다. 실제 연구는 band 재현 뒤에도 원래 기저의 transmission과 전류를 별도로 대조하였다.[1–3,5,6]

수치 오차를 기록할 때는 비교할 에너지 격자 $E_l$을 고정하고, 예를 들어 다음 최대 절대 오차를 사용할 수 있다.

$$
\Delta_T=\max_l\left|T_r(E_l)-T_f(E_l)\right|
$$

이는 이 글에서 선택한 비교 지표이며, $T$와 마찬가지로 무차원이다. 문헌 공통의 허용 오차를 뜻하지 않으며, 허용값은 대상 소자의 목적에 맞춰 정한다. $T_f$가 0에 가까워도 정의할 수 있다. 다만 작은 터널링 신호의 상대적인 차이나 공명 위치의 이동은 이 숫자 하나로 충분히 드러나지 않는다. 관심 에너지 구간에서 두 곡선을 함께 보고, 공명이나 문턱 부근은 에너지 격자를 좁혀 확인한다. 같은 소자에서 mode 수와 기저 구성에 쓴 에너지 범위를 바꾸어 결과가 안정되는지도 살핀다.[1–3]

| 검증 단계 | 원래 공간과 축소 공간에서 맞출 입력 | 주로 보는 결과 |
| --- | --- | --- |
| 주기적 기준 | 같은 $H_0,W,a,\mathcal W$와 $k$ 격자 | Band 에너지, 누락된 band와 가짜 해 |
| 열린 장치 | 같은 $H_D$, 전위, 접촉, 에너지 격자 | $T_f(E)$와 $T_r(E)$ |
| 필요한 관측량 | 같은 바이어스와 점유 조건 | 전류, 전하, local density of states |

Transmission이 맞지 않으면 먼저 관심 에너지와 lead 주입 상태가 기저에 들어갔는지 확인한다. 이어 표본 $k$와 $m$을 늘리고, band의 가짜 해 및 장치 전위가 만드는 혼합을 살핀다. Band 검사와 열린 장치 검사를 별도로 하는 이유는 주기적 기준계에 없는 전위·접촉·결함이 장치에 들어가기 때문이다.[1–4]

## 5. 계산 이득의 범위

Cell마다 $M$개 궤도를 가진 $N$-cell 장치에서 block recursive Green's function (RGF)의 조밀한 block 분해 비용은 대표적으로

$$
C_f\sim\mathcal O(NM^3),\qquad C_r\sim\mathcal O(Nm^3)
$$

이다. 이는 **같은 cell 분할에서 조밀한 block을 처리하는 연산량**의 비교이다. 전체 계산 시간에는 Bloch 표본 계산, SVD, 투영, 접촉 처리, 에너지 적분, 전위의 self-consistent 계산 비용도 포함된다. $m$이 $M$보다 훨씬 작고 축소 block이 조밀하더라도 충분히 작을 때 이득이 커진다. 반대로 관심 에너지에 많은 band가 필요하거나 장치의 공간 변화가 강해 $m$을 늘려야 하면 이득이 줄어든다.[1,3,4]

$$
\text{cell block storage: }\mathcal O(M^2)\longrightarrow\mathcal O(m^2)
$$

이 저장량 관계도 같은 수의 조밀한 block을 보관한다는 가정에서 나온다. RGF는 길이 방향의 소거 알고리즘이고 mode-space reduction은 각 block의 기저 차원을 줄이는 단계이므로, 둘을 이어서 쓸 수 있다. 실제 계산 보고에는 원래·축소 차원, 기저 구성 시간, 전파 시간과 전체 시간을 따로 적는 편이 계산 이득의 원인을 보여 준다.[1,3,4,5]

## 6. 기본 모형의 확장

### (1) 위치별 기저와 mode 결합

물질·단면·결함 때문에 모든 cell을 한 주기적 기준으로 대표할 수 없으면 cell마다 $U_i\in\mathbb C^{M_i\times m_i}$를 만들 수 있다. 이때 인접 block은

$$
h_{i,i+1}=U_i^\dagger H_{i,i+1}U_{i+1}
$$

로 계산하며 크기는 $m_i\times m_{i+1}$일 수 있다. 이 block의 서로 다른 mode 사이 원소가 공간 변화에 따른 혼합을 담는다. Coupled mode space (CMS)는 이를 유지하고, uncoupled mode space (UMS)는 개별 mode 또는 mode 묶음 사이의 결합을 추가로 무시한다. 후자는 기저 축소와 별개의 근사이므로 급격한 구조 변화나 무질서에서는 CMS 및 원래 공간과 대조한다.[3,4,7]

### (2) 산란과 비직교 궤도

전자–포논 산란을 넣으면 줄인 $H$만으로 끝나지 않는다. 상호작용 연산자와 관련 self-energy도 같은 기저 규약에서 구성해야 하며, 산란은 서로 다른 mode와 에너지를 연결할 수 있다. Ballistic $T(E)$가 맞아도 산란을 켠 전류가 자동으로 맞는 것은 아니다. 산란 모형, 에너지 범위와 mode 수에 대한 수렴 검사를 다시 해야 한다.[2,4,8]

원래 원자 궤도가 비직교이고 overlap $S$가 있다면 $H\psi=ES\psi$의 generalized eigenproblem을 쓴다. 축소 문제에서도

$$
S_r=\mathcal U^\dagger S\mathcal U,\qquad H_r=\mathcal U^\dagger H\mathcal U
$$

를 함께 유지한다. Euclidean 직교화 $U^\dagger U=I$만으로 $S_r=I$라고 둘 수 없다. 이 확장에서는 중첩 행렬 $S$로 정의한 내적에 맞춰 기저를 정규화하고, lead 결합과 전자 밀도도 비직교 기저의 규약으로 계산한다.[3,6]

## 7. 요약

- 지정된 주기적 $H_0,W$와 관심 에너지 범위에서 출발해 $H(k)$의 Bloch 상태를 여러 $k$에서 모은다.
- 수집한 상태의 중복 방향을 정리한 $k$ 독립 cell 기저 $U$로 모든 관련 block을 투영한다.
- 축소 band의 누락된 band와 가짜 해를 확인한 뒤, 같은 조건의 원래 공간과 축소 공간에서 장치 transmission을 비교한다.
- 가짜 해가 있으면 기저를 보완해 band 검증을 반복한다. 위치별 기저, 산란, 비직교 overlap은 기본 모형에 필요한 연산자를 추가하는 확장이다.

## 8. 참고문헌

1. J. Z. Huang, H. Ilatikhameneh, M. Povolotskyi, and G. Klimeck, “Robust Mode Space Approach for Atomistic Modeling of Realistically Large Nanowire Transistors,” *Journal of Applied Physics* **123**, 044303 (2018). [DOI: 10.1063/1.5010238](https://doi.org/10.1063/1.5010238). [arXiv:1710.08064](https://arxiv.org/abs/1710.08064).
2. G. Mil’nikov, N. Mori, and Y. Kamakura, “Low-dimensional Quantum Transport Models in Atomistic Device Simulations,” *2011 International Conference on Simulation of Semiconductor Processes and Devices (SISPAD)*, 315–318 (2011). [DOI: 10.1109/SISPAD.2011.6035033](https://doi.org/10.1109/SISPAD.2011.6035033). [Full text](https://in4.iue.tuwien.ac.at/pdfs/sispad2011/pdf/11-5.pdf).
3. M. Shin, “Hetero-structure mode space method for efficient device simulations,” *Journal of Applied Physics* **130**, 104303 (2021). [DOI: 10.1063/5.0064314](https://doi.org/10.1063/5.0064314). [arXiv:2107.10511](https://arxiv.org/abs/2107.10511).
4. R. Grassi, A. Gnudi, I. Imperiale, E. Gnani, S. Reggiani, and G. Baccarani, “Mode space approach for tight-binding transport simulations in graphene nanoribbon field-effect transistors including phonon scattering,” *Journal of Applied Physics* **113**, 144506 (2013). [DOI: 10.1063/1.4800900](https://doi.org/10.1063/1.4800900). [arXiv:1302.0694](https://arxiv.org/abs/1302.0694).
5. C. H. Lewenkopf and E. R. Mucciolo, “The recursive Green’s function method for graphene,” *Journal of Computational Electronics* **12**, 203–231 (2013). [DOI: 10.1007/s10825-013-0458-7](https://doi.org/10.1007/s10825-013-0458-7). [arXiv:1304.3934](https://arxiv.org/abs/1304.3934).
6. T. Ozaki, K. Nishio, and H. Kino, “Efficient implementation of the nonequilibrium Green function method for electronic transport calculations,” *Physical Review B* **81**, 035116 (2010). [DOI: 10.1103/PhysRevB.81.035116](https://doi.org/10.1103/PhysRevB.81.035116). [arXiv:0908.4142](https://arxiv.org/abs/0908.4142).
7. M. Luisier, A. Schenk, and W. Fichtner, “Quantum transport in two- and three-dimensional nanoscale transistors: Coupled mode effects in the nonequilibrium Green’s function formalism,” *Journal of Applied Physics* **100**, 043713 (2006). [DOI: 10.1063/1.2244522](https://doi.org/10.1063/1.2244522). [Author-hosted full text](https://iis-people.ee.ethz.ch/~schenk/JApplPhys_100_043713.pdf).
8. D. A. Lemus, J. Charles, and T. Kubis, “Mode-space-compatible inelastic scattering in atomistic nonequilibrium Green’s function implementations,” *Journal of Computational Electronics* **19**, 1389–1398 (2020). [DOI: 10.1007/s10825-020-01549-8](https://doi.org/10.1007/s10825-020-01549-8). [arXiv:2003.09536](https://arxiv.org/abs/2003.09536).
