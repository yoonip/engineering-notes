# 문제: 당구 연습
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/169198
# 풀이: 목표 공을 각 벽에 대칭시켜 반사 경로를 직선 거리로 바꾼다. 벽보다 목표 공을 먼저 맞히는 후보는 제외한다.
# 복잡도: 공 B개: 시간 O(B), 반환 배열을 제외한 추가 공간 O(1).

def solution(m, n, startX, startY, balls):
    answer = []
    for x, y in balls:
        distances = []
        if not (startY == y and x < startX):
            distances.append((startX + x) ** 2 + (startY - y) ** 2)
        if not (startY == y and x > startX):
            distances.append((2 * m - startX - x) ** 2 + (startY - y) ** 2)
        if not (startX == x and y < startY):
            distances.append((startX - x) ** 2 + (startY + y) ** 2)
        if not (startX == x and y > startY):
            distances.append((startX - x) ** 2 + (2 * n - startY - y) ** 2)
        answer.append(min(distances))
    return answer
