# 문제: 지게차와 크레인
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/388353
# 풀이: 바깥 빈칸에서 deque BFS로 접근 가능한 컨테이너를 찾는다. 크레인은 종류 전체를, 지게차는 접근 가능한 목표만 동시에 제거한다.
# 복잡도: 행 R·열 C·요청 Q개: 시간 O(QRC), 추가 공간 O(RC).

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
                    if board[nr][nc] == '.':
                        queue.append((nr, nc))
                    elif board[nr][nc] == target:
                        removed.append((nr, nc))

        for r, c in removed:
            board[r][c] = '.'
        remaining -= len(removed)

    return remaining
