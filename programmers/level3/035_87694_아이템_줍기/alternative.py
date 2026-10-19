# 직사각형 내부 칸을 채우는 대신 각 테두리 선분만 정점으로 만듭니다. 다른 직사각형의 엄격한 내부에 있는 정점을 제거한 뒤
# BFS합니다.
from collections import deque

def solution(rectangle,characterX,characterY,itemX,itemY):
    rects=[tuple(2*v for v in rect) for rect in rectangle];points=set()
    for x1,y1,x2,y2 in rects:
        points.update((x,y) for x in range(x1,x2+1) for y in (y1,y2))
        points.update((x,y) for x in (x1,x2) for y in range(y1,y2+1))
    points={p for p in points if not any(x1<p[0]<x2 and y1<p[1]<y2 for x1,y1,x2,y2 in rects)}
    start=2*characterX,2*characterY;goal=2*itemX,2*itemY
    queue=deque([(start,0)]);seen={start}
    while queue:
        (x,y),distance=queue.popleft()
        if (x,y)==goal:return distance//2
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            p=x+dx,y+dy
            if p in points and p not in seen:seen.add(p);queue.append((p,distance+1))
    return 0
