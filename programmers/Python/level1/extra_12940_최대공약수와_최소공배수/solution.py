from math import gcd

def solution(n, m):
    g = gcd(n, m)
    l = n * m // g
    return [g, l]

# 전체 코드 줄별 설명
# from math import gcd  # from math import는 math 모듈에서 이름을 가져옴. gcd는 최대공약수를 구하는 함수. math 모듈에서 최대공약수를 구하는 gcd 함수를 가져옴
# 
# def solution(n, m):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 두 자연수 n과 m을 입력받는 함수
#     g = gcd(n, m)  # gcd는 최대공약수. =는 값 저장. gcd()로 n과 m의 최대공약수를 계산
#     l = n * m // g  # //는 내림한 정수 몫. =는 값 저장. 두 수를 곱한 뒤 최대공약수로 나누어 최소공배수 계산
#     return [g, l]  # return은 결과를 돌려주고 함수 종료. []는 리스트. 최대공약수와 최소공배수를 리스트로 반환

# 풀이 요약
# gcd가 두 수의 최대공약수 g를 구한다. 두 수의 곱은 최대공약수×최소공배수이므로 n×m/g가 최소공배수다. 나누어떨어지는 정수 계산에 //를 쓴다.
# 입력 정수 범위에서 gcd의 나눗셈 횟수 O(log min(n,m)), 보조 공간 O(1).
