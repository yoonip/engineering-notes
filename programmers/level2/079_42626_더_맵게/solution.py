# 문제: 더 맵게
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/42626
# 풀이: 최소 힙에서 가장 작은 두 음식을 꺼내 섞는다. 섞은 값을 다시 넣어 매번 전체 정렬 없이 다음 두 최솟값을 고른다.
# 복잡도: 음식 N개: 시간 O(N log N), 추가 공간 O(1). 입력 리스트를 힙으로 재사용한다.

from heapq import heapify, heappop, heappush

def solution(scoville, K):
    heapify(scoville)
    answer = 0
    while scoville[0] < K:
        if len(scoville) < 2:
            return -1
        first = heappop(scoville)
        second = heappop(scoville)
        heappush(scoville, first + second * 2)
        answer += 1
    return answer
