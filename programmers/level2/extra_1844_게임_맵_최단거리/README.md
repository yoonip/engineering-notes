# 게임 맵 최단거리

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/1844) · Level 2 · Python3

## 문제와 조건 / Task and conditions

행·열은 각각 1~100이며 둘 다 1인 판은 없습니다. 0은 벽,1은 통로입니다. 좌상단에서 우하단까지 지나는 칸 수의 최솟값을 반환하고 불가능하면 −1입니다.

Both dimensions are 1–100, excluding a 1×1 board. Zero is a wall and one is passable. Return the minimum visited-cell count from top-left to bottom-right, or −1 if unreachable.

## 풀이 흐름 / Approach

한 칸 이동 비용이 모두 같으므로 BFS를 사용합니다. 시작 칸의 거리는 1이며 큐에 넣을 때 방문 처리해 중복 삽입을 막습니다. 도착점을 처음 꺼낸 거리가 최단거리입니다.

All moves have equal cost, so use BFS. Start distance is one, and mark cells when enqueuing to prevent duplicates. The first dequeued target distance is shortest.

## 정답이 되는 이유 / Why it works

BFS는 거리 k의 모든 칸을 거리 k+1보다 먼저 처리합니다. 따라서 처음 도착한 경로보다 짧은 미처리 경로가 있을 수 없습니다. 큐가 비면 도달 불가능입니다.

BFS processes all cells at distance k before distance k+1. Therefore the first target visit cannot have an undiscovered shorter path. An empty queue means unreachable.

## 비용 / Complexity

시간·공간 O(rc) / O(rc) time and space

## 구현 / Implementation

[solution.py](solution.py)

```python
from collections import deque

def solution(maps):
    # 직사각형의 행·열 수를 따로 저장.
    rows, cols = len(maps), len(maps[0])
    distance = [[0] * cols for _ in range(rows)]
    # 출발 칸도 하나로 세므로 거리는 1부터 시작.
    distance[0][0] = 1
    queue = deque([(0, 0)])
    while queue:
        # 두 변수로 언패킹.
        row, col = queue.popleft()
        if row == rows - 1 and col == cols - 1:
            return distance[row][col]
        # 상하좌우 이동 변화량 순회.
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = row + dr, col + dc
            # 범위 안·길·미방문 조건이 모두 참인 칸만 허용.
            if 0 <= nr < rows and 0 <= nc < cols and maps[nr][nc] and distance[nr][nc] == 0:
                distance[nr][nc] = distance[row][col] + 1
                # 나중에 주변 탐색.
                queue.append((nr, nc))
    return -1
```

## 다른 방법: 격자 다익스트라 / Grid Dijkstra

거리와 좌표를 최소 힙에 넣는 일반 최단경로 알고리즘입니다. 시간 O(rc log(rc))로 BFS보다 무겁지만 이동 비용이 서로 달라져도 확장할 수 있습니다.

Use a min-heap of distances and coordinates. O(rc log(rc)) time is heavier than BFS, but the method generalizes to unequal movement costs.

[alternative.py](alternative.py)

```python
from heapq import heappush, heappop

def solution(maps):
    rows, cols = len(maps), len(maps[0])
    distance = {(0, 0): 1}
    heap = [(1, 0, 0)]
    while heap:
        cost, r, c = heappop(heap)
        if cost != distance[(r, c)]:
            continue
        if (r, c) == (rows - 1, cols - 1):
            return cost
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maps[nr][nc] and cost + 1 < distance.get((nr, nc), float('inf')):
                distance[(nr, nc)] = cost + 1
                heappush(heap, (cost + 1, nr, nc))
    return -1
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
        1,
        1,
        1
      ],
      [
        1,
        0,
        1,
        0,
        1
      ],
      [
        1,
        0,
        1,
        1,
        1
      ],
      [
        1,
        1,
        1,
        0,
        1
      ],
      [
        0,
        0,
        0,
        0,
        1
      ]
    ]
  ],
  "output": 11
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

출처: [프로그래머스 문제 1844](https://school.programmers.co.kr/learn/courses/30/lessons/1844), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 1844](https://school.programmers.co.kr/learn/courses/30/lessons/1844), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
