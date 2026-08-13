---
title: "1.1. Electronic structure: Hartree–Fock method"
description: 단일 Slater determinant 변분에서 Fock equation과 Roothaan–Hall equation을 유도하고 SCF 계산, spin 선택과 근사 한계를 설명
status: verified
last_verified: 2026-08-13
---

# 1.1. Electronic structure: Hartree–Fock method

Hartree–Fock (HF) method는 반대칭인 $N$전자 파동함수를 하나의 Slater determinant로 제한하고, 그 집합 안에서 에너지 기대값을 최소화하는 mean-field 전자구조 방법이다. 전자–전자 Coulomb 반발은 모든 점유 궤도함수가 만드는 평균장으로 처리하고, 행렬식의 반대칭성에서 생기는 exchange는 정확히 포함한다. 그러나 하나의 determinant로 나타낼 수 없는 전자 상관은 포함하지 않는다.[1–3]

이 글은 고정된 핵, 비상대론적 전자 Hamiltonian과 원자 단위계를 사용한다. 먼저 spin orbital을 이용해 일반식을 유도하고, 실제 분자 계산에서 널리 쓰는 closed-shell restricted Hartree–Fock (RHF)와 유한 basis의 Roothaan–Hall equation으로 내려간다. 주기적 고체의 $k$-point 구현과 post-HF 방법의 상세 유도는 범위에서 제외한다.

## 1. 전자 문제와 변분 공간

### (1) Born–Oppenheimer 전자 Hamiltonian

핵 위치 ${\mathbf R_A\}$를 고정하면 $N$전자 Hamiltonian은

$$
\hat H_{\mathrm e}
=
\sum_{i=1}^{N}\hat h(i)
+\sum_{i<j}^{N}\frac{1}{r_{ij}},
$$

$$
\hat h(i)
=-\frac{1}{2}\nabla_i^2
-\sum_A\frac{Z_A}{|\mathbf r_i-\mathbf R_A|}
$$

로 쓴다. $\hat h$는 전자 운동에너지와 전자–핵 인력을 포함하는 one-electron operator이고, $r_{ij}=|\mathbf r_i-\mathbf r_j|$이다. 핵–핵 반발

$$
E_{\mathrm{NN}}
=\sum_{A<B}\frac{Z_AZ_B}{|\mathbf R_A-\mathbf R_B|}
$$

은 고정된 구조에서 상수이므로 전자 변분 문제를 푼 뒤 더한다.[1–3]

따라서 한 구조에서 SCF가 최소화하는 양은 $E_{\mathrm{HF}}$이지만, 서로 다른 핵 배치의 에너지를 비교할 때 사용하는 Born–Oppenheimer potential energy는

$$
E_{\mathrm{tot}}(\{\mathbf R_A\})
=E_{\mathrm{HF}}(\{\mathbf R_A\})+E_{\mathrm{NN}}(\{\mathbf R_A\})
$$

이다. $E_{\mathrm{NN}}$은 한 번의 전자 SCF 순환 안에서는 변하지 않지만 핵 좌표를 바꾸면 달라진다. 그러므로 결합 길이, 구조 안정성 또는 힘을 비교하면서 전자에너지와 총에너지를 혼용하면 안 된다. HF 근사와 basis 선택은 전자 항에 들어가고, 핵–핵 항은 같은 원자 단위계의 고전적 Coulomb 항으로 정확히 계산한다.[1–3]

정확한 $N$전자 파동함수는 전자 좌표 $x_i=(\mathbf r_i,\omega_i)$를 교환하면 부호가 바뀌어야 한다. 여기서 $\omega_i$는 spin 좌표이다. HF method는 이 조건을 만족시키면서 계산 가능한 가장 단순한 변분 공간으로 단일 Slater determinant를 선택한다.[1–3]

### (2) Slater determinant

서로 직교 정규화된 spin orbital $\{\chi_i(x)\}_{i=1}^{N}$로 HF 파동함수를

