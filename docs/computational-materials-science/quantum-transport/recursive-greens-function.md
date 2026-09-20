---
description: Block-tridiagonal 소자의 Green's function 블록을 재귀적으로 계산하고 자기일관적 소자 모사에 연결하는 방법을 설명
---

# NEGF: Recursive Green's function

Recursive Green's function (RGF)은 국소 결합 Hamiltonian의 block-tridiagonal structure를 이용해 필요한 Green's function 블록만 계산하는 수치 방법이다. Nonequilibrium Green's function (NEGF)은 열린 양자계의 물리적 정식화이고, RGF는 새로운 수송 이론이나 NEGF의 추가 근사가 아니다. [NEGF formalism](negf-formalism.md)에서 정의한 열린 소자 행렬에 Gaussian elimination과 Schur complement를 특정 순서로 적용하는 알고리즘이다.[1–4]

RGF의 계산 범위는 원하는 관측량에 따라 달라진다. Transmission에는 두 경계 사이의 일부 블록만 필요할 수 있지만, local density of states (LDOS)와 전하 밀도에는 모든 대각 블록이 필요하고 국소 전류에는 인접한 비대각 블록도 필요하다. 따라서 먼저 출력량을 정한 뒤 저장할 재귀 블록과 후진 복원 범위를 결정해야 한다.[1–4]

## 1. Slice 분할과 block-tridiagonal 구조

### (1) Block-tridiagonal structure

소자 영역을 수송 방향으로 $N$개의 slice로 나누고 인접 slice끼리만 직접 결합하도록 정렬한다. 직교 기저에서 열린 소자의 retarded energy matrix는

$$
\mathcal A(E)
=
(E+i\eta)I-H_D-\Sigma_L^R-\Sigma_R^R
$$

이며, block form은

$$
\mathcal A=
\begin{pmatrix}
A_1-\Sigma_L^R & -V_{12} & 0 & \cdots & 0\\
-V_{21} & A_2 & -V_{23} & \cdots & 0\\
0 & -V_{32} & A_3 & \ddots & \vdots\\
\vdots & \vdots & \ddots & \ddots & -V_{N-1,N}\\
0 & 0 & \cdots & -V_{N,N-1} & A_N-\Sigma_R^R
\end{pmatrix},
$$

$$
A_n=(E+i\eta)I-H_{nn},
\qquad
G^R=\mathcal A^{-1}
$$

이다. $V_{n,n+1}=V_{n+1,n}^\dagger$이며 전극 self-energy는 경계 slice에만 작용한다고 썼다.[1–4]

각 원자나 격자점을 별도의 slice로 둘 필요는 없다. 핵심은 같은 slice를 건너뛰는 직접 결합이 없어야 한다는 점이다. 예를 들어 두 원자층을 건너뛰는 hopping이 있으면 필요한 원자층을 한 slice로 묶거나 자유도를 재정렬해 block-tridiagonal form을 만든다.[1–4]

### (2) Slice 폭과 계산 비용

각 slice의 궤도 수가 $M$이고 모든 slice에서 비슷하다고 하자. 조밀한 $M\times M$ 블록의 분해·역연산이 각 slice에서 일어나므로 한 에너지당 계산량은 대략

$$
\mathcal O(NM^3)
$$

이다. 전체 $NM$ 차원 행렬을 조밀하게 직접 역산하는 $\mathcal O((NM)^3)$보다 길이 방향 확장성이 좋지만, 단면이 커져 $M$이 증가하면 비용은 빠르게 커진다.[2–5]

따라서 slice 수만 줄이는 것이 항상 유리하지 않다. 여러 slice를 합치면 $N$은 줄지만 $M^3$ 비용이 커진다. 결합 범위를 만족하는 범위에서 최대 block 크기와 fill-in을 작게 만드는 정렬이 중요하다.[2–4]

Slice 크기가 서로 다르면 $n$번째 크기를 $M_n$으로 둔다. $g^L_{nn}$은 $M_n\times M_n$ 정사각 행렬이지만 $V_{n,n+1}$은 $M_n\times M_{n+1}$ 직사각 행렬이다. 따라서 $V_{n,n-1}g^L_{n-1,n-1}V_{n-1,n}$은 다시 $M_n\times M_n$이 되어 해당 slice의 대각 블록에서 뺄 수 있다. 동일한 블록 폭은 비용을 간단히 표현하기 위한 가정이며, 재귀식 자체의 필요조건은 아니다. 입력 검증에서는 각 곱의 차원과 경계 self-energy가 작용하는 부분공간을 먼저 확인한다.[2,3]

