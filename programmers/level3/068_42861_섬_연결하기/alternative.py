# 이미 연결한 섬 집합에서 바깥으로 나가는 가장 싼 다리를 고릅니다. 전체 간선을 정렬하는 Kruskal과 달리 하나의
# 연결된 집합을 확장합니다.
from heapq import heappush,heappop

def solution(n,costs):
    graph=[[] for _ in range(n)]
    for a,b,w in costs:graph[a].append((w,b));graph[b].append((w,a))
    seen=set();heap=[(0,0)];total=0
    while heap:
        cost,node=heappop(heap)
        if node in seen:continue
        seen.add(node);total+=cost
        for edge in graph[node]:
            if edge[1] not in seen:heappush(heap,edge)
    return total
