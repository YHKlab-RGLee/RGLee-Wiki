---
description: 주기적 cell Hamiltonian의 Bloch 표본으로 작은 공통 기저를 구성하고, band·잔차·NEGF transmission으로 적용 범위를 검증한다.
---

# NEGF: Mode-space reduction

**Mode-space reduction**은 nonequilibrium Green's function (NEGF) 계산에서 각 cell의 궤도 자유도를 줄이는 방법이다. 소자를 수송 방향으로 여러 cell block으로 나누더라도, 각 cell에 원자 궤도가 많이 포함되어 있으면 에너지마다 수행하는 Green's function 계산의 비용이 크다. 관심 에너지의 상태를 작은 cell 기저로 표현하고 onsite·hopping·접촉을 그 기저에 투영하면 반복 계산의 행렬 크기를 줄일 수 있다. 따라서 mode-space reduction의 목적은 작은 고유값 문제를 한 번 푸는 데 그치지 않고, 축소된 block을 반복적인 수송 계산에 활용하는 것이다.[1,2,3]

이 글은 이미 주어진 Hamiltonian에서 출발한다. 직교 atomic orbital (AO) 기저와 이웃 cell 결합을 기본으로 설명한 뒤, 비직교 기저를 사용하는 SIESTA형 행렬쌍으로 확장한다. [Model reduction fundamentals](fundamentals.md)의 상태·출력 구분, [Low-rank approximation](low-rank-approximation.md)의 표본 압축, [Projection methods](projection-methods.md)의 Galerkin 조건을 cell 수송 문제에 적용한다. [Wannierization](wannierization.md)이 Bloch 부분공간의 국소 표현을 만드는 과정이라면, 여기서는 cell block 크기를 줄이고 열린 소자의 관측량을 검증하는 데 초점을 둔다.

| 기호 | 의미와 크기 | 공통 문서와의 관계 |
| --- | --- | --- |
| $M,m$ | 원래·축소 cell 차원 | 한 cell에서 $V=U$, $r=m$ |
| $H_0,W$ | Onsite·이웃 cell hopping, $M\times M$ | $W$는 test basis가 아니다 |
| $U$ | 공통 cell 기저, $M\times m$ | Galerkin의 trial·test 공간이 같다 |
| $c_i,\xi_i$ | Cell $i$의 원래·축소 계수 | $c_i\simeq U\xi_i$ |
| $a,k$ | Cell 간격·파수 | $a$는 축소 좌표가 아니다 |
| $V$ | 전체 장치의 block 대각 기저 | 동일 cell이면 $V=I_N\otimes U$ |

계산 순서는 **실공간 block → 주기적 band → Bloch 표본 → 공통 $U$ → 축소 block → band 검증 → 열린 소자 검증**이다. 주기적 기준계는 기저를 설계하는 자료이며, 그 기준계의 정확도와 실제 장치의 정확도는 구별한다.[1,2,3]

## 1. Real-space cell block과 주기적 기준계

### (1) Onsite·hopping과 Bloch 문제

수송축을 따라 같은 cell이 간격 $a$로 반복된다고 하자. $H_0=H_0^\dagger$는 cell 내부 Hamiltonian이고, $W$는 행이 cell $i$, 열이 cell $i+1$인 hopping block이다. 직교 AO에서 에너지 $E$인 상태의 계수는 다음 실공간 방정식을 만족한다.[1,2,3]

$$
H_{ii}=H_0,\qquad H_{i,i+1}=W,\qquad H_{i+1,i}=W^\dagger.
$$

$$
W^\dagger c_{i-1}+H_0c_i+Wc_{i+1}=Ec_i.
$$

방정식 왼쪽의 세 항은 각각 이전 cell과의 결합, 현재 cell 내부의 Hamiltonian, 다음 cell과의 결합이 $i$번째 cell의 계수에 미치는 영향을 나타낸다. Bloch 형태 $c_i=e^{ikia}\psi_{nk}$를 대입하면 무한 chain을 한 cell의 문제로 바꿀 수 있다. $n$은 band 번호, $\psi_{nk}\in\mathbb C^M$는 **한 cell 안의 궤도 계수벡터**이다.[1,2,3]

$$
H(k)=H_0+We^{ika}+W^\dagger e^{-ika}.
$$

$$
H(k)\psi_{nk}=\varepsilon_n(k)\psi_{nk},\qquad
\psi_{nk}^\dagger\psi_{nk}=1.
$$

$H(k)$와 $\varepsilon_n(k)$의 단위는 에너지이고, $ka$는 무차원이다. 반대 방향 hopping에 dagger와 반대 위상이 함께 붙으므로 $H(k)$는 Hermitian이다. 이 식은 선택한 이웃 cell 모형에서는 정확하다. 원래 모형에 더 먼 cell 결합이 있으면 해당 Fourier 항을 포함하거나, 모든 유한 범위 결합이 이웃 block 안에 들어가도록 cell을 크게 묶어야 한다.[1,3]

### (2) 세 orbital chain

앞선 문서의 교육용 세 orbital 모형에 cell 간 결합을 추가한다. 실제 물질의 fitted parameter나 실험 결과가 아니며, 에너지는 eV, $a=1$은 임의 길이 단위이다.

$$
H_0=\begin{pmatrix}
0&-1&0.3\\-1&0.5&0.4\\0.3&0.4&4
\end{pmatrix}\ \mathrm{eV},\qquad S=I_3.
$$

$$
W=\operatorname{diag}(-0.30,-0.15,-0.05)\ \mathrm{eV}.
$$

이 예제의 $W$는 실수 대각행렬이므로 $H(k)=H_0+2W\cos(ka)$이다. 따라서 각 궤도의 onsite 에너지가 $k$에 따라 서로 다른 폭으로 움직인다. $H_0$에 궤도 간 혼합이 있으므로 그 변화는 고유벡터의 궤도 조성도 바꾼다. 이 결과는 위 행렬을 Bloch 식에 대입한 해석이며, 6절에서 직접 계산한다. 높은 세 번째 orbital의 에너지가 멀리 있어도 낮은 두 상태의 세 번째 성분이 정확히 0이라고 가정하지 않는다.

먼저 고립된 cell에서 에너지가 낮은 고유상태를 골라 전체 chain에 공통 기저로 적용할 수 있다. 그러나 그 선택이 $W$가 만드는 모든 $k$ 의존 혼합을 대표하는지는 다시 풀어 보아야 한다. 따라서 mode-space 기저를 구성할 때에는 서로 다른 파수의 Bloch 상태를 표본으로 모아, cell 사이 결합에 따른 상태의 변화를 반영한다.[1,2,3]

## 2. Energy window와 Bloch 표본

### (1) 관심 상태와 학습 범위

