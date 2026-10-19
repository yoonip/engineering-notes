
from math import isqrt

def solution(n):
    x = isqrt(n)

    if x * x == n:
        return (x + 1) ** 2

    return -1


# ========== 공부용 코드 (전체 주석 처리) ==========

# from math import isqrt                # math 모듈에서 정수 제곱근을 구하는 isqrt 함수 가져오기
#
# def solution(n):                      # 자연수 n을 입력받는 함수
#     x = isqrt(n)                      # n의 제곱근에서 소수 부분을 버린 정수 구하기
#
#     if x * x == n:                    # x의 제곱이 n과 같으면 완전제곱수
#         return (x + 1) ** 2           # 제곱근에 1을 더한 뒤 제곱하여 반환
#
#     return -1                         # 완전제곱수가 아니라면 -1 반환
