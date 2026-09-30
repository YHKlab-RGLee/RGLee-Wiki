---
description: Python 문자열의 비교 규약에서 빈도·괄호·접두사 처리와 Knuth–Morris–Pratt·rolling hash의 정확성 및 비용까지 설명한다.
---

# String algorithms

문자열 알고리즘은 문자 사이의 순서와 반복을 이용해 필요한 정보를 찾는 방법이다. 같은 문자열이라도 문자별 개수만 필요하면 빈도표를, 중첩 순서를 보존해야 하면 stack을, 공통 접두사를 재사용해야 하면 trie나 패턴의 접두사 정보를 사용한다. 이 문서는 Python 3의 `str`를 기준으로 이 선택을 설명한다. 정규표현식 문법이나 자연어의 단어 경계 판정은 다루지 않는다.

## 1. 문자열 표현과 비교 단위

### (1) 인덱스와 구간

Python의 `str`는 Unicode code point의 불변 시퀀스이며, 인덱스와 `len`도 이 원소를 기준으로 한다.[1,2] 여기서 불변이란 기존 문자열의 특정 위치를 대입으로 고칠 수 없다는 뜻이다. 인덱스는 0부터 시작하며, `s[l:r]`은 왼쪽 끝을 포함하고 오른쪽 끝을 제외한다. 따라서 문자열을 다루기 전에 길이가 무엇을 세고 구간의 끝이 어디에 있는지 확정해야 한다.[1,3]

| 기호 | 의미 | 이 문서의 규약 |
| --- | --- | --- |
| $T,n$ | 본문 문자열과 길이 | $n=\operatorname{len}(T)$ |
| $P,m$ | 찾을 패턴과 길이 | 별도 계약이 없으면 $m>0$ |
| $[l,r)$ | 부분 문자열의 구간 | $0\le l\le r\le n$ |
| $j$ | 현재 일치한 패턴 접두사의 길이 | 다음 비교 위치는 `P[j]` |
| $z$ | 보고할 일치 위치의 수 | 결과 저장 비용에 포함 |

유효한 구간에서 부분 문자열의 길이는 다음과 같다. 끝 인덱스 $r$은 문자의 위치가 아니라 구간 밖 첫 경계이므로 $r=n$도 허용한다.[1,3]

$$
\left|T[l:r]\right|=r-l.
$$

예를 들어 `T = "cabca"`의 `T[1:4]`는 `"abc"`이며, 마지막 `a`의 인덱스는 4이다. 길이 3인 부분 문자열이 인덱스 2에서 시작하면 끝 경계는 5이다. 아래 값은 이 규약을 직접 적용한 수동 계산이다.

```python
text = "cabca"
segment = text[1:4]    # "abc"
last = text[4]         # "a"
empty = text[3:3]      # ""
```

이후의 알고리즘은 문자열 한 원소의 비교와 접근, 실용적인 크기의 인덱스 계산을 상수 비용으로 세는 모형을 사용한다. 다만 문자열 전체 비교와 새 부분 문자열 구성은 그 길이를 따로 계산한다. 입력 자체를 저장하는 공간과 알고리즘이 추가로 쓰는 공간도 구분한다.

### (2) Unicode 정규화와 대소문자

Code point의 수가 화면에 보이는 글자의 수와 항상 같지는 않다. 조합 가능한 문자는 단일 code point와 기본 문자·결합 부호의 시퀀스로 표현될 수 있다. 예컨대 `"é"`와 `"e\u0301"`은 같은 형태로 표시될 수 있어도 원래 시퀀스의 길이는 각각 1과 2이다. 두 표현을 같게 볼 것인지는 알고리즘의 입력 계약에 포함해야 한다.[4,5]

| 비교 정책 | 처리 | 보존하거나 합치는 차이 |
| --- | --- | --- |
| 원문 일치 | 변환 없이 비교 | Code point 차이를 보존 |
| Canonical 일치 | 같은 Unicode 정규형으로 변환 | 정준적으로 동등한 표현을 합침 |
| Canonical caseless 일치 | 정준 분해·case folding·재분해 | 정준적 차이와 대소문자 차이를 합침 |

정규형을 택할 때 Normalization Form C (NFC)는 정준 분해 후 가능한 합성을 수행하며, Normalization Form D (NFD)는 정준 분해를 사용한다.[5,6] 호환성 정규화는 정준적 차이 외에 호환 문자 사이의 차이까지 제거한다.[5,6] 따라서 검색에서 보존할 차이를 먼저 정한 뒤 정규형을 선택해야 한다. 대소문자 무시에는 `casefold()`가 쓰이며 `"ß"`가 `"ss"`로 바뀌는 것처럼 길이도 달라질 수 있다. 정준 동등성까지 포함한 비교는 다음 키를 사용한다.[4,7]

```python
import unicodedata


def canonical_caseless_key(text):
    decomposed = unicodedata.normalize("NFD", text)
    folded = decomposed.casefold()
    return unicodedata.normalize("NFD", folded)
```

이 함수는 두 문자열의 비교 키를 만드는 코드이다. 모든 예제에 자동으로 적용하는 전처리는 아니다. `"A"`와 `"a"`를 서로 다른 기호로 취급하는 데이터에는 원문을 사용한다. 공백이나 문장부호를 제거할지도 별도로 결정한다. Case folding과 공백 제거는 서로 다른 규칙이며, 하나를 요청했다고 다른 하나까지 허용되는 것은 아니다.

길이가 달라질 수 있다는 사실에서 검색 위치의 해석도 달라진다. 예를 들어 원문 `"ßa"`를 case folding하면 `"ssa"`가 되므로 `a`의 위치가 1에서 2로 이동한다. 따라서 변환한 문자열에서 얻은 위치를 원문의 인덱스로 바로 반환할 수 없다. 원문 위치가 필요한 경우에는 변환 단위와 위치 대응을 별도로 설계해야 한다. 이 문서의 패턴 검색 함수는 변환하지 않은 입력의 인덱스를 반환한다.[4,7]

## 2. 기본 연산과 구성 비용

### (1) 분리·정리·결합

기본 메서드는 짧은 처리를 명확하게 표현한다. `split`의 구분자, `find`의 검색 대상, `replace`의 치환 대상은 여기서 모두 리터럴 문자열이다. 예를 들어 `"."`을 넘기면 마침표 자체를 뜻한다. 정규표현식의 임의 문자 기호로 해석하지 않는다.[1,8]

