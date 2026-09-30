---
description: Python 정수 연산을 바탕으로 약수와 소수, 모듈러 연산, 조합 계수와 비트 집합을 설명하고 주기 동기화 문제와 큰 정수의 계산 비용을 분석한다.
---

# Number theory and combinatorics

정수 알고리즘은 나눗셈으로 약수 관계를 판별하고, 나머지로 같은 상태를 묶으며, 조합식으로 선택의 수를 계산한다. 이 문서는 Python 3.10 이상에서 사용할 수 있는 정수 연산을 기준으로 한다. 작은 수의 계산 결과도 규약에 따라 직접 유도하며, 마지막에는 여러 주기 사건이 다시 만나는 시점을 구하는 하나의 문제에 적용한다. 예제 코드는 실행 결과를 제시하는 형식이 아니라 수식과 불변식을 구현한 참고 코드이다. `gcd`, `isqrt`, 세 인자 `pow` 등 표준 함수의 기능은 [Python algorithm toolkit](python-toolkit.md)에서 확인하고, 여기서는 그 배경이 되는 정수 알고리즘과 적용 조건을 다룬다.

## 1. 정수 나눗셈과 나머지

### (1) 몫과 나머지의 규약

정수 $a$를 0이 아닌 정수 $b$로 나눌 때 Python의 `a // b`는 실수 몫을 아래쪽으로 내린 정수이다. 0을 향한 절삭과는 다르다. 몫을 $q$, 나머지를 $r$라 하면 다음 관계를 만족한다.[1,2]

$$
q=\left\lfloor\frac{a}{b}\right\rfloor,
\qquad r=a-bq,
\qquad a=bq+r.
$$

여기서 바닥 함수 $\lfloor x\rfloor$는 $x$ 이하인 가장 큰 정수이다. `a % b`가 반환하는 $r$는 0이거나 $b$와 같은 부호이다. 따라서 양수 $b$에서는 $0\le r<b$, 음수 $b$에서는 $b<r\le0$이다. 나눗셈 대상이 음수라는 이유만으로 나머지가 음수가 되는 것은 아니다.[1,3]

다음 표는 식에 값을 대입한 수작업 계산이다. 마지막 열을 확인하면 음수 조합에서도 같은 항등식이 유지됨을 알 수 있다.

| $a$ | $b$ | `a // b` | `a % b` | 복원식 |
| --- | --- | --- | --- | --- |
| 7 | 3 | 2 | 1 | $7=3\cdot2+1$ |
| -7 | 3 | -3 | 2 | $-7=3\cdot(-3)+2$ |
| 7 | -3 | -3 | -2 | $7=(-3)\cdot(-3)-2$ |
| -7 | -3 | 2 | -1 | $-7=(-3)\cdot2-1$ |

몫과 나머지가 모두 필요하면 `divmod(a, b)`로 한 쌍을 받는다. 정수 인수에서는 `(a // b, a % b)`와 같은 수학적 결과이다. NumPy도 같은 몫·나머지 규약을 명시하지만, 이 문서의 코드는 배열이 아닌 Python 기본 정수를 사용한다.[4,5]

예를 들어 `q, r = divmod(-7, 3)`에서 수식으로 구한 값은 `q = -3`, `r = 2`이다.

### (2) 정수 경계의 계산

나누어떨어짐은 `a % b == 0`으로 판별한다. 양수 $b$에 대해 $a$ 이상의 첫 $b$의 배수를 구하려면 올림한 몫이 필요하다. 바닥 함수의 부호 관계를 적용하면 정수 $a$의 부호와 무관하게 다음 식을 얻는다. 이는 앞의 나눗셈 정의에서 유도한 정확한 관계이다.[1,2]

$$
\left\lceil\frac{a}{b}\right\rceil
=-\left\lfloor\frac{-a}{b}\right\rfloor
=\left\lfloor\frac{a+b-1}{b}\right\rfloor
\qquad(a\in\mathbb Z,\ b>0).
$$

코드로는 `ceil_quotient = -((-a) // b)`이며, 이 몫에 `b`를 곱하면 첫 배수이다.

첫 식은 `-a // b`의 바깥에 음수 부호를 붙여야 한다는 점이 중요하다. 예를 들어 $a=-7,b=3$이면 올림 몫은 $-2$이고 첫 배수는 $-6$이다. 양수만 염두에 둔 직관으로 $-9$를 고르면 $a$ 이상이라는 조건을 위반한다. 모든 식은 제수가 0이 아니라는 전제에서만 의미가 있다.

이 문서의 경계 계산은 바닥 몫 `//`를 기준으로 한다. `/`의 나눗셈 결과와 바닥 몫을 구별하고, 위 올림식처럼 필요한 정수 경계를 직접 표현한다.[1,2]

## 2. 최대공약수와 최소공배수

### (1) Euclidean algorithm의 불변식

Greatest common divisor (GCD)는 두 정수를 함께 나누는 가장 큰 양의 정수이며, 두 수가 모두 0인 경우에는 별도의 규약을 둔다. 양수 $a,b$에 대해 $a=bq+r$라고 쓰면 $a,b$의 공약수 집합과 $b,r$의 공약수 집합은 같다. 따라서 나머지 계산으로 문제를 줄일 수 있다.[6,7]

$$
\gcd(a,b)=\gcd(b,a\bmod b),
\qquad \gcd(a,0)=a\quad(a>0).
$$

공약수 $d$가 $a,b$를 나누면 $r=a-bq$도 나눈다. 반대로 $d$가 $b,r$를 나누면 $a=bq+r$도 나눈다. 이 양방향 논증이 Euclidean algorithm의 불변식이다. $b>0$일 때 새 나머지는 $0\le r<b$이므로 두 번째 값이 계속 작아져 0에 도달한다. 그때 남은 첫 값이 답이다.[6,7]

다음은 음수 입력을 절댓값으로 정규화한 반복 구현이다. 절댓값을 취해도 양의 공약수 집합이 바뀌지 않는다. 아래 함수에서는 두 입력이 모두 0이면 0을 반환하도록 별도 정의한다. 이는 양수 입력의 공약수 정의를 확장한 이 문서의 함수 계약이다.[6,7]

```python
def gcd_euclid(a: int, b: int) -> int:
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a
```

