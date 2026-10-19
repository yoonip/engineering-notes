# 문제: 빛의 경로 사이클
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/86052
# 풀이: 칸과 진행 방향을 함께 방문 상태로 둔다. 다음 상태가 정해진 경로를 따라가며 각 상태를 한 번씩 사이클에 배정한다.
# 복잡도: 상태 V=4·행·열, 사이클 K개: 시간 O(V+K log K), 추가 공간 O(V).

def solution(grid):
    rows, cols = len(grid), len(grid[0])
    visited = [bytearray(cols * 4) for _ in range(rows)]
    directions = ((-1, 0), (0, 1), (1, 0), (0, -1))
    answer = []
    for r in range(rows):
        for c in range(cols):
            for direction in range(4):
                if visited[r][c * 4 + direction]:
                    continue
                x, y, d, length = r, c, direction, 0
                while not visited[x][y * 4 + d]:
                    visited[x][y * 4 + d] = 1
                    length += 1
                    if grid[x][y] == 'L':
                        d = (d - 1) % 4
                    elif grid[x][y] == 'R':
                        d = (d + 1) % 4
                    dx, dy = directions[d]
                    x, y = (x + dx) % rows, (y + dy) % cols
                answer.append(length)
    return sorted(answer)
