# 문제: 두 큐 합 같게 만들기
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/118667
# 풀이: 합이 큰 큐의 앞 원소를 작은 큐로 옮긴다. 양수 조건에서 두 포인터처럼 합을 조절하며 deque로 앞 삭제 비용을 줄인다.
# 복잡도: 각 큐 길이 N: 시간·추가 공간 O(N). 원소는 양수다.

from collections import deque

def solution(queue1, queue2):
    current = sum(queue1)
    total = current + sum(queue2)
    if total % 2:
        return -1
    target = total // 2
    first, second = deque(queue1), deque(queue2)
    for moves in range(2 * (len(queue1) + len(queue2)) + 1):
        if current == target:
            return moves
        if current > target:
            value = first.popleft()
            second.append(value)
            current -= value
        else:
            value = second.popleft()
            first.append(value)
            current += value
    return -1
