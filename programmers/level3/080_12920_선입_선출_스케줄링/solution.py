# 작업 수와 코어별 처리 시간 목록을 받음.
def solution(n, cores):
    # len은 코어 수.
    count = len(cores)
    # 0시각에는 모든 코어가 비어 있어 코어 번호순으로 바로 작업 배정.
    if n <= count:
        # 작업이 코어 수 이하면 마지막 작업의 코어 번호는 n.
        return n
    # 가장 빠른 코어만 추가 작업을 처리해도 되는 시각을 이분 탐색 상한으로 사용.
    left, right = 1, min(cores) * (n - count)
    # n번째 작업이 배정되는 최초 시각 탐색.
    while left < right:
        middle = (left + right) // 2
        # 0시각의 count개에 각 코어의 재배정 횟수를 더함.
        assigned = count + sum(middle // core for core in cores)
        # 이 시각까지 충분한 작업을 시작할 수 있으면 더 이른 시각 탐색.
        if assigned >= n:
            # 가능한 시각은 상한으로 남김.
            right = middle
        else:
            # 이 시각 이하를 버리고 더 늦은 구간 탐색.
            left = middle + 1
    # n번째 작업이 시작되는 정확한 시각.
    time = left
    # 직전 시각까지 배정한 작업을 빼서 time시각에 몇 번째 빈 코어를 골라야 하는지 계산.
    remaining = n - count - sum((time - 1) // core for core in cores)
    # 코어 번호가 작은 순서대로 확인.
    for i, core in enumerate(cores):
        # 처리 시간의 배수 시각에 해당 코어가 비어 다음 작업을 받음.
        if time % core == 0:
            # 현재 빈 코어에 작업 하나 배정.
            remaining -= 1
            # 이 코어가 마지막 n번째 작업을 받는지 확인.
            if remaining == 0:
                # 배열 인덱스는 0부터지만 코어 번호는 1부터라 +1.
                return i + 1
