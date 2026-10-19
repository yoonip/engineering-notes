# 타겟 넘버

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/43165) · Level 2 · Python3

## 문제와 조건 / Task and conditions

숫자는 2~20개이고 각각 1~50입니다. target은 1~1000입니다. 모든 수를 원래 순서대로 정확히 한 번 사용하며 + 또는 −를 붙인 방법 수를 반환합니다.

There are 2–20 numbers in [1,50] and target is in [1,1000]. Use every number exactly once in order with either sign and return the number of assignments.

## 풀이 흐름 / Approach

숫자를 하나 사용할 때마다 현재 합에 더한 경우와 뺀 경우로 나눕니다. 같은 합에 도착한 경로는 Counter에 방법 수를 더해 하나의 상태로 묶습니다.

For each number, branch into adding or subtracting it. Aggregate the counts of paths that reach the same sum in a Counter.

## 정답이 되는 이유 / Why it works

i개 숫자를 처리한 합별 방법 수가 정확하다고 가정합니다. 다음 숫자에 부호를 붙인 모든 선택은 이전 상태와 두 부호 중 하나로 유일하게 분해되므로 점화식이 정확합니다.

Assume the counts after i numbers are correct. Every next choice decomposes uniquely into a previous state and one of two signs, proving the transition by induction.

## 비용 / Complexity

도달 합 상태 S개 기준 시간 O(nS), 공간 O(S); 최악 O(2ⁿ) / O(nS) time and O(S) space; exponential worst case

## 구현 / Implementation

[solution.py](solution.py)

```python
from collections import Counter

def solution(numbers, target):
    # 숫자를 사용하기 전 합 0을 만드는 방법은 1개.
    ways = Counter({0: 1})
    for number in numbers:
        # 다음 숫자까지 사용한 방법 수를 담을 빈 Counter.
        next_ways = Counter()
        for total, count in ways.items():
            # 이번 숫자를 더하는 모든 방법 누적.
            next_ways[total + number] += count
            next_ways[total - number] += count
        # =로 다음 단계의 방법 수 표로 교체.
        ways = next_ways
    return ways[target]
```

## 다른 방법: 부호 선택 DFS / Sign-assignment DFS

각 숫자의 부호를 직접 정합니다. 중복 합을 합치지 않아 시간 O(2ⁿ), 호출 공간 O(n)이며 작은 입력의 독립 기준으로 간단합니다.

Enumerate signs directly. Without merging equal sums it takes O(2ⁿ) time and O(n) recursion space and provides a simple independent reference.

[alternative.py](alternative.py)

```python
def solution(numbers, target):
    def visit(index, total):
        if index == len(numbers):
            return int(total == target)
        value = numbers[index]
        return visit(index + 1, total + value) + visit(index + 1, total - value)
    return visit(0, 0)
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    [
      1,
      1,
      1,
      1,
      1
    ],
    3
  ],
  "output": 5
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

출처: [프로그래머스 문제 43165](https://school.programmers.co.kr/learn/courses/30/lessons/43165), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 43165](https://school.programmers.co.kr/learn/courses/30/lessons/43165), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
