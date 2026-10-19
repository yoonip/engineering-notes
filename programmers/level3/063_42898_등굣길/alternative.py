# 학교에서 집 방향으로 위·왼쪽 경로 수를 재귀로 더합니다. 웅덩이와 경계를 0으로 처리합니다. 반복 DP와 점화식은 같지만
# 계산 요청 순서가 다릅니다.
from functools import lru_cache

def solution(m,n,puddles):
    blocked={tuple(p) for p in puddles};mod=1000000007
    @lru_cache(None)
    def count(x,y):
        if x<1 or y<1 or (x,y) in blocked:return 0
        if (x,y)==(1,1):return 1
        return (count(x-1,y)+count(x,y-1))%mod
    return count(m,n)
