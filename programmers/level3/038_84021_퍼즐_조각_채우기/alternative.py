# 빈 공간과 조각을 각각 추출한 뒤 네 회전을 직접 비교합니다. 같은 모양을 Counter로 세는 대신 이분 매칭으로 조각의
# 중복 사용을 막습니다.
def solution(game_board,table):
    def extract(grid,value):
        n=len(grid);seen=set();result=[]
        for r in range(n):
            for c in range(n):
                if grid[r][c]!=value or (r,c) in seen:continue
                stack=[(r,c)];seen.add((r,c));cells=[]
                while stack:
                    a,b=stack.pop();cells.append((a,b))
                    for da,db in ((1,0),(-1,0),(0,1),(0,-1)):
                        p=a+da,b+db
                        if 0<=p[0]<n and 0<=p[1]<n and grid[p[0]][p[1]]==value and p not in seen:
                            seen.add(p);stack.append(p)
                result.append(cells)
        return result
    def norm(cells):
        a=min(r for r,c in cells);b=min(c for r,c in cells)
        return sorted((r-a,c-b) for r,c in cells)
    holes=extract(game_board,0);pieces=extract(table,1);adj=[]
    for hole in holes:
        options=[]
        for j,piece in enumerate(pieces):
            if len(hole)!=len(piece):continue
            rotated=piece[:]
            for _ in range(4):
                if norm(hole)==norm(rotated):options.append(j);break
                rotated=[(c,-r) for r,c in rotated]
        adj.append(options)
    matched={}
    def assign(h,seen):
        for p in adj[h]:
            if p in seen:continue
            seen.add(p)
            if p not in matched or assign(matched[p],seen):matched[p]=h;return True
        return False
    return sum(len(hole) for h,hole in enumerate(holes) if assign(h,set()))
