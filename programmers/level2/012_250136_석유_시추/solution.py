def solution(land):
    rows, cols = len(land), len(land[0])
    totals = [0] * cols
    for r in range(rows):
        for c in range(cols):
            if land[r][c] == 0:
                continue
            stack = [(r, c)]
            # 발견 즉시 방문 표시해 같은 칸을 중복으로 넣지 않는다.
            land[r][c] = 0
            columns = set()
            size = 0
            while stack:
                x, y = stack.pop()
                size += 1
                # 시추관이 같은 덩어리를 여러 칸에서 만나도 한 번만 센다.
                columns.add(y)
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and land[nx][ny] == 1:
                        land[nx][ny] = 0
                        stack.append((nx, ny))
            # 덩어리 크기 전체를 닿는 열마다 한 번씩 더한다.
            for column in columns:
                totals[column] += size
    return max(totals)
