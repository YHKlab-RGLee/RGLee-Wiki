---
description: 전자구조의 일반화 고유값 문제에서 출발해 reduced basis의 물리적 의미, Hamiltonian 축소, 상태 복원과 오차·비용 검증을 설명한다.
---

# Model reduction: Fundamentals

Model reduction은 원래의 많은 기저 함수로 기술하던 관심 상태를 더 적은 수의 기저 함수로 표현하고, 축소된 공간에서 해당 상태를 계산할 방정식을 구성하는 방법이다. 전자구조 계산에 적용할 때에는 orbital 기저의 차원을 줄이면서도 관심 에너지 범위의 고유상태와 관측량을 얼마나 정확히 유지할 수 있는지가 중요하다. 이 글은 고정된 단일입자 Hamiltonian의 $Hc=\epsilon Sc$에서 출발하여 기저변환, 부분공간 제한과 반복 eigensolver를 구별한다. 이어 축소 기저를 서로 다른 매개변수 조건에 재사용할 수 있는지, 계산 비용이 실제로 줄어드는지 살펴보고, 일반 선형계와 동역학으로 논의를 확장한다.[1–6]

## 1. 전자구조 계산의 차원과 축소 목표

### (1) 원래 orbital과 관심 상태

서로 선형독립인 atomic orbital (AO) $\{\phi_\alpha\}_{\alpha=1}^{M}$로 단일입자 상태 $\psi_n$을 전개하자. $M$은 원래 기저 함수 수, $n$은 고유상태 번호, $c_n\in\mathbb C^M$은 그 상태의 계수 벡터이다. Hamiltonian 연산자 $\hat H$를 AO 기저로 표현한 행렬과 AO 사이의 overlap 행렬을 다음과 같이 정의한다.[1,2,4]

$$
|\psi_n\rangle=\sum_{\alpha=1}^{M}|\phi_\alpha\rangle(c_n)_\alpha,
\qquad H_{\alpha\beta}=\langle\phi_\alpha|\hat H|\phi_\beta\rangle,
\qquad S_{\alpha\beta}=\langle\phi_\alpha|\phi_\beta\rangle.
$$

이때 에너지 $\epsilon_n$과 계수는 다음 일반화 고유값 문제를 만족한다. 본문은 $H=H^\dagger$, $S=S^\dagger>0$를 가정하며, $\dagger$는 켤레전치이다. $H$와 $\epsilon_n$의 단위는 eV, 정규화한 AO에서 $S$와 계수는 무차원이다.[1–4]

$$
Hc_n=\epsilon_nSc_n,\qquad c_m^\dagger Sc_n=\delta_{mn}.
$$

$M$은 기저 함수의 개수이므로 전자 수나 관심 band의 개수와 같을 필요가 없다. 예를 들어 전체 AO로 구성한 $M$차원 공간에서 특정 energy window에 속하는 몇 개의 고유상태만 필요할 수 있다. 하지만 필요한 고유상태가 몇 개뿐이더라도, 원래 AO 기저에서 각 고유벡터는 여전히 $M$개의 성분으로 표현된다. 일부 고유값만 구하는 계산과, 상태를 표현하는 공간 자체를 작은 공간으로 바꾸는 계산을 이 지점에서 구별해야 한다.[1,3]

AO를 더 풍부하게 선택하여 원래 이산화 오차를 줄이는 일과, 이미 주어진 $M$차원 행렬쌍을 축소하는 일도 별개이다. 이 글에서는 **원래의 동일한 행렬쌍 $H,S$를 충분히 정확하게 풀어 얻은 해**를 축소 모형의 정확도 비교 기준으로 사용한다. Density functional theory (DFT)의 물리적 근사나 AO basis의 완전성까지 이 기준으로 검증되는 것은 아니다.[1,2,5,6]

### (2) Energy window와 관측량

축소 전에 에너지 창 $\mathcal W=[E_{\min},E_{\max}]$, 사용할 조건의 집합 $\mathcal D$, 비교할 관측량을 정한다. $\mu\in\mathcal D$는 일반적인 제어 매개변수이며, 아래 수치 예제에서는 두 번째 orbital의 onsite energy 변화이다. Reduced-order model (ROM)은 해당 조건에서 원래 full-order model (FOM)의 필요한 결과를 적은 자유도로 근사하도록 구성한 모형이다. 특정 매개변수 한 점에서 정확하다는 사실만으로 다른 점까지 정확해지지는 않는다.[5,6]

에너지와 상태의 정확도는 서로 다른 검증 대상이다. 예를 들어 직교 orbital에서 세 번째 성분의 확률 $|(c_n)_3|^2$는 에너지 오차와 다른 정보를 담는다. 비직교 AO에서는 단순 성분 제곱을 그대로 orbital 점유 확률로 읽을 수 없으므로, 관측 연산자와 중첩을 포함한 정의가 먼저 필요하다. 이 글의 성분별 확률 예제는 $S=I$에만 한정한다.[1,4]

| 축소 목적 | 먼저 고정할 대상 | 비교할 결과 |
| --- | --- | --- |
| 저에너지 spectrum | 에너지 창과 관심 상태 수 | 고유값, 원래 방정식의 잔차 |
| 상태의 orbital 성격 | 기저와 내적, 상태 대응 | 복원 상태와 관측량 |
| 조건 변화의 반복 계산 | $\mathcal D$, 기저 구성 표본과 별도 시험점 | 새 조건에서의 오차와 시간 |
| 동적 응답 | 입력, 시간 구간과 출력 | 시간에 따른 상태·출력 오차 |

이 표는 축소 기저를 정하는 것과 별개로, 그 기저에서 어떤 물리량을 계산하고 검증할 것인지 먼저 정해야 함을 보여 준다. 뒤의 방법마다 기저 구성 방식은 달라도, 검증 목적은 유지해야 비교가 가능하다.[3,5,6]

## 2. 기저변환과 부분공간 축소

### (1) 정보가 보존되는 기저변환

가역인 정사각 행렬 $T\in\mathbb C^{M\times M}$로 $c=Tb$라 쓰면 새 좌표 $b$와 원래 좌표 사이를 양방향으로 변환할 수 있다. 왼쪽에서 $T^\dagger$를 곱하면 다음과 같다.[3,4]

$$
H'b_n=\epsilon_nS'b_n,
\qquad H'=T^\dagger HT,\qquad S'=T^\dagger ST.
$$

