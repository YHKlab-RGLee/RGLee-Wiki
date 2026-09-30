---
description: Prefix sum, difference array, two pointers와 sliding window의 불변식을 비교하고 Python 구현과 동적 구간 질의의 선택 기준을 설명한다.
---

# Prefix sums and two pointers

**Prefix sum**은 배열 앞부분의 합을 저장하여 구간 합을 두 경계의 차로 계산하는 방법이다. **Two pointers**는 두 위치를 움직이면서 더 이상 답이 될 수 없는 후보를 제외하는 방법이다. 전자는 합의 분해를, 후자는 후보를 버려도 된다는 순서 관계를 이용한다. 두 방법 모두 연속 구간을 다루지만, 합에 음수가 포함되는지와 원래 배열의 순서를 보존해야 하는지에 따라 적용 조건이 달라진다.[1,2]

이 문서는 Python 정수 배열을 대상으로 정적 구간 합, 일괄 구간 갱신, 목표 합의 구간 개수, 이동하는 창의 합과 최솟값을 연결한다. 마지막에는 값이 바뀌는 질의를 위한 Fenwick tree와 segment tree를 다룬다. 복잡도는 정수 덧셈·비교를 상수 시간으로 보는 연산 모형이며, hash table을 쓰는 곳에서는 평균적인 조회 비용이라는 조건을 따로 밝힌다. 각 코드는 반환값과 경계 처리를 명시한 구현 예시이다.

## 1. Prefix sum과 구간 경계

### (1) 경계에 저장한 누적 합

길이가 $n$인 배열을 $a$라 하자. 원소 인덱스는 $0$부터 $n-1$까지이고, 구간은 오른쪽 끝을 포함하지 않는 **반열린 구간** $[l,r)$로 표시한다. 조건은 $0\le l\le r\le n$이며 길이는 $r-l$이다. Prefix 배열 $P$에는 원소가 아니라 경계까지의 합을 저장한다.[1,2]

$$
P[0]=0,\qquad P[t]=\sum_{i=0}^{t-1}a[i]\quad(1\le t\le n).
$$

따라서 $P$의 길이는 $n+1$이다. $P[t]$는 인덱스 $t$의 원소를 포함하지 않는다. $P[0]$은 빈 앞부분의 합이며, $P[n]$은 배열 전체의 합이다. 이 규약을 쓰면 첫 원소에서 시작하는 질의를 별도로 처리할 필요가 없다. 문헌의 1-based 닫힌 구간 $[L,R]$는 이 문서의 0-based $[L-1,R)$에 해당한다.[1,2]

구간 합을 $S(l,r)$라 정의하면 다음 관계는 근사가 아닌 정확한 항등식이다.[1,2]

$$
S(l,r)=\sum_{i=l}^{r-1}a[i]=P[r]-P[l].
$$

$P[r]$에 들어 있는 앞부분 $[0,l)$을 $P[l]$로 제거하면 원하는 구간만 남는다. 원소의 부호는 이 소거에 영향을 주지 않는다. $l=r$이면 같은 값을 빼므로 빈 구간 합은 0이다. 아래 표는 직접 정한 배열 $a=[3,-2,0,5]$의 경계별 값을 계산한 것이다.

| 경계 $t$ | 앞부분 $a[0:t]$ | $P[t]$ |
| --- | --- | ---: |
| 0 | 빈 배열 | 0 |
| 1 | `[3]` | 3 |
| 2 | `[3, -2]` | 1 |
| 3 | `[3, -2, 0]` | 1 |
| 4 | `[3, -2, 0, 5]` | 6 |

이 표에서 $S(1,4)=6-3=3$이며 실제 합 $-2+0+5$와 같다. 경계 2와 3의 값이 같은 것은 중간 원소가 0이기 때문이다. 서로 다른 위치가 같은 prefix 값을 가질 수 있다는 사실은 뒤의 구간 개수 계산에서 중요하다.

### (2) 전처리와 질의 비용

Prefix 배열은 이전 경계의 합에 새 원소 하나만 더하여 만든다. 아래 구현의 반복문 직전에는 `prefix[i]`가 `a[0:i]`의 합이라는 불변식이 성립한다. 한 번의 대입으로 다음 경계까지 불변식을 확장한다.[1,2]

```python
def prefix_sums(a):
    prefix = [0] * (len(a) + 1)
    for i, value in enumerate(a):
        prefix[i + 1] = prefix[i] + value
    return prefix


def range_sum(prefix, left, right):
    n = len(prefix) - 1
    if not 0 <= left <= right <= n:
        raise ValueError("invalid half-open range")
    return prefix[right] - prefix[left]
```

전처리는 $O(n)$ 시간·추가 공간을 사용하고, 질의는 두 값을 읽어 빼므로 $O(1)$이다. 질의가 $q$개이면 총 $O(n+q)$이다. 단 한 번의 합만 필요하다면 전처리 없이 더하는 것으로 충분하지만, 같은 배열에 여러 경계의 질의가 반복되면 저장한 합을 재사용할 수 있다.[1,2]

Prefix라는 저장 형태만으로 모든 구간 연산이 해결되지는 않는다. 예를 들어 `[1, 3]`과 `[1, 8]`은 앞부분 최솟값 배열이 모두 `[1, 1]`이다. 그러나 뒤 원소 하나의 최솟값은 각각 3과 8이다. 이 직접 구성한 반례에서 보듯 앞부분 최솟값 두 개로는 내부 구간의 최솟값을 복원할 수 없다. 합에서 쓰던 뺄셈에 대응하는 역연산이 없기 때문이다. 이런 질의에는 뒤에서 설명할 구간별 정보의 결합이 필요하다.[1,3]

## 2. 이차원 구간 합과 포함·배제

### (1) 누적 직사각형

행이 $h$개, 열이 $w$개인 직사각형 배열을 $A$라 하자. 이차원 prefix 배열 $P_2[x][y]$는 행 $[0,x)$와 열 $[0,y)$가 이루는 직사각형의 합이다. 첫 행과 첫 열은 0으로 두며 크기는 $(h+1)\times(w+1)$이다.[1,2]

$$
P_2[x][y]=\sum_{i=0}^{x-1}\sum_{j=0}^{y-1}A[i][j].
$$

현재 칸 $A[i][j]$까지 포함하는 누적 합은 위쪽 직사각형과 왼쪽 직사각형을 더한 뒤, 두 번 포함된 왼쪽 위 부분을 한 번 뺀 값이다.[1,2]

$$
P_2[i+1][j+1]
=P_2[i][j+1]+P_2[i+1][j]-P_2[i][j]+A[i][j].
$$

