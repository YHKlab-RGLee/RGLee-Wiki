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

실제 구현에서는 복소 제곱근 함수가 반환하는 주값을 위 식에 그대로 넣는 것만으로 retarded 가지가 정해지지 않는다. $w=z-\varepsilon$라 두면 필요한 제곱근은 큰 $|w|$에서 $w$와 같은 방향으로 접근해야 한다. 특히 band 아래쪽의 음의 실수 에너지에서는 양의 실수 제곱근을 계속 쓰면 $g_s^R\sim1/z$ 조건을 잃는다. 따라서 이차식의 두 후보를 계산한 뒤 상반평면에서의 인과성과 고에너지 점근 조건을 함께 검사하거나, 그 조건에 맞는 해를 에너지에 따라 연속적으로 추적해야 한다. Band 안의 허수부 부호만 확인하면 band 밖에서 잘못된 가지를 선택한 오류가 남을 수 있다.[2,3]

이차식은 올바른 해뿐 아니라 잘못된 해에서도 잔차가 0이다. 따라서 원래 표면 방정식의 잔차는 대수적 정확성을 검사하지만 물리적 경계조건까지 선택하지는 않는다. $\eta>0$를 유지한 상태에서 $\operatorname{Im}g_s^R\le0$를 확인하고, 전극 band 밖과 양·음의 큰 에너지까지 시험점을 포함해야 하는 이유가 여기에 있다. 행렬 문제에서도 작은 잔차와 retarded 응답의 음의 준정부호 조건을 별개로 확인한다.[2,3]

### (2) 전극 band와 broadening

실수 에너지에서 $|E-\varepsilon|<2|t|$이면 무한 사슬의 전파 band 안에 있으므로 $\operatorname{Im}g_s^R<0$이고 전극 broadening이 유한하다. Band 밖에서는 $\eta\rightarrow0^+$일 때 $g_s^R$가 실수가 되고 $\Gamma_\alpha$가 0으로 수렴한다. 따라서 analytic chain은 branch, 부호와 band edge를 확인하는 가장 작은 단위 시험이다.[2,3]

!!! info "[Measurement]"
    단일 사슬 구현에서는 수치해와 analytic $g_s^R$를 같은 $\eta$에서 비교한다. 비교에 사용할 양의 기준 에너지 $E_{\mathrm{ref}}$를 먼저 정하고, 에너지별 정규화 오차를

    $$
    \delta_g(E)
    =
    \frac{\|g_{s,\mathrm{num}}^R-g_{s,\mathrm{analytic}}^R\|_F}
    {\max(E_{\mathrm{ref}}^{-1},\|g_{s,\mathrm{analytic}}^R\|_F)}
    $$

    로 계산한다. Green's function의 단위가 에너지의 역수이므로 분모의 두 항도 같은 단위로 맞춘 것이다. 이후 오차 비교에도 같은 $E_{\mathrm{ref}}$를 사용하고, 에너지 단위를 바꿀 때 기준 에너지의 수치도 함께 변환한다. Band 안에서 $\operatorname{Im}g_s^R\le0$, band 밖에서 $\Gamma\rightarrow0$인지 함께 확인한다.[2,3]

### (3) 한 사이트 소자에 연결한 계산 예제

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

갱신식에서 표면과 내부의 onsite 보정이 다른 이유는 제거할 이웃의 수가 다르기 때문이다. 첫 반복에서 제거하는 홀수층의 대각 resolvent를 $g^{(0)}=(zI-H_0)^{-1}$라 하자. 표면 0번 층은 오른쪽의 1번 층으로 나갔다 돌아오는 경로만 가지므로 $Vg^{(0)}V^\dagger$가 더해진다. 내부의 2번 층은 왼쪽 1번 층과 오른쪽 3번 층을 모두 거치므로 $V^\dagger g^{(0)}V$와 $Vg^{(0)}V^\dagger$가 함께 더해진다. 같은 소거에서 0번에서 2번으로 가는 유효 결합은 $Vg^{(0)}V$가 된다. 이 경로를 각각 추적하면 표면 보정은 하나, 내부 보정은 둘이라는 차이와 행렬 곱의 순서를 동시에 확인할 수 있다.[2,3]

