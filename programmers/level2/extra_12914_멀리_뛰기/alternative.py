from math import comb

def solution(n):
    return sum(comb(n - doubles, doubles) for doubles in range(n // 2 + 1)) % 1234567
