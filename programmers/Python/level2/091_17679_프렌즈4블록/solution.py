def solution(m, n, board):
    # 리스트 내포와 list로 문자열 행을 수정 가능한 문자 목록으로 변환.
    board = [list(row) for row in board]
    answer = 0
    while True:
        removed = set()
        # 2×2의 왼쪽 위 행 순회.
        for r in range(m - 1):
            for c in range(n - 1):
                # 빈칸은 거짓이라 제외.
                if board[r][c] and board[r][c] == board[r + 1][c] == board[r][c + 1] == board[r + 1][c + 1]:
                    removed.update(((r, c), (r + 1, c), (r, c + 1), (r + 1, c + 1)))
        # 제거할 좌표 집합이 비면 종료.
        if not removed:
            return answer
        answer += len(removed)
        # 좌표 튜플을 언패킹하며 순회.
        for r, c in removed:
            board[r][c] = ''
        # 중력 처리를 위해 열별 순회.
        for c in range(n):
            remaining = [board[r][c] for r in range(m) if board[r][c]]
            # 위는 빈칸, 아래는 남은 블록으로 구성.
            column = [''] * (m - len(remaining)) + remaining
            for r, value in enumerate(column):
                # 다시 2×2 검색으로 돌아감.
                board[r][c] = value
