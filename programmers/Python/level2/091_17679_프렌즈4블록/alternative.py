def solution(m, n, board):
    columns = [[board[r][c] for r in range(m)] for c in range(n)]
    answer = 0
    while True:
        marked = set()
        for c in range(n - 1):
            for r in range(m - 1):
                value = columns[c][r]
                if value and value == columns[c + 1][r] == columns[c][r + 1] == columns[c + 1][r + 1]:
                    marked.update(((c, r), (c + 1, r), (c, r + 1), (c + 1, r + 1)))
        if not marked:
            return answer
        answer += len(marked)
        for c, r in marked:
            columns[c][r] = ''
        for column in columns:
            for _ in range(m):
                for r in range(m - 1, 0, -1):
                    if not column[r] and column[r - 1]:
                        column[r], column[r - 1] = column[r - 1], ''