!!! warning "[Interpretation Caveat]"
    “RGF는 선형 복잡도이다”라는 말은 slice 폭 $M$이 길이 $N$과 무관하게 유지될 때의 길이 의존성을 뜻한다. 2차원 정사각형 소자를 한 방향으로 길게 만들면서 단면도 함께 키우면 $M$도 증가하므로 전체 계산량은 소자 크기에 선형이 아니다.[2–5]

## 2. 전진 소거

### (1) Left-connected Green's function

왼쪽 전극과 첫 번째부터 $n$번째 slice까지만 연결한 계의 마지막 대각 블록을 $g^L_{nn}$이라 하자. 첫 블록은

$$
g^L_{11}
=
\left[A_1-\Sigma_L^R\right]^{-1}
$$

이고, $n=2,\ldots,N-1$에 대해

$$
\Sigma_{n}^{L}
=V_{n,n-1}g^L_{n-1,n-1}V_{n-1,n},
$$

$$
g^L_{nn}
=
\left[A_n-\Sigma_n^L\right]^{-1}
$$

로 갱신한다. $\Sigma_n^L$은 이미 제거한 왼쪽 부분 전체가 $n$번째 slice에 미치는 유효 self-energy이다.[1–4]

마지막 slice에서도 먼저 $\Sigma_N^L=V_{N,N-1}g^L_{N-1,N-1}V_{N-1,N}$을 계산한 뒤 오른쪽 전극까지 연결해

$$
G^R_{NN}
=
\left[
A_N-\Sigma_R^R-\Sigma_N^L
\right]^{-1}
$$

을 얻는다. 이 단계는 왼쪽부터 한 slice씩 붙이는 Dyson equation으로도, 앞선 블록을 제거하는 block Gaussian elimination으로도 해석할 수 있다.[1–4]

위 재귀는 $N\ge2$에 대한 것이다. Slice가 하나뿐이면 재귀 없이 $G^R_{11}=[A_1-\Sigma_L^R-\Sigma_R^R]^{-1}$로 두 전극을 함께 연결한다.

### (2) 경계 사이의 전파

Transmission만 필요하면 전체 대각 블록을 복원하지 않고 경계 사이 블록을 함께 전진시킬 수 있다. $n$번째 slice까지만 연결한 부분계의 $(1,n)$ 블록을 $g^L_{1n}$이라 정의한다. 초기값은 앞 절의 $g^L_{11}$이고, $n=2,\ldots,N-1$에서

$$
g^L_{1n}=g^L_{1,n-1}V_{n-1,n}g^L_{nn}
$$

로 갱신한다. 아직 오른쪽 나머지 부분을 연결하지 않았으므로 이 블록은 전체 소자의 $G^R_{1n}$과 일반적으로 다르다. 마지막 단계에서는 양 전극을 포함한 $G^R_{NN}$을 사용하여

$$
G^R_{1N}=g^L_{1,N-1}V_{N-1,N}G^R_{NN}
$$

으로 닫는다. 이 최종 블록으로 경계끼리의 transmission을 계산한다. $N=2$이면 중간 반복 없이 $g^L_{11}$에서 바로 마지막 식을 적용한다.[2–4]

이 경로는 메모리를 줄이지만 모든 국소량을 제공하지 않는다. 이후에 어떤 블록이 필요한지 알 수 없다면 $g^L_{nn}$을 저장해 후진 복원이 가능하도록 하는 편이 안전하다.

### (3) 두 slice의 해석적 예제

전진과 후진 단계의 역할은 각 slice에 궤도가 하나씩 있는 두 사이트에서 직접 확인할 수 있다. $z=E+i\eta$, onsite 에너지를 $\varepsilon_1,\varepsilon_2$, hopping을 $t$라 하고 $a=z-\varepsilon_1-\Sigma_L^R$, $d=z-\varepsilon_2-\Sigma_R^R$로 두면