이는 $M$개의 새로운 orbital $\chi_j=\sum_\alpha\phi_\alpha T_{\alpha j}$로 같은 공간을 표현한 것이다. $T$와 $T^\dagger$가 모두 가역이므로 원래 방정식을 되찾을 수 있고 고유값도 보존된다. 원래 기저가 직교하고 $T$가 unitary이면 $S'=I$이다. 일반적인 가역 변환에서는 $H'$만 바꾸고 $S'$를 버리면 같은 문제가 아니다.[3,4]

따라서 orbital이 국소적으로 보이도록 회전하거나, Hamiltonian을 대각화했다고 해서 차원이 줄어든 것은 아니다. 예를 들어 고정된 $J$개의 isolated bands 안에서 Wannier gauge를 unitary하게 바꾸는 단계는 그 $J$차원 공간을 보존한다. 더 많은 입력 상태에서 $J$차원 공간을 선택하는 단계와 구별해야 한다.[7,8]

### (2) Reduced basis와 새로운 좌표

축소에서는 열독립인 직사각 행렬 $V\in\mathbb C^{M\times r}$, $r<M$을 선택한다. $V$의 각 열 $v_j$는 원래 $M$개의 orbital을 선형결합하여 새로운 기저 함수를 구성할 때 사용하는 계수 벡터이다. 상태의 축소 좌표 $a_n\in\mathbb C^r$와 복원 상태 $\widetilde c_n$은 다음 관계로 연결된다.[2,3,5,6]

$$
|\chi_j\rangle=\sum_{\alpha=1}^{M}|\phi_\alpha\rangle V_{\alpha j},
\qquad \widetilde c_n=Va_n,
\qquad |\widetilde\psi_n\rangle=\sum_{j=1}^{r}|\chi_j\rangle(a_n)_j.
$$

따라서 $V$의 한 열이 특정 원자 하나 또는 원래 Hamiltonian의 정확한 고유상태 하나에 대응할 필요는 없다. 특정 AO를 그대로 선택한 열일 수도 있고, 여러 원자에 걸친 bonding 조합이나 학습 상태에서 얻은 방향일 수도 있다. 행렬 $V$는 **어떤 상태를 축소 공간에서 표현할 수 있는지**를 결정한다. 그 공간에서 각 상태의 좌표 $a_n$을 구하려면 별도의 축소 방정식이 필요하다.[2,3,5]

$\mathcal V=\operatorname{range}(V)$ 밖의 성분을 버리는 순간 정보 손실이 가능해진다. 정규직교 기저에서는 $V^\dagger V=I_r$이지만 $VV^\dagger$는 $I_M$이 아니라 $\mathcal V$로의 projector이다. 비직교 AO에서는 $S$ 내적 $\langle x,y\rangle_S=x^\dagger Sy$와 노름 $\|x\|_S=\sqrt{x^\dagger Sx}$를 사용한다.[3,4]

$$
P_S=V(V^\dagger SV)^{-1}V^\dagger S,
\qquad P_S^2=P_S,
\qquad c=P_Sc+(I-P_S)c.
$$

두 항은 $S$ 내적에서 직교한다. 첫 항은 선택 공간에서 가장 가까운 표현이고, 둘째 항은 그 공간으로 표현할 수 없는 성분이다. $P_S$는 보통 Euclidean 내적에서 Hermitian인 행렬은 아니지만 $P_S^\dagger S=SP_S$를 만족한다. 따라서 비직교 AO 기저에서 projection을 정의할 때에는 Euclidean 내적과 $S$ 내적을 구별해야 한다.[3,4]

## 3. 세 orbital tight-binding 모형

### (1) 전체 고유상태와 좌표 선택

이 절에서는 물질 계산 결과가 아닌 다음 설명용 tight-binding Hamiltonian을 사용한다. 원래 orbital은 $\phi_1,\phi_2,\phi_3$, $S=I_3$이며, 아래 행렬의 수치에 eV를 곱한다. 대각 원소는 onsite energy, 비대각 원소는 orbital 사이 결합이다. 일반적인 행렬 원소 정의를 작은 실수 대칭 모형에 적용한 예이다.[1,3,4]

$$
H_0=\begin{pmatrix}
0&-1&0.3\\
-1&0.5&0.4\\
0.3&0.4&4
\end{pmatrix}\mathrm{eV},
\qquad H(\mu)=H_0+\operatorname{diag}(0,\mu,0).
$$

$\mu$의 단위는 eV이고 기준 조건은 $\mu=0$이다. 세 번째 onsite energy가 높다는 이유로 첫 두 orbital만 남긴다고 하자. 아래 $e_j$는 원래 좌표의 표준 단위벡터이다.

$$
V=[e_1,e_2]=\begin{pmatrix}1&0\\0&1\\0&0\end{pmatrix},
\qquad H_r=V^\dagger H_0V=
\begin{pmatrix}0&-1\\-1&0.5\end{pmatrix}\mathrm{eV}.
$$

원래 3차원 문제의 고유값과 고유벡터는 아래 코드로 얻는다. 작은 에너지부터 정렬했고, 각 벡터에서 절댓값이 가장 큰 성분이 양수가 되도록 부호를 정했다. 행렬 $C$의 열이 각각 해당 고유상태이며, 숫자는 여덟 자리로 반올림하였다.

$$
(\epsilon_1,\epsilon_2,\epsilon_3)
=(-0.82909176,\ 1.27476220,\ 4.05432956)\ \mathrm{eV},
$$

$$
C\simeq\begin{pmatrix}
0.78047412&-0.62323450&0.04938524\\
0.61720184&0.78068222&0.09796510\\
-0.09960941&-0.04597857&0.99396375
\end{pmatrix}.
$$

원래 Hamiltonian에서 에너지가 낮은 두 고유상태에도 세 번째 orbital의 성분이 포함되어 있다. 따라서 이 모형에서 에너지가 낮은 두 고유상태가 만드는 공간은 onsite energy가 낮은 두 orbital이 만드는 공간과 일치하지 않는다. 축소 기저를 고르는 판단이 에너지 순서를 고르는 판단과 같지 않다는 점이 행렬의 열에서 드러난다.

### (2) 축소 spectrum과 누락된 coupling

