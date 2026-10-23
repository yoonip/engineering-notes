def solution(n):
    modulus = 1000000007
    dp = [1, 1, 3, 10] + [0] * max(0, n - 3)
    for width in range(4, n + 1):
        subtract = dp[width - 6] if width >= 6 else 0
        dp[width] = (dp[width - 1] + 2 * dp[width - 2] + 6 * dp[width - 3] + dp[width - 4] - subtract) % modulus
    return dp[n]

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. n은 높이 3인 판의 가로 길이.
#     modulus = 1000000007  # =는 대입. 문제에서 요구한 나머지 기준 저장.
#     dp = [1, 1, 3, 10] + [0] * max(0, n - 3)  # []는 리스트, +는 이어 붙이기, *는 반복. 폭 0·1·2·3의 경우의 수로 초기화하고 필요한 공간 추가.
#     for width in range(4, n + 1):  # for와 range로 폭 4부터 n까지 순회. range의 끝은 제외.
#         subtract = dp[width - 6] if width >= 6 else 0  # a if 조건 else b는 조건식. 폭 6 이상일 때만 여섯 칸 전 항을 사용.
#         dp[width] = (dp[width - 1] + 2 * dp[width - 2] + 6 * dp[width - 3] + dp[width - 4] - subtract) % modulus  # [인덱스]는 이전 상태 조회. 특수 끝 모양의 3칸 주기 누적을 정리한 점화식. %는 나머지이며 음수도 올바른 나머지로 바꿈.
#     return dp[n]  # return으로 폭 n의 전체 배치 수 반환.

# 풀이 요약
# 높이 3의 I·L 트리오미노 타일링을 폭별 DP로 셉니다. 세로로 더 나눌 수 없는 끝 묶음은 폭 1·2·3에서 1·2·5가지, 이후 2·2·4가 3칸 주기로 반복됩니다.
# 이 주기 누적식에서 3칸 전 식을 빼면 D[w]=D[w-1]+2D[w-2]+6D[w-3]+D[w-4]-D[w-6]으로 정리됩니다. 폭 0·1·2·3은 1·1·3·10으로 따로 시작합니다. 시간·공간 O(N).
# 예: 폭 4는 10+2×3+6×1+1=23. 폭 6부터 여섯 칸 전 항을 빼 중복 누적을 보정합니다.
