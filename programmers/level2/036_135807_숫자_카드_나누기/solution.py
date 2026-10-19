from math import gcd
from functools import reduce

def solution(arrayA, arrayB):
    # 한쪽 모든 수를 나눌 수 있는 가장 큰 후보는 최대공약수다.
    a = reduce(gcd, arrayA)
    b = reduce(gcd, arrayB)
    # 반대쪽 하나라도 나누면 이 최대공약수의 약수도 모두 탈락한다.
    if any(value % a == 0 for value in arrayB):
        a = 0
    if any(value % b == 0 for value in arrayA):
        b = 0
    return max(a, b)
