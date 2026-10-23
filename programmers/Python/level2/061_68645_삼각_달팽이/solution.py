def solution(n):
    board = [[0] * (r + 1) for r in range(n)]
    r, c, value = -1, 0, 1
    directions = ((1, 0), (0, 1), (-1, -1))
    # 이동 길이를 하나씩 줄이며 세 방향을 순환한다.
    for side in range(n):
        dr, dc = directions[side % 3]
        for _ in range(n - side):
            r += dr
            c += dc
            board[r][c] = value
            value += 1
    # 채운 경로 순서가 아니라 행 순서로 펼친다.
    return [number for row in board for number in row]