$(84,30)$의 진행은 $(30,24)$, $(24,6)$, $(6,0)$이므로 GCD는 6이다. 대입문은 오른쪽의 기존 `a`, `b`로 두 새 값을 계산한다. `a = b`를 먼저 하고 그 변경된 `a`로 나머지를 구하면 이 진행을 구현하지 못한다.

양수 입력에서 나머지 계산 횟수는 $O(\log\min(a,b))$이다. 인접한 Fibonacci 수가 긴 실행 경로를 만드는 대표적인 경우이다. 이 표기는 나머지 한 번을 하나의 연산으로 세는 모형이며, 수가 매우 클 때 나머지 계산 자체의 비용까지 상수라고 주장하지 않는다.[6,7]

### (2) 공배수와 0의 경계

Least common multiple (LCM)은 양수 두 수의 공통 배수 가운데 가장 작은 양수이다. $g=\gcd(a,b)$라 할 때 양수 입력의 LCM은 다음 식으로 계산한다.[6,7]

$$
\operatorname{lcm}(a,b)=\frac{ab}{g}
=\left(\frac{a}{g}\right)b.
$$

$a=gu,b=gv$로 쓰면 $u,v$는 서로소이다. 두 수의 공통 배수는 $g$에 더해 $u,v$의 요인을 모두 포함해야 하므로 가장 작은 값은 $guv$이다. 구현에서는 $a$가 $g$로 정확히 나누어떨어지는 사실을 이용해 `a // g * b` 순서로 계산한다. 중간에 필요 이상으로 큰 곱 $ab$를 만들지 않는 이점이 있다.[6,7]

부호 있는 인수와 0까지 다룰 때는 양의 정의를 그대로 적용하지 말고 함수 규약을 명시해야 한다. 여기서는 앞의 `gcd_euclid`와 아래의 `lcm_pair`에 다음 표의 계약을 부여한다. 음수 입력의 처리는 양의 약수 관계가 절댓값에 의해 바뀌지 않는다는 사실에서 유도하고, 0의 LCM은 별도로 0으로 정의한다.[6,7]

| 입력 조건 | GCD | LCM |
| --- | --- | --- |
| 양수 $a,b$ | 가장 큰 공약수 | 가장 작은 양의 공배수 |
| 한 입력만 0, 다른 입력 $a\ne0$ | $|a|$ | 0 |
| 두 입력 모두 0 | 0으로 정의 | 0으로 정의 |
| 0이 아닌 음수 포함 | 절댓값의 GCD | 절댓값의 LCM |

LCM을 직접 만들면 두 입력이 모두 0인 경우를 나눗셈보다 먼저 처리해야 한다. 그렇지 않으면 $0/\gcd(0,0)$에서 0으로 나누게 된다. 다음 구현은 앞서 정의한 `gcd_euclid`를 사용하며 모든 정수 입력에 대해 위 표의 규약을 따른다. 0 분기를 먼저 통과한 뒤에는 GCD가 양수이므로 나눗셈이 정의된다.[6,7]

```python
def lcm_pair(a: int, b: int) -> int:
    if a == 0 or b == 0:
        return 0
    return abs((a // gcd_euclid(a, b)) * b)
```

## 3. 소수 판별과 소인수분해

### (1) Trial division과 정확한 제곱근

소수는 1보다 크고 양의 약수가 1과 자기 자신뿐인 정수이다. 따라서 음수, 0, 1은 소수가 아니다. 합성수 $n$에는 $n=uv$인 두 정수 $u,v>1$이 있으므로 적어도 하나는 $\sqrt n$ 이하이다. 두 인수가 모두 $\sqrt n$보다 크다면 곱이 $n$보다 커지는 모순이 생긴다.[7,8]

$$
n\ge2\text{가 소수}
\iff
\text{정수 }d\in[2,\lfloor\sqrt n\rfloor]\text{ 중 }n\bmod d=0\text{인 값이 없다}.
$$

제곱근 경계를 정수 연산으로 표현하려면 후보 $d$에 대해 $d^2\le n$을 직접 검사하면 된다. $s=\lfloor\sqrt n\rfloor$를 다음 부등식으로 정의하면, 양의 정수 후보에서 $d\le s$와 $d^2\le n$은 동치이다.[7,8]

$$
s=\lfloor\sqrt n\rfloor
\quad\Longleftrightarrow\quad
s^2\le n<(s+1)^2,
\qquad n\ge0.
$$

다음 코드는 2를 별도로 처리하고 홀수 약수만 확인한다. 반복에 들어가기 전에 `n < 2`를 처리한다.[7,8]

```python
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True
```

경계의 `<=`는 완전제곱을 놓치지 않기 위해 필요하다. $49$의 약수 7은 $\lfloor\sqrt{49}\rfloor$ 자체이다. $n=3$에서는 반복 구간이 비고 `True`가 반환되는 것이 맞다. `n=2`는 앞 분기에서 처리된다. 이 구현은 최악에 $O(\sqrt n)$번의 나머지 검사를 하며, 단일 작은 정수의 정확한 판별에 적합하다. $n$의 자릿수가 커질수록 이 반복 상한이 급격히 커진다는 한계가 있다.[7,8]

### (2) Sieve of Eratosthenes

여러 정수의 소수 여부가 필요하고 상한 $N$을 미리 알고 있다면, 각 수를 따로 판별하는 대신 Sieve of Eratosthenes로 $0$부터 $N$까지의 표를 만든다. 아직 지워지지 않은 소수 $p$의 배수를 합성수로 표시한다. $p^2$보다 작은 $p$의 배수는 이미 더 작은 소인수를 가지므로 그 소인수 단계에서 처리되었다.[7,9]

```python
def prime_table(limit: int) -> list[bool]:
    if limit < 0:
        raise ValueError("limit must be nonnegative")
    prime = [True] * (limit + 1)
    prime[0] = False
    if limit >= 1:
        prime[1] = False
    p = 2
    while p * p <= limit:
        if prime[p]:
            for multiple in range(p * p, limit + 1, p):
                prime[multiple] = False
        p += 1
    return prime
```

