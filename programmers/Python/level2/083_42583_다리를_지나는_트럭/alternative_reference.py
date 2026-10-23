from collections import deque

def solution(bridge_length, weight, truck_weights):
    waiting = deque(truck_weights)
    bridge = deque([0] * bridge_length)
    time = load = 0
    while waiting or load:
        time += 1
        load -= bridge.popleft()
        if waiting and load + waiting[0] <= weight:
            truck = waiting.popleft()
            bridge.append(truck)
            load += truck
        else:
            bridge.append(0)
    return time
