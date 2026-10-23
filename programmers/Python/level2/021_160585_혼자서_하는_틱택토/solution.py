def solution(board):
    text = ''.join(board)
    o, x = text.count('O'), text.count('X')
    # 선공 개수는 후공과 같거나 하나 많아야 한다.
    if o not in (x, x + 1):
        return 0
    lines = list(board)
    for c in range(3):
        lines.append(''.join(board[r][c] for r in range(3)))
    lines.append(''.join(board[i][i] for i in range(3)))
    lines.append(''.join(board[i][2 - i] for i in range(3)))
    o_win, x_win = 'OOO' in lines, 'XXX' in lines
    # 게임은 첫 승리에서 끝나므로 동시 승자는 불가능하다.
    if o_win and x_win:
        return 0
    if o_win and o != x + 1:
        return 0
    # 후공이 마지막에 이겼다면 두 사람의 수가 같다.
    if x_win and o != x:
        return 0
    return 1
