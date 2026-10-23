# 다음 숫자와 양손 위치를 재귀 상태로 둡니다. 남은 문자열의 최저 비용을 반환하므로 앞에서부터 비용을 누적하는 기본 DP와
# 방향이 반대입니다. 긴 문자열의 제출에는 반복 DP가 안전합니다.
# 작은 입력의 비교·검증용입니다. 원래 최대 입력 제출에는 기본 풀이를 사용합니다.
from functools import lru_cache

def solution(numbers):
    coords={str(i):divmod(i-1,3) for i in range(1,10)}; coords['0']=(3,1)
    def cost(a,b):
        if a==b:return 1
        r=abs(coords[a][0]-coords[b][0]);c=abs(coords[a][1]-coords[b][1])
        return 3*min(r,c)+2*abs(r-c)
    @lru_cache(None)
    def solve(index,left,right):
        if index==len(numbers):return 0
        target=numbers[index];choices=[]
        if target!=right:choices.append(cost(left,target)+solve(index+1,target,right))
        if target!=left:choices.append(cost(right,target)+solve(index+1,left,target))
        return min(choices)
    return solve(0,'4','6')
