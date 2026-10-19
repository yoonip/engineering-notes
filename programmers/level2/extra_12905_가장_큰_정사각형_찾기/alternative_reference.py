def solution(board):
    rows, cols = len(board), len(board[0])
    prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
    for r in range(rows):
        for c in range(cols):
            prefix[r + 1][c + 1] = board[r][c] + prefix[r][c + 1] + prefix[r + 1][c] - prefix[r][c]
    for side in range(min(rows, cols), 0, -1):
        for r in range(rows - side + 1):
            for c in range(cols - side + 1):
                count = prefix[r + side][c + side] - prefix[r][c + side] - prefix[r + side][c] + prefix[r][c]
                if count == side * side:
                    return side * side
    return 0
