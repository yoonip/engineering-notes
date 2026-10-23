def solution(board, moves):  # 인형 배치와 크레인 이동 순서를 받음
    basket = []  # 뽑은 인형을 담을 리스트
    answer = 0  # 사라진 인형 개수
    n = len(board)  # 보드의 행 개수

    for move in moves:  # 이동 번호를 하나씩 꺼냄
        col = move - 1  # 세로줄 번호를 리스트 인덱스로 바꿈

        for row in range(n):  # 맨 위 행부터 아래로 확인
            if board[row][col] != 0:  # 현재 칸에 인형이 있으면
                doll = board[row][col]  # 꺼낼 인형을 기억
                board[row][col] = 0  # 꺼낸 자리를 빈칸으로 변경

                if len(basket) == 0:  # 바구니가 비어 있으면
                    basket.append(doll)  # 첫 인형을 바구니에 추가
                else:  # 바구니에 인형이 있으면
                    if basket[-1] == doll:  # 마지막 인형과 현재 인형이 같으면
                        basket.pop()  # 기존 마지막 인형을 제거
                        answer += 2  # 기존 인형과 현재 인형 두 개를 셈
                    else:  # 마지막 인형과 현재 인형이 다르면
                        basket.append(doll)  # 현재 인형을 뒤에 추가

                break  # 한 번의 이동에서는 인형 하나만 뽑고 종료

    return answer  # 사라진 인형의 총개수를 반환



def solution(board, moves):
    basket = []
    answer = 0
    n = len(board)
    
    for move in moves:
        col = move -1
        
        for row in range(n):
            if board[row][col] !=0:
                doll = board[row][col]
                board[row][col] = 0
            
                if len(basket) == 0:
                    basket.append(doll)
                else:
                    if basket[-1] ==doll:
                        basket.pop()
                        answer +=2
                    else:
                        basket.append(doll)
                    
                break
    return answer

def solution(board, moves):
    basket = []
    answer = 0
    n = len(board)
    
    for move in moves:
        col = move -1
        
        for row in range(n):
            if board[row][col] !=0:
                doll = board[row][col]
                board[row][col] = 0
                
                if len(basket) == 0:
                    basket.append(doll)
                else:
                    if basket[-1] == doll:
                        basket.pop()
                        answer +=2
                    else:
                        basket.append(doll)
                break
    return answer            
        





# 같은 정답 코드 + 줄별 문법 설명
# 아래는 전체가 주석이므로 실행되지 않습니다.

# def solution(board, moves):  # def로 함수를 정의합니다. 인형 배치와 크레인 명령 리스트를 받습니다.
#     n = len(board)  # len()으로 행 수를 구합니다.
#     board = [row[:] for row in board]  # 리스트 컴프리헨션입니다. [:]로 각 행을 복사하여 원본 입력을 보존합니다.
#     basket = []  # 빈 리스트입니다. 끝에 넣고 빼는 스택으로 사용합니다.
#     answer = 0  # 사라진 인형 수를 저장합니다.
#
#     for move in moves:  # 크레인 명령을 순서대로 하나씩 꺼냅니다.
#         col = move - 1  # 명령의 열 번호는 1부터, 리스트 인덱스는 0부터이므로 1을 뺍니다.
#
#         for row in range(n):  # 0번 행부터 n-1번 행까지 위에서 아래로 검사합니다.
#             if board[row][col] == 0:  # [행][열]로 값을 읽습니다. ==는 같은지 비교하며 0은 빈칸입니다.
#                 continue  # 현재 반복의 나머지를 건너뛰고 다음 행을 검사합니다.
#
#             doll = board[row][col]  # 발견한 인형의 값을 저장합니다.
#             board[row][col] = 0  # 뽑은 자리를 빈칸으로 바꿉니다.
#
#             if basket and basket[-1] == doll:  # 바구니가 비지 않았을 때만 and 오른쪽을 검사합니다. [-1]은 마지막 원소입니다.
#                 basket.pop()  # pop()으로 바구니의 마지막 인형을 제거합니다. 새 인형은 추가하지 않습니다.
#                 answer += 2  # 기존 인형과 새 인형, 총 두 개가 사라지므로 2를 더합니다.
#             else:  # 바구니가 비었거나 마지막 인형이 다르면 실행합니다.
#                 basket.append(doll)  # append()로 새 인형을 맨 뒤에 추가합니다.
#
#             break  # 안쪽 행 검사 반복문을 종료합니다. 한 명령에서 하나만 뽑고 다음 명령으로 갑니다.
#
#     return answer  # 모든 명령을 처리한 뒤 사라진 인형 수를 반환합니다.