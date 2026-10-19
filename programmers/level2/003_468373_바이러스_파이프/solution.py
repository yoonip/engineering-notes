def solution(n, infection, edges, k):
    graph = [[[] for _ in range(n)] for _ in range(3)]
    for x, y, kind in edges:
        graph[kind - 1][x - 1].append(y - 1)
        graph[kind - 1][y - 1].append(x - 1)

    groups = [[] for _ in range(3)]
    for kind in range(3):
        visited = [False] * n
        for start in range(n):
            if visited[start]:
                continue
            visited[start] = True
            stack = [start]
            component = 0
            while stack:
                node = stack.pop()
                # 노드 번호에 해당하는 비트로 연결 요소를 표현한다.
                component |= 1 << node
                for neighbor in graph[kind][node]:
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        stack.append(neighbor)
            groups[kind].append(component)

    answer = 1

    def dfs(mask, remaining):
        nonlocal answer
        answer = max(answer, bin(mask).count('1'))
        if remaining == 0 or answer == n:
            return
        for components in groups:
            next_mask = mask
            for component in components:
                # 현재 감염과 닿은 연결 요소는 통째로 감염된다.
                if mask & component:
                    next_mask |= component
            # 감염이 늘지 않는 행동은 생략한다.
            if next_mask != mask:
                dfs(next_mask, remaining - 1)

    dfs(1 << (infection - 1), k)
    return answer
