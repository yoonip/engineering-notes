from collections import Counter, deque

def solution(priorities, location):
    queue = deque(enumerate(priorities))
    remaining = Counter(priorities)
    maximum = max(remaining)
    executed = 0
    while queue:
        index, priority = queue.popleft()
        if priority < maximum:
            queue.append((index, priority))
            continue
        executed += 1
        remaining[priority] -= 1
        if index == location:
            return executed
        # 높은 중요도가 소진되면 다음으로 남은 중요도를 찾는다.
        while maximum and remaining[maximum] == 0:
            maximum -= 1
