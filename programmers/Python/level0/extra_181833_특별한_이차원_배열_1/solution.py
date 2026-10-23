def solution(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. 정사각형 행렬의 크기 입력.
#     return [[int(i == j) for j in range(n)] for i in range(n)]  # 중첩 리스트 내포로 행·열 생성. range는 0부터 n-1, ==는 같음 비교, int는 참을 1·거짓을 0으로 변환.

# 풀이 요약
# 행 번호와 열 번호가 같은 대각선만 1로 채웁니다.
# 