# 마지막 곱셈의 경계를 재귀로 고르고 부분 구간의 답을 캐시합니다. 짧은 구간부터 반복하는 기본 DP와 계산 순서가
# 다릅니다.
from functools import lru_cache

def solution(matrix_sizes):
    @lru_cache(None)
    def cost(left,right):
        if left==right:return 0
        return min(cost(left,k)+cost(k+1,right)+matrix_sizes[left][0]*matrix_sizes[k][1]*matrix_sizes[right][1]
                   for k in range(left,right))
    return cost(0,len(matrix_sizes)-1)
