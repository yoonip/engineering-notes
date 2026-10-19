from collections import deque

def solution(board):
    n = len(board)
    grid = [[1] * (n + 2) for _ in range(n + 2)]
    for row in range(n):
        grid[row + 1][1:n + 1] = board[row]
    start = ((1, 1), (1, 2))
    queue = deque([(start, 0)])
    visited = {start}
    while queue:
        state, time = queue.popleft()
        first, second = state
        if (n, n) in state:
            return time
        r1, c1 = first
        r2, c2 = second
        candidates = []
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if grid[r1 + dr][c1 + dc] == 0 and grid[r2 + dr][c2 + dc] == 0:
                candidates.append(((r1 + dr, c1 + dc), (r2 + dr, c2 + dc)))
        if r1 == r2:
            for dr in (-1, 1):
                if grid[r1 + dr][c1] == 0 and grid[r2 + dr][c2] == 0:
                    candidates.append((first, (r1 + dr, c1)))
                    candidates.append((second, (r2 + dr, c2)))
        else:
            for dc in (-1, 1):
                if grid[r1][c1 + dc] == 0 and grid[r2][c2 + dc] == 0:
                    candidates.append((first, (r1, c1 + dc)))
                    candidates.append((second, (r2, c2 + dc)))
        for candidate in candidates:
            next_state = tuple(sorted(candidate))
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, time + 1))
    return -1

# 전체 코드 줄별 설명
# from collections import deque  # import는 도구 가져오기. deque는 앞에서 꺼내기 빠른 선입선출 큐로 BFS에 사용.
# 
# def solution(board):  # def는 함수 정의. 0은 빈칸, 1은 벽인 보드를 받음.
#     n = len(board)  # len은 한 변의 길이.
#     grid = [[1] * (n + 2) for _ in range(n + 2)]  # []는 리스트. 보드 바깥에 한 칸 두께의 벽을 둘러 범위 검사를 단순화.
#     for row in range(n):  # range(n)은 0~n-1. 원래 보드의 행 순회.
#         grid[row + 1][1:n + 1] = board[row]  # [시작:끝]은 슬라이스. 테두리 안쪽에 보드 한 행 복사.
#     start = ((1, 1), (1, 2))  # ()는 튜플. 로봇이 차지한 두 칸을 하나의 상태로 표현.
#     queue = deque([(start, 0)])  # (상태,걸린 시간)을 담은 BFS 큐 초기화.
#     visited = {start}  # {} 안 원소만 쓰면 집합. 이미 발견한 로봇 상태의 중복 방문 방지.
#     while queue:  # 큐가 비어 있지 않은 동안 너비 우선 탐색.
#         state, time = queue.popleft()  # popleft는 맨 앞 원소 추출·삭제. 가장 짧은 시간부터 처리.
#         first, second = state  # 두 좌표를 언패킹.
#         if (n, n) in state:  # in은 포함 여부. 두 칸 중 하나라도 도착점이면 성공.
#             return time  # 모든 이동 비용이 1이므로 처음 도착한 시간이 최소.
#         r1, c1 = first  # 첫 칸의 행·열 분리.
#         r2, c2 = second  # 둘째 칸의 행·열 분리.
#         candidates = []  # 다음에 갈 수 있는 로봇 상태 목록.
#         for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):  # 상하좌우 평행 이동 변화량 순회.
#             if grid[r1 + dr][c1 + dc] == 0 and grid[r2 + dr][c2 + dc] == 0:  # ==는 같음, and는 모두 참. 두 도착 칸이 모두 비어 있어야 함.
#                 candidates.append(((r1 + dr, c1 + dc), (r2 + dr, c2 + dc)))  # append는 끝에 추가. 두 칸을 같은 방향으로 이동.
#         if r1 == r2:  # 두 행이 같으면 가로 방향 로봇.
#             for dr in (-1, 1):  # 위쪽·아래쪽으로 회전하는 경우.
#                 if grid[r1 + dr][c1] == 0 and grid[r2 + dr][c2] == 0:  # 회전 중 지나가는 2×2 영역의 나머지 두 칸이 모두 비어 있어야 함.
#                     candidates.append((first, (r1 + dr, c1)))  # 첫 칸을 축으로 회전.
#                     candidates.append((second, (r2 + dr, c2)))  # 둘째 칸을 축으로 회전.
#         else:  # 두 열이 같은 세로 방향 로봇.
#             for dc in (-1, 1):  # 왼쪽·오른쪽 회전 확인.
#                 if grid[r1][c1 + dc] == 0 and grid[r2][c2 + dc] == 0:  # 회전 공간 두 칸 검사.
#                     candidates.append((first, (r1, c1 + dc)))  # 첫 칸을 축으로 회전.
#                     candidates.append((second, (r2, c2 + dc)))  # 둘째 칸을 축으로 회전.
#         for candidate in candidates:  # 가능한 다음 상태를 순회.
#             next_state = tuple(sorted(candidate))  # sorted는 정렬, tuple은 변경 불가 묶음. 두 칸 순서를 통일해 앞뒤가 바뀐 중복 제거.
#             if next_state not in visited:  # not in은 포함되어 있지 않음. 처음 보는 상태만 탐색.
#                 visited.add(next_state)  # add는 집합 원소 추가. 큐에 넣을 때 방문 표시.
#                 queue.append((next_state, time + 1))  # 이동·회전 모두 1초 추가.
#     return -1  # 도달 불가일 때의 반환값. 문제에서는 도달 가능한 보드만 주어짐.

# 풀이 요약
# 로봇의 두 칸 전체를 하나의 상태로 BFS한다. 평행 이동 네 방향과 두 칸 각각을 축으로 한 회전을 검사한다.
# 회전은 도착 칸뿐 아니라 지나가는 대각선 공간도 비어 있어야 한다. 예제에서는 이동·회전 7번으로 도착한다.
# 로봇 위치와 방향의 상태 수가 O(N²)이므로 시간·공간 O(N²).
# 