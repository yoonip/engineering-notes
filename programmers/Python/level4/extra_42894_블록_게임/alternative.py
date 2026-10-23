from functools import cache

def solution(board):
    n=len(board);labels={x for row in board for x in row if x}
    if len(labels)>10:raise ValueError("블록 10개 이하의 제거 순서 전수 비교용입니다")
    @cache
    def search(state):
        grid=[state[r*n:(r+1)*n] for r in range(n)];best=0
        for label in set(state)-{0}:
            cells=[(r,c) for r in range(n) for c in range(n) if grid[r][c]==label]
            top=min(r for r,c in cells);bottom=max(r for r,c in cells)
            left=min(c for r,c in cells);right=max(c for r,c in cells)
            if (bottom-top+1)*(right-left+1)!=6:continue
            missing=[(r,c) for r in range(top,bottom+1) for c in range(left,right+1) if grid[r][c]!=label]
            if all(grid[r][c]==0 and all(grid[y][c]==0 for y in range(r)) for r,c in missing):
                following=tuple(0 if value==label else value for value in state)
                best=max(best,1+search(following))
        return best
    return search(tuple(x for row in board for x in row))
