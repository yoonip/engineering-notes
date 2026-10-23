# heappush는 삽입, heappop은 최솟값 추출.
from heapq import heappush, heappop

# 정점 수·출발지·목적지 둘·요금 목록을 받음.
def solution(n, s, a, b, fares):
    # 1번부터 n번까지 인접 간선들을 저장할 중첩 리스트.
    graph = [[] for _ in range(n + 1)]
    # for로 각 도로의 두 정점과 요금을 언패킹.
    for u, v, cost in fares:
        # 이웃 정점과 요금을 묶어 저장.
        graph[u].append((v, cost))
        # 양방향 도로이므로 반대 방향도 추가.
        graph[v].append((u, cost))
    # 음수가 아닌 요금에서 한 출발점의 최단 거리를 찾는 다익스트라 함수.
    def dijkstra(start):
        # 아직 도달하지 않은 정점의 거리.
        distance = [float('inf')] * (n + 1)
        # 자기 자신까지의 요금은 0.
        distance[start] = 0
        # 튜플은 앞 원소부터 비교됨.
        heap = [(0, start)]
        # 힙에 후보가 남아 있는 동안 반복.
        while heap:
            # 현재까지 알려진 거리가 가장 작은 후보를 꺼냄.
            cost, node = heappop(heap)
            # 이후 더 짧은 경로가 생긴 오래된 후보 제외.
            if cost != distance[node]:
                # 이번 반복을 건너뜀.
                continue
            # 현재 정점의 이웃과 도로 요금 순회.
            for neighbor, fare in graph[node]:
                # 이 도로를 거쳐 가는 새 거리.
                candidate = cost + fare
                # 더 싼 경로인지 비교.
                if candidate < distance[neighbor]:
                    # []로 최단 거리 갱신.
                    distance[neighbor] = candidate
                    # 갱신한 후보를 최소 힙에 추가.
                    heappush(heap, (candidate, neighbor))
        # 출발점에서 모든 정점까지의 최단 요금 반환.
        return distance
    # 출발지에서 각 분기점까지의 요금.
    from_start = dijkstra(s)
    # 무방향이므로 a에서 분기점까지 = 분기점에서 a까지.
    from_a = dijkstra(a)
    # b까지의 별도 이동 비용도 계산.
    from_b = dijkstra(b)
    # 모든 분기점에 대해 합승 한 번+개별 이동 둘을 비교.
    return min(from_start[i] + from_a[i] + from_b[i] for i in range(1, n + 1))
