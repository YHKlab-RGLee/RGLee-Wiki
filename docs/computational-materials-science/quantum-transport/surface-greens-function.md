---
description: 반무한 주기 전극의 표면 응답, analytic branch와 López Sancho repeated-doubling 알고리즘을 설명
---

# NEGF: Surface Green's function

Surface Green's function은 분리된 반무한 전극에서 소자와 직접 맞닿는 마지막 반복층의 retarded Green's function이다. Nonequilibrium Green's function (NEGF)의 기본 관계는 [NEGF formalism](negf-formalism.md)을 따른다. 전극 self-energy

$$
\Sigma_\alpha^R(E)
=\tau_\alpha g_{\alpha,s}^R(E)\tau_\alpha^\dagger
$$

를 계산하려면 반무한 전극 전체의 역행렬이 아니라 표면 블록 $g_{\alpha,s}^R$만 필요하다. 이 글은 직교 국소 기저와 최근접 principal layer 결합을 기준으로 표면 방정식, 단일 사슬의 해, López Sancho repeated-doubling과 수치 검증을 차례로 설명한다.[1–4]

Surface Green's function과 소자 Green's function은 역할이 다르다. 전자는 반복되는 전극의 outgoing 경계조건을 나타내고, 후자는 그 경계를 포함한 유한 소자의 응답을 나타낸다.[2–4]

## 1. 반무한 전극과 principal layer

### (1) Principal layer의 정의

반무한 주기 전극을 층 $n=0,1,2,\ldots$로 나누고 한 층의 Hamiltonian을 $H_0$, 오른쪽 인접 층으로의 결합을 $V=H_{n,n+1}$로 쓰자. **Principal layer**는 이 층보다 멀리 떨어진 층 사이의 직접 결합이 없도록 선택한 최소 반복 블록이다. 원래 모형에 더 먼 이웃 결합이 있으면 여러 원자층을 하나의 principal layer로 묶어 block-tridiagonal form을 만들어야 한다.[1–4]

층 내부 궤도 수를 $M$이라 하면 전극 Hamiltonian은

$$
H_\mathrm{lead}=
\begin{pmatrix}
H_0 & V & 0 & \cdots\\
V^\dagger & H_0 & V & \cdots\\
0 & V^\dagger & H_0 & \ddots\\
\vdots & \vdots & \ddots & \ddots
\end{pmatrix}
$$

이다. 표면은 $n=0$ 층이며, $n=1$부터 시작하는 나머지 반무한 전극은 원래 전극과 같은 구조를 가진다. 이 자기유사성이 무한한 층을 유한한 행렬 방정식으로 줄이는 핵심이다.[1–4]

!!! warning "[Interpretation Caveat]"
    원자층 하나가 항상 principal layer인 것은 아니다. 선택한 층을 건너뛰는 결합이 남으면 이후의 표면 방정식과 decimation 갱신식이 그 Hamiltonian을 정확히 나타내지 않는다. 먼저 결합 범위를 조사하고 필요한 원자층을 하나의 블록으로 묶어야 한다.[1–3]

### (2) 표면의 비선형 행렬 방정식

$z=E+i\eta$와 $\eta>0$를 두자. 표면층에서 내부로 한 층 이동한 뒤 보이는 반무한 구조도 원래 전극과 같으므로, 직교 기저의 retarded surface Green's function은

$$
g_s^R(E)
=
\left[
zI-H_0-Vg_s^R(E)V^\dagger
\right]^{-1}
$$

을 만족한다. 가운데의

$$
\Sigma_\mathrm{tail}^R=Vg_s^RV^\dagger
$$

는 표면에서 내부로 들어간 진폭이 반무한 전극 안에서 전파된 뒤 표면에 미치는 효과이다.[1–4]

$g_s^R$가 식의 양쪽에 모두 있으므로 한 번의 역행렬 계산으로 끝나지 않는다. 전극 mode를 풀어 내부로 진행하거나 감쇠하는 해를 고르는 방법과, 내부층을 반복적으로 제거하는 decimation 방법이 대표적이다. 여기서는 유효 층 사이의 거리를 반복마다 두 배로 늘리는 López Sancho 방법을 사용한다.[1–4]

## 2. 단일 궤도 사슬과 retarded branch

### (1) 대수적 해

