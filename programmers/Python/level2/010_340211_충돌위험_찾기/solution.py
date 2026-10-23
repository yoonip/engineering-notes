def solution(points, routes):
    robots = []
    for route in routes:
        r, c = points[route[0] - 1]
        robots.append((r, c, 1, route))
    answer = 0
    while robots:
        counts = {}
        next_robots = []
        for r, c, index, route in robots:
            position = (r, c)
            # 같은 시각 같은 좌표에 있는 로봇 수를 센다.
            counts[position] = counts.get(position, 0) + 1
            if index == len(route):
                continue
            target_r, target_c = points[route[index] - 1]
            # 행을 먼저 맞춘 뒤 열을 움직인다.
            if r != target_r:
                r += 1 if r < target_r else -1
            elif c != target_c:
                c += 1 if c < target_c else -1
            if r == target_r and c == target_c:
                index += 1
            next_robots.append((r, c, index, route))
        for count in counts.values():
            # 여러 대가 모여도 좌표 하나의 위험은 한 번만 센다.
            if count >= 2:
                answer += 1
        robots = next_robots
    return answer
