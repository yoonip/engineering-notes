# N개의 최소공배수

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12953) · Level 2 · Python3

## 문제와 조건 / Task and conditions

배열은 1~15개 원소로 각 값은 1~100입니다. 모든 원소의 최소공배수를 반환합니다.

The array has 1–15 integers in [1,100]. Return their least common multiple.

## 풀이 흐름 / Approach

두 수의 최소공배수 a/gcd(a,b)×b를 차례로 누적합니다. 곱한 뒤 나누기보다 먼저 나누면 중간값도 작아집니다.

Fold the identity lcm(a,b)=a/gcd(a,b)×b across the list. Dividing before multiplying keeps intermediate values smaller.

## 정답이 되는 이유 / Why it works

누적값은 앞서 처리한 모든 수의 공배수 중 가장 작습니다. 그 값과 다음 수의 최소공배수를 취하면 처리 범위 전체의 최소공배수가 되어 귀납적으로 답을 얻습니다.

The accumulator is the least common multiple of all processed values. Taking its LCM with the next value preserves this invariant for the extended prefix.

## 비용 / Complexity

정수 연산 횟수 기준 O(n log V), 공간 O(1); 큰 정수 비용 별도 / O(n log V) arithmetic-operation bound, O(1) accumulators

## 구현 / Implementation

[solution.py](solution.py)

```python
from math import gcd

def solution(arr):
    answer = 1
    # 모든 수를 순회.
    for number in arr:
        answer = answer // gcd(answer, number) * number
    return answer
```

## 다른 방법: 소인수 지수의 최댓값 / Maximum prime-factor exponents

각 수를 소인수분해하고 소수별로 가장 큰 지수를 모아 곱합니다. 최대공약수 공식과 다른 방식으로 최소공배수의 정의를 확인할 수 있습니다.

Factor each number and retain the maximum exponent per prime. Multiplying them gives an independent construction from the prime-factor definition.

[alternative.py](alternative.py)

```python
def solution(arr):
    maximum = {}
    for value in arr:
        factor = 2
        while factor * factor <= value:
            exponent = 0
            while value % factor == 0:
                value //= factor
                exponent += 1
            maximum[factor] = max(maximum.get(factor, 0), exponent)
            factor += 1
        if value > 1:
            maximum[value] = max(maximum.get(value, 0), 1)
    result = 1
    for prime, exponent in maximum.items():
        result *= prime ** exponent
    return result
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    [
      2,
      6,
      8,
      14
    ]
  ],
  "output": 168
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 30개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 30 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 30개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 30 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 12953](https://school.programmers.co.kr/learn/courses/30/lessons/12953), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 12953](https://school.programmers.co.kr/learn/courses/30/lessons/12953), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