여기서 두 큰 prefix에 현재 칸은 아직 들어 있지 않으므로 마지막에 한 번 더한다. 이 식은 포함·배제 원리를 배열 경계에 적용한 것이다. 행을 위에서 아래로, 열을 왼쪽에서 오른쪽으로 채우면 우변의 세 prefix가 모두 먼저 계산되어 있다.[1,2]

```python
def prefix_sums_2d(matrix):
    height = len(matrix)
    width = len(matrix[0]) if height else 0
    if any(len(row) != width for row in matrix):
        raise ValueError("matrix must be rectangular")
    prefix = [[0] * (width + 1) for _ in range(height + 1)]
    for i in range(height):
        for j in range(width):
            prefix[i + 1][j + 1] = (
                prefix[i][j + 1] + prefix[i + 1][j]
                - prefix[i][j] + matrix[i][j]
            )
    return prefix
```

이 구현은 행마다 별도 리스트를 만든다. 입력이 `[]`이면 반환값은 `[[0]]`이며, 열이 없는 행들에도 0으로 된 경계를 보존한다. 양의 $h,w$에 대해 전처리 시간과 추가 공간은 $O(hw)$이다. 일반적인 질의 비용은 직사각형의 넓이에 의존하지 않는다.[1,2]

### (2) 네 모서리의 부호

질의의 위·아래 경계를 $x_1,x_2$, 왼쪽·오른쪽 경계를 $y_1,y_2$라 하자. 범위는 $0\le x_1\le x_2\le h$, $0\le y_1\le y_2\le w$이다. 원하는 합 $R$은 다음 네 prefix로 계산한다.[1,2]

$$
R=P_2[x_2][y_2]-P_2[x_1][y_2]
-P_2[x_2][y_1]+P_2[x_1][y_1].
$$

첫 항에서 질의보다 위쪽인 부분과 왼쪽인 부분을 각각 제거한다. 이때 왼쪽 위 영역은 두 번 빠졌으므로 마지막 항으로 한 번 되돌린다. 다음은 직접 만든 행렬에서 이 부호를 확인한 계산이다.

| 항목 | 값 |
| --- | --- |
| 행렬 $A$ | `[[2, -1, 4], [0, 3, 5]]` |
| 질의 | 행 `[0, 2)`, 열 `[1, 3)` |
| 필요한 네 값 | $P_2[2][3]=13$, $P_2[0][3]=0$, $P_2[2][1]=2$, $P_2[0][1]=0$ |
| 네 항의 합 | $13-0-2+0=11$ |
| 원소별 확인 | $-1+4+3+5=11$ |

아래 함수는 이미 구성한 prefix 배열을 입력받는다. 높이나 너비가 0인 질의도 같은 식으로 0을 반환한다. 본문에서 행·열 순서를 고정했으므로 `top`, `bottom`을 열 인덱스로 바꾸어 넘기지 않아야 한다.

```python
def rectangle_sum(prefix, top, left, bottom, right):
    height, width = len(prefix) - 1, len(prefix[0]) - 1
    if not (0 <= top <= bottom <= height
            and 0 <= left <= right <= width):
        raise ValueError("invalid rectangle")
    return (prefix[bottom][right] - prefix[top][right]
            - prefix[bottom][left] + prefix[top][left])
```

두 차원의 경계를 변환할 때는 각 축을 독립적으로 처리한다. 예를 들어 1-based 닫힌 행 구간 `[2, 4]`와 열 구간 `[3, 5]`는 각각 0-based `[1, 4)`와 `[2, 5)`이다. 오른쪽 경계를 두 번 증가시키거나 왼쪽 경계를 두 번 감소시키면 포함할 행 또는 열이 달라진다. 이 변환은 1절의 한 축 규약을 두 축에 적용한 것이며, 넓이는 두 길이의 곱 $(x_2-x_1)(y_2-y_1)$이다. 행마다 열 개수가 다른 입력에서는 하나의 너비 경계를 공유할 수 없으므로 위 생성 함수는 그런 입력을 거부한다.[1,2]

## 3. Difference array와 일괄 구간 갱신

### (1) 누적과 차분의 역관계

**Difference array**는 인접한 값의 차이를 저장한다. $n>0$인 배열 $a$에 대해 $D[0]=a[0]$, $D[i]=a[i]-a[i-1]$로 정의하면 차이를 다시 누적하여 원래 값을 복원할 수 있다.[1,4]

$$
D[0]=a[0],\quad D[i]=a[i]-a[i-1]\ (1\le i<n),
\qquad a[i]=\sum_{j=0}^{i}D[j].
$$

중간의 $a[j]$와 $-a[j]$가 소거되어 마지막 값만 남는 관계이다. Prefix sum이 여러 구간의 **조회**를 위해 앞부분의 합을 저장한다면, difference array는 여러 구간의 **가산 갱신**을 경계의 변화로 저장한다. 이미 주어진 배열에 갱신량만 더할 때는 원래 배열의 차분까지 만들지 않고, 갱신량 전용 차분을 0으로 초기화해도 된다.[1,4,5]

반열린 구간 $[l,r)$의 모든 원소에 정수 $v$를 더하는 갱신은 다음 두 사건으로 나타낸다.[1,5]

$$
D[l]\leftarrow D[l]+v,\qquad D[r]\leftarrow D[r]-v.
$$

$l$ 이전에서는 두 사건을 아직 만나지 않았고, $l$부터 $r-1$까지에서는 첫 사건만 누적하여 $v$가 남는다. $r$부터는 두 사건이 상쇄된다. $r=n$인 갱신도 같은 코드로 표현하려고 차분 배열에 길이 $n+1$을 할당한다. 마지막 칸은 종료 사건을 담는 경계이며 결과 배열의 원소는 아니다.[1,5]

### (2) 갱신의 합성과 복원

아래 함수는 `updates`에 주어진 `(left, right, delta)`들을 모두 적용한 새 배열을 반환한다. 입력 `a`는 그대로 두고, `running`에는 현재 위치까지 유효한 갱신량의 합을 유지한다. 여러 갱신이 겹치면 각 경계 사건을 더하면 된다.[1,4,5]

```python
def apply_range_additions(a, updates):
    n = len(a)
    difference = [0] * (n + 1)
    for left, right, delta in updates:
        if not 0 <= left <= right <= n:
            raise ValueError("invalid half-open range")
        difference[left] += delta
        difference[right] -= delta
    result = []
    running = 0
    for i, value in enumerate(a):
        running += difference[i]
        result.append(value + running)
    return result
```