$H_r$의 고유값을 $\theta_n$, 정규화한 고유벡터를 $a_n$이라 쓰자. 원래 좌표로 복원한 두 상태는 다음과 같다.

$$
(\theta_1,\theta_2)=(-0.78077641,\ 1.28077641)\ \mathrm{eV},
\qquad [Va_1,Va_2]\simeq
\begin{pmatrix}
0.78820544&-0.61541221\\
0.61541221&0.78820544\\
0&0
\end{pmatrix}.
$$

원래 방정식의 잔차를 $\rho_n=H_0Va_n-\theta_nVa_n$으로 정의하면, 첫 두 행은 축소 방정식 때문에 0이지만 세 번째 행은 일반적으로 0이 아니다. 이 모형에서는 다음 식을 이용해 축소 과정에서 제외한 세 번째 orbital과의 결합이 잔차에 어떻게 나타나는지 확인할 수 있다.

$$
\rho_n=\begin{pmatrix}0\\0\\0.3(a_n)_1+0.4(a_n)_2\end{pmatrix}\mathrm{eV}.
$$

| 상태 | 전체 에너지 (eV) | 축소 에너지 (eV) | 에너지 오차 (eV) | $\|\rho_n\|_2$ (eV) |
| --- | ---: | ---: | ---: | ---: |
| 낮은 첫째 상태 | -0.82909176 | -0.78077641 | 0.04831536 | 0.48262652 |
| 낮은 둘째 상태 | 1.27476220 | 1.28077641 | 0.00601420 | 0.13065851 |

전체 상태의 세 번째 orbital 확률은 각각 약 $0.00992203$, $0.00211403$이지만 이 축소에서는 둘 다 0이다. 즉 고유에너지의 오차가 작더라도 축소 기저가 특정 orbital 성분을 전혀 표현하지 못할 수 있다. 위 표의 원래 잔차와 축소 잔차를 혼동하면 이 누락을 발견하지 못한다. 이것은 앞서 정의한 모형을 직접 계산한 결과이며, 일반적인 모든 축소의 오차 크기를 뜻하지 않는다.

다음 Python/NumPy 코드는 입력부터 상태 복원까지 한 번에 실행한다. `eigh`에 넣는 문제는 여기서 $S_r=I$인 실수 대칭 문제이다. 일반적인 $S_r$에 같은 코드를 그대로 적용해서는 안 된다. NumPy 1.21.5에서 실행하여 표와 아래 비교 결과를 확인하였다.

```python
import numpy as np

np.set_printoptions(precision=8, suppress=True)
H0 = np.array([[0.0, -1.0, 0.3],
               [-1.0, 0.5, 0.4],
               [0.3, 0.4, 4.0]])  # eV
S = np.eye(3)
energies, C = np.linalg.eigh(H0)
for n in range(C.shape[1]):
    if C[np.argmax(np.abs(C[:, n])), n] < 0:
        C[:, n] *= -1
print('full energies:', energies)
print('full eigenvectors (columns):\n', C)
assert np.linalg.norm(H0 @ C - (S @ C) * energies) < 1e-12

V = np.eye(3)[:, :2]
Hr, Sr = V.T @ H0 @ V, V.T @ S @ V
assert np.allclose(Sr, np.eye(2))
ritz, A = np.linalg.eigh(Hr)
for n in range(A.shape[1]):
    if A[np.argmax(np.abs(A[:, n])), n] < 0:
        A[:, n] *= -1
C_reduced = V @ A
residual = H0 @ C_reduced - (S @ C_reduced) * ritz
print('coordinate energies:', ritz)
print('reconstructed eigenvectors:\n', C_reduced)
print('full residual norms:', np.linalg.norm(residual, axis=0))
print('energy errors:', ritz - energies[:2])
print('third-orbital populations:', np.abs(C[2, :2])**2)
assert np.linalg.norm(V.T @ residual) < 1e-12
assert np.all(ritz >= energies[:2] - 1e-12)

V_exact = C[:, :2]  # reference basis from the full solution
for mu in (0.0, 0.5):
    H = H0 + np.diag([0.0, mu, 0.0])
    E_full = np.linalg.eigvalsh(H)
    theta, a = np.linalg.eigh(V_exact.T @ H @ V_exact)
    reconstructed = V_exact @ a
    rho = H @ reconstructed - reconstructed * theta
    print(f'mu={mu:.1f}: max energy error='
          f'{np.max(np.abs(theta - E_full[:2])):.8f}, '
          f'max residual={np.max(np.linalg.norm(rho, axis=0)):.8f}')
    if mu == 0.0:
        assert np.linalg.norm(rho) < 1e-12
```

마지막 비교에서는 같은 $r=2$라도 $V_{\rm exact}=[c_1,c_2]$를 사용한다. 이 기저는 세 orbital 성분을 모두 포함한 정확한 저에너지 공간이므로 $\mu=0$에서 두 고유쌍을 수치 정밀도 안에서 보존한다. 다만 정확한 저에너지 고유상태를 기저로 사용하려면 원래의 전체 고유값 문제를 먼저 풀어야 하므로, 이 기저 구성 자체를 저비용 계산으로 볼 수는 없다. 기저의 품질과 기저를 구하는 비용을 분리해 보여 주는 기준이다.[3,4]

| 고정한 $V_{\rm exact}$의 사용 조건 | 최대 에너지 오차 (eV) | 최대 원래 잔차 (eV) |
| --- | ---: | ---: |
| $\mu=0$ eV | $10^{-12}$ 미만 | $10^{-12}$ 미만 |
| $\mu=0.5$ eV | 0.00069312 | 0.04124855 |

매개변수 $\mu$를 바꾼 새로운 조건에서는 해당 기저가 더 이상 정확한 invariant subspace를 이루지 않는다. 이것은 기저를 한 번 만든 뒤 재사용할 때 별도 시험점이 필요한 이유를 보여 준다. 이 한 점의 결과는 다른 $\mu$에서의 오차 보증이나 속도 측정을 대신하지 않는다.[5,6]

## 4. Reduced Hamiltonian과 상태 복원

### (1) 일반화 고유값 문제

앞의 직교 예제를 비직교 AO로 확장하면 축소 행렬과 정규화는 다음과 같다. $H_r,S_r$의 크기는 $r\times r$이며, 상태별 축소 좌표 $a_n$을 풀고 나서 $Va_n$으로 원래 좌표의 상태를 복원한다.[2,3]

