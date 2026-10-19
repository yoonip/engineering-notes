def solution(matrix_sizes):
    n = len(matrix_sizes)
    dimensions = [matrix_sizes[0][0]] + [col for row, col in matrix_sizes]
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for start in range(n - length + 1):
            end = start + length - 1
            best = float('inf')
            for middle in range(start, end):
                cost = dp[start][middle] + dp[middle + 1][end] + dimensions[start] * dimensions[middle + 1] * dimensions[end + 1]
                best = min(best, cost)
            dp[start][end] = best
    return dp[0][n - 1]

# 전체 코드 줄별 설명
# def solution(matrix_sizes):  # def는 함수 정의. 곱할 순서대로 주어진 행렬의 [행 수,열 수] 목록을 받음.
#     n = len(matrix_sizes)  # len은 행렬 개수.
#     dimensions = [matrix_sizes[0][0]] + [col for row, col in matrix_sizes]  # []는 리스트. 이어지는 행렬의 공통 차원을 겹치지 않게 기록. i번 행렬은 dimensions[i]×dimensions[i+1].
#     dp = [[0] * n for _ in range(n)]  # 리스트 컴프리헨션. dp[i][j]는 i~j번 행렬의 최소 곱셈 수. 행렬 하나만 있으면 연산 0번.
#     for length in range(2, n + 1):  # range는 끝 제외. 짧은 구간부터 긴 구간으로 계산하는 구간 DP(동적 계획법).
#         for start in range(n - length + 1):  # 현재 길이의 가능한 시작 인덱스 순회.
#             end = start + length - 1  # 구간 마지막 행렬 인덱스.
#             best = float('inf')  # float('inf')는 무한대. 최소 연산 수의 초기값.
#             for middle in range(start, end):  # 마지막 곱셈을 할 때 왼쪽·오른쪽 부분으로 나누는 모든 경계 시도.
#                 cost = dp[start][middle] + dp[middle + 1][end] + dimensions[start] * dimensions[middle + 1] * dimensions[end + 1]  # 왼쪽 부분 비용+오른쪽 부분 비용+두 결과 행렬을 곱하는 행×공통 차원×열 비용.
#                 best = min(best, cost)  # min은 작은 값. 가장 싼 괄호 배치 선택.
#             dp[start][end] = best  # []로 현재 구간의 최적값 저장.
#     return dp[0][n - 1]  # 전체 행렬 구간의 최소 곱셈 연산 수 반환.

# 풀이 요약
# 최종 곱셈은 어떤 경계 k를 기준으로 (i~k 결과)×(k+1~j 결과)로 나뉜다. 두 부분의 최적 비용과 마지막 곱셈 비용을 합쳐 최소를 고른다.
# 예: 5×3,3×10,10×6은 뒤 두 행렬부터 곱하면 3×10×6+5×3×6=270으로, 앞부터 곱한 450보다 작다.
# 구간을 짧은 순서로 계산하면 필요한 두 부분의 값이 이미 있다. 시간 O(N³), 공간 O(N²).
# 