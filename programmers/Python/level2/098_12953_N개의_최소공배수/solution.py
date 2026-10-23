from math import gcd

def solution(arr):
    answer = 1
    # 모든 수를 순회.
    for number in arr:
        answer = answer // gcd(answer, number) * number
    return answer
