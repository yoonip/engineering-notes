from collections import deque

def solution(board):
    rows,cols=len(board),len(board[0])
    ends={}
    for r in range(rows):
        c=0
        while c<cols:
            if board[r][c]=='D': c+=1; continue
            start=c
            while c<cols and board[r][c]!='D': c+=1
            for y in range(start,c):
                ends[(r,y)]=[(r,start),(r,c-1)]
    for c in range(cols):
        r=0
        while r<rows:
            if board[r][c]=='D': r+=1; continue
            start=r
            while r<rows and board[r][c]!='D': r+=1
            for x in range(start,r):
                ends[(x,c)].extend(((start,c),(r-1,c)))
    start=next((r,c) for r in range(rows) for c in range(cols) if board[r][c]=='R')
    queue=deque([(start,0)])
    seen={start}
    while queue:
        point,d=queue.popleft()
        if board[point[0]][point[1]]=='G': return d
        for following in ends[point]:
            if following not in seen:
                seen.add(following)
                queue.append((following,d+1))
    return -1
