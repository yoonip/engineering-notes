# [PCCP 기출문제] 4번 / 수레 움직이기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/250134) · Level 3 · Python3

## 문제와 조건 / Task and conditions

판의 각 변은 1~4이며 두 수레의 시작·목표가 하나씩 있습니다. 각 수레는 자신의 방문 칸에 재진입할 수 없고 같은 칸 도착·자리 맞교환도 금지합니다. 둘 다 도착하는 최소 턴, 불가능하면 0입니다.

Both dimensions are 1–4 with one start and goal for each cart. Carts cannot revisit their own cells, share an arrival cell or swap positions. Return minimum turns for both goals, or zero if impossible.

## 풀이 흐름 / Approach

두 수레의 위치뿐 아니라 각 수레가 방문한 칸을 따로 저장합니다. 한 턴의 두 이동을 동시에 고르며 같은 칸 도착과 자리 교환을 막습니다. 도착한 수레는 고정하고 목적지까지의 맨해튼 거리로 가지치기합니다.

Store both positions and separate visited-cell sets. Choose both moves simultaneously, rejecting same-cell arrivals and swaps. A cart stays at its goal; Manhattan-distance lower bounds prune unhelpful branches.

## 왜 맞는가 / Why it works

미래 이동 가능성은 두 위치와 두 방문 집합으로 완전히 정해집니다. 모든 합법 동시 이동을 탐색하고, 현재 최선보다 나을 수 없는 거리 하한만 제거하므로 최소 턴 해를 보존합니다.

The two positions and visited masks completely determine future legal moves. Enumerating every legal simultaneous move and pruning only with an admissible distance bound preserves the minimum-turn solution.

## 비용 / Complexity

가능 경로 조합에 지수 시간·상태 공간 / Exponential time and stored-state space in the number of possible path combinations

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(maze):
    # 행·열 수 언패킹.
    n, m = len(maze), len(maze[0])
    locations = {}
    # 리스트 내포로 각 칸의 통행 가능한 이웃 목록 생성.
    neighbors = [[] for _ in range(n * m)]
    for r in range(n):
        # 모든 열 순회.
        for c in range(m):
            pos = r * m + c
            # 시작·도착 표식이면 위치 기록.
            if maze[r][c] in (1, 2, 3, 4):
                locations[maze[r][c]] = pos
            # () 튜플의 네 방향을 언패킹해 순회.
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                # 경계 안의 벽이 아닌 칸만 허용.
                if 0 <= nr < n and 0 <= nc < m and maze[nr][nc] != 5:
                    neighbors[pos].append(nr * m + nc)
    # 빨강·파랑의 목적지 위치.
    red_goal, blue_goal = locations[3], locations[4]
    red_distance = [abs(pos // m - red_goal // m) + abs(pos % m - red_goal % m) for pos in range(n * m)]
    # 파란 수레도 목적지까지 필요한 최소 이동 횟수의 하한 계산.
    blue_distance = [abs(pos // m - blue_goal // m) + abs(pos % m - blue_goal % m) for pos in range(n * m)]
    answer = n * m + 1
    seen = set()

    def dfs(red, blue, red_mask, blue_mask, turns):
        # nonlocal은 바깥 solution의 answer를 재대입하겠다는 선언.
        nonlocal answer
        if red == red_goal and blue == blue_goal:
            # 최소 턴 수 갱신.
            answer = min(answer, turns)
            return
        if turns + max(red_distance[red], blue_distance[blue]) >= answer:
            return
        # 불변 튜플로 미래 이동을 결정하는 상태 전체 묶음.
        state = (red, blue, red_mask, blue_mask)
        if state in seen:
            return
        # add로 방문 상태 추가.
        seen.add(state)
        reds = [red] if red == red_goal else sorted((pos for pos in neighbors[red] if not red_mask & (1 << pos)), key=lambda pos: red_distance[pos])
        # not은 부정, &와 <<는 방문 비트 검사.
        blues = [blue] if blue == blue_goal else sorted((pos for pos in neighbors[blue] if not blue_mask & (1 << pos)), key=lambda pos: blue_distance[pos])
        for next_red in reds:
            # 파란 수레 후보와 동시에 조합.
            for next_blue in blues:
                if next_red == next_blue or next_red == blue and next_blue == red:
                    continue
                dfs(next_red, next_blue, red_mask | (1 << next_red), blue_mask | (1 << next_blue), turns + 1)

    red, blue = locations[1], locations[2]
    dfs(red, blue, 1 << red, 1 << blue, 0)
    return 0 if answer == n * m + 1 else answer
```

## 다른 방법: 전체 상태 BFS / Breadth-first search over full states

방문 기록을 포함한 상태를 턴 순서대로 넓게 탐색합니다. 최단 턴의 의미가 직접 드러나지만 DFS 가지치기보다 많은 상태를 동시에 보관할 수 있습니다.

Explore states including visited masks in increasing turn order. This makes shortest-turn optimality direct but may retain more states simultaneously than pruned DFS.

[alternative.py](alternative.py)

```python
from collections import deque

def solution(maze):
    rows, cols = len(maze), len(maze[0])
    points = {maze[r][c]: r * cols + c for r in range(rows) for c in range(cols) if maze[r][c] in (1, 2, 3, 4)}
    def moves(pos, goal, mask):
        if pos == goal:
            return [pos]
        r, c = divmod(pos, cols)
        result = []
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            nxt = nr * cols + nc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != 5 and not (mask >> nxt & 1):
                result.append(nxt)
        return result
    start = (points[1], points[2], 1 << points[1], 1 << points[2])
    queue, seen = deque([(start, 0)]), {start}
    while queue:
        (red, blue, rm, bm), turns = queue.popleft()
        if (red, blue) == (points[3], points[4]):
            return turns
        for nr in moves(red, points[3], rm):
            for nb in moves(blue, points[4], bm):
                if nr == nb or (nr == blue and nb == red):
                    continue
                state = (nr, nb, rm | (1 << nr), bm | (1 << nb))
                if state not in seen:
                    seen.add(state)
                    queue.append((state, turns + 1))
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
        1,
        4
      ],
      [
        0,
        0
      ],
      [
        2,
        3
      ]
    ]
  ],
  "output": 3
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 32개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 32 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 32개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 32 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 250134](https://school.programmers.co.kr/learn/courses/30/lessons/250134), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 250134](https://school.programmers.co.kr/learn/courses/30/lessons/250134), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
