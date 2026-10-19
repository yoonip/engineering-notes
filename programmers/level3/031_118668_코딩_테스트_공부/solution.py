# alp·cop는 초기 알고력·코딩력, problems는 요구치·보상·시간 목록.
def solution(alp, cop, problems):
    # 모든 문제를 풀 수 있는 데 필요한 최대 알고력.
    goal_alp = max(problem[0] for problem in problems)
    # 목표는 모든 요구치의 최댓값.
    goal_cop = max(problem[1] for problem in problems)
    # 이미 목표를 넘은 초기 능력은 목표로 묶어 상태 수를 줄임.
    alp, cop = min(alp, goal_alp), min(cop, goal_cop)
    # 일반 공부도 요구치 0·시간 1·능력 +1인 행동으로 추가.
    actions = problems + [[0, 0, 1, 0, 1], [0, 0, 0, 1, 1]]
    # 아직 도달하지 못한 상태의 큰 시간.
    infinity = 10 ** 9
    # 중첩 리스트 내포로 dp[알고력][코딩력]의 최소 시간을 저장할 독립 행 생성.
    dp = [[infinity] * (goal_cop + 1) for _ in range(goal_alp + 1)]
    # 초기 능력 상태까지 필요한 추가 시간은 0.
    dp[alp][cop] = 0
    # 능력이 줄지 않으므로 작은 알고력부터 처리.
    for current_alp in range(alp, goal_alp + 1):
        # 같은 알고력에서는 작은 코딩력부터 처리.
        for current_cop in range(cop, goal_cop + 1):
            # for로 각 행동의 다섯 값을 언패킹.
            for need_alp, need_cop, gain_alp, gain_cop, cost in actions:
                # 현재 풀 수 있는 행동만 허용.
                if current_alp >= need_alp and current_cop >= need_cop:
                    # 목표를 넘는 보상은 목표 상태로 합침.
                    next_alp = min(goal_alp, current_alp + gain_alp)
                    # 다음 코딩력도 목표 이하로 제한.
                    next_cop = min(goal_cop, current_cop + gain_cop)
                    # 현재 최소 시간+행동 시간을 더해 같은 다음 능력 상태의 최솟값 갱신.
                    dp[next_alp][next_cop] = min(dp[next_alp][next_cop], dp[current_alp][current_cop] + cost)
    # return으로 모든 문제를 풀 수 있는 능력에 도달하는 최소 시간 반환.
    return dp[goal_alp][goal_cop]