`limit=0`에서도 존재하지 않는 인덱스 1을 쓰지 않도록 분기했다. 입력 상한보다 큰 수의 소수 여부는 이 표로 알 수 없다. 모든 합성수는 제곱근 이하의 소인수를 하나 이상 가지므로 바깥 반복은 `p * p <= limit`인 동안만 진행해도 충분하다.[7,9]

소수 $p$에 대한 표시 횟수는 대략 $N/p$이며, 이를 소수에 대해 더한 결과로 표준 체의 전체 연산 수는 $O(N\log\log N)$이다. 표의 저장 공간은 $O(N)$개 항목이다. 이는 항목 개수를 센 것이며 실제 저장 바이트 수에 대한 주장이 아니다. 이후 개별 소수 여부는 해당 인덱스의 값을 읽는다.[7,9]

| 요구 사항 | 먼저 검토할 방법 | 확보하는 결과 |
| --- | --- | --- |
| 한 수의 소수 여부 | Trial division | 참 또는 거짓 |
| 상한 안의 많은 수 | Sieve | 모든 수의 소수 여부 표 |
| 한 수의 소인수와 지수 | 반복 나눗셈 | 소인수별 출현 횟수 |

### (3) 남은 몫의 소인수분해

소인수분해에서는 약수를 발견한 뒤 같은 약수로 더 나누어질 때까지 반복한다. 원래 수를 계속 검사하는 대신 나누고 남은 몫을 줄이면 종료 경계도 함께 줄어든다. 더 이상 제곱근 이하의 약수가 없는데 남은 몫이 1보다 크면, 그 몫 자체가 마지막 소수이다.[7,10]

```python
def factorize(n: int) -> dict[int, int]:
    if n < 1:
        raise ValueError("n must be positive")
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors
```

이 함수에서 1의 결과는 빈 사전이다. 0은 이 문서의 양의 정수 소인수분해 대상이 아니므로 거부한다. 첫 검사를 없애고 0을 넣으면 `d * d <= n`부터 거짓이 되어 빈 사전으로 끝나며, 1과 0을 구별하지 못한다. 이는 코드의 분기 조건을 대입해 확인한 결과이다. 음수의 부호를 소인수와 별도로 기록하는 설계는 가능하지만, 여기서는 양수만 받는 계약을 택했다. 반복에서 합성수 `d`도 지나가지만, 작은 소인수를 모두 제거한 뒤에는 그 합성수로 나누어질 수 없어 결과 사전에는 소수만 남는다.[7,10]

$84$를 예로 들면 2로 두 번 나누어 남은 값이 21, 3으로 한 번 나누어 7이다. 다음 후보 4에서는 $4^2>7$이므로 종료하고 7을 추가한다. 원래 입력을 $n_0$라 하면 매 단계에서 다음 불변식이 성립한다. $e_p$는 지금까지 기록한 소수 $p$의 지수이고, $n_{\mathrm{rem}}$은 현재의 남은 몫이다.[7,10]

$$
n_0=\left(\prod_{p\text{가 기록됨}}p^{e_p}\right)n_{\mathrm{rem}}.
$$

나눌 때마다 곱에 같은 소수 하나를 추가하므로 이 식이 보존된다. 마지막 몫까지 기록하면 원래 수가 완전히 복원된다. 최악의 연산 수는 처음부터 소수여서 끝까지 검사하는 경우의 $O(\sqrt{n_0})$이다. 결과를 저장하는 공간은 실제로 기록한 서로 다른 소인수의 수에 비례한다.[7,10]

## 4. 모듈러 연산과 역원

### (1) 합동 관계와 곱셈

이 절에서는 modulus $m$을 $m\ge2$인 정수로 고정한다. $a\equiv b\pmod m$은 $m$이 $a-b$를 나눈다는 뜻이며, 두 정수가 같은 나머지로 표현된다는 관계이다. 덧셈·뺄셈·곱셈 도중에 나머지를 취해도 최종 나머지는 보존된다.[7,11]

$$
(a+b)\bmod m=((a\bmod m)+(b\bmod m))\bmod m,
\qquad
ab\bmod m=((a\bmod m)(b\bmod m))\bmod m.
$$

이 성질은 큰 거듭제곱을 만드는 도중에 수를 줄이는 근거이다. 예를 들어 $a=mq+r$를 곱에 대입하면 $m$의 배수인 항들은 최종 나머지에 기여하지 않는다. 하지만 나머지를 취하는 것은 원래 정수의 크기 정보를 버리는 연산이므로, 대소 비교나 일반적인 나눗셈에도 같은 치환이 가능하다고 확대하면 안 된다.[11,12]

### (2) Binary exponentiation

지수 $e$가 비음수 정수일 때 거듭제곱을 반복 제곱으로 분해한다. 짝수 지수는 절반 지수의 제곱, 홀수 지수는 거기에 밑 하나를 더 곱한 형태이다. 이 관계를 각 단계에서 modulus $m$으로 줄이는 것이 modular exponentiation이다.[7,12]

$$
a^e=
\begin{cases}
1,&e=0,\\
(a^{e/2})^2,&e>0\text{이고 짝수},\\
a(a^{(e-1)/2})^2,&e\text{가 홀수}.
\end{cases}
$$

다음 구현은 $a$가 정수, $e\ge0$, $m\ge2$인 계약을 사용한다. 남은 지수가 홀수이면 현재 밑을 결과에 곱하고, 밑을 제곱하며 지수를 절반의 바닥 몫으로 줄인다. 각 곱셈마다 나머지를 취하므로 전체 거듭제곱을 먼저 구성하지 않는다.[7,12]

```python
def power_mod(a: int, e: int, m: int) -> int:
    if e < 0 or m < 2:
        raise ValueError("invalid modular power domain")
    result = 1
    base = a % m
    while e:
        if e % 2:
            result = (result * base) % m
        base = (base * base) % m
        e //= 2
    return result
```

반복 직전의 `result * base ** e`는 원래 거듭제곱과 합동이다. 홀수 지수에서 밑 하나를 결과로 옮긴 뒤 제곱과 지수 절반 처리를 하면 이 관계가 유지된다. $e=0$이면 처음부터 결과 1을 반환한다. 이 불변식은 앞의 반복 제곱 관계와 합동의 곱셈 성질에서 유도된다.[7,12] 예를 들어 `power_mod(7, 13, 11)`의 나머지는 다음 수작업 전개로 구할 수 있다.

