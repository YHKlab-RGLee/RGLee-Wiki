---
description: Depthwise 분해, inverted residual, channel shuffle과 compound scaling을 tensor 경로와 정확한 연산 비용으로 비교한다.
---

# CNN: Efficient architectures

Convolutional neural network (CNN)의 효율을 높이는 설계는 공간 필터링과 채널 혼합을 분리하고, 비선형 변환을 적용할 폭과 실제로 저장할 표현의 폭을 구별하며, 전체 네트워크의 깊이·폭·해상도를 함께 조정한다. MobileNet, ShuffleNet, EfficientNet은 이 선택을 서로 다른 수준에서 구체화한다. 이 글은 정확도 순위보다 각 선택이 바꾸는 연결 관계와 비용을 설명한다.[1,2,3,4,5,6,7,8]

기본 convolution과 비용 규약은 [CNN: Classic architectures](classic-cnn-architectures.md), residual 연결과 grouped convolution은 [CNN: Residual and dense architectures](residual-and-dense-cnn.md)을 따른다. Multiply-accumulate (MAC) 한 번을 곱셈과 누산 한 쌍으로 센다. Floating-point operation (FLOP)을 곱셈·덧셈 각각 한 번으로 세면 convolution의 산술량은 약 2 FLOP/MAC이다. 아래의 $P$는 convolution 가중치 수, $M$은 입력 하나의 convolution MAC이며 bias, 정규화, activation, 덧셈과 데이터 복사를 제외한다. 따라서 제시하는 계산 예는 해석적 계수이지 장치에서 측정한 실행 시간이나 정확도가 아니다.

## 1. 공간 필터링과 채널 혼합의 분리

### (1) Depthwise separable convolution

Depthwise separable convolution은 입력 채널마다 공간 필터를 적용하는 depthwise convolution과, 같은 위치의 채널들을 결합하는 $1\times1$ pointwise convolution의 연속이다. 입력 채널 수를 $C$, 출력 채널 수를 $D$, 정사각 커널의 한 변을 $k$, 출력 격자를 $H'\times W'$라 하자. 여기서는 입력 채널마다 depthwise 필터를 하나만 두는 depth multiplier 1을 사용한다.[1,2]

공간 위치 $(u,v)$에서 입력을 $x$, depthwise 출력을 $z$, 최종 출력을 $y$라 쓰면, stride 1에서 두 선형 연산은 다음과 같다. $a,b$는 커널 안의 공간 offset이며 경계에는 선택한 padding을 적용한다. $d_{ab c}$는 공간 가중치, $p_{oc}$는 pointwise 가중치이다.[1,2]

$$
z_{uvc}=\sum_{a,b}d_{ab c}x_{u+a,v+b,c},
\qquad y_{uvo}=\sum_{c=1}^{C}p_{oc}z_{uvc}.
$$

Depthwise 단계에는 서로 다른 채널 사이의 합이 없다. 채널 혼합은 두 번째 단계에서 처음 생긴다. 이 때문에 depthwise를 단독으로 적용한 층과 separable 블록 전체는 같은 연산이 아니다. 전자는 각 채널을 따로 변환하고, 후자는 그 결과를 모든 출력 채널로 전달할 수 있다. 실제 MobileNetV1은 두 convolution 뒤에 각각 batch normalization (BN)과 rectified linear unit (ReLU)을 배치한다. 따라서 위 식은 비용과 연결을 설명하는 선형 부분이며, 실제 블록 전체를 하나의 선형 convolution으로 합친 식은 아니다.[1,2]

두 단계 사이의 비선형성을 잠시 제외하면 합성 커널의 제한을 직접 유도할 수 있다. 일반 convolution의 가중치를 $K_{abco}$라 할 때 다음 관계를 만족해야 한다.

$$
K_{abco}=d_{ab c}p_{oc}.
$$

입력 채널 $c$를 하나 고정하여 $k^2$개의 공간 좌표와 $D$개의 출력 채널을 축으로 펼친 행렬은 rank가 최대 1이다. 즉 같은 입력 채널에서 여러 출력 채널로 전달되는 공간 패턴은 하나의 필터에 대한 배수로 제한된다. 임의의 일반 convolution 커널을 언제나 이 두 층으로 정확히 대체할 수 있다는 뜻은 아니다. 연산량 감소는 이 구조적 제한과 맞교환한 결과이며, 여러 블록과 비선형성을 쌓았을 때의 표현 능력은 별도 문제이다.

### (2) 가중치와 산술량

일반 convolution과 separable 블록이 같은 $C,D,k,H',W'$를 가진다고 하자. Depthwise에 stride를 적용하고 뒤의 pointwise는 같은 출력 격자에서 계산하면 다음 계수가 성립한다.[1,2]

$$
P_{\rm regular}=k^2CD,
\qquad M_{\rm regular}=H'W'k^2CD.
$$

$$
P_{\rm sep}=k^2C+CD,
\qquad M_{\rm sep}=H'W'(k^2C+CD).
$$

첫 항은 채널마다 $k^2$개인 공간 가중치, 둘째 항은 입력·출력 채널 쌍마다 하나인 혼합 가중치이다. 두 구현의 출력 격자가 같으므로 비용 비에서는 공간 크기와 입력 폭이 소거된다.

$$
\frac{M_{\rm sep}}{M_{\rm regular}}
=\frac{P_{\rm sep}}{P_{\rm regular}}
=\frac1D+\frac1{k^2}.
$$

$k=3$이고 $D$가 충분히 크면 비율은 $1/9$에 접근한다. 그러나 출력 채널이 적으면 $1/D$를 무시할 수 없다. $D=1$에서는 일반 convolution보다 depthwise 단계가 추가된 만큼 오히려 비싸다. 이는 “항상 9배 감소”라는 표현의 경계 조건이다. Pointwise가 전체에서 차지하는 비율도 같은 식으로부터 얻는다.

$$
\eta_{\rm pw}=\frac{CD}{k^2C+CD}=\frac{D}{k^2+D}.
$$

예를 들어 $56\times56$ 격자에서 $C=64,D=128,k=3$을 적용하면 다음과 같다. Padding 1, stride 1을 가정하며, 비교하는 것은 같은 입출력 형상을 가진 convolution 부분이다.

| 구성 | 가중치 $P$ | MAC $M$ |
| --- | --- | --- |
| 일반 $3\times3$ | 73,728 | 231,211,008 |
| Depthwise $3\times3$ | 576 | 1,806,336 |
| Pointwise $1\times1$ | 8,192 | 25,690,112 |
| Separable 합계 | 8,768 | 27,496,448 |

