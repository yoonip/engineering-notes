# n은 높이 3인 판의 가로 길이.
def solution(n):
    # 문제에서 요구한 나머지 기준 저장.
    modulus = 1000000007
    # 폭 0·1·2·3의 경우의 수로 초기화하고 필요한 공간 추가.
    dp = [1, 1, 3, 10] + [0] * max(0, n - 3)
    # range의 끝은 제외.
    for width in range(4, n + 1):
        # 폭 6 이상일 때만 여섯 칸 전 항을 사용.
        subtract = dp[width - 6] if width >= 6 else 0
        # %는 나머지이며 음수도 올바른 나머지로 바꿈.
        dp[width] = (dp[width - 1] + 2 * dp[width - 2] + 6 * dp[width - 3] + dp[width - 4] - subtract) % modulus
    # return으로 폭 n의 전체 배치 수 반환.
    return dp[n]
