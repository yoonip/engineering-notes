def solution(n, lighthouse):
    graph = [[] for _ in range(n + 1)]
    for a, b in lighthouse:
        graph[a].append(b)
        graph[b].append(a)
    parent = [0] * (n + 1)
    order = [1]
    for node in order:
        for neighbor in graph[node]:
            if neighbor != parent[node]:
                parent[neighbor] = node
                order.append(neighbor)
    off = [0] * (n + 1)
    on = [1] * (n + 1)
    for node in reversed(order[1:]):
        p = parent[node]
        off[p] += on[node]
        on[p] += min(off[node], on[node])
    return min(off[1], on[1])

# 전체 코드 줄별 설명
# def solution(n, lighthouse):  # def는 함수 정의. n은 등대 수, lighthouse는 연결된 두 등대의 목록.
#     graph = [[] for _ in range(n + 1)]  # [] 리스트 내포로 1~n번의 인접 리스트 생성. _는 사용하지 않는 반복 변수.
#     for a, b in lighthouse:  # for~in으로 간선 양 끝을 언패킹.
#         graph[a].append(b)  # append는 이웃 하나 추가.
#         graph[b].append(a)  # 무방향 연결이므로 반대쪽에도 추가.
#     parent = [0] * (n + 1)  # []와 * 반복으로 부모 번호 초기화.
#     order = [1]  # 1번을 임시 루트로 정하고 방문 순서를 저장.
#     for node in order:  # 리스트 순회는 뒤에 추가된 원소도 차례로 처리. 부모가 자식보다 먼저 나오는 순서를 만듦.
#         for neighbor in graph[node]:  # 현재 노드의 이웃 순회.
#             if neighbor != parent[node]:  # if는 조건문, !=는 다름. 트리이므로 부모 방향만 제외하면 미방문 자식.
#                 parent[neighbor] = node  # 자식의 부모 기록.
#                 order.append(neighbor)  # 방문 순서의 뒤에 자식 추가.
#     off = [0] * (n + 1)  # off[v]는 v를 끈 상태에서 그 부분 트리를 안전하게 만드는 최소 켠 등대 수.
#     on = [1] * (n + 1)  # on[v]는 v를 켠 상태의 최소 수. 자기 자신 한 개로 시작.
#     for node in reversed(order[1:]):  # [1:]은 루트 제외, reversed는 역순. 모든 자식을 계산한 뒤 부모에 합산.
#         p = parent[node]  # 현재 노드의 부모 번호.
#         off[p] += on[node]  # +=는 더해 저장. 부모가 꺼져 있으면 이 간선을 위해 자식은 반드시 켬.
#         on[p] += min(off[node], on[node])  # min은 작은 값. 부모가 켜져 있으면 자식은 켜거나 끄는 상태 중 최솟값 선택.
#     return min(off[1], on[1])  # return으로 임시 루트를 켜는 경우·끄는 경우 중 최소 등대 수 반환.

# 풀이 요약
# 모든 뱃길을 덮는 트리의 최소 정점 커버 문제입니다. 각 노드를 켜는 경우·끄는 경우의 최소 비용을 따로 둡니다.
# 부모가 꺼져 있으면 자식은 켜야 하고, 부모가 켜져 있으면 자식 두 상태 중 싼 쪽을 택합니다. 방문 순서를 뒤집어 재귀 깊이 문제 없이 계산합니다. 시간·공간 O(N).
# 예: 첫 예제에서 1번을 켜면 2·3·4번은 꺼도 되고, 5번을 켜면 6·7·8번도 꺼도 됩니다. 총 2개입니다.
# 