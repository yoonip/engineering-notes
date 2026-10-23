from collections import defaultdict

def solution(edges):
    incoming, graph = defaultdict(int), defaultdict(list)
    for a,b in edges:
        graph[a].append(b)
        incoming[b] += 1
    root = next(v for v in graph if incoming[v]==0 and len(graph[v])>=2)
    counts = [0,0,0]
    for start in graph[root]:
        seen, stack = set(), [start]
        while stack:
            node = stack.pop()
            if node in seen:
                continue
            seen.add(node)
            stack.extend(graph[node])
        edge_count = sum(len(graph[v]) for v in seen)
        # 연결 부분마다 E−V는 도넛 0, 막대 −1, 8자 1이다.
        kind = {0:0,-1:1,1:2}[edge_count-len(seen)]
        counts[kind] += 1
    return [root] + counts
