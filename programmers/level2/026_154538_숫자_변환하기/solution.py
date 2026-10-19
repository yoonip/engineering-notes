# 문제: 숫자 변환하기
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/154538
# 풀이: 숫자를 상태로 보고 세 연산을 간선으로 삼아 deque BFS를 수행한다. 모두 증가하는 연산이므로 목표보다 큰 상태는 제외한다.
# 복잡도: 목표 값 Y: 시간·추가 공간 O(Y).

from collections import deque

def solution(x, y, n):
    distance = [-1] * (y + 1)
    distance[x] = 0
    queue = deque([x])
    while queue:
        value = queue.popleft()
        if value == y:
            return distance[value]
        for next_value in (value + n, value * 2, value * 3):
            if next_value <= y and distance[next_value] == -1:
                distance[next_value] = distance[value] + 1
                queue.append(next_value)
    return -1
