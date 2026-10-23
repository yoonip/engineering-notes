# 처음 모든 코어에 하나씩 주고, 그다음부터 (다음 빈 시각, 코어 번호)를 힙에서 꺼냅니다. 동시 시각에 작은 번호가 먼저
# 받는 규칙을 직접 따릅니다.
from heapq import heapify,heapreplace

def solution(n,cores):
    if n<=len(cores):return n
    heap=[(duration,i) for i,duration in enumerate(cores)];heapify(heap)
    for job in range(len(cores)+1,n+1):
        time,index=heap[0]
        if job==n:return index+1
        heapreplace(heap,(time+cores[index],index))
