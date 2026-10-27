---
description: LCAO localized basis의 전체 Hamiltonian·overlap 행렬에서 출발하여 전극 chemical potential, self-energy, spectral function, nonequilibrium 점유, 전류와 DFT-NEGF 자기일관 계산을 연결한다.
---

# NEGF formalism

Nonequilibrium Green's function (NEGF)은 반무한 전극에 연결된 소자의 전자 상태와 비평형 점유, 단자 전류를 일관되게 계산하는 방법이다. 닫힌 계의 DFT에서는 하나의 Fermi level을 기준으로 고유상태를 채우지만, 열린 소자에서는 **왼쪽 전극에서 주입된 상태와 오른쪽 전극에서 주입된 상태가 각 전극의 Fermi 분포를 따른다.** 따라서 같은 에너지에서도 두 전극과의 결합에 따라 소자 내부의 점유가 달라질 수 있다. NEGF는 전극의 영향을 self-energy로 포함하여 전자 상태를 계산하고, lesser Green's function에서 구한 전자 밀도로 Kohn–Sham (KS) Hamiltonian을 갱신할 수 있게 한다.[1–5]

이 문서는 SIESTA/TranSIESTA와 같은 **localized linear combination of atomic orbitals (LCAO)** 계산을 기본 모형으로 사용한다. 처음부터 일반적인 비직교 overlap 행렬 $S$를 포함하고, 식이 단순해지는 경우에만 $S=I$인 정규직교 기저로 제한한다. 좌우 전극을 $L,R$, 소자 영역을 $D$로 표기한다. 그리스 문자 **$\alpha\in\{L,R\}$는 전극을 선택하는 지표**, **$\mu,\nu$는 localized basis orbital을 선택하는 지표**이다. 전극의 electrochemical potential은 $\mu_\alpha$로 적는데, 여기의 아래첨자 $\alpha$는 orbital 지표 $\mu,\nu$와 서로 다른 역할을 한다. 각 기호의 물리적 의미와 정의를 필요한 절에서 다시 확인한다.[4,5]

전자는 전하 $-e$를 가지며 $e>0$이다. 이 글에서는 $I_\alpha>0$을 전극 $\alpha$에서 소자로 들어오는 **전자 입자 flux에 $+e$를 곱한 값**으로 정의한다. 따라서 이는 전자가 운반하는 실제 음전하의 방향과 반대인 전류 부호 규약이다. Spin을 행렬의 자유도로 포함한 경우에는 추가로 spin 축퇴 인자 2를 곱하지 않는다. 기본 전개는 정상 직류, 비상호작용 전극, 유효 단일입자 KS Hamiltonian과 coherent 수송을 기준으로 한다. 내부 산란 self-energy를 넣는 일반화는 필요한 곳에서 구분한다.[1–3]

## 1. Localized LCAO 기저와 전극–소자 분할

### (1) 원자 궤도에서 Hamiltonian 행렬까지

원자 규모의 소자를 기술할 때에는 원자 주변에 국소화된 basis function $|\phi_\mu\rangle$를 사용한다. 하나의 원자에 여러 s, p, d 또는 polarization orbital이 포함될 수 있으므로, **$\mu$는 원자 번호가 아니라 전체 basis orbital 번호**이다. 전자 상태를 $|\psi\rangle=\sum_\mu c_\mu|\phi_\mu\rangle$로 전개하면 전자구조 문제는 다음 일반화된 고유값 문제로 표현된다.[4,5]

$$
H_{\mu\nu}=\langle\phi_\mu|\hat H_{\mathrm{KS}}|\phi_\nu\rangle,\qquad
S_{\mu\nu}=\langle\phi_\mu|\phi_\nu\rangle,\qquad
H\mathbf c_n=\varepsilon_n S\mathbf c_n.
$$

$H_{\mu\nu}$는 orbital $\nu$와 $\mu$ 사이의 Hamiltonian matrix element이고, $S_{\mu\nu}$는 두 orbital의 overlap이다. Localized AO들은 서로 겹칠 수 있으므로 일반적으로 $S_{\mu\nu}\ne\delta_{\mu\nu}$이다. 고유벡터는 $\mathbf c_n^\dagger S\mathbf c_n=1$로 정규화한다. 이 문서에서 아래첨자 $\mu,\nu$가 붙은 $H$, $S$, $G$, $P$는 모두 **동일한 localized basis에서 표현한 행렬**이다. $H$와 $S$에는 각각 에너지와 무차원의 단위가 부여된다.

수송 방향을 따라 전체 계를 왼쪽의 반무한 전극 $L$, 명시적으로 계산하는 유한 영역 $D$, 오른쪽의 반무한 전극 $R$로 나눈다. Localized basis를 세 영역별로 정렬하면 **full Hamiltonian과 overlap 행렬**은 다음과 같다.[4,5]

$$
H_{\mathrm{full}}=
\begin{pmatrix}
H_L&H_{LD}&0\\
H_{DL}&H_D&H_{DR}\\
0&H_{RD}&H_R
\end{pmatrix},
\qquad
S_{\mathrm{full}}=
\begin{pmatrix}
S_L&S_{LD}&0\\
S_{DL}&S_D&S_{DR}\\
0&S_{RD}&S_R
\end{pmatrix}.
$$

$H_D,S_D$는 $D$에 포함된 $N_D$개 orbital의 유한 $N_D\times N_D$ 행렬이다. $H_\alpha,S_\alpha$는 전극 $\alpha=L,R$의 반무한 행렬이며, $H_{D\alpha},S_{D\alpha}$는 소자와 해당 전극에 속한 orbital 사이의 결합 및 overlap 블록이다. 이 두 full matrix에서 $L$–$R$ 직접 결합을 0으로 둔 이유는 양 전극의 상호작용을 유한 영역 $D$를 통해 모두 포함하도록 분할했기 때문이다. 더 멀리까지 미치는 Hamiltonian 또는 overlap 결합이 있으면 principal layer나 소자 영역을 확대해야 한다.[4,5]

| 표기 | 정의 | 이후 식에서의 역할 |
| --- | --- | --- |
| $\mu,\nu$ | Localized AO 번호 | $H_{\mu\nu}$, $S_{\mu\nu}$, $G_{\mu\nu}$, $P_{\mu\nu}$의 행·열 |
| $L,D,R$ | 왼쪽 전극, 유한 소자, 오른쪽 전극 | Full matrix의 block 분할 |
| $\alpha$ | 전극 지표, $\alpha=L$ 또는 $R$ | $\Sigma_\alpha$, $\Gamma_\alpha$, $f_\alpha$, $I_\alpha$ |
| $\mu_L,\mu_R$ | 전극별 electron electrochemical potential | Reservoir의 Fermi 점유 결정 |
| $E,z=E+i\eta$ | 실제 전자 에너지, retarded 복소 에너지 | Green's function의 energy argument |
| $G^R,G^A,G^<$ | 전파 응답, advanced 응답, 점유 상관 | Spectral weight와 density kernel |
| $P_{\mu\nu}$ | Density kernel의 orbital matrix element | 실공간 전자 밀도 복원 |

