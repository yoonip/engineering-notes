from collections import deque

def solution(n, roads, sources, destination):
    graph = [[] for _ in range(n + 1)]
    for a, b in roads:
        graph[a].append(b)
        graph[b].append(a)
    distance = [-1] * (n + 1)
    distance[destination] = 0
    queue = deque([destination])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if distance[neighbor] == -1:
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)
    return [distance[source] for source in sources]

# 전체 코드 줄별 설명
# from collections import deque  # collections에서 deque를 import. 먼저 넣은 정점을 먼저 꺼내는 BFS 큐로 사용.
# 
# def solution(n, roads, sources, destination):  # def는 함수 정의. 지역 수·양방향 길·부대원 위치·복귀 지역 입력.
#     graph = [[] for _ in range(n + 1)]  # [] 리스트 내포로 각 지역의 이웃 목록 생성. _는 사용하지 않는 반복 변수.
#     for a, b in roads:  # for~in으로 길의 두 끝 번호를 언패킹.
#         graph[a].append(b)  # append로 a에서 b로 가는 이웃 추가.
#         graph[b].append(a)  # 양방향 길이므로 반대 연결도 추가.
#     distance = [-1] * (n + 1)  # []와 * 반복. -1은 아직 도달하지 못한 지역.
#     distance[destination] = 0  # 복귀 지역 자기 자신까지 거리는 0.
#     queue = deque([destination])  # 목적지에서 출발하는 BFS 시작 큐.
#     while queue:  # while은 조건이 참인 동안 반복. 큐가 비면 탐색 완료.
#         node = queue.popleft()  # popleft는 큐 맨 앞 정점을 제거·반환.
#         for neighbor in graph[node]:  # 현재 지역에서 갈 수 있는 이웃 순회.
#             if distance[neighbor] == -1:  # if는 조건문, ==는 같음. 미방문 이웃만 처리.
#                 distance[neighbor] = distance[node] + 1  # 모든 길의 시간은 1이므로 첫 방문 거리가 최단시간.
#                 queue.append(neighbor)  # 큐에 넣는 순간 방문 표시를 끝내 중복 추가 방지.
#     return [distance[source] for source in sources]  # 리스트 내포로 원래 부대원 순서의 거리를 반환. 불가능한 지역은 -1 유지.

# 풀이 요약
# 길이 양방향이므로 각 출발지→목적지 거리와 목적지→각 출발지 거리가 같습니다. 목적지에서 BFS 한 번으로 모든 답을 구합니다.
# 거리를 -1로 시작해 도달하지 못한 지역을 그대로 구분합니다. 시간 O(N+E+S), 공간 O(N+E).
# 예: 두 번째 예제에서 5번부터 거리를 구하면 1번까지 2, 단절된 3번은 -1, 5번 자기 자신은 0입니다.
# 