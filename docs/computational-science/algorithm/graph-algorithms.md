---
description: 그래프의 표현과 탐색, 최단 경로, 위상 정렬, 서로소 집합과 최소 신장 트리를 Python 구현과 불변식으로 설명한다.
---

# Graph algorithms

그래프 알고리즘은 정점 사이의 연결을 따라 도달 가능성, 이동 비용, 선행 관계와 연결망의 구조를 계산한다. 같은 그래프에서도 **무엇을 최소화하는지**와 **어떤 이동을 허용하는지**에 따라 필요한 알고리즘이 달라진다. 간선 수가 가장 적은 경로와 가중치 합이 가장 작은 경로는 다른 대상이며, 모든 정점을 가장 싸게 연결하는 문제도 별도로 구분해야 한다.[1,2,3,4]

이 문서는 Python으로 인접 리스트를 구성하고, 탐색의 방문 상태와 최단 거리의 확정 조건을 구별하는 데서 시작한다. 이어서 이력이 필요한 상태 확장, 방향 그래프의 처리 순서, 연결 성분을 합치는 자료구조를 다룬다. 마지막 예제는 간선 하나에 선택적으로 할인을 적용할 수 있는 최소 비용 경로이다. 코드는 기본 절차를 보여 주는 참조 구현이며, 예제의 결과는 경로 대응과 수동 추적으로 설명한다.

## 1. 그래프 표현과 비용 모형

### (1) 정점·간선·경로

그래프를 $G=(V,E)$로 쓰고 정점 수를 $n=|V|$, 입력 간선 수를 $m=|E|$로 둔다. 정점 번호는 `0`부터 `n-1`이다. 방향 간선 $(u,v)$는 $u$에서 $v$로만 이동하며, 무방향 간선은 양쪽 이동을 허용한다. 같은 두 정점 사이에 여러 간선이 있는 경우를 parallel edges, 정점 자신으로 돌아가는 간선을 self-loop라고 한다.[1,5,6]

이 문서에서 경로의 비용은 통과한 간선의 가중치를 모두 더한 값이다. 정점이나 간선을 반복할 수 있는 이동열은 walk, 정점을 반복하지 않는 경로는 simple path라고 구별한다. 아래 최단 경로 알고리즘은 반복 이동을 허용하는 모형을 사용한다. 음수 순환이 없다면 순환을 제거해 비용을 늘리지 않을 수 있지만, 음수 순환을 반복할 수 있으면 최소 비용 자체가 유한하지 않을 수 있다.[3,4]

정점별 배열의 한 칸을 읽거나 쓰는 비용과 정수의 덧셈·비교를 상수 시간으로 보는 모형에서 복잡도를 적는다. 따라서 표의 수치는 실행 시간이나 메모리 사용량을 보장하는 측정값이 아니다. 매우 큰 정수를 다루면 정수의 자릿수에 따른 연산 비용도 별도로 고려해야 한다. 아래 구현의 유한 가중치는 정수이며, `float("inf")`는 아직 도달하지 못했다는 표지로만 사용한다.

### (2) 인접 리스트와 인접 행렬

인접 리스트는 실제 간선을, 인접 행렬은 가능한 정점 쌍을 저장한다. 필요한 연산을 기준으로 선택한다. 다음 저장량은 각 정점의 리스트와 각 간선 항목 또는 행렬 칸을 직접 세어 얻은 것이다. 무방향 간선은 인접 리스트에 두 번 저장하지만 $m$은 입력 간선 수로 유지한다.[1,5,6]

| 표현 | 저장량 | 정점 `u`의 이웃 열거 | 주된 용도 |
| --- | --- | --- | --- |
| 인접 리스트 | $O(n+m)$ | 나가는 간선 수에 비례 | 탐색, 희소 그래프의 최단 경로 |
| 인접 행렬 | $O(n^2)$ | 한 행의 $n$칸 조사 | 모든 정점 쌍의 거리 계산 |
| 간선 리스트 | $O(m)$ | 전체 조사 시 $O(m)$ | Bellman–Ford, Kruskal |

가중치가 있는 입력의 각 항목을 `(u, v, w)`로 약속하면 다음 함수로 인접 리스트를 만든다. 가중치가 없는 탐색에서는 `(v, w)` 대신 `v`만 저장한다. 행마다 독립적인 리스트가 필요하므로 리스트 내포를 사용한다.

```python
def make_graph(n, edges, directed=True):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        if not directed:
            adj[v].append((u, w))
    return adj
```

리스트에 parallel edges를 보존하면 각각이 독립적인 이동 후보가 된다. 최단 거리만 필요한 행렬에서는 같은 $(u,v)$의 가중치 중 최솟값을 저장해도 된다. 그러나 간선의 식별자나 서로 다른 이동 방식이 후속 제약에 사용된다면, 최솟값 하나로 합치는 과정에서 필요한 정보를 잃을 수 있다. 이는 간선 정보와 상태 정의를 먼저 결정해야 하는 이유이다.[3,4]

행렬의 `0`을 간선 부재 표지로 사용하면 비용이 0인 실제 간선과 구별할 수 없다. 최단 거리용 초기 행렬은 대각선을 0, 나머지를 무한대로 두고 각 간선을 `min`으로 반영한다. 음수 self-loop가 있으면 대각선도 음수가 될 수 있어야 한다.[7,8]

```python
INF = float("inf")
distance = [[INF] * n for _ in range(n)]
for v in range(n):
    distance[v][v] = 0
for u, v, w in edges:
    distance[u][v] = min(distance[u][v], w)
```

## 2. 너비 우선 탐색과 깊이 우선 탐색

### (1) BFS의 거리 계층

Breadth-first search (BFS)는 시작점에서 간선 수가 적은 정점부터 처리한다. 모든 간선의 비용이 1인 경우, 처음 발견한 거리가 곧 최단 거리이다. 방향 그래프에서도 나가는 간선만 따라가면 같은 논리가 성립한다. 모든 간선 비용이 같은 양의 상수라면 BFS가 구한 간선 수에 그 상수를 곱하면 된다.[1,2]

시작점 $s$에서 정점 $v$까지의 최소 간선 수를 $d[v]$라 하자. BFS가 $u$에서 아직 발견하지 않은 $v$를 처음 발견하면 다음 관계로 거리를 정한다. `-1`은 이 정수 거리와 겹치지 않는 미방문 표지이다.[1,2]

$$
d[s]=0,\qquad d[v]=d[u]+1.
$$

큐에는 현재 거리 계층의 나머지 정점과 바로 다음 계층의 정점만 들어간다. 따라서 더 짧은 경로가 있었다면 그 직전 정점은 이미 먼저 처리되었어야 한다. **큐에 넣을 때** 방문 표시를 해야 여러 이웃이 같은 정점을 중복 삽입하지 않는다. 다음 함수의 `adj[u]`는 정수 정점 번호의 리스트이다.[1,2]

