def solution(rc, operations):
    board=[row[:] for row in rc];n,m=len(board),len(board[0])
    perimeter=[(0,c) for c in range(m)]+[(r,m-1) for r in range(1,n)]
    perimeter += [(n-1,c) for c in range(m-2,-1,-1)]+[(r,0) for r in range(n-2,0,-1)]
    for operation in operations:
        if operation=="ShiftRow":board=board[-1:]+board[:-1]
        else:
            old=[board[r][c] for r,c in perimeter]
            for index,(r,c) in enumerate(perimeter):board[r][c]=old[index-1]
    return board
