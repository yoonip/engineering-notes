from collections import deque

def solution(board):
    rows, cols = len(board), len(board[0])
    distance = [[-1] * cols for _ in range(rows)]
    queue = deque()
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'R':
                distance[r][c] = 0
                queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        if board[r][c] == 'G':
            return distance[r][c]
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r, c
            # 한 번 움직이면 벽이나 장애물 앞까지 멈추지 않는다.
            while 0 <= nr + dr < rows and 0 <= nc + dc < cols and board[nr + dr][nc + dc] != 'D':
                nr += dr
                nc += dc
            # 같은 정지 위치는 BFS에서 처음 도달한 이동 수가 최소다.
            if distance[nr][nc] == -1:
                distance[nr][nc] = distance[r][c] + 1
                queue.append((nr, nc))
    return -1
