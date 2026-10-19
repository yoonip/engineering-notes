def solution(price):
    if price >= 500000:
        return price * 80 // 100
    if price >= 300000:
        return price * 90 // 100
    if price >= 100000:
        return price * 95 // 100
    return price

# 전체 코드 줄별 설명
# def solution(price):  # def는 함수 정의. 구매 금액 입력.
#     if price >= 500000:  # if는 조건, >=는 이상 비교. 가장 큰 할인 구간부터 검사.
#         return price * 80 // 100  # 20% 할인 후 80% 지불. //로 소수점 이하 버림.
#     if price >= 300000:  # 30만 원 이상 구간 검사.
#         return price * 90 // 100  # 10% 할인 후 90% 지불.
#     if price >= 100000:  # 10만 원 이상 구간 검사.
#         return price * 95 // 100  # 5% 할인 후 95% 지불.
#     return price  # 할인 기준 미만이면 원래 가격 반환.

# 풀이 요약
# 큰 금액 구간부터 검사하고 정수 연산으로 할인 후 금액의 소수점을 버립니다.
# 