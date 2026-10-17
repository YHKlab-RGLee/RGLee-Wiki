---
description: 반무한 전극의 principal layer와 표면 응답을 정의하고 단일 사슬 해석해, López Sancho decimation, 비직교 기저의 self-energy를 연결한다.
---

# Surface Green's function

Surface Green's function은 **소자에서 분리된 반무한 전극의 경계층 응답**이다. 반무한 전극의 모든 자유도를 소자 Hamiltonian에 직접 포함하지 않고, 경계 principal layer의 작은 Green's function 행렬만 계산하면 전극이 소자에 미치는 영향을 self-energy로 표현할 수 있다. 이 글은 주기적인 일전자 전극을 principal layer로 표현하고, 단일 사슬의 해석해에서 López Sancho decimation과 실제 접촉 계산으로 나아간다.[1–4]

Density functional theory (DFT)로 계산한 Hamiltonian을 입력하더라도, 먼저 전극의 반복 구조를 어떤 블록으로 표현할지와 블록 사이의 직접 결합이 어디까지 이어지는지를 확인해야 한다. Nonequilibrium Green's function (NEGF)의 전류·점유 관계는 [NEGF formalism](negf-formalism.md)을 따른다. 아래에서는 직교 국소 기저를 기준으로 설명한 뒤 비직교 원자 궤도 기저로 확장한다. 전극의 밀도·전위를 정하는 자기일관 계산과, 주어진 전극 행렬에서 표면 응답을 구하는 계산은 구별한다.[3,4]

## 1. 반무한 전극과 principal layer

### (1) 소자 경계와 반복 전극

전극은 유한 소자에 붙인 몇 개의 원자층으로 끝나지 않고 그 뒤로 계속 이어진다. 수송 계산에서는 소자 가까이의 구조·전위 변화를 명시적 소자 영역에 포함하고, 충분히 멀어져 주기성을 회복한 곳부터 동일한 전극 셀을 반복한다. 아래 그림에서는 검은 영역과 각각의 붉은 전극 사이가 그 계산 경계이다.[3,4]

