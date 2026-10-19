# 이웃한 칸
# 분류: 격자 탐색
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/250125
# 선택 이유: 현재 칸의 상하좌우 네 칸만 확인하면 된다.
# 비용: 방향 수가 고정이므로 시간 O(1), 추가 공간 O(1).

def solution(board, h, w):
    n = len(board)
    count = 0
    dh = [0, 1, -1, 0]
    dw = [1, 0, 0, -1]

    for i in range(4):
        h_check = h + dh[i]
        w_check = w + dw[i]

        if 0 <= h_check < n and 0 <= w_check < n:
            if board[h_check][w_check] == board[h][w]:
                count += 1

    return count
