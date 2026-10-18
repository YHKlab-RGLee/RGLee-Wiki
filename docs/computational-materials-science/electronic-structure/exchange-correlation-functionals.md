---
description: Jacob’s ladder의 LDA·GGA·meta-GGA·hybrid를 입력 정보와 물성별 한계로 비교하고 SCAN·rSCAN·r²SCAN의 설계와 수치 안정성을 설명한다.
---

# Exchange–correlation functionals

Exchange–correlation (XC) 범함수의 선택은 같은 원자 구조에서 얻는 결합 에너지, 평형 부피와 전자구조를 바꾼다. **Jacob’s ladder는 범함수가 사용하는 정보를 단계적으로 늘리는 분류이며, 모든 물성의 정확도가 반드시 높아지는 순위표는 아니다.** 국소 밀도를 사용하는 local density approximation (LDA), 밀도 기울기를 추가하는 generalized gradient approximation (GGA), 궤도함수의 운동에너지 밀도 등을 활용하는 meta-GGA, 비국소적인 Fock exchange를 혼합하는 hybrid 범함수를 차례로 다룬다. 각 단계에서 어떤 전자 환경과 상호작용을 추가로 기술할 수 있는지 구분하는 것이 중요하다.[1–4]

[Density functional theory](density-functional-theory.md) (DFT)의 Kohn–Sham (KS) 구성과 자기일관 계산을 선행 지식으로 삼는다. 여기서는 원자핵의 위치를 고정한 비상대론적 바닥상태를 기준으로 주요 식과 물성 비교를 설명하며, 범함수의 상세한 유도와 구현 방법은 다루지 않는다. Hartree 원자단위계 $\hbar=m_e=e=4\pi\varepsilon_0=1$을 사용하고, 궤도 자기장과 전류가 없는 경우를 다룬다. $m_e$는 전자 질량, $e$는 기본 전하의 양의 크기, $\varepsilon_0$는 진공 유전율이다. 자성 물성을 다룰 때에는 spin 채널을 분리한다. 다만 아래의 LDA·GGA 대표식과 SCAN 지표는 별도 언급이 없으면 spin 비편극 상태의 전체 전자 밀도로 표현한다.[1,2]

## 1. XC 에너지와 Jacob’s ladder

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

따라서 XC 에너지는 고전적인 Hartree 반발 항에 포함되지 않은 전자 간 상호작용의 기여와, 실제 상호작용계 및 KS 보조계 사이의 운동에너지 차이를 함께 포함한다. 아래에서 근사하는 것은 이 나머지 에너지의 범함수이다. 밀도와 궤도함수는 선택한 근사에 맞춰 다시 자기일관적으로 결정되므로, 서로 다른 범함수의 결과 차이는 같은 밀도에서 평가한 XC 에너지 차이만을 뜻하지 않는다.[1,2]

### (2) 입력 정보의 단계

대표 범함수로 Perdew–Burke–Ernzerhof (PBE), strongly constrained and appropriately normed (SCAN), Heyd–Scuseria–Ernzerhof (HSE)를 비교한다. SCAN의 변형인 regularized SCAN (rSCAN)과 regularized-restored SCAN (r²SCAN)은 제5절에서 설명한다. 표에 제시한 대표 범함수들은 같은 단계에 속하더라도 서로 다른 물성과 정확한 제약을 설계 목표로 삼을 수 있음을 보여 준다. 여기서 반국소란 공간의 한 점에서 밀도·기울기·운동에너지 밀도를 평가하여 적분한다는 뜻이다. 특히 $\tau$를 쓰는 meta-GGA는 궤도함수에 의존하므로 밀도만의 명시적 국소 함수와는 다르다.[2,3]

| 단계 | 추가하는 정보 | 대표 범함수 | 새로 구별하는 대상 |
| --- | --- | --- | --- |
| 1: LDA | 국소 밀도 $n$ | 균일 전자기체 기반 LDA | 밀도가 다른 영역 |
| 2: GGA | 밀도 기울기 $\nabla n$ | PBE, PBEsol | 밀도 비균일성 |
| 3: meta-GGA | $\tau$, 또는 $\nabla^2n$ | SCAN, rSCAN, r²SCAN | 같은 밀도·기울기에서도 다른 궤도 환경 |
| 4: hybrid | 점유 궤도 사이의 Fock exchange | PBE0, HSE | 공간적으로 떨어진 점 사이의 exchange |
| 5: 비점유 상태를 활용하는 근사 | 비점유 궤도·응답 정보 등 | Double hybrid, random phase approximation (RPA) 계열 | 반국소 모형을 넘는 correlation |

다섯째 단계의 RPA와 double hybrid는 여기서 위치만 짚는다. 이 단계는 비점유 상태까지 이용하는 correlation 모형으로 확장하며, hybrid에 exchange 비율만 더 높인 것을 뜻하지 않는다. 또한 경험적 매개변수의 수와 사다리의 높이는 별개의 분류이다. 같은 GGA나 meta-GGA 안에도 정확한 제약을 우선하는 설계와 기준 자료에 맞추는 설계가 존재한다.[1–3,5]

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

