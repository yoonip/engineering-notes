def solution(n):
    dp = [0] * (n + 1)  # []는 리스트, *는 반복. dp[i]는 i쌍으로 만드는 올바른 괄호 문자열 수.
    dp[0] = 1  # 아무 괄호도 없는 빈 문자열을 만드는 경우는 한 가지.
    for pairs in range(1, n + 1):
        for inside in range(pairs):  # 첫 여는 괄호와 짝인 닫는 괄호 사이에 놓을 괄호 쌍 수를 순회.
            outside = pairs - 1 - inside  # 첫 괄호 한 쌍과 내부를 제외한 뒤쪽의 괄호 쌍 수 계산.
            dp[pairs] += dp[inside] * dp[outside]
    return dp[n]  # return으로 n쌍의 올바른 괄호 문자열 개수 반환.
