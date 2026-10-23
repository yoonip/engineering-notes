# deque는 앞에서 빠르게 꺼낼 수 있는 큐 자료구조.
from collections import deque

# 노드 수와 양방향 간선 목록을 받음.
def solution(n, edge):
    # 1~n번 노드별 인접 노드 목록 생성.
    graph = [[] for _ in range(n + 1)]
    # for로 간선의 양 끝을 언패킹.
    for first, second in edge:
        # append는 리스트 끝에 추가.
        graph[first].append(second)
        # 반대 방향도 기록.
        graph[second].append(first)
    # -1은 아직 방문하지 않은 상태.
    distance = [-1] * (n + 1)
    # 출발점 1까지의 거리는 0.
    distance[1] = 0
    # 출발점을 담은 선입선출 큐 생성.
    queue = deque([1])
    # 큐가 비어 있지 않은 동안 반복하는 너비 우선 탐색(BFS).
    while queue:
        # 가장 먼저 넣은 노드를 꺼내 삭제.
        node = queue.popleft()
        # 인접 노드 순회.
        for neighbor in graph[node]:
            # 처음 발견한 노드만 방문.
            if distance[neighbor] == -1:
                # BFS라 첫 발견 거리가 최단 거리.
                distance[neighbor] = distance[node] + 1
                # 새 노드를 큐 끝에 추가.
                queue.append(neighbor)
    # 가장 먼 노드 수 반환.
    return distance.count(max(distance))
