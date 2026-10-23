from math import isqrt

def solution(brown, yellow):
    # 전체 카펫 넓이 계산.
    area = brown + yellow
    for height in range(3, isqrt(area) + 1):
        # 전체 넓이를 나눌 수 있는 세로 길이인지 검사.
        if area % height == 0:
            width = area // height
            # 테두리 한 칸씩을 뺀 내부 넓이 검사.
            if (width - 2) * (height - 2) == yellow:
                return [width, height]