$$
\Phi(x_1,\ldots,x_N)
=\frac{1}{\sqrt{N!}}
\det[\chi_i(x_j)]
$$

로 정의한다. 두 전자 좌표를 맞바꾸면 determinant의 두 행이 교환되어 부호가 바뀌므로 fermion 반대칭성이 자동으로 보존된다. 궤도함수에는

$$
\langle\chi_i|\chi_j\rangle=\delta_{ij}
$$

를 부과한다. HF 에너지는

$$
E_{\mathrm{HF}}
=\min_{\Phi\,\in\,\mathcal D}
\langle\Phi|\hat H_{\mathrm e}|\Phi\rangle
$$

이며, $\mathcal D$는 직교 정규화된 spin orbital로 만든 단일 determinant의 집합이다. 따라서 완전한 Hilbert space가 아니라 제한된 변분 공간에서 얻은 최솟값이다.[1,2]

이 제한은 계산 가능성을 주지만, determinant의 개수를 늘리는 것과 basis function의 개수를 늘리는 것을 서로 다른 근사 축으로 만든다. HF에서는 전자는 하나의 determinant에 머물고 궤도함수 표현만 basis와 함께 개선된다.[1,2]

## 2. Hartree–Fock 에너지

### (1) One-electron, Coulomb와 exchange 적분

One-electron 적분과 two-electron 적분을 각각

$$
h_{ij}=\langle\chi_i|\hat h|\chi_j\rangle,
$$

$$
(ij|kl)
=\iint
\chi_i^*(x_1)\chi_j(x_1)
\frac{1}{r_{12}}
\chi_k^*(x_2)\chi_l(x_2)
\,dx_1dx_2
$$

로 정의한다. 점유 spin orbital $i,j$에 대한 Coulomb 적분과 exchange 적분은

$$
J_{ij}=(ii|jj),
\qquad
K_{ij}=(ij|ji)
$$

이다. Slater–Condon rule을 적용하면 전자 에너지는

$$
\boxed{
E_{\mathrm{HF}}
=\sum_i^{\mathrm{occ}}h_{ii}
+\frac{1}{2}
\sum_{i,j}^{\mathrm{occ}}
\left(J_{ij}-K_{ij}\right)
}
$$

가 된다.[1–3] $J_{ij}$는 두 궤도함수 밀도의 고전적 Coulomb 반발에 해당하지만, $K_{ij}$는 고전적 대응물이 없는 비국소 항이다. Spin 함수가 서로 직교하면 $K_{ij}=0$이므로 exchange는 같은 spin 성분 사이에서만 남는다.[1–3]

같은 궤도함수에 대해서는 $J_{ii}=K_{ii}$이다. 따라서 위 식에서 한 전자가 자기 자신의 Coulomb 장과 상호작용하는 항은 정확히 상쇄된다. 이 상쇄는 단일 determinant의 exchange가 수행하는 역할이며, 서로 다른 전자의 순간적인 위치 상관까지 포함한다는 뜻은 아니다.[1–3]

### (2) Closed-shell 에너지

RHF에서는 $n=N/2$개의 공간 궤도함수 $\{\phi_i(\mathbf r)\}$를 각각 $\alpha$, $\beta$ 전자가 공유한다. 이때

$$
\boxed{
E_{\mathrm{RHF}}
=2\sum_{i=1}^{n}h_{ii}
+\sum_{i,j=1}^{n}
\left(2J_{ij}-K_{ij}\right)
}
$$

이다.[1–3] 첫 항의 계수 2는 공간 궤도함수의 이중 점유에서 오고, $2J-K$는 spin 합을 끝낸 결과이다. Spin-orbital 식의 $J-K$와 closed-shell 공간-orbital 식의 $2J-K$를 같은 합 범위에서 섞어 쓰면 계수가 틀린다.

## 3. Fock equation

### (1) 직교 제약 변분

궤도함수 직교 조건을 Lagrange multiplier $\varepsilon_{ij}$로 부과하면

