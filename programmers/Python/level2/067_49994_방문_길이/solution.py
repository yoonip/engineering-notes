def solution(dirs):
    # {} 딕셔너리에 명령별 이동량 () 튜플 저장.
    moves = {'U': (0, 1), 'D': (0, -1), 'R': (1, 0), 'L': (-1, 0)}
    x = y = 0
    edges = set()
    # 명령 순회.
    for command in dirs:
        dx, dy = moves[command]
        # +로 다음 좌표 계산.
        nx, ny = x + dx, y + dy
        if -5 <= nx <= 5 and -5 <= ny <= 5:
            # 반대 방향 이동도 같은 길로 표현.
            edge = tuple(sorted(((x, y), (nx, ny))))
            edges.add(edge)
            # 유효한 이동에서만 현재 좌표 갱신.
            x, y = nx, ny
    return len(edges)
