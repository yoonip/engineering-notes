from collections import deque

def solution(food_times, k):
    if k>200000:raise ValueError("시간 20만 초 이하의 직접 시뮬레이션 비교용입니다")
    remaining=food_times[:];queue=deque(i for i,x in enumerate(remaining) if x)
    for _ in range(k):
        if not queue:return -1
        index=queue.popleft();remaining[index]-=1
        if remaining[index]:queue.append(index)
    return queue[0]+1 if queue else -1
