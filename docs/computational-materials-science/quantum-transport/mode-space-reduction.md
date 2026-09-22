---
description: NEGF 수송 문제의 국소 mode 기저 구성, 연산자 투영, spurious state 제거, 산란 변환과 full-space 검증을 설명한다.
---

# NEGF: Mode-space reduction

Nonequilibrium Green's function (NEGF) 계산에서 **mode-space reduction**은 수송축에 수직인 자유도 가운데 관심 에너지 구간의 수송에 필요한 부분공간만 남기는 기저 축소 방법이다. Full space의 slice마다 원자 궤도나 격자점이 수천 개이면, 길이 방향 재귀를 사용해도 큰 transverse block의 분해가 병목이 된다. Mode space는 각 block을 더 작은 국소 mode 기저에 투영해 이 병목을 줄인다.[1–4]

이 방법은 유효질량 Hamiltonian의 confinement eigenmode뿐 아니라 다중 궤도 tight-binding (TB), 국소 원자 궤도, [Wannierization](../electronic-structure/wannierization.md)으로 만든 Hamiltonian에도 적용할 수 있다. 다만 작은 기저를 고르는 순간 full-space 문제와 완전히 같은 표현이 아니라 제어해야 할 근사가 된다. 특히 atomistic full-band 모형에서는 관심 band를 잘 맞추는 기저가 오히려 원래 모형에 없는 spurious band를 만들 수 있고, 산란을 포함하면 상호작용 연산자도 같은 부분공간으로 옮겨야 한다.[3,5–10]

이 글은 정상상태 단일입자 [NEGF formalism](negf-formalism.md)을 전제로 한다. 수송축 slice를 $i=1,\ldots,N$으로 표시하고, full-space slice 차원을 $M_i$, retained mode 수를 $m_i$라 한다. 열벡터가 retained basis인 행렬을 $U_i\in\mathbb C^{M_i\times m_i}$로 쓰며, $q>0$는 elementary charge의 크기이다. Conventional current의 양의 방향은 왼쪽 전극 $L$에서 오른쪽 전극 $R$로 정한다.

## 1. Full-space block NEGF

### (1) Energy matrix와 관측량

국소 결합을 가진 소자는 원자층을 묶어 block-tridiagonal form으로 정렬할 수 있다. $z=E+i\eta$와 $\eta\rightarrow0^+$를 두고, overlap이 있는 일반적인 기저의 retarded energy matrix를

$$
\mathcal K^R(E)=zS-H-\Sigma_L^R-\Sigma_R^R-\Sigma_{\mathrm{sc}}^R
$$

로 정의한다. $H$, $S$, $\Sigma_{\mathrm{sc}}^R$가 같은 slice 또는 인접 slice까지만 연결하고 두 contact self-energy가 끝 slice에 작용한다고 하면 구조는

$$
\mathcal K^R=
\begin{pmatrix}
K_{11}-\Sigma_L^R & K_{12} & 0 & \cdots & 0\\
K_{21} & K_{22} & K_{23} & \ddots & \vdots\\
0 & K_{32} & K_{33} & \ddots & 0\\
\vdots & \ddots & \ddots & \ddots & K_{N-1,N}\\
0 & \cdots & 0 & K_{N,N-1} & K_{NN}-\Sigma_R^R
\end{pmatrix},
\qquad
K_{ij}=zS_{ij}-H_{ij}-\Sigma_{\mathrm{sc},ij}^R
$$

이다. 직교 기저에서는 $S=I$이다. 비직교 기저에서는 $H$만 block-tridiagonal로 만드는 것으로 충분하지 않고 $zS-H$ 전체가 같은 연결 범위를 갖도록 slice를 정해야 한다.[9–11]

Green's function과 lesser 성분은

$$
G^R=(\mathcal K^R)^{-1},
\qquad
G^<=G^R\Sigma^<G^A,
\qquad
G^A=(G^R)^\dagger
$$

로 계산한다. 위상 결맞음 두 전극 문제의 transmission과 전류는

$$
T(E)=\operatorname{Tr}\!\left[
\Gamma_LG^R\Gamma_RG^A
\right],
\qquad
I=\frac{q}{h}\int dE\,T(E)\left[f_L(E)-f_R(E)\right]
$$

이며, $\Gamma_\alpha=i(\Sigma_\alpha^R-\Sigma_\alpha^A)$이다. Spin을 Hamiltonian에 명시적으로 포함하지 않았고 두 spin이 축퇴할 때에만 해당 축퇴 인자를 별도로 곱한다. 산란이 있으면 단순한 두 contact Landauer 식 대신 상호작용 self-energy와 일관된 전류식을 사용해야 한다.[1,2,7,8]

### (2) 큰 transverse block의 병목

