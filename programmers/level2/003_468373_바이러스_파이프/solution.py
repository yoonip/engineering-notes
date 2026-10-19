# 문제: 바이러스 파이프
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/468373
# 풀이: 파이프 종류별 연결요소를 비트마스크로 합친다. 같은 감염 집합에서는 남은 횟수가 더 적은 상태를 생략한다.
# 복잡도: 정점 N·간선 E·확장 상태 S·세 종류의 연결요소 총 G개: 시간 O(N+E+SG), 추가 공간 O(N+E+S). 비트마스크의 큰 정수 연산 비용은 별도다.

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
                component |= 1 << node
                for neighbor in graph[kind][node]:
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        stack.append(neighbor)
            groups[kind].append(component)

    answer = 1
    best_remaining = {}

    def dfs(mask, remaining):
        nonlocal answer
        # 같은 감염 집합에서 횟수가 더 남은 상태가 이미 있으면 생략한다.
        if best_remaining.get(mask, -1) >= remaining:
            return
        best_remaining[mask] = remaining
        answer = max(answer, mask.bit_count())
        if remaining == 0 or answer == n:
            return
        for components in groups:
            next_mask = mask
            for component in components:
                if mask & component:
                    next_mask |= component
            if next_mask != mask:
                dfs(next_mask, remaining - 1)

    dfs(1 << (infection - 1), k)
    return answer
