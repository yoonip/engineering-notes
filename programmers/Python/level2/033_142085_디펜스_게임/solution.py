from heapq import heappush, heappop

def solution(n, k, enemy):
    shielded = []
    for index, count in enumerate(enemy):
        # 현재까지 가장 큰 k개 공격에 무적권을 배정한다.
        heappush(shielded, count)
        if len(shielded) > k:
            # k개를 넘으면 가장 작은 공격을 병사로 막는 편이 유리하다.
            n -= heappop(shielded)
        if n < 0:
            return index
    return len(enemy)
