def solution(arr):
    answer = [0, 0]
    def compress(row, column, size):
        value = arr[row][column]
        if all(arr[r][c] == value for r in range(row, row + size) for c in range(column, column + size)):
            answer[value] += 1
            return
        half = size // 2
        compress(row, column, half)
        compress(row, column + half, half)
        compress(row + half, column, half)
        compress(row + half, column + half, half)
    compress(0, 0, len(arr))
    return answer

# 전체 코드 줄별 설명
# def solution(arr):  # def는 함수 정의. arr은 0·1 정사각형 행렬 입력.
#     answer = [0, 0]  # []는 리스트. 압축 후 0·1 개수를 인덱스 0·1에 저장.
#     def compress(row, column, size):  # 중첩 함수. 좌측 위 좌표와 한 변 길이로 영역 표현.
#         value = arr[row][column]  # [][]는 행·열 접근. 영역 첫 칸의 값 저장.
#         if all(arr[r][c] == value for r in range(row, row + size) for c in range(column, column + size)):  # all은 전부 참인지 검사. 중첩 생성식 for로 영역의 모든 칸이 같은지 비교.
#             answer[value] += 1  # +=는 더해 저장. 같은 값 영역을 숫자 하나로 압축해 집계.
#             return  # 값 없는 return은 현재 재귀 호출 종료.
#         half = size // 2  # //는 정수 몫. 영역을 나눌 절반 길이 계산.
#         compress(row, column, half)  # 왼쪽 위 사분면 재귀 처리.
#         compress(row, column + half, half)  # 오른쪽 위 사분면 처리.
#         compress(row + half, column, half)  # 왼쪽 아래 사분면 처리.
#         compress(row + half, column + half, half)  # 오른쪽 아래 사분면 처리.
#     compress(0, 0, len(arr))  # len은 행 수. 전체 영역부터 압축 시작.
#     return answer  # return으로 압축된 0·1 개수 반환.

# 풀이 요약
# 영역 값이 모두 같으면 한 개로 세고, 다르면 네 사분면으로 나눠 같은 규칙을 재귀 적용합니다.
# 예: 전체가 1인 행렬은 크기와 무관하게 [0,1]. 한 변 N일 때 시간 상한 O(N² log N), 재귀 공간 O(log N).