$$
\mathcal L
=E_{\mathrm{HF}}
-\sum_{ij}\varepsilon_{ij}
\left(\langle\chi_i|\chi_j\rangle-\delta_{ij}\right)
$$

를 얻는다. $\chi_i^*$에 대한 정상 조건 $\delta\mathcal L=0$은

$$
\hat f\chi_i
=\sum_j\varepsilon_{ji}\chi_j
$$

를 준다. Fock operator는

$$
\boxed{
\hat f
=\hat h
+\sum_{j}^{\mathrm{occ}}
\left(\hat J_j-\hat K_j\right)
}
$$

이며, 작용은

$$
\hat J_j\chi_i(x_1)
=\left[
\int\frac{|\chi_j(x_2)|^2}{r_{12}}\,dx_2
\right]\chi_i(x_1),
$$

$$
\hat K_j\chi_i(x_1)
=\left[
\int\frac{\chi_j^*(x_2)\chi_i(x_2)}{r_{12}}\,dx_2
\right]\chi_j(x_1)
$$

로 정의한다.[1–3] $\hat J_j$는 위치 $x_1$에서 스칼라 Coulomb potential을 곱하지만, $\hat K_j$는 $\chi_i$의 다른 위치 값에 의존하여 $\chi_j(x_1)$를 돌려주는 nonlocal operator이다.

### (2) Canonical orbital과 자기일관성

$\varepsilon_{ij}$는 Hermitian matrix이므로 점유 궤도함수 사이의 unitary transformation으로 대각화할 수 있다. 이렇게 선택한 canonical orbital은

$$
\boxed{
\hat f\chi_p=\epsilon_p\chi_p
}
$$

를 만족한다.[1,2] 그러나 $\hat f$ 자체가 점유 궤도함수로 만든 $\hat J_j$와 $\hat K_j$에 의존하므로 이 식은 보통의 선형 고유값 문제가 아니다. 입력 궤도함수로 만든 Fock operator의 고유함수가 다시 같은 점유 공간을 만들 때에만 자기일관적이다.[1–3]

점유 궤도함수끼리의 unitary rotation은 determinant를 전체 위상만큼 바꾸고 one-particle density matrix와 HF 에너지는 보존한다. 따라서 canonical orbital은 편리한 표현이지만 유일한 국소 궤도함수 집합은 아니다.[1,2]

## 4. 유한 basis와 SCF 계산

### (1) Roothaan–Hall equation

분자 궤도함수를 $M$개의 일반적으로 비직교인 basis function $\{\varphi_\mu\}$로

$$
\phi_i(\mathbf r)
=\sum_{\mu=1}^{M}C_{\mu i}\varphi_\mu(\mathbf r)
$$

처럼 전개한다. Fock equation을 basis에 사영하면 closed-shell RHF의 Roothaan–Hall equation

$$
\boxed{
\mathbf F\mathbf C
=\mathbf S\mathbf C\boldsymbol\epsilon
}
$$

을 얻는다. 여기서

$$
F_{\mu\nu}=\langle\varphi_\mu|\hat f|\varphi_\nu\rangle,
\qquad
S_{\mu\nu}=\langle\varphi_\mu|\varphi_\nu\rangle
$$

이다.[1–3] $\mathbf S\neq\mathbf I$이므로 generalized eigenvalue problem이며, $\mathbf X^\dagger\mathbf S\mathbf X=\mathbf I$인 직교화 행렬을 사용하면

$$
\widetilde{\mathbf F}\widetilde{\mathbf C}
=\widetilde{\mathbf C}\boldsymbol\epsilon,
\qquad
\widetilde{\mathbf F}=\mathbf X^\dagger\mathbf F\mathbf X
$$

인 보통의 Hermitian eigenvalue problem으로 바뀐다.[1–3]

Closed-shell density matrix를

$$
P_{\mu\nu}
=2\sum_{i=1}^{n}C_{\mu i}C_{\nu i}^*
$$

로 정의하면 $\mathbf F$는 $\mathbf P$의 함수이다. 따라서 Roothaan–Hall equation도 한 번의 대각화로 끝나지 않는다.[1–3]

