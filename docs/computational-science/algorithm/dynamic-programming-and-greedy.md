---
description: 상태와 점화식에서 출발해 Python으로 경로·배낭·부분수열·구간·부분집합 동적 계획법과 교환 논증에 기반한 탐욕 알고리즘을 설명한다.
---

# Dynamic programming and greedy algorithms

Dynamic programming (DP)는 같은 부분문제를 반복해서 풀지 않도록 답을 저장하고 재사용하는 방법이다. Greedy algorithm은 매 단계 하나의 선택을 확정한다. 두 방법의 차이는 배열이나 정렬의 사용 여부가 아니라, 미래의 가능성을 어떤 근거로 합치거나 버리는가에 있다. DP는 상태가 담아야 할 정보를 정의하고, greedy는 당장의 선택을 포함하는 최적해가 존재함을 증명해야 한다.[1,2,3]

이 문서는 유한한 이산 상태를 다룬다. 코드는 Python 3.10 이상을 기준으로 작성하며, 입력은 별도 언급이 없으면 정수 리스트이다. 코드와 수작업 추적표는 설명을 위해 직접 구성한 예시이다. 제시한 예상 결과는 점화식과 불변식으로 검산한 값이며 실행 결과가 아니다. 시간 복잡도는 정수 덧셈·비교와 배열 접근을 기본 연산으로 세는 기준이다. 경우의 수나 비용의 정수 자릿수가 커지면 실제 비트 연산 비용도 추가된다.[1,4]

## 1. 상태와 점화식

### (1) 상태의 충분성

상태는 부분문제를 구별하는 정보이다. 같은 상태로 합칠 두 이력이 앞으로 허용하는 선택과 그 선택에 따른 추가 비용이 같아야, 과거의 세부 경로를 버려도 된다. 예를 들어 한 번씩만 선택할 수 있는 항목에서는 남은 용량만으로 부족하다. 어떤 항목까지 고려했는지도 필요하다. 반대로 모든 항목을 반복 사용할 수 있다면 남은 용량만으로 후속 문제가 결정될 수 있다.[1,4,5]

상태를 정할 때에는 “지금까지 가장 좋았던 값”이라는 표현보다, 어떤 입력 범위와 제약 아래의 답인지를 먼저 적는다. 다음 표는 서로 다른 정보를 저장하는 대표 상태이다. 아래 식과 코드에서는 표에 제시한 기호를 해당 절 안에서 사용한다.[1,4,5]

| 대상 | 상태가 뜻하는 부분문제 | 빠뜨리면 안 되는 정보 |
| --- | --- | --- |
| 0–1 배낭 | 처음 $i$개 항목, 용량 상한 $c$에서의 최대 보상 | 사용 가능한 항목의 범위 |
| 격자 경로 | 시작점에서 $(r,c)$까지 도달한 경로의 답 | 위치와 이동 제약 |
| 증가 부분수열 | 인덱스 $i$에서 끝나는 최대 길이 | 마지막 원소의 위치 |
| 구간 분할 | 반열린 구간 $[i,j)$를 처리하는 최소 비용 | 양 끝과 결합 비용 |
| 부분집합 경로 | 방문 집합 $S$, 마지막 정점 $v$의 최소 비용 | 방문 여부와 현재 위치 |

이 정보가 충분하면 최적해의 마지막 선택을 제거하여 더 작은 상태로 옮길 수 있다. 남은 부분이 그 상태의 최적해가 아니라면 더 좋은 부분해로 교체하여 전체도 개선할 수 있다. 이 교체 논증이 **optimal substructure**의 근거이다. 단, 전역 제약을 상태에서 지운 채 이 논증을 적용하면 틀린 점화식이 된다. 예를 들어 “특정 종류는 최대 두 개”라는 제약이 새로 생기면 그 사용 개수까지 구별해야 한다.[1,4,5]

### (2) 기저값과 불가능 상태

기저값은 재귀가 끝나는 작은 문제의 실제 답이다. 불가능 상태는 답이 없다는 뜻이다. 또한 아직 계산하지 않았다는 상태도 이 둘과 구별해야 한다. `0`이 정답일 수 있는데 `if dp[state]`로 계산 여부를 판단하면, 이미 계산한 상태를 반복 처리할 수 있다.[1,2,6]

| 목적 | 시작 상태 | 불가능 상태 | 결합 방식 |
| --- | --- | --- | --- |
| 경로 수 | 빈 경로 한 개이므로 `1` | `0` | 서로 다른 경우의 수를 더함 |
| 최소 비용 | 시작 비용 `0` | 수식의 $+\infty$, 코드의 `None` | 가능한 후보의 최솟값 |
| 최대 보상 | 문제에서 정한 시작 보상 | 수식의 $-\infty$, 코드의 `None` | 가능한 후보의 최댓값 |
| 존재 여부 | 빈 구성은 `True` | `False` | 논리합 |

용량 **이하**를 사용하는 배낭에서 빈 선택을 허용하면, 항목이 없을 때 모든 용량의 최대 보상은 0이다. 정확히 용량을 채워야 한다면 용량 0만 가능하고 나머지는 불가능하다. 두 문제는 같은 전이식처럼 보여도 초기화가 다르다. 이 차이를 수작업으로 확인하려면 무게 3인 항목 하나와 목표 용량 2를 생각하면 된다. “2 이하”의 답은 빈 선택, “정확히 2”의 답은 불가능이다.[4,5]

### (3) 의존 순서와 계산 비용

부분문제가 더 작은 부분문제에만 의존하면 그 의존 관계는 directed acyclic graph (DAG)를 이룬다. 선행 상태에서 그것을 사용하는 상태로 간선을 그렸을 때, 모든 선행 상태를 먼저 계산하는 순서가 유효하다. 정수 인덱스를 증가시키는 순서가 언제나 답은 아니다. 접미사 상태는 인덱스 감소 순서가, 구간 상태는 길이 증가 순서가 필요할 수 있다.[1,4,5]

상태 집합을 $\mathcal S$, 상태 $s$의 계산에서 확인하는 전이 수를 $d(s)$라 하자. 각 전이의 비용이 상수이고 상태 저장소 초기화 비용도 포함하면, 전체 기본 연산 횟수는 다음과 같이 평가한다.[1,4,5]

$$
T=O\!\left(|\mathcal S|+\sum_{s\in\mathcal S}d(s)\right).
$$

“상태 수 × 상태당 최대 전이 수”는 이 합의 편리한 상한이다. 부분집합이 상태이면 상태 수부터 지수적일 수 있다. 또 의존 관계가 순환하는데 캐시만 붙여서는 먼저 계산할 값을 얻을 수 없다. 방문 제한이나 단계 수를 상태에 추가하여 순환을 제거할 수 있는지, 다른 그래프 알고리즘이 필요한지부터 판단해야 한다.[1,4]

## 2. Memoization과 tabulation

Memoization은 재귀적으로 요청한 상태의 답을 저장한다. Tabulation은 의존 순서에 따라 표를 채운다. 두 구현이 같은 상태 정의와 점화식을 사용하면 같은 답을 구한다. 다만 memoization은 시작 상태에서 실제 요청되는 부분문제만 방문하는 반면, 조밀한 표를 사용하는 tabulation은 정의한 범위를 모두 순회한다.[1,4,6]

양의 정수 단위 `units`를 여러 번 사용하여 `target`을 만드는 최소 개수를 생각하자. 단위 중복은 없다고 가정한다. `memo`에 키가 있다는 사실은 계산 완료를, 값 `None`은 불가능을 나타낸다. 아래 함수는 이 구분을 보이기 위한 재귀 구현이다.[2,6]

