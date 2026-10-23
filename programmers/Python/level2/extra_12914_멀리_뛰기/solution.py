def solution(n):
    # 0칸은 아무것도 안 하는 한 가지, 1칸은 한 번 뛰는 한 가지.
    previous, current = 1, 1
    for _ in range(2, n + 1):
        # %는 나머지.
        previous, current = current, (previous + current) % 1234567
    return current
