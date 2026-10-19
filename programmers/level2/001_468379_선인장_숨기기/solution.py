from collections import deque


def window_minimum(values, size):
    q = deque()
    result = []

    for i, value in enumerate(values):
        while q and q[0] <= i - size:
            q.popleft()

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
