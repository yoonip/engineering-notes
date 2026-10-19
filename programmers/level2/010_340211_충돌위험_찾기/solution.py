# 문제: 충돌위험 찾기
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/340211
# 풀이: 같은 시각의 좌표를 해시로 집계해 충돌 지점을 센다. 로봇을 행 우선으로 한 칸씩 옮긴 뒤 다음 시각을 처리한다.
# 복잡도: 로봇 R대·최대 이동 시간 T: 시간 O(RT), 추가 공간 O(R).

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
            counts[position] = counts.get(position, 0) + 1
            if index == len(route):
                continue
            target_r, target_c = points[route[index] - 1]
            if r != target_r:
                r += 1 if r < target_r else -1
            elif c != target_c:
                c += 1 if c < target_c else -1
            if r == target_r and c == target_c:
                index += 1
            next_robots.append((r, c, index, route))
        for count in counts.values():
            if count >= 2:
                answer += 1
        robots = next_robots
    return answer
