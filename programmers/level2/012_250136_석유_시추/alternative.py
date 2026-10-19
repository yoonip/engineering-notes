def solution(land):
    rows, cols = len(land), len(land[0])
    parent = list(range(rows*cols))
    size = [1]*(rows*cols)
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a,b):
        a,b = find(a),find(b)
        if a==b:
            return
        if size[a] < size[b]:
            a,b=b,a
        parent[b]=a
        size[a]+=size[b]
    for r in range(rows):
        for c in range(cols):
            if land[r][c]:
                if r and land[r-1][c]: union(r*cols+c,(r-1)*cols+c)
                if c and land[r][c-1]: union(r*cols+c,r*cols+c-1)
    return max(sum(size[root] for root in {find(r*cols+c) for r in range(rows) if land[r][c]}) for c in range(cols))
