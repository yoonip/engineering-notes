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

# 전체 코드 줄별 설명
# from collections import deque  # collections의 deque를 import. 진입 순서대로 트럭을 꺼내는 큐 자료구조.
# 
# def solution(bridge_length, weight, truck_weights):  # def는 함수 정의. 다리 길이·허용 무게·트럭 목록 입력.
#     bridge = deque()  # 다리 위 (무게,퇴장 시각) 튜플을 저장할 빈 큐.
#     time = load = 0  # 연쇄 대입으로 현재 시각·다리 위 총 무게 초기화.
#     for truck in truck_weights:  # for~in으로 대기 트럭을 순서대로 처리.
#         time += 1  # +=는 더해 저장. 트럭은 한 초에 한 대씩 새로 진입 가능.
#         while bridge and (bridge[0][1] <= time or load + truck > weight):  # and는 둘 다 참, or는 하나 이상 참. 이미 도착했거나 무게 때문에 기다려야 할 앞 트럭 처리.
#             leaving, exit_time = bridge.popleft()  # popleft는 가장 먼저 진입한 트럭을 꺼내 삭제. 두 값 언패킹.
#             time = max(time, exit_time)  # max는 최댓값. 필요하면 가장 빠른 퇴장 시각까지 바로 건너뜀.
#             load -= leaving  # -=는 빼서 저장. 떠난 트럭 무게 차감.
#         bridge.append((truck, time + bridge_length))  # append로 진입 트럭과 진입 시각+다리 길이인 퇴장 시각 저장.
#         load += truck  # 진입한 트럭의 무게 추가.
#     return bridge[-1][1]  # [-1]은 마지막 트럭, [1]은 퇴장 시각. 모든 트럭이 지난 시각 반환.

# 풀이 요약
# 다리 위 트럭을 퇴장 시각과 함께 큐에 둡니다. 다음 트럭이 무게 때문에 못 들어가면 앞 트럭 퇴장 시각으로 건너뜁니다.
# 예: 길이 2·무게 10의 예제는 마지막 트럭이 8초에 퇴장. 트럭 N개일 때 시간·공간 O(N).