비용 비는 약 0.118924이고, separable 블록 안의 pointwise 비중은 약 93.43%이다. 공간 필터를 더 단순하게 만드는 방법의 절감 여지는 이 예에서 이미 작다. 반대로 채널 혼합을 줄이면 큰 비용 항을 건드리지만, 서로 다른 채널의 정보를 결합하는 방식도 바뀐다. 뒤의 ShuffleNet이 pointwise 연결 자체를 다루는 이유를 이 분해에서 읽을 수 있다.[5,6]

## 2. MobileNetV1의 폭과 해상도

### (1) 두 축의 서로 다른 비용 의존성

MobileNetV1은 첫 일반 convolution 뒤에 separable 블록들을 연결한다. Width multiplier $\alpha$는 내부 입력·출력 채널을 함께 줄이고, resolution multiplier $\rho$는 입력 영상의 두 공간 축을 줄인다. 실제 정수 채널과 격자 반올림을 무시한 내부 블록에서는 $C\to\alpha C$, $D\to\alpha D$, $H',W'\to\rho H',\rho W'$로 계산한다.[1,2]

$$
P(\alpha)=\alpha k^2C+\alpha^2CD,
\qquad
M(\alpha,\rho)=\rho^2H'W'(\alpha k^2C+\alpha^2CD).
$$

Depthwise 비용은 폭에 선형이고 pointwise 비용은 이차이다. 따라서 전체 비용이 정확히 $\alpha^2\rho^2$에 비례하는 것은 아니다. 위 식을 기준 블록의 비용으로 나누면, 어떤 근사를 사용했는지 더 명확하게 드러난다.

$$
\frac{M(\alpha,\rho)}{M(1,1)}
=\rho^2\frac{\alpha k^2+\alpha^2D}{k^2+D}.
$$

$\alpha D\gg k^2$이면 축소 후에도 pointwise가 지배하여 이차 근사가 유용하다. 폭을 매우 작게 만들면 depthwise 항이 상대적으로 커지므로 근사의 오차가 증가한다. 예를 들어 앞 절의 $C=64,D=128$ 블록에서 폭을 절반으로 줄이면 실제 가중치는 2,336개이고 MAC은 7,325,696이다. 비용 비 0.266423은 이차 근사의 0.25보다 크다. 축소 후 채널 혼합이 싸진 만큼 공간 필터링의 상대적 비중이 증가한 결과이다.

| $\alpha$ | $\rho$ | 입력→출력 폭 | 출력 격자 | MAC |
| --- | --- | --- | --- | --- |
| 1 | 1 | 64→128 | 56×56 | 27,496,448 |
| 0.5 | 1 | 32→64 | 56×56 | 7,325,696 |
| 1 | 0.5 | 64→128 | 28×28 | 6,874,112 |
| 0.5 | 0.5 | 32→64 | 28×28 | 1,831,424 |

이 예에서는 모든 축소값이 정수이므로 격자 반올림이 없다. 해상도만 절반으로 하면 가중치는 그대로이고 MAC만 4분의 1이 된다. 폭만 절반으로 하면 가중치와 동일 해상도 MAC이 같은 비율로 줄어든다. 두 조작은 같은 연산 예산에 도달하더라도 서로 다른 tensor를 만든다. 해상도 축소는 공간 표본 수를, 폭 축소는 위치마다 유지하는 feature 좌표 수를 줄인다.

### (2) 네트워크 끝단과 정수 경계

위의 이차 폭 법칙은 두 채널 축이 함께 변하는 내부 층의 성질이다. 영상의 입력 채널이 3으로 고정된 stem에서는 출력 폭만 변한다. 분류할 범주의 수를 $K$로 고정한 최종 선형 분류기에서도 입력 폭만 변한다. 따라서 내부 separable 블록의 식을 전체 네트워크의 모든 파라미터에 그대로 적용할 수 없다.[1,2]

$$
P_{\rm stem}=k^2(3)(\alpha D_0),
\qquad P_{\rm classifier}=(\alpha C_f)K.
$$

$D_0$는 기준 stem 출력 폭, $C_f$는 기준 분류기 입력 폭이다. Global average pooling을 거친 분류기는 공간 크기가 1이므로 해상도 배수도 이 가중치 수를 바꾸지 않는다. 반면 pooling까지 도달하기 전 각 convolution의 실제 출력 격자는 입력 해상도에 따라 달라진다. 이 항들을 따로 세면 작은 네트워크에서 내부 블록 바깥의 비용이 상대적으로 커지는 이유를 설명할 수 있다.

Dilation 1인 convolution에서 입력 높이 $H$, 각 측면의 padding $p$, stride $s$에 대한 출력 높이는 다음과 같다. 너비에도 같은 식을 적용한다.[9,10]

$$
H'=\left\lfloor\frac{H+2p-k}{s}\right\rfloor+1.
$$

예를 들어 $k=3,p=1,s=2$이면 입력 높이 28과 27은 모두 출력 높이 14가 된다. 입력 높이를 연속 배수로 바꾸더라도 중간 격자는 계단처럼 변한다. 해상도 배수 $\rho^2$는 각 축이 그 배수대로 바뀌는 이상화이며, 실제 모델 계수에서는 각 층의 정수 출력 형상을 사용해야 한다. 폭 역시 정수이어야 하므로 구현에 지정한 채널 배수와 반올림 규칙을 함께 기록한다.

## 3. MobileNetV2의 확장과 선형 압축

### (1) Inverted residual의 tensor 경로

MobileNetV2는 블록 사이에 좁은 표현을 전달하고, 블록 안에서 채널을 확장하여 변환한 뒤 다시 압축한다. 입력 폭 $C$, 출력 폭 $D$, expansion factor $t$, 내부 폭 $E=tC$라 하자. 정수 $E$가 확보된 $t>1$ 블록의 경로는 다음과 같다. $\operatorname{DW}$는 depthwise convolution을 뜻한다.[3,4]

$$
H\times W\times C
\xrightarrow{1\times1}
H\times W\times E
\xrightarrow{k\times k\ \operatorname{DW},\ s}
H'\times W'\times E
\xrightarrow{1\times1}
H'\times W'\times D.
$$

앞선 [ResNet bottleneck](residual-and-dense-cnn.md)에서는 넓은 외부 표현 사이에 좁은 내부 변환을 둔다. 여기서는 좁은 외부 표현 사이에 넓은 내부 변환을 두므로 inverted residual이라 부른다. Shortcut의 끝점은 확장된 $E$채널이 아니라 블록 입출력의 좁은 채널이다. 표준 블록에서는 stride 1이고 $C=D$일 때만 identity를 더한다.[3,4]

