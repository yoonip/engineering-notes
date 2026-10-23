# 방향을 포함한 모든 상태의 거리를 반복해서 완화합니다. 비용이 서로 달라 단순 BFS 최초 방문으로 확정할 수 없다는 점을
# 보여줍니다. 힙보다 느린 작은 보드 검증용입니다.
# 작은 입력의 비교·검증용입니다. 원래 최대 입력 제출에는 기본 풀이를 사용합니다.
def solution(board):
    n=len(board);dirs=((1,0),(-1,0),(0,1),(0,-1));inf=float('inf')
    d=[[[inf]*4 for _ in range(n)] for _ in range(n)]
    d[0][0]=[0]*4
    for _ in range(4*n*n):
        changed=False
        for r in range(n):
            for c in range(n):
                if board[r][c]:continue
                for old in range(4):
                    for new,(dr,dc) in enumerate(dirs):
                        nr,nc=r+dr,c+dc
                        if not (0<=nr<n and 0<=nc<n) or board[nr][nc]:continue
                        candidate=d[r][c][old]+100+500*(old!=new)
                        if candidate<d[nr][nc][new]:d[nr][nc][new]=candidate;changed=True
        if not changed:break
    return min(d[-1][-1])
