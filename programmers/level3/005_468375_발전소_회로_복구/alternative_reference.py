from collections import deque

def solution(h, grid, panels, seqs):
    rows, cols = len(grid), len(grid[0])
    panel_at = {(f - 1, r - 1, c - 1): i for i, (f, r, c) in enumerate(panels)}
    required = [0] * len(panels)
    for a, b in seqs:
        required[b - 1] |= 1 << (a - 1)
    def activate(f, r, c, mask):
        i = panel_at.get((f, r, c))
        if i is not None and mask & required[i] == required[i]:
            mask |= 1 << i
        return mask
    f, r, c = (value - 1 for value in panels[0])
    start = (f, r, c, activate(f, r, c, 0))
    queue, seen = deque([(start, 0)]), {start}
    while queue:
        (f, r, c, mask), distance = queue.popleft()
        if mask == (1 << len(panels)) - 1:
            return distance
        candidates = [(f, r + dr, c + dc) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))]
        if grid[r][c] == '@':
            candidates += [(f - 1, r, c), (f + 1, r, c)]
        for nf, nr, nc in candidates:
            if 0 <= nf < h and 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
                state = (nf, nr, nc, activate(nf, nr, nc, mask))
                if state not in seen:
                    seen.add(state)
                    queue.append((state, distance + 1))
    return -1
