# 문제: 석유 시추
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/250136
# 풀이: 석유 덩어리마다 스택 DFS로 크기와 지나는 열을 구한다. 열 집합을 써서 같은 덩어리가 한 열에 중복 합산되지 않게 한다.
# 복잡도: 행 R·열 C: 시간 O(RC), 추가 공간 O(RC). 입력 land를 방문 표시로 변경한다.

def solution(land):
    rows, cols = len(land), len(land[0])
    totals = [0] * cols
    for r in range(rows):
        for c in range(cols):
            if land[r][c] == 0:
                continue
            stack = [(r, c)]
            land[r][c] = 0
            columns = set()
            size = 0
            while stack:
                x, y = stack.pop()
                size += 1
                columns.add(y)
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and land[nx][ny] == 1:
                        land[nx][ny] = 0
                        stack.append((nx, ny))
            for column in columns:
                totals[column] += size
    return max(totals)
