# 발전소 회로 복구

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/468375) · Level 3 · Python3

## 문제와 조건 / Task and conditions

층은 1~10개이고 층별 구조는 같은 2~40×2~40 격자입니다. 패널은 2~15개, 선행 관계는 1~100개입니다. 1번 패널에서 출발해 모든 패널을 조건대로 켜는 최소 이동시간을 반환합니다.

There are 1–10 floors sharing a 2–40 by 2–40 layout, with 2–15 panels and 1–100 prerequisites. Starting at panel 1, return minimum travel time to activate all panels legally.

## 풀이 흐름 / Approach

패널 위치에서 BFS를 해 같은 층의 이동거리를 구합니다. 층이 다르면 엘리베이터까지의 거리와 층 차이를 더합니다. 켜진 패널 집합과 현재 위치를 상태로, 선행 조건을 만족하는 다음 패널만 선택합니다.

Run BFS from panel coordinates to obtain within-floor distances. Cross-floor travel goes via the elevator plus the floor difference. A state consists of the activated-panel set and current panel, and only prerequisite-satisfied panels may activate next.

## 왜 맞는가 / Why it works

한 층의 최단거리는 BFS로 정확하고 층 사이 유일한 연결은 엘리베이터입니다. 이후 방문 순서는 현재 위치·활성 집합에만 의존하므로 비트마스크 DP가 모든 유효 순서를 비교합니다. 1번도 선행 조건이 있으면 출발 때 켜지지 않습니다.

BFS gives exact planar distances and the elevator is the only connection between floors. Future choices depend only on position and activated set, making bitmask DP exhaustive over valid orders. Panel 1 is not initially active if it has unmet prerequisites.

## 비용 / Complexity

시간 O(kmn+k²2ᵏ), 공간 O(kmn+k2ᵏ) / O(kmn+k²2ᵏ) time, O(kmn+k2ᵏ) space

## 구현 / Implementation

[solution.py](solution.py)

```python
from collections import deque
from functools import lru_cache

def solution(h, grid, panels, seqs):
    # 행·열 수를 언패킹으로 나눠 받음.
    n, m = len(grid), len(grid[0])
    k = len(panels)
    # 도달 불가능 거리를 나타낼 충분히 큰 값.
    infinity = 10 ** 9
    elevator = next(r * m + c for r in range(n) for c in range(m) if grid[r][c] == '@')

    def bfs(start):
        # 각 칸을 아직 미도달 상태로 설정.
        distance = [infinity] * (n * m)
        distance[start] = 0
        # []에 시작 위치를 담아 deque 큐 생성.
        queue = deque([start])
        while queue:
            pos = queue.popleft()
            # 위치를 행·열로 복원.
            r, c = divmod(pos, m)
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                # 이웃 칸의 좌표 계산.
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] != '#':
                    # 이웃의 1차원 위치 계산.
                    neighbor = nr * m + nc
                    if distance[neighbor] == infinity:
                        # BFS는 가까운 순서이므로 첫 방문이 최단 거리.
                        distance[neighbor] = distance[pos] + 1
                        queue.append(neighbor)
        return distance

    # 1부터 세는 행·열을 0 기반 위치로 변환, _는 여기서 안 쓰는 층.
    positions = [(r - 1) * m + c - 1 for _, r, c in panels]
    maps = [bfs(pos) for pos in positions]
    # 서로 독립인 행들로 패널 간 거리 표 생성.
    travel = [[0] * k for _ in range(k)]
    for i in range(k):
        # 도착 패널 순회.
        for j in range(k):
            if panels[i][0] == panels[j][0]:
                # i 위치에서 j 위치까지 BFS 거리.
                travel[i][j] = maps[i][positions[j]]
            else:
                travel[i][j] = maps[i][elevator] + abs(panels[i][0] - panels[j][0]) + maps[j][elevator]
    # 패널별 선행 패널 집합을 정수 비트마스크로 저장.
    required = [0] * k
    for a, b in seqs:
        # b를 켜기 전에 필요한 a를 표시.
        required[b - 1] |= 1 << (a - 1)
    full = (1 << k) - 1

    @lru_cache(None)
    def dfs(mask, current):
        if mask == full:
            return 0
        answer = infinity
        for target in range(k):
            bit = 1 << target
            if mask & bit or required[target] & mask != required[target]:
                continue
            answer = min(answer, travel[current][target] + dfs(mask | bit, target))
        return answer

    return dfs(1 if required[0] == 0 else 0, 0)
```

## 다른 방법: 층 전체 상태 BFS / BFS over physical position and activated set

각 층의 각 칸을 실제 이동하면서 패널 활성화 상태까지 함께 탐색합니다. 별도의 거리 압축과 순서 DP가 없어 독립적인 기준이지만 O(hmn2ᵏ) 상태로 작은 건물에서만 사용합니다.

Search physical floor/cell positions together with activation masks. It avoids distance compression and ordering DP, providing an independent oracle with O(hmn2^k) states for small buildings.

[alternative_reference.py](alternative_reference.py)

```python
from collections import deque

def solution(h, grid, panels, seqs):
    rows, cols = len(grid), len(grid[0])
    panel_at = {(f - 1, r - 1, c - 1): i for i, (f, r, c) in enumerate(panels)}
    required = [0] * len(panels)
    for a, b in seqs:
        required[b - 1] |= 1 << (a - 1)
    def activate(f, r, c, mask):
        i = panel_at.get((f, r, c))
        if i is not None and mask & required[i] == required[i]:
            mask |= 1 << i
        return mask
    f, r, c = (value - 1 for value in panels[0])
    start = (f, r, c, activate(f, r, c, 0))
    queue, seen = deque([(start, 0)]), {start}
    while queue:
        (f, r, c, mask), distance = queue.popleft()
        if mask == (1 << len(panels)) - 1:
            return distance
        candidates = [(f, r + dr, c + dc) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))]
        if grid[r][c] == '@':
            candidates += [(f - 1, r, c), (f + 1, r, c)]
        for nf, nr, nc in candidates:
            if 0 <= nf < h and 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
                state = (nf, nr, nc, activate(nf, nr, nc, mask))
                if state not in seen:
                    seen.add(state)
                    queue.append((state, distance + 1))
    return -1
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    3,
    [
      ".#.##..",
      ".#..##.",
      ".......",
      "##.###.",
      ".@.#...",
      "...#..."
    ],
    [
      [
        2,
        3,
        4
      ],
      [
        2,
        5,
        6
      ],
      [
        1,
        1,
        1
      ],
      [
        3,
        6,
        3
      ]
    ],
    [
      [
        3,
        2
      ],
      [
        1,
        2
      ],
      [
        4,
        1
      ],
      [
        4,
        3
      ]
    ]
  ],
  "output": 36
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 31개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 31 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 31개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 31 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 468375](https://school.programmers.co.kr/learn/courses/30/lessons/468375), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 468375](https://school.programmers.co.kr/learn/courses/30/lessons/468375), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
