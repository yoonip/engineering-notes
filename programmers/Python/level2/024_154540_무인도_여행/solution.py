def solution(maps):
    board = [list(row) for row in maps]
    rows, cols = len(board), len(board[0])
    answer = []
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'X':
                continue
            food = int(board[r][c])
            # 방문한 육지를 지워 같은 식량을 중복해서 더하지 않는다.
            board[r][c] = 'X'
            stack = [(r, c)]
            while stack:
                x, y = stack.pop()
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and board[nx][ny] != 'X':
                        # 상하좌우로 이어진 섬의 식량을 모두 합한다.
                        food += int(board[nx][ny])
                        board[nx][ny] = 'X'
                        stack.append((nx, ny))
            answer.append(food)
    return sorted(answer) if answer else [-1]
