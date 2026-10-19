def solution(depth, money, excavate):
    # 전체 열 수.
    n = len(depth)
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    # 구간마다 먼저 굴착할 최적의 열 번호 저장.
    choice = [[0] * (n + 1) for _ in range(n)]
    for size in range(1, n + 1):
        # 구간의 왼쪽 끝을 순회하는 for 반복.
        for left in range(n - size + 1):
            right = left + size
            # 최소값 비교의 초기값.
            best = float('inf')
            for middle in range(left, right):
                # 현재 비용에 왼쪽·오른쪽 중 최악의 추가 비용을 더함.
                cost = depth[middle] + max(dp[left][middle], dp[middle + 1][right])
                if cost < best:
                    best = cost
                    # 이 구간의 최적 첫 굴착 위치 저장.
                    choice[left][right] = middle
            dp[left][right] = best
    # 처음에는 전체 열이 후보.
    left, right = 0, n
    while left < right:
        # 미리 구한 최적 전략에서 굴착할 열을 선택.
        middle = choice[left][right]
        result = excavate(middle + 1)
        # 0이면 실제 보물을 발굴한 상태.
        if result == 0:
            return middle + 1
        if result < 0:
            # 현재 열을 제외한 왼쪽 구간으로 축소.
            right = middle
        else:
            left = middle + 1
    return 0
