def solution(grid, d, k):
    n,m=len(grid),len(grid[0]);mod=1_000_000_007
    if len(d)*k>5000:raise ValueError("반복 길이 5000 이하의 직접 DP 비교용입니다")
    current=[[1]*m for _ in range(n)]
    for step in range(len(d)*k):
        following=[[0]*m for _ in range(n)]
        for r in range(n):
            for c in range(m):
                for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr,nc=r+dr,c+dc
                    if 0<=nr<n and 0<=nc<m and grid[nr][nc]-grid[r][c]==d[step%len(d)]:
                        following[nr][nc]=(following[nr][nc]+current[r][c])%mod
        current=following
    return sum(map(sum,current))%mod
