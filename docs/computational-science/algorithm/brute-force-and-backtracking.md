---
description: 상태 모델링과 완전 탐색에서 백트래킹, 가지치기, 비트마스크, meet in the middle, 동시 격자 갱신으로 이어지는 Python 구현 원리를 설명한다.
---

# Brute force and backtracking

Brute force는 가능한 후보를 빠짐없이 살펴 답을 구하는 방법이며, backtracking은 부분 해를 한 단계씩 확장하는 탐색이다. 두 방법의 출발점은 반복문이나 재귀 문법이 아니라 **무엇을 서로 다른 후보로 셀지**, **현재 상태로부터 무엇을 결정할 수 있을지**이다. 이후의 모든 확장에서 실패할 부분 해를 일찍 제거하면 탐색량을 줄일 수 있다.[1,2]

이 문서는 유한한 선택 공간의 모델링, Python의 조합 생성, 상태 복원, 안전한 가지치기와 격자 시뮬레이션을 다룬다. 코드는 Python 3의 표준 라이브러리만 사용한다. 두 대표 문제와 작은 추적 예시의 예상 결과는 수작업으로 유도한 값이며 실행 측정값이 아니다. 시간 복잡도는 별도 언급이 없으면 인덱스·비용의 산술과 비교를 상수 시간으로 세는 모형이다.

## 1. 상태와 탐색 공간

### (1) 부분 해와 충분한 상태

탐색 노드는 지금까지 내린 결정의 요약이고, 간선은 다음 결정 하나이다. 상태에는 이후 선택의 허용 여부와 완성된 답을 판정하는 데 필요한 정보가 있어야 한다. 과거 경로가 달라도 미래의 허용 선택과 목적값이 같다면 같은 요약을 쓸 수 있지만, 과거 방문 자체를 제한하는 규칙이 있으면 방문 이력도 상태에 포함한다.[1,2]

다음 표는 이 원칙을 적용한 설계 예시이다. `depth`는 이미 결정한 항목 수이며, `path`는 선택 순서를 보존하는 목록이다. `used`는 다시 선택하면 안 되는 입력 인덱스의 집합이다.

| 대상 | 다음에 결정할 것 | 필요한 상태 | 빠뜨렸을 때의 문제 |
| --- | --- | --- | --- |
| 부분집합 | 현재 원소 포함 여부 | `depth`, 현재 합 | 같은 원소를 여러 번 선택 |
| 순열 | 다음 자리에 놓을 원소 | `path`, `used` | 이미 쓴 인덱스를 재사용 |
| 제약 있는 배정 | 현재 작업의 자원 | 작업 번호, 사용 자원, 비용 | 자원 중복과 비용 누락 |
| 격자 시뮬레이션 | 다음 시각의 모든 칸 | 현재 격자, 외부 입력 | 갱신 도중의 값을 재사용 |

표의 각 행에서 상태에 무엇을 넣을지는 출력 계약에도 달려 있다. 존재 여부만 반환하면 현재 합과 위치로 충분한 경우에도, 실제 선택 목록을 반환하려면 경로를 별도로 보존해야 한다. 단, 출력 경로를 보존한다는 이유만으로 이후 판정에 필요 없는 이력까지 매번 복사할 필요는 없다.[1,2]

탐색 상태를 $s$, 그 상태에서 허용되는 다음 선택의 집합을 $A(s)$, 선택 $a$를 반영한 상태를 $F(s,a)$라 하자. 상태에서 도달하는 완성 후보의 집합 $R(s)$는 다음처럼 정의할 수 있다. 이는 유한 탐색 트리의 정의를 집합으로 적은 것이다.[1,2]

$$
R(s)=
\begin{cases}
\{s\}, & s\text{가 완성된 유효 후보일 때},\\
\displaystyle\bigcup_{a\in A(s)}R(F(s,a)), & s\text{가 미완성일 때},\\
\varnothing, & s\text{가 완성되었으나 무효일 때}.
\end{cases}
$$

이 관계를 구현할 때에는 완성 조건, 불가능 조건, 다음 후보 생성의 순서를 분명히 한다. 부분 해가 아직 완성되지 않았다는 이유만으로 실패를 반환하면 안 된다. 반대로 완성된 해를 계속 확장하면 문제에서 허용하지 않은 길이의 후보를 만들게 된다.

### (2) 완전성과 비용의 분리

정확성은 모든 유효한 답에 도달하는 경로가 있는지로 판단한다. 서로 다른 경로가 같은 답을 만들면 존재 판정에는 문제가 없을 수 있지만, 개수 계산에서는 중복을 제거하거나 그 중복 자체를 문제의 의미로 인정해야 한다. 이 구분은 아래 순열과 조합의 인덱스 규약에 그대로 이어진다.[1,2,3]

비용을 추정할 때에는 잎의 개수와 잎 하나의 처리 비용을 함께 센다. 길이 $n$인 순열을 전부 반환하는 함수는 $n!$개의 결과뿐 아니라 각 결과의 $n$개 항목도 기록해야 한다. 현재 합만 갱신하는 탐색과 매번 `sum(path)`를 계산하는 탐색은 같은 트리를 방문해도 비용이 다르다. 따라서 코드에서 복사·정렬·검증을 수행하는 위치를 확인한다.[1,2]

## 2. 후보의 열거와 조합 생성

### (1) 순서와 재사용의 구분

입력의 서로 다른 **위치**가 $n$개이고 선택 길이가 $k$라 하자. 순서의 의미와 같은 위치의 재사용 가능 여부로 후보 공간을 정한다. 아래 개수는 위치 기준이며, 값이 같은 원소를 구별하지 않는 문제에서는 그대로 답의 개수가 되지 않는다.[2,3,4]

| 선택 공간 | 순서 | 같은 위치 재사용 | 후보 수 | Python 도구 |
| --- | --- | --- | --- | --- |
| 순열 | 구별 | 불가 | $n!/(n-k)!$ | `permutations(a, k)` |
| 조합 | 구별하지 않음 | 불가 | $\binom nk$ | `combinations(a, k)` |
| 반복 선택 수열 | 구별 | 가능 | $n^k$ | `product(a, repeat=k)` |
| 중복조합 | 구별하지 않음 | 가능 | $\binom{n+k-1}{k}$ | `combinations_with_replacement(a, k)` |
| 부분집합 | 구별하지 않음 | 불가 | $2^n$ | 포함·제외 재귀 또는 bitmask |

순열·조합은 $0\le k\le n$에서 표의 식을 적용하고, $k>n$이면 후보가 없다. 중복조합의 식은 $n>0$일 때이다. 길이 0인 선택은 빈 tuple 하나로 취급한다. 빈 입력에서 양의 길이를 요구하면 후보가 없다.[3,4]

