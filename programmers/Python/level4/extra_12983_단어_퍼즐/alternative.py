from collections import deque

def solution(strs, t):
    pieces=set(strs);n=len(t);distance=[-1]*(n+1);distance[0]=0;queue=deque([0])
    while queue:
        start=queue.popleft()
        for end in range(start+1,min(n,start+5)+1):
            if distance[end]<0 and t[start:end] in pieces:
                distance[end]=distance[start]+1
                if end==n:return distance[end]
                queue.append(end)
    return distance[n]