유한 영역에는 분자·결함뿐 아니라 접촉부에서 전하와 전위가 변하는 전극의 일부 원자층도 포함한다. 소자와 반무한 전극의 경계가 충분히 bulk-like한 곳에 놓여야, 반복 전극에서 얻은 self-energy와 소자 경계의 Hamiltonian·overlap이 일관된다. 이러한 분할의 개념을 아래 그림에 나타냈다.[4,5]

<figure markdown="span">
![검은 유한 scattering region에 세 붉은 반무한 전극이 연결되고 각 전극의 첫째와 둘째 반복 셀이 진한 색과 옅은 색으로 표시된 모식도](images/negf-device-lead-partition.png)
<figcaption markdown="1">
그림 1. 검은 영역은 명시적으로 계산하는 유한 영역, 붉은 영역은 반무한 전극이다. 원도는 lead 0, 1, 2의 세 단자이며, 아래 유도는 그중 일반적인 두 단자 구조를 별도로 가정한다. 출처: X. Waintal et al., “Computational quantum transport: A scattering approach perspective,” arXiv:2407.16257v3, Fig. 3, p. 17, [원문](https://arxiv.org/abs/2407.16257v3), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). 수정하여 재현: PDF의 그림 영역만 발췌하여 PNG로 변환했으며 색과 레이블은 변경하지 않았다.[1]
</figcaption>
</figure>

원래 그림은 세 단자 사례를 보여 주지만, 이하의 유도에서는 그중 두 단자인 $L$–$D$–$R$을 사용한다. 전극은 첫 번째 경계 셀 뒤에도 무한히 반복되므로 첫 셀만 계산하고 끝내면 열린 경계조건을 잃게 된다. 다음 절에서는 이 반무한 반복 구조의 영향을 $D$에 작용하는 self-energy로 바꾼다.[1,5]

### (2) 전극의 electrochemical potential과 인가 전압

각 전극은 커다란 electron reservoir와 연결되어 있고, 내부에서는 국소 열평형을 유지한다. 전극 $\alpha$의 electron electrochemical potential $\mu_\alpha$는 **그 전극의 전자 점유를 구분하는 Fermi level(에너지 단위)**이며, 온도 $T_\alpha$와 함께 Fermi–Dirac 분포 $f_\alpha(E)$를 결정한다. 평형에서는 $\mu_L=\mu_R=E_F$이고, 두 전극 사이에 bias를 인가하면 일반적으로 $\mu_L\ne\mu_R$가 된다.[2–5]

아래에서는 에너지 차이를 전압으로 환산한 bias를

$$
V_b\equiv\frac{\mu_L-\mu_R}{e}
$$

로 **정의**한다. 따라서 $V_b>0$이면 $\mu_L>\mu_R$이며, 동일 온도에서 그 사이 에너지에 있는 상태는 왼쪽 전극의 주입이 더 많아질 수 있다. 예를 들어 평형 Fermi energy를 $E_F$로 잡고 대칭 bias를 사용하면 $\mu_L=E_F+eV_b/2$, $\mu_R=E_F-eV_b/2$이다. 이것은 전자 에너지 차이에 대한 부호 규약이다. 물리적 electrostatic voltage $\varphi_L-\varphi_R$와 비교할 때에는 전자의 potential energy가 $-e\varphi$라는 점과 전극의 work function, 접촉 전위를 함께 고려해야 한다.[4,5]

**전극의 $\mu_\alpha$와 소자 내 한 orbital의 onsite energy $\varepsilon_\mu$는 다른 물리량이다.** $\mu_\alpha$는 reservoir의 경계조건이며, $\varepsilon_\mu$는 Hamiltonian으로부터 얻는 전자 상태의 에너지이다. 특히 두 전극에 서로 다른 Fermi 분포가 존재하는 coherent 비평형 소자에는 모든 orbital에 공통으로 적용할 단 하나의 소자 chemical potential을 일반적으로 정의할 수 없다. 따라서 뒤에서는 소자 점유를 전극별 주입으로 계산한다.[2–5]

## 2. Retarded Green's function과 열린 경계

### (1) Localized basis의 Green's function

제1절의 일반화된 고유값 문제 $H_D\mathbf c=E S_D\mathbf c$를 에너지 $E$에서의 선형 응답 문제로 생각하자. 에너지 차원의 작은 양수 $\eta>0$로 복소 에너지 $z=E+i\eta$를 정의하고, 소자 orbital 공간의 외부 source 벡터를 $\mathbf b$라 쓰면 다음과 같다.[1–3,5]

$$
(zS_D-H_D)\mathbf c=\mathbf b,\qquad
\mathbf c=G_0^R(E)\mathbf b,\qquad
G_0^R(E)=(zS_D-H_D)^{-1}.
$$

아래첨자 0은 **아직 전극에 연결하지 않은 고립 소자**를 의미하고, 위첨자 $R$은 retarded Green's function을 의미한다. 행렬 원소 $G^R_{0,\mu\nu}(E)$는 $\nu$번째 orbital 성분의 source에 대한 $\mu$번째 orbital 성분의 응답이다. 따라서 $G^R$는 하나의 물리적 orbital이나 고유상태가 아니라, 선택한 모든 localized basis를 연결하는 $N_D\times N_D$ 행렬이다. 이 설명에서 $\mu,\nu$는 모두 $D$에 속한 orbital 번호이다.

$+i\eta$는 시간상 나중에 발생하는 응답을 선택하는 retarded boundary condition이며, 실제 물리식에는 $\eta\to0^+$의 극한을 사용한다. 전극으로의 탈출에 따른 물리적 broadening은 다음 절에서 정의할 $\Gamma_L,\Gamma_R$가 결정한다. 수치적 $\eta$를 크게 사용하면 상태가 인위적으로 넓어질 수 있으므로 두 효과를 구분해야 한다.[1–3]

고립 소자의 고유벡터 $\mathbf c_m$을 $\mathbf c_m^\dagger S_D\mathbf c_n=\delta_{mn}$로 정규화하면, 완결된 유한 기저 안에서 Green's function은 다음과 같이 전개된다.[4,5]

$$
G_0^R(E)=\sum_m\frac{\mathbf c_m\mathbf c_m^\dagger}{E-\varepsilon_m+i\eta}.
$$

분모는 고립 소자의 고유에너지 $\varepsilon_m$에 대한 응답을, 분자의 바깥곱 $\mathbf c_m\mathbf c_m^\dagger$는 해당 상태가 여러 AO에 어떻게 분포하는지를 나타낸다. 따라서 $G^R_{0,\mu\nu}$에는 서로 다른 localized orbital 사이의 혼합도 포함된다. 정규직교 기저를 쓰면 $S_D=I_D$가 되어 익숙한 $(zI_D-H_D)^{-1}$을 회복한다.

### (2) 두 전극에 연결된 소자의 Green's function

실제 NEGF에서는 전자가 $D$에서 왼쪽·오른쪽 전극으로 이동한 뒤 전극의 연속 상태에 흡수될 수 있다. 이 영향을 소자 orbital 공간의 retarded self-energy $\Sigma_\alpha^R(E)$에 포함하면, 앞의 고립 소자 Green's function은 다음의 **열린 소자 Green's function**으로 바뀐다.[1–5]

$$
G^R(E)=
\left[
zS_D-H_D-\Sigma_L^R(E)-\Sigma_R^R(E)
\right]^{-1},\qquad
G^A(E)=[G^R(E)]^\dagger.
$$

여기서 $\Sigma_L^R$와 $\Sigma_R^R$는 **각각 왼쪽 전극과 오른쪽 전극의 영향**이다. 보다 간결하게 쓸 때 $\sum_{\alpha=L,R}\Sigma_\alpha^R$로 표기한다. 즉, 이 문서의 $\alpha$는 언제나 $L$ 또는 $R$을 대신하는 전극 지표이다. $H_D,S_D,G^R,\Sigma_\alpha^R$는 모두 $N_D\times N_D$ 행렬이며, 예를 들어 $G_{\mu\nu}^R$와 $(\Sigma_\alpha^R)_{\mu\nu}$의 $\mu,\nu$는 동일한 소자 basis를 가리킨다.

Advanced Green's function $G^A$는 retarded Green's function의 Hermitian conjugate로 정의한다. 이 두 행렬을 사용하여 상태의 spectral weight와 실제 점유를 계산한다. $\Sigma_\alpha^R$가 복소수 행렬이고 에너지에 의존할 수 있으므로, 전극에 연결된 공명 준위는 고립계 고유에너지에서 이동하거나 폭을 가질 수 있다. 다음 절에서는 full $H,S$로부터 이 self-energy가 어떻게 나오는지 유도한다.

## 3. 전극 self-energy와 broadening

### (1) Full Hamiltonian·overlap의 전극 자유도 소거

제1절에서 정의한 **full Hamiltonian $H_{\mathrm{full}}$과 overlap $S_{\mathrm{full}}$**로 돌아가자. 두 행렬은 localized orbital을 $L,D,R$ 순서로 정렬한 것이며, 그 차이인 energy matrix는 다음 블록 구조를 갖는다.[4,5]

$$
\mathcal K(z)\equiv zS_{\mathrm{full}}-H_{\mathrm{full}}
=
\begin{pmatrix}
zS_L-H_L&zS_{LD}-H_{LD}&0\\
zS_{DL}-H_{DL}&zS_D-H_D&zS_{DR}-H_{DR}\\
0&zS_{RD}-H_{RD}&zS_R-H_R
\end{pmatrix}.
$$

전극의 자유도를 제거할 때 필요한 전체 Green's function은 $G_{\mathrm{full}}^R=\mathcal K^{-1}$이다. 여기서 $G_{DD}^R$는 full Green's function 중 소자 orbital의 행과 열에 해당하는 유한 블록을 뜻한다. 전극 $\alpha=L,R$에 대해서는 $K_{\alpha\alpha}=zS_\alpha-H_\alpha$, $K_{D\alpha}=zS_{D\alpha}-H_{D\alpha}$라고 표기할 수 있다.

$\mathcal K G_{\mathrm{full}}^R=I$에서 소자 열을 선택하면, 전극 $\alpha$에 해당하는 행은 다음을 만족한다.

$$
K_{\alpha\alpha}G_{\alpha D}^R
+K_{\alpha D}G_{DD}^R=0.
$$

이 방정식을 $G_{\alpha D}^R$에 대해 풀면 $G_{\alpha D}^R=-(K_{\alpha\alpha})^{-1}K_{\alpha D}G_{DD}^R$이다. 전극 내부의 무한한 자유도가 $G_{DD}^R$에 미치는 영향을 이 식으로 대체할 수 있다. 이를 전체 행렬의 소자 행에 대입하면 다음 Schur complement를 얻는다.[4,5]

$$
\left[
zS_D-H_D
-\sum_{\alpha=L,R}K_{D\alpha}
 (zS_\alpha-H_\alpha)^{-1}K_{\alpha D}
\right]G_{DD}^R=I_D.
$$

따라서 $G^R\equiv G_{DD}^R$와 $\widetilde g_\alpha^R=(zS_\alpha-H_\alpha)^{-1}$를 정의하면, 전극 self-energy는 아래와 같다.

$$
\Sigma_\alpha^R(z)=
 (H_{D\alpha}-zS_{D\alpha})
 \widetilde g_\alpha^R(z)
 (H_{\alpha D}-zS_{\alpha D}).
$$

앞의 두 괄호는 full energy matrix의 off-diagonal block에 각각 마이너스 부호를 붙인 것이므로 Schur complement의 전체 부호가 일치한다. 즉, $H_D$에서 전극 원자와 전극–소자 결합을 단순히 삭제하는 대신, **전극의 무한한 응답을 유한한 self-energy 행렬로 정확히 접어 넣은 결과**이다. 이 소거는 주어진 single-particle $H,S$에 대해서 정확하며, KS 근사 자체의 정확성까지 보장하는 주장은 아니다.[4,5]

### (2) Surface Green's function과 orbital별 결합

실제 소자 orbital과 직접 결합하는 것은 각 전극의 첫 번째 principal layer에 있는 orbital들이다. 따라서 $\widetilde g_\alpha^R$ 전체를 저장하는 대신 전극의 경계 orbital에 해당하는 **surface Green's function** $g_{\alpha,s}^R$만 계산한다. 소자와 경계 orbital 사이의 결합을 $C_{D\alpha}(z)=H_{D\alpha}-zS_{D\alpha}$로 정의하면 self-energy는 다음과 같이 쓸 수 있다.[4,5]

$$
\Sigma_\alpha^R(z)
=C_{D\alpha}(z)\,
g_{\alpha,s}^R(z)\,
C_{\alpha D}(z),\qquad
C_{\alpha D}(z)=H_{\alpha D}-zS_{\alpha D}.
$$

이 식에서 $C_{D\alpha}$는 $N_D\times N_{\alpha,s}$, $g_{\alpha,s}^R$는 $N_{\alpha,s}\times N_{\alpha,s}$ 행렬이다. 결과인 $\Sigma_\alpha^R$의 크기는 $N_D\times N_D$가 된다. 여기서 $N_{\alpha,s}$는 전극 경계 principal layer의 orbital 수이다. 앞서 사용한 $\alpha$는 여전히 **전극의 종류**이며, orbital 번호는 $\mu,\nu$를 계속 사용한다.

예를 들어 소자 orbital $\mu,\nu\in D$에 대한 self-energy 성분은 다음과 같다. 합의 지표 $p,q$는 해당 전극 경계의 localized orbital을 가리킨다.

$$
(\Sigma_\alpha^R)_{\mu\nu}
=\sum_{p,q\in\alpha\text{ surface}}
(C_{D\alpha})_{\mu p}
(g_{\alpha,s}^R)_{pq}
(C_{\alpha D})_{q\nu}.
$$

따라서 전극 하나에 연결되어 있어도 여러 소자 orbital 사이에 self-energy의 비대각 성분이 생길 수 있다. Surface Green's function은 반무한 전극 전체를 고려한 경계 응답이며, **고립된 첫 번째 원자층의 Hamiltonian 역행렬이 아니다.** 구체적인 반복·decimation 계산은 [Surface Green's function](surface-greens-function.md)에서 설명한다.[4,5]

