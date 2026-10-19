# 먼저 넣은 정점을 먼저 꺼내는 BFS 큐로 사용.
from collections import deque

# 지역 수·양방향 길·부대원 위치·복귀 지역 입력.
def solution(n, roads, sources, destination):
    # _는 사용하지 않는 반복 변수.
    graph = [[] for _ in range(n + 1)]
    # for~in으로 길의 두 끝 번호를 언패킹.
    for a, b in roads:
        # append로 a에서 b로 가는 이웃 추가.
        graph[a].append(b)
        # 양방향 길이므로 반대 연결도 추가.
        graph[b].append(a)
    # -1은 아직 도달하지 못한 지역.
    distance = [-1] * (n + 1)
    # 복귀 지역 자기 자신까지 거리는 0.
    distance[destination] = 0
    # 목적지에서 출발하는 BFS 시작 큐.
    queue = deque([destination])
    # 큐가 비면 탐색 완료.
    while queue:
        # popleft는 큐 맨 앞 정점을 제거·반환.
        node = queue.popleft()
        # 현재 지역에서 갈 수 있는 이웃 순회.
        for neighbor in graph[node]:
            # 미방문 이웃만 처리.
            if distance[neighbor] == -1:
                # 모든 길의 시간은 1이므로 첫 방문 거리가 최단시간.
                distance[neighbor] = distance[node] + 1
                # 큐에 넣는 순간 방문 표시를 끝내 중복 추가 방지.
                queue.append(neighbor)
    # 불가능한 지역은 -1 유지.
    return [distance[source] for source in sources]
