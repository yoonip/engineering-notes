from functools import cache

def solution(arr):
    if len(arr)>23:raise ValueError("숫자 12개 이하의 모든 괄호 값 비교용입니다")
    @cache
    def values(left,right):
        if left==right:return frozenset([int(arr[2*left])])
        results=set()
        for split in range(left,right):
            for a in values(left,split):
                for b in values(split+1,right):results.add(a+b if arr[2*split+1]=='+' else a-b)
        return frozenset(results)
    return max(values(0,len(arr)//2))
