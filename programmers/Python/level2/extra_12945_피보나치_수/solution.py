def solution(n):
    # 두 변수만 사용하는 동적 계획법(DP).
    previous, current = 0, 1
    for _ in range(n):
        # 연속 두 피보나치 값을 다음으로 이동.
        previous, current = current, (previous + current) % 1234567
    return previous
