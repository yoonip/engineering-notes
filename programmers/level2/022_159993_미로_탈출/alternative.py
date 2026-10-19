from collections import deque

def solution(maps):
    rows,cols=len(maps),len(maps[0])
    r,c=next((r,c) for r in range(rows) for c in range(cols) if maps[r][c]=='S')
    queue=deque([(r,c,False,0)])
    seen={(r,c,False)}
    while queue:
        r,c,lever,d=queue.popleft()
        if maps[r][c]=='E' and lever: return d
        for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
            nr,nc=r+dr,c+dc
            if 0<=nr<rows and 0<=nc<cols and maps[nr][nc]!='X':
                active=lever or maps[nr][nc]=='L'
                state=(nr,nc,active)
                if state not in seen:
                    seen.add(state)
                    queue.append((nr,nc,active,d+1))
    return -1