$$
H_r=V^\dagger HV,\qquad S_r=V^\dagger SV,
\qquad H_ra_n=\theta_nS_ra_n,
\qquad a_m^\dagger S_ra_n=\delta_{mn}.
$$

이는 새 orbital 사이의 행렬 원소 $\langle\chi_i|\hat H|\chi_j\rangle$와 $\langle\chi_i|\chi_j\rangle$를 계산한 결과이다. 원래 $H$가 이미 AO 사이의 조립 Hamiltonian이므로 $H_r$에 $S$를 한 번 더 삽입하지 않는다. 계수에 작용하는 연산자를 $S^{-1}H$로 쓴 경우에는 $S$ 내적의 투영에서 $S$와 $S^{-1}$가 상쇄되어 같은 식이 된다.[2–4]

$$
V^\dagger S(S^{-1}HVa_n-\theta_nVa_n)
=V^\dagger HVa_n-\theta_nV^\dagger SVa_n=0.
$$

$V$가 열독립이면 $S_r$도 양의 정부호이므로 축소 정규화가 잘 정의된다. 이를 확인하는 식은 $a^\dagger S_ra=(Va)^\dagger S(Va)>0$이다. 반면 $V^\dagger V=I_r$만 확인한 것으로 $S_r=I_r$라 둘 수는 없다. 필요한 것은 $V^\dagger SV=I_r$이다. 거의 종속인 열은 수치적 정규화를 어렵게 하므로 작은 차원만큼이나 기저의 독립성이 중요하다.[3,4]

Galerkin 조건은 $\rho_n$이 선택한 시험 공간에 직교하도록 요구한다. 여기서는 trial space와 test space가 모두 $\mathcal V$이다.[2,3]

$$
\rho_n=HVa_n-\theta_nSVa_n,
\qquad V^\dagger\rho_n=0.
$$

이 조건은 원래 공간 전체의 잔차를 없애지 않는다. 앞의 예제에서 첫 두 성분만 0이었던 이유가 바로 이 식이다. Rayleigh–Ritz의 변분 성질과 더 일반적인 test space 선택은 [Projection methods](projection-methods.md)에서 다룬다.

### (2) 표현 오차와 계산 오차

정확한 상태 $c_n$이 주어졌다고 가정하면 선택 공간에서 가장 가까운 좌표와 표현 오차는 다음처럼 정의된다. 이는 기저의 표현 능력을 측정하는 이상적 비교이며, 실제 계산에서는 보통 $c_n$을 미리 모르므로 바로 사용할 수 없다.[3,4]

$$
a_n^\star=S_r^{-1}V^\dagger Sc_n,
\qquad e_{\rm rep}=\|c_n-Va_n^\star\|_S
=\|(I-P_S)c_n\|_S.
$$

축소 방정식이 반환한 $a_n$은 일반적으로 $a_n^\star$와 다르다. 같은 상태로 대응시키고 위상을 맞춘 뒤의 오차에는 다음 분해가 성립한다. $\|b\|_{S_r}^2=b^\dagger S_rb$이다.[3,4]

$$
\|c_n-Va_n\|_S^2
=e_{\rm rep}^2+\|a_n^\star-a_n\|_{S_r}^2.
$$

첫 항은 공간을 고정한 상태에서 줄일 수 없는 오차이고, 둘째 항은 그 공간 안에서 선택된 좌표의 차이이다. 둘째 항을 모두 수치 풀이 오차라고 부르면 안 된다. 축소 문제를 정확하게 풀어도 최적 표현 좌표와 일치하지 않을 수 있다. 실제 eigensolver를 유한 허용오차에서 멈추면 여기에 별도의 풀이 오차가 더해진다.[3–6]

고유벡터는 전역 위상을 바꾸어도 같은 상태이다. 또 축퇴한 고유값에서는 같은 eigenspace 안의 기저 회전이 가능하다. 따라서 벡터 성분을 그대로 뺀 값만으로 정확도를 판단하지 말고, 고립된 상태에서는 위상을 정렬하거나 overlap을 보고, 축퇴한 상태 묶음에서는 해당 공간의 projector를 비교한다.[3,4]

| 오차의 층 | 바꾸어 볼 대상 | 검증이 답하는 질문 |
| --- | --- | --- |
| 원래 전자구조 근사 | AO basis·격자·물리 모형 | FOM 자체가 충분한가 |
| 공간 표현 | $V$의 방향과 $r$ | 관심 상태를 담을 수 있는가 |
| 축소 방정식 | projection·연산자 근사 | 그 공간에서 필요한 해를 얻는가 |
| 수치 풀이 | eigensolver 허용오차 | 정한 축소 문제를 정확히 풀었는가 |

이 구분은 본문의 정의에서 얻는 검증 절차이다. 한 층의 오차가 작다고 다른 층이 사라지는 것은 아니며, 두 모형을 비교할 때에는 원래 $H,S$와 정규화 규약을 일치시켜야 한다.[1–6]

## 5. 주요 축소 방법과 eigensolver

### (1) 기저 구성과 방정식 구성

어떤 상태를 축소 기저에 포함할지 결정하는 과정과, 선택한 기저에서 방정식을 구성하는 과정은 구별해야 한다. Proper orthogonal decomposition (POD)은 여러 조건에서 얻은 상태 표본인 snapshot의 주요 방향을 고르는 방법이다. Singular value decomposition (SVD)을 이용해 상태 표본을 압축할 수 있지만, 그렇게 얻은 $V$만으로는 새 조건의 $a_n$이 결정되지 않는다. $H_r,S_r$ 같은 축소 방정식이 추가로 필요하다.[5,6]

다음 표는 서로 다른 방법을 “남기는 상태”와 “제거한 정보의 처리”라는 같은 기준으로 비교한다. 세부 유도는 각 문서에서 다루며, 표에 나열한 방법들은 서로 다른 목적과 단계에 해당하므로, 반드시 하나만 선택해야 하는 대안 관계는 아니다.

