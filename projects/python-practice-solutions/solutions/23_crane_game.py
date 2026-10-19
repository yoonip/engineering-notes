# 크레인 인형뽑기 게임
# 분류: 스택 / 시뮬레이션
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/64061
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

def solution(board, moves):
    n = len(board)
    board = [row[:] for row in board]
    basket = []
    answer = 0

    for move in moves:
        col = move - 1

        for row in range(n):
            if board[row][col] == 0:
                continue

            doll = board[row][col]
            board[row][col] = 0

            if basket and basket[-1] == doll:
                basket.pop()
                answer += 2
            else:
                basket.append(doll)

            break

    return answer


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# def solution(board, moves):  # def로 함수를 정의합니다. 인형 배치와 크레인 이동 리스트를 매개변수로 받습니다.
#     n = len(board)  # len()은 원소 수입니다. board의 원소는 행이므로 n은 행 수입니다.
#     board = [row[:] for row in board]  # 리스트 컴프리헨션으로 각 행을 복사합니다. [:]는 전체 슬라이싱이며 원본 입력을 보존합니다.
#     basket = []  # []는 빈 리스트입니다. 끝에 넣고 빼는 스택으로 사용합니다.
#     answer = 0  # 사라진 인형 수를 0으로 시작합니다.
#
#     for move in moves:  # 명령을 순서대로 하나씩 꺼냅니다.
#         col = move - 1  # 명령은 1번 열부터지만 리스트 인덱스는 0부터이므로 1을 뺍니다.
#
#         for row in range(n):  # range(n)은 0부터 n-1까지입니다. 위쪽 행부터 아래로 내려갑니다.
#             if board[row][col] == 0:  # board[행][열]로 값을 읽습니다. ==는 같은지 비교하며 0은 빈칸입니다.
#                 continue  # 가장 가까운 반복문의 다음 반복으로 갑니다. 여기서는 다음 행을 검사합니다.
#
#             doll = board[row][col]  # 발견한 인형의 숫자를 변수에 저장합니다.
#             board[row][col] = 0  # =는 대입입니다. 뽑은 자리를 빈칸으로 바꿉니다.
#
#             if basket and basket[-1] == doll:  # 빈 리스트는 거짓입니다. and는 왼쪽이 참일 때만 오른쪽을 검사하므로 빈 바구니의 [-1] 접근을 막습니다.
#                 basket.pop()  # pop()은 마지막 원소를 꺼내 제거합니다. 새 인형과 같은 기존 인형을 제거합니다.
#                 answer += 2  # +=는 더해 다시 저장합니다. 기존 인형과 새 인형, 두 개가 사라집니다.
#             else:  # 바구니가 비었거나 마지막 인형이 다르면 실행합니다.
#                 basket.append(doll)  # append()로 새 인형을 리스트 맨 뒤에 추가합니다.
#
#             break  # 안쪽 행 검사 반복문만 종료합니다. 명령 한 번에 한 개만 뽑고 다음 move로 넘어갑니다.
#
#     return answer  # 모든 명령을 처리한 뒤 사라진 인형 수를 반환하고 함수를 종료합니다.
#
