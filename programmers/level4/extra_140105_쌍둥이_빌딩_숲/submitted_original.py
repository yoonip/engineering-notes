def solution(n, count):
    mod = 1_000_000_007
    dp = [0] * (count + 1)
    dp[0] = 1
    for pairs in range(1, n + 1):
        next_dp = [0] * (count + 1)
        for visible in range(1, min(pairs, count) + 1):
            next_dp[visible] = (dp[visible - 1] + 2 * (pairs - 1) * dp[visible]) % mod
        dp = next_dp
    return dp[count]

# 전체 코드 줄별 설명
# def solution(n, count):  # def는 함수 정의. n은 빌딩 쌍의 수, count는 보여야 하는 서로 다른 높이의 수.
#     mod = 1_000_000_007  # 큰 정답을 나눌 수. 숫자 사이 _는 읽기 위한 구분자.
#     dp = [0] * (count + 1)  # []는 리스트, *는 반복. dp[j]는 j종류 높이가 보이는 배치 수.
#     dp[0] = 1  # 빌딩이 없는 상태의 배치는 한 가지이며 보이는 높이는 0가지.
#     for pairs in range(1, n + 1):  # range의 끝은 제외되므로 1부터 n쌍까지 순회.
#         next_dp = [0] * (count + 1)  # 이번 빌딩 쌍 수에 대한 새 DP 리스트 생성.
#         for visible in range(1, min(pairs, count) + 1):  # min은 작은 값 선택. 가능한 보이는 높이 개수만 순회.
#             next_dp[visible] = (dp[visible - 1] + 2 * (pairs - 1) * dp[visible]) % mod  # 맨 앞 삽입은 보이는 수 +1, 나머지 2*(pairs-1)곳 삽입은 그대로. %는 나머지.
#         dp = next_dp  # 이전 단계 리스트를 이번 단계 결과로 교체.
#     return dp[count]  # return은 요구한 개수의 배치 수를 반환하고 함수를 끝냄.

# 풀이 요약
# 기존 빌딩 높이를 1씩 올리고 가장 낮은 빌딩 쌍을 붙여 삽입합니다. 더 높은 빌딩이 사이에 올 수 없어 새 쌍은 반드시 붙어 있습니다.
# 맨 앞 한 곳은 보이는 수가 1 늘고, 나머지 2*(쌍 수-1)곳은 기존 빌딩에 가려 보이는 수가 같습니다. 예: n=3의 결과는 [8,6,1].
# 시간 O(n*count), 공간 O(count).
# 