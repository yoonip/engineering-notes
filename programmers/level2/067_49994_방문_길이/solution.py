# 문제: 방문 길이
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/49994
# 풀이: 두 끝점을 정렬한 간선을 set에 넣는다. 같은 길의 왕복을 같은 키로 표현해 처음 방문한 길만 센다.
# 복잡도: 명령 N개: 평균 시간 O(N), 길 집합은 고정 격자에서 최대 220개다.

def solution(dirs):
    moves = {'U': (0, 1), 'D': (0, -1), 'R': (1, 0), 'L': (-1, 0)}
    x = y = 0
    edges = set()
    for command in dirs:
        dx, dy = moves[command]
        nx, ny = x + dx, y + dy
        if -5 <= nx <= 5 and -5 <= ny <= 5:
            edge = tuple(sorted(((x, y), (nx, ny))))
            edges.add(edge)
            x, y = nx, ny
    return len(edges)
