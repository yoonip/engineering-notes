from math import isqrt

def solution(r1, r2):
    answer = 0
    for x in range(1, r2 + 1):
        # 바깥원 안에 들어오는 y의 정수 최댓값이다.
        high = isqrt(r2 * r2 - x * x)
        inner = max(0, r1 * r1 - x * x)
        low = isqrt(inner)
        # 안쪽원 바깥 조건은 제곱근의 올림이다.
        if low * low < inner:
            low += 1
        answer += high - low + 1
    # 양의 x·음이 아닌 y 영역을 네 번 회전하면 전체를 중복 없이 센다.
    return answer * 4