```python
def min_units_memo(units: list[int], target: int) -> int | None:
    if target < 0 or any(unit <= 0 for unit in units):
        raise ValueError("invalid target or unit")
    memo: dict[int, int | None] = {0: 0}

    def solve(amount: int) -> int | None:
        if amount in memo:
            return memo[amount]
        best = None
        for unit in units:
            if unit <= amount:
                previous = solve(amount - unit)
                if previous is not None:
                    candidate = previous + 1
                    if best is None or candidate < best:
                        best = candidate
        memo[amount] = best
        return best

    return solve(target)
```

모든 단위가 양수이므로 `amount - unit`은 엄격히 작아진다. `units=[2,5]`, `target=7`이면 2를 먼저 빼든 5를 먼저 빼든 두 개로 만들 수 있다. `target=3`이면 1을 만들 수 없어 `None`이다. 단위 0을 허용하면 같은 상태를 다시 호출하므로 위 종료 논증이 무너진다. 계산 중 입력 자체가 변해서도 안 된다. 캐시는 동일한 부분문제에 대한 답을 재사용하기 때문이다.[1,2,6]

같은 문제를 아래처럼 양을 증가시키며 계산할 수 있다. 재귀 호출 없이 `0`에서 `target`까지의 선행 값을 사용한다.[2,6]

```python
def min_units_table(units: list[int], target: int) -> int | None:
    if target < 0 or any(unit <= 0 for unit in units):
        raise ValueError("invalid target or unit")
    dp: list[int | None] = [None] * (target + 1)
    dp[0] = 0
    for amount in range(1, target + 1):
        for unit in units:
            if unit <= amount and dp[amount - unit] is not None:
                candidate = dp[amount - unit] + 1
                if dp[amount] is None or candidate < dp[amount]:
                    dp[amount] = candidate
    return dp[target]
```

단위 수가 $k$, 목표가 $A$이면 위 반복문은 $O(kA)$번의 후보를 확인하고 $O(A)$개 값을 저장한다. Memoization도 최악에는 같은 수의 상태를 계산하지만 재귀 호출 스택을 추가로 사용한다. 이 예시에서 단위 1이 있으면 호출 깊이가 $A$까지 늘 수 있으므로 큰 입력에서는 반복 구현을 선택한다. 캐시가 재귀 깊이까지 줄여 주는 것은 아니다.[1,2,4]

| 선택 기준 | Memoization | Tabulation |
| --- | --- | --- |
| 상태 방문 | 요청된 상태부터 계산 | 미리 정한 순서로 계산 |
| 상태가 드문 경우 | 불필요한 상태 방문을 피할 수 있음 | 조밀한 표는 전체 범위를 처리 |
| 의존 순서 표현 | 재귀 호출에 나타남 | 반복문에 직접 나타남 |
| 메모리 검토 | 캐시와 호출 스택 | 표와 살아 있는 선행 행 |

## 3. 경로와 경우의 수

### (1) 격자 경로

오른쪽 또는 아래로만 이동하는 직사각형 격자에서는, 시작점 이외의 칸에 들어오는 마지막 이동이 위쪽 또는 왼쪽에서 온다. 따라서 두 선행 상태의 답을 결합할 수 있다. 두 집합은 마지막 간선이 달라 겹치지 않으므로 경로 수는 더하고, 최대 보상은 더 큰 선행 보상을 고른다.[2,7]

문헌 [2]는 양의 보상을, [7]은 장애물과 0·1 보상 및 최대 보상 경로의 수를 다룬다. 여기서는 두 자료의 마지막 이동 분할을 이용해 임의의 정수 보상으로 확장한다. 이는 원문의 입력 조건을 그대로 옮긴 것이 아니라 이 문서의 유도이다. 모든 보상을 0으로 두면 가능한 경로가 모두 최대 보상 경로가 되므로 [7]의 경로 수는 모든 경로의 수로 특수화된다.[2,7]

$N(r,c)$를 시작점 $(0,0)$에서 $(r,c)$까지의 경로 수, $R(r,c)$를 그 경로의 최대 누적 보상, $a_{r,c}$를 현재 칸의 보상이라 하자. 시작점 보상도 포함한다. 통행 가능한 시작점의 값은 각각 1과 $a_{0,0}$이다. 다른 통행 가능 칸에서는 다음 정확한 점화식을 쓴다. 격자 밖과 장애물의 값은 각각 0과 $-\infty$로 둔다.[2,7]

$$
\begin{aligned}
N(r,c)&=N(r-1,c)+N(r,c-1),\\
R(r,c)&=a_{r,c}+\max\{R(r-1,c),R(r,c-1)\}.
\end{aligned}
$$

보상이 음수여도 오른쪽·아래 이동만 허용하면 의존 관계는 비순환이므로 같은 분할 논증이 성립한다. 그러나 불가능한 선행 보상을 0으로 두면 경계 밖에서 새로 출발하는 가짜 경로가 선택될 수 있다. 예를 들어 한 행의 보상이 `[-5,-2]`이면 도착 보상은 `-7`이며 `-2`가 아니다. 이것은 양수 격자의 편의적 경계 처리를 음수 격자에 그대로 옮길 수 없는 이유이다.[2,7]

다음 함수는 장애물 격자의 경로 수만 반환한다. `blocked[r][c]`가 참이면 통행할 수 없다. 직사각형 입력을 검사하고 빈 격자의 경로 수는 0으로 정한다. `dp[c]`는 갱신 전에는 위쪽 칸의 값이고, `dp[c-1]`은 갱신 후의 왼쪽 칸 값이다.[2,7]

```python
def count_grid_paths(blocked: list[list[bool]]) -> int:
    if not blocked:
        return 0
    width = len(blocked[0])
    if any(len(row) != width for row in blocked):
        raise ValueError("ragged grid")
    if width == 0:
        return 0
    dp = [0] * width
    dp[0] = 1
    for row in blocked:
        for col in range(width):
            if row[col]:
                dp[col] = 0
            elif col > 0:
                dp[col] += dp[col - 1]
    return dp[-1]
```

가운데 칸만 막힌 $3\times3$ 격자를 위에서 아래로 수작업 추적하면 다음과 같다. 장애물에서 값을 0으로 지우지 않으면 이전 행의 경로가 그 칸을 통과한 것처럼 남는다. 높이 $h$, 너비 $w$에서 연산 수는 $O(hw)$, 보조 공간은 $O(w)$이다. `dp[0]=1`도 시작점이 막혔으면 첫 반복에서 0으로 지워진다.[2,7]

| 처리한 행 | 장애물 위치 | 행 처리 뒤 `dp` |
| --- | --- | --- |
| 첫 행 | 없음 | `[1, 1, 1]` |
| 둘째 행 | 가운데 | `[1, 0, 1]` |
| 셋째 행 | 없음 | `[1, 1, 2]` |

### (2) 순서와 조합

수를 센다는 목적만으로는 점화식이 결정되지 않는다. `[1,2]`와 `[2,1]`을 다른 결과로 볼지부터 정해야 한다. 아래 유도는 마지막 선택별 경로 수를 더하는 원리와, 사용 가능한 종류를 상태에 보존하는 원리를 결합한다. 전자는 [2]의 동전 나열과 [7]의 격자 경로에서, 후자는 [4]의 배낭 상태와 [8]의 complete knapsack에서 확인할 수 있다. [4,8]의 최적값 식을 곧바로 경우의 수 식으로 읽는 것은 아니며, 덧셈을 쓰려면 경우들이 빠짐없이 나뉘고 겹치지 않음을 별도로 증명해야 한다.[2,4,7,8]