$$
\mathcal A=\begin{pmatrix}a&-t\\-t^*&d\end{pmatrix},\qquad
G^R=\frac{1}{ad-|t|^2}
\begin{pmatrix}d&t\\t^*&a\end{pmatrix}.
$$

이 식은 앞의 열린 소자 행렬을 $N=2$에 대입해 직접 역산한 결과이다. 같은 계에 RGF를 적용하면 $g^L_{11}=1/a$이고, 왼쪽을 제거한 self-energy는 $\Sigma_2^L=|t|^2/a$이므로

$$
G^R_{22}=\frac{1}{d-|t|^2/a},\qquad
G^R_{12}=\frac{t}{a}G^R_{22},\qquad
G^R_{11}=\frac1a+\frac{|t|^2}{a^2}G^R_{22}
$$

를 얻는다. 각 식을 통분하면 직접 역행렬의 해당 원소가 된다. 이 예제는 Dyson 식과 Schur complement가 같은 소거임을 보여 주며, 후진 복원의 마지막 인자가 $g^L_{11}$이지 그 복소켤레가 아니라는 점도 드러낸다. Retarded 응답을 복원하는 단계에 advanced 인자를 섞으면 직접 역행렬과 달라진다.[2,3]

연결을 끊는 $t=0$ 극한에서는 위 식이 $G^R_{11}=1/a$, $G^R_{22}=1/d$, $G^R_{12}=0$으로 환원된다. 두 전극 사이 전파는 사라지지만 각 사이트의 국소 응답은 남는다. 이 극한은 경계 간 transmission이 0이라는 사실과 소자 안에 상태가 없다는 주장을 구별하는 간단한 시험이다.[2,3]

분모 $ad-|t|^2$는 양쪽 전극과 두 사이트가 함께 만드는 공명을 포함한다. 반면 $1/a$는 오른쪽 사이트를 연결하기 전의 응답이므로 일반적으로 최종 LDOS에 사용할 수 없다. 연결 전 첫 사이트에서 보이지 않던 두 번째 사이트의 영향이 후진 복원의 두 번째 항에 들어간다. 따라서 전진 계산 중 얻은 대각 블록을 바로 최종 소자의 LDOS로 출력하는 구현은 전진 재귀가 정확해도 잘못된 관측량을 낸다.[2,3]

이 예제의 스칼라 식을 실제 행렬에 옮길 때에는 분수를 항별 나눗셈으로 해석하지 않는다. 블록 역연산은 선형계 풀이이며 곱셈 순서를 유지해야 한다. 또한 $G^R_{21}$은 일반적으로 $(G^R_{12})^\dagger$가 아니다. Dagger 관계는 $G^A_{21}=(G^R_{12})^\dagger$이다. 두 사이트에서도 공통 분모가 복소수이므로 이 차이를 확인할 수 있다. 실수 hopping만 시험하면 일부 방향 오류가 가려질 수 있어 복소 hopping을 포함한 작은 계를 별도로 검사하는 것이 유용하다.[2,3]

## 3. 후진 복원과 관측량

### (1) 대각 블록 복원

$G^R_{NN}$을 얻은 뒤 $n=N-1,\ldots,1$ 순서로 되짚는다. 완전히 연결된 대각 블록은

$$
G^R_{nn}
=
g^L_{nn}
+g^L_{nn}V_{n,n+1}G^R_{n+1,n+1}
V_{n+1,n}g^L_{nn}
$$

로 복원할 수 있다. 첫 항은 오른쪽 부분을 아직 연결하지 않은 응답이고, 둘째 항은 $n$번째 slice에서 오른쪽으로 나갔다가 완전한 오른쪽 부분을 거쳐 돌아오는 모든 경로를 더한다.[1–4]

인접한 비대각 블록은

$$
G^R_{n,n+1}
=
g^L_{nn}V_{n,n+1}G^R_{n+1,n+1},
$$

$$
G^R_{n+1,n}
=
G^R_{n+1,n+1}V_{n+1,n}g^L_{nn}
$$

로 얻는다. 이 식들은 전체 역행렬을 만들지 않고 대각 및 인접 블록을 복원한다.[1–4]

### (2) 관측량별 필요 블록