$13=8+4+1$이고 $7^2\equiv5$, $7^4\equiv3$, $7^8\equiv9\pmod{11}$이다. 따라서 $7^{13}\equiv9\cdot3\cdot7=189\equiv2\pmod{11}$이다. $7^{13}$ 전체를 십진수로 계산할 필요가 없다는 점이 핵심이다.

양수 지수에서 반복 제곱은 $O(\log e)$번의 모듈러 곱셈으로 표현된다. 각 곱셈이 끝난 뒤에는 나머지를 $0$ 이상 $m$ 미만으로 유지할 수 있다. 다만 곱셈 직후, 나머지 연산 전의 중간 곱까지 항상 $m$ 미만인 것은 아니다. 이 점근식은 위 반복의 모듈러 곱셈 횟수를 세며 개별 큰 정수 곱셈의 시간은 별도로 다룬다.[7,12]

### (3) 역원의 존재 조건

$a$의 modular inverse는 $ax\equiv1\pmod m$을 만족하는 정수 $x$의 나머지이다. 역원은 $a$와 $m$이 서로소일 때에만 존재하며, 존재하면 modulus $m$ 안에서 유일하다. 이는 다음 Bézout 관계와 연결된다.[11,13]

$$
ax\equiv1\pmod m
\iff \exists y\in\mathbb Z:\ ax+my=1
\iff \gcd(a,m)=1.
$$

공약수 $d>1$이 있다면 왼쪽 정수 선형결합의 모든 값이 $d$의 배수이므로 1이 될 수 없다. 반대로 GCD가 1이면 extended Euclidean algorithm으로 이런 $x,y$를 찾을 수 있다. 찾은 계수 $x$를 $m$으로 줄이면 역원의 표준 나머지를 얻는다.[11,13]

계수를 찾는 과정은 나머지를 구한 기록을 거꾸로 대입하는 것으로 이해할 수 있다. 나눗셈 한 단계가 $A_0=A_1q+r$이고, 다음 단계에서 얻은 GCD 표현이 $g=A_1c_0+rc_1$라고 하자. 여기서 $A_0,A_1$은 현재의 두 양의 정수, $q,r$는 몫과 나머지, $c_0,c_1$은 정수 계수이다. $r=A_0-A_1q$를 대입하면 다음 관계를 얻는다.[11,13]

$$
g=A_1c_0+(A_0-A_1q)c_1=A_0c_1+A_1(c_0-qc_1).
$$

따라서 작은 쌍 $(A_1,r)$의 계수 $(c_0,c_1)$를 알면 이전 쌍 $(A_0,A_1)$의 계수는 $(c_1,c_0-qc_1)$로 복원된다. 마지막 나머지가 0일 때 남은 GCD는 자기 자신의 1배이므로 복원의 출발점이 있다. 이 과정을 처음 입력까지 반복하면 원래 두 수의 정수 선형결합을 얻는다. 나머지만 보존하는 앞의 `gcd_euclid`와 달리, 역원을 구하려면 이런 계수 정보도 추적해야 한다.[11,13]

예를 들어 modulus 10에서 3의 역원을 수작업으로 구하면 $10=3\cdot3+1$에서 바로 $1=10-3\cdot3$을 얻는다. 따라서 Bézout 계수는 $x=-3$, $y=1$이고, $x$의 표준 나머지는 7이다. 음수 계수가 나온 것은 실패가 아니라 같은 나머지류의 다른 대표를 얻은 것이다. $3\cdot7=21\equiv1\pmod{10}$으로 원래 조건도 확인된다. 이 계산은 정수 등식을 먼저 얻고 나서 modulus를 적용한 것이며, 중간 과정에서 역원이 없는 수로 모듈러 나눗셈을 하지 않는다.[11,13]

두 후보 $x_1,x_2$가 모두 역원이라면 $m$은 $a(x_1-x_2)$를 나눈다. 이때 Bézout 등식 $ax+my=1$에 $x_1-x_2$를 곱하면 오른쪽도 $m$의 배수여야 한다. 따라서 두 후보의 차이는 $m$의 배수이다. 이것이 정수 계수 자체는 여러 개일 수 있어도 $0$ 이상 $m$ 미만의 역원은 하나라는 뜻이다.[11,13]

소수 $p$이고 $a$가 $p$의 배수가 아닐 때에는 Fermat의 관계에서 역원을 구할 수 있다. 여기서 $p$는 일반 modulus가 아니라 소수라는 조건을 갖는다.[7,13]

$$
a^{p-1}\equiv1\pmod p
\quad\Longrightarrow\quad
a^{-1}\equiv a^{p-2}\pmod p.
$$

합성수에서도 서로소인 수의 역원은 존재한다. 다만 지수 $m-2$가 역원을 준다는 보장은 없다. 예를 들어 modulus 9에서 2의 역원은 5이지만 $2^7=128\equiv2\pmod9$이다. 반대로 modulus 10에서 2는 역원이 없다. 다음 구분은 위 정리와 직접 곱셈으로 확인할 수 있다.[11,13]

| modulus와 밑 | 역원 존재 | 적용 가능한 계산 |
| --- | --- | --- |
| 소수 $p$, $p\nmid a$ | 존재 | Extended Euclidean algorithm 또는 $a^{p-2}\bmod p$ |
| 합성수 $m$, $\gcd(a,m)=1$ | 존재 | Extended Euclidean algorithm |
| $\gcd(a,m)>1$ | 없음 | 역원 곱셈으로 나눌 수 없음 |

정수의 정확한 나눗셈과 모듈러 나눗셈도 구별한다. $6/2=3$이라는 정수 계산은 가능하지만, modulus 4에서 2의 역원을 곱해 이를 복구할 수는 없다. 실제로 $2x\equiv2\pmod4$는 $x=1,3$을 모두 허용한다. 이 경우 2를 약분하면서 modulus 4를 그대로 유지하면 서로 다른 해를 하나로 오인한다.[11,13]

## 5. 조합 계수와 경우의 수

### (1) 순서와 중복의 구별

개수를 계산하기 전에 같은 결과로 취급할 기준부터 정한다. 서로 다른 $n$개 항목에서 $k$개를 중복 없이 고를 때, 순서를 구별하면 permutation이고 순서를 버리면 combination이다. $0\le k\le n$에서 두 개수는 다음과 같다. $n!$는 $1$부터 $n$까지의 곱이며 $0!=1$이다.[7,14]