양의 서로 다른 단위 집합 $U$로 합 $x$를 만드는 **순서 있는 나열**의 수를 $A(x)$라 하자. 마지막 단위가 $u$인 나열에서 그 단위를 지우면 합 $x-u$의 나열과 일대일 대응한다. 서로 다른 마지막 단위의 경우는 겹치지 않고 모든 비어 있지 않은 나열을 포함한다. 따라서 다음 식이 성립한다. $A(0)=1$이며 음수 합의 값은 0이다. 이는 [2]의 식을 마지막 이동별 분할 원리로 다시 유도한 것이다.[2,7]

$$
A(x)=\sum_{u\in U,\ u\le x}A(x-u)\qquad(x>0).
$$

합을 바깥 반복문으로 두면 각 마지막 단위가 별도의 경우를 만든다. 단위가 양수이므로 읽는 합은 모두 현재 합보다 작고 이미 계산되어 있다. 아래 핵심 부분에서 `target`은 음이 아닌 정수이며 `units`는 중복 없는 양의 정수 리스트이다.[2,7]

```python
ordered = [0] * (target + 1)
ordered[0] = 1
for amount in range(1, target + 1):
    for unit in units:
        if unit <= amount:
            ordered[amount] += ordered[amount - unit]
```

반면 단위별 사용 개수만 구별하는 **조합**은 항목 종류를 상태에 포함한다. 첫 $i$개 종류로 합 $x$를 만드는 수를 $B(i,x)$, 그중 마지막 단위를 $u_i$라 하자. 사용 개수 벡터에서 $u_i$의 개수가 0인 경우는 $B(i-1,x)$이다. 개수가 양수인 경우에는 그 개수를 하나 줄여 $B(i,x-u_i)$의 벡터와 일대일 대응시킨다. 두 경우는 마지막 성분의 0 여부로 나뉘므로 겹치지 않으며, 가능한 벡터를 모두 포함한다. 이 분할과 앞서 확인한 덧셈 원리로 다음 식을 직접 유도한다. $B(0,0)=1$, $B(0,x>0)=0$이며 두 번째 항은 $x\ge u_i$일 때만 존재한다.[2,4,7,8]

$$
B(i,x)=B(i-1,x)+B(i,x-u_i).
$$

이를 한 배열로 압축할 때 종류 $i$의 반복이 시작되면 모든 칸은 $B(i-1,x)$이다. 합 $x$를 증가시키며 처리하면 갱신 전 현재 칸은 여전히 $B(i-1,x)$이고, 더 작은 칸 $x-u_i$는 $B(i,x-u_i)$이다. 그 칸이 $u_i$보다 작아 갱신되지 않았더라도 새 종류를 쓸 수 없으므로 두 행의 값이 같다. 따라서 아래 덧셈은 위 점화식과 일치한다. 이것은 [4,8]의 상태·의존 순서에 앞의 일대일 대응을 적용한 유도이며, 두 자료가 조합 수 점화식을 직접 제시한다는 뜻은 아니다.[2,4,7,8]

```python
combinations = [0] * (target + 1)
combinations[0] = 1
for unit in units:
    for amount in range(unit, target + 1):
        combinations[amount] += combinations[amount - unit]
```

`units=[1,2]`, `target=3`이면 첫 코드는 `[1,1,1]`, `[1,2]`, `[2,1]`의 3개를 세고, 둘째 코드는 사용 개수 `(3,0)`, `(1,1)`의 2개를 센다. 위 정의로 직접 센 결과이다. 둘째 코드에서 `[1,2]`와 `[2,1]`은 같은 사용 개수 `(1,1)`이므로 별도 결과가 아니다. 입력에 같은 단위가 두 번 들어오면 서로 다른 종류로 취급되어 의미가 바뀐다. 값을 기준으로 같은 종류를 합칠 것인지는 입력 계약에 명시해야 한다.[2,4,7,8]

두 코드는 종류 수 $k$에 대해 $O(kA)$개의 덧셈, $O(A)$개의 정수 저장 공간을 쓴다. 큰 경우의 수를 나머지로 반환하도록 요구할 때만 지정한 양의 정수로 매번 나머지를 취한다. 나머지 값은 원래 경우의 수가 아니므로, 임의로 적용하면 반환값의 의미가 바뀐다.[1,2]

## 4. 배낭과 상태 압축

### (1) 0–1 선택

0–1 knapsack에서는 각 항목을 최대 한 번 사용한다. 항목 $i$의 무게를 $w_i$, 보상을 $v_i$, 전체 용량을 $W$라 하자. $F(i,c)$는 처음 $i$개 항목으로 총무게 $c$ 이하에서 얻는 최대 보상이다. 빈 선택을 허용하고 무게는 음이 아닌 정수로 둔다. $F(0,c)=0$이며, 마지막 항목을 선택하는지에 따라 다음처럼 나뉜다.[4,5,8]

$$
F(i,c)=
\begin{cases}
F(i-1,c),&c<w_i,\\
\max\{F(i-1,c),F(i-1,c-w_i)+v_i\},&c\ge w_i.
\end{cases}
$$

양쪽 후보가 모두 이전 행에서 오므로 항목 $i$를 두 번 사용할 수 없다. 이전 행만 필요하다는 사실을 이용하면 최적값 계산의 공간을 $O(W)$로 줄일 수 있다. 양의 무게에서는 아래처럼 용량을 감소시키면 작은 용량의 원소가 아직 이전 행의 값으로 남아 있다. `range(capacity, weight-1, -1)`의 끝은 포함되지 않아 `weight`까지 처리한다.[2,8]

```python
def knapsack_value(items: list[tuple[int, int]], capacity: int) -> int:
    if capacity < 0 or any(weight <= 0 for weight, _ in items):
        raise ValueError("capacity >= 0 and weights > 0 required")
    dp = [0] * (capacity + 1)
    for weight, value in items:
        for cap in range(capacity, weight - 1, -1):
            dp[cap] = max(dp[cap], dp[cap - weight] + value)
    return dp[capacity]
```

방향의 의미는 항목 `(무게 2, 보상 3)` 하나와 용량 4를 수작업으로 추적하면 드러난다. 초기 `dp`는 모두 0이다. 다음 표의 오름차순은 이 0–1 문제에 잘못 적용한 경우이다.[2,8]

| 갱신 방향 | 먼저 계산한 값 | 용량 4의 후보 | 결과의 의미 |
| --- | --- | --- | --- |
| 내림차순 | `dp[4]=0+3` | 아직 이전 행인 `dp[2]+3` | 항목 한 번, 보상 3 |
| 오름차순 | `dp[2]=0+3` | 이미 갱신한 `dp[2]+3` | 항목 두 번, 보상 6 |

용량을 이진수로 표현하는 데 필요한 길이는 $W$ 자체보다 훨씬 작다. 따라서 $O(nW)$는 입력 숫자의 값에 의존하는 **pseudopolynomial time**이다. 항목 수만 보고 빠르다고 판단하면 안 되며, `capacity+1` 크기의 표를 실제로 저장할 수 있는지도 확인해야 한다.[4,5]

### (2) 무제한 선택

Unbounded knapsack에서는 동일 항목을 반복 사용한다. 첫 $i$개 종류를 허용하는 최대 보상을 $G(i,c)$라 하면, 항목 하나를 선택한 뒤에도 같은 종류를 쓸 수 있으므로 같은 행의 작은 용량을 참조한다. 무게는 양수이고 빈 선택을 허용한다. 초기값은 $G(0,c)=0$이다.[4,8]

$$
G(i,c)=\max\{G(i-1,c),G(i,c-w_i)+v_i\}\qquad(c\ge w_i).
$$