| 연산 | 역할 | 수동 계산 예 |
| --- | --- | --- |
| `s.split()` | 연속 공백을 구분자로 분리 | `" a  b ".split()` → `["a", "b"]` |
| `s.split(",")` | 지정 구분자로 분리 | `"a,,b".split(",")` → `["a", "", "b"]` |
| `s.strip()` | 양 끝의 공백 제거 | `" a b ".strip()` → `"a b"` |
| `"/".join(parts)` | 문자열 조각 사이에 구분자 삽입 | `["a", "b"]` → `"a/b"` |
| `s.replace("-", "/")` | 지정 부분 문자열 치환 | `"a-b-c"` → `"a/b/c"` |

특히 인자 없는 `split()`과 구분자로 공백 하나를 지정한 `split(" ")`은 다르다. 전자는 연속 공백을 묶고, 후자는 연속 구분자 사이의 빈 필드도 남긴다. 빈 필드가 누락값을 뜻하는 형식에서 이를 지우면 데이터의 열 위치가 달라진다. `strip()` 역시 내부 공백을 지우는 연산은 아니다.[1,8,9]

다음은 구분자 `;`를 사용하고 각 필드 양 끝의 공백만 무시하기로 정한 입력 계약을 구현한 예이다. 빈 필드는 유지한다. 결과는 문서상 수동 계산이며, 따옴표 안의 구분자나 escape 문법을 처리하는 parser는 아니다.

```python
record = " red ; ; blue "
fields = [part.strip() for part in record.split(";")]
canonical_record = ";".join(fields)
# fields: ["red", "", "blue"]
# canonical_record: "red;;blue"
```

| 전처리 선택 | 남는 정보 | 잃을 수 있는 정보 |
| --- | --- | --- |
| 필드별 `strip()` | 내부 공백, 빈 필드 | 양 끝 공백의 수 |
| `split()` 후 공백으로 `join` | 공백으로 나눈 토큰 순서 | 원래 공백 종류와 수 |
| 리터럴 `replace` | 치환되지 않은 부분 | 치환 대상의 원래 표기 |

`join`을 `split`의 역연산으로 외우는 것보다, 어떤 구분자와 빈 필드를 보존했는지 확인하는 편이 정확하다. 위 예에서 양 끝 공백을 제거했으므로 `canonical_record`만으로 원래 `record`를 복원할 수 없다. 이는 표준 메서드 의미를 조합한 결과이며, 문자열 정리가 정보 보존 연산인지 먼저 따져야 하는 이유이다.[1,8,9]

### (2) 검색·계수와 겹침

`find`는 첫 일치의 시작 인덱스를 반환하고 찾지 못하면 `-1`을 반환한다. `count`는 서로 겹치지 않는 출현을 센다. 따라서 첫 위치, 존재 여부, 겹치지 않는 개수, 겹침을 포함한 모든 위치는 구분해서 선택해야 한다.[1,8,10]

```python
text = "aaaaa"
first = text.find("aaa")     # 0
missing = text.find("b")     # -1
nonoverlap = text.count("aaa")  # 1
# "aaa"의 모든 시작 위치를 직접 열거하면 [0, 1, 2]이다.
```

`if text.find(pattern):`처럼 결과를 곧바로 조건식으로 사용하면 첫 위치 0과 실패값 -1을 잘못 구분한다. 원하는 조건을 `text.find(pattern) != -1`로 표현해야 한다. 위 예에서는 길이 3인 구간 `[0,3)`, `[1,4)`, `[2,5)`가 모두 일치하지만 서로 겹치므로 `count`의 답은 1이다.[1,3,10]

| 요구 결과 | 간단한 선택 | 주의할 계약 |
| --- | --- | --- |
| 첫 위치 | `find` | 실패값 `-1` 처리 |
| 겹치지 않는 개수 | `count` | 겹친 시작점은 제외 |
| 모든 시작점 | 직접 탐색 또는 Knuth–Morris–Pratt (KMP) | 빈 패턴·겹침 규칙 명시 |
| 문자별 개수 | 한 번 순회하며 빈도 누적 | 부분 문자열 계수와 구별 |

### (3) 불변 문자열의 누적 구성

Python 공식 문서와 PyPy 문서는 불변 문자열을 반복해서 연결할 때 이차 비용이 생길 수 있음을 설명하고, 조각을 모아 `join`으로 결합하는 방식을 제시한다.[1,11] 이 비용의 원인을 보기 위해 이전 접두사 전체를 매번 복사하는 모형을 두자. 길이 1인 조각을 $k$번 붙이고 매번 현재 전체 길이만큼 복사한다면, $r$번째 단계의 복사량은 $r$이다. 따라서 총 복사량 $C$는 다음과 같이 직접 유도된다. 이는 해당 복사 모형에서의 정확한 합이며 모든 구현의 최적화 동작을 단정하는 식은 아니다.

$$
C=\sum_{r=1}^{k}r=\frac{k(k+1)}{2}=\Theta(k^2).
$$

누적 접두사를 매번 다시 구성하지 않도록 조각을 모은 뒤 한 번 결합하는 구조를 사용한다.[1,11] 아래 예의 목적은 출력 구성 방식의 설명이다. 빈 항목을 버리는 규칙은 이 예에서만 명시적으로 선택했다.

```python
parts = []
for token in ["red", "", "blue", "green"]:
    if token != "":
        parts.append(token)
result = "|".join(parts)   # "red|blue|green"
```

부분 문자열 검색에서도 같은 주의가 필요하다. 반복문 안에서 `text[i:i+m]`를 만들고 비교하면 반복 한 번의 비용을 무조건 상수로 셀 수 없다. 알고리즘 분석은 반복문의 개수뿐 아니라 그 내부에서 읽거나 복사하는 문자열 길이까지 포함해야 한다. 뒤의 KMP는 본문 부분 문자열을 생성하지 않고 문자 위치로 비교하고, 검증형 rolling hash는 후보에서만 원문을 다시 비교한다.

## 3. 빈도와 anagram

### (1) 다중집합으로의 변환

Anagram은 한 문자열의 문자를 재배열해 다른 문자열을 얻는 관계이다. 여기서는 공백·대소문자를 포함한 모든 code point를 기호로 취급한다. 순서를 버려도 문자별 개수는 보존해야 하므로 집합만으로 판정할 수 없다. `"aab"`와 `"abb"`의 문자 집합은 같지만 anagram은 아니다.[12,13,14]

문자 $c$의 문자열 $s$ 내 빈도를 $f_s(c)$로 쓰면 판정 조건은 다음과 같다. $c$는 비교 대상에 등장하는 모든 기호를 순회한다. 길이가 다르면 이 조건을 만족할 수 없으므로 먼저 길이를 검사할 수 있다.[12,14]

