def solution(cap, n, deliveries, pickups):
    delivery = pickup = answer = 0
    # 가장 먼 집부터 처리하면 필수 운행의 여유를 가까운 집에 쓸 수 있다.
    for index in range(n - 1, -1, -1):
        delivery += deliveries[index]
        pickup += pickups[index]
        # 배달과 수거 중 더 많은 왕복을 요구하는 쪽에 맞춘다.
        trips = max(0, (delivery + cap - 1) // cap, (pickup + cap - 1) // cap)
        answer += trips * (index + 1) * 2
        # 음수는 이 운행에 남은 용량이므로 그대로 유지한다.
        delivery -= trips * cap
        pickup -= trips * cap
    return answer