$$
y=\begin{cases}
x+F(x),&s=1\ \text{및}\ C=D,\\
F(x),&\text{그 밖의 경우}.
\end{cases}
$$

Expansion과 depthwise 뒤에는 BN과 ReLU6을, 마지막 projection 뒤에는 BN을 두고 activation을 추가하지 않는다. ReLU6은 $\min(\max(z,0),6)$이다. 이 마지막 activation 생략을 linear bottleneck이라 부른다. 이는 블록 전체가 선형이라는 뜻이 아니라, 압축된 출력 좌표에 다시 clipping을 적용하지 않는다는 구조적 명칭이다.[3,4]

정보 손실의 문제는 간단한 스칼라 예로 이해할 수 있다. 음수 두 값을 ReLU에 통과시키면 모두 0이 되어 원래 값의 구별이 사라진다. 반면 부호를 두 좌표에 나누는 다음 표현은 실수 $a$를 복원할 수 있다. 이는 넓은 표현에서 비선형성을 적용하는 동기를 보여 주는 해석적 예이며, 학습한 MobileNetV2가 항상 이 부호 표현를 만든다는 주장은 아니다.

$$
h(a)=[\max(a,0),\max(-a,0)],
\qquad a=h_1(a)-h_2(a).
$$

폭을 넓혔다는 사실만으로 정보 보존이 보장되지는 않는다. Expansion 가중치와 데이터가 만드는 부분공간, activation의 포화, projection의 차원 축소가 모두 관계한다. 논문의 저차원 표현에 대한 동기는 압축 단계에서 불필요한 비선형 절단을 피하는 설계 이유로 해석하는 것이 적절하다. 여기서는 그 동기와 실제 구현에서 projection activation이 없는 사실을 구분한다.[3,4]

### (2) Stride 위치와 비용

Expansion은 축소 전 격자에서 실행되고 depthwise와 projection은 축소 후 격자에서 실행된다. 따라서 convolution 비용은 세 항의 공간 면적을 구별해야 한다. 다음 식은 expansion이 존재하고 bias를 제외한 경우에 정확하다.[3,4]

$$
P_{\rm inv}=CE+k^2E+ED=E(C+k^2+D).
$$

$$
M_{\rm inv}=HWCE+H'W'(k^2E+ED).
$$

Stride 1, 동일 격자에서는 $M=HWP$로 줄어들지만, stride 2에서는 첫 항만 원래 면적에 남는다. 같은 입력 격자와 채널을 가진 두 블록을 비교하고 공간 면적비를 $r_s=H'W'/(HW)$라 두면 다음과 같다.

$$
\frac{M_s}{M_{s=1}}
=\frac{C+r_s(k^2+D)}{C+k^2+D}.
$$

$28\times28\times32$ 입력에서 $E=192,D=32,k=3$을 사용하자. Stride 2의 출력은 $14\times14\times32$이고, shortcut은 사용하지 않는다. Stride 1과 2의 가중치 수는 모두 14,016개이다.

| 단계 | 가중치 | Stride 1 MAC | Stride 2 MAC |
| --- | --- | --- | --- |
| Expansion 32→192 | 6,144 | 4,816,896 | 4,816,896 |
| Depthwise, 폭 192 | 1,728 | 1,354,752 | 338,688 |
| Projection 192→32 | 6,144 | 4,816,896 | 1,204,224 |
| 합계 | 14,016 | 10,988,544 | 6,359,808 |

면적이 4분의 1로 줄어도 전체 MAC 비는 약 0.578767이다. 첫 expansion을 함께 4분의 1로 세면 비용을 크게 과소평가한다. 또한 폭 32의 일반 $3\times3$ convolution 하나는 같은 격자에서 가중치 9,216개, 7,225,344 MAC이다. Inverted 블록이 그 한 층보다 비싸다는 계산은 모순이 아니다. 비교 대상은 확장·비선형 변환·projection을 포함한 블록과 단일 층이며 함수의 구성 자체가 다르다.

$t=1$에서는 확인한 표준 구현이 expansion convolution을 생략한다. 이때 첫 항 $C^2$를 남겨 두면 존재하지 않는 층을 계수하게 된다.[3,4]

$$
P_{t=1}=k^2C+CD,
\qquad M_{t=1}=H'W'(k^2C+CD).
$$

### (3) 좁은 경계와 넓은 중간 activation

외부 경계가 좁다는 사실과 모든 중간 tensor가 작다는 사실은 구별해야 한다. Batch 크기를 $N$, 원소당 byte를 $q$라 하면 expansion 출력 하나의 원소 수와 저장량은 다음과 같다. 가중치, gradient와 workspace는 포함하지 않는다.

$$
A_{\rm expand}=NHWE,
\qquad B_{\rm expand}=qNHWE.
$$

앞 예에서 $N=1,q=4$이면 입력은 25,088개 원소이고 expansion 출력은 150,528개 원소이다. 후자를 독립 배열로 보관하면 602,112 byte가 필요하다. 블록 사이에 전달하는 폭 32와 내부에서 사용하는 폭 192를 혼동하면 이 저장량을 놓친다. Stride 2도 expansion 이전의 해상도를 줄이지 않으므로 이 중간 tensor의 형상은 두 경우에 동일하다.

MobileNetV2 논문은 확장 tensor 전체를 한 번에 저장하지 않는 실행 전략도 논의한다. 그러나 고수준 코드에서 층을 연결했다는 사실만으로 그런 실행이 자동 보장되지는 않는다. 확인한 Torchvision 구현은 expansion, depthwise, projection을 별도 모듈로 표현한다. 실제 전체 tensor의 생성 여부와 수명은 실행 backend의 fusion·분할 전략에 따라 확인해야 한다.[3,4]

## 4. ShuffleNet의 채널 연결과 실행 구조

### (1) Grouped pointwise와 channel shuffle

ShuffleNetV1은 pointwise convolution까지 그룹으로 나누어 채널 혼합 비용을 줄인다. 입력과 출력 폭을 $C,D$, 그룹 수를 $g$라 하면 각 그룹은 $C/g$개의 입력을 $D/g$개의 출력으로 연결한다. 두 폭은 $g$로 나누어떨어져야 한다.[5,6]

$$
P_{\rm gpw}=\frac{CD}{g},
\qquad M_{\rm gpw}=HW\frac{CD}{g}.
$$