길이 5의 영 배열에 `[1, 4)`의 `+3`, `[2, 5)`의 `-1`을 적용한다고 하자. 다음 수작업 표에서 같은 위치의 사건은 합쳐지며, 인덱스 5의 종료 사건은 결과에 포함되지 않는다.

| 위치 | 0 | 1 | 2 | 3 | 4 | 5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 경계 사건 | 0 | 3 | -1 | 0 | -3 | 1 |
| 복원한 갱신량 | 0 | 3 | 2 | 2 | -1 | 결과 밖 |

갱신 $q$개는 각각 두 칸만 바꾸고 마지막 복원은 한 번 순회하므로 이 코드의 시간은 $O(n+q)$, 추가 공간은 $O(n)$이다. 빈 구간은 같은 칸에 $+v$와 $-v$를 더하므로 아무 효과가 없다. 이 비용은 **모든 갱신 후 결과를 한 번 읽는 경우**의 비용이다. 갱신 사이마다 현재 값을 읽어야 한다면 매번 전체를 복원하는 대신, 8절의 Fenwick tree에 차분을 저장하는 방법을 고려한다.[1,5]

## 4. 목표 합을 갖는 연속 구간의 개수

### (1) 문제와 prefix 쌍의 대응

다음은 위 관계를 적용하도록 구성한 예제이다. 정수 변화량 배열 `a`와 목표 합 `target`이 주어진다. 원래 순서를 유지하는 **비어 있지 않은 연속 구간** 중 합이 `target`인 구간의 개수를 반환한다. 경계가 다르면 원소 값이 같더라도 서로 다른 구간으로 센다. 입력 조건은 $0\le n\le200000$, $|a[i]|\le10^9$, $|\mathrm{target}|\le10^{14}$이며 음수와 0을 허용한다.

문제의 수학적 대상은 $0\le l<r\le n$인 경계 쌍이다. 목표 합을 $K$라 쓰면 prefix 항등식에서 다음 동치가 나온다. 음수가 있어도 이 동치는 그대로 성립한다.[6,7,8]

$$
S(l,r)=K\quad\Longleftrightarrow\quad P[l]=P[r]-K.
$$

오른쪽 경계 $r$를 고정하면 앞선 경계 중 값이 $P[r]-K$인 것의 수만 알면 된다. 매번 모든 $l$을 검사하는 대신 **prefix 값별 출현 횟수**를 dictionary에 저장한다. 출처 [8]의 앞선 prefix 인덱스 찾기를 개수 질의로 바꾸면, 하나의 인덱스 대신 그 값이 나타난 모든 경계의 수가 필요하다. 이 빈도 방식은 출처 [6]의 구간 개수 풀이와 일치한다.[6,8]

조회 직전의 빈도 함수를 $F_r$라 정의하자. $s$는 dictionary의 키가 되는 임의의 정수이다.[6,8]

$$
F_r(s)=\#\{l\mid 0\le l<r,\ P[l]=s\},
\qquad \mathrm{answer}=\sum_{r=1}^{n}F_r(P[r]-K).
$$

집합 기호 안에는 값의 종류가 아니라 **경계 인덱스**가 들어 있다. 같은 prefix 값이 세 번 나타났다면 새 오른쪽 경계에 대해 서로 다른 시작점 세 개가 생길 수 있다. `set`으로 존재 여부만 저장하면 이러한 중복을 잃는다. 또한 prefix 전체를 미리 빈도표에 넣으면 미래 경계까지 포함하여 $l<r$ 조건을 깨므로, 왼쪽에서 오른쪽으로 처리한 이력만 저장한다.[6,8]

### (2) 완전한 함수와 반복 불변식

초기 상태에는 경계 0만 존재하므로 `frequency = {0: 1}`로 시작한다. `prefix`에 새 값을 더한 뒤 현재 합에서 `target`을 뺀 키의 빈도를 조회하고, **조회가 끝난 뒤** 현재 prefix를 등록한다. 이 순서가 앞선 경계만 허용하는 조건을 코드에 구현한다.[6,8]

```python
def count_target_subarrays(a, target):
    frequency = {0: 1}
    prefix = 0
    answer = 0
    for value in a:
        prefix += value
        answer += frequency.get(prefix - target, 0)
        frequency[prefix] = frequency.get(prefix, 0) + 1
    return answer
```

함수는 정수들을 한 번 순서대로 읽으며 구간 자체를 저장하지 않는다. `get(key, 0)`은 해당 키가 없을 때 0을 사용한다.[9,10] 따라서 아직 본 적 없는 필요한 prefix 값은 기여가 0이고, 같은 값이 다시 나타나면 누적된 빈도를 모두 더한다. 반환값은 구간의 개수이며 입력 배열의 길이나 서로 다른 prefix 값의 수와는 다른 양이다.[6,9]

이 코드의 정확성은 다음과 같이 원문 관계를 경계별로 적용하여 증명할 수 있다. $r$번째 원소를 반영한 직후 `prefix`는 $P[r]$이고 dictionary에는 $P[0],\ldots,P[r-1]$만 있다. 조회 결과는 정확히 오른쪽 경계가 $r$인 유효 구간의 수이다. 이들 구간은 이전 오른쪽 경계에서 센 구간과 다르므로 `answer`에 더해도 중복되지 않는다. 그 뒤 $P[r]$을 삽입하면 다음 반복을 위한 빈도표가 된다. 초기 빈 prefix가 귀납의 시작을 제공하고, $r=n$까지 처리하면 모든 비어 있지 않은 구간이 자신의 오른쪽 경계에서 한 번씩 검사된다.[6,8]

이 증명은 정렬이나 합의 단조성을 사용하지 않는다. 음수가 들어가도 prefix 값의 차라는 관계만 유지하면 된다. Dictionary 조회·갱신을 평균 $O(1)$로 보는 모형에서 전체 시간은 기대 $O(n)$이고, 서로 다른 prefix는 최대 $n+1$개이므로 공간은 $O(n)$이다. Python dictionary의 모든 입력에 대해 최악 $O(n)$을 보장한다는 뜻은 아니다.[6,8]

### (3) 수작업 추적과 경계 사례

예제 입력은 `a = [2, -2, 0, 2, -1, 1]`, `target = 2`이다. 아래 표는 실행 결과가 아니라 각 prefix와 조회 빈도를 직접 계산한 추적이다. 조회 시점에는 현재 prefix가 아직 등록되지 않았다는 점에 주목한다.

| 오른쪽 경계 $r$ | $P[r]$ | 찾는 값 $P[r]-2$ | 앞선 출현 횟수 | 누적 개수 |
| --- | ---: | ---: | ---: | ---: |
| 1 | 2 | 0 | 1 | 1 |
| 2 | 0 | -2 | 0 | 1 |
| 3 | 0 | -2 | 0 | 1 |
| 4 | 2 | 0 | 3 | 4 |
| 5 | 1 | -1 | 0 | 4 |
| 6 | 2 | 0 | 3 | 7 |

