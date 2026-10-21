# 주식가격

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/42584) · Level 2 · Python3

## 문제와 조건 / Task and conditions

가격은 2~100000개, 각 값은 1~10000입니다. 이후 처음 더 낮아질 때까지의 초를 구하며 끝까지 떨어지지 않으면 마지막 시점까지 셉니다. 같은 가격은 하락이 아닙니다.

There are 2–100000 prices in [1,10000]. Count seconds until the first lower price, or until the end if none occurs. Equal prices are not drops.

## 풀이 흐름 / Approach

아직 가격이 떨어지는 시점을 못 찾은 인덱스를 스택에 둡니다. 현재 가격이 더 낮으면 해당 인덱스의 기다린 시간을 확정합니다. 끝까지 남은 것은 마지막 시점까지 떨어지지 않은 가격입니다.

Keep indices whose first price drop is still unknown in a stack. A lower current price resolves those entries; unresolved indices last until the final time.

## 정답이 되는 이유 / Why it works

스택에 남아 있던 가격은 그 이후 지금 전까지 더 낮은 값을 만나지 않았습니다. 따라서 처음 작아진 현재 인덱스가 정확한 종료 시점입니다. 각 인덱스는 한 번 들어가고 한 번 이하로 나옵니다.

A stack entry has not encountered a lower value before the current index, so the current lower value is its first drop. Every index is pushed once and popped at most once.

## 비용 / Complexity

시간 O(n), 공간 O(n) / Time O(n), space O(n)

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(prices):
    # =는 대입.
    n = len(prices)
    answer = [n - index - 1 for index in range(n)]
    stack = []
    # 현재 시점·가격 언패킹.
    for index, price in enumerate(prices):
        while stack and prices[stack[-1]] > price:
            # pop으로 하락 시점이 확정된 인덱스를 꺼내 삭제.
            previous = stack.pop()
            answer[previous] = index - previous
        # append로 현재 시점을 대기 스택에 추가.
        stack.append(index)
    return answer
```

## 다른 방법: 각 가격에서 앞으로 순회 / Forward scan from each price

각 시점에서 가격이 처음 떨어질 때까지 셉니다. 시간 O(n²)지만 스택의 경계 처리와 같은 가격 처리를 독립적으로 확인하기 쉽습니다.

Scan forward from each timestamp until the first lower price. The O(n²) method is useful for independently checking boundaries and equal prices.

[alternative_reference.py](alternative_reference.py)

```python
def solution(prices):
    result = []
    for i, price in enumerate(prices):
        duration = 0
        for following in prices[i + 1:]:
            duration += 1
            if following < price:
                break
        result.append(duration)
    return result
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
      2,
      3
    ]
  ],
  "output": [
    4,
    3,
    1,
    1,
    0
  ]
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 29개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 29 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 29개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 29 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 42584](https://school.programmers.co.kr/learn/courses/30/lessons/42584), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 42584](https://school.programmers.co.kr/learn/courses/30/lessons/42584), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

큰 입력 검사: 범위 안의 비증가 가격 10만 개 / One hundred thousand nonincreasing prices within bounds

```bash
python verify_stress.py
```
