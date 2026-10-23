def solution(n):
    board = [[0] * (r + 1) for r in range(n)]
    r, c, value = -1, 0, 1
    directions = ((1, 0), (0, 1), (-1, -1))
    for side in range(n):
        dr, dc = directions[side % 3]
        for _ in range(n - side):
            r += dr
            c += dc
            board[r][c] = value
            value += 1
    return [number for row in board for number in row]

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의, n은 삼각형 높이 입력.
#     board = [[0] * (r + 1) for r in range(n)]  # 리스트 내포로 길이가 1,2,...,n인 행 생성. *는 리스트 반복.
#     r, c, value = -1, 0, 1  # 첫 이동으로 (0,0)에 오도록 행 -1에서 시작. 채울 숫자는 1.
#     directions = ((1, 0), (0, 1), (-1, -1))  # () 튜플에 아래·오른쪽·왼쪽 위 이동량 저장.
#     for side in range(n):  # range(n)은 0~n-1. 채울 변을 순서대로 순회.
#         dr, dc = directions[side % 3]  # %는 나머지, []는 접근. 세 방향을 반복 선택해 언패킹.
#         for _ in range(n - side):  # _는 안 쓰는 변수. 이동 칸 수는 매 변마다 하나씩 감소.
#             r += dr  # +=는 더해 저장. 행 이동.
#             c += dc  # 열 이동.
#             board[r][c] = value  # [][]는 행·열 접근. 현재 칸에 숫자 대입.
#             value += 1  # 다음 칸에 쓸 숫자 증가.
#     return [number for row in board for number in row]  # 중첩 리스트 내포로 각 행을 이어 붙여 return으로 반환.

# 풀이 요약
# 아래→오른쪽→왼쪽 위 순서로 이동하며, 채울 길이를 n,n-1,...,1로 줄입니다. 마지막에 행 순서로 펼칩니다.
# 예: n=4는 [1,2,9,3,10,8,4,5,6,7]. 시간·공간 O(n²).
