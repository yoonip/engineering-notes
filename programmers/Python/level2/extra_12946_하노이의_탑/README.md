# 하노이의 탑

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12946) · Level 2 · Python3

## 문제와 조건 / Task and conditions

원판 수는 1~15입니다. 작은 원판 위에 큰 원판을 놓지 않으며 1번에서 3번 기둥으로 옮기는 최소 이동 [출발,도착] 목록을 반환합니다.

There are 1–15 disks. Never place a larger disk on a smaller one. Return a minimum move list [source,target] transferring the stack from peg 1 to peg 3.

## 풀이 흐름 / Approach

큰 원판을 옮기려면 위의 n−1개를 보조 기둥으로 옮겨야 합니다. 큰 원판 하나를 목적지로 옮긴 뒤 보조 기둥의 원판들을 그 위로 옮깁니다.

Move the top n−1 disks to the spare peg, move the largest disk to the target, then move the smaller disks onto it.

## 정답이 되는 이유 / Why it works

가장 큰 원판의 이동 전후에는 n−1개 원판을 각각 옮겨야 하므로 T(n)≥2T(n−1)+1입니다. 재귀 방식은 그 하한을 달성하여 정확히 2ⁿ−1번 이동합니다.

Moving the largest disk requires transferring n−1 disks both before and after it, so T(n)≥2T(n−1)+1. The recursive construction attains this bound with 2ⁿ−1 moves.

## 비용 / Complexity

시간·출력 공간 O(2ⁿ), 호출 공간 O(n) / O(2ⁿ) time and output space, O(n) recursion space

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(n):
    answer = []
    def move(count, start, goal, spare):
        # 옮길 원판이 없으면 재귀 종료.
        if count == 0:
            return
        move(count - 1, start, spare, goal)
        # 가장 큰 원판 하나를 목적지로 이동.
        answer.append([start, goal])
        move(count - 1, spare, goal, start)
    # 원판 n개를 1번에서 3번으로 옮기고 2번을 보조로 사용.
    move(n, 1, 3, 2)
    return answer
```

## 다른 방법: 원판 이동 주기의 반복 구현 / Iterative disk-move schedule

이동 번호의 가장 낮은 1비트가 움직일 원판을 알려줍니다. 원판마다 일정한 방향으로 한 칸씩 순환해 재귀 없이 같은 최단 이동을 생성합니다.

The lowest set bit of the move number identifies the disk to move. Each disk cycles in a fixed direction, producing the same minimal schedule without recursion.

[alternative.py](alternative.py)

```python
def solution(n):
    pegs = [0] * (n + 1)
    answer = []
    for step in range(1, 1 << n):
        disk = (step & -step).bit_length()
        direction = -1 if (n + disk) % 2 == 0 else 1
        start = pegs[disk]
        pegs[disk] = (start + direction) % 3
        answer.append([start + 1, pegs[disk] + 1])
    return answer
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    2
  ],
  "output": [
    [
      1,
      2
    ],
    [
      1,
      3
    ],
    [
      2,
      3
    ]
  ]
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 13개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 13 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 13개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 13 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 12946](https://school.programmers.co.kr/learn/courses/30/lessons/12946), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 12946](https://school.programmers.co.kr/learn/courses/30/lessons/12946), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
