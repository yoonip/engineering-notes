def solution(m, n, picture):
    # 원래 그림을 보존하며 방문 칸을 지울 준비.
    grid = [row[:] for row in picture]
    areas = largest = 0
    # 모든 행 순회.
    for row in range(m):
        for col in range(n):
            # []로 현재 색 조회.
            color = grid[row][col]
            if color == 0:
                continue
            areas += 1
            # 스택에 넣는 즉시 방문 표시.
            grid[row][col] = 0
            stack = [(row, col)]
            size = 0
            while stack:
                # 좌표 언패킹.
                r, c = stack.pop()
                size += 1
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    # 이웃 좌표 계산.
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == color:
                        # 방문 표시해 중복 추가 방지.
                        grid[nr][nc] = 0
                        stack.append((nr, nc))
            # 완성한 영역 넓이 반영.
            largest = max(largest, size)
    return [areas, largest]
