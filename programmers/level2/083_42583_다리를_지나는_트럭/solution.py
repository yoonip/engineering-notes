from collections import deque

def solution(bridge_length, weight, truck_weights):
    # 다리 위 (무게,퇴장 시각) 튜플을 저장할 빈 큐.
    bridge = deque()
    time = load = 0
    # 대기 트럭을 순서대로 처리.
    for truck in truck_weights:
        time += 1
        while bridge and (bridge[0][1] <= time or load + truck > weight):
            # 두 값 언패킹.
            leaving, exit_time = bridge.popleft()
            time = max(time, exit_time)
            # 떠난 트럭 무게 차감.
            load -= leaving
        bridge.append((truck, time + bridge_length))
        # 진입한 트럭의 무게 추가.
        load += truck
    return bridge[-1][1]
