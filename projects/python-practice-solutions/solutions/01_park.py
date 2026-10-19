# 공원 산책
# 분류: 격자 시뮬레이션
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/172928
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

def solution(park, routes):
    height = len(park)
    width = len(park[0])

    row, col = 0, 0
    for r, line in enumerate(park):
        if "S" in line:
            row, col = r, line.index("S")
            break

    directions = {
        "N": (-1, 0),
        "S": (1, 0),
        "W": (0, -1),
        "E": (0, 1),
    }

    for route in routes:
        direction, distance = route.split()
        distance = int(distance)
        dr, dc = directions[direction]

        next_row, next_col = row, col
        valid = True

        for _ in range(distance):
            next_row += dr
            next_col += dc

            if not (0 <= next_row < height and 0 <= next_col < width):
                valid = False
                break

            if park[next_row][next_col] == "X":
                valid = False
                break

        if valid:
            row, col = next_row, next_col

    return [row, col]


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# # def는 함수를 정의합니다. park, routes는 입력을 전달받는 매개변수입니다.
# # 콜론 다음의 들여쓴 부분이 함수에 속합니다. 별도 import는 필요 없습니다.
# def solution(park, routes):
#     # len(리스트)는 원소 개수를 반환합니다. park의 각 원소는 행 문자열입니다.
#     height = len(park)
#     # park[0]은 첫 행 문자열, len(문자열)은 문자 개수이므로 공원의 열 수입니다.
#     width = len(park[0])
#
#     # 두 변수에 0을 각각 대입합니다. row는 현재 행, col은 현재 열입니다.
#     row, col = 0, 0
#     # enumerate는 (인덱스, 원소) 튜플을 순서대로 제공합니다. 인덱스는 0부터입니다.
#     # r, line은 두 값을 각각 받는 언패킹 문법입니다.
#     for r, line in enumerate(park):
#         # '문자열 in 문자열'은 왼쪽 문자열이 오른쪽에 포함되는지 확인합니다.
#         if "S" in line:
#             # 문자열.index("S")는 S가 처음 나오는 위치 번호를 반환합니다.
#             # 위에서 포함 여부를 확인했으므로 여기서는 S가 존재합니다.
#             row, col = r, line.index("S")
#             # break는 가장 가까운 반복문 하나를 종료합니다. 여기서는 시작점 탐색입니다.
#             break
#
#     # {키: 값, ...}은 딕셔너리입니다. 방향 문자열과 이동 변화량을 연결합니다.
#     # (-1,0)처럼 괄호로 묶은 두 값은 튜플입니다. 원소를 바꿀 수 없는 묶음입니다.
#     # 각 튜플은 (행 변화량, 열 변화량)입니다.
#     # 아래로 갈수록 행 번호가 커지고, 오른쪽으로 갈수록 열 번호가 커집니다.
#     directions = {
#         "N": (-1, 0),
#         "S": (1, 0),
#         "W": (0, -1),
#         "E": (0, 1),
#     }
#
#     # for는 routes에서 문자열을 하나씩 꺼내 route에 대입하며 반복합니다.
#     for route in routes:
#         # split()은 공백을 기준으로 나눕니다. "E 2" → ["E", "2"]
#         # 두 원소를 direction과 distance에 각각 대입합니다.
#         direction, distance = route.split()
#         # int는 숫자 문자열을 정수로 바꿉니다. "2" → 2
#         distance = int(distance)
#         # 딕셔너리[키]로 튜플을 꺼내 두 변수에 언패킹합니다.
#         # direction이 "E"라면 dr=0, dc=1입니다.
#         dr, dc = directions[direction]
#
#         # 정수 값을 임시 좌표에 각각 대입합니다. 현재 위치 row,col은 그대로입니다.
#         next_row, next_col = row, col
#         # True/False는 참/거짓을 나타내는 bool 값입니다. 이번 명령의 성공 여부입니다.
#         valid = True
#
#         # range(distance)는 0부터 distance-1까지 제공하므로 거리만큼 반복합니다.
#         # _는 값을 따로 사용하지 않는 반복 변수에 관례적으로 쓰는 이름입니다.
#         for _ in range(distance):
#             # +=는 오른쪽 값을 기존 값에 더한 뒤 다시 저장합니다.
#             next_row += dr
#             next_col += dc
#
#             # 0 <= 값 < 크기는 유효한 인덱스 범위입니다. and는 두 조건 모두 참이어야 참입니다.
#             # not은 조건을 반대로 바꿉니다. 행/열 중 하나라도 범위 밖이면 실행됩니다.
#             if not (0 <= next_row < height and 0 <= next_col < width):
#                 valid = False
#                 # 이번 break는 한 칸씩 경로를 검사하는 반복문만 종료합니다.
#                 # 바깥 for route는 계속되므로 다음 명령은 처리합니다.
#                 break
#
#             # park[행]은 문자열이고 그 문자열[열]은 문자 하나를 읽습니다.
#             # ==는 같은지 비교합니다. 인덱스 범위를 먼저 확인한 다음 접근합니다.
#             if park[next_row][next_col] == "X":
#                 valid = False
#                 break
#
#         # if valid는 valid가 참일 때만 실행합니다.
#         if valid:
#             # 명령의 모든 칸이 유효했을 때만 임시 위치를 실제 위치에 반영합니다.
#             row, col = next_row, next_col
#
#     # []로 두 정수를 담은 리스트를 만듭니다. 반환 순서는 행, 열입니다.
#     # return은 결과를 전달하고 함수 전체를 종료합니다.
#     return [row, col]
