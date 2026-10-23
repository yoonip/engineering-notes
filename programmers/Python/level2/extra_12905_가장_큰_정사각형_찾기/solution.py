def solution(board):
    # 0번은 경계용.
    dp = [0] * (len(board[0]) + 1)
    best = 0
    for row in board:
        diagonal = 0
        # 경계용 칸 다음부터 계산.
        for col, value in enumerate(row, 1):
            above = dp[col]
            if value:
                # 위·왼쪽·왼쪽 위 세 정사각형 중 가장 작은 변에 현재 칸을 붙임.
                dp[col] = min(above, dp[col - 1], diagonal) + 1
                if dp[col] > best:
                    # 새 최댓값 저장.
                    best = dp[col]
            else:
                dp[col] = 0
            diagonal = above
    return best * best
