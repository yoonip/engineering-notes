def solution(rows,columns,queries):
    board=[[r*columns+c+1 for c in range(columns)] for r in range(rows)]
    answer=[]
    for a,b,x,y in queries:
        a,b,x,y=a-1,b-1,x-1,y-1
        carried=board[a][b]
        smallest=carried
        for r,c in ([(a,c) for c in range(b+1,y+1)] + [(r,y) for r in range(a+1,x+1)] + [(x,c) for c in range(y-1,b-1,-1)] + [(r,b) for r in range(x-1,a-1,-1)]):
            board[r][c],carried=carried,board[r][c]
            smallest=min(smallest,carried)
        answer.append(smallest)
    return answer
