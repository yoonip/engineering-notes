from collections import deque

def solution(places):
    def valid(room):
        for r in range(5):
            for c in range(5):
                if room[r][c]!='P': continue
                queue=deque([(r,c,0)])
                seen={(r,c)}
                while queue:
                    x,y,d=queue.popleft()
                    if d==2: continue
                    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                        nx,ny=x+dx,y+dy
                        if 0<=nx<5 and 0<=ny<5 and (nx,ny) not in seen and room[nx][ny]!='X':
                            if room[nx][ny]=='P': return 0
                            seen.add((nx,ny))
                            queue.append((nx,ny,d+1))
        return 1
    return [valid(room) for room in places]