표의 구조·응집 경향은 고체와 원자화 에너지 비교, gap과 장거리 한계는 전자구조 및 비국소 상호작용 분석에 근거한다.[1,4,5,7,8] LDA에서 격자 상수가 우연히 잘 맞아도, 그 사실만으로 분해 에너지나 gap까지 검증된 것은 아니다.

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

## 4. Meta-GGA와 SCAN의 결합 환경 구별

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

### (3) SCAN의 제약과 성능

SCAN은 개발 당시 알려진 **meta-GGA가 만족할 수 있는 17개 정확한 제약**과 적절한 기준계를 함께 사용한 범함수이다. 제약에는 균일계 극한, scaling 관계와 gradient expansion 등이 포함된다. Appropriate norms는 반국소 근사가 정확하거나 매우 정확할 수 있는 기준계로, 희가스 원자와 jellium 표면 등이 쓰인다. “비경험적”이라는 말은 임의의 물질군 성능에 맞춘 피팅을 피한다는 설계 성격이며 매개변수가 전혀 없다는 뜻은 아니다.[3,6,11]

SCAN이 주목받은 이유는 Fock exchange를 계산하지 않는 단계에서 서로 다른 결합 환경의 구조와 에너지를 함께 개선할 가능성을 보였기 때문이다. 독립 benchmark에서는 여러 고체의 평형 구조가 PBE보다 개선되었다.[3,4] 강하게 결합한 화합물의 형성에너지에서도 GGA 대비 개선이 관찰되었지만, 약하게 결합한 화합물에서는 상대 성능이 달라진다. Band gap의 오차도 여전히 남으므로 구조와 에너지의 개선을 전자구조 전체의 정확성으로 확대하지 않는다.[3,12]

| SCAN의 설계상 추가 정보 | 설명할 수 있는 개선 | 그대로 남는 문제 |
| --- | --- | --- |
| $\alpha$에 따른 환경 구별 | 다양한 결합 영역에 다른 에너지 형태 적용 | 국소 지표만으로 모든 비국소 효과 결정 불가 |
| 제약과 기준계의 결합 | 여러 구조·결합 문제로의 전이 가능성 | 모든 물성에 대한 정확도 보증은 아님 |
| 반국소 범위의 correlation | 일부 중간 거리 약한 상호작용 | 장거리 dispersion의 정확한 꼬리 부재 |

표의 마지막 행은 특히 중요하다. 평형 거리 근처의 약한 결합을 잘 기술하는 것과, 멀리 떨어진 부분계 사이의 분산 상호작용을 재현하는 것은 다른 요구이다. SCAN의 중간 거리 성능은 장거리 보정을 불필요하게 만들지 않는다.[4–6]

## 5. SCAN에서 rSCAN과 r²SCAN으로의 발전

### (1) 수치 안정성과 물리적 정확도

SCAN에서 결합 환경을 구별하는 $\alpha$와 보간 함수는 물리적 유연성을 주지만, 그 미분은 수치적으로 까다로울 수 있다. 낮은 밀도 영역의 작은 분모와 보간 함수의 급격한 변화는 XC potential과 수치 적분에 민감도를 만든다. 따라서 에너지 함수가 합리적이라는 사실만으로 거친 적분 격자에서 안정된 에너지·힘을 얻는 것은 아니다.[10,11]

여기서 구별할 두 목표는 다음과 같다. 첫째는 충분히 수렴한 계산의 물리량이 기준 자료와 얼마나 가까운가이다. 둘째는 그 수렴한 값을 얼마나 안정적으로 얻는가이다. SCAN의 격자 민감도는 구현에 따라 다르며, 분자용 원자 중심 적분 격자에서 관찰한 문제를 모든 평면파 계산에 같은 크기로 적용해서는 안 된다.[10–12]

### (2) rSCAN의 regularization

rSCAN은 $\alpha$의 낮은 밀도 거동과 보간 함수를 매끄럽게 고쳐 수치 불안정을 줄였다. 이는 pseudopotential 생성과 자기일관 계산의 안정성을 개선하려는 변경이다. 그러나 원래 함수와 가까운 수치값을 유지하려는 변경이라도 정확한 scaling이나 균일계 극한을 자동으로 보존하지는 않는다.[10,11]

따라서 rSCAN을 단순히 “동일한 SCAN을 더 빠르게 계산하는 방법”으로 해석하면 안 된다. 수학적 형태와 만족하는 제약이 바뀐 별도의 범함수이므로, 수치 안정성과 물성의 정확도를 각각 평가해야 한다.[10,11]

### (3) r²SCAN의 제약 복원

r²SCAN은 수치적인 매끄러움을 유지하면서 rSCAN이 잃은 주요 제약을 회복하도록 설계되었다. 대표적인 변경은 iso-orbital indicator를 다음과 같이 정규화한 것이다.[10,12]

