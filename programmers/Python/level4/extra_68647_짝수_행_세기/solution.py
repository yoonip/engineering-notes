def solution(a):
    mod = 10_000_019  # 문제에서 지정한 나머지 연산 기준 10의 7제곱+19. _는 자릿수 구분자.
    n = len(a)
    choose = [[0] * (n + 1) for _ in range(n + 1)]  # 리스트 내포로 조합 수 표 생성. choose[i][j]는 i개 중 j개를 고르는 경우의 수.
    for total in range(n + 1):  # 0개부터 n개까지의 조합을 계산.
        choose[total][0] = choose[total][total] = 1  # 아무것도 고르지 않거나 전부 고르는 방법은 한 가지.
        for selected in range(1, total):  # 양끝을 제외한 선택 개수를 순회.
            choose[total][selected] = (choose[total - 1][selected - 1] + choose[total - 1][selected]) % mod  # 특정 원소를 고르는 경우와 안 고르는 경우를 더하는 파스칼 점화식. %는 나머지.
    dp = [0] * (n + 1)  # dp[e]는 지금까지 1의 개수가 짝수인 행이 e개인 행렬 수.
    dp[n] = 1  # 아직 열을 채우지 않으면 모든 행의 1 개수가 0이므로 n개 행 모두 짝수.
    for column in zip(*a):  # *a는 행들을 인자로 펼치고 zip은 같은 위치 값을 묶어 열별 순회.
        ones = sum(column)  # sum은 합계. 이번 열에 반드시 배치해야 하는 1의 개수.
        next_dp = [0] * (n + 1)  # 이번 열을 채운 뒤의 DP 결과 초기화.
        for even, ways in enumerate(dp):  # enumerate는 (인덱스, 값) 제공. 짝수 행 개수와 해당 경우의 수 순회.
            if not ways:  # not은 부정. 경우의 수가 0인 상태는 계산 생략.
                continue  # continue는 이번 반복을 건너뜀.
            low = max(0, ones - (n - even))  # max는 큰 값 반환. 홀수 행에 다 놓고 남는 1은 짝수 행에 놓아야 함.
            high = min(even, ones)  # min은 작은 값 반환. 짝수 행에서 고를 수 있는 1의 최대 개수.
            for changed in range(low, high + 1):  # 기존 짝수 행 중 1을 놓아 홀수가 될 행 수를 순회.
                new_even = even + ones - 2 * changed  # 기존 짝수에서 changed개 감소, 기존 홀수에서 ones-changed개 증가.
                next_dp[new_even] += ways * choose[even][changed] * choose[n - even][ones - changed]  # 두 그룹에서 1을 놓을 행을 고르는 조합 수를 곱해 합산.
        dp = [value % mod for value in next_dp]  # 리스트 내포로 각 경우의 수를 나머지로 바꾸어 다음 열에 사용.
    return dp[n]  # 모든 행이 짝수인 상태의 경우의 수 반환.
