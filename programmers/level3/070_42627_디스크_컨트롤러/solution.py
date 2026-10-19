# 두 함수는 삽입·최솟값 추출.
from heapq import heappush, heappop

# 각 작업의 [요청 시각,소요 시간] 목록을 받음.
def solution(jobs):
    # 튜플을 요청 시각 순으로 정렬하되 원래 작업 번호도 보관.
    arrivals = sorted((start, duration, i) for i, (start, duration) in enumerate(jobs))
    # len은 작업 수.
    n = len(jobs)
    # 다음 요청 인덱스·현재 시각·반환 시간 합을 언패킹 대입.
    index, time, total = 0, 0, 0
    # 도착해서 대기 중인 작업의 최소 힙.
    heap = []
    # 미도착 작업이나 대기 작업이 남은 동안 실행.
    while index < n or heap:
        # 대기 작업이 없으면 다음 요청까지 시간 이동 가능.
        if not heap and index < n:
            # 비어 있는 시간만 건너뛰고 시각이 뒤로 가지 않게 함.
            time = max(time, arrivals[index][0])
        # 작업 완료 시각과 같은 요청도 포함.
        while index < n and arrivals[index][0] <= time:
            # []로 다음 요청 조회 후 언패킹.
            start, duration, number = arrivals[index]
            # 소요 시간→요청 시각→작업 번호 순 우선순위.
            heappush(heap, (duration, start, number))
            # 다음 요청을 가리킴.
            index += 1
        # 현재 대기 중 가장 우선순위가 높은 작업을 꺼냄.
        duration, start, number = heappop(heap)
        # 중간에 멈추지 않고 완료까지 처리.
        time += duration
        # 대기 시간도 포함.
        total += time - start
    # 모든 작업 반환 시간의 평균에서 소수 부분을 버림.
    return total // n
