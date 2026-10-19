# 모든 칸의 회전 횟수를 직접 적용해 마지막 보드를 확인합니다. 첫 행만 정하면 나머지가 강제된다는 성질을 독립적으로
# 검사합니다. 2×2 같은 작은 보드에만 사용합니다.
# 작은 입력의 비교·검증용입니다. 원래 최대 입력 제출에는 기본 풀이를 사용합니다.
from itertools import product

def solution(clockHands):
    n=len(clockHands);answer=3*n*n+1
    for rotations in product(range(4),repeat=n*n):
        cost=sum(rotations)
        if cost>=answer:continue
        grid=[row[:] for row in clockHands]
        for index,turns in enumerate(rotations):
            r,c=divmod(index,n)
            for dr,dc in ((0,0),(1,0),(-1,0),(0,1),(0,-1)):
                nr,nc=r+dr,c+dc
                if 0<=nr<n and 0<=nc<n:grid[nr][nc]=(grid[nr][nc]+turns)%4
        if not any(map(any,grid)):answer=cost
    return answer