$$
s\sim t\quad\Longleftrightarrow\quad
\forall c,\;f_s(c)=f_t(c).
$$

| 표현 | `aab` | `aba` | `abb` |
| --- | --- | --- | --- |
| 원문 | 순서 보존 | 순서 보존 | 순서 보존 |
| 문자 집합 | `{a,b}` | `{a,b}` | `{a,b}` |
| 빈도 `(a,b)` | `(2,1)` | `(2,1)` | `(1,2)` |

아래 코드는 정해진 알파벳 크기 없이 등장한 문자만 저장한다. 빈도 누적은 문자 하나를 읽을 때 그 문자 카운터만 1만큼 증가시킨다. 이 갱신을 귀납적으로 적용하면 처음 $r$개 문자를 처리한 사전이 정확히 `s[:r]`의 빈도를 담는다는 불변식을 얻는다.[12,13]

```python
def frequencies(text):
    counts = {}
    for ch in text:
        counts[ch] = counts.get(ch, 0) + 1
    return counts


def is_anagram(left, right):
    if len(left) != len(right):
        return False
    return frequencies(left) == frequencies(right)
```

빈도 일치가 충분한 이유도 직접 설명할 수 있다. 각 문자 종류마다 왼쪽의 출현을 오른쪽의 같은 문자 출현에 일대일로 대응시키면 모든 위치를 소모한다. 순서는 이 대응에 영향을 주지 않는다. 반대로 어떤 문자의 수라도 다르면 그 문자를 보충하거나 버리지 않고 재배열만으로 일치시킬 수 없다. 따라서 정렬이나 모든 순열 열거가 필수는 아니다.[12,14]

### (2) 표현별 비용과 전처리

길이가 각각 $n_1,n_2$인 두 문자열에서 서로 다른 문자의 수를 $u$라 하자. 사전 접근의 기대 상수 비용을 가정하면 빈도 구성·비교의 기대 시간은 $O(n_1+n_2)$, 추가 공간은 $O(u)$이다. 이 기대 비용은 hash table 가정에 의존하며 모든 입력에 대한 최악 상수 접근 보장과는 다르다. 알파벳이 작은 고정 집합이면 배열 카운터를 사용할 수 있다.[12,13,15]

| 표현 | 전제 | 선택 이유 |
| --- | --- | --- |
| 고정 크기 배열 | 기호가 알려진 작은 집합 | 인덱스 대응과 공간이 명확 |
| 사전 빈도표 | 등장 기호를 미리 모름 | 실제 등장한 문자만 저장 |
| 정렬 결과 | 문자 순서 비교 가능 | 정렬된 대표 표현도 필요할 때 |

정규화 후 anagram을 정의한다면 `is_anagram(key(a), key(b))`처럼 비교 전에 동일한 키 함수를 적용한다. 변환 전 길이를 비교하면 잘못 거절할 수 있다. 예컨대 case folding 전 `"ß"`와 `"ss"`의 길이는 다르지만 변환 후에는 같아진다. 이때 빈도표는 원문의 문자가 아니라 변환된 code point를 센다.[4,7,12]

Anagram 검색을 연속 부분 문자열로 확장할 때는 길이 $m$의 창 안 빈도와 패턴 빈도를 비교한다. 창을 한 칸 이동할 때 떠나는 문자 하나를 감소시키고 들어오는 문자 하나를 증가시킬 수 있다. 다만 사전 두 개 전체를 매번 비교하는 비용은 서로 다른 기호 수에 따라 커질 수 있다. 창 갱신이 두 번이라고 해서 전체 판정까지 자동으로 상수 시간이 되는 것은 아니다. 이 문서에서는 빈도 판정 원리까지만 사용하고 창 전체 알고리즘은 확장하지 않는다.[12,14]

## 4. Stack을 이용한 중첩 판정

### (1) 미완성 괄호의 불변식

괄호 검사는 문자 빈도만으로 해결할 수 없다. `"([)]"`는 여는 괄호와 닫는 괄호의 종류별 개수가 같지만 중첩이 맞지 않는다. 닫는 괄호는 가장 최근에 열렸고 아직 닫히지 않은 괄호와 대응해야 하므로 last in, first out (LIFO) 순서의 stack이 필요하다.[16,17]

처리한 접두사에 오류가 없을 때 stack은 아직 닫히지 않은 여는 괄호를 오래된 것부터 담는다. 닫는 괄호를 만났는데 stack이 비어 있으면 대응할 여는 괄호가 없고, 맨 위와 종류가 다르면 중첩 순서가 깨진다. 전체를 읽은 뒤 stack이 남아 있어도 닫히지 않은 괄호가 있으므로 실패이다.[16,17]

```python
def balanced_brackets(text):
    closing_to_opening = {')': '(', ']': '[', '}': '{'}
    opening = set(closing_to_opening.values())
    stack = []
    for ch in text:
        if ch in opening:
            stack.append(ch)
        elif ch in closing_to_opening:
            if not stack or stack[-1] != closing_to_opening[ch]:
                return False
            stack.pop()
        else:
            return False  # 이 함수는 괄호 여섯 종류만 허용한다.
    return not stack
```

아래 표는 `"([]){}"`를 직접 읽으며 얻은 상태이다. Stack 열은 아래쪽에서 위쪽 순서이다. 닫는 괄호는 자신의 짝만 제거하므로 정상 접두사에서의 불변식이 유지된다.

| 읽은 문자 | 동작 | 처리 후 stack |
| --- | --- | --- |
| `(` | 삽입 | `(` |
| `[` | 삽입 | `([` |
| `]` | `[` 제거 | `(` |
| `)` | `(` 제거 | 비어 있음 |
| `{` | 삽입 | `{` |
| `}` | `{` 제거 | 비어 있음 |

### (2) 비용과 parser의 경계

각 문자는 한 번 읽고, 여는 괄호는 최대 한 번 삽입·제거한다. Python list 끝의 삽입·제거를 분할상환 상수 비용으로 세면 전체 시간은 $O(n)$이다. 최대 중첩 깊이를 $d$라 하면 stack 공간은 $O(d)$이고, 여는 괄호만 계속 나오는 입력에서는 $d=n$이다.[15,16,17]

| 입력 | 수동 판정 | 실패 또는 성공 이유 |
| --- | --- | --- |
| `""` | `True` | 미완성 괄호가 없음 |
| `")("` | `False` | 첫 문자부터 대응 괄호가 없음 |
| `"([)]"` | `False` | `)` 앞 stack의 맨 위가 `[` |
| `"(("` | `False` | 끝난 뒤 stack이 남음 |
| `"(a)"` | `False` | 이 함수의 입력 알파벳 밖 문자 |

