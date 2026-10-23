from math import gcd

def solution(n):
    return n // gcd(n, 6)

# 전체 코드 줄별 설명
# from math import gcd  # from 모듈 import 이름은 도구 가져오기. math는 수학 모듈, gcd는 최대공약수 계산 함수.
# 
# def solution(n):  # def는 함수 정의. 똑같이 나누어 먹을 사람 수 입력.
#     return n // gcd(n, 6)  # n과 6의 최소공배수는 n*6/gcd. 이를 판당 6조각으로 나누면 n/gcd 판이 필요.

# 풀이 요약
# 총 조각 수가 사람 수와 6 모두의 배수여야 하므로 최소공배수를 이용합니다.
# 