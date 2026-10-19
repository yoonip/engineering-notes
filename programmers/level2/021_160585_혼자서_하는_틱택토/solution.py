# 문제: 혼자서 하는 틱택토
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/160585
# 풀이: O와 X 개수로 차례를 확인한 뒤 승리 선을 검사한다. 승자가 생긴 직후 게임이 끝나야 한다는 조건을 함께 적용한다.
# 복잡도: 3×3 고정 보드에서 시간·추가 공간 O(1).

def solution(board):
    text = ''.join(board)
    o, x = text.count('O'), text.count('X')
    if o not in (x, x + 1):
        return 0
    lines = list(board)
    for c in range(3):
        lines.append(''.join(board[r][c] for r in range(3)))
    lines.append(''.join(board[i][i] for i in range(3)))
    lines.append(''.join(board[i][2 - i] for i in range(3)))
    o_win, x_win = 'OOO' in lines, 'XXX' in lines
    if o_win and x_win:
        return 0
    if o_win and o != x + 1:
        return 0
    if x_win and o != x:
        return 0
    return 1
