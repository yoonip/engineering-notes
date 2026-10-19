import sys
from collections import deque

data = sys.stdin.buffer.read().split()
if not data:
    raise SystemExit

n, m = map(int, data[:2])
grid = data[2:2 + n]

distance = [[0] * m for _ in range(n)]
queue = deque()

if grid[0][0] == ord("1"):
    distance[0][0] = 1
    queue.append((0, 0))

directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
while queue:
    r, c = queue.popleft()
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if not (0 <= nr < n and 0 <= nc < m):
            continue
        if grid[nr][nc] != ord("1") or distance[nr][nc] != 0:
            continue
        distance[nr][nc] = distance[r][c] + 1
        queue.append((nr, nc))

answer = distance[n - 1][m - 1]
print(answer if answer != 0 else -1)
