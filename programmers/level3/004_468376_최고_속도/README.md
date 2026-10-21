# 최고 속도

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/468376) · Level 3 · Python3

## 문제와 조건 / Task and conditions

도시는 2~100개, 도로는 1~1000개입니다. 도로는 축 평행·짝수 길이이고 중앙 카메라 제한은 1~1000000입니다. 좌표 절댓값은 최대 10⁹이며 모두 연결됩니다. 첫 도시에서 목적지별 최대 통과 속도를 반환하며 제한 없이 가면 0입니다.

There are 2–100 cities and 1–1000 axis-aligned, even-length roads with midpoint camera limits 1–1000000. Coordinates have absolute value at most 10⁹ and the network is connected. Return each destination’s maximum feasible speed from city 1, or zero if unrestricted.

## 풀이 흐름 / Approach

카메라 지점에서 도로를 자릅니다. 카메라가 없는 교점으로 연결된 도로 조각은 같은 자유 이동 구역으로 합칩니다. 카메라를 지날 때만 제한 속도를 만나는 그래프에서 경로의 최소 제한을 가장 크게 만듭니다.

Split roads at camera locations and merge pieces connected through camera-free intersections into free-travel regions. On the remaining camera graph, maximize the minimum camera limit along the route.

## 정답이 되는 이유 / Why it works

카메라가 없는 연결 구역에서는 제한 없이 이동할 수 있으므로 압축해도 가능한 경로와 통과 카메라는 같습니다. max-min 다익스트라는 경로 병목값이 가장 큰 상태를 먼저 확정해 목적지별 최댓값을 구합니다.

Collapsing camera-free regions preserves possible routes and the cameras they cross. Max-min Dijkstra settles the largest attainable bottleneck first and yields the best value per destination.

## 비용 / Complexity

도로 m, 도시 n에 보수적 O(m² log m+nm), 공간 O(m²+n) / Conservative O(m² log m+nm) time, O(m²+n) space

## 구현 / Implementation

[solution.py](solution.py)

```python
from bisect import bisect_left, bisect_right
from heapq import heappush, heappop

def solution(city, road):
    cameras = {}
    # 도로별로 카메라 없는 조각을 생성.
    for x1, y1, x2, y2, limit in road:
        point = ((x1 + x2) // 2, (y1 + y2) // 2)
        # 같은 위치의 가장 엄격한 제한만 남김.
        cameras[point] = min(cameras.get(point, limit), limit)
    camera_points = list(cameras)
    cuts = []
    bases = []
    parent = []
    links = []
    # 도로별로 카메라 없는 조각을 생성.
    for x1, y1, x2, y2, limit in road:
        positions = [(x + y, i) for i, (x, y) in enumerate(camera_points) if x1 <= x <= x2 and y1 <= y <= y2]
        # 끝점·카메라 위치를 sorted로 정렬.
        boundaries = sorted({x1 + y1, x2 + y2} | {position for position, _ in positions})
        base = len(parent)
        # 인접 경계 사이마다 조각 하나.
        parent.extend(range(base, base + len(boundaries) - 1))
        cuts.append(boundaries)
        # 이 도로 조각 번호의 시작값 저장.
        bases.append(base)
        for position, camera in positions:
            # 카메라가 몇 번째 경계인지 이진 탐색.
            index = bisect_left(boundaries, position)
            if index > 0:
                # 카메라 앞 조각과 카메라의 연결을 튜플로 저장.
                links.append((base + index - 1, camera))
            if index + 1 < len(boundaries):
                # 카메라 뒤 조각의 연결 저장.
                links.append((base + index, camera))
    sizes = [1] * len(parent)

    def find(node):
        # 자기 자신이 부모이면 대표.
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            # 부모 방향으로 이동.
            node = parent[node]
        return node

    def piece(index, x, y):
        offset = min(bisect_right(cuts[index], x + y) - 1, len(cuts[index]) - 2)
        return bases[index] + offset

    # 도시가 놓인 도로를 찾음.
    for i, (x1, y1, x2, y2, _) in enumerate(road):
        for j in range(i):
            # 다른 도로의 양 끝 좌표를 언패킹.
            a, b, c, d, _ = road[j]
            x, y = max(x1, a), max(y1, b)
            # 교점이 없거나 카메라 위치이면 무료 연결을 하지 않음.
            if x > min(x2, c) or y > min(y2, d) or (x, y) in cameras:
                continue
            first, second = find(piece(i, x, y)), find(piece(j, x, y))
            if first != second:
                if sizes[first] < sizes[second]:
                    first, second = second, first
                parent[second] = first
                sizes[first] += sizes[second]
    offset = len(parent)
    graph = [[] for _ in range(offset + len(cameras))]
    for node, camera in links:
        node = find(node)
        limit = cameras[camera_points[camera]]
        graph[node].append((offset + camera, limit))
        graph[offset + camera].append((node, limit))
    cities = []
    for x, y in city:
        for i, (x1, y1, x2, y2, _) in enumerate(road):
            if x1 <= x <= x2 and y1 <= y <= y2:
                cities.append(find(piece(i, x, y)))
                break
    infinity = 1000001
    best = [0] * len(graph)
    best[cities[0]] = infinity
    heap = [(-infinity, cities[0])]
    while heap:
        negative, node = heappop(heap)
        speed = -negative
        if speed != best[node]:
            continue
        for neighbor, limit in graph[node]:
            candidate = min(speed, limit)
            if candidate > best[neighbor]:
                best[neighbor] = candidate
                heappush(heap, (-candidate, neighbor))
    return [0 if best[node] == infinity else best[node] for node in cities[1:]]
```

