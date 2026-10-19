def solution(maps):
    board = [list(row) for row in maps]
    rows, cols = len(board), len(board[0])
    answer = []
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'X':
                continue
            food = int(board[r][c])
            board[r][c] = 'X'
            stack = [(r, c)]
            while stack:
                x, y = stack.pop()
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and board[nx][ny] != 'X':
                        food += int(board[nx][ny])
                        board[nx][ny] = 'X'
                        stack.append((nx, ny))
            answer.append(food)
    return sorted(answer) if answer else [-1]

# 전체 코드 줄별 설명
# def solution(maps):  # def는 함수 정의, maps는 지도 문자열 리스트 입력.
#     board = [list(row) for row in maps]  # 리스트 내포로 각 문자열을 수정 가능한 문자 리스트로 변환.
#     rows, cols = len(board), len(board[0])  # len은 길이. 행·열 수를 각각 대입.
#     answer = []  # []는 빈 리스트. 섬별 식량 합 저장.
#     for r in range(rows):  # range(n)은 0~n-1. 행 순회.
#         for c in range(cols):  # 중첩 for로 열 순회.
#             if board[r][c] == 'X':  # [][]는 칸 접근, ==는 같음. 바다 또는 방문 칸 검사.
#                 continue  # continue로 이번 칸을 건너뜀.
#             food = int(board[r][c])  # int는 문자열을 정수로 변환. 섬 첫 칸의 식량 저장.
#             board[r][c] = 'X'  # =로 방문 표시. 같은 칸 중복 탐색 방지.
#             stack = [(r, c)]  # []는 스택용 리스트, ()는 좌표 튜플.
#             while stack:  # 스택이 비지 않은 동안 반복.
#                 x, y = stack.pop()  # pop은 마지막 좌표를 꺼내 삭제. 두 값 언패킹.
#                 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):  # 네 방향 이동량 순회.
#                     nx, ny = x + dx, y + dy  # 이웃 좌표 계산.
#                     if 0 <= nx < rows and 0 <= ny < cols and board[nx][ny] != 'X':  # 연쇄 비교는 범위, and는 모두 참, !=는 다름. 방문 가능한 이웃 검사.
#                         food += int(board[nx][ny])  # +=는 더해 저장. 이웃의 식량 누적.
#                         board[nx][ny] = 'X'  # 스택에 넣기 전에 방문 처리.
#                         stack.append((nx, ny))  # append로 탐색할 이웃 좌표 추가.
#             answer.append(food)  # 완성한 한 섬의 식량 합을 결과에 추가.
#     return sorted(answer) if answer else [-1]  # sorted는 오름차순 새 리스트. 조건 표현식으로 섬이 없으면 [-1] 반환.

# 풀이 요약
# 상하좌우로 연결된 땅을 스택으로 탐색하며 식량을 합산합니다. 방문한 땅은 X로 바꿔 한 번만 셉니다.
# 예: 섬의 합 27,1,1을 정렬해 [1,1,27]. 칸 수 V, 섬 수 K일 때 시간 O(V+K log K), 공간 O(V).