비직교 기저에서는 $H_{D\alpha}$와 $S_{D\alpha}$를 **모두** 포함해야 한다. 또한 $z=E+i\eta$가 복소수이므로 $C_{\alpha D}(z)$를 일반적으로 $C_{D\alpha}(z)^\dagger$로 대체할 수 없다. Hermitian $H,S$에 대해 $C_{D\alpha}(z)^\dagger=H_{\alpha D}-z^*S_{\alpha D}$인 반면, 정확한 retarded self-energy에서는 양쪽 결합을 같은 $z$에서 평가한다. 실수 에너지축의 $\eta\to0^+$ 극한에서는 이러한 차이가 사라진다.[4,5]

### (3) Level shift와 broadening 행렬

전극 self-energy는 일반적으로 복소수이며, Hermitian 부분과 anti-Hermitian 부분을 다음처럼 분리한다.[1–3]

$$
\Lambda_\alpha(E)
=\frac{\Sigma_\alpha^R+\Sigma_\alpha^A}{2},
\qquad
\Gamma_\alpha(E)
=i\bigl(\Sigma_\alpha^R-\Sigma_\alpha^A\bigr),
\qquad
\Sigma_\alpha^R=\Lambda_\alpha-\frac{i}{2}\Gamma_\alpha.
$$

