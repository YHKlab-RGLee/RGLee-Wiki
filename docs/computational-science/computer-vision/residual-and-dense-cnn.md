---
description: ResNet의 identity 경로, ResNeXt의 cardinality, DenseNet의 feature 누적을 Jacobian과 연산·메모리 비용으로 비교한다.
---

# CNN: Residual and dense architectures

Convolutional neural network (CNN)의 깊이를 늘릴 때에는 층의 수뿐 아니라 기존 feature를 다음 층에 전달하는 방식이 중요하다. Residual network (ResNet)은 같은 좌표의 feature에 보정값을 더하고, ResNeXt는 그 보정을 여러 같은 형태의 변환으로 나누며, densely connected convolutional network (DenseNet)은 이전 feature와 새 feature를 채널 방향으로 연결한다. 이 차이는 역전파 경로, 블록 내부 폭, 저장해야 할 tensor를 함께 바꾼다.[1,2,3,4,5]

Convolution의 출력 형상과 기본 비용은 [CNN: Classic architectures](classic-cnn-architectures.md)를 따른다. Multiply–accumulate (MAC)는 곱 하나의 누산이며, 이 글의 수치는 이미지 한 장의 forward convolution만 센다. Bias, batch normalization (BN), rectified linear unit (ReLU), pooling과 원소별 덧셈은 가중치·MAC 표에서 제외한다. Floating-point operation (FLOP)은 곱셈과 덧셈을 각각 세므로 내적 중심 환산은 약 $2\,\mathrm{MAC}$이다. 아래 수치는 명시한 계산 그래프의 직접 계수 결과이며 정확도나 실행 시간을 측정한 값이 아니다.

## 1. Residual 표현과 깊이의 최적화

### (1) Identity를 기준으로 한 보정

블록 입력을 $x$, 원하는 변환을 $T$, 학습하는 residual 함수를 $F$라 하자. 입출력 차원이 같을 때 residual 표현은 다음과 같다. 여기서 뺄셈과 덧셈은 같은 공간 위치와 채널 사이의 연산이다.[1,2]

$$
T(x)=x+F(x),\qquad F(x)=T(x)-x.
$$

이 표현에서 기준 상태는 identity이다. 필요한 변환이 입력과 비슷하면 $F$가 작은 보정을 담당하고, 정확한 identity가 필요하면 $F=0$인 해를 쓰면 된다. 다만 residual이라는 이름만으로 학습 중 $F$의 크기가 항상 작다는 조건이 생기지는 않는다. 함수의 표현을 바꾼 것이며, residual 크기를 제한하는 별도 제약을 도입한 것은 아니다.[1,2]

얕은 네트워크가 표현할 수 있는 함수 집합을 $\mathcal H_s$, identity 블록을 삽입한 깊은 네트워크의 집합을 $\mathcal H_d$라 하자. 삽입 위치의 형상이 같고 추가 블록이 identity를 정확히 표현할 수 있으며 다른 층의 파라미터를 그대로 복사할 수 있다면, 같은 훈련 목적함수 $\mathcal L_{\rm train}$에 대해 다음 관계가 성립한다. 이 식은 두 출처의 identity 구성 논리를 집합과 최적값으로 정리한 것이다.[1,2]

$$
\mathcal H_s\subseteq\mathcal H_d
\quad\Longrightarrow\quad
\inf_{f\in\mathcal H_d}\mathcal L_{\rm train}(f)
\leq
\inf_{f\in\mathcal H_s}\mathcal L_{\rm train}(f).
$$

왼쪽은 표현 가능한 해의 포함 관계이고, 오른쪽은 가능한 최선의 훈련 목적값에 관한 명제이다. 실제 optimizer가 제한된 학습 시간 안에 그 해에 도달한다는 명제는 아니다. 추가 파라미터에 다른 정규화 항을 부과하거나 downsampling으로 입력 정보를 버리는 블록을 삽입하면 위 구성의 조건부터 다시 확인해야 한다. Residual 연결의 역할은 좋은 해의 존재와 실제 학습의 접근성 사이를 다루는 데 있다.

### (2) Degradation과 일반화 오차

깊은 모델의 **degradation**은 깊이를 더 늘렸을 때 훈련 자체가 나빠지는 문제를 가리킨다. 훈련 오차가 낮아지면서 검증 오차가 나빠지는 overfitting과 관찰 축이 다르다. ResNet의 동기는 전자이며, identity 해를 넣을 수 있다는 사실만으로 최적화가 자동으로 쉬워지는 것은 아니라는 점이 핵심이다.[1,2]

| 비교 관찰 | 먼저 조사할 대상 | 필요한 비교 조건 |
| --- | --- | --- |
| 깊은 모델의 훈련 오차가 더 큼 | 최적화와 학습 예산 | 같은 자료·목적함수·평가 절차 |
| 훈련 오차는 감소하지만 검증 오차는 증가 | 일반화와 정규화 | 동일한 검증 분할과 전처리 |
| 훈련과 검증 모두 개선 | 해당 조건에서의 유효한 구조 변경 | 반복 학습과 자원 비용 |

두 현상은 서로 배타적인 모델 분류가 아니다. 한 모델에서도 초기에 최적화가 어렵고 이후 과적합이 생길 수 있다. 따라서 최종 검증 정확도 한 점을 보고 residual 연결의 효과를 판정하기보다, 같은 시점에서 훈련과 검증의 변화를 함께 비교해야 한다. 또한 BN과 자료 증강을 사용하는 훈련 중 지표는 평가 모드의 지표와 계산 조건이 다르므로, 지표를 대조할 때 그 차이도 고정해야 한다.[1,2,6,7,8]

