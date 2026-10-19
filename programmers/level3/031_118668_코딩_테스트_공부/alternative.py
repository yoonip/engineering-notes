# 능력 쌍을 정점으로, 공부와 문제 풀이를 간선으로 만듭니다. 목표 능력에서 값을 자르는 규칙은 같고, 작은 능력 순서 대신
# 최소 시간 순서로 탐색합니다.
from heapq import heappop,heappush

def solution(alp,cop,problems):
    A=max(p[0] for p in problems);C=max(p[1] for p in problems)
    start=min(alp,A),min(cop,C);best={start:0};heap=[(0,*start)]
    actions=problems+[[0,0,1,0,1],[0,0,0,1,1]]
    while heap:
        cost,a,c=heappop(heap)
        if cost!=best[(a,c)]:continue
        if (a,c)==(A,C):return cost
        for ra,rc,ga,gc,t in actions:
            if a<ra or c<rc:continue
            nxt=min(A,a+ga),min(C,c+gc)
            if cost+t<best.get(nxt,float('inf')):
                best[nxt]=cost+t;heappush(heap,(cost+t,*nxt))
