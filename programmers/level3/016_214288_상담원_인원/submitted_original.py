from heapq import heapreplace

def solution(k, n, reqs):
    groups = [[] for _ in range(k)]
    for start, duration, kind in reqs:
        groups[kind - 1].append((start, duration))
    limit = n - k + 1
    infinity = 10 ** 9
    dp = [infinity] * (n + 1)
    dp[0] = 0
    for requests in groups:
        waiting = [0] * (limit + 1)
        for staff in range(1, limit + 1):
            heap = [0] * staff
            for start, duration in requests:
                begin = max(start, heap[0])
                waiting[staff] += begin - start
                heapreplace(heap, begin + duration)
        next_dp = [infinity] * (n + 1)
        for used, cost in enumerate(dp):
            if cost == infinity:
                continue
            for staff in range(1, min(limit, n - used) + 1):
                total = used + staff
                next_dp[total] = min(next_dp[total], cost + waiting[staff])
        dp = next_dp
    return dp[n]

# 전체 코드 줄별 설명
# from heapq import heapreplace  # heapq의 heapreplace를 import. 최소 힙의 맨 작은 값을 새 값으로 교체하고 힙 순서를 유지.
# 
# def solution(k, n, reqs):  # def는 함수 정의. k는 상담 유형 수, n은 멘토 수, reqs는 요청 목록.
#     groups = [[] for _ in range(k)]  # [] 리스트 내포로 유형별 요청을 담을 서로 독립인 목록 생성.
#     for start, duration, kind in reqs:  # for~in으로 요청의 시작 시각·소요 시간·유형을 언패킹.
#         groups[kind - 1].append((start, duration))  # 1 기반 유형을 0 기반으로 변환. append로 요청 튜플 추가. 원래 시각순 정렬이 유지됨.
#     limit = n - k + 1  # 다른 유형에 최소 한 명씩 남겼을 때 한 유형에 줄 수 있는 최대 멘토 수.
#     infinity = 10 ** 9  # **는 거듭제곱. 아직 불가능한 배치 비용을 표현할 큰 값.
#     dp = [infinity] * (n + 1)  # dp[used]는 지금까지 처리한 유형에 used명을 배치한 최소 대기 합.
#     dp[0] = 0  # 아직 유형을 처리하지 않았으므로 0명·대기 0으로 시작.
#     for requests in groups:  # 유형을 하나씩 추가하며 인원 배치 DP를 갱신.
#         waiting = [0] * (limit + 1)  # waiting[staff]는 현재 유형에 staff명을 뒀을 때 총 대기 시간.
#         for staff in range(1, limit + 1):  # range는 끝 제외. 가능한 멘토 수를 하나씩 시험.
#             heap = [0] * staff  # 모두 0인 리스트는 이미 최소 힙. 각 멘토의 다음 상담 가능 시각을 저장.
#             for start, duration in requests:  # 먼저 요청한 순서대로 상담 배정.
#                 begin = max(start, heap[0])  # max는 큰 값. 요청 시각과 가장 빨리 비는 멘토 시각 중 늦은 쪽에 시작.
#                 waiting[staff] += begin - start  # +=는 더해 저장. 이 참가자의 실제 대기 시간 누적.
#                 heapreplace(heap, begin + duration)  # 가장 빨리 비는 멘토의 다음 가능 시각을 상담 종료 시각으로 교체.
#         next_dp = [infinity] * (n + 1)  # 현재 유형을 추가한 뒤의 인원별 최소 대기 표.
#         for used, cost in enumerate(dp):  # enumerate는 (인덱스,값). 이전에 쓴 인원과 최소 비용 순회.
#             if cost == infinity:  # if는 조건문, ==는 같음. 불가능한 이전 배치 제외.
#                 continue  # continue는 다음 이전 상태로 이동.
#             for staff in range(1, min(limit, n - used) + 1):  # min은 작은 값. 남은 인원을 넘지 않는 양수 배치만 검사.
#                 total = used + staff  # 이번 유형까지 배정한 총 인원.
#                 next_dp[total] = min(next_dp[total], cost + waiting[staff])  # 이전 유형의 대기 합과 현재 유형의 대기 합을 더해 최소화.
#         dp = next_dp  # 다음 유형을 처리할 표로 교체.
#     return dp[n]  # return으로 정확히 n명을 모든 유형에 양수로 배치한 최소 대기 합 반환.

# 풀이 요약
# 유형별로 멘토 수를 1명부터 늘려가며 대기 시간을 최소 힙으로 시뮬레이션합니다. 가장 빨리 비는 멘토에게 다음 요청을 배정합니다.
# 이후 유형을 하나씩 추가하는 DP로 총 n명을 나눠 배정합니다. 각 유형에 최소 한 명을 배치합니다. 요청 수 R일 때 시간 O(R(n-k+1) log n+kn²), 공간 O(R+kn).
# 예: 첫 예제는 유형별 2·1·2명으로 배치하면 대기 합이 5+20+0=25로 최소입니다.