이 식은 용량 증가 순서로 압축할 수 있다. 아래 부분은 `items`의 무게가 양수이며 `capacity`가 음이 아니라고 가정한다. 작은 용량에서 이번 항목이 이미 사용되었다면, 그것에 한 개를 더 붙이는 것이 정확히 의도한 전이이다.[4,8]

```python
dp = [0] * (capacity + 1)
for weight, value in items:
    for cap in range(weight, capacity + 1):
        dp[cap] = max(dp[cap], dp[cap - weight] + value)
```

무게 0은 단순한 작은 입력이 아니라 점화식의 의존성을 바꾸는 경계이다. 0–1 선택에서는 이전 항목 행으로 이동하므로 무게 0의 양의 보상도 한 번만 더할 수 있다. 무제한 선택에서 무게 0·양의 보상을 허용하면 용량을 전혀 쓰지 않고 보상을 계속 늘릴 수 있어 유한 최적값이 없다. 이 결론은 위 식의 자기 의존성을 풀어 보아도 확인된다.[4,8]

| 경계 조건 | 해석과 처리 |
| --- | --- |
| 모든 보상이 음수, 빈 선택 허용 | 0이 최적이며 억지로 고르지 않음 |
| 용량 0, 모든 무게 양수 | 빈 선택만 가능 |
| 0–1의 무게 0 | 이전 행에서 한 번만 선택; 아래 전체 표 구현이 처리 |
| 무제한의 무게 0·양의 보상 | 최대값이 유한하지 않음; 제시 코드의 입력 범위에서 제외 |
| 정확히 용량 충족 | 불가능 상태를 별도로 둔 초기화 필요 |

### (3) 선택 결과의 복원

최적값과 그 값을 만든 선택 집합은 서로 다른 출력이다. 전체 배낭 표를 보존하면 `F(i,c)`와 `F(i-1,c)`를 비교하여 항목을 뺄 수 있고, 선택한 경우에는 `c-w_i`로 이동한다. 동점이면 어느 쪽을 택할지 정해 두어야 출력이 일관된다. 단순히 동점을 버리는 규칙은 사전식 최소나 최소 항목 수를 자동으로 보장하지 않는다.[4,5,9]

한 차원 표를 사용하면서 각 용량에 마지막 항목 번호만 기록하는 방법은 조심해야 한다. 용량 값은 이전 항목 단계의 최적값을 참조했는데, 나중에 같은 용량의 부모 정보가 다른 단계의 것으로 덮어써질 수 있다. 예를 들어 항목 하나 `(2,3)`을 역순 처리하며 `parent[4]=2`라는 이전 용량과 항목 번호를 남긴 뒤 `parent[2]`에도 같은 항목을 기록하면, 최종 부모를 따라가는 복원은 그 항목을 두 번 선택할 수 있다. 값 계산 자체는 3으로 맞더라도 복원은 틀린 것이다.[5,8,9]

이 문제를 피하려면 항목 단계가 포함된 전체 표나 결정 표를 보존한다. 다른 방법으로는 덮어쓰지 않는 경로 기록, 또는 필요한 구간을 다시 계산하는 복원을 설계할 수 있다. 이때 각각의 추가 메모리와 재계산 비용을 별도로 분석해야 한다. 아래 자원 선택 문제는 판단을 직접 확인할 수 있도록 전체 표를 사용하는 구현을 제시한다.[5,6,9]

## 5. Longest increasing subsequence

### (1) 끝점 상태

Longest increasing subsequence (LIS)는 원래 인덱스 순서를 유지하면서 값이 엄격히 증가하는 가장 긴 부분수열이다. 연속 구간일 필요는 없다. 수열을 $a_0,\ldots,a_{n-1}$, 인덱스 $i$에서 끝나는 최대 길이를 $L(i)$라 하면 다음 식을 얻는다. 후보가 없는 최댓값은 0으로 정의하여 원소 하나의 길이 1을 포함한다.[1,2,4]

$$
L(i)=1+\max\bigl(\{L(j):0\le j<i,\ a_j<a_i\}\cup\{0\}\bigr).
$$

마지막 원소 바로 앞에 올 수 있는 모든 $j$를 조사하므로 누락되는 증가 부분수열이 없다. $i$가 증가하는 순서로 채우면 선행 값은 이미 계산되어 있다. 원래 문제의 답은 모든 끝점 중 최댓값이며, 마지막 인덱스에서 끝난다는 보장은 없다. 빈 입력의 길이는 0으로 따로 정의한다.[1,2,4]

```python
def lis_length_quadratic(values: list[int]) -> int:
    length = [1] * len(values)
    for i, value in enumerate(values):
        for j in range(i):
            if values[j] < value:
                length[i] = max(length[i], length[j] + 1)
    return max(length, default=0)
```

이 구현은 $O(n^2)$번 비교하고 $O(n)$개 길이를 저장한다. 원소 값이 같을 때 확장하지 않는 `<`가 정의의 일부이다. 비감소 부분수열을 원하면 `<=`로 바꾸지만, 그 경우 목표 자체가 달라진다. `[2,2,2]`의 엄격 증가 길이는 1이고 비감소 길이는 3이다.[2,4,10]

### (2) 최소 끝값과 복원

길이만 필요하면 각 길이의 부분수열 중 끝값이 가장 작은 것만 유지할 수 있다. 같은 길이에서 끝값이 작을수록 뒤에 붙일 수 있는 값의 범위가 넓으므로, 큰 끝값을 버려도 최대로 도달 가능한 길이는 줄지 않는다. `tails[k]`를 지금까지 읽은 접두사 안에서 길이 `k+1`인 증가 부분수열의 최소 끝값으로 둔다.[4,10,11]

엄격 증가에서 새 값 `x`가 들어오면 첫 `tails[k] >= x` 위치를 찾아 교체하거나, 그런 위치가 없으면 뒤에 붙인다. 앞선 끝값은 모두 `x`보다 작으므로 그 길이의 부분수열을 확장할 수 있다. `bisect_left`가 바로 이 경계를 반환한다. 비감소에서는 같은 값 뒤에도 붙일 수 있어 첫 `> x` 위치인 `bisect_right`를 사용한다.[10,11,12]

```python
from bisect import bisect_left, bisect_right


def subsequence_length(values: list[int], strict: bool = True) -> int:
    tails: list[int] = []
    locate = bisect_left if strict else bisect_right
    for value in values:
        pos = locate(tails, value)
        if pos == len(tails):
            tails.append(value)
        else:
            tails[pos] = value
    return len(tails)
```

`tails`는 실제 정답 부분수열이 아니라 길이별 대표 끝값이다. 직접 구성한 입력 `[3,5,6,2,4]`를 추적하면 다음처럼 마지막 표가 `[2,4,6]`이 된다. 하지만 6은 2와 4보다 먼저 등장하므로 이 표 자체를 원래 수열에서 순서대로 뽑을 수 없다. 실제 길이 3의 예는 `[3,5,6]`이다.[4,10,11]

| 새 값 | 갱신 위치 | 갱신 뒤 `tails` |
| --- | --- | --- |
| 3 | 0 | `[3]` |
| 5 | 1 | `[3,5]` |
| 6 | 2 | `[3,5,6]` |
| 2 | 0 | `[2,5,6]` |
| 4 | 1 | `[2,4,6]` |

실제 부분수열을 반환하려면 각 끝값을 만든 원래 인덱스와 그 인덱스의 선행 원소를 저장한다. 아래에서 `previous[i]`는 현재 원소 `i`를 붙이던 순간의 선행 인덱스를 고정한다. 이후 `tail_index`가 바뀌어도 이미 저장한 과거 인덱스 연결은 바뀌지 않는다.[4,10,11]

