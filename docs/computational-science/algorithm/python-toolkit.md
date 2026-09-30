---
description: Python 자료구조와 표준 함수의 반환값·변경 효과·계산 비용을 정리하고 사건 집계와 순위 산정에 적용한다.
---

# Python data structures and functions

Python으로 알고리즘을 표현할 때에는 **무엇을 저장하는가**, **어떤 연산을 반복하는가**, **그 연산이 원본을 바꾸는가**를 함께 결정해야 한다. 같은 원소를 담더라도 위치로 접근하는 `list`, 이름으로 찾는 `dict`, 존재 여부를 기록하는 `set`은 서로 다른 연산에 적합하다. 이 문서는 Python 3.10 이상에서 사용할 수 있는 기본 자료구조와 표준 라이브러리를 그 선택 기준에 따라 정리한다.[1–4]

표의 함수 표기는 자주 사용하는 **호출 형태**이다. 모든 오버로드를 나열하지는 않으며, 생략 가능한 인자의 기본값은 필요한 곳에 함께 쓴다. 표의 입력 조건은 이 문서에서 설명하는 적용 범위이며, 함수가 허용하는 모든 입력이나 예외를 열거한 것은 아니다. 코드 조각은 해당 절의 전제를 적용하는 짧은 사용법이고, 마지막 사건 집계 문제만 입력부터 출력까지 갖춘 완전한 예제이다. 예상값과 복잡도는 명세와 수작업 추적으로 설명한다.

## 1. 연산 비용과 입력 크기

### (1) Big O와 비용 모형

시간복잡도는 입력 크기에 따른 기본 연산 횟수의 증가를 나타낸다. 입력 원소 수를 $n$, 수행 비용을 $T(n)$이라고 할 때, Big O 표기 $T(n)=O(f(n))$는 충분히 큰 $n$에서 $T(n)$이 양의 상수 배 $f(n)$을 넘지 않는다는 상한이다. 실행 시간의 초 단위 예측이나 모든 입력에서 정확히 같은 횟수를 뜻하지 않는다.[1,5]

이 문서의 컨테이너 비용은 통상적인 CPython 구현을 기준으로 한다. 원소 참조의 이동, 길이가 제한된 정수의 산술, 짧은 키의 비교·해시를 상수 비용으로 놓는다. 긴 문자열과 큰 정수를 다룰 때에는 이 가정을 다시 검토해야 한다. Python의 정수는 고정된 비트 수에서 잘리는 자료형이 아니므로, 원소 수만으로 모든 산술 비용을 설명할 수는 없다.[2–4,6,7]

| 입력에서 반복하는 일 | 대표 증가율 | 판단할 내용 |
| --- | --- | --- |
| 인덱스 하나 접근 | $O(1)$ | 입력 전체를 훑는가 |
| 탐색 구간을 절반씩 축소 | $O(\log n)$ | 정렬 등 선행 조건이 있는가 |
| 원소를 한 번씩 처리 | $O(n)$ | 원소당 작업도 상수 비용인가 |
| 전체 비교 정렬 | $O(n\log n)$ 상한 | 비교 키 생성 비용이 큰가 |
| 모든 순서쌍 비교 | $O(n^2)$ | 내부 반복 범위가 외부와 함께 커지는가 |

이 표는 복잡도를 읽는 분류 기준이며 입력 제한만 보고 실행 가능 시간을 단정하는 표가 아니다. 예를 들어 바깥 반복이 $n$번이고 안에서 길이 $n$인 리스트의 포함 여부를 매번 검사하면, 코드의 반복문은 하나여도 최악의 비교 횟수는 이차로 증가한다. 반대로 두 반복문을 차례로 한 번씩 수행하면 비용을 곱하지 않고 더한다.[1,2,5]

### (2) 최악·평균·분할상환 비용

**최악 비용**은 같은 크기의 입력 중 가장 비싼 경우를 본다. **평균 비용**은 입력 또는 해시 분포에 관한 가정 아래 평균을 본다. **분할상환 비용**은 일련의 연산 전체 비용을 연산 수로 나누어 평가하며, 입력이 무작위라는 가정이 필요하지 않다. 따라서 “평균적으로 빠르다”와 “분할상환 상수 시간이다”는 바꾸어 쓸 수 없다.[1,3,5,8]

| 연산 | 통상적으로 사용하는 비용 | 숨겨진 조건 |
| --- | --- | --- |
| `a[i]` | $O(1)$ | `a`가 `list`, 유효한 인덱스 |
| `a.append(x)` | 분할상환 $O(1)$ | 개별 용량 확장은 비쌀 수 있음 |
| `a.pop(0)` | $O(n)$ | 뒤 원소를 앞으로 이동 |
| `key in d` | 평균 $O(1)$, 최악 $O(n)$ | 해시·동등성 비교 비용 별도 |
| `a[l:r]` | $O(k)$ | 결과 원소 수 $k$만큼 새 리스트 생성 |

위치 접근의 상수 비용은 배열의 인덱스 접근 모형에, 사전의 평균·최악 구분은 해시 충돌 분석에 근거한다. 슬라이스는 결과에 참조 $k$개를 복사하므로 결과 길이에 비례한다.[2,3,8–10]

분할상환을 설명하는 단순 모형으로, 빈 배열에서 시작하여 용량이 찰 때마다 두 배로 늘린다고 하자. $n$번 추가하는 동안 이전 참조들을 옮기는 횟수는 기하급수적으로 늘어나는 용량의 합이다. 이는 CPython의 정확한 용량 증가식을 주장하는 예가 아니라 비용을 합산하는 원리를 보이는 모형이다.[2,5,8]

$$
1+2+4+\cdots+2^j=2^{j+1}-1<2n.
$$

여기서 $2^j$는 마지막 확장 때 옮긴 원소 수이며 $2^j<n$이다. 새 원소를 놓는 $n$번의 작업까지 합쳐도 전체가 $O(n)$이므로 추가 한 번의 분할상환 비용은 $O(1)$이다. 개별 확장이 $O(n)$이라는 사실과 모순되지 않는다. 확장이 아직 없는 $n=0,1$은 상수 비용으로 별도 처리한다.[5,8]

## 2. 입력 해석과 수치 표현

### (1) 줄과 토큰의 구분

입력 처리는 문자열을 읽는 단계와 그 문자열을 값으로 바꾸는 단계로 나눈다. `input()`은 한 줄을 문자열로 읽고 끝의 줄바꿈을 제거한다. 파일 같은 스트림의 `readline()`은 줄바꿈이 있으면 포함하여 반환한다. `read()`는 남은 내용을 한 번에 읽으므로, 입력을 모두 보관할 공간이 필요한지 먼저 판단한다.[4,11–14]

| 호출 형태 | 반환값 | 경계 또는 용도 |
| --- | --- | --- |
| `input()` | 한 줄의 `str` | 읽을 데이터 없이 입력이 끝나면 `EOFError` |
| `sys.stdin.readline()` | 줄바꿈을 포함할 수 있는 `str` | 명세가 지정한 개수의 줄을 읽을 때 사용 |
| `sys.stdin.read()` | 남은 전체 `str` | 전체 입력 크기만큼 저장 공간 필요 |
| `int(token)` | 십진 정수 | 정수 문자열이 아니면 `ValueError` |
| `float(token)` | 부동소수점 수 | 십진 소수의 정확한 저장을 보장하지 않음 |
| `print(*values, end=ending)` | 값을 텍스트로 출력 | 마지막에 붙일 문자열을 명시 |