## 2. Identity 경로와 Jacobian

### (1) 블록 내부와 깊이 방향의 미분

동일한 형상을 유지하는 구간에서 블록 번호를 $l$, 마지막 번호를 $L$이라 하자. 덧셈 뒤 activation이 없고 shortcut이 identity이면 블록은 $x_{l+1}=x_l+F_l(x_l)$이다. Tensor를 벡터로 펼친 뒤 $J_{F_l}=\partial F_l/\partial x_l$로 정의하면 다음 Jacobian을 얻는다.[9,10]

$$
\frac{\partial x_{l+1}}{\partial x_l}=I+J_{F_l}.
$$

$I$는 입력 차원의 identity matrix이다. 손실을 $\mathcal L$, 열벡터 gradient를 $g_l=\nabla_{x_l}\mathcal L$이라 두면 chain rule은 다음과 같다. $J_{F_l}$에는 residual 경로의 convolution, BN, activation 미분이 모두 포함된다.

$$
g_l=(I+J_{F_l})^{\mathsf T}g_{l+1}
=g_{l+1}+J_{F_l}^{\mathsf T}g_{l+1}.
$$

이 식의 첫 항에는 residual 경로의 가중치 곱이 없다. 그러나 전체 gradient는 두 항의 합이므로, identity 경로가 있다는 것과 gradient norm에 양의 하한이 있다는 것은 다르다. 예를 들어 국소적으로 $J_{F_l}=-I$이면 두 항이 상쇄된다. 이 예는 chain rule 자체에서 얻는 반례이며, 실제 학습에서 그러한 상태가 흔하다는 주장은 아니다.

같은 조건의 블록을 이어 붙이면 중간 상태를 소거하여 다음 관계를 얻는다. 각 $F_i$의 입력 $x_i$는 앞 블록에 의존하므로, residual 함수들이 독립적으로 계산된다는 의미는 아니다.[9,10]

$$
x_L=x_l+\sum_{i=l}^{L-1}F_i(x_i),
\qquad
\frac{\partial x_L}{\partial x_l}
=I+\frac{\partial}{\partial x_l}\sum_{i=l}^{L-1}F_i(x_i).
$$

전체 미분을 블록별 Jacobian의 곱으로 적어도 같은 결과를 얻는다. 직접 전달 항과 여러 residual 경로의 항이 곱을 전개했을 때 함께 나타나는 것이다. 단지 $I$ 항만 떼어 놓고 나머지를 무시하면 폭발이나 상쇄 가능성을 판단할 수 없다.

이를 정량적으로 보기 위해 모든 블록이 같은 하나의 국소 미분값 $\alpha$를 갖는 스칼라 모형을 생각하자. 이 모형은 여러 채널과 BN의 결합을 제거한 설명용 선형화이다. $n=L-l$개의 블록에 대해 다음과 같다.

$$
\frac{\mathrm d x_L}{\mathrm d x_l}=(1+\alpha)^n.
$$

예를 들어 $n=100$이면 $\alpha=0.01$에서 약 2.705, $\alpha=-0.01$에서 약 0.366이다. 작은 residual Jacobian도 많은 깊이에 걸쳐 누적되며, identity 연결은 모든 singular value를 1로 고정하는 장치가 아니다. 반대로 $\alpha=0$인 지점에서는 깊이와 관계없이 직접 경로의 미분이 정확히 1이다. 이런 비교가 residual 크기와 깊이를 함께 보아야 하는 이유를 설명한다.

### (2) Post-activation과 pre-activation

원래 ResNet의 post-activation 블록은 합산 결과에 ReLU를 적용한다. $u_l=x_l+F_l(x_l)$라 두고, $D_l$을 $u_l$의 양수 좌표에서는 1, 음수 좌표에서는 0인 대각행렬이라 하면 미분 가능한 점에서 다음과 같다. 0에서의 미분은 사용하는 구현의 규약에 따르며 여기의 국소 식에서는 제외한다.[1,6,9]

$$
x_{l+1}=\operatorname{ReLU}(u_l),
\qquad
\frac{\partial x_{l+1}}{\partial x_l}=D_l(I+J_{F_l}).
$$

이제 shortcut을 거친 항도 $D_l$을 통과한다. 따라서 앞 절의 여러 블록 사이 identity 식을 post-activation 네트워크 전체에 그대로 적용하면 안 된다. 또한 $F_l=0$일 때 출력은 $\operatorname{ReLU}(x_l)$이므로, identity라는 설명은 $x_l\geq0$인 영역에서 성립한다. 이전 블록 출력이 ReLU를 거친 구간에서는 이 조건을 만족할 수 있지만 임의의 부호를 가진 입력에 대한 전역 identity는 아니다.

Full pre-activation은 BN과 ReLU를 각 가중치 층 앞에 두고, identity 블록의 덧셈 뒤에는 activation을 놓지 않는 구성이다. $\widetilde F_l$에 pre-activation을 포함한 residual 경로 전체를 모으면 다음과 같다.[9,10]

$$
x_{l+1}=x_l+\widetilde F_l(x_l).
$$

| 구성 | Residual 경로의 기본 순서 | 덧셈 뒤 연산 | 같은 형상에서의 직접 경로 |
| --- | --- | --- | --- |
| Post-activation | Conv–BN–ReLU, 마지막 Conv–BN | ReLU | ReLU 미분을 통과 |
| Full pre-activation | BN–ReLU–Conv 반복 | 없음 | Identity |

