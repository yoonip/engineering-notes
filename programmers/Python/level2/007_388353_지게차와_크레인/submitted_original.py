from collections import deque


def solution(storage, requests):
    n, m = len(storage), len(storage[0])
    board = [['.'] * (m + 2)]
    for row in storage:
        board.append(['.'] + list(row) + ['.'])
    board.append(['.'] * (m + 2))
    remaining = n * m
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

    for request in requests:
        target = request[0]
        removed = []
        if len(request) == 2:
            for r in range(1, n + 1):
                for c in range(1, m + 1):
                    if board[r][c] == target:
                        removed.append((r, c))
        else:
            visited = [[False] * (m + 2) for _ in range(n + 2)]
            visited[0][0] = True
            queue = deque([(0, 0)])
            while queue:
                r, c = queue.popleft()
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if not (0 <= nr < n + 2 and 0 <= nc < m + 2):
                        continue
                    if visited[nr][nc]:
                        continue
                    visited[nr][nc] = True
                    if board[nr][nc] == '.':
                        queue.append((nr, nc))
                    elif board[nr][nc] == target:
                        removed.append((nr, nc))

        for r, c in removed:
            board[r][c] = '.'
        remaining -= len(removed)

    return remaining

# 전체 코드 줄별 설명 (아래는 모두 실행되지 않는 주석입니다.)
# from collections import deque  # from~import는 모듈의 이름을 가져오는 문법. collections는 컨테이너 모듈, deque는 양끝 삽입·삭제가 빠른 큐 자료구조.
#
#
# def solution(storage, requests):  # def는 함수 정의. storage·requests는 입력, : 아래 들여쓰기는 함수 본문.
#     n, m = len(storage), len(storage[0])  # len은 원소 수, [0]은 첫 행 접근. 쉼표 언패킹으로 행·열 수 저장.
#     board = [['.'] * (m + 2)]  # '.'은 빈칸 문자열. []는 리스트, *는 반복. 맨 위 바깥 행 생성.
#     for row in storage:  # for~in으로 창고의 행 문자열을 하나씩 순회.
#         board.append(['.'] + list(row) + ['.'])  # list는 문자열을 문자 리스트로 변환, +는 리스트 연결, append는 행을 끝에 추가.
#     board.append(['.'] * (m + 2))  # 아래쪽 바깥 행도 추가해 창고를 빈칸으로 둘러쌈.
#     remaining = n * m  # *는 곱셈. 남은 컨테이너 수 초기화.
#     directions = ((1, 0), (-1, 0), (0, 1), (0, -1))  # ()는 튜플. 상하좌우 이동량 네 쌍을 저장.
#
#     for request in requests:  # 요청을 입력 순서대로 순회.
#         target = request[0]  # [0]은 첫 문자 인덱싱. 제거할 컨테이너 종류를 읽음.
#         removed = []  # []는 빈 리스트. 이번 요청에서 제거할 좌표를 저장.
#         if len(request) == 2:  # if는 조건문, ==는 같음. 두 글자면 크레인 요청.
#             for r in range(1, n + 1):  # range(1,n+1)은 1부터 n까지. 실제 창고 행 순회.
#                 for c in range(1, m + 1):  # 실제 창고 열 1부터 m까지 순회.
#                     if board[r][c] == target:  # [][]는 행·열 접근. 목표 종류인지 비교.
#                         removed.append((r, c))  # (r,c) 좌표 튜플을 제거 목록 끝에 추가.
#         else:  # else는 앞 if가 거짓일 때 실행. 지게차 요청 처리.
#             visited = [[False] * (m + 2) for _ in range(n + 2)]  # 리스트 컴프리헨션으로 각 행을 따로 생성. False는 미방문, _는 안 쓸 변수.
#             visited[0][0] = True  # 바깥 시작 칸 방문 처리. True는 참.
#             queue = deque([(0, 0)])  # deque를 (0,0) 하나로 초기화. queue는 먼저 넣은 것을 먼저 꺼내는 FIFO 큐 변수.
#             while queue:  # while은 조건 반복. 큐가 비지 않은 동안 실행.
#                 r, c = queue.popleft()  # popleft()는 큐 왼쪽 원소를 제거·반환. 쉼표로 좌표 두 값을 언패킹.
#                 for dr, dc in directions:  # 상하좌우 이동량을 순회하며 두 변수에 풀어 받음.
#                     nr, nc = r + dr, c + dc  # +로 이동 후의 행·열 좌표 계산.
#                     if not (0 <= nr < n + 2 and 0 <= nc < m + 2):  # 연쇄 비교로 범위 검사, and는 둘 다 참, not은 참·거짓 부정. 범위 밖이면 실행.
#                         continue  # continue는 이번 방향을 건너뛰고 다음 방향으로 진행.
#                     if visited[nr][nc]:  # 이미 방문한 좌표인지 확인.
#                         continue  # 방문한 좌표는 건너뜀.
#                     visited[nr][nc] = True  # 현재 좌표를 방문 처리해 중복 확인 방지.
#                     if board[nr][nc] == '.':  # '.'인지 비교해 통과 가능한 빈 공간인지 확인.
#                         queue.append((nr, nc))  # 빈 공간 좌표를 큐 오른쪽 끝에 추가.
#                     elif board[nr][nc] == target:  # elif는 앞 조건이 거짓일 때의 추가 조건. 목표 컨테이너인지 확인.
#                         removed.append((nr, nc))  # 외부 빈 공간에 닿은 목표를 제거 목록에만 기록. 아직 지우지 않음.
#
#         for r, c in removed:  # 탐색이 끝난 후 제거 목록의 좌표를 순회.
#             board[r][c] = '.'  # 해당 칸을 빈칸 '.'으로 대입. 동시에 제거되는 효과를 유지.
#         remaining -= len(removed)  # -=는 빼서 저장. 제거한 개수만큼 남은 수 감소.
#
#     return remaining  # return으로 남은 컨테이너 수 반환.

# 풀이 요약
# 크레인은 목표 종류를 모두 제거하고, 지게차는 바깥 빈칸에서 BFS(가까운 칸부터 큐로 탐색)해 닿는 목표만 제거합니다.
# 한 요청의 탐색이 끝난 뒤 한꺼번에 지워, 방금 열린 통로를 같은 요청에서 사용하지 않게 합니다.
# 예: A로 가득한 3x3 창고에서 요청 A 한 번이면 바깥 8개만 빠져 1개가 남습니다. 시간 O(요청 수*행*열).
