def solution(edges):
    size = max(max(a, b) for a, b in edges) + 1
    incoming = [0] * size
    outgoing = [0] * size
    for a, b in edges:
        outgoing[a] += 1
        incoming[b] += 1
    created = sticks = eights = 0
    for node in range(1, size):
        # 추가 정점은 들어오는 간선이 없고 두 개 이상으로 갈라진다.
        if incoming[node] == 0 and outgoing[node] >= 2:
            created = node
        # 막대 그래프마다 끝점이 하나씩 있다.
        elif outgoing[node] == 0 and incoming[node] > 0:
            sticks += 1
        elif outgoing[node] == 2 and incoming[node] >= 2:
            eights += 1
    # 전체 그래프 수에서 막대와 8자 수를 뺀다.
    donuts = outgoing[created] - sticks - eights
    return [created, donuts, sticks, eights]
