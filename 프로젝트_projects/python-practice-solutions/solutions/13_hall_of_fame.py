# 명예의 전당 (1)
# 분류: 최소 힙
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/138477
# 선택 이유: 명예의 전당에는 상위 k개만 최소 힙으로 유지한다. 매일 전체 점수를 다시 정렬하지 않는다.
# 비용: 점수 N개: 시간 O(N log(k+1)), 추가 공간 O(min(N,k))이며 반환 리스트는 제외한다.

import heapq


def solution(k, score):
    hall = []
    answer = []

    for point in score:
        heapq.heappush(hall, point)

        if len(hall) > k:
            heapq.heappop(hall)

        answer.append(hall[0])

    return answer
