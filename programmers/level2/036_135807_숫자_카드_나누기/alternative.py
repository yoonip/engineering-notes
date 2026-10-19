from math import isqrt

def solution(arrayA,arrayB):
    best=0
    for own,other in ((arrayA,arrayB),(arrayB,arrayA)):
        candidates=set()
        for d in range(1,isqrt(own[0])+1):
            if own[0]%d==0: candidates.update((d,own[0]//d))
        for d in sorted(candidates,reverse=True):
            if d<=best: break
            if all(x%d==0 for x in own) and all(x%d for x in other):
                best=d
                break
    return best
