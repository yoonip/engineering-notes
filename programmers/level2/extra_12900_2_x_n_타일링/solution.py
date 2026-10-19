def solution(n):
    # 너비 0은 빈 배치 한 가지, 너비 1은 세로 타일 한 가지.
    previous, current = 1, 1
    for _ in range(2, n + 1):
        # 세로 타일 한 장·가로 타일 두 장으로 끝나는 경우의 합.
        previous, current = current, (previous + current) % 1000000007
    return current