$\Sigma_\alpha^A=(\Sigma_\alpha^R)^\dagger$이다. $\Lambda_\alpha$는 전극과 결합하면서 소자의 에너지 준위가 이동하고 혼합되는 효과를, $\Gamma_\alpha$는 해당 전극의 연속 상태로 전자가 빠져나갈 수 있는 폭을 나타낸다. 두 행렬의 단위는 모두 에너지이다. 정상적인 수동 전극에 대해 실수 에너지에서 $\Gamma_\alpha$는 Hermitian 양의 준정부호이다.

**$\Gamma_\alpha$는 소자 orbital 공간의 전체 행렬**이다. 특히 $(\Gamma_\alpha)_{\mu\nu}$는 orbital $\mu,\nu$가 전극 $\alpha$를 통해 어떻게 연결되는지를 나타낸다. 단일 orbital 모형에서는 이 행렬이 비음수 실수 하나로 축소되지만, 일반적인 LCAO 계산에서는 각 orbital에 공통인 하나의 탈출률로 바꿔서는 안 된다. 실제로 특정 에너지에 전극의 전파 상태가 없으면 해당 연속체로의 broadening은 0이 될 수 있지만, $\Lambda_\alpha$에 의한 에너지 이동은 남을 수 있다.[1–3]

이제 전극 자유도 소거와 self-energy를 모두 포함한 **핵심 행렬식**을 다시 쓰면 다음과 같다.

$$
\boxed{
G^R(E)=
\left[zS_D-H_D-\Sigma_L^R(E)-\Sigma_R^R(E)\right]^{-1}
}
$$

이 식의 모든 행렬은 소자 영역 $D$의 동일한 $\mu,\nu$ 기저로 표현한다. 따라서 나중에 구하는 점유 행렬과 전류식도 **바로 이 $G^R$와 동일한 $\Sigma_\alpha,\Gamma_\alpha$**를 사용해야 한다.

## 4. Spectral function과 상태 밀도

Spectral function $A$는 에너지별 spectral weight를 행렬로 나타낸다. 직교 기저에서 density of states (DOS)는 단위 에너지당 상태 수, local density of states (LDOS)는 특정 궤도에 투영한 상태 밀도이다.[1,2]

$$
A(E)=i[G^R(E)-G^A(E)],\qquad
D(E)=\frac{\operatorname{Tr}A(E)}{2\pi},\qquad
D_i(E)=\frac{A_{ii}(E)}{2\pi}
=-\frac{1}{\pi}\operatorname{Im}G^R_{ii}(E).
$$

$G^R$와 $A$의 차원은 에너지의 역수이다. $D_i(E)$가 커도 그 에너지의 상태가 채워져 있다는 뜻은 아니다. 예를 들어 공명이 두 전극의 electrochemical potential보다 훨씬 위에 있으면 LDOS peak는 존재하지만 전자 점유는 작을 수 있다. 점유에는 다음 절의 Fermi 분포와 lesser 함수가 필요하다.[1–3]

전극 이외의 self-energy가 없는 직교 문제에서 역행렬 차이 항등식을 적용하면

$$
A=G^R\left[\Gamma_L+\Gamma_R+2\eta I_D\right]G^A
$$

를 얻는다. 전극과 연결된 연속 상태만 고려하고 $\eta\to0^+$를 취하면, 전극별 partial spectral function

$$
A_\alpha=G^R\Gamma_\alpha G^A,\qquad A=A_L+A_R
$$

로 나뉜다. $A_\alpha$는 전극 $\alpha$에서 입사한 상태가 소자 안에 만드는 spectral weight이다. 전극 연속체와 분리된 진정한 bound state가 있으면 $2\eta G^RG^A$가 적분 후 유한한 기여를 남길 수 있다. 이 경우 그 항을 먼저 버리면 상태 수가 누락된다.[1,2,4]

비직교 기저에서는 단순한 대각 원소를 곧바로 궤도별 상태 수로 읽을 수 없다. 완결된 유한 기저 전체에서는 metric을 포함한 $D(E)=\operatorname{Tr}[S A(E)]/(2\pi)$가 상태 수를 센다. 이는 $c_m^\dagger S c_m=1$인 고유상태의 spectral representation에 trace를 취한 결과이다. 그러나 열린 부분공간의 $\operatorname{Tr}[S_D A_{DD}]$를 임의의 공간 영역에 들어 있는 총 DOS와 동일시해서는 안 된다. 경계를 가로지르는 기저 overlap과 Green's function 블록, 선택한 원자별 분할 방법에 따라 투영량이 달라진다. 실제 공간의 LDOS가 필요하면 그 위치에 기여하는 모든 기저 함수로 kernel을 복원해야 한다.[4,5]

## 5. Lesser·greater Green's function과 점유

### (1) 점유와 비점유 상태

직교 궤도 $i$의 전자 소멸·생성 연산자를 $c_i,c_i^\dagger$라 한다. 정상 상태에서 시간 차이 $\tau=t-t'$에 대한 상관을 에너지로 변환하여

