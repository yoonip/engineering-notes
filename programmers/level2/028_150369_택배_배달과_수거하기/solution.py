# 문제: 택배 배달과 수거하기
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/150369
# 풀이: 먼 집부터 필요한 왕복 횟수를 확정한다. 배달과 수거의 남는 용량을 가까운 집에 넘겨 각 집을 한 번씩 처리한다.
# 복잡도: 집 N개: 시간 O(N), 추가 공간 O(1).

def solution(cap, n, deliveries, pickups):
    delivery = pickup = answer = 0
    for index in range(n - 1, -1, -1):
        delivery += deliveries[index]
        pickup += pickups[index]
        trips = max(0, (delivery + cap - 1) // cap, (pickup + cap - 1) // cap)
        answer += trips * (index + 1) * 2
        delivery -= trips * cap
        pickup -= trips * cap
    return answer
