# 문제: 삼각 달팽이
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/68645
# 풀이: 아래·오른쪽·왼쪽 위로 방향을 바꾸며 채울 길이를 하나씩 줄인다. 삼각형 배열을 채운 뒤 행 순서로 펼친다.
# 복잡도: 삼각형 높이 N: 시간·추가 공간 O(N²).

def solution(n):
    board = [[0] * (r + 1) for r in range(n)]
    r, c, value = -1, 0, 1
    directions = ((1, 0), (0, 1), (-1, -1))
    for side in range(n):
        dr, dc = directions[side % 3]
        for _ in range(n - side):
            r += dr
            c += dc
            board[r][c] = value
            value += 1
    return [number for row in board for number in row]
