def solution(m, n, startX, startY, balls):
    answer = []
    for x, y in balls:
        distances = []
        # 왼쪽 벽보다 공을 먼저 맞히는 일직선 경로는 제외한다.
        if not (startY == y and x < startX):
            distances.append((startX + x) ** 2 + (startY - y) ** 2)
        if not (startY == y and x > startX):
            distances.append((2 * m - startX - x) ** 2 + (startY - y) ** 2)
        if not (startX == x and y < startY):
            distances.append((startX - x) ** 2 + (startY + y) ** 2)
        if not (startX == x and y > startY):
            distances.append((startX - x) ** 2 + (2 * n - startY - y) ** 2)
        # 가능한 네 벽 반사 경로 중 최솟값을 고른다.
        answer.append(min(distances))
    return answer