먼저 목표 energy window $\mathcal W=[E_{\min},E_{\max}]$를 정한다. 이는 모든 band를 재현하겠다는 요구를 관심 상태의 재현으로 제한한다. 소자에 적용할 때에는 접촉의 주입 에너지, 바이어스와 전위 변화로 이동하는 상태도 고려해야 한다. 기준계의 매우 좁은 구간만 맞춘 기저를 다른 동작 조건에 그대로 적용할 근거는 없다.[1,2,3]

$$
\mathcal B_{\mathcal W}(k)=\{n:\varepsilon_n(k)\in\mathcal W\}.
$$

$\mathcal B_{\mathcal W}(k)$는 해당 $k$에서 선택할 band 번호의 집합이다. Brillouin zone에 놓인 학습점 $k_l$마다 이 집합의 벡터를 수집한다. Valley나 band 극값 부근을 포함하되, 학습점 사이에서 나타나는 분산도 별도 격자로 검사한다. 몇 개 대표 파수의 일치만으로 전체 구간의 spurious branch를 배제할 수 없다는 점은 실제 mode-space 연구에서도 핵심 문제이다.[1,3]

이 글의 toy에서는 $\mathcal W=[-1.4,1.8]$ eV를 택하고 각 학습점의 낮은 두 상태를 모은다. 6절 코드는 이 구간의 두 band를 다루며, 세 번째 band 전체를 맞추려는 목표는 두지 않는다. 에너지 구간과 표본 수는 예제의 입력값이지 보편적인 권장값이 아니다.

### (2) 여러 파수와 하나의 mode의 한계

하나의 Bloch 벡터만으로 관심 상태 전체를 표현하기 어려운 이유는 두 가지이다. 같은 $k$에서도 서로 독립인 관심 상태가 둘이면 한 방향만으로 둘을 표현할 수 없다. 또한 같은 band라도 $k$가 변하면 cell 안의 궤도 조성이 달라질 수 있다. 여러 $k$에서 상태를 모으는 것은 이러한 방향 변화를 포착하려는 것이다. 특별한 분리 가능 모형에서는 적은 표본으로 충분할 수 있지만, 이를 일반 atomistic Hamiltonian의 성질로 가정하지 않는다.[1,2,3]

서로 다른 파수의 **전체 Bloch 파동함수**가 직교한다는 사실과, 여기서 모으는 $M$차원 cell 벡터들이 직교한다는 주장은 다르다. 전체 Bloch 상태의 내적에는 모든 cell의 위상합이 들어간다. 유한 주기 chain의 허용 파수에서 그 구조는 다음과 같다. $N_c$는 여기서 정규화에 사용하는 주기 cell 수이다.[2,4]

