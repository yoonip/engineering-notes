from collections import deque


def window_minimum(values, size):
    q = deque()
    result = []

    for i, value in enumerate(values):
        # 현재 창에서 빠진 후보를 앞에서 제거한다.
        while q and q[0] <= i - size:
            q.popleft()

        # 새 값보다 큰 후보는 이후에도 최솟값이 될 수 없다.
        while q and values[q[-1]] >= value:
            q.pop()

        q.append(i)

        if i >= size - 1:
            result.append(values[q[0]])

    return result


def solution(m, n, h, w, drops):
    never = len(drops) + 1
    rain = [never] * (m * n)

    for time, (r, c) in enumerate(drops, start=1):
        rain[r * n + c] = time

    cols = n - w + 1

    # 가로 창의 최솟값을 먼저 구한 뒤 세로 창을 계산한다.
    row_min = []

    for r in range(m):
        row = rain[r * n:(r + 1) * n]
        row_min.extend(window_minimum(row, w))

    best_time = -1
    answer = [0, 0]

    for c in range(cols):
        column = row_min[c::cols]
        area_times = window_minimum(column, h)

        for r, time in enumerate(area_times):
            if time > best_time or (
                time == best_time and [r, c] < answer
            ):
                best_time = time
                answer = [r, c]

    return answer
