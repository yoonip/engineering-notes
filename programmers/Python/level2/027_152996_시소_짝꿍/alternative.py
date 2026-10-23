from itertools import combinations

def solution(weights):
    return sum(any(a*x==b*y for x in (2,3,4) for y in (2,3,4)) for a,b in combinations(weights,2))