```python
def one_lis(values: list[int]) -> list[int]:
    tails: list[int] = []
    tail_index: list[int] = []
    previous = [-1] * len(values)
    for i, value in enumerate(values):
        pos = bisect_left(tails, value)
        if pos > 0:
            previous[i] = tail_index[pos - 1]
        if pos == len(tails):
            tails.append(value)
            tail_index.append(i)
        else:
            tails[pos] = value
            tail_index[pos] = i
    answer: list[int] = []
    cur = tail_index[-1] if tail_index else -1
    while cur != -1:
        answer.append(values[cur])
        cur = previous[cur]
    answer.reverse()
    return answer
```

`bisect_left`는 위치만 찾고 배열에 원소를 삽입하지 않는다. 길이별 끝값 하나를 교체하거나 끝에 추가하므로 원소당 탐색은 $O(\log n)$이고 전체는 $O(n\log n)$이다. `insort`처럼 중간 삽입을 하면 원소 이동 비용이 생겨 이 분석이 깨진다. 복원 구현은 인덱스 배열 때문에 $O(n)$ 공간을 사용하며 여러 최장 부분수열 중 하나를 반환한다.[10,11,12]

## 6. 구간과 부분집합 상태

### (1) Interval DP

Interval DP는 연속 구간의 답을 더 짧은 구간의 답으로 결합한다. 행렬 연쇄 곱을 예로 들면 원래 행렬 순서는 유지하면서 괄호만 바꾼다. 행렬 $A_i$의 크기를 $p_i\times p_{i+1}$, $M(i,j)$를 $A_i\cdots A_{j-1}$를 계산하는 최소 스칼라 곱셈 수로 정의한다. 보통의 세 겹 반복문 방식으로 두 행렬을 곱한다는 비용 모형이며, 빠른 행렬 곱셈이나 실제 하드웨어 시간의 모형은 아니다.[4,5]

마지막 곱셈의 분할 위치가 $k$이면 왼쪽 결과는 $p_i\times p_k$, 오른쪽 결과는 $p_k\times p_j$이다. 따라서 결합 비용은 $p_ip_kp_j$이고, 행렬 하나는 곱셈할 필요가 없어 $M(i,i+1)=0$이다.[4,5]

$$
M(i,j)=\min_{i<k<j}\{M(i,k)+M(k,j)+p_ip_kp_j\}
\qquad(j-i\ge2).
$$

두 자식 구간을 모두 계산해야 하므로 의존 DAG의 간선을 따라 경로 하나를 고르는 문제와는 다르다. 마지막 분할을 고정하면 두 부분의 계산 비용을 더한다. 각 자식이 더 짧다는 성질에 따라 길이 증가 순서로 계산한다.[4,5]

```python
def matrix_chain_cost(dimensions: list[int]) -> int:
    if len(dimensions) < 2 or any(size <= 0 for size in dimensions):
        raise ValueError("at least one matrix with positive dimensions")
    count = len(dimensions) - 1
    dp = [[0] * (count + 1) for _ in range(count)]
    for span in range(2, count + 1):
        for left in range(count - span + 1):
            right = left + span
            dp[left][right] = min(
                dp[left][mid] + dp[mid][right]
                + dimensions[left] * dimensions[mid] * dimensions[right]
                for mid in range(left + 1, right)
            )
    return dp[0][count]
```

행렬 개수 $n$에 대해 구간은 $O(n^2)$개이고 분할 후보는 구간당 $O(n)$개이므로 시간은 $O(n^3)$, 공간은 $O(n^2)$이다. 실제 곱셈 순서를 복원하려면 최솟값을 만든 `mid`를 구간별로 보존한다. `dimensions=[8,2,5,3]`의 두 괄호 배치를 직접 계산하면 다음과 같다.[4,5]

| 괄호 배치 | 스칼라 곱셈 수 | 합계 |
| --- | --- | --- |
| $(A_0A_1)A_2$ | $8\cdot2\cdot5+8\cdot5\cdot3$ | 200 |
| $A_0(A_1A_2)$ | $2\cdot5\cdot3+8\cdot2\cdot3$ | 78 |

### (2) Bitmask DP

방문 순서의 과거 전체가 필요하지 않고 방문한 집합과 마지막 위치만 필요할 때에는 집합을 비트마스크로 표현한다. 아래 예시는 정점 0에서 시작하여 모든 정점을 한 번씩 방문하는 최소 비용 **경로**이다. 출발점으로 돌아오는 비용은 포함하지 않는다. 두 정점 사이 비용은 주어진 행렬의 직접 간선 비용이며, 다른 정점을 경유한 최단 거리로 임의 변환하지 않는다.[4,13]

문헌 [4]의 순회 문제는 부분집합 경로를 계산한 뒤 복귀 간선을 더하고, [13]은 먼저 정점 사이 비용을 최단 거리로 바꾼다. 여기서는 두 자료의 집합·끝점 상태와 마지막 간선 분할만 이용한다. 복귀 간선을 제외하고, 없는 간선과 음의 직접 간선 비용까지 허용하는 아래 계약은 그 분할에서 유도한 확장이다. 최단 거리로 변환하면 한 전이가 다른 정점을 경유하여 정확히 한 번 방문 조건을 바꿀 수 있으므로 수행하지 않는다.[4,13]

$D(S,v)$를 0에서 출발하여 집합 $S$의 정점을 정확히 한 번씩 방문하고 $v$에서 끝나는 최소 비용이라 하자. 시작은 $D(\{0\},0)=0$, 나머지 불가능 상태는 $+\infty$이다. $v\ne0$을 마지막에 붙이면 다음 관계를 얻는다. 간선이 없거나 이전 상태가 불가능한 후보는 제외한다.[4,13]

$$
D(S,v)=\min_{u\in S\setminus\{v\}}\{D(S\setminus\{v\},u)+c_{uv}\}.
$$

코드의 `1 << vertex`는 해당 정점의 비트, `mask & bit`는 포함 여부, `mask | bit`는 집합에 정점을 추가한 값이다. 이미 없는 비트를 켜면 정수 마스크 값도 증가하므로, 아래 증가 순서에서는 모든 전이가 뒤쪽 상태로 향한다. 이는 집합 크기 증가 순서와 달라도 유효한 의존 순서이다.[2,4,13]

```python
def visit_all_cost(cost: list[list[int | None]]) -> int | None:
    count = len(cost)
    if count == 0:
        return 0
    if any(len(row) != count for row in cost):
        raise ValueError("square matrix required")
    total_masks = 1 << count
    dp: list[list[int | None]] = [
        [None] * count for _ in range(total_masks)
    ]
    dp[1][0] = 0
    for mask in range(1, total_masks):
        for last in range(count):
            current = dp[mask][last]
            if current is None:
                continue
            for nxt in range(count):
                bit = 1 << nxt
                edge = cost[last][nxt]
                if mask & bit or edge is None:
                    continue
                new_mask = mask | bit
                candidate = current + edge
                old = dp[new_mask][nxt]
                if old is None or candidate < old:
                    dp[new_mask][nxt] = candidate
    possible = [value for value in dp[-1] if value is not None]
    return min(possible, default=None)
```

