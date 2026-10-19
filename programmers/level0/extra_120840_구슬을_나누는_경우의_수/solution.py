from math import comb

def solution(balls, share):
    return comb(balls, share)

# 전체 코드 줄별 설명
# from math import comb  # from 모듈 import 이름은 도구 가져오기. math는 수학 모듈, comb(n,k)는 서로 다른 n개 중 k개를 순서 없이 고르는 조합 수.
# 
# def solution(balls, share):  # def는 함수 정의. 전체 구슬 수와 선택할 구슬 수 입력.
#     return comb(balls, share)  # comb를 호출해 정수 조합 수를 구하고 return으로 반환.

# 풀이 요약
# 구슬을 고르는 순서를 고려하지 않으므로 조합 nCk를 사용합니다.
# 