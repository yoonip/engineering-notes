# 현재 화폐를 0개부터 가능한 개수까지 사용하고 다음 화폐로 넘어갑니다. 조합을 직접 세어 1차원 DP의 바깥 반복 순서를
# 검증합니다.
# 작은 입력의 비교·검증용입니다. 원래 최대 입력 제출에는 기본 풀이를 사용합니다.
from functools import lru_cache

def solution(n,money):
    coins=tuple(sorted(set(money)))
    @lru_cache(None)
    def count(index,remaining):
        if index==len(coins):return int(remaining==0)
        return sum(count(index+1,remaining-value) for value in range(0,remaining+1,coins[index]))%1000000007
    return count(0,n)