이 확장의 정확성은 집합 크기에 대한 귀납으로 확인한다. 마지막 간선을 제거하면 더 작은 집합의 경로가 되고, 그 경로를 같은 집합·끝점의 더 싼 경로로 교체해도 방문 제약은 유지된다. 반대로 유효한 이전 경로에 아직 없는 정점을 붙인 후보는 모두 허용된다. 두 방향의 대응은 간선 비용의 부호와 무관하다. 각 전이가 방문 정점을 하나 늘려 최대 $n-1$개의 간선만 쓰므로 음의 간선으로 비용을 무한히 줄일 수도 없다. 정점 한 개의 답은 0이고, 빈 그래프도 함수 계약상 0으로 정했다. 모든 정점을 잇는 경로가 없으면 `None`을 반환한다.[4,13]

이 구현은 $2^n n$칸을 만들고 각 상태에서 최대 $n$개의 다음 정점을 본다. 따라서 시간은 $O(n^2 2^n)$, 공간은 $O(n2^n)$이다. 순열을 모두 열거하는 것보다 줄어들어도 지수 시간과 메모리라는 사실은 남는다. 예를 들어 $n=20$이면 상태 슬롯만 $20\cdot2^{20}=20,971,520$개이다. 이 수는 바이트 수가 아니며 Python 리스트와 정수 객체의 저장 비용은 별도로 고려해야 한다.[4,13]

## 7. 문제: 제한 자원의 항목 선택

### (1) 문제

여러 분석 항목 중 일부를 수행하려 한다. `items[i]=(소모량, 보상)`이며 각 항목은 최대 한 번 선택한다. 총소모량은 `capacity` 이하여야 한다. 최대 총보상과 이를 달성하는 원래 항목 인덱스 리스트를 반환하라. 빈 선택도 허용한다. 동일한 최적값의 후보가 있으면, 표를 채우는 각 단계에서 현재 항목을 선택하지 않는 쪽을 유지한다. 이는 아래 함수의 결정적 동점 규칙이며 별도의 사전식 최적화 조건은 아니다.

다음 제약은 설명용 문제의 입력 계약이다. 일반 알고리즘은 0–1 배낭 점화식과 전체 표 복원을 따른다.[4,5,9]

| 항목 | 조건 |
| --- | --- |
| 항목 수 | $0\le n\le100$ |
| 용량 | 정수, $0\le W\le2000$ |
| 소모량 | 정수, $0\le w_i\le2000$ |
| 보상 | 정수, $-10^6\le v_i\le10^6$ |
| 반환값 | `(최대 보상, 오름차순 인덱스 리스트)` |

### (2) 답

다음 함수는 소모량 0과 음의 보상을 포함하여 처리한다. [9]의 예시는 양의 무게·보상을 사용하지만, 여기서는 [4,5,9]의 선택·비선택 분할을 이 문제의 계약으로 확장한다. 소모량이 0이어도 이전 항목 행을 읽고, 빈 선택과 비교하므로 음의 보상을 강제로 택하지 않는다. 아래 해설에서 이 확장을 귀납으로 확인한다. 전체 표를 저장하여 값과 복원이 같은 항목 단계를 참조하도록 한다.[4,5,9]

```python
def select_resources(
    items: list[tuple[int, int]], capacity: int
) -> tuple[int, list[int]]:
    if capacity < 0 or any(weight < 0 for weight, _ in items):
        raise ValueError("negative capacity or weight")
    count = len(items)
    dp = [[0] * (capacity + 1) for _ in range(count + 1)]
    for i, (weight, value) in enumerate(items, start=1):
        for cap in range(capacity + 1):
            best = dp[i - 1][cap]
            if weight <= cap:
                candidate = dp[i - 1][cap - weight] + value
                if candidate > best:
                    best = candidate
            dp[i][cap] = best

    chosen: list[int] = []
    cap = capacity
    for i in range(count, 0, -1):
        if dp[i][cap] != dp[i - 1][cap]:
            chosen.append(i - 1)
            cap -= items[i - 1][0]
    chosen.reverse()
    return dp[count][capacity], chosen
```

설명용 입력 `items=[(0,2),(2,5),(3,6),(4,8),(1,-3)]`, `capacity=5`의 수작업 예상 반환값은 `(13,[0,1,2])`이다. 선택 항목의 소모량은 $0+2+3=5$, 보상은 $2+5+6=13$이다. 마지막 음의 보상 항목을 버리면 같은 소모량 이하에서 더 높은 보상을 얻는다.

### (3) 해설

다음은 위 입력으로 표의 일부를 직접 채운 결과이다. 용량 0에서도 소모량 0의 항목을 고려해야 하므로 용량 반복문은 0에서 시작한다.

| 고려한 항목 인덱스 | 용량 0 | 용량 2 | 용량 3 | 용량 4 | 용량 5 |
| --- | --- | --- | --- | --- | --- |
| 없음 | 0 | 0 | 0 | 0 | 0 |
| 0 | 2 | 2 | 2 | 2 | 2 |
| 0–1 | 2 | 7 | 7 | 7 | 7 |
| 0–2 | 2 | 7 | 8 | 8 | 13 |
| 0–3 | 2 | 7 | 8 | 10 | 13 |
| 0–4 | 2 | 7 | 8 | 10 | 13 |

정확성은 항목 수에 대한 귀납으로 증명한다. 항목이 없으면 빈 선택의 보상 0이 최적이다. 앞선 행이 정확하다고 가정하면 현재 항목을 쓰지 않는 모든 해는 `dp[i-1][cap]` 이하이다. 쓰는 해에서는 현재 항목을 하나 제거한 나머지가 `cap-weight` 이하의 이전 항목 해이므로 `dp[i-1][cap-weight]+value` 이하이다. 두 경우를 모두 비교하고 각 후보는 실제 구성 가능하므로 현재 행도 정확하다.[4,5]

복원에서는 값이 이전 행과 같으면 현재 항목 없이도 최적값을 달성한다. 다르면 현재 항목을 포함하는 후보가 엄격히 더 좋았으므로 해당 항목을 기록하고 사용한 용량을 뺀다. 소모량이 0이면 `cap`은 그대로이지만 `i`가 줄어들어 같은 항목을 다시 고르지 않는다. 동점에서 이전 행을 유지한다는 규칙과 이 복원 조건은 일치한다.[5,9]

표 계산 시간과 공간은 모두 $O(nW)$이며, 복원은 $O(n)$이다. 코드의 정확한 반복 횟수를 포함하면 $O((n+1)(W+1))$ 크기의 표를 사용한다. 항목이 없거나 모든 보상이 음수이면 `(0,[])`이다. 용량 0에서도 소모량 0·양의 보상 항목은 한 번씩 고른다. 반면 “반드시 하나 이상 선택”으로 문제를 바꾸면 현재 초기화는 그대로 사용할 수 없다. 그 조건을 만족했는지 상태에 추가하거나 별도로 초기값을 설계해야 한다.[4,5,9]

## 8. Greedy와 교환 논증

### (1) 안전한 선택

Greedy의 핵심은 현재 좋아 보이는 기준이 전체 최적해와 양립하는지이다. 먼저 임의의 최적해를 잡고 그 첫 선택을 greedy 선택으로 바꾸어도 실현 가능성과 목적값이 나빠지지 않음을 보인다. 그 선택을 고정한 뒤 남은 문제가 같은 구조로 줄어들면 귀납을 적용할 수 있다. 정렬은 선택 순서를 구현하는 수단이며 최적성 증명을 대신하지 않는다.[3,14]

Interval scheduling에서 최대 개수의 겹치지 않는 구간을 고른다고 하자. 가장 빨리 끝나는 구간을 $g$, 어떤 최적 일정의 첫 구간을 $o$라 하면 $g$의 종료 시각은 $o$보다 늦지 않다. 따라서 $o$를 $g$로 교체해도 $o$ 뒤에 수행하던 모든 구간을 그대로 수행할 수 있고 개수도 같다. 이를 남은 일정에 반복하면 earliest-finish 규칙의 최적성이 성립한다.[3,14]

