def solution(n, m, edge_list, k, gps_log):
    graph = [[] for _ in range(n + 1)]
    for u, v in edge_list:
        graph[u].append(v)
        graph[v].append(u)
    infinity = 10 ** 9
    dp = [infinity] * (n + 1)
    dp[gps_log[0]] = 0
    for time in range(1, k):
        next_dp = [infinity] * (n + 1)
        for node in range(1, n + 1):
            best = dp[node]
            for neighbor in graph[node]:
                best = min(best, dp[neighbor])
            next_dp[node] = best + (node != gps_log[time])
        dp = next_dp
    answer = dp[gps_log[-1]]
    return answer if answer < infinity else -1

# 전체 코드 줄별 설명
# def solution(n, m, edge_list, k, gps_log):  # def는 함수 정의. 거점·도로·시간별 GPS 기록 입력.
#     graph = [[] for _ in range(n + 1)]  # []는 리스트. 각 거점의 이웃 목록 생성.
#     for u, v in edge_list:  # 도로 양 끝을 언패킹하며 반복.
#         graph[u].append(v)  # append는 끝에 추가. u에서 v로 이동 가능.
#         graph[v].append(u)  # 양방향 도로이므로 반대쪽도 기록.
#     infinity = 10 ** 9  # **는 거듭제곱. 불가능 상태를 나타낼 충분히 큰 정수.
#     dp = [infinity] * (n + 1)  # dp[v]는 현재 거점 v의 최소 수정 수. *는 반복.
#     dp[gps_log[0]] = 0  # 첫 거점은 수정할 수 없으므로 해당 거점에서만 시작.
#     for time in range(1, k):  # range는 끝 제외. 두 번째 기록부터 차례로 DP 갱신.
#         next_dp = [infinity] * (n + 1)  # 다음 시각의 비용 배열. 이전 시각과 분리해 같은 시각 이동 방지.
#         for node in range(1, n + 1):  # 각 도착 거점 후보 순회.
#             best = dp[node]  # 제자리에 머무는 경우의 직전 비용.
#             for neighbor in graph[node]:  # 이웃에서 한 번 이동해 오는 경우 확인.
#                 best = min(best, dp[neighbor])  # min은 최솟값. 가능한 직전 위치 중 최소 비용 선택.
#             next_dp[node] = best + (node != gps_log[time])  # !=는 다름. 불리언은 정수 계산에서 참 1·거짓 0으로 사용되어 수정 비용 반영.
#         dp = next_dp  # 다음 시각으로 이동.
#     answer = dp[gps_log[-1]]  # [-1]은 마지막 원소. 수정 불가인 원래 도착 거점만 정답으로 사용.
#     return answer if answer < infinity else -1  # 조건부 표현식. 도달 불가면 -1.

# 풀이 요약
# dp[v]는 현재 시각에 v에 있을 때 필요한 최소 GPS 수정 횟수다. 직전 시각에 같은 거점에 머물거나 인접 거점에서 이동한 경우 중 최소를 선택한다.
# 시작 거점만 비용 0으로 초기화하고 마지막에는 원래 도착 거점의 값만 반환해 양 끝을 고정한다. 기록과 현재 거점이 다르면 수정 비용 1을 더한다.
# 예제 [1,2,3,3,6,7]은 네 번째 3을 5로 바꿔 한 번 수정한다. 시간 O(K(N+M)), 공간 O(N+M).
# 