---
description: LDA·GGA·meta-GGA·hybrid의 입력 정보와 근사 방식을 비교하고 XC 범함수가 따라야 하는 주요 exact constraints를 설명한다.
---

# Exchange–correlation functionals

Exchange–correlation (XC) 범함수의 선택은 같은 원자 구조에서 얻는 결합 에너지, 평형 부피와 전자구조를 바꾼다. **Jacob’s ladder는 범함수가 사용하는 정보를 단계적으로 늘리는 분류이며, 모든 물성의 정확도가 반드시 높아지는 순위표는 아니다.** 국소 밀도를 사용하는 local density approximation (LDA), 밀도 기울기를 추가하는 generalized gradient approximation (GGA), 궤도함수의 운동에너지 밀도 등을 활용하는 meta-GGA, nonlocal Fock exchange를 혼합하는 hybrid 범함수를 차례로 다룬다. 각 단계에서 어떤 전자 환경과 상호작용을 추가로 기술할 수 있는지 구분하는 것이 중요하다.[1–4]

[Density functional theory](density-functional-theory.md) (DFT)의 Kohn–Sham (KS) 구성과 자기일관 계산을 선행 지식으로 삼는다. 여기서는 원자핵의 위치를 고정한 비상대론적 바닥상태를 기준으로 주요 식과 물성 비교를 설명하며, 범함수의 상세한 유도와 구현 방법은 다루지 않는다. Hartree 원자단위계 $\hbar=m_e=e=4\pi\varepsilon_0=1$을 사용하고, 궤도 자기장과 전류가 없는 경우를 다룬다. $m_e$는 전자 질량, $e$는 기본 전하의 양의 크기, $\varepsilon_0$는 진공 유전율이다. 자성 물성을 다룰 때에는 spin 채널을 분리한다. 다만 아래의 LDA·GGA 대표식과 SCAN 지표는 별도 언급이 없으면 spin 비편극 상태의 전체 전자 밀도로 표현한다.[1,2]

## 1. XC 에너지와 범함수의 분류

### (1) 근사가 들어가는 위치

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

따라서 XC 에너지는 고전적인 Hartree 반발 항에 포함되지 않은 전자 간 상호작용의 기여와, 실제 상호작용계 및 KS 보조계 사이의 운동에너지 차이를 함께 포함한다. 아래에서 근사하는 것은 이 나머지 에너지의 범함수이다. 밀도와 궤도함수는 선택한 근사에 맞춰 다시 자기일관적으로 결정되므로, 서로 다른 범함수의 결과 차이는 같은 밀도에서 평가한 XC 에너지 차이만을 뜻하지 않는다.[1,2]

### (2) 입력 정보의 단계

대표 범함수로 Perdew–Burke–Ernzerhof (PBE), strongly constrained and appropriately normed (SCAN), Heyd–Scuseria–Ernzerhof (HSE)를 비교한다. SCAN의 변형인 regularized SCAN (rSCAN)과 regularized-restored SCAN (r²SCAN)은 meta-GGA 절에서 함께 설명한다. 표에 제시한 대표 범함수들은 같은 단계에 속하더라도 서로 다른 물성과 exact constraints를 설계 목표로 삼을 수 있음을 보여 준다. 여기서 semilocal이란 공간의 한 점에서 밀도·기울기·운동에너지 밀도를 평가하여 적분한다는 뜻이다. 특히 $\tau$를 쓰는 meta-GGA는 궤도함수에 의존하므로 밀도만의 명시적 국소 함수와는 다르다.[2,3]

| 단계 | 추가하는 정보 | 대표 범함수 | 새로 구별하는 대상 |
| --- | --- | --- | --- |
| 1: LDA | 국소 밀도 $n$ | 균일 전자기체 기반 LDA | 밀도가 다른 영역 |
| 2: GGA | 밀도 기울기 $\nabla n$ | PBE, PBEsol | 밀도 비균일성 |
| 3: meta-GGA | $\tau$, 또는 $\nabla^2n$ | SCAN, rSCAN, r²SCAN | 같은 밀도·기울기에서도 다른 궤도 환경 |
| 4: hybrid | 점유 궤도 사이의 Fock exchange | PBE0, HSE | 공간적으로 떨어진 점 사이의 exchange |
| 5: 비점유 상태를 활용하는 근사 | 비점유 궤도·응답 정보 등 | Double hybrid, random phase approximation (RPA) 계열 | semilocal 모형을 넘는 correlation |

