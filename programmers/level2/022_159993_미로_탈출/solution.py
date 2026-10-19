from collections import deque

def solution(maps):
    rows, cols = len(maps), len(maps[0])
    positions = {}
    for r in range(rows):
        for c in range(cols):
            if maps[r][c] in 'SLE':
                positions[maps[r][c]] = (r, c)
    def bfs(start, goal):
        queue = deque([(start[0], start[1], 0)])
        visited = {start}
        while queue:
            r, c, distance = queue.popleft()
            if (r, c) == goal:
                return distance
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and maps[nr][nc] != 'X' and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc, distance + 1))
        return -1
    first = bfs(positions['S'], positions['L'])
    second = bfs(positions['L'], positions['E'])
    return first + second if first >= 0 and second >= 0 else -1

# 전체 코드 줄별 설명
# from collections import deque  # collections 모듈에서 양끝 삽입·삭제가 빠른 큐 deque를 import로 가져옴.
# 
# def solution(maps):  # def는 함수 정의, maps는 미로 문자열 리스트 입력.
#     rows, cols = len(maps), len(maps[0])  # len은 길이. 행 수·열 수를 각각 대입.
#     positions = {}  # {}는 빈 딕셔너리. 시작·레버·출구 좌표를 문자 키에 연결.
#     for r in range(rows):  # range(n)은 0~n-1. 행 순회.
#         for c in range(cols):  # 중첩 for로 열 순회.
#             if maps[r][c] in 'SLE':  # [][]는 칸 접근, in은 포함 여부. 특별한 칸인지 검사.
#                 positions[maps[r][c]] = (r, c)  # [키]에 () 좌표 튜플 저장.
#     def bfs(start, goal):  # 중첩 함수 정의. 두 좌표 사이의 최단 거리 계산.
#         queue = deque([(start[0], start[1], 0)])  # 큐에 (행,열,거리) 튜플을 담아 시작.
#         visited = {start}  # {원소}는 집합. 이미 방문한 좌표를 중복 없이 저장.
#         while queue:  # 큐가 비지 않은 동안 반복.
#             r, c, distance = queue.popleft()  # popleft는 먼저 들어온 값을 꺼내 삭제. 세 값을 언패킹.
#             if (r, c) == goal:  # ==는 같음. 현재 좌표가 목표인지 검사.
#                 return distance  # 처음 도착한 거리가 최단 거리이므로 반환.
#             for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):  # 상하좌우 이동량 순회.
#                 nr, nc = r + dr, c + dc  # 이웃 좌표 계산·대입.
#                 if 0 <= nr < rows and 0 <= nc < cols and maps[nr][nc] != 'X' and (nr, nc) not in visited:  # 연쇄 비교는 범위, and는 모두 참, !=는 다름, not in은 미포함 검사.
#                     visited.add((nr, nc))  # add는 집합 원소 추가. 이웃을 방문 표시.
#                     queue.append((nr, nc, distance + 1))  # append로 거리 1 증가한 이웃을 큐 끝에 추가.
#         return -1  # 경로를 찾지 못하면 -1 반환.
#     first = bfs(positions['S'], positions['L'])  # 시작에서 레버까지 BFS 함수 호출.
#     second = bfs(positions['L'], positions['E'])  # 레버에서 출구까지 별도 최단 거리 계산.
#     return first + second if first >= 0 and second >= 0 else -1  # 조건 표현식 a if 조건 else b. 두 경로가 모두 있을 때 합, 아니면 -1.

# 풀이 요약
# 시작→레버와 레버→출구의 최단 거리를 각각 BFS로 구해 더합니다. 어느 한 경로라도 없으면 탈출 불가입니다.
# 예: 첫 미로는 4+12=16초. 레버 전에도 출구 칸은 통과할 수 있습니다. 시간·공간 O(행*열).
