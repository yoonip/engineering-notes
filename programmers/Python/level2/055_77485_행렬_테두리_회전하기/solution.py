def solution(rows, columns, queries):
    board = [[r * columns + c + 1 for c in range(columns)] for r in range(rows)]
    answer = []
    for query in queries:
        top, left, bottom, right = [value - 1 for value in query]
        path = [(top, c) for c in range(left, right)]
        path.extend((r, right) for r in range(top, bottom))
        path.extend((bottom, c) for c in range(right, left, -1))
        path.extend((r, left) for r in range(bottom, top, -1))
        # 먼저 값을 복사해 회전 중 덮어쓰기 영향을 없앤다.
        values = [board[r][c] for r, c in path]
        for index, (r, c) in enumerate(path):
            # 시계방향 경로에서 바로 이전 칸의 값이 들어온다.
            board[r][c] = values[index - 1]
        answer.append(min(values))
    return answer