### (2) 반례와 목적함수

“작은 것부터”, “비율이 큰 것부터”와 같은 기준은 제약에 따라 성립 여부가 달라진다. 다음은 규칙의 한계를 직접 확인하기 위해 구성한 반례이다. 각 행은 한 규칙이 항상 최적이라는 주장을 깨는 충분한 반례이며, 다른 greedy 규칙도 모두 불가능하다는 뜻은 아니다.[3,4,14]

| 잘못 일반화한 규칙 | 입력 | 규칙의 결과와 더 좋은 결과 |
| --- | --- | --- |
| 시작이 가장 빠른 구간 우선 | `[0,10), [1,3), [3,5)` | 긴 구간 하나보다 짧은 두 구간이 많음 |
| 길이가 가장 짧은 구간 우선 | `[0,4), [4,8), [3,5)` | 가운데 길이 2 구간 하나보다 바깥 두 구간이 많음 |
| 0–1 배낭의 보상/무게 비율 우선 | 용량 4, `(3,5),(2,3),(2,3)` | 비율이 큰 첫 항목의 5보다 뒤의 두 항목 합 6이 큼 |
| 가중치가 있어도 종료 시각 우선 | `[0,2)` 보상 1, `[0,3)` 보상 9 | 개수는 같지만 총보상은 1보다 9가 큼 |

가중 구간에서는 종료가 빠른 한 구간을 고르면 나중의 큰 보상을 잃을 수 있다. 따라서 위 교환 논증에서 “개수를 유지한다”는 결론을 “보상을 유지한다”로 바꿀 수 없다. 가중치가 다른 경우는 선택·비선택을 비교하는 별도의 DP가 필요한 대표적인 확장이다.[3,9]

## 9. 문제: 단일 장비의 일정 선택

### (1) 문제

하나의 장비에 예약 후보 구간들이 주어진다. 구간은 정수 시작·종료 시각 `(start,end)`의 반열린 구간 `[start,end)`이며 항상 `start < end`이다. 한 구간이 끝나는 시각에 다음 구간을 시작할 수 있다. 각 구간을 중간에 나누거나 이동할 수 없고, 구간별 보상은 모두 같다. 서로 겹치지 않게 수행할 수 있는 최대 개수의 구간을 고르고 원래 인덱스를 수행 순서대로 반환하라.

설명용 제약은 구간 수 $0\le n\le200,000$, 각 시각의 절댓값 $10^9$ 이하이다. 같은 시작·종료 시각을 가진 후보도 별개 항목이다. 결과를 결정적으로 만들기 위해 종료 시각, 시작 시각, 원래 인덱스 순으로 정렬한다. 이 문제의 개수 최대화는 앞 절의 교환 논증을 그대로 만족한다.[3,14]

문헌 [3]의 의사코드는 시작 시각이 이전 종료 시각보다 엄격히 큰 조건을 쓰지만, 이 문제는 [14]처럼 경계 접촉을 허용한다. 더 일찍 끝나는 구간으로 바꾸면 뒤 구간의 시작 시각 이상 조건도 유지되므로 같은 교환 논증이 성립한다.[3,14]

### (2) 답

`sorted(enumerate(intervals), key=...)`는 정렬 전 인덱스를 구간에 붙인다. `last_end=None`은 아직 선택한 구간이 없음을 나타내어 음수 시각도 처리한다. 0으로 초기화하면 0 이전의 유효한 예약을 놓칠 수 있다.[3,14]

```python
def select_intervals(intervals: list[tuple[int, int]]) -> list[int]:
    if any(start >= end for start, end in intervals):
        raise ValueError("positive duration required")
    ordered = sorted(
        enumerate(intervals),
        key=lambda pair: (pair[1][1], pair[1][0], pair[0]),
    )
    chosen: list[int] = []
    last_end = None
    for index, (start, end) in ordered:
        if last_end is None or start >= last_end:
            chosen.append(index)
            last_end = end
    return chosen
```

입력 `[(-3,0),(-2,2),(0,2),(2,4),(1,5),(4,6)]`의 수작업 예상 결과는 `[0,2,3,5]`이다. 종료 시각이 같은 두 번째·세 번째 후보 중 먼저 검사한 구간이 겹치더라도, 뒤의 호환 구간을 계속 검사해야 한다.

### (3) 해설

| 검사한 원래 인덱스 | 구간 | 판단 | 선택 뒤 종료 시각 |
| --- | --- | --- | --- |
| 0 | `[-3,0)` | 첫 구간 선택 | 0 |
| 1 | `[-2,2)` | 겹쳐서 제외 | 0 |
| 2 | `[0,2)` | 경계 접촉 허용 | 2 |
| 3 | `[2,4)` | 선택 | 4 |
| 4 | `[1,5)` | 겹쳐서 제외 | 4 |
| 5 | `[4,6)` | 선택 | 6 |

반복문 시작 시 `chosen`은 겹치지 않는 구간들로 구성되고 `last_end`는 마지막 선택의 종료 시각이다. 다음 구간의 시작이 이 값 이상이면 이전에 선택한 모든 구간과 호환된다. 가장 최근 구간보다 앞선 구간들은 더 일찍 끝났기 때문이다. 호환되지 않는 후보를 제외해도, 이미 선택한 접두사를 유지하는 해에서는 그 후보를 사용할 수 없다.[3,14]

교환 논증으로 첫 선택을 포함하는 최적해가 존재한다. 그 선택 이후의 후보 집합에서도 같은 규칙이 적용되므로, 귀납적으로 코드가 고른 전체 일정이 최적이다. 종료 시각 동점에서는 어떤 호환 구간을 골라도 뒤에 남는 시간 경계가 같다. 보조 정렬 기준은 반환값을 안정적으로 정할 뿐 최대 개수를 바꾸지 않는다.[3,14]

정렬이 $O(n\log n)$, 순회가 $O(n)$이므로 전체 시간은 $O(n\log n)$이다. 입력을 보존하는 정렬 사본과 출력 리스트 때문에 공간은 $O(n)$이다. 빈 입력은 빈 리스트, 모두 겹치는 입력은 한 구간을 반환한다. 길이 0인 구간은 입력에서 제외했다. 이를 허용하려면 빈 구간의 자원 점유 의미와 동점 순서를 별도로 정해야 하며 현재 문제의 증명을 무조건 재사용하지 않는다.[3,14]

## 10. 최소 비용 병합

서로 독립된 묶음 두 개를 합칠 때 비용이 두 크기의 합이고, 새 묶음의 크기도 그 합이라고 하자. 모든 묶음을 하나로 만드는 총비용은 가장 작은 두 묶음을 반복해서 합치면 최소이다. 이는 Huffman coding의 최소 가중 경로 길이와 같은 최적화 구조이다. 여기서는 묶음 크기가 음이 아니고 **임의의 두 묶음을 합칠 수 있다**고 가정한다.[2,3]

병합 과정을 이진 트리로 표현하면 초기 묶음은 잎이다. 초기 크기를 $b_i$, 해당 잎이 최종 묶음에 도달할 때까지 참여하는 병합 횟수를 $d_i$라 하자. 각 병합에서 포함된 모든 초기 크기를 한 번씩 지불하므로 총비용 $C$는 다음과 같다. 이 식은 병합별 합을 초기 묶음별 합으로 다시 센 정확한 관계이다.[2,3]

$$
C=\sum_i b_i d_i.
$$