| 관측량 | 주로 필요한 블록 | 계산 전략 |
| --- | --- | --- |
| 두 단자 transmission | $G^R_{1N}$ 또는 경계 블록 | 한 방향 전진과 마지막 경계 연결 |
| slice-resolved LDOS | 모든 $G^R_{nn}$ | $g^L_{nn}$ 저장 후 후진 복원 |
| 전하 밀도 | 모든 $G^<_{nn}$ | retarded 재귀와 주입 상관 재귀 또는 필요한 열 복원 |
| 인접 slice 전류 | $G^<_{n,n+1}$, $G^<_{n+1,n}$ | 인접 비대각 lesser 블록 복원 |
| 여러 단자의 국소량 | 단자별 주입 블록 | geometry-aware slicing 또는 일반 sparse 방법 검토 |

두 단자 transmission의 경계 표현은

$$
\mathcal T(E)=\operatorname{Tr}\!\left[
\Gamma_LG^R_{1N}\Gamma_R(G^R_{1N})^\dagger\right]
$$

이다. 왼쪽 경계 크기가 $M_1$, 오른쪽이 $M_N$이면 $G^R_{1N}$은 $M_1\times M_N$이고 trace 안의 최종 행렬은 $M_1\times M_1$이다. 전극 linewidth $\Gamma_{L/R}$는 해당 경계에 투영한 블록으로 사용한다. 여기서는 Hamiltonian에 포함한 spin 자유도 그대로 transmission을 세며, spin을 생략한 모형의 축퇴도 인자는 전류를 계산할 때 별도로 정한다.[2,3]

이 표현의 차원은 에너지×역에너지×에너지×역에너지이므로 transmission은 무차원이다. 또한 물리적인 전극에서 $\Gamma_{L/R}$가 양의 준정부호이면 $X=\Gamma_L^{1/2}G^R_{1N}\Gamma_R^{1/2}$를 정의하여 $\mathcal T=\operatorname{Tr}(XX^\dagger)\ge0$로 쓸 수 있다. 이 대수적 결과는 구현에서 큰 음의 transmission이나 유의한 허수부를 발견했을 때 경계 블록·dagger·곱 순서를 점검하는 근거가 된다. 다만 양수라는 조건만으로 값의 정확성이 보장되지는 않으므로 직접 역행렬 비교도 필요하다.[2,3]

위상 결맞음을 유지하는 정상 상태에서 점유를 공급하는 항이 평형 전극뿐이라면 전극 $\alpha$의 lesser self-energy는

$$
\Sigma_\alpha^<(E)=i f_\alpha(E)\Gamma_\alpha(E)
$$

이다. RGF 전진·후진 과정에서 전극 경계 $b_\alpha$와 slice $n$ 사이의 블록을 복원하면, 임의의 두 slice에 대한 lesser 블록은

$$
G^<_{mn}(E)
=i\sum_\alpha f_\alpha(E)
G^R_{m b_\alpha}(E)\Gamma_\alpha(E)G^A_{b_\alpha n}(E)
$$

으로 계산할 수 있다. 즉 retarded 재귀가 전파 경로를 만들고, 전극별 $f_\alpha\Gamma_\alpha$가 그 경로에 점유를 주입한다. 모든 $G^<_{mn}$을 조밀하게 만들 필요는 없으며, 전하에는 $m=n$, 인접 slice 전류에는 $m=n\pm1$인 블록만 복원하면 된다.[2,3]

Slice $n$의 단일입자 density-matrix block은

$$
\rho_{nn}
=-\frac{i}{2\pi}\int_{-\infty}^{\infty}G^<_{nn}(E)\,dE
$$

이다. 이 관계는 비상호작용 또는 유효 단일입자 모형에서 전극 주입으로 형성된 산란 상태의 점유를 나타낸다. 전극과 결합하지 않은 진정한 속박 상태가 있으면 $G^R\Sigma^<G^A$만으로 그 점유가 정해지지 않을 수 있으므로 별도의 속박 상태 항과 점유 규약을 확인해야 한다.[2,3]

직교 기저에서 slice $n$의 LDOS는

$$
\operatorname{LDOS}_n(E)
=-\frac{1}{\pi}\operatorname{Im}\operatorname{Tr}G^R_{nn}(E)
$$

으로 계산한다. 궤도별 값을 원하면 trace 대신 해당 대각 원소를 사용한다.[2,3]

