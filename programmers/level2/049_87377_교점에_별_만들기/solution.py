from itertools import combinations

def solution(line):
    points = set()
    for first, second in combinations(line, 2):
        a, b, e = first
        c, d, f = second
        denominator = a * d - b * c
        # 평행한 직선 쌍은 유일한 교점이 없다.
        if denominator == 0:
            continue
        nx, ny = b * f - e * d, e * c - a * f
        # 나머지가 둘 다 0이어야 교점 좌표가 정수다.
        if nx % denominator == 0 and ny % denominator == 0:
            points.add((nx // denominator, ny // denominator))
    min_x = min(x for x, y in points)
    max_x = max(x for x, y in points)
    min_y = min(y for x, y in points)
    max_y = max(y for x, y in points)
    board = [['.'] * (max_x - min_x + 1) for _ in range(max_y - min_y + 1)]
    for x, y in points:
        # 화면 행은 아래로 증가하므로 y축 방향을 뒤집는다.
        board[max_y - y][x - min_x] = '*'
    return [''.join(row) for row in board]
