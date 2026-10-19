# 문제: 디펜스 게임
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/142085
# 풀이: 최소 힙에 큰 공격 K개를 남겨 무적권에 배정한다. 힙에서 빠진 가장 작은 공격만 병사로 막아 매번 전체를 정렬하지 않는다.
# 복잡도: 라운드 N개·무적권 K개: 시간 O(N log(min(K,N)+1)), 추가 공간 O(min(K,N)+1).

from heapq import heappush, heappop

def solution(n, k, enemy):
    shielded = []
    for index, count in enumerate(enemy):
        heappush(shielded, count)
        if len(shielded) > k:
            n -= heappop(shielded)
        if n < 0:
            return index
    return len(enemy)
