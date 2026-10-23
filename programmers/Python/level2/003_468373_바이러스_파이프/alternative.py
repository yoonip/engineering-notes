def solution(n, infection, edges, k):
    graph = [[[] for _ in range(n)] for _ in range(3)]
    for a, b, kind in edges:
        graph[kind-1][a-1].append(b-1)
        graph[kind-1][b-1].append(a-1)
    frontier = {1 << (infection-1)}
    for _ in range(k):
        following = set()
        for mask in frontier:
            for kind in range(3):
                reached = mask
                stack = [v for v in range(n) if mask >> v & 1]
                while stack:
                    v = stack.pop()
                    for w in graph[kind][v]:
                        if not reached >> w & 1:
                            reached |= 1 << w
                            stack.append(w)
                following.add(reached)
        # 같은 감염 집합은 이후의 선택도 같으므로 한 번만 남긴다.
        frontier = following
    return max(mask.bit_count() for mask in frontier)
