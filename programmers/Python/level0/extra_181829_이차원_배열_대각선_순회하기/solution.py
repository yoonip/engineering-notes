def solution(board, k):
    return sum(value for i, row in enumerate(board) for j, value in enumerate(row) if i + j <= k)

# 전체 코드 줄별 설명
# def solution(board, k):  # def는 함수 정의. 이차원 리스트와 인덱스 합 기준 입력.
#     return sum(value for i, row in enumerate(board) for j, value in enumerate(row) if i + j <= k)  # enumerate는 위치와 값 제공. 중첩 생성기에서 행+열 인덱스가 k 이하인 칸만 골라 sum으로 합산.

# 풀이 요약
# 행과 열의 인덱스 합이 기준 이하인 위치만 더합니다.
# 