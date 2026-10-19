from heapq import heappush, heappop

def solution(N, road, K):
    graph = [[] for _ in range(N)]
    for a, b, cost in road:
        graph[a - 1].append((b - 1, cost))
        graph[b - 1].append((a - 1, cost))
    distances = [float('inf')] * N
    distances[0] = 0
    heap = [(0, 0)]
    while heap:
        distance, node = heappop(heap)
        if distance != distances[node]:
            continue
        for neighbor, cost in graph[node]:
            candidate = distance + cost
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                heappush(heap, (candidate, neighbor))
    return sum(distance <= K for distance in distances)
