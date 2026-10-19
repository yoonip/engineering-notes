def solution(n):
    cost = [0] * (n + 1)
    for position in range(1, n + 1):
        cost[position] = cost[position - 1] + 1
        if position % 2 == 0:
            cost[position] = min(cost[position], cost[position // 2])
    return cost[n]