이 설명은 잘라낸 층을 물리적으로 없애는 근사가 아니라, 그 층의 진폭을 선형 방정식에서 풀어 남은 층의 식에 대입한다는 뜻이다. 제거한 층을 통한 전파는 에너지 의존적인 onsite와 hopping에 남는다. 따라서 반복 뒤의 $\alpha$와 $\beta$를 원래 Hamiltonian의 hopping과 같은 의미로 해석하면 안 된다. 특히 $z$가 복소수이므로 초기 직교 Hamiltonian에서 $\beta^{(0)}=\alpha^{(0)\dagger}$였더라도 이후의 유효 결합을 서로의 dagger로 강제해서는 안 된다. 두 갱신식을 같은 이전 반복값에서 각각 계산해야 소거한 선형계와 동등하다.[2,3]

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

    를 저장한다. $\operatorname{Im}g_s^R$가 음의 준정부호이고 $\Gamma_\alpha=i(\Sigma_\alpha^R-\Sigma_\alpha^A)$가 양의 준정부호인지 확인한다. 동일한 주기 전극을 소자와 양쪽 전극에 사용한 완전 결정 시험에서는 열린 각 mode가 불필요한 경계 반사 없이 전달되어야 한다.[2–4]

### (4) 유한 사슬과 수렴 검사의 구분

반무한 전극을 길이 $N$의 사슬로 잘라 직접 역행렬과 비교할 때에는 $N$과 $\eta$를 함께 지정해야 한다. 열린 끝을 가진 유한 사슬의 표면 응답을 $g_N$이라 쓰면, 같은 블록 소거에서

$$
g_1(z)=\frac{1}{z-\varepsilon},\qquad
g_{N+1}(z)=\frac{1}{z-\varepsilon-|t|^2g_N(z)}
$$

을 얻는다. 이 유한계는 끝에서 되돌아오는 반사를 포함한다. 따라서 작은 $N$의 결과가 반무한 analytic 해와 다르다는 사실만으로 decimation 구현이 틀렸다고 판단할 수 없다. 비교에는 먼저 유한 사슬의 직접 역행렬과 위 재귀식이 일치하는지 확인하는 대수 시험, 이어 고정된 양의 $\eta$에서 $N$을 늘려 반무한 해에 접근하는지 확인하는 경계 시험이 필요하다.[2,3]

이 구별은 극한을 취하는 순서에서도 드러난다. 유한 $N$의 Hermitian Hamiltonian은 이산 고유값을 가지므로, 고유값이 아닌 실수 $E$에서 먼저 $\eta\to0^+$를 취하면 대각 Green 함수의 허수부가 0으로 간다. 반면 반무한 사슬의 band 내부에는 연속적인 spectral weight가 있다. 따라서 고정된 유한 크기에서 $\eta$만 줄이는 계산은 반무한 전극의 매끄러운 band 응답을 재현하는 절차가 아니다. 이는 유한계의 spectral representation과 앞의 반무한 해를 비교하여 얻는 결론이며, 실제 시험에서는 길이 수렴을 먼저 확보한 뒤 broadening 의존성을 검사한다.[2,3]

수치 오차도 서로 다른 원인을 나누어 기록해야 한다. 반복 종료 오차는 같은 $\eta$에서 반복 허용 오차를 줄였을 때의 변화이다. Broadening 오차는 충분히 수렴한 해에서 $\eta$를 줄였을 때의 변화이다. Principal layer의 결합 누락은 이 두 조절로 해결되지 않는 모형 오류이다. 예를 들어 잔차가 작고 반복 횟수를 늘려도 결과가 같지만 균일 사슬 transmission이 틀리다면, hopping 방향이나 접촉 블록의 배치를 먼저 대조한다. 반대로 band edge 근처에서만 $\eta$에 민감하면 analytic 해도 같은 $\eta$로 계산했는지부터 확인한다.[2,3]

| 검사 | 고정하는 조건 | 변화시키는 조건 | 판별하는 문제 |
| --- | --- | --- | --- |
| 작은 유한계 직접 역행렬 | Hamiltonian, $N$, $\eta$ | 행렬 소거 구현 | 블록 순서·부호·갱신 오류 |
| 유한계 길이 수렴 | $E$, 양의 $\eta$, 결합 | $N$ | 먼 끝의 반사 영향 |
| Decimation 종료 수렴 | $E$, $\eta$, 전극 모형 | 반복 허용 오차 | 조기 종료 영향 |
| Retarded 극한 | 수렴한 반복·전극 모형 | 양의 $\eta$ | 인공 broadening 영향 |
| 균일 소자 연결 | 동일한 전극·소자 재료 | 경계 배치·명시적 층 수 | 계면 결합과 영역 분할 오류 |