그룹 구분을 바꾸지 않은 채 여러 층을 쌓으면 한 출력 그룹이 이전의 같은 그룹에서만 정보를 받는다. Channel shuffle은 채널 순서를 바꾸어 다음 grouped convolution이 서로 다른 이전 그룹의 feature를 입력받게 한다. 채널 수 $C=gn$을 그룹 축 $g$와 그룹당 채널 축 $n$으로 펼친 뒤 두 축을 전치하고 다시 평탄화한다.[5,6]

$$
(N,C,H,W)\to(N,g,n,H,W)
\to(N,n,g,H,W)\to(N,C,H,W).
$$

예를 들어 $g=2,n=3$이면 입력 순서 $[0,1,2,3,4,5]$는 $[0,3,1,4,2,5]$가 된다. 다음 층이 연속한 세 채널씩 묶으면 첫 그룹은 이전 두 그룹 모두에서 입력을 받는다. 다만 하나의 shuffle을 거쳤다고 각 출력이 곧바로 모든 입력 채널의 임의 선형결합이 되는 것은 아니다. 한 층에서 섞이는 범위는 채널 수와 그룹 크기로 제한된다.

이 차이는 채널 하나의 위치에서 permutation matrix $\Pi$와 grouped pointwise 행렬 $W_1,W_2$를 써서 표현할 수 있다. $W_1,W_2$는 각각 block diagonal 구조이며, 비선형성을 생략한 채널 연결은 다음과 같다.

$$
y=W_2\Pi W_1x.
$$

$\Pi$는 학습한 가중치가 아니라 순서를 바꾸는 고정 행렬이다. 따라서 채널 간의 값 결합은 여전히 $W_1,W_2$가 담당한다. Shuffle에 convolution MAC을 부과하지 않더라도 tensor의 실제 배치를 바꾸는 비용은 남을 수 있다. 확인한 구현은 전치 뒤 `contiguous()`를 사용한다.[6,8]

V1의 일반 stride 1 블록은 grouped pointwise 압축, shuffle, depthwise, grouped pointwise 복원 뒤 shortcut과 덧셈을 수행한다. 내부 폭을 $C_b$라 하고 입출력 폭이 $C$이면 convolution 가중치는 다음과 같다. 첫 stage의 첫 압축에서 일반 pointwise를 사용하는 예외는 이 식에서 제외한다.[5,6]

$$
P_{\rm shuffle1}=\frac{2CC_b}{g}+k^2C_b.
$$

예를 들어 $C=240,C_b=60,g=3,k=3$이면 가중치는 10,140개이며, $g=1$로 동일 폭을 유지하면 29,340개이다. 절감 대상은 두 pointwise 항이고 depthwise 항은 그대로이다. Stride 2 블록에서는 shortcut 쪽에 average pooling을 적용하고 변환 경로와 채널 방향으로 연결한다. 따라서 외부 출력 폭이 $D$라면 변환 경로의 최종 폭은 $D-C$이다. 덧셈 블록의 마지막 폭을 그대로 쓰면 downsampling 블록의 형상과 비용을 모두 잘못 세게 된다.[5,6]

### (2) ShuffleNetV2의 split과 concatenation

ShuffleNetV2는 일반 stride 1 블록의 입력 채널을 절반으로 나누고 한쪽은 identity로 유지한다. 나머지 절반에 일반 pointwise–depthwise–일반 pointwise를 적용한 뒤 두 경로를 concatenation하고 두 그룹 shuffle을 수행한다. 여기의 두 pointwise는 각 변환 경로 안에서 dense하게 연결되며 V1의 grouped pointwise와 다르다.[7,8]

$$
x=[x_a,x_b],\qquad y=\operatorname{shuffle}_2([x_a,F(x_b)]).
$$

입출력 폭 $C$가 같고 짝수이며 두 경로 폭이 각각 $C/2$일 때 convolution 비용은 다음과 같다. Identity 경로와 shuffle은 이 MAC에 포함하지 않는다.

$$
P_{\rm shuffle2}=2\left(\frac C2\right)^2+k^2\frac C2,
\qquad M_{\rm shuffle2}=HWP_{\rm shuffle2}.
$$

$C=116,k=3$이면 변환 경로의 폭은 58이고 가중치는 7,250개이다. $28\times28$ 격자에서는 5,684,000 MAC이다. 전체 폭 116에 세 convolution을 적용하는 비용으로 계산해서는 안 된다. 다음 블록에서는 shuffle된 결과를 다시 나누므로, 이번에 identity로 지나간 feature 일부도 이후 변환 경로에 들어갈 수 있다. 이러한 이동은 채널 좌표를 보존한 단순 identity 반복과 구별된다.[7,8]

Stride 2에서는 입력을 반으로 나누어 한 경로를 그대로 통과시킬 수 없다. 두 경로 모두 공간을 축소해야 한다. 확인한 구조에서 첫 경로는 전체 입력의 depthwise와 pointwise이고, 둘째 경로는 전체 입력의 pointwise, depthwise, pointwise이다. 각 경로의 최종 폭은 $D/2$이다.[7,8]

| 경로 | 축소 전 연산 | 축소 후 연산 | 최종 폭 |
| --- | --- | --- | --- |
| 첫 경로 | — | Depthwise $C$; pointwise $C\to D/2$ | $D/2$ |
| 둘째 경로 | Pointwise $C\to D/2$ | Depthwise $D/2$; pointwise $D/2\to D/2$ | $D/2$ |

표의 depthwise는 입력의 큰 격자를 읽지만 출력 위치마다 MAC을 수행하므로 축소 후 면적으로 센다. 둘째 경로의 첫 pointwise만 축소 전 면적에서 실행된다. 이를 합하면 다음 계수이다.

$$
M_{\rm shuffle2,s2}
=HW\frac{CD}{2}
+H'W'\left(k^2C+\frac{CD}{2}+\frac{k^2D}{2}+\frac{D^2}{4}\right).
$$

$C=116,D=232$이고 입력 격자가 $28\times28$, 출력이 $14\times14$이면 첫 pointwise는 10,549,504 MAC, 축소 뒤 항의 합은 5,684,000 MAC이다. 합계는 16,233,504 MAC이다. 같은 stage의 stride 1 블록 비용을 단순히 면적비로 환산하면 두 전체입력 경로와 채널 증가를 놓친다.

### (3) 메모리 접근 모형과 고정 조건

