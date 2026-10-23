def solution(N, road, K):
    distance = [[float('inf')] * N for _ in range(N)]
    for village in range(N):
        distance[village][village] = 0
    for a, b, time in road:
        distance[a - 1][b - 1] = min(distance[a - 1][b - 1], time)
        distance[b - 1][a - 1] = distance[a - 1][b - 1]
    for via in range(N):
        for start in range(N):
            for end in range(N):
                distance[start][end] = min(distance[start][end], distance[start][via] + distance[via][end])
    return sum(time <= K for time in distance[0])
