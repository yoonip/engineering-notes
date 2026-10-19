# 문제: 배달
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/12978
# 풀이: 1번 마을의 거리만 필요해 인접 목록과 최소 힙 Dijkstra를 쓴다. 양수 도로 시간에서 K보다 긴 경로는 확장하지 않는다.
# 복잡도: 마을 V개·도로 E개: 시간 O((V+E) log(V+E)), 추가 공간 O(V+E). 중복 도로도 그대로 처리한다.

from heapq import heappop, heappush


def solution(N, road, K):
    graph = [[] for _ in range(N + 1)]
    for a, b, time in road:
        graph[a].append((b, time))
        graph[b].append((a, time))

    distance = [float('inf')] * (N + 1)
    distance[1] = 0
    queue = [(0, 1)]
    while queue:
        elapsed, village = heappop(queue)
        if elapsed != distance[village]:
            continue
        if elapsed > K:
            break
        for neighbor, time in graph[village]:
            candidate = elapsed + time
            if candidate < distance[neighbor] and candidate <= K:
                distance[neighbor] = candidate
                heappush(queue, (candidate, neighbor))
    return sum(time <= K for time in distance[1:])
