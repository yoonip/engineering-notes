def solution(grid):
    rows, cols = len(grid), len(grid[0])
    # 칸뿐 아니라 들어온 방향까지 방문 상태에 넣는다.
    visited = [bytearray(cols * 4) for _ in range(rows)]
    directions = ((-1, 0), (0, 1), (1, 0), (0, -1))
    answer = []
    for r in range(rows):
        for c in range(cols):
            for direction in range(4):
                if visited[r][c * 4 + direction]:
                    continue
                x, y, d, length = r, c, direction, 0
                # 후속 상태가 하나이므로 경로를 따라가며 한 사이클 길이를 센다.
                while not visited[x][y * 4 + d]:
                    visited[x][y * 4 + d] = 1
                    length += 1
                    if grid[x][y] == 'L':
                        d = (d - 1) % 4
                    elif grid[x][y] == 'R':
                        d = (d + 1) % 4
                    dx, dy = directions[d]
                    x, y = (x + dx) % rows, (y + dy) % cols
                answer.append(length)
    return sorted(answer)
