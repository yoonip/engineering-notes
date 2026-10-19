from heapq import heapify, heapreplace

def solution(n, works):
    if sum(works) <= n:
        return 0
    heap = [-work for work in works]
    heapify(heap)
    for _ in range(n):
        heapreplace(heap, heap[0] + 1)
    return sum(work * work for work in heap)

# 전체 코드 줄별 설명
# from heapq import heapify, heapreplace  # import는 도구 가져오기. 최소 힙은 가장 작은 값을 맨 앞에 유지하는 자료구조. heapify는 힙 구성, heapreplace는 최솟값 제거와 새 값 삽입을 한 번에 수행.
# 
# def solution(n, works):  # def는 함수 정의. 처리할 수 있는 시간과 남은 작업량 목록을 받음.
#     if sum(works) <= n:  # sum은 합계. 시간 안에 일을 전부 끝낼 수 있는지 확인.
#         return 0  # 작업량은 음수가 되지 않으므로 모두 끝내면 피로도 0.
#     heap = [-work for work in works]  # []는 리스트 컴프리헨션. 음수를 넣어 최소 힙을 최대 작업량 힙처럼 사용.
#     heapify(heap)  # 리스트를 제자리에서 힙으로 바꿈. 맨 앞이 가장 큰 작업량의 음수.
#     for _ in range(n):  # range(n)은 n번 반복, _는 사용하지 않는 반복 변수.
#         heapreplace(heap, heap[0] + 1)  # [0]은 힙 최솟값. 음수에 1을 더하면 원래 최대 작업량은 1 줄어듦.
#     return sum(work * work for work in heap)  # 생성식으로 남은 작업량 제곱을 합산. 음수도 제곱하면 원래 양수의 제곱과 같음.

# 풀이 요약
# 작업량 x를 1 줄이면 제곱 합이 x²-(x-1)²=2x-1 감소한다. 따라서 매번 가장 큰 작업을 줄이는 것이 가장 이득이다.
# 예: [4,3,3]을 네 번 줄이면 [2,2,2]가 되어 피로도 12. 전체 합이 n보다 크므로 반복 중 최대 작업량이 0이 되는 일은 없다.
# 작업 수 W일 때 시간 O(W+n log W), 공간 O(W). heapreplace는 같은 힙의 최댓값 감소 처리를 효율적으로 한다.
# 