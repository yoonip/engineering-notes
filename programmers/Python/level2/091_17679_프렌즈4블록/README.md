# [1차] 프렌즈4블록

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/17679) · Level 2 · Python3

## 문제와 조건 / Task and conditions

판의 각 변은 2~30입니다. 같은 문자 2×2들을 한꺼번에 지우고 중력으로 내린 뒤 반복하며 삭제된 칸 수를 반환합니다.

Both board dimensions are 2–30. Simultaneously remove all equal-letter 2×2 blocks, apply gravity and repeat. Return the total removed cells.

## 풀이 흐름 / Approach

한 단계에서 지울 2×2 블록의 좌표를 먼저 모두 모읍니다. 찾자마자 지우면 겹친 블록을 놓칠 수 있습니다. 한꺼번에 지운 뒤 각 열의 남은 문자를 아래로 모으는 과정을 반복합니다.

Collect every matching 2×2 block before deleting anything, since immediate deletion could miss overlaps. Remove them simultaneously, compact each column downward and repeat.

## 정답이 되는 이유 / Why it works

현재 판에서 지워야 할 칸의 합집합을 정확히 모아 중복 없이 셉니다. 열별 압축은 남은 블록의 위아래 순서를 유지하므로 중력 규칙과 같습니다. 지울 칸이 없으면 종료 상태입니다.

The collected union counts every removed cell once. Column compaction preserves the vertical order of survivors and therefore implements gravity. No marked cells means the fixed point is reached.

## 비용 / Complexity

제거 단계 R에 시간 O(Rmn), 공간 O(mn); R≤mn/4 / O(Rmn) time, O(mn) space; R≤mn/4

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(m, n, board):
    # 리스트 내포와 list로 문자열 행을 수정 가능한 문자 목록으로 변환.
    board = [list(row) for row in board]
    answer = 0
    while True:
        removed = set()
        # 2×2의 왼쪽 위 행 순회.
        for r in range(m - 1):
            for c in range(n - 1):
                # 빈칸은 거짓이라 제외.
                if board[r][c] and board[r][c] == board[r + 1][c] == board[r][c + 1] == board[r + 1][c + 1]:
                    removed.update(((r, c), (r + 1, c), (r, c + 1), (r + 1, c + 1)))
        # 제거할 좌표 집합이 비면 종료.
        if not removed:
            return answer
        answer += len(removed)
        # 좌표 튜플을 언패킹하며 순회.
        for r, c in removed:
            board[r][c] = ''
        # 중력 처리를 위해 열별 순회.
        for c in range(n):
            remaining = [board[r][c] for r in range(m) if board[r][c]]
            # 위는 빈칸, 아래는 남은 블록으로 구성.
            column = [''] * (m - len(remaining)) + remaining
            for r, value in enumerate(column):
                # 다시 2×2 검색으로 돌아감.
                board[r][c] = value
```

## 다른 방법: 열 중심 좌표와 한 칸씩 낙하 / Column-major board with stepwise falling

판을 열 목록으로 저장하고 빈칸 위 블록을 한 칸씩 떨어뜨립니다. 열을 한 번에 압축하는 풀이보다 느리지만 낙하 규칙 자체로 결과를 대조할 수 있습니다.

Use a column-major board and drop blocks into empty cells one step at a time. It is slower than compaction but independently follows the falling rule.

[alternative.py](alternative.py)

```python
def solution(m, n, board):
    columns = [[board[r][c] for r in range(m)] for c in range(n)]
    answer = 0
    while True:
        marked = set()
        for c in range(n - 1):
            for r in range(m - 1):
                value = columns[c][r]
                if value and value == columns[c + 1][r] == columns[c][r + 1] == columns[c + 1][r + 1]:
                    marked.update(((c, r), (c + 1, r), (c, r + 1), (c + 1, r + 1)))
        if not marked:
            return answer
        answer += len(marked)
        for c, r in marked:
            columns[c][r] = ''
        for column in columns:
            for _ in range(m):
                for r in range(m - 1, 0, -1):
                    if not column[r] and column[r - 1]:
                        column[r], column[r - 1] = column[r - 1], ''
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    4,
    5,
    [
      "CCBDE",
      "AAADE",
      "AAABF",
      "CCBBF"
    ]
  ],
  "output": 14
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

출처: [프로그래머스 문제 17679](https://school.programmers.co.kr/learn/courses/30/lessons/17679), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 17679](https://school.programmers.co.kr/learn/courses/30/lessons/17679), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