ShuffleNetV2가 강조한 효율은 convolution 산술량만으로 결정되지 않는다. 이를 이해하기 위해 모든 입력·출력 원소와 가중치를 각각 한 번만 읽거나 쓴다는 단순 접근 모형을 세우자. 원 논문은 충분한 cache를 가정하며 메모리 접근 비용에 MAC이라는 약어를 사용한다. 이 글에서는 곱셈·누산과 혼동하지 않도록 접근 원소 수를 $Q$로 쓴다.[7,8]

$H\times W$ 격자의 일반 pointwise에서 다음 식은 그 가정 아래의 접근량이다. 원소당 byte가 $q$이면 대응하는 byte 수는 $qQ$이다.

$$
Q=HW(C+D)+CD,
\qquad M=HWCD.
$$

격자와 산술 예산 $M$을 고정하면 $CD=M/(HW)$가 고정된다. 양수 $C,D$에 대한 산술·기하평균 부등식으로 다음 하한을 직접 얻는다.

$$
Q\geq2\sqrt{HWM}+\frac{M}{HW},
\qquad \text{등호 조건: }C=D.
$$

이는 입출력 폭이 같을 때 실제 장치에서 언제나 가장 빠르다는 정리가 아니다. 단순 접근 모형에서 같은 곱 $CD$를 만드는 두 폭의 합이 최소라는 결과이다. 예를 들어 $HW=784$에서 $C=D=128$과 $C=64,D=256$은 모두 12,845,056 MAC이다. 전자의 $Q$는 217,088개, 후자는 267,264개이다. 연산량은 같지만 읽고 쓸 activation의 합이 달라지는 사례이다.

Grouped pointwise에서도 같은 모형을 적용하면 다음과 같다. 첫째 등식은 폭을 고정한 비교, 둘째 등식은 $M$과 입력 폭 $C$를 고정하여 출력 폭을 조정하는 비교를 구별하는 데 유용하다.[7,8]

$$
Q_g=HW(C+D)+\frac{CD}{g}
=HWC+\frac{Mg}{C}+\frac{M}{HW}.
$$

$C,D$를 고정하고 $g$만 늘리면 가중치 접근과 MAC은 줄고 activation 항은 그대로이다. 반면 $C,M$을 고정하면 $D=Mg/(HWC)$가 증가하여 activation 접근량이 늘어난다. 따라서 “그룹 수가 많으면 메모리 접근이 늘어난다”는 설명에는 고정한 예산이 반드시 따라야 한다. V1의 같은 폭 비교와 V2의 같은 산술 예산 비교는 서로 모순되는 주장이 아니다.

실제 cache가 부족하거나 tensor가 여러 번 복사되면 위 모형보다 많은 접근이 필요하다. 작은 연산을 여러 경로로 나누는 fragmentation, activation과 덧셈, concatenation, shuffle 역시 convolution MAC 바깥에서 시간을 사용한다. 원 논문의 실행 분석과 구현 그래프, 독립적인 PyTorch 측정 예제는 이런 항을 따로 확인해야 함을 뒷받침한다. 효과의 크기와 유리한 구조는 장치 및 실행 설정에 따라 달라진다.[7,8,11]

## 5. EfficientNet의 블록과 compound scaling

### (1) Mobile inverted bottleneck과 채널 재가중

EfficientNet의 기본 구성은 mobile inverted bottleneck convolution (MBConv)과 squeeze-and-excitation (SE)이다. MBConv는 앞서 설명한 expansion–depthwise–projection 경로를 사용하며, SE는 depthwise 출력에 대해 영상 전체의 공간 정보를 모아 채널별 배율을 만든다. EfficientNet-B0에는 $3\times3$과 $5\times5$ depthwise 블록이 포함된다.[12,13]

Depthwise 뒤의 tensor를 $U\in\mathbb R^{H'\times W'\times E}$라 하자. SE의 squeeze는 각 채널의 공간 평균 $z_c$를 만든다. 이는 위치를 구별하는 feature map을 한 채널당 하나의 값으로 요약하는 연산이다.[14,15]

$$
z_c=\frac1{H'W'}\sum_{u=1}^{H'}\sum_{v=1}^{W'}U_{uvc}.
$$

중간 squeeze 폭을 $S$, 첫 채널 변환을 $W_s\in\mathbb R^{S\times E}$, 둘째를 $W_e\in\mathbb R^{E\times S}$라 하자. Bias를 $a,b$, 중간 activation을 $\delta$, sigmoid를 $\sigma$라 쓰면 excitation과 재가중은 다음과 같다.[14,15]

$$
v=\sigma\bigl(W_e\delta(W_sz+a)+b\bigr),
\qquad \widetilde U_{uvc}=v_cU_{uvc}.
$$

$v$는 입력 영상에 따라 달라지지만 같은 채널 안에서는 모든 위치에 동일하게 적용된다. 따라서 SE는 공간 위치마다 다른 가중치를 만드는 연산과 구별된다. 또한 $v$를 계산하는 두 채널 변환은 다른 채널의 평균을 함께 사용하므로 depthwise 필터처럼 채널별로 독립인 연산이 아니다. 입력 전체의 요약이 국소 feature의 채널 배율에 영향을 주는 경로가 생긴다.[14,15]

원래 SE 모듈의 대표 구성은 중간 ReLU를 쓰지만, 확인한 EfficientNet 구현은 sigmoid linear unit (SiLU)을 사용한다. SiLU는 $\operatorname{SiLU}(z)=z\sigma(z)$이며 MBConv의 expansion과 depthwise 뒤에도 쓰인다. Projection 뒤에는 activation을 추가하지 않는다. 따라서 MobileNetV2의 ReLU6을 사용하는 블록과 EfficientNet의 MBConv를 완전히 동일한 연산으로 취급하면 안 된다.[3,4,13,16,17]

두 SE 채널 변환의 가중치·bias 수와 MAC을 별도로 세면 다음과 같다. 공간 pooling과 원소별 재가중은 이 MAC에서 제외한다.

$$
P_{\rm SE}=2ES+S+E,
\qquad M_{\rm SE,linear}=2ES.
$$

두 변환은 이미 $1\times1$이 된 공간에서 실행되므로 $H'W'$를 곱하지 않는다. 반면 채널 배율을 전체 tensor에 적용하는 곱셈 수는 $H'W'E$이며, pooling도 공간 원소를 읽어 합산해야 한다. SE 비용이 작다는 표현을 사용할 때에도 작은 채널 변환과 전체 feature에 대한 접근을 구별해야 한다.

