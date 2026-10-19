# 문제: 리코쳇 로봇
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/169199
# 풀이: 미끄러진 뒤 멈춘 위치를 BFS의 정점으로 삼는다. deque에서 가까운 이동 횟수부터 꺼내 목표에 처음 도달한 거리를 반환한다.
# 복잡도: 행 R·열 C: 시간 O(RC·max(R,C)), 추가 공간 O(RC).

from collections import deque

def solution(board):
    rows, cols = len(board), len(board[0])
    distance = [[-1] * cols for _ in range(rows)]
    queue = deque()
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'R':
                distance[r][c] = 0
                queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        if board[r][c] == 'G':
            return distance[r][c]
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r, c
            while 0 <= nr + dr < rows and 0 <= nc + dc < cols and board[nr + dr][nc + dc] != 'D':
                nr += dr
                nc += dc
            if distance[nr][nc] == -1:
                distance[nr][nc] = distance[r][c] + 1
                queue.append((nr, nc))
    return -1
