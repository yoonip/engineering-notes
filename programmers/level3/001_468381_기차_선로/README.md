# 기차 선로

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/468381) · Level 3 · Python3

## 문제와 조건 / Task and conditions

각 변은 2~8이지만 전체 칸은 최대 20개입니다. −1은 장애물,0은 빈칸,1~7은 선로이고 빈칸이 존재합니다. 시작 선로는 1, 끝은 1 또는 2입니다. 기존 선로를 모두 쓰는 유효 추가 배치 수를 반환합니다.

Each dimension is 2–8, with at most 20 cells overall. −1 is blocked, zero is empty and 1–7 are rail types, with at least one empty cell. The start rail is 1 and end is 1 or 2. Count valid additions using all existing rails.

## 풀이 흐름 / Approach

기차가 실제로 진행할 수 있는 경로를 탐색합니다. 각 칸에서 진입 방향과 호환되는 선로만 선택합니다. 같은 칸을 가로·세로로 한 번씩 지나면 교차 선로가 되며, 기존 교차 선로는 두 방향을 모두 지나야 합니다.

Explore the train’s actual route and choose only rail shapes compatible with its entry direction. Traversing an empty cell once horizontally and once vertically makes a crossing; every existing crossing must be used on both axes.

## 왜 맞는가 / Why it works

진입·진출 연결을 만족하는 선택만 생성하며 같은 축 재방문은 순환으로 막습니다. 기존 선로 미방문 집합과 교차 선로의 미완료 집합이 모두 비었을 때만 도착을 인정해 사용 조건을 함께 보장합니다.

Only compatible entry/exit choices are generated, and revisiting an axis is rejected as a cycle. Arrival is accepted only when all required rails and both axes of every existing crossing have been covered.

## 비용 / Complexity

빈칸 e의 선로 선택에 대해 지수 시간, 호출·상태 공간 O(nm) / Exponential search in empty-cell choices, O(nm) path state and recursion space

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(grid):
    # 행 수와 열 수를 두 변수로 나눠 받는 언패킹.
    n, m = len(grid), len(grid[0])
    original = [value for row in grid for value in row]
    # 탐색 중 설치할 선로를 별도로 저장.
    rails = original[:]
    size = n * m
    neighbors = []
    required = 0
    # 원소 순회.
    for pos, kind in enumerate(original):
        r, c = divmod(pos, m)
        # append는 이웃 튜플 하나를 추가.
        neighbors.append((pos + 1 if c + 1 < m else -1, pos + m if r + 1 < n else -1, pos - 1 if c else -1, pos - m if r else -1))
        if kind > 0:
            required |= 1 << pos
    # 선로별 연결 방향을 R=1,D=2,L=4,U=8 비트로 표현.
    ends = (0, 5, 10, 15, 12, 9, 3, 6)
    choices = [[] for _ in range(4)]
    # 기차가 현재 칸에 들어오는 이동 방향.
    for direction in range(4):
        entry = (direction + 2) % 4
        # 3번 교차 선로는 빈칸을 실제로 두 번 통과할 때만 확정.
        for kind in (1, 2, 4, 5, 6, 7):
            if ends[kind] & (1 << entry):
                # 들어온 쪽 비트를 지워 나갈 방향만 남김.
                exit_bit = ends[kind] ^ (1 << entry)
                choices[direction].append((kind, exit_bit.bit_length() - 1))
    # 가로 1, 세로 2, 완전히 사용한 칸은 3.
    visited = [0] * size
    visited[0] = 1

    def dfs(pos, direction, remaining, pending):
        # 경계 밖이나 장애물이면 불가능.
        if pos < 0 or original[pos] == -1:
            return 0
        axis = 1 << (direction % 2)
        # 현재 칸에 정해진 선로 종류.
        kind = rails[pos]
        used = visited[pos]
        if used:
            # 같은 축 재방문과 곡선 재방문을 금지.
            if used & axis or kind not in (1, 2, 3):
                return 0
            if kind != 3 and original[pos] != 0:
                return 0
            # 빈칸에서 설치한 직선을 두 축으로 통과하면 교차 선로로 확정.
            rails[pos] = 3
            visited[pos] = 3
            # ~는 비트 반전, &로 이 칸의 미완성 표시 제거.
            result = dfs(neighbors[pos][direction], direction, remaining, pending & ~(1 << pos))
            rails[pos] = kind
            visited[pos] = used
            return result
        remaining &= ~(1 << pos)
        if pos == size - 1:
            valid_entry = kind == 1 and direction == 0 or kind == 2 and direction == 1
            return int(valid_entry and remaining == 0 and pending == 0)
        visited[pos] = axis
        if kind == 3:
            result = dfs(neighbors[pos][direction], direction, remaining, pending | (1 << pos))
        else:
            result = 0
            for candidate, exit_direction in choices[direction]:
                if kind != 0 and kind != candidate:
                    continue
                rails[pos] = candidate
                visited[pos] = axis if candidate <= 2 else 3
                result += dfs(neighbors[pos][exit_direction], exit_direction, remaining, pending)
        rails[pos] = kind
        visited[pos] = 0
        return result

    return dfs(1, 0, required & ~1, 0)
```

## 다른 방법: 배치 전체 생성 후 경로 시뮬레이션 / Enumerate assignments then simulate

작은 격자에서 빈칸마다 비어 있음 또는 선로 1~7을 먼저 정하고 기차를 움직입니다. 경로 중심 탐색과 독립적이지만 8ᵉ개 배치가 생겨 빈칸이 몇 개일 때만 검증용으로 사용합니다.

On a tiny grid, assign every empty cell either zero or rail 1–7 before simulating the train. This independently checks route-based search but has 8^e assignments and is only a small-input oracle.

[alternative_reference.py](alternative_reference.py)

```python
from itertools import product

def solution(grid):
    rows, cols = len(grid), len(grid[0])
    original = [v for row in grid for v in row]
    empty = [i for i, v in enumerate(original) if v == 0]
    ports = (0, 5, 10, 15, 12, 9, 3, 6)
    moves = ((0, 1), (1, 0), (0, -1), (-1, 0))
    answer = 0
    for values in product(range(8), repeat=len(empty)):
        rails = original[:]
        for pos, kind in zip(empty, values):
            rails[pos] = kind
        seen, pos, direction = {0: 1}, 1, 0
        valid = False
        while 0 <= pos < rows * cols:
            kind = rails[pos]
            axis = 1 << (direction % 2)
            if kind <= 0 or seen.get(pos, 0) & axis:
                break
            entry = (direction + 2) % 4
            if not (ports[kind] >> entry & 1):
                break
            seen[pos] = seen.get(pos, 0) | axis
            if pos == rows * cols - 1:
                valid = True
                break
            outgoing = direction if kind == 3 else (ports[kind] ^ (1 << entry)).bit_length() - 1
            r, c = divmod(pos, cols)
            dr, dc = moves[outgoing]
            r, c = r + dr, c + dc
            if not (0 <= r < rows and 0 <= c < cols):
                break
            pos, direction = r * cols + c, outgoing
        if valid:
            for i, kind in enumerate(rails):
                if kind > 0 and (i not in seen or kind == 3 and seen[i] != 3):
                    valid = False
                    break
            answer += valid
    return answer
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
        0,
        -1
      ],
      [
        0,
        0,
        7
      ],
      [
        0,
        0,
        2
      ]
    ]
  ],
  "output": 2
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 18개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 18 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 13개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 13 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 468381](https://school.programmers.co.kr/learn/courses/30/lessons/468381), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 468381](https://school.programmers.co.kr/learn/courses/30/lessons/468381), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