```python
from collections import deque


def bfs(adj, start):
    dist = [-1] * len(adj)
    parent = [-1] * len(adj)
    dist[start] = 0
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if dist[v] != -1:
                continue
            dist[v] = dist[u] + 1
            parent[v] = u
            queue.append(v)
    return dist, parent
```

정점마다 큐에 한 번 들어가고 인접 항목마다 한 번 조사하므로 배열 초기화를 포함한 시간은 $O(n+m)$, 그래프를 제외한 보조 공간은 $O(n)$이다.[1,2] Python의 `deque`는 양 끝 삽입·삭제를 $O(1)$ 시간에 지원한다.[9,10] `list.pop(0)`은 큐 길이에 비례하는 시간이 들므로, 앞 원소 제거를 이 연산으로 바꾸면 위의 선형 시간 분석을 그대로 적용할 수 없다.[9,11]

| 기록 | 의미 | 종료 뒤 해석 |
| --- | --- | --- |
| `dist[v] == -1` | 발견한 경로 없음 | 시작점에서 도달 불가 |
| `dist[start] == 0` | 이동하지 않은 시작 상태 | 시작점 자신까지 거리는 0 |
| `parent[v] == u` | 처음 발견할 때 거친 직전 정점 | 최소 간선 경로의 역방향 연결 |

경로 자체가 필요하면 도착점에서 부모를 따라가고 마지막에 순서를 뒤집는다. 아래 복원은 위 함수의 `parent`에 대해 정의되며, 도달 불가와 시작점 자신을 구분한다. 반환 경로의 정점 수에 비례하는 시간과 공간이 든다. 같은 길이의 경로가 여럿이면 인접 리스트의 순서에 따라 그중 하나를 얻는다.[1,2]

```python
def restore_path(start, target, dist, parent):
    if dist[target] == -1:
        return None
    path = []
    v = target
    while v != -1:
        path.append(v)
        if v == start:
            return path[::-1]
        v = parent[v]
    return None
```

### (2) DFS와 연결 성분

Depth-first search (DFS)는 한 갈래를 더 탐색할 수 없을 때까지 내려간 뒤 이전 갈림길로 돌아온다. 도달 가능성, 탐색 트리, 진입·종료 순서가 목적일 때 유용하다. 일반 그래프에서는 처음 찾은 경로가 최소 간선 경로라는 보장이 없다. 반복형 구현으로 재귀 호출의 깊이 제한에 대한 의존을 줄일 수 있다.[12,13,14,15]

무방향 그래프의 연결 성분은 서로 도달할 수 있는 정점들의 최대 집합이다. 미방문 정점에서 탐색을 새로 시작할 때마다 새 성분 번호를 부여하고, 앞선 탐색의 방문 정보는 유지한다. 다음 코드는 연결 성분을 위한 stack 탐색이며, 재귀 DFS의 정확한 진입·종료 순서를 재현하려는 코드는 아니다.[13,14]

```python
def connected_components(adj):
    label = [-1] * len(adj)
    count = 0
    for start in range(len(adj)):
        if label[start] != -1:
            continue
        label[start] = count
        stack = [start]
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if label[v] == -1:
                    label[v] = count
                    stack.append(v)
        count += 1
    return count, label
```

바깥 반복문이 $n$번 있어도 각 정점의 인접 리스트는 한 번만 조사하므로 전체 시간은 $O(n+m)$이다. 고립 정점도 하나의 성분이며, 정점이 없는 입력은 성분 수 0과 빈 배열을 반환한다. 단, 방향 그래프에 이 코드를 그대로 적용한 결과는 일반적으로 strong components가 아니다. 양방향 도달 가능성을 요구하는 strong connectivity와 방향을 제거한 뒤 판단하는 weak connectivity를 먼저 구별해야 한다.[13,14,16]

진입과 종료 이벤트가 필요한 DFS라면 stack에 정점만 저장하는 것으로는 부족하다. 현재 정점에서 다음에 조사할 이웃 위치도 함께 보관하거나 이웃 iterator를 유지해야 한다. 그래야 자식 탐색이 끝난 뒤 부모의 중단 지점으로 정확히 돌아간다. 이는 재귀 호출의 실행 상태를 명시적 자료구조로 옮긴 것이다.[12,13]

방향 순환을 DFS로 판별할 때는 미방문, 현재 활성, 종료의 세 상태를 구별한다. 활성 정점으로 향하는 간선은 현재 탐색 경로의 조상으로 돌아가는 순환을 만든다. 이미 종료한 정점으로 향하는 간선만으로 순환을 결론 내릴 수는 없다.[12,13]

| 도착 정점 상태 | DFS에서의 의미 | 방향 순환 판단 |
| --- | --- | --- |
| 미방문 | 새 자식 탐색 가능 | 아직 결정할 수 없음 |
| 활성 | 현재 재귀 경로에 존재 | 돌아가는 간선으로 순환 확인 |
| 종료 | 해당 정점의 탐색이 끝남 | 그 간선만으로는 순환을 뜻하지 않음 |

무방향 그래프에서는 방금 지나온 간선의 반대쪽 인접 항목을 순환으로 오인하지 않아야 한다. Parallel edges까지 허용하면 부모 **정점**만 제외하는 방식은 충분하지 않으므로 간선 식별자를 기준으로 되돌아온 간선 하나를 제외한다. 방향 그래프의 활성 상태 규칙과 무방향 그래프의 부모 간선 규칙은 서로 다른 판정이다.[17,18]

### (3) 트리의 부모와 깊이

트리는 연결되어 있고 순환이 없는 무방향 그래프이다. 서로 다른 두 정점을 잇는 simple path가 하나뿐이므로, 어느 탐색으로 찾더라도 그 유일한 경로를 얻는다. 정점 하나를 루트로 정하면 부모와 깊이를 정의할 수 있다. 루트 선택은 트리의 간선을 바꾸지 않고, 부모·자식 방향과 깊이만 바꾼다.[1,12,13]

$n\ge1$인 트리의 간선 수는 $n-1$이다. 루트를 제외한 각 정점에는 부모로 향하는 간선이 정확히 하나씩 있다는 사실로 셀 수 있다. $c$개의 성분을 가진 forest에서는 각 트리에 같은 계산을 적용하여 총 간선 수 $n-c$를 얻는다. 이 관계는 나중에 Kruskal 결과의 연결 여부를 해석할 때도 사용한다.[1,19,20]

이미 트리임이 보장된 입력에서는 아래처럼 부모 간선만 건너뛰어 부모와 깊이를 구할 수 있다. `depth`는 가중치 합이 아니라 루트에서의 간선 수이다. 일반 그래프에 그대로 쓰면 순환 때문에 재방문할 수 있으므로, 트리라는 사전 조건을 생략하면 안 된다.[1,12,13]

```python
def root_tree(adj, root):
    parent = [-1] * len(adj)
    depth = [0] * len(adj)
    stack = [root]
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            depth[v] = depth[u] + 1
            stack.append(v)
    return parent, depth
```

