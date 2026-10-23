def solution(n,left,right):
    if n>500: raise ValueError('작은 배열의 규칙 확인용: n≤500')
    board=[[0]*n for _ in range(n)]
    for side in range(1,n+1):
        for row in range(side): board[row][side-1]=side
        for col in range(side-1): board[side-1][col]=side
    flat=[value for row in board for value in row]
    return flat[left:right+1]