이 표는 한 번의 작은 residual로 모든 검증을 대신하지 않기 위한 절차이다. 검사 결과에는 사용한 에너지 단위, $\eta$, 블록 크기, 결합 방향, 반복 횟수와 최대 잔차를 함께 남긴다. 그래야 같은 transmission 차이가 물리 모형의 변경인지 수치 설정의 변경인지 구별할 수 있다.

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

비직교 기저에서는 principal layer를 정할 때 Hamiltonian의 결합 범위뿐 아니라 overlap의 범위도 조사한다. $H_{02}=0$이어도 $S_{02}\ne0$이면 $zS-H$의 0번–2번 블록은 일반적으로 0이 아니므로 최근접층 소거식의 전제가 성립하지 않는다. 이 경우 원자층을 더 큰 블록으로 묶어 두 행렬을 함께 block-tridiagonal 형태로 만들어야 한다. 이는 계산 결과에 뒤늦게 보정을 붙이는 문제가 아니라, 반복에 넣을 선형계 자체를 정확하게 구성하는 문제이다.[3,4]

직교 극한도 항별로 확인할 수 있다. $S_{00}=I$, $S_{01}=S_{10}=0$을 대입하면 $e^{(0)}=zI-H_0$, $\alpha^{(0)}=V$, $\beta^{(0)}=V^\dagger$가 된다. $e=zI-\varepsilon$로 놓으면 energy matrix에서 보정항을 빼는 연산이 onsite $\varepsilon$에는 같은 항을 더하는 연산으로 바뀐다. 따라서 3절과 4절의 부호 차이는 서로 다른 물리 모형이 아니라 저장하는 행렬의 정의 차이이다. 두 구현을 비교할 때에는 중간 변수 이름보다 최종 $g_s^R$와 원래 $zS-H$ 방정식의 잔차를 비교하는 편이 명확하다.[3,4]

또한 overlap은 무차원이고 $z$와 Hamiltonian은 에너지 단위이므로 $H-zS$의 모든 항은 에너지 차원을 갖는다. Hamiltonian을 eV에서 다른 단위로 바꿀 때 $E$와 $\eta$도 같은 비율로 바꾸어야 하지만 $S$는 그대로 둔다. $\eta$만 이전 수치로 남기면 단순한 단위 변환이 아니라 상대 broadening을 바꾼 계산이 된다. 이 점검은 앞 절의 $E_{\mathrm{ref}}$를 사용한 무차원 잔차와 함께 적용한다.

### (2) 전극–소자 경계

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

로 들어간다. 이는 $zS-H$의 전극 블록을 소거한 결과이다.[4,6] $H$와 $S$가 Hermitian이어도 $K_{D\alpha}(z)^\dagger=H_{\alpha D}-z^*S_{\alpha D}$이므로, 유한한 $\eta$와 경계 overlap에서는 $K_{\alpha D}(z)$를 $K_{D\alpha}(z)^\dagger$로 바꿀 수 없다. 같은 이유로 4절(1)의 초기 $\beta^{(0)}$를 $\alpha^{(0)\dagger}$로 만들면 안 된다. 직교 기저에서는 경계 overlap이 0이므로 도입부의 $\tau_\alpha=H_{D\alpha}$와 $\tau_\alpha^\dagger$ 표현이 회복된다. 전극과 소자 사이의 전위 또는 구조가 아직 bulk-like하지 않은 층을 전극 반복단위에 억지로 포함하면 자기유사성 가정이 깨진다. 그런 층은 명시적 소자 영역에 포함하고, 경계가 충분히 주기적인 지점에서 전극 self-energy를 연결해야 한다.[4,5]

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

6. CP2K developers, "negf_green_methods.F," `negf_contact_self_energy`, lines 269–305, source revision `5b7fc9f`. [Source](https://doxygen.cp2k.org/dd/ddf/negf__green__methods_8F_source.html).