확인한 Torchvision EfficientNet 구현은 $S=\max(1,\lfloor C/4\rfloor)$로 두며 여기의 $C$는 expansion 이전 블록 입력 폭이다. $E/4$가 아니라는 점이 중요하다. $C=32,E=192$이면 $S=8$이고, SE 가중치와 bias는 3,272개, 두 채널 변환은 3,072 MAC이다. $S=48$로 잘못 잡으면 중간 폭이 여섯 배가 된다. 이 수치는 해당 구현의 폭 규칙을 대입한 계산이며 원 저자 구현의 기본 SE 비율 0.25와도 일치한다.[13,16]

### (2) 깊이·폭·해상도의 공동 조정

Compound scaling은 기준 블록의 종류를 유지하면서 stage 반복 수, 채널 폭, 입력 해상도를 함께 바꾸는 방법이다. 깊이 배수를 $d$, 폭 배수를 $w$, 해상도 배수를 $r$라 하고, 세 증가율 상수를 $a_d,a_w,a_r$, 자원 증가를 제어하는 계수를 $\phi$라 쓰자. MobileNet의 width multiplier $\alpha$와 혼동하지 않도록 원 논문의 세 상수 기호를 이와 같이 구별한다.[12,13]

$$
d=a_d^\phi,\qquad w=a_w^\phi,\qquad r=a_r^\phi,
\qquad a_d,a_w,a_r\geq1.
$$

기준 반복 구조의 일반 convolution만 생각하면 입력·출력 채널에 각각 $w$, 공간의 두 축에 각각 $r$, 반복 수에 $d$가 곱해진다. 채널·격자·반복 수를 연속 변수로 보는 이상화에서 산술량 배수는 다음과 같다.[12,13]

$$
\frac{M_{\rm regular}(d,w,r)}{M_{\rm regular}(1,1,1)}
=dw^2r^2
=(a_da_w^2a_r^2)^\phi.
$$

EfficientNet은 이 마지막 밑을 약 2로 맞추는 방식으로 자원 증가를 배분한다. 이 관계는 정확도에 대한 법칙이 아니다. 어느 비율이 좋은지는 기준 구조와 학습 문제에 의존하고, 식 자체는 정한 확장 규칙에서의 비용을 설명한다. 특히 깊이 증가로 추가하는 블록은 stage 첫 downsampling 블록의 복제가 아니라 같은 출력 형상을 유지하는 반복 블록이므로, 실제 네트워크의 총비용은 개별 block을 펼쳐 합해야 한다.[12,13]

Depthwise convolution은 입력과 출력 채널이 독립적인 두 축으로 곱해지지 않는다. 폭이 $w$배가 되면 독립 필터 수도 $w$배가 된다. 따라서 같은 이상화에서 다음과 같다.

$$
\frac{M_{\rm dw}(d,w,r)}{M_{\rm dw}(1,1,1)}=dwr^2.
$$

기준 MBConv들의 pointwise MAC 합을 $M_{\rm pw,0}$, depthwise MAC 합을 $M_{\rm dw,0}$라 하고 expansion 비율과 상대적 격자를 유지하면 convolution 부분의 연속 근사는 다음과 같다.

$$
M_{\rm conv}(d,w,r)
\approx dr^2\left(w^2M_{\rm pw,0}+wM_{\rm dw,0}\right).
$$

이 식의 근사는 stage 경계, 정수 반복과 반올림을 평균적인 확대 배수로 표현한 데서 온다. 반면 한 개의 고정된 블록에서 채널과 격자가 정확히 그 배수대로 변한다면 각 항의 대수적 의존성은 정확하다. SE의 두 채널 변환은 $E$와 $S$가 모두 폭과 함께 증가할 때 대략 $dw^2$에 비례하지만 공간 평균 뒤에 있으므로 $r^2$가 붙지 않는다. 재가중과 pooling 항은 공간 원소 수에 의존한다.

| 비용 항 | 연속 확대 배수 | 전제 |
| --- | --- | --- |
| 일반·pointwise convolution | $dw^2r^2$ | 두 채널 축 모두 확대 |
| Depthwise convolution | $dwr^2$ | Depth multiplier 유지 |
| SE의 두 채널 변환 | 약 $dw^2$ | $E,S$가 같은 비율로 확대 |
| Feature tensor 하나의 원소 수 | $wr^2$ | 같은 상대적 stage 위치 |
| 고정 범주 수의 분류기 가중치 | $w$ | 최종 입력 폭만 확대 |

예를 들어 $a_d=1.2,a_w=1.1,a_r=1.15$를 선택한 연속 계산에서 $\phi=1$이면 일반 convolution 배수는 1.92027, depthwise 배수는 1.7457이다. 둘 다 정확히 2가 아니다. 같은 계수를 적용해도 비용 항의 구성 비율에 따라 전체 증가율이 달라진다. 이 예는 주어진 숫자의 대수적 결과이며, 특정 EfficientNet 체크포인트의 실제 MAC을 대신하지 않는다.

### (3) 정수 반올림과 stage별 차이

실제 네트워크의 채널 수와 반복 수는 정수이다. Torchvision의 EfficientNet 설정은 채널을 8의 배수로 조정하고 stage 반복은 올림한다. 기준 stage 반복 수를 $L_i$라 하면 확대 후 반복 수는 다음과 같다. 같은 규칙을 모든 stage에 적용해도 상대적 증가율은 같지 않다.[12,13,16]

$$
L'_i=\lceil dL_i\rceil.
$$

$d=1.2$일 때 반복 수가 1인 stage는 2가 되어 두 배이고, 4인 stage는 5가 되어 1.25배이다. 적은 반복 수를 가진 stage에서 올림의 상대적 영향이 더 크다. 따라서 전체 깊이 증가를 단일 실수 배수로 표현한 식은 구체적 네트워크의 반복 수를 생성하는 규칙과 구별해야 한다.

정수 격자의 영향을 분리해서 보기 위해, 다음 계산 예에서는 양수 목표 폭 $v$를 가장 가까운 8의 배수로 반올림하고 최소폭을 8로 제한하는 규칙 $R$을 정의한다. 중간값은 위쪽 배수로 보낸다. 이는 정수화의 불연속성을 설명하기 위한 예시 규칙이며, 특정 EfficientNet 구현의 채널 보정 규칙을 재현하는 식은 아니다.

$$
R(v)=\max\left(8,8\left\lfloor\frac{v+4}{8}\right\rfloor\right).
$$

| 기준 폭 $C$ | 목표 $v=1.1C$ | 예시 폭 $R(v)$ | 예시 배수 |
| --- | --- | --- | --- |
| 16 | 17.6 | 16 | 1.000 |
| 24 | 26.4 | 24 | 1.000 |
| 32 | 35.2 | 32 | 1.000 |
| 40 | 44.0 | 48 | 1.200 |