예상 반환값은 **7**이다. 직접 경계를 열거하면 `[0, 1)`, `[0, 4)`, `[2, 4)`, `[3, 4)`, `[0, 6)`, `[2, 6)`, `[3, 6)`이다. 특히 $r=4$에서 $P[0]=P[2]=P[3]=0$이므로 기여가 3이다. 값 0이 하나의 키로 저장되더라도 빈도는 세 경계를 구별한다.

다음 경계 사례도 같은 불변식으로 손으로 확인할 수 있다. 별도 예제 문제를 늘리는 대신, 초기화와 순서가 틀렸을 때 어느 계약이 깨지는지 보여 준다.

| 입력과 목표 | 예상 개수 | 확인할 계약 |
| --- | ---: | --- |
| `[]`, `0` | 0 | 빈 구간 자체를 답으로 세지 않음 |
| `[0]`, `0` | 1 | 현재 prefix를 먼저 넣으면 잘못 2가 됨 |
| `[0, 0, 0]`, `0` | 6 | 같은 prefix의 빈도가 1, 2, 3으로 기여 |
| `[2]`, `2` | 1 | 초기 `{0: 1}`이 시작점 0을 나타냄 |
| `[2, -2]`, `-2` | 1 | 음수 목표에서도 차 관계가 유지됨 |

모든 원소가 0이고 목표도 0이면 가능한 모든 비어 있지 않은 구간이 답이다. 길이별 개수를 합하면 다음 상한을 얻는다. 이는 직접 유도한 개수이며, 알고리즘은 구간을 생성하지 않고 빈도만 더하므로 반환값이 이차적으로 커져도 반복 횟수는 선형이다.

$$
0\le\mathrm{answer}\le n+(n-1)+\cdots+1
=\frac{n(n+1)}{2}.
$$

이 예제의 입력 상한을 대입하면 prefix 절댓값은 최대 $2\times10^{14}$이고 구간 개수는 최대 $20000100000$이다. 이는 위에서 정한 제약과 개수 식으로 직접 계산한 상한이다. Python 정수는 고정 비트 폭에 묶이지 않지만, 그 사실이 임의로 큰 정수의 연산까지 상수 시간이라는 뜻은 아니다. 이 문서의 선형 시간은 정수 크기가 일정 범위에 머무는 연산 모형의 설명이다. 입력 정수의 자릿수도 증가하는 문제에서는 덧셈과 키 처리 비용을 별도로 고려해야 한다.[1,9]

빈 prefix를 준비하는 것과 빈 구간을 세는 것은 다르다. 전자는 왼쪽 경계 $l=0$을 허용하며, 후자는 $l=r$를 허용하는 것이다. 코드의 조회 후 삽입 순서는 두 조건을 분리한다. 이 작은 순서 차이가 특히 $K=0$에서 자기 자신과의 잘못된 짝을 막는다.[6,8]

## 5. 정렬된 배열의 Two pointers

### (1) 후보 제거의 근거

정렬된 배열에서 서로 다른 두 원소의 합이 $K$인 쌍 하나를 찾는 경우를 보자. 이 절의 `left`, `right`는 **두 원소의 인덱스**이므로 초기값이 0과 $n-1$이다. 앞의 구간 경계 `right`와 역할이 다르다. 배열이 비감소 순서이면 현재 합이 작을 때 왼쪽 원소를, 클 때 오른쪽 원소를 후보에서 제외할 수 있다.[1,2]

현재 위치를 $l<r$라 하자. 합이 작다면 현재 왼쪽 원소를 남은 어느 원소와 더해도 목표에 도달하지 못한다.[1,2]

$$
a[l]+a[r]<K
\quad\Longrightarrow\quad
 a[l]+a[j]\le a[l]+a[r]<K\quad(l<j\le r).
$$

따라서 $l$을 증가시켜도 정답을 놓치지 않는다. 반대로 합이 크면 현재 오른쪽 원소는 남은 어떤 왼쪽 후보와도 짝이 될 수 없다.[1,2]

$$
a[l]+a[r]>K
\quad\Longrightarrow\quad
 a[i]+a[r]\ge a[l]+a[r]>K\quad(l\le i<r).
$$

이때는 $r$을 감소시킨다. 핵심은 합을 목표에 가깝게 만들려는 직관이 아니라, 제거하는 행이나 열 전체가 불가능하다는 부등식이다. 배열에 음수가 있어도 정렬 관계는 성립하므로 이 쌍 찾기에서는 음수를 금지할 이유가 없다.[1,2]

### (2) 쌍 찾기와 원래 순서

아래 함수는 이미 정렬된 입력에서 인덱스 쌍 하나를 반환하며 없으면 `None`을 반환한다. 정렬 여부는 호출자가 보장한다. 같은 값을 가진 서로 다른 위치도 허용하지만, `left < right`이므로 같은 위치를 두 번 사용하지 않는다.[1,2]

```python
def pair_with_sum_sorted(a, target):
    left, right = 0, len(a) - 1
    while left < right:
        total = a[left] + a[right]
        if total == target:
            return left, right
        if total < target:
            left += 1
        else:
            right -= 1
    return None
```

매 반복에서 하나의 포인터가 한 칸 이동하고 되돌아가지 않으므로 스캔은 $O(n)$ 시간과 $O(1)$ 추가 공간을 사용한다. 정렬되지 않은 입력을 먼저 정렬한다면 일반적인 비교 정렬 비용을 포함하여 $O(n\log n)$ 시간이 필요하다. 반환할 위치가 원래 배열의 인덱스라면 값과 원래 인덱스를 함께 정렬해야 한다.[1,2,11]

아래 구분은 겉보기에는 비슷한 합 문제에서 정렬을 적용할 수 있는지 판단하는 기준이다. 이는 문제 정의에 따른 차이이다.

| 대상 | 순서 변경의 영향 | 이 절의 함수와 관계 |
| --- | --- | --- |
| 서로 다른 원소 두 개의 값 합 | 가능한 값 쌍은 유지됨 | 정렬 후 적용 가능 |
| 원래 인덱스 쌍 | 위치 정보가 바뀜 | 원래 인덱스를 함께 보관 |
| 원래 배열의 연속 구간 | 인접 관계가 바뀜 | 정렬하면 다른 문제가 됨 |
| 조건을 만족하는 모든 쌍의 개수 | 같은 값의 위치 수까지 필요 | 쌍 하나만 반환하는 함수로 해결되지 않음 |

