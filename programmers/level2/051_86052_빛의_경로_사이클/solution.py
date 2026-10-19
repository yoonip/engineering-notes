def solution(grid):
    rows, cols = len(grid), len(grid[0])
    visited = [bytearray(cols * 4) for _ in range(rows)]
    directions = ((-1, 0), (0, 1), (1, 0), (0, -1))
    answer = []
    for r in range(rows):
        for c in range(cols):
            for direction in range(4):
                if visited[r][c * 4 + direction]:
                    continue
                x, y, d, length = r, c, direction, 0
                while not visited[x][y * 4 + d]:
                    visited[x][y * 4 + d] = 1
                    length += 1
                    if grid[x][y] == 'L':
                        d = (d - 1) % 4
                    elif grid[x][y] == 'R':
                        d = (d + 1) % 4
                    dx, dy = directions[d]
                    x, y = (x + dx) % rows, (y + dy) % cols
                answer.append(length)
    return sorted(answer)

# 전체 코드 줄별 설명
# def solution(grid):  # def는 함수 정의. grid는 방향 전환 문자가 담긴 격자 입력.
#     rows, cols = len(grid), len(grid[0])  # len은 길이. 높이·너비 각각 대입.
#     visited = [bytearray(cols * 4) for _ in range(rows)]  # bytearray(n)은 0으로 채운 수정 가능한 바이트 배열. 리스트 내포로 각 행의 네 방향 방문 상태 생성.
#     directions = ((-1, 0), (0, 1), (1, 0), (0, -1))  # () 튜플에 위·오른쪽·아래·왼쪽 이동량 저장.
#     answer = []  # []는 빈 리스트. 각 사이클 길이 저장.
#     for r in range(rows):  # range(n)은 0~n-1. 시작 행 순회.
#         for c in range(cols):  # 시작 열 순회.
#             for direction in range(4):  # 같은 칸의 네 진행 방향도 서로 다른 상태로 검사.
#                 if visited[r][c * 4 + direction]:  # []는 접근. 0은 거짓, 방문한 1은 참.
#                     continue  # continue로 이미 처리한 상태 건너뜀.
#                 x, y, d, length = r, c, direction, 0  # 현재 좌표·방향·길이를 각각 대입.
#                 while not visited[x][y * 4 + d]:  # while은 반복, not은 반전. 방문 상태를 만날 때까지 이동.
#                     visited[x][y * 4 + d] = 1  # 현재 (칸,방향) 방문 표시.
#                     length += 1  # +=는 더해 저장. 경로 길이 증가.
#                     if grid[x][y] == 'L':  # ==는 같음. 현재 칸이 좌회전인지 검사.
#                         d = (d - 1) % 4  # %는 나머지. 방향 번호를 왼쪽으로 순환 이동.
#                     elif grid[x][y] == 'R':  # elif는 앞 조건이 거짓일 때 검사. 우회전 처리.
#                         d = (d + 1) % 4  # 오른쪽으로 방향 번호 한 칸 이동. S면 그대로 유지.
#                     dx, dy = directions[d]  # 방향에 해당하는 이동량 튜플 언패킹.
#                     x, y = (x + dx) % rows, (y + dy) % cols  # 나머지 연산으로 경계 밖 이동을 반대편으로 연결.
#                 answer.append(length)  # append로 한 사이클의 길이 저장.
#     return sorted(answer)  # sorted는 오름차순 새 리스트. return으로 길이 목록 반환.

# 풀이 요약
# (칸,진행 방향)을 상태로 탐색합니다. 각 상태의 다음·이전 상태가 유일하므로 미방문 상태에서 출발하면 하나의 사이클을 얻습니다.
# 예: ['SL','LR']은 16, ['S']는 길이 1 네 개. 상태 수 V=4*행*열, 사이클 수 K일 때 시간 O(V+K log K), 공간 O(V).
