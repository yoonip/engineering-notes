from heapq import heappush, heappop

def solution(m, n, s, time_map):
    if m*n>25 or s>1000:raise ValueError("작은 격자의 대화 시간 상태 탐색 비교용입니다")
    best={(0,0,0):0};heap=[(0,0,0,0)]
    while heap:
        steps,talk,r,c=heappop(heap)
        if steps!=best.get((r,c,talk)):continue
        if (r,c)==(m-1,n-1):return [steps,talk]
        for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
            nr,nc=r+dr,c+dc
            if 0<=nr<m and 0<=nc<n and time_map[nr][nc]>=0:
                nt=talk+time_map[nr][nc]
                if nt<=s and steps+1<best.get((nr,nc,nt),10**18):
                    best[nr,nc,nt]=steps+1;heappush(heap,(steps+1,nt,nr,nc))
    return [-1,-1]
