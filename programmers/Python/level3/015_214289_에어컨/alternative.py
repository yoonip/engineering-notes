# 시간과 온도를 정점으로 만들고 다익스트라로 최소 소비전력을 찾습니다. 기본 풀이는 매 분 모든 온도를 검사하고, 대안은
# 비용이 낮은 상태부터 꺼냅니다.
from heapq import heappush, heappop

def solution(temperature, t1, t2, a, b, onboard):
    heap = [(0, 0, temperature)]
    best = {(0, temperature): 0}
    while heap:
        cost, minute, temp = heappop(heap)
        if cost != best[(minute, temp)]:
            continue
        if minute == len(onboard) - 1:
            return cost
        # 꺼 두면 실외 온도 쪽으로 한 도 움직입니다.
        natural = temp + (temp < temperature) - (temp > temperature)
        for nxt, price in ((natural, 0), (temp, b), (temp-1, a), (temp+1, a)):
            if not -10 <= nxt <= 40 or onboard[minute+1] and not t1 <= nxt <= t2:
                continue
            state = minute+1, nxt
            if cost + price < best.get(state, float('inf')):
                best[state] = cost + price
                heappush(heap, (cost+price, minute+1, nxt))
