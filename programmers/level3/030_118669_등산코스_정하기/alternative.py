# 허용할 간선의 최대 시간을 정하고 출입구들에서 BFS로 산봉우리를 찾습니다. 가능한 강도는 단조이므로 이분탐색할 수
# 있습니다. 산봉우리는 경유하지 않습니다.
from collections import deque

def solution(n,paths,gates,summits):
    graph=[[] for _ in range(n+1)]
    for a,b,w in paths:graph[a].append((b,w));graph[b].append((a,w))
    peaks=set(summits)
    def reachable(limit):
        seen=set(gates);queue=deque(gates);found=[]
        while queue:
            node=queue.popleft()
            if node in peaks:found.append(node);continue
            for nxt,w in graph[node]:
                if w<=limit and nxt not in seen:seen.add(nxt);queue.append(nxt)
        return min(found) if found else None
    low,high=0,max(w for a,b,w in paths)
    while low<high:
        mid=(low+high)//2
        if reachable(mid) is not None:high=mid
        else:low=mid+1
    return [reachable(low),low]