$$
P(n,k)=\frac{n!}{(n-k)!},
\qquad
\binom nk=\frac{n!}{k!(n-k)!}.
$$

첫 자리는 $n$가지, 다음 자리는 $n-1$가지이므로 순서 있는 선택은 $n(n-1)\cdots(n-k+1)$개이다. 같은 $k$개를 고른 뒤 순서만 바꾸는 방법이 $k!$개이므로 이를 나누면 조합 수가 된다. 이 유도는 항목들이 서로 구별되고, 한 항목을 두 번 뽑지 않는 조건에 의존한다.[7,14]

다음은 같은 네 개의 서로 다른 표지에서 두 개를 고르는 계산이다. 순서 있는 선택은 $4\cdot3=12$, 순서 없는 선택은 $12/2=6$이다. 예를 들어 `(A, B)`와 `(B, A)`를 별개로 기록하는지에 따라 답이 달라진다.

| 선택 모형 | 같은 결과의 기준 | 개수 |
| --- | --- | --- |
| 중복 없는 순서 있는 $k$개 | 순서까지 일치 | $P(n,k)$ |
| 중복 없는 순서 없는 $k$개 | 선택한 집합이 일치 | $\binom nk$ |
| 각 원소의 포함 여부를 선택 | 부분집합이 일치 | $2^n$ |

마지막 행은 각 원소를 넣거나 빼는 두 선택을 독립적으로 한다는 뜻이다. 크기별 조합 수를 합쳐도 같은 전체 부분집합 수를 얻는다. 이 표는 동일한 값을 가진 입력 항목들을 자동으로 하나로 합치지 않는다. 값의 중복과 항목의 식별 가능성은 별도의 모델 선택이다.[7,14]

이 선택 모형에서 $k>n$이면 가능한 선택이 없어 0으로 센다. $k=0$이면 빈 선택 하나이다. 아래 구현은 $n,k$가 비음수인 경우만 대상으로 한다.[7,14]

### (2) Pascal identity와 갱신 순서

고정된 한 원소를 포함하는 선택과 포함하지 않는 선택은 겹치지 않으며 전체를 이룬다. 이에 따라 $1\le k<n$에서 Pascal identity를 얻는다. 경계에는 빈 선택과 전체 선택이 각각 하나씩 있다.[7,14]

$$
\binom nk=\binom{n-1}{k-1}+\binom{n-1}{k},
\qquad \binom n0=\binom nn=1.
$$

전체 삼각형 대신 한 행만 유지하려면 오른쪽에서 왼쪽으로 갱신한다. 다음 코드는 $n,k$가 비음수이고 modulus $m\ge2$라는 계약 아래 조합의 나머지를 계산한다. 덧셈만 사용하므로 $m$이 소수일 필요가 없다.[7,14]

```python
def comb_mod_pascal(n: int, k: int, m: int) -> int:
    if n < 0 or k < 0 or m < 2:
        raise ValueError("invalid counting domain")
    if k > n:
        return 0
    k = min(k, n - k)
    row = [0] * (k + 1)
    row[0] = 1
    for i in range(1, n + 1):
        for j in range(min(i, k), 0, -1):
            row[j] = (row[j] + row[j - 1]) % m
    return row[k]
```

여기서 `i`는 현재 행 번호, `j`는 선택 수이다. 갱신 직전의 `row[j]`, `row[j - 1]`은 이전 행의 두 값을 나타내야 한다. `j`를 감소시키면 작은 인덱스는 아직 갱신하지 않았으므로 그 조건이 유지된다. 반대로 증가시키면 방금 바꾼 현재 행을 다시 더하게 된다. 예를 들어 이전 행이 `[1, 2, 1]`일 때 다음 행의 앞 세 값은 `[1, 3, 3]`이어야 한다. 왼쪽부터 갱신하면 마지막 값이 $1+3=4$가 되어 틀린다. 이는 점화식으로부터 직접 확인한 갱신 순서의 결과이다.[7,14]