가중 트리에서 DFS로 부모 경로의 가중치를 누적하면 유일한 simple path의 비용을 구할 수 있다. 다만 음수 간선이 있는 무방향 그래프에서 반복 이동까지 허용한 최소 walk 문제는 다르다. 음수 간선을 왕복하면 비용을 계속 낮출 수 있으므로, 트리의 유일 경로 성질과 음수 최단 walk 문제를 혼동하면 안 된다.[4,7,12]

## 3. 격자와 상태 확장

### (1) 암시적 격자 그래프

격자의 칸을 정점으로, 허용된 이동을 간선으로 정의하면 별도의 인접 리스트 없이 탐색할 수 있다. $R$행 $C$열의 네 방향 이동 격자라면 정점은 최대 $RC$개이고 각 정점에서 조사할 후보는 최대 네 개이다. 다음 이웃 생성 규칙과 BFS를 결합할 때 시간과 방문 배열의 공간은 모두 $O(RC)$이다. 이 비용은 상태당 후보 수가 상수라는 조건에서 직접 유도된다.[2,21]

```python
def grid_neighbors(grid, r, c):
    rows, cols = len(grid), len(grid[0])
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            if grid[nr][nc] != "#":
                yield nr, nc
```

이 함수는 비어 있지 않은 직사각형 격자에서 `#`만 통행 불가라는 약속을 사용한다. 행 번호는 아래쪽으로, 열 번호는 오른쪽으로 증가한다. 대각선, 순간 이동, 특정 방향의 일방통행을 허용하면 이웃 생성 규칙을 바꾸어야 한다. 좌표가 가깝다는 사실보다 문제에서 허용한 이동이 그래프의 간선을 결정한다.[2,21]

### (2) 여러 시작점의 공통 거리

Multi-source BFS는 모든 시작점을 거리 0으로 큐에 넣은 뒤 하나의 BFS를 수행한다. 시작점 집합을 $S$, 한 시작점 $s$에서의 최단 간선 수를 $d_s[v]$라 하면 결과는 다음과 같다. 이는 모든 시작점이 같은 거리 계층에 놓인다는 BFS 불변식의 확장이며, 각 시작점에 대해 탐색을 따로 반복할 필요가 없다.[22,23]

$$
d_S[v]=\min_{s\in S}d_s[v].
$$

위 `bfs` 함수의 `while queue:` 앞 초기화 부분 전체를 다음으로 바꾸고, 함수의 입력 `start` 대신 시작점 목록 `sources`를 받는다. `parent` 배열도 초기화하므로 나머지 큐 처리와 `return dist, parent`를 그대로 유지할 수 있다. 시작점 중복은 한 번만 넣는다. 이 구현 규약에서는 빈 시작점 목록을 허용하며 그때 모든 거리가 `-1`로 남는다. 시작점 목록 길이를 $q$라 하면 초기화까지 포함한 시간은 $O(n+m+q)$이다.[22,23]

```python
dist = [-1] * len(adj)
parent = [-1] * len(adj)
queue = deque()
for s in sources:
    if dist[s] == -1:
        dist[s] = 0
        queue.append(s)
```

가장 가까운 시작점의 식별자도 필요하면 최초 발견 때 부모의 시작점 표지를 함께 전달한다. 거리가 같은 시작점이 여럿이면 큐의 초기 순서와 이웃 순서가 선택을 결정한다. 모든 시작점과의 거리를 각각 구하는 문제와 가장 가까운 하나까지의 거리를 구하는 문제는 출력 정보량부터 다르다.[22,23]

### (3) 이력의 상태화

어떤 정점에 도착한 뒤 가능한 행동이 이전 이력에 따라 달라진다면 정점 번호만으로 방문 여부를 기록할 수 없다. 필요한 이력을 유한한 상태로 요약하여 `(위치, 상태)`를 새로운 정점으로 만든다. BFS의 `(정점, 간선 수의 홀짝)` 변환이 대표적인 예이며, 가중 경로에서도 같은 상태 변환 뒤 적합한 최단 경로 알고리즘을 적용한다.[2,6]

| 이후 이동에 필요한 정보 | 확장 정점 | 방문·거리 배열의 구분 |
| --- | --- | --- |
| 이동 횟수의 홀짝 | `(v, parity)` | 정점마다 두 상태 |
| 일회성 권한의 사용 여부 | `(v, used)` | 미사용·사용 상태 |
| 서로 다른 열쇠의 보유 여부 | `(v, mask)` | 필요한 보유 집합별 상태 |

이 표는 상태 확장 원리를 적용한 모형 예시이다. 열쇠가 $k$종이고 각 열쇠의 보유 여부가 독립적이면 가능한 집합은 최대 $2^k$개이므로 위치가 같아도 상태 수가 지수적으로 늘 수 있다. 상태를 추가할 때는 미래의 합법 이동과 추가 비용을 결정하기에 충분한지, 동시에 불필요한 과거까지 저장하고 있지는 않은지 확인한다.[2,6]

확장 후 정점과 간선 수를 각각 $N,M$이라 쓰면 원래의 $n,m$ 대신 이 값을 복잡도에 넣어야 한다. 상태가 정점마다 $K$개라고 해서 전이까지 반드시 $Km$개인 것은 아니다. 한 원래 간선이 몇 종류의 상태 전이를 만드는지도 따로 세어야 한다. 마지막 할인 예제에서는 두 상태와 세 종류의 전이가 생긴다.[2,6]

특히 위치가 같은 두 이력을 하나로 합치려면, 이후 허용되는 이동과 그 추가 비용이 같아야 한다. 상태 함수 $\sigma$가 이동 이력 $h$를 요약한다고 할 때 다음 조건이 상태 설계의 기준이다. 이는 상태 확장 사례들에서 미래 행동을 보존한다는 요구를 명시한 것이다.[2,6]

$$
\sigma(h_1)=\sigma(h_2)
\ \Longrightarrow\
\text{동일한 후속 이동의 허용 여부와 추가 비용이 같다.}
$$

## 4. 가중 최단 경로

### (1) 완화와 알고리즘 선택

가중 최단 경로는 이미 발견한 경로를 더 싼 경로로 바꾸는 relaxation을 중심으로 구성한다. `dist[u]`가 발견한 $s\to u$ 경로의 비용이고 $w(u,v)$가 간선 비용이면, 그 간선을 이어 붙인 후보는 다음과 같다. 후보가 더 작을 때만 갱신한다.[3,4]

$$
d_{\mathrm{new}}[v]=\min\bigl(d[v],\ d[u]+w(u,v)\bigr).
$$

유한한 거리 값은 실제로 구성할 수 있는 경로의 비용이라는 불변식을 갖는다. 따라서 참 최단 거리보다 작게 추측한 값이 아니라, 현재까지 발견한 후보 중 최솟값이다. 핵심 차이는 어떤 순서로 완화를 수행하고 언제 더 이상 좋아지지 않는다고 판단하는가이다.[3,4]

