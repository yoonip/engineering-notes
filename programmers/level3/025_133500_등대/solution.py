# n은 등대 수, lighthouse는 연결된 두 등대의 목록.
def solution(n, lighthouse):
    # _는 사용하지 않는 반복 변수.
    graph = [[] for _ in range(n + 1)]
    # for~in으로 간선 양 끝을 언패킹.
    for a, b in lighthouse:
        # append는 이웃 하나 추가.
        graph[a].append(b)
        # 무방향 연결이므로 반대쪽에도 추가.
        graph[b].append(a)
    # []와 * 반복으로 부모 번호 초기화.
    parent = [0] * (n + 1)
    # 1번을 임시 루트로 정하고 방문 순서를 저장.
    order = [1]
    # 부모가 자식보다 먼저 나오는 순서를 만듦.
    for node in order:
        # 현재 노드의 이웃 순회.
        for neighbor in graph[node]:
            # 트리이므로 부모 방향만 제외하면 미방문 자식.
            if neighbor != parent[node]:
                # 자식의 부모 기록.
                parent[neighbor] = node
                # 방문 순서의 뒤에 자식 추가.
                order.append(neighbor)
    # off[v]는 v를 끈 상태에서 그 부분 트리를 안전하게 만드는 최소 켠 등대 수.
    off = [0] * (n + 1)
    # 자기 자신 한 개로 시작.
    on = [1] * (n + 1)
    # 모든 자식을 계산한 뒤 부모에 합산.
    for node in reversed(order[1:]):
        # 현재 노드의 부모 번호.
        p = parent[node]
        # 부모가 꺼져 있으면 이 간선을 위해 자식은 반드시 켬.
        off[p] += on[node]
        # 부모가 켜져 있으면 자식은 켜거나 끄는 상태 중 최솟값 선택.
        on[p] += min(off[node], on[node])
    # return으로 임시 루트를 켜는 경우·끄는 경우 중 최소 등대 수 반환.
    return min(off[1], on[1])