이 예시의 네 기준 폭에 같은 배수 1.1을 지정해도 반올림 결과는 균일하게 증가하지 않는다. 표는 특정 체크포인트의 stage 채널 목록이 아니다. 실제 모델에서는 해당 구현의 최소폭과 보정 규칙까지 지정해야 하며, “폭을 10% 늘렸다”고만 기록하면 재현할 tensor 형상이 정해지지 않는다.

실제 비용 계산에서는 먼저 반올림된 stage별 입출력 폭과 반복 수를 확정하고, 각 stage의 첫 stride와 이후 stride 1 블록을 나눈다. 다음으로 입력 해상도에서 실제 격자를 순차 계산한 뒤 각 convolution의 MAC을 합한다. SE와 stem·head는 앞에서 구분한 별도 항으로 추가한다. 이 순서를 따르면 연속 근사와 정확한 정수 네트워크 계수가 어느 부분에서 달라졌는지 추적할 수 있다.[12,13]

## 6. 산술량과 실제 추론의 비교

### (1) 비교 지표와 실행 범위

효율 비교에는 가중치 수, MAC, activation 저장량과 지연 시간을 분리한 기록이 필요하다. 앞 절의 수식들은 실행 그래프에 포함된 convolution의 크기를 설명한다. 실제 지연 시간에는 convolution 외 연산과 호출·데이터 이동도 들어가므로, MAC 비를 그대로 시간 비로 바꾸는 것은 측정되지 않은 가정이다. ShuffleNetV2의 실행 분석과 독립적인 PyTorch benchmark 예제는 연산 분할과 실행 설정에 따라 이런 차이가 생김을 보여 준다.[7,11]

비교할 네트워크를 A와 B라 하고 측정 지연 시간을 $T_A,T_B$, convolution MAC을 $M_A,M_B$라 하자. 다음 두 비는 별도로 기록한다. 모두 같은 입력·batch·정밀도·측정 범위를 사용해야 한다.

$$
R_M=\frac{M_B}{M_A},
\qquad R_T=\frac{T_B}{T_A}.
$$

$R_M<1$이고 $R_T>1$인 결과가 나와도 계수식의 오류라고 곧바로 결론낼 수 없다. 예를 들어 grouped 연산이 작은 작업들로 실행되거나 shuffle에서 데이터 복사가 추가되면, 적은 convolution MAC과 긴 실행 시간이 함께 나타날 수 있다. 반대로 fusion이 중간 tensor의 읽기·쓰기를 줄이면 고수준 그래프에 표시된 경계가 실제 실행에서는 사라질 수 있다. 이런 설명은 가능한 원인이며, 해당 실험의 원인을 확정하려면 실제 실행 연산과 시간을 확인해야 한다.[7,8,11]

| 지표 | 계산·측정 대상 | 이 글의 식에서 빠진 대표 항 |
| --- | --- | --- |
| Convolution 가중치 $P$ | 커널 원소 | Bias, BN, SE bias |
| Convolution MAC $M$ | 출력 위치별 곱셈·누산 | Activation, pooling, shuffle |
| Tensor byte | 지정한 배열의 원소 수×정밀도 | 수명 중첩, workspace |
| 추론 지연 시간 $T$ | 지정한 입력에서 완료까지 | 측정 범위 밖의 전처리·전송 |

가중치 수는 입력 해상도를 낮춰도 변하지 않을 수 있지만, activation과 convolution MAC은 줄어든다. 반대로 SE의 작은 채널 변환은 가중치를 추가하면서도 매우 작은 공간에서 실행된다. 이런 구조가 섞인 전체 모델을 “작다”라는 한 단어로 비교하면 어느 자원이 줄었는지 불분명해진다. 특히 모델 파일 크기와 실제 실행 중 peak memory는 서로 다른 저장 대상을 포함한다.

### (2) 재현 가능한 측정 절차

측정 전에 구조와 구현을 고정한다. 모델 이름만 쓰지 말고 입력 해상도, 폭 배수, 실제 채널 수, expansion 비율, stage 반복, stride 위치, SE 폭을 남긴다. 각 층의 실제 출력 형상으로 비용을 합한 결과를 먼저 확보하면, 실행 시간을 해석할 때 어떤 연산 경로가 달라졌는지 확인할 수 있다. 앞의 MobileNetV2 stride 예와 ShuffleNetV2 downsampling 예는 이 절차가 필요한 최소 사례이다.[3,4,7,8,13]

실행 기록에는 장치, 소프트웨어 버전, backend, 정밀도, batch, 스레드 수와 추론 실행 범위를 명시한다. 입력의 장치 전송과 전처리를 포함할지 먼저 정하고 모든 모델에 같은 경계를 적용한다. 동일한 모델도 스레드 설정에 따라 상대적인 속도가 달라질 수 있으므로, 사용할 환경의 설정을 유지하여 비교한다.[11,18]

비동기 장치에서는 호출 반환 시점과 계산 완료 시점이 다를 수 있다. 준비 실행을 수행한 뒤, 측정 경계에서 대상 연산이 완료되도록 동기화하고 반복 측정값을 수집한다. PyTorch의 benchmark 도구는 준비 실행과 필요한 동기화를 처리하며, 독립 교재의 비동기 실행 예제도 완료 대기 없이 잰 시간이 실제 연산 시간을 나타내지 않을 수 있음을 보여 준다.[11,18]

반복 측정에서는 중앙값과 산포를 함께 기록하고, 최초 초기화 시간은 정상 상태의 반복 추론과 구별한다. 모델 전체의 지연 시간을 먼저 비교한 뒤 차이가 큰 경우에만 연산별 측정으로 원인을 좁힌다. 개별 연산 시간의 단순 합은 fusion이나 호출 순서가 다른 전체 실행의 시간을 대신하지 못하므로, 전체 모델과 연산별 분석의 범위를 분명히 남긴다.[7,11]

정확도까지 비교할 때에는 같은 데이터와 평가 절차로 확인한 값을 비용 지표에 연결해야 한다. 이 글의 해석적 예는 특정 구조가 더 정확하다는 결과를 제공하지 않는다. 예를 들어 일반 convolution 한 층과 inverted 블록은 입력·출력 형상이 같아도 내부 비선형성과 채널 경로가 다르다. 비용이 낮은 쪽을 먼저 찾은 뒤 같은 함수라고 가정하기보다, 필요한 표현과 실행 자원의 조건을 함께 평가해야 한다.