일반 문자를 무시하려면 마지막 `else`의 정책을 바꾸어야 한다. 그러나 그것만으로 프로그래밍 언어 parser가 되지는 않는다. 문자열 리터럴 안의 괄호를 제외하려면 따옴표와 escape 상태를 먼저 판정하는 규칙이 추가로 필요하다. 여기서 증명한 것은 여섯 괄호 기호로 이루어진 입력의 균형 판정이며, 언어 전체의 문법 유효성은 아니다.

## 5. Trie와 접두사 질의

### (1) 경로와 단어 끝

Trie는 루트에서 내려가는 간선의 문자 시퀀스로 문자열을 표현한다. 같은 접두사를 가진 단어는 그 경로를 공유한다. 경로가 있다는 것과 그 위치에서 단어가 끝난다는 것은 다르므로 종료 표시가 필요하다. 예를 들어 `"car"`, `"cart"`, `"cat"`을 저장하면 `"ca"`는 경로이지만 저장된 완전한 단어는 아니다.[18,19]

| 루트부터의 접두사 | 다음 문자 | 단어 종료 표시 |
| --- | --- | --- |
| `""` | `c` | 거짓 |
| `c` | `a` | 거짓 |
| `ca` | `r`, `t` | 거짓 |
| `car` | `t` | 참 |
| `cart` | 없음 | 참 |
| `cat` | 없음 | 참 |

아래 구현은 노드 번호를 정수로 두고, 각 노드의 사전에 `문자 → 자식 번호`를 저장한다. 문자 키와 종료 표시를 같은 사전에 섞지 않아 특정 문자를 종료 기호로 예약할 필요가 없다. 반복 삽입은 집합처럼 취급하며, 빈 문자열을 삽입하면 루트의 종료 표시를 켠다. 이는 표준 trie의 경로·종료 원리를 Python으로 구성한 예이다.[18,19]

```python
class Trie:
    def __init__(self):
        self.children = [{}]
        self.terminal = [False]

    def insert(self, word):
        node = 0
        for ch in word:
            nxt = self.children[node].get(ch)
            if nxt is None:
                nxt = len(self.children)
                self.children[node][ch] = nxt
                self.children.append({})
                self.terminal.append(False)
            node = nxt
        self.terminal[node] = True

    def _walk(self, text):
        node = 0
        for ch in text:
            node = self.children[node].get(ch)
            if node is None:
                return None
        return node

    def contains(self, word):
        node = self._walk(word)
        return node is not None and self.terminal[node]

    def has_prefix(self, prefix):
        node = self._walk(prefix)
        if node is None:
            return False
        return self.terminal[node] or bool(self.children[node])
```

`has_prefix`는 해당 접두사로 시작하는 저장 단어가 하나 이상 있는지를 뜻한다. 비어 있는 trie에서도 빈 경로 자체는 루트에 존재하므로, 단순히 `_walk("")` 성공 여부만 반환하면 이 계약과 어긋난다. 위 코드는 루트에 종료 표시 또는 자식이 있는지를 확인한다. 삭제 연산이 없으므로 루트 이외의 모든 생성 노드는 어떤 저장 단어로 이어진다.

| 질의 | 위 세 단어를 저장한 뒤의 답 | 의미 |
| --- | --- | --- |
| `contains("ca")` | `False` | 접두사일 뿐 완전한 단어는 아님 |
| `has_prefix("ca")` | `True` | 그 아래에 저장 단어가 존재 |
| `contains("car")` | `True` | 더 긴 단어의 접두사이면서 단어 |
| `has_prefix("cab")` | `False` | `b` 간선이 없음 |
| `has_prefix("")` | `True` | 저장 단어가 하나 이상 존재 |

### (2) 질의 비용과 자료구조 선택

길이 $q$의 질의는 최대 $q$번 간선을 따라간다. 문자 사전의 기대 상수 접근을 가정한 위 구현의 기대 시간은 $O(q)$이다. 삽입한 모든 단어 길이의 합을 $L$이라 할 때, 문자 하나를 처리하며 새 노드를 최대 하나 만들기 때문에 노드 수 $V$에는 다음 상계가 있다. 고정 크기 자식 배열의 최악 비용과 사전 기반 구현의 기대 비용을 혼동하지 않아야 한다.[15,18,19]

$$
V\le 1+L.
$$

루트 1개가 더해지며, 공통 접두사와 중복 삽입이 있으면 실제 노드는 더 적다. 위 세 단어의 길이 합은 10이지만 표에 나온 노드는 루트를 포함해 6개이다. 이 구현의 간선 수는 $V-1$이므로 자식 사전에 저장되는 항목 수 역시 선형이다. 다만 Python 객체와 작은 사전마다 관리 비용이 있어 노드 개수만으로 실제 메모리 바이트를 판단할 수는 없다.

| 질의 종류 | 방문 범위 | 추가 고려 사항 |
| --- | --- | --- |
| 완전한 단어 존재 | 한 경로 | 종료 표시 검사 |
| 접두사 존재 | 한 경로 | 저장 단어의 존재 의미 |
| 접두사 아래 모든 단어 | 경로와 하위 노드 | 결과 문자열 구성 비용 |

접두사 존재 확인이 $O(q)$라고 해서 자동완성 후보 전체의 출력도 $O(q)$인 것은 아니다. 후보를 나열하려면 하위 노드를 방문하고 문자열을 출력해야 한다. 반대로 완전한 단어 존재만 필요하면 공통 경로 구조를 직접 관리할 필요가 있는지부터 따져야 한다. Trie의 핵심 이점은 단어 수보다 질의 길이에 따라 경로를 검사하고 접두사 정보를 그대로 재사용하는 데 있다.[18,19]

## 6. Knuth–Morris–Pratt와 접두사 정보

### (1) Border와 prefix function

KMP 알고리즘은 이미 일치한 문자열의 접두사·접미사 관계를 이용해 불필요한 재비교를 건너뛴다. 본문에서 뒤로 돌아가는 대신 패턴에서 유지할 수 있는 일치 길이를 줄인다. 이를 위해 패턴의 각 접두사에 대해 prefix function을 먼저 계산한다.[14,20,21]

