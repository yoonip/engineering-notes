from collections import deque

def solution(n, path, order):
    tree=[[] for _ in range(n)]
    for a,b in path:tree[a].append(b);tree[b].append(a)
    parent=[-1]*n;parent[0]=0;queue=deque([0]);arcs=[[] for _ in range(n)];degree=[0]*n
    while queue:
        node=queue.popleft()
        for child in tree[node]:
            if parent[child]<0:
                parent[child]=node;arcs[node].append(child);degree[child]+=1;queue.append(child)
    # 나무를 지나갈 순서와 별도 방문 조건을 같은 선행 관계로 놓는다.
    for before,after in order:arcs[before].append(after);degree[after]+=1
    ready=deque(i for i,d in enumerate(degree) if d==0);count=0
    while ready:
        node=ready.popleft();count+=1
        for child in arcs[node]:
            degree[child]-=1
            if degree[child]==0:ready.append(child)
    return count==n
