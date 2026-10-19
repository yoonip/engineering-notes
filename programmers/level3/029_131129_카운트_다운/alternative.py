# 점수를 정점으로 두고 비용을 (다트 수, 싱글·불 수의 음수)로 표현합니다. 튜플 비교로 두 우선순위를 함께 처리합니다.
# 기본 DP보다 힙 비용이 들지만 우선순위를 명확히 확인할 수 있습니다.
from heapq import heappop,heappush

def solution(target):
    options=[(i,-1) for i in range(1,21)]+[(2*i,0) for i in range(1,21)]+[(3*i,0) for i in range(1,21)]+[(50,-1)]
    best={0:(0,0)};heap=[(0,0,0)]
    while heap:
        count,negative,score=heappop(heap)
        if (count,negative)!=best[score]:continue
        if score==target:return [count,-negative]
        for value,bonus in options:
            nxt=score+value;cost=count+1,negative+bonus
            if nxt<=target and cost<best.get(nxt,(float('inf'),0)):
                best[nxt]=cost;heappush(heap,(*cost,nxt))