<figure markdown="span">
![검은 유한 scattering region에 세 붉은 전극이 연결되고 각 전극의 첫째와 둘째 반복 셀 및 무한 연장을 나타내는 점이 표시된 모식도](images/negf-device-lead-partition.png)
<figcaption markdown="1">
그림 1. 세 단자 구조에서 각 전극은 독립적인 반무한 반복 영역이다. 진한 붉은 셀과 옅은 붉은 셀은 첫째와 둘째 셀이며, 이 글은 각 전극의 소자 쪽 경계 응답을 따로 계산한다. 출처: X. Waintal et al., “Computational quantum transport: a scattering approach perspective,” [arXiv:2407.16257v3](https://arxiv.org/abs/2407.16257v3), Fig. 3, p. 17, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). 수정하여 재현: 원본 PDF의 그림 영역을 잘라 PNG로 변환했으며 색과 표식은 변경하지 않았다.[3]
</figcaption>
</figure>

그림의 세 전극을 하나의 긴 사슬로 잇는 것은 아니다. 각 전극에서 소자로부터 전극 내부를 향해 층 번호를 매기고, 소자와 직접 맞닿는 층을 $n=0$으로 둔다. 여기서 ‘표면’은 진공과 만나는 실제 결정 표면이 아니라, **전극을 소자에서 분리했을 때 드러나는 계산 경계층**이다. 반무한 전극을 유한 길이로 잘라 닫힌 끝을 만들면 그 끝의 반사가 추가되므로 같은 경계조건이 아니다.[2–4]

### (2) Principal layer와 결합 범위

반무한 주기 전극을 층 $n=0,1,2,\ldots$로 나누고 한 층의 Hamiltonian을 $H_0$, 인접 층의 계수에서 현재 층의 방정식으로 작용하는 결합을 $V=H_{n,n+1}$로 쓰자. **Principal layer**는 이 층보다 멀리 떨어진 층 사이의 직접 결합이 없도록 선택한 반복 블록이다. 원래 모형에 더 먼 이웃 결합이 있으면 여러 원자층을 하나의 principal layer로 묶어 block-tridiagonal form을 만들어야 한다.[1–4]

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
    Principal layer 하나가 결정학적 원자층 하나에 반드시 대응하는 것은 아니다. 선택한 principal layer를 건너뛰는 직접 결합이 남아 있으면, 인접 블록 결합만 가정한 표면 Green's function 방정식과 decimation 갱신식은 원래 Hamiltonian을 정확하게 표현하지 못한다. 먼저 결합 범위를 조사하고 필요한 원자층을 하나의 블록으로 묶어야 한다.[1–3]

## 2. Surface Green's function

### (1) 표면 블록과 retarded 경계조건

실수 시험 에너지를 $E$, 양의 수치 broadening을 $\eta$라 하고 $z=E+i\eta$로 쓴다. 직교 기저에서 전체 전극 resolvent의 $n=0$ 대각 블록을 취하면 surface Green's function이 된다. $I$는 해당 공간의 항등행렬이다. 이하 $g_s^R(E)$는 별도 언급이 없으면 지정한 양의 $\eta$에서 평가한 $g_s^R(E+i\eta)$를 뜻한다.[2,3]

$$
g_s^R(z)=\left[(zI-H_{\mathrm{lead}})^{-1}\right]_{00}.
$$

전체 역행렬은 무한 차원이지만 이 블록은 $M\times M$이며 에너지의 역수 단위를 가진다. $\eta\to0^+$가 retarded 경계조건을 정한다. 전파 가능한 파동은 소자에서 전극 내부로 나가고, evanescent 성분은 내부로 갈수록 감쇠하는 해를 택한다. $g_s^R$에는 $n\ge1$인 모든 층의 효과가 포함되므로 고립된 한 층의 $(zI-H_0)^{-1}$와 다르다.[2,3]

소자 Green's function $G_D^R$는 양쪽 또는 여러 전극을 붙인 뒤 소자 영역에서 계산하는 응답이다. 같은 재료의 한 층을 소자로 정해도 전극 표면은 한쪽에만 이웃이 있고 소자는 두 방향 전극에 연결될 수 있으므로 두 함수는 같지 않다. 행렬의 크기가 같다는 이유로 $g_s^R$를 $G_D^R$ 자리에 넣으면 접촉 경계조건을 잘못 계산한다.[2,3]

### (2) 자기유사성과 표면 방정식

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

## 3. 단일 궤도 사슬

### (1) Bulk band와 전파 조건

먼저 무한한 직교 tight-binding 사슬에서 각 사이트의 onsite energy를 $\varepsilon$, 실수인 최근접 hopping을 $t\ne0$, 격자 간격을 $a$라 하자. [Coherent quantum transport](coherent-quantum-transport.md)의 hopping $-t_0$ ($t_0>0$)와 onsite $\varepsilon_c$는 여기서 $t=-t_0$, $\varepsilon=\varepsilon_c$에 대응한다. 파수 $k$의 Bloch 진폭 $\psi_n=e^{ikna}\psi_0$를 사이트 방정식에 대입하면 다음 분산관계를 얻는다. 이는 일반적인 전극 Bloch 방정식의 단일 궤도 특수 경우이다.[2,3]

$$
E\psi_n=\varepsilon\psi_n+t\psi_{n+1}+t\psi_{n-1},
\qquad E(k)=\varepsilon+2t\cos(ka).
$$

따라서 실수 $k$가 존재하는 band는 $\varepsilon-2|t|\le E\le\varepsilon+2|t|$이다. $t<0$인 관례를 쓰면 band 최소점이 $k=0$에 놓이지만 band 폭 $4|t|$은 변하지 않는다. Band 내부에는 서로 반대 방향으로 진행하는 해가 있고, band 밖에서는 복소 파수의 감쇠 해를 사용한다. 반무한 사슬의 경계 응답은 이 bulk 분산관계에 표면이라는 경계조건을 더한 결과이다.[2,3]

### (2) 해석해와 retarded branch

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

실제 구현에서는 복소 제곱근 함수가 반환하는 주값을 위 식에 그대로 넣는 것만으로 retarded 가지가 정해지지 않는다. $w=z-\varepsilon$라 두면 필요한 제곱근은 큰 $|w|$에서 $w$와 같은 방향으로 접근해야 한다. 특히 band 아래쪽의 음의 실수 에너지에서는 양의 실수 제곱근을 계속 쓰면 $g_s^R\sim1/z$ 조건을 잃는다. 따라서 이차식의 두 후보를 계산한 뒤 상반평면에서의 인과성과 고에너지 점근 조건을 함께 검사하거나, 그 조건에 맞는 해를 에너지에 따라 연속적으로 추적해야 한다. Band 안의 허수부 부호만 확인하면 band 밖에서 잘못된 가지를 선택한 오류가 남을 수 있다.[2,3]

이차식은 올바른 해뿐 아니라 잘못된 해에서도 잔차가 0이다. 따라서 원래 표면 방정식의 잔차는 대수적 정확성을 검사하지만 물리적 경계조건까지 선택하지는 않는다. $\eta>0$를 유지한 상태에서 $\operatorname{Im}g_s^R\le0$를 확인하고, 전극 band 밖과 양·음의 큰 에너지까지 시험점을 포함해야 하는 이유가 여기에 있다. 행렬 문제에서도 작은 잔차와 retarded 응답의 음의 준정부호 조건을 별개로 확인한다.[2,3]

### (3) Band edge와 해석해 검증

실수 에너지에서 $|E-\varepsilon|<2|t|$이면 무한 사슬의 전파 band 안에 있으므로 $\operatorname{Im}g_s^R<0$이고 전극 broadening이 유한하다. Band 밖에서는 $\eta\rightarrow0^+$일 때 $g_s^R$가 실수가 되고 $\Gamma_\alpha$가 0으로 수렴한다. 따라서 사슬의 해석해는 branch, 부호와 band edge를 확인하는 가장 작은 단위 시험이다.[2,3]

!!! info "[Measurement]"
    단일 사슬 구현에서는 수치해와 해석해 $g_s^R$를 같은 $\eta$에서 비교한다. 비교에 사용할 양의 기준 에너지 $E_{\mathrm{ref}}$를 먼저 정하고, 에너지별 정규화 오차를

    $$
    \delta_g(E)
    =
    \frac{\|g_{s,\mathrm{num}}^R-g_{s,\mathrm{analytic}}^R\|_F}
    {\max(E_{\mathrm{ref}}^{-1},\|g_{s,\mathrm{analytic}}^R\|_F)}
    $$

    로 계산한다. Green's function의 단위가 에너지의 역수이므로 분모의 두 항도 같은 단위로 맞춘 것이다. 이후 오차 비교에도 같은 $E_{\mathrm{ref}}$를 사용하고, 에너지 단위를 바꿀 때 기준 에너지의 수치도 함께 변환한다. Band 안에서 $\operatorname{Im}g_s^R\le0$, band 밖에서 $\Gamma\rightarrow0$인지 함께 확인한다.[2,3]

## 4. López Sancho decimation

### (1) 층 소거와 갱신식

Decimation은 내부층의 계수를 풀어 남길 층의 방정식에 대입하는 블록 소거이다. 일반적인 [Downfolding and effective Hamiltonians](../../computational-science/model-reduction/downfolding.md)의 Schur complement를 주기 사슬에 반복 적용한 것으로, 이때 버린 층의 전파 효과는 에너지 의존적인 유효 항에 남는다. López Sancho 방법은 한 층씩 붙이는 대신 번갈아 놓인 층을 한꺼번에 소거해 남은 층의 간격을 두 배씩 늘린다.[1–4]

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

갱신식에서 표면과 내부의 onsite 보정이 다른 이유는 제거할 이웃의 수가 다르기 때문이다. 첫 반복에서 제거하는 홀수층의 대각 resolvent를 $g^{(0)}=(zI-H_0)^{-1}$라 하자. 표면 0번 층에는 오른쪽의 1번 층으로 나갔다 돌아오는 경로만 있으므로 $Vg^{(0)}V^\dagger$가 더해진다. 내부의 2번 층은 왼쪽 1번 층과 오른쪽 3번 층을 모두 거치므로 $V^\dagger g^{(0)}V$와 $Vg^{(0)}V^\dagger$가 함께 더해진다. 같은 소거에서 0번에서 2번으로 가는 유효 결합은 $Vg^{(0)}V$가 된다. 이 경로를 각각 추적하면 표면 보정은 하나, 내부 보정은 둘이라는 차이와 행렬 곱의 순서를 동시에 확인할 수 있다.[2,3]

이 설명은 잘라낸 층을 물리적으로 없애는 근사가 아니라, 그 층의 진폭을 선형 방정식에서 풀어 남은 층의 식에 대입한다는 뜻이다. 제거한 층을 통한 전파는 에너지 의존적인 onsite와 hopping에 남는다. 따라서 반복 뒤의 $\alpha$와 $\beta$를 원래 Hamiltonian의 hopping과 같은 의미로 해석하면 안 된다. 특히 $z$가 복소수이므로 초기 직교 Hamiltonian에서 $\beta^{(0)}=\alpha^{(0)\dagger}$였더라도 이후의 유효 결합을 서로의 dagger로 강제해서는 안 된다. 두 갱신식을 같은 이전 반복값에서 각각 계산해야 소거한 선형계와 동등하다.[2,3]

### (2) 구현 순서와 방향성

구현 순서는 다음과 같다.

1. 전극 결합 범위를 포함하도록 principal layer를 정하고 $H_0$, $V$를 만든다.
2. 관심 에너지마다 $z=E+i\eta$를 정하고 네 유효 행렬을 초기화한다.
3. $g^{(i)}$를 구한 뒤 $\varepsilon_s$, $\varepsilon$, $\alpha$, $\beta$를 이전 반복값만 사용해 동시에 갱신한다.
4. 유효 결합과 표면 방정식의 잔차가 모두 허용 오차보다 작아질 때까지 반복한다.
5. $g_s^R$, $\Sigma_\alpha^R$와 $\Gamma_\alpha$를 계산하고 물리·수치 검사를 수행한다.

행렬 곱은 교환되지 않는다. $\alpha g\beta$와 $\beta g\alpha$의 순서를 바꾸거나 같은 반복에서 먼저 갱신한 값을 다른 식에 사용하면 다른 계산이 된다. 또한 왼쪽과 오른쪽 전극은 소자에서 전극 내부로 향하는 층 번호의 방향이 반대이므로 $V$와 $V^\dagger$의 배치를 각각 확인해야 한다.[1–4]

### (3) 수렴 종료 기준

Decimation 반복에서 유효 결합의 크기가 작아졌다는 사실만으로는 최종 surface Green's function $g_s^R$가 원래 표면 방정식을 정확히 만족한다고 판단할 수 없다. Frobenius norm을 사용하면

$$
r_{\mathrm{hop}}^{(i)}
=
\frac{
\max\left(\|\alpha^{(i)}\|_F,\|\beta^{(i)}\|_F\right)
}{
\max\left(E_{\mathrm{ref}},\|zI-\varepsilon^{(i)}\|_F\right)
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

를 함께 확인할 수 있다. $r_{\mathrm{hop}}$의 분자와 분모는 에너지 단위이고 $r_s$의 행렬 곱은 무차원이므로 두 잔차 모두 무차원이다. 허용 오차는 부동소수점 정밀도와 이후에 필요한 transmission·전하 정확도에 맞춰 정하며, 모든 모형에 적용되는 하나의 숫자로 고정하지 않는다.[2–4]

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
    \max(E_{\mathrm{ref}},\|\Sigma_\alpha^R(E;\eta/2)\|_F)
    }
    $$

    를 저장한다. 이 직교 기저 검사에서 행렬 허수부는 $\operatorname{Im}g=(g-g^\dagger)/(2i)$이며, $\operatorname{Im}g_s^R$가 음의 준정부호이고 $\Gamma_\alpha=i(\Sigma_\alpha^R-\Sigma_\alpha^A)$가 양의 준정부호인지 확인한다. 동일한 주기 전극을 소자와 양쪽 전극에 사용한 완전 결정 시험에서는 열린 각 mode가 불필요한 경계 반사 없이 전달되어야 한다.[2–4]

### (4) NumPy 구현과 해석해 비교

아래 예제는 Python 3와 NumPy로 실행한다. 에너지는 eV, $E_{\mathrm{ref}}=1$ eV이며, `surface`는 $e=zS-H$를 저장하는 형태로 작성했다. 직교 기저에서는 `s`, `q`를 생략한다. 비직교 입력의 뜻은 6절에서 설명한다. `solve`로 각 선형계를 풀고 이전 단계의 값으로 네 행렬을 동시에 갱신한다. 허용 오차와 최대 반복 횟수는 이 예제의 선택이며 모든 전극에 대한 보장은 아니다.[2,4,5]

```python
import numpy as np

def surface(z, h, v, s=None, q=None, tol=1e-13):
    """V=H[n,n+1], Q=S[n,n+1]; all energies in eV."""
    eye = np.eye(len(h), dtype=complex)
    s = eye if s is None else s
    q = np.zeros_like(v) if q is None else q
    e = z*s - h
    es = e.copy()
    a, b = v-z*q, v.conj().T-z*q.conj().T
    e0, a0, b0 = e.copy(), a.copy(), b.copy()
    for count in range(200):
        x, y = np.linalg.solve(e, a), np.linalg.solve(e, b)
        es, e, a, b = es-a@y, e-a@y-b@x, a@x, b@y
        rhop = max(np.linalg.norm(a), np.linalg.norm(b))/max(1., np.linalg.norm(e))
        if rhop < tol:
            g = np.linalg.solve(es, eye)
            residual = np.linalg.norm((e0-a0@g@b0)@g-eye)/np.linalg.norm(eye)
            if residual > 1e-8:
                raise RuntimeError(f"surface residual {residual:g}")
            return g, count+1, residual
    raise RuntimeError("decimation did not converge")

def analytic(z, eps=0., t=1.):
    w = z-eps
    root = np.sqrt(w*w-4*abs(t)**2+0j)
    if root.imag < 0:
        root = -root
    return 2/(w+root)  # rationalized physical root, eta>0

h, v = np.array([[0.]]), np.array([[1.]])
energies = [-10., -2.1, -2., -1.3, 0., .7, 2., 2.1, 10.]
errors, residuals, counts = [], [], []
for energy in energies:
    z = energy+1e-3j
    g, n, r = surface(z, h, v)
    errors.append(abs(g[0,0]-analytic(z)))
    residuals.append(r)
    counts.append(n)
print("scalar max error/residual/iterations", max(errors), max(residuals), max(counts))
assert max(errors) < 1e-8

```

제곱근 `root`의 허수부를 양수로 고르면 $\eta>0$인 scalar 문제의 retarded 가지가 된다. `2/(w+root)`는 위 해석해를 유리화한 같은 식으로, band에서 멀리 떨어졌을 때 두 큰 수를 빼는 연산을 피한다. 이차식 잔차와 인과성을 함께 확인해야 한다는 원칙은 그대로 적용된다.[2,3]

실행 결과에서 9개 에너지의 최대 절대 오차는 약 $2.92\times10^{-11}$ eV$^{-1}$, 최대 표면 잔차는 $5.84\times10^{-11}$, 최대 반복 수는 16이었다. 이 값들은 제시한 모형·입력으로 직접 계산한 검산 결과이며 다른 행렬이나 더 작은 $\eta$에서의 오차 상한이 아니다. 이 예제는 band 안팎과 두 band edge를 같은 양의 $\eta$에서 비교한다.

## 5. 전극 self-energy와 소자 연결

### (1) 계면 결합과 embedding

전극 $\alpha$의 표면 응답 $g_{\alpha,s}^R$를 구한 뒤에는 실제 계면 Hamiltonian 블록 $\tau_\alpha=H_{D\alpha}$로 소자 $D$에 연결한다. 직교 기저에서 $\tau_\alpha$는 소자 궤도 수와 표면층 궤도 수를 행·열 크기로 갖는다. 전극 자유도를 소거하면 다음 관계가 성립한다.[2,3]

$$
\Sigma_\alpha^R(z)=\tau_\alpha g_{\alpha,s}^R(z)\tau_\alpha^\dagger,
\qquad
G_D^R(z)=\left[zI-H_D-\sum_\alpha\Sigma_\alpha^R(z)\right]^{-1}.
$$

$H_D$는 명시적 소자의 Hamiltonian이다. $\Sigma_\alpha^R$는 소자와 같은 행렬 크기와 에너지 단위를 가지며, 전극으로 나갔다가 돌아오는 진폭의 효과를 담는다. 실수 에너지의 retarded 극한에서 Hermitian 부분은 준위 이동, $\Gamma_\alpha=i(\Sigma_\alpha^R-\Sigma_\alpha^{R\dagger})$는 전극으로 탈출하는 폭을 나타낸다. 반무한 전극 내부의 반복 결합 $V$와 소자–전극 계면 결합 $\tau_\alpha$는 서로 다른 위치의 결합을 나타낸다. 두 블록이 같은 값으로 놓일 수 있는지는 전극과 소자가 실제로 동일한 구조로 연속 연결되는지에 따라 판단해야 한다.[2,3]

### (2) 균일 사슬의 transmission

표면 응답이 실제 소자 계산에 어떻게 들어가는지는 같은 단일 사슬을 양쪽 전극으로 둔 한 사이트 소자에서 확인할 수 있다. 소자의 onsite도 $\varepsilon$이고 두 접촉 hopping의 크기도 $|t|$라고 하자. Spin을 따로 세지 않는 하나의 궤도 모형이며, 별도 산란이나 비탄성 self-energy는 없다. 양 전극에 동일한 표면 해를 적용하면

$$
\Sigma_L^R=\Sigma_R^R=|t|^2g_s^R,\qquad
G_D^R=\left[z-\varepsilon-2|t|^2g_s^R\right]^{-1}.
$$

소자에서 보이는 양쪽 반무한 tail을 모두 포함한 식이다. 이를 한쪽 tail만 포함하는 $g_s^R$와 구별해야 한다. 두 함수는 같은 재료로 만들어졌어도 경계가 달라 서로 같지 않다. 이 예제는 전극 self-energy와 소자 역행렬을 연결하는 기존 NEGF 식에 단일 사슬을 대입한 결과이다.[2,3]

Band 안에서 $d=E-\varepsilon$, $b=\sqrt{4|t|^2-d^2}>0$라 놓고 $\eta\to0^+$를 취하면

$$
g_s^R=\frac{d-ib}{2|t|^2},\qquad
\Gamma_L=\Gamma_R=b,\qquad
G_D^R=\frac{1}{ib}.
$$

따라서 이 모형의 transmission은 $\mathcal{T}=\Gamma_L\Gamma_R|G_D^R|^2=1$이다. 외부에서 가져온 측정값이 아니라 위 식을 직접 대입한 해석적 결과이다. 전극과 소자를 같은 사슬로 이어 놓았으므로, 인위적으로 나눈 경계에서 반사가 생기지 않는다는 검사에 해당한다. 정확한 band edge에서는 $b=0$이므로 이 형태의 $0\times\infty$를 직접 계산하지 않고 band 내부에서 접근한 극한을 비교한다. 유한한 $\eta$에서는 소자 resolvent에도 인공적인 감쇠가 들어가므로 transmission이 정확히 1이어야 한다고 요구하지 않고 $\eta$ 감소에 따른 접근을 확인한다.[2,3]

같은 식으로 접촉 결합과 전극 재료의 효과를 분리할 수 있다. 전극 내부 hopping은 그대로 두고 실제 계면 결합만 $\tau$로 바꾸면 표면 $g_s^R$는 그대로이고 $\Sigma^R=|\tau|^2g_s^R$가 바뀐다. 즉 전극 band 폭을 바꾸는 조작과 접촉을 약하게 만드는 조작은 서로 다르다. 결합이 약해졌다는 이유로 전극 자체의 $t$까지 함께 바꾸면 접촉뿐 아니라 전극의 상태 분포도 바꾼 계산이 된다. 일반 행렬에서도 전극 반복 결합 $V$와 소자–전극 결합 $\tau$를 별도의 입력으로 관리해야 한다.[2,3]

앞 절의 함수와 단일 사슬 입력에 이어 아래 코드를 실행하면, 소자 onsite $\varepsilon=0$ eV와 $E=0.7$ eV에서 $\eta$ 의존성을 검사할 수 있다. $\Gamma$와 $G_D$를 각각 계산하므로 표면 응답만 맞는지와 실제 소자 연결까지 맞는지를 구별한다.[2,3]

```python
for eta in [1e-2, 1e-4, 1e-6]:
    z = .7+1j*eta
    gs, _, _ = surface(z, h, v)
    sigma = gs[0,0]  # |t|^2=1
    gamma = -2*sigma.imag
    gd = 1/(z-2*sigma)
    trans = gamma**2*abs(gd)**2
    print("eta, T", eta, trans)
    assert 0 < trans < 1
assert abs(trans-1) < 2e-6
```

실행한 transmission은 $\eta=10^{-2},10^{-4},10^{-6}$ eV에서 각각 약 0.98934952, 0.99989325, 0.99999893이었다. 제시한 코드에서 얻은 수치이며, 무반사 극한 $\mathcal T=1$에 접근한다. Band edge의 정확한 점에서는 이 수열을 같은 방식으로 해석하지 않는다.

## 6. 비직교 기저와 수치 검증

### (1) Energy matrix 표현

양의 정부호 overlap 행렬 $S$를 가진 비직교 기저에서는 $zI-H$ 대신 $zS-H$를 일관되게 사용한다. 초기 energy matrix를

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

로 decimation한다. 수렴 뒤에는 $g_s^R=\lim_i[e_s^{(i)}]^{-1}$이다. 이는 앞의 onsite 갱신식과 같은 소거를 $zS-H$ 규약으로 표현한 것이다.[4,5]

비직교 기저에서는 principal layer를 정할 때 Hamiltonian의 결합 범위뿐 아니라 overlap의 범위도 조사한다. $H_{02}=0$이어도 $S_{02}\ne0$이면 $zS-H$의 0번–2번 블록은 일반적으로 0이 아니므로 최근접층 소거식의 전제가 성립하지 않는다. 이 경우 원자층을 더 큰 블록으로 묶어 두 행렬을 함께 block-tridiagonal 형태로 만들어야 한다. 이는 계산 결과에 뒤늦게 보정을 붙이는 문제가 아니라, 반복에 넣을 선형계 자체를 정확하게 구성하는 문제이다.[3,4]

직교 극한도 항별로 확인할 수 있다. $S_{00}=I$, $S_{01}=S_{10}=0$을 대입하면 $e^{(0)}=zI-H_0$, $\alpha^{(0)}=V$, $\beta^{(0)}=V^\dagger$가 된다. $e=zI-\varepsilon$로 놓으면 energy matrix에서 보정항을 빼는 연산이 onsite $\varepsilon$에는 같은 항을 더하는 연산으로 바뀐다. 따라서 4절과 6절의 부호 차이는 서로 다른 물리 모형이 아니라 저장하는 행렬의 정의 차이이다. 두 구현을 비교할 때에는 중간 변수 이름보다 최종 $g_s^R$와 원래 $zS-H$ 방정식의 잔차를 비교하는 편이 명확하다.[3,4]

또한 overlap은 무차원이고 $z$와 Hamiltonian은 에너지 단위이므로 $H-zS$의 모든 항은 에너지 차원을 갖는다. Hamiltonian을 eV에서 다른 단위로 바꿀 때 $E$와 $\eta$도 같은 비율로 바꾸어야 하지만 $S$는 그대로 둔다. $\eta$만 이전 수치로 남기면 단순한 단위 변환이 아니라 상대 broadening을 바꾼 계산이 된다. 이 점검은 앞 절의 $E_{\mathrm{ref}}$를 사용한 무차원 잔차와 함께 적용한다.[3,4]

### (2) 같은 복소 에너지의 경계 결합

전극의 반복층 $H_0$, $V$와 소자–전극 경계 결합은 서로 다른 역할을 한다. 소자 영역을 $D$, 접촉하는 전극 표면층을 $\alpha$라 쓰고 비직교 기저의 두 방향 결합을 먼저 정의한다.

$$
K_{D\alpha}(z)=H_{D\alpha}-zS_{D\alpha},\qquad
K_{\alpha D}(z)=H_{\alpha D}-zS_{\alpha D}.
$$

전극 decimation은 $g_{\alpha,s}^R(z)$를 만들고, 실제 계면의 결합은 같은 복소 에너지 $z$에서

$$
\Sigma_\alpha^R(z)
=K_{D\alpha}(z)g_{\alpha,s}^R(z)K_{\alpha D}(z)
$$

로 들어간다. 이는 $zS-H$의 전극 블록을 소거한 결과이다.[4,5] $H$와 $S$가 Hermitian이어도 $K_{D\alpha}(z)^\dagger=H_{\alpha D}-z^*S_{\alpha D}$이므로, 유한한 $\eta$와 경계 overlap에서는 $K_{\alpha D}(z)$를 $K_{D\alpha}(z)^\dagger$로 바꿀 수 없다. 같은 이유로 6절(1)의 초기 $\beta^{(0)}$를 $\alpha^{(0)\dagger}$로 만들면 안 된다. 직교 기저에서는 경계 overlap이 0이므로 5절의 $\tau_\alpha=H_{D\alpha}$와 $\tau_\alpha^\dagger$ 표현이 회복된다. 전극과 소자 사이의 전위 또는 구조가 아직 bulk-like하지 않은 층을 전극 반복단위에 억지로 포함하면 자기유사성 가정이 깨진다. 그런 층은 명시적 소자 영역에 포함하고, 경계가 충분히 주기적인 지점에서 전극 self-energy를 연결해야 한다.[3,4]

!!! warning "[Interpretation Caveat]"
    Surface Green's function이 수렴했다는 사실만으로 물리적인 접촉이 검증된 것은 아니다. 잘못된 principal layer, 반대 방향의 hopping, 너무 짧은 명시적 전극 완충영역도 작은 반복 잔차를 만들 수 있다. 균일 전극 transmission과 소자 영역 길이 수렴을 별도로 검사해야 한다.[2–4]

비직교 기저에서 유한한 $\eta$를 쓸 때에는 broadening의 부호 검사를 그대로 옮기지 않도록 주의한다. $\Sigma=K_{D\alpha}(z)gK_{\alpha D}(z)$는 유한 $\eta$에서 $K g K^\dagger$ 꼴이 아니므로 $i(\Sigma-\Sigma^\dagger)$만의 양의 준정부호성을 위 직교 증명으로 보장할 수 없다. 물리적 전극 폭은 실수 에너지의 $\eta\to0^+$ 극한에서 해석하고, 유한 $\eta$의 구현은 전체 $zS-H$ 블록 소거와 대조한다. 이는 같은 $z$를 사용하는 경계식에서 얻는 대수적 귀결이다.[3,4,5]

### (3) 유한계 대조와 수렴 한계

반무한 전극을 길이 $N$의 사슬로 잘라 직접 역행렬과 비교할 때에는 $N$과 $\eta$를 함께 지정해야 한다. 열린 끝을 가진 유한 사슬의 표면 응답을 $g_N$이라 쓰면, 같은 블록 소거에서

$$
g_1(z)=\frac{1}{z-\varepsilon},\qquad
g_{N+1}(z)=\frac{1}{z-\varepsilon-|t|^2g_N(z)}
$$

을 얻는다. 이 유한계는 끝에서 되돌아오는 반사를 포함한다. 따라서 작은 $N$의 결과가 반무한 해석해와 다르다는 사실만으로 decimation 구현이 틀렸다고 판단할 수 없다. 비교에는 먼저 유한 사슬의 직접 역행렬과 위 재귀식이 일치하는지 확인하는 대수 시험, 이어 고정된 양의 $\eta$에서 $N$을 늘려 반무한 해에 접근하는지 확인하는 경계 시험이 필요하다.[2,3]

이 구별은 극한을 취하는 순서에서도 드러난다. 유한 $N$의 Hermitian Hamiltonian은 이산 고유값을 가지므로, 고유값이 아닌 실수 $E$에서 먼저 $\eta\to0^+$를 취하면 대각 Green's function의 허수부가 0으로 간다. 반면 반무한 사슬의 band 내부에는 연속적인 spectral weight가 있다. 따라서 고정된 유한 크기에서 $\eta$만 줄이는 계산은 반무한 전극의 매끄러운 band 응답을 재현하는 절차가 아니다. 이는 유한계의 spectral representation과 앞의 반무한 해를 비교하여 얻는 결론이며, 실제 시험에서는 길이 수렴을 먼저 확보한 뒤 broadening 의존성을 검사한다.[2,3]

수치 오차도 원인별로 나누어 기록해야 한다. 반복 종료 오차는 같은 $\eta$에서 반복 허용 오차를 줄였을 때의 변화이다. Broadening 오차는 충분히 수렴한 해에서 $\eta$를 줄였을 때의 변화이다. Principal layer의 결합 누락은 이 두 조절로 해결되지 않는 모형 오류이다. 예를 들어 잔차가 작고 반복 횟수를 늘려도 결과가 같지만 균일 사슬 transmission이 틀리다면, hopping 방향이나 접촉 블록의 배치를 먼저 대조한다. 반대로 band edge 근처에서만 $\eta$에 민감하면 해석해도 같은 $\eta$로 계산했는지부터 확인한다.[2,3]

| 검사 | 고정하는 조건 | 변화시키는 조건 | 판별하는 문제 |
| --- | --- | --- | --- |
| 작은 유한계 직접 역행렬 | Hamiltonian, $N$, $\eta$ | 행렬 소거 구현 | 블록 순서·부호·갱신 오류 |
| 유한계 길이 수렴 | $E$, 양의 $\eta$, 결합 | $N$ | 먼 끝의 반사 영향 |
| Decimation 종료 수렴 | $E$, $\eta$, 전극 모형 | 반복 허용 오차 | 조기 종료 영향 |
| Retarded 극한 | 수렴한 반복·전극 모형 | 양의 $\eta$ | 인공 broadening 영향 |
| 균일 소자 연결 | 동일한 전극·소자 재료 | 경계 배치·명시적 층 수 | 계면 결합과 영역 분할 오류 |

이 표는 한 번의 작은 잔차로 모든 검증을 대신하지 않기 위한 절차이다. 검사 결과에는 사용한 에너지 단위, $\eta$, 블록 크기, 결합 방향, 반복 횟수와 최대 잔차를 함께 남긴다. 그래야 같은 transmission 차이가 물리 모형의 변경인지 수치 설정의 변경인지 구별할 수 있다.

### (4) 행렬 순서와 비직교 검산

Scalar 사슬에서는 곱의 순서 오류가 드러나지 않는다. 다음 코드는 앞의 `surface` 정의 뒤에 이어 실행하며, 서로 교환되지 않는 두 궤도 블록과 overlap을 사용한다. 160층 tail 소거와 반무한 decimation을 비교하고, 별도로 12층의 전체 역행렬과 같은 길이의 tail 소거를 대조한다. 두 비교는 각각 길이 수렴과 블록 대수를 검사한다. 입력 $S$의 양의 정부호성과 같은 $z$를 사용하는 Schur complement는 비직교 기저 계산의 전제이다.[3,4,5]

```python
# Noncommuting matrix lead: independent finite-chain inverse and tail recursion.
h2 = np.array([[.2, .13j], [-.13j, -.3]])
v2 = np.array([[.7, .2j], [.1, -.4]])
s2 = np.array([[1., .03], [.03, 1.1]])
q2 = np.array([[.04, .01j], [.02, -.03]])
z = .31+.12j
for nonorth in [False, True]:
    s = s2 if nonorth else np.eye(2)
    q = q2 if nonorth else np.zeros((2,2))
    e, a, b = z*s-h2, v2-z*q, v2.conj().T-z*q.conj().T
    gs, _, r = surface(z, h2, v2, s, q)
    finite = np.linalg.inv(e)
    for n in range(1, 160):
        finite = np.linalg.inv(e-a@finite@b)
    error = np.linalg.norm(gs-finite)
    # Direct 12-layer inverse vs finite recursion, at exactly the same N.
    n = 12
    mat = np.kron(np.eye(n), e)-np.kron(np.eye(n,k=1),a)-np.kron(np.eye(n,k=-1),b)
    direct = np.linalg.inv(mat)[:2,:2]
    tail = np.linalg.inv(e)
    for _ in range(n-1):
        tail = np.linalg.inv(e-a@tail@b)
    print("matrix nonorth/error/residual/direct", nonorth, error, r, np.linalg.norm(direct-tail))
    assert error < 1e-10 and np.linalg.norm(direct-tail) < 1e-12
    if nonorth:
        overlap = np.kron(np.eye(n),s)+np.kron(np.eye(n,k=1),q)+np.kron(np.eye(n,k=-1),q.conj().T)
        print("finite overlap minimum eigenvalue", np.linalg.eigvalsh(overlap).min())
        correct = np.linalg.inv(e-a@np.linalg.inv(e)@b)
        wrong = np.linalg.inv(e-a@np.linalg.inv(e)@a.conj().T)
        full = np.linalg.inv(np.block([[e,-a],[-b,e]]))[:2,:2]
        print("same-z Schur error/wrong-dagger error", np.linalg.norm(correct-full), np.linalg.norm(wrong-full))
        assert np.linalg.norm(correct-full) < 1e-12 and np.linalg.norm(wrong-full) > 1e-3
```

위 입력에서 160층과 반무한 해의 차이는 직교·비직교 경우 모두 $1.1\times10^{-14}$ eV$^{-1}$ 미만이었고, 12층 직접 역행렬과 재귀식의 차이는 $8.3\times10^{-16}$ eV$^{-1}$ 미만이었다. 비직교 12층 overlap의 최소 고유값은 약 0.9213이었다. 마지막 두 블록 검산에서는 같은 $z$를 사용한 식의 오차가 $1.8\times10^{-16}$ eV$^{-1}$ 정도인 반면, 역방향 결합을 잘못 dagger로 만든 결과는 약 $2.43\times10^{-2}$ eV$^{-1}$ 달랐다. 이는 표시된 인공 모형을 실행한 결과이며 물질 계산의 정확도 기준은 아니다.

## 7. 요약

- Surface Green's function은 반무한 전극 전체가 아니라 소자와 맞닿는 마지막 principal layer의 retarded 응답이다.
- Principal layer는 직접 결합이 인접 블록 사이에만 남도록 정해야 하며, 더 먼 결합은 더 큰 블록으로 흡수한다.
- 단일 사슬의 해석해는 retarded branch, band edge와 broadening의 부호를 점검하는 기준이다.
- López Sancho repeated-doubling은 내부층을 제거하면서 남은 층 사이의 거리를 두 배로 늘리고 표면 유효 onsite block을 수렴시킨다.
- 실제 구현에서는 유효 결합, 원래 표면 방정식의 잔차, $\eta$ 의존성, causality와 균일 전극 transmission을 함께 검사한다.

## 8. 참고문헌

1. M. P. López Sancho, J. M. López Sancho, and J. Rubio, "Highly convergent schemes for the calculation of bulk and surface Green functions," *Journal of Physics F: Metal Physics* **15**, 851–858 (1985). [DOI](https://doi.org/10.1088/0305-4608/15/4/009).
2. C. H. Lewenkopf and E. R. Mucciolo, "The recursive Green's function method for graphene," *Journal of Computational Electronics* **12**, 203–231 (2013). [DOI](https://doi.org/10.1007/s10825-013-0458-7), [arXiv](https://arxiv.org/abs/1304.3934).
3. X. Waintal, M. Wimmer, A. Akhmerov, C. Groth, B. K. Nikolić, M. Istas, T. Ö. Rosdahl, and D. Varjas, "Computational quantum transport: A scattering approach perspective," *arXiv:2407.16257v3* (2026). [arXiv](https://arxiv.org/abs/2407.16257).
4. T. Ozaki, K. Nishio, and H. Kino, "Efficient implementation of the nonequilibrium Green function method for electronic transport calculations," *Physical Review B* **81**, 035116 (2010). [DOI](https://doi.org/10.1103/PhysRevB.81.035116), [arXiv](https://arxiv.org/abs/0908.4142).

5. CP2K developers, "negf_green_methods.F," `do_sancho`, `negf_contact_self_energy`, lines 223–305 (접근: 2026-10-15). [Source](https://doxygen.cp2k.org/dd/ddf/negf__green__methods_8F_source.html).
