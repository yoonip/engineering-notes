from heapq import heapify, heappop, heappush

def solution(scoville, K):
    # 인덱스 0이 항상 최솟값.
    heapify(scoville)
    answer = 0
    while scoville[0] < K:
        # 음식이 하나면 더 섞을 수 없음.
        if len(scoville) < 2:
            return -1
        first = heappop(scoville)
        # 남은 것 중 가장 작은 음식, 즉 원래 둘째 음식 꺼내기.
        second = heappop(scoville)
        heappush(scoville, first + second * 2)
        answer += 1
    return answer