| 가중치·구조 | 방법 | 이 문서의 구현 기준 시간 |
| --- | --- | --- |
| 모든 이동 비용 1 | BFS | $O(n+m)$ |
| 비용이 0 또는 1 | 0–1 BFS | $O(n+m)$ |
| 모든 비용이 음이 아님 | Lazy-heap Dijkstra | $O(n+m\log(m+2))$ |
| 음수 간선이 있는 일반 방향 그래프 | Bellman–Ford | $O(n+nm)$ |
| 모든 정점 쌍의 거리 | Floyd–Warshall | $O(n^3+m)$ |
| 방향 순환이 없음 | 위상 순서 완화 | $O(n+m)$ |

이 표의 선택 조건은 음수 순환의 영향을 받는 거리가 유한하지 않다는 점을 전제로 한다. Bellman–Ford와 Floyd–Warshall은 음수 간선을 허용하지만 음수 순환을 통과하는 쌍에 정상적인 최소 비용을 돌려주지는 않는다. 순환이 없는 경우에는 음수 간선이 있어도 위상 순서로 한 번씩 처리할 수 있다.[3,4,7,8,24,25]

### (2) Dijkstra와 오래된 heap 항목

Dijkstra는 잠정 거리가 가장 작은 정점을 꺼내 그 정점의 나가는 간선을 완화한다. 모든 가중치가 음이 아니면 유효하게 꺼낸 거리보다 더 싼 경로가 뒤늦게 등장할 수 없다. 더 싼 우회 경로를 가정하면 그 경로에서 아직 확정되지 않은 첫 정점이 현재 정점보다 먼저 선택되어야 하므로 모순이다. 이 확정 논리가 음수 간선에서는 성립하지 않는다.[3,4]

Python의 `heapq`를 이용하는 구현에서는 이미 들어간 원소의 우선순위를 직접 수정하지 않고, 개선된 `(거리, 정점)`을 새로 삽입한다. 같은 정점의 과거 거리도 heap에 남으므로 꺼낸 거리와 현재 `dist`를 비교한다. 정점 번호를 정수로 두면 거리 동률 때도 tuple의 비교가 정의된다.[26,27]

```python
from heapq import heappop, heappush


def dijkstra(adj, start):
    inf = float("inf")
    dist = [inf] * len(adj)
    dist[start] = 0
    heap = [(0, start)]
    while heap:
        cost, u = heappop(heap)
        if cost != dist[u]:
            continue
        for v, weight in adj[u]:
            candidate = cost + weight
            if candidate < dist[v]:
                dist[v] = candidate
                heappush(heap, (candidate, v))
    return dist
```

BFS처럼 **처음 삽입할 때** 정점을 확정하면 안 된다. 예를 들어 `u`로 직접 가는 비용이 8이고 다른 정점을 통한 비용이 5라면 `(8, u)`를 넣은 뒤에도 5로 개선되어야 한다. `(5, u)`가 처리된 후 꺼낸 `(8, u)`는 `dist[u]`와 달라 인접 간선을 다시 조사하지 않는다. 두 기록은 같은 정점에 대한 새 후보와 오래된 후보를 나타낸다.[3,26,27]

음이 아닌 그래프에서는 정점이 유효하게 처리될 때만 나가는 간선을 조사한다. 성공한 완화는 간선 조사당 최대 한 번이므로 heap 삽입은 최대 $m+1$번이고, heap에 동시에 $O(m)$개 항목이 남을 수 있다. 배열 초기화까지 포함한 시간은 $O(n+m\log(m+2))$, 인접 리스트까지 포함한 공간은 $O(n+m)$이다. `+2`는 간선이 없을 때도 로그 표기를 정의하기 위한 편의이다.[3,26]

Simple graph에서는 $m=O(n^2)$이므로 로그 항을 $O(\log n)$으로 단순화할 수 있다. Parallel edges의 수에 제한이 없는 모형에서는 $\log m$과 $\log n$을 무조건 같다고 놓지 않는다. 목표 정점만 필요하다면 그 정점을 **오래된 항목 검사를 통과해 꺼냈을 때** 종료할 수 있다. 처음 발견했을 때의 종료는 같은 보장을 갖지 않는다.[3,4,26]

### (3) 0–1 BFS

0–1 BFS는 가중치가 정확히 0 또는 1일 때 Dijkstra의 우선순위 처리를 deque로 단순화한다. 현재 유효한 최소 거리 $d$에서 새로 생기는 후보는 $d$ 또는 $d+1$뿐이다. 비용 0의 개선은 앞에, 비용 1의 개선은 뒤에 넣으면 작은 거리부터 처리하는 순서를 유지한다.[21,24]

```python
from collections import deque


def zero_one_bfs(adj, start):
    dist = [float("inf")] * len(adj)
    dist[start] = 0
    queue = deque([(0, start)])
    while queue:
        cost, u = queue.popleft()
        if cost != dist[u]:
            continue
        for v, weight in adj[u]:
            candidate = cost + weight
            if candidate < dist[v]:
                dist[v] = candidate
                item = (candidate, v)
                if weight == 0:
                    queue.appendleft(item)
                else:
                    queue.append(item)
    return dist
```

위 구현은 삽입 시 거리도 저장해 오래된 항목을 건너뛴다. 유효한 항목의 거리 순서가 Dijkstra와 같으므로 정점의 나가는 간선을 한 번만 유효하게 조사하며, 삽입·삭제는 간선 조사 수에 비례한다. `deque`의 끝 연산 비용을 적용하면 시간은 $O(n+m)$이다. 보조 공간의 안전한 상한은 중복 항목을 포함하여 $O(n+m)$이다.[9,10,21,24]

일반 BFS의 최초 발견 표시는 여기서 사용할 수 없다. 비용 1로 발견한 정점이 다른 정점을 통한 비용 0의 이동으로 개선될 수 있기 때문이다. 또 가중치가 1과 2라는 이유만으로 같은 앞·뒤 규칙을 사용하면 안 된다. 0과 1에서 성립한 두 거리 계층의 불변식이 그 규칙으로 유지되는지부터 다시 증명해야 한다.[3,21,24]

### (4) Bellman–Ford와 음수 순환

Bellman–Ford는 모든 간선을 반복 조사한다. 시작점에서 도달 가능한 음수 순환이 없다면 최단 경로 하나를 $n-1$개 이하의 간선으로 선택할 수 있다. 따라서 $n-1$회의 전체 간선 조사 뒤에는 모든 도달 가능한 거리가 최적값이다. 한 회 안에서 갱신값을 바로 쓰는 구현은 간선 순서에 따라 여러 간선을 연속 전파할 수도 있으므로, “$k$회 뒤 정확히 $k$개 이하 간선의 후보만 담는다”는 설명은 맞지 않는다.[4,25]

다음 함수는 간선 리스트 `edges`를 사용한다. 반환값 두 번째 항목은 시작점에서 도달 가능한 음수 순환의 존재 여부이다. 존재하면 첫 항목을 `None`으로 돌려 중간 거리 배열을 최단 거리로 오용하지 않게 한다. 도달 불가 정점의 값은 정상 종료 시 `inf`로 남는다.[4,25]