국소 전류에는 점유 정보가 필요하므로 $G^R$만으로는 충분하지 않다. 인접 slice 사이의 에너지별 입자 흐름은 사용하는 전하·전류 방향 규약에 맞춰 $V_{n,n+1}G^<_{n+1,n}$과 그 Hermitian counterpart의 조합으로 계산한다. 구현에서는 단자 전류와 모든 내부 단면 전류의 부호 규약을 동일하게 정해야 한다.[1–3]

!!! info "[Measurement]"
    같은 Hamiltonian의 작은 시험계에서는 전체 역행렬 $G_{\mathrm{direct}}^R$와 RGF 블록을 비교한다. 선택한 블록 집합 $\mathcal B$에 대해

    $$
    r_G(E)
    =
    \max_{(m,n)\in\mathcal B}
    \frac{
    \|G^R_{mn,\mathrm{RGF}}-G^R_{mn,\mathrm{direct}}\|_F
    }{
    \max(E_{\mathrm{ref}}^{-1},\|G^R_{mn,\mathrm{direct}}\|_F)
    }
    $$

    를 기록한다. $E_{\mathrm{ref}}>0$는 미리 정한 기준 에너지이다. Green's function의 단위가 에너지의 역수이므로 분모의 두 항을 같은 단위로 맞췄으며, 에너지 단위 변환 때 $E_{\mathrm{ref}}$도 함께 변환한다. $\mathcal B$에는 양 끝 블록, 모든 대각 블록과 몇 개의 인접 비대각 블록을 포함해야 전진과 후진 단계의 오류를 함께 찾을 수 있다.[2–4]

    정상 상태 전류 보존은 단면별 전류 $I_n$으로

    $$
    r_I
    =
    \frac{\max_n|I_n-I_{n-1}|}
    {\max(I_{\mathrm{scale}},\max_n|I_n|)}
    $$

    를 계산해 검사한다. $I_{\mathrm{scale}}$은 평형 또는 무전류 근처에서 분모가 사라지지 않도록 미리 선언한 기준 전류이다. $r_G$는 행렬 재귀의 구현 오류를, $r_I$는 lesser 블록·에너지 적분·전류 부호 규약을 함께 검사한다.[2,3]

## 4. 실제 소자 모사

### (1) Poisson–NEGF 반복

게이트가 있는 소자에서는 운반자 밀도가 electrostatic potential을 바꾸고, 바뀐 전위가 다시 Hamiltonian과 운반자 밀도를 바꾼다. Electrostatic potential을 $\phi(\mathbf r)$, 전자 전하량의 크기를 $e>0$로 두면

$$
\nabla\cdot
\left[
\epsilon(\mathbf r)\nabla\phi(\mathbf r)
\right]
=-\rho_{\mathrm{tot}}(\mathbf r),
$$

$$
\rho_{\mathrm{tot}}
=e\left[p-n+N_D^+-N_A^-\right]+\rho_{\mathrm{fixed}}
$$

로 쓸 수 있다. 전자의 potential energy는 $-e\phi$이므로 local approximation에서는

$$
H_D[\phi]=H_{D,0}-e\phi
$$

로 갱신한다. 다른 부호 규약을 사용한다면 Poisson equation, 전하 밀도와 Hamiltonian 갱신의 부호를 함께 바꿔야 한다.[1,3,6]

Self-consistent calculation은 다음 순서로 진행한다.

1. 단자 바이어스, 정전기적 경계조건과 초기 $\phi^{(0)}$를 정한다.
2. $H_D[\phi^{(k)}]$를 slice별로 구성하고 전극 self-energy를 연결한다.
3. RGF로 필요한 $G^R$, $G^<$ 블록과 전하 밀도 $n^{(k)}(\mathbf r)$를 구한다.
4. Poisson 방정식을 풀어 $\phi_{\mathrm{out}}^{(k)}$를 얻는다.
5. 선형 혼합이나 Newton 계열 방법으로 $\phi^{(k+1)}$를 만들고 반복한다.[1,3,6]

RGF는 3단계의 Green's function 계산을 가속하지만 self-consistency 자체를 대신하지 않는다. 전하–전위 반복의 수렴성과 에너지 적분의 정확도는 별도로 관리해야 한다.[1,3,6]

### (2) 에너지 적분과 수렴

