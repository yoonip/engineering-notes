from collections import Counter

def normalize(cells):
    min_row = min(row for row, col in cells)
    min_col = min(col for row, col in cells)
    return tuple(sorted((row - min_row, col - min_col) for row, col in cells))

def shape(cells):
    forms = []
    for _ in range(4):
        forms.append(normalize(cells))
        cells = [(col, -row) for row, col in cells]
    return min(forms)

def components(board, target):
    n = len(board)
    visited = [[False] * n for _ in range(n)]
    result = []
    for row in range(n):
        for col in range(n):
            if visited[row][col] or board[row][col] != target:
                continue
            visited[row][col] = True
            stack = [(row, col)]
            cells = []
            while stack:
                r, c = stack.pop()
                cells.append((r, c))
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc] and board[nr][nc] == target:
                        visited[nr][nc] = True
                        stack.append((nr, nc))
            result.append(shape(cells))
    return result

def solution(game_board, table):
    pieces = Counter(components(table, 1))
    answer = 0
    for hole in components(game_board, 0):
        if pieces[hole] > 0:
            answer += len(hole)
            pieces[hole] -= 1
    return answer

# 전체 코드 줄별 설명
# from collections import Counter  # import는 도구 가져오기. Counter는 원소별 개수를 세는 딕셔너리형 자료구조.
# 
# def normalize(cells):  # def는 함수 정의. 좌표 목록을 같은 기준점으로 옮기는 함수.
#     min_row = min(row for row, col in cells)  # min은 최솟값, 괄호 안 생성식은 각 좌표의 행만 차례로 꺼냄.
#     min_col = min(col for row, col in cells)  # 가장 왼쪽 열의 좌표를 구함. for의 두 변수는 튜플 언패킹.
#     return tuple(sorted((row - min_row, col - min_col) for row, col in cells))  # sorted는 정렬, tuple은 변경 불가 묶음. 위치와 탐색 순서의 차이를 제거.
# 
# def shape(cells):  # 회전해도 같다고 판단할 대표 모양을 만드는 함수.
#     forms = []  # []는 리스트. 네 방향의 모양을 저장.
#     for _ in range(4):  # range(4)는 0~3. _는 쓰지 않는 반복 변수.
#         forms.append(normalize(cells))  # append는 리스트 끝에 추가. 현재 방향의 표준 좌표를 저장.
#         cells = [(col, -row) for row, col in cells]  # 리스트 컴프리헨션. (행,열)을 90도 회전한 좌표로 변환.
#     return min(forms)  # 튜플은 앞 원소부터 비교 가능. 네 방향 중 가장 작은 것을 대표값으로 선택.
# 
# def components(board, target):  # board에서 target 값으로 연결된 덩어리를 추출.
#     n = len(board)  # len은 길이를 반환. 정사각형 한 변의 칸 수.
#     visited = [[False] * n for _ in range(n)]  # 중첩 리스트로 방문 표 생성. False는 아직 방문하지 않았다는 불리언 값.
#     result = []  # 각 덩어리의 대표 모양을 담을 리스트.
#     for row in range(n):  # 모든 행을 순회.
#         for col in range(n):  # 각 행의 모든 열을 순회.
#             if visited[row][col] or board[row][col] != target:  # or는 둘 중 하나가 참, !=는 다름. 이미 방문했거나 대상이 아니면 제외.
#                 continue  # 이번 반복만 건너뛰고 다음 칸으로 이동.
#             visited[row][col] = True  # =는 대입. 탐색에 넣는 시점에 방문 처리해 중복 삽입 방지.
#             stack = [(row, col)]  # 리스트를 스택으로 사용. ()는 두 좌표를 묶은 튜플.
#             cells = []  # 현재 덩어리의 모든 좌표를 저장.
#             while stack:  # 리스트가 비어 있지 않은 동안 반복하는 깊이 우선 탐색(DFS).
#                 r, c = stack.pop()  # pop은 마지막 원소를 꺼내 삭제. 좌표를 두 변수에 나눠 대입.
#                 cells.append((r, c))  # 현재 칸을 덩어리에 추가.
#                 for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):  # 상하좌우 네 방향의 변화량을 순회.
#                     nr, nc = r + dr, c + dc  # 인접 칸의 행과 열 계산.
#                     if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc] and board[nr][nc] == target:  # and는 모두 참, not은 부정, ==는 같음. 범위·미방문·대상 여부 검사.
#                         visited[nr][nc] = True  # 새 칸을 방문 표시.
#                         stack.append((nr, nc))  # 스택에 넣어 나중에 탐색.
#             result.append(shape(cells))  # 완성된 덩어리를 회전 기준으로 표준화해 저장.
#     return result  # 발견한 모든 덩어리의 모양 반환.
# 
# def solution(game_board, table):  # 프로그래머스가 호출하는 정답 함수.
#     pieces = Counter(components(table, 1))  # 테이블의 조각을 모양별로 세기. 딕셔너리 키에는 튜플 사용 가능.
#     answer = 0  # 채운 칸 수를 0으로 시작.
#     for hole in components(game_board, 0):  # 게임 보드의 빈 공간 덩어리를 차례로 확인.
#         if pieces[hole] > 0:  # []는 키로 조회. Counter는 없는 키의 개수를 0으로 돌려줌.
#             answer += len(hole)  # +=는 더해 저장. 모양이 같으면 빈 공간 전체를 채움.
#             pieces[hole] -= 1  # -=는 빼서 저장. 사용한 조각 한 개 차감.
#     return answer  # 최대한 채운 칸 수 반환.

# 풀이 요약
# DFS로 빈 공간과 조각을 추출하고, 회전한 네 모양을 같은 대표값으로 바꿔 Counter로 일치시킨다.
# 예: 4칸짜리 빈 공간과 회전해서 같은 4칸 조각이 만나면 4칸 추가하고 조각 수를 하나 줄인다. 반사는 허용하지 않는다.
# 조각 크기는 최대 6이므로 시간·공간 O(N²). 동일한 빈 공간에는 동일 모양 조각만 들어가므로 개수만 맞추면 된다.
# 