각 위치에서 사용할 후보 집합을 $A_0,\ldots,A_{k-1}$라 하고 크기를 $m_0,\ldots,m_{k-1}$라 하자. 위치별 선택이 독립이면 Cartesian product의 개수는 다음과 같다. 앞 위치의 선택마다 뒤 위치의 모든 선택을 붙이는 중첩 반복문의 개수를 곱한 결과이다.[3,4]

$$
\left|A_0\times\cdots\times A_{k-1}\right|
=\prod_{i=0}^{k-1}m_i.
$$

조합 수는 서로 다른 $k$개를 고른 순열을 선택 내부의 $k!$개 순서로 묶어 유도할 수 있다. 부분집합 수는 각 입력 위치에 포함·제외 두 선택이 있으므로 $2^n$이다. 이 유도는 후보 값의 대소관계에 의존하지 않는다. 값의 중복을 제거하려면 별도의 동치 기준을 정의해야 한다.[2,3]

### (2) 표준 라이브러리와 출력 계약

`itertools`의 조합 생성기는 tuple을 차례로 제공한다. 아래 코드는 각 후보 공간을 비교하는 작은 사용 예시이다. 입력을 정렬하면 그 순서를 바탕으로 후보를 얻을 수 있지만, 순서가 답의 일부가 아니라면 불필요한 정렬을 먼저 할 이유는 없다.[3,4]

```python
from itertools import (
    combinations,
    combinations_with_replacement,
    permutations,
    product,
)

a = (2, 5, 8)
ordered_pairs = permutations(a, 2)
unordered_pairs = combinations(a, 2)
repeated_pairs = product(a, repeat=2)
repeated_unordered_pairs = combinations_with_replacement(a, 2)
```

수작업으로 나열하면 `unordered_pairs`는 `(2, 5), (2, 8), (5, 8)`이다. `ordered_pairs`에는 각 쌍의 역순도 있다. `repeated_pairs`에는 `(2, 2), (5, 5), (8, 8)`이 추가되어 9개가 된다. 중복조합은 역순을 따로 세지 않으면서 자기 자신과의 쌍을 허용하므로 6개이다.

모든 결과를 `list(...)`로 감싸면 결과 전체가 메모리에 남는다. 답 하나를 찾거나 최소값만 유지하는 작업에서는 생성기를 순회하며 집계한다.[3,4] 이 문서의 조합 생성 예시는 입력 후보가 유한한 tuple이나 목록인 경우로 한정한다.

입력 `a = (4, 4, 9)`의 앞 두 위치를 `4₀`, `4₁`로 표시하면 중복의 의미가 드러난다. `itertools`는 위치를 구별하고, 값만 같은 결과를 자동으로 합치지 않는다. SymPy의 multiset 조합·순열 문서는 이런 위치 기준 열거와 서로 다른 값 배열의 열거를 별도로 구분한다.[3,5]

| 위치 기준의 두 원소 조합 | 값으로 반환되는 tuple | 값만 구별하는 경우 |
| --- | --- | --- |
| `4₀, 4₁` | `(4, 4)` | 한 종류 |
| `4₀, 9` | `(4, 9)` | 한 종류 |
| `4₁, 9` | `(4, 9)` | 앞 행과 같은 종류 |

위치가 서로 다른 물체의 식별자라면 마지막 두 행은 별개의 답이다. 값만 중요하다면 같은 깊이에서 같은 값으로 시작하는 가지를 하나만 남길 수 있다. 이 정규화는 4절에서 직접 구현한다.

## 3. 깊이 우선 열거와 상태 복원

### (1) 포함·제외 재귀

Depth-first search (DFS)는 한 가지를 끝까지 따라간 뒤 이전 분기점으로 돌아오는 순서이다. 부분집합에서는 현재 인덱스를 포함하는 경우와 제외하는 경우를 모두 탐색한다. 아래 함수는 입력 인덱스의 부분집합을 tuple로 생성하므로 입력 값에 중복이 있어도 각 원소의 정체성이 유지된다.[1,2]

```python
def subset_indices(n):
    path = []

    def dfs(i):
        if i == n:
            yield tuple(path)
            return
        yield from dfs(i + 1)
        path.append(i)
        yield from dfs(i + 1)
        path.pop()

    yield from dfs(0)
```

계약은 $n\ge0$인 정수를 받는 것이다. 호출 `dfs(i)` 직전의 `path`에는 `0`부터 `i-1`까지의 인덱스 중 지금까지 포함하기로 한 것만 오름차순으로 들어 있다. 제외 가지는 목록을 바꾸지 않고, 포함 가지는 `i` 하나를 넣었다가 제거한다. 따라서 두 가지가 모두 종료되면 부모가 보던 상태로 돌아온다. 이는 재귀 열거와 복원 원리를 이 코드에 적용한 불변식이다.[1,2]

이를 집합으로 쓰면 깊이 $i$에서 선택 목록 $P_i$가 만족할 조건은 다음과 같다. $P_i$의 순서는 증가 순서이며, 이 식은 원소의 범위를 나타낸다.

$$
P_i\subseteq\{0,\ldots,i-1\},\qquad
P_{i+1}=P_i\ \text{또는}\ P_i\cup\{i\}.
$$

서로 다른 부분집합은 최초로 포함 여부가 다른 인덱스에서 다른 가지로 갈라진다. 모든 인덱스에서 두 선택을 제공하므로 빠진 부분집합도 없다. 깊이는 매번 1 증가하므로 $n$에서 종료한다. 이 세 관찰로 완전성, 중복 부재, 종료를 함께 확인할 수 있다.

`yield path` 대신 `yield tuple(path)`를 쓰는 이유는 이후의 `append`와 `pop`이 이미 제공한 결과를 바꾸지 않게 하기 위해서이다. Python의 대입은 객체를 복제하지 않으며, 가변 목록의 참조를 저장하면 그 목록의 후속 변경을 함께 보게 된다. 여기서는 원소가 정수이므로 tuple로 옮기는 것만으로 결과 상태가 고정된다.[6,7]

### (2) 선택·탐색·복원의 대응

순열에서는 현재 경로에 들어간 인덱스를 다시 고르면 안 된다. 아래 코드는 길이 $k$인 위치 기준 순열을 만든다. `used[j]`와 `path`의 변경은 반드시 한 쌍으로 복원한다.[1,2]

