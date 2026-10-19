# 문제: 다리를 지나는 트럭
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/42583
# 풀이: 트럭의 무게와 퇴장 시각을 deque에 저장한다. 무게가 부족하면 앞 트럭의 퇴장 시각으로 바로 이동한다.
# 복잡도: 트럭 N개: 시간 O(N), 추가 공간 O(N). 비어 있는 초를 하나씩 반복하지 않는다.

from collections import deque

def solution(bridge_length, weight, truck_weights):
    bridge = deque()
    time = load = 0
    for truck in truck_weights:
        time += 1
        while bridge and (bridge[0][1] <= time or load + truck > weight):
            leaving, exit_time = bridge.popleft()
            time = max(time, exit_time)
            load -= leaving
        bridge.append((truck, time + bridge_length))
        load += truck
    return bridge[-1][1]
