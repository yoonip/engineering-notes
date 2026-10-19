def solution(land):
    rows, cols = len(land), len(land[0])
    totals = [0] * cols
    for r in range(rows):
        for c in range(cols):
            if land[r][c] == 0:
                continue
            stack = [(r, c)]
            land[r][c] = 0
            columns = set()
            size = 0
            while stack:
                x, y = stack.pop()
                size += 1
                columns.add(y)
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and land[nx][ny] == 1:
                        land[nx][ny] = 0
                        stack.append((nx, ny))
            for column in columns:
                totals[column] += size
    return max(totals)

# 전체 코드 줄별 설명
# def solution(land):  # def는 함수 정의. () 안 land는 땅의 2차원 리스트 입력.
#     rows, cols = len(land), len(land[0])  # len은 길이, [0]은 첫 행. 쉼표로 높이·너비를 각각 대입.
#     totals = [0] * cols  # [0]을 cols번 반복한 리스트로 열별 석유량 초기화.
#     for r in range(rows):  # range(n)은 0부터 n-1까지. 각 행을 순회.
#         for c in range(cols):  # 중첩 for로 각 열을 순회. 들여쓰기로 포함 관계 표시.
#             if land[r][c] == 0:  # [][]는 행·열 접근, ==는 같음. 빈 땅 또는 방문한 칸 검사.
#                 continue  # continue는 이번 반복을 건너뜀.
#             stack = [(r, c)]  # []는 리스트, (r,c)는 좌표 튜플. 탐색할 칸을 스택에 저장.
#             land[r][c] = 0  # 방문 표시로 0 대입. 같은 석유를 중복 탐색하지 않음.
#             columns = set()  # set()은 중복 없는 빈 집합. 덩어리가 지나는 열을 저장.
#             size = 0  # 현재 석유 덩어리의 크기 초기화.
#             while stack:  # while은 조건 반복. 스택이 비면 거짓이 되어 종료.
#                 x, y = stack.pop()  # pop()은 리스트 마지막 값을 꺼내 삭제. 튜플을 두 변수로 언패킹.
#                 size += 1  # +=는 더해서 저장. 방문 칸 수 증가.
#                 columns.add(y)  # add는 집합 원소 추가. 같은 열은 한 번만 남음.
#                 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):  # 튜플에 담은 상하좌우 이동량을 순회.
#                     nx, ny = x + dx, y + dy  # +로 이웃 좌표 계산하고 두 변수에 대입.
#                     if 0 <= nx < rows and 0 <= ny < cols and land[nx][ny] == 1:  # 연쇄 비교는 범위 검사, and는 모든 조건이 참일 때만 통과.
#                         land[nx][ny] = 0  # 스택에 넣기 전에 방문 표시해 중복 추가 방지.
#                         stack.append((nx, ny))  # append는 리스트 끝에 추가. 이웃 칸을 스택에 넣음.
#             for column in columns:  # 집합에 있는 서로 다른 열을 순회.
#                 totals[column] += size  # 덩어리를 지나는 각 열에 전체 크기를 한 번씩 더함.
#     return max(totals)  # max는 최댓값, return은 결과 반환. 가장 많은 석유량을 선택.

# 풀이 요약
# 연결된 석유를 깊이 우선 탐색해 크기와 지나는 열을 구하고, 각 열의 합에 크기를 더합니다.
# 예: 7번 열이 크기 7과 2 덩어리를 지나면 9. 각 덩어리는 열마다 한 번만 더합니다. 시간·공간 O(행*열).
