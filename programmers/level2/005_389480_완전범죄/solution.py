def solution(info, n, m):
    # B 흔적별 최소 A 흔적을 저장하며 n은 불가능 상태다.
    dp = [n] * m
    dp[0] = 0
    for a_trace, b_trace in info:
        # 물건 하나를 중복 배정하지 않도록 다음 상태를 따로 만든다.
        next_dp = [n] * m
        for b_used, a_used in enumerate(dp):
            if a_used == n:
                continue
            if a_used + a_trace < n:
                next_dp[b_used] = min(next_dp[b_used], a_used + a_trace)
            # B가 맡을 때도 체포 기준 미만이어야 한다.
            if b_used + b_trace < m:
                next_dp[b_used + b_trace] = min(next_dp[b_used + b_trace], a_used)
        dp = next_dp
    answer = min(dp)
    return answer if answer < n else -1
