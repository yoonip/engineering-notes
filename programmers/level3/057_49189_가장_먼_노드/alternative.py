# 모든 간선의 가중치를 1로 두고 다익스트라를 적용합니다. BFS와 거리는 같지만 힙 연산이 추가되므로 이 문제에서는
# BFS가 더 간단하고 빠릅니다.
from heapq import heappop,heappush

def solution(n,edge):
    graph=[[] for _ in range(n+1)]
    for a,b in edge:graph[a].append(b);graph[b].append(a)
    d=[float('inf')]*(n+1);d[1]=0;heap=[(0,1)]
    while heap:
        cost,v=heappop(heap)
        if cost!=d[v]:continue
        for u in graph[v]:
            if cost+1<d[u]:d[u]=cost+1;heappush(heap,(cost+1,u))
    maximum=max(x for x in d[1:] if x<float('inf'))
    return d.count(maximum)