| 방법 | 남기는 표현 | 제거한 정보와 검증 대상 |
| --- | --- | --- |
| [Low-rank approximation](low-rank-approximation.md)·POD | snapshot을 잘 표현하는 방향 | 표본 밖의 상태와 관심 관측량을 별도 검증한다.[5,6] |
| [Projection methods](projection-methods.md) | 미리 선택한 $\mathcal V$ | 공간 밖 성분을 제한하며, 원래 잔차가 남을 수 있다.[2,3] |
| [Downfolding](downfolding.md) | 선택한 active orbital 성분 | 제거 공간의 결합을 에너지 의존 유효 연산자에 반영한다.[3,9] |
| [Wannierization](wannierization.md) | 선택한 band 공간의 국소 표현 | 고정 공간 안의 unitary gauge는 정보를 보존하며, 공간 선택·보간의 근사는 별개이다.[7,8] |
| [Mode-space reduction](mode-space-reduction.md) | cell·단면 상태의 조합 | onsite·hopping 등의 block을 투영하며, band와 수송 결과의 검증이 필요하다.[10,11] |

세 orbital 예제로 단순한 부분공간 projection과 downfolding의 차이를 살펴보자. $A=\{1,2\}$를 남길 공간, $B=\{3\}$을 제거할 공간이라 하고, 결합 열을 $b=(0.3,0.4)^T\ \mathrm{eV}$라 하자. 세 번째 행을 풀어 역대입하면, $E\ne4\ \mathrm{eV}$에서 다음 식을 얻는다.[3,9]

$$
c_B=(E-4\ \mathrm{eV})^{-1}b^\dagger c_A,
\qquad H_{\rm eff}(E)=H_{AA}+\frac{bb^\dagger}{E-4\ \mathrm{eV}}.
$$

단순 projection은 $H_{AA}$만 남기지만 정확한 제거는 두 번째 항을 포함한다. 이 보정은 eV 단위이고, $E<4\ \mathrm{eV}$에서는 음의 준정부호이다. 따라서 높은 onsite orbital과의 결합이 낮은 에너지에도 영향을 미칠 수 있다. $H_{\rm eff}(E)c_A=Ec_A$는 에너지 의존 방정식이며, 임의의 기준 에너지에 고정해 ordinary eigenproblem으로 바꾸는 것은 추가 근사이다. 이 식은 유한 단일입자 모형의 대수적 제거이지, DFT의 상호작용이나 밀도 응답을 자동으로 제거한 식은 아니다.[3,9]

### (2) Davidson·Lanczos와 ROM

Davidson과 Lanczos도 작은 부분공간에 Hamiltonian을 투영한다. 그러나 반복 eigensolver에서 그 공간은 **현재 큰 문제의 고유쌍을 수렴시키기 위한 작업 공간**이다. 반복마다 방향을 더하거나 restart하며 원래 문제의 잔차를 줄인다. Davidson 계열에서는 현재 Ritz vector의 잔차에 preconditioner를 적용한 보정 방향을 추가한다. 전자구조 계산의 한 self-consistent field (SCF) 단계 안에서도 이런 과정이 일어난다.[2,3]

표준 Hermitian Lanczos에서는 $S=I$이고 시작 벡터 $v$로 만든 Krylov 공간을 사용한다. 아래 $q$는 공간의 최대 차수이며, 선형종속이 생기면 실제 차원은 더 작다.[3,12]

$$
\mathcal K_q(H,v)=\operatorname{span}\{v,Hv,H^2v,\ldots,H^{q-1}v\}.
$$

이 공간의 정규직교 기저에서 작은 고유값 문제를 풀어 Ritz pair를 얻는다. 큰 행렬에 대한 matrix–vector product가 공간을 만드는 과정에 계속 필요하다. Davidson/Lanczos가 전체 $M$개의 고유값을 모두 구하지 않는다는 사실과, 새로운 조건을 원래 크기의 연산 없이 계산하는 ROM을 이미 만들었다는 주장은 다르다.[2,3,5,12]

재사용할 ROM에서는 $V$와 축소 연산자 구성법을 정해 두고, 여러 $\mu$에서의 출력 정확도와 계산 비용을 검증한다. Eigensolver의 최종 공간을 재사용할 수도 있고, 반복 공간의 정보를 모아 ROM을 만들 수도 있다. 따라서 차이는 projection 사용 여부가 아니라 **무엇을 수렴시키고 어느 조건까지 재사용을 검증했는가**이다.[2,3,5,6]

| 구분 | 반복 eigensolver | 재사용을 목표로 한 ROM |
| --- | --- | --- |
| 직접 목표 | 현재 $H,S$의 고유쌍 수렴 | 지정 조건 범위의 결과 근사 |
| 기저의 역할 | 계산 중 갱신하는 탐색 공간 | 반복 사용을 위해 구성한 표현 공간 |
| 대표 확인 | 원래 고유값 문제의 잔차 | 새 조건의 상태·관측량 오차와 비용 |
| 비용의 핵심 | 큰 행렬의 작용과 직교화 | 준비 비용, 작은 문제, 조립·복원 비용 |

## 6. 정확도와 계산 비용

### (1) 잔차와 관측량 검증

$S=I$, $\|\widetilde c\|_2=1$일 때 Hermitian $H$에 대한 잔차 $\rho=(H-\theta I)\widetilde c$는 적어도 하나의 정확한 고유값과의 거리를 제한한다. 정확한 정규직교 고유기저로 $\widetilde c=\sum_j\alpha_jc_j$를 전개하면 다음 식에서 직접 확인할 수 있다.[3,4]

$$
\|\rho\|_2^2=\sum_j|\alpha_j|^2(\epsilon_j-\theta)^2,
\qquad \min_j|\epsilon_j-\theta|\le\|\rho\|_2.
$$

다만 잔차가 작다는 사실만으로 원하는 특정 band의 고유값 또는 고유벡터를 정확히 찾았다고 보장할 수는 없다. 고립된 목표 상태 $n$에 대해 나머지 spectrum과의 거리 $\delta=\min_{j\ne n}|\epsilon_j-\theta|>0$를 알면, 그 상태와 이루는 각 $\vartheta$에 다음 bound가 성립한다. $\cos\vartheta=|c_n^\dagger\widetilde c|$이다.[3,4]

$$
\sin\vartheta\le\frac{\|\rho\|_2}{\delta}.
$$

따라서 같은 잔차라도 가까운 상태들이 모여 있으면 개별 고유벡터 정확도를 강하게 제한하지 못한다. 축퇴에서는 개별 벡터 대신 공간을 비교해야 한다. 비직교 문제에서는 $\bar H=S^{-1/2}HS^{-1/2}$, $\bar c=S^{1/2}\widetilde c$로 바꾸면 Hermitian 표준 문제를 얻고, 그 잔차는 $S^{-1/2}\rho$이다. 여기서 제곱근은 양의 정부호 square root이다.[2–4]

