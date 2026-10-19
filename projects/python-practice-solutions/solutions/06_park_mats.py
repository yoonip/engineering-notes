# 공원 / 돗자리
# 분류: 완전탐색
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/340198
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

def solution(mats, park):
    rows = len(park)
    cols = len(park[0])

    for size in sorted(mats, reverse=True):
        for row in range(rows - size + 1):
            for col in range(cols - size + 1):
                possible = True

                for r in range(row, row + size):
                    for c in range(col, col + size):
                        if park[r][c] != "-1":
                            possible = False
                            break

                    if not possible:
                        break

                if possible:
                    return size

    return -1


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# # def는 함수를 정의합니다. mats와 park는 함수가 전달받는 매개변수입니다.
# # 콜론(:) 다음의 들여쓴 줄들이 함수에 속합니다. import할 기능은 없습니다.
# def solution(mats, park):
#     # len(리스트)는 원소 개수입니다. park의 원소는 각 행이므로 전체 행 수입니다.
#     # =는 오른쪽 값을 왼쪽 변수 이름에 대입합니다.
#     rows = len(park)
#     # park[0]은 첫 번째 행입니다. Python의 인덱스는 0부터 시작합니다.
#     # 첫 번째 행의 칸 수를 세면 열 수를 알 수 있습니다.
#     cols = len(park[0])
#
#     # sorted는 정렬된 새 리스트를 반환하며 mats 자체를 수정하지 않습니다.
#     # reverse=True는 큰 값부터 작은 값으로 정렬한다는 이름 붙은 인자입니다.
#     # for는 리스트에서 원소를 하나씩 꺼내 size에 대입하며 반복합니다.
#     # 예: mats가 [2,5,3]이면 size는 차례로 5,3,2가 됩니다.
#     for size in sorted(mats, reverse=True):
#         # range(끝)은 0부터 끝-1까지의 정수를 만듭니다.
#         # rows=6, size=3이면 range(4)이므로 row는 0,1,2,3입니다.
#         # rows-size+1이 0 이하라면 반복할 원소가 없어 이 반복문을 건너뜁니다.
#         for row in range(rows - size + 1):
#             # col은 돗자리 왼쪽 위 꼭짓점의 열 번호입니다.
#             for col in range(cols - size + 1):
#                 # True/False는 참/거짓을 나타내는 bool(불리언) 값입니다.
#                 # 각 시작 위치를 검사할 때마다 possible에 True를 다시 대입합니다.
#                 possible = True
#
#                 # range(시작,끝)은 시작부터 끝-1까지입니다.
#                 # row=1,size=3이면 r은 1,2,3입니다. 정확히 세 행을 검사합니다.
#                 for r in range(row, row + size):
#                     # c는 돗자리가 차지할 칸들의 실제 열 번호입니다.
#                     for c in range(col, col + size):
#                         # park[r][c]: r번 행 안에서 c번 칸을 읽는 2차원 인덱싱입니다.
#                         # !=는 '같지 않다'입니다. "-1"은 따옴표가 있는 문자열입니다.
#                         # 이 문제에서 빈칸은 정수 -1이 아니라 문자열 "-1"입니다.
#                         if park[r][c] != "-1":
#                             possible = False
#                             # break는 가장 가까이 감싼 반복문 하나만 종료합니다.
#                             # 여기서는 for c 반복문을 종료합니다.
#                             break
#
#                     # not은 참/거짓을 반대로 바꿉니다.
#                     # possible이 False면 not possible은 True입니다.
#                     if not possible:
#                         # 이번 break는 for r 반복문을 종료합니다.
#                         break
#
#                 # if 변수는 그 변수가 참일 때 실행됩니다.
#                 if possible:
#                     # return은 값을 반환하면서 solution 함수 전체를 종료합니다.
#                     # 따라서 바깥쪽 반복문들도 더 이상 실행되지 않습니다.
#                     return size
#
#     # 어떤 후보에서도 return size를 하지 못한 경우 이 줄에 도달합니다.
#     # 반환값 -1은 문제에서 불가능을 뜻하도록 정한 정수입니다.
#     return -1
