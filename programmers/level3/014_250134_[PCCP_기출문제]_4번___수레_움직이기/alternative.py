from collections import deque

def solution(maze):
    rows, cols = len(maze), len(maze[0])
    points = {maze[r][c]: r * cols + c for r in range(rows) for c in range(cols) if maze[r][c] in (1, 2, 3, 4)}
    def moves(pos, goal, mask):
        if pos == goal:
            return [pos]
        r, c = divmod(pos, cols)
        result = []
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            nxt = nr * cols + nc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != 5 and not (mask >> nxt & 1):
                result.append(nxt)
        return result
    start = (points[1], points[2], 1 << points[1], 1 << points[2])
    queue, seen = deque([(start, 0)]), {start}
    while queue:
        (red, blue, rm, bm), turns = queue.popleft()
        if (red, blue) == (points[3], points[4]):
            return turns
        for nr in moves(red, points[3], rm):
            for nb in moves(blue, points[4], bm):
                if nr == nb or (nr == blue and nb == red):
                    continue
                state = (nr, nb, rm | (1 << nr), bm | (1 << nb))
                if state not in seen:
                    seen.add(state)
                    queue.append((state, turns + 1))
    return 0
