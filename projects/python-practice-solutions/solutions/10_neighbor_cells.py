# 이웃한 칸
# 분류: 격자 탐색
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/250125
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

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


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# # def는 함수를 정의합니다. board, h, w는 입력값을 전달받는 매개변수입니다.
# # 콜론 다음 들여쓴 부분이 함수 몸체입니다. 별도 import는 필요 없습니다.
# def solution(board, h, w):
#     # len(리스트)는 원소 수를 반환합니다. board의 원소는 각 행입니다.
#     # 정사각형이므로 행 수와 열 수가 모두 n입니다.
#     n = len(board)
#     # =는 오른쪽 값을 왼쪽 변수에 대입합니다. 같은 색 이웃 수를 0으로 시작합니다.
#     count = 0
#     # [] 안에 값을 쉼표로 나열하면 리스트가 됩니다.
#     # dh는 행 번호 변화량, dw는 열 번호 변화량을 담은 변수 이름입니다.
#     # 같은 인덱스의 두 값을 짝으로 사용합니다.
#     dh = [0, 1, -1, 0]
#     dw = [1, 0, 0, -1]
#
#     # range(4)는 0,1,2,3을 제공합니다. 네 방향을 한 번씩 검사합니다.
#     for i in range(4):
#         # 리스트[i]는 i번 위치 값을 읽습니다. 인덱스는 0부터입니다.
#         # i=0이면 dh[0]=0, dw[0]=1이므로 오른쪽 칸입니다.
#         h_check = h + dh[i]
#         w_check = w + dw[i]
#
#         # 0 <= h_check < n은 '0 이상이고 n 미만'이라는 연속 비교입니다.
#         # and는 왼쪽 조건과 오른쪽 조건이 모두 참이어야 참입니다.
#         # 행/열 둘 다 범위 안에 있을 때만 안쪽 코드를 실행합니다.
#         if 0 <= h_check < n and 0 <= w_check < n:
#             # board[행][열]은 2차원 리스트에서 해당 칸을 읽습니다.
#             # ==는 두 값이 같은지 비교합니다. 여기서는 색 이름 문자열을 비교합니다.
#             if board[h_check][w_check] == board[h][w]:
#                 # += 1은 count = count + 1과 같습니다.
#                 count += 1
#
#     # return은 결과를 호출한 곳에 전달하고 함수 전체를 종료합니다.
#     # 들여쓰기가 for보다 바깥이므로 네 방향을 모두 확인한 뒤 실행됩니다.
#     return count