Pre-activation에서는 residual 경로가 양수와 음수 보정을 모두 출력할 수 있고 합산 결과도 부호가 제한되지 않는다. 마지막 residual 출력에 ReLU를 붙인 뒤 합산하는 변경은 이 구조와 다르다. 그 경우 residual이 원소별 비음수가 되어 각 좌표가 감소하는 보정을 제한하기 때문이다. 또한 pre-activation이라는 이름만으로 transition의 projection까지 identity가 되지는 않는다.[9,10]

BN을 포함한 미분은 평가 모드와 훈련 모드를 구별해야 한다. 평가 시 고정된 평균·분산을 사용하면 BN은 채널별 affine 변환으로 볼 수 있다. 훈련 시에는 통계가 batch에 의존하므로 $J_F$를 이미지 한 장에만 닫힌 행렬로 해석하면 충분하지 않을 수 있다. 위 식은 필요한 batch 전체를 $x$에 포함하면 그대로 적용되는 chain rule이며, BN의 영향을 생략한 gradient 보존 증명은 아니다.[7,8]

### (3) Projection과 stage 경계

입출력 채널이나 공간 격자가 다르면 원소별 덧셈을 바로 할 수 없다. Shortcut에 형상을 맞추는 함수 $S_l$을 두면 일반식은 다음과 같다. $J_{S_l}$은 이 함수의 Jacobian이며, 평가 모드의 convolution과 BN을 선형화한 shortcut에서는 그 affine 변환의 선형 부분이다.[1,6,9]

$$
x_{l+1}=S_l(x_l)+F_l(x_l),
\qquad
\frac{\partial x_{l+1}}{\partial x_l}=J_{S_l}+J_{F_l}.
$$

Projection이 차원을 줄이면 Jacobian은 직사각형일 수 있다. 이 경계에서는 $I$를 통한 모든 입력 좌표의 보존을 요구할 수 없다. 따라서 긴 ResNet을 이해할 때에는 같은 형상의 identity 블록 구간과, 해상도·채널을 바꾸는 stage 경계를 나누어 분석하는 것이 정확하다. Post-activation projection 블록이라면 위 Jacobian 앞에 앞 절의 $D_l$도 추가된다.

Stride를 가진 $1\times1$ convolution으로 $C_{\rm in}$에서 $C_{\rm out}$으로 투영하고 출력 격자가 $H'\times W'$이면, bias와 BN을 제외한 비용은 다음과 같다. $P$는 가중치 수, $M$은 MAC 수이다.[1,6]

$$
P_{\rm proj}=C_{\rm in}C_{\rm out},
\qquad M_{\rm proj}=H'W'C_{\rm in}C_{\rm out}.
$$

예를 들어 $256\to512$, 출력 $28\times28$이면 projection만으로 가중치 131,072개와 102,760,448 MAC을 쓴다. Identity shortcut에는 학습 가중치가 없지만 모든 shortcut이 무비용인 것은 아니다. 원소별 합산도 출력 원소 수만큼 덧셈과 데이터 접근이 필요하며, 여기서는 정한 MAC 계수 범위 밖에 있을 뿐이다.

## 3. ResNet의 블록 폭과 계산 배치

### (1) Basic block과 bottleneck

Basic block은 두 $3\times3$ convolution을 사용한다. Bottleneck은 $1\times1$ 축소, $3\times3$ 공간 변환, $1\times1$ 복원 순서로 계산한다. 같은 해상도와 외부 채널 $C$, 내부 채널 $B$를 갖는 identity 블록에서 가중치 수는 다음과 같다.[1,6]

$$
P_{\rm basic}=18C^2,
\qquad
P_{\rm bottle}=2CB+9B^2.
$$

두 식은 같은 외부 형상을 갖는 서로 다른 블록을 비교한다. Bottleneck의 두 pointwise convolution은 모든 외부 채널을 낮은 차원으로 혼합하고 다시 펼친다. 내부 $3\times3$가 다루는 채널 수가 $B$로 줄어 비용이 내려가지만, 이것을 두 full-width convolution과 동일한 함수의 단순한 빠른 실행법으로 볼 수는 없다. 중간 차원과 비선형 변환의 위치가 다르기 때문이다.[1,6]

표준적인 $B=C/4$를 대입하면 다음 비율이 나온다. 세 convolution 모두 같은 격자에서 계산되고 projection이 없는 경우에는 MAC 비율도 동일하다.

$$
P_{\rm bottle}=\frac{17}{16}C^2,
\qquad
\frac{P_{\rm bottle}}{P_{\rm basic}}=\frac{17}{288}\simeq0.0590.
$$

이 큰 차이를 해석할 때 비교 축을 확인해야 한다. 실제 ResNet 계열의 basic stage와 bottleneck stage는 외부 폭을 같게 두지 않을 수 있다. 예를 들어 basic의 외부 폭 64와 bottleneck의 내부 폭 64·외부 폭 256을 비교하면 두 블록의 가중치 수는 73,728개와 69,632개로 비슷해진다. 앞의 약 5.9%는 외부 폭을 256으로 맞춘 별도의 비교이며 모델 계열 전체의 절감률이 아니다.[1,6]

| 블록 조건 | 첫 convolution | 중간 convolution | 마지막 convolution | 합계 가중치 |
| --- | --- | --- | --- | --- |
| Basic, $C=64$ | 36,864 | — | 36,864 | 73,728 |
| Basic, $C=256$ | 589,824 | — | 589,824 | 1,179,648 |
| Bottleneck, $C=256,B=64$ | 16,384 | 36,864 | 16,384 | 69,632 |

마지막 행을 $56\times56$에 놓으면 convolution MAC은 $69{,}632\times3{,}136=218{,}365{,}952$이다. 이 예제는 첫 stage에 진입하는 projection 블록이 아니라 이미 폭 256을 갖는 stage 내부 블록이다. 입력이 64에서 256으로 바뀌는 첫 블록을 계수하려면 첫 convolution의 입력 폭과 projection 비용을 따로 넣어야 한다.

