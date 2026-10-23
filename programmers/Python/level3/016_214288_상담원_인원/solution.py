# 최소 힙의 맨 작은 값을 새 값으로 교체하고 힙 순서를 유지.
from heapq import heapreplace

# k는 상담 유형 수, n은 멘토 수, reqs는 요청 목록.
def solution(k, n, reqs):
    # [] 리스트 내포로 유형별 요청을 담을 서로 독립인 목록 생성.
    groups = [[] for _ in range(k)]
    # for~in으로 요청의 시작 시각·소요 시간·유형을 언패킹.
    for start, duration, kind in reqs:
        # 원래 시각순 정렬이 유지됨.
        groups[kind - 1].append((start, duration))
    # 다른 유형에 최소 한 명씩 남겼을 때 한 유형에 줄 수 있는 최대 멘토 수.
    limit = n - k + 1
    # 아직 불가능한 배치 비용을 표현할 큰 값.
    infinity = 10 ** 9
    # dp[used]는 지금까지 처리한 유형에 used명을 배치한 최소 대기 합.
    dp = [infinity] * (n + 1)
    # 아직 유형을 처리하지 않았으므로 0명·대기 0으로 시작.
    dp[0] = 0
    # 유형을 하나씩 추가하며 인원 배치 DP를 갱신.
    for requests in groups:
        # waiting[staff]는 현재 유형에 staff명을 뒀을 때 총 대기 시간.
        waiting = [0] * (limit + 1)
        # 가능한 멘토 수를 하나씩 시험.
        for staff in range(1, limit + 1):
            # 각 멘토의 다음 상담 가능 시각을 저장.
            heap = [0] * staff
            # 먼저 요청한 순서대로 상담 배정.
            for start, duration in requests:
                # 요청 시각과 가장 빨리 비는 멘토 시각 중 늦은 쪽에 시작.
                begin = max(start, heap[0])
                # 이 참가자의 실제 대기 시간 누적.
                waiting[staff] += begin - start
                # 가장 빨리 비는 멘토의 다음 가능 시각을 상담 종료 시각으로 교체.
                heapreplace(heap, begin + duration)
        # 현재 유형을 추가한 뒤의 인원별 최소 대기 표.
        next_dp = [infinity] * (n + 1)
        # 이전에 쓴 인원과 최소 비용 순회.
        for used, cost in enumerate(dp):
            # 불가능한 이전 배치 제외.
            if cost == infinity:
                # continue는 다음 이전 상태로 이동.
                continue
            # 남은 인원을 넘지 않는 양수 배치만 검사.
            for staff in range(1, min(limit, n - used) + 1):
                # 이번 유형까지 배정한 총 인원.
                total = used + staff
                # 이전 유형의 대기 합과 현재 유형의 대기 합을 더해 최소화.
                next_dp[total] = min(next_dp[total], cost + waiting[staff])
        # 다음 유형을 처리할 표로 교체.
        dp = next_dp
    # return으로 정확히 n명을 모든 유형에 양수로 배치한 최소 대기 합 반환.
    return dp[n]