```python
def bellman_ford(n, edges, start):
    inf = float("inf")
    dist = [inf] * n
    dist[start] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, weight in edges:
            if dist[u] != inf and dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                changed = True
        if not changed:
            break
    for u, v, weight in edges:
        if dist[u] != inf and dist[u] + weight < dist[v]:
            return None, True
    return dist, False
```

추가 한 번의 조사에서 개선할 수 있는 간선이 남으면 시작점에서 도달 가능한 음수 순환이 있다. 개선이 전혀 없는 회가 나오면 거리 배열이 고정되었으므로 일찍 끝낼 수 있다. 최악에는 $n-1$회의 $m$개 조사와 추가 조사가 필요하며 초기화까지 포함해 $O(n+nm)$이다.[4,25]

음수 순환이 있다고 해서 모든 정점의 거리가 무의미해지는 것은 아니다. 시작점에서 그 순환에 도달하고, 다시 목표 정점에 도달할 수 있어야 그 목표 비용을 끝없이 낮출 수 있다. 위 함수는 영향받은 정점을 분류하는 대신 원점 기준 거리 계산 전체를 보수적으로 거부하는 인터페이스이다. 다른 성분의 음수 순환은 이 함수의 검출 대상이 아니다.[4,7,25]

### (5) Floyd–Warshall과 모든 정점 쌍

Floyd–Warshall은 경로 중간에 허용하는 정점 집합을 차례로 넓힌다. $D^{(k)}[i,j]$를 중간 정점으로 `0`부터 `k-1`까지만 허용했을 때의 최소 비용이라 하자. 새 정점 $k$를 사용하지 않는 경우와 사용하는 경우를 비교하면 다음 정확한 점화식을 얻는다. 음수 순환이 없는 조건에서 $k$를 지나는 최적 경로를 앞뒤 두 최적 부분 경로로 나눌 수 있다.[7,8]

$$
D^{(k+1)}[i,j]=\min\left(D^{(k)}[i,j],\ D^{(k)}[i,k]+D^{(k)}[k,j]\right).
$$

그래서 `k` 반복문을 가장 바깥에 두어야 한다. `i, j`만 먼저 반복하면서 갱신하는 것은 같은 점화식의 계산 순서가 아니다. 아래 구현은 초기 행렬 구성부터 포함하며, 음수 대각선이 생기면 음수 순환을 보고하고 전체 거리 행렬을 반환하지 않는다.[7,8]

```python
def floyd_warshall(n, edges):
    inf = float("inf")
    dist = [[inf] * n for _ in range(n)]
    for v in range(n):
        dist[v][v] = 0
    for u, v, weight in edges:
        dist[u][v] = min(dist[u][v], weight)
    for k in range(n):
        for i in range(n):
            if dist[i][k] == inf:
                continue
            for j in range(n):
                if dist[k][j] != inf:
                    candidate = dist[i][k] + dist[k][j]
                    if candidate < dist[i][j]:
                        dist[i][j] = candidate
    if any(dist[v][v] < 0 for v in range(n)):
        return None, True
    return dist, False
```

정점 삼중 반복은 $O(n^3)$, 행렬 공간은 $O(n^2)$이다. 입력 간선을 읽는 시간까지 포함하면 $O(n^3+m)$이다. 단일 시작점만 필요하거나 $n$이 큰 희소 그래프라면 모든 쌍 행렬을 만드는 비용이 불필요할 수 있다. 반대로 모든 쌍의 거리가 필요하고 행렬을 감당할 수 있다면 초기화와 점화식이 명료하다는 장점이 있다.[7,8]

## 5. 위상 정렬과 비순환 의존성

### (1) Kahn 알고리즘

Directed acyclic graph (DAG)는 방향 순환이 없는 그래프이다. 위상 정렬은 모든 간선 $u\to v$에서 $u$를 $v$보다 앞에 놓는 정점 순서이다. 방향 순환이 있으면 순환을 따라 서로 먼저 와야 하는 모순이 생기므로 불가능하며, DAG에는 위상 순서가 존재한다.[16,28]

Kahn 알고리즘은 **아직 제거하지 않은 그래프에서** 들어오는 간선 수가 0인 정점을 차례로 제거한다. 이 indegree는 원래 그래프의 고정 속성이 아니라 남은 의존 관계의 수이다. 어떤 정점을 출력하면 그 정점에서 나가는 간선을 제거한 것으로 보고 이웃의 값을 감소시킨다.[29,30]

```python
from collections import deque


def topological_order(adj):
    n = len(adj)
    indegree = [0] * n
    for neighbors in adj:
        for v in neighbors:
            indegree[v] += 1
    queue = deque(v for v in range(n) if indegree[v] == 0)
    order = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in adj[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    return order if len(order) == n else None
```

출력한 정점은 남은 선행 정점이 없으므로 그 위치에 안전하게 놓을 수 있다. 큐가 비었는데 정점이 남으면 남은 모든 정점에는 들어오는 간선이 있다. 이를 거슬러 계속 따라가면 유한한 정점 집합에서 정점을 반복하므로 순환이 존재한다. 따라서 출력 길이가 $n$인지 확인하면 순환 여부도 알 수 있다.[13,28,29,30]

각 정점과 간선을 한 번씩 처리하여 시간은 $O(n+m)$, 보조 공간은 $O(n)$이다. Parallel edges가 있으면 처음에 센 횟수만큼 indegree를 감소시켜야 한다. 고립 정점도 순서에 포함되고, 순서가 여러 개일 수 있다. 정점 번호가 작은 것을 항상 먼저 고르는 추가 요구가 없다면 일반 큐면 충분하다.[16,28,29,30]

### (2) DAG의 경로 계산

DAG에서는 위상 순서상 모든 선행 정점을 처리한 뒤 현재 정점에 도달한다. 따라서 현재 정점의 거리로 나가는 간선을 한 번씩 완화하면 된다. 이 방식은 간선 가중치의 부호보다 비순환 구조에 의존하므로 음수 간선도 허용한다.[3,4]

```python
# order는 가중 그래프의 방향 구조에 대한 유효한 위상 순서이다.
dist = [float("inf")] * len(adj)
dist[start] = 0
for u in order:
    if dist[u] == float("inf"):
        continue
    for v, weight in adj[u]:
        dist[v] = min(dist[v], dist[u] + weight)
```

위의 `topological_order`는 정수 이웃을 받으므로, 가중 인접 리스트에서 호출하려면 `v`만 추출한 방향 구조를 전달하거나 indegree 계산과 감소에서 `(v, weight)`를 풀도록 수정한다. 위상 정렬과 거리 완화를 합해 $O(n+m)$이다. 순환이 있는 입력에서 일부 순서만 얻어 이 코드를 실행하면 유효한 답을 보장할 수 없다.[3,4,29]

