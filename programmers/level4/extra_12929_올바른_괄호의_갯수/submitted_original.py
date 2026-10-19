def solution(n):
    dp = [0] * (n + 1)
    dp[0] = 1
    for pairs in range(1, n + 1):
        for inside in range(pairs):
            outside = pairs - 1 - inside
            dp[pairs] += dp[inside] * dp[outside]
    return dp[n]

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. 사용할 괄호 쌍의 수 n을 입력받음.
#     dp = [0] * (n + 1)  # []는 리스트, *는 반복. dp[i]는 i쌍으로 만드는 올바른 괄호 문자열 수.
#     dp[0] = 1  # 아무 괄호도 없는 빈 문자열을 만드는 경우는 한 가지.
#     for pairs in range(1, n + 1):  # range는 끝을 제외하므로 괄호 1쌍부터 n쌍까지 계산.
#         for inside in range(pairs):  # 첫 여는 괄호와 짝인 닫는 괄호 사이에 놓을 괄호 쌍 수를 순회.
#             outside = pairs - 1 - inside  # 첫 괄호 한 쌍과 내부를 제외한 뒤쪽의 괄호 쌍 수 계산.
#             dp[pairs] += dp[inside] * dp[outside]  # +=는 합산. 내부와 뒤쪽 문자열을 독립적으로 고르므로 경우의 수를 곱함.
#     return dp[n]  # return으로 n쌍의 올바른 괄호 문자열 개수 반환.

# 풀이 요약
# 모든 올바른 괄호 문자열은 유일하게 (내부 문자열)+뒤쪽 문자열로 나뉩니다. 내부·뒤쪽의 가능한 쌍 수별 곱을 모두 더하는 카탈란 수 DP입니다.
# 예: 2쌍은 (())와 ()() 두 가지, 3쌍은 다섯 가지입니다.
# 시간 O(n^2), 공간 O(n). 이 문제는 나머지 연산 없이 실제 개수를 반환합니다.
# 