각 층에 궤도가 하나이고 $H_0=\varepsilon$, $V=t$인 반무한 사슬을 보자. 표면 방정식은

$$
g_s^R
=
\frac{1}{z-\varepsilon-|t|^2g_s^R}
$$

이고,

$$
|t|^2(g_s^R)^2-(z-\varepsilon)g_s^R+1=0
$$

로 정리된다. 두 대수적 해 가운데 retarded 해는

$$
g_s^R(E)
=
\frac{
z-\varepsilon
-\sqrt{(z-\varepsilon)^2-4|t|^2}
}{
2|t|^2
}
$$

이다. 제곱근의 가지는 $\operatorname{Im}g_s^R\le0$이고 $|z|\rightarrow\infty$에서 $g_s^R\sim1/z$가 되도록 고른다.[2,3]

이 조건은 단순한 부호 선택이 아니다. Retarded Green's function은 전극 내부로 들어가는 전파 mode와 깊이에 따라 감쇠하는 evanescent mode를 선택해야 한다. 반대 가지는 advanced 경계조건이나 전극 내부로 갈수록 발산하는 해에 대응할 수 있다.[2,3]

### (2) 전극 band와 broadening

실수 에너지에서 $|E-\varepsilon|<2|t|$이면 무한 사슬의 전파 band 안에 있으므로 $\operatorname{Im}g_s^R<0$이고 전극 broadening이 유한하다. Band 밖에서는 $\eta\rightarrow0^+$일 때 $g_s^R$가 실수가 되고 $\Gamma_\alpha$가 0으로 수렴한다. 따라서 analytic chain은 branch, 부호와 band edge를 확인하는 가장 작은 단위 시험이다.[2,3]

!!! info "[Measurement]"
    단일 사슬 구현에서는 수치해와 analytic $g_s^R$를 같은 $\eta$에서 비교한다. 에너지별 상대 오차를

    $$
    \delta_g(E)
    =
    \frac{\|g_{s,\mathrm{num}}^R-g_{s,\mathrm{analytic}}^R\|_F}
    {\max(1,\|g_{s,\mathrm{analytic}}^R\|_F)}
    $$

    로 계산하고, band 안에서 $\operatorname{Im}g_s^R\le0$, band 밖에서 $\Gamma\rightarrow0$인지 함께 확인한다.[2,3]

## 3. López Sancho repeated-doubling

### (1) 초기화와 갱신식

직교 기저에서는 다음 네 행렬로 반복을 시작한다.

$$
\varepsilon_s^{(0)}=H_0,\qquad
\varepsilon^{(0)}=H_0,\qquad
\alpha^{(0)}=V,\qquad
\beta^{(0)}=V^\dagger.
$$

$\varepsilon_s^{(i)}$는 실제 표면층의 유효 onsite block이고, $\varepsilon^{(i)}$는 내부층의 유효 onsite block이다. $\alpha^{(i)}$와 $\beta^{(i)}$는 $i$번 decimation 뒤 남은 순방향·역방향 유효 결합이다. 각 반복에서

$$
g^{(i)}
=
\left[zI-\varepsilon^{(i)}\right]^{-1}
$$

을 계산하고

$$
\varepsilon_s^{(i+1)}
=
\varepsilon_s^{(i)}
+\alpha^{(i)}g^{(i)}\beta^{(i)},
$$

$$
\varepsilon^{(i+1)}
=
\varepsilon^{(i)}
+\alpha^{(i)}g^{(i)}\beta^{(i)}
+\beta^{(i)}g^{(i)}\alpha^{(i)},
$$

$$
\alpha^{(i+1)}
=
\alpha^{(i)}g^{(i)}\alpha^{(i)},
\qquad
\beta^{(i+1)}
=
\beta^{(i)}g^{(i)}\beta^{(i)}
$$

로 갱신한다.[1–4]

한 반복은 홀수 또는 짝수 층을 제거하고 남은 층 사이의 거리를 두 배로 만든다. $i$번 뒤의 유효 결합은 원래 약 $2^i$개 층을 건너뛴 결합을 나타낸다. 유효 결합이 충분히 작아지면

$$
g_s^R(E)
=
\left[zI-\varepsilon_s^{(\infty)}\right]^{-1}
$$

로 표면 응답을 얻는다. 최근접 principal-layer 모형 안에서 이 반복은 층 사이의 상호작용을 버리는 근사가 아니라 내부층을 순차적으로 소거하는 정확한 재배열이다.[1–4]

