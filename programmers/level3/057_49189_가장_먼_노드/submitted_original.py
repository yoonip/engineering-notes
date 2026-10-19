from collections import deque

def solution(n, edge):
    graph = [[] for _ in range(n + 1)]
    for first, second in edge:
        graph[first].append(second)
        graph[second].append(first)
    distance = [-1] * (n + 1)
    distance[1] = 0
    queue = deque([1])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if distance[neighbor] == -1:
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)
    return distance.count(max(distance))

# 전체 코드 줄별 설명
# from collections import deque  # import는 도구 가져오기. deque는 앞에서 빠르게 꺼낼 수 있는 큐 자료구조.
# 
# def solution(n, edge):  # def는 함수 정의. 노드 수와 양방향 간선 목록을 받음.
#     graph = [[] for _ in range(n + 1)]  # []는 리스트. 1~n번 노드별 인접 노드 목록 생성.
#     for first, second in edge:  # for로 간선의 양 끝을 언패킹.
#         graph[first].append(second)  # append는 리스트 끝에 추가.
#         graph[second].append(first)  # 반대 방향도 기록.
#     distance = [-1] * (n + 1)  # *는 리스트 반복. -1은 아직 방문하지 않은 상태.
#     distance[1] = 0  # []로 인덱스 접근. 출발점 1까지의 거리는 0.
#     queue = deque([1])  # 출발점을 담은 선입선출 큐 생성.
#     while queue:  # 큐가 비어 있지 않은 동안 반복하는 너비 우선 탐색(BFS).
#         node = queue.popleft()  # 가장 먼저 넣은 노드를 꺼내 삭제.
#         for neighbor in graph[node]:  # 인접 노드 순회.
#             if distance[neighbor] == -1:  # ==는 같음. 처음 발견한 노드만 방문.
#                 distance[neighbor] = distance[node] + 1  # 간선 하나를 지나므로 거리 1 증가. BFS라 첫 발견 거리가 최단 거리.
#                 queue.append(neighbor)  # 새 노드를 큐 끝에 추가.
#     return distance.count(max(distance))  # max는 최대 거리, count는 그 값의 개수. 가장 먼 노드 수 반환.

# 풀이 요약
# 모든 간선의 길이가 1이므로 BFS를 사용한다. 시작점에서 가까운 노드부터 방문하며 최단 거리를 기록한다.
# 예제에서는 거리 0에 1번, 거리 1에 2·3번, 거리 2에 4·5·6번이 있어 답은 3이다.
# 노드 N, 간선 M일 때 시간·공간 O(N+M).
# 