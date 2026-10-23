# 구명보트

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/42885) · Level 2 · Python3

## 문제와 조건 / Task and conditions

사람은 1~50000명, 무게·한도는 40~240입니다. 보트에는 최대 2명만 탈 수 있고 각 개인은 한도 이내입니다. 필요한 최소 보트 수를 반환합니다.

There are 1–50000 people; weights and capacity are in [40,240]. Each boat carries at most two people and each person individually fits. Return the minimum boat count.

## 풀이 흐름 / Approach

몸무게를 정렬한 뒤 가장 무거운 사람을 반드시 태웁니다. 가장 가벼운 사람과 함께 탈 수 있으면 둘을 태우고, 그렇지 않으면 무거운 사람만 태웁니다.

Sort weights and always place the heaviest remaining person. Pair them with the lightest when possible; otherwise send the heaviest alone.

## 정답이 되는 이유 / Why it works

가장 가벼운 사람과도 한도를 넘으면 무거운 사람은 누구와도 함께 탈 수 없습니다. 함께 탈 수 있으면 가벼운 사람과 짝지어도 다른 최적 해의 짝을 교환해 보트 수를 늘리지 않을 수 있습니다.

If the lightest cannot accompany the heaviest, nobody can. Otherwise an exchange of partners preserves feasibility and does not increase the number of boats, justifying the greedy pairing.

## 비용 / Complexity

정렬 시간 O(n log n), Python 정렬 보조 공간 O(n) / O(n log n) time, O(n) sorting workspace

## 구현 / Implementation

이 구현은 입력 배열을 제자리에서 정렬하거나 힙으로 바꿉니다.

This implementation sorts or heapifies the input array in place.

[solution.py](solution.py)

```python
def solution(people, limit):
    # sort는 리스트를 제자리 오름차순 정렬.
    people.sort()
    left, right = 0, len(people) - 1
    answer = 0
    # 남은 사람이 있는 동안 진행.
    while left <= right:
        if left < right and people[left] + people[right] <= limit:
            left += 1
        right -= 1
        answer += 1
    return answer
```

## 다른 방법: 부분집합 최적 매칭 / Subset matching reference

아직 구조하지 않은 한 사람을 혼자 또는 가능한 상대와 함께 태우는 모든 경우를 메모이제이션합니다. 시간 O(n²2ⁿ) 상한이라 작은 입력 최적값 대조용입니다.

Memoize all choices of sending a remaining person alone or with a feasible partner. The O(n²2ⁿ) upper bound makes this a small-input optimality oracle.

[alternative_reference.py](alternative_reference.py)

```python
from functools import lru_cache

def solution(people, limit):
    @lru_cache(None)
    def boats(mask):
        if not mask:
            return 0
        bit = mask & -mask
        i = bit.bit_length() - 1
        rest = mask ^ bit
        best = 1 + boats(rest)
        for j in range(i + 1, len(people)):
            if rest >> j & 1 and people[i] + people[j] <= limit:
                best = min(best, 1 + boats(rest ^ (1 << j)))
        return best
    return boats((1 << len(people)) - 1)
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    [
      70,
      50,
      80,
      50
    ],
    100
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

출처: [프로그래머스 문제 42885](https://school.programmers.co.kr/learn/courses/30/lessons/42885), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 42885](https://school.programmers.co.kr/learn/courses/30/lessons/42885), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
