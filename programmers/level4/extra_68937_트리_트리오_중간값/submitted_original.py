from collections import deque

def solution(n, edges):
    graph = [[] for _ in range(n + 1)]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    def distances(start):
        distance = [-1] * (n + 1)
        distance[start] = 0
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if distance[neighbor] == -1:
                    distance[neighbor] = distance[node] + 1
                    queue.append(neighbor)
        return distance
    initial = distances(1)
    first = initial.index(max(initial))
    distance = distances(first)
    diameter = max(distance)
    if distance.count(diameter) >= 2:
        return diameter
    second = distance.index(diameter)
    other = distances(second)
    return diameter if other.count(diameter) >= 2 else diameter - 1

# 전체 코드 줄별 설명
# from collections import deque  # from A import B는 모듈에서 가져오기. deque는 양끝 작업이 빠르며 BFS의 큐로 사용.
# 
# def solution(n, edges):  # def는 함수 정의. 정점 수와 트리의 간선을 입력받음.
#     graph = [[] for _ in range(n + 1)]  # 리스트 내포로 정점별 독립적인 이웃 목록 생성. 번호는 1부터 사용.
#     for a, b in edges:  # 간선의 두 정점 번호를 나눠 받음.
#         graph[a].append(b)  # append는 리스트 끝에 추가. a의 이웃으로 b 등록.
#         graph[b].append(a)  # 트리는 양방향이므로 반대 연결도 등록.
#     def distances(start):  # 시작점부터 모든 정점의 거리를 구하는 내부 함수 정의.
#         distance = [-1] * (n + 1)  # -1은 아직 방문하지 않았다는 표시. 모든 정점 거리 초기화.
#         distance[start] = 0  # 시작점에서 자기 자신까지 거리는 0.
#         queue = deque([start])  # 먼저 넣은 정점을 먼저 꺼내는 FIFO 큐 초기화.
#         while queue:  # while은 큐가 비어 있지 않은 동안 반복.
#             node = queue.popleft()  # popleft는 덱 맨 앞 원소 제거·반환. 가까운 정점부터 처리하는 BFS.
#             for neighbor in graph[node]:  # 현재 정점의 모든 이웃을 검사.
#                 if distance[neighbor] == -1:  # if는 조건문. 아직 방문하지 않은 정점만 처리.
#                     distance[neighbor] = distance[node] + 1  # 간선 하나를 더 지나므로 거리 1 증가.
#                     queue.append(neighbor)  # 큐에 넣을 때 방문 처리하여 중복 탐색 방지.
#         return distance  # 시작점에서 모든 정점까지의 거리 목록 반환.
#     initial = distances(1)  # 임의의 1번 정점에서 거리 계산.
#     first = initial.index(max(initial))  # max는 최댓값, index는 그 값의 첫 위치. 트리 지름의 한 끝점을 찾음.
#     distance = distances(first)  # 지름 끝점에서 모든 정점까지 거리 계산.
#     diameter = max(distance)  # 지름은 트리에서 가장 긴 두 정점 사이 거리.
#     if distance.count(diameter) >= 2:  # count는 같은 값의 원소 수. 끝점에서 지름 거리인 정점이 두 개 이상인지 확인.
#         return diameter  # 세 정점 중 두 거리를 지름으로 만들 수 있어 중간값도 지름.
#     second = distance.index(diameter)  # 지름 반대쪽 끝점 번호를 찾음.
#     other = distances(second)  # 반대쪽에서도 최장 거리 정점의 중복 여부 검사.
#     return diameter if other.count(diameter) >= 2 else diameter - 1  # 조건 표현식. 지름을 공유하는 세 점이 없으면 최대 중간값은 지름-1.

# 풀이 요약
# BFS로 지름 양 끝점을 찾습니다. 어느 한 끝점에서 지름 거리의 정점이 둘 이상이면 두 거리가 지름인 세 점을 고를 수 있습니다.
# 그렇지 않으면 지름 경로에서 끝점 바로 옆 점을 세 번째 점으로 골라 지름-1을 얻습니다. 예: 4점 일자 트리는 2, 별 모양은 2.
# BFS를 최대 세 번 수행합니다. 시간·공간 O(n).
# 