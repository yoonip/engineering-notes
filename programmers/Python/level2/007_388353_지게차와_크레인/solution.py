from collections import deque


def solution(storage, requests):
    n, m = len(storage), len(storage[0])
    board = [['.'] * (m + 2)]
    for row in storage:
        board.append(['.'] + list(row) + ['.'])
    board.append(['.'] * (m + 2))
    remaining = n * m
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

    for request in requests:
        target = request[0]
        removed = []
        if len(request) == 2:
            for r in range(1, n + 1):
                for c in range(1, m + 1):
                    if board[r][c] == target:
                        removed.append((r, c))
        else:
            visited = [[False] * (m + 2) for _ in range(n + 2)]
            # 추가한 바깥 테두리에서 접근 가능 영역을 찾는다.
            visited[0][0] = True
            queue = deque([(0, 0)])
            while queue:
                r, c = queue.popleft()
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if not (0 <= nr < n + 2 and 0 <= nc < m + 2):
                        continue
                    if visited[nr][nc]:
                        continue
                    visited[nr][nc] = True
                    # 빈칸만 통과하며 대상 컨테이너를 지나가지는 않는다.
                    if board[nr][nc] == '.':
                        queue.append((nr, nc))
                    elif board[nr][nc] == target:
                        removed.append((nr, nc))

        # 요청 한 번의 탐색이 끝난 뒤 한꺼번에 제거한다.
        for r, c in removed:
            board[r][c] = '.'
        remaining -= len(removed)

    return remaining