가장 깊은 형제 잎 두 개에 가장 작은 크기를 배치해도 위 합은 커지지 않는다. 더 작은 가중치를 더 깊이 보내고 더 큰 가중치를 얕게 보내는 교환의 비용 변화가 0 이하이기 때문이다. 따라서 가장 작은 두 묶음이 먼저 합쳐지는 최적 트리가 존재한다. 이를 합 크기의 잎 하나로 축약하면 같은 형태의 작은 문제가 되어 귀납적으로 greedy의 최적성을 얻는다.[2,3]

최소 두 값을 반복해서 꺼내려면 최소 힙을 쓴다. `heapify`는 리스트를 제자리 힙으로 만들고, `heappop`은 현재 최솟값을 제거하여 반환하며, `heappush`는 새 값을 넣고 힙 성질을 유지한다. 아래 함수는 입력을 복사하므로 호출자가 가진 원본 리스트를 병합 중에 바꾸지 않는다.[15,16]

```python
from heapq import heapify, heappop, heappush


def optimal_merge_cost(sizes: list[int]) -> int:
    if any(size < 0 for size in sizes):
        raise ValueError("negative size")
    heap = list(sizes)
    heapify(heap)
    total = 0
    while len(heap) > 1:
        merged = heappop(heap) + heappop(heap)
        total += merged
        heappush(heap, merged)
    return total
```

크기 `[2,3,7,8]`의 수작업 추적은 다음과 같다. 표의 남은 묶음은 보기 쉽게 정렬하여 적은 것이며 실제 힙 배열 전체가 정렬되어 있다는 뜻은 아니다. 마지막 남은 묶음의 크기 20과 누적 병합 비용 37을 구별해야 한다.[2,3,15]

| 병합 | 새 크기 | 남은 크기의 집합 | 누적 비용 |
| --- | --- | --- | --- |
| 2와 3 | 5 | 5, 7, 8 | 5 |
| 5와 7 | 12 | 8, 12 | 17 |
| 8과 12 | 20 | 20 | 37 |

크기 $n$의 힙 생성은 $O(n)$, 각 삽입·제거는 $O(\log n)$이며 병합이 $n-1$번이므로 전체는 $O(n\log n)$ 시간, $O(n)$ 공간이다. 묶음이 없거나 하나뿐이면 실제 병합이 없어 비용은 0이다. 크기 0도 힙과 교환 논증에 들어갈 수 있다.[3,15,16]

인접한 묶음만 합칠 수 있으면 이 선택은 허용되지 않을 수 있다. 예를 들어 원래 순서가 $(1,100,1)$이면 두 1을 먼저 합칠 수 없다. 무제약 최솟값은 $2+102=104$이지만 인접 병합에서는 어느 쪽을 먼저 합쳐도 $101+102=203$이다. 이처럼 순서 제약이 생기면 구간 분할 상태와 결합 비용을 다시 설계해야 한다. 행렬 연쇄 곱과 최소 비용 병합은 “두 부분을 합친다”는 외형만으로 같은 greedy를 적용할 수 있는 문제가 아니다.[3,4,5]

## 11. 설계 기준 요약

- DP를 설계할 때에는 상태의 의미, 기저값, 전이의 완전성, 의존 순서, 최종 답의 위치를 먼저 적는다.[1,4]
- 상태 압축과 복원은 별도로 검토한다. 같은 배열을 덮어쓸 때에는 읽는 값이 이전 단계인지 현재 단계인지 구별해야 한다. 반복문 방향은 이 의존성을 코드로 나타낸 것이다.[4,8]
- Greedy를 선택할 때에는 임의의 최적해를 현재 선택과 양립하는 해로 바꾸는 논증을 먼저 세운다.[3,14]
- 일정의 개수와 보상, 0–1 선택과 무제한 선택, 자유 병합과 인접 병합처럼 문제의 제약이나 목적이 바뀌면 그 증명도 다시 확인한다.[3,4,9,14]

## 12. 참고문헌

1. Jeff Erickson, *Algorithms*, Chapter 3, “Dynamic Programming,” §§3.1, 3.4, 3.6. [원문](https://jeffe.cs.illinois.edu/teaching/algorithms/book/03-dynprog.pdf).
2. Antti Laaksonen, *Competitive Programmer's Handbook*, Chapters 6, 7, 10, 특히 pp. 57–73, 102–104. [원문](https://cses.fi/book/book.pdf).
3. Jeff Erickson, *Algorithms*, Chapter 4, “Greedy Algorithms,” §§4.2–4.4. [원문](https://jeffe.cs.illinois.edu/teaching/algorithms/book/04-greedy.pdf).
4. Sanjoy Dasgupta, Christos H. Papadimitriou, Umesh Vazirani, *Algorithms*, Chapter 6, “Dynamic Programming,” §§6.1–6.6. [원문](https://people.eecs.berkeley.edu/~vazirani/algorithms/chap6.pdf).
5. Erik Demaine and Srini Devadas, MIT 6.006, Fall 2011, “Lecture 21: Dynamic Programming III,” pp. 1–2, 4–5. [원문](https://www.ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/3484e876d81aba07911a1109f5b5e81e_MIT6_006F11_lec21.pdf).
6. Brad Miller and David Ranum, *Problem Solving with Algorithms and Data Structures using Python*, “Dynamic Programming.” [원문](https://runestone.academy/ns/books/published/pythonds3/Recursion/DynamicProgramming.html).
7. Justin Solomon, MIT 6.006, Spring 2020, “Problem Session 8,” transcript, pp. 20–23. [원문](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/mit6_006s20_04_17_problem_session_8_transcript.pdf).
8. cp-algorithms contributors, “Knapsack Problem,” “0-1 Knapsack” and “Complete Knapsack.” [원문](https://cp-algorithms.com/dynamic_programming/knapsack.html).
9. Kevin Wayne, “Dynamic Programming I,” *Algorithm Design* lecture slides, “Weighted interval scheduling” and “Knapsack problem.” [원문](https://www.cs.princeton.edu/~wayne/kleinberg-tardos/pdf/06DynamicProgrammingI.pdf).
10. cp-algorithms contributors, “Longest increasing subsequence,” minimum endpoint, reconstruction and non-decreasing variants. [원문](https://cp-algorithms.com/dynamic_programming/longest_increasing_subsequence.html).
11. Kevin Wayne, “Longest Increasing Subsequence,” lecture slides, “Patience-LIS” and “Greedy algorithm: implementation,” slides 8–10, 4-up layout. [원문](https://www.cs.princeton.edu/~wayne/kleinberg-tardos/pdf/LongestIncreasingSubsequence-2x2.pdf).
12. Python Software Foundation, *Python 3.10 Documentation*, “bisect — Array bisection algorithm.” [원문](https://docs.python.org/3.10/library/bisect.html).
13. Carnegie Mellon University, 15-451, Fall 2013, “Lecture 11: Dynamic Programming II,” §11.5. [원문](https://www.cs.cmu.edu/afs/cs/academic/class/15451-f13/www/lectures/lect1001.pdf).
14. Kevin Wayne, “Greedy Algorithms I,” *Algorithm Design* lecture slides, “Interval scheduling.” [원문](https://www.cs.princeton.edu/~wayne/kleinberg-tardos/pdf/04GreedyAlgorithmsI.pdf).
15. Python Software Foundation, *Python 3.10 Documentation*, “heapq — Heap queue algorithm.” [원문](https://docs.python.org/3.10/library/heapq.html).
16. Brad Miller and David Ranum, *Problem Solving with Algorithms and Data Structures using Python*, “Binary Heap Implementation.” [원문](https://runestone.academy/ns/books/published/pythonds3/Trees/BinaryHeapImplementation.html).
