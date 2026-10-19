def solution(m, n, picture):
    grid = [row[:] for row in picture]
    areas = largest = 0
    for row in range(m):
        for col in range(n):
            color = grid[row][col]
            if color == 0:
                continue
            areas += 1
            grid[row][col] = 0
            stack = [(row, col)]
            size = 0
            while stack:
                r, c = stack.pop()
                size += 1
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == color:
                        grid[nr][nc] = 0
                        stack.append((nr, nc))
            largest = max(largest, size)
    return [areas, largest]

# 전체 코드 줄별 설명
# def solution(m, n, picture):  # def는 함수 정의. 행·열 수와 색 번호 격자 입력.
#     grid = [row[:] for row in picture]  # []는 리스트 컴프리헨션, [:]는 각 행 복사. 원래 그림을 보존하며 방문 칸을 지울 준비.
#     areas = largest = 0  # 연쇄 대입. 영역 개수·최대 영역 넓이 초기화.
#     for row in range(m):  # range는 정수 범위. 모든 행 순회.
#         for col in range(n):  # 모든 열 순회.
#             color = grid[row][col]  # []로 현재 색 조회.
#             if color == 0:  # ==는 같음. 빈칸이거나 이미 방문한 칸은 제외.
#                 continue  # 이번 칸을 건너뜀.
#             areas += 1  # +=는 더해 저장. 새 연결 영역 발견.
#             grid[row][col] = 0  # 스택에 넣는 즉시 방문 표시.
#             stack = [(row, col)]  # 리스트를 후입선출 스택으로 사용. ()는 좌표 튜플.
#             size = 0  # 현재 영역 넓이 초기화.
#             while stack:  # 스택에 원소가 있는 동안 깊이 우선 탐색(DFS).
#                 r, c = stack.pop()  # pop은 마지막 원소를 꺼내 삭제. 좌표 언패킹.
#                 size += 1  # 현재 영역에 칸 하나 추가.
#                 for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):  # 상하좌우 이동 변화량 순회.
#                     nr, nc = r + dr, c + dc  # 이웃 좌표 계산.
#                     if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == color:  # and는 모두 참. 범위 안이고 같은 색인 미방문 칸만 허용.
#                         grid[nr][nc] = 0  # 방문 표시해 중복 추가 방지.
#                         stack.append((nr, nc))  # append는 스택 끝에 추가.
#             largest = max(largest, size)  # max는 최댓값. 완성한 영역 넓이 반영.
#     return [areas, largest]  # 영역 수·최대 넓이를 순서대로 리스트 반환.

# 풀이 요약
# 0이 아닌 미방문 칸을 찾으면 새 영역을 시작하고 같은 색의 상하좌우 칸을 DFS로 전부 탐색한다. 영역별 넓이를 세어 최대값을 갱신한다.
# 방문한 칸은 복사한 그림에서 0으로 지워 재방문을 막는다. 대각선만 맞닿은 같은 색은 별개 영역이다.
# 예제는 영역 4개·최대 넓이 5. 모든 칸을 한 번씩 방문하므로 시간 O(MN), 그림 복사와 스택 공간 O(MN).
# 