다섯째 단계의 RPA와 double hybrid는 여기서 위치만 짚는다. 이 단계는 비점유 상태까지 이용하는 correlation 모형으로 확장하며, hybrid에 exchange 비율만 더 높인 것을 뜻하지 않는다. 또한 경험적 매개변수의 수와 사다리의 높이는 별개의 분류이다. 같은 GGA나 meta-GGA 안에도 exact constraints를 우선하는 설계와 기준 자료에 맞추는 설계가 존재한다.[1–3,5]

## 2. LDA: 균일 전자기체의 국소 적용

### (1) 국소 근사의 의미

LDA는 실제 밀도의 각 점을 **그 점과 같은 밀도를 가진 균일 전자기체**에 대응시킨다. 균일계의 전자당 XC 에너지를 $\varepsilon_{\mathrm{xc}}^{\mathrm{unif}}$라 하면

$$
E_{\mathrm{xc}}^{\mathrm{LDA}}[n]=\int n(\mathbf r)\varepsilon_{\mathrm{xc}}^{\mathrm{unif}}(n(\mathbf r))\,d\mathbf r
$$

이다. 실제 결정이나 분자의 밀도 자체를 균일하게 만드는 근사가 아니다. KS 방정식은 여전히 비균일한 핵 potential 안에서 풀며, 국소적인 에너지 평가 규칙에 균일계의 정보를 사용하는 것이다.[1,2,6]

Spin 비편극 균일 전자기체의 exchange 에너지는 전자당

$$
\varepsilon_{\mathrm x}^{\mathrm{unif}}(n)=-\frac34\left(\frac3\pi\right)^{1/3}n^{1/3}
$$

이다. 음의 부호는 exchange가 Hartree 기준 에너지를 낮춘다는 뜻이다. 이 식은 균일계 exchange에 대해서는 정확하지만, 실제 비균일계에 국소적으로 대입한 결과는 근사이다. Correlation에는 균일 상호작용 전자기체에 대한 별도 자료와 매개화가 필요하다. 따라서 LDA라는 계열명만 쓰기보다 실제 exchange·correlation 조합도 기록하는 것이 좋다.[1,6]

Spin 분극을 허용할 때에는 $n_\uparrow,n_\downarrow$를 따로 넣는 local spin density approximation (LSDA)을 사용한다. 비편극식에 전체 밀도를 대입하는 것만으로 자기 상태를 비교할 수 있는 것은 아니다.[1,2]

### (2) 잘 맞는 물성과 대표 오차

LDA는 조밀한 고체의 구조를 비교하는 유용한 기준이지만, 결합 에너지와 격자 상수의 오차를 동일시해서는 안 된다. 여러 고체 benchmark에서 격자를 짧게, 응집을 강하게 예측하는 경향이 나타난다. 그러나 물질군에 따라 오차 크기와 예외가 달라지므로 이 경향을 부호가 고정된 법칙으로 쓰지 않는다.[4,7]

| 비교 대상 | LDA에서 기대할 수 있는 역할 | 별도 확인할 한계 |
| --- | --- | --- |
| 조밀한 고체의 평형 구조 | 단순한 기준 계산, 일부 계의 양호한 격자 상수 | 격자 과소평가와 bulk modulus 오차 |
| 분자 결합·고체 응집 | 결합 형성의 정성적 기술 | 과도한 결합과 원자 기준 에너지 오차 |
| 반도체 전자구조 | 밴드와 밀도의 출발점 | 고윳값 gap의 큰 과소평가 |
| 멀리 떨어진 중성 부분계 | 국소 환경의 XC 기술 | 올바른 장거리 dispersion 부재 |

표의 구조·응집 경향은 고체와 원자화 에너지 비교, gap과 장거리 한계는 전자구조 및 nonlocal 상호작용 분석에 근거한다.[1,4,5,7,8] LDA에서 격자 상수가 우연히 잘 맞아도, 그 사실만으로 분해 에너지나 gap까지 검증된 것은 아니다.

## 3. GGA: 밀도 기울기와 설계 목표

### (1) 비균일성의 표현

GGA는 밀도가 얼마나 빠르게 변하는지도 에너지에 반영한다. $e_{\mathrm{xc}}$를 부피당 에너지로 쓰면 대표 형식은

$$
E_{\mathrm{xc}}^{\mathrm{GGA}}[n]=\int e_{\mathrm{xc}}(n,\nabla n)\,d\mathbf r
$$

