# 곱할 순서대로 주어진 행렬의 [행 수,열 수] 목록을 받음.
def solution(matrix_sizes):
    # len은 행렬 개수.
    n = len(matrix_sizes)
    # i번 행렬은 dimensions[i]×dimensions[i+1].
    dimensions = [matrix_sizes[0][0]] + [col for row, col in matrix_sizes]
    # 행렬 하나만 있으면 연산 0번.
    dp = [[0] * n for _ in range(n)]
    # 짧은 구간부터 긴 구간으로 계산하는 구간 DP(동적 계획법).
    for length in range(2, n + 1):
        # 현재 길이의 가능한 시작 인덱스 순회.
        for start in range(n - length + 1):
            # 구간 마지막 행렬 인덱스.
            end = start + length - 1
            # 최소 연산 수의 초기값.
            best = float('inf')
            # 마지막 곱셈을 할 때 왼쪽·오른쪽 부분으로 나누는 모든 경계 시도.
            for middle in range(start, end):
                # 왼쪽 부분 비용+오른쪽 부분 비용+두 결과 행렬을 곱하는 행×공통 차원×열 비용.
                cost = dp[start][middle] + dp[middle + 1][end] + dimensions[start] * dimensions[middle + 1] * dimensions[end + 1]
                # 가장 싼 괄호 배치 선택.
                best = min(best, cost)
            # []로 현재 구간의 최적값 저장.
            dp[start][end] = best
    # 전체 행렬 구간의 최소 곱셈 연산 수 반환.
    return dp[0][n - 1]