```python
def permutation_indices(n, k):
    used = [False] * n
    path = []

    def dfs():
        if len(path) == k:
            yield tuple(path)
            return
        for j in range(n):
            if used[j]:
                continue
            used[j] = True
            path.append(j)
            yield from dfs()
            path.pop()
            used[j] = False

    if 0 <= k <= n:
        yield from dfs()
```

불변식은 `used[j]`가 참인 것과 `j`가 현재 `path`에 들어 있는 것이 동치라는 것이다. `used`만 되돌리고 `path`를 남기면 길이와 출력이 오염된다. 반대로 목록만 줄이고 표시를 남기면 형제 가지에서 쓸 수 있는 원소를 누락한다. 위 함수는 경로 상태를 함수 내부에 가두므로 사용자가 순회를 중단해도 다른 호출과 상태를 공유하지 않는다.

복원 순서는 복합 상태일수록 명시해야 한다. 예를 들어 합을 증가시킨 뒤 방문 표시를 하고 경로를 추가했다면, 복귀하면서 경로 제거·방문 해제·합 복원을 짝짓는다. 조기 `return`이 이 복원 구간을 건너뛰는지 수작업으로 확인한다. 불변식을 유지하는 상태 전달과 복원 방식의 선택은 다음과 같다.[1,2,6,7]

| 상태 전달 방식 | 장점 | 확인할 비용·조건 |
| --- | --- | --- |
| 정수·tuple을 새 인자로 전달 | 부모 상태를 직접 바꾸지 않음 | 긴 tuple 연결의 복사 비용 |
| 공유 목록을 수정하고 복원 | 경로 복사를 줄임 | 모든 반환 경로의 복원 |
| 필요한 상태만 복사 | 분기 간 간섭을 줄임 | 내부 가변 객체의 공유 여부 |

### (3) 명시적 스택과 재귀 깊이

재귀는 호출 프레임에 복귀 위치와 지역 상태를 보관한다. 명시적 스택을 쓰면 이 제어 정보를 직접 나타낼 수 있다. Python에는 재귀 깊이 제한이 있으므로 탐색 깊이가 커질 수 있는 코드에서 종료 증명만으로 실제 호출 가능성까지 보장되지는 않는다.[8,9,10]

다음 반복형 DFS는 각 대기 상태를 `(다음 인덱스, 선택 tuple)`로 저장한다. 마지막에 넣은 항목을 먼저 꺼내므로 포함 가지를 먼저 넣어야 제외 가지를 먼저 방문한다. 이는 앞의 재귀 함수와 같은 결과 순서를 갖도록 구성한 구현이다.[1,8]

```python
def subset_indices_iterative(n):
    stack = [(0, ())]
    while stack:
        i, chosen = stack.pop()
        if i == n:
            yield chosen
            continue
        stack.append((i + 1, chosen + (i,)))
        stack.append((i + 1, chosen))
```

이진 탐색 트리의 한 경로를 처리하는 동안 각 깊이에는 미처리 형제 하나가 남으므로 대기 상태 수는 $O(n)$이다. 그러나 각 상태가 길이 $O(n)$인 tuple을 따로 가질 수 있어 이 구현의 보조 저장량 상한은 $O(n^2)$이다. 재귀형의 공유 `path`는 출력 저장분을 제외하면 $O(n)$이다. 반복형으로 바꿨다는 사실만으로 메모리 사용이 줄지는 않는다. 이 비용은 코드의 상태 복사에서 직접 도출된다.[1,8]

모든 부분집합을 실제 tuple로 제공하는 두 구현의 시간 상한은 $O(n2^n)$이다. 반면 leaf에서 상수 크기의 통계만 처리하고 경로 복사를 하지 않으면 포함·제외 트리 자체는 $O(2^n)$개의 노드만 가진다. 출력의 표현을 빼고 알고리즘 이름만으로 복잡도를 적으면 이 차이를 놓치게 된다.[1,2]

## 4. 가지치기와 중복 제거

### (1) 불가능성 증명과 목적값 경계

Pruning은 현재 부분 해가 유효한 완성으로 확장될 수 없음을 보인 뒤 그 하위 트리를 생략하는 것이다. 이미 결정한 두 항목의 충돌이 이후 선택으로 사라지지 않는다면 즉시 제거할 수 있다. 단순히 지금의 합이 크거나 모양이 좋지 않다는 판단은 증명이 아니다.[1,2]

부분집합 합에서 현재 합을 $s$, 목표를 $T$, 아직 처리하지 않은 값들을 $a_i,\ldots,a_{n-1}$라 하자. 각 원소를 한 번씩 선택하거나 제외할 수 있을 때, 남은 모든 음수를 더한 값은 가능한 추가 합의 하한이고 모든 양수를 더한 값은 상한이다. 다음 식은 포함·제외 모형에서 직접 유도한 안전한 범위이다.[1,2]

$$
s+\sum_{j=i}^{n-1}\min(0,a_j)
\ \le\ \text{완성된 부분집합의 합}\ \le\
s+\sum_{j=i}^{n-1}\max(0,a_j).
$$

목표 $T$가 이 닫힌 구간 밖이면 제거할 수 있다. 구간 안에 있다고 반드시 만들 수 있는 것은 아니다. 예를 들어 남은 값이 `4, 8`이면 구간 `[0, 12]` 안의 `5`도 만들 수 없다. 따라서 범위 검사는 필요조건이며 충분조건이 아니다.

다음 표는 가지치기 조건을 입력 가정과 함께 읽어야 함을 보이는 수작업 반례이다. 잎에서 목표를 검사한다는 사실만으로 중간 가지치기의 오류가 고쳐지지는 않는다.

| 상황 | 성급한 판단 | 남은 선택 | 올바른 결론 |
| --- | --- | --- | --- |
| 현재 합 8, 목표 5 | 이미 초과했으므로 제거 | `-3` 포함 | 합 5가 가능 |
| 현재 합 2, 목표 7 | 차이가 크므로 제거 | `5` 포함 | 합 7이 가능 |
| 현재 합 8, 목표 5, 남은 값 모두 비음수 | 초과했으므로 제거 | 합을 줄일 수 없음 | 안전한 제거 |

이 불가능성 원리를 최소화 문제에 적용하여 다음 제거 조건을 직접 유도할 수 있다. 출발점은 모든 허용 확장을 탐색한다는 원리와, 요구 조건을 만족하는 완성이 없으면 그 가지를 제거할 수 있다는 원리이다.[1,2] 이미 찾은 유효한 해의 최선 비용을 $B$, 현재 가지의 임의의 유효한 완성 비용을 $C$라 하자. 이 가지에서 더 나은 해를 찾으려면 $C<B$가 필요하다. 모든 완성에 대해 $L\le C$인 하한 $L$을 증명했다면, $L\ge B$일 때 $C\ge L\ge B$이므로 그 요구 조건은 불가능하다. 따라서 기존 해를 보관하고 이 가지를 버려도 최적해 하나는 보존된다. 최적해를 전부 세거나 전부 반환할 때에는 $C=B$인 완성도 필요하므로 등호를 포함한 제거를 그대로 적용할 수 없다. 7절에서는 같은 부등식으로 배정 비용 하한을 유도한다.

