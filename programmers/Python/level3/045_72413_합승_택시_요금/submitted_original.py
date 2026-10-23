from heapq import heappush, heappop

def solution(n, s, a, b, fares):
    graph = [[] for _ in range(n + 1)]
    for u, v, cost in fares:
        graph[u].append((v, cost))
        graph[v].append((u, cost))
    def dijkstra(start):
        distance = [float('inf')] * (n + 1)
        distance[start] = 0
        heap = [(0, start)]
        while heap:
            cost, node = heappop(heap)
            if cost != distance[node]:
                continue
            for neighbor, fare in graph[node]:
                candidate = cost + fare
                if candidate < distance[neighbor]:
                    distance[neighbor] = candidate
                    heappush(heap, (candidate, neighbor))
        return distance
    from_start = dijkstra(s)
    from_a = dijkstra(a)
    from_b = dijkstra(b)
    return min(from_start[i] + from_a[i] + from_b[i] for i in range(1, n + 1))

# 전체 코드 줄별 설명
# from heapq import heappush, heappop  # import는 도구 가져오기. 최소 힙은 가장 작은 값부터 꺼내는 자료구조. heappush는 삽입, heappop은 최솟값 추출.
# 
# def solution(n, s, a, b, fares):  # def는 함수 정의. 정점 수·출발지·목적지 둘·요금 목록을 받음.
#     graph = [[] for _ in range(n + 1)]  # []는 리스트. 1번부터 n번까지 인접 간선들을 저장할 중첩 리스트.
#     for u, v, cost in fares:  # for로 각 도로의 두 정점과 요금을 언패킹.
#         graph[u].append((v, cost))  # append는 끝에 추가, ()는 튜플. 이웃 정점과 요금을 묶어 저장.
#         graph[v].append((u, cost))  # 양방향 도로이므로 반대 방향도 추가.
#     def dijkstra(start):  # 음수가 아닌 요금에서 한 출발점의 최단 거리를 찾는 다익스트라 함수.
#         distance = [float('inf')] * (n + 1)  # float('inf')는 무한대. 아직 도달하지 않은 정점의 거리.
#         distance[start] = 0  # 자기 자신까지의 요금은 0.
#         heap = [(0, start)]  # (거리,정점) 튜플을 저장하는 최소 힙. 튜플은 앞 원소부터 비교됨.
#         while heap:  # 힙에 후보가 남아 있는 동안 반복.
#             cost, node = heappop(heap)  # 현재까지 알려진 거리가 가장 작은 후보를 꺼냄.
#             if cost != distance[node]:  # !=는 다름. 이후 더 짧은 경로가 생긴 오래된 후보 제외.
#                 continue  # 이번 반복을 건너뜀.
#             for neighbor, fare in graph[node]:  # 현재 정점의 이웃과 도로 요금 순회.
#                 candidate = cost + fare  # 이 도로를 거쳐 가는 새 거리.
#                 if candidate < distance[neighbor]:  # 더 싼 경로인지 비교.
#                     distance[neighbor] = candidate  # []로 최단 거리 갱신.
#                     heappush(heap, (candidate, neighbor))  # 갱신한 후보를 최소 힙에 추가.
#         return distance  # 출발점에서 모든 정점까지의 최단 요금 반환.
#     from_start = dijkstra(s)  # 출발지에서 각 분기점까지의 요금.
#     from_a = dijkstra(a)  # 무방향이므로 a에서 분기점까지 = 분기점에서 a까지.
#     from_b = dijkstra(b)  # b까지의 별도 이동 비용도 계산.
#     return min(from_start[i] + from_a[i] + from_b[i] for i in range(1, n + 1))  # min은 최솟값. 모든 분기점에 대해 합승 한 번+개별 이동 둘을 비교.

# 풀이 요약
# 분기점 i까지 합승하고 이후 각 목적지로 간다. s·a·b에서 다익스트라를 한 번씩 실행해 세 거리의 합을 최소화한다.
# 예제 3은 4→6 합승 7원, 이후 6→5 11원으로 총 18원. 분기점=s이면 처음부터 따로 가는 경우도 포함된다.
# 간선 수 M일 때 시간 O((N+M) log N), 공간 O(N+M).
# 