## 6. 서로소 집합과 최소 신장 구조

### (1) DSU의 대표자와 병합

Disjoint set union (DSU)은 서로 겹치지 않는 집합들의 분할을 유지한다. `find(x)`는 원소가 속한 집합의 대표자를 돌려주고, `union(a, b)`는 두 집합을 합친다. 무방향 연결에서 간선이 추가될 때 두 끝점의 집합을 합치면 현재 연결 여부를 관리할 수 있다. 대표자 번호는 구현상 선택이며 가장 작은 번호나 경로상의 특정 정점을 뜻하지 않는다.[31,32]

다음 구현은 작은 집합의 루트를 큰 집합의 루트에 붙이는 union by size와, 찾는 경로의 부모를 루트로 바꾸는 path compression을 함께 사용한다. `size`는 대표자 위치에서만 집합 크기로 해석한다. 반환값은 실제로 다른 두 집합을 합쳤는지 나타낸다.[31,32]

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

    def find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != x:
            nxt = self.parent[x]
            self.parent[x] = root
            x = nxt
        return root

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        self.components -= 1
        return True
```

두 최적화를 결합하면 연산당 amortized 시간은 $O(\alpha(n))$이다. $\alpha$는 inverse Ackermann 함수이며 매우 느리게 증가하지만, 이를 각 호출이 엄밀히 상수 시간이라는 뜻으로 읽으면 안 된다. 분석은 여러 연산을 수행한 총비용에 대한 보장이다. 이 복잡도 정리의 상세 증명은 여기서 생략한다.[19,31]

DSU의 부모 링크는 집합을 빠르게 찾기 위한 내부 표현이다. 경로 압축 때 원래 그래프에 없던 정점 쌍으로 부모가 바뀔 수 있으므로, 이를 실제 이동 경로로 출력하면 안 된다. 또한 기본 DSU는 병합은 지원하지만 간선 삭제로 성분을 다시 나누는 작업을 직접 지원하지 않는다.[31,32]

### (2) Kruskal과 최소 신장 forest

Minimum spanning tree (MST)는 연결된 무방향 가중 그래프의 모든 정점을 연결하는 트리 중 간선 가중치 합이 최소인 것이다. 출발점에서 각 정점까지의 최단 거리를 최소화하는 트리와 목적이 다르다. MST에서는 음수 가중치도 허용되며, 같은 가중치가 있으면 최적 트리가 여러 개일 수 있다.[19,33]

가능한 spanning tree의 집합을 $\mathcal T$, 선택한 트리를 $T$, 간선 비용을 $w(e)$로 쓰면 최적화 대상은 다음과 같다. 경로마다 가중치를 합하는 최단 경로와 달리 선택한 연결망의 각 간선을 한 번씩 센다.[19,33]

$$
\min_{T\in\mathcal T}\ \sum_{e\in T}w(e).
$$

Kruskal은 간선을 가중치 오름차순으로 조사하고, 끝점이 서로 다른 현재 성분에 속할 때만 선택한다. 같은 성분이면 이미 두 정점을 잇는 경로가 있으므로 간선을 추가하면 순환이 생긴다. 서로 다른 성분이면 DSU를 병합하며 선택 간선을 별도 목록에 기록한다.[19,20]

```python
def kruskal_forest(n, edges):
    dsu = DSU(n)
    total = 0
    chosen = []
    for u, v, weight in sorted(edges, key=lambda e: e[2]):
        if dsu.union(u, v):
            total += weight
            chosen.append((u, v, weight))
    return total, chosen, dsu.components
```

정당성은 교환 논증으로 보인다. 현재 선택 집합을 포함하는 최적 신장 트리가 있다고 가정하자. 새로 고른 간선이 그 트리에 없다면 추가했을 때 생기는 순환에서 두 현재 성분을 가로지르는 다른 간선을 제거한다. 오름차순 처리 때문에 제거한 간선보다 새 간선이 무겁지 않으므로 최적성은 유지된다. 동률이어도 비용을 늘리지 않는 교환이면 충분하다.[19,20]

연결되지 않은 입력에는 전체를 잇는 트리가 존재하지 않는다. 위 함수는 연결 성분별 MST를 모은 minimum spanning forest와 성분 수를 반환한다. 각 성분에서 같은 교환 논증이 적용된다. $n>0$일 때 최종 성분 수가 1이면 전체 MST이고, 2 이상이면 forest이다. 선택 간선 수가 $n-c$인지도 결과의 구조를 해석하는 기준이다.[19,20,33]

간선 정렬에는 $O(m\log(m+2))$, 집합 초기화에는 $O(n)$, 병합 조사에는 $O(m\alpha(n))$ 시간이 든다. 전체 상한은 $O(n+m\log(m+2))$이며, 복사 정렬과 선택 목록을 포함한 추가 공간은 $O(n+m)$이다. 무방향 입력 간선은 여기서는 한 번씩만 전달한다. Self-loop는 같은 대표자로 판정되어 제외되고, parallel edges는 비용 순서대로 자연스럽게 경쟁한다.[19,20,31]

## 7. 예제: 한 번의 선택적 간선 할인

### (1) 문제와 상태 정의

다음은 상태 확장과 Dijkstra를 결합하기 위해 구성한 예제이다. 정점 `0..n-1`과 방향 간선 `(u, v, w)`가 주어진다. `start`에서 `target`으로 이동할 때 **최대 한 번**, 통과하는 간선 하나의 비용 $w$를 $\lfloor w/2\rfloor$로 줄일 수 있다. 사용하지 않아도 되며, 도달 불가이면 `None`을 반환한다. 제약은 $1\le n\le 100000$, $0\le m\le 200000$, 정수 비용 $0\le w\le10^9$이다. Parallel edges와 self-loop를 허용하며, 시작점과 목표점은 유효한 정점이다. 이 제약은 계산 모형을 명시하기 위한 것이며 특정 환경의 실행 시간을 보장하지 않는다.

같은 정점에 도착하더라도 할인을 남겨 두었는지에 따라 이후 선택이 달라진다. 상태를 `(v, used)`로 두고 `used=0`은 미사용, `used=1`은 사용 완료로 정의한다. 아래 전이는 일반적인 상태 확장 원리를 이 문제의 규칙에 적용한 것이다.[2,6]

| 현재 상태 | 선택 | 다음 상태 | 추가 비용 |
| --- | --- | --- | --- |
| `(u, 0)` | 정상 요금 | `(v, 0)` | $w$ |
| `(u, 0)` | 이번 간선 할인 | `(v, 1)` | $\lfloor w/2\rfloor$ |
| `(u, 1)` | 정상 요금 | `(v, 1)` | $w$ |

사용 상태에서 미사용 상태로 돌아가는 전이는 없다. 원래 간선 하나당 세 전이가 있고 정점마다 두 상태가 있으므로 확장 그래프에는 $2n$개 정점과 $3m$개 전이가 있다. 모든 비용이 음이 아니므로 이 그래프에 Dijkstra를 적용할 수 있다. 전이 목록을 실제로 만들 필요 없이 원래 인접 리스트를 조사할 때 필요한 전이만 계산한다.[2,3,4]

### (2) 답안 함수

`dist[v][used]`는 정확히 그 상태까지의 최소 비용 후보이다. 초기값은 `(start, 0)`만 0으로 두며, 선택적 할인 조건에 맞게 마지막에는 목표점의 두 상태 중 작은 것을 반환한다. 모든 행은 독립적인 리스트로 생성한다. 아래 함수는 앞 절의 함수를 호출하지 않고 단독으로 사용할 수 있는 형태이다.

```python
from heapq import heappop, heappush