이다. 앞 절의 $\varepsilon_{\mathrm{xc}}$와 달리 $e_{\mathrm{xc}}$에는 밀도 인자가 포함된다. GGA는 각 공간점의 밀도와 그 기울기에 의존하는 에너지 함수를 사용한다. 따라서 LDA에서 출발하여 기울기 보정항을 낮은 차수부터 순서대로 더하는 gradient expansion과 동일한 방법은 아니다. 비균일성이 큰 실제 계에서는 단순 저차 전개보다 제약과 극한을 고려한 함수 형태가 중요하다.[1,2,6]

Spin 비편극 exchange의 비균일성을 비교할 때 국소 Fermi 파수 $k_F$와 무차원 reduced density gradient $s$를 쓴다.[6,9]

$$
k_F=(3\pi^2n)^{1/3},\qquad s=\frac{|\nabla n|}{2k_Fn}.
$$

$s$는 밀도의 절대 기울기를 국소 전자 길이 척도에 맞춰 정규화한다. 따라서 같은 $|\nabla n|$이라도 밀도가 다르면 $s$가 달라진다. 이를 이용한 exchange enhancement factor $F_{\mathrm x}$의 정의는

$$
E_{\mathrm x}^{\mathrm{GGA}}=\int n\varepsilon_{\mathrm x}^{\mathrm{unif}}(n)F_{\mathrm x}(s)\,d\mathbf r
$$

이다. $F_{\mathrm x}$는 균일계 exchange에 비해 적분의 각 영역을 어떻게 가중하는지 나타낸다. 이 식은 exchange의 설명용이며 correlation 전체가 같은 $s$만으로 정해진다는 뜻은 아니다.[6,9]

천천히 변하는 밀도에서의 개념적 전개는

$$
F_{\mathrm x}(s)=1+\mu s^2+\cdots\qquad(s\to0)
$$

로 쓴다. $\mu$는 이 극한의 이차항 계수이다. 서로 다른 GGA는 이 계수와 큰 기울기 영역의 거동을 다르게 선택할 수 있다. 기울기가 작은 영역과 큰 영역에 어떤 보정을 적용하는지가 원자·분자와 조밀한 고체에서 범함수의 상대적인 성능이 달라지는 원인 중 하나이다.[7,9]

### (2) PBE와 PBEsol의 차이

PBE는 폭넓은 결합 환경을 다루는 GGA이고, PBEsol은 고체의 천천히 변하는 밀도 영역에 더 적합하도록 수정한 GGA이다. PBEsol의 핵심은 exchange의 gradient expansion을 회복하여 조밀한 고체의 평형 구조를 개선하려는 것이다. 원자화 에너지에서는 같은 변경이 불리할 수 있다.[7,9]

| 비교 축 | PBE | PBEsol |
| --- | --- | --- |
| 설계에서 강조한 영역 | 원자·분자·고체를 함께 다루는 절충 | 조밀한 고체와 표면의 천천히 변하는 밀도 |
| 흔한 격자 경향 | LDA의 짧은 격자를 지나치게 늘리기도 함 | PBE의 격자 과대평가를 줄이는 경우가 많음 |
| 원자 기준 에너지 | 원자화·응집 비교의 유용한 출발점 | 원자화 에너지 악화 가능 |
| 선택할 때 볼 자료 | 실제 물질군의 에너지 차이 | 구조 개선과 에너지 차이를 각각 검증 |

이 비교는 “고체이면 항상 PBEsol”이라는 규칙이 아니다. 독립 고체 benchmark에서도 PBE는 응집 에너지에서 경쟁력이 있고, PBEsol의 구조상 이점이 모든 에너지 지표로 이어지지는 않는다. 구조 최적화와 상 안정성을 함께 연구한다면 두 목표를 따로 평가해야 한다.[4,7,9]

## 4. Meta-GGA: 운동에너지 밀도와 궤도 환경

### (1) 운동에너지 밀도

GGA의 정보만으로 구별하기 어려운 국소 궤도 환경을 구분하기 위해 meta-GGA는 양의 궤도 운동에너지 밀도 $\tau$ 등을 추가한다. SCAN 계열에서 사용하는 대표 형식은 다음과 같다.[2,3,6]

$$
E_{\mathrm{xc}}^{\mathrm{meta-GGA}}=\int e_{\mathrm{xc}}(n,\nabla n,\tau)\,d\mathbf r.
$$

Spin 채널을 $\sigma$, 정규화된 공간 궤도함수를 $\phi_{i\sigma}$, 그 점유수를 $f_{i\sigma}\in[0,1]$이라 하면

$$
\tau(\mathbf r)=\frac12\sum_{i,\sigma}f_{i\sigma}|\nabla\phi_{i\sigma}(\mathbf r)|^2
$$

