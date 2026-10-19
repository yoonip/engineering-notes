def solution(board):
    text = ''.join(board)
    o, x = text.count('O'), text.count('X')
    if o not in (x, x + 1):
        return 0
    lines = list(board)
    for c in range(3):
        lines.append(''.join(board[r][c] for r in range(3)))
    lines.append(''.join(board[i][i] for i in range(3)))
    lines.append(''.join(board[i][2 - i] for i in range(3)))
    o_win, x_win = 'OOO' in lines, 'XXX' in lines
    if o_win and x_win:
        return 0
    if o_win and o != x + 1:
        return 0
    if x_win and o != x:
        return 0
    return 1

# 전체 코드 줄별 설명
# def solution(board):  # def는 함수 정의. board는 세 행의 문자열 리스트.
#     text = ''.join(board)  # ''는 빈 문자열, join은 문자열들을 연결. 아홉 칸을 한 문자열로 만듦.
#     o, x = text.count('O'), text.count('X')  # count는 해당 문자 개수. 두 결과를 쉼표로 각각 대입.
#     if o not in (x, x + 1):  # not in은 묶음에 없음. () 튜플의 두 합법적인 O 개수인지 검사.
#         return 0  # 차례가 맞지 않으므로 0 반환.
#     lines = list(board)  # list로 행 문자열 목록 복사. 승리 검사할 줄 저장.
#     for c in range(3):  # range(3)은 0,1,2. 열 번호 순회.
#         lines.append(''.join(board[r][c] for r in range(3)))  # []는 원소 접근. 각 열을 생성식으로 연결해 append로 추가.
#     lines.append(''.join(board[i][i] for i in range(3)))  # 왼쪽 위부터 오른쪽 아래 대각선 추가.
#     lines.append(''.join(board[i][2 - i] for i in range(3)))  # 오른쪽 위부터 왼쪽 아래 대각선 추가.
#     o_win, x_win = 'OOO' in lines, 'XXX' in lines  # in은 포함 여부. 각 표시의 승리 여부를 참·거짓으로 저장.
#     if o_win and x_win:  # and는 둘 다 참. 두 사람이 동시에 이긴 경우는 불가능.
#         return 0  # 불가능한 판을 0으로 반환.
#     if o_win and o != x + 1:  # !=는 다름. O가 이겼으면 O가 한 번 더 놓았어야 함.
#         return 0  # 승리 뒤 추가 진행한 경우 제외.
#     if x_win and o != x:  # X가 이겼으면 두 표시의 개수가 같아야 함.
#         return 0  # X 승리 뒤 O가 더 둔 경우 제외.
#     return 1  # 개수와 승리 조건을 모두 만족하면 합법적인 상태.

# 풀이 요약
# O·X 개수로 차례를 검사하고, 승자가 있으면 그 승자의 마지막 차례에서 끝났는지 검사합니다.
# 예: OOO와 XXX가 함께 있으면 0, 빈 판은 1. 판이 항상 3×3이므로 시간·공간 O(1).
