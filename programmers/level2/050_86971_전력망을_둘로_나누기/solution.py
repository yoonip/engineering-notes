def solution(n, wires):
    graph = [[] for _ in range(n + 1)]
    for a, b in wires:
        graph[a].append(b)
        graph[b].append(a)
    answer = n
    def dfs(node, parent):
        nonlocal answer
        size = 1
        for neighbor in graph[node]:
            if neighbor == parent:
                continue
            # 자식 아래에 연결된 송전탑 수를 구한다.
            child_size = dfs(neighbor, node)
            # 이 간선을 끊으면 자식 부분과 나머지로 갈라진다.
            answer = min(answer, abs(n - 2 * child_size))
            size += child_size
        return size
    dfs(1, 0)
    return answer
