from math import isqrt

def solution(k, d):
    answer = 0
    for x in range(0, d + 1, k):
        # 실수 오차 없이 원 안의 최대 정수 y를 구한다.
        max_y = isqrt(d * d - x * x)
        # 0도 가능한 y이므로 개수에 1을 더한다.
        answer += max_y // k + 1
    return answer
