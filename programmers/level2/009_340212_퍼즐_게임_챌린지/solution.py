def solution(diffs, times, limit):
    left = 1
    right = max(diffs)
    # 소요 시간이 제한 안에 들어오는 최소 숙련도를 찾는다.
    while left < right:
        level = (left + right) // 2
        elapsed = 0
        previous = 0
        for diff, current in zip(diffs, times):
            elapsed += current
            if diff > level:
                # 실패 한 번에는 현재 퍼즐과 이전 퍼즐 시간이 함께 든다.
                elapsed += (diff - level) * (current + previous)
            # 이미 제한을 넘었으므로 이 숙련도의 나머지 계산은 필요 없다.
            if elapsed > limit:
                break
            previous = current
        if elapsed <= limit:
            right = level
        else:
            left = level + 1
    return left