문자열의 border는 전체보다 짧으면서 접두사이자 접미사인 문자열이다. 빈 문자열도 길이 0인 border로 허용한다. $\pi[i]$를 `P[:i+1]`의 가장 긴 border 길이로 정의하면 다음과 같다. 집합의 $\ell$은 길이이며 $\ell\le i$이므로 전체 길이 $i+1$은 제외된다.[14,20]

$$
\pi[i]=\max\{\ell\mid 0\le\ell\le i,\;
P[0:\ell]=P[i+1-\ell:i+1]\}.
$$

다음은 `P = "ababaca"`에 대한 정의의 직접 적용이다. `"ababa"`의 가장 긴 border는 `"aba"`이고, 그보다 짧은 border `"a"`도 있지만 표에는 가장 긴 길이만 기록한다.

| $i$ | 현재 접두사 | 가장 긴 border | $\pi[i]$ |
| --- | --- | --- | --- |
| 0 | `a` | 빈 문자열 | 0 |
| 1 | `ab` | 빈 문자열 | 0 |
| 2 | `aba` | `a` | 1 |
| 3 | `abab` | `ab` | 2 |
| 4 | `ababa` | `aba` | 3 |
| 5 | `ababac` | 빈 문자열 | 0 |
| 6 | `ababaca` | `a` | 1 |

일부 문헌은 `prefix[k]`를 길이 $k$인 접두사의 border 길이로 정의한다. 이 문서의 배열과는 `prefix[k] = pi[k-1]`로 대응한다. 다른 구현의 `next` 배열은 `-1` 초기 상태나 추가 최적화를 사용하기도 하므로 숫자만 복사해서 섞으면 안 된다.[20,21]

### (2) 실패 연결과 선형 전처리

`pi[i-1]`을 $j$로 두면 직전 접두사의 끝 $j$글자가 `P[:j]`와 같다. 새 문자 `P[i]`가 `P[j]`와 같으면 길이 $j+1$로 확장한다. 다르면 다음 후보는 $j-1$이 아니라 `pi[j-1]`이다. 새 후보도 기존에 일치한 접두사 `P[:j]`의 border여야 하기 때문이다.[20,21]

$$
j\leftarrow\pi[j-1]\qquad(j>0\text{ 이고 현재 비교가 불일치}).
$$

아래 코드는 이 규약을 그대로 따른다. 빈 패턴에서도 빈 배열을 반환하며, 길이 1이면 처음 넣은 0 하나가 결과이다. `j`는 각 `i`에서 $i$보다 작으므로 `pattern[j]` 접근은 유효하다.[20,21]

```python
def prefix_function(pattern):
    pi = [0] * len(pattern)
    for i in range(1, len(pattern)):
        j = pi[i - 1]
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        pi[i] = j
    return pi
```

`"ababaca"`에서 $i=5$의 문자는 `c`이다. 직전 값 `pi[4]=3`부터 시작하는 과정을 손으로 추적하면 다음과 같다. 세 후보는 모두 같은 새 문자 `c`와 비교한다.

| 후보 길이 $j$ | 다음 패턴 문자 | `c`와 비교 후 동작 |
| --- | --- | --- |
| 3 | `P[3]=b` | 불일치 → `pi[2]=1` |
| 1 | `P[1]=b` | 불일치 → `pi[0]=0` |
| 0 | `P[0]=a` | 불일치 → `pi[5]=0` |

후보를 건너뛰어도 답을 놓치지 않는 이유는 border의 포함 관계에 있다. 이미 일치한 부분의 접미사 중 다음 패턴 접두사가 될 수 있는 것은 그 부분의 border뿐이다. 가장 긴 border에서 다시 가장 긴 proper border를 따라가면 가능한 길이가 큰 것부터 줄어든다. 단순히 길이를 1씩 줄이는 것은 border가 아닌 길이까지 검사하는 방식이다.[20,21]

중첩 `while`이 있다고 전처리가 이차 시간이 되지는 않는다. $j$는 성공한 확장에서 한 번에 1만 증가하며 전체 증가 횟수는 $m$보다 작다. 실패 연결에서는 엄격하게 감소하고 0 아래로 내려가지 않는다. 따라서 전체 감소 횟수도 선형으로 제한되며 전처리 시간은 $O(m)$, 배열 공간은 $O(m)$이다.[14,20]

### (3) 본문 검색과 완전 일치 후 상태

본문 검색에서도 `j`는 처리한 본문 접미사와 같은 패턴 접두사의 길이를 나타낸다. 불일치하면 실패 연결을 따라가며 현재 본문 문자를 다시 비교한다. 본문 인덱스는 감소시키지 않는다. `j=m`이 되면 인덱스 $i$에서 패턴 하나가 끝났으므로 시작점은 $i-m+1$이다.[20,21]

$$
\text{일치 구간}=[i-m+1,\;i+1).
$$

모든 일치를 찾으려면 첫 성공에서 종료하는 구현을 바꾸어야 한다. 성공을 기록한 뒤 `j=pi[m-1]`로 되돌리면 방금 일치한 전체 패턴의 가장 긴 border를 유지한다. 이 상태는 그 끝부분을 다음 일치의 시작부분으로 재사용하므로 겹침을 보존한다. 이는 border의 최소 이동 원리에서 유도한 확장이다.[14,20]

| 성공 후 선택 | 유지하는 정보 | `ababa` 뒤의 상태 |
| --- | --- | --- |
| 함수 종료 | 첫 위치만 필요 | 이후 검색 없음 |
| `j=0` | 겹침 정보 없음 | `aba` 접미사를 버림 |
| `j=pi[m-1]` | 가능한 가장 긴 겹침 | 길이 3인 `aba` 유지 |

성공 후 `j=m`을 그대로 두면 다음 본문 문자에서 `P[m]`을 접근하게 된다. 반대로 `j=0`으로 초기화하고 본문을 계속 읽으면 겹친 일치가 누락될 수 있다. 결과 기록과 상태 복구를 한 묶음으로 두면 두 오류를 피할 수 있다.

## 7. 예제 문제: 겹치는 패턴 위치

### (1) 문제

문자열 `text`와 `pattern`을 받아 패턴이 등장하는 모든 시작 인덱스를 오름차순 리스트로 반환하는 `overlapping_positions`를 작성한다. 두 일치가 같은 문자를 공유해도 모두 포함한다. 이 절의 문제와 입력 예는 접두사 상태를 설명하기 위해 구성한 독자적인 예제이다.