def shortest_with_discount(n, edges, start, target):
    adj = [[] for _ in range(n)]
    for u, v, weight in edges:
        adj[u].append((v, weight))

    inf = float("inf")
    dist = [[inf, inf] for _ in range(n)]
    dist[start][0] = 0
    heap = [(0, start, 0)]

    while heap:
        cost, u, used = heappop(heap)
        if cost != dist[u][used]:
            continue
        for v, weight in adj[u]:
            normal = cost + weight
            if normal < dist[v][used]:
                dist[v][used] = normal
                heappush(heap, (normal, v, used))
            if used == 0:
                reduced = cost + weight // 2
                if reduced < dist[v][1]:
                    dist[v][1] = reduced
                    heappush(heap, (reduced, v, 1))

    answer = min(dist[target])
    return None if answer == inf else answer
```

거리 개선 조건을 `<`로 두므로 비용 0의 순환을 돌아 같은 값이 생겨도 새 항목을 넣지 않는다. Heap에는 `(비용, 정점, 사용 여부)`를 저장하며, 같은 비용에서 정점 번호와 상태가 비교되어도 최단 비용 계산에는 영향을 주지 않는다. 입력에 음수 비용을 허용하려면 이 정당성과 복잡도 분석을 그대로 사용할 수 없다.[3,26,27]

### (3) 수동 추적과 정답

아래 입력은 문서에서 구성한 것이다. 도착점은 3이며, 정점 4는 고립되어 있다. 표시한 정답은 코드를 실행한 출력이 아니라 경로별 비용을 직접 비교해 얻은 값이다.

```python
n = 5
edges = [
    (0, 1, 8),
    (0, 2, 5),
    (1, 2, 1),
    (1, 3, 8),
    (2, 3, 10),
]
start, target = 0, 3
# 수동 도출 정답: 10
```

처음 `(0,0)`을 처리하면 정점 1의 미사용·사용 비용은 각각 8과 4, 정점 2는 각각 5와 2가 된다. Heap에서 같은 비용이면 정점 번호가 앞선 항목이 먼저 나오며, 아래 표는 오래되지 않은 항목에서 발생하는 주요 개선만 적는다.

| 꺼낸 `(비용, 정점, used)` | 주요 거리 개선 | 의미 |
| --- | --- | --- |
| `(0, 0, 0)` | `d[1]=[8,4]`, `d[2]=[5,2]` | 첫 간선의 할인 여부 분기 |
| `(2, 2, 1)` | `d[3][1]=12` | 첫 간선을 할인한 뒤 정상 이동 |
| `(4, 1, 1)` | 더 좋은 후보 없음 | 사용한 할인을 되돌릴 수 없음 |
| `(5, 2, 0)` | `d[3][0]=15`, `d[3][1]=10` | 비용 10의 마지막 간선을 할인 |
| `(8, 1, 0)` | 더 좋은 후보 없음 | 이 경로는 목표 비용을 개선하지 못함 |
| `(10, 3, 1)` | 나가는 간선 없음 | 사용 상태의 최적 비용 확정 |

이후 `(12,3,1)`은 현재 거리 10과 달라 버리고, `(15,3,0)`은 미사용 상태의 유효한 거리이다. 정점 4의 두 값은 모두 무한대로 남는다. 미사용 경로 `0→2→3`의 비용은 15이고, 마지막 간선을 할인하면 다음처럼 10이 된다.

$$
5+\lfloor10/2\rfloor=10.
$$

이 입력은 세 가지 `0→3` 경로만 갖는다. `0→1→3`은 최선의 할인으로 12, `0→1→2→3`은 14, `0→2→3`은 10이다. 따라서 경로를 직접 열거한 결과와 상태별 수동 추적이 일치한다. 여기서 할인 전 최단 경로만 구한 뒤 임의의 간선을 할인하는 방식을 일반 해법으로 결론 내리지는 않는다. 할인으로 경로들의 비용 순위 자체가 바뀔 수 있으므로 함수는 두 상태를 모두 유지한다.

### (4) 정당성·복잡도·경계 조건

원래 문제의 합법 이동열 하나를 잡으면 각 위치에 할인 사용 여부를 붙여 확장 그래프의 이동열을 만들 수 있다. 정상 간선은 상태를 유지하고, 할인한 간선에서만 0에서 1로 바뀐다. 반대로 확장 그래프의 이동열에서 상태 표지를 지우면 할인을 최대 한 번 사용한 원래 이동열이 된다. 대응 전후의 간선별 비용도 같으므로 두 문제의 최적 비용이 같다. 이 비용 보존 대응에 비음수 Dijkstra의 정당성을 적용한 것이 함수의 증명이다.[2,3,4]

확장 그래프의 크기는 상수 배이므로 시간은 $O(n+m\log(m+2))$, 공간은 $O(n+m)$이다. 상태당 거리 두 개만 있다고 heap도 $2n$칸에 제한되는 것은 아니다. 성공한 완화마다 과거 항목을 남긴 채 새 항목을 넣을 수 있으므로 heap 공간에는 간선 수가 들어간다.[26,27]

| 경계 조건 | 함수의 결과·처리 | 확인할 이유 |
| --- | --- | --- |
| `start == target` | 이동하지 않는 비용 0 | 할인은 선택 사항 |
| `m == 0`, 서로 다른 두 정점 | `None` | 초기 상태에서 목표로 전이 불가 |
| 가중치 0 또는 1 | 할인 후 비용 0 허용 | 정수 나눗셈과 strict 개선 조건 |
| 같은 두 정점 사이 여러 간선 | 각 간선 독립 완화 | 처음 발견한 간선으로 확정하지 않음 |
| 고립 목표 정점 | 두 상태 모두 무한대 | 도달 불가를 숫자 최적값과 구별 |
| 정확히 한 번 사용하도록 문제 변경 | `dist[target][1]`만 선택 | 선택적 사용과 출력 조건이 다름 |

경로까지 복원하려면 개선된 상태마다 이전 `(정점, used)`와 통과한 간선 식별자를 저장한다. 정점 번호만 부모로 기록하면 할인 전후 상태를 잃고, parallel edges에서는 어느 비용의 간선을 사용했는지도 구분할 수 없다. 이는 BFS의 부모 복원을 확장 상태 그래프에 그대로 적용한 것이다.[2,3]

## 8. 요약

- 그래프 표현은 이웃 열거, 전체 간선 순회, 모든 정점 쌍 처리 중 필요한 연산에 맞춘다.
- BFS의 최초 발견 확정은 동일 비용 이동에 의존한다. 가중 최단 경로에서는 거리 개선과 유효한 항목의 처리 순서를 구별한다.
- 상태 확장은 미래 행동에 필요한 이력을 정점의 일부로 만든다. 복잡도는 확장된 정점과 전이 수로 계산한다.
- 위상 정렬은 비순환 의존 관계를, DSU는 집합 병합을 다룬다. 기본 DSU의 부모는 이동 경로가 아니다.
- Kruskal의 목적은 연결망 전체의 간선 합 최소화이다. 연결되지 않은 입력은 최소 신장 forest로 해석한다.

## 9. 참고문헌

1. R. Sedgewick and K. Wayne, *Algorithms, 4th Edition*, [“4.1 Undirected Graphs”](https://algs4.cs.princeton.edu/41graph/).
2. CP-Algorithms contributors, [“Breadth-first search”](https://cp-algorithms.com/graph/breadth-first-search.html).
3. R. Sedgewick and K. Wayne, *Algorithms, 4th Edition*, [“4.4 Shortest Paths”](https://algs4.cs.princeton.edu/44sp/).
4. J. Erickson, *Algorithms* (2019), Chapter 8, [“Shortest Paths”](https://jeffe.cs.illinois.edu/teaching/algorithms/book/08-sssp.pdf), §§8.2–8.7 and Exercises.
5. J. Aspnes, [“C/Graphs”](https://www.cs.yale.edu/homes/aspnes/pinewiki/C%282f%29Graphs.html), Yale University, §§4.1–4.2.
6. E. Demaine, J. Ku, and J. Solomon, *6.006 Introduction to Algorithms*, Spring 2020, [“Recitation 9”](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/6afd7e9a85d7d36e204533569f9fccf6_MIT6_006S20_r09.pdf), pp. 1–4.
7. CP-Algorithms contributors, [“Floyd-Warshall — finding all shortest paths”](https://cp-algorithms.com/graph/all-pair-shortest-path-floyd-warshall.html).
8. J. Erickson, *Algorithms* (2019), Chapter 9, [“All-Pairs Shortest Paths”](https://jeffe.cs.illinois.edu/teaching/algorithms/book/09-apsp.pdf), §9.8.
9. Python Software Foundation, [“collections — Container datatypes: deque objects”](https://docs.python.org/3/library/collections.html#collections.deque).
10. University of Michigan, *ROB 502: Programming for Robotics*, Fall 2020, [“Class 11”](https://robotics.umich.edu/academics/courses/online-courses/rob502-f20/class11/), “Stacks, queues, and double-ended queues”.
11. University of Toronto, *CSC110/111 Course Notes*, [“10.7 Queues”](https://www.cs.toronto.edu/~david/course-notes/csc110-111/10-abstraction/07-queues.html), “Implementation efficiency”.
12. CP-Algorithms contributors, [“Depth First Search”](https://cp-algorithms.com/graph/depth-first-search.html).
13. J. Erickson, *Algorithms* (2019), Chapter 6, [“Depth-First Search”](https://jeffe.cs.illinois.edu/teaching/algorithms/book/06-dfs.pdf), §§6.1–6.3.
14. CP-Algorithms contributors, [“Finding Connected Components”](https://cp-algorithms.com/graph/search-for-connected-components.html).
15. Python Software Foundation, [“sys — System-specific parameters and functions: setrecursionlimit”](https://docs.python.org/3/library/sys.html#sys.setrecursionlimit).
16. R. Sedgewick and K. Wayne, *Algorithms, 4th Edition*, [“4.2 Directed Graphs”](https://algs4.cs.princeton.edu/42digraph/).
17. CP-Algorithms contributors, [“Finding bridges in a graph in O(N+M)”](https://cp-algorithms.com/graph/bridge-searching.html), “Implementation”.
18. R. Sedgewick and K. Wayne, [“Cycle.java”](https://algs4.cs.princeton.edu/code/edu/princeton/cs/algs4/Cycle.java.html), parallel-edge check and parent-edge handling.
19. J. Erickson, *Algorithms* (2019), Chapter 7, [“Minimum Spanning Trees”](https://jeffe.cs.illinois.edu/teaching/algorithms/book/07-mst.pdf), §§7.1–7.2, 7.5.
20. CP-Algorithms contributors, [“Minimum Spanning Tree — Kruskal”](https://cp-algorithms.com/graph/mst_kruskal.html).
21. J. Robel, “Trolley Troubles,” *Solution Sketches — CS@Mines High School Programming Competition 2024*, [pp. 19–22 (PDF pp. 20–23)](https://mineshspc.com/static/2024-solutions.pdf).
22. R. Sedgewick and K. Wayne, [“BreadthFirstPaths.java”](https://algs4.cs.princeton.edu/code/edu/princeton/cs/algs4/BreadthFirstPaths.java.html), multiple-source constructor and `bfs` implementation.
23. [“Breadth-First Search”](https://site.ada.edu.az/~medv/acm/Articles/graphs/breadth_eng.pdf), ADA University-hosted teaching material, PDF pp. 6–9, simultaneous sources and “Bitmap”.
24. CP-Algorithms contributors, [“0-1 BFS”](https://cp-algorithms.com/graph/01_bfs.html).
25. CP-Algorithms contributors, [“Bellman-Ford — finding shortest paths with negative weights”](https://cp-algorithms.com/graph/bellman_ford.html).
26. CP-Algorithms contributors, [“Dijkstra on sparse graphs”](https://cp-algorithms.com/graph/dijkstra_sparse.html), “priority_queue”.
27. Python Software Foundation, [“heapq — Heap queue algorithm”](https://docs.python.org/3/library/heapq.html), “Priority Queue Implementation Notes”.
28. CP-Algorithms contributors, [“Topological Sorting”](https://cp-algorithms.com/graph/topological-sort.html).
29. R. Sedgewick and K. Wayne, [“TopologicalX.java”](https://algs4.cs.princeton.edu/code/edu/princeton/cs/algs4/TopologicalX.java.html).
30. N. Troccoli, Stanford University, *CS 106X*, [“Lecture 25: Topological Sort”](https://web.stanford.edu/class/archive/cs/cs106x/cs106x.1192/lectures/Lecture25/Lecture25.pdf), slides 80, 90, 93.
31. CP-Algorithms contributors, [“Disjoint Set Union”](https://cp-algorithms.com/data_structures/disjoint_set_union.html).
32. R. Sedgewick and K. Wayne, *Algorithms, 4th Edition*, [“1.5 Case Study: Union-Find”](https://algs4.cs.princeton.edu/15uf/).
33. R. Sedgewick and K. Wayne, *Algorithms, 4th Edition*, [“4.3 Minimum Spanning Trees”](https://algs4.cs.princeton.edu/43mst/).
