from functools import lru_cache

def solution(depth, money, excavate):
    @lru_cache(None)
    def pivot(left, right, budget):
        if left == right:
            return -2
        for middle in range(left, right):
            rest = budget - depth[middle]
            if rest >= 0 and pivot(left, middle, rest) != -1 and pivot(middle + 1, right, rest) != -1:
                return middle
        return -1
    left, right, budget = 0, len(depth), money
    while left < right:
        middle = pivot(left, right, budget)
        if middle < 0:
            raise ValueError('주어진 예산으로 보장할 수 없는 입력입니다.')
        budget -= depth[middle]
        response = excavate(middle + 1)
        if response == 0:
            return middle + 1
        if response < 0:
            right = middle
        else:
            left = middle + 1
    return 0
