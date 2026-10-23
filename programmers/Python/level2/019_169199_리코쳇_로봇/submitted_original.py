from collections import deque

def solution(board):
    rows, cols = len(board), len(board[0])
    distance = [[-1] * cols for _ in range(rows)]
    queue = deque()
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'R':
                distance[r][c] = 0
                queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        if board[r][c] == 'G':
            return distance[r][c]
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r, c
            while 0 <= nr + dr < rows and 0 <= nc + dc < cols and board[nr + dr][nc + dc] != 'D':
                nr += dr
                nc += dc
            if distance[nr][nc] == -1:
                distance[nr][nc] = distance[r][c] + 1
                queue.append((nr, nc))
    return -1

# 전체 코드 줄별 설명
# from collections import deque  # from~import는 기능 가져오기. collections의 deque는 양끝 삽입·삭제가 빠른 큐 자료구조.
# 
# def solution(board):  # def는 함수 정의, ()의 board는 문자열로 된 게임판 입력.
#     rows, cols = len(board), len(board[0])  # len은 길이, [0]은 첫 행. 행·열 수를 각각 대입.
#     distance = [[-1] * cols for _ in range(rows)]  # 리스트 내포로 독립된 행 생성. -1은 미방문, _는 사용하지 않는 반복 변수.
#     queue = deque()  # 먼저 들어온 위치부터 처리하는 빈 큐 생성.
#     for r in range(rows):  # range(n)은 0~n-1. 시작 위치를 찾기 위해 행 순회.
#         for c in range(cols):  # 중첩 for로 열 순회.
#             if board[r][c] == 'R':  # [][]는 행·열 접근, ==는 같음. 로봇 시작 칸 검사.
#                 distance[r][c] = 0  # 시작 위치의 이동 횟수를 0으로 저장.
#                 queue.append((r, c))  # append는 오른쪽 추가, () 튜플로 좌표 묶기.
#     while queue:  # 큐가 비지 않은 동안 반복. 빈 deque는 거짓.
#         r, c = queue.popleft()  # popleft는 왼쪽에서 꺼내 삭제. 좌표를 두 변수로 언패킹.
#         if board[r][c] == 'G':  # if는 조건 분기. 목표에서 멈췄는지 검사.
#             return distance[r][c]  # BFS의 첫 도착이 최소 이동 횟수이므로 반환.
#         for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):  # 네 방향의 이동량 튜플을 순회.
#             nr, nc = r, c  # 현재 위치에서 미끄러지기 시작.
#             while 0 <= nr + dr < rows and 0 <= nc + dc < cols and board[nr + dr][nc + dc] != 'D':  # 연쇄 비교는 범위, and는 모두 참, !=는 다름. 다음 칸으로 갈 수 있는 동안 이동.
#                 nr += dr  # +=는 더해 저장. 행 이동.
#                 nc += dc  # 열 이동. 장애물 직전 또는 경계에서 멈춤.
#             if distance[nr][nc] == -1:  # 멈춘 위치가 아직 방문하지 않은 칸인지 검사.
#                 distance[nr][nc] = distance[r][c] + 1  # 미끄러지기 한 번을 이동 횟수 1로 계산.
#                 queue.append((nr, nc))  # 새 정지 위치를 큐 끝에 넣어 다음 거리 순으로 탐색.
#     return -1  # 가능한 정지 위치를 모두 찾아도 목표가 없으면 -1 반환.

# 풀이 요약
# 멈출 수 있는 위치를 정점으로 보고 한 번 미끄러지는 이동을 간선으로 삼아 너비 우선 탐색합니다.
# 예: 첫 게임판은 7번, 둘째는 목표에서 멈출 수 없어 -1. 시간 O(행*열*max(행,열)), 공간 O(행*열).
