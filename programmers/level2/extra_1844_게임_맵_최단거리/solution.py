from collections import deque

def solution(maps):
    # 직사각형의 행·열 수를 따로 저장.
    rows, cols = len(maps), len(maps[0])
    distance = [[0] * cols for _ in range(rows)]
    # 출발 칸도 하나로 세므로 거리는 1부터 시작.
    distance[0][0] = 1
    queue = deque([(0, 0)])
    while queue:
        # 두 변수로 언패킹.
        row, col = queue.popleft()
        if row == rows - 1 and col == cols - 1:
            return distance[row][col]
        # 상하좌우 이동 변화량 순회.
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = row + dr, col + dc
            # 범위 안·길·미방문 조건이 모두 참인 칸만 허용.
            if 0 <= nr < rows and 0 <= nc < cols and maps[nr][nc] and distance[nr][nc] == 0:
                distance[nr][nc] = distance[row][col] + 1
                # 나중에 주변 탐색.
                queue.append((nr, nc))
    return -1