### (2) Self-consistent field 순환

Self-consistent field (SCF) 계산은 다음 순환을 수행한다.[1–3]

1. 원자 밀도의 합이나 core Hamiltonian에서 초기 $\mathbf P^{(0)}$를 만든다.
2. $\mathbf P^{(k)}$로 Coulomb·exchange 적분을 축약하여 $\mathbf F^{(k)}$를 만든다.
3. $\mathbf F^{(k)}\mathbf C^{(k+1)}=\mathbf S\mathbf C^{(k+1)}\boldsymbol\epsilon^{(k+1)}$을 푼다.
4. 점유 궤도함수로 새 $\mathbf P^{(k+1)}$와 에너지를 계산한다.
5. 에너지와 밀도 또는 orbital-gradient residual이 허용 오차보다 작아질 때까지 반복한다.

!!! info "[Measurement]"
    SCF 수렴은 에너지 변화 하나만으로 판정하지 않는다. 대표적으로

    $$
    \Delta E^{(k)}
    =E^{(k)}-E^{(k-1)},
    \qquad
    \Delta\mathbf P^{(k)}
    =\mathbf P^{(k)}-\mathbf P^{(k-1)}
    $$

    와 비직교 basis의 commutator residual

    $$
    \mathbf R^{(k)}
    =\mathbf F^{(k)}\mathbf P^{(k)}\mathbf S
    -\mathbf S\mathbf P^{(k)}\mathbf F^{(k)}
    $$

    의 norm을 함께 확인한다. 보고할 때에는 $|\Delta E|$, density RMS 또는 $\|\mathbf R\|$, 허용 오차, 최대 반복 횟수, 초기 추정과 수렴 가속법을 명시한다.[2,3]

### (3) 수렴과 안정성의 구분

SCF 고정점에 도달했다는 사실은 선택한 변분 공간의 전역 최솟값을 찾았다는 뜻이 아니다. 정상점은 국소 최솟값, saddle point 또는 점유가 다른 해일 수 있다. 점유–비점유 orbital rotation에 대한 에너지의 이차 변화, 즉 orbital Hessian을 검사해야 주어진 HF ansatz 안에서 안정한 해인지 판단할 수 있다.[1–3]

SCF가 진동하거나 발산하면 density mixing, damping, level shifting 또는 direct inversion in the iterative subspace (DIIS)를 사용할 수 있다. 이 기법들은 고정점 탐색을 안정화하지만, basis 불충분·잘못된 spin 상태·강한 다중 determinant 성격 같은 모형 문제를 해결하지는 않는다.[2,3]

## 5. Spin 제약의 선택

같은 HF 변분 원리라도 $\alpha$와 $\beta$ 공간 궤도함수에 어떤 제약을 두는지에 따라 해가 달라진다.[2,3]

| 방법 | 궤도함수 제약 | 적합한 기본 대상 | 주요 주의점 |
| --- | --- | --- | --- |
| RHF | $\phi_i^\alpha=\phi_i^\beta$인 이중 점유 | closed-shell singlet | 결합 해리나 spin polarization에서 지나치게 제한될 수 있음 |
| UHF | $\alpha$, $\beta$ 공간 궤도함수를 독립 최적화 | 일반 open-shell 또는 broken-symmetry 해 | 더 낮은 에너지를 얻을 수 있으나 $\hat S^2$ 고유함수가 아닐 수 있음 |
| ROHF | 이중 점유 궤도함수를 공유하면서 open-shell 점유를 유지 | 명확한 spin multiplicity의 open-shell | Fock operator와 canonical orbital energy의 정의가 UHF보다 덜 단순함 |

RHF보다 UHF의 변분 공간이 더 크므로 같은 basis와 Hamiltonian에서 $E_{\mathrm{UHF}}\le E_{\mathrm{RHF}}$이다. 그러나 낮은 에너지가 곧 원하는 spin 대칭성을 보존한다는 뜻은 아니다. UHF에서는 계산한 $\langle\hat S^2\rangle$를 목표값 $S(S+1)$과 비교하고, spin contamination과 symmetry breaking이 물리적 현상인지 근사의 산물인지 따로 판단해야 한다.[2,3]

