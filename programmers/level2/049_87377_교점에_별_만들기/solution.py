# 문제: 교점에 별 만들기
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/87377
# 풀이: 직선 쌍의 교점을 정수 나눗셈으로 판정한다. 교점 set으로 중복을 없앤 뒤 최소 사각형에 별을 배치한다.
# 복잡도: 직선 N개·고유 교점 P개·출력 넓이 A: 시간 O(N²+A), 추가 공간 O(P+A).

from itertools import combinations

def solution(line):
    points = set()
    for first, second in combinations(line, 2):
        a, b, e = first
        c, d, f = second
        denominator = a * d - b * c
        if denominator == 0:
            continue
        nx, ny = b * f - e * d, e * c - a * f
        if nx % denominator == 0 and ny % denominator == 0:
            points.add((nx // denominator, ny // denominator))
    min_x = min(x for x, y in points)
    max_x = max(x for x, y in points)
    min_y = min(y for x, y in points)
    max_y = max(y for x, y in points)
    board = [['.'] * (max_x - min_x + 1) for _ in range(max_y - min_y + 1)]
    for x, y in points:
        board[max_y - y][x - min_x] = '*'
    return [''.join(row) for row in board]
