def solution(n):
    board=[[0]*(r+1) for r in range(n)]
    directions=((1,0),(0,1),(-1,-1))
    r=c=d=0
    for value in range(1,n*(n+1)//2+1):
        board[r][c]=value
        dr,dc=directions[d]
        nr,nc=r+dr,c+dc
        if not(0<=nr<n and 0<=nc<=nr) or board[nr][nc]:
            d=(d+1)%3
            dr,dc=directions[d]
            nr,nc=r+dr,c+dc
        r,c=nr,nc
    return [value for row in board for value in row]
