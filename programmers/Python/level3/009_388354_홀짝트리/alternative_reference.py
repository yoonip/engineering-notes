def solution(nodes, edges):
    graph = {node: [] for node in nodes}
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    unseen, answer = set(nodes), [0, 0]
    while unseen:
        first = next(iter(unseen))
        component, stack = [], [first]
        unseen.remove(first)
        while stack:
            node = stack.pop()
            component.append(node)
            for nxt in graph[node]:
                if nxt in unseen:
                    unseen.remove(nxt)
                    stack.append(nxt)
        possible = [False, False]
        for root in component:
            good, inverse = True, True
            stack = [(root, None)]
            while stack:
                node, parent = stack.pop()
                children = [nxt for nxt in graph[node] if nxt != parent]
                matches = node % 2 == len(children) % 2
                good &= matches
                inverse &= not matches
                stack.extend((nxt, node) for nxt in children)
            possible[0] |= good
            possible[1] |= inverse
        answer[0] += possible[0]
        answer[1] += possible[1]
    return answer