$$
\|\rho\|_{S^{-1}}=\sqrt{\rho^\dagger S^{-1}\rho}
=\|S^{-1/2}\rho\|_2.
$$

이 노름은 원래 물리적 정규화와 맞는다. 구현에서 임의로 AO의 크기를 바꾼 뒤 같은 Euclidean 잔차 기준만 비교하면 의미가 달라질 수 있다. 잔차의 크기, 단위, 정규화와 함께 어떤 norm을 사용했는지 남겨야 한다.[2–4]

관측 연산자 $\hat O$의 조립 행렬을 $O_{\alpha\beta}=\langle\phi_\alpha|\hat O|\phi_\beta\rangle$라 하면, 정규화한 상태의 기대값도 같은 기저로 변환한다.[1,4]

$$
\langle O\rangle=c^\dagger Oc,
\qquad O_r=V^\dagger OV,
\qquad \langle O\rangle_r=a^\dagger O_ra.
$$

Hamiltonian의 차원만 줄이고 원래 모형에서 정의한 관측량을 축소 기저에 맞게 변환하지 않으면, 축소 결과가 실제 계산 목적을 충족하는지 검증하기 어렵다. 작은 에너지 오차 외에도 목표 orbital 성격, 필요한 행렬 원소, 수송 계산이라면 transmission 같은 실제 출력을 비교한다. 마지막 항목은 lead와 장치 모형까지 일치시켜야 의미가 있으므로 고정된 유한 $H$의 spectrum 검증보다 넓은 작업이다.[5,6,10,11]

기저 구성과 차원 선택에 사용하지 않은 시험 집합 $\mathcal D_{\rm test}\subset\mathcal D$에서 오차 지표 $\eta(\mu)$를 평가한다. 유한 표본 최대값이 연속 영역 전체의 최대값과 같다는 보장은 없다.[5,6]

$$
\max_{\mu\in\mathcal D_{\rm test}}\eta(\mu)
\le\sup_{\mu\in\mathcal D}\eta(\mu).
$$

$r$을 늘리는 검사는 같은 조건·출력·풀이 허용오차에서 수행해야 기저 확장의 효과를 분리할 수 있다. 검증 범위를 벗어난 조건에 같은 코드를 적용할 수 있다는 사실만으로 정확성이 확보되지는 않는다.[5,6]

### (2) Offline·online 비용과 DFT 한계

ROM의 offline 단계에서는 원래 모형에서 상태 snapshot을 계산하고, 이를 바탕으로 축소 기저와 축소 연산자를 준비한다. Online 단계는 새 조건의 작은 문제를 풀고 필요한 출력을 계산한다. 밀집 Hermitian 행렬의 전체 대각화 비용은 대표적으로 $O(M^3)$, 작은 행렬에서는 $O(r^3)$이지만, 희소 반복 eigensolver와 비교할 때 이 비율을 곧바로 실제 speedup으로 사용할 수는 없다.[1,3,5,6]

$H$가 밀집이면 매번 $V^\dagger H(\mu)V$를 형성하는 데 $O(M^2r+Mr^2)$ 연산이 든다. 이는 행렬곱 차원에서 얻는 비용이다. 모든 복원 상태를 만들면 상태 하나당 $O(Mr)$도 필요하다. 큰 $H$의 조립, 잔차 평가와 출력 복원이 계속 남는다면 따라서 축소 고유값 문제를 빠르게 풀더라도 원래 크기의 행렬 조립, 잔차 평가와 상태 복원이 실행 시간을 지배하면 실제 가속 효과는 제한적이다.[5,6]

고정 $V$와 적은 수 $Q$의 항으로 Hamiltonian을 다음처럼 분리할 수 있으면, 각 $H_{r,\ell}$을 미리 계산하여 online 조립에서 원래 차원 의존성을 줄일 수 있다. $f_\ell(\mu)$는 무차원 계수, $H_\ell$은 에너지 단위 행렬이다.[5,6]

$$
H(\mu)=\sum_{\ell=1}^{Q}f_\ell(\mu)H_\ell,
\qquad H_r(\mu)=\sum_{\ell=1}^{Q}f_\ell(\mu)H_{r,\ell},
\qquad H_{r,\ell}=V^\dagger H_\ell V.
$$

이것이 affine decomposition을 이용한 offline–online 분리이다. 분리형 표현 자체를 근사했다면 그 연산자 오차도 추가로 검증한다. 예제의 onsite 변화는 기준 에너지 단위로 나누어 두 항의 이런 표현을 만들 수 있지만, 일반 SCF Hamiltonian이 저절로 같은 형태를 갖는 것은 아니다.[1,2,5,6]

평가 횟수를 $N_{\rm eval}$, 준비 시간을 $T_{\rm off}$, 한 번의 전체·축소 평가 시간을 각각 $T_{\rm full},T_{\rm on}$이라 하면 같은 출력 요구에서의 손익 조건은 다음과 같다. $T_{\rm on}$에는 필요한 검증·복원 비용도 포함한다.[5,6]

$$
T_{\rm off}+N_{\rm eval}T_{\rm on}
<N_{\rm eval}T_{\rm full}.
$$

$T_{\rm full}>T_{\rm on}$일 때만 준비 비용을 반복 평가로 회수할 가능성이 있다. 메모리에서도 밀집 $H_r$는 $O(r^2)$이지만 $V$ 저장은 $O(Mr)$이며, 원래 연산자를 계속 사용하면 그 저장 요구가 없어지지 않는다. 따라서 $M,r$, 기저 구성 시간, 평가 시간과 복원 여부를 함께 기록한다.[5,6]

DFT의 SCF 과정에서는 전자 밀도가 Hamiltonian을 바꾸고, 점유 상태의 변화가 다시 밀도를 바꾼다. 고정한 $H$에서 좁은 에너지 창의 band를 재현한 결과만으로 총전하, 전체 점유공간, self-consistency, total energy와 원자 힘의 정확도를 선언할 수 없다. 힘은 에너지의 위치 미분과 기저 의존성까지 포함하므로 별도 검증이 필요하다.[1,2]

