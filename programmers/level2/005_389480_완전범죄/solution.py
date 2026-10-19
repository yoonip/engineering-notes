# 문제: 완전범죄
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/389480
# 풀이: B의 흔적 합마다 가능한 최소 A 흔적만 DP 배열에 남긴다. 같은 B 합에서 A 흔적이 더 큰 상태는 버려도 된다.
# 복잡도: 물건 N개·B 흔적 한도 M: 시간 O(NM), 추가 공간 O(M).

def solution(info, n, m):
    dp = [n] * m
    dp[0] = 0
    for a_trace, b_trace in info:
        next_dp = [n] * m
        for b_used, a_used in enumerate(dp):
            if a_used == n:
                continue
            if a_used + a_trace < n:
                next_dp[b_used] = min(next_dp[b_used], a_used + a_trace)
            if b_used + b_trace < m:
                next_dp[b_used + b_trace] = min(next_dp[b_used + b_trace], a_used)
        dp = next_dp
    answer = min(dp)
    return answer if answer < n else -1
