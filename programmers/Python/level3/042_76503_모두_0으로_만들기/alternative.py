# 현재 리프의 무게를 유일한 이웃으로 옮기고 그 리프를 제거합니다. 부모 배열을 먼저 만드는 기본 풀이와 달리 차수가 1인
# 정점부터 처리합니다.
from collections import deque

def solution(a,edges):
    if sum(a):return -1
    graph=[set() for _ in a];weight=a[:]
    for u,v in edges:graph[u].add(v);graph[v].add(u)
    queue=deque(i for i,adj in enumerate(graph) if len(adj)==1);answer=0
    while queue:
        node=queue.popleft()
        if not graph[node]:continue
        parent=next(iter(graph[node]));answer+=abs(weight[node]);weight[parent]+=weight[node]
        graph[parent].remove(node);graph[node].clear()
        if len(graph[parent])==1:queue.append(parent)
    return answer
