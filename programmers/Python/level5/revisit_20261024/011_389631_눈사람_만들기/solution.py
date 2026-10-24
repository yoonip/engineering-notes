def solution(grid):
    width = len(grid[0])
    stride = width + 2
    wall = "#" * stride
    board = wall + "".join("#" + row + "#" for row in grid) + wall
    cells = len(board)
    starts = [i for i, cell in enumerate(board) if cell == "o"]
    directions = (-stride, stride, -1, 1)

    def bfs(start, blocked=-1, save_parents=False):
        distance = [-1] * cells
        parents = [-1] * cells if save_parents else None
        queue = [start]
        distance[start] = 0
        for node in queue:
            next_distance = distance[node] + 1
            for delta in directions:
                other = node + delta
                if other == blocked or board[other] == "#" or distance[other] >= 0:
                    continue
                distance[other] = next_distance
                if parents is not None:
                    parents[other] = node
                queue.append(other)
        return queue, distance, parents

    queue, distance, parents = bfs(starts[0], save_parents=True)
    total = len(queue)
    separation = distance[starts[1]]
    if separation < 0:
        return 0
    degree = bytearray(cells)
    for node in queue:
        degree[node] = (board[node - 1] != "#") + (board[node + 1] != "#") + (board[node - stride] != "#") + (board[node + stride] != "#")
    internal_branch = False
    node = parents[starts[1]]
    while node >= 0 and node != starts[0]:
        if degree[node] >= 3:
            internal_branch = True
        node = parents[node]
    parents = None
    queue, distance, _ = bfs(starts[0], blocked=starts[1])
    first_capacity = len(queue)
    nearest = min((distance[node] for node in queue if degree[node] >= 3), default=cells + 1)
    queue, distance, _ = bfs(starts[1], blocked=starts[0])
    second_capacity = len(queue)
    nearest = min(nearest, min((distance[node] for node in queue if degree[node] >= 3), default=cells + 1))
    small_capacity = min(first_capacity, second_capacity)
    large_capacity = max(first_capacity, second_capacity)
    answer = 0
    for head in range(1, total // 2 + 1):
        body_limit = total - head
        basic_low = max(head, separation + 1 - head)
        basic_high = min(large_capacity, body_limit)
        if head <= small_capacity and basic_low <= basic_high:
            answer += basic_high - basic_low + 1
        flexible_low = body_limit + 1
        if internal_branch:
            flexible_low = max(head, separation + 2 - head)
        elif nearest <= cells:
            flexible_low = max(head, nearest + 2, separation + nearest + 3 - head)
        if flexible_low <= body_limit:
            answer += body_limit - flexible_low + 1
            overlap_low = max(basic_low, flexible_low)
            if head <= small_capacity and overlap_low <= basic_high:
                answer -= basic_high - overlap_low + 1
    return answer

# 전체 코드 줄별 설명
# def solution(grid):  # 위치와 무관하게 머리·몸통 크기 쌍의 종류 수 반환
#     width = len(grid[0])  # 원래 격자의 열 수
#     stride = width + 2  # 양쪽 벽을 붙인 뒤 한 행의 길이
#     wall = "#" * stride  # 격자 위아래를 감쌀 벽 한 행
#     board = wall + "".join("#" + row + "#" for row in grid) + wall  # 외곽 벽을 붙여 이웃 탐색의 경계 분기를 없애기
#     cells = len(board)  # 패딩까지 포함한 작업 배열 길이
#     starts = [i for i, cell in enumerate(board) if cell == "o"]  # 크기 1인 두 눈덩이의 초기 칸 번호
#     directions = (-stride, stride, -1, 1)  # 일차원 번호에서 상하좌우로 움직이는 변화량
#
#     def bfs(start, blocked=-1, save_parents=False):  # 한 칸을 막거나 모두 열고 연결성분·최단거리 계산
#         distance = [-1] * cells  # 이번 탐색에서 아직 도착하지 않은 칸은 -1
#         parents = [-1] * cells if save_parents else None  # 초기 최단경로를 복원할 때만 부모 배열 확보
#         queue = [start]  # 리스트 뒤에 추가하며 사용할 BFS 큐
#         distance[start] = 0  # 시작점까지 거리는 0
#         for node in queue:  # 가까운 칸부터 도달 가능한 모든 칸 순회
#             next_distance = distance[node] + 1  # 현재 칸의 이웃까지 거리
#             for delta in directions:  # 상하좌우 이웃 확인
#                 other = node + delta  # 패딩된 격자의 다음 칸 번호
#                 if other == blocked or board[other] == "#" or distance[other] >= 0:  # 고정한 눈덩이·벽·이미 방문한 칸은 제외
#                     continue  # 다음 이웃 검사
#                 distance[other] = next_distance  # 처음 도착한 최단거리 기록
#                 if parents is not None:  # 경로 복원이 필요한 첫 탐색에서만 부모 저장
#                     parents[other] = node  # 다음 칸에 도착하기 직전의 칸
#                 queue.append(other)  # 도달한 칸을 다음 탐색에 추가
#         return queue, distance, parents  # 방문 목록·거리·선택적으로 만든 부모 배열 반환
#
#     queue, distance, parents = bfs(starts[0], save_parents=True)  # 두 눈덩이가 쓸 수 있는 연결성분과 초기 최단경로 계산
#     total = len(queue)  # 눈이 한 번씩만 소비되므로 두 크기 합의 상한이 되는 칸 수
#     separation = distance[starts[1]]  # 두 초기 칸 사이 최단거리 D
#     if separation < 0:  # 서로 다른 연결성분이면 만날 수 없음
#         return 0  # 눈사람을 만들 수 없는 입력의 방어 처리
#     degree = bytearray(cells)  # 벽 아닌 이웃 수는 최대 4라 한 바이트씩 보관
#     for node in queue:  # 실제로 도달하는 연결성분의 차수만 확인
#         degree[node] = (board[node - 1] != "#") + (board[node + 1] != "#") + (board[node - stride] != "#") + (board[node + stride] != "#")  # 앞뒤 경로 외에 옆으로 비켜설 수 있는 분기점 찾기용 차수
#     internal_branch = False  # 초기 최단경로 내부에 차수 3 이상 칸이 있는지 표시
#     node = parents[starts[1]]  # 양끝은 제외하고 둘째 눈덩이 직전 칸부터 확인
#     while node >= 0 and node != starts[0]:  # 첫 시작점 직전까지 부모를 따라 최단경로 복원
#         if degree[node] >= 3:  # 경로의 앞뒤 외에 다른 방향이 있는 내부 분기점
#             internal_branch = True  # 옆 칸 하나로 Y를 만들 수 있는 경우
#         node = parents[node]  # 최단경로의 이전 칸으로 이동
#     parents = None  # 이후 탐색에는 경로 복원이 없어 큰 부모 배열 해제
#     queue, distance, _ = bfs(starts[0], blocked=starts[1])  # 둘째 눈덩이를 고정했을 때 첫째가 모을 수 있는 최대 크기
#     first_capacity = len(queue)  # 첫째 쪽 기본 크기 상한
#     nearest = min((distance[node] for node in queue if degree[node] >= 3), default=cells + 1)  # 첫 시작점에서 가장 가까운 분기점 거리 후보
#     queue, distance, _ = bfs(starts[1], blocked=starts[0])  # 첫째를 고정했을 때 둘째가 모을 수 있는 최대 크기
#     second_capacity = len(queue)  # 둘째 쪽 기본 크기 상한
#     nearest = min(nearest, min((distance[node] for node in queue if degree[node] >= 3), default=cells + 1))  # 양쪽 시작점 중 분기점까지 더 가까운 거리 k
#     small_capacity = min(first_capacity, second_capacity)  # 머리에 배정할 기본 크기 상한
#     large_capacity = max(first_capacity, second_capacity)  # 몸통에 배정할 기본 크기 상한
#     answer = 0  # Python 정수는 수백억 개의 크기 쌍도 그대로 합산 가능
#     for head in range(1, total // 2 + 1):  # 머리가 몸통 이하인 크기만 순회
#         body_limit = total - head  # 한 칸의 눈은 한 번만 사용하므로 몸통 상한
#         basic_low = max(head, separation + 1 - head)  # 몸통은 머리 이상이며 두 초기점을 잇는 D+1칸도 필요
#         basic_high = min(large_capacity, body_limit)  # 기본 영역에서 몸통이 커질 수 있는 상한
#         if head <= small_capacity and basic_low <= basic_high:  # 각 시작점 쪽에서 따로 눈을 모으는 기본 구간이 있는 경우
#             answer += basic_high - basic_low + 1  # 가능한 몸통 정수 크기 수 합산
#         flexible_low = body_limit + 1  # 분기점으로 열리는 추가 구간이 없다는 초기값
#         if internal_branch:  # 초기 최단경로 안에서 옆 칸 하나로 Y를 만들 수 있는 경우
#             flexible_low = max(head, separation + 2 - head)  # 크기 합 D+2부터 두 눈덩이를 자유롭게 재배치 가능
#         elif nearest <= cells:  # 중심 경로 밖에 분기점이 있는 경우
#             flexible_low = max(head, nearest + 2, separation + nearest + 3 - head)  # 큰 눈덩이는 k+2 이상, 두 크기 합은 D+k+3 이상이어야 비켜설 수 있음
#         if flexible_low <= body_limit:  # 재배치 이후 가능한 몸통 구간이 있는 경우
#             answer += body_limit - flexible_low + 1  # 남은 눈을 원하는 쪽에 배정할 수 있는 추가 구간 합산
#             overlap_low = max(basic_low, flexible_low)  # 기본 구간과 추가 구간이 겹치기 시작하는 크기
#             if head <= small_capacity and overlap_low <= basic_high:  # 같은 머리·몸통 쌍이 두 구간에 모두 있는 경우
#                 answer -= basic_high - overlap_low + 1  # 중복된 크기 쌍을 한 번 빼기
#     return answer  # 최종 크기 쌍의 종류 수 반환

# 풀이 요약
# 상대 초기 칸을 막고 얻은 두 연결성분 크기로 기본 영역을 계산. 크기 합은 두 초기점 거리 D에 1을 더한 값 이상이고 전체 연결성분 크기 이하.
# 눈을 치운 연결 영역에 Y가 생기면 두 눈덩이를 추가 성장 없이 서로 비켜 줄 수 있어, 남은 눈을 원하는 쪽에 배정 가능.
# 초기 경로 내부 분기점이면 합 D+2부터 추가 영역. 바깥 분기점까지 최근접 거리 k라면 몸통 k+2 이상·합 D+k+3 이상이 추가 영역.
# 머리 크기별로 기본·추가 몸통 구간의 합집합 길이 계산. 외곽 벽을 붙인 일차원 격자에서 BFS 세 번을 사용해 시간·공간 O(NM).

