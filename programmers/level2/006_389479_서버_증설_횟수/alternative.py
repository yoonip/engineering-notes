from heapq import heappush, heappop

def solution(players, m, k):
    expires = []
    active = answer = 0
    for hour, people in enumerate(players):
        while expires and expires[0][0] <= hour:
            _, count = heappop(expires)
            active -= count
        added = max(0, people//m-active)
        if added:
            heappush(expires, (hour+k, added))
            active += added
            answer += added
    return answer