## 6. 결과의 해석과 적용 한계

### (1) 변분 상한과 basis-set limit

고정한 Hamiltonian과 허용한 spin·공간 대칭성 아래에서 HF 에너지는 단일 determinant 집합의 최솟값이다. 따라서 정확한 바닥상태 에너지보다 낮아질 수 없지만, 이 명제는 SCF가 실제 최솟값에 수렴하고 수치 적분과 행렬 연산이 충분히 정확하다는 조건을 전제로 한다.[1,2]

유한 basis에서 얻은 값은 basis-set-dependent HF 에너지이다. Basis 공간을 포함 관계로 확장하고 각 단계에서 같은 변분 문제의 최솟값을 찾으면 에너지는 HF basis-set limit를 향해 내려간다. 이는 전자 상관이 복원된다는 뜻이 아니라, 선택한 단일 determinant를 더 유연하게 표현한다는 뜻이다.[1,2,4]

### (2) 단일 determinant 근사

HF는 Pauli 반대칭성에서 생기는 exchange를 포함하지만, 서로 다른 determinant의 중첩이 필요한 correlation은 잃는다. 특히 여러 전자배치가 비슷한 가중치를 가져야 하는 계에서는 한 determinant의 궤도함수를 아무리 최적화해도 필요한 파동함수 구조를 만들 수 없다.[1–3]

| 구분 | HF가 보존하는 정보 | HF가 잃는 정보 또는 위험 |
| --- | --- | --- |
| 반대칭성 | 전자 교환에서 파동함수 부호가 바뀜 | 없음 |
| Exchange | 같은 spin 전자의 비국소 exchange와 자기상호작용 상쇄 | 반대 spin의 동적 상관은 포함하지 않음 |
| 변분 | 단일 determinant 집합 안의 정상점과 최솟값 | 정확한 다중 determinant 바닥상태는 변분 공간 밖에 있을 수 있음 |
| 궤도함수 | 점유 공간과 density matrix를 자기일관적으로 최적화 | Canonical orbital 하나하나를 직접 관측량으로 동일시할 수 없음 |
| Basis | 주어진 basis에서 재현 가능한 최적 determinant | 유한 basis 오차와 선형 의존성 |

### (3) Orbital energy와 총에너지

Canonical HF orbital energy $\epsilon_i$는 수렴한 Fock operator의 고유값이다. Spin-orbital 표기에서 점유 궤도함수의 고유값을 합하면

$$
\sum_i^{\mathrm{occ}}\epsilon_i
=\sum_i^{\mathrm{occ}}h_{ii}
+\sum_{i,j}^{\mathrm{occ}}
\left(J_{ij}-K_{ij}\right)
$$

가 된다. 반면 HF 총 전자에너지는 전자쌍 상호작용을 한 번만 세기 위해 two-electron 항에 $1/2$이 붙는다. 따라서

$$
\boxed{
E_{\mathrm{HF}}
=\sum_i^{\mathrm{occ}}\epsilon_i
-\frac{1}{2}
\sum_{i,j}^{\mathrm{occ}}
\left(J_{ij}-K_{ij}\right)
}
$$

이며, 점유 orbital energy의 단순한 합은 HF 총에너지가 아니다.[1–3] 각 $\epsilon_i$에는 다른 점유 전자가 만드는 평균장이 이미 들어 있으므로 합만 취하면 전자–전자 상호작용을 두 번 센다.

또한 canonical orbital energy는 수렴한 $N$전자 determinant의 Fock operator에서 정의된 Lagrange multiplier이다. 점유 공간 안의 unitary rotation은 density matrix와 총에너지를 보존하지만 개별 orbital의 모양은 바꿀 수 있다. 그러므로 canonical orbital의 순서와 공간 분포는 유용한 분석 자료이지만, 모든 $\epsilon_p$를 독립적인 실제 전자 여기 에너지와 동일시해서는 안 된다. 특히 비점유 orbital은 바닥상태 density matrix를 만들지 않으므로 점유 orbital과 같은 변분적 지위를 갖지 않는다.[1–3]

