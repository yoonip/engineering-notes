def solution(triangle):
    dp = triangle[-1][:]
    for row in reversed(triangle[:-1]):
        for i, value in enumerate(row):
            dp[i] = value + max(dp[i], dp[i + 1])
    return dp[0]

# 전체 코드 줄별 설명
# def solution(triangle):  # def는 함수 정의. 삼각형의 각 행을 담은 중첩 리스트를 받음.
#     dp = triangle[-1][:]  # [-1]은 마지막 행, [:]는 복사. dp[i]는 해당 칸에서 바닥까지의 최대 합을 뜻하는 동적 계획법(DP) 배열.
#     for row in reversed(triangle[:-1]):  # [:-1]은 마지막 행 제외, reversed는 역순 순회. 바닥 바로 위부터 꼭대기로 이동.
#         for i, value in enumerate(row):  # enumerate는 인덱스·값을 함께 제공. 현재 행의 각 칸 순회.
#             dp[i] = value + max(dp[i], dp[i + 1])  # max는 큰 값. 바로 아래 두 자식 중 더 큰 경로 합을 현재 값에 더함.
#     return dp[0]  # []로 첫 원소 조회. 꼭대기부터 바닥까지 가능한 최대 합 반환.

# 풀이 요약
# 아래 칸에서 바닥까지의 최적값을 알고 있으면 현재 칸은 자기 값+두 자식 최적값 중 큰 값이다. 이를 바닥부터 반복한다.
# 예: 7→3→8→7→5를 고르면 30. 왼쪽부터 갱신할 때 오른쪽 dp[i+1]은 아직 이전 행 값이라 한 배열을 재사용할 수 있다.
# 높이 H일 때 시간 O(H²), 추가 공간 O(H). 입력 삼각형은 수정하지 않는다.
# 