평형 전하 성분은 Green's function의 해석성을 이용한 복소 contour 적분으로 계산할 수 있고, 전극 점유 차이가 만드는 비평형 성분은 일반적으로 실수축 적분이 필요하다. 좁은 공명과 band edge가 있으면 고정된 등간격 격자가 전하나 전류를 놓칠 수 있으므로 적응형 적분 또는 구간 세분화가 필요하다.[3,6]

!!! info "[Measurement]"
    계산 결과에는 전극의 $\mu_\alpha$와 온도, spin 처리, 에너지 적분 구간과 기준, 공간 격자 또는 basis, slice 정의, 전극 principal layer, 전위 혼합 방법과 수렴 기준을 함께 기록한다. 대표 전위 residual은

    $$
    R_\phi^{(k)}
    =
    \max_{\mathbf r}
    \left|
    \phi^{(k+1)}(\mathbf r)-\phi^{(k)}(\mathbf r)
    \right|
    $$

    이다. 마지막 반복에서는 전하 변화, Poisson residual과 각 단면의 전류 불일치도 함께 확인한다.[1,3,6]

### (3) 산란이 있는 계산

Phonon, impurity 또는 다른 산란을 넣으면 retarded와 lesser scattering self-energy가 추가되고, 이 self-energy가 $G^R$와 $G^<$에 의존할 수 있다. 이 경우 Poisson 반복 안에 scattering self-energy 반복이 더해진다. 산란 self-energy의 공간 구조가 block local 또는 짧은 범위이면 RGF 구조를 유지하기 쉽지만, 긴 범위의 조밀한 self-energy는 block-tridiagonal 이점을 약화시킬 수 있다.[1,3]

!!! warning "[Interpretation Caveat]"
    전극 self-energy는 열린 경계를 정확히 포함하는 항이고, scattering self-energy는 선택한 상호작용 근사에 따른 항이다. 두 항을 모두 self-energy라고 부르지만 물리적 역할과 근사 수준이 다르다.[1,3]

## 5. 구현 검증과 방법 선택

### (1) 필수 검증

다음 검사는 서로 다른 오류를 찾으므로 함께 수행한다.[1–4,6]

- **직접 역행렬 비교:** 작은 계에서 경계·대각·인접 블록이 직접 계산과 일치하는가
- **평형 검사:** $\mu_L=\mu_R$와 같은 온도에서 순전류가 수치 오차 안에서 0인가
- **전류 보존:** 전극 외의 입자원·흡수원이 없는 정상 상태에서 모든 내부 단면과 양 단자의 전류가 일치하는가
- **스펙트럼 항등식:** 아래의 유한 $\eta$ 항을 포함한 행렬 항등식과 $\eta\to0^+$ 수렴을 구분하여 검사했는가
- **분할 독립성:** 물리적으로 같은 Hamiltonian을 허용되는 다른 slice로 묶어도 결과가 유지되는가
- **소자 길이 수렴:** 전극과 맞닿는 명시적 완충영역을 늘려도 관심 관측량이 유지되는가
- **적분·격자 수렴:** 에너지 구간, 적분 격자와 공간 discretization을 세분화해도 전하와 전류가 유지되는가

스펙트럼 검증에는 Green 함수 계산에 실제로 사용한 $\eta$를 반영해야 한다. 직교 기저에서 $\Sigma^R=\Sigma_L^R+\Sigma_R^R$, $\Gamma=i(\Sigma^R-\Sigma^{R\dagger})$로 두면, 1절의 역행렬 정의와 $G^A=G^{R\dagger}$로부터

$$
A=i(G^R-G^A)
=G^R\left(\Gamma+2\eta I\right)G^A
$$

를 얻는다. 이는 $G^R-G^A=G^R[(G^A)^{-1}-(G^R)^{-1}]G^A$에 두 역행렬을 대입한 대수적 결과이다.[2,3] 따라서 유한 $\eta$에서 $G^R\Gamma G^A$만 비교한 차이를 재귀 구현의 오류로 판정해서는 안 된다. $\eta\to0^+$에서 속박 상태의 기여가 남는 문제는 3절의 점유 조건과 함께 별도로 다룬다.

### (2) RGF의 적용 한계

