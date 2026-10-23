def solution(a, edges):
    if sum(a) != 0:
        return -1
    n = len(a)
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    parent = [-1] * n
    order = [0]
    for node in order:
        for neighbor in graph[node]:
            if neighbor != parent[node]:
                parent[neighbor] = node
                order.append(neighbor)
    weight = a[:]
    answer = 0
    for node in reversed(order[1:]):
        answer += abs(weight[node])
        weight[parent[node]] += weight[node]
    return answer

# 전체 코드 줄별 설명
# def solution(a, edges):  # def는 함수 정의. a는 정점별 가중치, edges는 트리의 간선 목록.
#     if sum(a) != 0:  # sum은 합계, !=는 다름. 연산은 전체 합을 바꾸지 못하므로 합이 0이어야 함.
#         return -1  # 불가능한 경우 즉시 -1 반환.
#     n = len(a)  # len은 원소 개수.
#     graph = [[] for _ in range(n)]  # 리스트 컴프리헨션으로 정점별 인접 리스트 생성. _는 쓰지 않는 변수.
#     for u, v in edges:  # for로 간선의 두 끝을 언패킹.
#         graph[u].append(v)  # append는 끝에 추가. u에서 v로 연결.
#         graph[v].append(u)  # 무방향이므로 반대 방향도 추가.
#     parent = [-1] * n  # []는 리스트, *는 반복. 각 정점의 부모를 기록.
#     order = [0]  # 루트 0부터 부모가 자식보다 먼저 나오는 방문 순서를 생성.
#     for node in order:  # 리스트에 새로 추가되는 자식도 차례로 방문.
#         for neighbor in graph[node]:  # 현재 정점과 연결된 이웃 순회.
#             if neighbor != parent[node]:  # 트리이므로 부모 방향만 제외하면 아직 탐색하지 않은 자식.
#                 parent[neighbor] = node  # []로 자식의 부모를 기록.
#                 order.append(neighbor)  # 방문 목록 끝에 자식 추가.
#     weight = a[:]  # [:]는 리스트의 얕은 복사. 입력을 보존하면서 누적 가중치 계산.
#     answer = 0  # 연산 횟수 초기화.
#     for node in reversed(order[1:]):  # [1:]로 루트 제외, reversed로 역순. 자식부터 부모 방향으로 처리.
#         answer += abs(weight[node])  # abs는 절댓값, +=는 더해 저장. 현재 가중치만큼 부모와 주고받아야 함.
#         weight[parent[node]] += weight[node]  # 현재 정점의 남은 가중치를 부모에 합침. 현재 정점은 0이 된 것으로 간주.
#     return answer  # 모든 간선에서 필요한 이동량의 합 반환.

# 풀이 요약
# 전체 가중치 합이 0일 때만 가능하다. 잎부터 가중치를 부모에게 넘기고 넘긴 양의 절댓값을 더한다.
# 예: [-5,0,2,1,2]에서는 두 잎의 2씩과 가운데 누적 5를 옮겨 2+2+5=9번.
# 트리의 간선을 끊으면 부분 트리의 합만큼 반드시 그 간선을 지나야 하므로 이 횟수가 최소. 시간·공간 O(N).
# 