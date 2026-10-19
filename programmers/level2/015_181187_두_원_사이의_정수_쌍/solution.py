# 문제: 두 원 사이의 정수 쌍
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/181187
# 풀이: x를 고정하고 두 원 사이의 정수 y 범위를 isqrt로 구한다. 정수 계산으로 경계를 포함하고 사분면 대칭을 이용한다.
# 복잡도: 바깥 반지름 R: 시간 O(R), 추가 공간 O(1). isqrt의 큰 정수 비용은 별도다.

from math import isqrt

def solution(r1, r2):
    answer = 0
    for x in range(1, r2 + 1):
        high = isqrt(r2 * r2 - x * x)
        inner = max(0, r1 * r1 - x * x)
        low = isqrt(inner)
        if low * low < inner:
            low += 1
        answer += high - low + 1
    return answer * 4
