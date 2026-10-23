from collections import deque

def solution(priorities, location):
    queue = deque(enumerate(priorities))
    executed = 0
    while queue:
        index, priority = queue.popleft()
        if any(other > priority for _, other in queue):
            queue.append((index, priority))
        else:
            executed += 1
            if index == location:
                return executed