예를 들어 `[2, -2, 0]`을 정렬하면 원래의 `[2, -2]`라는 연속 구간은 보존되지 않는다. 따라서 4절의 구간 개수 문제를 정렬된 두 원소의 합 문제로 바꾸어서는 안 된다. 정렬된 위치의 단조성과 원래 구간 합의 단조성은 별개의 조건이다.

## 6. Sliding window와 합의 단조성

### (1) 고정 길이 창

**Sliding window**는 배열의 연속 구간을 유지하며 경계를 이동하는 방식이다. 길이 $k$가 고정되면 합을 갱신할 때 빠지는 원소 하나와 들어오는 원소 하나만 처리하면 된다. $1\le k\le n$이고 $W_l=S(l,l+k)$라 하면 다음 정확한 관계를 얻는다. Prefix 항등식을 이웃한 두 창에 적용한 결과이며, Python 공식 문서의 이동 평균 예제도 같은 합 갱신을 사용한다.[2,12]

$$
W_{l+1}=W_l-a[l]+a[l+k]\quad(0\le l<n-k).
$$

이 식은 원소가 음수인지와 관계없다. 창 크기를 합에 맞추어 조절하는 판단이 없기 때문이다. 아래 함수는 각 길이 $k$ 구간의 합을 순서대로 반환한다. 첫 창은 직접 더하고 이후 창은 위 점화식을 사용한다.

```python
def fixed_window_sums(a, k):
    if not 1 <= k <= len(a):
        raise ValueError("window width must be between 1 and n")
    total = 0
    for i in range(k):
        total += a[i]
    result = [total]
    for right in range(k, len(a)):
        total += a[right] - a[right - k]
        result.append(total)
    return result
```

초기 $k$회 덧셈과 이후 $n-k$회 갱신을 합쳐 $O(n)$ 시간이다. 반환 리스트에는 $n-k+1$개의 값이 있으므로 출력 공간은 $O(n)$이고, 출력물을 제외한 상태는 상수 개 변수이다. Prefix 배열은 임의의 여러 구간을 조회할 때 유용하고, 이 구현은 고정 길이 창을 순서대로 한 번 훑을 때 필요한 상태만 유지한다.[2,12]

### (2) 비음수 합의 가변 길이 창

창 길이를 합 조건에 따라 바꾸려면 포인터를 되돌리지 않아도 되는 이유가 필요하다. 모든 원소가 비음수이고 합의 상한이 $B\ge0$이라고 하자. 합이 $B$를 넘으면 왼쪽 원소를 제거하여 조건을 회복하고, 회복된 창의 길이로 최장 길이를 갱신할 수 있다. 양수 입력에 대한 two-pointer 원리를 0까지 확장한 것으로, 필요한 성질은 엄격한 증가가 아니라 감소하지 않는다는 점이다.[1,2,11]

$$
a[i]\ge0
\quad\Longrightarrow\quad
S(l,r+1)\ge S(l,r),\qquad S(l+1,r)\le S(l,r).
$$

아래 함수는 정수 배열에서 합이 `budget` 이하인 연속 구간의 최대 길이를 반환한다. 가능한 비어 있지 않은 구간이 없으면 0이다. 입력 부호를 확인하는 순회도 $O(n)$에 포함된다. `right`는 새로 들어오는 원소의 인덱스이고, 갱신 후 창은 `[left, right + 1)`이다.

```python
def longest_sum_at_most(a, budget):
    if budget < 0 or any(value < 0 for value in a):
        raise ValueError("requires nonnegative values and budget")
    left = 0
    total = 0
    best = 0
    for right, value in enumerate(a):
        total += value
        while total > budget:
            total -= a[left]
            left += 1
        best = max(best, right + 1 - left)
    return best
```

축소가 끝난 뒤 `total`은 현재 창의 합이고 $B$ 이하이다. 이미 버린 더 왼쪽 시작점은 버릴 당시 합이 너무 컸다. 이후 비음수 원소만 더해지므로 그 시작점은 다시 유효해질 수 없다. 따라서 남은 `left`는 현재 오른쪽 경계에서 가능한 가장 이른 시작점이고, 이 창이 그 경계에서 가장 길다. 모든 오른쪽 경계의 최댓값을 취하면 전체 최장 길이가 된다. 이는 앞의 단조 부등식에서 직접 얻은 불변식 증명이다.[1,2,11]

반복문 안에 `while`이 있어도 `left`는 전체 실행 동안 최대 $n$번만 증가한다. `right`도 $n$번 진행하므로 총 이동 횟수는 선형이다. 0이 연속되어도 `total > budget`인 동안에는 위치를 계속 진행하며, 비음수 상한 아래에서는 늦어도 창을 비울 때 합 0이 되어 종료한다. `>`를 `>=`로 바꾸면 합이 상한과 같은 유효 구간도 제거하므로 다른 알고리즘이 된다.[1,2,11]

### (3) 음수와 개수 질의의 경계

음수를 허용하면 너무 큰 합을 가졌던 시작점이 나중에 다시 유효해질 수 있다. 직접 구성한 반례 `a = [4, -3, 2]`, $B=3$을 보자. 비음수 전용 규칙으로 처리하면 첫 값 4를 버린다. 그러나 전체 합은 $4-3+2=3$이므로 길이 3인 전체 구간이 유효하다. 이미 버린 시작점을 복구하지 않는 스캔은 이 답을 놓친다. 앞선 함수는 이런 입력을 명시적으로 거부한다.[1,2,8]

고정 창의 합에는 이러한 금지가 없으며, 음수 입력에서도 잘 정의된다. 또한 음수가 없더라도 **목표와 같은 합의 구간 개수**를 세는 문제는 단순히 유효 창 하나를 발견하는 문제와 다르다. 예를 들어 `[0, 0]`의 합이 0인 비어 있지 않은 구간은 3개이다. 오른쪽 끝마다 창 하나만 세면 중복 시작점을 놓친다. 4절의 빈도 방식은 이런 경우도 같은 코드로 처리한다.[6,8]

| 유지할 정보 | 원소 조건 | 필요한 근거 |
| --- | --- | --- |
| 고정 길이 창의 합 | 부호 제한 없음 | 나가는 값과 들어오는 값의 정확한 교체 |
| 합이 상한 이하인 최장 창 | 여기서는 모두 비음수 | 확장 시 합 비감소, 축소 시 합 비증가 |
| 목표 합인 모든 구간의 개수 | 부호 제한 없음 | 앞선 prefix 값의 빈도 |
| 고정 길이 창의 최솟값 | 부호 제한 없음 | 다음 절의 후보 우월성과 만료 시점 |