## 다른 방법: 작은 좌표 격자의 임계값 도달성 / Threshold reachability on a small coordinate grid

짧은 정수 도로를 한 칸씩 펼친 뒤 속도 후보마다 통과할 수 있는 카메라만 남겨 BFS를 합니다. 좌표 크기에 의존하므로 실제 10⁹ 좌표용이 아닌 작은 지도 대조용입니다.

Expand short integer roads into unit edges, then run BFS for each speed threshold, allowing only compatible cameras. This depends on coordinate spans and is a small-map reference, not suitable for 10^9-scale coordinates.

[alternative_reference.py](alternative_reference.py)

```python
from collections import defaultdict, deque

def solution(city, road):
    graph, cameras = defaultdict(set), {}
    for x1, y1, x2, y2, limit in road:
        point = ((x1 + x2) // 2, (y1 + y2) // 2)
        cameras[point] = min(limit, cameras.get(point, limit))
        dx, dy = int(x2 > x1), int(y2 > y1)
        length = x2 - x1 + y2 - y1
        for step in range(length):
            a = (x1 + step * dx, y1 + step * dy)
            b = (a[0] + dx, a[1] + dy)
            graph[a].add(b)
            graph[b].add(a)
    def reachable(speed):
        seen, queue = {tuple(city[0])}, deque([tuple(city[0])])
        while queue:
            node = queue.popleft()
            for nxt in graph[node]:
                if nxt not in seen and cameras.get(nxt, float('inf')) >= speed:
                    seen.add(nxt)
                    queue.append(nxt)
        return seen
    unrestricted = reachable(float('inf'))
    answer = [0] * (len(city) - 1)
    for speed in sorted(set(cameras.values())):
        seen = reachable(speed)
        for i, target in enumerate(city[1:]):
            if tuple(target) in seen and tuple(target) not in unrestricted:
                answer[i] = speed
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
        -1,
        3
      ],
      [
        7,
        3
      ],
      [
        1,
        -1
      ],
      [
        -2,
        6
      ]
    ],
    [
      [
        -1,
        7,
        7,
        7,
        80
      ],
      [
        -3,
        3,
        9,
        3,
        45
      ],
      [
        -2,
        -4,
        -2,
        6,
        60
      ],
      [
        1,
        -4,
        1,
        8,
        50
      ],
      [
        5,
        1,
        5,
        7,
        70
      ]
    ]
  ],
  "output": [
    70,
    50,
    0
  ]
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

출처: [프로그래머스 문제 468376](https://school.programmers.co.kr/learn/courses/30/lessons/468376), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 468376](https://school.programmers.co.kr/learn/courses/30/lessons/468376), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
