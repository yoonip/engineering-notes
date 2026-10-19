def solution(m, n, picture):
    parent = list(range(m * n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for r in range(m):
        for c in range(n):
            if not picture[r][c]:
                continue
            for dr, dc in ((1, 0), (0, 1)):
                nr, nc = r + dr, c + dc
                if nr < m and nc < n and picture[nr][nc] == picture[r][c]:
                    parent[find(nr * n + nc)] = find(r * n + c)
    sizes = {}
    for r in range(m):
        for c in range(n):
            if picture[r][c]:
                root = find(r * n + c)
                sizes[root] = sizes.get(root, 0) + 1
    return [len(sizes), max(sizes.values(), default=0)]