$$
G^<_{ij}(E)=\frac{i}{\hbar}\int d\tau\,
 e^{iE\tau/\hbar}\langle c_j^\dagger(0)c_i(\tau)\rangle,
\qquad
G^>_{ij}(E)=-\frac{i}{\hbar}\int d\tau\,
 e^{iE\tau/\hbar}\langle c_i(\tau)c_j^\dagger(0)\rangle
$$

로 정의한다. $\hbar=h/(2\pi)$이며 이 Fourier 정규화는 $G(E)$가 에너지의 역수 차원을 갖도록 한다. Lesser 함수는 점유된 전자 상태의 상관을, greater 함수는 전자를 추가할 수 있는 빈 상태의 상관을 담는다. `lesser`와 `greater`는 에너지가 작고 크다는 분류가 아니다.[1–3]

실수 관측량과 연결하기 편한 조합은

$$
G^n=-iG^<,\qquad G^p=iG^>,\qquad A=G^n+G^p
$$

이다. 위첨자 $n,p$는 각각 electron·hole correlation을 가리킨다. 여기서 hole은 같은 전자 상태의 비점유 부분을 뜻하며, 별도의 valence-band hole 근사를 도입한 것은 아니다. 평형에서만 공통 Fermi 함수 $f$로 $G^n=fA$, $G^p=(1-f)A$를 쓸 수 있다.[1–3]

### (2) 전극 주입과 Keldysh 관계

전극 $\alpha$의 electrochemical potential $\mu_\alpha$, 온도 $T_\alpha$, Boltzmann 상수 $k_B$로

$$
f_\alpha(E)=\left[1+\exp\frac{E-\mu_\alpha}{k_BT_\alpha}\right]^{-1}
$$

를 정의한다. 각 전극은 내부 평형을 유지하므로 그 lesser·greater self-energy는

$$
\Sigma_\alpha^<=if_\alpha\Gamma_\alpha,\qquad
\Sigma_\alpha^>=-i(1-f_\alpha)\Gamma_\alpha
$$

이다. 전극만이 점유를 공급하는 유효 단일입자 정상 상태이고 별도로 채워야 하는 bound state가 없으면 Keldysh 관계는

$$
G^{<,>}=G^R\left(\Sigma_L^{<,>}+\Sigma_R^{<,>}\right)G^A
$$

로 닫힌다. 왼쪽의 $<$ 또는 $>$를 오른쪽에서도 같은 성분으로 선택한다. 이를 partial spectral function으로 쓰면

$$
G^n=f_LA_L+f_RA_R,\qquad
G^p=(1-f_L)A_L+(1-f_R)A_R
$$

이다. 같은 에너지라도 왼쪽과 잘 연결된 궤도와 오른쪽과 잘 연결된 궤도의 점유가 다를 수 있다. 일반적인 여러 궤도 문제에서 $f_L,f_R$를 산술평균한 함수로 소자 전체를 채울 수 없는 이유이다.[1–3]

### (3) Density matrix와 density kernel

직교 기저의 단일입자 density matrix $P_{ij}=\langle c_j^\dagger c_i\rangle$는

$$
P=\frac{1}{2\pi}\int_{-\infty}^{\infty}G^n(E)\,dE
=-\frac{i}{2\pi}\int_{-\infty}^{\infty}G^<(E)\,dE
$$

이다. $P_{ii}$는 궤도 점유, 비대각 원소는 궤도 사이의 상관을 나타낸다. LDOS를 에너지 적분하는 것과 달리, 이 식에는 전극별 점유 가중치가 포함된다. $G^<$는 anti-Hermitian이고 $P$는 Hermitian이어야 한다.[1–3]

비직교 원자 궤도에서 같은 계수 표현으로 얻은 $P$는 density kernel이다. 모든 관련 기저를 포함하면 전자 수 밀도와 전자 수는

$$
n(\mathbf r)=\sum_{ij}\phi_i(\mathbf r)P_{ij}\phi_j^*(\mathbf r),\qquad
N=\int n(\mathbf r)d\mathbf r=\operatorname{Tr}(PS)
$$

이다. $N=\operatorname{Tr}P$는 직교 기저에서만 성립한다. 열린 소자의 공간 경계 근처에서는 전극 중심의 궤도 꼬리도 그 위치에 기여하므로, $P_{DD}$만으로 만든 밀도에 필요한 경계 교차항과 전극 항을 보충해야 한다. 전극 원자층을 충분히 포함하면 bulk 값을 이용한 이 경계 처리가 타당해지는지 검사할 수 있다.[4,5]

전극에서 완전히 분리된 bound state는 주입식만으로 점유가 정해지지 않는다. 초기 상태나 추가 평형화 과정이 필요할 수 있으며, 이 누락은 density kernel을 거쳐 자기일관 전위에도 영향을 준다. 이런 상태를 발견하면 두 Fermi 함수의 평균을 임의로 넣는 대신 별도의 점유 가정을 명시해야 한다.[1,4]

## 6. Transmission과 단자 전류

### (1) 일반적인 접촉 전류

평형을 유지하는 비상호작용 전극과 bilinear coupling으로 연결된 소자에서는, 소자 내부 상호작용을 포함하더라도 일관된 $G^{<,>}$를 알면 접촉 전류를 계산할 수 있다. 이 글의 $+e$ 순주입 규약에서

$$
I_\alpha=\frac{e}{h}\int dE\,
\operatorname{Tr}\left[\Sigma_\alpha^<G^>-\Sigma_\alpha^>G^<\right]
=\frac{e}{h}\int dE\,
\operatorname{Tr}\left[\Gamma_\alpha(f_\alpha A-G^n)\right]
$$

이다. 첫 항은 접촉이 공급하는 점유와 소자의 빈 상태, 둘째 항은 접촉의 빈 상태와 소자의 점유가 만드는 역방향 과정이다. 두 번째 형태는 앞 절의 전극 self-energy와 $A=G^n+G^p$를 대입한 결과이다. 내부 상호작용이 있으면 $G^R$뿐 아니라 $G^n$도 그 상호작용을 포함하여 구해야 한다.[2,3]

이 식으로 정상 상태의 전하 보존도 확인할 수 있다. 전자가 축적되지 않고 별도 전자 source가 없으면 $I_L+I_R=0$이다. 근사 self-energy나 에너지 적분이 일관되지 않으면 이 합이 수치적으로 0이 아닐 수 있으므로, 한쪽 접촉 전류만 계산하여 수렴을 판정하지 않는다.[2,3]

### (2) Coherent Landauer 전류

전극 self-energy만 포함한 coherent 단일입자 문제에서는 앞서 정의한 $A=A_L+A_R$와 $G^n=f_LA_L+f_RA_R$를 일반적인 전류식에 대입할 수 있다. 같은 전극의 항이 상쇄되어

$$
T(E)=\operatorname{Tr}\left[\Gamma_LG^R\Gamma_RG^A\right],\qquad
I_L=\frac{e}{h}\int dE\,T(E)[f_L-f_R],\qquad I_R=-I_L
$$

