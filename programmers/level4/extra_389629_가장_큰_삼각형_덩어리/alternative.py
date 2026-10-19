def solution(grid):
    n,m=len(grid),len(grid[0])
    cells=n*m
    if cells>6:
        raise ValueError("삼각형 부분집합을 전부 확인하는 6칸 이하 기준 풀이입니다")
    adjacency=[set() for _ in range(2*cells)]
    def link(a,b):
        adjacency[a].add(b)
        adjacency[b].add(a)
    for r in range(n):
        for c in range(m):
            cell=r*m+c
            if r+1<n:link(2*cell+1,2*(cell+m))
            if c+1<m:link(2*cell+(grid[r][c]==1),2*(cell+1)+(grid[r][c+1]==-1))
    best=0
    # 각 정사각형에서 위/아래 삼각형 하나 또는 아무것도 선택하지 않는다.
    def choose(cell,selected):
        nonlocal best
        if cell<cells:
            for node in (None,2*cell,2*cell+1):
                choose(cell+1,selected if node is None else selected|{node})
            return
        if len(selected)<=best:return
        reached={next(iter(selected))};pending=list(reached)
        while pending:
            for node in adjacency[pending.pop()]&selected-reached:
                reached.add(node);pending.append(node)
        if reached==selected:best=len(selected)
    choose(0,set())
    return best
