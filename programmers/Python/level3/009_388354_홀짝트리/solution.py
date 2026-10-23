def solution(nodes, edges):
    # 실제 노드 수.
    n = len(nodes)
    index = {node: i for i, node in enumerate(nodes)}
    # 서로소 집합의 부모를 자기 자신으로 초기화.
    parent = list(range(n))
    sizes = [1] * n
    # 노드별 연결된 간선 수인 차수 초기화.
    degrees = [0] * n

    def find(node):
        while parent[node] != node:
            # 다음 대표 탐색이 빨라지도록 조상으로 바로 연결.
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    # 간선 두 끝 번호를 언패킹.
    for a, b in edges:
        a, b = index[a], index[b]
        # a의 차수 증가.
        degrees[a] += 1
        degrees[b] += 1
        # 두 노드의 연결 집합 대표 조회.
        first, second = find(a), find(b)
        if first != second:
            # 작은 집합을 큰 집합에 붙이기 위해 순서 조정.
            if sizes[first] < sizes[second]:
                first, second = second, first
            # 두 집합을 하나로 합침.
            parent[second] = first
            sizes[first] += sizes[second]
    # 각 트리에서 번호와 차수의 홀짝이 같은 노드 수 저장.
    matches = [0] * n
    for i, node in enumerate(nodes):
        # 번호와 차수의 홀짝 일치 여부.
        if node % 2 == degrees[i] % 2:
            matches[find(i)] += 1
    # 홀짝 트리 수·역홀짝 트리 수를 담은 리스트.
    answer = [0, 0]
    for root in range(n):
        # 부모가 자기 자신이면 한 트리의 대표.
        if parent[root] == root:
            answer[0] += int(matches[root] == 1)
            # 불일치 노드가 정확히 하나이면 그 노드를 루트로 삼아 역홀짝 트리 가능.
            answer[1] += int(matches[root] == sizes[root] - 1)
    return answer