| 조건 | 계약 |
| --- | --- |
| 입력 길이 | $0\le n\le 200\,000$, $0\le m\le 200\,000$ |
| 비교 단위 | Python `str`의 원문 code point |
| 대소문자·공백 | 그대로 구별 |
| 빈 패턴 | 모든 경계 `0,1,...,n` 반환 |
| 미발견 | 빈 리스트 반환 |
| 출력 | 0부터 시작하는 인덱스, 겹침 포함 |

빈 패턴 계약은 이 문제에서 명시적으로 정한 것이다. 일반적인 비어 있지 않은 패턴의 KMP 루프와 분리해서 처리한다. 다음 입력에서 답은 `[0, 2, 4]`이다. 길이 5인 구간 세 개가 각각 `"ababa"`가 되는지 직접 확인할 수 있다.

```python
text = "ababababa"
pattern = "ababa"
# 기대 반환값: [0, 2, 4]
```

### (2) 답

함수 안에 전처리까지 포함해 독립적으로 읽을 수 있게 작성했다. 앞 절의 prefix function과 같은 규약이며, 이 코드는 실행 결과를 보고하는 것이 아니라 해설용 구현이다. 정확성은 아래 불변식과 수동 추적으로 확인한다.[20,21]

```python
def overlapping_positions(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []

    pi = [0] * m
    for i in range(1, m):
        j = pi[i - 1]
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        pi[i] = j

    positions = []
    j = 0
    for i, ch in enumerate(text):
        while j > 0 and ch != pattern[j]:
            j = pi[j - 1]
        if ch == pattern[j]:
            j += 1
        if j == m:
            positions.append(i - m + 1)
            j = pi[m - 1]
    return positions
```

### (3) 해설과 수동 검산

`"ababa"`의 prefix function은 `[0,0,1,2,3]`이다. 첫 성공 후 길이 3의 `"aba"`를 남기므로 다음 두 문자 `"ba"`만 읽어 다음 성공을 얻는다. 다음 표는 입력 전체를 왼쪽에서 오른쪽으로 직접 추적한 것이다.

| 본문 인덱스 $i$ | 문자 | 비교 직후 $j$ | 기록 위치 | 다음 반복의 $j$ |
| --- | --- | --- | --- | --- |
| 0 | `a` | 1 | 없음 | 1 |
| 1 | `b` | 2 | 없음 | 2 |
| 2 | `a` | 3 | 없음 | 3 |
| 3 | `b` | 4 | 없음 | 4 |
| 4 | `a` | 5 | 0 | 3 |
| 5 | `b` | 4 | 없음 | 4 |
| 6 | `a` | 5 | 2 | 3 |
| 7 | `b` | 4 | 없음 | 4 |
| 8 | `a` | 5 | 4 | 3 |

정확성은 세 단계로 나눌 수 있다. 처음에는 읽은 문자가 없고 `j=0`이므로 일치 접두사 조건이 성립한다. 다음 문자가 같으면 접두사를 1만큼 연장하고, 다르면 가능한 border만 차례로 검사하므로 유효한 후보를 놓치지 않는다. `j=m`일 때만 기록하므로 거짓 일치는 없고, 성공 뒤에도 가장 긴 proper border를 남기므로 이전 성공과 겹치는 후보가 이어진다.[14,20,21]

결과는 본문에서 끝 위치가 증가하는 순서로 기록되며, 패턴 길이는 고정이므로 시작 위치도 증가한다. 별도의 결과 정렬이 필요하지 않다. 전처리는 $O(m)$, 검색은 앞 절의 증가·감소 논증으로 $O(n)$, 결과 기록은 $O(z)$이다. 따라서 총 시간은 $O(n+m+z)$, 입력을 제외한 공간은 `pi`와 반환 리스트를 합쳐 $O(m+z)$이다. 개수만 요구한다면 리스트 대신 정수 카운터를 증가시켜 출력 저장 공간을 줄일 수 있다.[14,20]

| 입력 `(text, pattern)` | 수동 기대값 | 확인할 경계 |
| --- | --- | --- |
| `("", "")` | `[0]` | 길이 0의 유일한 경계 |
| `("abc", "")` | `[0,1,2,3]` | 빈 패턴 계약 |
| `("", "a")` | `[]` | 본문이 더 짧음 |
| `("aaaa", "aa")` | `[0,1,2]` | 연속 중첩 |
| `("ab", "ab")` | `[0]` | 전체 길이 일치 |
| `("ab", "ba")` | `[]` | 미발견 |

이 표는 실행한 테스트 목록이 아니라 정의와 코드 흐름으로 계산한 경계 사례이다. 특히 `m>n` 조기 반환은 빈 패턴 처리 다음에 배치해 빈 본문·빈 패턴 계약을 함께 만족시킨다.

## 8. Rolling hash와 충돌 검증

### (1) 다항식 표현과 창 갱신

Rolling hash는 이웃한 길이 $m$의 부분 문자열이 대부분의 문자를 공유한다는 점을 이용해 hash를 갱신한다. Rabin–Karp 검색은 패턴과 창의 hash가 다르면 즉시 제외하고, 같으면 실제 문자를 확인할 수 있다. Hash의 역할은 동일성 증명이 아니라 비교할 후보를 줄이는 것이다.[15,22]

문자 $c$의 정수 코드를 $v(c)$, 밑을 $B$, 양의 나머지 연산의 modulus를 $Q>1$이라 하자. 여기서는 왼쪽 문자에 높은 거듭제곱을 주며, 길이 $m>0$인 창의 hash를 다음과 같이 정의한다. 산술은 정수 modulo $Q$에서 수행한다.[15,22]

$$
H_i=\left(\sum_{k=0}^{m-1}v(T[i+k])B^{m-1-k}\right)\bmod Q.
$$

새 창에서는 맨 왼쪽 항을 제거하고 남은 항에 $B$를 곱한 뒤 새 문자를 더한다. $R=B^{m-1}\bmod Q$를 미리 계산하면 다음 식을 얻는다. 이는 앞 식의 항을 직접 정리한 정확한 항등식이다.[15,22]

$$
H_{i+1}=\bigl((H_i-v(T[i])R)B+v(T[i+m])\bigr)\bmod Q.
$$

예를 들어 `a,b,c`의 코드를 각각 1,2,3으로 두고 $B=10$, $Q=101$, $m=3$을 택한다. 아래 값은 작은 정수로 갱신을 보여 주기 위한 수동 계산이며 실용 hash 매개변수의 권장은 아니다.

| 창 | 원래 다항식 값 | $Q$로 나눈 hash |
| --- | --- | --- |
| `abc` | $1\cdot100+2\cdot10+3=123$ | 22 |
| `bca` | $2\cdot100+3\cdot10+1=231$ | 29 |

