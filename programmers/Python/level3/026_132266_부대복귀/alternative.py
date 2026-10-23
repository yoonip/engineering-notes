# 출발지마다 BFS를 따로 수행합니다. 목적지 하나에서 거꾸로 탐색하는 기본 풀이와 같은 거리를 얻지만 출발지가 많으면 중복
# 탐색이 큽니다.
from collections import deque

def solution(n,roads,sources,destination):
    graph=[[] for _ in range(n+1)]
    for a,b in roads:graph[a].append(b);graph[b].append(a)
    answer=[]
    for source in sources:
        queue=deque([(source,0)]);seen={source};found=-1
        while queue:
            node,d=queue.popleft()
            if node==destination:found=d;break
            for nxt in graph[node]:
                if nxt not in seen:seen.add(nxt);queue.append((nxt,d+1))
        answer.append(found)
    return answer
