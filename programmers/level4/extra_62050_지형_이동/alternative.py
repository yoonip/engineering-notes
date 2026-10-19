def solution(land, height):
    n=len(land);parent=list(range(n*n));size=[1]*(n*n);edges=[]
    def find(a):
        while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
        return a
    for r in range(n):
        for c in range(n):
            for dr,dc in ((1,0),(0,1)):
                nr,nc=r+dr,c+dc
                if nr<n and nc<n:
                    difference=abs(land[r][c]-land[nr][nc])
                    edges.append((difference if difference>height else 0,r*n+c,nr*n+nc))
    answer=0
    for cost,a,b in sorted(edges):
        a,b=find(a),find(b)
        if a!=b:
            if size[a]<size[b]:a,b=b,a
            parent[b]=a;size[a]+=size[b];answer+=cost
    return answer