### (2) 생성 규칙에 포함하는 제약

순서 없는 조합은 다음 인덱스를 현재 인덱스보다 크게 제한하면 된다. 정답을 다 생성한 뒤 정렬하고 중복을 제거하기보다 후보 표현 자체를 증가 수열로 정한다. 아래 코드는 $n\ge0$, $k\ge0$에 대해 길이 $k$의 인덱스 조합을 생성한다.[2,3]

```python
def combination_indices(n, k):
    path = []

    def dfs(start):
        need = k - len(path)
        if need == 0:
            yield tuple(path)
            return
        if n - start < need:
            return
        for j in range(start, n - need + 1):
            path.append(j)
            yield from dfs(j + 1)
            path.pop()

    yield from dfs(0)
```

필요한 개수 `need`보다 남은 위치 `n-start`가 적으면 완성은 불가능하다. 또한 첫 원소를 `j`로 선택한 뒤에는 적어도 `need-1`개가 남아야 하므로 `j <= n-need`이다. 이 부등식이 `range`의 끝 `n-need+1`을 결정한다. 임의의 조합에는 유일한 증가 순서가 있으므로 이 제한은 순서 없는 답을 잃지 않는다.

값의 중복을 제거하는 것은 다른 제약이다. 예를 들어 정렬된 정수 입력의 서로 다른 값 순열을 생성하려면, 같은 값의 복사본을 인덱스 순서대로 사용하도록 고정할 수 있다. 위치 기준 순열과 multiset 순열의 차이를 바탕으로 다음 조건을 유도한다.[3,5]

```python
def unique_permutations(values):
    a = sorted(values)
    used = [False] * len(a)
    path = []

    def dfs():
        if len(path) == len(a):
            yield tuple(path)
            return
        for j in range(len(a)):
            if used[j]:
                continue
            if j > 0 and a[j] == a[j - 1] and not used[j - 1]:
                continue
            used[j] = True
            path.append(a[j])
            yield from dfs()
            path.pop()
            used[j] = False

    yield from dfs()
```

동일한 값의 앞 복사본을 아직 쓰지 않았는데 뒤 복사본부터 고르면, 앞 복사본을 고르는 가지와 같은 값 배열을 만든다. 그때만 뒤 가지를 건너뛴다. 앞 복사본이 이미 경로에 있으면 뒤 복사본을 허용하므로 `(4, 4, 9)`처럼 같은 값을 여러 번 쓰는 답은 남는다. 수작업 결과는 `(4, 4, 9), (4, 9, 4), (9, 4, 4)`이다.

이 규칙은 값이 같은 복사본을 서로 바꾸어도 제약과 출력 의미가 같다는 가정에 의존한다. 예를 들어 같은 비용을 가진 서로 다른 자원은 작업별 허용 조건이 다를 수 있다. 이때 비용이 같다는 이유로 배정 가지를 합치면 유효한 해를 누락한다.

## 5. Bitmask를 이용한 부분집합 표현

Bitmask는 선택 여부를 정수의 각 비트에 저장한다. 입력 위치 $i$의 선택 여부를 $b_i\in\{0,1\}$, 전체 위치 수를 $n$이라 할 때 마스크 $M$을 다음과 같이 정의한다. 가장 낮은 비트를 인덱스 0에 대응시킨다.[2,11]

$$
M=\sum_{i=0}^{n-1}b_i2^i,\qquad 0\le M<2^n.
$$

서로 다른 비트 배열은 서로 다른 정수이므로 `range(1 << n)`이 모든 위치 기준 부분집합을 한 번씩 나타낸다. 이 표현은 원소를 여러 번 고르는 중복 선택 횟수를 저장하지 않는다. 횟수가 필요하면 비트 하나로 충분하지 않다.[2,11]

아래 연산에서 `i`는 `0 <= i < n`인 인덱스이고, `M`과 `N`은 같은 $n$개 위치를 나타내는 비음수 마스크이다. 전체 집합의 마스크를 `U = (1 << n) - 1`로 정의한다. 표의 식은 AND·OR·XOR와 왼쪽 이동의 의미를 이 유한 집합에 적용한 것이다.[2,11]

| 목적 | Python 식 | 의미 |
| --- | --- | --- |
| 포함 여부 | `bool(M & (1 << i))` | $i$번째 비트 검사 |
| 원소 추가 | `M \| (1 << i)` | 해당 비트를 1로 설정 |
| 원소 제거 | `M & (U ^ (1 << i))` | 해당 비트를 0으로 설정 |
| 두 집합 교집합 | `M & N` | 공통 위치만 선택 |
| 두 집합 합집합 | `M \| N` | 어느 쪽에든 있는 위치 |
| 전체 $n$개에 대한 여집합 | `U ^ M` | 아래 $n$개 비트만 반전 |

유한 집합의 여집합은 전체 위치 수 $n$을 먼저 정해야 한다. 위 XOR 식은 `U`의 아래 $n$비트가 모두 1이고 `M`의 그 밖의 비트가 모두 0이라는 조건에서 유도된다. 범위 안에서는 선택 여부를 반전하고 범위 밖에서는 0을 유지하므로, 결과도 같은 전체 집합 안에 남는다. 원소 제거식에서는 `U`의 $i$번째 비트만 0으로 만든 뒤 AND를 취한다.[2,11]

다음은 마스크를 선택 인덱스로 바꾸는 가장 직접적인 구현이다. 현재 원소가 몇 개인지는 마스크 표현과 무관하게 `n`으로 고정한다.

```python
def indices_from_mask(mask, n):
    return tuple(i for i in range(n) if mask & (1 << i))
```

예를 들어 $n=4$, $M=13$의 이진 표현은 `1101`이므로 반환값은 `(0, 2, 3)`이다. 모든 $2^n$개 마스크에 이 함수를 적용하면 매번 $n$비트를 검사하여 시간은 $O(n2^n)$이다. 모든 결과를 저장하면 출력 자체도 지수 크기이다. Bitmask는 상태 표현을 압축하지만 후보 수를 줄이지 않는다는 점을 이 계산에서 확인할 수 있다.[1,2,11]

