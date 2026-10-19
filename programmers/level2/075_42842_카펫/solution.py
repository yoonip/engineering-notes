# 문제: 카펫
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/42842
# 풀이: 전체 넓이의 약수 쌍을 가로·세로 후보로 삼는다. 테두리를 뺀 내부 넓이가 yellow인 조합만 고른다.
# 복잡도: 전체 넓이 A: 반복 O(√A), 추가 공간 O(1).

from math import isqrt

def solution(brown, yellow):
    area = brown + yellow
    for height in range(3, isqrt(area) + 1):
        if area % height == 0:
            width = area // height
            if (width - 2) * (height - 2) == yellow:
                return [width, height]
