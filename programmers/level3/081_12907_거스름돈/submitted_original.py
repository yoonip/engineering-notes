def solution(n, money):
    dp = [0] * (n + 1)
    dp[0] = 1
    for coin in money:
        for amount in range(coin, n + 1):
            dp[amount] = (dp[amount] + dp[amount - coin]) % 1000000007
    return dp[n]

# 전체 코드 줄별 설명
# def solution(n, money):  # def는 함수 정의. 거슬러 줄 금액과 화폐 종류 목록을 받음.
#     dp = [0] * (n + 1)  # []는 리스트, *는 반복. dp[amount]는 현재까지 허용한 화폐로 amount원을 만드는 조합 수인 동적 계획법(DP) 배열.
#     dp[0] = 1  # 0원을 만드는 방법은 아무 화폐도 쓰지 않는 한 가지. 다른 조합의 출발점.
#     for coin in money:  # for로 화폐 종류를 하나씩 추가. 동전 순서가 다른 중복 조합을 세지 않도록 종류가 바깥 반복문.
#         for amount in range(coin, n + 1):  # range는 끝 제외. 작은 금액부터 올라가므로 같은 화폐를 여러 번 사용하는 것도 허용.
#             dp[amount] = (dp[amount] + dp[amount - coin]) % 1000000007  # []로 값 조회. 기존 조합+현재 동전 하나를 붙이는 조합. %는 나머지 연산.
#     return dp[n]  # 목표 금액의 조합 수 반환.

# 풀이 요약
# 화폐 종류별로 금액을 오름차순 갱신한다. dp[x-coin]의 모든 방법에 현재 동전 하나를 추가하면 x원을 만드는 새 방법이 된다.
# 예: 5원을 [1,2,5]로 만들면 1×5, 1×3+2, 1+2×2, 5의 네 조합. [1,2]와 [2,1]은 같은 방법이라 종류를 바깥에서 반복한다.
# 화폐 C종류일 때 시간 O(NC), 공간 O(N). 금액 반복을 내림차순으로 바꾸면 동전당 한 번만 사용하는 다른 문제가 된다.
# 