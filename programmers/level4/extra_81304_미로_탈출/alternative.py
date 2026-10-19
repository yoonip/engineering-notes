def solution(n, start, end, roads, traps):
    if n>20 or len(traps)>4:raise ValueError("작은 확장 그래프의 Bellman–Ford 비교용입니다")
    bits={node:1<<i for i,node in enumerate(traps)};states=1<<len(traps)
    distance=[[float('inf')]*states for _ in range(n+1)];distance[start][0]=0
    for _ in range(n*states-1):
        changed=False
        for mask in range(states):
            for a,b,cost in roads:
                reverse=bool(mask&bits.get(a,0))^bool(mask&bits.get(b,0))
                u,v=(b,a) if reverse else (a,b)
                new_mask=mask^bits.get(v,0)
                proposed=distance[u][mask]+cost
                if proposed<distance[v][new_mask]:distance[v][new_mask]=proposed;changed=True
        if not changed:break
    return min(distance[end])
