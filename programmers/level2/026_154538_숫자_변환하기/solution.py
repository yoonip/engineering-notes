from collections import deque

def solution(x, y, n):
    distance = [-1] * (y + 1)
    distance[x] = 0
    queue = deque([x])
    while queue:
        value = queue.popleft()
        if value == y:
            return distance[value]
        # 한 번에 가능한 세 연산 결과를 확인한다.
        for next_value in (value + n, value * 2, value * 3):
            # 값은 증가하므로 목표를 넘은 상태는 볼 필요가 없다.
            if next_value <= y and distance[next_value] == -1:
                distance[next_value] = distance[value] + 1
                queue.append(next_value)
    return -1