## 7. Monotonic deque와 이동 최솟값

### (1) 후보의 우월성과 만료

합은 빠지는 값을 빼면 되지만, 창의 최솟값이 빠졌을 때는 그다음 후보를 알아야 한다. **Monotonic deque**는 미래에 최솟값이 될 가능성이 있는 인덱스만 남긴다. 인덱스는 앞에서 뒤로 증가하고, 대응하는 값도 증가하도록 관리한다. 창 밖으로 나간 인덱스는 앞에서, 새 값보다 크거나 같은 이전 후보는 뒤에서 제거한다.[1,13]

뒤에서 제거해도 되는 이유는 위치와 값에 모두 있다. 이전 후보 $i$보다 새 후보 $j$가 나중에 들어왔고 값도 작거나 같다고 하자.[1,13]

$$
i<j,\qquad a[j]\le a[i].
$$

이후 $i$가 남아 있는 모든 창에는 더 최근에 들어온 $j$도 남아 있다. 따라서 이전 후보 $i$는 최소 **값**을 결정하는 데 필요하지 않다. 이 주장은 창의 오른쪽 경계와 왼쪽 경계가 앞으로만 움직일 때 성립한다. 같을 때도 이전 후보를 제거하면 같은 값 중 가장 늦게 만료되는 위치를 남긴다. 최솟값의 가장 이른 인덱스를 요구하는 다른 문제라면 동률 처리 규칙부터 바꾸어야 한다.[1,13]

### (2) 구현과 분할 상환 분석

아래 함수는 길이 $k$인 모든 창의 최솟값을 반환한다. `deque`는 양 끝 삽입·삭제를 지원하며, 코드에서는 `popleft()`로 만료된 앞 원소를, `pop()`으로 지배된 뒤 후보를 제거한다. 이 양 끝 삽입·삭제는 $O(1)$ 연산이다.[12,14]

```python
from collections import deque


def sliding_minimum(a, k):
    if not 1 <= k <= len(a):
        raise ValueError("window width must be between 1 and n")
    candidates = deque()
    result = []
    for right, value in enumerate(a):
        left = right - k + 1
        while candidates and candidates[0] < left:
            candidates.popleft()
        while candidates and a[candidates[-1]] >= value:
            candidates.pop()
        candidates.append(right)
        if right >= k - 1:
            result.append(a[candidates[0]])
    return result
```

원소마다 삽입은 한 번이고, 뒤에서 지배되어 제거되거나 앞에서 만료되어 제거되는 일은 합쳐 최대 한 번이다. 어떤 반복에서 후보 여러 개를 한꺼번에 지우더라도 전체 삭제 수는 $n$을 넘지 않는다. 따라서 총 시간은 $O(n)$이며 각 반복이 최악 $O(1)$이라는 주장은 아니다. Deque에는 현재 창 안의 인덱스만 남으므로 작업 공간은 $O(k)$, 출력 공간은 별도로 $O(n)$이다.[1,12,13]

직접 정한 `a = [4, 2, 2, 5, 1]`, $k=3$의 추적은 더 작거나 같은 값이 들어올 때 뒤쪽 후보를 제거하는 과정을 보여 준다. 후보는 `(인덱스: 값)`으로 표기했다.

| 새 인덱스 | 제거 내용 | 삽입 후 후보 | 완성된 창의 최솟값 |
| --- | --- | --- | ---: |
| 0 | 없음 | `0:4` | 아직 길이 부족 |
| 1 | 뒤의 `0:4` | `1:2` | 아직 길이 부족 |
| 2 | 동률인 `1:2` | `2:2` | 2 |
| 3 | 없음 | `2:2, 3:5` | 2 |
| 4 | 뒤의 `3:5`, `2:2` | `4:1` | 1 |

값만 저장하면 같은 값의 어느 위치가 만료되었는지 따로 구별해야 한다. 인덱스를 저장하면 유효 범위를 `candidates[0] < left`로 직접 확인할 수 있다. $k=1$이면 매번 현재 원소 하나가 답이며, $k=n$이면 전체 배열의 최솟값 하나가 출력된다. 합과 달리 최솟값의 갱신은 역연산보다 **필요 없어진 후보를 증명하여 버리는 것**에 의존한다.[1,13]

## 8. 동적 구간 질의와 자료구조 선택

### (1) 조회와 갱신의 조합

원소 하나가 바뀌면 그 뒤의 prefix 합들도 바뀐다. 따라서 정적 prefix 배열의 $O(1)$ 질의 성능만 보고 갱신이 섞인 작업에 그대로 적용하면, 갱신마다 최악 $O(n)$을 사용하게 된다. **Fenwick tree**는 합을 여러 크기의 블록에 저장하고, **segment tree**는 구간을 나누어 각 부분의 요약을 저장하여 이 비용을 줄인다.[1,3,5]

다음 표는 앞에서 다룬 연산과 이후 두 구현의 계약을 비교한다. $n$은 배열 길이, $q$는 일괄 갱신 수이다. 추가 공간에서 반환 결과는 제외한다.[1,3,4,5]

| 작업 | 알맞은 기본 구조 | 주요 시간 | 추가 공간 |
| --- | --- | --- | --- |
| 변경 없이 구간 합 반복 | Prefix 배열 | 전처리 $O(n)$, 질의 $O(1)$ | $O(n)$ |
| 구간 가산 후 최종 배열만 필요 | Difference array | 전체 $O(n+q)$ | $O(n)$ |
| 점 가산과 구간 합이 교차 | Fenwick tree | 각 연산 $O(\log n)$ | $O(n)$ |
| 점 대입과 합·최솟값 등의 구간 결합 | Segment tree | 각 연산 $O(\log n)$ | $O(n)$ |
| 구간 가산과 점 조회가 교차 | 차분을 저장한 Fenwick tree | 각 연산 $O(\log n)$ | $O(n)$ |

마지막 행은 difference array의 두 경계 사건을 두 번의 점 갱신으로 처리하고, 현재 위치까지 차분의 합을 조회하는 구성이다.[1,5] 반면 구간 전체의 가산과 구간 합을 모두 빠르게 처리하는 기능은 아래의 기본 코드에 포함되어 있지 않다. 이 두 연산을 함께 지원하려면 lazy propagation처럼 여러 원소의 갱신을 노드에 지연 저장하는 별도 확장을 설계해야 한다.[1,3]

### (2) Fenwick tree의 인덱스 변환

Fenwick tree의 내부 인덱스는 $1$부터 $n$까지 사용한다. 양의 정수 $i$에 대해 $b(i)=i\mathbin{\&}(-i)$를 가장 낮은 1 비트에 대응하는 값이라 정의하자. 내부 칸 `tree[i]`는 0-based 원배열의 반열린 구간 $[i-b(i),i)$의 합을 저장한다.[1,5]

