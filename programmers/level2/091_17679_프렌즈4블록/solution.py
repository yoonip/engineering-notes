# 문제: 프렌즈4블록
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/17679
# 풀이: 지울 2×2 좌표를 set에 모아 동시에 제거한다. 열별 남은 블록을 아래로 내린 뒤 더 지울 수 없을 때까지 반복한다.
# 복잡도: 행 M·열 N·제거 라운드 R회: 시간 O(RMN), 추가 공간 O(MN).

def solution(m, n, board):
    board = [list(row) for row in board]
    answer = 0
    while True:
        removed = set()
        for r in range(m - 1):
            for c in range(n - 1):
                if board[r][c] and board[r][c] == board[r + 1][c] == board[r][c + 1] == board[r + 1][c + 1]:
                    removed.update(((r, c), (r + 1, c), (r, c + 1), (r + 1, c + 1)))
        if not removed:
            return answer
        answer += len(removed)
        for r, c in removed:
            board[r][c] = ''
        for c in range(n):
            remaining = [board[r][c] for r in range(m) if board[r][c]]
            column = [''] * (m - len(remaining)) + remaining
            for r, value in enumerate(column):
                board[r][c] = value
