from collections import deque

def solution(maps):
    rows, cols = len(maps), len(maps[0])
    distance = [[0] * cols for _ in range(rows)]
    distance[0][0] = 1
    queue = deque([(0, 0)])
    while queue:
        row, col = queue.popleft()
        if row == rows - 1 and col == cols - 1:
            return distance[row][col]
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols and maps[nr][nc] and distance[nr][nc] == 0:
                distance[nr][nc] = distance[row][col] + 1
                queue.append((nr, nc))
    return -1

# 전체 코드 줄별 설명
# from collections import deque  # import는 도구 가져오기. deque는 앞에서 꺼내기 빠른 선입선출 큐. BFS에 사용.
# 
# def solution(maps):  # def는 함수 정의. 1은 길, 0은 벽인 격자 입력.
#     rows, cols = len(maps), len(maps[0])  # len은 길이. 직사각형의 행·열 수를 따로 저장.
#     distance = [[0] * cols for _ in range(rows)]  # []는 중첩 리스트. 0은 미방문, 양수는 시작 칸까지 포함해 지나온 칸 수.
#     distance[0][0] = 1  # 출발 칸도 하나로 세므로 거리는 1부터 시작.
#     queue = deque([(0, 0)])  # ()는 좌표 튜플. 출발 좌표를 담은 큐 생성.
#     while queue:  # 큐가 비어 있지 않은 동안 너비 우선 탐색(BFS).
#         row, col = queue.popleft()  # popleft는 가장 먼저 넣은 좌표를 꺼내 삭제. 두 변수로 언패킹.
#         if row == rows - 1 and col == cols - 1:  # ==는 같음, and는 모두 참. 목적지에 도달했는지 검사.
#             return distance[row][col]  # 가까운 거리부터 방문하므로 첫 도달 칸 수가 최소.
#         for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):  # 상하좌우 이동 변화량 순회.
#             nr, nc = row + dr, col + dc  # 다음 칸 좌표 계산.
#             if 0 <= nr < rows and 0 <= nc < cols and maps[nr][nc] and distance[nr][nc] == 0:  # 범위 안·길·미방문 조건이 모두 참인 칸만 허용.
#                 distance[nr][nc] = distance[row][col] + 1  # 이웃 칸을 한 번 더 지나므로 칸 수 1 증가. 큐에 넣을 때 방문 표시.
#                 queue.append((nr, nc))  # append는 끝에 추가. 나중에 주변 탐색.
#     return -1  # 큐가 빌 때까지 목적지에 도달하지 못하면 실패.

# 풀이 요약
# 모든 이동이 한 칸이므로 BFS로 최단 거리를 구한다. DFS는 처음 도착한 길이 최단이라는 보장이 없다.
# 출발 칸도 세어 예제의 최단 경로는 11칸이다. 갈 수 없는 지도는 -1. 시간·공간 O(RC), 입력 지도는 수정하지 않는다.
# 