$$
\mathrm{tree}[i]=\sum_{j=i-b(i)}^{i-1}a[j],
\qquad b(i)=i\mathbin{\&}(-i).
$$

예를 들어 내부 인덱스 6은 이진수 `110`이므로 $b(6)=2$이고 원배열 `[4, 6)`의 합을 담는다. `prefix_sum(6)`은 내부 인덱스 6, 4를 읽어 `[4, 6)`과 `[0, 4)`를 결합한다. 내부 인덱스에서 낮은 비트를 제거하며 내려가므로 겹치지 않는 블록으로 앞부분이 분해된다.[1,5]

다음 구현의 외부 인덱스는 계속 0-based이다. `add(index, delta)`만 내부에서 1을 더하며, `prefix_sum(end)`는 처음부터 경계 인덱스 `end`를 받으므로 더하지 않는다. `prefix_sum(0)`은 아무 블록도 읽지 않고 0을 반환한다.[1,5]

```python
class Fenwick:
    def __init__(self, n):
        if n < 0:
            raise ValueError("negative size")
        self.n = n
        self.tree = [0] * (n + 1)

    def add(self, index, delta):
        if not 0 <= index < self.n:
            raise IndexError("invalid index")
        i = index + 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    def prefix_sum(self, end):
        if not 0 <= end <= self.n:
            raise IndexError("invalid prefix boundary")
        total = 0
        i = end
        while i > 0:
            total += self.tree[i]
            i -= i & -i
        return total

    def range_sum(self, left, right):
        if not 0 <= left <= right <= self.n:
            raise IndexError("invalid half-open range")
        return self.prefix_sum(right) - self.prefix_sum(left)
```

각 반복은 다음 상위 갱신 블록으로 이동하거나 prefix의 마지막 블록을 제거한다. $n\ge1$에서 조회와 갱신은 $O(\log n)$개 블록을 처리하며 저장 공간은 $O(n)$이다. `add`는 **새 값 대입이 아니라 변화량 더하기**이다. 현재 값을 $u$에서 $v$로 바꾸려면 변화량 $v-u$를 더해야 하므로 기존 값을 별도로 보관하거나 한 점의 합으로 조회한다.[1,5]

갱신 방향도 같은 블록 정의로 확인할 수 있다. 크기 8에서 외부 인덱스 4에 값을 더하면 내부 인덱스는 5로 시작하여 5, 6, 8 순서로 바뀐다. 각 블록은 원배열의 `[4, 5)`, `[4, 6)`, `[0, 8)`이며 모두 갱신 위치 4를 포함한다. 반면 외부 경계 4까지의 합에는 그 원소가 포함되지 않으므로 `prefix_sum(4)`는 영향받지 않는다. 조회 `prefix_sum(5)`는 블록 5와 4를 읽어 새 값을 한 번만 포함한다. 이는 원문의 내부 1-based 정의를 이 코드의 외부 반열린 구간으로 바꾼 수작업 추적이다.[1,5]

이 클래스는 영 배열로 시작한다. 초기 배열을 넣으려면 각 `(index, value)`에 `add`를 호출할 수 있으며, 그 구성법의 시간은 $O(n\log n)$이다. 크기 0에서는 `[0, 0)` 합이 0이고 갱신할 유효 원소는 없다. 반복 갱신으로 구성하는 비용은 앞서 설명한 점 갱신 비용을 $n$번 합한 결과이다.[1,5]

### (3) Segment tree의 결합과 경계 이동

Segment tree는 각 노드에 구간의 요약을 저장하고 두 자식의 요약을 결합한다. 합에서는 덧셈을, 최솟값에서는 `min`을 사용한다. 핵심은 두 구간의 정보를 다시 결합할 수 있다는 것이며, prefix 차처럼 역연산을 요구하지 않는다. 순서를 보존한 결합의 결합법칙과 빈 구간을 표현하는 항등원을 정해야 한다.[15,16]

$$
\operatorname{merge}(\operatorname{merge}(x,y),z)
=\operatorname{merge}(x,\operatorname{merge}(y,z)),
\qquad \operatorname{merge}(e,x)=\operatorname{merge}(x,e)=x.
$$

$x,y,z$는 인접한 구간의 요약값이고 $e$는 빈 구간 요약이다. 합의 항등원은 0, 최솟값의 항등원은 양의 무한대이다. 결합법칙은 구간을 어떻게 묶든 결과가 같다는 조건이다. 서로 다른 순서로 바꾸어도 된다는 교환법칙과는 구별해야 한다. 아래에서는 정수 합만 구현하여 결합 연산과 항등원을 코드에서 고정한다.[15,16]

리프 수 `size`를 $n$ 이상인 가장 작은 2의 거듭제곱으로 잡고 남는 칸에는 0을 채운다. 리프는 `tree[size + i]`, 부모는 두 자식의 합이며 인덱스 1이 루트이다. `set_value`는 한 점을 **대입**하고, `range_sum`은 반열린 구간의 합을 반환한다.[1,3]

```python
class SegmentSum:
    def __init__(self, a):
        self.n = len(a)
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.tree = [0] * (2 * self.size)
        for i, value in enumerate(a):
            self.tree[self.size + i] = value
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def set_value(self, index, value):
        if not 0 <= index < self.n:
            raise IndexError("invalid index")
        i = self.size + index
        self.tree[i] = value
        i //= 2
        while i:
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]
            i //= 2

    def range_sum(self, left, right):
        if not 0 <= left <= right <= self.n:
            raise IndexError("invalid half-open range")
        left += self.size
        right += self.size
        total = 0
        while left < right:
            if left & 1:
                total += self.tree[left]
                left += 1
            if right & 1:
                right -= 1
                total += self.tree[right]
            left //= 2
            right //= 2
        return total
```

질의에서 `left`가 오른쪽 자식이면 그 왼쪽 형제는 질의 밖에 있으므로 현재 노드만 답에 넣고 `left`를 증가시킨다. `right`는 제외 경계이므로 홀수이면 **먼저 하나 줄인 노드**를 포함한다. 양쪽의 남은 경계가 짝수가 된 뒤 부모로 올라가면 남은 구간이 정확히 두 칸씩 묶인다. `total`에 이미 더한 구간과 아직 처리하지 않은 구간은 겹치지 않고 합쳐서 원래 질의를 이룬다는 것이 이 반복문의 불변식이다.[1,3]

리프 수가 8일 때 `[1, 7)`을 조회하는 경계 이동을 손으로 추적하면 다음과 같다. 표의 노드 번호는 내부 배열 인덱스이며 원배열 인덱스와 다르다.