여기서 상수 시간으로 센 것은 비트 연산 한 번이다. 이 분석은 마스크가 제한된 기계 워드 수 안에 들어간다는 비용 모형을 전제로 한다. 비트 수 자체가 커지는 입력의 산술 비용은 이 상한에 포함하지 않는다.

## 6. Meet in the middle

### (1) 두 부분의 요약과 결합

Meet in the middle은 입력을 두 부분으로 나누어 각각의 후보를 열거한 뒤, 필요한 관계를 만족하는 두 요약을 결합한다. 분할만으로 빨라지는 것은 아니다. 두 결과의 모든 쌍을 다시 조사하면 원래의 조합 수로 돌아간다. 합처럼 작은 요약으로 결합 조건을 검사할 수 있어야 한다.[2,12]

부분집합 합에서 인덱스 집합을 겹치지 않는 두 부분 $A,B$로 나누고, 각 부분의 가능한 합 목록을 $S_A,S_B$라 하자. 목표 합을 $T$라 하면 다음 동치가 성립한다. 목록에는 서로 다른 부분집합에서 나온 같은 합이 여러 번 나타날 수 있다.[2,12]

$$
\exists\text{ 부분집합의 합 }T
\quad\Longleftrightarrow\quad
\exists x\in S_A,\ y\in S_B:\ x+y=T.
$$

이 동치는 모든 전체 부분집합이 두 부분과의 교집합으로 유일하게 분해된다는 사실에서 나온다. 합만 묻는 경우에는 선택 원소의 배열을 저장할 필요가 없다. 선택 개수가 정확히 $k$개라는 조건이 추가되면 합뿐 아니라 개수도 요약에 넣어야 한다. 두 부분 사이의 제약을 요약에서 판별할 수 없다면 같은 결합법을 그대로 적용할 수 없다.

아래는 방법의 핵심을 보이는 존재 판정 함수이다. 정수 값의 부호를 제한하지 않는다. 이진 탐색은 오른쪽 합 목록을 정렬한 뒤 사용하며, `bisect_left`의 위치에서 값이 같은지 마지막으로 확인한다.[13,14] 이는 정렬된 두 합 목록을 결합하는 원리를 이진 탐색으로 구현한 변형이다.[2,12]

```python
from bisect import bisect_left


def subset_sum_exists(values, target):
    def sums(part):
        result = [0]
        for value in part:
            added = [s + value for s in result]
            result.extend(added)
        return result

    mid = len(values) // 2
    left = sums(values[:mid])
    right = sorted(sums(values[mid:]))
    for x in left:
        wanted = target - x
        j = bisect_left(right, wanted)
        if j < len(right) and right[j] == wanted:
            return True
    return False
```

`added`는 확장 전 목록만 읽어 만들어야 한다. `result`를 순회하면서 즉시 같은 목록에 새로운 합을 붙이면 새 항목을 다시 읽어 같은 원소를 반복 사용하게 될 수 있다. 현재 목록과 추가 목록을 분리하면 `value`를 제외한 합과 정확히 한 번 포함한 합만 합쳐진다. 이 단계 불변식은 부호에 의존하지 않으므로 음수 입력에도 성립한다.

### (2) 비용과 요약의 한계

수작업 예시로 `values = [6, -2, 9, 3]`, `target = 7`을 두 원소씩 나누면 다음과 같다. 왼쪽의 `-2`와 오른쪽의 `9`가 목표를 만든다. 빈 부분집합의 합 0은 한쪽에서 아무것도 선택하지 않는 해를 보존한다.

| 부분 | 정렬한 가능한 합 | 결합에 쓰는 값 |
| --- | --- | --- |
| `[6, -2]` | `[-2, 0, 4, 6]` | $-2$ |
| `[9, 3]` | `[0, 3, 9, 12]` | $9$ |
| 전체 | 두 부분에서 한 합씩 선택 | $-2+9=7$ |

왼쪽 원소 수를 $p=\lfloor n/2\rfloor$, 오른쪽 원소 수를 $q=\lceil n/2\rceil$라 하자. 위 코드의 합 생성은 매 단계 목록 크기를 두 배로 만들고, 오른쪽 정렬과 왼쪽 각 항목의 이진 탐색이 추가된다. 따라서 $n\ge1$인 입력과 고정 크기 정수의 산술·비교 모형에서 다음 상한을 얻는다.[2,12]

$$
\text{시간}=O(2^p+q2^q+q2^p)=O(n2^{\lceil n/2\rceil}),
\qquad
\text{공간}=O(2^{\lceil n/2\rceil}).
$$

문헌에는 합 목록을 정렬된 상태로 병합 생성하고 두 포인터로 결합하여 $O(2^{n/2})$ 시간에 처리하는 구현도 있다. 위 코드는 일반 정렬과 개별 이진 탐색을 택했으므로 그 더 강한 시간 경계를 그대로 붙이지 않는다.[2,12]

존재 판정에서는 같은 합을 합쳐도 결론이 같지만 개수 계산에서는 합의 빈도가 필요하다. 왼쪽 합 $x$를 만드는 부분집합이 $u$개이고 오른쪽 합 $T-x$를 만드는 부분집합이 $v$개라면 이 결합에서 $uv$개의 인덱스 부분집합이 생긴다. 이는 두 인덱스 영역이 겹치지 않는다는 전제에서 곱의 법칙을 적용한 결과이다. 실제 원소를 복원하려면 합과 함께 적어도 하나의 대표 마스크를 보존해야 한다.[2,3,12]

## 7. 대표 문제: 제약 있는 최소 비용 배정

### (1) 문제와 입력 계약

**문제.** 번호 `0`부터 `n-1`까지의 작업과 자원이 각각 $n$개 있다. 작업마다 자원 하나를 배정하고 각 자원은 한 번만 사용한다. `cost[i][j]`는 작업 `i`를 자원 `j`에 배정하는 비용이며 `None`이면 금지된 배정이다. 최소 총비용과 배정 tuple을 반환하라. 불가능하면 `None`, 작업이 없으면 `(0, ())`를 반환한다. 최소 해가 여러 개면 그중 하나를 반환한다.

이 문제는 순열 열거에 허용 간선과 목적값 하한을 결합한 자체 구성 예시이다. 부분 배정의 확장·복원은 앞서 설명한 backtracking 원리를 사용한다.[1,2]

| 항목 | 조건 |
| --- | --- |
| 작업 수 | $0\le n\le10$ |
| 입력 형태 | 각 행 길이가 $n$인 정방 목록 |
| 유한 비용 | $0\le\text{cost}[i][j]\le10^6$인 정수 |
| 금지 표현 | `None`; 비용 0과 구별 |
| 반환 배정 | tuple의 $i$번째 값이 작업 $i$의 자원 번호 |

