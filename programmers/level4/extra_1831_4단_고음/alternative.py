from functools import cache

def solution(n):
    if n>10000:raise ValueError("최종 음높이 10000 이하의 정방향 문자열 비교용입니다")
    @cache
    def count(value, pending):
        if value>n:return 0
        if value==n:return int(pending==0)
        total=count(value+1,pending-1) if pending else 0
        if value*3<=n:total+=count(value*3,pending+2)
        return total
    return count(3,2)