[Recursive Green's function](recursive-greens-function.md)은 길이 방향 block을 차례로 소거한다. Dense $M_i\times M_i$ block을 쓰면 한 에너지의 대표 연산량은

$$
C_{\mathrm{full}}
\sim \sum_{i=1}^{N}\mathcal O(M_i^3)
$$

이다. $M_i=M$이면 흔히 $\mathcal O(NM^3)$로 쓴다. 이는 전체 $NM$ 차원 행렬을 통째로 역산하는 것보다 길이 확장성이 좋지만, 단면 원자 수와 궤도 수가 늘어 $M$이 커질 때 생기는 cubic block 비용은 남는다.[3,10,11]

Mode-space reduction의 목표는 slice 수 $N$을 줄이는 것이 아니라 $M_i$를 $m_i\ll M_i$로 바꾸는 데 있다. 따라서 mode space와 recursive Green's function (RGF)은 경쟁하는 두 방법이 아니라 서로 다른 층의 가속이다. 먼저 basis를 줄이고, 그 reduced block chain에 RGF를 적용할 수 있다.[2,3,10,11]

## 2. Local mode와 투영

### (1) Slice별 basis

유효질량 모형에서는 각 수송 위치의 confinement Hamiltonian을 풀어 낮은 transverse eigenfunction을 mode로 고른다. 직교 real-space discretization이라면

$$
H_{\perp,i}\phi_{in}=\varepsilon_{in}\phi_{in},
\qquad
U_i=\begin{pmatrix}\phi_{i1}&\cdots&\phi_{im_i}\end{pmatrix},
\qquad
U_i^\dagger U_i=I_{m_i}
$$

로 쓸 수 있다. Atomistic 모형에서는 $H_{\perp,i}$ 하나의 eigenvector만 고르는 대신, 뒤에서 설명할 Bloch mode 표본과 basis completion을 사용한다. 어느 경우든 전체 device transformation은

$$
U=\operatorname{diag}(U_1,U_2,\ldots,U_N)
$$

인 block-diagonal rectangular matrix이다. 모든 $m_i=M_i$이면 단순한 기저 변환이고, $m_i<M_i$이면 retained subspace에 대한 Galerkin approximation이다.[1–4]

Hamiltonian과 overlap은 같은 $U$로

$$
H_r=U^\dagger HU,
\qquad
S_r=U^\dagger SU
$$

로 옮긴다. 아래첨자 $r$은 reduced space를 뜻한다. 비직교 원자 궤도에서는 $U$의 열을 Euclidean norm으로 정규화했다는 이유만으로 $S_r=I$라 두면 안 된다. $S$-metric orthonormalization을 명시적으로 수행하지 않았다면 generalized problem을 그대로 유지한다.[4,9,10]

### (2) Reduced NEGF

Contact와 scattering self-energy도 같은 부분공간에 놓였다고 하자. Reduced retarded Green's function은

$$
G_r^R(E)=
\left[
zS_r-H_r-\Sigma_{L,r}^R-\Sigma_{R,r}^R-\Sigma_{\mathrm{sc},r}^R
\right]^{-1}
$$

이고,

$$
G_r^<=G_r^R\Sigma_r^<G_r^A
$$

이다. Full-space inverse의 retained block이 항상 이 값과 같은 것은 아니다. 이를 보려면 full energy matrix를 retained 공간 $P$와 discarded 공간 $Q$로 나누어

$$
\mathcal K=
\begin{pmatrix}
K_{PP} & K_{PQ}\\
K_{QP} & K_{QQ}
\end{pmatrix}
$$

로 쓴다. 주어진 $z$에서 $K_{QQ}$가 가역이면 $Q$ 행을 소거한 정확한 retained-space 연산자는

$$
K_{\mathrm{eff}}(z)
=K_{PP}(z)-K_{PQ}(z)K_{QQ}^{-1}(z)K_{QP}(z),
\qquad
G_{PP}(z)=K_{\mathrm{eff}}^{-1}(z)
$$

이다. 두 번째 항은 제외 공간을 통한 왕복을 담으며, $K=zS-H-\Sigma$이므로 일반적으로 에너지 의존적이다. 보통의 rectangular Galerkin mode-space 계산은 이 항을 따로 구성하지 않고 $K_{PP}$만 사용하므로, retained modes를 늘려 누락 효과를 수렴시킨다. 이 Schur-complement 소거는 RGF의 block 소거와 같은 선형대수 구조를 보이지만, 여기서는 한 slice 안의 retained/discarded 부분공간에 적용했다.[2,3,10,11] 따라서 full basis limit에서는 정확하지만, truncated basis에서는 에너지 구간과 관측량별 검증이 필요하다.[1–3,5,6]

Full-space self-energy를 이미 계산했다면

$$
\Sigma_{x,r}^{R,<}=U^\dagger\Sigma_x^{R,<}U,
\qquad x\in\{L,R,\mathrm{sc}\}
$$

로 투영한다. 계산량을 줄이기 위해 contact나 scattering 항을 처음부터 mode space에서 구성할 수도 있다. 두 경로가 같은 결과를 내려면 lead–device interface, interaction vertex, overlap과 energy convention이 같은 retained subspace를 나타내야 한다.[1,2,7,9]

### (3) 관측량의 복원

Reduced transmission은 모든 행렬을 같은 subspace에 두고

$$
T_r(E)=\operatorname{Tr}\!\left[
\Gamma_{L,r}G_r^R\Gamma_{R,r}G_r^A
\right]
$$

로 구한다. Transmission은 contact 사이의 전체 전달량이므로 mode cross correlation이 trace 안에 포함된다. 반면 local density of states (LDOS), 전하 밀도와 국소 전류는 원래 궤도 또는 실공간으로 되돌려야 한다.[1,2,10,11]

직교 기저에서 $G^<_{ab}(t,t')=i\langle c_b^\dagger(t')c_a(t)\rangle$ convention을 쓰면 Green's function과 density matrix의 근사 복원은

$$
G^{R,<}_{\mathrm{app}}=UG_r^{R,<}U^\dagger,
\qquad
\rho_r=-\frac{i}{2\pi}\int dE\,G_r^<(E),
\qquad
\rho_{\mathrm{app}}=U\rho_rU^\dagger
$$

이다. 이 convention에서 $-iG^<(t,t)$가 one-particle density matrix이다. 원래 basis function을 $\chi_a(\mathbf r)$라 하면 실공간 전자 밀도는

$$
n(\mathbf r)=
\sum_{ab}\chi_a(\mathbf r)
(\rho_{\mathrm{app}})_{ab}
\chi_b^*(\mathbf r)
$$

로 복원한다. Orthogonal orbital $a$의 LDOS는

$$
D_a(E)=-\frac{1}{\pi}
\operatorname{Im}
\left(G^R_{\mathrm{app}}\right)_{aa}
$$

이다. Non-orthogonal basis에서는 coefficient Green's function, dual basis와 density matrix convention을 함께 고정해야 한다. Total density of states는 $-\pi^{-1}\operatorname{Im}\operatorname{Tr}(SG^R)$처럼 overlap을 포함하며, 원자별 값을 나눌 때에는 Mulliken 등 선택한 population convention을 밝혀야 한다.[1,9,10]

Local current에는 인접 slice의 off-diagonal $G^<_{ij}$가 필요하다. 비직교 기저에서는 current operator에도 $H_{ij}$와 $ES_{ij}$가 정한 같은 boundary convention을 사용해야 한다. 따라서 $G_{r,ii}^<$의 mode-diagonal 원소만 전하로 바꾸거나, mode마다 독립 전류를 더하는 방식은 coupled mode 문제에서 불완전하다. Abrupt confinement에서 cross-mode 항을 빠뜨리면 interface charge가 비물리적으로 솟거나 공간 전류가 보존되지 않을 수 있다.[1,2,7,9,10]

## 3. Coupled mode와 공간 변화

### (1) Interslice coupling

이웃 slice 사이의 reduced block은

$$
H_{r,ij}=U_i^\dagger H_{ij}U_j,
\qquad
S_{r,ij}=U_i^\dagger S_{ij}U_j
$$

이다. $U_i$와 $U_j$의 mode 모양이 다르면 $H_{r,ij}$와 $S_{r,ij}$는 mode 지표에 대해 일반적으로 full matrix이다. 이것이 discrete coupled mode space (CMS)에서 mode 변환과 혼합을 나타낸다. 연속 유효질량 유도에서 basis의 공간 미분으로 나타나는 결합도, 일관된 discretization에서는 이 projected interslice block에 포함된다.[1,2,4]

Uncoupled mode space (UMS)는 서로 다른 mode 또는 mode group 사이의 원소를 추가로 버린다. 예를 들어 선택한 group projector를 $P_g$라 할 때

$$
H_{r,ij}^{\mathrm{UMS}}
=\sum_g P_gH_{r,ij}P_g,
\qquad
S_{r,ij}^{\mathrm{UMS}}
=\sum_g P_gS_{r,ij}P_g
$$

로 block-diagonal approximation을 만든다. 이는 mode-space projection 자체와 별개의 근사이다. 매끄러운 confinement와 약한 disorder에서는 정확할 수 있지만, 급격한 단면·재료·전위 변화, 결함, mode 간 산란에서는 CMS가 필요할 수 있다.[1,2,4,7]

| 표현 | 유지하는 항 | 적합한 조건 | 먼저 확인할 실패 신호 |
| --- | --- | --- | --- |
| Full space | 모든 transverse/orbital 자유도 | 기준 계산, 강한 혼합 | 계산량과 memory |
| CMS | Retained mode 사이의 모든 결합 | 공간 변화, heterostructure, disorder | Window 밖 상태 누락 |
| Grouped mode space | Group 내부 결합과 지정한 group 간 산란 | 대칭이나 band 구조로 group 분리가 검증된 경우 | Group별 전류 합과 full-space 오차 |
| UMS | Mode-diagonal 전파 | 매끄럽고 약하게 변하는 confinement | Interface LDOS, 전류 연속성, off-state 오차 |

이 표의 조건은 선택 규칙이 아니라 검증 가설이다. 같은 장치에서도 bias가 달라져 높은 subband가 채워지거나 산란 channel이 열리면 UMS의 유효성이 달라질 수 있다.[1,2,7,8]

### (2) 위치별 basis와 heterostructure

$m_i$는 모든 slice에서 같을 필요가 없다. 넓은 source/drain에는 mode를 더 남기고 좁은 channel에는 적게 남길 수 있으며, 이때 $H_{r,i,i+1}$은 $m_i\times m_{i+1}$ 직사각 행렬이다. 서로 다른 재료, 결함 또는 표면 거칠기가 있는 구조에서는 cell별 $U_i$를 block-diagonal로 구성해 원래 연결성을 보존할 수 있다.[1,4,7]

다만 basis를 공간마다 독립적으로 고르면 각 basis vector의 phase, 축퇴 부분공간 안의 회전과 mode 순서는 임의적이다. 이 임의성 때문에 $U_i$와 $U_{i+1}$의 개별 열을 그대로 비교해 물리적 불연속을 판정해서는 안 된다. 실제 device 연산자에는 $U_i^\dagger H_{i,i+1}U_{i+1}$와 $U_i^\dagger S_{i,i+1}U_{i+1}$를 사용하고, 그 block의 차원·Hermiticity 관계와 최종 transmission, LDOS, 전하·전류가 full-space 기준에 수렴하는지 검사한다. 서로 다른 크기나 원자 배열의 cell에도 별도 비교 map을 가정하지 않고 이 실제 projected block으로 연결을 정의할 수 있다.[1,4,7]

## 4. Energy window와 atomistic subspace

### (1) 계산 범위에서 출발한 window

Retained basis의 energy window는 평형 band edge만 보고 정하지 않는다. 적어도 contact의 점유 구간, applied bias, 온도 broadening, source-to-drain tunneling 경로와 관측하려는 spectral range를 덮어야 한다. Electron–phonon scattering이 $E$를 $E\pm\hbar\omega_\lambda$에 연결하면 basis와 energy grid도 그 연결을 수용해야 한다.[3,6–8]

이를 범위 조건으로 쓰면

$$
E\in\mathcal W_{\mathrm{solve}},\quad
M^\lambda\ne0
\quad\Longrightarrow\quad
E\pm\hbar\omega_\lambda
\in\mathcal W_{\mathrm{basis}}
$$

이다. 실제로 허용되는 emission과 absorption은 점유, 최종 상태와 phonon mode에 따라 달라지므로 모든 부호가 항상 필요한 것은 아니다. 구간을 넓히면 정확도 가능성은 높아지지만 mode 수와 basis 정리 비용도 증가한다.[3,6–8]

### (2) Physical mode sampling

주기적인 atomistic lead 또는 nanowire unit cell의 intra-cell matrix를 $H_0,S_0$, 이웃 cell 결합을 $W_H,W_S$라 하자. 수송축의 물리적 Bloch wave vector를 $k$, cell period를 $a$라 하면 Bloch 문제는

$$
H(k)\psi_{nk}=\varepsilon_{nk}S(k)\psi_{nk},
$$

$$
H(k)=H_0+W_He^{ika}+W_H^\dagger e^{-ika},
\qquad
S(k)=S_0+W_Se^{ika}+W_S^\dagger e^{-ika}
$$

이다. 따라서 $ka$가 무차원 Bloch phase이고, $k$의 단위는 길이의 역수이다. 관심 window의 physical Bloch states를 Brillouin zone 전체의 여러 $k$에서 모은다. Window 경계에서는 full/reduced model의 real propagating wave vector를 비교하고, 그 사이의 branch는 dense-$k$ band scan으로 확인한다.[3,5,6]

표본을 열로 이어 붙인 $\Phi_0$에는 선형종속 또는 거의 같은 상태가 포함될 수 있다. Orthogonal full basis에서는 singular value decomposition (SVD)

$$
\Phi_0=L\,\operatorname{diag}(\sigma_1,\ldots)R^\dagger
$$

으로 작은 $\sigma_a$ 방향을 제거하고 남은 $L$ 열을 initial basis로 삼을 수 있다. Non-orthogonal full basis에서는 해당 overlap metric으로 Gram matrix를 만들거나 먼저 일관된 generalized orthonormalization을 수행한다. Threshold를 높여 basis를 줄이면 필요한 valley·orbital 조합도 잃을 수 있으므로, singular value 자체가 아니라 band와 transport 오차로 최종 선택을 검증한다.[3–6,9]

### (3) Spurious state와 basis completion

Initial basis가 표본으로 넣은 physical eigenvector를 재현하더라도, projected periodic Hamiltonian의 window 안에 원래 full model에는 없는 branch가 나타날 수 있다. Atomistic multiorbital Hamiltonian에서는 일부 $k$의 eigenvector만 모은 부분공간이 다른 $k$에서 Hamiltonian의 작용에 충분히 닫혀 있지 않기 때문이다.[3,5–7]

Basis completion은 현재 basis $\Phi$의 바깥 방향

$$
Q_\perp=I-\Phi\Phi^\dagger
$$

에서 후보 벡터를 만들고, target window의 unphysical branch를 밖으로 이동시키는 방향을 추가한다. 비직교 기저에서는 이 projector를 그대로 쓰지 않고 chosen metric에 맞는 projector를 사용한다. 이 절차는 physical state를 삭제해 곡선을 맞추는 것이 아니라, 필요한 complement를 더해 reduced operator의 closure를 개선하는 방식이다.[3,5–7]

Window 안의 extra branch를 찾을 때 고정된 몇 $k$점만 비교하면 그 사이의 좁은 spurious branch를 놓칠 수 있다. Periodic one-dimensional band가 정의된 조건에서는 window 직사각형의 경계, 즉 Brillouin-zone 양 끝의 eigenenergy와 window 위·아래 경계에서의 real propagating wave vector를 full/reduced model 사이에 비교하는 방법이 제안되어 있다. 더 일반적인 구조에서는 dense-$k$ scan 또는 eigenvalue count와 mode character 검사를 함께 사용한다.[3,5,6]

| Subspace 단계 | 보존하려는 정보 | 대표 검사 | 실패 시 조치 |
| --- | --- | --- | --- |
| Window 설계 | Bias와 산란이 접근하는 상태 | Contact 점유·$E\pm\hbar\omega$ 범위 | Window 확대 |
| Mode sampling | Valley, band, orbital character | Full-BZ band와 propagating mode | $k/E$ 표본 추가 |
| Rank 정리 | 독립인 physical direction | Singular spectrum와 band 오차 | Threshold 완화 또는 표본 수정 |
| Band completion | Window 안 physical branch만 유지 | Extra/missing band와 mode count | Complement vector 최적화 |
| Device 적용 | 비주기 전위에서 retained closure | $T(E)$, LDOS, 전하, 전류 | Local basis 또는 mode 수 확대 |

## 5. Contact와 scattering self-energy

### (1) Contact projection

비직교 기저에서 device $D$와 lead $\alpha$의 경계 결합을

$$
B_{D\alpha}(z)=H_{D\alpha}-zS_{D\alpha},
\qquad
B_{\alpha D}(z)=H_{\alpha D}-zS_{\alpha D}
$$

로 두면 full-space contact self-energy는

$$
\Sigma_\alpha^R(z)
=B_{D\alpha}(z)g_\alpha^R(z)B_{\alpha D}(z)
$$

이다. 이 식은 문헌에서 $(zS-H)g(zS-H)$로 쓰는 convention과 동치이다. 위처럼 $B=H-zS$로 정의하면 두 경계 인자의 minus sign이 곱에서 상쇄된다. 또한 $z=E+i\eta$일 때 $B_{D\alpha}(z)^\dagger=H_{\alpha D}-z^*S_{\alpha D}$이므로, 유한한 $\eta$와 boundary overlap이 있으면 이것은 $B_{\alpha D}(z)$와 다르다. Retarded self-energy의 두 방향 인자는 같은 $z$로 평가한다.[10] Device와 lead transformation을 각각 $U_D,U_\alpha$라 할 때 reduced interface matrix는

$$
B_{D\alpha,r}=U_D^\dagger B_{D\alpha}U_\alpha
$$

이다. Lead surface Green's function도 $H_{\alpha,r}=U_\alpha^\dagger H_\alpha U_\alpha$와 $S_{\alpha,r}=U_\alpha^\dagger S_\alpha U_\alpha$로 계산한다. 이 방식과 $U_D^\dagger\Sigma_\alpha^RU_D$를 직접 계산하는 방식은 lead의 retained subspace와 경계 결합이 호환될 때 비교할 수 있다.[1,2,4,5,10]

Reduced lead가 target window의 주입 상태를 빠뜨리면 device basis만 넓혀도 transmission을 복원할 수 없다.[1,3,5] 이 글에서는 이를 확인하는 실무 비교로, 같은 energy window에서 full/reduced lead band와 surface spectral density를 먼저 대조하고 이어 같은 device의 $T(E)$를 비교한다. 이것은 단일한 문헌 표준 지표가 아니라, reduced lead self-energy와 open-device 결과를 함께 점검하기 위한 이 글의 검증 순서이다.[5,10]

### (2) Interaction vertex의 변환

전자–phonon 상호작용을 full space에서 $M^\lambda$라 쓰면 reduced vertex는

$$
M_r^\lambda=U^\dagger M^\lambda U
$$

이다. Local deformation-potential 모형처럼 real-space scattering self-energy가 위치별 Green's function 곱으로 주어져도, mode space에서는 일반적으로 여러 mode 지표가 결합한다. Mode 성분을 $U_{a\mu}$라 할 때 대표적인 four-index form factor는

$$
F_{\mu\nu\kappa\lambda}
=\sum_a
U_{a\mu}^*U_{a\nu}
U_{a\kappa}U_{a\lambda}^*
$$

형태이다. 정확한 켤레 배치와 추가 원자·편극 지표는 채택한 interaction Hamiltonian에 따라 정한다.[2,7,8]

Self-consistent Born approximation (SCBA)의 reduced lesser self-energy는 모식적으로

$$
(\Sigma_{\mathrm{sc},r}^<)_{\mu\nu}(E)
=\sum_{\kappa\lambda,\xi}
C_\xi(E)
F^{(\xi)}_{\mu\nu\kappa\lambda}
(G_r^<)_{\kappa\lambda}(E+\Delta E_\xi)
$$

로 쓸 수 있다. $\xi$는 phonon branch와 emission/absorption channel, $C_\xi$는 coupling·점유·정규화 계수, $\Delta E_\xi$는 에너지 이동이다. 구체적인 phonon 정규화와 retarded 성분은 [Electron–phonon coupling](electron-phonon-coupling.md)의 convention을 따른다.[2,7,8]

### (3) 추가 근사의 한계

Full four-index form factor의 저장과 적용은 reduced dimension에도 빠르게 증가할 수 있다. $F_{\mu\nu\kappa\lambda}$의 off-diagonal 항을 버리거나 $\Sigma_{\mathrm{sc}}^R$의 Hermitian 부분을 생략하면 계산은 가벼워지지만, 이것은 mode-space reduction에서 자동으로 따라오는 결과가 아니라 추가 근사이다.[2,7,8]

독립적인 graphene nanoribbon과 atomistic nanowire 연구에서 diagonal form-factor approximation은 일부 조건에서 full-space 결과를 잘 재현했지만, optical-phonon-assisted off-state tunneling이나 mode correlation에는 오차가 커질 수 있었다. Retarded self-energy의 실수부를 빼면 resonance와 band edge 이동도 잃는다. 따라서 ballistic 기준만 맞춘 basis로 dissipative 계산까지 검증했다고 간주하지 않는다.[2,7,8]

!!! warning "산란 계산의 검증 범위"
    산란을 켠 뒤에는 mode/window convergence 외에도 full form factor와 simplified form factor, retarded 실수부의 포함 여부, SCBA 반복 수렴과 정상상태 전류 보존을 따로 검사한다. 한 근사의 성공을 다른 phonon branch, bias 또는 재료에 자동으로 옮기지 않는다.[2,7,8]

## 6. 계산량과 적용 한계

### (1) 조건부 scaling

Dense block RGF를 기준으로 reduced 전파의 대표 비용은

$$
C_{\mathrm{CMS}}
\sim\sum_i\mathcal O(m_i^3),
\qquad
C_{\mathrm{UMS}}
\sim\sum_i\sum_g\mathcal O(m_{ig}^3)
$$

이다. 같은 slice에서 $m_i\ll M_i$이면 큰 이득이 가능하고, 독립 group으로 분해할 수 있으면 cubic 비용의 convexity 때문에 더 줄어든다. 그러나 이 식은 dense factorization만 센다. 실제 wall time에는 basis construction, $U^\dagger HU$ 변환, contact mode, energy integration, Poisson 반복, scattering form factor와 통신 비용이 포함된다.[2,3,6,7,10,11]

| 비용 항목 | Full space | Reduced space에서의 변화 | 지배 조건 |
| --- | --- | --- | --- |
| Device RGF | $\sum_i M_i^3$ | $\sum_i m_i^3$ | 큰 transverse block |
| Block memory | $\sum_i M_i^2$ | $\sum_i m_i^2$ | 저장하는 diagonal/off-diagonal block 수 |
| Basis 생성 | 없음 또는 단순 정렬 | Eigenproblem, sampling, completion | 큰 unit cell과 넓은 window |
| Operator 변환 | 없음 | $U_i^\dagger H_{ij}U_j$ 등 | 긴 결합 범위와 local basis 수 |
| Scattering | 큰 real-space self-energy | Full form factor는 mode 수에 고차 의존 가능 | 많은 mode와 phonon channel |
| Poisson coupling | Full density 복원 | $U\rho_rU^\dagger$ 비용과 memory | 큰 실공간 mesh, 많은 bias 반복 |

따라서 문헌의 수백 배 또는 그 이상의 speedup은 특정 구조·basis·hardware에서 얻은 사례이지 보편 예측식이 아니다. Reduction ratio의 세제곱만으로 실제 speedup을 보고하면 transformation overhead, reduced matrix의 fill-in과 basis 정리 시간을 빠뜨린다.[3,6,7,10]

### (2) 적용이 어려운 경우

Mode space의 이득은 강한 confinement 때문에 transport에 관여하는 mode가 전체 transverse 자유도보다 훨씬 적을 때 크다. 많은 subband가 점유되는 넓은 단면, 금속처럼 넓은 에너지 범위가 필요한 문제, 강한 무질서와 급격한 heterostructure, 비국소 산란이 많은 문제에서는 $m_i$가 커지거나 reduced matrix가 dense해져 이득이 작아진다.[1,2,4,7]

다음 변경은 basis 재사용 전에 재검증해야 한다.

| 변경 | 누락될 수 있는 정보 | 필요한 재검사 |
| --- | --- | --- |
| Bias·온도 범위 확대 | 높은 subband와 tunneling path | Window, $T(E)$, charge/current |
| 새 재료·단면·strain | Valley와 orbital character | Band와 real propagating mode |
| Disorder·defect 추가 | Local mixing과 localized state | LDOS와 CMS–UMS 차이 |
| 새 phonon branch | $E\pm\hbar\omega$ state와 vertex | Scattering window, form factor |
| Contact 변경 | Injection channel과 broadening | Surface spectrum, $\Gamma$, transmission |

## 7. Full-space 기준 검증

### (1) Basis 검증과 transport 검증의 분리

Band가 맞는다는 사실만으로 open-device transport가 맞는 것은 아니다. 먼저 periodic reference에서 retained window의 missing/extra branch, band energy, group velocity와 propagating mode 수를 검사한다. 이어서 full-space 계산이 가능한 짧거나 작은 device에서 동일한 electrostatic potential, contact, energy grid와 scattering model을 사용해 $T(E)$, LDOS, density와 current를 비교한다.[1,3–7]

아래의 $\epsilon_T$, $\epsilon_X$, $\epsilon_I$는 문헌의 단일 표준을 옮긴 식이 아니라, full/reduced 비교를 재현 가능하게 보고하기 위해 이 글에서 제안하는 정규화 정의이다. 실제 허용 오차와 norm, 무전류·무상태 구간의 기준값은 계산 목적에 맞게 사전에 선언한다.

Transmission의 가중 상대 오차 예시는

$$
\epsilon_T=
\frac{
\int_{\mathcal W}dE\,w(E)|T_r(E)-T_f(E)|
}{
\int_{\mathcal W}dE\,w(E)\max[T_f(E),T_{\mathrm{scale}}]
}
$$

이다. 아래첨자 $r,f$는 reduced/full space, $w(E)$는 관심 bias의 점유 차이나 균일 가중치, $T_{\mathrm{scale}}>0$는 transmission이 거의 0인 구간에서 분모가 사라지는 것을 막는 선언된 기준이다. Peak 위치가 중요한 resonant tunneling에서는 이 적분 오차와 peak energy 오차를 함께 보고한다.[1,3,4]

Spatial quantity $X$의 오차는 비교 region $\Omega$에서

$$
\epsilon_X=
\frac{\|X_r-X_f\|_{\Omega}}
{\max(X_{\mathrm{scale}},\|X_f\|_{\Omega})}
$$

로 정의할 수 있다. $X$가 LDOS이면 energy와 공간 범위, 전하이면 단위 cell 또는 원자 population 규약, potential이면 gauge 기준을 함께 기록한다. 서로 다른 population analysis에서 얻은 원자 전하를 같은 수치처럼 비교하지 않는다.[1,4,7,9]

### (2) 수렴 순서

검증은 다음 순서로 수행하면 어느 선택이 오차를 만들었는지 분리하기 쉽다.[1–7]

1. Full-space lead/device의 band, contact spectrum과 energy grid를 먼저 수렴시킨다.
2. 같은 geometry에서 mode sampling을 늘려 missing physical branch가 사라지는지 확인한다.
3. Basis completion 뒤 target window 전체에서 spurious branch가 없는지 확인한다.
4. Ballistic CMS의 $T(E)$와 LDOS를 full space와 비교한다.
5. Spatial density와 인접 slice current를 복원해 Poisson self-consistency와 전류 연속성을 비교한다.
6. Mode/group을 줄인 UMS 결과를 CMS와 비교해 decoupling 오차를 분리한다.
7. Scattering을 켠 뒤 vertex/form factor, energy sideband와 self-energy 반복을 다시 수렴시킨다.

정상상태 slice current의 보존 오차는

$$
\epsilon_I=
\frac{
\max_i|I_{i+1/2}-\overline I|
}{
\max(I_{\mathrm{scale}},|\overline I|)
},
\qquad
\overline I=\frac{1}{N-1}\sum_{i=1}^{N-1}I_{i+1/2}
$$

로 기록할 수 있다. 산란 self-energy가 전하 보존형이어야 한다는 조건과 수치 반복이 충분히 수렴했다는 조건을 mode truncation 오차와 구별한다.[1,2,7,8]

!!! info "[Verification]"
    최종 보고에는 full/reduced dimension, basis window, sampled $k$와 energy, rank threshold, completion 종료 조건, CMS 또는 UMS 선택, contact basis, scattering approximation, energy grid와 Poisson/SCBA tolerance를 남긴다. Mode 수나 window를 늘렸을 때 $T(E)$, LDOS, 총전하와 전류가 설정한 허용 오차 안에서 더 이상 변하지 않는지 확인한다.[3–8]

## 8. 인접 방법과의 구별

### (1) Wannierization과 mode space

[Wannierization](../electronic-structure/wannierization.md)은 주기적 Bloch band의 gauge와, entangled band이면 부분공간을 정해 국소화된 Wannier basis와 interpolation Hamiltonian을 만드는 과정이다. 고정된 band subspace 안의 Bloch–Wannier 변환은 square unitary representation change이며, maximally localized Wannier function은 real-space spread를 목적 함수로 삼는다.[12,13]

Mode-space reduction은 열린 device NEGF에서 수송에 필요한 state만 남기기 위해 rectangular $U$를 사용하는 reduced-order step이다. 목적 함수는 Wannier spread가 아니라 target transport window의 band와 observable 정확도이다. 따라서 Wannier Hamiltonian은 mode-space 계산의 full-space 입력이 될 수 있지만, wannierization을 했다는 사실만으로 mode-space reduction이 끝난 것은 아니다.[3–7,12,13]

### (2) Recursive Green's function과 mode space

RGF는 block-tridiagonal matrix의 필요한 inverse block을 Schur complement로 계산하는 선형대수 알고리즘이다. 같은 basis를 유지하므로, 정확한 block arithmetic에서는 full inverse의 해당 block과 같다. Mode-space truncation은 block 안의 Hilbert-space dimension을 줄이며 오차 검증이 필요한 model reduction이다.[2,3,10,11]

| 방법 | 바꾸는 대상 | 주된 목적 | 고유한 검증 질문 |
| --- | --- | --- | --- |
| Wannierization | Bloch subspace의 gauge·국소 basis | 국소화와 interpolation | Band/subspace와 spread가 맞는가? |
| Mode-space reduction | Device block의 retained subspace | NEGF block dimension 축소 | Window의 transport observable이 수렴하는가? |
| RGF | Block chain의 소거 순서 | 필요한 Green block의 효율적 계산 | Algebra와 current reconstruction이 맞는가? |

이 세 방법은 연속해서 사용할 수 있다. 예를 들어 first-principles band에서 Wannier Hamiltonian을 만들고, 그 atomistic block을 transport mode space로 줄인 뒤, reduced NEGF를 RGF로 푼다. 각 단계의 오차와 수렴 조건은 서로 대신하지 않는다.[3,4,9–13]

## 9. 요약

- Mode-space reduction은 full-space slice의 transverse/orbital 자유도를 transport window의 local subspace로 줄이는 방법이며, truncated basis에서는 제어해야 할 근사이다.
- $H$, $S$, contact, scattering self-energy와 관측량을 모두 같은 basis convention으로 변환해야 한다. Spatial LDOS·전하·전류에는 mode cross correlation을 포함한 복원이 필요하다.
- UMS는 weak mode mixing을 가정하는 추가 근사이고, 공간적으로 급격한 구조·전위·disorder에는 CMS와의 비교가 필요하다.
- Atomistic basis는 full-BZ physical mode sampling, rank 정리와 spurious-band completion을 거쳐야 하며, energy window는 bias와 inelastic sideband까지 포함해야 한다.
- 계산 이득은 $M_i$에서 $m_i$로 줄어든 block 크기에 달려 있지만, basis 생성·변환·산란 form factor와 self-consistency 비용을 포함해 측정해야 한다.
- 최종 검증은 full-space band, transmission, LDOS, charge/current와 전류 보존을 기준으로 mode 수·window·산란 근사를 각각 수렴시키는 과정이다.

## 10. 참고문헌

1. M. Luisier, A. Schenk, and W. Fichtner, “Quantum transport in two- and three-dimensional nanoscale transistors: Coupled mode effects in the nonequilibrium Green’s function formalism,” *Journal of Applied Physics* **100**, 043713 (2006). [DOI: 10.1063/1.2244522](https://doi.org/10.1063/1.2244522). [Author-hosted full text](https://iis-people.ee.ethz.ch/~schenk/JApplPhys_100_043713.pdf).
2. R. Grassi, A. Gnudi, I. Imperiale, E. Gnani, S. Reggiani, and G. Baccarani, “Mode space approach for tight-binding transport simulations in graphene nanoribbon field-effect transistors including phonon scattering,” *Journal of Applied Physics* **113**, 144506 (2013). [DOI: 10.1063/1.4800900](https://doi.org/10.1063/1.4800900). [arXiv:1302.0694](https://arxiv.org/abs/1302.0694).
3. J. Z. Huang, H. Ilatikhameneh, M. Povolotskyi, and G. Klimeck, “Robust Mode Space Approach for Atomistic Modeling of Realistically Large Nanowire Transistors,” *Journal of Applied Physics* **123**, 044303 (2018). [DOI: 10.1063/1.5010238](https://doi.org/10.1063/1.5010238). [arXiv:1710.08064](https://arxiv.org/abs/1710.08064).
4. M. Shin, “Hetero-structure Mode Space Method for Efficient Device Simulations,” *Journal of Applied Physics* **130**, 104303 (2021). [DOI: 10.1063/5.0064314](https://doi.org/10.1063/5.0064314). [arXiv:2107.10511](https://arxiv.org/abs/2107.10511).
5. G. Mil’nikov, N. Mori, and Y. Kamakura, “Equivalent transport models in atomistic quantum wires,” *Physical Review B* **85**, 035317 (2012). [DOI: 10.1103/PhysRevB.85.035317](https://doi.org/10.1103/PhysRevB.85.035317).
6. A. Afzalian, T. Vasen, P. Ramvall, T.-M. Shen, J. Wu, and M. Passlack, “Physics and performances of III–V nanowire broken-gap heterojunction TFETs using an efficient tight-binding mode-space NEGF model enabling million-atom nanowire simulations,” *Journal of Physics: Condensed Matter* **30**, 254002 (2018). [DOI: 10.1088/1361-648X/aac156](https://doi.org/10.1088/1361-648X/aac156). [Earlier preprint with a different title: arXiv:1705.00909](https://arxiv.org/abs/1705.00909).
7. D. A. Lemus, J. Charles, and T. Kubis, “Mode-space-compatible inelastic scattering in atomistic nonequilibrium Green’s function implementations,” *Journal of Computational Electronics* **19**, 1389–1398 (2020). [DOI: 10.1007/s10825-020-01549-8](https://doi.org/10.1007/s10825-020-01549-8). [arXiv:2003.09536](https://arxiv.org/abs/2003.09536).
8. H. S. Pal, D. E. Nikonov, R. Kim, and M. S. Lundstrom, “Electron–phonon scattering in planar MOSFETs: NEGF and Monte Carlo methods,” arXiv:1209.4878 (2012). [arXiv:1209.4878](https://arxiv.org/abs/1209.4878).
9. M. Shin, W. J. Jeong, and J. Lee, “Density functional theory based simulations of silicon nanowire field effect transistors,” *Journal of Applied Physics* **119**, 154505 (2016). [DOI: 10.1063/1.4946754](https://doi.org/10.1063/1.4946754).
10. T. Ozaki, K. Nishio, and H. Kino, “Efficient implementation of the nonequilibrium Green function method for electronic transport calculations,” *Physical Review B* **81**, 035116 (2010). [DOI: 10.1103/PhysRevB.81.035116](https://doi.org/10.1103/PhysRevB.81.035116). [arXiv:0908.4142](https://arxiv.org/abs/0908.4142).
11. C. H. Lewenkopf and E. R. Mucciolo, “The recursive Green’s function method for graphene,” *Journal of Computational Electronics* **12**, 203–231 (2013). [DOI: 10.1007/s10825-013-0458-7](https://doi.org/10.1007/s10825-013-0458-7). [arXiv:1304.3934](https://arxiv.org/abs/1304.3934).
12. N. Marzari, A. A. Mostofi, J. R. Yates, I. Souza, and D. Vanderbilt, “Maximally localized Wannier functions: Theory and applications,” *Reviews of Modern Physics* **84**, 1419–1475 (2012). [DOI: 10.1103/RevModPhys.84.1419](https://doi.org/10.1103/RevModPhys.84.1419). [arXiv:1112.5411](https://arxiv.org/abs/1112.5411).
13. J. Kuneš, “Wannier Functions and Construction of Model Hamiltonians,” in *The LDA+DMFT approach to strongly correlated materials*, E. Pavarini, E. Koch, D. Vollhardt, and A. Lichtenstein (eds.), Modeling and Simulation Vol. 1, Forschungszentrum Jülich (2011), Chapter 4. ISBN 978-3-89336-734-4. [Full text](https://www.cond-mat.de/events/correl11/manuscripts/kunes.pdf).
