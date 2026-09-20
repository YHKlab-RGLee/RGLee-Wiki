---
description: LeNet에서 AlexNet, VGG, Inception으로 이어지는 CNN 설계를 연결 구조, 수용영역, 파라미터와 연산량으로 비교한다.
---

# CNN: Classic architectures

Convolutional neural network (CNN)의 고전적 계보는 **국소 연결을 얼마나 넓게, 깊게, 여러 경로로 조합할 것인가**라는 설계 문제로 읽을 수 있다. LeNet은 공간적으로 공유하는 필터와 축소된 표현을 연결하고, AlexNet은 이 구조에 더 많은 채널과 층을 배치한다. Visual Geometry Group (VGG) 모델은 작은 필터의 반복을 일정한 블록으로 정리하며, Inception은 서로 다른 공간 범위의 경로를 병렬로 계산한다. 이 문서는 각 구조를 이름이나 발표 성적 순으로 나열하기보다, 출력 하나를 계산하는 비용에서 시작해 이러한 선택의 이득과 제약을 유도한다. 아래 수치는 별도 표시가 없으면 지정한 구조에 대한 직접 계산값이며, 학습 정확도를 재현한 실험 결과가 아니다.

## 1. Convolution의 연결 구조와 계산 규약

### (1) 출력 형상과 공유 가중치

입력의 높이와 너비를 $H,W$, 입력·출력 채널 수를 $C_{\mathrm{in}},C_{\mathrm{out}}$이라 한다. 한 이미지에 적용하는 정사각 필터의 한 변은 $k$, stride는 $s$, 한쪽 padding은 $p$로 쓴다. 아래에서는 dilation을 사용하지 않으며, 바깥 영역은 0으로 채운다. 딥러닝 라이브러리의 convolution은 보통 필터를 뒤집지 않는 cross-correlation으로 정의된다. 입력 $X$, 가중치 $K$, 출력 채널 $o$의 bias $b_o$에 대해 출력 $Y$는 다음과 같다.[1,2]

$$
Y_{o,u,v}=b_o+\sum_{c=1}^{C_{\mathrm{in}}}
\sum_{a=0}^{k-1}\sum_{b=0}^{k-1}
K_{o,c,a,b}X_{c,su+a-p,sv+b-p}.
$$

여기서 $u,v$는 출력 위치이며, $a,b$는 필터 내부 위치이다. 같은 $K$가 모든 $u,v$에 쓰이므로 출력의 공간 크기가 커져도 가중치 수는 증가하지 않는다. 반면 각 위치에서 내적을 다시 계산하므로 연산량은 출력 면적에 비례한다. **가중치 공유는 저장량의 절감이며, 모든 위치의 계산을 한 번만 수행한다는 뜻은 아니다.** 이 구별이 LeNet의 파라미터 효율과 VGG의 큰 연산량을 함께 설명한다.[1,2]

출력 높이 $H_o$와 너비 $W_o$는 완전히 들어맞는 필터 위치만 취하는 다음 규약으로 정한다. 문헌에서 padding을 양쪽 합계로 정의하기도 하므로, 식에 대입하기 전에 $2p$와 총 padding을 구별해야 한다.[1,3]

$$
H_o=\left\lfloor\frac{H+2p-k}{s}\right\rfloor+1,
\qquad
W_o=\left\lfloor\frac{W+2p-k}{s}\right\rfloor+1.
$$

예를 들어 $H=W=32,k=5,s=1,p=0$이면 출력은 $28\times28$이다. $k=3,s=1,p=1$이면 입력 해상도를 유지한다. 이 두 선택은 각각 아래 LeNet 예제의 공간 축소와 VGG 블록 내부의 해상도 유지에 대응한다. 나누어떨어지지 않는 경우에도 위 식의 바닥함수로 출력은 정의되지만, 좌우 가장자리에 남는 영역과 중심 정렬이 대칭인지는 별도로 확인해야 한다.[1,3]

채널을 $g$개의 서로 겹치지 않는 그룹으로 나누면 출력 채널 하나는 $C_{\mathrm{in}}/g$개의 입력 채널만 본다. $g$는 두 채널 수를 모두 나누는 정수이며, 일반적인 dense convolution은 $g=1$이다. 학습하는 가중치 수 $P_w$와 bias를 포함한 파라미터 수 $P$는 다음과 같이 직접 셀 수 있다.[1,2]

$$
P_w=k^2\frac{C_{\mathrm{in}}C_{\mathrm{out}}}{g},
\qquad P=P_w+C_{\mathrm{out}}.
$$

이 식에서 그룹을 늘리면 비용은 줄어들지만 채널 사이의 직접 연결도 줄어든다. 따라서 그룹 수가 다른 두 모델의 파라미터 차이를 단순한 구현 최적화로 해석하면 안 된다. 특히 원래 AlexNet의 일부 층은 채널이 두 묶음으로 분리되므로, 모든 층을 dense convolution으로 바꾼 교육용 구현과 비용이 다르다.[1,4]

### (2) 연산량과 메모리

Multiply–accumulate (MAC)는 하나의 곱을 누산하는 연산으로 센다. 이 문서는 이미지 한 장의 forward에서 convolution과 fully connected 층의 내적만 집계한다. Bias 덧셈, activation, pooling, 정규화, 입력 전처리는 MAC 합계에 포함하지 않는다. Floating-point operation (FLOP)은 곱셈과 덧셈을 각각 한 번으로 세는 규약을 사용하므로 내적 중심 추정값은 약 $2\,\mathrm{MAC}$이다. 이 환산은 측정 규약이며 특정 하드웨어의 명령어 개수에 대한 주장이 아니다. 내적 길이를 $L=k^2C_{\mathrm{in}}/g$라 하면 출력 하나가 $L$ MAC을 사용하므로 다음 식을 얻는다.[1,2]

$$
M_{\mathrm{conv}}=H_oW_oP_w
=H_oW_ok^2\frac{C_{\mathrm{in}}C_{\mathrm{out}}}{g}.
$$

길이 $D_{\mathrm{in}}$의 벡터를 $D_{\mathrm{out}}$차원으로 바꾸는 fully connected (FC) 층에서는 공간 재사용이 없다. 같은 내적 계산 규칙을 적용하면 다음과 같다.[2,5]

