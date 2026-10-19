def solution(n, numlist):
    return [value for value in numlist if value % n == 0]

# 전체 코드 줄별 설명
# def solution(n, numlist):  # def는 함수 정의. 배수 기준과 정수 리스트 입력.
#     return [value for value in numlist if value % n == 0]  # 리스트 내포에서 for는 순회, if는 필터. %는 나머지, ==는 같음 비교. 나누어떨어지는 값만 선택.

# 풀이 요약
# n으로 나눈 나머지가 0인 원소만 원래 순서대로 남깁니다.
# 