따라서 이 글의 예제는 “주어진 Hamiltonian의 어떤 상태를 축소 공간이 표현하는가”를 검증한다. SCF를 축소하려면 밀도·점유수·Hamiltonian 갱신을 일관되게 정의해야 하고, 구조 최적화에 사용하려면 힘까지 비교해야 한다. 이것은 새로운 축소 기법의 제안이 아니라, 고정-$H$ 계산의 결과를 확대 해석하지 않기 위한 적용 범위의 구분이다.[1,2]

## 7. 일반 선형 모형으로의 확장

### (1) 선형계와 입출력

같은 사고방식은 고유값 문제 밖에서도 사용한다. 가역 행렬 $K$에 대한 정적 문제 $Kx=b$에서 $x\simeq Va$라 두고 Galerkin 조건을 적용하면 다음 축소계를 얻는다. 여기서 $x$는 일반 상태이고 전자구조 계수 $c$와 구별한다.[5,6]

$$
K_ra=b_r,\qquad K_r=V^\dagger KV,\qquad b_r=V^\dagger b.
$$

원래 $K$가 가역이어도 임의의 projection으로 만든 $K_r$가 항상 가역인 것은 아니다. $K$가 Hermitian positive-definite이고 $V$가 열독립이면 $a^\dagger K_ra=(Va)^\dagger K(Va)>0$이므로 가역성이 유지된다. 그보다 일반적인 문제에서는 축소계의 조건을 따로 확인한다.[4,6]

근사 상태 $\widetilde x=Va$의 잔차를 $\rho_K=b-K\widetilde x$라 하면, 오차 $e=x-\widetilde x$는 다음 정확한 관계를 만족한다. $\|\cdot\|_2$는 벡터의 Euclidean norm 또는 그에 대응하는 operator norm이다.[4,6]

$$
e=K^{-1}\rho_K,
\qquad \|e\|_2\le\|K^{-1}\|_2\,\|\rho_K\|_2.
$$

작은 잔차가 작은 상태 오차로 이어지려면 역연산자의 증폭을 고려해야 한다. 차원이 없는 보조 예제로 $K=\operatorname{diag}(1,10^{-3})$, $b=(1,10^{-3}p)^T$, $V=e_1$을 택하면 전체 상태는 $(1,p)^T$, 복원 상태는 $(1,0)^T$이다.

$$
\|e\|_2=|p|,\qquad \|\rho_K\|_2=10^{-3}|p|.
$$

출력을 $y_1=x_1$로 잡으면 정확하지만 $y_2=x_2$로 잡으면 오차는 $|p|$이다. 또한 $K$의 작은 대각 원소를 0으로 만드는 rank-one 행렬 근사는 상대 행렬 오차가 $10^{-3}$이어도 가역성을 잃는다. 반면 위 projection은 가역인 $1\times1$ 축소계이다. 이 직접 계산은 행렬의 low-rank 근사, 작은 방정식과 출력 정확도가 같은 개념이 아님을 보여 준다.[4–6]

동적 문제에서는 질량 행렬 $E_d$, 진화 행렬 $A_d$, 입력 행렬 $B_d$, 출력 행렬 $C_d$를 사용하자. $x(t)\in\mathbb C^M$은 상태, $u(t)$는 입력, $y(t)$는 출력이다. $E_d$는 에너지 변수가 아니며 이 절에서는 가역으로 가정한다. 고정된 trial basis $V$와 test basis $Z\in\mathbb C^{M\times r}$로 Petrov–Galerkin 조건을 적용한다.[5,6]

$$
E_d\dot x=A_dx+B_du,\qquad y=C_dx,
$$

$$
E_{d,r}\dot a=A_{d,r}a+B_{d,r}u,\qquad y_r=C_{d,r}a,
$$

$$
E_{d,r}=Z^\dagger E_dV,\quad A_{d,r}=Z^\dagger A_dV,
\quad B_{d,r}=Z^\dagger B_d,\quad C_{d,r}=C_dV.
$$

일반적인 ordinary differential equation으로 풀려면 $E_{d,r}$도 가역이어야 한다. 초기상태를 $Va(0)$로 근사한 오차와 시간에 따른 잔차가 함께 영향을 주며, 출력 오차에는 $\|y-y_r\|_2\le\|C_d\|_2\|x-Va\|_2$가 성립한다. 이 식은 상태 정확도와 출력 정확도를 연결하지만, 출력 연산자의 영향을 생략하지 않는다.[5,6]

### (2) 안정성의 조건

Hermitian 전자구조 문제에서 $H_r$가 Hermitian인 성질과, 일반 동역학에서 시간이 지나도 해가 발산하지 않는 성질은 다르다. 축소 안정성은 보존하려는 구조에 맞는 조건에서 확인해야 한다.[4,5]

예를 들어 입력이 없고 $E_d=I$이며 $D=(A_d+A_d^\dagger)/2$가 negative-definite이면 다음 norm 감소가 성립한다. 여기서 $D$는 진화 행렬의 Hermitian part이다.[4,5]

$$
\frac{d}{dt}\|x\|_2^2=2x^\dagger Dx<0\qquad(x\ne0).
$$

$Z=V$, $V^\dagger V=I_r$로 투영하면 축소 진화 행렬의 Hermitian part는 $V^\dagger DV$이다. $V$가 열독립이므로 이 행렬도 negative-definite이며 같은 감소 조건을 유지한다. 반면 원래 고유값들의 실수부가 모두 음수라는 조건만으로 위 증명을 적용할 수는 없다.[4,5]

시간 단위를 하나 정한 다음 보조 예제를 보자. 행렬의 원소 단위는 그 시간 단위의 역수이다.

$$
A_d=\begin{pmatrix}-1&4\\0&-1\end{pmatrix},
\qquad v=\frac{1}{\sqrt2}\begin{pmatrix}1\\1\end{pmatrix},
\qquad v^\dagger A_dv=1.
$$

원래 해는 $e^{A_dt}=e^{-t}\begin{pmatrix}1&4t\\0&1\end{pmatrix}$ 때문에 장시간에 0으로 가지만, 축소계는 $\dot a=a$이므로 0이 아닌 초기조건에서 증가한다. 이 반례는 안정한 FOM에 임의의 작은 공간을 적용한다고 안정한 ROM이 자동으로 만들어지지 않음을 보여 준다. 같은 기저를 사용하더라도 eigenproblem, 정적 선형계와 동역학이 요구하는 검증은 각각 구별한다.[4,5]

