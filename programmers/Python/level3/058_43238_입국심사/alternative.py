# 다음 심사가 끝나는 시각을 힙에서 하나씩 꺼냅니다. 실제 사람 수만큼 이벤트를 처리하므로 n이 큰 원래 제한에는 이분탐색이
# 필요합니다.
# 작은 입력의 비교·검증용입니다. 원래 최대 입력 제출에는 기본 풀이를 사용합니다.
from heapq import heapify,heapreplace

def solution(n,times):
    heap=[(duration,i,duration) for i,duration in enumerate(times)];heapify(heap)
    answer=0
    for _ in range(n):
        answer,index,duration=heap[0]
        heapreplace(heap,(answer+duration,index,duration))
    return answer
