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
