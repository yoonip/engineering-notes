# 소수 찾기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/42839) · Level 2 · Python3

## 문제와 조건 / Task and conditions

숫자 조각 문자열 길이는 1~7입니다. 조각 일부 또는 전부를 각 한 번씩 사용해 만들 수 있는 서로 다른 소수 수를 반환합니다. 앞의 0은 같은 정수로 합쳐집니다.

The digit-piece string has length 1–7. Use any nonempty subset of pieces once each and count distinct primes. Leading zeros do not distinguish integers.

## 풀이 흐름 / Approach

종이 조각으로 만들 수 있는 모든 길이의 순열을 정수로 바꿔 집합에 넣습니다. 같은 숫자가 여러 번 나오거나 앞에 0이 붙어도 한 숫자로 셉니다. 각 수는 제곱근까지만 나누어 봅니다.

Generate permutations of every length, convert them to integers and deduplicate them. Repeated digits and leading zeros must not count a number twice. Test primality using divisors up to the square root.

## 정답이 되는 이유 / Why it works

모든 가능한 조각 선택·배열은 어느 길이의 순열에 포함됩니다. 합성수에는 제곱근 이하의 약수가 하나 이상 있으므로 그 범위에서 나누어지지 않는 2 이상의 수만 소수입니다.

Every valid arrangement appears in a permutation of some length. A composite integer has a divisor no larger than its square root, so this divisor test correctly recognizes primes.

## 비용 / Complexity

서로 다른 후보 P개, 최댓값 V에 O(n!·n+P√V), 공간 O(Pn) 상한 / O(n!n+P√V) time, conservative O(Pn) space

## 구현 / Implementation

[solution.py](solution.py)

```python
from itertools import permutations
from math import isqrt

def solution(numbers):
    # 조각으로 만든 정수 후보 저장.
    candidates = set()
    for size in range(1, len(numbers) + 1):
        # 선행 0·중복 순열은 집합에서 통합.
        candidates.update(int(''.join(parts)) for parts in permutations(numbers, size))
    answer = 0
    for value in candidates:
        # all로 제곱근 이하 약수가 없는지 검사.
        if value >= 2 and all(value % divisor for divisor in range(2, isqrt(value) + 1)):
            answer += 1
    return answer
```

## 다른 방법: 에라토스테네스의 체 / Sieve of Eratosthenes

최대 후보까지 소수 표를 한 번 만듭니다. 후보별 나눗셈 대신 표를 조회하므로 후보가 많을 때 유리하지만 O(V) 메모리가 필요합니다.

Build a prime table up to the largest candidate. This replaces repeated division with table lookups but requires O(V) memory.

[alternative.py](alternative.py)

```python
from itertools import permutations
from math import isqrt

def solution(numbers):
    values = {int(''.join(p)) for length in range(1, len(numbers) + 1)
              for p in permutations(numbers, length)}
    maximum = max(values)
    prime = bytearray(b'\x01') * (maximum + 1)
    prime[:min(2, len(prime))] = b'\x00' * min(2, len(prime))
    for p in range(2, isqrt(maximum) + 1):
        if prime[p]:
            prime[p * p:maximum + 1:p] = b'\x00' * ((maximum - p * p) // p + 1)
    return sum(prime[value] for value in values)
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    "17"
  ],
  "output": 3
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

출처: [프로그래머스 문제 42839](https://school.programmers.co.kr/learn/courses/30/lessons/42839), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 42839](https://school.programmers.co.kr/learn/courses/30/lessons/42839), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
