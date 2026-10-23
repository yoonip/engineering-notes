from itertools import combinations
from math import comb

def solution(distance, rocks, n):
    rocks=sorted(rocks);remaining=len(rocks)-n
    if comb(len(rocks),remaining)>500000:raise ValueError("남길 바위 조합 50만 이하 비교용입니다")
    answer=0
    for selected in combinations(rocks,remaining):
        points=(0,)+selected+(distance,)
        answer=max(answer,min(b-a for a,b in zip(points,points[1:])))
    return answer