### (2) Downsampling 위치와 구현 변형

Stride 2를 bottleneck의 첫 $1\times1$에 놓는 구성과 가운데 $3\times3$에 놓는 구성은 같은 가중치 수를 갖지만 MAC은 다르다. Keras의 ResNet v1 구현은 전자를, 여기서 확인한 Torchvision bottleneck은 후자를 사용하며 후자는 흔히 ResNet v1.5라 부른다. 이 구분은 pre-activation을 뜻하는 v2 구분과 별개의 축이다.[6,10]

입력 $H\times W\times C_{\rm in}$, 내부 폭 $B$, 출력 $H'\times W'\times C_{\rm out}$인 블록을 생각하자. 두 공간 길이가 정확히 절반이 되어 $H'W'=HW/4$이고, 둘 다 같은 출력 크기의 projection을 쓴다고 가정하면 residual 경로의 MAC은 다음과 같다. 아래에는 projection을 아직 더하지 않았다.[6,10]

$$
M_{\rm first}=H'W'(C_{\rm in}B+9B^2+BC_{\rm out}),
$$

$$
M_{\rm middle}=HWC_{\rm in}B+H'W'(9B^2+BC_{\rm out}).
$$

후자는 첫 pointwise 변환을 큰 격자에서 수행하므로 차이는 다음과 같다. 홀수 해상도나 다른 padding에서는 실제 출력 크기로 첫 두 식을 계산해야 한다.

$$
M_{\rm middle}-M_{\rm first}
=(HW-H'W')C_{\rm in}B
=\frac34HWC_{\rm in}B.
$$

$56\times56$, $C_{\rm in}=256$, $B=128$, $C_{\rm out}=512$에서 출력이 $28\times28$이면, 첫 pointwise를 큰 격자에 유지하는 데 77,070,336 MAC이 추가된다. Projection까지 포함한 비용을 직접 비교하면 다음과 같다.

| Stride 2 위치 | Residual 경로 MAC | Projection MAC | 블록 합계 MAC |
| --- | --- | --- | --- |
| 첫 $1\times1$ | 192,675,840 | 102,760,448 | 295,436,288 |
| 가운데 $3\times3$ | 269,746,176 | 102,760,448 | 372,506,624 |

같은 ResNet-50이라는 이름만으로 정확한 계산 그래프가 결정되지는 않는다는 예이다. 재현 시에는 stage 반복 수뿐 아니라 stride 위치, shortcut, activation 순서를 기록해야 한다. 학습된 checkpoint의 성능 차이를 비교하려면 이 구조 차이와 학습 방식 차이도 분리해야 하며, 위 표는 연산 배치에 관한 차이만 계수한 것이다.

## 4. ResNeXt의 cardinality와 연산 예산

### (1) 같은 형태의 병렬 변환

ResNeXt의 **cardinality**는 집계하는 변환 경로의 수이다. 경로 수를 $g$, 각 경로의 변환을 $T_j$라 하면 residual 부분을 다음과 같이 쓴다. 각 경로는 같은 구조를 갖지만 가중치를 공유한다는 뜻은 아니다.[2,3]

$$
F(x)=\sum_{j=1}^{g}T_j(x).
$$

구현에서는 경로마다 전체 연산을 따로 실행하는 대신 내부 채널을 $g$개 그룹으로 나눈 $3\times3$ convolution을 사용할 수 있다. 그룹당 폭을 $d$, 전체 내부 폭을 $D=gd$로 두면, 외부 폭 $C$인 블록의 연결은 다음과 같다. 앞뒤 $1\times1$는 일반적인 dense convolution이며 가운데만 grouped convolution이다.[3,6]

$$
C\ \xrightarrow{1\times1}\ D=gd
\ \xrightarrow{3\times3,\;g\text{ groups}}\ D
\ \xrightarrow{1\times1}\ C.
$$

첫 pointwise 층이 입력 전체로부터 그룹별 feature를 만들고, 마지막 pointwise 층이 각 그룹의 결과를 출력 채널로 합친다. 따라서 가운데 공간 변환이 그룹별로 분리되어 있어도 블록 전체가 입력 채널의 독립적인 $g$개 조각으로 분리되는 것은 아니다. 모든 convolution을 group으로 바꾸면 이 연결 관계와 비용식도 달라진다.[2,3,6]

마지막 pointwise의 가중치를 그룹별 열 묶음 $W_j$로 나누고, 중간 출력을 $z_j$라 쓰면 $W[z_1;\ldots;z_g]=\sum_jW_jz_j$이다. 이 선형성으로 concatenation 뒤 dense pointwise와 경로별 projection 뒤 summation의 대응을 확인할 수 있다. 다만 이 등가성을 사용할 때에는 합산 뒤 BN을 경로별 BN으로 마음대로 이동시키면 안 된다. 별도의 정규화와 비선형성이 들어가면 같은 선형 항의 재배열이라는 조건이 깨진다.[3,6]

### (2) 폭 고정 조건별 비용

같은 해상도·입출력 폭·stride 1에서 가중치 수는 다음과 같다. 그룹 수 $g$는 $D$를 나누어야 하며, 식의 $D$는 한 그룹의 폭이 아니라 전체 내부 폭이다.[2,3,6]

$$
P_{\rm next}=2CD+\frac{9D^2}{g}
=g(2Cd+9d^2),
\qquad M_{\rm next}=HW P_{\rm next}.
$$

