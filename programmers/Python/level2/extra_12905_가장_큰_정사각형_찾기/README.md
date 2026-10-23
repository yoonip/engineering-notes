# 가장 큰 정사각형 찾기

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12905) · Level 2 · Python3

## 문제와 조건 / Task and conditions

행·열은 각각 1~1000, 값은 0 또는 1입니다. 1로만 채운 가장 큰 정사각형의 변 길이가 아닌 넓이를 반환합니다.

Both dimensions are 1–1000 and cells are binary. Return the area, not the side length, of the largest all-one square.

## 풀이 흐름 / Approach

현재 칸을 오른쪽 아래 꼭짓점으로 하는 정사각형의 최대 변 길이를 구합니다. 값이 1이면 위·왼쪽·왼쪽 위의 세 길이 중 최솟값에 1을 더합니다. 한 행 DP와 이전 대각선 값만 보관합니다.

Compute the largest all-one square ending at each bottom-right corner. At a one cell, add one to the minimum of the top, left and top-left sizes. Store one DP row and the old diagonal.

## 정답이 되는 이유 / Why it works

변 길이 s의 정사각형을 늘리려면 세 인접 방향 모두 최소 s−1 크기를 갖춰야 합니다. 가장 작은 방향이 한계이며 현재 칸이 1이면 그 최소 크기를 실제로 함께 확장할 수 있습니다.

Extending a square of side s requires all three neighbors to support side s−1. The smallest neighbor is the limiting bound, and a one cell permits that bound to be achieved.

## 비용 / Complexity

행 r, 열 c에 시간 O(rc), 공간 O(c) / O(rc) time, O(c) space

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(board):
    # 0번은 경계용.
    dp = [0] * (len(board[0]) + 1)
    best = 0
    for row in board:
        diagonal = 0
        # 경계용 칸 다음부터 계산.
        for col, value in enumerate(row, 1):
            above = dp[col]
            if value:
                # 위·왼쪽·왼쪽 위 세 정사각형 중 가장 작은 변에 현재 칸을 붙임.
                dp[col] = min(above, dp[col - 1], diagonal) + 1
                if dp[col] > best:
                    # 새 최댓값 저장.
                    best = dp[col]
            else:
                dp[col] = 0
            diagonal = above
    return best * best
```

## 다른 방법: 2차원 누적합과 변 길이 탐색 / Prefix sums and square-size search

누적합으로 각 후보 정사각형의 1 개수를 O(1)에 확인합니다. 시간 O(rc·min(r,c))의 작은 입력 기준이며 DP 점화식과 독립적입니다.

A two-dimensional prefix sum checks a square’s one count in O(1). The O(rc·min(r,c)) method is an independent small-input oracle.

[alternative_reference.py](alternative_reference.py)

```python
def solution(board):
    rows, cols = len(board), len(board[0])
    prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
    for r in range(rows):
        for c in range(cols):
            prefix[r + 1][c + 1] = board[r][c] + prefix[r][c + 1] + prefix[r + 1][c] - prefix[r][c]
    for side in range(min(rows, cols), 0, -1):
        for r in range(rows - side + 1):
            for c in range(cols - side + 1):
                count = prefix[r + side][c + side] - prefix[r][c + side] - prefix[r + side][c] + prefix[r][c]
                if count == side * side:
                    return side * side
    return 0
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    [
      [
        0,
        1,
        1,
        1
      ],
      [
        1,
        1,
        1,
        1
      ],
      [
        1,
        1,
        1,
        1
      ],
      [
        0,
        0,
        1,
        0
      ]
    ]
  ],
  "output": 9
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

출처: [프로그래머스 문제 12905](https://school.programmers.co.kr/learn/courses/30/lessons/12905), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 12905](https://school.programmers.co.kr/learn/courses/30/lessons/12905), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

큰 입력 검사: 1000×1000 정사각형 / All-one 1000×1000 board

```bash
python verify_stress.py
```
