def solution(n,wires):
    answer=n
    for removed in range(len(wires)):
        graph=[[] for _ in range(n+1)]
        for i,(a,b) in enumerate(wires):
            if i!=removed:
                graph[a].append(b)
                graph[b].append(a)
        seen={1}
        stack=[1]
        while stack:
            for other in graph[stack.pop()]:
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
        answer=min(answer,abs(n-2*len(seen)))
    return answer
