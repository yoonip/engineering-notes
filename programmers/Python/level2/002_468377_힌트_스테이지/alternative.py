def solution(cost, hint):
    n = len(cost)
    answer = float('inf')
    for mask in range(1 << (n - 1)):
        tickets = [0] * n
        price = 0
        for i, bundle in enumerate(hint):
            if mask & (1 << i):
                price += bundle[0]
                for stage in bundle[1:]:
                    tickets[stage-1] += 1
        # 이전 단계에서만 지급되는 티켓이므로 구매 집합만 알면 비용이 확정된다.
        price += sum(cost[i][min(n-1, tickets[i])] for i in range(n))
        answer = min(answer, price)
    return answer
