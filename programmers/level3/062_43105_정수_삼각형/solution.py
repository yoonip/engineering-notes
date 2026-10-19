# 삼각형의 각 행을 담은 중첩 리스트를 받음.
def solution(triangle):
    # dp[i]는 해당 칸에서 바닥까지의 최대 합을 뜻하는 동적 계획법(DP) 배열.
    dp = triangle[-1][:]
    # 바닥 바로 위부터 꼭대기로 이동.
    for row in reversed(triangle[:-1]):
        # 현재 행의 각 칸 순회.
        for i, value in enumerate(row):
            # 바로 아래 두 자식 중 더 큰 경로 합을 현재 값에 더함.
            dp[i] = value + max(dp[i], dp[i + 1])
    # 꼭대기부터 바닥까지 가능한 최대 합 반환.
    return dp[0]