## 8. 요약

- $M$은 원래 orbital 수이고 $r$은 남기는 독립 조합 수이다. $V$의 열은 새 orbital의 계수이며 축소 좌표를 $Va_n$으로 원래 공간에 복원한다.
- 가역 기저변환은 전체 공간을 보존한다. 직사각 $V$를 사용한 부분공간 제한은 그 밖의 상태 성분을 표현하지 못한다.
- 조립 행렬에는 $H_r=V^\dagger HV$, $S_r=V^\dagger SV$를 함께 사용한다. $V^\dagger\rho=0$은 전체 잔차가 0이라는 뜻이 아니다.
- Davidson·Lanczos의 작업 공간과 재사용할 ROM은 목적과 검증 범위로 구별한다. 기저 생성, 방정식 구성, downfolding과 고정 공간의 Wannier 회전도 서로 다른 단계이다.
- 에너지·상태·관측량의 오차와 준비·조립·복원 비용을 함께 확인한다. 고정 Hamiltonian의 성공을 SCF 밀도나 힘의 정확도로 확대하지 않는다.

## 9. 참고문헌

1. J. M. Soler et al., “The SIESTA method for ab initio order-N materials simulation,” *Journal of Physics: Condensed Matter* **14**, 2745–2779 (2002). [DOI: 10.1088/0953-8984/14/11/302](https://doi.org/10.1088/0953-8984/14/11/302). [Full text](https://arxiv.org/pdf/cond-mat/0111138). AO basis, Hamiltonian·density, total energy·forces와 diagonalization 절.
2. P. Giannozzi et al., “QUANTUM ESPRESSO: a modular and open-source software project for quantum simulations of materials,” *Journal of Physics: Condensed Matter* **21**, 395502 (2009). [DOI: 10.1088/0953-8984/21/39/395502](https://doi.org/10.1088/0953-8984/21/39/395502). [Full text](https://arxiv.org/pdf/0906.2569). Appendix A.1–A.2, Eqs. (A.8)–(A.13). 이 문헌의 overlap operator는 AO 중첩과 기원이 다르지만 일반화 고유값 문제의 대수적 규약을 교차검증한다.
3. Y. Saad, *Numerical Methods for Large Eigenvalue Problems*, revised edition (2011). [Author-hosted full text](https://www-users.cse.umn.edu/~saad/eig_book_2ndEd.pdf). §§3.1–3.2, 4.3, 6.3, 8.3, 8.5, 9.2.5–9.2.6.
4. S. Axler, *Linear Algebra Done Right*, 4th ed. (Springer, 2024). [Open-access author edition](https://linear.axler.net/LADR4e.pdf). §§6C, 7B–7C; Theorems 6.61, 7.29, 7.31, 7.38.
5. P. Benner, S. Gugercin, and K. Willcox, “A Survey of Projection-Based Model Reduction Methods for Parametric Dynamical Systems,” *SIAM Review* **57**(4), 483–531 (2015). [DOI: 10.1137/130932715](https://doi.org/10.1137/130932715). [Author-hosted full text](https://kiwi.oden.utexas.edu/papers/Parametric-model-reduction-survey-Benner-Gugercin-Willcox.pdf). §§1–3, 5.
6. B. Haasdonk, “Reduced Basis Methods for Parametrized PDEs—A Tutorial Introduction for Stationary and Instationary Problems,” in *Model Reduction and Approximation: Theory and Algorithms*, 65–136 (SIAM, 2017). [DOI: 10.1137/1.9781611974829.ch2](https://doi.org/10.1137/1.9781611974829.ch2). [Author preprint](https://pnp.mathematik.uni-stuttgart.de/ians/haasdonk/data/oberwolfach2014/RBtutorial.pdf). §§2–4; proposition 번호는 공개 preprint를 따른다.
7. N. Marzari, A. A. Mostofi, J. R. Yates, I. Souza, and D. Vanderbilt, “Maximally localized Wannier functions: Theory and applications,” *Reviews of Modern Physics* **84**, 1419–1475 (2012). [DOI: 10.1103/RevModPhys.84.1419](https://doi.org/10.1103/RevModPhys.84.1419). [Full text](https://arxiv.org/pdf/1112.5411). §§II.A, II.I, VI.
8. J. Kuneš, “Wannier Functions and Construction of Model Hamiltonians,” in *The LDA+DMFT approach to strongly correlated materials*, Modeling and Simulation Vol. 1, Chapter 4 (Forschungszentrum Jülich, 2011). [Full text](https://www.cond-mat.de/events/correl11/manuscripts/kunes.pdf). §3.1, Eqs. (13)–(18), pp. 4.7–4.8 (PDF pp. 7–8).
9. I. V. Solovyev, Z. V. Pchelkina, and V. I. Anisimov, “Construction of Wannier functions from localized atomiclike orbitals,” *Physical Review B* **75**, 045110 (2007). [DOI: 10.1103/PhysRevB.75.045110](https://doi.org/10.1103/PhysRevB.75.045110). [Full text](https://arxiv.org/pdf/cond-mat/0608528). §II.B, Eqs. (7)–(12).
10. J. Z. Huang, H. Ilatikhameneh, M. Povolotskyi, and G. Klimeck, “Robust Mode Space Approach for Atomistic Modeling of Realistically Large Nanowire Transistors,” *Journal of Applied Physics* **123**, 044303 (2018). [DOI: 10.1063/1.5010238](https://doi.org/10.1063/1.5010238). [Full text](https://arxiv.org/pdf/1710.08064). §§II–IV.
11. R. Grassi et al., “Mode space approach for tight-binding transport simulations in graphene nanoribbon field-effect transistors including phonon scattering,” *Journal of Applied Physics* **113**, 144506 (2013). [DOI: 10.1063/1.4800900](https://doi.org/10.1063/1.4800900). [Full text](https://arxiv.org/pdf/1302.0694). §II.B, Eqs. (8)–(13).
12. A. Ruhe, “Lanczos Method,” in Z. Bai et al. (eds.), *Templates for the Solution of Algebraic Eigenvalue Problems: A Practical Guide* (SIAM, 2000). [Online chapter](https://netlib.org/utk/people/JackDongarra/etemplates/node103.html).
