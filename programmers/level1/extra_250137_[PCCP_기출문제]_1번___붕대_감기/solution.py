def solution(bandage, health, attacks):
    duration, heal, bonus = bandage
    current = health
    success = 0
    attack_index = 0
    last_time = attacks[-1][0]
    for time in range(1, last_time + 1):
        if time == attacks[attack_index][0]:
            damage = attacks[attack_index][1]
            current -= damage
            success = 0
            attack_index += 1
            if current <= 0:
                return -1
        else:
            current += heal
            success += 1
            if success == duration:
                current += bonus
                success = 0
            current = min(health, current)
    return current

# 전체 코드 줄별 설명
# def solution(bandage, health, attacks):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 붕대 정보·최대 체력·공격 목록을 입력받음.
#     duration, heal, bonus = bandage  # =는 값 저장. 연속 성공 시간·초당 회복량·추가 회복량을 나눔.
#     current = health  # =는 값 저장. 현재 체력을 최대 체력으로 시작.
#     success = 0  # =는 값 저장. 연속 회복 성공 초 수 초기화.
#     attack_index = 0  # =는 값 저장. 다음 공격의 목록 위치 초기화.
#     last_time = attacks[-1][0]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 마지막 공격 시각 확인.
#     for time in range(1, last_time + 1):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. 1초부터 마지막 공격까지 순서대로 처리.
#         if time == attacks[attack_index][0]:  # if는 조건이 참일 때 실행. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. ==는 같음 비교. 현재 초에 공격이 있는지 확인.
#             damage = attacks[attack_index][1]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 공격의 피해량 조회.
#             current -= damage  # -=는 빼서 저장. 현재 체력에서 피해량을 뺌.
#             success = 0  # =는 값 저장. 공격받으면 연속 회복 기록 초기화.
#             attack_index += 1  # +=는 더하거나 연결한 값을 저장. 다음 공격을 가리키도록 이동.
#             if current <= 0:  # if는 조건이 참일 때 실행. <=는 이하 비교. 체력이 0 이하가 되었는지 확인.
#                 return -1  # return은 결과를 돌려주고 함수 종료. 죽었으므로 -1을 반환하고 종료.
#         else:  # else는 앞 조건들에 해당하지 않는 경우. 공격이 없는 초인 경우.
#             current += heal  # +=는 더하거나 연결한 값을 저장. 초당 회복량을 더함.
#             success += 1  # +=는 더하거나 연결한 값을 저장. 연속 회복 초 수 증가.
#             if success == duration:  # if는 조건이 참일 때 실행. ==는 같음 비교. 연속 회복 시간이 기준에 도달했는지 검사.
#                 current += bonus  # +=는 더하거나 연결한 값을 저장. 추가 회복량 적용.
#                 success = 0  # =는 값 저장. 추가 회복 후 연속 횟수를 새로 셈.
#             current = min(health, current)  # min은 최솟값. =는 값 저장. 최대 체력을 넘지 않도록 제한.
#     return current  # return은 결과를 돌려주고 함수 종료. 마지막 공격 뒤 남은 체력 반환.

# 풀이 요약
# 매초 공격 여부를 먼저 판단한다. 공격받으면 피해를 빼고 연속 회복 횟수를 초기화하며 그 초에는 회복하지 않는다. 공격이 없으면 기본 회복과 연속 성공 보너스를 적용하고 최대 체력으로 제한한다. 체력이 0 이하가 되는 즉시 끝낸다.
# 마지막 공격 시각 T: 시간 O(T), 보조 공간 O(1).