$$
\bar\alpha=\frac{\tau-\tau_{\mathrm W}}{\tau_{\mathrm{unif}}+\eta\tau_{\mathrm W}},\qquad \eta=10^{-3}.
$$

$\eta$는 무차원 regularization 매개변수이다. 상수 에너지 밀도를 분모에 더하는 대신 같은 차원과 scaling을 갖는 $\tau_{\mathrm W}$를 더한다. 균일 비편극계에서는 $\tau_{\mathrm W}=0$이므로 $\bar\alpha=1$이 유지된다. 그러나 r²SCAN을 구성하려면 이 지표뿐 아니라 보간 함수가 gradient expansion에 미치는 영향도 보정해야 한다. 따라서 위 식의 정의만 바꾸어서는 전체 r²SCAN 범함수를 구현한 것이 아니다.[10,12]

| 항목 | SCAN | rSCAN | r²SCAN |
| --- | --- | --- | --- |
| 우선 목표 | 제약·기준계와 폭넓은 정확도 | 수치 불안정 완화 | 안정성과 주요 제약의 동시 유지 |
| 균일계·scaling 제약 | 만족하도록 설계 | 일부 손실 | 주요 제약 복원 |
| Exchange의 이차 gradient expansion | 회복하도록 설계 | 변경으로 교란 | 복원하도록 보정 |
| Exchange의 사차 gradient expansion | 포함 | 보존하지 않음 | 의도적으로 복원하지 않음 |
| 실제 계산에서의 확인점 | 적분·자기일관 수렴 민감도 | 수치 개선과 제약의 변화 | 성능 유지 범위와 남은 물성 오차 |

“r²SCAN이 SCAN의 모든 제약을 그대로 만족한다”는 표현은 정확하지 않다. 특히 exchange의 사차 전개를 포기하면서 매끄러움을 확보한 절충을 구별해야 한다. 제약을 많이 만족한다는 사실과 유한한 시험 집합에서 오차가 작다는 사실은 서로 다른 평가이므로, 제약의 개수만으로 세 범함수의 물성 순위를 정하지 않는다.[10,12,13]

### (4) 대규모 계산에서의 의의

r²SCAN의 주요 목적은 meta-GGA가 사용하는 궤도 환경 정보를 유지하면서, 실제 자기일관 계산과 수치 적분을 더 안정적으로 수행할 수 있도록 하는 데 있다. 원 개발 논문의 분자·격자 시험과 독립적인 대규모 고체 계산에서는 SCAN과 유사한 수준의 물성 예측 정확도를 유지하면서도 수치적 안정성이 개선되는 결과를 보고했다. 독립 고체 연구는 형성에너지, 부피와 gap을 따로 비교하여 물성별 차이도 드러냈다.[10,12]

그렇다고 r²SCAN을 GGA와 같은 계산 비용으로 간주하거나, SCAN보다 모든 물성에서 정확하다고 해석할 수는 없다. 대규모 workflow의 시간에는 전자·이온 반복 수, 초기 구조와 병렬 설정이 함께 들어간다. 성공한 계산의 평균 시간뿐 아니라 실패와 재시도의 비중도 중요하다. r²SCAN의 수치적 장점은 연구를 더 안정적으로 수행하게 하지만, 남은 XC 근사 오차를 없애지는 않는다.[10,12]

## 6. Hybrid: 비국소 exchange의 도입

### (1) Fock exchange와 혼합

Hybrid는 반국소 exchange의 일부를 점유 궤도함수로 계산한 Fock exchange로 바꾼다. 앞에서 정의한 $\phi_{i\sigma}$와 $f_{i\sigma}$를 사용하면 그 에너지는

