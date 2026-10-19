def solution(alp, cop, problems):
    goal_alp = max(problem[0] for problem in problems)
    goal_cop = max(problem[1] for problem in problems)
    alp, cop = min(alp, goal_alp), min(cop, goal_cop)
    actions = problems + [[0, 0, 1, 0, 1], [0, 0, 0, 1, 1]]
    infinity = 10 ** 9
    dp = [[infinity] * (goal_cop + 1) for _ in range(goal_alp + 1)]
    dp[alp][cop] = 0
    for current_alp in range(alp, goal_alp + 1):
        for current_cop in range(cop, goal_cop + 1):
            for need_alp, need_cop, gain_alp, gain_cop, cost in actions:
                if current_alp >= need_alp and current_cop >= need_cop:
                    next_alp = min(goal_alp, current_alp + gain_alp)
                    next_cop = min(goal_cop, current_cop + gain_cop)
                    dp[next_alp][next_cop] = min(dp[next_alp][next_cop], dp[current_alp][current_cop] + cost)
    return dp[goal_alp][goal_cop]

# 전체 코드 줄별 설명
# def solution(alp, cop, problems):  # def는 함수 정의. alp·cop는 초기 알고력·코딩력, problems는 요구치·보상·시간 목록.
#     goal_alp = max(problem[0] for problem in problems)  # max는 최댓값. 모든 문제를 풀 수 있는 데 필요한 최대 알고력.
#     goal_cop = max(problem[1] for problem in problems)  # [1]은 코딩력 요구치. 목표는 모든 요구치의 최댓값.
#     alp, cop = min(alp, goal_alp), min(cop, goal_cop)  # min은 작은 값. 이미 목표를 넘은 초기 능력은 목표로 묶어 상태 수를 줄임.
#     actions = problems + [[0, 0, 1, 0, 1], [0, 0, 0, 1, 1]]  # +는 리스트 결합. 일반 공부도 요구치 0·시간 1·능력 +1인 행동으로 추가.
#     infinity = 10 ** 9  # **는 거듭제곱. 아직 도달하지 못한 상태의 큰 시간.
#     dp = [[infinity] * (goal_cop + 1) for _ in range(goal_alp + 1)]  # 중첩 리스트 내포로 dp[알고력][코딩력]의 최소 시간을 저장할 독립 행 생성.
#     dp[alp][cop] = 0  # 초기 능력 상태까지 필요한 추가 시간은 0.
#     for current_alp in range(alp, goal_alp + 1):  # range는 끝 제외. 능력이 줄지 않으므로 작은 알고력부터 처리.
#         for current_cop in range(cop, goal_cop + 1):  # 같은 알고력에서는 작은 코딩력부터 처리.
#             for need_alp, need_cop, gain_alp, gain_cop, cost in actions:  # for로 각 행동의 다섯 값을 언패킹.
#                 if current_alp >= need_alp and current_cop >= need_cop:  # if는 조건문, >=는 이상, and는 모두 참. 현재 풀 수 있는 행동만 허용.
#                     next_alp = min(goal_alp, current_alp + gain_alp)  # 목표를 넘는 보상은 목표 상태로 합침.
#                     next_cop = min(goal_cop, current_cop + gain_cop)  # 다음 코딩력도 목표 이하로 제한.
#                     dp[next_alp][next_cop] = min(dp[next_alp][next_cop], dp[current_alp][current_cop] + cost)  # 현재 최소 시간+행동 시간을 더해 같은 다음 능력 상태의 최솟값 갱신.
#     return dp[goal_alp][goal_cop]  # return으로 모든 문제를 풀 수 있는 능력에 도달하는 최소 시간 반환.

# 풀이 요약
# 모든 문제를 실제로 풀 필요는 없고, 알고력·코딩력이 각각 최대 요구치 이상이면 끝입니다. 공부와 문제 풀이를 같은 종류의 행동으로 처리합니다.
# 능력은 감소하지 않으므로 작은 능력 상태부터 DP를 갱신합니다. 목표 이상의 능력은 하나로 묶습니다. 목표 능력 A·C와 문제 수 P에 대해 시간 O(AC(P+2)), 공간 O(AC).
# 예: 이미 모든 요구치 이상이면 초기 상태가 목표이므로 추가 시간 0입니다. 같은 문제를 반복해 능력을 올리는 선택도 DP에 자연스럽게 포함됩니다.
# 