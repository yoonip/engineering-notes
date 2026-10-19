# 두 L자 선분만 보는 대신 타일 사이의 이동을 (위치, 방향, 꺾은 횟수)로 탐색합니다. 한 번 이하로 꺾어 도달하는 쌍
# 중 작은 글자부터 제거합니다.
from collections import deque

def solution(m,n,board):
    grid=[list(row) for row in board];positions={}
    for r,row in enumerate(grid):
        for c,ch in enumerate(row):
            if ch.isupper():positions.setdefault(ch,[]).append((r,c))
    directions=((1,0),(-1,0),(0,1),(0,-1))
    def connected(a,b):
        queue=deque([(a[0],a[1],-1,0)]);seen=set()
        while queue:
            r,c,old,turns=queue.popleft()
            for direction,(dr,dc) in enumerate(directions):
                nr,nc=r+dr,c+dc;changed=turns+int(old!=-1 and old!=direction)
                if changed>1 or not (0<=nr<m and 0<=nc<n):continue
                if (nr,nc)==b:return True
                state=nr,nc,direction,changed
                if grid[nr][nc]=='.' and state not in seen:seen.add(state);queue.append(state)
        return False
    answer=[]
    while positions:
        for ch in sorted(positions):
            a,b=positions[ch]
            if connected(a,b):
                grid[a[0]][a[1]]=grid[b[0]][b[1]]='.';answer.append(ch);del positions[ch];break
        else:return 'IMPOSSIBLE'
    return ''.join(answer)
