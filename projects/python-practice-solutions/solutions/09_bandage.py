# 붕대 감기
# 분류: 시뮬레이션
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/250137
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

def solution(bandage, health, attacks):
    duration, heal, bonus = bandage
    current = health
    streak = 0
    damage_at = {}

    for time, damage in attacks:
        damage_at[time] = damage

    last_time = attacks[-1][0]

    for time in range(1, last_time + 1):
        if time in damage_at:
            current -= damage_at[time]
            streak = 0

            if current <= 0:
                return -1
        else:
            current += heal
            streak += 1

            if streak == duration:
                current += bonus
                streak = 0

            current = min(current, health)

    return current


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# # def는 함수를 정의합니다. 세 매개변수에는 프로그래머스 채점기가 입력을 전달합니다.
# # 콜론 다음의 들여쓴 코드가 함수에 속합니다. 별도 import는 필요 없습니다.
# def solution(bandage, health, attacks):
#     # 리스트의 세 원소를 세 변수에 각각 대입하는 '언패킹' 문법입니다.
#     # bandage=[5,1,5]라면 duration=5, heal=1, bonus=5입니다.
#     duration, heal, bonus = bandage
#     # =는 오른쪽 값을 왼쪽 변수 이름에 대입합니다.
#     # current는 변하는 현재 체력, health는 최대 체력으로 사용합니다.
#     current = health
#     # streak는 공격받지 않고 연속으로 회복한 초 수입니다.
#     streak = 0
#     # {}는 빈 딕셔너리입니다. 딕셔너리는 키와 값을 연결해 저장합니다.
#     damage_at = {}
#
#     # attacks의 각 원소는 [공격 시각, 피해량]인 리스트입니다.
#     # for의 각 반복에서 두 값을 time과 damage로 언패킹합니다.
#     for time, damage in attacks:
#         # 딕셔너리[키] = 값으로 저장합니다. 예: 2초에 피해 10이면 {2: 10}.
#         damage_at[time] = damage
#
#     # 리스트[-1]은 마지막 원소입니다. attacks[-1]은 마지막 공격 기록입니다.
#     # 그 기록의 [0]번 값, 즉 공격 시각을 읽습니다.
#     # 공격이 시간순으로 주어지므로 이 값이 전체 마지막 시각입니다.
#     last_time = attacks[-1][0]
#
#     # range(시작, 끝)은 시작 이상, 끝 미만의 정수를 순서대로 제공합니다.
#     # 마지막 공격 시각도 포함해야 하므로 끝값에 +1을 합니다.
#     for time in range(1, last_time + 1):
#         # '키 in 딕셔너리'는 해당 키가 존재하는지를 확인합니다.
#         # 현재 초에 공격 기록이 있으면 이 if 안의 코드를 실행합니다.
#         if time in damage_at:
#             # -=는 오른쪽 값을 기존 값에서 뺀 뒤 저장합니다.
#             current -= damage_at[time]
#             streak = 0
#
#             # <=는 '작거나 같다'입니다. 체력이 정확히 0인 경우도 사망입니다.
#             if current <= 0:
#                 # return은 값을 전달하고 함수 전체를 즉시 종료합니다.
#                 return -1
#         # else는 짝인 if 조건이 거짓일 때 실행합니다.
#         # 따라서 공격받은 초에는 이 회복 코드가 실행되지 않습니다.
#         else:
#             # +=는 오른쪽 값을 기존 값에 더한 뒤 저장합니다.
#             current += heal
#             streak += 1
#
#             # ==는 두 값이 같은지 비교합니다. 값을 대입하는 =와 구분합니다.
#             if streak == duration:
#                 current += bonus
#                 streak = 0
#
#             # min(a,b)는 둘 중 작은 값을 반환합니다.
#             # 회복한 체력이 최대 체력보다 크면 최대 체력까지만 저장합니다.
#             current = min(current, health)
#
#     # 모든 초를 처리한 뒤의 현재 체력을 반환합니다.
#     return current
