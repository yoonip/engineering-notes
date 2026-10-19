def solution(n):
    dp = {0: 1}
    for _ in range(n):
        next_dp = {}
        def fill(mask, following, count):
            if mask == 7:
                next_dp[following] = (next_dp.get(following, 0) + count) % 1000000007
                return
            row = next(i for i in range(3) if not (mask >> i & 1))
            # 가로 도미노는 다음 열의 같은 칸을 예약한다.
            fill(mask | (1 << row), following | (1 << row), count)
            if row + 1 < 3 and not (mask >> (row + 1) & 1):
                fill(mask | (3 << row), following, count)
        for mask, count in dp.items():
            fill(mask, 0, count)
        dp = next_dp
    return dp.get(0, 0)