RGF는 길고 단면이 제한된 두 단자 또는 준일차원 계에서 특히 효과적이다. 단면이 매우 크거나, 연결 그래프가 여러 갈래로 뻗거나, 다수 단자가 복잡한 위치에 연결되거나, 긴 범위 결합 때문에 큰 slice가 필요하면 일반 sparse direct solver, nested dissection, wave-function 또는 geometry-aware recursive method가 더 적합할 수 있다.[2,4,5]

방법 선택은 전체 행렬 차원만으로 결정하지 않는다. 필요한 Green's function 블록, 연결 그래프, slice 폭, 메모리, 여러 에너지의 병렬성 및 self-consistent 반복 횟수를 함께 고려해야 한다.[2,4,5]

### (3) 비직교 기저

Non-orthogonal basis에서는

$$
\mathcal A(E)
=
(E+i\eta)S_D-H_D-\Sigma_L^R-\Sigma_R^R
$$

를 먼저 block-tridiagonal form으로 나눈다. 대각 블록은 $(E+i\eta)S_{nn}-H_{nn}$, 인접 결합 블록은 $(E+i\eta)S_{n,n+1}-H_{n,n+1}$에서 얻는다. 이후 RGF는 이 energy matrix의 block 소거로 수행한다. Hamiltonian만 slice하고 overlap의 비대각 결합을 빠뜨리면 원래 generalized eigenproblem과 다른 문제가 된다.[3,6]

## 6. 요약

- RGF는 NEGF와 별개의 물리 이론이 아니라 block-tridiagonal 열린 소자 행렬에 적용한 block Gaussian elimination이다.
- 전진 소거는 왼쪽 부분의 효과를 slice별 self-energy로 축약하고, 후진 복원은 LDOS·전하·국소 전류에 필요한 대각 및 인접 블록을 되찾는다.
- 한 에너지당 대표 계산량 $\mathcal O(NM^3)$은 slice 폭 $M$이 고정될 때 길이 $N$에 선형이다.
- 필요한 관측량에 따라 경계 블록만 전파할지, 모든 $g^L_{nn}$을 저장해 국소량을 복원할지 결정해야 한다.
- Poisson–NEGF에서는 RGF가 Green's function 단계를 담당하며, 전하–전위·에너지 적분·산란 self-energy 수렴은 별도로 확인해야 한다.
- 직접 역행렬, 평형, 전류 보존, 분할·소자 길이와 적분 수렴을 함께 검사해야 구현과 물리 모형을 구분해 검증할 수 있다.

## 7. 참고문헌

1. R. Lake, G. Klimeck, R. C. Bowen, and D. Jovanovic, "Single and multiband modeling of quantum electron transport through layered semiconductor devices," *Journal of Applied Physics* **81**, 7845–7869 (1997). [DOI](https://doi.org/10.1063/1.365394).
2. C. H. Lewenkopf and E. R. Mucciolo, "The recursive Green's function method for graphene," *Journal of Computational Electronics* **12**, 203–231 (2013). [DOI](https://doi.org/10.1007/s10825-013-0458-7), [arXiv](https://arxiv.org/abs/1304.3934).
3. X. Waintal, M. Wimmer, A. Akhmerov, C. Groth, B. K. Nikolić, M. Istas, T. Ö. Rosdahl, and D. Varjas, "Computational quantum transport: A scattering approach perspective," *arXiv:2407.16257v3* (2026). [arXiv](https://arxiv.org/abs/2407.16257).
4. S. Kazymyrenko and X. Waintal, "Knitting algorithm for calculating Green functions in quantum systems," *Physical Review B* **77**, 115119 (2008). [DOI](https://doi.org/10.1103/PhysRevB.77.115119).
5. Y. Egami, S. Tsukamoto, and T. Ono, "Efficient calculation of the Green's function in scattering region for electron-transport simulations," *Physical Review Research* **3**, 013038 (2021). [DOI](https://doi.org/10.1103/PhysRevResearch.3.013038), [arXiv](https://arxiv.org/abs/2005.01308).
6. T. Ozaki, K. Nishio, and H. Kino, "Efficient implementation of the nonequilibrium Green function method for electronic transport calculations," *Physical Review B* **81**, 035116 (2010). [DOI](https://doi.org/10.1103/PhysRevB.81.035116), [arXiv](https://arxiv.org/abs/0908.4142).