$$
\langle\Psi_{nk}|\Psi_{n'k'}\rangle
=\frac{1}{N_c}\sum_i e^{i(k'-k)ia}
\psi_{nk}^\dagger\psi_{n'k'}.
$$

$k\ne k'$에서 위상합이 0이어도 $\psi_{nk}^\dagger\psi_{n'k'}$가 0일 필요는 없다. 이 대입 결과 때문에 snapshot의 서로 다른 열이 거의 같은 cell 방향일 수 있다. $-\pi/a$와 $+\pi/a$는 같은 Brillouin-zone 경계점이며 독립 정보 두 개로 세지 않는다. Toy처럼 $H(k)=H(-k)$이면 다른 파수 표본도 같은 cell 부분공간을 줄 수 있다. 열을 많이 모았다는 사실보다 그 열들이 어떤 공간을 대표하는지가 중요하다.[1,2,5,6]

## 3. Reduced cell basis 구성

### (1) Snapshot SVD와 차원 선택

선택한 $p$개의 정규화된 cell 벡터를 열로 모은 행렬을 $X\in\mathbb C^{M\times p}$라 한다. 여기서 SVD로 먼저 압축하는 대상은 Hamiltonian 자체가 아니라 여러 파수에서 수집한 상태 벡터들이다. Singular value decomposition (SVD)으로 중복 방향을 정리하고 큰 singular value에 해당하는 왼쪽 벡터를 남긴다.[5,6]

$$
X=[\psi_{n_1k_1},\ldots,\psi_{n_pk_p}]
=U_s\Sigma R_s^\dagger.
$$

$$
U=(U_s)_{:,1:m},\qquad U^\dagger U=I_m.
$$

$U_s$는 왼쪽 singular vector, $R_s$는 표본 조합을 나타내는 오른쪽 singular vector의 행렬이고, $\Sigma$의 대각값 $\sigma_1\ge\sigma_2\ge\cdots\ge0$는 singular value이다. 이 구성이 proper orthogonal decomposition (POD)이다. 직교 내적과 동일한 열 가중치에서 주어진 차원 $m$의 기저 중 학습 상태 재구성의 제곱오차를 최소화한다.[5,6]

$$
\|X-UU^\dagger X\|_F^2=\sum_{j>m}\sigma_j^2.
$$

$$
\eta_m=\frac{\sum_{j>m}\sigma_j^2}{\sum_j\sigma_j^2}.
$$

$\|\cdot\|_F$는 Frobenius norm, $\eta_m$은 버린 학습 표본의 제곱 norm 비율이다. 두 양 모두 이 예제의 무차원 정규화된 상태에서 정의된다. 표본이 자주 등장하거나 큰 가중치를 받으면 목적함수에도 더 크게 반영된다. 따라서 $\eta_m$의 작음은 선택한 학습 자료에 대한 진술이다. Band 에너지, 새로운 전위에서의 파동함수, transmission의 최대 오차를 직접 최소화한 값은 아니다.[5,6]

POD의 첫 방향이 최저에너지 상태라는 보장도 없다. 이 목적함수에는 고유에너지의 낮고 높음이 들어 있지 않기 때문이다. 같은 가중치로 낮은 두 상태를 반복 수집하면 두 주요 singular value가 비슷할 수 있다. 그중 하나만 남기는 $m=1$ 계산을 “가장 낮은 band를 선택했다”고 해석하지 않는다. 6절의 예제가 이 차이를 수치로 보여 준다.[5,6]

### (2) 공통 기저와 cell 좌표

$U$의 각 열은 원래 cell AO들의 선형결합이다. 같은 cell의 원래 orbital을 $|\alpha,i\rangle$라 하면 $\mu$번째 축소 orbital은 다음처럼 정의된다. $\alpha=1,\ldots,M$, $\mu=1,\ldots,m$이다.[2,3]

$$
|u_\mu,i\rangle=\sum_{\alpha=1}^{M}|\alpha,i\rangle U_{\alpha\mu}.
$$

$$
c_i\simeq U\xi_i,\qquad \xi_i=U^\dagger c_i.
$$

첫 식은 상태를 $m$차원 부분공간으로 제한하는 근사이고, 두 번째 식은 주어진 상태의 직교 투영 좌표이다. 그 결과 복원되는 상태는 $UU^\dagger c_i$이다. 축소 기저 $U$의 각 열이 특정 band 또는 특정 파수 $k$의 Bloch 상태와 일대일로 대응할 필요는 없다. 여러 파수에서 수집한 표본으로 기저를 구성했지만, 최종 $U$는 **$k$와 무관하게 모든 cell에 적용하는 공통 기저**이다.[1,2,3]

예제에서는 네 학습 파수에서 두 상태씩 수집하므로 $X$는 $3\times8$이다. $m=2$이면 $U$는 $3\times2$, 축소 onsite·hopping은 각각 $2\times2$이다. 세 cell 장치의 전체 기저 $V=I_3\otimes U$는 $9\times6$이다. 이는 단순한 좌표 이름 변경과 다르다. $m=M$인 square unitary 기저는 정보를 보존하지만, $m<M$이면 버린 방향의 동역학이 없어지므로 결과를 검증해야 한다.[3,7]

## 4. Onsite·hopping block의 projection

### (1) Galerkin 조건과 축소 band

각 cell에 공통으로 적용할 기저 $U$를 정한 뒤에는 cell 내부의 onsite block과 이웃 cell 사이의 hopping block을 모두 이 기저로 투영한다. 축소 상태의 계수를 $y\in\mathbb C^m$, 에너지를 $\theta$라 하면 전체 잔차는 $\rho=H(k)Uy-\theta Uy$이다. Galerkin 조건 $U^\dagger\rho=0$은 다음 작은 고유값 문제를 준다.[8,9]

$$
h_0=U^\dagger H_0U,\qquad w=U^\dagger WU.
$$

$$
h(k)=h_0+we^{ika}+w^\dagger e^{-ika}=U^\dagger H(k)U.
$$

$$
h(k)y=\theta y,\qquad y^\dagger y=1.
$$

$h_0,w,h(k)$는 $m\times m$의 에너지 행렬이다. 마지막 Fourier 등식은 모든 $k$에 같은 $U$를 사용한다는 조건에서 성립한다. $k$마다 독립적으로 고유벡터 몇 개를 골라 대각행렬만 저장하는 것과는 다르다. 여기서는 cell 사이 결합 $w$가 남아 있어 실공간 소자 방정식을 계속 구성할 수 있다.[1,2,3]

$$
w^\dagger\xi_{i-1}+h_0\xi_i+w\xi_{i+1}=E\xi_i.
$$

축소한 방정식은 원래 chain의 cell 간 연결 구조를 유지하면서, 각 cell에서 풀어야 하는 미지수의 수만 $M$개에서 $m$개로 줄인다. 작은 고유값 문제의 잔차가 0이어도 원래 공간의 $\rho$가 0일 필요는 없다. Galerkin 조건은 원래 방정식의 잔차가 선택한 기저의 열공간에 직교하도록 요구할 뿐, 축소 과정에서 제외한 자유도의 방정식까지 만족시키지는 않는다.[8,9]

### (2) 장치 전위와 cell별 기저

유한 장치의 cell $i$에 더해지는 전위 에너지 행렬을 $\Delta_i$라 쓰면 $H_{ii}=H_0+\Delta_i$이다. 이는 전압 자체가 아니라 입력 Hamiltonian과 같은 부호·단위의 에너지이다. 동일한 $U$를 쓰는 기본 장치는 다음 block으로 구성한다.[3,7]

$$
h_{ii}=h_0+U^\dagger\Delta_iU,\qquad h_{i,i+1}=w.
$$

Cell 전체에 일정한 전위 $\Delta_i=d_iI_M$는 $d_iI_m$으로 투영된다. 반면 orbital마다 다른 전위는 일반적으로 mode 사이의 비대각 결합을 만든다. 이 결합은 우선 모두 유지한다. 나중에 결합을 버리는 uncoupled 근사는 기저를 줄이는 일과 다른 단계이다.[7,10]

재료나 단면이 달라지면 각 cell에 $U_i\in\mathbb C^{M_i\times m_i}$를 둘 수 있다. 경계 결합은 왼쪽과 오른쪽의 서로 다른 기저를 함께 사용한다.[3,7]

$$
h_{i,i+1}=U_i^\dagger H_{i,i+1}U_{i+1}
\in\mathbb C^{m_i\times m_{i+1}}.
$$

단, 불규칙 cell을 임의로 무한 반복한 band가 실제 접합을 대표한다고 가정해서는 안 된다. 접합·결함을 포함한 supercell이나 적절한 상태 자료로 해당 영역의 공간을 구성하고, cell 사이의 mapping까지 검증해야 한다. Shin의 hetero-structure 구성은 이 문제를 block 기저와 supercell 자료로 다룬 사례이다.[3,7]

## 5. Reduced band와 spurious branch

### (1) 표본 밖 band와 상태 수

축소 Hamiltonian의 고유값은 수학적으로 유효한 Ritz value이다. 그러나 관심 energy window에서 원래 물리적 band에 대응하지 않는 분산 곡선이 나타날 수 있다. 이를 mode-space 문헌에서는 **spurious branch** 또는 unphysical band라 부른다. 이는 Hermiticity가 깨졌다는 뜻도, eigensolver가 수치적으로 실패했다는 뜻도 아니다.[1,2,3]

고정 $k$에서 원래·축소 고유값을 오름차순으로 정렬하면 Hermitian Rayleigh–Ritz의 상한은 다음과 같다.[8,9]

$$
\varepsilon_j(k)\le\widetilde\varepsilon_j(k),\qquad j=1,\ldots,m.
$$

이 부등식은 원래 Hamiltonian과 축소 Hamiltonian의 고유값을 같은 순번으로 정렬했을 때 성립하는 관계이다. 내부 energy window에 들어오는 branch의 개수나 각 branch의 정확한 위치가 맞는다고 말하지 않는다. 따라서 “변분 상한이 있으므로 가짜 branch가 없다”는 결론은 성립하지 않는다. Mode-space 논문에서 band 가장자리 구간의 정확도를 별도로 다루는 이유와 Hermitian 행렬의 Ritz 이론은 모순되지 않는다.[1,2,8,9]

학습에 쓰지 않은 조밀한 $k$ 격자에서 다음을 비교한다. 단순히 원래 관심 상태마다 가까운 축소 에너지 하나를 찾는 것만으로 끝내면, 남아 있는 추가 branch를 놓칠 수 있다.[1,3]

| 검증 대상 | 비교 내용 | 드러나는 문제 |
| --- | --- | --- |
| 관심 band 에너지 | 같은 $k$의 위치·극값·분산 | 잘못된 에너지와 곡률 |
| 구간 안의 상태 수 | 원래·축소 branch의 개수 | 누락 또는 추가 branch |
| 복원 상태 | 원래 방정식의 전체 잔차 | 축소 해의 원공간 부정합 |
| 표본 밖 상태 | 기저 밖에 남는 norm | 학습 범위의 부족 |

Band crossing이나 축퇴가 있으면 단순한 순번 대응만으로 상태의 동일성을 판단하기 어렵다. 그때는 관심 부분공간과 상태 수를 함께 확인한다. 아래 toy는 낮은 두 band를 순번으로 비교하지만, 이 방법을 임의의 얽힌 band 추적 규칙으로 일반화하지 않는다.[8,9]

### (2) 잔차와 기저 보강

정규화된 원래 상태 $\psi_{nk}$의 표현 오차와 축소 고유상태 $y_{\mu k}$의 전체 잔차를 분리해 기록한다. 전자는 무차원이고 후자는 에너지 단위이다.[5,6,8,9]

$$
r^{\mathrm{rep}}_{nk}=\|(I_M-UU^\dagger)\psi_{nk}\|_2.
$$

$$
\rho_{\mu k}=H(k)Uy_{\mu k}
-\widetilde\varepsilon_\mu(k)Uy_{\mu k}.
$$

표현 오차에는 원래 상태가 필요하다. 잔차에는 원래 고유벡터가 없어도 되지만 원차원 Hamiltonian의 작용이 필요하다. 잔차가 작으면 축소 고유값이 원래 문제의 어떤 고유값에 가깝다는 근거가 되지만, 그것만으로 그 고유값이 목표 band에 속하는지 또는 다른 관심 branch가 누락되었는지 판단할 수는 없다.[8,9]

문제가 있는 파수의 상태를 더 수집하거나 현재 공간 밖의 잔차 방향을 보강 후보로 쓸 수 있다. 직교 기저에서 버린 공간의 projector는 다음과 같다.[1,2,3,8]

$$
Q_\perp=I_M-UU^\dagger.
$$

보강 벡터를 $Q_\perp$로 정리하여 $U$에 추가하고 다시 직교화한 뒤 $h_0,w$를 새로 계산한다. 원래 공간에 이미 정확히 포함된 고유상태는 더 큰 공간에도 남지만, 추가 벡터가 모든 표본 밖 문제를 해결한다고 보장할 수는 없다. 문헌의 spurious-state 제거는 목적함수와 상태 수 검사를 사용하는 기저 최적화이며, band 그림에서 불편한 곡선을 삭제하는 작업이 아니다.[1,2,3]

## 6. 1D chain의 NumPy 검산

### (1) 학습·검증 조건과 코드

네 학습점은 $ka=(-\pi,-\pi/2,0,\pi/2)$이고, 각 점의 낮은 두 상태를 동일 가중치로 모은다. $+\pi$를 다시 넣지 않지만 이 실수 toy에서는 $\pm\pi/2$의 자료가 중복 방향을 준다. 이는 명시적으로 택한 표본 가중치이며 독립 방향 여덟 개를 의미하지 않는다. 평균을 빼지 않고 상태의 원점을 유지한다.

검증에는 학습점과 겹치지 않는 800개 중간 격자점을 쓴다. $m=1,2,3$에서 같은 SVD의 앞 열을 차례로 남긴다. Band·잔차 최대값은 $\min(m,2)$개 축소 상태에 대해 계산하고, 표현 오차는 항상 원래 낮은 **두** 상태를 대상으로 한다. $m=1$의 band 오차는 최저 순번 하나의 비교일 뿐 두 band 검증이 아니다.

다음은 Python 3와 NumPy만 사용하는 하나의 완결 코드이다. 앞부분은 band와 기저를 검증하고, 뒷부분은 7절에서 해석할 인공 접촉의 수송을 계산한다. 코드의 $q$는 무차원 $ka$이다. Toy가 작아서 전체 대각화·조밀 선형해법을 쓰며 대형 소자의 성능 구현은 아니다.

```python
import numpy as np

# Educational orthogonal model; energies in eV, a = 1 length unit.
H0 = np.array([[0., -1., .3], [-1., .5, .4], [.3, .4, 4.]])
W = np.diag([-.30, -.15, -.05])
def bloch(q):  # q = k*a
    return H0 + W * np.exp(1j*q) + W.T * np.exp(-1j*q)

# Distinct points on the BZ circle; this real toy has H(q) = H(-q).
q_train = np.array([-np.pi, -np.pi/2, 0., np.pi/2])
X = np.column_stack([np.linalg.eigh(bloch(q))[1][:, :2]
                     for q in q_train])
Us, singular, _ = np.linalg.svd(X, full_matrices=False)
q_test = -np.pi + (np.arange(800) + .5) * (2*np.pi/800)
assert min(abs(q_test[:, None] - q_train).ravel()) > 1e-6
print('singular values', singular)
for m in (1, 2, 3):
    U = Us[:, :m]
    count = min(m, 2)
    band_error = residual = reconstruction = 0.
    for q in q_test:
        H = bloch(q)
        energies, states = np.linalg.eigh(H)
        reduced, coeff = np.linalg.eigh(U.conj().T @ H @ U)
        lifted = U @ coeff[:, :count]
        band_error = max(band_error, np.max(abs(reduced[:count]-energies[:count])))
        residual = max(residual, np.max(np.linalg.norm(
            H @ lifted - lifted * reduced[:count], axis=0)))
        reconstruction = max(reconstruction, np.max(np.linalg.norm(
            states[:, :2] - U @ (U.conj().T @ states[:, :2]), axis=0)))
    tail = np.sum(singular[m:]**2) / np.sum(singular**2)
    print(f'm={m}: tail={tail:.8e}, band={band_error:.8e}, '
          f'residual={residual:.8e}, representation={reconstruction:.8e}')

# Finite three-cell device with artificial wide-band contacts.
N = 3
D0 = (np.kron(np.eye(N), H0) + np.kron(np.eye(N, k=1), W)
      + np.kron(np.eye(N, k=-1), W.T))
left = np.zeros_like(D0)
right = np.zeros_like(D0)
left[:3, :3] = .2 * np.eye(3)
right[-3:, -3:] = .2 * np.eye(3)
U = Us[:, :2]
V = np.kron(np.eye(N), U)
left_r = V.conj().T @ left @ V
right_r = V.conj().T @ right @ V

def transmission(E, H, gamma_l, gamma_r):
    # Sigma^R = -i*Gamma/2, eta=0; contact broadening makes these solves regular.
    G = np.linalg.solve(E*np.eye(len(H)) - H + .5j*(gamma_l+gamma_r),
                        np.eye(len(H)))
    return np.trace(gamma_l @ G @ gamma_r @ G.conj().T).real

energies = np.linspace(-1.4, 1.7, 621)
for shift in (0., -3.):
    D = D0.copy()
    D[5, 5] += shift  # third orbital of middle cell, zero-based index 5
    Dr = V.conj().T @ D @ V
    full = np.array([transmission(E, D, left, right) for E in energies])
    small = np.array([transmission(E, Dr, left_r, right_r) for E in energies])
    j = np.argmax(abs(small-full))
    print(f'shift={shift:.1f}: E={energies[j]:.3f}, full={full[j]:.8f}, '
          f'reduced={small[j]:.8f}, max_error={abs(small[j]-full[j]):.8f}')
    # A square unitary basis must recover the entire finite device calculation.
    V3 = np.kron(np.eye(N), Us)
    for E in (-1., .935, 1.4):
        exact = transmission(E, D, left, right)
        rotated = transmission(E, V3.conj().T@D@V3,
                               V3.conj().T@left@V3, V3.conj().T@right@V3)
        assert abs(exact-rotated) < 1e-11
```

### (2) 차원별 오차의 해석

실행한 singular value는 약 $(1.99999997,1.99997899,0.00917430)$이다. 다음은 코드의 검증 격자 최대값을 반올림한 결과이다. $m=3$은 전체 공간이므로 잔차와 오차가 부동소수점 반올림 수준으로 내려가는 확인용 계산이다.

| $m$ | 학습 꼬리 $\eta_m$ | Band 오차 (eV) | 전체 잔차 (eV) | 두 상태 표현 오차 |
| --- | --- | --- | --- | --- |
| 1 | $5.0000\times10^{-1}$ | $2.1831$; 한 순번만 비교 | $1.8249\times10^{-1}$ | $1.0000$ |
| 2 | $1.0521\times10^{-5}$ | $2.0269\times10^{-4}$ | $3.2686\times10^{-2}$ | $6.6866\times10^{-3}$ |
| 3 | $0$ | $2.3\times10^{-15}$ 미만 | $2.2\times10^{-15}$ 미만 | $1.0\times10^{-15}$ 미만 |

$m=1$의 작은 문제는 하나의 Ritz value만 갖는다. 첫 POD 방향이 최저 band를 우선하지 않으므로 최저 에너지와의 오차가 크다. 거의 1인 두 상태 표현 오차는 적어도 하나의 관심 상태가 빠진다는 사실도 보여 준다. 따라서 그 행을 “band 하나로 수렴했다”는 결과로 읽으면 안 된다.

$m=2$에서는 학습 꼬리와 시험 상태의 표현 오차가 작아지고 낮은 두 band도 잘 맞는다. 그러나 에너지 오차와 잔차는 서로 다른 수치이며, $\eta_m$은 둘 중 어느 것의 상대 오차도 아니다. 이 toy에서 spurious branch의 일반적인 발생·제거 알고리즘을 입증한 것도 아니다. 큰 원자 모형에서는 목표 구간의 상태 수와 추가 branch 검사가 계속 필요하다.[1,3,5,6,8,9]

## 7. NEGF와 transmission 정확도

### (1) Lead·device의 일관된 기저

장치 Hamiltonian을 $H_D$, 접촉 $\alpha=L,R$의 retarded self-energy를 $\Sigma_\alpha^R$라 하자. 이미 원공간 접촉을 계산했다면 $H_D$와 동일한 장치 기저 $V$로 투영하는 경로가 있다. 접촉은 경계 orbital에 작용하지만 전체 장치 행렬 안에 그 위치를 정확히 배치해야 한다.[7,11,12]

$$
H_r=V^\dagger H_DV,\qquad
\Sigma_{\alpha,r}^R=V^\dagger\Sigma_\alpha^RV.
$$

Lead Hamiltonian과 결합을 먼저 줄인 뒤 surface Green's function을 재계산하는 경로도 있다. **두 경로는 일반적으로 같지 않다.** 직교 기저에서 장치–lead 결합을 $\tau$, 분리된 원래 lead의 surface Green's function을 $g_L^R$라 하면 첫 경로는 $V^\dagger\tau g_L^R\tau^\dagger V$이다. Lead 경계 기저를 $U_L$, 축소 lead에서 재계산한 함수를 $g_{L,r}^R$라 하면 두 번째는 다음과 같다.[7,11,12]

$$
\Sigma_{L,r}^{R,\mathrm{recompute}}
=(V^\dagger\tau U_L)g_{L,r}^R(U_L^\dagger\tau^\dagger V).
$$

두 경로의 차이는 원래 lead에서 계산한 $g_L^R$를 그대로 사용하는지, 축소한 lead에서 다시 계산한 $g_{L,r}^R$를 원래 공간으로 복원한 $U_Lg_{L,r}^RU_L^\dagger$를 사용하는지에 있다. 역행렬을 포함하는 lead 제거와 부분공간 투영은 일반적으로 교환되지 않는다. 버린 lead 상태를 단순히 생략하는 것과 그 영향을 self-energy로 남기는 것은 다르며, 이 대수적 차이는 [Downfolding and effective Hamiltonians](downfolding.md)의 제거 항과 같다. 어느 경로를 쓰든 원래 접촉 조건과의 일치를 별도로 확인한다.[7,11,12]

직교 기본 모형에서 축소 장치의 retarded Green's function과 broadening은 다음과 같다. $z=E+i0^+$이고 $I$의 크기는 전체 축소 장치 차원이다. 여기서는 위상 결맞음 ballistic 수송이며 추가 산란 self-energy가 없다.[11,12,13]

$$
G_r^R(E)=[zI-H_r-\Sigma_{L,r}^R(E)-\Sigma_{R,r}^R(E)]^{-1}.
$$

$$
\Gamma_{\alpha,r}=i(\Sigma_{\alpha,r}^R-\Sigma_{\alpha,r}^{R\dagger}),
\qquad G_r^A=G_r^{R\dagger}.
$$

$\Gamma$는 에너지 단위이며 접촉으로 인한 broadening을 나타낸다. 본문은 위 정의를 사용하므로 $\Gamma$에 별도의 $1/2$를 붙이지 않는다. $H,S,\Sigma,\Gamma$와 관측 연산자를 서로 다른 기저로 섞지 않는 것이 수송 계산의 기본 조건이다.[11,12,13]

### (2) Band와 transmission의 별도 검증

동일한 접촉·장치 전위에서 원래 계산 $T_f$와 축소 계산 $T_r$를 비교한다. 무차원 transmission은 다음 trace로 계산한다.[4,11,13]

$$
T_r(E)=\operatorname{Tr}[\Gamma_{L,r}G_r^R\Gamma_{R,r}G_r^A].
$$

$$
\Delta_T=\max_{E_l\in\mathcal E}|T_r(E_l)-T_f(E_l)|.
$$

$\mathcal E$는 명시적으로 택한 비교 에너지 격자이다. $\Delta_T$는 이 글의 최대 절대 오차 지표이며 보편적인 허용 기준이 아니다. 전류 적분에 중요한 구간, 공명 위치, 작은 터널링 신호는 별도로 확인한다. $T_f\simeq0$에서 상대 오차만 쓰면 지표가 불안정하므로 절대 오차와 곡선의 형태를 함께 보는 편이 목적에 맞다.[1,3,11]

6절 코드의 수송 부분은 $N=3$인 유한 chain에 **인공적인 wide-band limit (WBL) 접촉**을 붙인 것이다. 각 경계 cell의 세 orbital에 $\Gamma_L=0.2I_3$ eV와 $\Gamma_R=0.2I_3$ eV를 각각 놓고, 나머지 원소는 0으로 한다. 에너지 의존 broadening을 상수로 두고 실수 준위 이동을 버린 다음 식을 모형의 입력으로 택한다.[13,14]

$$
\Sigma_\alpha^R=-\frac{i}{2}\Gamma_\alpha.
$$

이 접촉은 앞서 정의한 주기적 chain의 실제 semi-infinite lead self-energy가 아니다. 넓고 평탄한 reservoir를 이상화한 접촉을 사용하여 **같은 외부 조건에서 기저 축소만 비교**하는 교육 예제이다. WBL을 실제 재료에 적용할 수 있는지는 전극의 에너지 의존성을 따로 검토해야 한다.[13,14]

두 장치를 비교한다. 첫 장치는 모든 $\Delta_i=0$이고, 두 번째 장치는 중앙 cell의 세 번째 onsite만 $-3$ eV만큼 이동시킨다. 양쪽 계산에 같은 장치 전위와 같은 접촉을 넣고, $m=2$의 $V$로 장치와 $\Gamma$를 모두 투영한다. 학습 기저는 두 장치에서 동일하다. $[-1.4,1.7]$ eV의 621개 격자점에서 얻은 결과는 다음과 같다.

| 중앙 세 번째 onsite 변화 | 최대 오차의 $E$ (eV) | $T_f$ | $T_r$ | $\Delta_T$ |
| --- | --- | --- | --- | --- |
| $0$ eV | $-1.190$ | $0.70829874$ | $0.70659587$ | $0.00170286$ |
| $-3$ eV | $0.935$ | $0.99527658$ | $0.28610351$ | $0.70917306$ |

주기적 **학습 기준계**는 두 경우 모두 같으므로 6절의 작은 band 오차도 그대로이다. 그러나 두 번째 장치에서는 높은 orbital을 관심 구간으로 크게 이동시켰고, 원래 기저가 대표하지 못한 혼합이 중요해진다. 이는 위 toy의 계산 결과이며 “작은 band 오차에는 항상 이 정도의 수송 오차가 따른다”는 법칙이 아니다. 학습에 없던 장치 조건까지 기준 band 검증으로 인증할 수 없다는 반례이다.

코드는 $m=3$의 square unitary 기저로 장치와 접촉을 모두 바꾸었을 때 선택한 세 에너지의 $T$가 $10^{-11}$ 이내에서 복원되는지도 검사한다. 이 확인은 투영 위치나 contact mapping의 구현 실수와, $m=2$에서 공간을 버려 생긴 오차를 구별하는 데 사용한다. 실제 소자에서는 바이어스별 전위, 접촉 주입 상태, energy window와 mode 수를 바꾸어 필요한 관측량의 수렴을 확인해야 한다.[1,3,7]

### (3) Basis mode와 transmission eigenchannel

$U$의 각 열은 cell 내부 상태를 표현하는 basis mode이다. 반면 transmission eigenchannel은 주어진 에너지에서 전극과 장치를 포함한 산란 문제를 푼 뒤 정의하므로, basis mode와 구별해야 한다. Flux-normalized 입사·출사 채널 사이 transmission amplitude 행렬을 $t(E)$라 하면 $t^\dagger t$의 고유값 $\tau_\nu(E)$가 각 eigenchannel의 전달 확률이다.[4,11]

$$
T(E)=\operatorname{Tr}[t^\dagger(E)t(E)]=\sum_\nu\tau_\nu(E).
$$

따라서 cell mode 수 $m$, 주어진 에너지의 lead 전파 채널 수, 실제로 큰 $\tau_\nu$를 갖는 eigenchannel 수는 같은 개수가 아니다. $U$의 열을 “각각 transmission 하나”로 읽지 않는다. 기저에는 상태와 결합을 표현하는 방향이 포함되고, eigenchannel은 접촉과 장치의 산란을 반영한 에너지별 조합이다.[2,4,11]

## 8. Coupled mode와 비직교 basis

### (1) CMS·UMS와 산란

Coupled mode space (CMS)는 남긴 mode 사이의 결합을 유지한다. Uncoupled mode space (UMS)는 mode 사이 결합을 추가로 무시하여 작은 독립 문제로 나눈다. Mode를 묶은 그룹 사이 결합만 버리는 구성도 있다. 완전한 unitary 기저변환, mode 수의 절단, mode 결합의 삭제는 서로 다른 연산이다.[7,10]

| 단계 | 유지하는 정보 | 추가 검증 |
| --- | --- | --- |
| 전체 unitary 변환 | 모든 차원과 결합 | 좌표변환의 일관성 |
| CMS의 차원 절단 | 선택한 공간 내부의 모든 결합 | 원공간 band·수송 비교 |
| UMS 또는 그룹 분리 | 정한 mode 내부·그룹 내부 결합 | 버린 결합의 영향 |

전위나 형상이 수송축을 따라 급격히 변하거나 mode 혼합이 강하면 UMS의 추가 근사가 중요해질 수 있다. 특정 소자에서 결합을 버려도 정확했다는 결과를 다른 모형의 정확도 보장으로 옮기지 않는다. 먼저 CMS와 비교하고, CMS 자체도 원공간과 비교한다.[7,10]

전자–포논 산란을 넣는 경우에는 상호작용과 산란 self-energy도 같은 기저에서 구성해야 한다. 산란이 다른 mode와 에너지를 연결하므로 ballistic $T(E)$의 일치가 산란 전류의 정확도를 보장하지 않는다. 실제 구현에서는 mode-space 변환된 산란 항의 근사와 계산 비용을 따로 다룬다.[7,15]

### (2) Cell overlap과 비직교 Bloch 문제

비직교 AO에서는 전체 overlap $S$가 양의 정부호인 행렬쌍 $Hc=ESc$를 사용한다. Cell onsite overlap을 $S_0$, $i$에서 $i+1$로 향하는 overlap block을 $S_1$이라 하면 Bloch 문제는 다음과 같다. $S$와 그 block은 무차원이다.[3,12,16]

$$
S(k)=S_0+S_1e^{ika}+S_1^\dagger e^{-ika}.
$$

$$
H(k)\psi_{nk}=\varepsilon_n(k)S(k)\psi_{nk},\qquad
\psi_{nk}^\dagger S(k)\psi_{nk}=1.
$$

서로 다른 $k$의 벡터를 모을 때에는 그 정규화에 사용한 $S(k)$와 cell 기저를 압축하는 내적을 구별한다. 고정 $S_0$를 양의 정부호 cell metric으로 선택한다면 $S_0=L^\dagger L$로 분해하고 $LX$를 SVD한 뒤 $U=L^{-1}\widehat U_s$로 되돌릴 수 있다. 여기서 $\widehat U_s$는 남길 왼쪽 singular vector들이다. 이 선택은 $S_0$ 내적에서 표본을 압축하는 절차이며, $k$마다 다른 $S(k)$ norm을 하나의 동일한 POD 목적함수로 자동 변환한 것은 아니다.[3,5,6]

$$
U^\dagger S_0U=I_m,\qquad
s_0=U^\dagger S_0U,\qquad s_1=U^\dagger S_1U.
$$

$$
s(k)=s_0+s_1e^{ika}+s_1^\dagger e^{-ika},\qquad
h(k)y=\theta s(k)y.
$$

$U^\dagger S_0U=I_m$로 만들었어도 $s_1$이 일반적으로 남는다. 따라서 고정 cell 기저 하나로 모든 $s(k)=I_m$이 되었다고 둘 수 없다. Euclidean 직교화 $U^\dagger U=I_m$만 한 경우에는 $s_0=I_m$조차 보장하지 않는다. 이 결론은 위 Fourier 식에 투영을 대입하면 바로 확인된다.[3,12]

### (3) 조립된 행렬과 복소 에너지의 접촉

SIESTA형 입력에서 $H$가 이미 AO 사이의 Hamiltonian 행렬 원소이면, 축소 행렬은 $H_r=V^\dagger HV$, $S_r=V^\dagger SV$이다. $V^\dagger SHV$처럼 overlap을 추가하지 않는다. 원래 행렬쌍을 왼쪽에서 $V^\dagger$로 투영하는 것과, 계수 연산자 $S^{-1}H$에 $S$ 내적의 Galerkin 조건을 적용하는 것은 같은 결과를 준다.[3,8,12]

$$
G_r^R(E)=[zS_r-H_r-\Sigma_{L,r}^R(z)-\Sigma_{R,r}^R(z)]^{-1}.
$$

비직교 접촉에서도 hopping만 변환해서는 충분하지 않다. 장치 $D$와 lead $L$ 사이의 block을 $K_{DL}(z)=zS_{DL}-H_{DL}$로 정의하면, 분리된 lead의 surface Green's function $g_L(z)$를 통한 self-energy는 다음 형태이다.[12,16]

$$
\Sigma_L(z)=K_{DL}(z)g_L(z)K_{LD}(z).
$$

두 coupling block 모두 **같은** $z$에서 평가한다. Hermitian $H,S$여도 복소 $z$에서는 $K_{LD}(z)\ne K_{DL}(z)^\dagger$이다. Dagger는 $z$도 복소켤레로 바꾸기 때문이다. $z=E+i\eta$를 쓰는 코드에서 한쪽 coupling을 무조건 다른 쪽의 dagger로 만들면 이 차이를 놓친다. 이 식을 투영할 때에도 onsite·hopping overlap, 경계 coupling, self-energy의 배치를 같은 기저로 맞춘다.[12,16]

## 9. 계산 비용과 적용 한계

Mode-space reduction은 cell block의 행렬 차원을 줄여, 여러 에너지 지점이나 서로 다른 장치 조건에서 반복하는 계산 비용을 절감하는 데 목적이 있다. Recursive Green's function (RGF)의 조밀 block 연산을 같은 $N$개 cell 분할에서 비교하면 대표적인 비용은 다음과 같다.[1,7,11]

$$
C_f\sim\mathcal O(NM^3),\qquad C_r\sim\mathcal O(Nm^3).
$$

$$
\text{같은 수의 조밀 block 저장량:}\qquad
\mathcal O(NM^2)\longrightarrow\mathcal O(Nm^2).
$$

이는 전체 벽시계 시간의 측정값이 아니다. 원래 행렬의 희소성, lead 해법, 하드웨어와 병렬화가 달라지면 실제 이득도 달라진다. RGF는 수송축을 따라 block을 소거하는 해법이고, mode-space는 그 block의 내부 차원을 줄이므로 둘은 함께 사용할 수 있다.[1,7,11]

| 비용 단계 | 수행하는 작업 | 원래 차원의 의존성 |
| --- | --- | --- |
| Offline 구성 | Bloch 표본, SVD, 기저 보강 | 원차원 고유상태 계산 필요 |
| 행렬 준비 | $H_0,W,\Delta,S,\Sigma$의 투영 | 투영·조립 방식에 따라 남음 |
| 반복 NEGF | 에너지별 작은 선형계와 trace | 적은 $m$의 이득이 누적됨 |
| 검증·복원 | 전체 잔차, 상태 복원, 기준 계산 | $M$ 의존 작업이 다시 필요 |

준비 시간 $C_{\mathrm{off}}$, 원래·축소 반복 계산 한 회의 비용 $C_{\mathrm{full}}$, $C_{\mathrm{red}}$, 재사용 횟수 $N_{\mathrm{call}}$을 정의하면, 이득의 최소 조건을 다음 비용 장부로 표현할 수 있다. 추가 조립·검증 비용은 해당 항에 포함해야 한다.[1,5]

$$
C_{\mathrm{off}}+N_{\mathrm{call}}C_{\mathrm{red}}
<N_{\mathrm{call}}C_{\mathrm{full}}.
$$

한 번의 작은 문제에서는 기저 준비가 더 비쌀 수 있다. Energy window를 넓히거나 공간 변화가 강해 $m$이 커지면 반복 계산의 절감도 작아진다. 전체 잔차를 모든 에너지에서 원공간으로 계산하면 검증 비용이 커지므로, 어떤 조건과 격자에서 검사했는지도 결과와 함께 보고한다.[1,3,5]

고정 Hamiltonian의 band나 transmission을 맞춘 것만으로 전하, density functional theory (DFT)의 self-consistent field (SCF) 갱신, 힘까지 검증한 것은 아니다. 밀도 재구성과 비평형 점유는 더 넓은 에너지 범위·기저 정보를 요구할 수 있고, 갱신된 전위가 훈련 범위를 벗어날 수도 있다. 여기서의 검증 대상은 명시한 행렬과 관측량이며, 전하·SCF·힘을 계산하려면 그 출력과 일관된 연산자 및 수렴 검사를 별도로 수행해야 한다.[1,3,12,16]

## 10. 요약

- Real-space $H_0,W$로 주기적 $H(k)$를 구성하고, 관심 energy window의 여러 Bloch cell 벡터를 모아 공통 $U$를 만든다.
- SVD/POD의 작은 꼬리는 학습 표본의 표현 정확도이다. Band·전체 잔차·상태 수·표본 밖 정확도를 따로 확인한다.
- 동일한 $U$로 onsite와 hopping을 투영하면 연결 구조를 유지하면서 cell 차원을 줄인다. Spurious branch 검사는 Ritz 상한과 별개의 요구이다.
- 장치·접촉을 같은 기저로 구성하고 transmission을 원공간과 비교한다. Basis mode는 transmission eigenchannel과 다르다.
- CMS의 차원 절단, UMS의 결합 삭제, 비직교 overlap 처리는 구별한다. 실제 계산 이득은 준비·검증 비용과 반복 사용 범위에 달려 있다.

## 11. 참고문헌

1. J. Z. Huang, H. Ilatikhameneh, M. Povolotskyi, and G. Klimeck, “Robust Mode Space Approach for Atomistic Modeling of Realistically Large Nanowire Transistors,” *Journal of Applied Physics* **123**, 044303 (2018). [DOI: 10.1063/1.5010238](https://doi.org/10.1063/1.5010238). [Full text](https://arxiv.org/html/1710.08064). §§I–IV.
2. G. Mil’nikov, N. Mori, and Y. Kamakura, “Low-dimensional Quantum Transport Models in Atomistic Device Simulations,” *2011 International Conference on Simulation of Semiconductor Processes and Devices (SISPAD)*, 315–318 (2011). [DOI: 10.1109/SISPAD.2011.6035033](https://doi.org/10.1109/SISPAD.2011.6035033). [Full text](https://in4.iue.tuwien.ac.at/pdfs/sispad2011/pdf/11-5.pdf). Eqs. (1)–(3), p. 316의 basis 구성과 spurious branch 논의.
3. M. Shin, “Hetero-structure mode space method for efficient device simulations,” *Journal of Applied Physics* **130**, 104303 (2021). [DOI: 10.1063/5.0064314](https://doi.org/10.1063/5.0064314). [Full text](https://arxiv.org/html/2107.10511). §§III–V, Eqs. (2)–(8).
4. M. Paulsson and M. Brandbyge, “Transmission eigenchannels from nonequilibrium Green’s functions,” *Physical Review B* **76**, 115117 (2007). [DOI: 10.1103/PhysRevB.76.115117](https://doi.org/10.1103/PhysRevB.76.115117). [Full text](https://arxiv.org/pdf/cond-mat/0702295). §II, Eqs. (1)–(5).
5. P. Benner, S. Gugercin, and K. Willcox, “A Survey of Projection-Based Model Reduction Methods for Parametric Dynamical Systems,” *SIAM Review* **57**(4), 483–531 (2015). [DOI: 10.1137/130932715](https://doi.org/10.1137/130932715). [Full text](https://kiwi.oden.utexas.edu/papers/Parametric-model-reduction-survey-Benner-Gugercin-Willcox.pdf). §§2, 3.3.1, Eqs. (3.17)–(3.18).
6. B. Haasdonk, “Reduced Basis Methods for Parametrized PDEs—A Tutorial Introduction for Stationary and Instationary Problems,” in *Model Reduction and Approximation: Theory and Algorithms*, 65–136 (SIAM, 2017). [DOI: 10.1137/1.9781611974829.ch2](https://doi.org/10.1137/1.9781611974829.ch2). [Author preprint](https://pnp.mathematik.uni-stuttgart.de/ians/haasdonk/data/oberwolfach2014/RBtutorial.pdf). Proposition 3.18–3.19, Eq. (3.12); preprint 번호.
7. R. Grassi, A. Gnudi, I. Imperiale, E. Gnani, S. Reggiani, and G. Baccarani, “Mode space approach for tight-binding transport simulations in graphene nanoribbon field-effect transistors including phonon scattering,” *Journal of Applied Physics* **113**, 144506 (2013). [DOI: 10.1063/1.4800900](https://doi.org/10.1063/1.4800900). [Full text](https://arxiv.org/pdf/1302.0694). §II, Eqs. (8)–(16).
8. Y. Saad, *Numerical Methods for Large Eigenvalue Problems*, revised edition (SIAM, 2011). [DOI: 10.1137/1.9781611970739](https://doi.org/10.1137/1.9781611970739). [Full text](https://www-users.cse.umn.edu/~saad/eig_book_2ndEd.pdf). §§3.2, 4.3, 9.2.
9. J. Demmel, “Notes for Ma221 Lecture 19: Symmetric eigenvalue problems and the SVD,” University of California, Berkeley (2010). [Author course notes](https://people.eecs.berkeley.edu/~demmel/ma221_Fall10/Lectures/Lecture_19.html). Courant–Fischer theorem와 residual bound.
10. M. Luisier, A. Schenk, and W. Fichtner, “Quantum transport in two- and three-dimensional nanoscale transistors: Coupled mode effects in the nonequilibrium Green’s function formalism,” *Journal of Applied Physics* **100**, 043713 (2006). [DOI: 10.1063/1.2244522](https://doi.org/10.1063/1.2244522). [Full text](https://iis-people.ee.ethz.ch/~schenk/JApplPhys_100_043713.pdf). §§II–III.
11. C. H. Lewenkopf and E. R. Mucciolo, “The recursive Green’s function method for graphene,” *Journal of Computational Electronics* **12**, 203–231 (2013). [DOI: 10.1007/s10825-013-0458-7](https://doi.org/10.1007/s10825-013-0458-7). [Full text](https://arxiv.org/pdf/1304.3934). §§2–3, Eqs. (15)–(18).
12. T. Ozaki, K. Nishio, and H. Kino, “Efficient implementation of the nonequilibrium Green function method for electronic transport calculations,” *Physical Review B* **81**, 035116 (2010). [DOI: 10.1103/PhysRevB.81.035116](https://doi.org/10.1103/PhysRevB.81.035116). [Full text](https://arxiv.org/pdf/0908.4142). §II, Eqs. (3)–(8).
13. C. J. O. Verzijl, J. S. Seldenthuis, and J. M. Thijssen, “Applicability of the wide-band limit in DFT-based molecular transport calculations,” *The Journal of Chemical Physics* **138**, 094102 (2013). [DOI: 10.1063/1.4793259](https://doi.org/10.1063/1.4793259). [Full text](https://arxiv.org/pdf/1403.3861). §II, Eqs. (2)–(6).
14. A.-P. Jauho, N. S. Wingreen, and Y. Meir, “Time-dependent transport in interacting and noninteracting resonant-tunneling systems,” *Physical Review B* **50**, 5528–5544 (1994). [DOI: 10.1103/PhysRevB.50.5528](https://doi.org/10.1103/PhysRevB.50.5528). [Author preprint](https://arxiv.org/pdf/cond-mat/9404027). §V.C.1, Eq. (39); preprint 제목은 “Time-dependent transport in interacting and non-interacting mesoscopic systems”이다.
15. D. A. Lemus, J. Charles, and T. Kubis, “Mode-space-compatible inelastic scattering in atomistic nonequilibrium Green’s function implementations,” *Journal of Computational Electronics* **19**, 1389–1398 (2020). [DOI: 10.1007/s10825-020-01549-8](https://doi.org/10.1007/s10825-020-01549-8). [Full text](https://arxiv.org/pdf/2003.09536). §II.
16. M. Brandbyge, J.-L. Mozos, P. Ordejón, J. Taylor, and K. Stokbro, “Density-functional method for nonequilibrium electron transport,” *Physical Review B* **65**, 165401 (2002). [DOI: 10.1103/PhysRevB.65.165401](https://doi.org/10.1103/PhysRevB.65.165401). [Full text](https://arxiv.org/pdf/cond-mat/0110650). §§II–III, Eqs. (9)–(13).
