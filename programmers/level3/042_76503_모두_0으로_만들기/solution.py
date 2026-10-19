# a는 정점별 가중치, edges는 트리의 간선 목록.
def solution(a, edges):
    # 연산은 전체 합을 바꾸지 못하므로 합이 0이어야 함.
    if sum(a) != 0:
        # 불가능한 경우 즉시 -1 반환.
        return -1
    # len은 원소 개수.
    n = len(a)
    # _는 쓰지 않는 변수.
    graph = [[] for _ in range(n)]
    # for로 간선의 두 끝을 언패킹.
    for u, v in edges:
        # u에서 v로 연결.
        graph[u].append(v)
        # 무방향이므로 반대 방향도 추가.
        graph[v].append(u)
    # 각 정점의 부모를 기록.
    parent = [-1] * n
    # 루트 0부터 부모가 자식보다 먼저 나오는 방문 순서를 생성.
    order = [0]
    # 리스트에 새로 추가되는 자식도 차례로 방문.
    for node in order:
        # 현재 정점과 연결된 이웃 순회.
        for neighbor in graph[node]:
            # 트리이므로 부모 방향만 제외하면 아직 탐색하지 않은 자식.
            if neighbor != parent[node]:
                # []로 자식의 부모를 기록.
                parent[neighbor] = node
                # 방문 목록 끝에 자식 추가.
                order.append(neighbor)
    # 입력을 보존하면서 누적 가중치 계산.
    weight = a[:]
    # 연산 횟수 초기화.
    answer = 0
    # 자식부터 부모 방향으로 처리.
    for node in reversed(order[1:]):
        # 현재 가중치만큼 부모와 주고받아야 함.
        answer += abs(weight[node])
        # 현재 정점은 0이 된 것으로 간주.
        weight[parent[node]] += weight[node]
    # 모든 간선에서 필요한 이동량의 합 반환.
    return answer
