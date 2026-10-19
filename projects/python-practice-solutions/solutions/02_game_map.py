# 게임 맵 최단거리
# 분류: BFS / deque
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/1844
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

from collections import deque


def solution(maps):
    rows = len(maps)
    cols = len(maps[0])
    distance = [[-1] * cols for _ in range(rows)]
    distance[0][0] = 1
    queue = deque([(0, 0)])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        row, col = queue.popleft()

        if row == rows - 1 and col == cols - 1:
            return distance[row][col]

        for dr, dc in directions:
            next_row = row + dr
            next_col = col + dc

            if not (0 <= next_row < rows and 0 <= next_col < cols):
                continue

            if maps[next_row][next_col] == 0:
                continue

            if distance[next_row][next_col] != -1:
                continue

            distance[next_row][next_col] = distance[row][col] + 1
            queue.append((next_row, next_col))

    return -1


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# from collections import deque  # from 모듈 import 이름: collections에서 양끝 큐 자료형 deque를 가져옵니다.
#
#
# def solution(maps):  # def로 함수를 정의합니다. maps는 채점기가 전달하는 2차원 리스트입니다.
#     rows = len(maps)  # len은 원소 수를 구합니다. maps의 원소는 행이므로 전체 행 수입니다.
#     cols = len(maps[0])  # maps[0]은 첫 행입니다. 그 행의 원소 수는 열 수입니다.
#     distance = [[-1] * cols for _ in range(rows)]  # 리스트 컴프리헨션으로 독립된 행들을 만듭니다. -1은 아직 방문하지 않았다는 표시입니다.
#     distance[0][0] = 1  # 리스트[행][열]로 값을 대입합니다. 시작 칸도 지나간 칸 수에 포함하므로 1입니다.
#     queue = deque([(0, 0)])  # deque에 시작 좌표 튜플 (0,0)을 넣습니다. 튜플은 값들을 묶으며 원소를 변경할 수 없습니다.
#     directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 리스트에 네 방향의 (행 변화량, 열 변화량) 튜플을 담습니다.
#
#     while queue:  # 큐가 비어 있지 않은 동안 반복합니다. 빈 큐는 조건에서 거짓으로 평가됩니다.
#         row, col = queue.popleft()  # popleft는 맨 왼쪽 항목을 꺼냅니다. 좌표 두 값을 언패킹하여 각각 대입합니다.
#
#         if row == rows - 1 and col == cols - 1:  # ==는 같은지 비교합니다. and는 두 조건이 모두 참이어야 참입니다. 마지막 행과 열인지 확인합니다.
#             return distance[row][col]  # 해당 칸까지의 칸 수를 반환하고 함수 전체를 종료합니다.
#
#         for dr, dc in directions:  # 튜플의 두 값을 각각 dr,dc에 받아 방향마다 반복합니다.
#             next_row = row + dr  # 현재 행 번호에 행 변화량을 더하여 다음 행 번호를 저장합니다.
#             next_col = col + dc  # 현재 열 번호에 열 변화량을 더하여 다음 열 번호를 저장합니다.
#
#             if not (0 <= next_row < rows and 0 <= next_col < cols):  # 연속 비교는 범위를 확인하고 not은 참과 거짓을 뒤집습니다. 격자 밖인지 확인합니다.
#                 continue  # 현재 반복의 남은 코드를 건너뛰고 가장 가까운 반복문의 다음 반복으로 갑니다.
#
#             if maps[next_row][next_col] == 0:  # 다음 칸의 값이 숫자 0인지 비교합니다. 0이면 벽입니다.
#                 continue  # 현재 반복의 남은 코드를 건너뛰고 가장 가까운 반복문의 다음 반복으로 갑니다.
#
#             if distance[next_row][next_col] != -1:  # !=는 같지 않다는 비교입니다. -1이 아니면 이미 방문했습니다.
#                 continue  # 현재 반복의 남은 코드를 건너뛰고 가장 가까운 반복문의 다음 반복으로 갑니다.
#
#             distance[next_row][next_col] = distance[row][col] + 1  # 현재 칸까지의 칸 수에 1을 더하여 다음 칸의 거리를 기록합니다.
#             queue.append((next_row, next_col))  # append는 맨 오른쪽에 추가합니다. 두 좌표를 튜플로 묶어 큐에 넣습니다.
#
#     return -1  # 끝까지 도착하지 못했을 때 정수 -1을 반환합니다.
