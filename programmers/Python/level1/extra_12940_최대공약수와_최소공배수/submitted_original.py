
from math import gcd

def solution(n, m):
    g = gcd(n, m)
    l = n * m // g

    return [g, l]


# ========== 공부용 코드 (전체 주석 처리) ==========

# from math import gcd                  # math 모듈에서 최대공약수를 구하는 gcd 함수를 가져옴
#
# def solution(n, m):                   # 두 자연수 n과 m을 입력받는 함수
#     g = gcd(n, m)                     # gcd()로 n과 m의 최대공약수를 계산
#     l = n * m // g                    # 두 수를 곱한 뒤 최대공약수로 나누어 최소공배수 계산
#
#     return [g, l]                     # 최대공약수와 최소공배수를 리스트로 반환
