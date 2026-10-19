# 예약을 직접 세어 최대 동시 인원을 구한 뒤, 작은 격자에서 그 수만큼 락커를 고르는 모든 조합의 최소 맨해튼 거리를
# 비교합니다. 배치 탐욕의 작은 격자 기준값입니다.
# 작은 입력의 비교·검증용입니다. 원래 최대 입력 제출에는 기본 풀이를 사용합니다.
from itertools import combinations

def solution(n,m,timetable):
    peak=max((sum(start<=time<=end for start,end in timetable) for time in range(600,1321)),default=0)
    if peak<=1:return 0
    best=0
    for chosen in combinations(range(n*n),peak):
        distance=min(abs(a//n-b//n)+abs(a%n-b%n) for a,b in combinations(chosen,2))
        best=max(best,distance)
    return best
