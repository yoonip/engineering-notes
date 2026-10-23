def solution(n):
    answer = 0
    while n:
        # 홀수 위치는 1칸 점프 비용이 필요하고 짝수는 비용 0.
        answer += n % 2
        n //= 2
    return answer
