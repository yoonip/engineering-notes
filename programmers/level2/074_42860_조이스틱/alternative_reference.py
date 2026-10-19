from collections import deque

def solution(name):
    n = len(name)
    required = sum(1 << i for i, ch in enumerate(name) if ch != 'A')
    vertical = sum(min(ord(ch) - 65, 91 - ord(ch)) for ch in name)
    start = (0, required & ~1)
    queue = deque([(start[0], start[1], 0)])
    seen = {start}
    while queue:
        pos, left, cost = queue.popleft()
        if not left:
            return vertical + cost
        for nxt in ((pos - 1) % n, (pos + 1) % n):
            state = (nxt, left & ~(1 << nxt))
            if state not in seen:
                seen.add(state)
                queue.append((state[0], state[1], cost + 1))