표는 텍스트 표준 입력을 전제로 한다. 바이너리 입력을 선택하면 문자열 대신 `bytes`를 얻으므로 자료형 경계를 따로 설계해야 한다. 수치만 있는 작은 입력에서는 `list(map(int, input().split()))`이 한 줄의 값을 보관하는 직접적인 표현이다. 행마다 의미가 다른 입력에서는 전체 파일을 무조건 토큰으로 평탄화하기보다 행의 구조를 보존하는 편이 명세와 대응하기 쉽다.[4,11–14]

문자열 `s`의 분할과 문자열 목록의 결합은 다음처럼 구분한다. 아래 연산들은 `s`의 문자를 직접 바꾸지 않고 새 결과를 만든다.[6,15]

| 호출 형태 | 반환값과 의미 | 주의할 경계 |
| --- | --- | --- |
| `s.split()` | 공백 단위의 `list[str]` | 연속 공백을 묶고 양 끝 공백을 무시 |
| `s.split(sep, maxsplit=-1)` | 지정 구분자로 나눈 문자열 목록 | 연속 구분자 사이의 빈 문자열 유지 |
| `sep.join(parts)` | 문자열들을 연결한 `str` | `parts`의 각 원소는 문자열이어야 함 |
| `s.strip()` | 양 끝 공백을 제거한 `str` | 내부 공백은 유지 |

예를 들어 `'a  b'.split()`의 결과는 `['a', 'b']`이지만 `'a,,b'.split(',')`의 결과는 `['a', '', 'b']`이다. 빈 항목이 의미 있는 데이터에서는 두 방식을 혼동하면 필드 수가 달라진다. 숫자 목록을 출력 문자열로 결합할 때에는 먼저 문자열로 변환한다.[6,15]

```python
values = [4, 12, 7]
line = " ".join(map(str, values))  # 수작업 예상값: '4 12 7'
print(line)
```

입력 토큰의 수와 값의 범위는 별개의 조건이다. `a, b = map(int, line.split())`은 두 정수를 기대한다는 뜻이지 임의 개수의 정수를 받아 주는 코드가 아니다. 명세가 두 필드를 보장할 때에만 이 형태를 쓴다. 입력 크기를 줄 수로만 세면 매우 긴 한 줄의 처리 비용을 놓칠 수 있으므로, 파싱 비용에는 전체 문자 수도 포함한다.[4,6,15]

### (2) 정수와 부동소수점의 경계

개수·인덱스·정수 가중치에는 `int`를 유지한다. `float`는 유한 정밀도의 이진 부동소수점 표현이므로 `0.1`처럼 유한 십진 소수라도 정확히 표현되지 않을 수 있다. 출력 자릿수를 줄이는 작업과 내부 계산 오차를 없애는 작업은 다르다.[6,16,17]

정수 $a$, 0이 아닌 정수 $b$에 대해 몫과 나머지는 다음 관계를 만족한다.[4,6,7]

