# 배달

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12978) · Level 2 · Python3

## 문제와 조건 / Task and conditions

마을은 1~50개, 도로는 1~2000개, 이동 시간은 1~10000이고 K는 1~500000입니다. 같은 두 마을의 복수 도로가 가능하며 그래프는 연결됩니다. 1번에서 K 이내인 마을 수를 셉니다.

There are 1–50 villages and 1–2000 roads of weight 1–10000, with K in [1,500000]. Parallel roads are allowed and the graph is connected. Count villages within K from village 1.

## 풀이 흐름 / Approach

1번 마을에서 필요한 최단거리만 최소 힙 다익스트라로 구합니다. 짧은 경로를 찾으면 이웃 거리를 갱신하고, 이미 더 짧은 값으로 처리된 힙 항목은 건너뜁니다.

Use heap-based Dijkstra to compute only distances from village 1. Relax neighbors on improvement and skip stale heap entries whose distance is no longer current.

## 왜 맞는가 / Why it works

도로 시간이 양수이므로 아직 처리하지 않은 경로를 우회해도 현재 최소 거리보다 작아질 수 없습니다. 최소 힙에서 확정한 거리는 최단거리이며 K 이하 마을만 세면 됩니다.

Positive edge weights prevent an unsettled detour from improving the current minimum. Distances settled by the heap are shortest-path distances; count those at most K.

## 비용 / Complexity

도로 e, 마을 v에 시간 O((v+e)log(v+e)), 공간 O(v+e) / O((v+e)log(v+e)) time, O(v+e) space

## 구현 / Implementation

[solution.py](solution.py)

```python
from heapq import heappush, heappop

def solution(N, road, K):
    graph = [[] for _ in range(N)]
    for a, b, cost in road:
        graph[a - 1].append((b - 1, cost))
        graph[b - 1].append((a - 1, cost))
    distances = [float('inf')] * N
    distances[0] = 0
    heap = [(0, 0)]
    while heap:
        distance, node = heappop(heap)
        if distance != distances[node]:
            continue
        for neighbor, cost in graph[node]:
            candidate = distance + cost
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                heappush(heap, (candidate, neighbor))
    return sum(distance <= K for distance in distances)
```

## 다른 방법: 플로이드–워셜 / Floyd–Warshall

모든 출발·도착 마을의 최단거리를 구합니다. 시간 O(v³), 공간 O(v²)이지만 경유 정점 DP라 다익스트라와 별개의 독립 대조가 됩니다.

Compute all-pairs shortest paths with intermediate-vertex DP. It costs O(v³) time and O(v²) space and independently checks Dijkstra.

[alternative.py](alternative.py)

```python
def solution(N, road, K):
    distance = [[float('inf')] * N for _ in range(N)]
    for village in range(N):
        distance[village][village] = 0
    for a, b, time in road:
        distance[a - 1][b - 1] = min(distance[a - 1][b - 1], time)
        distance[b - 1][a - 1] = distance[a - 1][b - 1]
    for via in range(N):
        for start in range(N):
            for end in range(N):
                distance[start][end] = min(distance[start][end], distance[start][via] + distance[via][end])
    return sum(time <= K for time in distance[0])
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    5,
    [
      [
        1,
        2,
        1
      ],
      [
        2,
        3,
        3
      ],
      [
        5,
        2,
        2
      ],
      [
        1,
        4,
        2
      ],
      [
        5,
        3,
        1
      ],
      [
        5,
        4,
        2
      ]
    ],
    3
  ],
  "output": 4
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

출처: [프로그래머스 문제 12978](https://school.programmers.co.kr/learn/courses/30/lessons/12978), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 12978](https://school.programmers.co.kr/learn/courses/30/lessons/12978), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