| 반복 시작 `(left, right)` | 이번에 더하는 노드 | 해당 원배열 구간 | 다음 경계 |
| --- | --- | --- | --- |
| `(9, 15)` | 9, 14 | `[1, 2)`, `[6, 7)` | `(5, 7)` |
| `(5, 7)` | 5, 6 | `[2, 4)`, `[4, 6)` | `(3, 3)` |

각 높이에서 경계 쪽 노드 두 개까지만 답에 더하고 남은 구간을 위로 올린다. 따라서 질의와 점 갱신은 $O(\log n)$이고, $n\ge1$이면 $n\le\mathrm{size}<2n$이므로 생성 시간과 공간은 $O(n)$이다. 빈 배열은 코드에서 크기 1의 영 리프를 쓰며 `[0, 0)`만 유효한 질의이다.[1,3]

점 갱신은 해당 리프에서 루트로 이어지는 경로만 바꾼다. 갱신 위치를 포함하지 않는 노드는 이전 요약을 그대로 유지하므로, 다음 질의는 변경된 블록과 변경되지 않은 블록을 구별 없이 결합할 수 있다. 반대로 구간 전체를 바꾸면서 각 리프의 `set_value`를 호출하면 구간 길이에 비례한 갱신 수가 발생한다. 기본 트리를 사용한다는 이유만으로 구간 갱신도 한 번의 $O(\log n)$ 연산이 되지는 않는다. Lazy propagation은 여러 원소에 미칠 갱신을 노드에 지연 저장하는 별도 설계이며, 본문의 점 대입 함수와 구분해야 한다.[1,3]

합을 최솟값으로 바꾸려면 부모 계산뿐 아니라 질의 누적, 항등원과 패딩도 함께 바꾸어야 한다. 더 일반적인 순서 의존 결합으로 확장할 때는 왼쪽 누적값과 오른쪽 누적값을 따로 두고 원래 순서대로 결합한다. 위 코드는 덧셈의 교환법칙을 이용해 누적값 하나로 단순화한 것이므로, 연산 기호만 치환하면 어떤 요약에도 사용할 수 있는 범용 구현은 아니다. 이는 앞의 순서 보존 조건을 코드에 적용한 결론이다.[15,16]

## 9. 핵심 정리

구간 문제에서는 먼저 무엇을 보존해야 하는지 결정한다. Prefix sum은 경계까지의 합을, difference array는 갱신의 시작과 종료를 저장한다. Two pointers와 가변 창은 버린 후보가 다시 필요하지 않다는 단조성을 요구하고, monotonic deque는 값과 만료 순서가 모두 열세인 후보를 제거한다. 값의 수정이 질의와 교차하면 블록별 요약을 갱신하는 트리로 넘어간다.[1,2,3,5,13]

구현을 읽을 때는 인덱스가 원소인지 경계인지, 입력을 정렬해도 되는지, 같은 값의 다른 위치를 몇 번 세는지 확인한다. 특히 목표 합 구간 개수의 빈도표는 **현재 경계보다 앞선 prefix만** 담아야 한다. 이 불변식을 유지하면 음수, 0, 중복 prefix와 시작점 0을 같은 함수로 처리할 수 있다.[6,8]

## 10. 참고문헌

1. Antti Laaksonen, *Competitive Programmer's Handbook* (2018), Chapters 1, 8–9; Section 28.1, “Lazy propagation.” [Original PDF](https://cses.fi/book/book.pdf).
2. Darren Yao, *An Introduction to the USA Computing Olympiad*, C++ Edition (2020), Sections 11.1–11.2, 14.1. [Original PDF](https://darrenyao.com/usacobook/cpp.pdf).
3. cp-algorithms contributors, “Segment Tree,” construction, sum queries, update queries, range updates (lazy propagation). [Technical reference](https://cp-algorithms.com/data_structures/segment_tree.html).
4. Zhongtang Luo, “CS 31100, Competitive Programming II (Fall 2023),” Purdue University, Topics 1–3. [Course material](https://www.cs.purdue.edu/homes/luo401/teaching/cs311-fall2023/index.html).
5. cp-algorithms contributors, “Fenwick Tree,” one-based indexing and range operations. [Technical reference](https://cp-algorithms.com/data_structures/fenwick.html).
6. USACO Guide, “Solution — Subarray Sums II (CSES).” [Explanation](https://usaco.guide/problems/cses-1661-subarray-sums-ii/solution).
7. BITS Pilani, CS F211, *Data Structures and Algorithms: Practice Problems — Hashmaps, AVL Trees, and Red-Black Trees*, Problem 1. [Original PDF](https://www.bits-pilani.ac.in/wp-content/uploads/Homework7-Hashmaps-AVL-RBT.pdf).
8. Kyle and Freddie, “Hashing In The Real World,” UNSW Competitive Programming and Mathematics Society, T1 Week 4 (2024), slides 17–18. [Original slides](https://unswcpmsoc.com/workshops/programming/2024/t1w4.pdf).
9. Python Software Foundation, “Built-in Types,” numeric types, mapping types, `dict.get`. [Official documentation](https://docs.python.org/3/library/stdtypes.html#dict.get).
10. Carnegie Mellon University, Computer Science 15-112 (Fall 2011), “Class Notes: Dictionaries (Maps),” dictionary operations and the `mostFrequent` example using `get`. [Course notes](https://www.cs.cmu.edu/afs/cs/academic/class/15112-f11/www/handouts/notes-dictionaries.html).
11. USACO Guide, “Two Pointers.” [Tutorial](https://usaco.guide/silver/two-pointers).
12. Python Software Foundation, “collections — Container datatypes,” `deque`, `deque` recipes. [Official documentation](https://docs.python.org/3/library/collections.html#collections.deque).
13. cp-algorithms contributors, “Minimum Stack / Minimum Queue,” queue methods 1–2. [Technical reference](https://cp-algorithms.com/data_structures/stack_queue_modification.html).
14. University of Michigan, ROB 502: Programming for Robotics (Fall 2020), “Class 11,” “Stacks, queues, and double-ended queues.” [Course material](https://robotics.umich.edu/academics/courses/online-courses/rob502-f20/class11/).
15. AtCoder Library, “Segtree,” monoid contract, constructor and `prod`. [Official documentation](https://atcoder.github.io/ac-library/production/document_en/segtree.html).
16. Stanford University, CS240H (Winter 2016), “Phantoms,” sections “Monoids” and “Monoids for numbers.” [Lecture slides](https://www.scs.stanford.edu/16wi-cs240h/slides/phantoms.html).
