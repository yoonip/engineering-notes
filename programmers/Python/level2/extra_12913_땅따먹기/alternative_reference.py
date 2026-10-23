def solution(land):
    def visit(row, previous):
        if row == len(land):
            return 0
        return max(land[row][col] + visit(row + 1, col) for col in range(4) if col != previous)
    return visit(0, -1)
