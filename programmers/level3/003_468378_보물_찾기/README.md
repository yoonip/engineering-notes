# 보물 찾기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/468378) · Level 3 · Python3

## 문제와 조건 / Task and conditions

열은 2~200개, 깊이는 1~100000입니다. money는 깊이 합 이하이며 확실히 찾는 최소 비용 이상으로 보장됩니다. excavate(1기반 열)는 찾으면 0, 왼쪽이면 −1, 오른쪽이면 1을 반환합니다. 예산 안에서 정답 열을 반환합니다.

There are 2–200 columns with depths 1–100000. money is at most the depth sum and at least the optimal guaranteed cost. excavate(one-based column) returns 0 for found, −1 for left, +1 for right. Return the treasure column within budget.

## 풀이 흐름 / Approach

구간 안에서 어느 열을 먼저 파더라도 그 열의 깊이 비용을 먼저 냅니다. 보물이 왼쪽·오른쪽 어느 쪽에 있어도 찾아야 하므로 둘 중 더 큰 잔여 비용을 더합니다. 이 최악 비용이 가장 작은 열을 구간 DP로 선택합니다.

Choosing a column first always pays its excavation cost. Since the treasure may lie on either side, add the larger remaining cost. Interval DP selects the pivot minimizing this worst-case expense.

## 정답이 되는 이유 / Why it works

구간 [l,r)의 최적 보장 비용은 min_p(depth[p]+max(dp[l,p],dp[p+1,r]))입니다. 두 응답 구간은 더 짧으므로 길이순 DP가 최적 전략을 만듭니다. 주어진 예산은 이 보장 비용 이상입니다.

The optimal guaranteed cost on [l,r) is min_p(depth[p]+max(dp[l,p],dp[p+1,r])). Shorter subintervals establish the optimal strategy inductively; the supplied budget is at least this guaranteed cost.

## 비용 / Complexity

열 w개에 시간 O(w³), 공간 O(w²) / O(w³) time, O(w²) space

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(depth, money, excavate):
    # 전체 열 수.
    n = len(depth)
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    # 구간마다 먼저 굴착할 최적의 열 번호 저장.
    choice = [[0] * (n + 1) for _ in range(n)]
    for size in range(1, n + 1):
        # 구간의 왼쪽 끝을 순회하는 for 반복.
        for left in range(n - size + 1):
            right = left + size
            # 최소값 비교의 초기값.
            best = float('inf')
            for middle in range(left, right):
                # 현재 비용에 왼쪽·오른쪽 중 최악의 추가 비용을 더함.
                cost = depth[middle] + max(dp[left][middle], dp[middle + 1][right])
                if cost < best:
                    best = cost
                    # 이 구간의 최적 첫 굴착 위치 저장.
                    choice[left][right] = middle
            dp[left][right] = best
    # 처음에는 전체 열이 후보.
    left, right = 0, n
    while left < right:
        # 미리 구한 최적 전략에서 굴착할 열을 선택.
        middle = choice[left][right]
        result = excavate(middle + 1)
        # 0이면 실제 보물을 발굴한 상태.
        if result == 0:
            return middle + 1
        if result < 0:
            # 현재 열을 제외한 왼쪽 구간으로 축소.
            right = middle
        else:
            left = middle + 1
    return 0
```

## 다른 방법: 예산 충족 여부 탐색 / Budget-feasibility search

각 구간을 남은 예산으로 반드시 찾을 수 있는지 검사합니다. 가능한 열을 찾으면 그 열의 양쪽 응답 모두 같은 잔여 예산 안에 들어야 합니다. 예산 상태가 커져 작은 입력 전략 검증용입니다.

Ask whether an interval can always be searched within a remaining budget. A feasible pivot must leave both possible response intervals solvable with that same reduced budget. The extra budget state makes this a small-input strategy oracle.

[alternative_reference.py](alternative_reference.py)

```python
from functools import lru_cache

def solution(depth, money, excavate):
    @lru_cache(None)
    def pivot(left, right, budget):
        if left == right:
            return -2
        for middle in range(left, right):
            rest = budget - depth[middle]
            if rest >= 0 and pivot(left, middle, rest) != -1 and pivot(middle + 1, right, rest) != -1:
                return middle
        return -1
    left, right, budget = 0, len(depth), money
    while left < right:
        middle = pivot(left, right, budget)
        if middle < 0:
            raise ValueError('주어진 예산으로 보장할 수 없는 입력입니다.')
        budget -= depth[middle]
        response = excavate(middle + 1)
        if response == 0:
            return middle + 1
        if response < 0:
            right = middle
        else:
            left = middle + 1
    return 0
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    [
      1,
      2,
      3,
      4,
      5,
      6,
      7,
      8,
      9,
      10
    ],
    55
  ],
  "output": 3
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 34개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 34 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 34개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 34 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 468378](https://school.programmers.co.kr/learn/courses/30/lessons/468378), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 468378](https://school.programmers.co.kr/learn/courses/30/lessons/468378), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
