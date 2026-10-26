import sys  # 정수 입력 읽기
tokens = iter(map(int, sys.stdin.read().split()))  # 공백 토큰 순회
n, target = next(tokens), next(tokens)  # 동전 종류와 목표
coins = [next(tokens) for _ in range(n)]  # 사용할 양의 동전
dp = [target + 1] * (target + 1)  # 불가능 상태 표시
dp[0] = 0  # 빈 선택의 동전 수
for amount in range(1, target + 1):  # 의존 상태가 먼저 계산되는 순서
    for coin in coins:  # 마지막 동전 후보
        if coin <= amount:  # 음수 금액 제외
            dp[amount] = min(dp[amount], dp[amount - coin] + 1)  # 최선의 전이 선택
print(-1 if dp[target] == target + 1 else dp[target])  # 불가능과 최솟값 구분
