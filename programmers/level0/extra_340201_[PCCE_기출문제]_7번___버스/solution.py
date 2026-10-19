def func1(num):
    if 0 > num:
        return 0
    else:
        return num

def func2(num):
    if num > 0:
        return 0
    else:
        return num

def func3(station):
    num = 0
    for people in station:
        if people == "Off":
            num += 1
    return num

def func4(station):
    num = 0
    for people in station:
        if people == "On":
            num += 1
    return num

def solution(seat, passengers):
    num_passenger = 0
    for station in passengers:
        num_passenger += func4(station)
        num_passenger -= func3(station)
    answer = func1(seat - num_passenger)
    return answer

# 전체 코드 줄별 설명
# def func1(num):  # def는 함수 정의. 음수를 0으로 바꾸는 보조 함수.
#     if 0 > num:  # if는 조건, >는 큼 비교. num이 음수인지 확인.
#         return 0  # 음수라면 0 반환.
#     else:  # else는 앞 조건이 거짓인 경우.
#         return num  # 0 이상이면 원래 수 반환.
# 
# def func2(num):  # 양수를 0으로 바꾸는 보조 함수. 이번 정답에서는 사용하지 않음.
#     if num > 0:  # num이 양수인지 비교.
#         return 0  # 양수라면 0 반환.
#     else:  # 0 이하인 경우.
#         return num  # 원래 수 반환.
# 
# def func3(station):  # 한 정거장에서 내린 승객 수를 세는 함수.
#     num = 0  # 인원 수 초기화.
#     for people in station:  # for는 반복문. 정거장의 승하차 문자열 순회.
#         if people == "Off":  # ==는 같음 비교. 하차 문자열인지 확인.
#             num += 1  # +=는 더해 저장. 하차 인원 1명 증가.
#     return num  # 하차 인원 반환.
# 
# def func4(station):  # 한 정거장에서 탄 승객 수를 세는 함수.
#     num = 0  # 승차 인원 초기화.
#     for people in station:  # 정거장 기록의 각 문자열 순회.
#         if people == "On":  # 승차 문자열인지 확인.
#             num += 1  # 승차 인원 1명 증가.
#     return num  # 승차 인원 반환.
# 
# def solution(seat, passengers):  # 좌석 수와 정거장별 승하차 2차원 리스트를 입력받는 함수.
#     num_passenger = 0  # 버스에 탄 현재 승객 수 초기화.
#     for station in passengers:  # 각 정거장의 기록 리스트 순회.
#         num_passenger += func4(station)  # 함수 호출 괄호 ()로 승차 인원을 구해 현재 승객 수에 더함.
#         num_passenger -= func3(station)  # -=는 빼서 저장. 하차 인원을 현재 승객 수에서 뺌.
#     answer = func1(seat - num_passenger)  # 전체 좌석에서 승객 수를 뺀 값을 음수가 되지 않게 보정.
#     return answer  # 남은 좌석 수 반환. 서 있는 승객이 있으면 0.

# 풀이 요약
# 승차 인원을 더하고 하차 인원을 뺀 뒤 좌석 수에서 최종 승객 수를 뺍니다. 음수는 func1으로 0으로 바꿉니다.
# 