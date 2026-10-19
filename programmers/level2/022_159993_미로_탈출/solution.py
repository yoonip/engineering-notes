# 문제: 미로 탈출
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/159993
# 풀이: 시작점에서 레버까지, 레버에서 출구까지 deque BFS를 수행한다. 두 최단 거리 중 하나라도 없으면 탈출할 수 없다.
# 복잡도: 행 R·열 C: 시간·추가 공간 O(RC). BFS를 두 번 수행한다.

from collections import deque

def solution(maps):
    rows, cols = len(maps), len(maps[0])
    positions = {}
    for r in range(rows):
        for c in range(cols):
            if maps[r][c] in 'SLE':
                positions[maps[r][c]] = (r, c)
    def bfs(start, goal):
        queue = deque([(start[0], start[1], 0)])
        visited = {start}
        while queue:
            r, c, distance = queue.popleft()
            if (r, c) == goal:
                return distance
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and maps[nr][nc] != 'X' and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc, distance + 1))
        return -1
    first = bfs(positions['S'], positions['L'])
    second = bfs(positions['L'], positions['E'])
    return first + second if first >= 0 and second >= 0 else -1
