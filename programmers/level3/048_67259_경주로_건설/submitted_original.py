from heapq import heappush, heappop

def solution(board):
    n = len(board)
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
    distance = [[[float('inf')] * 4 for _ in range(n)] for _ in range(n)]
    heap = []
    for direction in range(4):
        distance[0][0][direction] = 0
        heappush(heap, (0, 0, 0, direction))
    while heap:
        cost, row, col, old_direction = heappop(heap)
        if cost != distance[row][col][old_direction]:
            continue
        for direction, (dr, dc) in enumerate(directions):
            nr, nc = row + dr, col + dc
            if not (0 <= nr < n and 0 <= nc < n) or board[nr][nc]:
                continue
            candidate = cost + 100 + (500 if direction != old_direction else 0)
            if candidate < distance[nr][nc][direction]:
                distance[nr][nc][direction] = candidate
                heappush(heap, (candidate, nr, nc, direction))
    return min(distance[n - 1][n - 1])

# 전체 코드 줄별 설명
# from heapq import heappush, heappop  # import는 도구 가져오기. 최소 힙은 가장 작은 비용부터 꺼내는 자료구조. 두 함수는 삽입·최솟값 추출.
# 
# def solution(board):  # def는 함수 정의. 0은 빈칸, 1은 벽인 보드를 받음.
#     n = len(board)  # len은 보드 한 변의 길이.
#     directions = ((1, 0), (-1, 0), (0, 1), (0, -1))  # ()는 튜플. 방향 번호 0~3에 대응하는 변화량.
#     distance = [[[float('inf')] * 4 for _ in range(n)] for _ in range(n)]  # 중첩 리스트. 칸·진입 방향별 최소 비용을 무한대로 초기화.
#     heap = []  # []는 리스트. 최소 힙으로 사용.
#     for direction in range(4):  # range(4)는 0~3. 출발점의 방향을 모두 허용해 첫 도로에는 코너 비용이 없게 함.
#         distance[0][0][direction] = 0  # 출발 비용은 0.
#         heappush(heap, (0, 0, 0, direction))  # (비용,행,열,방향) 튜플을 최소 힙에 추가.
#     while heap:  # 후보가 남아 있는 동안 반복하는 다익스트라 최단 경로 탐색.
#         cost, row, col, old_direction = heappop(heap)  # 최소 비용 후보를 꺼내 네 변수로 언패킹.
#         if cost != distance[row][col][old_direction]:  # !=는 다름. 더 좋은 경로로 대체된 오래된 후보는 무시.
#             continue  # 이번 반복 건너뜀.
#         for direction, (dr, dc) in enumerate(directions):  # enumerate는 번호와 값을 함께 제공. 방향별 이동 확인.
#             nr, nc = row + dr, col + dc  # 다음 칸 좌표.
#             if not (0 <= nr < n and 0 <= nc < n) or board[nr][nc]:  # not은 부정, and는 모두 참, or는 하나라도 참. 범위 밖이나 벽이면 제외.
#                 continue  # 이동 불가 방향 건너뜀.
#             candidate = cost + 100 + (500 if direction != old_direction else 0)  # 조건부 표현식. 직선 100원에 방향 전환 시 500원 추가.
#             if candidate < distance[nr][nc][direction]:  # 같은 칸·방향 상태에 더 싼 경로인지 비교.
#                 distance[nr][nc][direction] = candidate  # 최소 비용 갱신.
#                 heappush(heap, (candidate, nr, nc, direction))  # 새 후보를 힙에 삽입.
#     return min(distance[n - 1][n - 1])  # min은 최솟값. 도착 칸의 네 방향 중 최소 건설 비용 반환.

# 풀이 요약
# 같은 칸이라도 들어온 방향에 따라 다음 코너 비용이 달라진다. (행,열,방향)을 각각 다른 상태로 두고 다익스트라를 실행한다.
# 예: 빈 3×3은 직선 4개와 코너 1개로 400+500=900원. 최소 이동 횟수 경로가 최소 건설 비용 경로와 항상 같지는 않다.
# 즉시 되돌아가는 경로는 양수 비용만 늘려 최적 경로에 필요하지 않다. 시간 O(N² log N), 공간 O(N²).
# 