def solution(arr):
    n = len(arr)
    return int(all(arr[i][j] == arr[j][i] for i in range(n) for j in range(n)))

# 전체 코드 줄별 설명
# def solution(arr):  # def는 함수 정의. 정사각형 이차원 리스트 입력.
#     n = len(arr)  # len은 길이. 행렬 한 변의 크기 저장.
#     return int(all(arr[i][j] == arr[j][i] for i in range(n) for j in range(n)))  # all은 모든 조건이 참인지 검사. 행·열을 바꾼 값과 비교하고 int로 1·0 반환.

# 풀이 요약
# 주대각선을 기준으로 서로 마주 보는 두 칸의 값이 모두 같은지 검사합니다.
# 