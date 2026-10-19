from math import gcd

def solution(arr):
    answer = 1
    for number in arr:
        answer = answer // gcd(answer, number) * number
    return answer

# 전체 코드 줄별 설명
# from math import gcd  # math 모듈의 gcd를 import. 두 정수의 최대공약수를 반환하는 함수.
# 
# def solution(arr):  # def는 함수 정의. arr은 자연수 목록 입력.
#     answer = 1  # =는 대입. 1과의 최소공배수는 원래 수이므로 누적 초기값 1.
#     for number in arr:  # for~in으로 모든 수를 순회.
#         answer = answer // gcd(answer, number) * number  # //는 정수 몫, *는 곱셈. 두 수의 최소공배수=a/gcd(a,b)*b를 누적 적용.
#     return answer  # return으로 모든 수의 최소공배수 반환.

# 풀이 요약
# 현재까지의 최소공배수와 다음 수의 최소공배수를 반복 계산합니다. 두 수의 곱에서 공통 인수인 최대공약수를 한 번 나눕니다.
# 예: [2,6,8,14]는 2→6→24→168. 정수 연산 기준 N개·중간 최대값 V에 대해 시간 O(N log V), 공간 O(1).