$$
a=(a//b)b+(a\%b).
$$

`//`는 음의 무한대 쪽으로 내린 몫이다. 예를 들어 $a=-7$, $b=3$이면 몫은 $-3$, 나머지는 $2$이다. 실수에서 `int(x)`는 0 쪽으로 잘라내므로 음수의 `//`와 의미가 다르다. 정수 나눗셈에 `int(a / b)`를 대신 쓰면 부동소수점 변환까지 개입한다.[4,6,7,17]

| 목적 | 표현 | 해석 |
| --- | --- | --- |
| 정수 몫·나머지 동시 계산 | `divmod(a, b)` | `(a // b, a % b)` |
| 실수의 아래 정수 | `math.floor(x)` | $x$ 이하의 가장 큰 정수 |
| 실수의 위 정수 | `math.ceil(x)` | $x$ 이상의 가장 작은 정수 |
| 허용오차 내 실수 비교 | `math.isclose(a, b, rel_tol=1e-9, abs_tol=0.0)` | 상대·절대 허용오차를 함께 사용 |

유한한 실수 $a,b$를 비교하며, 이 문서에서는 허용오차를 $0\leq r<1$, $u\geq0$인 유한한 값으로 정한다. $r$은 무차원 상대 허용오차 `rel_tol`, $u$는 비교값과 같은 단위를 가진 절대 허용오차 `abs_tol`이다. 이 유효한 적용 범위에서 `isclose`는 다음 기준을 사용한다.[17,18]

$$
|a-b|\leq\max\!\left(r\max(|a|,|b|),u\right).
$$

0 근처에서는 상대 허용오차만으로 기대하는 비교가 되지 않을 수 있다. 이때 문제의 수치 오차 기준에 맞춰 $u$를 지정한다. 반면 정수 개수의 일치 여부에는 허용오차를 도입할 이유가 없다. 입력 자료형이 같아 보여도 “정확한 동일성”과 “수치적 근접성” 중 무엇을 묻는지 구분해야 한다.[16–18]

## 3. 기본 컨테이너와 변경 효과

### (1) List와 tuple

`list`는 순서가 있는 변경 가능한 원소열이며, `tuple`은 원소 참조의 배열을 변경할 수 없는 원소열이다. 이 절의 tuple 예시는 정수·문자열처럼 불변인 원소를 묶는 경우로 제한한다.[6,9,19]

| 자료구조 | 접근 기준 | 주된 용도 |
| --- | --- | --- |
| `list` | 0부터 시작하는 위치 | 값을 교체하거나 뒤에 추가하는 원소열 |
| `tuple` | 0부터 시작하는 위치 | `(행, 열)`, `(우선순위, 식별자)` 같은 묶음 |
| `dict` | 해시 가능한 키 | 이름별 누적값, 상태별 결과 |
| `set` | 해시 가능한 원소 | 방문 여부, 중복 제거, 집합 연산 |

빈 리스트는 `[]`, 빈 tuple은 `()`, 원소 하나의 tuple은 `(x,)`로 쓴다. `(x)`는 괄호로 묶인 표현식일 뿐이다. `a[l:r]`는 왼쪽 끝을 포함하고 오른쪽 끝을 제외한다. 인덱스 `-1`은 마지막 원소를 뜻하지만 빈 원소열에서 마지막 원소가 생기는 것은 아니다.[6,9,19]

리스트 메서드는 **반환값**과 **리스트에 남는 변화**를 따로 읽어야 한다. 다음 표에서 $n$은 기존 길이, $k$는 추가하거나 복사하는 원소 수이다. 삽입·삭제의 원소 이동, 검색의 순차 비교, 복사의 참조 수를 세면 선형 비용 행을 얻는다. 끝 추가의 연속 비용은 앞 절의 동적 배열 분할상환 모형을 따른다.[2,8,9,19]

| 호출 형태 | 반환값·변경 | 비용·적용 조건 |
| --- | --- | --- |
| `a.append(x)` | 끝에 한 원소 추가 | 분할상환 $O(1)$ |
| `a.extend(items)` | 원소들을 차례로 추가 | 추가분 기준 분할상환 $O(k)$ |
| `a.pop()` | 마지막 원소를 제거하고 반환 | 분할상환 $O(1)$, 비어 있지 않을 때 사용 |
| `a.pop(i)` | 지정 위치 원소를 제거하고 반환 | 일반 위치는 $O(n)$, 유효한 인덱스 사용 |
| `a.insert(i, x)` | 지정 위치 앞에 삽입 | $O(n)$ |
| `a.remove(x)` | 첫 동등 원소 삭제 | $O(n)$, 동등 원소가 있을 때 사용 |
| `a.index(x)` | 첫 동등 원소의 인덱스 | $O(n)$, 동등 원소가 있을 때 사용 |
| `a.copy()` | 새 얕은 복사 리스트 | $O(n)$, 원본 유지 |

`a.append([3, 4])`는 리스트 하나를 원소로 추가한다. `a.extend([3, 4])`는 두 정수 원소를 추가한다. 표에서 “추가”·“삭제”로 설명한 메서드는 원본의 상태를 바꾸는 호출로 사용한다. 변경된 원본과 새 결과를 받는 표현은 구분한다.[9,19]

### (2) 별칭과 얕은 복사

대입 `b = a`는 새 리스트를 만드는 복사가 아니다. 같은 객체를 가리키는 이름을 하나 더 만든다. `a.copy()`는 바깥 리스트를 새로 만들지만, 그 안의 원소 참조는 공유한다. 이것이 **얕은 복사**이다. `copy.deepcopy(a)`는 복합 객체의 내부를 재귀적으로 복사하는 별도의 연산이다.[20,21]

다음은 실행 결과 대신 객체의 공유 관계로 추적한 예이다.[20,21]

```python
a = [[1], [2]]
alias = a
shallow = a.copy()
alias.append([3])   # a와 alias의 바깥 리스트가 함께 길어짐
shallow[0].append(9)  # 첫 내부 리스트는 세 이름에서 공유됨
# a:       [[1, 9], [2], [3]]
# alias:   [[1, 9], [2], [3]]
# shallow: [[1, 9], [2]]
```

같은 원리로 `[[0] * width] * height`는 행 리스트 하나의 참조를 반복한다. 독립적으로 바꿀 행이 필요하면 행마다 새 리스트를 만든다. 아래에서는 각 반복에서 `[0] * width`를 새로 평가하므로 한 칸을 바꿔도 다른 행의 같은 열이 바뀌지 않는다. 이는 참조 공유 규칙에서 얻는 직접적인 적용이다.[6,20,21]

```python
height, width = 3, 4
grid = [[0] * width for _ in range(height)]
grid[0][1] = 7  # 첫 행의 두 번째 칸만 변경
```

복사 깊이는 자료의 소유권에 맞게 정한다. 정수 목록에서는 얕은 복사로 바깥 원소 교체를 독립시킬 수 있지만, 중첩된 목록을 수정하는 알고리즘은 안쪽 공유까지 살펴야 한다. 무조건 깊은 복사를 넣기보다 수정할 상태만 별도로 만들면 어떤 변화가 다른 상태에 전달되는지 명확해진다.[20,21]

### (3) Dict와 set

`dict`의 `in`은 값이 아니라 **키의 존재 여부**를 검사한다. `set`은 동등한 원소의 중복을 제거한다. 둘 다 키 또는 원소가 해시 가능해야 하므로, 변경 가능한 리스트를 그대로 키나 집합 원소로 넣을 수 없다. 정수 두 개의 좌표는 `(row, col)`처럼 tuple로 표현할 수 있다.[6,19,22,23]

| 호출 형태 | 결과 또는 변경 | 없는 원소·키 |
| --- | --- | --- |
| `d[key]` | 연결된 값 반환 | `KeyError` |
| `d.get(key, default=None)` | 값 또는 기본값 반환 | 기본값을 반환하며 삽입하지 않음 |
| `d[key] = value` | 값 삽입 또는 덮어쓰기 | 새 키 생성 |
| `d.items()` | `(키, 값)`들을 순회할 뷰 | 빈 사전이면 순회할 원소 없음 |
| `s.add(x)` | 원소 추가 | 이미 있으면 집합 의미상 변화 없음 |
| `s.remove(x)` | 원소 제거 | `KeyError` |
| `s.discard(x)` | 있으면 제거 | 없으면 그대로 유지 |

사전 호출은 공식 명세와 Stanford의 조회 예시를, 집합 변경은 공식 명세와 Duke의 오류·삭제 예시를 따른다.[6,22,23]

해시 테이블의 조회·추가·삭제를 상수 시간으로 쓰는 분석에는 해시 충돌이 과도하지 않다는 평균적 가정이 붙는다. 키 수가 $n$일 때 충돌이 집중되면 한 연산이 $O(n)$까지 나빠질 수 있다. 긴 문자열 키의 해시 계산 비용도 별도이며, 사용자 정의 객체의 해시 함수와 비교 함수는 이 표의 범위를 벗어난다.[3,6,10,22]

집합 연산은 입력의 의미를 직접 표현한다. `a & b`는 공통 원소, `a - b`는 `a`에만 있는 원소, `a | b`는 둘 중 하나에 있는 원소를 만든다. 순서를 요구하는 출력에서는 집합 자체의 순회 순서를 답의 순서로 사용하지 않고, 필요한 정렬 기준을 명시한다.[6,19,23]

```python
seen = set()
unique = []
for value in [8, 3, 8, 5, 3]:
    if value not in seen:
        seen.add(value)
        unique.append(value)
# 첫 등장 순서를 보존한 수작업 예상값: [8, 3, 5]
```

이 패턴에서 `seen`은 존재 여부를, `unique`는 출력 순서를 담당한다. 한 컨테이너에 두 목적을 억지로 맡기지 않아도 된다. 처리한 접두 구간에서 이미 본 값만 `seen`에 들어 있다는 불변식을 유지하면, 같은 값이 다시 나타날 때 추가를 건너뛰는 이유가 명확하다.[19,22]

## 4. 순회·변환·축약 함수

### (1) Iterable과 iterator

**Iterable**은 원소를 차례로 꺼내는 순회를 제공하는 객체이고, **iterator**는 현재 어디까지 꺼냈는지 상태를 유지하며 다음 값을 내는 객체이다. 리스트는 다시 순회할 수 있지만, 한 번 소비한 iterator의 값을 자동으로 되돌려 주지는 않는다. `map`, `zip`, `enumerate`의 결과를 “이미 계산된 리스트”로 간주하지 않아야 한다.[4,24–26]

| 호출 형태 | 반환값과 의미 | 경계 |
| --- | --- | --- |
| `range(stop)` | `0`부터 `stop` 전까지의 정수열 | 음의 `stop`이면 빈 원소열 |
| `range(start, stop, step=1)` | `step` 간격의 정수열 | 0이 아닌 `step` 사용, 끝은 제외 |
| `enumerate(items, start=0)` | `(번호, 원소)` iterator | 원래 인덱스와 시작 번호를 구분 |
| `zip(a, b)` | 대응 원소 tuple의 iterator | 짧은 쪽이 끝나면 종료 |
| `map(func, items)` | `func` 적용 결과의 iterator | 소비할 때 함수를 적용 |
| `list(items)` | 원소를 모은 새 리스트 | iterator를 끝까지 소비 |

`range`는 원소 전체를 리스트로 저장하지 않는 정수열이다. 단순 반복에는 그대로 사용하고 실제로 원소를 변경·보관할 때 `list(range(n))`을 만든다. `zip`으로 두 원소열을 묶을 때에는 길이가 같은지 입력 계약에서 확인해야 한다. 기본 호출이 짧은 쪽에서 멈추는 것은 누락 검사가 아니다.[4,6,24,25]

```python
names = ["amber", "blue", "cyan"]
scores = [12, 7, 12]
rows = [(name, score) for name, score in zip(names, scores)]
for number, row in enumerate(rows, start=1):
    print(number, row[0], row[1])
```

이 조각에서 번호는 표시 순서이며 `rows`의 0 기반 인덱스와 다르다. `map(int, tokens)`를 두 번 순회해야 한다면 처음부터 필요한 정수들을 리스트로 보관하거나, 매번 새 iterator를 만들어야 한다. 지연 평가가 결과 저장 비용을 줄이는 대신 소비 상태를 관리하게 한다는 점을 이해하면 불필요한 변환을 줄일 수 있다.[4,24–26]

### (2) 최소·최대·합·논리 축약

축약 함수는 여러 원소를 하나의 결과로 모은다. `min`과 `max`가 필요한데 전체를 정렬하면 필요하지 않은 순서까지 계산한다. 기본 스칼라 값에서는 한 번 훑어 얻는 최소·최대·합의 비용은 $O(n)$이다. 키 계산이나 덧셈이 비싸면 그 비용을 함께 세어야 한다.[2,4,9,25,27]

| 호출 형태 | 반환값 | 적용 범위 또는 빈 입력 |
| --- | --- | --- |
| `min(items, key=None)` | 키가 가장 작은 원소 | 비어 있지 않은 입력 사용 |
| `max(items, key=None)` | 키가 가장 큰 원소 | 비어 있지 않은 입력 사용 |
| `sum(items)` | 수치 원소들의 합 | 여기서는 비어 있지 않은 입력 |
| `any(items)` | 하나라도 참이면 `True` | `False` |
| `all(items)` | 모두 참이면 `True` | `True` |

논리 축약은 존재·전칭 조건에 대응한다. 빈 원소열에는 참인 사례가 없으므로 `any`는 거짓이며, 반례가 없으므로 `all`은 참이다. 반환값과 빈 입력 처리는 공식 정의를, 논리 해석은 전칭·존재 양화의 의미를 따른다.[4,27]

전체가 양수인지 묻는 표현은 `all(x > 0 for x in values)`이다. 여기서 빈 원소열까지 허용하는지 여부는 수학적 전칭 조건과 입력 명세의 문제이다. 최소 하나의 값이 있어야 한다면 비어 있지 않다는 조건을 별도로 확인한다.[4,24–26]

`key`는 비교용 값을 만들 뿐 원래 원소를 그 값으로 바꾸지 않는다. 따라서 `max(rows, key=lambda row: row[1])`은 점수만 반환하는 것이 아니라 선택된 행을 반환한다. 동점 처리까지 필요한 경우에는 필요한 우선순위를 tuple로 구성하거나 뒤 절의 전체 정렬을 사용한다.[4,9,28]

## 5. 집계용 collections

### (1) Counter와 defaultdict

`Counter`는 원소별 개수를, `defaultdict`는 없는 키에 사용할 값 생성 규칙을 제공한다. 값이 처음 등장했는지 확인하는 코드를 줄이지만 두 객체의 목적은 다르다. 단순 빈도는 `Counter`, 그룹별 원소 목록이나 누적 합은 `defaultdict`로 표현하면 저장하는 값의 의미가 드러난다.[29–31]

| 호출 형태 | 반환값 또는 효과 | 적용 |
| --- | --- | --- |
| `Counter(items)` | 원소별 개수의 새 객체 | 빈도 집계 |
| `c[key]` | 저장한 개수, 없으면 `0` | 특정 원소의 빈도 조회 |
| `c.update(items)` | 기존 빈도에 새 빈도를 더함 | 기존 개수에 추가 |
| `c.most_common(n)` | 빈도 내림차순 `(원소, 개수)` 목록 | 상위 빈도 확인 |
| `defaultdict(int)` | 없는 키에서 `0`을 만드는 사전 | 키별 정수 누적 |
| `defaultdict(list)` | 없는 키에서 새 리스트를 만드는 사전 | 키별 원소 묶기 |

`Counter.update`는 일반 사전의 값 덮어쓰기와 다르게 기존 개수에 더한다. `defaultdict(list)`의 인자는 리스트 객체 `[]`가 아니라 새 리스트를 만드는 호출 가능한 `list`이다. 각 새 키가 독립된 리스트를 받도록 한다.[29–31]

```python
from collections import Counter, defaultdict

labels = ["a", "b", "a", "c", "b", "a"]
counts = Counter(labels)  # a: 3, b: 2, c: 1
positions = defaultdict(list)
for i, label in enumerate(labels):
    positions[label].append(i)
# positions['a']: [0, 2, 5]
```

`defaultdict`에서 없는 키를 `d[key]`로 조회하면 기본값 생성과 삽입이 일어난다. 조회가 상태를 바꾸므로, 키가 이미 있는지만 판단하려는 때와 기본값을 만들어 집계를 시작하려는 때를 구분한다.[29,31,32]

명세가 “빈도 동점이면 이름 오름차순”처럼 두 번째 기준을 요구하면 `most_common`이라는 이름만으로 그 조건이 충족된다고 생각하지 않는다. 필요한 키를 명시한 정렬로 순서를 정의하는 편이 결과의 의미를 직접 보여 준다. 최종 문제에서는 빈도 대신 점수 합계를 집계하고 이 방식을 적용한다.[28–30]

### (2) Deque와 양 끝 연산

`collections.deque`는 양 끝에서 추가·제거하는 작업에 적합하다. 왼쪽과 오른쪽을 구별하는 메서드로 다음에 꺼낼 원소를 정한다. 여기서는 양 끝 연산의 의미만 사용한다.[19,29,33]

| 호출 형태 | 반환값·변경 | 경계 |
| --- | --- | --- |
| `deque(items)` | 새 deque | 순회 순서로 원소 보관 |
| `q.append(x)` | 오른쪽 추가 | 큐의 새 입력 |
| `q.appendleft(x)` | 왼쪽 추가 | 반대편에서 추가 |
| `q.pop()` | 오른쪽 원소 제거·반환 | 원소가 있을 때 사용 |
| `q.popleft()` | 왼쪽 원소 제거·반환 | 원소가 있을 때 사용 |

한쪽 끝에 넣고 반대쪽 끝에서 꺼내면 first-in, first-out (FIFO) 큐이다. 같은 끝에 넣고 꺼내면 last-in, first-out (LIFO) 스택이다. 자료구조의 이름보다 어떤 원소를 다음에 처리해야 하는지를 먼저 정하면, 스택·큐·우선순위 큐의 선택을 혼동하지 않는다.[19,33]

## 6. 정렬과 정렬된 자료의 탐색

### (1) Sort와 key

`sorted(items, key=None, reverse=False)`는 새 정렬 리스트를 반환하고, `a.sort(key=None, reverse=False)`는 리스트 `a`를 직접 정렬하며 `None`을 반환한다. 두 방식 모두 키가 같은 원소들의 기존 상대 순서를 유지하는 안정 정렬이다.[28,34]

| 필요한 결과 | 호출 형태 | 원본 |
| --- | --- | --- |
| 새 오름차순 목록 | `sorted(items)` | 유지 |
| 기존 리스트 재정렬 | `a.sort()` | 변경 |
| 점수 내림차순 | `sorted(rows, key=lambda r: r[1], reverse=True)` | 유지 |
| 점수 내림차순·이름 오름차순 | `sorted(rows, key=lambda r: (-r[1], r[0]))` | 유지 |

정수 점수의 부호를 뒤집으면 큰 점수가 작은 키가 되고, tuple은 앞 성분부터 비교하므로 같은 점수에서 이름이 두 번째 기준이 된다. `reverse=True`를 tuple 전체에 적용하면 이름 방향까지 뒤집히므로, 성분마다 정렬 방향이 다를 때에는 원하는 방향을 키 자체에 표현한다.[28,34]

정렬의 비교 횟수 상한은 $O(n\log n)$이다. 긴 문자열을 비교하거나 키를 만드는 데 별도 탐색이 필요하다면 그 비용을 더한다. “원본을 직접 정렬한다”는 표현은 새 결과 리스트를 반환하지 않는다는 뜻이며, 내부 보조 공간이 반드시 $O(1)$이라는 뜻은 아니다.[2,28,34]

### (2) Bisect의 경계 인덱스

`bisect`는 오름차순 원소열에서 **값을 넣어도 정렬이 유지되는 경계 인덱스**를 구한다. 존재 여부를 직접 반환하는 함수가 아니다. 여기서는 비교 가능한 값들을 담은 리스트를 사용하고 `key`는 지정하지 않는다.[35,36]

| 호출 형태 | 반환값·효과 | 비용 |
| --- | --- | --- |
| `bisect_left(a, x)` | 같은 값들 앞의 삽입 인덱스 | $O(\log n)$ |
| `bisect_right(a, x)` | 같은 값들 뒤의 삽입 인덱스 | $O(\log n)$ |
| `insort_left(a, x)` | 왼쪽 경계에 삽입 | $O(n)$ |
| `insort_right(a, x)` | 오른쪽 경계에 삽입 | $O(n)$ |

반환값이 `len(a)`여도 정상이며 “마지막 원소 뒤에 넣으라”는 뜻이다. `insort`는 탐색 뒤 리스트 원소들을 이동하므로 탐색 비용만 보고 로그 시간 삽입이라고 판단하면 안 된다. 정렬된 리스트의 탐색 구간을 절반씩 줄이면 비교 횟수가 로그 규모로 늘어나며, Python `bisect`도 이 이진 탐색 비용을 갖는다.[2,35–37]

```python
from bisect import bisect_left, bisect_right

a = [2, 4, 4, 4, 9]
left = bisect_left(a, 4)    # 1
right = bisect_right(a, 4)  # 4
count = right - left       # 3
pos = bisect_left(a, 7)    # 4
exists = pos < len(a) and a[pos] == 7  # False
```

정렬된 자료에서 같은 값은 연속 구간에 모인다. 따라서 두 경계의 차이는 그 값의 개수이다. 존재 확인은 경계가 범위 안에 있는지 먼저 확인한 뒤 실제 값을 비교한다. 이 결론은 `left` 앞의 값은 작고 `right` 뒤의 값은 크다는 경계 정의에서 직접 따른다.[35,36]

## 7. 스택·큐·우선순위 큐

### (1) 처리 순서와 컨테이너

스택은 가장 최근에 보류한 일을, 큐는 가장 먼저 들어온 일을 처리한다. 우선순위 큐는 들어온 시간과 독립적으로 비교 키가 가장 작은 일을 선택한다. 다음 대응은 알고리즘에서 “다음 원소”의 의미를 고르는 기준이다.[19,33,38,39]

| 다음에 처리할 원소 | 표현 | 넣기·꺼내기 |
| --- | --- | --- |
| 가장 최근 원소 | `list` 스택 | `append`, `pop` |
| 가장 오래 기다린 원소 | `deque` 큐 | `append`, `popleft` |
| 가장 작은 우선순위 | `heapq` 최소 힙 | `heappush`, `heappop` |

```python
from collections import deque

stack = []
stack.append("first")
stack.append("second")
latest = stack.pop()  # 'second'

queue = deque(["first", "second"])
earliest = queue.popleft()  # 'first'
```

위 조각처럼 꺼낼 원소가 있음을 알고 있을 때와 입력에 따라 비어 있을 수 있는 때를 구분한다. 반복 처리에서는 `while queue:`처럼 원소가 남아 있는 동안만 꺼내는 조건으로 빈 컨테이너의 예외를 피할 수 있다. 이러한 조건은 데이터가 없다는 상황을 오류로 볼지 정상 종료로 볼지 정하는 명세의 일부이다.[19,29,33]

### (2) Heapq의 불변식

최소 힙은 모든 부모가 자식보다 작거나 같은 순서 조건을 유지한다. 원소 수가 $n$인 리스트 `h`에서 유효한 자식 인덱스에 대해 다음 관계가 성립한다. $i$는 부모의 0 기반 인덱스이다.[38–40]

$$
h[i]\leq h[2i+1],\qquad h[i]\leq h[2i+2].
$$

이 조건으로부터 최소 원소가 `h[0]`에 있다는 사실이 따른다. 형제끼리나 서로 다른 부분 트리 사이에는 완전한 정렬을 요구하지 않으므로, 힙 리스트를 그대로 순회한 결과는 정렬된 결과가 아니다. 정렬 순서대로 꺼내려면 최소 원소 제거를 반복한다.[38–40]

| 호출 형태 | 반환값·변경 | 통상 비용 |
| --- | --- | --- |
| `heapify(h)` | 기존 리스트를 힙으로 변경 | $O(n)$ |
| `heappush(h, x)` | 힙에 추가 | 분할상환 $O(\log n)$ |
| `heappop(h)` | 최소 원소 제거·반환 | 분할상환 $O(\log n)$, 원소가 있을 때 사용 |
| `h[0]` | 최소 원소 조회 | $O(1)$, 원소가 있을 때 사용 |
| `heapreplace(h, x)` | 기존 최소를 반환하고 `x` 삽입 | $O(\log n)$, 원소가 있을 때 사용 |

삽입·제거는 힙 높이만큼의 비교와 이동으로 순서 조건을 회복한다. 리스트 저장 공간의 재할당까지 포함하는 개별 호출에는 더 큰 비용이 생길 수 있으므로 표는 연속 연산에 대한 분할상환 비용을 표시했다. 모든 원소가 이미 있다면 반복 삽입으로 만들기보다 선형 시간 `heapify`를 사용한다.[2,5,38,40]

정수의 최대값을 먼저 꺼내려면 부호를 뒤집어 최소 힙에 넣고 꺼낸 값의 부호를 되돌릴 수 있다. 아래는 순서를 뒤집는 변환에서 바로 얻는 사용법이며, 음수 원소에도 같은 원리가 적용된다.[38,39]

```python
import heapq

h = [-value for value in [6, 2, 11]]
heapq.heapify(h)
largest = -heapq.heappop(h)  # 11
```

우선순위가 같은 레코드를 다룰 때에는 `(priority, sequence, payload)`처럼 두 번째 성분에 서로 다른 정수 순번을 둘 수 있다. 그러면 우선순위 동점은 순번으로 결정되어, 비교를 지원하지 않는 `payload`끼리 비교하는 상황을 피한다. 이는 tuple의 사전식 비교와 힙의 최소값 선택을 결합한 적용이다.[28,38,40]

## 8. 조합 생성과 수학 함수

### (1) Itertools의 목적별 선택

`itertools`는 순회하는 자료를 결합하거나 후보를 만드는 도구를 제공한다. 결과를 iterator로 받는다고 해서 가능한 후보의 수 자체가 줄어드는 것은 아니다. 입력 원소 수를 $n$, 뽑는 길이를 $r$로 둘 때 순열·조합·중복 선택은 서로 다른 후보 집합을 나타낸다.[24,41]

| 호출 형태 | 만드는 값 | 구분 기준 |
| --- | --- | --- |
| `chain(a, b)` | `a` 다음에 `b`의 원소 | 원소열 연결 |
| `accumulate(items)` | 차례로 누적한 합 | 중간 누적값 모두 필요 |
| `product(items, repeat=r)` | 길이 $r$의 tuple | 순서 있음, 같은 위치 재선택 가능 |
| `permutations(items, r)` | 길이 $r$의 tuple | 순서 있음, 같은 위치 재선택 없음 |
| `combinations(items, r)` | 길이 $r$의 tuple | 순서 없는 위치 선택 |
| `combinations_with_replacement(items, r)` | 길이 $r$의 tuple | 순서 없는 선택, 위치 재선택 가능 |

여기서는 입력값들이 서로 다른 경우로 제한하여, 입력 위치 선택과 값 선택을 구분할 필요가 없는 예를 사용한다. 순서가 결과의 일부인지는 순열과 조합을 선택하는 기준이다.[24,41]

```python
from itertools import combinations, permutations, product

letters = ["x", "y"]
# combinations(letters, 2): ('x', 'y')
# permutations(letters, 2): ('x', 'y'), ('y', 'x')
# product(letters, repeat=2): ('x', 'x'), ('x', 'y'), ('y', 'x'), ('y', 'y')
```

후보 수가 $M$이고 각 후보의 $r$개 원소를 모두 읽는다면 그 작업만으로 $\Omega(Mr)$가 필요하다. 이는 출력해야 하는 원소 수에서 얻는 하한이다. 결과를 `list(...)`로 모두 모으면 그만큼 저장 공간도 필요하므로, 한 후보씩 처리할 수 있다면 iterator를 직접 순회한다. 다만 조합 생성 함수는 입력 원소를 내부에 보관할 수 있어 “결과 지연 생성”을 “추가 공간이 전혀 없음”으로 해석하지 않는다.[24,41]

### (2) 수학 함수의 입력 영역

`math`의 함수들은 필요한 수학 연산을 드러내지만, 정수 계산과 근사 실수 계산을 섞지 않도록 반환형을 확인해야 한다. 다음 표는 정수·실수 경계 판단에 쓰는 기본 범위이다. 조합 수와 최소공배수의 수론적 성질은 이 문서의 범위에서 제외한다. 함수 하나를 호출한다는 이유로 큰 정수에 대한 계산 비용까지 상수 시간이라고 가정하지 않는다.[4,17,18,42,43]

| 호출 형태 | 반환값·목적 | 입력 조건 |
| --- | --- | --- |
| `math.gcd(a, b)` | 최대공약수인 정수 | 여기서는 양의 정수 두 개 |
| `math.isqrt(n)` | $\lfloor\sqrt n\rfloor$인 정수 | 음이 아닌 정수 |
| `pow(a, b, m)` | $a^b\bmod m$인 정수 | 여기서는 정수 $a$, $b\geq0$, $m>0$ |
| `math.factorial(n)` | 정수 $n!$ | 음이 아닌 정수, $0!=1$ |
| `math.sqrt(x)` | 제곱근의 `float` | 실수 범위에서는 $x\geq0$ |
| `math.floor(x)` | 아래쪽 정수 | 유한 실수의 바닥값 |
| `math.ceil(x)` | 위쪽 정수 | 유한 실수의 천장값 |
| `math.fsum(items)` | 실수 합의 `float` | 중간 반올림 오차를 줄이는 합산 |
| `math.isfinite(x)` | 유한 여부의 `bool` | 무한대와 not a number (NaN)이면 거짓 |

`math.factorial`과 `math.gcd`는 정수값을 구하는 데 사용하며, `math.sqrt`의 결과를 다시 정수로 바꾼다고 정확한 정수 경계 계산이 되는 것은 아니다. 큰 정수의 제곱 여부는 `r = math.isqrt(n)`으로 정수 경계를 구한 뒤 `r * r == n`인지 판단할 수 있다. 이는 정수 제곱근의 정의에서 바로 얻는 적용이다. 또 `fsum`은 입력에 이미 들어간 표현 오차를 원래의 정확한 실수값으로 복원하는 함수가 아니다.[16–18,42]

## 9. 대표 문제: 사건 집계와 순위

### (1) 문제와 입력 조건

관측 기록에는 `event_id name score`가 들어 있다. 같은 `event_id`가 여러 번 들어오면 첫 번째 기록만 유효하다. 유효 기록의 점수를 이름별로 모두 합산한 뒤, 다음 기준으로 상위 $K$개 이름을 출력한다.

1. 합계가 큰 이름이 먼저이다.
2. 합계가 같으면 유효 기록 수가 많은 이름이 먼저이다.
3. 두 값이 모두 같으면 이름의 사전식 오름차순이다.

첫 줄은 기록 수 $N$과 출력 상한 $K$이다. 이후 정확히 $N$줄이 주어지며 각 줄은 세 필드이다. 제약은 $0\leq N\leq200\,000$, $0\leq K\leq N$, $|\mathrm{score}|\leq10^6$이다. `event_id`는 양의 정수이며 $10^9$ 이하이다. 이름은 길이 1 이상 20 이하의 영문 소문자 문자열이다. 모든 정수 필드는 숫자 `0`–`9`를 사용한 십진 표기이며, 0은 `0`으로만 쓰고 나머지 값에는 선행 0을 붙이지 않는다. 음수에만 앞에 `-`를 붙이며, `+`나 밑줄은 사용하지 않는다. 중복 식별자의 뒤 기록은 이름이나 점수가 달라도 무시한다. 유효 이름 수가 $K$보다 작으면 존재하는 이름을 모두 출력한다.

출력은 `name total count` 형식이다. $K=0$이거나 유효 이름이 없으면 출력할 줄이 없다. 합계가 0 또는 음수여도 유효 기록이 존재하면 순위 대상이다. 이 문제의 입력 조건과 아래 예시는 이 문서에서 정의한 것이며, 외부 자료의 실험 결과가 아니다.

예시 입력은 다음과 같다.

```text
8 3
101 amber 5
102 blue 7
101 cyan 100
103 amber -2
104 cyan 3
105 blue -4
106 amber 0
107 dune 3
```

수작업으로 도출한 출력은 다음과 같다.

```text
amber 3 3
blue 3 2
cyan 3 1
```

### (2) 정답 코드

중복 확인에는 집합을, 이름별 합계·개수에는 사전을, 최종 순위에는 복합 키 정렬을 사용한다. 이미 읽은 레코드는 다시 사용할 필요가 없으므로 한 줄씩 처리한다. 사용한 연산의 의미는 앞 절의 집합·집계·정렬 정의를 따른다.[19,22,28,29,34]

```python
import sys
from collections import defaultdict


def solve():
    stream = sys.stdin
    n, k = map(int, stream.readline().split())
    seen = set()
    totals = defaultdict(int)
    counts = defaultdict(int)

    for _ in range(n):
        event_text, name, score_text = stream.readline().split()
        event_id = int(event_text)
        if event_id in seen:
            continue
        seen.add(event_id)
        totals[name] += int(score_text)
        counts[name] += 1

    names = sorted(
        totals,
        key=lambda name: (-totals[name], -counts[name], name),
    )
    lines = [
        f"{name} {totals[name]} {counts[name]}"
        for name in names[:k]
    ]
    if lines:
        sys.stdout.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    solve()
```

코드는 입력 명세를 만족하는 자료를 전제로 한다. 중복 여부를 판단하는 데에는 `event_id`만 사용한다. 중복인 줄의 점수를 합계에 넣기 전에 건너뛰므로, 나중에 같은 식별자로 들어온 다른 이름도 집계에 영향을 주지 않는다. `totals`의 키가 바로 유효 이름 집합이므로 별도의 이름 목록을 만들 필요가 없다.

### (3) 수작업 추적과 불변식

다음 표는 각 입력 줄에서 유효성 판단과 그에 따른 해당 이름의 상태를 추적한 것이다. `(합계, 개수)` 순서를 사용한다.

| 줄 | 식별자 | 판단 | 변경 뒤 해당 이름 |
| --- | --- | --- | --- |
| 1 | 101 | 첫 기록 | amber: `(5, 1)` |
| 2 | 102 | 첫 기록 | blue: `(7, 1)` |
| 3 | 101 | 중복, 무시 | cyan은 아직 없음 |
| 4 | 103 | 첫 기록 | amber: `(3, 2)` |
| 5 | 104 | 첫 기록 | cyan: `(3, 1)` |
| 6 | 105 | 첫 기록 | blue: `(3, 2)` |
| 7 | 106 | 첫 기록 | amber: `(3, 3)` |
| 8 | 107 | 첫 기록 | dune: `(3, 1)` |

집계 반복문의 불변식은 다음과 같다. 처음 $j$줄을 처리한 뒤 `seen`에는 그 접두 구간의 모든 사건 식별자가 들어 있으며, `totals[name]`과 `counts[name]`은 그 구간에서 각 식별자의 첫 기록만 사용한 이름별 합계와 개수이다.

$j=0$에서는 세 컨테이너가 비어 있으므로 성립한다. 다음 줄의 식별자가 `seen`에 있으면 이미 첫 기록을 처리했으므로 아무 값도 바꾸지 않아야 한다. 없으면 이번 줄이 첫 기록이므로 식별자를 추가하고 해당 이름의 합계와 개수를 한 번 갱신한다. 따라서 어느 분기에서도 불변식이 유지되고, $j=N$에서 원하는 집계가 완성된다.

최종 키는 amber가 `(-3, -3, 'amber')`, blue가 `(-3, -2, 'blue')`, cyan이 `(-3, -1, 'cyan')`, dune이 `(-3, -1, 'dune')`이다. 앞에서부터 작은 tuple을 택하면 문제의 세 우선순위와 일치한다. 네 이름의 합계가 모두 3이어도 출력 순서가 결정되며, 상위 세 이름만 출력하면 제시한 결과를 얻는다. 이 정당화는 tuple 비교 규칙과 집계 불변식의 결합이다.[28,34]

### (4) 복잡도와 경계 조건

유효 사건 수를 $D$, 유효 이름 수를 $U$, 전체 입력 문자 수를 $L$이라고 하자. 이름 길이와 정수 범위가 제약으로 제한되어 있고 해시 연산이 평균 상수 비용이라는 모형에서는 집계가 $O(N)$, 최종 정렬이 $O(U\log U)$이다. 파싱 비용을 명시하면 전체 평균 시간 상한은 다음과 같다. $U=0$에서도 식이 정의되도록 $\log(U+1)$을 쓴다.[2,3,22,34]

$$
T=O\!\left(L+N+U\log(U+1)\right).
$$

집합에 $D$개 식별자, 두 사전에 $U$개 이름, 정렬 결과에 $U$개 참조가 저장된다. 출력 문자열의 총 길이를 $B$, 최대 입력 줄의 문자 수를 $R$이라고 하면 공간은 $O(1+D+U+B+R)$이다. `readline().split()`이 현재 줄과 그 필드들을 보관하므로 $R$을 포함한다. 수치의 값 범위가 제한되어 있어도 구분 공백의 길이까지 제한되는 것은 아니다. 출력 줄들을 모으는 부분을 제거하면 출력 버퍼를 줄일 수 있지만, 이 코드는 최대 20자 이름과 제한된 정수 범위에서 출력의 형식을 한곳에서 만들기 위해 목록을 사용한다. 해시가 최악으로 충돌하는 경우에는 이 평균 시간 상한을 적용하지 않는다.[3,11,12]

| 경계 입력 | 코드에서의 처리 | 확인할 의미 |
| --- | --- | --- |
| `N=0, K=0` | 반복·정렬 결과가 비고 출력 없음 | 빈 입력 집계 |
| `K=0` | `names[:0]`이 비어 출력 없음 | 합계와 무관한 출력 상한 |
| 모든 식별자가 동일 | 첫 줄만 반영 | 중복 단위는 이름이 아니라 사건 |
| 같은 이름에 여러 식별자 | 각각 합산 | 이름 중복을 제거하면 안 됨 |
| 합계가 0 또는 음수 | 키로 남아 순위 대상 | 0을 “없음”으로 해석하지 않음 |
| 합계·개수 모두 동점 | 이름으로 결정 | 입력 순서와 독립적인 순위 |
| `K > U` | 존재하는 이름만 선택 | 없는 순위를 만들지 않음 |

이 표는 코드를 실행한 시험 결과가 아니라 각 분기의 의미와 슬라이스·정렬 규칙을 대입한 정적 검토이다. 예를 들어 점수가 모두 음수일 때에도 부호를 뒤집은 키는 원래 합계가 큰 이름을 먼저 놓는다. 사건 수가 많아져도 매 줄에서 전체 기록을 다시 검색하지 않는 이유는 이미 본 식별자를 집합으로 따로 유지하기 때문이다.

## 10. 적용 한계와 요약

자료구조의 비용표를 적용하기 전에 원소 수, 키 길이, 정수 크기, 복사 범위, 정렬 기준을 확인한다. 특히 “함수 한 번”과 “상수 시간”을 동일하게 보지 않는다. `sorted`, `sum`, 슬라이스, 전체 입력 읽기에는 내부 순회나 저장이 있고, iterator도 끝까지 소비하면 그 원소 수만큼의 작업이 필요하다.[2,4,11,24]

- 위치 접근에는 `list`, 이름별 조회에는 `dict`, 중복 확인에는 `set`이 자연스럽다.
- 변경 메서드의 반환값, 별칭, 얕은 복사를 구분해야 상태가 의도한 범위에서만 바뀐다.
- 최소·최대·합만 필요하면 축약 함수를, 전체 순서가 필요하면 명시적인 `key` 정렬을 사용한다.
- 스택·큐·힙은 다음 원소의 선택 규칙이 다르며, `bisect`는 정렬된 원소열의 경계를 찾는다.
- 평균 비용과 분할상환 비용을 구별하고, 입력 제한과 불변식으로 라이브러리 조합의 의미를 확인한다.

## 11. 참고문헌

1. Brad Miller and David Ranum, *Problem Solving with Algorithms and Data Structures using Python*, 3rd ed., [“Big O Notation”](https://runestone.academy/ns/books/published/pythonds3/AlgorithmAnalysis/BigONotation.html).
2. Brad Miller and David Ranum, *Problem Solving with Algorithms and Data Structures using Python*, 3rd ed., [“Lists”](https://runestone.academy/ns/books/published/pythonds3/AlgorithmAnalysis/Lists.html).
3. Brad Miller and David Ranum, *Problem Solving with Algorithms and Data Structures using Python*, 3rd ed., [“Dictionaries”](https://runestone.academy/ns/books/published/pythonds3/AlgorithmAnalysis/Dictionaries.html).
4. Python Software Foundation, [“Built-in Functions,” Python 3.10 documentation](https://docs.python.org/3.10/library/functions.html).
5. Charles E. Leiserson and Erik D. Demaine, [“Lecture 13: Amortized Analysis,” MIT 6.046J/18.401J](https://ocw.mit.edu/courses/6-046j-introduction-to-algorithms-sma-5503-fall-2005/0a02bc84e917b9aeddaf69c8dc151a6f_lec13.pdf), slides 14–18 (2005).
6. Python Software Foundation, [“Built-in Types,” Python 3.10 documentation](https://docs.python.org/3.10/library/stdtypes.html).
7. David Beazley, *Practical Python Programming*, [“Numbers”](https://dabeaz-course.github.io/practical-python/Notes/01_Introduction/03_Numbers.html).
8. David Kauchak, [*Amortized Analysis and Heaps Intro*, CS302](https://cs.pomona.edu/~dkauchak/classes/s13/cs302-s13/lectures/lecture7-amortized-heaps.pdf), Pomona College (2013), handout pp. 1, 4–5.
9. Nick Parlante, [“Python Lists,” Stanford Python Guide](https://cs.stanford.edu/people/nick/py/python-list.html).
10. Michael T. Goodrich, Roberto Tamassia, and Michael H. Goldwasser, [*Data Structures and Algorithms in Python*](https://nibmehub.com/opac-service/pdf/read/Data%20Structures%20and%20Algorithms%20in%20Python.pdf) (2013), §10.2.2–10.2.3, pp. 419–421, Table 10.2.
11. Python Software Foundation, [“Input and Output,” Python 3.10 Tutorial](https://docs.python.org/3.10/tutorial/inputoutput.html).
12. Mike Driscoll, *Python 101*, [“Chapter 8 — Working with Files”](https://python101.pythonlibrary.org/chapter8_file_io.html).
13. Swaroop C H, *A Byte of Python*, [“Exceptions”](https://cs.du.edu/~intropython/byte-of-python/exceptions.html), University of Denver edition.
14. Mike Driscoll, *Python 101*, [“Chapter 2 — All About Strings”](https://python101.pythonlibrary.org/chapter2_strings.html).
15. Nick Parlante, [“Python Strings,” Stanford Python Guide](https://cs.stanford.edu/people/nick/py/python-string.html).
16. Python Software Foundation, [“Floating Point Arithmetic: Issues and Limitations,” Python 3.10 Tutorial](https://docs.python.org/3.10/tutorial/floatingpoint.html).
17. Doug Hellmann, [“math — Mathematical Functions,” PyMOTW-3](https://pymotw.com/3/math/index.html).
18. Python Software Foundation, [“math — Mathematical functions,” Python 3.10 documentation](https://docs.python.org/3.10/library/math.html).
19. Python Software Foundation, [“Data Structures,” Python 3.10 Tutorial](https://docs.python.org/3.10/tutorial/datastructures.html).
20. Python Software Foundation, [“copy — Shallow and deep copy operations,” Python 3.10 documentation](https://docs.python.org/3.10/library/copy.html).
21. Doug Hellmann, [“copy — Duplicate Objects,” PyMOTW-3](https://pymotw.com/3/copy/index.html).
22. Nick Parlante, [“Python Dict,” Stanford Python Guide](https://cs.stanford.edu/people/nick/py/python-dict.html).
23. Duke University Course Staff, *Programming for Financial Technology*, [“Sets”](https://fintechpython.pages.oit.duke.edu/jupyternotebooks/1-Core%20Python/15-Sets.html).
24. Doug Hellmann, [“itertools — Iterator Functions,” PyMOTW-3](https://pymotw.com/3/itertools/index.html).
25. David Beazley, *Practical Python Programming*, [“Sequences”](https://dabeaz-course.github.io/practical-python/Notes/02_Working_with_data/04_Sequences.html).
26. David Beazley, *Practical Python Programming*, [“Iteration Protocol”](https://dabeaz-course.github.io/practical-python/Notes/06_Generators/01_Iteration_protocol.html).
27. David Liu, *Introduction to Computer Science*, [“Predicate Logic”](https://www.cs.toronto.edu/~david/course-notes/csc110-111/03-logic/02-predicate-logic.html).
28. Nick Parlante, [“Python Sorting,” Stanford Python Guide](https://cs.stanford.edu/people/nick/py/python-sort.html).
29. Python Software Foundation, [“collections — Container datatypes,” Python 3.10 documentation](https://docs.python.org/3.10/library/collections.html).
30. Doug Hellmann, [“Counter — Count Hashable Objects,” PyMOTW-3](https://pymotw.com/3/collections/counter.html).
31. Doug Hellmann, [“defaultdict — Missing Keys Return a Default Value,” PyMOTW-3](https://pymotw.com/3/collections/defaultdict.html).
32. David Beazley, *Practical Python Programming*, [“Collections”](https://dabeaz-course.github.io/practical-python/Notes/02_Working_with_data/05_Collections.html).
33. Doug Hellmann, [“deque — Double-Ended Queue,” PyMOTW-3](https://pymotw.com/3/collections/deque.html).
34. Andrew Dalke and Raymond Hettinger, [“Sorting HOW TO,” Python 3.10 documentation](https://docs.python.org/3.10/howto/sorting.html).
35. Python Software Foundation, [“bisect — Array bisection algorithm,” Python 3.10 documentation](https://docs.python.org/3.10/library/bisect.html).
36. Doug Hellmann, [“bisect — Maintain Lists in Sorted Order,” PyMOTW-3](https://pymotw.com/3/bisect/index.html).
37. Loyola University Chicago Computer Science Department, edited by George K. Thiruvathukal, [“Searching,” *Introduction to Computer Science in Python: Principles and Practice*](https://introcs-python.cs.luc.edu/lists/searching.html), “Binary Search” and “Performance Comparison” (2026).
38. Python Software Foundation, [“heapq — Heap queue algorithm,” Python 3.10 documentation](https://docs.python.org/3.10/library/heapq.html).
39. Doug Hellmann, [“heapq — Heap Sort Algorithm,” PyMOTW-3](https://pymotw.com/3/heapq/index.html).
40. Brad Miller and David Ranum, *Problem Solving with Algorithms and Data Structures using Python*, 3rd ed., [“Binary Heap Implementation”](https://runestone.academy/ns/books/published/pythonds3/Trees/BinaryHeapImplementation.html).
41. Python Software Foundation, [“itertools — Functions creating iterators for efficient looping,” Python 3.10 documentation](https://docs.python.org/3.10/library/itertools.html).
42. Mark A. Austin, [*Python Tutorial – Part I: Introduction*, ENCE 688R](https://terpconnect.umd.edu/~austin/ence688r.d/lecture-material2023/python-introduction.pdf), University of Maryland (2023), mathematical functions table.
43. Indiana State University Computer Science, [“RSA,” Fermat prime test / modular exponentation](https://cs.indstate.edu/web/index.php?redirect=no&title=RSA).
