# 사람 수와 심사관별 한 사람 처리 시간을 받음.
def solution(n, times):
    # 가장 빠른 심사관 혼자 전부 처리하는 시간을 가능한 상한으로 사용.
    left, right = 0, min(times) * n
    # 가능한 최소 시간을 찾는 이분 탐색.
    while left < right:
        # 탐색 범위의 중간 시간.
        middle = (left + right) // 2
        # middle 시간까지 심사를 마칠 수 있는 사람 수.
        completed = 0
        # for로 심사관의 처리 시간을 순회.
        for time in times:
            # 각 심사관이 해당 시간 내 완료할 수 있는 인원 합산.
            completed += middle // time
            # 중간 시간이 충분한 경우.
            if completed >= n:
                break
        # 중간 시간이 충분한 경우.
        if completed >= n:
            # 더 작은 시간도 가능한지 왼쪽 범위 탐색.
            right = middle
        else:
            # middle 이하는 불가능하므로 다음 시간부터 탐색.
            left = middle + 1
    # 두 경계가 만나는 최소 가능 시간 반환.
    return left
