def solution(number, n, m):
    return int(number % n == 0 and number % m == 0)

# 전체 코드 줄별 설명
# def solution(number, n, m):  # def는 함수 정의. 검사할 정수와 두 배수 기준 입력.
#     return int(number % n == 0 and number % m == 0)  # %는 나머지, and는 모두 참일 때 참, int는 참·거짓을 1·0으로 변환.

# 풀이 요약
# 두 수 모두로 나누어떨어지는지 검사합니다.
# 