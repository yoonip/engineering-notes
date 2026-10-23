from collections import Counter

def solution(grid):
    rows,cols=len(grid),len(grid[0])
    count=rows*cols*4
    parent=list(range(count))
    size=[1]*count
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]
            x=parent[x]
        return x
    direction=((-1,0),(0,1),(1,0),(0,-1))
    for r in range(rows):
        for c in range(cols):
            for d in range(4):
                nd=(d+{'L':-1,'R':1,'S':0}[grid[r][c]])%4
                dr,dc=direction[nd]
                a=find((r*cols+c)*4+d)
                b=find((((r+dr)%rows)*cols+(c+dc)%cols)*4+nd)
                if a!=b:
                    if size[a]<size[b]: a,b=b,a
                    parent[b]=a
                    size[a]+=size[b]
    return sorted(Counter(find(i) for i in range(count)).values())