전체 폭 $D$를 고정하면 $g$를 늘릴수록 가운데 항만 줄어든다. 그룹 수가 늘수록 각 그룹의 폭 $d=D/g$가 작아져 공간 convolution이 연결할 수 있는 채널 쌍이 줄기 때문이다. 반대로 그룹당 폭 $d$를 고정하면 전체 폭도 함께 증가하여 비용이 $g$에 비례한다. 따라서 “cardinality 증가의 비용”에는 무엇을 고정했는지 반드시 따라붙어야 한다.

| 고정하는 값 | $g$ 증가에 따른 변화 | 가중치의 의존성 |
| --- | --- | --- |
| $C,D$ | 그룹당 폭 감소 | $2CD+9D^2/g$ |
| $C,d$ | 전체 내부 폭 증가 | $g(2Cd+9d^2)$ |
| $C,P$ | 비용에 맞추어 $d$ 조정 | 정수 폭 선택 필요 |

예를 들어 $C=256$에서 $g=1,d=64$와 $g=32,d=4$를 직접 비교하자. 후자는 내부 전체 폭이 128이므로 “폭 4인 블록”이라고만 부르면 실제 tensor를 잘못 이해하게 된다.[3,6]

$$
P_{1\times64}=2(256)(64)+9(64)^2=69{,}632,
$$

$$
P_{32\times4}=2(256)(128)+9(128)^2/32=70{,}144.
$$

두 값은 약 0.74% 차이이며, $56\times56$ 격자에서 후자는 219,971,584 MAC이다. 두 배 넓어진 내부 tensor와 강하게 줄어든 공간 채널 연결이 거의 같은 가중치 예산 안에서 교환된 셈이다. 이것이 ResNeXt를 단순한 폭 증가와 구별하는 정량적 내용이다. 이 구조 비교만으로 정확도 차이나 실행 시간 차이는 계산할 수 없다.

Pointwise 비용이 차지하는 비율도 설계에 중요하다. 같은 식에서 얻은 비율은 다음과 같다.

$$
\eta_{1\times1}
=\frac{2CD}{2CD+9D^2/g}
=\frac{2C}{2C+9d}.
$$

$C=256,d=4$이면 이 비율은 약 93.4%이다. 이때 가운데 grouped convolution을 더 줄여도 블록 전체의 절감 여지는 이미 작다. $1/g$라는 가운데 층의 절감률을 전체 블록에 적용하면 비용을 크게 과소평가한다. 또한 전체 폭 128의 중간 tensor는 폭 64보다 원소 수가 두 배이므로, 가중치 수가 비슷하다고 중간 activation 저장량도 같다고 볼 수 없다.

## 5. DenseNet의 feature 누적과 성장률

### (1) 덧셈과 concatenation의 차이

DenseNet은 이전 feature를 같은 좌표에 더하지 않고 별도의 채널로 유지한다. 하나의 dense block 입력을 $x_0$, $l$번째 층이 새로 만든 feature를 $x_l$, 층별 변환을 $H_l$이라 하자. $[\cdot]$는 채널 방향 concatenation이다.[4,5,11]

$$
x_l=H_l([x_0,x_1,\ldots,x_{l-1}]).
$$

한 block 안에서는 공간 크기를 일정하게 유지한다. 입력 채널 수를 $C_0$, 각 층이 추가하는 채널 수인 growth rate를 $k$, 층 수를 $L$이라 하면 다음과 같다. 여기의 한 층은 새 feature $k$개를 만드는 변환 한 개이며, bottleneck 안에 있는 개별 convolution 수와 구별한다.[4,5,11]

$$
C_l^{\rm in}=C_0+(l-1)k,
\qquad C_{\rm block}^{\rm out}=C_0+Lk.
$$

ResNet의 덧셈은 동일한 채널 공간을 갱신한다. DenseNet의 concatenation은 기존 좌표를 남겨 놓고 상태 공간을 확장한다. 그 결과 뒤의 층은 초기 feature를 별도의 채널 묶음으로 직접 입력받는다. 다만 “기존 feature 보존”은 이 연결 연산에 대한 설명이다. Transition이나 최종 분류기에서 압축된 뒤에도 원래 입력을 복원할 수 있다는 주장은 아니다.[4,5,11]

Gradient 관점에서도 두 연결의 차이를 간단히 도출할 수 있다. 새 feature 하나를 추가하는 누적 상태를 $z=[x,H(x)]$라 쓰면 다음 Jacobian은 직사각형이다. 이 식은 앞의 연결 정의에 chain rule을 적용한 결과이다.

$$
\frac{\partial z}{\partial x}
=\begin{bmatrix}I\\J_H\end{bmatrix},
\qquad
\nabla_x\mathcal L
=g_{\rm old}+J_H^{\mathsf T}g_{\rm new}.
$$

$g_{\rm old}$와 $g_{\rm new}$는 각각 $z$의 기존 채널 부분과 새 채널 부분에 대한 gradient이다. Identity 경로가 별도 좌표로 남아 있다는 것이 덧셈의 $I+J_F$와의 차이이다. 그러나 이후 손실이 기존 좌표를 사용하지 않으면 $g_{\rm old}$가 작을 수 있고, 역전파 합에서 상쇄도 가능하다. 연결이 많다는 이유만으로 손실까지의 모든 gradient가 커진다고 해석해서는 안 된다.

### (2) Growth rate와 block 비용

먼저 각 $H_l$을 BN–ReLU–$3\times3$ convolution으로 두는 plain dense block을 계수하자. 각 층은 입력 전체에서 $k$개 새 채널을 생성하므로 가중치 수는 $9kC_l^{\rm in}$이다. 이를 합하면 다음과 같다.[4,5]

