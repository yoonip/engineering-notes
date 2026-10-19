def solution(storage, usage, change):
    total_usage = 0
    for i in range(len(change)):
        usage = usage * (100 + change[i]) // 100
        total_usage += usage
        if total_usage > storage:
            return i
    return -1

# 전체 코드 줄별 설명
# def solution(storage, usage, change):  # def는 함수 정의. storage는 저장량, usage는 지난달 사용량, change는 월별 증감률 리스트.
#     total_usage = 0  # 누적 사용량을 0으로 초기화.
#     for i in range(len(change)):  # len은 길이, range는 0부터 길이-1까지 생성하여 월 번호 순회.
#         usage = usage * (100 + change[i]) // 100  # []는 인덱스 접근, *는 곱셈, //는 정수 나눗셈. 전월 사용량에 증감률을 적용하고 소수점 버림.
#         total_usage += usage  # +=는 기존 값에 더해 저장. 이번 달 사용량 누적.
#         if total_usage > storage:  # if는 조건문, >는 큼 비교. 저장량을 초과했는지 검사.
#             return i  # return은 함수 종료와 결과 반환. 0부터 세는 부족 발생 월 반환.
#     return -1  # 모든 달에 물이 충분하면 -1 반환.

# 풀이 요약
# 월 사용량은 누적량이 아닌 직전 달 사용량을 기준으로 바꿉니다. 사용량 계산 한 줄만 수정하는 문제입니다.
# 