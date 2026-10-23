def solution(m, n, h, w, drops):
    def find(dry_until):
        # 이 시각까지 젖은 칸을 1로 표시하고 누적합을 만든다.
        wet = [[0] * n for _ in range(m)]
        for r, c in drops[:dry_until]:
            wet[r][c] = 1
        prefix = [[0] * (n + 1) for _ in range(m + 1)]
        for r in range(m):
            running = 0
            for c in range(n):
                running += wet[r][c]
                prefix[r+1][c+1] = prefix[r][c+1] + running
        for r in range(m-h+1):
            for c in range(n-w+1):
                total = prefix[r+h][c+w]-prefix[r][c+w]-prefix[r+h][c]+prefix[r][c]
                if total == 0:
                    return [r, c]
        return None
    low, high = 0, len(drops)
    while low < high:
        mid = (low + high + 1) // 2
        if find(mid) is not None:
            low = mid
        else:
            high = mid - 1
    return find(low)
