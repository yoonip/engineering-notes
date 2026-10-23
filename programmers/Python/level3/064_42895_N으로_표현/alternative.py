# 정확히 k개의 N으로 만든 값들을 재귀적으로 생성하고 캐시합니다. 나눗셈은 음수에서도 0쪽으로 버림하도록 구현합니다.
# 양방향 연산과 이어 쓰기 모두 포함합니다.
from functools import lru_cache

def solution(N,number):
    def divide(a,b):
        q=abs(a)//abs(b)
        return -q if (a<0)!=(b<0) else q
    @lru_cache(None)
    def values(count):
        result={int(str(N)*count)}
        for left in range(1,count):
            for a in values(left):
                for b in values(count-left):
                    result.update((a+b,a-b,a*b))
                    if b:result.add(divide(a,b))
        return result
    for count in range(1,9):
        if number in values(count):return count
    return -1