$$
P_{w,\mathrm{FC}}=D_{\mathrm{in}}D_{\mathrm{out}},
\qquad M_{\mathrm{FC}}=D_{\mathrm{in}}D_{\mathrm{out}}.
$$

따라서 convolution은 같은 가중치를 여러 위치에 사용하여 가중치당 MAC이 많고, FC 층은 이미지 한 장당 가중치를 한 번 사용한다. 이것만으로도 파라미터가 가장 많은 층과 연산량이 가장 큰 층이 달라질 수 있음을 알 수 있다. 예를 들어 $56\times56$ 출력, $C_{\mathrm{in}}=C_{\mathrm{out}}=64$, $k=3$, $g=1$인 층의 직접 계산은 다음과 같다.[1,2]

$$
P_w=9\cdot64^2=36{,}864,
\qquad M=56^2\cdot36{,}864=115{,}605{,}504.
$$

이 층은 약 $0.116$ billion MAC, 위 규약에서는 약 $0.231$ billion FLOP이다. $10^6$과 $10^9$를 각각 million과 billion으로 사용한다. 동일한 가중치를 유지한 채 높이와 너비를 두 배로 늘리면 공간 위치는 네 배가 되어 MAC도 네 배가 된다. 이 관계는 채널과 필터, stride를 고정한 비교에만 적용한다.

저장 공간도 파라미터와 activation을 분리해야 한다. Batch size를 $B$, 스칼라 하나의 저장 바이트 수를 $q$라 하면, 한 층의 가중치·bias와 출력 tensor를 담는 데 필요한 순수 데이터 바이트 수는 다음과 같다.[5,6]

$$
S_{\mathrm{param}}=qP,
\qquad S_{\mathrm{out}}=qBH_oW_oC_{\mathrm{out}}.
$$

이는 실제 peak memory가 아니다. 여러 층의 출력이 동시에 살아 있을 수 있고, 학습에는 gradient와 optimizer 상태가 추가되며, backend는 별도 workspace를 사용할 수 있다. $B$를 키우면 파라미터 저장량은 그대로인 반면 activation 저장량은 커진다. 따라서 모델 파일이 작다는 사실만으로 큰 batch를 처리할 수 있다고 결론 내릴 수 없다.[5,6]

### (3) 이론적 수용영역과 입력 간격

Receptive field는 한 출력이 의존할 수 있는 입력 영역이다. 단일 경로에서 $l$번째 층의 이론적 수용영역 한 변을 $r_l$, 인접 출력 중심 사이의 입력 좌표 간격을 $j_l$이라 한다. 입력에서는 $r_0=j_0=1$이다. 필터 크기 $k_l$, stride $s_l$인 convolution 또는 pooling에 대해 다음 재귀식을 사용한다.[7,8]

$$
j_l=s_lj_{l-1},
\qquad r_l=r_{l-1}+(k_l-1)j_{l-1}.
$$

두 번째 식의 의미는 인접한 입력 feature 중심 사이 간격 $j_{l-1}$을 $k_l-1$번 더해 새 출력의 공간 범위를 얻는다는 것이다. Padding은 출력 중심과 실제 이미지가 겹치는 영역을 바꾸지만, 위에서 세는 잠재적 범위의 크기에는 직접 들어가지 않는다. 가장자리 출력의 일부 범위는 실제 이미지가 아니라 padding에 걸릴 수 있다.[3,7]

다음은 stride 1의 $3\times3$ convolution 두 개와 $2\times2$, stride 2 pooling을 잇는 직접 계산이다. 작은 필터를 반복해도 범위가 넓어지는 과정과, pooling이 이후 층의 입력 간격을 바꾸는 과정을 구별할 수 있다.

| 단계 | $k,s$ | $r_l$ | $j_l$ |
| --- | --- | ---: | ---: |
| 입력 | — | 1 | 1 |
| 첫 convolution | $3,1$ | 3 | 1 |
| 둘째 convolution | $3,1$ | 5 | 1 |
| Pooling | $2,2$ | 6 | 2 |
| 다음 convolution | $3,1$ | 10 | 2 |

위 표는 연결 가능 범위만 계산한다. 실제 입력에 대한 출력의 민감도는 가중치와 activation에 의존한다. 출력 스칼라 $y$에 대한 입력 위치의 영향은 예를 들어 $|\partial y/\partial X_{c,u,v}|$로 조사할 수 있으며, 이 값이 큰 영역과 이론적 수용영역 전체는 같을 필요가 없다. 이 구별 때문에 수용영역을 이미지보다 크게 만들었다는 사실만으로 장거리 정보를 충분히 활용한다고 주장할 수 없다.[7,8]

## 2. LeNet의 공간 공유와 분류기

### (1) 원형과 교육용 계산 모형