$$
E_{\mathrm x}^{\mathrm{Fock}}=-\frac12\sum_{\sigma,i,j}f_{i\sigma}f_{j\sigma}
\iint\frac{\phi_{i\sigma}^*(\mathbf r)\phi_{j\sigma}(\mathbf r)
\phi_{j\sigma}^*(\mathbf r')\phi_{i\sigma}(\mathbf r')}
{|\mathbf r-\mathbf r'|}\,d\mathbf r\,d\mathbf r'
$$

이다. 같은 spin의 궤도 사이에 공간의 두 점을 연결하는 적분이 등장한다. 이 점이 한 점의 $n,\nabla n,\tau$만 평가하는 반국소 근사와 다르다. “Exact exchange”라는 이름은 주어진 궤도로 만든 determinant의 exchange를 정확히 계산한다는 뜻이며 correlation까지 정확하다는 뜻은 아니다.[1,2]

혼합 비율을 $a$, 반국소 근사를 $\mathrm{sl}$로 표기한 단순 global hybrid의 예는

$$
E_{\mathrm{xc}}^{\mathrm{hyb}}=aE_{\mathrm x}^{\mathrm{Fock}}+(1-a)E_{\mathrm x}^{\mathrm{sl}}+E_{\mathrm c}^{\mathrm{sl}}
$$

이다. $a$는 공간과 전자 간 거리에 무관한 무차원 상수이다. 이는 전체 Hartree–Fock 에너지와 전체 DFT 에너지를 섞는 공식이 아니다. 또한 모든 hybrid가 위의 단순 혼합형을 따르는 것은 아니다. PBE0는 이 형식에 PBE exchange·correlation과 $a=1/4$을 사용하는 대표 사례이다.[1,2,8,14]

### (2) 거리 분리와 HSE

Range-separated hybrid는 전자 사이 거리 $r_{12}=|\mathbf r-\mathbf r'|$에 따라 Coulomb kernel을 나눈다. Error function $\operatorname{erf}$와 complementary error function $\operatorname{erfc}=1-\operatorname{erf}$를 쓰는 분리는

$$
\frac1{r_{12}}=\frac{\operatorname{erfc}(\omega r_{12})}{r_{12}}+\frac{\operatorname{erf}(\omega r_{12})}{r_{12}}
$$

이다. $\omega$는 길이의 역수 차원을 가진 분리 매개변수이며, 두 항은 각각 short range (SR)와 long range (LR)를 나타낸다. 이 kernel 분리 자체는 항등식이지만, 두 구간에서 어떤 exchange 근사를 선택할지는 모형의 선택이다.[2,8]

HSE 계열은 Fock exchange를 단거리 부분에만 혼합한다. 개념식은 다음과 같다.[2,8]

$$
E_{\mathrm{xc}}^{\mathrm{HSE}}=aE_{\mathrm x}^{\mathrm{Fock,SR}}(\omega)
+(1-a)E_{\mathrm x}^{\mathrm{PBE,SR}}(\omega)
+E_{\mathrm x}^{\mathrm{PBE,LR}}(\omega)+E_{\mathrm c}^{\mathrm{PBE}}.
$$

장거리 Fock exchange를 제한하면 주기계에서의 계산 부담을 줄일 수 있다. 반대로 장거리 exchange를 Fock형으로 바꾸는 long-range-corrected 계열도 있다. 두 방향은 목적이 다르므로 “거리 분리”라는 이름만으로 장거리 처리 방식이 같다고 생각하면 안 된다.[2,8,14]

| Hybrid 형태 | Fock exchange의 범위 | 선택에서 중요한 사항 |
| --- | --- | --- |
| Global hybrid | 모든 거리에서 일정 비율 | 혼합률과 주기계 계산 비용 |
| HSE형 screened hybrid | 단거리 부분 | 일반 반도체 gap과 넓은 gap 절연체의 차이 |
| Long-range-corrected hybrid | 장거리 비중을 강조 | 장거리 전하 분포·exchange의 요구 |

독립적인 고체 benchmark들은 hybrid가 GGA보다 많은 반도체 gap을 개선함을 보여 준다. 동시에 HSE가 유리한 보통의 반도체와 큰 gap의 이온성 절연체에서는 적합한 거리 처리와 혼합률이 다를 수 있다. “Hybrid이면 gap이 정확하다”는 결론은 성립하지 않는다.[8,14]

### (3) 비용과 잔여 오차

Fock exchange는 자기상호작용 오차를 줄이는 데 도움이 되지만, 부분 혼합만으로 일반적인 오차가 완전히 사라지는 것은 아니다. 단전자 밀도 $n_1$에 대한 정확한 조건은 다음과 같다.[1,8]

$$
E_{\mathrm x}[n_1]=-E_{\mathrm H}[n_1],\qquad E_{\mathrm c}[n_1]=0.
$$

이 조건에서 exchange에 의한 자기반발 상쇄와 correlation이 0이라는 조건은 구별된다. 특정 원자나 특정 correlation 한계를 잘 맞춘 meta-GGA를 모든 단전자 밀도에 대해 자기상호작용이 없는 범함수로 부를 수 없다. Hybrid 또한 사용하는 반국소 성분과 혼합 비율의 영향을 받는다.[1,6,8]

Hybrid의 비국소 연산자는 보통 GKS 틀에서 다룬다. 계산 비용의 증가와 함께 금속의 응집 에너지처럼 오히려 반국소 근사가 나은 물성도 있다. 구조·에너지·gap의 요구가 다르면 높은 단계 하나를 일괄 적용하기보다 각 목표에 맞는 검증이 필요하다.[1,4,8,14]

## 7. 물성별 평가와 비교 규약

### (1) 구조와 결합 에너지

서로 다른 범함수의 성능을 비교하려면 평가할 물리량부터 동일하게 정의해야 한다. 평형 격자 상수가 정확한지, 원자 사이의 결합이 얼마나 강한지, 기준 원소상에 비해 화합물이 얼마나 안정한지는 서로 다른 평가 문제이다. 아래 식들은 실제 비교에서 사용할 정의이며, 핵–핵 반발을 포함한 총에너지를 사용한다.[3,4,7,12]

!!! info "[Measurement]"
    **평형 구조와 압축성:** 여러 부피 $V$에서 내부 원자 좌표를 동일한 기준으로 고정하거나 이완하여 에너지 곡선 $E(V)$를 구한다. 그 최소점과 곡률을 각각

    $$
    V_0=\operatorname*{arg\,min}_V E(V)
    $$

    및

    $$
    B_0=V_0\left.\frac{d^2E}{dV^2}\right|_{V_0}
    $$

    로 정의한다. $V_0$는 평형 부피, $B_0$는 등온 영온 기준의 bulk modulus이다. $B_0$의 차원은 에너지/부피이다. 같은 최소점을 주는 두 곡선도 곡률이 다를 수 있으므로 부피와 압축성은 각각 검증한다. 측정치와 비교할 때 온도에 따른 팽창과 영점 진동을 어떻게 처리했는지 기록한다.[4,7]

!!! info "[Measurement]"
    **응집 에너지:** 계산 셀 안의 원소 $A$의 원자 수를 $N_A$, 전체 원자 수를 $N_{\mathrm{at}}$, 고립 원자의 에너지를 $E_A^{\mathrm{atom}}$, 셀 에너지를 $E_{\mathrm{cell}}$이라 하면 원자당 응집 에너지를

    $$
    E_{\mathrm{coh}}=\frac{\sum_A N_AE_A^{\mathrm{atom}}-E_{\mathrm{cell}}}{N_{\mathrm{at}}}
    $$

    로 정의한다. 이 문서에서는 결합으로 안정해지면 양수이다. 고립 원자의 spin과 점유 상태도 동일한 범함수로 적절히 계산해야 한다. 결정 에너지만 정확하게 수렴시키고 원자 기준을 잘못 잡으면 응집 에너지 비교가 달라진다.[4,7]

!!! info "[Measurement]"
    **형성 에너지:** $x_A=N_A/N_{\mathrm{at}}$, 기준 원소상의 원자당 에너지를 $\mu_A^{\mathrm{elem}}$이라 하면

    $$
    \Delta E_f=\frac{E_{\mathrm{cell}}}{N_{\mathrm{at}}}-\sum_Ax_A\mu_A^{\mathrm{elem}}
    $$

    이다. 형성 에너지가 음수이면 해당 화합물의 에너지가 지정한 원소 기준상들의 에너지 합보다 낮음을 뜻한다. 응집 에너지의 고립 원자 기준과 다르며, 음의 형성 에너지만으로 모든 경쟁 화합물에 대한 안정성을 보장하지는 않는다. 다른 범함수의 원소 기준을 섞지 말고, 실험 형성 enthalpy와 비교할 때 온도·압력·보정의 차이를 명시한다.[3,12]

### (2) 전자구조와 상호작용

Band gap을 평가할 때에는 전자 추가·제거 에너지와 KS/GKS 고윳값 차이를 구별한다. 고정 핵 유한계에서 $E_0(M)$을 전자 수 $M$의 바닥상태 에너지라 하면 fundamental gap은

$$
E_g=E_0(N+1)+E_0(N-1)-2E_0(N)
$$

이다. 이 fundamental gap은 정확한 국소 KS의 고윳값 gap과도 일반적으로 같지 않다.[1,8] Gap 종류의 이론적 구분은 선행 DFT 문서의 gap 절을 따른다. 여기서는 각 benchmark가 명시한 정의에 따라 KS/GKS 고윳값 gap을 평가하며, 기준값과 계산값의 정의를 확인한 뒤 오차를 비교한다.[8,14]

약한 결합에서는 분리 거리와 기준 부분계를 고정해야 한다. 두 부분계 $A,B$의 결합계 에너지를 $E_{AB}(R)$, 같은 내부 구조의 분리된 부분계 에너지를 $E_A,E_B$라 할 때 상호작용 에너지를

$$
E_{\mathrm{int}}(R)=E_{AB}(R)-E_A-E_B
$$

로 정의한다. 이 규약에서는 인력이 우세한 결합이 음수이다. 구조 이완에 따른 에너지까지 포함한 결합·해리 에너지와 구별하고, 기저 중첩 오차의 처리도 기록한다. 평형 거리와 잘 떨어진 구간을 함께 보아야 SCAN 계열의 중간 거리 기술과 장거리 dispersion의 누락을 구별할 수 있다.[5,10]

| 목표 물성 | 비교에 포함할 범함수의 역할 | 주요 해석상 한계 |
| --- | --- | --- |
| 조밀한 고체의 부피·격자 | LDA/PBE 기준, PBEsol과 SCAN 계열 비교 | 구조상 우위가 응집·형성 에너지의 우위는 아님 |
| 화합물 형성 에너지 | PBE와 SCAN/r²SCAN의 동일 원소 기준 비교 | 강한 결합 화합물과 금속간 화합물의 차이 |
| 반도체 gap | GGA/meta-GGA와 적절한 hybrid 비교 | KS/GKS 계산 방식과 기준 gap의 정의 |
| 약한 결합·층간 상호작용 | 반국소 성분과 명시적 dispersion 처리 비교 | 중간 거리 성능을 장거리로 외삽 불가 |
| 금속·자기 상태 | 초기 spin, 상과 에너지 차이를 함께 비교 | 초기 spin과 수렴한 상태의 구분 |

이 표는 모든 계에 적용할 하나의 범함수를 추천하는 것이 아니라, 목표 물성에 따라 무엇을 비교하고 검증해야 하는지 정리한 것이다. 고체 benchmark의 구조·응집 결과, 형성에너지·전자구조 분석과 분산 보정 시험을 함께 보면 물성마다 비교 축이 달라져야 함을 알 수 있다.[3–5,8,12,14]

### (3) 오차 통계와 수렴

!!! info "[Measurement]"
    동일한 물리량 $Q$에 대한 $M$개 표본에서 오차를 $d_i=Q_i^{\mathrm{calc}}-Q_i^{\mathrm{ref}}$로 둔다. 부호 편향은 mean error (ME), 전형적인 절대 오차는 mean absolute error (MAE)로 구분한다.

    $$
    \mathrm{ME}=\frac1M\sum_{i=1}^M d_i,\qquad
    \mathrm{MAE}=\frac1M\sum_{i=1}^M|d_i|.
    $$

    양·음의 오차가 상쇄되면 ME가 작아도 개별 예측은 부정확할 수 있다. 표본 목록, 기준값, 단위와 물질군별 통계를 함께 남긴다. 큰 gap 절연체나 큰 응집 에너지 물질을 추가하면 전체 평균과 순위가 달라질 수 있으므로 서로 다른 benchmark의 평균을 직접 순위화하지 않는다.[4,7,14]

상대 오차는 크기가 다른 양을 비교하는 데 유용하지만 기준값이 0에 가까울 때 주의해야 한다. $Q_i^{\mathrm{ref}}\ne0$일 때 이 문서에서는

$$
\delta_i=\frac{Q_i^{\mathrm{calc}}-Q_i^{\mathrm{ref}}}{|Q_i^{\mathrm{ref}}|}
$$

로 정의한다. $\delta_i$는 무차원이며, 백분율로 쓸 때 100을 곱한다. 약하게 형성되는 화합물처럼 기준 에너지의 크기가 작은 경우에는 절대 오차를 함께 보고해야 한다. 이는 형성에너지 차이를 상대적으로만 해석하지 않기 위한 보고 규약이다.[4,12,14]

## 8. 범함수 선택과 남은 한계

### (1) 계산 오차와 근사 오차의 분리

수렴하지 않은 계산을 비교하면 XC의 차이와 수치 오차를 혼동한다. Self-consistent field (SCF) 반복, 기저 표현, XC 적분과 결정의 파수 공간 표본은 서로 다른 수렴 문제이다. 특히 SCAN 계열에서는 에너지뿐 아니라 구조 최적화에 사용한 힘과 수치 격자의 민감도를 확인해야 한다.[2,10–12]

| 확인 대상 | 바꾸어 볼 조건 | 판단할 결과 |
| --- | --- | --- |
| 전자 반복 | SCF 허용 오차와 초기 밀도 | 에너지·밀도 잔차의 안정성 |
| 공간 표현 | 기저 크기, 평면파 cutoff | 목표 에너지 차이·힘의 변화 |
| 적분·표본 | XC 적분 격자, $k$-point 밀도 | 구조와 에너지 차이의 안정성 |
| 전자 상태 | 초기 spin과 점유 | 다른 자기일관 해의 존재 |
| 핵심 모형 | XC 이름, dispersion 및 추가 보정 | 수렴 후에도 남는 물리적 차이 |

서로 다른 범함수의 절대 총에너지를 나란히 놓고 더 낮은 값이 더 정확하다고 고르지 않는다. 범함수의 정확도는 동일한 기준으로 정의한 에너지 차이와 관측량이 기준값에서 얼마나 벗어나는지를 비교하여 평가해야 한다. 또한 다른 범함수로 최적화한 구조에서 한 번만 에너지를 평가한 결과와 완전히 재최적화한 결과를 구별해야 한다. 두 계산은 서로 다른 질문에 답한다.[1,2,4]

### (2) 사다리 전체에 걸친 한계

반국소 근사는 공간적으로 떨어진 영역을 직접 연결하는 정보가 제한되어 있어 장거리 전하 분포와 dispersion을 모두 해결하지 못한다. SCAN의 중간 거리 결합이나 hybrid의 exact exchange만으로 장거리 correlation을 일반적으로 확보할 수 없으므로, 비국소 correlation 또는 검증된 dispersion 보정을 별도로 고려한다. 보정을 추가한 계산은 원래 범함수 단독 계산과 구별해서 이름과 매개변수를 기록해야 한다.[1,2,5]

결합 길이가 크게 늘어나거나 여러 전자배치가 경쟁하는 경우에도 Jacob’s ladder의 상위 단계 범함수를 선택하는 것만으로 모든 문제가 해결된다고 기대해서는 안 된다. 근사 XC의 자기상호작용, 전하 비국소화와 강한 correlation 문제는 서로 관련되지만 하나의 오차 이름으로 모두 환원되지 않는다. 정확한 DFT의 가능성과 실제 LDA·GGA·meta-GGA·hybrid의 한계를 구분해야 한다.[1,6,8]

실제 선택에서는 먼저 목표 물성의 정의와 요구 오차를 정하고, 해당 물질군에서 검증된 범함수를 비교한다. 많은 후보 구조를 탐색해야 한다면 상대적으로 저비용인 반국소 범함수가 기준 계산으로 유용할 수 있다. 반대로 목표 전자구조가 비국소 exchange의 영향을 크게 받는다면 hybrid 범함수와의 비교가 필요하다. SCAN 계열의 발전은 이 사이에서 **더 풍부한 반국소 정보와 계산의 안정성을 함께 확보하려는 진전**으로 이해할 수 있다. 이 해석은 반국소·hybrid의 성능과 비용, SCAN/r²SCAN의 독립 시험 결과를 종합한 선택 원칙이며 보편적인 우열 선언은 아니다.[4,8,10,12,14]

## 9. 요약

- Jacob’s ladder는 사용 정보의 계층이다. 같은 단계 안의 설계 차이와 물성별 오차를 함께 보아야 한다.[2–4]
- LDA는 균일 전자기체를 국소 적용하고, GGA는 밀도 기울기를 추가한다. PBEsol의 구조상 이점이 원자화·형성 에너지 개선까지 보장하지 않는다.[1,4,7,9]
- Meta-GGA는 $\tau$ 등으로 국소 궤도 환경을 구별한다. SCAN의 제약과 기준계는 넓은 적용을 돕지만 장거리 dispersion과 gap의 오차는 남는다.[3–6,12]
- rSCAN은 수치적인 매끄러움을 높였고, r²SCAN은 주요 제약을 복원했다. r²SCAN은 exchange의 사차 gradient expansion까지 복원한 범함수는 아니다.[10–13]
- Hybrid는 비국소 Fock exchange를 혼합한다. 비용과 거리 처리, 남은 correlation 오차를 확인하면서 목표 물성에 맞춰 검증해야 한다.[1,2,8,14]

## 10. 참고문헌

1. K. Capelle, “A Bird's-Eye View of Density-Functional Theory,” *Brazilian Journal of Physics* **36**, 1318–1343 (2006). [DOI: 10.1590/S0103-97332006000700035](https://doi.org/10.1590/S0103-97332006000700035), [Author manuscript](https://arxiv.org/abs/cond-mat/0211443). §§4–5의 에너지 분해, 국소·반국소·궤도 의존 범함수와 한계를 참조한다.
2. S. Lehtola, F. Blockhuys, and C. Van Alsenoy, “An Overview of Self-Consistent Field Calculations Within Finite Basis Sets,” *Molecules* **25**, 1218 (2020). [DOI: 10.3390/molecules25051218](https://doi.org/10.3390/molecules25051218), [Author manuscript](https://arxiv.org/abs/1912.12029). §§III, XI의 에너지, $\tau$, 거리 분리와 비국소 correlation을 참조한다.
3. E. B. Isaacs and C. Wolverton, “Performance of the strongly constrained and appropriately normed density functional for solid-state materials,” *Physical Review Materials* **2**, 063801 (2018). [DOI: 10.1103/PhysRevMaterials.2.063801](https://doi.org/10.1103/PhysRevMaterials.2.063801), [Author manuscript](https://arxiv.org/abs/1804.06914). Introduction의 Eq. (3), 형성에너지 및 구조·자성·gap 시험을 참조한다.
4. G.-X. Zhang, A. M. Reilly, A. Tkatchenko, and M. Scheffler, “Performance of various density-functional approximations for cohesive properties of 64 bulk solids,” *New Journal of Physics* **20**, 063020 (2018). [DOI: 10.1088/1367-2630/aac7f0](https://doi.org/10.1088/1367-2630/aac7f0), [Repository full text](https://orbilu.uni.lu/bitstream/10993/38240/1/125-solids-DFT-NJP-2018.pdf). §§2–4의 물질군별 격자·응집·압축성 및 dispersion 비교를 참조한다.
5. J. G. Brandenburg, J. E. Bates, A. Ruzsinszky, J. Sun, and J. P. Perdew, “Benchmark tests of a strongly constrained semilocal functional with a long-range dispersion correction,” *Physical Review B* **94**, 115144 (2016). [DOI: 10.1103/PhysRevB.94.115144](https://doi.org/10.1103/PhysRevB.94.115144), [Author manuscript](https://arxiv.org/abs/1605.06971). §§I–III의 중간 거리와 장거리 구분, 분자·결정의 분산 보정 시험을 참조한다.
6. J. Sun, A. Ruzsinszky, and J. P. Perdew, “Strongly Constrained and Appropriately Normed Semilocal Density Functional,” *Physical Review Letters* **115**, 036402 (2015). [DOI: 10.1103/PhysRevLett.115.036402](https://doi.org/10.1103/PhysRevLett.115.036402), [Author manuscript](https://arxiv.org/abs/1504.03028). Eqs. (1)–(4), 제약·기준계와 Supplementary Material을 참조한다.
7. G. I. Csonka, J. P. Perdew, A. Ruzsinszky, P. H. T. Philipsen, S. Lebègue, J. Paier, O. A. Vydrov, and J. G. Ángyán, “Assessing the performance of recent density functionals for bulk solids,” *Physical Review B* **79**, 155107 (2009). [DOI: 10.1103/PhysRevB.79.155107](https://doi.org/10.1103/PhysRevB.79.155107), [Author manuscript](https://arxiv.org/abs/0903.4037). 격자·응집·bulk modulus와 영점·온도 보정 비교를 참조한다.
8. Y.-i. Matsushita, K. Nakamura, and A. Oshiyama, “Comparative study of hybrid functionals applied to structural and electronic properties of semiconductors and insulators,” *Physical Review B* **84**, 075205 (2011). [DOI: 10.1103/PhysRevB.84.075205](https://doi.org/10.1103/PhysRevB.84.075205), [Author manuscript](https://arxiv.org/abs/1104.2769). §II의 PBE0·HSE·LC 정의와 §IV의 물질별 비교를 참조한다.
9. J. P. Perdew et al., “Restoring the Density-Gradient Expansion for Exchange in Solids and Surfaces,” *Physical Review Letters* **100**, 136406 (2008). [DOI: 10.1103/PhysRevLett.100.136406](https://doi.org/10.1103/PhysRevLett.100.136406), [Author manuscript](https://arxiv.org/abs/0707.2088). Eqs. (1)–(2)와 Tables I–II의 PBEsol 설계·격자·원자화 에너지를 참조한다.
10. J. W. Furness, A. D. Kaplan, J. Ning, J. P. Perdew, and J. Sun, “Accurate and Numerically Efficient r²SCAN Meta-Generalized Gradient Approximation,” *The Journal of Physical Chemistry Letters* **11**, 8208–8215 (2020). [DOI: 10.1021/acs.jpclett.0c02405](https://doi.org/10.1021/acs.jpclett.0c02405), [Author manuscript](https://arxiv.org/abs/2008.03374). Eq. (6), Tables 1–2, Figs. 1–3의 제약·안정성·물성 시험을 참조한다.
11. A. P. Bartók and J. R. Yates, “Regularized SCAN functional,” *The Journal of Chemical Physics* **150**, 161101 (2019). [DOI: 10.1063/1.5094646](https://doi.org/10.1063/1.5094646), [Author manuscript](https://arxiv.org/abs/1903.01007). §II의 지표·보간 regularization, §III의 수치 시험을 참조한다.
12. R. Kingsbury, A. S. Gupta, C. J. Bartel, J. M. Munro, S. Dwaraknath, M. Horton, and K. A. Persson, “Performance comparison of r²SCAN and SCAN metaGGA density functionals for solid materials via an automated, high-throughput computational workflow,” *Physical Review Materials* **6**, 013801 (2022). [DOI: 10.1103/PhysRevMaterials.6.013801](https://doi.org/10.1103/PhysRevMaterials.6.013801), [Author-hosted full text](https://perssongroup.lbl.gov/papers/kingsbury_performance_comparison_2021.pdf). §§II–III와 Figs. 3–4의 물성별 오차·workflow 신뢰성을 참조한다.
13. J. W. Furness, A. D. Kaplan, J. Ning, J. P. Perdew, and J. Sun, “Construction of meta-GGA functionals through restoration of exact constraint adherence to regularized SCAN functionals,” *The Journal of Chemical Physics* **156**, 034109 (2022). [DOI: 10.1063/5.0073623](https://doi.org/10.1063/5.0073623), [Author manuscript](https://arxiv.org/abs/2110.00647). §§II–III의 regularization·gradient expansion과 제약 복원 범위를 참조한다.
14. A. J. Garza and G. E. Scuseria, “Predicting Band Gaps with Hybrid Density Functionals,” *The Journal of Physical Chemistry Letters* **7**, 4165–4170 (2016). [DOI: 10.1021/acs.jpclett.6b01807](https://doi.org/10.1021/acs.jpclett.6b01807), [Author manuscript](https://arxiv.org/abs/1608.04796). Statistical Evaluation과 discussion의 독립 gap benchmark·비용 비교를 참조한다.
