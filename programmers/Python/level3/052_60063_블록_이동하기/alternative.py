# 두 좌표 집합 대신 로봇의 왼쪽·위쪽 기준 칸과 가로·세로 방향을 저장합니다. 회전 시 두 칸이 휩쓰는 2×2 영역이
# 비었는지 확인합니다.
from collections import deque

def solution(board):
    n=len(board)
    def empty(r,c):return 0<=r<n and 0<=c<n and board[r][c]==0
    queue=deque([(0,0,0,0)]);seen={(0,0,0)}
    while queue:
        r,c,o,d=queue.popleft();cells=((r,c),(r,c+1)) if o==0 else ((r,c),(r+1,c))
        if (n-1,n-1) in cells:return d
        candidates=[]
        for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
            if all(empty(a+dr,b+dc) for a,b in cells):candidates.append((r+dr,c+dc,o))
        if o==0:
            for delta in (-1,1):
                if empty(r+delta,c) and empty(r+delta,c+1):
                    candidates.extend([(min(r,r+delta),c,1),(min(r,r+delta),c+1,1)])
        else:
            for delta in (-1,1):
                if empty(r,c+delta) and empty(r+1,c+delta):
                    candidates.extend([(r,min(c,c+delta),0),(r+1,min(c,c+delta),0)])
        for state in candidates:
            if state not in seen:seen.add(state);queue.append((*state,d+1))
    return -1