$R=100$이므로 `abc`에서 `bca`로 옮길 때 $(22-100)\cdot10+1=-779$이고, 이를 101로 나눈 비음수 나머지는 29이다. 매번 세 항을 다시 더할 필요가 없다는 것이 갱신식의 의미이다.

### (2) 원문 확인을 포함한 구현

다음 함수는 앞 문제와 같은 빈 패턴·겹침 계약을 사용한다. 예시에서는 고정된 $B=257$, $Q=1\,000\,000\,007$과 `ord` 값을 사용한다. 이 선택에 대해 충돌 확률의 수치 보장은 주장하지 않는다. 정확성은 hash가 같은 모든 후보에서 실제 문자를 비교하는 데서 나온다.[15,22]

```python
def verified_hash_positions(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []

    base = 257
    modulus = 1_000_000_007
    leading_power = pow(base, m - 1, modulus)
    target_hash = 0
    window_hash = 0
    for k in range(m):
        target_hash = (target_hash * base + ord(pattern[k])) % modulus
        window_hash = (window_hash * base + ord(text[k])) % modulus

    positions = []
    for start in range(n - m + 1):
        if window_hash == target_hash:
            matches = True
            for k in range(m):
                if text[start + k] != pattern[k]:
                    matches = False
                    break
            if matches:
                positions.append(start)
        if start + m < n:
            window_hash = (
                (window_hash - ord(text[start]) * leading_power) * base
                + ord(text[start + m])
            ) % modulus
    return positions
```

창을 검사한 뒤 다음 창이 있을 때만 갱신한다. 이 순서는 마지막 창을 빠뜨리거나 `text[n]`에 접근하는 오류를 막는다. 문자별 확인을 사용하므로 후보마다 길이 $m$인 slice를 만들지도 않는다. 충돌한 창은 확인 단계에서 탈락하고, 실제 일치는 반드시 같은 hash를 가지므로 걸러지지 않는다.[15,22]

### (3) 충돌과 재검사 비용

서로 다른 문자열도 같은 hash를 가질 수 있다. 작은 예로 코드 $1,2,3$, $B=2$, $Q=5$를 쓰면 길이 2인 `ab`와 `cc`의 hash가 모두 4이다. 원문을 확인하지 않는다면 이 둘을 구분할 수 없다.[15,22]

$$
H(\text{ab})=(1\cdot2+2)\bmod5=4,
\qquad
H(\text{cc})=(3\cdot2+3)\bmod5=4.
$$

Hash 후보 수를 $c$, 실제 답 수를 $z$라 하자. 위 구현은 전처리에 $O(m)$, 창 이동에 $O(n)$, 후보당 최대 $m$회 문자 비교를 사용한다. 따라서 고정 크기 modulus 산술 모형에서 다음 상계를 직접 얻는다. $c$에는 충돌뿐 아니라 실제 일치도 포함된다.[15,22]

$$
\text{시간}=O(n+m+cm+z),\qquad
\text{추가 공간}=O(z+1).
$$

`text`와 `pattern`이 모두 `a`의 반복이면 모든 창이 실제 일치이다. 충돌이 한 번도 없어도 $c=n-m+1$이 되어 원문 검증 비용이 커진다. 따라서 첫 일치에서 끝나는 확률적 검색의 기대 비용을, 모든 겹친 일치를 전부 검증하는 위 함수의 최악 비용으로 옮길 수 없다. KMP는 이런 반복 입력에서도 동일한 선형 시간 논증을 유지한다.[14,15,20,22]

| 방식 | 정확성의 근거 | 남는 비용 또는 한계 |
| --- | --- | --- |
| Hash만 비교 | 동일 hash라는 후보 조건 | 충돌을 참으로 오인할 수 있음 |
| 서로 다른 hash 둘 비교 | 더 많은 후보 필터 | 확률 모형 없이 오류율을 단정할 수 없음 |
| Hash 후 원문 확인 | 문자별 정확한 일치 | 후보가 많으면 재검사 증가 |
| KMP | 접두사 상태와 문자 비교 | 패턴 길이만큼 전처리 공간 |

큰 modulus나 이중 hash는 원문 확인을 생략할 근거와 동일하지 않다. 이 문서의 결정적 정확성이 필요한 함수에서는 끝까지 원문을 확인한다. 매개변수를 고정한 구현에 무작위 독립성 가정을 덧붙여 임의의 작은 충돌 확률을 제시하지 않는다.

## 9. 알고리즘 선택과 실패 조건

입력 규모보다 먼저 출력 의미를 확인해야 한다. 문자 순서를 버릴 수 있는지, 중첩을 보존해야 하는지, 사전의 접두사를 찾는지, 본문에서 고정 패턴을 찾는지에 따라 저장할 상태가 달라진다. 다음 표는 앞 절에서 설명한 조건과 비용을 같은 기준으로 정리한 것이다.

| 요구 사항 | 방법 | 주요 비용 | 먼저 확인할 조건 |
| --- | --- | --- | --- |
| 간단한 분리·치환·첫 위치 | `str` 메서드 | 실제 입력·출력 길이에 의존 | 구분자와 실패값 |
| 문자 재배열 관계 | 빈도표 | 기대 $O(n_1+n_2)$ | 비교 전 정규화 정책 |
| 괄호 중첩 | Stack | $O(n)$, 공간 $O(d)$ | 허용 문자와 종료 상태 |
| 사전의 접두사 존재 | Trie | 기대 $O(q)$ 질의 | 완전 단어와 접두사 구별 |
| 한 패턴의 모든 겹친 위치 | KMP | $O(n+m+z)$ | 빈 패턴과 성공 후 복구 |
| Hash로 후보 필터링 | 검증형 rolling hash | $O(n+m+cm+z)$ | 후보 수와 원문 확인 |

복잡도를 비교할 때 `n`만 크게 보는 것으로는 충분하지 않다. 패턴 길이 $m$, 서로 다른 기호 수 $u$, 접두사 구조의 노드 수 $V$, 최대 중첩 깊이 $d$, hash 후보 수 $c$, 출력 수 $z$가 서로 다른 자원을 결정한다. 예를 들어 답 리스트가 거의 본문 길이만큼 커지는 경우 출력 저장 비용을 빼고 공간을 상수라고 말하면 실제 함수의 계약을 설명하지 못한다.

