# 비트마스크 대신 실제 보드를 한 칸 지웠다가 재귀가 끝나면 복원합니다. 캐시가 없어 느리지만 발판 소멸과 플레이어 교대
# 규칙을 눈으로 확인하기 쉽습니다.
# 작은 입력의 비교·검증용입니다. 원래 최대 입력 제출에는 기본 풀이를 사용합니다.
def solution(board,aloc,bloc):
    grid=[row[:] for row in board];n,m=len(grid),len(grid[0])
    def play(a,b):
        r,c=a
        if grid[r][c]==0:return False,0
        wins=[];losses=[]
        grid[r][c]=0
        for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
            nr,nc=r+dr,c+dc
            if 0<=nr<n and 0<=nc<m and grid[nr][nc]:
                won,turns=play(b,(nr,nc))
                (losses if won else wins).append(turns+1)
        grid[r][c]=1
        return (True,min(wins)) if wins else (False,max(losses,default=0))
    return play(tuple(aloc),tuple(bloc))[1]
