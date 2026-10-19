# 유연근무제
# 분류: 시간 변환 / 시뮬레이션
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/388351
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

def solution(schedules, timelogs, startday):
    answer = 0

    for i in range(len(schedules)):
        scheduled = schedules[i]
        limit = (scheduled // 100) * 60 + scheduled % 100 + 10
        eligible = True

        for day in range(7):
            weekday = (startday + day - 1) % 7 + 1

            if weekday >= 6:
                continue

            arrival = timelogs[i][day]
            arrival_minutes = (arrival // 100) * 60 + arrival % 100

            if arrival_minutes > limit:
                eligible = False
                break

        if eligible:
            answer += 1

    return answer


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# # def는 함수를 정의합니다. 괄호 안 세 이름은 채점기가 전달하는 값을 받는 매개변수입니다.
# # 함수 이름과 매개변수 순서는 문제의 기본 틀을 따릅니다. 이 풀이에는 import가 필요하지 않습니다.
# def solution(schedules, timelogs, startday):
#     # answer는 작성자가 정한 변수 이름입니다. =는 오른쪽 정수를 왼쪽 이름에 대입합니다.
#     answer = 0
#
#     # len(schedules)는 직원 수입니다. range(n)은 0부터 n-1까지 정수를 제공합니다.
#     # for i in ...는 그 정수를 순서대로 i에 넣고 들여쓴 코드를 반복합니다.
#     for i in range(len(schedules)):
#         # 리스트[인덱스]로 원소를 읽습니다. i=0이면 첫 직원의 희망 시각입니다.
#         scheduled = schedules[i]
#         # //는 정수 몫, %는 나머지입니다. 958//100은 9, 958%100은 58입니다.
#         # 괄호 안의 몫을 구하고 *60을 계산한 뒤 분과 10을 더합니다.
#         # limit는 HHMM 표현이 아니라 자정 이후의 총 분 수인 정수입니다.
#         limit = (scheduled // 100) * 60 + scheduled % 100 + 10
#         # True는 따옴표 없이 쓰는 불리언 참 상수입니다. eligible은 변수 이름입니다.
#         # 매 직원의 for 반복마다 다시 True를 대입합니다.
#         eligible = True
#
#         # range(7)은 0,1,2,3,4,5,6을 제공하므로 7일을 검사합니다.
#         for day in range(7):
#             # %7의 결과는 0~6입니다. -1로 기준을 맞추고 마지막에 +1 하여 1~7로 만듭니다.
#             weekday = (startday + day - 1) % 7 + 1
#
#             # >=는 크거나 같은지 비교합니다. 조건식의 결과는 True 또는 False입니다.
#             if weekday >= 6:
#                 # continue는 가장 가까운 for의 이번 반복을 생략하고 다음 day로 넘어갑니다.
#                 continue
#
#             # timelogs[i]는 i번 직원의 기록 리스트이고, 거기에 [day]를 써 해당 날짜를 읽습니다.
#             arrival = timelogs[i][day]
#             # 실제 출근 시각도 같은 단위인 총 분 수로 바꿉니다. *는 곱셈, +는 덧셈입니다.
#             arrival_minutes = (arrival // 100) * 60 + arrival % 100
#
#             # >는 엄격하게 큰지만 비교합니다. 인정 마감 시각과 같으면 이 조건은 거짓입니다.
#             if arrival_minutes > limit:
#                 # False는 불리언 거짓 상수입니다. 위에서 만든 변수를 새 값으로 갱신합니다.
#                 eligible = False
#                 # break는 가장 가까운 day 반복문을 끝냅니다. 바깥 직원 반복문은 계속됩니다.
#                 break
#
#         # if 뒤에 불리언 변수 자체를 쓸 수 있습니다. == True를 따로 붙이지 않아도 됩니다.
#         # day 반복문 밖이므로 한 직원의 검사를 마친 뒤 실행합니다.
#         if eligible:
#             # += 1은 answer = answer + 1과 같습니다.
#             answer += 1
#
#     # return은 정수 결과를 채점기에 전달하고 함수를 끝냅니다. 직원 반복문 밖에 둡니다.
#     return answer