를 얻는다. $T(E)$는 무차원인 Caroli transmission이다. 상태가 있어도 한쪽 전극과 연결되지 않으면 전달이 일어나지 않고, 전달 경로가 있어도 양쪽 점유가 같으면 순전류가 0이다. 이는 DOS, transmission, 전류가 서로 다른 양임을 보여 준다.[1–3,5]

여기서 행렬이 두 spin을 모두 포함하면 추가 인자 2를 곱하지 않는다. 한 spin 블록만 계산하고 두 spin이 독립적으로 축퇴된 경우에 한해 결과를 두 배로 한다. Spin별 계산이면 $T=\sum_\sigma T_\sigma$로 합한다. 횡방향 주기성이 있는 DFT 계산에서는 각 $\mathbf k_\perp$의 transmission을 Brillouin zone에서 정규화된 가중치로 평균하며, 결과가 횡방향 단위 셀당 전류인지도 명시한다.[4,5]

같은 온도에서 $V=(\mu_L-\mu_R)/e$로 정의한 bias를 작게 바꾸면

$$
G_{\rm lin}=\left.\frac{\partial I_L}{\partial V}\right|_{V=0}
=\frac{e^2}{h}\int dE\,T(E)\left(-\frac{\partial f}{\partial E}\right)

$$

이다. 영온 극한에서는 $G_{\rm lin}=(e^2/h)T(E_F)$이며, $E_F$는 평형 Fermi energy이다. 유한 bias에서는 $H_D$와 전극 응답 자체가 달라질 수 있으므로 평형 $T(E)$를 큰 bias window에 적분한 값은 일반적인 자기일관 전류가 아니다.[1,3–5]

## 7. 단일 공명 준위

### (1) 상태의 폭과 점유 가중치

지금까지 행렬로 표현한 식을 한 spin 궤도로 축소한다. 고립 에너지는 $\varepsilon_0$, 전극 self-energy는 $\Delta_\alpha-i\Gamma_\alpha/2$이다. Wide-band approximation에서 $\Gamma_\alpha\ge0$와 실수 이동을 상수로 두고 $\bar\varepsilon=\varepsilon_0+\Delta_L+\Delta_R$, $\Gamma=\Gamma_L+\Gamma_R>0$라 쓰면

$$
G^R(E)=\frac{1}{E-\bar\varepsilon+i\Gamma/2},\qquad
A(E)=\frac{\Gamma}{(E-\bar\varepsilon)^2+(\Gamma/2)^2},
$$

$$
T(E)=\frac{\Gamma_L\Gamma_R}{(E-\bar\varepsilon)^2+(\Gamma/2)^2},\qquad
G^n(E)=A(E)f_{\rm eff}(E),\qquad
f_{\rm eff}=\frac{\Gamma_Lf_L+\Gamma_Rf_R}{\Gamma}.
$$

이는 앞의 resolvent, spectral function, Keldysh, Caroli 식을 scalar로 쓴 결과이다. $A$의 Lorentzian 폭과 $f_{\rm eff}$의 점유 가중치는 서로 다른 역할을 한다. 가중 점유식 자체는 에너지 의존 $\Gamma_\alpha(E)$에도 성립하지만, 아래의 단순 Lorentzian 적분에는 상수 폭과 고정된 $\bar\varepsilon$가 필요하다.[2,3]

공명 중심에서

$$
T(\bar\varepsilon)=\frac{4\Gamma_L\Gamma_R}{\Gamma^2}
=1-\frac{(\Gamma_L-\Gamma_R)^2}{\Gamma^2}\le1
$$

이다. 총 폭이 같아도 한쪽 결합이 약하면 transmission이 감소한다. 한쪽 전극만 연결된 준위는 넓어지고 채워질 수 있지만 반대편으로 전자를 전달하지 못한다. 두 결합이 모두 0인 극한에는 $f_{\rm eff}$를 이 비율로 정할 수 없다.[2,3]

총 폭을 고정하고 영온 bias window 안에서 $f_L=1$, $f_R=0$이라 두면 다음 비교가 가능하다. 수치는 위 식에서 직접 얻은 모형 값이다.

| 결합 비율 | 공명 transmission | $f_{\rm eff}$ | 점유를 정하는 접촉 |
| --- | --- | --- | --- |
| $\Gamma_L:\Gamma_R=1:1$ | $1$ | $1/2$ | 양쪽 기여가 같다. |
| $3:1$ | $3/4$ | $3/4$ | 채워진 왼쪽 접촉의 기여가 크다. |
| $1:3$ | $3/4$ | $1/4$ | 비어 있는 오른쪽 접촉의 기여가 크다. |

마지막 두 경우는 $T(E)$가 같아도 내부 점유가 다르다. 같은 transmission을 얻었다고 해서 소자 내부의 전하 분포까지 같다고 볼 수는 없다. DFT와 결합한 자기일관 계산에서는 이 전하 분포의 차이가 전위와 공명 준위의 위치를 다시 바꿀 수 있다.[3–5]

### (2) 점유와 전류의 적분 검산

한 spin 궤도의 상태 수는

$$
\int_{-\infty}^{\infty}\frac{A(E)}{2\pi}\,dE=1
$$

이다. 접촉이 폭을 만들어도 총 spectral weight는 한 상태이다. 영온에서 각 전극까지 채운 누적 spectral weight는

$$
F_\alpha=\int_{-\infty}^{\mu_\alpha}\frac{A(E)}{2\pi}\,dE
=\frac12+\frac1\pi\arctan\frac{2(\mu_\alpha-\bar\varepsilon)}{\Gamma}
$$

이고, 점유수 $n_0=(\Gamma_LF_L+\Gamma_RF_R)/\Gamma$는 0과 1 사이이다. 이 결과는 앞의 Lorentzian과 점유식을 직접 적분한 것이다. 공명 중심의 $f_{\rm eff}$만 평가한 것과 달리, 중심에서 떨어진 spectral tail도 점유에 포함한다.[2,3]

같은 모형의 전류 적분은

$$
I_L=\frac{e}{h}\frac{2\Gamma_L\Gamma_R}{\Gamma}
\left[
\arctan\frac{2(\mu_L-\bar\varepsilon)}{\Gamma}
-\arctan\frac{2(\mu_R-\bar\varepsilon)}{\Gamma}
\right]
$$

이다. $\mu_L>\mu_R$이면 이 글의 순주입 규약에서 양수이다. 괄호는 무차원이고 $\Gamma_L\Gamma_R/\Gamma$는 에너지이므로 전체 차원은 전류이다. 에너지를 eV로 적분할 때에는 SI 단위의 $h$와 결합하기 전에 에너지 단위를 맞춰야 한다.[2,3]

