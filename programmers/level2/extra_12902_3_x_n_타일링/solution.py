def solution(n):
    if n % 2:
        return 0
    # 너비 0은 빈 배치 한 가지, 너비 2는 세 가지.
    previous, current = 1, 3
    for _ in range(4, n + 1, 2):
        # 점화식 f(n)=4f(n-2)-f(n-4), %는 나머지.
        previous, current = current, (4 * current - previous) % 1000000007
    return current
