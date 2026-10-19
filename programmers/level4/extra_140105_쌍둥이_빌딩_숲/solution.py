def solution(n, count):
    mod = 1_000_000_007  # 큰 정답을 나눌 수. 숫자 사이 _는 읽기 위한 구분자.
    dp = [0] * (count + 1)  # []는 리스트, *는 반복. dp[j]는 j종류 높이가 보이는 배치 수.
    dp[0] = 1  # 빌딩이 없는 상태의 배치는 한 가지이며 보이는 높이는 0가지.
    for pairs in range(1, n + 1):  # range의 끝은 제외되므로 1부터 n쌍까지 순회.
        next_dp = [0] * (count + 1)  # 이번 빌딩 쌍 수에 대한 새 DP 리스트 생성.
        for visible in range(1, min(pairs, count) + 1):  # min은 작은 값 선택. 가능한 보이는 높이 개수만 순회.
            next_dp[visible] = (dp[visible - 1] + 2 * (pairs - 1) * dp[visible]) % mod  # 맨 앞 삽입은 보이는 수 +1, 나머지 2*(pairs-1)곳 삽입은 그대로. %는 나머지.
        dp = next_dp  # 이전 단계 리스트를 이번 단계 결과로 교체.
    return dp[count]