$$
P_{\rm dense}=9k\sum_{l=1}^{L}[C_0+(l-1)k]
=9k\left(LC_0+\frac{kL(L-1)}2\right).
$$

Growth rate가 일정해도 입력 폭은 층마다 늘어나므로, block 가중치는 깊이 $L$에 대해 이차항을 갖는다. 출력 폭 $C_0+Lk$의 선형 증가와 가중치의 이차 증가를 혼동하면 안 된다. 동일 격자에서는 전체 MAC이 $HW P_{\rm dense}$이며, 앞쪽과 뒤쪽 층의 새 출력 폭은 같아도 뒤쪽 층이 더 많은 연산을 수행한다.

$C_0=64,k=32,L=6$인 예제의 각 층을 펼치면 다음과 같다. 모든 $3\times3$에 padding 1과 stride 1을 사용한다.

| 층 $l$ | 입력 채널 | 새 출력 채널 | Convolution 가중치 |
| --- | --- | --- | --- |
| 1 | 64 | 32 | 18,432 |
| 2 | 96 | 32 | 27,648 |
| 3 | 128 | 32 | 36,864 |
| 4 | 160 | 32 | 46,080 |
| 5 | 192 | 32 | 55,296 |
| 6 | 224 | 32 | 64,512 |
| 합계 | — | 최종 누적 256 | 248,832 |

마지막 층의 비용은 첫 층의 3.5배이다. $56\times56$ 격자에 놓은 block 전체는 780,337,152 MAC이다. 이때 출력 폭 256만 보고 외부 폭 256의 ResNet 블록 하나와 비교하면, 6회의 feature 생성과 하나의 residual 변환이라는 서로 다른 범위를 섞게 된다. 정량 비교에는 깊이의 단위와 비교할 subgraph를 함께 명시해야 한다.

### (3) Bottleneck의 절감 조건

DenseNet-B는 각 층의 $3\times3$ 앞에 $1\times1$ convolution을 두고 중간 폭을 $bk$로 만든다. $b$는 bottleneck 배수이며 흔히 사용하는 구성은 $b=4$이다. 두 convolution 앞에 각각 BN과 ReLU가 있으며, 그 구조는 독립 구현에서도 확인된다.[4,11]

$$
C_l^{\rm in}\ \xrightarrow{1\times1}\ bk
\ \xrightarrow{3\times3}\ k,
\qquad
P_{l,B}=bkC_l^{\rm in}+9bk^2.
$$

이 구조의 이름에 bottleneck이 포함되어 있어도 실제 $bk$가 현재 입력 폭보다 작다는 보장은 없다. 입력 폭이 작은 초기 층에서는 오히려 확장이며, 첫 pointwise의 추가 비용도 지불한다. $0<b<9$에서 plain 층보다 가중치·동일 격자 MAC이 작아지는 필요충분조건은 다음처럼 직접 유도된다.[4,11]

$$
bkC_l^{\rm in}+9bk^2<9kC_l^{\rm in}
\quad\Longleftrightarrow\quad
C_l^{\rm in}>\frac{9b}{9-b}k.
$$

$b=4$에서는 경계가 $7.2k$이다. 앞의 $k=32$ 예제라면 입력 폭이 230.4보다 커야 한다. 여섯 층의 최대 입력은 224이므로 이 block에서는 모든 층이 convolution 비용만으로는 더 비싸진다. BN 파라미터나 activation 저장량까지 포함한 다른 비용 지표의 경계는 별도로 계산해야 한다.

Block 전체의 bottleneck 비용과 비용 절감 조건은 입력 폭의 평균으로 쓸 수 있다. 다음 식은 각 층의 식을 합한 것으로, $\overline C_{\rm in}$은 arithmetic mean이다.

$$
P_{{\rm dense},B}
=bk\left(LC_0+\frac{kL(L-1)}2\right)+9bk^2L,
\qquad
\overline C_{\rm in}=C_0+\frac{k(L-1)}2.
$$

$$
P_{{\rm dense},B}<P_{\rm dense}
\quad\Longleftrightarrow\quad
\overline C_{\rm in}>\frac{9b}{9-b}k
\quad(0<b<9).
$$

같은 $C_0=64,k=32,b=4$에서 깊이만 바꾸면 다음 결과를 얻는다. 실제 DenseNet의 서로 다른 전체 모델 성능 비교가 아니라, 고정된 해상도에서 단일 block을 길게 만든 계수 실험이다.

| $L$ | 최종 채널 | Plain 가중치 | Bottleneck 가중치 | Bottleneck/plain |
| --- | --- | --- | --- | --- |
| 6 | 256 | 248,832 | 331,776 | 1.333 |
| 12 | 448 | 829,440 | 811,008 | 0.978 |
| 24 | 832 | 2,985,984 | 2,211,840 | 0.741 |

따라서 bottleneck은 넓은 입력을 반복해서 처리하는 뒤쪽 층에서 절감 효과가 커진다. 초반 몇 층이 더 비싸더라도 뒤쪽 절감이 이를 상쇄할 수 있으며, 전체 이득은 평균 입력 폭으로 판단한다. “Pointwise를 추가하면 언제나 가볍다”라는 설명 대신 이 경계식을 사용하면 작은 block과 깊은 block을 같은 원리로 해석할 수 있다.

### (4) Transition과 compression

Dense block 사이의 transition은 채널 혼합과 공간 축소를 담당한다. Compression factor를 $0<\theta\leq1$, 입력 채널을 $C$라 하면 $1\times1$ 출력 폭은 $C'=\lfloor\theta C\rfloor$이다. 그 뒤 $2\times2$, stride 2 average pooling으로 해상도를 줄인다. Bottleneck과 compression을 함께 쓰는 구성을 DenseNet-BC라 부른다.[4,11]

