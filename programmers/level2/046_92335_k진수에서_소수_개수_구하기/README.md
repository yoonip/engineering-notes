# k진수에서 소수 개수 구하기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/92335) · Level 2 · Python3

n을 k진수로 바꿔 0으로 구분된 조각을 십진수로 읽고 소수 조각 수를 센다.

## 조건과 입출력

입력 매개변수: `n, k`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과다.

- 1 ≤ n ≤ 1,000,000
- 3 ≤ k ≤ 10

## 풀이를 따라가기

divmod로 진수 표현을 만든다. 0으로 나눠 빈 조각을 버린다. 2는 소수로, 그보다 큰 홀수는 제곱근 이하 홀수 약수가 없는지 확인한다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
from math import isqrt

def solution(n, k):
    digits = ''
    while n:
        n, remainder = divmod(n, k)
        digits = str(remainder) + digits
    answer = 0
    # 0으로 분리한 숫자는 십진수로 읽는다.
    for piece in digits.split('0'):
        if not piece:
            continue
        value = int(piece)
        if value == 2:
            answer += 1
        # 2 이외의 짝수와 1을 제외하고 제곱근까지 약수를 확인한다.
        elif value > 2 and value % 2 and all(value % divisor for divisor in range(3, isqrt(value) + 1, 2)):
            answer += 1
    return answer
```

## 왜 맞는가

약수가 있는 합성수는 제곱근 이하의 약수를 반드시 가진다. 0으로 구분된 최대 조각이 문제에서 세는 후보와 일치하므로 각 조각의 소수 여부만 보면 된다.

시간 O(L²+Σsqrt(P)), 공간 O(L) / Time O(L²+Σsqrt(P)), space O(L); L=진수 표현 길이, P=조각의 십진수 값 / digit length and decimal token values

주의할 점: 조각은 k진수가 아니라 십진수로 읽는다. 1은 소수가 아니며 연속 0 사이 빈 문자열을 무시한다.

## 다른 방법: 체로 소수 약수를 먼저 준비

기본 풀이와 같은 결과를 구하되 중간 상태와 계산 방식이 다르다.

```python
from math import isqrt

def solution(n,k):
    digits=[]
    while n:
        n,d=divmod(n,k)
        digits.append(str(d))
    values=[int(s) for s in ''.join(reversed(digits)).split('0') if s]
    bound=isqrt(max(values,default=1))
    sieve=bytearray([1])*(bound+1)
    if bound>=0: sieve[0]=0
    if bound>=1: sieve[1]=0
    for p in range(2,isqrt(bound)+1):
        if sieve[p]:
            for multiple in range(p*p,bound+1,p): sieve[multiple]=0
    primes=[p for p in range(2,bound+1) if sieve[p]]
    answer=0
    for value in values:
        if value<2: continue
        for p in primes:
            if p*p>value: break
            if value%p==0: break
        else:
            answer+=1
            continue
        if p*p>value: answer+=1
    return answer
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | divmod로 진수 표현을 만든다. 0으로 나눠 빈 조각을 버린다. 2는 소수로, 그보다 큰 홀수는 제곱근 이하 홀수 약수가 없는지 확인한다. | 체로 소수 약수를 먼저 준비 |
| 비용 | 시간 O(L²+Σsqrt(P)), 공간 O(L) / Time O(L²+Σsqrt(P)), space O(L); L=진수 표현 길이, P=조각의 십진수 값 / digit length and decimal token values | 시간 O(sqrt(M) log log M+Σπ(sqrt(P))), 공간 O(sqrt(M)) / Time O(sqrt(M) log log M+Σπ(sqrt(P))), space O(sqrt(M)); M=최대 조각 / largest token |

## 검증

공식 예제 2개와 생성 입력 60개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Convert n to base k, split at zeros, interpret each token as decimal and count prime tokens.

### Conditions and input/output

Input arguments: `n, k`. The return value is an integer satisfying the task described below.

- 1 ≤ n ≤ 1000000; 3 ≤ k ≤ 10; zero-separated tokens are read as decimal

### Approach

Build base-k digits using divmod and split at zeros. Ignore empty tokens; accept two and test larger odd values for divisors up to their square root.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Every composite has a divisor no larger than its square root. Maximal zero-separated tokens are exactly the candidates specified by the problem.

시간 O(L²+Σsqrt(P)), 공간 O(L) / Time O(L²+Σsqrt(P)), space O(L); L=진수 표현 길이, P=조각의 십진수 값 / digit length and decimal token values

Boundary cases: Read tokens in decimal, not base k. One is not prime, and consecutive zeros create ignored empty tokens.

### Alternative: Sieve prime trial divisors once

It computes the same result using different intermediate states or evaluation steps. 시간 O(sqrt(M) log log M+Σπ(sqrt(P))), 공간 O(sqrt(M)) / Time O(sqrt(M) log log M+Σπ(sqrt(P))), space O(sqrt(M)); M=최대 조각 / largest token

The main approach follows the steps described above. The alternative uses sieve prime trial divisors once; compare its intermediate state and cost with the main implementation before choosing it.

### Verification

Local checks covered 2 official examples and 60 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: k진수에서 소수 개수 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/92335) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