### (2) 구현 순서와 방향성

구현 순서는 다음과 같다.

1. 전극 결합 범위를 포함하도록 principal layer를 정하고 $H_0$, $V$를 만든다.
2. 관심 에너지마다 $z=E+i\eta$를 정하고 네 유효 행렬을 초기화한다.
3. $g^{(i)}$를 구한 뒤 $\varepsilon_s$, $\varepsilon$, $\alpha$, $\beta$를 이전 반복값만 사용해 동시에 갱신한다.
4. 유효 결합과 surface equation residual이 모두 허용 오차보다 작아질 때까지 반복한다.
5. $g_s^R$, $\Sigma_\alpha^R$와 $\Gamma_\alpha$를 계산하고 물리·수치 검사를 수행한다.

행렬 곱은 교환되지 않는다. $\alpha g\beta$와 $\beta g\alpha$의 순서를 바꾸거나 같은 반복에서 먼저 갱신한 값을 다른 식에 사용하면 다른 계산이 된다. 또한 왼쪽과 오른쪽 전극은 소자에서 전극 내부로 향하는 층 번호의 방향이 반대이므로 $V$와 $V^\dagger$의 배치를 각각 확인해야 한다.[1–4]

### (3) 수렴 종료 기준

유효 결합만 작아졌다고 종료하면 최종 $g_s^R$가 원래 표면 방정식을 만족하는지 알 수 없다. Frobenius norm을 사용하면

$$
r_{\mathrm{hop}}^{(i)}
=
\frac{
\max\left(\|\alpha^{(i)}\|_F,\|\beta^{(i)}\|_F\right)
}{
\max\left(1,\|zI-\varepsilon^{(i)}\|_F\right)
}
$$

와

$$
r_s
=
\frac{
\left\|
\left[zI-H_0-Vg_s^RV^\dagger\right]g_s^R-I
\right\|_F
}{
\|I\|_F
}
$$

를 함께 확인할 수 있다. 허용 오차는 부동소수점 정밀도와 이후에 필요한 transmission·전하 정확도에 맞춰 정하며, 모든 모형에 적용되는 하나의 숫자로 고정하지 않는다.[2–4]

$\eta$는 retarded branch를 선택하고 역행렬의 특이성을 완화하지만 인공적인 spectral broadening도 만든다. 너무 크면 band edge와 좁은 구조가 퍼지고, 너무 작으면 band edge나 표면 상태 근처에서 조건수가 나빠질 수 있다. 따라서 $\eta$를 줄이면서 전극 self-energy와 최종 관측량이 수렴하는지 확인해야 한다.[2–4]

!!! info "[Measurement]"
    각 전극과 에너지에서

    $$
    r_s(E),\qquad
    r_{\mathrm{hop}}(E),\qquad
    \delta_\Sigma(E)
    =
    \frac{
    \|\Sigma_\alpha^R(E;\eta)-\Sigma_\alpha^R(E;\eta/2)\|_F
    }{
    \max(1,\|\Sigma_\alpha^R(E;\eta/2)\|_F)
    }
    $$

    를 저장한다. $\operatorname{Im}g_s^R$가 음의 준정부호이고 $\Gamma_\alpha=i(\Sigma_\alpha^R-\Sigma_\alpha^A)$가 양의 준정부호인지 확인한다. 동일한 주기 전극을 소자와 양쪽 전극에 사용한 완전 결정 시험에서는 열린 각 mode가 불필요한 경계 반사 없이 전달되어야 한다.[2–4]

## 4. 비직교 기저와 실제 전극

### (1) Energy-matrix form

Overlap 행렬이 있는 non-orthogonal basis에서는 $zI-H$ 대신 $zS-H$를 일관되게 사용한다. 초기 energy matrix를

$$
e_s^{(0)}=e^{(0)}=zS_{00}-H_{00},
$$

$$
\alpha^{(0)}=H_{01}-zS_{01},
\qquad
\beta^{(0)}=H_{10}-zS_{10}
$$

로 구성하고

$$
a^{(i)}=\left[e^{(i)}\right]^{-1}\alpha^{(i)},
\qquad
b^{(i)}=\left[e^{(i)}\right]^{-1}\beta^{(i)}
$$

