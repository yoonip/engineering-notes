from collections import deque
from itertools import combinations

def solution(n, edges):
    if n>60:raise ValueError("정점 60개 이하의 세 정점 직접 비교용입니다")
    graph=[[] for _ in range(n)]
    for a,b in edges:graph[a-1].append(b-1);graph[b-1].append(a-1)
    distances=[]
    for root in range(n):
        row=[-1]*n;row[root]=0;queue=deque([root])
        while queue:
            u=queue.popleft()
            for v in graph[u]:
                if row[v]<0:row[v]=row[u]+1;queue.append(v)
        distances.append(row)
    return max(sorted((distances[a][b],distances[a][c],distances[b][c]))[1]
               for a,b,c in combinations(range(n),3))
