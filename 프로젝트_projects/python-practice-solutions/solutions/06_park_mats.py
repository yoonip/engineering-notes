# 공원 / 돗자리
# 분류: 최대 정사각형 DP
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/340198
# 선택 이유: 각 칸을 오른쪽 아래로 하는 최대 빈 정사각형을 DP로 구하면 같은 영역을 반복 검사하지 않는다.
# 비용: H×W 격자, 돗자리 M개: 시간 O(HW+M), 추가 공간 O(W).

def solution(mats, park):
    rows = len(park)
    cols = len(park[0])
    dp = [0] * (cols + 1)
    largest = 0

    for row in range(rows):
        diagonal = 0
        for col in range(1, cols + 1):
            above = dp[col]
            if park[row][col - 1] == "-1":
                # 위·왼쪽·왼쪽 위가 모두 받쳐 주는 크기까지만 정사각형을 넓힌다.
                dp[col] = min(above, dp[col - 1], diagonal) + 1
                largest = max(largest, dp[col])
            else:
                dp[col] = 0
            diagonal = above

    return max((size for size in mats if size <= largest), default=-1)
