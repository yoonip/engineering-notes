def solution(n):
    left, total, answer = 1, 0, 0
    for right in range(1, n + 1):
        total += right
        while total > n:
            total -= left
            left += 1
        answer += total == n
    return answer
