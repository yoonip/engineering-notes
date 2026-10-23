def solution(name):
    vertical = sum(min(ord(ch) - ord('A'), ord('Z') - ord(ch) + 1) for ch in name)
    n = len(name)
    # 각 위치에서 다음으로 만나는 비-A 위치를 오른쪽부터 미리 구한다.
    next_needed = [n] * (n + 1)
    for i in range(n - 1, -1, -1):
        next_needed[i] = i if name[i] != 'A' else next_needed[i + 1]
    horizontal = n - 1
    for i in range(n):
        tail = n - next_needed[i + 1]
        # 앞쪽을 왕복하는 경로와 뒤쪽을 왕복하는 경로를 비교한다.
        horizontal = min(horizontal, 2 * i + tail, i + 2 * tail)
    return vertical + horizontal