완성 배정을 순열 $\pi$로 쓰면 목적은 다음과 같다. 합에는 허용된 배정만 들어가야 한다. 같은 숫자의 비용을 가진 자원도 서로 다른 식별자이다.

$$
\min_{\pi}\sum_{i=0}^{n-1}\text{cost}[i][\pi(i)],
\qquad
\pi\text{는 순열},\quad
\text{cost}[i][\pi(i)]\ne\texttt{None}.
$$

### (2) 답

각 행의 허용 비용 중 최솟값을 구하고 뒤쪽 행의 합을 `suffix`로 저장한다. 자원 중복을 무시한 낙관적인 비용이므로 하한으로 사용할 수 있다. 반환값의 비용은 항상 정수이며, 아직 해를 찾지 못한 상태는 `best_cost is None`으로 구별한다.

```python
def minimum_assignment(cost):
    n = len(cost)
    if any(len(row) != n for row in cost):
        raise ValueError("cost must be square")

    row_min = []
    for row in cost:
        allowed = [v for v in row if v is not None]
        if not allowed:
            return None
        row_min.append(min(allowed))

    suffix = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix[i] = suffix[i + 1] + row_min[i]

    used = [False] * n
    path = []
    best_cost = None
    best_path = None

    def dfs(i, total):
        nonlocal best_cost, best_path
        if best_cost is not None and total + suffix[i] >= best_cost:
            return
        if i == n:
            best_cost = total
            best_path = tuple(path)
            return
        for j in range(n):
            value = cost[i][j]
            if used[j] or value is None:
                continue
            used[j] = True
            path.append(j)
            dfs(i + 1, total + value)
            path.pop()
            used[j] = False

    dfs(0, 0)
    if best_cost is None:
        return None
    return best_cost, best_path
```

다음 입력의 예상 반환값은 수작업으로 구한 `(7, (2, 0, 1))`이다. 아래 호출은 사용법을 나타내며 실행 결과를 보고한 것이 아니다.

```python
cost = [
    [4, None, 2],
    [3, 1, 5],
    [None, 2, 3],
]
answer = minimum_assignment(cost)
# 수작업 예상: (7, (2, 0, 1))
```

### (3) 해설과 수작업 검증

가능한 자원 순열은 여섯 개이다. 다음 표는 금지 조건과 비용을 모두 검사하므로 작은 입력에 대한 완전한 수작업 기준표가 된다.

| 배정 tuple | 비용 계산 | 판정 |
| --- | --- | --- |
| `(0, 1, 2)` | $4+1+3=8$ | 허용 |
| `(0, 2, 1)` | $4+5+2=11$ | 허용 |
| `(1, 0, 2)` | 작업 0 → 자원 1 금지 | 제외 |
| `(1, 2, 0)` | 작업 0 → 자원 1 금지 | 제외 |
| `(2, 0, 1)` | $2+3+2=7$ | 최소 |
| `(2, 1, 0)` | 작업 2 → 자원 0 금지 | 제외 |

`dfs(i, total)`의 불변식은 앞의 $i$개 작업에 서로 다른 허용 자원이 배정되어 있고 `total`이 그 비용의 합이라는 것이다. 순환문은 사용하지 않은 허용 자원을 모두 고려하므로 모든 완성 배정은 가지치기를 제외하면 도달 가능하다. 깊이 $n$에서는 정확히 $n$개 작업이 끝나며 자원 중복도 없으므로 유효한 배정이다.[1,2]

가지치기의 안전성은 행별 최소 비용의 의미에서 직접 나온다. `suffix[i]`를 남은 행의 최소값 합, $c$를 현재 비용, $C$를 임의의 유효한 완성 비용이라 하면 각 행에서 실제 선택 비용이 행의 최솟값 이상이므로 다음 부등식이 성립한다.

$$
C\ge c+\sum_{r=i}^{n-1}\min_{j:\,\text{cost}[r][j]\ne\texttt{None}}
\text{cost}[r][j]
=c+\text{suffix}[i].
$$

최솟값을 주는 자원이 이미 사용되었거나 여러 행이 같은 자원을 원해도 하한이라는 사실은 유지된다. 그 제약을 무시하면 실제 가능한 최솟값보다 작아질 수 있을 뿐 커지지는 않는다. 하한이 현재 최선 이상이면 더 나은 완성은 없으므로 가지를 제거해도 최소 해 하나는 남는다. 최선이 아직 없을 때는 이 제거를 하지 않는다.

수작업 입력에서 행 최솟값은 `2, 1, 2`이다. 처음 발견하는 배정 `(0, 1, 2)`가 비용 8을 만든 뒤, `(0, 2)`까지 선택한 상태의 하한은 `9+2=11`이므로 제거할 수 있다. 첫 작업을 자원 2에 배정한 가지는 하한이 `2+1+2=5`이므로 남고, 그 안에서 비용 7을 얻는다. 하한 5 자체가 가능한 완성값이라고 주장하는 것은 아니다.

깊이 $i$의 부분 순열 수는 $n!/(n-i)!$이다. 각 미완성 상태에서 $n$개의 자원을 검사하므로 $n\ge1$에서 시간의 안전한 상한은 $O(n\cdot n!)$이고, 입력 행렬을 제외한 보조 공간은 경로·표시·suffix·호출 스택을 합쳐 $O(n)$이다. 가지치기가 실제 입력에서 줄이는 방문 수를 최악 복잡도의 개선으로 단정하지 않는다.[1,2]

빈 입력에서는 `dfs(0, 0)`이 곧 완성 상태여서 `(0, ())`를 반환한다. 허용 비용이 전혀 없는 행은 즉시 불가능하다. 각 행에 허용 자원이 있더라도 모든 행이 같은 자원 하나만 허용하면 완성할 수 없으며, 이 경우 탐색 종료 뒤 `None`을 반환한다. 비용이 모두 0이면 첫 유효 배정으로 최솟값 0을 얻고 같은 비용의 나머지 가지를 제거한다.

## 8. 대표 문제: 동시 격자 갱신

### (1) 좌표와 시각의 분리

시뮬레이션은 정해진 규칙에 따라 상태를 바꾸는 계산이다. 결정적인 규칙이라면 현재 상태와 입력이 다음 상태를 정한다. 특히 동시 갱신은 모든 칸이 같은 이전 시각의 값을 읽어야 한다. 한 칸의 새 값을 즉시 다른 칸의 입력으로 사용하면 같은 반복 안에서 변화가 연쇄적으로 전파되어 순차 갱신이 된다.[15,16]

