from itertools import product

def solution(visible, hidden, k):
    n, m = len(visible), len(visible[0])
    if n*m > 9:
        raise ValueError("전체 경로를 비교하는 작은 격자용 풀이입니다")
    answer = -10**18
    for flips in product((0, 1), repeat=n+m):
        values = [[hidden[r][c] if flips[r]^flips[n+c] else visible[r][c]
                   for c in range(m)] for r in range(n)]
        cost = k*sum(flips)
        def walk(r, c, visited, score):
            nonlocal answer
            if (r,c)==(n-1,m-1):
                answer=max(answer,score-cost)
                return
            for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                nr,nc=r+dr,c+dc
                if 0<=nr<n and 0<=nc<m and not visited>>(nr*m+nc)&1:
                    walk(nr,nc,visited|1<<(nr*m+nc),score+values[nr][nc])
        walk(0,0,1,values[0][0])
    return answer