## 7. 설계 원리의 요약

- Depthwise separable convolution은 공간 필터와 채널 혼합을 분리한다. 절감 비율은 $1/D+1/k^2$이며 pointwise 비용이 남는다.
- MobileNetV1의 폭 축소는 depthwise에는 선형, pointwise에는 이차로 작용한다. 해상도 축소와 폭 축소는 서로 다른 tensor 축을 바꾼다.
- MobileNetV2는 좁은 경계 사이에서 넓은 변환을 수행한다. Stride 2에서도 expansion은 큰 격자에 남으며, $t=1$에서는 생략된 층을 제외해야 한다.
- ShuffleNetV1은 grouped pointwise와 permutation을, V2는 split·identity·일반 pointwise 경로를 사용한다. 같은 산술 예산과 같은 폭의 비교는 메모리 접근에 서로 다른 조건이다.
- EfficientNet의 compound scaling은 여러 자원 축을 함께 조정한다. Depthwise·SE·정수 반올림 때문에 전체 비용이 정확한 $dw^2r^2$ 법칙을 따르지는 않는다.
- 실제 효율은 완성된 tensor 경로를 계수한 뒤 동일 실행 조건에서 측정한다. MAC, 저장량과 지연 시간은 각각의 의미를 유지하여 보고한다.

## 8. 참고문헌

1. A. G. Howard et al., “MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications,” arXiv:1704.04861 (2017), §§3.1–3.4, Table 1. [원문](https://arxiv.org/html/1704.04861v1).
2. PyTorchCV contributors, “MobileNet” and “Convolution blocks,” `MobileNet`, `get_mobilenet`, `DwsConvBlock`, 2026-09-21 확인. [모델 구현](https://raw.githubusercontent.com/osmr/pytorchcv/master/pytorchcv/models/mobilenet.py), [Depthwise·pointwise 구현](https://raw.githubusercontent.com/osmr/pytorchcv/master/pytorchcv/models/common/conv.py).
3. M. Sandler, A. Howard, M. Zhu, A. Zhmoginov, and L.-C. Chen, “MobileNetV2: Inverted Residuals and Linear Bottlenecks,” arXiv:1801.04381 (2019 version), §§3–5, Table 1. [원문](https://arxiv.org/html/1801.04381v4). TensorFlow authors, `expanded_conv`, 2026-09-21 확인. [원 저자 expansion 조건](https://raw.githubusercontent.com/tensorflow/models/master/research/slim/nets/mobilenet/conv_blocks.py).
4. Torchvision contributors, “torchvision.models.mobilenetv2,” `InvertedResidual`, `MobileNetV2`, 2026-09-21 확인. [구현](https://docs.pytorch.org/vision/main/_modules/torchvision/models/mobilenetv2.html).
5. X. Zhang, X. Zhou, M. Lin, and J. Sun, “ShuffleNet: An Extremely Efficient Convolutional Neural Network for Mobile Devices,” arXiv:1707.01083 (2017), §§3.1–3.2. [원문](https://arxiv.org/html/1707.01083v2).
6. Jaxony and contributors, “ShuffleNet in PyTorch,” `channel_shuffle`, `ShuffleUnit`, 2026-09-21 확인. [독립 구현](https://raw.githubusercontent.com/jaxony/ShuffleNet/master/model.py).
7. N. Ma, X. Zhang, H.-T. Zheng, and J. Sun, “ShuffleNet V2: Practical Guidelines for Efficient CNN Architecture Design,” arXiv:1807.11164 (2018), §§2–3. [원문](https://arxiv.org/html/1807.11164v1).
8. Torchvision contributors, “torchvision.models.shufflenetv2,” `channel_shuffle`, `InvertedResidual`, 2026-09-21 확인. [구현](https://docs.pytorch.org/vision/main/_modules/torchvision/models/shufflenetv2.html).
9. PyTorch contributors, “Conv2d,” *PyTorch 2.14 documentation*, Shape. [출력 형상](https://docs.pytorch.org/docs/2.14/generated/torch.nn.Conv2d.html).
10. A. Zhang, Z. C. Lipton, M. Li, and A. J. Smola, “Padding and Stride,” *Dive into Deep Learning*, §7.3, Eq. (7.3.2). [Padding·stride와 출력 형상](https://d2l.ai/chapter_convolutional-neural-networks/padding-and-strides.html).
11. PyTorch contributors, “PyTorch Benchmark,” *PyTorch Tutorials*, §§3–4. [준비 실행·동기화·반복 측정](https://docs.pytorch.org/tutorials/recipes/recipes/benchmark.html).
12. M. Tan and Q. V. Le, “EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks,” *Proceedings of Machine Learning Research* 97, 6105–6114 (2019), §§3–4. [원문](https://proceedings.mlr.press/v97/tan19a/tan19a.pdf).
13. Torchvision contributors, “torchvision.models.efficientnet,” `MBConvConfig`, `MBConv`, `_efficientnet_conf`, 2026-09-21 확인. [구현](https://docs.pytorch.org/vision/main/_modules/torchvision/models/efficientnet.html).
14. J. Hu, L. Shen, S. Albanie, G. Sun, and E. Wu, “Squeeze-and-Excitation Networks,” arXiv:1709.01507 (2019 version), §III. [원문](https://arxiv.org/html/1709.01507v4).
15. Torchvision contributors, “torchvision.ops.misc,” `SqueezeExcitation`, 2026-09-21 확인. [구현](https://docs.pytorch.org/vision/main/_modules/torchvision/ops/misc.html).
16. TensorFlow authors, “EfficientNet model and builder,” `MBConvBlock`, `round_filters`, `_DEFAULT_BLOCKS_ARGS`, `swish`, 2026-09-21 확인. [원 저자 모델 구현](https://raw.githubusercontent.com/tensorflow/tpu/master/models/official/efficientnet/efficientnet_model.py), [기본 SE 비율과 activation](https://raw.githubusercontent.com/tensorflow/tpu/master/models/official/efficientnet/efficientnet_builder.py).
17. PyTorch contributors, “SiLU,” *PyTorch 2.14 documentation*. [함수 정의](https://docs.pytorch.org/docs/2.14/generated/torch.nn.SiLU.html).
18. A. Zhang, Z. C. Lipton, M. Li, and A. J. Smola, “Asynchronous Computation,” *Dive into Deep Learning*, §13.2.1. [비동기 실행과 완료 대기](https://d2l.ai/chapter_computational-performance/async-computation.html).
