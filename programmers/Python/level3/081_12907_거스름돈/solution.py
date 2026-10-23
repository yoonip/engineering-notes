# 거슬러 줄 금액과 화폐 종류 목록을 받음.
def solution(n, money):
    # dp[amount]는 현재까지 허용한 화폐로 amount원을 만드는 조합 수인 동적 계획법(DP) 배열.
    dp = [0] * (n + 1)
    # 다른 조합의 출발점.
    dp[0] = 1
    # 동전 순서가 다른 중복 조합을 세지 않도록 종류가 바깥 반복문.
    for coin in money:
        # 작은 금액부터 올라가므로 같은 화폐를 여러 번 사용하는 것도 허용.
        for amount in range(coin, n + 1):
            # %는 나머지 연산.
            dp[amount] = (dp[amount] + dp[amount - coin]) % 1000000007
    # 목표 금액의 조합 수 반환.
    return dp[n]
