# 두 함수는 삽입·최솟값 추출.
from heapq import heappush, heappop

# 0은 빈칸, 1은 벽인 보드를 받음.
def solution(board):
    # len은 보드 한 변의 길이.
    n = len(board)
    # 방향 번호 0~3에 대응하는 변화량.
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
    # 칸·진입 방향별 최소 비용을 무한대로 초기화.
    distance = [[[float('inf')] * 4 for _ in range(n)] for _ in range(n)]
    # 최소 힙으로 사용.
    heap = []
    # 출발점의 방향을 모두 허용해 첫 도로에는 코너 비용이 없게 함.
    for direction in range(4):
        # 출발 비용은 0.
        distance[0][0][direction] = 0
        # (비용,행,열,방향) 튜플을 최소 힙에 추가.
        heappush(heap, (0, 0, 0, direction))
    # 후보가 남아 있는 동안 반복하는 다익스트라 최단 경로 탐색.
    while heap:
        # 최소 비용 후보를 꺼내 네 변수로 언패킹.
        cost, row, col, old_direction = heappop(heap)
        # 더 좋은 경로로 대체된 오래된 후보는 무시.
        if cost != distance[row][col][old_direction]:
            # 이동 불가 방향 건너뜀.
            continue
        # 방향별 이동 확인.
        for direction, (dr, dc) in enumerate(directions):
            nr, nc = row + dr, col + dc
            # 범위 밖이나 벽이면 제외.
            if not (0 <= nr < n and 0 <= nc < n) or board[nr][nc]:
                # 이동 불가 방향 건너뜀.
                continue
            # 직선 100원에 방향 전환 시 500원 추가.
            candidate = cost + 100 + (500 if direction != old_direction else 0)
            # 같은 칸·방향 상태에 더 싼 경로인지 비교.
            if candidate < distance[nr][nc][direction]:
                # 최소 비용 갱신.
                distance[nr][nc][direction] = candidate
                # 새 후보를 힙에 삽입.
                heappush(heap, (candidate, nr, nc, direction))
    # 도착 칸의 네 방향 중 최소 건설 비용 반환.
    return min(distance[n - 1][n - 1])