대칭성 $\binom nk=\binom n{n-k}$를 사용해 $k$를 작은 쪽으로 줄였다. 줄인 값을 $k'$라 하면 반복문의 범위를 직접 세면 덧셈·나머지 계산은 $O(nk')$회이고, 저장 공간은 $O(k'+1)$개 정수이다. $k'=0$일 때도 한 항목을 저장하고 바깥 반복은 $n$회 진행한다. 초기화와 반복 제어까지 세는 단위 연산 모형의 전체 작업량은 $O(1+n(1+k'))$로 쓸 수 있다. 고정된 작은 $m$의 연산 수를 세는 표기이며, 큰 modulus의 비트 비용은 별도로 고려한다.[7,14]

### (3) Factorial의 모듈러 나눗셈 한계

일반 정수 조합식의 분모가 정확히 나누어떨어진다고 해서, 분자와 분모를 먼저 modulus로 줄인 뒤 정수 나눗셈을 해도 되는 것은 아니다. 소수 $p>n$이면 $1$부터 $n$까지 모두 $p$와 서로소이므로 factorial의 역원이 존재한다. 그때에는 다음 식을 사용할 수 있다.[11,14]

$$
\binom nk\equiv n!\,(k!)^{-1}\,((n-k)!)^{-1}\pmod p,
\qquad 0\le k\le n<p.
$$

많은 조합 질의를 같은 범위에서 처리하면 factorial과 inverse factorial을 미리 준비하는 방법을 고려할 수 있다. 여기서는 역원 존재 조건을 만족시키는 범위가 핵심이다. $n\ge p$이면 $n!$가 $p$의 배수가 되어 위 방식으로 factorial의 역원을 만드는 절차가 깨진다. 조합 수 자체가 항상 0이 된다는 뜻은 아니다.[11,14]

수작업 반례로 $\binom52=10$을 modulus 5로 줄이면 0이지만, $\binom51=5$가 0이라는 사실만으로 같은 행 전체가 0이라고 할 수 없다. 양끝 $\binom50=\binom55=1$은 여전히 1이다. 합성수 modulus에서도 분모에 modulus와 공통인 소인수가 있으면 역원 계산이 실패한다. 예를 들어 $\binom42=6$은 modulus 8에서 6이지만, 분모 $2!2!=4$의 역원은 없다. 작은 범위에서는 덧셈만 쓰는 Pascal 계산이 이런 역원 가정을 피한다.[11,14]

## 6. 비트 연산과 유한 집합

### (1) 부분집합의 정수 표현

서로 다른 $w$개 항목을 인덱스 $0,\ldots,w-1$로 표시하고, 선택된 인덱스 집합을 $S$라 하자. 각 비트의 포함 여부를 정수에 담으면 다음 일대일 대응을 얻는다. 가장 오른쪽 비트의 인덱스를 0으로 정한다.[1,7]

$$
\operatorname{mask}(S)=\sum_{i\in S}2^i,
\qquad 0\le\operatorname{mask}(S)<2^w.
$$

비트마다 0과 1의 두 상태가 있어 총 $2^w$개 부분집합을 표현한다. 비트 표현은 선택 상태를 간결하게 저장하지만, 모든 부분집합을 실제로 방문하는 횟수까지 줄이지는 않는다. 다음 표에서 `mask`는 유효한 $w$비트 비음수 정수이고 `i`는 `0 <= i < w`이다.[1,7]

| 연산 목적 | Python 식 | 비트에 미치는 영향 |
| --- | --- | --- |
| 포함 여부 | `bool(mask & (1 << i))` | $i$번째 비트 검사 |
| 추가 | `mask | (1 << i)` | $i$번째를 1로 설정 |
| 제거 | `mask ^ (mask & (1 << i))` | $i$번째를 0으로 설정 |
| 선택 반전 | `mask ^ (1 << i)` | 해당 비트만 반전 |
| 교집합 | `left & right` | 둘 다 1인 위치 |
| 합집합 | `left | right` | 하나라도 1인 위치 |

Bitwise exclusive OR (XOR)는 두 비트가 다를 때 1을 만드는 연산이다. 제거 식은 비트별 논리곱 `&`로 먼저 기존 비트만 골라 XOR하므로, 이미 없는 원소는 그대로 둔다. 반대로 `mask ^ (1 << i)`는 해당 비트를 무조건 반전하여 원래 없던 원소를 추가할 수 있다. 예를 들어 `0b1010`에서 인덱스 0을 XOR하면 `0b1011`이 되므로 제거가 아니다.[1,7]

### (2) 유한 비트 폭과 가장 낮은 비트

전체 집합의 마스크를 `full = (1 << w) - 1`로 정의한다. 유효한 마스크는 $0\le\texttt{mask}<2^w$를 만족한다. 이 범위에서 `full ^ mask`는 $w$개 비트를 각각 뒤집으므로 여집합이다. 이는 비음수 정수의 비트별 XOR 정의로부터 직접 유도한 식이다.[1,7]

```python
w = 5
mask = 0b00101
full = (1 << w) - 1
complement = full ^ mask  # 수작업: 0b11010
```

입력에 범위 밖의 1비트가 있으면 이 XOR는 그 비트를 없애지 않는다. 따라서 표현의 전제인 비트 폭을 먼저 정해야 한다. 예를 들어 $w=5$에서 인덱스 5는 집합 원소가 아니며, 그 비트가 켜진 정수는 유효한 입력이 아니다.[1,7]

양수 $x$에서 `x & (x - 1)`은 가장 낮은 1비트를 지운다. $x-1$을 만들면 그 1비트가 0이 되고 그 아래 0들은 1이 된다. 비트별 논리곱을 취하면 높은 비트는 유지되고 해당 1비트만 사라진다. 따라서 원래 $x$와 지운 결과를 XOR하면 바뀐 한 비트만 분리된다. 다음 두 번째 식은 이 관찰에서 직접 유도했다.[1,7]

```python
x = 0b101100
without_lowest = x & (x - 1)  # 0b101000
lowest_only = x ^ without_lowest  # 0b000100
```

양수 $x$의 가장 낮은 1비트를 지운 값이 0이면 원래 1비트는 하나뿐이므로 $x$는 2의 거듭제곱이다. 이 설명과 코드는 $x>0$인 입력에 한정한다. 위 연산들은 음수의 표현 규약을 필요로 하지 않으며, 집합 계산 전체를 정해진 폭의 비음수 마스크 안에서 해석한다.[1,7]

## 7. 대표 문제: 주기 사건의 동기화

### (1) 문제

$M$개의 장치가 정수 시각 0에 동시에 신호를 내고, 장치 $i$는 이후 양의 정수 주기 $p_i$마다 신호를 낸다. 모든 시간의 단위는 동일하다. 정수 시각 $T$ 이상에서 모든 장치가 동시에 신호를 내는 가장 이른 시각을 반환하라. 시작 시각 0도 사건에 포함하며, 입력은 $1\le M\le10^4$, $1\le p_i\le10^9$, $0\le T\le10^{18}$로 정한다. 결과의 크기에는 별도의 고정 정수 폭 제한을 두지 않는다.

입력 예시에서 `periods`의 원소는 순서대로 12, 18, 30이고 `threshold = 250`이다. 이 문제는 LCM과 정수 올림을 적용하도록 구성한 창작 예제이며, 아래 답은 손으로 유도한다.

### (2) 답

동시에 발생하는 시각은 모든 $p_i$의 공통 배수이다. 그중 기본 주기를 $L$이라 하면 정답 $t_*$는 다음과 같다. $T$는 허용되는 최소 시각이며, $L$은 입력 목록의 LCM이다.[6,7]

$$
L=\operatorname{lcm}(p_1,\ldots,p_M),
\qquad t_*=L\left\lceil\frac TL\right\rceil.
$$

다음 함수는 주기 목록을 한 번 훑으며 LCM을 누적한다. 모든 인수는 정수라는 계약이며, 빈 목록·0 이하의 주기·음수 시작 조건은 거부한다. 앞서 정의한 `gcd_euclid`를 사용한다.

```python
def next_synchronization(periods: list[int], threshold: int) -> int:
    if not periods or threshold < 0:
        raise ValueError("periods must be nonempty and threshold nonnegative")

    cycle = 1
    for period in periods:
        if period <= 0:
            raise ValueError("periods must be positive")
        cycle = (cycle // gcd_euclid(cycle, period)) * period

    cycles_needed = (threshold + cycle - 1) // cycle
    return cycles_needed * cycle
```

예시의 수작업 누적 과정은 다음과 같다.

| 반영한 주기 | 이전 LCM | GCD | 새 LCM |
| --- | --- | --- | --- |
| 12 | 1 | 1 | 12 |
| 18 | 12 | 6 | 36 |
| 30 | 36 | 6 | 180 |

$L=180$이고 $250$ 이상인 첫 배수는 $180\cdot2=360$이다. 따라서 답은 **360**이다. $180<250\le360$이며 360은 12, 18, 30으로 각각 나누어떨어진다. 이 두 사실이 하한 조건과 동시 발생 조건을 함께 확인한다.

### (3) 해설과 경계 사례

루프의 불변식은 `cycle`이 지금까지 읽은 모든 주기의 LCM이라는 것이다. 초기값 1은 아직 반영한 주기가 없는 곱셈의 기준값으로 사용할 수 있다. 다음 주기 `period`를 반영할 때 두 수의 LCM 공식을 적용하므로 불변식이 유지된다. 따라서 마지막에는 모든 장치의 공통 주기가 정확히 구해진다.[6,7]

공통 발생 시각은 $qL$ 형태이며, 시작 시각 0을 포함하므로 $q$는 비음수 정수이다. $qL\ge T$를 $L>0$으로 나누면 $q\ge T/L$이고, 이를 만족하는 가장 작은 정수는 $\lceil T/L\rceil$이다. 앞 절에서 유도한 정수 올림식으로 `cycles_needed`를 구한다. 이 논증은 답을 찾을 뿐 아니라 그보다 작은 허용 시각이 없다는 최소성까지 보인다.[1,2,6,7]

| 조건 | 수식으로 확인한 결과 | 의미 |
| --- | --- | --- |
| $T=0$ | $t_*=0$ | 최초 동시 신호를 포함 |
| $T$가 $L$의 배수 | $t_*=T$ | 하한을 포함하는 조건 |
| 모든 주기가 1 | $t_*=T$ | 모든 정수 시각에 발생 |
| 같은 주기의 반복 | LCM 불변 | 중복 장치는 주기를 늘리지 않음 |
| 한 주기가 다른 주기를 나눔 | 큰 주기가 두 주기의 LCM | 곱 전체가 필요하지 않음 |

장치들이 처음 만난 뒤 일정 간격으로 계속 만나는 성질을 이용하면 구간 내 횟수도 유도할 수 있다. $0\le T\le U$인 닫힌 구간 $[T,U]$에서 동시 발생 횟수 $C$는 허용되는 정수 $q$의 수이다. $U$는 구간의 마지막 시각이다.[1,2,6,7]

$$
C=\max\left(0,
\left\lfloor\frac UL\right\rfloor-
\left\lceil\frac TL\right\rceil+1\right).
$$

예시의 $L=180$으로 구간 $[250,\,1000]$을 계산하면 $\lfloor1000/180\rfloor=5$, $\lceil250/180\rceil=2$이므로 $C=4$이다. 해당 시각은 360, 540, 720, 900이다. 양끝 포함 여부를 바꾸면 정수 $q$의 경계도 바꾸어야 한다.

### (4) 시작 시각이 다른 경우

장치마다 시작 offset이 다르면 LCM만으로 첫 만남을 정할 수 없다. 두 장치가 각각 시각 $u_0,v_0$에서 시작하고 주기가 $a,b$라면 공통 시각 $t$는 $t\equiv u_0\pmod a$, $t\equiv v_0\pmod b$를 만족해야 한다. 두 식을 정수 방정식으로 바꾸면 다음과 같은 호환 조건이 나온다.[7,15]

$$
t=u_0+ax=v_0+by
\quad\Longrightarrow\quad
ax-by=v_0-u_0,
\qquad \gcd(a,b)\mid(v_0-u_0).
$$

마지막 조건은 정수 해가 존재할 필요충분조건이다. 존재할 때 해들은 LCM 간격으로 반복하므로 충분히 큰 시각을 택하면 두 장치의 실제 시작 시각 이후라는 조건도 만족시킬 수 있다. 예를 들어 주기 4와 6에 offset 0과 1을 주면 차이 1을 GCD 2가 나누지 못해 만남이 없다. 같은 주기에 offset 0과 2를 주면 시각 8에서 만나며, 주기 LCM 12가 첫 시각은 아니다. 이는 Chinese remainder theorem (CRT)의 비서로소 modulus 확장과 연결되는 경계이며, 앞 함수는 이런 offset 입력을 받지 않는다.[7,15]

## 8. 연산 횟수와 큰 정수의 비용

이 절의 분석은 필요한 자릿수를 저장하는 정수 산술 모형을 사용한다. 저장할 비트가 늘면 메모리와 계산 비용도 늘어난다. 큰 정수를 여러 자리로 저장하는 산술 모형에서는 정수 하나를 처리하는 비용과 알고리즘의 반복 횟수를 구별해야 한다.[11,16]

0이 아닌 정수 $x$의 비트 길이를 $B$라 하면 다음과 같이 값의 크기와 연결된다. 여기서는 부호를 제외한 이진 자릿수를 세고, 0의 길이는 비용 모형의 별도 규약으로 1로 둔다. 다음 식은 이진 자리 표현에서 유도한 것이다.[11,16]

$$
2^{B-1}\le |x|<2^B,
\qquad B=\lfloor\log_2|x|\rfloor+1\quad(x\ne0).
$$

이 자리 표현에서 두 $B$비트 수의 학교식 덧셈은 $B$개 자리를 훑고, 학교식 곱셈은 최대 $B^2$개의 자리 쌍을 처리한다. 따라서 직접 센 기본 연산 수는 각각 $O(B)$와 $O(B^2)$이다. 이는 특정 Python 구현의 시간 보장이 아니라 산술 알고리즘의 기준 모형이다.[11,16]

다음 표는 본문의 연산 수를 읽을 때 추가로 확인해야 할 크기를 모은 것이다. 구체적인 실행 시간은 이 정보만으로 고정할 수 없다.

| 계산 | 단위 연산 기준의 작업량 | 큰 정수에서 추가로 볼 항목 |
| --- | --- | --- |
| Euclidean algorithm | 로그 수의 나머지 계산 | 각 피연산자의 비트 길이 |
| Trial division | $O(\sqrt n)$ 나머지 검사 | 입력 비트 길이에 대한 반복 증가 |
| Modular exponentiation | $O(\log e)$ 모듈러 곱셈 | modulus의 비트 길이 |
| 조합의 정확한 값 | 선택한 계산법에 의존 | 결과와 중간 정수의 크기 |
| 비트 집합 연산 | 단어 안에서는 간단한 연산 | 마스크 폭이 여러 단어로 늘어나는지 |

특히 $B$비트 양수 $n$은 대략 $2^B$ 크기이므로 $\sqrt n$까지 검사하는 방식은 비트 길이에 대해 지수적으로 증가한다. 수의 값에 대한 $O(\sqrt n)$과 입력 길이에 대한 효율성을 같은 말로 취급하지 않는다. 또한 $w$비트 마스크로 집합 하나를 짧게 표시할 수 있다는 사실은 $2^w$개 상태를 모두 방문하는 알고리즘의 지수적 증가를 없애지 않는다.[7,8,11]

대표 문제에서 장치 수를 $M$, 최대 주기를 $P$라 하면 GCD를 $M$번 호출한다. 각 주기가 $P$ 이하이므로 각 호출의 나머지 단계 수는 $O(1+\log P)$로 상계할 수 있어 전체는 $O(M(1+\log P))$회의 산술 연산으로 표현된다. 하지만 누적 `cycle`은 $P$보다 훨씬 클 수 있다. 모든 주기의 곱은 공통 배수이므로 $L\le\prod_i p_i\le P^M$이며, $P\ge2$이면 $L$의 비트 길이는 $O(M\log P)$이다. 따라서 이 연산 수에 상수 시간을 곱해 실제 Python 시간을 단정할 수 없다. 특히 큰 `cycle`을 작은 `period`로 나누는 첫 나머지 계산에도 큰 피연산자를 읽는 비용이 든다.[6,11]

이 함수는 입력 목록 외에 상수 개의 정수 변수만 유지한다. 그렇더라도 비트 단위 보조 공간은 상수가 아니다. $L$의 비트 길이와 $T$의 비트 길이 중 큰 쪽에 비례하는 중간 값을 보유해야 한다. $P=1$에서는 $L=1$이지만 $T$를 나타내는 공간은 여전히 필요하다. 입력 개수, 정수 객체 개수, 정수의 총 비트 수를 나누어 보고해야 공간 설명이 정확해진다.[11,16]

## 9. 요약

- `//`와 `%`는 floor division 규약을 공유한다. 음수·0 제수·올림 경계를 먼저 확인한다.
- GCD는 공약수 집합을 보존하는 나머지 반복이며, LCM은 양수 입력에서 `a // gcd_euclid(a, b) * b`로 구한다.
- 단일 소수 판별, 범위 전체의 체, 소인수분해는 서로 다른 결과를 제공한다. 제곱근 경계는 정확한 정수로 계산한다.
- 모듈러 역원은 서로소 조건을 요구한다. 소수 전용 지수 공식과 factorial 역원 공식을 합성수나 범위 밖 입력에 그대로 적용하지 않는다.
- 조합 수는 순서·중복의 정의에 따라 달라진다. 유한 비트 집합에는 명시한 폭이 필요하며, 큰 정수의 연산 비용은 반복 횟수와 별도로 분석한다.

## 10. 참고문헌

1. Python Software Foundation, “Built-in Types,” *Python documentation*, Numeric Types; Bitwise Operations on Integer Types. [원문](https://docs.python.org/3/library/stdtypes.html).
2. Allen B. Downey, *Think Python*, 2nd ed., Chapter 5, “Conditionals and recursion,” §5.1. [원문](https://greenteapress.com/thinkpython2/html/thinkpython2006.html).
3. NumPy Developers, “numpy.remainder,” *NumPy reference*. [원문](https://numpy.org/doc/stable/reference/generated/numpy.remainder.html).
4. Python Software Foundation, “Built-in Functions,” *Python documentation*, `divmod`. [원문](https://docs.python.org/3/library/functions.html).
5. NumPy Developers, “numpy.divmod,” *NumPy reference*. [원문](https://numpy.org/doc/stable/reference/generated/numpy.divmod.html).
6. CP-Algorithms contributors, “Euclidean algorithm for computing the greatest common divisor.” [원문](https://cp-algorithms.com/algebra/euclid-algorithm.html).
7. Antti Laaksonen, *Competitive Programmer’s Handbook*, July 3, 2018 draft, Chapters 10, 21–22. [원문](https://cses.fi/book/book.pdf).
8. CP-Algorithms contributors, “Primality tests,” Trial division. [원문](https://cp-algorithms.com/algebra/primality_tests.html).
9. CP-Algorithms contributors, “Sieve of Eratosthenes.” [원문](https://cp-algorithms.com/algebra/sieve-of-eratosthenes.html).
10. CP-Algorithms contributors, “Integer factorization,” Trial division. [원문](https://cp-algorithms.com/algebra/factorization.html).
11. Victor Shoup, *A Computational Introduction to Number Theory and Algebra*, Version 2, Chapters 2–4. [원문](https://shoup.net/ntb/ntb-v2.pdf).
12. CP-Algorithms contributors, “Binary Exponentiation.” [원문](https://cp-algorithms.com/algebra/binary-exp.html).
13. CP-Algorithms contributors, “Modular Inverse” and “Extended Euclidean Algorithm.” [역원](https://cp-algorithms.com/algebra/module-inverse.html), [계수의 유도](https://cp-algorithms.com/algebra/extended-euclid-algorithm.html).
14. CP-Algorithms contributors, “Binomial Coefficients.” [원문](https://cp-algorithms.com/combinatorics/binomial-coefficients.html).
15. CP-Algorithms contributors, “Chinese Remainder Theorem,” Solution for not coprime moduli. [원문](https://cp-algorithms.com/algebra/chinese-remainder-theorem.html).
16. GNU MP contributors, “Integer Internals,” *GNU MP Manual*. [원문](https://gmplib.org/manual/Integer-Internals).
