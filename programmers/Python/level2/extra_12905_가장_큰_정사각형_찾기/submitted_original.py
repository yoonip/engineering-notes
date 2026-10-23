def solution(board):
    dp = [0] * (len(board[0]) + 1)
    best = 0
    for row in board:
        diagonal = 0
        for col, value in enumerate(row, 1):
            above = dp[col]
            if value:
                dp[col] = min(above, dp[col - 1], diagonal) + 1
                if dp[col] > best:
                    best = dp[col]
            else:
                dp[col] = 0
            diagonal = above
    return best * best

# 전체 코드 줄별 설명
# def solution(board):  # def는 함수 정의. 0·1 격자 입력.
#     dp = [0] * (len(board[0]) + 1)  # []는 리스트, len은 열 수. dp[c]는 해당 칸을 오른쪽 아래로 하는 최대 정사각형 한 변. 0번은 경계용.
#     best = 0  # 발견한 최대 한 변 길이.
#     for row in board:  # for로 위에서 아래로 행 순회.
#         diagonal = 0  # 현재 칸의 왼쪽 위 값. 행 시작 바깥 경계에서는 0.
#         for col, value in enumerate(row, 1):  # enumerate(row,1)은 인덱스를 1부터 제공. 경계용 칸 다음부터 계산.
#             above = dp[col]  # 현재 값을 덮기 전에 이전 행의 위쪽 값을 저장.
#             if value:  # 1은 참, 0은 거짓. 현재 칸이 1일 때만 정사각형 가능.
#                 dp[col] = min(above, dp[col - 1], diagonal) + 1  # min은 최솟값. 위·왼쪽·왼쪽 위 세 정사각형 중 가장 작은 변에 현재 칸을 붙임.
#                 if dp[col] > best:  # >는 초과. 최대 변 길이 갱신 여부 검사.
#                     best = dp[col]  # 새 최댓값 저장.
#             else:  # 현재 칸이 0이면 어떤 1 정사각형의 끝도 될 수 없음.
#                 dp[col] = 0  # 해당 상태 초기화.
#             diagonal = above  # 다음 열의 왼쪽 위는 지금 저장한 이전 행 값.
#     return best * best  # *는 곱셈. 요구한 값은 변이 아니라 넓이이므로 제곱 반환.

# 풀이 요약
# 현재가 1이면 인접한 위·왼쪽·왼쪽 위에서 가능한 정사각형의 최소 크기+1만큼 확장할 수 있다. 셋 중 하나라도 부족하면 그보다 큰 정사각형은 못 만든다.
# 예제의 최대 변은 3이라 넓이는 9. 이전 행 배열 하나와 덮어쓰기 전 대각 값만 보관해 시간 O(RC), 추가 공간 O(C).
# 