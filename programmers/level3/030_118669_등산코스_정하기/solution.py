# heapify는 힙 구성, heappop은 최소 항목 제거·반환, heappush는 삽입.
from heapq import heapify, heappop, heappush

# 지점 수·등산로·출입구·산봉우리 목록 입력.
def solution(n, paths, gates, summits):
    # [] 리스트 내포로 지점별 이웃·시간 목록 생성.
    graph = [[] for _ in range(n + 1)]
    # for~in으로 등산로의 양 끝과 소요 시간을 언패킹.
    for a, b, time in paths:
        # append는 이웃 번호·시간 튜플 하나 추가.
        graph[a].append((b, time))
        # 양방향 등산로이므로 반대 연결도 추가.
        graph[b].append((a, time))
    # 산봉우리 여부를 빠르게 조회할 리스트.
    is_summit = [False] * (n + 1)
    # 산봉우리 번호 순회.
    for summit in summits:
        is_summit[summit] = True
    # intensity[v]는 어느 출입구에서 v까지 가능한 최소 경로 최대 간선값.
    intensity = [10 ** 9] * (n + 1)
    # 리스트 내포로 모든 출입구를 비용 0의 시작 상태로 추가.
    heap = [(0, gate) for gate in gates]
    # 튜플은 첫 항목 intensity부터 비교.
    heapify(heap)
    # 출입구들의 거리 초기화.
    for gate in gates:
        # 모든 출입구를 이미 최소값 0으로 두므로 다른 경로가 출입구를 중간 경유하지 않음.
        intensity[gate] = 0
    # while은 힙이 비지 않은 동안 반복.
    while heap:
        # 가장 낮은 intensity 후보를 먼저 꺼내 언패킹.
        current, node = heappop(heap)
        # 낡은 후보 또는 산봉우리에서 더 이동하는 경로 제외.
        if current != intensity[node] or is_summit[node]:
            # 산봉우리는 종점으로만 사용.
            continue
        # 이웃 지점과 간선 시간을 순회.
        for neighbor, time in graph[node]:
            # 이동 시간 합이 아니라 경로에서 가장 긴 한 간선이 intensity.
            candidate = max(current, time)
            # 더 낮은 intensity 경로만 갱신.
            if candidate < intensity[neighbor]:
                # 이웃의 최솟값 기록.
                intensity[neighbor] = candidate
                # 갱신한 후보를 힙에 삽입.
                heappush(heap, (candidate, neighbor))
    # intensity 우선, 동률이면 작은 산봉우리 번호.
    summit = min(summits, key=lambda node: (intensity[node], node))
    # [] 리스트로 산봉우리 번호·최소 intensity를 순서대로 반환.
    return [summit, intensity[summit]]
