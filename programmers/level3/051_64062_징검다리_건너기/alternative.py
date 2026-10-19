# p명이 건너려면 원래 내구도가 p보다 작은 돌이 k개 연속이면 안 됩니다. 가능한 인원의 최댓값을 이분탐색합니다. 단조
# 큐보다 느리지만 조건을 직접 검사합니다.
def solution(stones,k):
    def possible(people):
        run=0
        for value in stones:
            run=run+1 if value<people else 0
            if run>=k:return False
        return True
    low,high=1,max(stones)
    while low<high:
        mid=(low+high+1)//2
        if possible(mid):low=mid
        else:high=mid-1
    return low
