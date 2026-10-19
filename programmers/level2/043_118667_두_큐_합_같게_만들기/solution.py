from collections import deque

def solution(queue1, queue2):
    current = sum(queue1)
    total = current + sum(queue2)
    # 전체 합이 홀수이면 같은 정수 합 두 개로 나눌 수 없다.
    if total % 2:
        return -1
    target = total // 2
    first, second = deque(queue1), deque(queue2)
    for moves in range(2 * (len(queue1) + len(queue2)) + 1):
        if current == target:
            return moves
        # 양수이므로 합이 크면 빼고 작으면 가져온다.
        if current > target:
            value = first.popleft()
            second.append(value)
            current -= value
        else:
            value = second.popleft()
            first.append(value)
            current += value
    return -1
