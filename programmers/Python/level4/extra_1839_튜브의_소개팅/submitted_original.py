def solution(m, n, s, time_map):
    size = m * n
    infinity = s + 1
    current = [infinity] * size
    current[0] = 0
    for steps in range(1, size):
        next_cost = [infinity] * size
        for r in range(m):
            for c in range(n):
                cost = current[r * n + c]
                if cost > s:
                    continue
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and time_map[nr][nc] != -1:
                        candidate = cost + time_map[nr][nc]
                        index = nr * n + nc
                        if candidate <= s and candidate < next_cost[index]:
                            next_cost[index] = candidate
        current = next_cost
        if current[-1] <= s:
            return [steps, current[-1]]
    return [-1, -1]

# 전체 코드 줄별 설명
# def solution(m, n, s, time_map):  # def는 함수 정의. 격자 행·열 수, 대화 제한 시간, 칸별 대화 시간을 입력받음.
#     size = m * n  # *는 곱셈. 전체 칸 수를 구함.
#     infinity = s + 1  # 허용 시간을 넘는 값으로 도달 불가능 상태 표시.
#     current = [infinity] * size  # []는 리스트. 현재 이동 횟수로 각 칸에 도착하는 최소 대화 시간 저장.
#     current[0] = 0  # 시작 칸에는 이동 없이 대화 시간 0으로 도착.
#     for steps in range(1, size):  # range는 끝을 제외. 비음수 대화 시간에서 최적 경로는 칸을 반복할 필요가 없어 최대 size-1번 이동.
#         next_cost = [infinity] * size  # 다음 이동 횟수의 최소 대화 시간 리스트 초기화.
#         for r in range(m):  # 현재 칸의 행을 순회.
#             for c in range(n):  # 현재 칸의 열을 순회.
#                 cost = current[r * n + c]  # 2차원 좌표를 1차원 번호로 변환해 현재 최소 시간 조회.
#                 if cost > s:  # if는 조건문. 도달할 수 없거나 제한을 초과한 상태는 사용하지 않음.
#                     continue  # continue는 이번 칸을 건너뜀.
#                 for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):  # ()는 튜플. 상하좌우 네 방향 이동 검사.
#                     nr, nc = r + dr, c + dc  # 이웃 칸 좌표 계산.
#                     if 0 <= nr < m and 0 <= nc < n and time_map[nr][nc] != -1:  # 연속 비교·and로 격자 내부이며 테이블 장애물이 아닌 칸만 선택.
#                         candidate = cost + time_map[nr][nc]  # 이웃 칸에서 필요한 대화 시간을 더함.
#                         index = nr * n + nc  # 이웃의 1차원 칸 번호 계산.
#                         if candidate <= s and candidate < next_cost[index]:  # 제한을 만족하고 같은 이동 횟수의 기존 경로보다 대화 시간이 적으면 갱신.
#                             next_cost[index] = candidate  # 이웃 칸의 최소 대화 시간 저장.
#         current = next_cost  # 한 번 더 이동한 결과로 현재 상태 교체.
#         if current[-1] <= s:  # [-1]은 마지막 칸. 도착 가능한 첫 이동 횟수인지 검사.
#             return [steps, current[-1]]  # return으로 최소 이동 횟수와 그중 최소 대화 시간 반환.
#     return [-1, -1]  # 조건을 만족하는 경로가 없을 때 기본값. 문제에서는 경로 존재 보장.

# 풀이 요약
# 이동 횟수별로 각 칸의 최소 대화 시간을 DP로 계산합니다. 같은 칸·같은 이동 횟수에서는 대화 시간이 적은 경로만 남기면 충분합니다.
# 도착점에 제한 시간 이내로 도달하는 첫 단계가 최단 경로이고 DP 값이 그중 최소 대화 시간입니다. 세 번째 예제의 답은 [12,11].
# V=m*n일 때 시간 O(V^2), 공간 O(V). Python3 미지원 문제의 학습용 코드이며 실제 제출은 같은 알고리즘의 C++입니다.
# 