LeNet에서 이어지는 핵심 구조는 국소 필터로 feature map을 만들고, 공간 해상도를 줄인 뒤, 여러 feature를 결합하여 분류하는 흐름이다. 원래 LeNet-5의 [Fig. 2](https://vitalab.github.io/papers/lecun-98.pdf#page=7)는 $32\times32$ 입력과 $6,16,120,84$의 중간 폭을 표시한다. 독립 교재의 실행 구현은 이 흐름을 현대의 convolution·pooling·linear 연산으로 단순화한다. 원문 그림의 Gaussian 출력 연결과 교재의 linear 출력만 비교해도 두 모델이 완전히 동일하지 않음을 확인할 수 있다.[9,10]

아래 계산 모형은 **$32\times32$ 단일 채널 입력, padding 없는 $5\times5$ convolution 두 개, 파라미터 없는 평균 pooling, 모든 입력 채널을 연결하는 convolution, $120\to84\to10$ FC 분류기**로 정의한다. 이는 형상과 비용을 설명하기 위한 LeNet 계열 예제이며 원래 LeNet-5의 정확한 파라미터 총수로 인용하지 않는다. 교재의 $28\times28$ 입력에 첫 층 padding 2를 주는 방식은 같은 첫 출력 형상을 만들지만, 입력 경계 조건까지 같은 것은 아니다.[1,9,10]

| 단계 | 출력 형상 | bias 제외 가중치 | MAC |
| --- | --- | ---: | ---: |
| Convolution 1 | $28\times28\times6$ | 150 | 117,600 |
| 평균 pooling | $14\times14\times6$ | 0 | 집계 제외 |
| Convolution 2 | $10\times10\times16$ | 2,400 | 240,000 |
| 평균 pooling | $5\times5\times16$ | 0 | 집계 제외 |
| FC 1 | 120 | 48,000 | 48,000 |
| FC 2 | 84 | 10,080 | 10,080 |
| 출력 FC | 10 | 840 | 840 |

첫 convolution에서 출력 하나는 $5\times5$ 영역의 25개 값만 받는다. 공간적으로 공유되는 6개 필터가 전체 $28\times28\times6$ 출력을 만든다. 이와 달리 같은 수의 출력을 만드는 완전 연결 변환을 가정하면 각 출력은 1,024개 입력과 별도 가중치로 연결된다. 두 구조의 가중치 수 비교는 다음과 같다.[1,2]

$$
P_{w,\mathrm{local}}=25\cdot6=150,
\qquad
P_{w,\mathrm{dense}}=32^2(28^2\cdot6)=4{,}816{,}896.
$$

이 비교는 두 모델의 정확도가 같다는 뜻이 아니다. 국소 연결과 공간 공유라는 제약을 넣으면 어떤 자유도를 제거하는지 수량화한 것이다. 완전 연결 변환은 위치마다 독립적인 관계를 학습할 수 있지만, 공유 필터는 여러 위치에서 동일한 패턴 검출 규칙을 사용한다. 따라서 절약된 파라미터와 도입한 구조적 가정을 함께 설명해야 한다.[1,2]

### (2) 공간 축소 이후의 병목

두 번의 pooling을 통과한 $5\times5\times16$ tensor를 펼치면 길이는 400이다. 첫 FC 층의 가중치 수만 48,000이므로, 이 작은 모델에서도 분류기 쪽이 저장량을 지배한다. 반면 convolution 2는 가중치가 2,400개뿐이어도 이를 100개 위치에서 사용하여 240,000 MAC을 수행한다. 앞 절에서 구별한 저장량과 계산량이 실제로 다른 층에 집중되는 예이다.[1,2,10]

$$
P=61{,}706,
\qquad M_{\mathrm{conv+FC}}=416{,}520.
$$

$P$는 표의 가중치에 각 convolution과 FC의 bias를 더한 값이며, $M$은 표에서 집계한 내적만의 합계이다. 평균 계산이나 sigmoid의 비용까지 포함한 전체 프로그램 연산량으로 해석하지 않는다. 또 마지막 $5\times5\times16$ 입력 전체를 보는 120개 FC 출력은 이 입력 크기에서는 $5\times5$, $16\to120$ convolution의 단일 공간 출력으로도 표현할 수 있다. 입력 해상도를 바꾸면 convolution은 여러 위치에 적용될 수 있으므로, 이러한 동등성은 지정한 입력 형상에 묶여 있다.[1,2,10]

같은 구조의 수용영역을 추적하면 두 번째 pooling 출력에서 $r=16,j=4$이다. 그 위에 공간 전체를 받는 $5\times5$ convolution 해석을 적용하면 $r=16+4\cdot4=32$가 된다. 아래 표는 32픽셀 입력을 끝에서 어떻게 포괄하는지 보여 주는 직접 계산이다.[7,9]

| 단계 | $r$ | $j$ |
| --- | ---: | ---: |
| 첫 $5\times5$ convolution | 5 | 1 |
| 첫 $2\times2$ pooling | 6 | 2 |
| 둘째 $5\times5$ convolution | 14 | 2 |
| 둘째 $2\times2$ pooling | 16 | 4 |
| $5\times5$ 전체 결합 | 32 | 4 |

## 3. AlexNet의 깊이와 자원 배분

### (1) 큰 입력과 채널 분할

AlexNet은 convolution 5개와 FC 3개를 연결하고, 앞쪽의 큰 필터에서 뒤쪽의 $3\times3$ 필터로 이동한다. 중요한 변화는 층 수만이 아니다. 채널 폭, activation, 데이터 증강과 분류기의 정규화가 함께 바뀐다. 원 논문의 [Fig. 2와 §3.5](https://proceedings.neurips.cc/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf#page=5)와 독립 교재 구현은 큰 구조를 공유하지만, 교육용 구현은 원래의 분할 연결 등을 단순화하므로 이름만으로 같은 계산 그래프라고 가정할 수 없다.[4,11]

다음 수치 예제는 채널 폭 $96,256,384,384,256$을 사용하고, convolution 2·4·5를 $g=2$로 둔다. 이것은 원문에서 같은 graphics processing unit (GPU)에 놓인 feature map끼리 연결하는 구성을 group convolution으로 계수한 것이다. 입력 크기는 **$227\times227$과 첫 층 padding 0**으로 명시하여 첫 출력을 55로 맞춘다. 원문 본문은 224 입력을 기술하고, 다른 구현은 padding을 조정한다. 이 예제의 227을 원문의 유일한 입력 규약으로 소급하지 않는다.[1,4,5]

| 층 | $k,s,g$ | convolution 출력 | MAC (million) |
| --- | --- | --- | ---: |
| Conv 1 | $11,4,1$ | $55\times55\times96$ | 105.415 |
| Conv 2 | $5,1,2$ | $27\times27\times256$ | 223.949 |
| Conv 3 | $3,1,1$ | $13\times13\times384$ | 149.520 |
| Conv 4 | $3,1,2$ | $13\times13\times384$ | 112.140 |
| Conv 5 | $3,1,2$ | $13\times13\times256$ | 74.760 |

Conv 1·2·5 뒤에 $3\times3$, stride 2 max pooling을 두며, Conv 2에는 padding 2, Conv 3–5에는 padding 1을 둔다. 따라서 최종 pooling 뒤 형상은 $6\times6\times256$이다. 표의 값은 이 조건을 앞의 MAC 식에 대입한 결과이다. 예를 들어 Conv 2에서는 출력 채널 하나가 96개 전체가 아니라 48개 입력 채널에 연결된다.[1,4]

$$
M_2=27^2\cdot25\cdot(96/2)\cdot256
=223{,}948{,}800.
$$

그룹을 제거하고 같은 입출력 폭을 유지하면 이 층의 가중치와 MAC은 정확히 두 배가 된다. 그러나 연결 가능한 채널 쌍도 늘어나므로, 이것은 동일 모델의 실행 장치만 바꾸는 조작과 다르다. 반대로 그룹이 있다고 출력 폭을 다시 절반으로 세면 비용을 이중으로 줄이는 오류가 생긴다. $C_{\mathrm{out}}=256$은 두 그룹의 출력을 합친 수이다.

### (2) FC 저장량과 activation

최종 공간 출력을 펼친 길이는 $6\cdot6\cdot256=9{,}216$이다. 뒤의 $9{,}216\to4{,}096\to4{,}096\to1{,}000$ 분류기는 다음과 같이 계수된다.[4,11]

$$
P_{w,\mathrm{FC}}=
9{,}216\cdot4{,}096+4{,}096^2+4{,}096\cdot1{,}000
=58{,}621{,}952.
$$

앞 표와 이 분류기를 합친 직접 계산값은 다음과 같다. Bias는 파라미터 수에만 포함한다.

$$
P=60{,}965{,}224,
\qquad M_{\mathrm{conv+FC}}=724{,}406{,}816.
$$

FC는 전체 가중치의 약 96%를 차지하지만, 집계한 MAC의 약 8%만 차지한다. 이 구조에서는 분류기를 줄이는 조작이 모델 저장량을 크게 낮출 수 있어도 convolution 계산을 같은 비율로 줄이지는 않는다. 반대로 앞쪽 feature map의 해상도를 줄이면 많은 convolution MAC을 줄일 수 있지만, 세부 공간 정보를 처리하는 방식도 변한다. 비용의 위치를 파악한 다음 어느 정보를 유지할지 결정해야 한다.[1,4,6]

입력 스칼라 $\xi$에 대한 rectified linear unit (ReLU)은 $f(\xi)=\max(0,\xi)$인 activation이다. Sigmoid $\sigma(\xi)$와의 중요한 수학적 차이는 양의 구간에서 activation 자체의 미분이 감쇠하지 않는다는 점이다. 두 미분을 나란히 쓰면 다음과 같다.[4,11]

$$
\sigma'(\xi)=\sigma(\xi)(1-\sigma(\xi)),
\qquad
f'(\xi)=\begin{cases}0,&\xi<0,\\1,&\xi>0.\end{cases}
$$

ReLU의 $\xi=0$은 미분 불가능한 지점이다. 양의 구간의 미분이 1이라는 사실도 여러 층을 통과한 전체 gradient가 항상 안정적이라는 보장은 아니다. 전체 derivative에는 가중치 행렬과 다른 activation의 미분이 함께 곱해진다. 따라서 깊이 증가의 효과를 ReLU 하나로 환원하거나, 원 논문의 학습 결과를 임의의 optimizer와 입력 전처리에서도 유지되는 성질로 해석하면 안 된다.[4,11]

AlexNet 계열을 비교할 때는 dropout과 데이터 증강을 구조와 구별해 기록해야 한다. Dropout을 사용하는 학습 과정과 비활성화한 추론 그래프는 계산 경로의 의미가 다르며, crop이나 반전은 모델이 접하는 입력 분포를 바꾼다. 이 때문에 더 낮은 오류가 관측되었다는 사실만으로 채널 폭이나 층 수의 인과적 효과를 식별할 수 없다. 한 요인의 효과를 보려면 나머지 학습·평가 조건을 고정한 비교가 필요하다.[4,6,11]

## 4. VGG의 작은 필터와 반복 블록

### (1) 깊이와 공간 범위의 교환

VGG의 설계는 $3\times3$, stride 1 convolution을 여러 번 적용한 뒤 pooling으로 해상도를 줄이는 것이다. 블록 안에서는 padding 1로 형상을 유지하므로, 공간 크기 감소와 비선형 변환 횟수를 따로 조절할 수 있다. 이 원리는 원 논문의 구성표와 독립 구현의 반복 블록에서 직접 확인할 수 있다.[12,13,14]

모든 층의 채널을 $C$로 고정하고 bias를 제외하면, $5\times5$ 한 층과 $3\times3$ 두 층은 같은 이론적 수용영역을 가지면서 가중치 수가 다르다. $7\times7$과 $3\times3$ 세 층도 같은 방식으로 비교한다.[12,14,15]

$$
P_{5\times5}=25C^2,
\qquad P_{3\times3\times2}=18C^2,
\qquad \frac{P_{3\times3\times2}}{P_{5\times5}}=\frac{18}{25}.
$$

$$
P_{7\times7}=49C^2,
\qquad P_{3\times3\times3}=27C^2,
\qquad \frac{P_{3\times3\times3}}{P_{7\times7}}=\frac{27}{49}.
$$

여기서 $3\times3\times2$와 $3\times3\times3$은 공간 3차원 필터가 아니라 각각 두 층과 세 층의 직렬 연결을 뜻한다. $C=64$인 직접 예제에서는 $5\times5$의 102,400개 가중치가 두 작은 층의 73,728개로 줄어든다. $7\times7$의 200,704개는 세 작은 층의 110,592개와 비교된다. 공간 해상도도 모든 층에서 같다면 MAC 비도 위 파라미터 비와 같다.

다만 수용영역이 같다고 두 변환이 같은 함수는 아니다. 작은 층 사이에 ReLU를 넣으면 입력에 따라 활성 경로가 달라지는 비선형 합성이 된다. 비선형을 제거하더라도 중간 채널 폭이 제한된 필터 합성은 임의의 큰 convolution과 동일한 매개화가 아니다. 따라서 이 비교의 결론은 **같은 잠재적 공간 범위를 더 적은 가중치와 더 많은 변환 단계로 다룰 수 있다**는 것이며, 모든 학습 과제에서 더 정확하거나 더 빠르다는 결론은 아니다.[12,14,15]

### (2) VGG-16의 단계별 비용

VGG-16은 원 논문의 configuration D에 해당한다. Convolution 개수는 블록별 $2,2,3,3,3$이고 출력 채널은 $64,128,256,512,512$이다. 아래는 입력 $224\times224\times3$, 각 블록 끝의 $2\times2$ max pooling, 그리고 bias 없는 가중치 집계로 직접 계산한 값이다. 독립 구현의 `cfgs["D"]`가 동일한 반복 수와 채널 폭을 제공한다.[12,13]

| 블록 | convolution 출력 해상도 | 반복 수·출력 채널 | 가중치 (million) | MAC (billion) |
| --- | --- | --- | ---: | ---: |
| 1 | $224\times224$ | $2,64$ | 0.038592 | 1.936392 |
| 2 | $112\times112$ | $2,128$ | 0.221184 | 2.774532 |
| 3 | $56\times56$ | $3,256$ | 1.474560 | 4.624220 |
| 4 | $28\times28$ | $3,512$ | 5.898240 | 4.624220 |
| 5 | $14\times14$ | $3,512$ | 7.077888 | 1.387266 |

블록 3과 4는 가중치 수가 네 배 차이나지만 MAC은 같다. 블록 4의 공간 위치가 4분의 1인 동시에, 대응하는 입력·출력 채널이 각각 두 배이기 때문이다. 전체 CNN에서 해상도 축소와 채널 증가를 함께 읽어야 하는 이유가 여기에 있다. 단일 같은 폭의 층에 대해 이 상쇄를 쓰면 다음과 같다.[1,2,12]

$$
(H/2)(W/2)\cdot9\cdot(2C)^2
=HW\cdot9C^2.
$$

이 등식은 두 채널을 모두 두 배로 할 때의 국소 비교이다. 첫 층처럼 입력 채널이 3으로 고정된 경우, 블록의 반복 수가 다른 경우, 마지막 블록처럼 채널 증가가 멈춘 경우에는 그대로 적용되지 않는다. 실제로 표의 블록 5는 해상도만 줄고 채널은 512로 유지되므로 MAC이 크게 줄어든다.

다섯 pooling을 통과한 tensor는 $7\times7\times512$이다. VGG의 첫 FC 층은 이것을 4,096차원으로 바꾸므로 다음 가중치 수를 요구한다.[5,12,13]

$$
P_{w,\mathrm{FC1}}=7^2\cdot512\cdot4{,}096=102{,}760{,}448.
$$

Convolution 전체의 가중치는 14,710,464개이고, 세 FC 층의 가중치는 123,633,664개이다. Convolution·FC의 bias까지 포함한 1,000분류 모델의 파라미터 총수는 138,357,544개가 된다. 32비트 스칼라 저장만 가정하면 파라미터 원소 자체에 필요한 공간은 약 553.43 million bytes이다. 압축 파일 크기나 실제 학습 peak memory를 뜻하지 않는다.[5,12,13]

$$
M_{\mathrm{VGG16}}=
15{,}346{,}630{,}656+123{,}633{,}664
=15{,}470{,}264{,}320.
$$

이 합계도 내적 중심 MAC이다. 작은 필터가 큰 필터보다 경제적인 국소 비교와, 전체 VGG가 연산량이 큰 모델이라는 사실은 양립한다. VGG는 높은 해상도에서 여러 층을 계산하고 상당한 채널 폭을 유지하기 때문이다. 어떤 블록을 작게 만들었다는 설명과 전체 네트워크의 비용 비교를 같은 수준의 주장으로 섞지 않아야 한다.[6,12,13]

### (3) 수용영역과 해상도 손실

같은 구성에 수용영역 재귀식을 적용하면 다음 표를 얻는다. 표의 endpoint는 각 블록의 마지막 convolution이 아니라 **pooling 직후**이다. 마지막 값 $r=212,j=32$는 독립적인 수용영역 분석의 VGG-16 결과와도 일치한다.[7,12,13]

| Endpoint | 공간 형상 | $r$ | $j$ |
| --- | --- | ---: | ---: |
| Pool 1 | $112\times112$ | 6 | 2 |
| Pool 2 | $56\times56$ | 16 | 4 |
| Pool 3 | $28\times28$ | 44 | 8 |
| Pool 4 | $14\times14$ | 100 | 16 |
| Pool 5 | $7\times7$ | 212 | 32 |

이를 통해 마지막 feature가 넓은 문맥에 의존할 수 있지만, 중심 위치는 입력 좌표에서 32픽셀 간격으로 배치됨을 동시에 읽어야 한다. 이미지 분류에서는 뒤의 분류기가 여러 위치를 결합하지만, 위치별 출력을 요구하는 문제에서는 이 성긴 출력 격자가 별도의 설계 조건이 된다. 수용영역과 출력 해상도는 서로 대체되는 지표가 아니며, 어느 endpoint를 사용할지 결정할 때 둘을 함께 보아야 한다.[7,8]

## 5. Inception의 병렬 경로와 차원 축소

### (1) 경로별 공간 범위와 채널 결합

Inception-v1의 기본 단위는 같은 입력을 여러 경로에 보내고, 공간 크기가 같은 출력을 채널 축으로 이어 붙이는 블록이다. 대표적으로 $1\times1$, $3\times3$, $5\times5$ convolution 경로와 pooling 경로를 둔다. 큰 공간 필터 앞에는 $1\times1$ convolution으로 중간 채널을 줄인다. 연결 관계는 원문의 [Fig. 2](https://www.cv-foundation.org/openaccess/content_cvpr_2015/papers/Szegedy_Going_Deeper_With_2015_CVPR_paper.pdf#page=4)와 독립 교재의 `Inception` 구현에서 확인할 수 있다.[16,17]

각 경로의 함수를 $F_1,F_3,F_5,F_p$, 채널 수를 $c_1,c_3,c_5,c_p$라 하면 블록 출력은 다음과 같다. `Concat`은 합산이 아니라 채널 연결이므로 출력 채널 수가 경로별 채널 수의 합이 된다.[16,17]

$$
Y=\operatorname{Concat}_{\mathrm{channel}}
\bigl(F_1(X),F_3(X),F_5(X),F_p(X)\bigr),
\qquad C_{\mathrm{out}}=c_1+c_3+c_5+c_p.
$$

각 경로에서 stride 1과 적절한 padding을 사용하면 같은 공간 위치의 출력을 결합할 수 있다. 높이와 너비가 같다는 조건 외에도, 그 위치가 가리키는 입력 중심을 정렬해야 한다. 예를 들어 홀수 크기 필터에 대칭 padding을 주는 v1 블록은 이 조건을 자연스럽게 충족한다. 모든 출력 채널이 같은 공간 범위를 거치는 것은 아니며, 각 경로의 범위를 따로 추적해야 한다.[7,16,17]

### (2) $1\times1$ 병목의 비용 조건

$1\times1$ convolution은 공간 이웃을 모으지 않고 같은 위치의 채널 벡터를 변환한다. 입력 위치의 벡터를 $x\in\mathbb{R}^{C_{\mathrm{in}}}$, 축소 채널 수를 $R$라 하면, bias를 생략한 선형 부분은 행렬 $A\in\mathbb{R}^{R\times C_{\mathrm{in}}}$에 의한 $Ax$이다. $R<C_{\mathrm{in}}$일 때 이를 bottleneck으로 사용하면 뒤의 공간 필터가 처리할 채널을 줄일 수 있다.[1,2,16]

직접 $k\times k$ convolution과, $1\times1$ 축소 후 $k\times k$ convolution을 비교하자. 입력·출력 공간 크기를 같게 유지하고 activation 비용을 제외하면 다음과 같다.[1,2,16]

$$
P_{w,\mathrm{direct}}=k^2C_{\mathrm{in}}C_{\mathrm{out}},
\qquad
P_{w,\mathrm{bottle}}=C_{\mathrm{in}}R+k^2RC_{\mathrm{out}}.
$$

앞의 축소 층도 공짜가 아니다. 두 비용의 비를 정리하면 축소 정도가 충분해야 절감된다는 조건을 얻는다.

$$
\frac{P_{w,\mathrm{bottle}}}{P_{w,\mathrm{direct}}}
=\frac{R}{k^2C_{\mathrm{out}}}+\frac{R}{C_{\mathrm{in}}},
\qquad
R<\frac{k^2C_{\mathrm{in}}C_{\mathrm{out}}}
{C_{\mathrm{in}}+k^2C_{\mathrm{out}}}.
$$

오른쪽 부등식은 이 두 연산만 비교할 때의 엄밀한 비용 절감 조건이다. 예를 들어 $C_{\mathrm{in}}=192$, $C_{\mathrm{out}}=32$, $k=5$, $R=16$이면 직접 가중치는 153,600개, 축소 경로는 15,872개이다. $28\times28$ 격자에서 직접 계산한 MAC은 다음과 같다.

$$
M_{\mathrm{direct}}=120{,}422{,}400,
\qquad M_{\mathrm{bottle}}=12{,}443{,}648.
$$

이 예제는 약 9.68배의 내적 감소를 보이지만, 정확도 유지나 같은 배수의 지연시간 감소를 증명하지 않는다. 더 좁은 중간 표현을 통해서만 정보를 전달하도록 연결을 제한했기 때문이다. 비선형을 제거한 경우에는 각 공간 offset의 유효 채널 변환이 $U_{a,b}A$ 형태이며, 여기서 $U_{a,b}$는 후속 공간 필터의 해당 offset에서 $R$개 채널을 출력 채널로 보내는 행렬이다. 그 rank가 $R$을 넘지 않는다는 선형대수적 제약을 직접 도출할 수 있다. 이 rank 설명은 비선형 경로 전체를 하나의 고정 행렬로 취급하는 근사가 아니다.[1,2,16]

$$
\operatorname{rank}(U_{a,b}A)\le R.
$$

실제 블록에 activation을 넣으면 입력에 따른 변환도 생긴다. 그래도 단순히 $R$을 작게 할수록 항상 좋은 구조라는 결론은 나오지 않는다. 병목 폭은 계산 예산과 중간 표현의 제약을 함께 정하는 설계 변수이다. 여러 경로를 남기는 구조에서는 한 경로의 축소만 보고 블록 전체가 동일한 정보 제한을 받는다고 해석해서도 안 된다.[2,15,16]

### (3) Inception 3a의 전체 계수

GoogLeNet의 첫 Inception 블록인 3a는 입력 채널 192개에 대해 아래 경로를 사용한다. 원 논문의 Table 1과 독립 구현의 생성자 인수가 같은 구성을 지정한다. 표의 가중치 수는 이 구조에서 직접 계산한 값이며, pooling 비교·activation·bias는 제외한다.[16,17]

| 경로 | 채널 변환 | 출력 채널 | 가중치 |
| --- | --- | ---: | ---: |
| $1\times1$ | $192\to64$ | 64 | 12,288 |
| $1\times1\to3\times3$ | $192\to96\to128$ | 128 | 129,024 |
| $1\times1\to5\times5$ | $192\to16\to32$ | 32 | 15,872 |
| $3\times3$ pooling 후 $1\times1$ | $192\to32$ | 32 | 6,144 |

총 출력 채널 수는 $64+128+32+32=256$이다. 공간 크기를 $28\times28$로 두면 다음 직접 계산을 얻는다.

$$
P_w=163{,}328,
\qquad M=28^2\cdot163{,}328=128{,}049{,}152.
$$

출력 채널은 그대로 두고 두 공간 필터 앞의 축소만 제거한 가상 블록을 비교 대상으로 정의할 수도 있다. Pooling 경로의 출력 projection은 유지한다. 그러면 가중치 수는 다음과 같다.

$$
P_{w,\mathrm{no\ reduction}}=
192\cdot64+9\cdot192\cdot128+
25\cdot192\cdot32+192\cdot32=393{,}216.
$$

따라서 축소를 넣은 블록의 가중치와 MAC은 이 비교 대상의 약 41.5%이다. 이 경우 $5\times5$ 경로 하나의 절감 배수와 블록 전체의 절감 배수는 다르다. 다른 경로는 같은 비용을 유지하거나 훨씬 큰 비중을 차지하기 때문이다. 실제 표에서는 $3\times3$ 경로가 전체 가중치의 약 79%를 차지한다. 가장 큰 공간 필터가 항상 가장 비싼 경로라고 판단할 수 없는 이유이다.

### (4) 공간 분해와 분류기 축소

후속 Inception 설계는 채널 축소에 더해 공간 필터도 분해한다. $5\times5$를 두 $3\times3$로 바꾸는 비교는 VGG 절의 조건과 같고, $n\times n$을 $1\times n$과 $n\times1$의 직렬 연결로 바꾸는 방법도 사용한다. 독립 구현의 `InceptionC`는 실제로 $(1,7)$과 $(7,1)$ 커널을 연결한다. 논문의 개념도를 모든 소프트웨어 구현과 완전히 동일한 블록 명세로 취급하지 말고, 사용할 구현의 kernel·중간 폭을 확인해야 한다.[15,18]

모든 입력·중간·출력 채널을 $C$로 고정하고 해상도를 유지하면 공간 분해의 직접 비용은 다음과 같다.

$$
P_{w,n\times n}=n^2C^2,
\qquad P_{w,\mathrm{factorized}}=2nC^2,
\qquad \frac{P_{w,\mathrm{factorized}}}{P_{w,n\times n}}=\frac{2}{n}.
$$

$n=7$이면 비는 $2/7$이다. 그러나 중간 채널 수가 $R$라면 분해된 비용은 $nC_{\mathrm{in}}R+nRC_{\mathrm{out}}$이므로, 폭을 늘리는 순간 단순한 $2/n$ 비를 적용할 수 없다. 두 비대칭 층은 합성하여 정사각 공간 범위를 볼 수 있지만, 중간 표현과 비선형의 배치가 바뀐다. 이는 기존 큰 필터의 값을 손실 없이 인수분해했다는 보장이 아니라 새 학습 구조를 정의한 것이다.[1,15,18]

GoogLeNet 계열의 다른 절감은 global average pooling (GAP)이다. 마지막 tensor의 높이·너비를 $H_f,W_f$, 채널을 $c$로 표시하면 공간 평균 $z_c$를 구한 뒤, 그 채널 벡터를 분류기에 전달한다.[16,17]

$$
z_c=\frac{1}{H_fW_f}\sum_{u=1}^{H_f}\sum_{v=1}^{W_f}X_{c,u,v}.
$$

평균 뒤 $C_f$개 채널을 $N_{\mathrm{cls}}$개 class로 선형 분류하면 가중치 수는 $C_fN_{\mathrm{cls}}$이다. 공간을 펼쳐 바로 $N_{\mathrm{cls}}$개로 연결하면 $H_fW_fC_fN_{\mathrm{cls}}$가 필요하다. $H_f=W_f=7$, $C_f=1{,}024$, $N_{\mathrm{cls}}=1{,}000$인 직접 비교에서는 다음과 같다.[1,16,17]

$$
P_{w,\mathrm{GAP+FC}}=1{,}024{,}000,
\qquad P_{w,\mathrm{flatten+FC}}=50{,}176{,}000.
$$

49배의 차이는 이 두 가지 **단일 선형 분류기** 비교에 한정된다. VGG의 다층 분류기를 그대로 바꿨을 때의 정확도 차이나 전체 모델 압축률을 뜻하지 않는다. 공간 평균은 채널별 위치 정보를 집계하므로, 가중치 절감뿐 아니라 분류기가 사용할 수 있는 표현도 달라진다. 병목 convolution과 global average pooling은 서로 다른 위치의 비용을 줄이는 설계이며, 둘을 하나의 원인으로 묶지 않는 편이 해석에 유리하다.[1,16,17]

## 6. 구조 비교의 측정 조건

모델 비교에서 파라미터 수는 계산 그래프의 속성이고, 정확도는 데이터·학습·checkpoint·평가 절차까지 포함한 결과이다. 실행 시간은 여기에 장치와 라이브러리, batch size가 더해진다. Canziani 등의 분석은 입력 crop 규약을 통일한 정확도 재평가와 장치 자원 측정을 구분하며, VGG의 공식 구현도 별도 학습 recipe로 생성한 weights를 표시한다. 따라서 같은 모델 이름이 같은 학습 실험을 뜻하지 않는다.[6,13]

아래 항목을 고정해야 구조 변화의 효과와 나머지 변경 효과를 구분할 수 있다. 이는 앞의 직접 계산 예제를 실제 평가로 연결하는 최소 기록표이다.[6,12,13]

| 비교 대상 | 함께 기록할 조건 | 조건이 다를 때 생기는 혼동 |
| --- | --- | --- |
| 파라미터 | 정확한 채널·그룹·분류 class 수 | 동일 이름의 다른 그래프를 비교 |
| MAC/FLOP | 입력 크기, crop 수, 포함 연산, MAC 환산 | 한 이미지 비용과 여러 crop 비용 혼합 |
| 분류 정확도 | 데이터 분할, checkpoint, resize·crop | 구조와 학습·전처리 효과 혼합 |
| 학습 효과 | optimizer, schedule, 증강, 정규화 | 깊이 변경의 인과 효과 오해 |
| 실행 지연 | batch, 정밀도, 장치, backend, 동기화 | 이론적 연산량을 실측 시간으로 오인 |
| 메모리 | 추론/학습, activation, workspace | 모델 파일 크기를 peak로 오인 |

특히 single-crop과 multi-crop 평가를 섞으면 정확도뿐 아니라 추론 비용도 달라진다. Crop $T$개를 각각 독립적으로 같은 네트워크에 통과시키고 결과만 합친다고 가정하면, 결합 비용을 제외한 MAC은 다음과 같다. 특징을 공유하는 별도 구현에는 이 단순식이 그대로 적용되지 않는다.[6,12]

$$
M_{\mathrm{multi\mbox{-}crop}}=T\,M_{\mathrm{single\mbox{-}crop}}.
$$

!!! info "[Measurement]"
    지정한 checkpoint와 입력 tensor를 사용하고 추론 모드에서 준비 실행을 마친 뒤, 장치 연산이 완료되는 경계를 기준으로 $N$회 batch 실행 시간을 잰다. 실행마다 batch size $B$가 같고 전체 경과 시간이 $t$초라면 평균 batch 지연은 $t/N$, 이미지 처리율은 $NB/t$이다. 입력 전송·전처리를 시간에 포함했는지와 장치 동기화 방식을 함께 기록한다. 이 산출은 batch를 처리한 측정값이므로, $t/(NB)$를 요청 한 건의 응답 지연으로 바꾸어 부르지 않는다.[19,20]

MAC이 작은 구조가 어떤 장치에서도 반드시 더 짧은 시간을 갖는다고 추론할 수는 없다. 분기별 tensor 크기, 중간 출력의 저장과 이동, 연산 구현이 실행 비용에 영향을 주기 때문이다. 같은 정밀도·batch·backend에서 실측한 결과를 우선하고, MAC은 원인을 분석하는 공통 좌표로 사용해야 한다. 특정 장치에서 관측한 연산량과 시간의 상관관계를 하드웨어와 무관한 등식으로 확대해서는 안 된다.[5,6]

## 7. 설계 원리의 연결

아래 표는 각 계열을 하나의 정량적 설계 질문으로 정리한다. 비교 축은 순위가 아니라 연결 구조를 바꿀 때 얻는 효과와 그에 따라 확인해야 할 제약이다.

| 계열 | 핵심 조작 | 정량적으로 확인할 효과 | 함께 확인할 제약 |
| --- | --- | --- | --- |
| LeNet 계열 | 국소 연결·공간 공유·pooling | $P_w$와 출력 면적의 분리 | 원형과 단순화 구현의 차이 |
| AlexNet | 깊이·폭 확대와 일부 채널 분할 | convolution MAC과 FC 저장량 | 그룹 연결·입력·학습 조건 |
| VGG | 작은 필터의 직렬 반복 | 동일 범위의 $18/25$, $27/49$ 비용 비 | 중간 폭·activation·전체 해상도 |
| Inception | 병렬 경로와 중간 폭 축소 | 경로별 $C_{\mathrm{in}}R+k^2RC_{\mathrm{out}}$ | 축소에 따른 표현 제약·실측 지연 |

작은 필터, 깊은 블록, 병렬 경로는 서로 배타적인 선택이 아니다. 공통 convolution 식에서 공간 크기, 채널 연결, 경로 수를 어떻게 배분하는지에 따라 조합할 수 있다. 이 장의 비용 유도는 이후 구조를 읽을 때도 적용되지만, 파라미터 수·MAC·수용영역 중 어느 하나만으로 학습 성능을 결정할 수는 없다. 계산 그래프에서 유도할 수 있는 값과 학습·측정해야 하는 결과를 나누어 해석하는 것이 고전 CNN 계보를 활용하는 출발점이다.[1,6,7,12,16]

## 8. 참고문헌

1. PyTorch contributors, “Conv2d,” *PyTorch documentation*. [공식 연산·형상·가중치 규약](https://docs.pytorch.org/docs/2.14/generated/torch.nn.Conv2d.html).
2. A. Zhang, Z. C. Lipton, M. Li, and A. J. Smola, “Multiple Input and Multiple Output Channels,” *Dive into Deep Learning*, §7.4. [본문과 독립 실행 구현](https://d2l.ai/chapter_convolutional-neural-networks/channels.html).
3. A. Zhang et al., “Padding and Stride,” *Dive into Deep Learning*, §7.3. [본문과 식 (7.3.2)](https://d2l.ai/chapter_convolutional-neural-networks/padding-and-strides.html).
4. A. Krizhevsky, I. Sutskever, and G. E. Hinton, “ImageNet Classification with Deep Convolutional Neural Networks,” *Advances in Neural Information Processing Systems* **25** (2012). [원문](https://proceedings.neurips.cc/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf).
5. Stanford CS231n, “Convolutional Neural Networks,” *Course notes*. [구조·VGG 계수·메모리 분석](https://cs231n.github.io/convolutional-networks/).
6. A. Canziani, A. Paszke, and E. Culurciello, “An Analysis of Deep Neural Network Models for Practical Applications,” arXiv:1605.07678v4 (2017). [측정 조건과 자원 분석 원문](https://arxiv.org/html/1605.07678v4).
7. A. Araujo, W. Norris, and J. Sim, “Computing Receptive Fields of Convolutional Neural Networks,” *Distill* (2019). [DOI: 10.23915/distill.00021](https://distill.pub/2019/computing-receptive-fields/).
8. W. Luo, Y. Li, R. Urtasun, and R. Zemel, “Understanding the Effective Receptive Field in Deep Convolutional Neural Networks,” *Advances in Neural Information Processing Systems* **29** (2016). [원문](https://proceedings.neurips.cc/paper/2016/file/c8067ad1937f728f51288b3eb986afaa-Paper.pdf).
9. Y. LeCun, L. Bottou, Y. Bengio, and P. Haffner, “Gradient-Based Learning Applied to Document Recognition,” *Proceedings of the IEEE* **86**, 2278–2324 (1998). [DOI: 10.1109/5.726791](https://doi.org/10.1109/5.726791), [원문 사본과 Fig. 2](https://vitalab.github.io/papers/lecun-98.pdf#page=7).
10. A. Zhang et al., “Convolutional Neural Networks (LeNet),” *Dive into Deep Learning*, §7.6. [교육용 구조와 실행 구현](https://d2l.ai/chapter_convolutional-neural-networks/lenet.html).
11. A. Zhang et al., “Deep Convolutional Neural Networks (AlexNet),” *Dive into Deep Learning*, §8.1. [본문과 단순화 구현](https://d2l.ai/chapter_convolutional-modern/alexnet.html).
12. K. Simonyan and A. Zisserman, “Very Deep Convolutional Networks for Large-Scale Image Recognition,” *International Conference on Learning Representations* (2015). [arXiv:1409.1556](https://arxiv.org/abs/1409.1556).
13. Torchvision contributors, “torchvision.models.vgg,” *Torchvision source documentation*. [구성 D, classifier와 weights metadata](https://docs.pytorch.org/vision/main/_modules/torchvision/models/vgg.html).
14. A. Zhang et al., “Networks Using Blocks (VGG),” *Dive into Deep Learning*, §8.2. [블록 분석과 구현](https://d2l.ai/chapter_convolutional-modern/vgg.html).
15. C. Szegedy, V. Vanhoucke, S. Ioffe, J. Shlens, and Z. Wojna, “Rethinking the Inception Architecture for Computer Vision,” *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition*, 2818–2826 (2016). [원문](https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Szegedy_Rethinking_the_Inception_CVPR_2016_paper.pdf).
16. C. Szegedy et al., “Going Deeper With Convolutions,” *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition*, 1–9 (2015). [원문](https://www.cv-foundation.org/openaccess/content_cvpr_2015/papers/Szegedy_Going_Deeper_With_2015_CVPR_paper.pdf).
17. A. Zhang et al., “Multi-Branch Networks (GoogLeNet),” *Dive into Deep Learning*, §8.4. [경로별 분석과 실행 구현](https://d2l.ai/chapter_convolutional-modern/googlenet.html).
18. Torchvision contributors, “torchvision.models.inception,” *Torchvision source documentation*. [InceptionC의 공간 분해 구현](https://docs.pytorch.org/vision/main/_modules/torchvision/models/inception.html).

19. PyTorch contributors, “PyTorch Benchmark,” *PyTorch Tutorials*, §3. [준비 실행과 장치 동기화](https://docs.pytorch.org/tutorials/recipes/recipes/benchmark.html).
20. A. Zhang et al., “Asynchronous Computation,” *Dive into Deep Learning*, §13.2.1. [비동기 실행과 독립 측정 예제](https://d2l.ai/chapter_computational-performance/async-computation.html).
