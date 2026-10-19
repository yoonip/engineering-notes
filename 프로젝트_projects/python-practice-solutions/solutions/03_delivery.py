# 배달
# 분류: Dijkstra / 최소 힙
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/12978
# 선택 이유: 도로 가중치가 양수이므로 최소 힙 Dijkstra를 쓴다. 이미 짧아진 거리의 낡은 힙 항목은 건너뛴다.
# 비용: 정점 N, 도로 E: 시간 O((N+E) log(N+E)), 추가 공간 O(N+E).

import heapq


def solution(N, road, K):
    graph = [[] for _ in range(N + 1)]
    for a, b, cost in road:
        graph[a].append((b, cost))
        graph[b].append((a, cost))

    distance = [float("inf")] * (N + 1)
    distance[1] = 0
    heap = [(0, 1)]

    while heap:
        current_distance, village = heapq.heappop(heap)

        if current_distance > distance[village]:
            continue

        for next_village, cost in graph[village]:
            next_distance = current_distance + cost

            if next_distance < distance[next_village]:
                distance[next_village] = next_distance
                heapq.heappush(heap, (next_distance, next_village))

    answer = 0
    for village in range(1, N + 1):
        if distance[village] <= K:
            answer += 1

    return answer
