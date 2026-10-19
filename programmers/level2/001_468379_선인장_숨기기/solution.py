# 문제: 선인장 숨기기
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/468379
# 풀이: 행과 열에 단조 deque를 차례로 적용한다. 각 인덱스를 한 번씩 넣고 빼면서 직사각형 안의 첫 빗방울 시각을 구한다.
# 복잡도: 행 M·열 N·비 기록 D개: 시간 O(MN+D), 추가 공간 O(MN).

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
