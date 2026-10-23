from heapq import heapify, heappop, heappush

def solution(n, paths, gates, summits):
    graph = [[] for _ in range(n + 1)]
    for a, b, time in paths:
        graph[a].append((b, time))
        graph[b].append((a, time))
    is_summit = [False] * (n + 1)
    for summit in summits:
        is_summit[summit] = True
    intensity = [10 ** 9] * (n + 1)
    heap = [(0, gate) for gate in gates]
    heapify(heap)
    for gate in gates:
        intensity[gate] = 0
    while heap:
        current, node = heappop(heap)
        if current != intensity[node] or is_summit[node]:
            continue
        for neighbor, time in graph[node]:
            candidate = max(current, time)
            if candidate < intensity[neighbor]:
                intensity[neighbor] = candidate
                heappush(heap, (candidate, neighbor))
    summit = min(summits, key=lambda node: (intensity[node], node))
    return [summit, intensity[summit]]

# 전체 코드 줄별 설명
# from heapq import heapify, heappop, heappush  # heapq의 최소 힙 도구 import. heapify는 힙 구성, heappop은 최소 항목 제거·반환, heappush는 삽입.
# 
# def solution(n, paths, gates, summits):  # def는 함수 정의. 지점 수·등산로·출입구·산봉우리 목록 입력.
#     graph = [[] for _ in range(n + 1)]  # [] 리스트 내포로 지점별 이웃·시간 목록 생성.
#     for a, b, time in paths:  # for~in으로 등산로의 양 끝과 소요 시간을 언패킹.
#         graph[a].append((b, time))  # append는 이웃 번호·시간 튜플 하나 추가.
#         graph[b].append((a, time))  # 양방향 등산로이므로 반대 연결도 추가.
#     is_summit = [False] * (n + 1)  # False는 거짓, *는 반복. 산봉우리 여부를 빠르게 조회할 리스트.
#     for summit in summits:  # 산봉우리 번호 순회.
#         is_summit[summit] = True  # True는 참. 산봉우리 표시.
#     intensity = [10 ** 9] * (n + 1)  # **는 거듭제곱. intensity[v]는 어느 출입구에서 v까지 가능한 최소 경로 최대 간선값.
#     heap = [(0, gate) for gate in gates]  # 리스트 내포로 모든 출입구를 비용 0의 시작 상태로 추가.
#     heapify(heap)  # 리스트를 최소 힙으로 바꿈. 튜플은 첫 항목 intensity부터 비교.
#     for gate in gates:  # 출입구들의 거리 초기화.
#         intensity[gate] = 0  # 모든 출입구를 이미 최소값 0으로 두므로 다른 경로가 출입구를 중간 경유하지 않음.
#     while heap:  # while은 힙이 비지 않은 동안 반복.
#         current, node = heappop(heap)  # 가장 낮은 intensity 후보를 먼저 꺼내 언패킹.
#         if current != intensity[node] or is_summit[node]:  # !=는 다름, or는 하나라도 참. 낡은 후보 또는 산봉우리에서 더 이동하는 경로 제외.
#             continue  # continue는 다음 힙 후보로 진행. 산봉우리는 종점으로만 사용.
#         for neighbor, time in graph[node]:  # 이웃 지점과 간선 시간을 순회.
#             candidate = max(current, time)  # max는 큰 값. 이동 시간 합이 아니라 경로에서 가장 긴 한 간선이 intensity.
#             if candidate < intensity[neighbor]:  # if는 조건문, <는 미만. 더 낮은 intensity 경로만 갱신.
#                 intensity[neighbor] = candidate  # 이웃의 최솟값 기록.
#                 heappush(heap, (candidate, neighbor))  # 갱신한 후보를 힙에 삽입.
#     summit = min(summits, key=lambda node: (intensity[node], node))  # min의 key는 비교 기준, lambda는 짧은 함수. intensity 우선, 동률이면 작은 산봉우리 번호.
#     return [summit, intensity[summit]]  # [] 리스트로 산봉우리 번호·최소 intensity를 순서대로 반환.

# 풀이 요약
# 모든 출입구에서 동시에 시작하는 다익스트라 형태의 탐색입니다. 거리 합 대신 경로의 최대 간선값을 최소화합니다.
# 산봉우리에서는 더 확장하지 않으며 출입구는 이미 0이라 중간에 다시 들어가지 않습니다. 간 길을 그대로 돌아오면 왕복 intensity가 같으므로 올라가는 최적 경로만 찾으면 됩니다. 시간 O((N+E) log N), 공간 O(N+E).
# 예: 간선이 3·2·3인 코스는 합 8이 아니라 intensity 3입니다. 같은 intensity라면 산봉우리 번호가 작은 코스를 고릅니다.
# 