# heapify는 힙 구성, heapreplace는 최솟값 제거와 새 값 삽입을 한 번에 수행.
from heapq import heapify, heapreplace

# 처리할 수 있는 시간과 남은 작업량 목록을 받음.
def solution(n, works):
    # 시간 안에 일을 전부 끝낼 수 있는지 확인.
    if sum(works) <= n:
        # 작업량은 음수가 되지 않으므로 모두 끝내면 피로도 0.
        return 0
    # 음수를 넣어 최소 힙을 최대 작업량 힙처럼 사용.
    heap = [-work for work in works]
    # 맨 앞이 가장 큰 작업량의 음수.
    heapify(heap)
    # range(n)은 n번 반복, _는 사용하지 않는 반복 변수.
    for _ in range(n):
        # 음수에 1을 더하면 원래 최대 작업량은 1 줄어듦.
        heapreplace(heap, heap[0] + 1)
    # 음수도 제곱하면 원래 양수의 제곱과 같음.
    return sum(work * work for work in heap)
