from heapq import heappush, heappop

def solution(jobs):
    arrivals = sorted((start, duration, i) for i, (start, duration) in enumerate(jobs))
    n = len(jobs)
    index, time, total = 0, 0, 0
    heap = []
    while index < n or heap:
        if not heap and index < n:
            time = max(time, arrivals[index][0])
        while index < n and arrivals[index][0] <= time:
            start, duration, number = arrivals[index]
            heappush(heap, (duration, start, number))
            index += 1
        duration, start, number = heappop(heap)
        time += duration
        total += time - start
    return total // n

# 전체 코드 줄별 설명
# from heapq import heappush, heappop  # import는 도구 가져오기. 최소 힙은 우선순위가 작은 작업부터 꺼내는 자료구조. 두 함수는 삽입·최솟값 추출.
# 
# def solution(jobs):  # def는 함수 정의. 각 작업의 [요청 시각,소요 시간] 목록을 받음.
#     arrivals = sorted((start, duration, i) for i, (start, duration) in enumerate(jobs))  # enumerate는 번호·값 제공. 튜플을 요청 시각 순으로 정렬하되 원래 작업 번호도 보관.
#     n = len(jobs)  # len은 작업 수.
#     index, time, total = 0, 0, 0  # 다음 요청 인덱스·현재 시각·반환 시간 합을 언패킹 대입.
#     heap = []  # []는 리스트. 도착해서 대기 중인 작업의 최소 힙.
#     while index < n or heap:  # while은 조건 반복, or는 하나라도 참. 미도착 작업이나 대기 작업이 남은 동안 실행.
#         if not heap and index < n:  # not은 부정, and는 모두 참. 대기 작업이 없으면 다음 요청까지 시간 이동 가능.
#             time = max(time, arrivals[index][0])  # max는 큰 값. 비어 있는 시간만 건너뛰고 시각이 뒤로 가지 않게 함.
#         while index < n and arrivals[index][0] <= time:  # 현재 시각까지 들어온 모든 요청을 먼저 큐에 넣음. 작업 완료 시각과 같은 요청도 포함.
#             start, duration, number = arrivals[index]  # []로 다음 요청 조회 후 언패킹.
#             heappush(heap, (duration, start, number))  # 튜플은 앞부터 비교. 소요 시간→요청 시각→작업 번호 순 우선순위.
#             index += 1  # +=는 더해 저장. 다음 요청을 가리킴.
#         duration, start, number = heappop(heap)  # 현재 대기 중 가장 우선순위가 높은 작업을 꺼냄.
#         time += duration  # 중간에 멈추지 않고 완료까지 처리.
#         total += time - start  # 반환 시간은 완료 시각-요청 시각. 대기 시간도 포함.
#     return total // n  # //는 정수 나눗셈. 모든 작업 반환 시간의 평균에서 소수 부분을 버림.

# 풀이 요약
# 요청을 시간순으로 읽으며 현재 도착한 작업만 힙에 넣는다. 대기 중 소요 시간이 가장 짧은 작업을 선택하고, 빈 시간에는 다음 요청 시각으로 건너뛴다.
# 예: [0,3],[1,9],[3,5]는 작업 0→2→1 순서로 실행되어 반환 시간이 3·5·16, 평균의 정수 부분은 8이다.
# 현재 지문의 요청 시각·작업 번호 동점 조건까지 튜플에 반영한다. 시간 O(N log N), 공간 O(N).
# 