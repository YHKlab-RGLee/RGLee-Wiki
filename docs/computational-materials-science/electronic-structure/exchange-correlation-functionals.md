---
description: LDA에서 hybrid까지 XC 범함수의 개발 배경과 물성별 개선 효과를 비교하고 PBE의 exchange enhancement factor 설계 및 주요 exact constraints를 설명한다.
---

# Exchange–correlation functionals

Exchange–correlation (XC) 범함수는 밀도범함수 이론(DFT)에서 결합 에너지, 평형 구조와 전자구조를 예측하는 정확도를 좌우하는 주요 근사이다. 범함수 개발은 이전 방법이 충분히 설명하지 못했던 물성과 결합 환경을 더 잘 기술하려는 과정으로 발전해 왔다. Local density approximation (LDA)의 국소 근사에서 출발한 generalized gradient approximation (GGA)은 원자·분자의 비균일한 밀도를 다루는 능력을 개선했고, PBE for solids (PBEsol)은 GGA의 고체 격자 상수 예측을 다시 최적화했다. Strongly constrained and appropriately normed (SCAN) meta-GGA는 다양한 결합 환경에서 구조와 에너지의 균형을 개선했으며, hybrid 범함수는 nonlocal Fock exchange를 도입하여 많은 반도체의 band gap 예측을 개선했다.[3,4,7–9,14]

**Jacob’s ladder**는 이러한 범함수를 사용하는 입력 정보에 따라 분류한다. 위쪽 단계로 올라갈수록 새로운 정보를 활용할 수 있지만, 실제 정확도는 목표 물성과 범함수의 설계에 따라 달라진다. 이 문서에서는 각 단계의 개발 동기, 에너지 식의 구조, 대표적인 성능 개선과 남아 있는 한계를 연결하여 설명한다.[1–4]

[Density functional theory](density-functional-theory.md) (DFT)의 Kohn–Sham (KS) 구성과 자기일관 계산을 선행 지식으로 삼는다. 여기서는 원자핵의 위치를 고정한 비상대론적 바닥상태를 기준으로 각 범함수의 물리적 가정과 설계 방법을 설명한다. 특히 GGA의 exchange enhancement factor를 실제로 구성하는 절차와 범함수의 self-consistent 계산에 필요한 수치적 고려사항을 다룬다. Hartree 원자단위계 $\hbar=m_e=e=4\pi\varepsilon_0=1$을 사용하고, 궤도 자기장과 전류가 없는 경우를 다룬다. $m_e$는 전자 질량, $e$는 기본 전하의 양의 크기, $\varepsilon_0$는 진공 유전율이다. 자성 물성을 다룰 때에는 spin 채널을 분리한다. 다만 아래의 LDA·GGA 대표식과 SCAN 지표는 별도 언급이 없으면 spin 비편극 상태의 전체 전자 밀도로 표현한다.[1,2]

## 1. Exchange–correlation functional의 근사

### (1) Kohn–Sham 에너지와 XC 근사

전자 수밀도를 $n(\mathbf r)$, 전자 수를 $N$이라 하면 정규화는 다음과 같다. $\mathbf r$는 공간 좌표이며, $n$은 전하밀도가 아니라 부피당 전자 수이다.[1,2]

$$
\int n(\mathbf r)\,d\mathbf r=N.
$$

KS 전자 에너지의 분해는

$$
E[n]=T_s[n]+E_{\mathrm H}[n]+\int v_{\mathrm{ext}}(\mathbf r)n(\mathbf r)\,d\mathbf r+E_{\mathrm{xc}}[n]
$$

이다. $T_s$는 보조 비상호작용계의 운동에너지, $E_{\mathrm H}$는 고전적 전자 밀도의 Coulomb 반발, $v_{\mathrm{ext}}$는 전자 한 개가 느끼는 외부 potential energy이다. 핵–핵 반발은 구조별 총에너지를 비교할 때 별도로 더한다. 실제 상호작용계의 운동에너지를 $T$, 전자–전자 반발 에너지를 $W$라 하면 XC의 정확한 정의는 다음과 같다.[1,2]

$$
E_{\mathrm{xc}}=(T-T_s)+(W-E_{\mathrm H}).
$$

이때 Hartree 에너지는