를 구한다. 이어서

$$
e_s^{(i+1)}
=e_s^{(i)}-\alpha^{(i)}b^{(i)},
$$

$$
e^{(i+1)}
=e^{(i)}-\beta^{(i)}a^{(i)}-\alpha^{(i)}b^{(i)},
$$

$$
\alpha^{(i+1)}=\alpha^{(i)}a^{(i)},
\qquad
\beta^{(i+1)}=\beta^{(i)}b^{(i)}
$$

로 decimation한다. 수렴 뒤에는 $g_s^R=\lim_i[e_s^{(i)}]^{-1}$이다. 이는 앞의 onsite 갱신식과 같은 소거를 $zS-H$ 규약으로 표현한 것이다.[1,4]

### (2) 전극–소자 경계

전극의 반복층 $H_0$, $V$와 소자 경계 결합 $\tau_\alpha$는 서로 다른 역할을 한다. 전극 decimation은 $g_{\alpha,s}^R$를 만들고, 실제 계면의 화학적·구조적 결합은

$$
\Sigma_\alpha^R
=\tau_\alpha g_{\alpha,s}^R\tau_\alpha^\dagger
$$

에서 따로 들어간다. 전극과 소자 사이의 전위 또는 구조가 아직 bulk-like하지 않은 층을 전극 반복단위에 억지로 포함하면 자기유사성 가정이 깨진다. 그런 층은 명시적 소자 영역에 포함하고, 경계가 충분히 주기적인 지점에서 전극 self-energy를 연결해야 한다.[4,5]

!!! warning "[Interpretation Caveat]"
    Surface Green's function이 수렴했다는 사실만으로 물리적인 접촉이 검증된 것은 아니다. 잘못된 principal layer, 반대 방향의 hopping, 너무 짧은 명시적 전극 완충영역도 작은 반복 residual을 만들 수 있다. 균일 전극 transmission과 소자 영역 길이 수렴을 별도로 검사해야 한다.[2–5]

## 5. 요약

- Surface Green's function은 반무한 전극 전체가 아니라 소자와 맞닿는 마지막 principal layer의 retarded 응답이다.
- Principal layer는 직접 결합이 인접 블록 사이에만 남도록 정해야 하며, 더 먼 결합은 더 큰 블록으로 흡수한다.
- 단일 사슬의 analytic 해는 retarded branch, band edge와 broadening의 부호를 점검하는 기준이다.
- López Sancho repeated-doubling은 내부층을 제거하면서 남은 층 사이의 거리를 두 배로 늘리고 표면 유효 onsite block을 수렴시킨다.
- 실제 구현에서는 유효 결합, 원래 표면 방정식 residual, $\eta$ 의존성, causality와 균일 전극 transmission을 함께 검사한다.

## 6. 참고문헌

1. M. P. López Sancho, J. M. López Sancho, and J. Rubio, "Highly convergent schemes for the calculation of bulk and surface Green functions," *Journal of Physics F: Metal Physics* **15**, 851–858 (1985). [DOI](https://doi.org/10.1088/0305-4608/15/4/009).
2. C. H. Lewenkopf and E. R. Mucciolo, "The recursive Green's function method for graphene," *Journal of Computational Electronics* **12**, 203–231 (2013). [DOI](https://doi.org/10.1007/s10825-013-0458-7), [arXiv](https://arxiv.org/abs/1304.3934).
3. X. Waintal, M. Wimmer, A. Akhmerov, C. Groth, B. K. Nikolić, M. Istas, T. Ö. Rosdahl, and D. Varjas, "Computational quantum transport: A scattering approach perspective," *arXiv:2407.16257v3* (2026). [arXiv](https://arxiv.org/abs/2407.16257).
4. T. Ozaki, K. Nishio, and H. Kino, "Efficient implementation of the nonequilibrium Green function method for electronic transport calculations," *Physical Review B* **81**, 035116 (2010). [DOI](https://doi.org/10.1103/PhysRevB.81.035116), [arXiv](https://arxiv.org/abs/0908.4142).
5. R. Lake, G. Klimeck, R. C. Bowen, and D. Jovanovic, "Single and multiband modeling of quantum electron transport through layered semiconductor devices," *Journal of Applied Physics* **81**, 7845–7869 (1997). [DOI](https://doi.org/10.1063/1.365394).
