def solution(numbers, n):
    total = 0
    for value in numbers:
        total += value
        if total > n:
            return total

# 전체 코드 줄별 설명
# def solution(numbers, n):  # def는 함수 정의. 양의 정수 리스트와 합계 기준 입력.
#     total = 0  # 누적 합계 초기화.
#     for value in numbers:  # for로 원소를 앞에서부터 순회.
#         total += value  # +=는 더해 저장. 현재 원소 누적.
#         if total > n:  # if는 조건, >는 초과 비교. 기준과 같을 때는 계속 더함.
#             return total  # 기준보다 커진 첫 순간의 합을 반환하고 종료.

# 풀이 요약
# 합이 n 이상이 아닌 n 초과가 될 때 멈춥니다.
# 