### (4) 후속 전자구조 방법과의 연결

HF determinant와 orbital은 perturbation theory, configuration interaction, coupled-cluster와 many-body Green's function 방법의 기준 상태로 자주 사용된다. 이 위키의 [GW approximation](../many-body-perturbation/gw-approximation.md)은 독립입자 기준에서 출발해 frequency-dependent self-energy로 quasiparticle energy를 다룬다. 두 방법의 orbital eigenvalue를 같은 물리량으로 간주하지 말고, 각각의 연산자와 근사를 확인해야 한다.

[Electron localization function](electron-localization-function.md)의 원래 유도도 HF 단일 determinant의 같은-spin pair density에서 시작한다. HF에서 exchange hole과 kinetic-energy density가 어떻게 생기는지를 이해하면 ELF가 전자 밀도 자체가 아니라 같은-spin 국소 회피를 정규화한 양이라는 점을 구분하기 쉬워진다.

!!! warning "[Interpretation Caveat]"
    SCF 수렴, basis 수렴과 물리 모형의 정확도는 서로 다른 문제이다. $\Delta E$와 density residual이 작아도 불안정한 HF 정상점일 수 있고, HF basis-set limit에 도달해도 단일 determinant 밖의 correlation은 남는다. Spin 상태, stability, basis와 후속 correlation 방법을 각각 독립적으로 점검해야 한다.[1–4]

## 7. 요약

- HF method는 반대칭 $N$전자 파동함수를 하나의 Slater determinant로 제한하여 에너지를 변분 최소화한다.
- HF 에너지는 one-electron 항과 $J-K$로 구성되며, exchange는 같은 spin 성분의 비국소 효과와 한 전자의 자기 Coulomb 항 상쇄를 포함한다.
- 궤도 변분은 $\hat f\chi_p=\epsilon_p\chi_p$를 주지만 Fock operator가 점유 궤도함수에 의존하므로 비선형 자기일관 문제이다.
- 유한 비직교 basis에서는 $\mathbf F\mathbf C=\mathbf S\mathbf C\boldsymbol\epsilon$을 밀도와 함께 반복해 푼다.
- SCF 수렴은 에너지와 density·commutator residual을 함께 확인하고, 수렴 뒤에도 orbital stability를 별도로 검사해야 한다.
- RHF, UHF와 ROHF는 spin 제약이 다르며, 더 낮은 UHF 에너지가 올바른 spin 대칭성을 보장하지 않는다.
- Basis-set limit는 단일 determinant 표현의 완성이지 electron correlation의 복원이 아니다.

## 8. 참고문헌

1. C. C. J. Roothaan, “New Developments in Molecular Orbital Theory,” *Reviews of Modern Physics* **23**, 69–89 (1951). [DOI: 10.1103/RevModPhys.23.69](https://doi.org/10.1103/RevModPhys.23.69).
2. S. Lehtola, F. Blockhuys, and C. Van Alsenoy, “An Overview of Self-Consistent Field Calculations Within Finite Basis Sets,” *Molecules* **25**, 1218 (2020). [DOI: 10.3390/molecules25051218](https://doi.org/10.3390/molecules25051218).
3. Psi4 developers, “HF: Hartree–Fock Theory,” official documentation (2026년 확인). [Documentation](https://psi4.github.io/psi4docs/master/scf.html).
4. S. Shahbazian and M. Zahedi, “Towards a complete basis set limit of Hartree–Fock method: correlation-consistent versus polarized-consistent basis sets,” *Theoretical Chemistry Accounts* **113**, 152–160 (2005). [DOI: 10.1007/s00214-005-0619-2](https://doi.org/10.1007/s00214-005-0619-2).
