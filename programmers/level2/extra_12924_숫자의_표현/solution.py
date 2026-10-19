def solution(n):
    # 연속 구간 길이와 가능한 방법 수 초기화.
    length, answer = 1, 0
    while length * (length + 1) // 2 <= n:
        # 증가분을 먼저 빼 시작값 곱만 남김.
        remaining = n - length * (length - 1) // 2
        if remaining % length == 0:
            answer += 1
        length += 1
    return answer
