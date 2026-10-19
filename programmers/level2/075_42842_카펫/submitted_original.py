from math import isqrt

def solution(brown, yellow):
    area = brown + yellow
    for height in range(3, isqrt(area) + 1):
        if area % height == 0:
            width = area // height
            if (width - 2) * (height - 2) == yellow:
                return [width, height]

# 전체 코드 줄별 설명
# from math import isqrt  # math의 isqrt를 import. 제곱근의 정수 내림값 반환.
# 
# def solution(brown, yellow):  # def는 함수 정의. 갈색·노란색 칸 수 입력.
#     area = brown + yellow  # +는 덧셈, =는 대입. 전체 카펫 넓이 계산.
#     for height in range(3, isqrt(area) + 1):  # range는 끝 미포함. 가로>=세로이므로 세로는 3부터 제곱근까지 검사.
#         if area % height == 0:  # %는 나머지, ==는 같음. 전체 넓이를 나눌 수 있는 세로 길이인지 검사.
#             width = area // height  # //는 정수 몫. 해당 세로에서 가로 길이 계산.
#             if (width - 2) * (height - 2) == yellow:  # ()는 연산 묶음, *는 곱셈. 테두리 한 칸씩을 뺀 내부 넓이 검사.
#                 return [width, height]  # [] 리스트에 가로·세로 순서로 담아 반환.

# 풀이 요약
# 전체 넓이의 약수로 가로·세로 후보를 만들고, 테두리를 뺀 내부 넓이가 yellow인지 확인합니다.
# 예: 전체 12칸은 4×3이고 내부 2×1=2라 [4,3]. 넓이 A에 대해 시간 O(√A), 공간 O(1).