$$
C'=\lfloor\theta C\rfloor,
\qquad
P_{\rm trans}=CC',
\qquad M_{\rm trans}=HWCC'.
$$

Convolution이 pooling보다 먼저이므로 MAC에는 축소 전 $HW$가 들어간다. $56\times56\times256$을 $\theta=0.5$로 압축하면 가중치 32,768개, 102,760,448 MAC을 쓰고 pooling 뒤 출력은 $28\times28\times128$이다. Pooling이 먼저라고 잘못 세면 convolution 비용이 4분의 1로 축소된다.

같은 예제에서 pooling 뒤 출력 원소 수는 pooling 전 block 출력의 8분의 1이다. 채널 절반과 공간 면적 4분의 1이 곱해지기 때문이다. 하지만 $256\to128$의 pointwise 혼합은 차원 축소여서 모든 입력 채널을 독립적으로 보존할 수 없다. Dense block 내부의 feature 재사용 원리와 block 사이 압축의 정보 손실 가능성은 서로 다른 수준에서 설명해야 한다.

## 6. Dense 연결의 저장량과 측정

### (1) 고유 feature와 중간 복사본

DenseNet의 가중치 효율과 학습 메모리 효율은 같은 지표가 아니다. 고유한 convolution 출력은 층마다 $k$개씩 늘어나지만, 각 층에 입력할 누적 tensor와 그 BN 결과를 모두 따로 보관하면 저장량에 이차항이 생긴다. 원 논문의 메모리 분석과 Torchvision의 checkpoint 대상 연산을 함께 보면 이 차이를 확인할 수 있다.[11,12]

Batch 크기를 $N$, 원소당 저장 byte를 $q$라 하자. 입력 $x_0$와 각 새 feature만 한 번씩 보관하는 단순 저장 모형은 다음과 같다. 가중치, gradient, optimizer 상태, convolution workspace는 포함하지 않는다.

$$
A_{\rm unique}=NHW(C_0+Lk),
\qquad B_{\rm unique}=qA_{\rm unique}.
$$

반면 각 층에 전달되는 concatenation 입력을 중복 포함하여 모두 별도의 연속 tensor로 보관한다고 가정하면 다음과 같다. 이는 그 입력 복사본만의 합계이며 앞 식과 서로 다른 저장 대상을 센다.[11,12]

$$
A_{\rm copies}
=NHW\sum_{l=1}^{L}[C_0+(l-1)k]
=NHW\left(LC_0+\frac{kL(L-1)}2\right).
$$

$N=1,H=W=56,C_0=64,k=32,L=6,q=4$를 대입하면 고유 feature는 802,816개, 3,211,264 byte이다. 누적 입력 복사본은 2,709,504개, 10,838,016 byte이다. Mebibyte (MiB)를 $2^{20}$ byte로 정의하면 각각 3.0625 MiB와 10.3359375 MiB이다. 이 두 수치는 장치에서 측정한 peak memory가 아니며, 복사본이 실제로 언제까지 살아 있는지에 따라 동시에 필요한 메모리가 달라진다.

| 저장 대상 | 고정 $C_0,k,H,W$에서 $L$ 의존성 | 별도로 확인할 사항 |
| --- | --- | --- |
| 새 convolution feature와 block 입력 | 선형 | 원소 정밀도와 batch |
| 모든 누적 입력·BN 출력의 개별 보관 | 이차항 가능 | 복사·보존·재사용 정책 |
| Dense convolution 가중치 | 이차항 | Plain/B의 계수 차이 |
| 전체 학습 peak memory | 위 항들의 수명에 의존 | Gradient·optimizer·workspace |

따라서 “DenseNet 메모리는 본질적으로 모두 이차 증가한다”와 “효율적 구현이면 전체 메모리가 선형이다”는 모두 범위를 지나치게 넓힌 말이다. 고유 feature, 중간 activation, 파라미터를 분리하면 어느 항을 줄일 수 있는지 드러난다. 특히 bottleneck은 출력 폭을 제한해도 첫 $1\times1$가 점점 넓어지는 입력을 읽으므로 가중치의 이차항 자체는 남는다.[11,12]

### (2) 재계산과 비교 절차

Activation checkpointing은 backward에 필요한 중간 결과를 모두 저장하는 대신 일부를 다시 계산한다. 확인한 Torchvision DenseNet 구현에서는 누적 입력의 concatenation, 첫 BN·ReLU, 첫 $1\times1$를 포함하는 bottleneck 함수가 checkpoint 대상이다. 이 실행 그래프는 메모리 효율 구현의 재계산 원리와 일치하지만, 실제 절감량과 시간 증가는 구현·장치·batch에 따라 측정해야 한다.[11,12]

재계산은 이전 feature의 의미나 growth rate를 바꾸는 것이 아니라 중간 결과의 보관 방법을 바꾼다. 이에 비해 $k$나 $\theta$를 줄이는 것은 tensor 형상과 학습 가능한 함수 자체를 바꾸는 설계 변경이다. 메모리 부족을 해결할 때 이 두 조작을 같은 실험으로 묶으면 구조의 효과와 실행 전략의 효과를 구별하기 어렵다.

