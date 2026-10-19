from heapq import heappush, heappop

def solution(maps):
    rows, cols = len(maps), len(maps[0])
    distance = {(0, 0): 1}
    heap = [(1, 0, 0)]
    while heap:
        cost, r, c = heappop(heap)
        if cost != distance[(r, c)]:
            continue
        if (r, c) == (rows - 1, cols - 1):
            return cost
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maps[nr][nc] and cost + 1 < distance.get((nr, nc), float('inf')):
                distance[(nr, nc)] = cost + 1
                heappush(heap, (cost + 1, nr, nc))
    return -1
