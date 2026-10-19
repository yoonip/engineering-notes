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

# 전체 코드 줄별 설명
# def solution(m, n, board):  # def는 함수 정의. 높이·너비·초기 블록판 입력.
#     board = [list(row) for row in board]  # 리스트 내포와 list로 문자열 행을 수정 가능한 문자 목록으로 변환.
#     answer = 0  # =는 대입. 제거 블록 수 초기화.
#     while True:  # True는 참. 더 지울 블록이 없을 때 반환하며 종료하는 반복.
#         removed = set()  # set은 중복 없는 집합. 이번에 동시에 지울 좌표 저장.
#         for r in range(m - 1):  # range는 끝 미포함. 2×2의 왼쪽 위 행 순회.
#             for c in range(n - 1):  # 2×2의 왼쪽 위 열 순회.
#                 if board[r][c] and board[r][c] == board[r + 1][c] == board[r][c + 1] == board[r + 1][c + 1]:  # and는 모두 참, 연쇄 ==는 네 값 일치. 빈칸은 거짓이라 제외.
#                     removed.update(((r, c), (r + 1, c), (r, c + 1), (r + 1, c + 1)))  # update로 네 좌표 튜플 추가. 겹친 블록도 한 번만 남음.
#         if not removed:  # not은 반전. 제거할 좌표 집합이 비면 종료.
#             return answer  # return으로 누적 제거 수 반환.
#         answer += len(removed)  # len은 원소 수, +=는 더해 저장. 이번 제거 수 누적.
#         for r, c in removed:  # 좌표 튜플을 언패킹하며 순회.
#             board[r][c] = ''  # [][]는 행·열 접근. 빈 문자열로 동시에 제거한 결과 표시.
#         for c in range(n):  # 중력 처리를 위해 열별 순회.
#             remaining = [board[r][c] for r in range(m) if board[r][c]]  # 조건부 리스트 내포로 빈칸을 제외한 블록을 위→아래 순으로 수집.
#             column = [''] * (m - len(remaining)) + remaining  # *는 빈칸 반복, +는 리스트 연결. 위는 빈칸, 아래는 남은 블록으로 구성.
#             for r, value in enumerate(column):  # enumerate는 행 번호·값 제공.
#                 board[r][c] = value  # 갱신한 열을 판에 대입. 다시 2×2 검색으로 돌아감.

# 풀이 요약
# 지울 2×2를 전부 찾은 뒤 좌표 집합으로 한꺼번에 제거합니다. 각 열의 남은 블록을 아래로 모으고 더 지울 것이 없을 때까지 반복합니다.
# 예: 첫 예제는 6개를 지운 뒤 8개를 더 지워 총 14개. 반복 R회일 때 시간 O(Rmn), 공간 O(mn).