| 잘못된 선택 또는 상태 | 작은 반례 | 수정 원리 |
| --- | --- | --- |
| Anagram을 집합으로 비교 | `aab`, `abb` | 중복 횟수 보존 |
| 괄호를 종류별 개수로만 비교 | `([)]` | 미완성 괄호의 순서 보존 |
| Trie 경로를 완전 단어로 취급 | `cart`만 저장하고 `car` 질의 | 종료 표시 검사 |
| `count`를 겹침 계수로 사용 | `aaaaa` 안의 `aaa` | 모든 시작점 계약 사용 |
| KMP 성공 후 0으로 복구 | `abababa` 안의 `ababa` | 가장 긴 proper border 유지 |
| Hash 같음을 일치로 취급 | 작은 $B,Q$의 충돌 예 | 원문 재검사 |

수동 검산에서는 정상 예 하나보다 상태가 바뀌는 경계를 고르는 편이 유용하다. Stack에서는 비어 있을 때의 닫는 괄호, trie에서는 경로만 있고 종료 표시는 없는 노드, KMP에서는 여러 차례 실패 연결을 타는 문자와 연속 성공, hash에서는 마지막 창과 충돌 후보를 살펴본다. 각 경우에 “현재 상태가 이미 읽은 입력에 대해 무엇을 뜻하는가”를 말할 수 있으면 구현과 증명을 같은 규약으로 검토할 수 있다.

## 10. 요약

- `str`의 인덱스는 원문 code point 기준이다. 정규화와 case folding을 사용하면 동등성뿐 아니라 위치 대응도 다시 정해야 한다.
- 빈도표는 순서를 버리고 개수를, stack은 미완성 중첩 순서를, trie는 사전의 접두사 경로와 종료 정보를 보존한다.
- KMP는 실패할 때 border 길이를 따라가며, 성공 뒤에도 proper border를 유지해 겹친 일치를 찾는다.
- Rolling hash는 후보 필터이다. 원문 검증은 정확성을 보장하지만 많은 후보와 반복 일치의 비용을 함께 세어야 한다.
- 반환값의 빈 입력·실패·겹침 계약과 출력 저장 비용을 정한 뒤 알고리즘을 선택한다.

## 11. 참고문헌

1. Python Software Foundation, [“Built-in Types — Text Sequence Type — str”](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Python 3 documentation. String methods 및 Common Sequence Operations 포함.
2. Clayton Cafiero, [“Strings as sequences”](https://www.uvm.edu/~cbcafier/cs1210/book/10_sequences/strings_as_sequences.html), University of Vermont (2025).
3. Allen B. Downey, [“Strings,” *Think Python*, 2nd ed., Chapter 8](https://greenteapress.com/thinkpython2/html/thinkpython2009.html).
4. Python Software Foundation, [“Unicode HOWTO — Comparing Strings”](https://docs.python.org/3/howto/unicode.html#comparing-strings).
5. Unicode Consortium, [“Unicode Standard Annex #15: Unicode Normalization Forms”](https://www.unicode.org/reports/tr15/), §§1.1–1.2.
6. Python Software Foundation, [“unicodedata — Unicode Database”](https://docs.python.org/3/library/unicodedata.html#unicodedata.normalize), `unicodedata.normalize`.
7. Unicode Consortium, [*The Unicode Standard*, Chapter 3, §3.13.5 “Default Caseless Matching”](https://www.unicode.org/versions/Unicode18.0.0/core-spec/chapter-3/), definition D145.
8. Google for Developers, [“Python Strings,” Python Education](https://developers.google.com/edu/python/strings), String Methods.
9. Phil Spector, [“Functions and Methods for Character Strings”](https://www.stat.berkeley.edu/~spector/extension/python/notes/node20.html), Python course notes, University of California, Berkeley (2003).
10. Clayton Cafiero, [“Count method”](https://www.uvm.edu/~cbcafier/cs1210/book/10_sequences/count_method.html), University of Vermont (2025).
11. PyPy Project, [“Differences between PyPy and CPython”](https://doc.pypy.org/cpython_differences.html#performance-differences), Performance Differences.
12. Brad Miller and David Ranum, [“An Anagram Detection Example,” *Problem Solving with Algorithms and Data Structures*](https://runestone.academy/ns/books/published/pythonds/AlgorithmAnalysis/AnAnagramDetectionExample.html), §3.4.
13. Allen B. Downey, [“Dictionaries,” *Think Python*, 2nd ed., Chapter 11](https://greenteapress.com/thinkpython2/html/thinkpython2012.html), §11.2.
14. Robert Sedgewick and Kevin Wayne, [“Substring Search,” *Algorithms*, 4th ed., §5.3](https://algs4.cs.princeton.edu/53substring/), KMP 및 border·anagram 연습문제.
15. MIT OpenCourseWare, [“Lecture 9: Hashing II,” *6.006 Introduction to Algorithms*, Fall 2011](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/160b3b5f9da2e03815ca1e6ee0dba62a_MIT6_006F11_lec09.pdf), pp. 1–5.
16. Brad Miller and David Ranum, [“Balanced Symbols (A General Case),” *Problem Solving with Algorithms and Data Structures*](https://runestone.academy/ns/books/published/pythonds/BasicDS/BalancedSymbolsAGeneralCase.html), §4.7.
17. Robert Sedgewick and Kevin Wayne, [“Parentheses.java,” *Algorithms*, 4th ed., §1.3](https://algs4.cs.princeton.edu/13stacks/Parentheses.java.html).
18. Robert Sedgewick and Kevin Wayne, [“Tries,” *Algorithms*, 4th ed., §5.2](https://algs4.cs.princeton.edu/52trie/), [“TrieST.java”](https://algs4.cs.princeton.edu/52trie/TrieST.java.html).
19. Thomas Cortina, Frank Pfenning, Rob Simmons, and Penny Anderson, [“Lecture Notes on Tries,” *15-122 Principles of Imperative Computation*, Lecture 23](https://www.cs.cmu.edu/~rjsimmon/15122-s15/lec/22-tries.pdf), Carnegie Mellon University (April 9, 2015), §3.
20. Cornell University, [“Lecture 25: String Matching,” *CS 312*, Spring 2002](https://www.cs.cornell.edu/courses/cs312/2002sp/lectures/lec25.htm), Knuth–Morris–Pratt Algorithm.
21. Robert Sedgewick and Kevin Wayne, [“KMPplus.java,” *Algorithms*, 4th ed., §5.3](https://algs4.cs.princeton.edu/53substring/KMPplus.java.html).
22. Robert Sedgewick and Kevin Wayne, [“RabinKarp.java,” *Algorithms*, 4th ed., §5.3](https://algs4.cs.princeton.edu/53substring/RabinKarp.java.html), hash, check, search.
