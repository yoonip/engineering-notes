# 게임 맵 최단거리
# 분류: BFS / deque
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/1844
# 선택 이유: 가중치가 없는 격자의 최단거리는 BFS로 구한다. deque에서 한 칸씩 꺼내고 방문은 넣을 때 기록한다.
# 비용: R×C 격자: 시간 O(RC), 추가 공간 O(RC).

from collections import deque


def solution(maps):
    rows = len(maps)
    cols = len(maps[0])
    distance = [[-1] * cols for _ in range(rows)]
    distance[0][0] = 1
    queue = deque([(0, 0)])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        row, col = queue.popleft()

        if row == rows - 1 and col == cols - 1:
            return distance[row][col]

        for dr, dc in directions:
            next_row = row + dr
            next_col = col + dc

            if not (0 <= next_row < rows and 0 <= next_col < cols):
                continue

            if maps[next_row][next_col] == 0:
                continue

            if distance[next_row][next_col] != -1:
                continue

            distance[next_row][next_col] = distance[row][col] + 1
            queue.append((next_row, next_col))

    return -1
