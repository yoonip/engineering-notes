def solution(msg):
    edges = [{} for _ in range(27)]
    root = {chr(65 + i): i + 1 for i in range(26)}
    output, start = [], 0
    while start < len(msg):
        node = root[msg[start]]
        end = start + 1
        while end < len(msg) and msg[end] in edges[node]:
            node = edges[node][msg[end]]
            end += 1
        output.append(node)
        if end < len(msg):
            edges[node][msg[end]] = len(edges)
            edges.append({})
        start = end
    return output