이 문서의 좌표는 `(r, c) = (행, 열)`이며 행은 아래로, 열은 오른쪽으로 증가한다. 격자 크기를 $H\times W$라 하고 유효 범위를 `0 <= r < H`, `0 <= c < W`로 정한다. 이웃의 정의와 가장자리 처리는 상태 전이 규칙의 일부이다.[2,15]

| 방향 | `dr` | `dc` | 이동 결과 |
| --- | --- | --- | --- |
| 위 | -1 | 0 | `(r-1, c)` |
| 오른쪽 | 0 | 1 | `(r, c+1)` |
| 아래 | 1 | 0 | `(r+1, c)` |
| 왼쪽 | 0 | -1 | `(r, c-1)` |

범위를 검사한 뒤 `grid[nr][nc]`에 접근한다. Python의 음수 인덱스는 뒤쪽 원소를 가리키므로 위쪽 경계를 넘어 `grid[-1]`을 읽어도 반드시 오류가 나는 것은 아니다. 양쪽 경계를 식으로 검사해야 의도하지 않은 반대편 연결을 막는다.[7,11]

격자를 복제할 때에는 바깥 목록뿐 아니라 행 목록도 분리한다. 정수 칸을 가진 2차원 목록에서는 아래와 같이 행마다 복사하면 충분하다. 칸 안에 또 다른 가변 객체를 넣는다면 이 복사는 그 내부까지 분리하지 않는다.[6,7]

```python
current = [row[:] for row in grid]
next_grid = [[0] * width for _ in range(height)]
# 피해야 할 구성: [[0] * width] * height
# 바깥 목록만 복사하는 grid[:] 역시 행 객체를 공유한다.
```

행을 곱셈으로 반복하면 여러 행이 같은 목록을 참조한다. 이는 읽기 시각의 문제와 별개인 객체 공유 문제이다. `next_grid`를 따로 만들었더라도 그 행들이 같은 객체를 참조하면 한 칸에 쓰는 동작이 다른 행에 영향을 준다.[7,11]

### (2) 문제와 답

**문제.** 0과 1로 이루어진 $H\times W$ 격자에서 1은 활성 상태이다. 한 단계마다 활성 칸은 활성 상태를 유지한다. 비활성 칸은 **이전 단계**의 상하좌우 이웃 가운데 활성 칸이 두 개 이상이면 활성화된다. 격자 밖은 이웃에 포함하지 않는다. $T$단계 후의 격자를 반환하라. 입력은 바꾸지 않는다. 조건은 $1\le H,W\le100$, $0\le T\le100$이며 직사각형 입력을 가정한다.

이 규칙은 동시 갱신을 설명하기 위한 자체 구성 모형이다. 문헌의 특정 cellular automaton 규칙을 재현한 것이 아니라, 이전 상태의 이웃으로 다음 상태를 정하는 원리와 double buffer를 적용한다.[15,16]

시각 $t$에서 칸 값을 $G_t(r,c)$, 유효한 네 방향 이웃 집합을 $\mathcal N(r,c)$, 이웃 활성 수를 $q_t(r,c)$라 하자. 전이식은 다음과 같으며 오른쪽에는 모두 시각 $t$만 등장한다.

$$
q_t(r,c)=\sum_{(u,v)\in\mathcal N(r,c)}G_t(u,v),\qquad
G_{t+1}(r,c)=
\begin{cases}
1,&G_t(r,c)=1\ \text{또는}\ q_t(r,c)\ge2,\\
0,&\text{그 외}.
\end{cases}
$$

다음 표는 문제의 규칙을 코드의 분기로 옮긴 것이다. 활성 칸의 유지 여부와 이웃 조건을 따로 해석해야 한다.

| 현재 값 | 활성 이웃 수 | 다음 값 |
| --- | --- | --- |
| 1 | 0–4 | 1 |
| 0 | 0–1 | 0 |
| 0 | 2–4 | 1 |

```python
def activate_grid(grid, steps):
    height = len(grid)
    width = len(grid[0])
    current = [row[:] for row in grid]
    directions = ((-1, 0), (0, 1), (1, 0), (0, -1))

    for _ in range(steps):
        next_grid = [[0] * width for _ in range(height)]
        for r in range(height):
            for c in range(width):
                neighbors = 0
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < height and 0 <= nc < width:
                        neighbors += current[nr][nc]
                next_grid[r][c] = int(
                    current[r][c] == 1 or neighbors >= 2
                )
        current = next_grid
    return current
```

다음 입력으로 활성 유지와 새 활성화를 함께 확인한다. 한 단계 결과와 두 단계 결과는 아래 해설에서 직접 계산한다.

```python
grid = [
    [1, 0, 0],
    [0, 1, 0],
]
after_one = activate_grid(grid, 1)
# 수작업 예상: [[1, 1, 0], [1, 1, 0]]
after_two = activate_grid(grid, 2)
# 수작업 예상: [[1, 1, 0], [1, 1, 0]]
```

### (3) 해설과 경계 조건

첫 단계에서 `(0,1)`은 왼쪽 `(0,0)`과 아래 `(1,1)`이 활성이라 바뀐다. `(1,0)`도 위 `(0,0)`과 오른쪽 `(1,1)` 때문에 바뀐다. 오른쪽 열은 아직 필요한 이웃 수에 미치지 못한다. 두 번째 단계에서도 각 오른쪽 칸의 활성 이웃은 왼쪽 하나뿐이므로 더 바뀌지 않는다.

| 칸 | 초기 값 | 첫 단계에서 읽는 활성 이웃 수 | 첫 단계 값 | 둘째 단계 값 |
| --- | --- | --- | --- | --- |
| `(0,0)` | 1 | 0 | 1 | 1 |
| `(0,1)` | 0 | 2 | 1 | 1 |
| `(0,2)` | 0 | 0 | 0 | 0 |
| `(1,0)` | 0 | 2 | 1 | 1 |
| `(1,1)` | 1 | 0 | 1 | 1 |
| `(1,2)` | 0 | 1 | 0 | 0 |

동시 갱신과 제자리 순차 갱신을 구별하는 반례는 `[[1, 0, 1], [0, 0, 1]]`이다. 올바른 동시 갱신에서는 첫 행 중앙만 새로 켜져 `[[1, 1, 1], [0, 0, 1]]`이 된다. 행 우선 제자리 갱신에서는 `(1,1)`이 이미 갱신된 위 `(0,1)`과 기존 오른쪽 `(1,2)`를 읽어 같은 단계에 켜진다. 이는 시간 $t$와 $t+1$을 혼합한 계산이다. 두 버퍼 구현은 읽는 객체를 고정하여 이 순서 의존성을 없앤다.[15,16]

