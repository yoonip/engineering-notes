# 숫자 카드 나누기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/135807) · Level 2 · Python3

한 배열의 모든 수를 나누고 다른 배열의 어떤 수도 나누지 않는 최대 양의 정수를 찾는다.

## 조건과 입출력

입력 매개변수: `arrayA, arrayB`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과다.

- 1 ≤ arrayA의 길이 = arrayB의 길이 ≤ 500,000
- 1 ≤ arrayA의 원소, arrayB의 원소 ≤ 100,000,000

## 풀이를 따라가기

각 배열의 최대공약수 g를 구한다. g가 반대 배열 중 하나라도 나누면 그 방향의 후보를 0으로 버린다. 두 방향의 후보 중 큰 값을 반환한다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
from math import gcd
from functools import reduce

def solution(arrayA, arrayB):
    # 한쪽 모든 수를 나눌 수 있는 가장 큰 후보는 최대공약수다.
    a = reduce(gcd, arrayA)
    b = reduce(gcd, arrayB)
    # 반대쪽 하나라도 나누면 이 최대공약수의 약수도 모두 탈락한다.
    if any(value % a == 0 for value in arrayB):
        a = 0
    if any(value % b == 0 for value in arrayA):
        b = 0
    return max(a, b)
```

## 왜 맞는가

한 배열의 공약수는 최대공약수의 약수다. 최대공약수가 반대 원소를 나누면 그 약수도 같은 원소를 나누므로 더 작은 후보를 볼 필요가 없다.

시간 O(N log V), 공간 O(1) / Time O(N log V), space O(1)

주의할 점: 다른 배열 전체를 나누지 않는 것만으로는 부족하고 어느 원소도 나누면 안 된다. 가능한 후보가 없으면 0이다.

## 다른 방법: 첫 원소의 약수 열거

```python
from math import isqrt

def solution(arrayA,arrayB):
    best=0
    for own,other in ((arrayA,arrayB),(arrayB,arrayA)):
        candidates=set()
        for d in range(1,isqrt(own[0])+1):
            if own[0]%d==0: candidates.update((d,own[0]//d))
        for d in sorted(candidates,reverse=True):
            if d<=best: break
            if all(x%d==0 for x in own) and all(x%d for x in other):
                best=d
                break
    return best
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 각 배열의 최대공약수 g를 구한다. g가 반대 배열 중 하나라도 나누면 그 방향의 후보를 0으로 버린다. 두 방향의 후보 중 큰 값을 반환한다. | 첫 원소의 약수 열거 |
| 비용 | 시간 O(N log V), 공간 O(1) / Time O(N log V), space O(1) | 시간 O(sqrt(V)+N·τ(V)), 공간 O(τ(V)) / Time O(sqrt(V)+N·τ(V)), space O(τ(V)); τ=약수 수 / divisor count |

## 검증

공식 예제 3개와 생성 입력 80개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Find the largest positive integer dividing every value in one array and none in the other.

### Conditions and input/output

Input arguments: `arrayA, arrayB`. The return value is an integer satisfying the task described below.

- 1 ≤ len(arrayA)=len(arrayB) ≤ 500000
- 1 ≤ each value ≤ 100000000; duplicate values allowed

### Approach

Compute each array’s gcd. Reject a gcd if it divides any value in the opposite array, then return the larger remaining candidate.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Every common divisor divides the gcd. If the gcd divides an opposite-array value, every smaller candidate divisor also divides that value, so none can work.

시간 O(N log V), 공간 O(1) / Time O(N log V), space O(1)

Boundary cases: The candidate must divide no value in the opposite array, not merely fail to divide all of them. Return zero if neither direction works.

### Alternative: Enumerate divisors of the first element

시간 O(sqrt(V)+N·τ(V)), 공간 O(τ(V)) / Time O(sqrt(V)+N·τ(V)), space O(τ(V)); τ=약수 수 / divisor count

### Verification

Local checks covered 3 official examples and 80 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 숫자 카드 나누기](https://school.programmers.co.kr/learn/courses/30/lessons/135807) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