!!! info "[Measurement]"
    구조 비교에서는 입력 크기, batch, 정밀도, 학습·평가 모드, backend와 checkpoint 설정을 고정한다. 먼저 각 convolution의 실제 출력 형상으로 MAC을 합산하고, 같은 실행 범위에서 시간과 peak allocated memory를 측정한다. 같은 모형의 기준 실행을 base, 재계산 실행을 ckpt라 하고, 측정 메모리를 $B$, 반복당 시간을 $t$라 두면 절감률과 시간 비는 다음과 같다.

    $$
    r_B=1-\frac{B_{\rm ckpt}}{B_{\rm base}},
    \qquad r_t=\frac{t_{\rm ckpt}}{t_{\rm base}}.
    $$

    학습 시간에는 forward만 포함했는지 backward와 optimizer step까지 포함했는지 명시한다. 비동기 장치에서는 동일한 동기화 경계를 두고, 준비 실행 이후 반복값의 중앙값과 분산 범위를 보고한다. 위의 해석적 activation byte와 측정 peak memory는 별도 열에 기록한다.[13,14]

이 측정 절차는 비용식에서 생략한 항을 실제로 드러내기 위한 것이다. 예를 들어 ResNeXt에서는 pointwise 연산과 넓은 중간 tensor가, DenseNet에서는 누적 입력과 재계산이 중요해질 수 있다. MAC이 비슷한 구조를 비교하더라도 계산 그래프에서 어떤 tensor가 언제 생성되고 사용되는지 함께 확인해야 결과를 해석할 수 있다.[6,11,12]

## 7. 설계 원리의 요약

- ResNet은 identity에 residual을 더하는 표현을 사용한다. 정확한 $I+J_F$ 관계에는 identity shortcut과 합산 뒤 identity라는 조건이 필요하다.
- Bottleneck 비용은 외부 폭, 내부 폭, stride 위치로 결정된다. 같은 모델 이름이나 가중치 수만으로 MAC을 확정할 수 없다.
- ResNeXt의 cardinality는 경로 수이다. 전체 내부 폭을 고정하는 비교와 그룹당 폭을 고정하는 비교는 비용의 변화 방향이 다르다.
- DenseNet의 growth rate는 새 출력 폭이며 누적 입력 폭은 계속 증가한다. Bottleneck의 절감 여부는 입력 폭과 추가 pointwise 비용을 함께 계수해야 한다.
- DenseNet의 고유 feature, 중복 중간 activation, 가중치는 서로 다른 저장량 항이다. 재계산의 효과는 실행 설정을 고정하여 측정한다.

## 8. 참고문헌

1. K. He, X. Zhang, S. Ren, and J. Sun, “Deep Residual Learning for Image Recognition,” arXiv:1512.03385 (2015), §§1, 3, Fig. 5. [원문](https://arxiv.org/html/1512.03385v1).
2. A. Zhang, Z. C. Lipton, M. Li, and A. J. Smola, *Dive into Deep Learning*, “Residual Networks (ResNet) and ResNeXt,” §§8.6.1–8.6.5. [본문과 구현](https://d2l.ai/chapter_convolutional-modern/resnet.html).
3. S. Xie, R. Girshick, P. Dollár, Z. Tu, and K. He, “Aggregated Residual Transformations for Deep Neural Networks,” arXiv:1611.05431 (2017), §3, Fig. 3, Table 2. [원문](https://arxiv.org/html/1611.05431v2).
4. G. Huang, Z. Liu, L. van der Maaten, and K. Q. Weinberger, “Densely Connected Convolutional Networks,” arXiv:1608.06993 (2018 version), §3. [원문](https://arxiv.org/html/1608.06993v5).
5. A. Zhang, Z. C. Lipton, M. Li, and A. J. Smola, *Dive into Deep Learning*, “Densely Connected Networks (DenseNet),” §§8.7.1–8.7.3. [본문과 구현](https://d2l.ai/chapter_convolutional-modern/densenet.html).
6. Torchvision contributors, “torchvision.models.resnet,” `BasicBlock`, `Bottleneck`, `_make_layer`, 2026-09-21 확인. [구현](https://docs.pytorch.org/vision/main/_modules/torchvision/models/resnet.html).
7. PyTorch contributors, “BatchNorm2d,” *PyTorch 2.14 documentation*. [정규화 식과 훈련·평가 통계](https://docs.pytorch.org/docs/2.14/generated/torch.nn.BatchNorm2d.html).
8. A. Zhang et al., “Batch Normalization,” *Dive into Deep Learning*, §§8.5.2.4–8.5.3. [평가 통계와 독립 구현](https://d2l.ai/chapter_convolutional-modern/batch-norm.html).
9. K. He, X. Zhang, S. Ren, and J. Sun, “Identity Mappings in Deep Residual Networks,” arXiv:1603.05027 (2016), §§2–4. [원문](https://arxiv.org/html/1603.05027v3).
10. Keras contributors, “ResNet models for Keras,” v3.11.3, `residual_block_v1`, `residual_block_v2`. [구현](https://raw.githubusercontent.com/keras-team/keras/v3.11.3/keras/src/applications/resnet.py).
11. Torchvision contributors, “torchvision.models.densenet,” `_DenseLayer`, `_DenseBlock`, `_Transition`, 2026-09-21 확인. [구현](https://docs.pytorch.org/vision/main/_modules/torchvision/models/densenet.html).
12. G. Pleiss, D. Chen, G. Huang, T. Li, L. van der Maaten, and K. Q. Weinberger, “Memory-Efficient Implementation of DenseNets,” arXiv:1707.06990 (2017), §§2–4. [원문](https://arxiv.org/html/1707.06990v1).
13. PyTorch contributors, “PyTorch Benchmark,” *PyTorch Tutorials*, §§3–4. [준비 실행·동기화·반복 측정](https://docs.pytorch.org/tutorials/recipes/recipes/benchmark.html).
14. A. Zhang et al., “Asynchronous Computation,” *Dive into Deep Learning*, §13.2.1. [비동기 실행과 측정 예제](https://d2l.ai/chapter_computational-performance/async-computation.html).
