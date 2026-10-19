# 공원 산책
# 분류: 격자 시뮬레이션
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/172928
# 선택 이유: 이동할 경로의 모든 칸을 확인해야 중간 장애물을 놓치지 않는다.
# 비용: H×W 격자, 이동 거리 합 D: 시간 O(HW+D), 추가 공간 O(1).

def solution(park, routes):
    height = len(park)
    width = len(park[0])

    row, col = 0, 0
    for r, line in enumerate(park):
        if "S" in line:
            row, col = r, line.index("S")
            break

    directions = {
        "N": (-1, 0),
        "S": (1, 0),
        "W": (0, -1),
        "E": (0, 1),
    }

    for route in routes:
        direction, distance = route.split()
        distance = int(distance)
        dr, dc = directions[direction]

        next_row, next_col = row, col
        valid = True

        for _ in range(distance):
            next_row += dr
            next_col += dc

            if not (0 <= next_row < height and 0 <= next_col < width):
                valid = False
                break

            if park[next_row][next_col] == "X":
                valid = False
                break

        if valid:
            row, col = next_row, next_col

    return [row, col]
