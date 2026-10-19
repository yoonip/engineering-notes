# 노란불 신호등
# 분류: 최소공배수 / 주기 탐색
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/468371
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

from math import gcd


def solution(signals):
    repeat_time = 1

    for green, yellow, red in signals:
        cycle = green + yellow + red
        repeat_time = repeat_time // gcd(repeat_time, cycle) * cycle

    for time in range(1, repeat_time + 1):
        all_yellow = True

        for green, yellow, red in signals:
            cycle = green + yellow + red
            phase = (time - 1) % cycle

            if not (green <= phase < green + yellow):
                all_yellow = False
                break

        if all_yellow:
            return time

    return -1


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# # from 모듈 import 이름은 모듈 안의 특정 기능을 현재 이름 공간에 가져옵니다.
# # math는 Python 표준 수학 모듈, gcd는 두 정수의 최대공약수를 반환하는 함수입니다.
# # 예를 들어 gcd(6,8)은 2입니다. 별도 패키지를 설치할 필요가 없습니다.
# from math import gcd
#
#
# # def는 함수 정의 문법입니다. signals는 채점기가 전달하는 2차원 리스트를 받습니다.
# # 함수 몸체는 콜론 다음 줄부터 네 칸 들여씁니다.
# def solution(signals):
#     # =는 오른쪽 값을 왼쪽 이름에 대입합니다. repeat_time은 작성자가 정한 변수 이름입니다.
#     repeat_time = 1
#
#     # signals 안의 [G,Y,R] 원소를 세 변수에 나누어 받는 언패킹입니다.
#     # for는 원소를 차례로 꺼내 들여쓴 코드들을 반복 실행합니다.
#     for green, yellow, red in signals:
#         # 세 정수의 덧셈 결과를 cycle이라는 지역 변수에 대입합니다.
#         cycle = green + yellow + red
#         # gcd(...)는 위에서 가져온 함수 호출입니다. 두 정수를 인자로 전달합니다.
#         # //는 정수 몫 나눗셈이며 *는 곱셈입니다. 결과는 정수로 유지됩니다.
#         repeat_time = repeat_time // gcd(repeat_time, cycle) * cycle
#
#     # range(시작, 끝)은 시작을 포함하고 끝은 제외합니다.
#     # 따라서 1부터 repeat_time까지 정수 시각을 순서대로 time에 넣습니다.
#     for time in range(1, repeat_time + 1):
#         # True는 불리언 참 상수입니다. 따옴표를 붙인 문자열 "True"와 다릅니다.
#         # 매 시각마다 이 줄이 다시 실행되어 True로 시작합니다.
#         all_yellow = True
#
#         # 바깥 시간 반복문 안의 중첩 for입니다. 세 값을 세 이름으로 언패킹합니다.
#         for green, yellow, red in signals:
#             # 정수 덧셈입니다. 이 신호등 한 주기의 길이를 구합니다.
#             cycle = green + yellow + red
#             # %는 정수 나머지 연산자입니다. 결과는 0부터 cycle-1 사이의 정수입니다.
#             # 괄호 안 time-1을 먼저 계산합니다. 1초가 0번 위치가 되도록 바꿉니다.
#             phase = (time - 1) % cycle
#
#             # green <= phase < green+yellow는 Python의 연속 비교식입니다.
#             # 두 비교가 모두 참이어야 참입니다. not은 그 bool 결과를 뒤집습니다.
#             if not (green <= phase < green + yellow):
#                 # bool 변수 값을 False로 갱신합니다.
#                 all_yellow = False
#                 # 가장 가까운 안쪽 신호등 for를 끝냅니다. 바깥 시간 for는 끝내지 않습니다.
#                 break
#
#         # bool 변수 자체를 if 조건으로 사용할 수 있습니다. == True를 쓸 필요가 없습니다.
#         # 안쪽 신호등 for와 같은 들여쓰기이므로 한 시각의 검사가 끝난 후 실행됩니다.
#         if all_yellow:
#             # time이라는 정수를 반환하고 함수 전체를 즉시 끝냅니다.
#             return time
#
#     # 바깥 for까지 끝났는데 위에서 답을 반환하지 못했을 때 정수 -1을 반환합니다.
#     return -1