정확성은 시각에 대한 귀납으로 보인다. 시작 시 `current`는 입력 격자와 같고 입력과 행 객체를 공유하지 않는다. 한 단계의 모든 읽기가 `current`만 참조하므로 각 칸은 정확히 전이식의 이웃 합을 얻는다. 모든 칸을 쓴 뒤에만 `current = next_grid`를 실행하므로 다음 반복의 입력은 완성된 다음 시각이다. 순환문의 칸 방문 순서가 바뀌어도 같은 값을 읽고 각자 다른 칸에 쓰므로 결과는 같다.[6,7,15,16]

각 단계는 $HW$개 칸에서 최대 네 이웃을 읽으므로 $T$단계의 시간은 초기 복사를 포함해 $O((T+1)HW)$이다. 두 격자를 보유하는 공간은 $O(HW)$이며, 전체 시각의 기록을 저장하지 않는다. $T=0$에서도 입력 복사 때문에 시간은 $O(HW)$이고 결과는 같은 값을 가진 별도 행 목록이다. 한 칸짜리 격자는 이웃이 없으므로 초기값을 유지한다. 한 행·한 열에서도 동일한 경계 검사로 처리한다.

## 9. 설계와 수작업 점검의 요약

완전 탐색의 핵심은 후보 표현, 상태 불변식, 복원과 제거 조건을 맞추는 것이다. 작은 입력에서 최종 답만 보는 것보다 분기 직전과 복귀 직후의 상태, 한 시각에서 읽는 값의 출처를 함께 추적하면 오류가 생기는 지점을 특정할 수 있다.[1,2,15,16]

| 점검 대상 | 수작업 확인 방법 |
| --- | --- |
| 후보 누락 | 가장 작은 입력의 후보를 직접 나열하고 경로에 대응 |
| 중복 계산 | 위치 식별자와 값의 동치 기준을 분리 |
| 상태 복원 | 호출 전후 `path`, `used`, 누적값을 비교 |
| 가지치기 | 잘라낸 상태의 모든 완성이 실패함을 부등식으로 설명 |
| 경계 인덱스 | 모서리·한 행·한 열의 이웃을 직접 기록 |
| 동시 갱신 | 새 값을 읽을 경우 달라지는 입력을 구성 |
| 공간 복잡도 | 대기 상태 수와 각 상태의 복사 크기를 따로 계산 |

순열·조합 생성기는 후보의 형태를 간결하게 나타내고, backtracking은 부분 해 제약을 조기에 반영한다. Bitmask는 부분집합의 표현을 바꾸며, meet in the middle은 결합 가능한 요약을 이용해 지수의 크기를 줄인다. 시뮬레이션에서는 탐색의 가지 대신 시간 단계가 진행되지만, 어떤 상태를 읽고 언제 새 상태를 공개하는지 명시해야 한다는 원칙은 같다.[1,2,15,16]

## 10. 참고문헌

1. Jeff Erickson, *Algorithms*, Chapter 2, “Backtracking,” §§2.1–2.4. [Author-hosted PDF](https://jeffe.cs.illinois.edu/teaching/algorithms/book/02-backtracking.pdf).
2. Antti Laaksonen, *Competitive Programmer's Handbook*, Chapters 5 and 10. [Author-hosted PDF](https://cses.fi/book/book.pdf).
3. Python Software Foundation, “itertools — Functions creating iterators for efficient looping,” combinatoric iterators. [Documentation](https://docs.python.org/3/library/itertools.html).
4. Doug Hellmann, “itertools — Iterator Functions,” *Python Module of the Week 3*, “Combining Inputs.” [Author's documentation](https://pymotw.com/3/itertools/index.html).
5. SymPy Development Team, “Iterables,” `multiset_combinations`, `multiset_permutations`. [Documentation](https://docs.sympy.org/latest/modules/utilities/iterables.html).
6. Python Software Foundation, “copy — Shallow and deep copy operations.” [Documentation](https://docs.python.org/3/library/copy.html).
7. Brad Miller and David Ranum, *How to Think Like a Computer Scientist: Interactive Edition*, “Cloning Lists,” “Repetition and References,” and “Accessing Elements.” [Cloning Lists](https://runestone.academy/ns/books/published/thinkcspy/Lists/CloningLists.html), [Repetition and References](https://runestone.academy/ns/books/published/thinkcspy/Lists/RepetitionandReferences.html), [Accessing Elements](https://runestone.academy/ns/books/published/thinkcspy/Lists/AccessingElements.html).
8. Brad Miller and David Ranum, *Problem Solving with Algorithms and Data Structures Using Python*, “Stack Frames: Implementing Recursion.” [Textbook](https://runestone.academy/ns/books/published/pythonds/Recursion/StackFramesImplementingRecursion.html).
9. Python Software Foundation, “sys — System-specific parameters and functions,” `getrecursionlimit`, `setrecursionlimit`. [Documentation](https://docs.python.org/3/library/sys.html#sys.getrecursionlimit).
10. Allen B. Downey, *Think Python*, 2nd edition, §§5.9–5.10. [Author-hosted textbook](https://greenteapress.com/thinkpython2/html/thinkpython2006.html).
11. Python Software Foundation, “Built-in Types,” numeric types, bitwise operations and sequences. [Documentation](https://docs.python.org/3/library/stdtypes.html).
12. Xi Chen, Yaonan Jin, Tim Randolph, and Rocco A. Servedio, “Subset Sum in Time $2^{n/2}/\mathrm{poly}(n)$,” arXiv:2301.07134, §2.1, Figures 1–2. [Full text](https://arxiv.org/html/2301.07134v2).
13. Python Software Foundation, “bisect — Array bisection algorithm,” `bisect_left` and “Searching Sorted Lists.” [Documentation](https://docs.python.org/3/library/bisect.html).
14. Doug Hellmann, “bisect — Maintain Lists in Sorted Order,” “Handling Duplicates.” [Author's documentation](https://pymotw.com/3/bisect/index.html).
15. Allen B. Downey, *Think Complexity*, 2nd edition, Chapter 5, “Cellular Automatons,” §§5.1–5.2, 5.10. [Author-hosted textbook](https://greenteapress.com/complexity2/html/thinkcomplexity2006.html).
16. Robert Nystrom, *Game Programming Patterns*, “Double Buffer,” “The Pattern” and “Buffered slaps.” [Author's source manuscript](https://raw.githubusercontent.com/munificent/game-programming-patterns/master/book/double-buffer.markdown).