이다. 이 문서에서는 $1/2$를 포함하고 두 spin 채널을 합한다. $\tau$의 차원은 원자단위계에서 길이의 역다섯제곱이며, 공간 적분은 보조계의 운동에너지 $T_s$를 준다. 다른 문헌의 spin별 $\tau_\sigma$ 또는 $1/2$ 없는 정의와 비교할 때 인자를 맞춰야 한다. Meta-GGA에는 밀도 Laplacian $\nabla^2n$을 쓰는 형태도 있지만 SCAN을 이해하는 데 필요한 추가 변수는 $\tau$이다.[2,3,6]

이 궤도 의존성 때문에 $\tau$ 기반 meta-GGA는 흔히 generalized Kohn–Sham (GKS) 방정식으로 구현한다. 이는 한 점에서 곱하는 국소 potential만을 쓰는 KS와 구별된다. 그렇다고 meta-GGA가 hybrid의 Fock exchange 적분을 이미 포함하는 것은 아니다.[1,2,10]

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

이는 한 공간점의 환경을 구별하는 지표이지, 원자 한 쌍의 결합 종류를 유일하게 판정하는 규칙은 아니다. 실제 결정에는 여러 $\alpha$ 영역이 공존한다. $\alpha\approx1$을 금속적 환경과 연결할 수는 있지만, 그 값만으로 물질 전체가 금속인지 판단하지 않는다.[3,6,12]

### (3) SCAN과 regularized 변형

SCAN은 meta-GGA 수준에서 만족할 수 있는 exact constraints와 appropriate norms를 함께 사용한다. Appropriate norms는 semilocal 근사가 정확하거나 매우 정확할 수 있는 기준계이며, 희가스 원자와 jellium 표면 등이 포함된다. 이는 특정 물질군의 오차에만 맞춘 피팅을 피하려는 설계이지 매개변수가 없다는 뜻은 아니다. 일반적인 exact constraints의 의미는 제6절에서 별도로 설명한다.[3,6,11]

SCAN의 $\alpha$와 보간 함수는 여러 국소 환경을 구별하지만, 낮은 밀도 영역과 보간 구간에서의 미분은 수치 적분에 민감할 수 있다. rSCAN은 지표와 보간 함수를 regularization하여 이를 완화했으나 일부 exact constraints를 잃었다. r²SCAN은 매끄러움을 유지하면서 균일계 극한, scaling과 이차 gradient expansion 등 주요 조건을 복원한다. 다만 exchange의 사차 gradient expansion은 복원하지 않으므로 세 범함수를 같은 수학적 함수의 구현 차이로 보아서는 안 된다.[10–13]

| 범함수 | 설계의 중심 | 구별할 한계 |
| --- | --- | --- |
| SCAN | 제약·기준계와 궤도 환경에 따른 보간 | 지표와 보간 함수의 수치적 민감도 |
| rSCAN | 지표·보간 함수의 regularization | 균일계 극한과 scaling 등 일부 조건의 손실 |
| r²SCAN | regularization과 주요 조건의 복원 | exchange의 사차 gradient expansion은 미복원 |

SCAN 계열의 국소 환경 구별은 여러 고체의 구조·에너지 기술을 개선할 수 있지만 모든 물성의 정확도를 보장하지 않는다. 특히 중간 거리의 약한 상호작용을 기술하는 것과 멀리 떨어진 중성 부분계 사이의 장거리 dispersion을 재현하는 것은 다르다. Semilocal correlation만으로 후자의 올바른 꼬리를 일반적으로 얻을 수 없으며, r²SCAN의 수치적 개선도 이 한계를 없애지 않는다.[3–6,10,12]

## 5. Hybrid: nonlocal exchange의 도입

### (1) Fock exchange와 혼합

Hybrid는 semilocal exchange의 일부를 점유 궤도함수로 계산한 Fock exchange로 바꾼다. 앞에서 정의한 $\phi_{i\sigma}$와 $f_{i\sigma}$를 사용하면 그 에너지는

