from collections import Counter

def solution(clothes):
    ways = 0
    for count in Counter(kind for _, kind in clothes).values():
        ways = ways + ways * count + count
    return ways