$$
E_{\mathrm H}[n]=\frac12\iint\frac{n(\mathbf r)n(\mathbf r')}{|\mathbf r-\mathbf r'|}\,d\mathbf r\,d\mathbf r'
$$

이다. 두 밀도 요소 사이의 Coulomb 에너지를 적분하며, $1/2$는 쌍의 중복 계수를 막는다. 이 고전적 항에는 전자가 자기 자신의 밀도와 상호작용하는 기여도 들어가므로 XC와 함께 해석해야 한다.[1,2]

정확한 XC 에너지는 Hartree 항으로 기술하는 고전적인 Coulomb 반발을 넘어서는 전자 간 상호작용과 운동에너지의 차이 $(T-T_s)$를 함께 포함한다. **LDA·GGA·meta-GGA·hybrid에서는 바로 이 $E_{\mathrm{xc}}$의 형태를 근사한다.** 선택한 XC 근사로부터 유효 potential 또는 generalized Kohn–Sham 연산자를 만들고, 그 해로 밀도와 궤도함수를 다시 갱신한다. 따라서 범함수를 바꾸면 XC 에너지뿐 아니라 self-consistent density, orbital, band structure와 총에너지도 함께 달라질 수 있다.[1,2]

### (2) Jacob’s ladder와 범함수의 설계 목표

범함수의 단계는 계산에 사용하는 입력 변수로 구분한다. LDA는 국소 밀도 $n$, GGA는 밀도 기울기 $\nabla n$, meta-GGA는 추가로 kinetic-energy density $\tau$ 등을 사용한다. Hybrid 범함수에서는 서로 다른 공간점의 궤도함수를 연결하는 Fock exchange 적분이 도입된다. GGA와 meta-GGA를 통틀어 **semilocal**이라 부르며, meta-GGA는 $\tau$를 통해 궤도함수에도 의존한다. 같은 단계에 속하는 범함수라도 만족시키려는 exact constraints와 정확도를 높이려는 물성은 서로 다를 수 있다.[2,3,9,15]

| 단계 | 새로 사용하는 정보 | 대표 범함수 | 개발 동기와 주된 개선 대상 |
| --- | --- | --- | --- |
| LDA | 국소 밀도 $n$ | 균일 전자기체 기반 LDA | 균일 전자기체의 정확한 정보를 실제 비균일계의 각 점에 적용 |
| GGA | 밀도 기울기 $\nabla n$ | PBE, PBEsol | LDA의 원자화·결합 에너지 오차 개선(PBE), 조밀한 고체의 평형 격자·표면 에너지 개선(PBEsol) |
| Meta-GGA | $\tau$ 또는 $\nabla^2n$ | SCAN, rSCAN, r²SCAN | 단일 궤도·금속적·약한 결합 영역의 차이 반영; 다양한 결합의 구조·형성 에너지 및 수치 안정성 개선 |
| Hybrid | Nonlocal Fock exchange | PBE0, HSE | Delocalization 및 exchange 관련 오차 완화; 많은 반도체·절연체의 band gap 개선 |
| 상위 correlation 근사 | 비점유 상태·응답 정보 등 | Double hybrid, random phase approximation (RPA) 계열 | Semilocal 범위를 넘는 correlation 및 비국소 응답 기술 |

이 표는 각 범함수가 **어떤 정보를 추가했고 어떤 문제를 개선하려 했는지**를 비교한다. 다섯째 단계의 double hybrid와 random phase approximation (RPA) 계열은 비점유 상태와 응답 정보를 correlation 계산에 활용한다. 반면 같은 GGA 단계에서도 PBE와 PBEsol은 성능을 우선한 물성이 다르다. 따라서 특정 물성에 대한 정확도는 Jacob’s ladder의 위치뿐 아니라 선택한 함수의 구조와 설계 조건으로 판단해야 한다.[1–5,7–9]

## 2. LDA: 균일 전자기체의 국소 적용

### (1) 국소 근사의 의미

LDA는 실제 밀도의 각 공간점에 대해 **그 점과 같은 전자 밀도를 갖는 균일 전자기체의 XC 에너지**를 사용한다. 균일 전자기체는 exchange를 해석적으로 구할 수 있고 correlation도 높은 정확도의 기준 자료로 매개화할 수 있어, 비균일계의 XC 에너지를 구성하는 출발점이 되었다. 균일계의 전자당 XC 에너지를 $\varepsilon_{\mathrm{xc}}^{\mathrm{unif}}$라 하면

$$
E_{\mathrm{xc}}^{\mathrm{LDA}}[n]=\int n(\mathbf r)\varepsilon_{\mathrm{xc}}^{\mathrm{unif}}(n(\mathbf r))\,d\mathbf r
$$

이다. 실제 결정과 분자에서는 비균일한 핵 potential을 사용해 KS 방정식을 풀고, 각 위치에서 계산된 $n(\mathbf r)$를 균일 전자기체의 XC 에너지 밀도에 대입한다. 근사가 도입되는 곳은 실제 밀도를 계산하는 과정이 아니라, 그 밀도에서 XC 에너지를 평가하는 규칙이다.[1,2,6]

Spin 비편극 균일 전자기체의 exchange 에너지는 전자당

$$
\varepsilon_{\mathrm x}^{\mathrm{unif}}(n)=-\frac34\left(\frac3\pi\right)^{1/3}n^{1/3}
$$

이다. 음의 부호는 exchange가 Hartree 기준 에너지를 낮춘다는 뜻이다. 이 식은 균일계 exchange에 대해서는 정확하지만, 실제 비균일계에 국소적으로 대입한 결과는 근사이다. Correlation에는 균일 상호작용 전자기체에 대한 별도 자료와 매개화가 필요하다. 따라서 LDA라는 계열명만 쓰기보다 실제 exchange·correlation 조합도 기록하는 것이 좋다.[1,6]

Spin 분극을 다룰 때에는 spin-up과 spin-down 밀도 $n_\uparrow,n_\downarrow$를 각각 사용하는 local spin density approximation (LSDA)으로 확장한다. 이렇게 해야 두 spin 채널의 점유 차이가 exchange–correlation 에너지에 반영된다.[1,2]

### (2) 잘 맞는 물성과 대표 오차

LDA는 계산 비용이 낮고 조밀한 고체의 평형 구조를 비교하는 기준으로 널리 사용되었다. 그러나 원자·분자처럼 밀도가 급격히 변하는 영역을 균일 전자기체의 국소 값으로 처리하는 과정에서 원자화 에너지와 결합 에너지에 상당한 오차가 남는다. 여러 고체 benchmark에서는 격자 상수를 짧게, 응집을 강하게 예측하는 경향이 나타난다. GGA는 이러한 비균일 밀도 환경을 더 정확히 다루기 위해 발전했으며, 실제 오차의 크기와 방향은 물질군별로 검증한다.[4,7,9,19]

| 비교 대상 | LDA에서 기대할 수 있는 역할 | 별도 확인할 한계 |
| --- | --- | --- |
| 조밀한 고체의 평형 구조 | 단순한 기준 계산, 일부 계의 양호한 격자 상수 | 격자 과소평가와 bulk modulus 오차 |
| 분자 결합·고체 응집 | 결합 형성의 정성적 기술 | 과도한 결합과 원자 기준 에너지 오차 |
| 반도체 전자구조 | 밴드와 밀도의 출발점 | 고윳값 gap의 큰 과소평가 |
| 멀리 떨어진 중성 부분계 | 국소 환경의 XC 기술 | 올바른 장거리 dispersion 부재 |

표의 구조·응집 경향은 고체와 원자화 에너지 비교, gap과 장거리 한계는 전자구조 및 nonlocal 상호작용 분석에 근거한다.[1,4,5,7,8] 따라서 LDA의 성능은 격자 상수, 결합·응집 에너지, band gap을 각각 구분하여 평가한다. 어느 한 물성에서 작은 오차가 나타났더라도 다른 물성에는 별도의 검증이 필요하다.

## 3. GGA: 밀도 기울기와 설계 목표

### (1) 비균일성의 표현

LDA는 각 위치의 밀도만으로 XC 에너지를 평가하므로, 동일한 밀도를 갖더라도 주변으로의 밀도 변화가 다른 영역을 구분하지 못한다. GGA는 $\nabla n$을 입력에 추가하여 원자·분자의 표면과 결합 주변처럼 밀도가 공간적으로 변하는 환경을 기술한다. $e_{\mathrm{xc}}$를 부피당 에너지로 쓰면 대표 형식은

$$
E_{\mathrm{xc}}^{\mathrm{GGA}}[n]=\int e_{\mathrm{xc}}(n,\nabla n)\,d\mathbf r
$$

이다. 앞 절의 $\varepsilon_{\mathrm{xc}}$와 달리 $e_{\mathrm{xc}}$에는 밀도 인자가 포함된다. GGA는 각 공간점의 밀도와 기울기에 의존하는 에너지 함수를 구성한다. Gradient expansion이 천천히 변하는 밀도 주변의 항별 근사라면, GGA는 실제 비균일계까지 다루기 위해 그 전개의 계수와 다른 정확한 극한·제약을 함께 반영한 함수 형태를 사용한다.[1,2,6]

Spin 비편극 exchange의 비균일성을 비교할 때 국소 Fermi 파수 $k_F$와 무차원 reduced density gradient $s$를 쓴다.[6,9]

$$
k_F=(3\pi^2n)^{1/3},\qquad s=\frac{|\nabla n|}{2k_Fn}.
$$

$s$는 밀도의 절대 기울기를 국소 전자 길이 척도에 맞춰 정규화한다. 따라서 같은 $|\nabla n|$이라도 밀도가 다르면 $s$가 달라진다. 이를 이용한 exchange enhancement factor $F_{\mathrm x}$의 정의는

$$
E_{\mathrm x}^{\mathrm{GGA}}=\int n\varepsilon_{\mathrm x}^{\mathrm{unif}}(n)F_{\mathrm x}(s)\,d\mathbf r
$$

이다. $F_{\mathrm x}(s)$는 해당 위치에서 균일 전자기체의 exchange 에너지 밀도를 얼마나 수정할지 정하는 무차원 함수이다. $s=0$이면 균일계 exchange를 회복하고, $s$가 증가할수록 밀도 변화의 효과를 반영한다. 이 식은 exchange에 대한 설계이며, correlation은 별도의 함수와 조건으로 구성한다.[6,9,15,19]

천천히 변하는 밀도에서의 개념적 전개는

$$
F_{\mathrm x}(s)=1+\mu s^2+\cdots\qquad(s\to0)
$$

로 쓴다. $\mu$는 작은 밀도 기울기에 대해 exchange 보정이 얼마나 빠르게 증가하는지를 결정하는 계수이다. 함수의 전체 형태는 작은 기울기에서의 전개 계수뿐 아니라 큰 $s$에서의 거동과 exact constraints를 함께 고려하여 정한다. 실제 PBE와 PBEsol이 동일한 함수 형태를 사용하면서도 다른 물성에 강점을 보이는 이유가 여기에 있다.[7,9,15,19]

### (2) Exchange enhancement factor $F_x$의 설계

$F_{\mathrm x}(s)$를 설계할 때에는 먼저 **정확히 만족해야 할 물리적 극한과 수학적 제약**을 정한다. 그런 다음 이 조건을 만족하는 함수 형태를 선택하고, 남은 매개변수를 다른 정확한 조건이나 신뢰할 수 있는 기준계의 정보로 결정한다. PBE의 exchange enhancement factor는 이 절차를 구체적으로 보여 주는 예이다.[9,15,19]

PBE는 균일계에서 $F_{\mathrm x}(0)=1$을 만족하면서, 작은 기울기의 보정 계수를 $\mu$로 제어하고, 큰 기울기에서는 정해진 상한에 부드럽게 접근하도록 다음 유리함수를 사용한다.[15,19]

$$
F_{\mathrm x}^{\mathrm{PBE}}(s)
=1+\kappa-\frac{\kappa}{1+\mu s^2/\kappa}
=1+\frac{\mu s^2}{1+\mu s^2/\kappa}.
$$

이 함수의 매개변수는 **$\mu$와 $\kappa$ 두 개**이다. $\mu$는 작은 기울기에서의 곡률을 정하고, $\kappa$는 큰 기울기에서 도달할 보정의 최대 크기를 정한다. 식을 전개하면 다음 관계를 직접 확인할 수 있다.

$$
F_{\mathrm x}(0)=1,\qquad
F_{\mathrm x}(s)=1+\mu s^2+O(s^4)\quad(s\to0),\qquad
\lim_{s\to\infty}F_{\mathrm x}(s)=1+\kappa.
$$

따라서 설계자는 작은 기울기의 정확한 거동을 제어하면서도 큰 기울기에서 $F_{\mathrm x}$가 무제한 증가하지 않도록 할 수 있다. PBE는 $\kappa=0.804$를 사용해 exchange 에너지에 대한 제약을 만족시키는 충분조건을 구성한다. PBE는 전체 XC 에너지에 대한 Lieb–Oxford bound를 고려하여 $F_{\mathrm x}$에 더 강한 점별 제한을 부과한다. 전체 공간에 대한 적분 부등식과 각 공간점에 대한 제한은 서로 다른 수준의 조건이다.[15,16,19]

**매개변수 선택에는 exchange와 correlation의 결합도 고려한다.** PBE correlation의 gradient 계수 $\beta=0.066725$를 기준으로 균일 전자기체의 LDA linear response를 회복하도록 $\mu=\pi^2\beta/3\approx0.21951$을 선택한다. 반면 PBEsol은 조밀한 고체의 천천히 변하는 밀도에 대한 정확한 exchange gradient expansion을 중시하여 $\mu=10/81\approx0.12346$으로 바꾼다. PBEsol의 correlation 계수 $\beta=0.046$은 jellium surface의 XC 에너지에 맞추어 조정한 값이다.[9,15,19]

| 매개변수·기준 | PBE | PBEsol |
| --- | --- | --- |
| 작은 기울기 exchange 계수 $\mu$ | $\approx0.21951$ | $10/81\approx0.12346$ |
| Correlation 계수 $\beta$ | $0.066725$ | $0.046$ |
| 큰 기울기 상한에 쓰는 $\kappa$ | $0.804$ | $0.804$ |
| $F_{\mathrm x}(s=1)$ | $\approx1.1724$ | $\approx1.1070$ |
| 주된 설계 기준 | Uniform-gas linear response와 원자 에너지 특성 | Exchange gradient expansion과 jellium surface 에너지 |

이 수치를 PBE의 함수식에 대입하면, 같은 국소 밀도와 기울기에서 PBEsol의 exchange 보정이 PBE보다 작게 나타나는 이유를 확인할 수 있다. 균일계 exchange 에너지 밀도는 음수이므로 $F_{\mathrm x}$가 커지면 해당 위치의 exchange 에너지는 더 음의 방향으로 변한다. **실제 결합 에너지와 격자 상수는 exchange와 correlation, 원자 기준 상태 및 self-consistent density를 모두 포함하여 비교한다.** 실제 물성 오차의 방향과 크기는 완성된 XC 범함수로 자기일관 계산한 결과를 기준값과 비교하여 판단한다.[7,9,15]

!!! note "계산 코드에서 $F_x$를 구현하는 순서"
    1. Self-consistent density $n(\mathbf r)$와 $\nabla n(\mathbf r)$에서 $k_F$와 $s$를 계산한다.
    2. 선택한 범함수의 $\mu,\kappa$로 $F_{\mathrm x}(s)$를 평가하고, $n\varepsilon_{\mathrm x}^{\mathrm{unif}}(n)F_{\mathrm x}(s)$를 적분하여 exchange 에너지를 구한다.
    3. Correlation은 해당 범함수에 정의된 별도의 함수와 계수로 계산한다. 전체 XC 범함수를 구현하려면 exchange와 correlation 두 부분이 모두 필요하다.
    4. Self-consistent 계산에는 에너지뿐 아니라 밀도에 대한 함수 미분도 필요하다. Spin 비편극 GGA의 exchange 에너지 밀도를 $e_{\mathrm x}(n,\nabla n)$이라 쓰면, 충분히 매끄러운 밀도에서 다음 관계로 국소 exchange potential을 얻는다.

    $$
    v_{\mathrm x}(\mathbf r)=
    \frac{\partial e_{\mathrm x}}{\partial n}
    -\nabla\cdot\frac{\partial e_{\mathrm x}}{\partial(\nabla n)}.
    $$

    5. 구현에서는 $s\to0$의 균일계 한계, 작은 밀도에서의 수치 안정성, 에너지와 potential의 일관성, 적분 격자 수렴을 확인한다. Spin-polarized 계산에서는 같은 exchange 설계를 spin scaling 관계에 맞게 확장한다.[1,2,15,19]

이 과정은 **함수의 형태를 설계하는 작업**과 **그 함수로 에너지·potential을 실제 계산하는 작업**을 연결한다. GGA에서 $F_{\mathrm x}(s)$를 만들 때 사용하는 exact constraints의 의미는 제6절에서 설명한다.

### (3) PBE와 PBEsol의 설계 목표와 물성

Perdew–Burke–Ernzerhof (PBE)는 LDA보다 원자·분자의 비균일한 밀도를 잘 다루면서도, uniform electron gas의 linear response와 exchange·correlation의 정확한 조건을 만족하도록 개발되었다. 이전 GGA인 Perdew–Wang 1991 (PW91)의 복잡한 형태를 더 단순한 함수로 정리하고 매끄러운 potential을 구성한 것도 PBE의 설계 목표였다. PBE는 LDA보다 분자의 atomization energy 등에서 개선을 보였지만, 조밀한 고체의 격자 상수를 과대평가하는 경향이 남았다.[1,7,15,19]

PBEsol은 바로 이 고체 구조 오차를 줄이기 위해 PBE의 함수 형태를 유지하면서 exchange gradient coefficient를 $10/81$로 복원했다. Correlation의 $\beta$도 jellium surface 에너지에 맞추어 변경했다. 이렇게 고체의 평형 부피·격자 상수와 표면 에너지를 개선했지만, 분자 atomization energy에서는 PBE보다 불리한 경우가 많다. **PBE와 PBEsol은 입력 정보가 같은 GGA이지만 서로 다른 물성을 우선해 설계한 범함수**이다.[4,7,9,15]

| 비교 축 | PBE | PBEsol |
| --- | --- | --- |
| 주요 개선 대상 | LDA에 비해 분자 atomization energy·비균일 밀도 기술 개선 | PBE에 비해 조밀한 고체의 격자 상수·표면 에너지 개선 |
| 함수 설계 | Uniform-gas linear response 및 다양한 정확한 조건 | Exchange의 이차 gradient expansion 및 jellium surface 기준 |
| 격자 상수 경향 | 여러 고체에서 과대평가 | 과대평가 완화 |
| 상대적인 약점 | 조밀한 고체의 구조 예측 오차 | 분자의 atomization energy에서 PBE보다 불리한 경우 |
| 실제 평가 | 원자화·결합·응집 에너지 | 격자 상수·bulk modulus·표면 에너지 |

구조 최적화에는 PBEsol이 유리한 물질군이 많지만, 화합물의 형성 에너지나 원자화 에너지까지 함께 연구한다면 PBE와의 비교가 필요하다. 실제 물질의 상 안정성을 결정하는 에너지 차이는 평형 격자 상수와 서로 다른 물리량이므로, 해당 물성에 대한 benchmark를 기준으로 범함수를 선택한다.[4,7,9]

## 4. Meta-GGA: 결합 환경의 구별과 SCAN

### (1) 운동에너지 밀도

GGA는 $n$과 $\nabla n$으로 밀도 변화의 크기를 알 수 있지만, 그 밀도가 단일 궤도에 집중되어 있는지 여러 궤도가 겹쳐 있는지까지 충분히 구별하기 어렵다. 이 차이는 공유 결합, 조밀한 금속 결합, 약한 결합을 함께 기술할 때 중요하다. **Meta-GGA는 orbital kinetic-energy density $\tau$ 등을 추가**하여 동일한 밀도와 기울기에서도 다른 궤도 환경에 서로 다른 XC 에너지를 적용할 수 있게 한다. SCAN 계열의 대표 형식은 다음과 같다.[2,3,6,15]

$$
E_{\mathrm{xc}}^{\mathrm{meta-GGA}}=\int e_{\mathrm{xc}}(n,\nabla n,\tau)\,d\mathbf r.
$$

Spin 채널을 $\sigma$, 정규화된 공간 궤도함수를 $\phi_{i\sigma}$, 그 점유수를 $f_{i\sigma}\in[0,1]$이라 하면

$$
\tau(\mathbf r)=\frac12\sum_{i,\sigma}f_{i\sigma}|\nabla\phi_{i\sigma}(\mathbf r)|^2
$$

이다. 이 문서에서는 $1/2$를 포함하고 두 spin 채널을 합한다. $\tau$의 차원은 원자단위계에서 길이의 역다섯제곱이며, 공간 적분은 보조계의 운동에너지 $T_s$를 준다. 다른 문헌의 spin별 $\tau_\sigma$ 또는 $1/2$ 없는 정의와 비교할 때 인자를 맞춰야 한다. Meta-GGA에는 밀도 Laplacian $\nabla^2n$을 쓰는 형태도 있지만 SCAN을 이해하는 데 필요한 추가 변수는 $\tau$이다.[2,3,6]

$\tau$는 점유 궤도함수의 기울기에서 계산되므로, $\tau$ 기반 meta-GGA는 궤도함수 의존성까지 고려하는 generalized Kohn–Sham (GKS) 형식으로 흔히 구현한다. 함수에 들어가는 정보는 기존 GGA보다 풍부하지만, 계산 과정에서는 여전히 각 공간점의 $n$, $\nabla n$, $\tau$를 사용하므로 hybrid의 두 공간점 사이 Fock exchange 적분과 구별된다.[1,2,10]

### (2) Iso-orbital indicator

SCAN에서는 운동에너지 밀도 $\tau$만으로 국소 환경을 판단하지 않고, 단일 궤도 한계와 균일 전자기체 한계를 나타내는 두 기준값과 비교한다. 먼저 전류가 없는 단일 실수 공간 궤도 영역의 von Weizsäcker 운동에너지 밀도는

$$
\tau_{\mathrm W}=\frac{|\nabla n|^2}{8n}
$$

이다. Spin 비편극 균일 전자기체의 기준은

$$
\tau_{\mathrm{unif}}=\frac3{10}(3\pi^2)^{2/3}n^{5/3}
$$

이다. 둘을 이용한 무차원 iso-orbital indicator는

$$
\alpha=\frac{\tau-\tau_{\mathrm W}}{\tau_{\mathrm{unif}}}
$$

로 정의한다. $\tau-\tau_{\mathrm W}$는 단일 궤도 기준을 넘는 운동에너지 밀도이며, $\tau_{\mathrm{unif}}$는 비교 척도이다. 위 식은 $n>0$인 영역에서 해석한다. 수치적으로 작은 밀도에서 분모와 미분의 거동이 중요하다는 점이 다음 절의 regularization으로 이어진다.[3,6,11]

| 국소 영역 | 대표 극한 | SCAN에서의 역할 |
| --- | --- | --- |
| 단일 공간 궤도 지배 | $\tau=\tau_{\mathrm W}$, $\alpha=0$ | 단일 궤도 한계의 에너지 형태 |
| 균일 비편극 전자기체 | $\nabla n=0$, $\tau=\tau_{\mathrm{unif}}$, $\alpha=1$ | 균일·천천히 변하는 밀도 한계 |
| 궤도 겹침이 다른 영역 | $\alpha>1$인 영역 포함 | 약한 결합 영역 등을 위한 보간·외삽 |

Iso-orbital indicator $\alpha$는 공간의 각 위치에서 전자 궤도가 얼마나 겹치는지 구별하는 데 사용한다. 실제 결정 내부에서는 여러 $\alpha$ 영역이 함께 나타나므로, 하나의 점에서 측정한 값보다는 공간에 따른 분포와 전체 전자구조를 함께 해석해야 한다. 예를 들어 $\alpha\approx1$은 균일 전자기체와 유사한 국소 환경을 나타내지만, 금속성 판정에는 band structure와 점유 상태에 대한 정보가 추가로 필요하다.[3,6,12]

### (3) SCAN의 설계 원리와 개선 물성

SCAN은 GGA에서 나타난 **분자의 결합 에너지와 고체의 격자 상수 사이의 정확도 절충**을 더 풍부한 궤도 환경 정보로 개선하기 위해 설계되었다. Spin 비편극계의 exchange를 나타내는 enhancement factor를 $F_{\mathrm x}(s,\alpha)$라고 쓰면, GGA에서는 하나의 $s$만으로 보정을 정하지만 SCAN에서는 $\alpha$에 따라 다른 교환 에너지 형태를 사용할 수 있다.[3,6,15,20]

$$
E_{\mathrm x}^{\mathrm{meta-GGA}}=
\int n(\mathbf r)\varepsilon_{\mathrm x}^{\mathrm{unif}}(n)
F_{\mathrm x}(s,\alpha)\,d\mathbf r.
$$

SCAN의 구성은 **단일 궤도 영역($\alpha\approx0$)과 천천히 변하는 밀도 영역($\alpha\approx1$)에서 적합한 에너지 형태를 각각 설계한 뒤, $\alpha$를 이용해 그 사이와 $\alpha>1$ 영역을 보간·외삽하는 방식**으로 이해할 수 있다. 보간 함수는 단순한 직선이 아니라 uniform limit, gradient expansion, scaling, exchange bound 등의 exact constraints를 보존하도록 만든다. 적절한 계의 정확한 에너지와 가까운 결과를 얻도록 희가스 원자, jellium 표면 등 appropriate norms도 활용한다. 실제 SCAN은 meta-GGA 수준에서 만족할 수 있는 17개 exact constraints를 반영했다.[6,13,15,20]

이 설계가 개선하려는 것은 특정 band 하나가 아니라 **서로 다른 결합 환경의 구조와 상대 에너지**이다. 예를 들어 covalent·ionic·metallic·hydrogen bond 및 중간 거리의 van der Waals 상호작용을 포함하는 분자와 고체에서, 기존 GGA에 비해 구조와 결합 에너지의 균형이 개선된 사례가 보고되었다. 약 1,000개 무기 화합물의 독립 benchmark에서는 강하게 결합한 화합물의 형성 에너지 평균 오차가 PBE에 비해 약 50% 감소했다. 반면 intermetallic 화합물에서는 PBE보다 오차가 커진 사례도 있었고, band gap의 개선 폭은 형성 에너지보다 제한적이었다.[3–6,20]

SCAN은 일부 전이금속 화합물의 구조·자기·상대 에너지를 개선할 수 있지만, **강한 전자 상관을 보편적으로 해결하는 방법은 아니다.** Mott 상태, 원자별 국소 moment와 금속의 자성 등은 해당 물질과 자기 상태를 구분하여 검증해야 한다. SCAN의 핵심 성과는 한 단계 높은 입력 정보를 사용하여 **여러 종류의 결합과 에너지 차이를 하나의 semilocal 범함수에서 더 균형 있게 기술한 것**이다.[3,6,15,20]

### (4) rSCAN과 r²SCAN: 수치적 안정성의 개선

SCAN의 $\alpha$ 보간 함수는 서로 다른 결합 환경을 연결하지만, 특정 구간에서 미분이 급격히 변해 XC potential과 적분 격자에 대한 민감도를 높일 수 있다. Regularized SCAN (rSCAN)은 iso-orbital indicator와 보간 함수를 regularization하여 이러한 수치 문제를 완화했다. 다만 이 변경으로 원래 SCAN이 만족하던 일부 exact constraints가 훼손되었다.[10,11,13]

Restored-regularized SCAN (r²SCAN)은 rSCAN의 안정성을 유지하면서 uniform electron gas limit, scaling, 이차 gradient expansion 등의 주요 조건을 다시 만족하도록 설계되었다. Exchange의 사차 gradient expansion까지 모두 복원하지는 않았지만, 수치적 매끄러움과 물성 정확도의 균형을 확보했다. 수천 개 고체를 대상으로 한 독립 benchmark에서는 SCAN보다 self-consistent 계산의 수렴이 안정적이고, 많은 재료에서 형성 에너지의 정확도도 개선되었다.[10,12,13]

| 범함수 | 해결하려는 문제 | 실제 개선·효과 | 검토할 한계 |
| --- | --- | --- | --- |
| SCAN | GGA의 결합 환경 구별 부족 | 다양한 결합의 구조·상대 에너지, 강한 결합 화합물의 형성 에너지 개선 | 수치 적분 민감도와 물성군별 오차 |
| rSCAN | SCAN의 급격한 보간·미분 변화 | 수치적 매끄러움과 계산 안정성 향상 | 일부 exact constraints 손실 |
| r²SCAN | rSCAN의 제약 손실 | 제약 복원, 더 안정적인 계산과 고체 형성 에너지 예측 개선 | 사차 exchange gradient expansion 미복원 |

SCAN 계열은 중간 거리의 약한 상호작용까지 일부 기술할 수 있지만, 멀리 떨어진 중성 부분계 사이의 정확한 장거리 dispersion에는 비국소 correlation 또는 별도의 분산 보정이 필요하다. 구조·에너지 예측의 성능과 계산의 수치 안정성, 장거리 상호작용의 정확도를 각각 구분하여 평가한다.[4–6,10,12]

## 5. Hybrid: Fock exchange와 band gap 개선

### (1) Hybrid 범함수의 개발 동기와 Fock exchange

LDA와 GGA는 많은 구조·결합 에너지를 효율적으로 계산하지만, 반도체·절연체의 KS 고윳값 gap을 실험적인 fundamental gap보다 작게 예측하는 경향이 있다. 국소·semilocal exchange 근사의 전하 delocalization 오차와 정확한 KS potential의 derivative discontinuity 문제는 이러한 차이를 이해하는 주요 요소이다. **Hybrid 범함수는 점유 궤도함수로 계산한 Fock exchange의 일부를 도입하여 exchange의 비국소성을 반영하고, 전하 분포와 band gap 예측을 개선하기 위해 개발되었다.**[8,14,17,18]

앞에서 정의한 $\phi_{i\sigma}$와 점유수 $f_{i\sigma}$에 대해 Fock exchange 에너지는 다음과 같다.

$$
E_{\mathrm x}^{\mathrm{Fock}}=-\frac12\sum_{\sigma,i,j}f_{i\sigma}f_{j\sigma}
\iint\frac{\phi_{i\sigma}^*(\mathbf r)\phi_{j\sigma}(\mathbf r)
\phi_{j\sigma}^*(\mathbf r')\phi_{i\sigma}(\mathbf r')}
{|\mathbf r-\mathbf r'|}\,d\mathbf r\,d\mathbf r'
$$

이다. 같은 spin을 가진 점유 궤도함수의 값이 서로 다른 두 위치 $\mathbf r,\mathbf r'$에서 적분으로 결합한다. 따라서 계산에는 공간의 각 위치에 있는 밀도·기울기·운동에너지 밀도만 사용하는 semilocal 범함수보다 많은 비국소 정보가 들어간다. Fock exchange는 주어진 궤도함수 집합에 대한 exchange를 정확하게 평가하지만, 다전자 correlation 에너지는 별도로 근사한다.[1,2,8]

혼합 비율을 $a$, semilocal 근사를 $\mathrm{sl}$로 표기한 단순 global hybrid의 예는

$$
E_{\mathrm{xc}}^{\mathrm{hyb}}=aE_{\mathrm x}^{\mathrm{Fock}}+(1-a)E_{\mathrm x}^{\mathrm{sl}}+E_{\mathrm c}^{\mathrm{sl}}
$$

이다. $a$는 Fock exchange가 exchange 전체에서 차지하는 비중을 정하며, global hybrid에서는 모든 전자 간 거리에 같은 비율을 적용한다. PBE0는 adiabatic connection에 기반한 설계 논리를 바탕으로 $a=1/4$을 선택하고, 나머지 exchange 및 correlation에는 PBE를 사용한다. 이렇게 구성한 에너지는 Hartree–Fock와 DFT의 **전체 에너지를 혼합하는 방식이 아니라 exchange 성분을 부분적으로 대체하는 방식**이다. Fock exchange를 더 많이 혼합하면 GKS gap이 변하지만, 가장 정확한 혼합률은 물질과 목표 물성에 따라 달라진다.[1,2,8,14]

### (2) Range-separated hybrid와 HSE

주기적 고체에서는 모든 거리의 Fock exchange를 계산하는 데 비용이 많이 든다. 특히 전극·금속처럼 장거리 screening이 중요한 계에서는 전자 간 거리에 따라 exchange를 다르게 취급할 필요가 있다. Range-separated hybrid는 전자 간 거리 $r_{12}=|\mathbf r-\mathbf r'|$에 따라 Coulomb kernel을 나누는 방식으로 이 문제에 대응한다. Error function $\operatorname{erf}$와 complementary error function $\operatorname{erfc}=1-\operatorname{erf}$를 쓰는 분리는

$$
\frac1{r_{12}}=\frac{\operatorname{erfc}(\omega r_{12})}{r_{12}}+\frac{\operatorname{erf}(\omega r_{12})}{r_{12}}
$$

이다. $\omega$는 길이의 역수 차원을 가진 range-separation parameter이며, 두 항은 각각 short range (SR)와 long range (LR)를 나타낸다. 이 kernel 분리 자체는 항등식이지만, 두 구간에서 어떤 exchange 근사를 선택할지는 모형의 선택이다.[2,8]

HSE 계열은 Fock exchange를 단거리 부분에만 혼합한다. 개념식은 다음과 같다.[2,8]

$$
E_{\mathrm{xc}}^{\mathrm{HSE}}=aE_{\mathrm x}^{\mathrm{Fock,SR}}(\omega)
+(1-a)E_{\mathrm x}^{\mathrm{PBE,SR}}(\omega)
+E_{\mathrm x}^{\mathrm{PBE,LR}}(\omega)+E_{\mathrm c}^{\mathrm{PBE}}.
$$

Heyd–Scuseria–Ernzerhof (HSE) 계열은 장거리 부분에 PBE exchange를 사용하고 Fock exchange는 단거리에서만 혼합하므로, 주기적 고체에서 비국소 exchange 계산의 부담을 줄이면서 여러 반도체의 band gap을 개선할 수 있다. 반면 long-range-corrected hybrid는 장거리 Fock exchange를 강조하여 장거리 전하 분포와 전하이동 특성을 다루도록 설계한다. 같은 range separation을 사용하더라도 두 방법이 비국소 exchange를 적용하는 거리 범위는 서로 다르다.[2,8,14]

| Hybrid 형태 | Fock exchange의 범위 | 선택에서 중요한 사항 |
| --- | --- | --- |
| Global hybrid | 모든 거리에서 일정 비율 | 혼합률과 주기계 계산 비용 |
| HSE형 screened hybrid | 단거리 부분 | 일반 반도체 gap과 넓은 gap 절연체의 차이 |
| Long-range-corrected hybrid | 장거리 비중을 강조 | 장거리 전하 분포·exchange의 요구 |

실제 semiconductor benchmark에서는 PBE0·HSE 등의 hybrid가 GGA보다 band gap과 valence-band width를 실험값에 가깝게 예측한 물질이 많았다. Covalent semiconductor의 gap에는 HSE가 유리한 사례가 있고, 이온성 절연체나 큰-gap 물질에서는 장거리 exchange를 강조한 LC hybrid가 더 잘 맞는 경우도 보고되었다. 따라서 hybrid의 주요 성과는 **많은 물질군에서 band gap 예측을 크게 개선한 것**이며, 범함수별 혼합률과 screening 길이를 선택할 때에는 연구 대상 물질군의 성능을 직접 비교해야 한다.[8,14]

### (3) Nonlocal exchange의 역할과 한계

Hybrid는 궤도함수 사이의 비국소 exchange 연산자를 사용하므로 generalized Kohn–Sham (GKS) 형식으로 흔히 계산한다. 실무적으로는 점유 궤도들의 쌍에 대한 Coulomb 적분과 그에 따른 연산자 작용이 추가되어, GGA의 국소 $F_{\mathrm x}(s)$ 평가보다 일반적으로 계산 비용이 크다. Fock exchange의 부분 혼합은 self-interaction과 delocalization 관련 오차를 완화할 수 있으며, 남아 있는 semilocal exchange와 correlation은 계속 근사로 취급한다. 단전자 자기반발 상쇄와 fractional electron number의 정확한 조건은 제6절에서 설명한다.[1,2,8,15]

Band gap을 비교할 때에는 hybrid가 계산한 GKS 고윳값 차이와 정확한 국소 KS 이론의 derivative discontinuity 관계를 구분한다. Hybrid의 GKS gap이 실험적인 fundamental gap에 가까워지는 것은 중요한 성능 개선이다. 다만 장거리 correlation과 정확한 derivative discontinuity는 별도의 이론적 성질이므로 각 근사가 이를 얼마나 기술하는지 추가로 검토해야 한다. 실제로 금속의 응집 에너지 등에서는 semilocal 근사가 더 우수한 사례도 있으므로, 구조·에너지·gap을 각각 별도의 지표로 평가한다.[1,2,4,8,14]

## 6. Exact constraints: 정확한 XC 범함수의 조건

Exact constraint는 물질별 계산값에 관계없이 정확한 XC 범함수가 만족해야 하는 수학적·물리적 조건이다. 일부는 모든 허용 밀도에 적용되고, 일부는 uniform electron gas나 단전자계처럼 정해진 극한에 적용된다. 범함수의 입력 정보가 많을수록 더 다양한 exact constraints를 함수 설계에 반영할 수 있다. 물성의 정확도는 제약의 충족 여부와 함께 해당 결합 환경에서 선택한 함수 형태 및 오차 검증 결과에 따라 평가한다. 이 절에서는 특정 SCAN 제약 목록과 독립적으로 주요 조건을 설명한다.[1,15]

| 조건 | 제한하는 대상 | 물리적 의미 |
| --- | --- | --- |
| Uniform electron gas limit | 일정한 밀도에서의 XC 에너지 | 균일계의 정확한 기준 회복 |
| Spin scaling·coordinate scaling | Exchange의 spin·공간척도 의존성 | 같은 spin의 교환과 Coulomb 길이척도 |
| One-electron limit | Hartree·exchange·correlation의 조합 | 단전자 자기반발의 제거 |
| XC hole sum rules | 조건부 전자 분포의 적분 | 기준 전자를 제외한 입자 수 보존 |
| Lieb–Oxford bound | 전체 XC 에너지의 하한 | 비물리적으로 큰 음의 에너지 제한 |
| Gradient expansion | 천천히 변하는 밀도에서의 에너지 | 균일계 주변 비균일성의 선도 보정 |
| Piecewise linearity·derivative discontinuity | 전자 수 변화에 따른 전체 에너지·potential | 전자 추가·제거 에너지의 일관성 |

### (1) Uniform electron gas limit

공간 전체에서 밀도가 일정한 $n_0$이고 spin이 비편극인 uniform electron gas에서는 XC 에너지가 균일계의 전자당 값으로 돌아가야 한다. 균일계의 thermodynamic limit에서 다음 관계를 사용한다.[1,15]

$$
\frac{E_{\mathrm{xc}}}{N}=\varepsilon_{\mathrm{xc}}^{\mathrm{unif}}(n_0).
$$

Uniform electron gas limit는 실제로 밀도가 공간 전체에 걸쳐 일정한 기준계에서 XC 에너지가 정확한 균일계 결과로 돌아가도록 요구한다. 유한 분자와 표면은 밀도와 경계가 달라지는 비균일계이므로, 각 위치의 국소 환경에 대한 추가 근사가 필요하다. LDA는 이 기준을 모든 점에 국소 적용하고, GGA와 meta-GGA는 추가 변수들이 균일계 값에 접근할 때 같은 기준으로 돌아가도록 설계할 수 있다. 실제 LDA의 correlation 매개화에는 기준 자료와 근사 오차가 있으므로, 정확한 균일계 한계라는 이론적 조건과 특정 수치 매개화의 정확도를 구별한다.[1,15]

제3절의 exchange enhancement factor로 쓰면 이 조건은 $F_{\mathrm x}(0)=1$이다. $\tau$ 기반 meta-GGA의 균일 비편극계에서는 $s=0$, $\alpha=1$이므로 같은 관례의 enhancement factor는 그 점에서 1이 되어야 한다. 균일계에서 살아남는 비정상적인 추가항은 LDA 기준 자체를 바꾸므로, gradient 보정이나 regularization을 설계할 때도 이 극한을 보존해야 한다.[9,10,15]

### (2) Exchange의 spin scaling과 coordinate scaling

Exchange의 spin dependence에는 정확한 **spin-scaling relation**이 있다. $E_{\mathrm x}^{\mathrm u}[n]$을 전체 밀도 $n$을 가진 spin 비편극계의 exchange 범함수라고 정의하면, collinear spin 밀도 $n_\uparrow,n_\downarrow$에 대해

$$
E_{\mathrm x}[n_\uparrow,n_\downarrow]
=\frac12\left(E_{\mathrm x}^{\mathrm u}[2n_\uparrow]
+E_{\mathrm x}^{\mathrm u}[2n_\downarrow]\right)
$$

이다. 같은 spin의 궤도 사이에서만 Fock exchange가 생긴다는 성질을 반영한다. 우변의 밀도를 두 배로 하고 에너지를 절반씩 더하는 규약이 중요하다. Exchange의 spin scaling을 적용할 때에는 각 spin 밀도를 두 배로 변환한 후 두 결과를 절반씩 더해야 한다. Correlation의 spin dependence는 별도의 관계로 구성하므로 exchange에 사용한 변환식을 그대로 적용할 수 없다.[1,15]

**Uniform coordinate scaling**은 공간 길이척도를 바꾸되 전자 수를 유지하는 변환이다. 양의 무차원 매개변수 $\gamma$에 대해

$$
n_\gamma(\mathbf r)=\gamma^3 n(\gamma\mathbf r),
\qquad \int n_\gamma(\mathbf r)\,d\mathbf r=N
$$

으로 정의한다. $\gamma>1$이면 밀도 분포가 원점 쪽으로 압축되고 $\gamma<1$이면 퍼진다. 이는 고정된 공간점에서 밀도만 일정 배수로 바꾸는 particle-number 변화와 다르다. 좌표변환의 Jacobian이 $\gamma^{-3}$이므로 앞의 $\gamma^3$이 입자 수를 보존한다.[1,15]

정확한 exchange는 이 변환에 대해

$$
E_{\mathrm x}[n_\gamma]=\gamma E_{\mathrm x}[n]
$$

을 만족한다. 정규화된 궤도는 $\phi_{i\sigma,\gamma}(\mathbf r)=\gamma^{3/2}\phi_{i\sigma}(\gamma\mathbf r)$로 변하고, 이를 Fock 적분에 넣으면 Coulomb kernel에서 남는 길이척도가 $\gamma$를 만든다. 이 관계는 Coulomb 상호작용이 공간 좌표의 크기 변화에 따라 어떻게 변하는지로부터 정확히 유도된다. Correlation에는 전자 간 상호작용과 운동에너지의 변화가 함께 반영되므로 exchange와 다른 coordinate-scaling 관계가 적용된다.[1,15]

궤도 기울기의 정의에서 직접 얻는 운동에너지 scaling은 다음과 같다.[2,15]

$$
\tau_\gamma(\mathbf r)=\gamma^5\tau(\gamma\mathbf r),
\qquad T_s[n_\gamma]=\gamma^2 T_s[n].
$$

$\tau_{\mathrm W}$와 $\tau_{\mathrm{unif}}$도 같은 $\gamma^5$ 인자로 변하므로 $s$와 $\alpha$는 변환된 위치에서 같은 무차원 값을 갖는다. 이 때문에 $n\varepsilon_{\mathrm x}^{\mathrm{unif}}$에 $s,\alpha$의 무차원 함수를 곱하는 설계가 exchange scaling과 자연스럽게 양립한다. 단위가 맞는다는 것만으로 충분하지는 않으며, regularization이 고정된 별도 척도를 도입하는지도 따져야 한다.[10,15]

### (3) One-electron limit과 self-interaction

정규화가 $\int n_1\,d\mathbf r=1$인 순수 단전자 상태에는 전자 쌍이 없다. 그럼에도 고전적 Hartree 항은 $E_{\mathrm H}[n_1]>0$을 주므로 정확한 exchange가 이를 모두 상쇄해야 한다.[1,15]

$$
E_{\mathrm x}[n_1]=-E_{\mathrm H}[n_1].
$$

같은 단전자계에서는 실제 운동에너지와 비상호작용 운동에너지가 같고 전자 간 correlation도 없으므로

$$
E_{\mathrm c}[n_1]=0
$$

이다. 두 식을 함께 적용해야 $E_{\mathrm H}+E_{\mathrm{xc}}=0$이 된다. 단전자계에서 정확한 XC 에너지를 얻으려면 $E_{\mathrm c}=0$인 조건과 $E_{\mathrm x}=-E_{\mathrm H}$인 조건을 동시에 만족해야 한다. 이 두 조건은 순수한 단전자 spin 상태에 대한 것으로, fractional-spin ensemble에서는 별도의 exchange·correlation 관계를 검토해야 한다.[1,15]

$\tau$를 사용하는 meta-GGA는 iso-orbital 정보를 활용하여 단전자 correlation이 사라지는 조건을 구현할 수 있다. 그러나 임의의 단전자 밀도에서 nonlocal Hartree 에너지를 정확히 상쇄하려면 exchange의 공간적 비국소성까지 고려해야 한다. Global hybrid도 Fock exchange를 부분적으로만 혼합하면 남은 semilocal 성분의 오차를 가질 수 있다. 특정 기준계에서의 에너지 일치와 모든 허용 단전자 밀도에 대한 항등식을 구별해야 한다.[1,15]

### (4) XC hole과 sum rules

XC hole은 한 전자가 $\mathbf r$에 있을 때 다른 전자의 조건부 분포가 전체 평균 밀도 $n(\mathbf r')$와 얼마나 다른지 나타낸다. 물리적 상호작용 세기를 $\lambda=1$로 표시한다. 정수 $N$의 고정 입자 수 상태에서 순서가 있는 spin 합산 pair density를 $P(\mathbf r,\mathbf r')$라 하고, $n(\mathbf r)>0$인 위치에서 다음과 같이 정의한다.[1,15]

$$
n_{\mathrm{cond}}(\mathbf r'|\mathbf r)
=\frac{P(\mathbf r,\mathbf r')}{n(\mathbf r)}
=n(\mathbf r')+n_{\mathrm{xc}}^{\lambda=1}(\mathbf r,\mathbf r').
$$

$n_{\mathrm{cond}}$는 부피당 전자 수이며, 조건으로 이미 지정한 전자 하나를 제외한 $N-1$개 전자를 포함한다. 따라서 $P$의 두 좌표 적분은 $N(N-1)$이고, hole의 적분은 다음과 같다.[1,15]

$$
\int n_{\mathrm{xc}}^{\lambda=1}(\mathbf r,\mathbf r')\,d\mathbf r'=-1.
$$

음의 적분은 전자 하나가 다른 곳으로 사라진다는 뜻이 아니라, 기준 전자를 제외한 조건부 분포와 $N$개 전자의 평균 밀도를 비교한 결과이다. Hole은 단순히 밀도가 부족한 공간 영역의 크기가 아니며, correlation 부분은 부호가 다른 영역을 함께 가질 수 있다.[1,15]

전체 $E_{\mathrm{xc}}$를 hole의 Coulomb 에너지로 표현하려면 물리적 상호작용 세기 $\lambda=1$의 hole만으로는 충분하지 않다. 전자–전자 상호작용을 $\lambda/|\mathbf r-\mathbf r'|$로 바꾸고, 각 $\lambda$에서 외부 potential을 조정하여 같은 밀도 $n$을 유지하는 adiabatic connection을 사용한다. Coupling-constant 평균을

$$
\bar n_{\mathrm{xc}}(\mathbf r,\mathbf r')
=\int_0^1 n_{\mathrm{xc}}^\lambda(\mathbf r,\mathbf r')\,d\lambda
$$

로 정의하면 정확한 관계는

$$
E_{\mathrm{xc}}[n]
=\frac12\iint\frac{n(\mathbf r)\bar n_{\mathrm{xc}}(\mathbf r,\mathbf r')}{|\mathbf r-\mathbf r'|}\,d\mathbf r\,d\mathbf r'
$$

이다. $\lambda=1$의 hole로 계산하면 상호작용 에너지의 Hartree 초과분을 얻지만, 위 평균은 운동에너지 correlation까지 포함한 전체 XC 에너지를 준다. 같은 밀도와 입자 수를 유지하므로 각 $\lambda$의 정규화와 그 평균의 정규화는 모두 $-1$이다.[1,15]

정수 점유 KS determinant의 exchange hole을 $n_{\mathrm x}$, 평균 correlation hole을 $\bar n_{\mathrm c}=\bar n_{\mathrm{xc}}-n_{\mathrm x}$로 나누면

$$
\int n_{\mathrm x}(\mathbf r,\mathbf r')\,d\mathbf r'=-1,
\qquad \int\bar n_{\mathrm c}(\mathbf r,\mathbf r')\,d\mathbf r'=0
$$

이다. Exchange가 이미 전자 하나의 결손을 정하므로 correlation은 전체 결손량을 더하는 대신 그 공간 분포를 바꾼다. Hole의 적분값이 같은 경우에도 XC 에너지는 달라질 수 있다. 에너지 적분에는 거리 가중치 $1/|\mathbf r-\mathbf r'|$가 들어가므로, 정확한 에너지를 얻으려면 적분값뿐 아니라 hole이 공간적으로 어떻게 분포하는지도 기술해야 한다.[1,15]

### (5) Lieb–Oxford bound

3차원 비상대론적 Coulomb 전자계의 XC 에너지는 밀도로 정해지는 보편적인 하한을 갖는다. Hartree 원자단위계에서 **Lieb–Oxford bound**의 한 유효한 형태는

$$
E_{\mathrm{xc}}[n]\ge -C_{\mathrm{LO}}\int n(\mathbf r)^{4/3}\,d\mathbf r,
\qquad C_{\mathrm{LO}}=1.68
$$

이다. 여기서 $C_{\mathrm{LO}}=1.68$은 널리 사용되는 전통적인 보편 상수 중 하나이다. 가능한 가장 작은 최적 상수를 구하는 문제는 이 부등식의 일반적인 적용과 별도로 다룬다. 이 부등식은 XC 에너지가 제한 없이 음의 방향으로 낮아지는 것을 막는다. Spin 분극 여부와 관계없이 우변에는 전체 밀도 $n$을 넣으며, 조건은 국소 값이 아니라 공간 적분에 적용된다.[1,15]

이 조건의 출발점은 간접 Coulomb 에너지 $W-E_{\mathrm H}$의 하한이다. $T-T_s\ge0$인 KS 분해에서 $E_{\mathrm{xc}}=(T-T_s)+(W-E_{\mathrm H})$이므로 같은 하한이 XC에도 적용된다. 따라서 이 하한은 Coulomb 상호작용을 가진 전자계의 XC 에너지 전체에 적용되는 보편적인 조건이다.[1,15]

범함수 설계에서는 enhancement factor에 점별 상한을 두어 적분 bound를 만족시키기도 한다. 점별 상한은 공간 전체에서 성립하는 적분 부등식을 보장하기 위해 추가하는 **더 강한 충분조건**이다. 따라서 일부 위치에서 점별 조건을 만족하지 않는 함수도 전체 XC 에너지의 Lieb–Oxford bound는 만족할 수 있다. PBE처럼 점별 제한을 선택한 경우에는 그 선택이 범함수 설계에 추가된 조건임을 구분하여 해석한다.[15,16]

### (6) Slowly varying density와 gradient expansion

Uniform electron gas limit는 기울기가 정확히 0인 기준이다. **Gradient expansion**은 그 주변에서 밀도가 충분히 천천히 변할 때의 선도 보정을 제한한다. Spin 비편극 exchange의 공간 적분을 부분적분으로 정리하는 통상적인 표현에서 이차까지의 관계는 다음과 같다.[9,15]

$$
E_{\mathrm x}^{\mathrm{GE2}}[n]
=\int n\varepsilon_{\mathrm x}^{\mathrm{unif}}(n)
\left[1+\frac{10}{81}s^2\right]d\mathbf r.
$$

$\mathrm{GE2}$는 second-order gradient expansion을 뜻한다. $10/81$은 천천히 변하는 밀도에서 정확한 이차 exchange 계수이다. 이 식은 그 주변에서 낮은 차수까지만 남긴 점근 전개이므로, 적용할 밀도는 기울기와 고차 공간 변화가 모두 충분히 작아야 한다. 경계항을 제거하는 부분적분의 조건을 가정하고, 급격한 표면·꼬리 영역으로 전개의 적용 범위를 무제한 넓히지 않는다.[9,15]

밀도 변화의 추가 척도로 reduced Laplacian $q$를 정의하면

$$
q=\frac{\nabla^2n}{4k_F^2n}
$$

이다. $q$는 무차원이며, slowly varying limit에서는 $s\ll1$과 $|q|\ll1$을 함께 고려한다. 단지 한 점에서 $\nabla n=0$이라는 사실만으로 주변 밀도가 천천히 변한다고 결론 내릴 수는 없다. 예를 들어 밀도의 극값에서는 기울기가 0이어도 곡률은 클 수 있다. 이는 전개에 필요한 공간 조건을 구별하기 위한 해석이다.[9,15]

PBEsol은 exchange의 이차 계수를 회복하도록 설계되었다. 반면 PBE가 선택한 계수에는 다른 조건과 원자 에너지 기술 사이의 절충이 반영되어 있다. GGA는 이차 gradient expansion에 더해 큰 기울기 영역의 함수 형태와 다른 exact constraints를 함께 고려하여 설계한다. PBEsol이 작은 기울기의 정확한 계수를 회복하더라도, 분자와 고체의 모든 에너지 차이는 각각의 조건에서 검증해야 한다.[1,7,9]

### (7) Piecewise linearity와 derivative discontinuity

전자 수에 관한 exact constraint는 공간 기울기에 관한 조건과 성격이 다르다. 핵 위치와 외부 potential을 고정하고 영온에서 인접한 정수 전자 수의 바닥상태를 혼합하는 ensemble을 생각한다. 정수 $M$과 $0\le\delta\le1$에 대해 평균 전자 수가 $M+\delta$이면, 안정한 인접 정수 상태를 잇는 정확한 전체 에너지는

$$
E_0(M+\delta)=(1-\delta)E_0(M)+\delta E_0(M+1)
$$

이다. 이것이 **piecewise linearity**이다. Piecewise linearity는 **전체 바닥상태 에너지 $E_0$**가 인접한 정수 전자 수 사이에서 선형으로 연결된다는 조건이다. 여기서 fractional electron number는 정수 전자 수가 서로 다른 상태들을 혼합한 ensemble의 평균 전자 수를 의미한다. 따라서 $E_{\mathrm{xc}}$ 자체에 같은 선형성을 독립적으로 부과하는 조건과 구별한다.[17,18]

전자 수 $N$의 유한계에서 인접한 $N-1,N,N+1$ 상태가 정의되어 있을 때 ionization energy $I$와 electron affinity $A$를

$$
I=E_0(N-1)-E_0(N),\qquad A=E_0(N)-E_0(N+1)
$$

로 정의한다. Piecewise linearity에서 정수 양옆의 chemical potential은 각각

$$
\mu^-=-I,\qquad \mu^+=-A
$$

가 된다. 두 기울기의 차이 $I-A$는 fundamental gap이다. 이 관계는 핵 위치를 고정한 상태에서 전자를 추가하거나 제거할 때의 에너지를 나타낸다. 구조 이완을 포함하는 adiabatic ionization energy와 중성 들뜸의 optical gap은 별도의 물리량으로 정의한다.[1,17,18]

정확한 multiplicative KS potential에서는 전자 수가 정수를 통과할 때 XC potential의 극한이 공간적으로 일정한 양만큼 달라질 수 있다. 동일한 potential 기준에서 그 차이를 **derivative discontinuity** $\Delta_{\mathrm{xc}}$로 정의하면

$$
v_{\mathrm{xc}}^+(\mathbf r)-v_{\mathrm{xc}}^-(\mathbf r)=\Delta_{\mathrm{xc}}
$$

이다. $v_{\mathrm{xc}}^\pm$는 전자 수가 정수의 위·아래에서 접근할 때의 함수 미분 $\delta E_{\mathrm{xc}}/\delta n$의 극한이다. 이 불연속은 전자 수가 정수값을 가로지를 때 XC potential에 추가되는 공간적으로 일정한 이동량이다. 특정 전자 수에서 potential이 공간적으로 급격하게 변하는 현상과 구별해야 한다.[1,18]

정확한 국소 KS의 가장 높은 점유 및 가장 낮은 비점유 고윳값을 각각 $\varepsilon_{\mathrm H}$와 $\varepsilon_{\mathrm L}$로 쓰면

$$
E_g=I-A=(\varepsilon_{\mathrm L}-\varepsilon_{\mathrm H})+\Delta_{\mathrm{xc}}
$$

이다. 따라서 정확한 KS 계산에서도 고윳값 차이와 fundamental gap은 일반적으로 같지 않다. 이 식은 정확한 국소 KS potential을 사용하는 경우에 성립하는 분해이다. Nonlocal exchange를 포함하는 GKS에서는 고윳값 문제가 다르므로 해당 형식의 gap과 residual discontinuity를 그 이론에 맞게 정의해야 한다.[1,17]

통상적인 근사 범함수의 유한계 $E_0(N+\delta)$가 정수점을 잇는 직선보다 아래로 휘면, 전하를 여러 조각으로 나눈 상태를 지나치게 낮은 에너지로 평가하여 delocalization을 선호할 수 있다. 반대 곡률은 localization을 지나치게 선호할 수 있다. 전하의 localization·delocalization 오차는 fractional electron number에서의 에너지 곡률로 직접 평가한다. 단전자 자기상호작용 상쇄 여부와 hybrid의 Fock exchange 혼합률은 관련된 특성이지만, piecewise linearity의 정확도에는 별도의 점검이 필요하다.[17,18]

## 7. 요약

- LDA는 uniform electron gas의 XC 에너지를 실제 밀도에 국소적으로 적용한다. GGA의 PBE는 비균일 밀도의 원자·분자 결합 에너지 기술을 개선했고, PBEsol은 조밀한 고체의 격자 상수와 표면 에너지를 개선하도록 설계되었다.[1,7,9,19]
- GGA의 exchange enhancement factor $F_{\mathrm x}(s)$는 균일계 극한, 작은 기울기의 계수와 큰 기울기의 상한을 만족하도록 설계한다. PBE와 PBEsol은 같은 함수 형태에서도 $\mu,\beta$의 선택에 따라 다른 물성에 강점을 보인다.[9,15,19]
- Meta-GGA는 $\tau$와 $\alpha$로 결합 환경을 구분한다. SCAN은 다양한 결합의 구조·형성 에너지를 개선했고, rSCAN과 r²SCAN은 수치적 안정성 및 exact constraints의 균형을 개선하도록 발전했다.[3,6,10–13,20]
- Hybrid는 nonlocal Fock exchange를 혼합하여 많은 반도체의 band gap을 개선한다. Global·screened·long-range-corrected 형태는 Fock exchange가 작용하는 거리와 계산 비용이 다르며, correlation은 별도로 근사한다.[1,2,8,14]
- Uniform electron gas limit, exchange scaling, 단전자 상쇄와 XC hole sum rules는 서로 다른 물리적 요구이다. Lieb–Oxford bound는 적분 에너지의 하한이며 gradient expansion은 천천히 변하는 밀도의 극한이다.[1,9,15]
- Piecewise linearity는 fractional electron number에 대한 전체 에너지의 조건이다. 정확한 국소 KS gap에는 derivative discontinuity가 더해지며, 이 조건을 semilocal 또는 hybrid의 계열명만으로 보장할 수 없다.[1,17,18]

## 8. 참고문헌

1. K. Capelle, “A Bird's-Eye View of Density-Functional Theory,” *Brazilian Journal of Physics* **36**, 1318–1343 (2006). [DOI: 10.1590/S0103-97332006000700035](https://doi.org/10.1590/S0103-97332006000700035), [Author manuscript](https://arxiv.org/abs/cond-mat/0211443). §§4–5의 에너지 분해, 국소·semilocal·궤도 의존 범함수와 한계를 참조한다.
2. S. Lehtola, F. Blockhuys, and C. Van Alsenoy, “An Overview of Self-Consistent Field Calculations Within Finite Basis Sets,” *Molecules* **25**, 1218 (2020). [DOI: 10.3390/molecules25051218](https://doi.org/10.3390/molecules25051218), [Author manuscript](https://arxiv.org/abs/1912.12029). §§III, XI의 에너지, $\tau$, range separation과 nonlocal correlation을 참조한다.
3. E. B. Isaacs and C. Wolverton, “Performance of the strongly constrained and appropriately normed density functional for solid-state materials,” *Physical Review Materials* **2**, 063801 (2018). [DOI: 10.1103/PhysRevMaterials.2.063801](https://doi.org/10.1103/PhysRevMaterials.2.063801), [Author manuscript](https://arxiv.org/abs/1804.06914). Introduction의 Eq. (3), 형성에너지 및 구조·자성·gap 시험을 참조한다.
4. G.-X. Zhang, A. M. Reilly, A. Tkatchenko, and M. Scheffler, “Performance of various density-functional approximations for cohesive properties of 64 bulk solids,” *New Journal of Physics* **20**, 063020 (2018). [DOI: 10.1088/1367-2630/aac7f0](https://doi.org/10.1088/1367-2630/aac7f0), [Repository full text](https://orbilu.uni.lu/bitstream/10993/38240/1/125-solids-DFT-NJP-2018.pdf). §§2–4의 물질군별 격자·응집·압축성 및 dispersion 비교를 참조한다.
5. J. G. Brandenburg, J. E. Bates, A. Ruzsinszky, J. Sun, and J. P. Perdew, “Benchmark tests of a strongly constrained semilocal functional with a long-range dispersion correction,” *Physical Review B* **94**, 115144 (2016). [DOI: 10.1103/PhysRevB.94.115144](https://doi.org/10.1103/PhysRevB.94.115144), [Author manuscript](https://arxiv.org/abs/1605.06971). §§I–III의 중간 거리와 장거리 구분, 분자·결정의 dispersion 보정 시험을 참조한다.
6. J. Sun, A. Ruzsinszky, and J. P. Perdew, “Strongly Constrained and Appropriately Normed Semilocal Density Functional,” *Physical Review Letters* **115**, 036402 (2015). [DOI: 10.1103/PhysRevLett.115.036402](https://doi.org/10.1103/PhysRevLett.115.036402), [Author manuscript](https://arxiv.org/abs/1504.03028). Eqs. (1)–(4), 제약·기준계와 Supplementary Material을 참조한다.
7. G. I. Csonka, J. P. Perdew, A. Ruzsinszky, P. H. T. Philipsen, S. Lebègue, J. Paier, O. A. Vydrov, and J. G. Ángyán, “Assessing the performance of recent density functionals for bulk solids,” *Physical Review B* **79**, 155107 (2009). [DOI: 10.1103/PhysRevB.79.155107](https://doi.org/10.1103/PhysRevB.79.155107), [Author manuscript](https://arxiv.org/abs/0903.4037). 격자·응집·bulk modulus와 영점·온도 보정 비교를 참조한다.
8. Y.-i. Matsushita, K. Nakamura, and A. Oshiyama, “Comparative study of hybrid functionals applied to structural and electronic properties of semiconductors and insulators,” *Physical Review B* **84**, 075205 (2011). [DOI: 10.1103/PhysRevB.84.075205](https://doi.org/10.1103/PhysRevB.84.075205), [Author manuscript](https://arxiv.org/abs/1104.2769). §II의 PBE0·HSE·LC 정의와 §IV의 물질별 비교를 참조한다.
9. J. P. Perdew et al., “Restoring the Density-Gradient Expansion for Exchange in Solids and Surfaces,” *Physical Review Letters* **100**, 136406 (2008). [DOI: 10.1103/PhysRevLett.100.136406](https://doi.org/10.1103/PhysRevLett.100.136406), [Author manuscript](https://arxiv.org/abs/0707.2088). Eqs. (1)–(2)와 Tables I–II의 PBEsol 설계·격자·원자화 에너지를 참조한다.
10. J. W. Furness, A. D. Kaplan, J. Ning, J. P. Perdew, and J. Sun, “Accurate and Numerically Efficient r²SCAN Meta-Generalized Gradient Approximation,” *The Journal of Physical Chemistry Letters* **11**, 8208–8215 (2020). [DOI: 10.1021/acs.jpclett.0c02405](https://doi.org/10.1021/acs.jpclett.0c02405), [Author manuscript](https://arxiv.org/abs/2008.03374). Eq. (6), Tables 1–2, Figs. 1–3의 제약·안정성·물성 시험을 참조한다.
11. A. P. Bartók and J. R. Yates, “Regularized SCAN functional,” *The Journal of Chemical Physics* **150**, 161101 (2019). [DOI: 10.1063/1.5094646](https://doi.org/10.1063/1.5094646), [Author manuscript](https://arxiv.org/abs/1903.01007). §II의 지표·보간 regularization, §III의 수치 시험을 참조한다.
12. R. Kingsbury, A. S. Gupta, C. J. Bartel, J. M. Munro, S. Dwaraknath, M. Horton, and K. A. Persson, “Performance comparison of r²SCAN and SCAN metaGGA density functionals for solid materials via an automated, high-throughput computational workflow,” *Physical Review Materials* **6**, 013801 (2022). [DOI: 10.1103/PhysRevMaterials.6.013801](https://doi.org/10.1103/PhysRevMaterials.6.013801), [Author-hosted full text](https://perssongroup.lbl.gov/papers/kingsbury_performance_comparison_2021.pdf). §§II–III와 Figs. 3–4의 물성별 오차·workflow 신뢰성을 참조한다.
13. J. W. Furness, A. D. Kaplan, J. Ning, J. P. Perdew, and J. Sun, “Construction of meta-GGA functionals through restoration of exact constraint adherence to regularized SCAN functionals,” *The Journal of Chemical Physics* **156**, 034109 (2022). [DOI: 10.1063/5.0073623](https://doi.org/10.1063/5.0073623), [Author manuscript](https://arxiv.org/abs/2110.00647). §§II–III의 regularization·gradient expansion과 제약 복원 범위를 참조한다.
14. A. J. Garza and G. E. Scuseria, “Predicting Band Gaps with Hybrid Density Functionals,” *The Journal of Physical Chemistry Letters* **7**, 4165–4170 (2016). [DOI: 10.1021/acs.jpclett.6b01807](https://doi.org/10.1021/acs.jpclett.6b01807), [Author manuscript](https://arxiv.org/abs/1608.04796). Statistical Evaluation과 discussion의 독립 gap benchmark·비용 비교를 참조한다.
15. A. D. Kaplan, M. Levy, and J. P. Perdew, “The Predictive Power of Exact Constraints and Appropriate Norms in Density Functional Theory,” *Annual Review of Physical Chemistry* **74**, 193–218 (2023). [DOI: 10.1146/annurev-physchem-062422-013259](https://doi.org/10.1146/annurev-physchem-062422-013259), [Author manuscript](https://arxiv.org/abs/2207.03855). §III의 hole, exchange, correlation 및 nonlocal 조건을 참조한다.
16. J. G. Vilhena, E. Räsänen, L. Lehtovaara, and M. A. L. Marques, “On the violation of a local form of the Lieb-Oxford bound,” *Physical Review A* **85**, 052514 (2012). [DOI: 10.1103/PhysRevA.85.052514](https://doi.org/10.1103/PhysRevA.85.052514), [Author manuscript](https://arxiv.org/abs/1204.6332). §II A–B, Eqs. (1)–(8)의 global bound와 더 강한 local 조건의 구분을 참조한다.
17. P. Mori-Sánchez, A. J. Cohen, and W. Yang, “Localization and Delocalization Errors in Density Functional Theory and Implications for Band-Gap Prediction,” *Physical Review Letters* **100**, 146401 (2008). [DOI: 10.1103/PhysRevLett.100.146401](https://doi.org/10.1103/PhysRevLett.100.146401), [Author manuscript](https://arxiv.org/abs/0708.3688). Eqs. (1)–(10), Fig. 1의 전체 에너지 선형성·gap·전하 분포 분석을 참조한다.
18. E. Kraisler and L. Kronik, “Piecewise Linearity of Approximate Density Functionals Revisited: Implications for Frontier Orbital Energies,” *Physical Review Letters* **110**, 126403 (2013). [DOI: 10.1103/PhysRevLett.110.126403](https://doi.org/10.1103/PhysRevLett.110.126403), [Author manuscript](https://arxiv.org/abs/1211.5950). Eqs. (1)–(6)의 ensemble 구성과 derivative discontinuity 논의를 참조한다.
19. J. P. Perdew, K. Burke, and M. Ernzerhof, “Generalized Gradient Approximation Made Simple,” *Physical Review Letters* **77**, 3865–3868 (1996). [DOI: 10.1103/PhysRevLett.77.3865](https://doi.org/10.1103/PhysRevLett.77.3865). Exchange enhancement factor의 함수 형태, uniform-gas linear response, 매개변수 선택과 PBE의 원래 개발 동기를 참조한다.
20. J. Sun, R. C. Remsing, Y. Zhang, et al., “Accurate first-principles structures and energies of diversely bonded systems from an efficient density functional,” *Nature Chemistry* **8**, 831–836 (2016). [DOI: 10.1038/nchem.2535](https://doi.org/10.1038/nchem.2535). SCAN의 다양한 결합 환경, 구조·결합 에너지 및 중간 거리 상호작용에 대한 성능을 참조한다.