예를 들어 $\Gamma_L=\Gamma_R=\Gamma/2$와 $\mu_{L,R}-\bar\varepsilon=\pm\Gamma/2$를 대입하면 $n_0=1/2$, $I_Lh/(e\Gamma)=\pi/4$이다. 이는 실험값이 아닌 무차원 검산값이다. 두 electrochemical potential을 서로 바꾸면 점유는 그대로이고 전류 부호가 바뀐다. 평형에서도 $n_0=1/2$일 수 있지만 순전류는 0이므로, 총점유 하나만으로 전류를 정할 수도 없다.

## 8. DFT-NEGF 자기일관 계산

### (1) 밀도와 Hamiltonian의 반복

DFT-NEGF는 $G^R$를 한 번 역산하는 것으로 끝나지 않는다. 접촉과 bias가 만든 밀도가 KS potential을 바꾸고, 바뀐 Hamiltonian이 다시 상태와 점유를 바꾼다. 고정 원자 구조에서 이 의존성은

$$
n^{(k)}(\mathbf r)\longrightarrow H_{\rm KS}[n^{(k)}]
\longrightarrow G^{R,(k)},G^{<,(k)}
\longrightarrow P^{(k)}\longrightarrow n_{\rm out}^{(k)}(\mathbf r)
\longrightarrow n^{(k+1)}(\mathbf r)
$$

이다. $k$는 자기일관 반복 번호이며, 마지막 단계에서는 입력·출력 밀도 차이를 줄이도록 mixing한다. 전극 bulk 계산은 이 반복 전에 수행하여 전극의 $H,S$, Fermi level, 경계 전위와 표면 self-energy의 기반을 정한다.[4,5]

KS Hamiltonian의 구조를

$$
\hat H_{\rm KS}[n]=\hat T+\hat V_{\rm ion}+U_H[n]+V_{\rm xc}[n]
$$

로 나타낼 수 있다. $\hat T$는 운동에너지, $\hat V_{\rm ion}$은 이온 또는 pseudopotential 항, $U_H$는 전자 밀도의 Hartree potential energy, $V_{\rm xc}$는 선택한 exchange-correlation potential이다. 계산하는 $H_{ij}$는 이 연산자를 기저로 표현한 행렬 원소이다. Density kernel은 앞 절의 $G^<$ 적분으로 얻고, 원자 궤도로 실공간 밀도를 재구성한다. 이 과정을 통해 수송 문제의 점유가 DFT의 입력 변수인 $n(\mathbf r)$에 연결된다.[4,5]

| 단계 | 입력과 계산 | 다음 단계에 전달할 양 |
| --- | --- | --- |
| 전극 준비 | 같은 기저·functional로 좌우 bulk를 각각 계산 | $H_\alpha,S_\alpha$, 에너지 기준, 경계 전위 |
| 열린 경계 | 주어진 bias의 전극과 경계 결합으로 표면 Green's function 계산 | $\Sigma_\alpha^R,\Gamma_\alpha$ |
| 소자 상태와 점유 | 현재 KS Hamiltonian의 $G^R$ 및 전극 주입 계산 | $G^<$와 density kernel $P$ |
| 실공간 갱신 | 궤도와 경계 기여로 $n(\mathbf r)$ 복원, Poisson과 exchange-correlation (XC) 계산 | 새 전위와 $H_D$ |
| 반복과 관측량 | 밀도·전위 잔차를 줄이고 적분·경계 수렴 확인 | 수렴한 $T(E,V)$와 $I(V)$ |

전극 self-energy를 재사용할 수 있는 범위는 bulk 전극과 경계 결합을 고정했는지에 달려 있다. 반복마다 모든 bulk 계산을 다시 할 필요는 없지만, 경계 결합이나 bias에 따른 전극 에너지 이동이 바뀌었는데도 이전 self-energy를 그대로 써서는 안 된다.[4,5]

### (2) Hartree 전위와 전극 경계조건

밀도만으로는 유한 소자의 정전기 문제를 완전히 정할 수 없다. Poisson 방정식에는 전극이 유지하는 경계값이 필요하다. Hartree atomic units에서 전자 밀도 $n$이 만드는 potential energy는

$$
\nabla^2U_H(\mathbf r)=-4\pi n(\mathbf r)
$$

를 만족한다. 이 식의 $U_H$는 전자의 Hartree **에너지**이며 전압 단위의 electrostatic potential $\phi$와 구분한다. 전자의 electrostatic energy는 $-e\phi$이고, 전체 KS potential에는 이온과 XC 항도 별도로 들어간다. 실제 구현은 중성 원자 기준 밀도를 빼서 차이 밀도의 Poisson 식을 풀 수 있지만, 같은 기준의 경계값을 함께 사용해야 한다.[4,5]

수송 방향 양끝에서는 별도 bulk 전극 계산과 일치하는 전위를 부여한다. 횡방향이 주기적인 모형이면 그 방향에는 주기 경계를 쓴다. Gate가 있는 문제에서는 실제 계산 모형에 맞는 추가 정전기 경계를 정한다. 전극에서 차폐가 끝나기도 전에 bulk 전위를 강제하면 접촉 전하와 인공적인 반사가 결과를 바꿀 수 있다.[4,5]

전극 $\alpha$의 모든 단일입자 에너지를 $\delta_\alpha$만큼 rigid shift하는 reservoir 모형에서는

$$
H_\alpha\mapsto H_\alpha+\delta_\alpha S_\alpha,
\qquad \mu_\alpha\mapsto\mu_\alpha+\delta_\alpha
$$

와 전극의 potential-energy 경계값 이동을 일관되게 적용한다. $\delta_\alpha$는 에너지이며 전압 자체가 아니다. 비직교 기저의 상수 potential matrix가 $\delta_\alpha S_\alpha$라는 점이 중요하다. 경계 결합에도 해당 potential 변화가 반영되어야 한다. Fermi 함수의 $\mu$만 이동하고 전극 band와 정전기 경계는 그대로 두는 계산은 이 rigid-shift bias 모형과 다르다.[4,5]

### (3) Density kernel의 에너지 적분

점유 적분에는 bias window의 전류뿐 아니라 그 아래 채워진 상태도 포함된다. 전극과 연결된 상태에 대해 기준 분포를 $f_L$로 선택하면

$$
P=\frac{1}{2\pi}\int dE\,f_L A
+\frac{1}{2\pi}\int dE\,(f_R-f_L)A_R
\equiv P_{\rm ref}+\Delta P
$$

이다. 이는 $G^n=f_LA_L+f_RA_R$를 다시 쓴 식이다. 첫 항은 현재의 비평형 Hamiltonian에 공통 분포를 적용한 적분이며, 별도로 계산한 bias가 0인 Hamiltonian의 밀도를 뜻하지 않는다. 둘째 항만 전극의 분포 차이가 유의한 에너지 범위에 집중된다.[4,5]

