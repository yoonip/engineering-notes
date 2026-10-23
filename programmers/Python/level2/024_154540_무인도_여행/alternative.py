from collections import defaultdict

def solution(maps):
    rows,cols=len(maps),len(maps[0])
    parent=list(range(rows*cols))
    def find(x):
        if parent[x]!=x: parent[x]=find(parent[x])
        return parent[x]
    for r in range(rows):
        for c in range(cols):
            if maps[r][c]=='X': continue
            for dr,dc in ((-1,0),(0,-1)):
                nr,nc=r+dr,c+dc
                if nr>=0 and nc>=0 and maps[nr][nc]!='X':
                    a,b=find(r*cols+c),find(nr*cols+nc)
                    if a!=b: parent[max(a,b)]=min(a,b)
    totals=defaultdict(int)
    for r in range(rows):
        for c in range(cols):
            if maps[r][c]!='X': totals[find(r*cols+c)]+=int(maps[r][c])
    return sorted(totals.values()) or [-1]
