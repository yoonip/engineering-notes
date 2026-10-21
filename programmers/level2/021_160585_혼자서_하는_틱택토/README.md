# 혼자서 하는 틱택토

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/160585) · Level 2 · Python3

선공 O와 후공 X가 규칙대로 두어 만들 수 있는 틱택토 상태인지 확인합니다.

## 조건과 입출력

입력 매개변수: `board`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과입니다.



## 풀이를 따라가기

O와 X의 개수 차이를 확인합니다. 가로·세로·대각선 승리 여부를 구합니다. O가 이겼으면 O가 하나 많아야 하고 X가 이겼으면 개수가 같아야 합니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(board):
    text = ''.join(board)
    o, x = text.count('O'), text.count('X')
    # 선공 개수는 후공과 같거나 하나 많아야 한다.
    if o not in (x, x + 1):
        return 0
    lines = list(board)
    for c in range(3):
        lines.append(''.join(board[r][c] for r in range(3)))
    lines.append(''.join(board[i][i] for i in range(3)))
    lines.append(''.join(board[i][2 - i] for i in range(3)))
    o_win, x_win = 'OOO' in lines, 'XXX' in lines
    # 게임은 첫 승리에서 끝나므로 동시 승자는 불가능하다.
    if o_win and x_win:
        return 0
    if o_win and o != x + 1:
        return 0
    # 후공이 마지막에 이겼다면 두 사람의 수가 같다.
    if x_win and o != x:
        return 0
    return 1
```

## 정답이 되는 이유

정상 진행에서 개수 차이는 0 또는 1입니다. 승리는 마지막 수를 둔 쪽만 가능하고 즉시 종료합니다. 3×3 판에서는 이 개수·승리 조건으로 가능한 상태를 판별할 수 있습니다.

시간 O(1), 공간 O(1) / Time and space O(1)

주의할 점: 두 사람이 동시에 이긴 판은 불가능합니다. 빈 판과 아직 승자가 없는 중간 판도 유효합니다.

## 다른 방법: 합법 게임 상태 전체 생성

```python
def solution(board):
    target=''.join(board)
    lines=((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
    seen=set()
    def visit(state,turn):
        if state in seen: return
        seen.add(state)
        if any(state[a]!='.' and state[a]==state[b]==state[c] for a,b,c in lines): return
        for i,char in enumerate(state):
            if char=='.':
                visit(state[:i]+turn+state[i+1:],'X' if turn=='O' else 'O')
    visit('.'*9,'O')
    return int(target in seen)
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | O와 X의 개수 차이를 확인합니다. 가로·세로·대각선 승리 여부를 구합니다. O가 이겼으면 O가 하나 많아야 하고 X가 이겼으면 개수가 같아야 합니다. | 합법 게임 상태 전체 생성 |
| 비용 | 시간 O(1), 공간 O(1) / Time and space O(1) | 최대 3^9 상태, 고정 크기 / At most 3^9 states, fixed board size |

## 검증

공식 예제 4개와 생성 입력 23개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Determine whether a tic-tac-toe board is reachable with O moving first and X second.

### Conditions and input/output

Input arguments: `board`. The return value is an integer satisfying the task described below.

- 3×3 board; cell ∈ {'O','X','.'}; O moves first

### Approach

Check O/X counts and all row, column and diagonal wins. An O win requires one extra O; an X win requires equal counts.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Legal play has a count difference of zero or one and stops as soon as the last mover wins. On a 3×3 board, these count and win conditions characterize reachable states.

시간 O(1), 공간 O(1) / Time and space O(1)

Boundary cases: Both players cannot win simultaneously. The empty board and unfinished positions may be valid.

### Alternative: Generate all legally reachable game states

최대 3^9 상태, 고정 크기 / At most 3^9 states, fixed board size

### Verification

Local checks covered 4 official examples and 23 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 혼자서 하는 틱택토](https://school.programmers.co.kr/learn/courses/30/lessons/160585) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
