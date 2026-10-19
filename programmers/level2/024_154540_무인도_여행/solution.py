# 문제: 무인도 여행
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/154540
# 풀이: 연결된 땅을 스택으로 탐색하며 식량을 합산한다. 방문 표시는 보드에 남겨 같은 칸을 다시 합산하지 않는다.
# 복잡도: 전체 칸 V개·섬 K개: 시간 O(V+K log K), 추가 공간 O(V).

def solution(maps):
    board = [list(row) for row in maps]
    rows, cols = len(board), len(board[0])
    answer = []
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'X':
                continue
            food = int(board[r][c])
            board[r][c] = 'X'
            stack = [(r, c)]
            while stack:
                x, y = stack.pop()
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and board[nx][ny] != 'X':
                        food += int(board[nx][ny])
                        board[nx][ny] = 'X'
                        stack.append((nx, ny))
            answer.append(food)
    return sorted(answer) if answer else [-1]