실제 구현에서는 analytic Green's function을 이용해 첫 항을 complex contour에서 효율적으로 적분하고, $G^R\Gamma_RG^A$가 들어가는 보정항은 실수 에너지축에서 적분한다. 보정항에는 retarded와 advanced 함수가 함께 있으므로 첫 항과 같은 analytic contour 처리를 그대로 적용할 수 없다. 유한 온도에서는 Fermi tail까지 포함하고, 좁은 공명이 있으면 그 폭을 충분히 분해해야 한다.[4,5]

왼쪽과 오른쪽을 바꾼 분해도 동일한 $P$를 주어야 한다. 같은 density kernel을 두 방식으로 계산했을 때의 차이를 비교하면, 에너지 적분의 수치 오차가 충분히 작은지 확인할 수 있다. 진정한 bound state가 있으면 앞서 명시한 별도의 점유 처리를 더해야 하며, contour에 pole이 잡힌다는 사실만으로 비평형 점유의 물리가 자동으로 정해지지는 않는다.[4,5]

### (4) 수렴과 결과 기록

자기일관 수렴과 수치 적분 수렴은 별도로 확인한다. 밀도 잔차가 작아도 전극 경계가 너무 가깝거나 에너지 격자가 공명을 놓쳤다면 전류는 잘못될 수 있다. 반대로 작은 전류 잔차만으로 밀도·Hartree 전위가 충분히 수렴했다고 판단할 수 없다.[4,5]

| 확인 대상 | 비교할 계산 | 물리적 점검 |
| --- | --- | --- |
| 자기일관 반복 | 밀도·전위 잔차와 반복 수 | 접촉 전하와 전위가 안정되는가? |
| 실수축 적분 | 에너지 간격·적분 범위·$\eta$ | 좁은 공명과 Fermi tail을 분해하는가? |
| 전극 경계 | 포함한 전극층 수 | 경계에서 bulk 전위·밀도로 이어지는가? |
| 기저와 횡방향 표본 | 기저 크기와 $\mathbf k_\perp$ 격자 | 전하와 transmission이 안정되는가? |
| 보존 관계 | 양쪽 접촉 전류 | $I_L+I_R$가 수치 오차 안에서 0인가? |

결과에는 원자 구조와 기저, functional, 전극 정의, $(\mu_L,\mu_R)$, 온도, 에너지 기준, spin 처리, 전류 부호, 에너지 적분과 횡방향 표본 조건을 함께 기록한다. 예를 들어 전류 격자 수렴은 선언한 기준 전류 $I_{\rm scale}>0$를 사용하여 $|I_{\rm fine}-I_{\rm coarse}|/\max(I_{\rm scale},|I_{\rm fine}|)$로 비교할 수 있다. 이 지표는 무전류 근처에서 상대 오차가 발산하는 것을 피하기 위한 계산상의 정의이며, 보편적인 허용 오차를 뜻하지 않는다.[4,5]

## 9. 적용 범위와 해석의 한계

Coherent NEGF에서도 $H_D$에 정적 결함이나 무질서를 넣으면 탄성 산란과 간섭을 계산한다. 따라서 coherent와 ballistic은 동의어가 아니다. 전극 self-energy만 사용하는 계산은 소자 안의 electron–phonon scattering을 자동으로 포함하지 않으며, 비탄성 산란에는 해당 retarded·lesser·greater self-energy와 보존적인 점유 계산이 필요하다. 관련 전개는 [Electron–phonon coupling](electron-phonon-coupling.md)과 [Inelastic electron transport](inelastic-electron-transport.md)에서 다룬다.[1–3]

DFT-NEGF의 자기일관 반복은 정적 KS potential의 전하 재배치를 포함한다. 이것만으로 일반적인 상호작용 비평형 전자계의 정확한 전류가 보장되지는 않는다. 선택한 XC functional, KS 단일입자 전류 해석, 빠진 동적 상관과 비탄성 과정의 한계를 구분해야 한다. 특히 전극 결합과 내부 상관의 상대적인 크기가 달라지면 단순한 coherent 단일입자 그림의 신뢰도도 다시 검토해야 한다.[2,4]

$\eta$는 경계조건을 선택하는 극한을 수치적으로 구현하는 값이다. 너무 큰 $\eta$는 공명을 인위적으로 넓히고 전극 주입만을 쓴 점유식과 spectral identity 사이의 차이를 키울 수 있다. 따라서 에너지 격자와 함께 줄여 가며 전하와 전류를 확인한다. 물리적인 산란을 넣으려면 retarded 폭뿐 아니라 그 과정의 주입·유출 성분도 함께 지정해야 한다.[1,3–5]

## 10. 요약

- 전극 self-energy는 반무한 전극의 응답을 유한 소자 resolvent에 포함한다. 표면 Green's function은 고립된 표면 셀의 역행렬과 다르다.
- $A$와 LDOS는 spectral weight, $G^<$와 density kernel은 실제 점유를 나타낸다. 비직교 기저에서는 overlap과 경계 교차항도 필요하다.
- 일반 접촉 전류식에 coherent Keldysh 관계를 대입하면 Caroli transmission과 Landauer 전류가 나온다. Spin과 전류 부호는 한 규약으로 유지한다.
- DFT-NEGF는 밀도, KS Hamiltonian, 열린 경계 점유, Hartree 전위를 반복하여 수렴시킨다. 전극의 에너지 기준과 Poisson 경계값도 계산의 일부이다.
- Bound state의 점유, 수치적인 $\eta$, 정적 DFT 근사와 실제 비탄성 산란은 별개의 문제로 다룬다.

## 11. 참고문헌

1. X. Waintal, M. Wimmer, A. Akhmerov, C. Groth, B. K. Nikolić, M. Istas, T. Ö. Rosdahl, and D. Varjas, "Computational quantum transport: A scattering approach perspective," *arXiv:2407.16257v3* (2026). [arXiv](https://arxiv.org/abs/2407.16257v3).
2. D. A. Ryndyk, R. Gutiérrez, B. Song, and G. Cuniberti, "Green function techniques in the treatment of quantum transport at the molecular scale," *arXiv:0805.0628v2* (2008). [arXiv](https://arxiv.org/abs/0805.0628v2).
3. S. Datta, "Electrical Resistance: An Atomistic View," *Nanotechnology* **15**, S433–S451 (2004). [DOI](https://doi.org/10.1088/0957-4484/15/7/051), [arXiv](https://arxiv.org/abs/cond-mat/0408319).
4. M. Brandbyge, J.-L. Mozos, P. Ordejón, J. Taylor, and K. Stokbro, "Density-functional method for nonequilibrium electron transport," *Physical Review B* **65**, 165401 (2002). [DOI](https://doi.org/10.1103/PhysRevB.65.165401), [arXiv](https://arxiv.org/abs/cond-mat/0110650).
5. T. Ozaki, K. Nishio, and H. Kino, "Efficient implementation of the nonequilibrium Green function method for electronic transport calculations," *Physical Review B* **81**, 035116 (2010). [DOI](https://doi.org/10.1103/PhysRevB.81.035116), [arXiv](https://arxiv.org/abs/0908.4142).
