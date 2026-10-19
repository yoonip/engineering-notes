def solution(num, n):
    return int(num % n == 0)

# 전체 코드 줄별 설명
# def solution(num, n):  # def는 함수 정의. 검사할 수와 배수 기준 입력.
#     return int(num % n == 0)  # %는 나머지, ==는 같음 비교. int는 True를 1, False를 0으로 변환.

# 풀이 요약
# 나누어떨어지면 배수입니다.
# 