$$
E_{\mathrm x}^{\mathrm{Fock}}=-\frac12\sum_{\sigma,i,j}f_{i\sigma}f_{j\sigma}
\iint\frac{\phi_{i\sigma}^*(\mathbf r)\phi_{j\sigma}(\mathbf r)
\phi_{j\sigma}^*(\mathbf r')\phi_{i\sigma}(\mathbf r')}
{|\mathbf r-\mathbf r'|}\,d\mathbf r\,d\mathbf r'
$$

이다. 같은 spin의 궤도 사이에 공간의 두 점을 연결하는 적분이 등장한다. 이 점이 한 점의 $n,\nabla n,\tau$만 평가하는 semilocal 근사와 다르다. “Exact exchange”라는 이름은 주어진 궤도로 만든 determinant의 exchange를 정확히 계산한다는 뜻이며 correlation까지 정확하다는 뜻은 아니다.[1,2]

혼합 비율을 $a$, semilocal 근사를 $\mathrm{sl}$로 표기한 단순 global hybrid의 예는

$$
E_{\mathrm{xc}}^{\mathrm{hyb}}=aE_{\mathrm x}^{\mathrm{Fock}}+(1-a)E_{\mathrm x}^{\mathrm{sl}}+E_{\mathrm c}^{\mathrm{sl}}
$$

이다. $a$는 공간과 전자 간 거리에 무관한 무차원 상수이다. 이는 전체 Hartree–Fock 에너지와 전체 DFT 에너지를 섞는 공식이 아니다. 또한 모든 hybrid가 위의 단순 혼합형을 따르는 것은 아니다. PBE0는 이 형식에 PBE exchange·correlation과 $a=1/4$을 사용하는 대표 사례이다.[1,2,8,14]

### (2) Range-separated hybrid와 HSE

Range-separated hybrid는 전자 사이 거리 $r_{12}=|\mathbf r-\mathbf r'|$에 따라 Coulomb kernel을 나눈다. Error function $\operatorname{erf}$와 complementary error function $\operatorname{erfc}=1-\operatorname{erf}$를 쓰는 분리는

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

장거리 Fock exchange를 제한하면 주기계에서의 계산 부담을 줄일 수 있다. 반대로 장거리 exchange를 Fock형으로 바꾸는 long-range-corrected 계열도 있다. 두 방향은 목적이 다르므로 range-separated hybrid라는 분류만으로 장거리 처리 방식이 같다고 생각하면 안 된다.[2,8,14]

| Hybrid 형태 | Fock exchange의 범위 | 선택에서 중요한 사항 |
| --- | --- | --- |
| Global hybrid | 모든 거리에서 일정 비율 | 혼합률과 주기계 계산 비용 |
| HSE형 screened hybrid | 단거리 부분 | 일반 반도체 gap과 넓은 gap 절연체의 차이 |
| Long-range-corrected hybrid | 장거리 비중을 강조 | 장거리 전하 분포·exchange의 요구 |

독립적인 고체 benchmark들은 hybrid가 GGA보다 많은 반도체 gap을 개선함을 보여 준다. 동시에 HSE가 유리한 보통의 반도체와 큰 gap의 이온성 절연체에서는 적합한 range separation과 혼합률이 다를 수 있다. “Hybrid이면 gap이 정확하다”는 결론은 성립하지 않는다.[8,14]

### (3) Nonlocal exchange의 역할과 한계

Hybrid의 nonlocal 연산자는 보통 GKS 틀에서 다룬다. Fock exchange 혼합은 semilocal 근사의 self-interaction 관련 오차를 줄일 수 있지만, 남아 있는 semilocal exchange와 correlation까지 정확하게 만들지는 않는다. 단전자 자기반발 상쇄 조건과 fractional electron number에서의 조건은 제6절에서 구별한다.[1,2,8,15]

Hybrid가 많은 반도체의 고윳값 gap을 개선하더라도, 그 사실이 정확한 국소 KS potential의 derivative discontinuity를 그대로 재현했다는 뜻은 아니다. GKS 연산자와 국소 KS potential은 서로 다른 고윳값 문제를 정의한다. 또한 Fock exchange 자체가 장거리 correlation을 제공하는 것은 아니며, 금속의 응집 에너지처럼 semilocal 근사가 더 나은 경우도 있다. Jacob’s ladder의 높이는 필요한 비국소 정보를 구분하는 기준이며 물성별 정확도의 보증서가 아니다.[1,2,4,8,14]

## 6. Exact constraints: 정확한 XC 범함수의 조건

Exact constraint는 특정 물질의 계산값에 맞춘 경험적 규칙이 아니라 정확한 XC 범함수가 따라야 하는 수학적·물리적 조건이다. 일부는 모든 허용 밀도에 적용되고, 일부는 uniform electron gas나 단전자계처럼 정해진 극한에 적용된다. 범함수의 입력 정보를 늘리면 더 많은 조건을 표현할 수 있지만, 몇 개를 만족하는지만으로 실제 물성의 정확도가 정해지지는 않는다. 이 절에서는 특정 SCAN 제약 목록과 독립적으로 주요 조건을 설명한다.[1,15]

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

이는 밀도가 비슷한 유한 분자나 표면을 균일계로 간주한다는 뜻이 아니다. 경계와 밀도 변화가 없는 기준계에서 근사가 일치해야 한다는 조건이다. LDA는 이 기준을 모든 점에 국소 적용하고, GGA와 meta-GGA는 추가 변수들이 균일계 값에 접근할 때 같은 기준으로 돌아가도록 설계할 수 있다. 실제 LDA의 correlation 매개화에는 기준 자료와 근사 오차가 있으므로, 정확한 균일계 한계라는 이론적 조건과 특정 수치 매개화의 정확도를 구별한다.[1,15]

제3절의 exchange enhancement factor로 쓰면 이 조건은 $F_{\mathrm x}(0)=1$이다. $\tau$ 기반 meta-GGA의 균일 비편극계에서는 $s=0$, $\alpha=1$이므로 같은 관례의 enhancement factor는 그 점에서 1이 되어야 한다. 균일계에서 살아남는 비정상적인 추가항은 LDA 기준 자체를 바꾸므로, gradient 보정이나 regularization을 설계할 때도 이 극한을 보존해야 한다.[9,10,15]

### (2) Exchange의 spin scaling과 coordinate scaling

Exchange의 spin dependence에는 정확한 **spin-scaling relation**이 있다. $E_{\mathrm x}^{\mathrm u}[n]$을 전체 밀도 $n$을 가진 spin 비편극계의 exchange 범함수라고 정의하면, collinear spin 밀도 $n_\uparrow,n_\downarrow$에 대해

$$
E_{\mathrm x}[n_\uparrow,n_\downarrow]
=\frac12\left(E_{\mathrm x}^{\mathrm u}[2n_\uparrow]
+E_{\mathrm x}^{\mathrm u}[2n_\downarrow]\right)
$$

이다. 같은 spin의 궤도 사이에서만 Fock exchange가 생긴다는 성질을 반영한다. 우변의 밀도를 두 배로 하고 에너지를 절반씩 더하는 규약이 중요하다. 각 spin 밀도를 그대로 비편극 범함수에 넣어 더하면 같은 관계가 아니다. Correlation에는 이 형태의 정확한 spin-scaling relation이 없으므로 exchange의 식을 correlation에 그대로 적용하지 않는다.[1,15]

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

을 만족한다. 정규화된 궤도는 $\phi_{i\sigma,\gamma}(\mathbf r)=\gamma^{3/2}\phi_{i\sigma}(\gamma\mathbf r)$로 변하고, 이를 Fock 적분에 넣으면 Coulomb kernel에서 남는 길이척도가 $\gamma$를 만든다. 따라서 이 조건은 exchange를 임의의 밀도 크기에 맞추는 경험적 규칙이 아니라 Coulomb exchange의 정확한 scaling이다. Correlation은 상호작용과 운동에너지의 변화를 함께 포함하므로 같은 일차 scaling 식을 따르지 않는다.[1,15]

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

이다. 두 식을 함께 적용해야 $E_{\mathrm H}+E_{\mathrm{xc}}=0$이 된다. 따라서 **self-correlation이 없다**는 조건과 **one-electron self-interaction이 없다**는 조건은 구별해야 한다. 이 설명은 순수 단전자 spin 상태에 대한 것이며 fractional-spin ensemble에 정의한 exchange·correlation 분해까지 같은 방식으로 확대하지 않는다.[1,15]

$\tau$를 사용하는 meta-GGA는 iso-orbital 정보를 통해 단전자 correlation 조건을 구현할 수 있지만, 이것만으로 임의의 단전자 밀도에 대한 nonlocal Hartree 에너지를 exchange가 정확히 상쇄하는 것은 아니다. Global hybrid도 Fock exchange를 부분적으로만 혼합하면 남은 semilocal 성분의 오차를 가질 수 있다. 특정 기준계에서의 에너지 일치와 모든 허용 단전자 밀도에 대한 항등식을 구별해야 한다.[1,15]

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

이다. Exchange가 이미 전자 하나의 결손을 정하므로 correlation은 전체 결손량을 더하는 대신 그 공간 분포를 바꾼다. 이 sum rule을 만족하는 hole이라도 정확한 에너지가 보장되지는 않는다. 에너지 적분에는 거리 가중치 $1/|\mathbf r-\mathbf r'|$가 있어, 같은 정규화를 가진 hole도 어디에 분포하는지에 따라 에너지가 달라진다.[1,15]

### (5) Lieb–Oxford bound

3차원 비상대론적 Coulomb 전자계의 XC 에너지는 밀도로 정해지는 보편적인 하한을 갖는다. Hartree 원자단위계에서 **Lieb–Oxford bound**의 한 유효한 형태는

$$
E_{\mathrm{xc}}[n]\ge -C_{\mathrm{LO}}\int n(\mathbf r)^{4/3}\,d\mathbf r,
\qquad C_{\mathrm{LO}}=1.68
$$

이다. 여기의 $C_{\mathrm{LO}}$는 사용할 수 있는 전통적인 보편 상수이며 최적으로 가장 작은 상수라는 주장은 아니다. 이 부등식은 XC 에너지가 제한 없이 음의 방향으로 낮아지는 것을 막는다. Spin 분극 여부와 관계없이 우변에는 전체 밀도 $n$을 넣으며, 조건은 국소 값이 아니라 공간 적분에 적용된다.[1,15]

이 조건의 출발점은 간접 Coulomb 에너지 $W-E_{\mathrm H}$의 하한이다. $T-T_s\ge0$인 KS 분해에서 $E_{\mathrm{xc}}=(T-T_s)+(W-E_{\mathrm H})$이므로 같은 하한이 XC에도 적용된다. 따라서 이 bound는 exchange만의 맞춤식이나 특정 균일계의 수치값이 아니다.[1,15]

범함수 설계에서는 enhancement factor에 점별 상한을 두어 적분 bound를 만족시키기도 한다. 이는 적분 조건을 보장하기 위한 더 강한 충분조건이며, 역방향의 함의는 성립하지 않는다. 따라서 국소적인 상한을 위반하더라도 전체 에너지의 Lieb–Oxford bound는 만족할 수 있다. 전 공간 적분의 정확한 bound를 점별 에너지 조건과 동일시해서는 안 된다.[15,16]

### (6) Slowly varying density와 gradient expansion

Uniform electron gas limit는 기울기가 정확히 0인 기준이다. **Gradient expansion**은 그 주변에서 밀도가 충분히 천천히 변할 때의 선도 보정을 제한한다. Spin 비편극 exchange의 공간 적분을 부분적분으로 정리하는 통상적인 표현에서 이차까지의 관계는 다음과 같다.[9,15]

$$
E_{\mathrm x}^{\mathrm{GE2}}[n]
=\int n\varepsilon_{\mathrm x}^{\mathrm{unif}}(n)
\left[1+\frac{10}{81}s^2\right]d\mathbf r.
$$

$\mathrm{GE2}$는 second-order gradient expansion을 뜻한다. 정확한 계수 $10/81$을 쓴 이 식도 임의의 비균일 밀도에 대한 정확한 exchange는 아니다. 낮은 차수에서 절단한 점근 전개이며, 밀도 기울기뿐 아니라 고차 공간 변화도 작아야 한다. 경계항을 제거하는 부분적분의 조건을 가정하고, 급격한 표면·꼬리 영역으로 전개의 적용 범위를 무제한 넓히지 않는다.[9,15]

밀도 변화의 추가 척도로 reduced Laplacian $q$를 정의하면

$$
q=\frac{\nabla^2n}{4k_F^2n}
$$

이다. $q$는 무차원이며, slowly varying limit에서는 $s\ll1$과 $|q|\ll1$을 함께 고려한다. 단지 한 점에서 $\nabla n=0$이라는 사실만으로 주변 밀도가 천천히 변한다고 결론 내릴 수는 없다. 예를 들어 밀도의 극값에서는 기울기가 0이어도 곡률은 클 수 있다. 이는 전개에 필요한 공간 조건을 구별하기 위한 해석이다.[9,15]

PBEsol은 exchange의 이차 계수를 회복하도록 설계되었다. 반면 PBE가 선택한 계수에는 다른 조건과 원자 에너지 기술 사이의 절충이 반영되어 있다. 따라서 GGA는 gradient expansion을 단순 절단한 것과 같지 않으며, 한 극한의 정확한 계수를 회복하는 것이 모든 밀도 영역에서 더 작은 오차를 보장하지는 않는다.[1,7,9]

### (7) Piecewise linearity와 derivative discontinuity

전자 수에 관한 exact constraint는 공간 기울기에 관한 조건과 성격이 다르다. 핵 위치와 외부 potential을 고정하고 영온에서 인접한 정수 전자 수의 바닥상태를 혼합하는 ensemble을 생각한다. 정수 $M$과 $0\le\delta\le1$에 대해 평균 전자 수가 $M+\delta$이면, 안정한 인접 정수 상태를 잇는 정확한 전체 에너지는

$$
E_0(M+\delta)=(1-\delta)E_0(M)+\delta E_0(M+1)
$$

이다. 이것이 **piecewise linearity**이다. 여기서 선형인 것은 전체 바닥상태 에너지 $E_0$이며 $E_{\mathrm{xc}}$만 따로 선형이어야 한다는 뜻이 아니다. Fractional electron number는 개별 순수 상태에 전자의 일부가 들어 있다는 뜻이 아니라, 서로 다른 정수 입자 수 상태의 ensemble 평균을 뜻한다.[17,18]

전자 수 $N$의 유한계에서 인접한 $N-1,N,N+1$ 상태가 정의되어 있을 때 ionization energy $I$와 electron affinity $A$를

$$
I=E_0(N-1)-E_0(N),\qquad A=E_0(N)-E_0(N+1)
$$

로 정의한다. Piecewise linearity에서 정수 양옆의 chemical potential은 각각

$$
\mu^-=-I,\qquad \mu^+=-A
$$

가 된다. 두 기울기의 차이 $I-A$는 fundamental gap이다. 이 관계는 고정 핵 전자 추가·제거 에너지에 관한 것이며, 구조 이완을 포함한 에너지나 광학 전이 에너지로 바꾸어 해석하지 않는다.[1,17,18]

정확한 multiplicative KS potential에서는 전자 수가 정수를 통과할 때 XC potential의 극한이 공간적으로 일정한 양만큼 달라질 수 있다. 동일한 potential 기준에서 그 차이를 **derivative discontinuity** $\Delta_{\mathrm{xc}}$로 정의하면

$$
v_{\mathrm{xc}}^+(\mathbf r)-v_{\mathrm{xc}}^-(\mathbf r)=\Delta_{\mathrm{xc}}
$$

이다. $v_{\mathrm{xc}}^\pm$는 전자 수가 정수의 위·아래에서 접근할 때의 함수 미분 $\delta E_{\mathrm{xc}}/\delta n$의 극한이다. 이 불연속은 입자 수가 달라질 때 나타나는 것이므로 한 전자 수에서 potential의 공간 의존성이 거칠어야 한다는 뜻은 아니다.[1,18]

정확한 국소 KS의 가장 높은 점유 및 가장 낮은 비점유 고윳값을 각각 $\varepsilon_{\mathrm H}$와 $\varepsilon_{\mathrm L}$로 쓰면

$$
E_g=I-A=(\varepsilon_{\mathrm L}-\varepsilon_{\mathrm H})+\Delta_{\mathrm{xc}}
$$

이다. 따라서 정확한 KS 계산에서도 고윳값 차이와 fundamental gap은 일반적으로 같지 않다. 이 식은 국소 KS 분해의 관계이며, nonlocal 연산자를 쓰는 근사 GKS gap에 같은 $\Delta_{\mathrm{xc}}$를 기계적으로 더하는 처방은 아니다.[1,17]

통상적인 근사 범함수의 유한계 $E_0(N+\delta)$가 정수점을 잇는 직선보다 아래로 휘면, 전하를 여러 조각으로 나눈 상태를 지나치게 낮은 에너지로 평가하여 delocalization을 선호할 수 있다. 반대 곡률은 localization을 지나치게 선호할 수 있다. 이 전하 분포 문제는 단전자 상쇄 한 가지만으로 완전히 판정되지 않으며, hybrid라는 계열명이나 exact exchange의 부분 혼합도 piecewise linearity를 자동으로 보장하지 않는다.[17,18]

## 7. 요약

- LDA는 uniform electron gas의 XC 에너지를 국소 적용하고, GGA는 밀도 기울기를 더한다. PBE와 PBEsol의 차이는 같은 정보 수준에서도 강조하는 밀도 영역과 조건이 달라질 수 있음을 보여 준다.[1,7,9]
- Meta-GGA는 운동에너지 밀도 등으로 궤도 환경을 구별한다. SCAN·rSCAN·r²SCAN은 이 계열 안에서 제약의 충족과 수치적 매끄러움을 다르게 조합한 범함수이다.[3,10–13]
- Hybrid는 nonlocal Fock exchange를 혼합하며, global·screened·long-range-corrected 형태는 이를 적용하는 거리가 다르다. Exact exchange가 정확한 correlation까지 뜻하지는 않는다.[1,2,8]
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
