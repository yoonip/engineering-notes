def solution(arr):
    size = max(len(arr), len(arr[0]))
    answer = [row + [0] * (size - len(row)) for row in arr]
    answer.extend([[0] * size for _ in range(size - len(arr))])
    return answer

# 전체 코드 줄별 설명
# def solution(arr):  # def는 함수 정의. 직사각형 이차원 리스트 입력.
#     size = max(len(arr), len(arr[0]))  # len은 길이, max는 최댓값. 행·열 중 큰 수를 정사각형 한 변으로 선택.
#     answer = [row + [0] * (size - len(row)) for row in arr]  # 리스트 내포로 각 행 끝에 부족한 개수의 0 추가. +는 리스트 연결.
#     answer.extend([[0] * size for _ in range(size - len(arr))])  # 부족한 행만큼 독립적인 0 행을 생성. extend로 여러 행 추가.
#     return answer  # 0으로 채운 정사각형 행렬 반환.

# 풀이 요약
# 행·열 중 큰 길이를 기준으로 부족한 열과 행만 0으로 채웁니다.
# 