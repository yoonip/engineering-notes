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

# 전체 코드 줄별 설명
# from collections import deque  # collections의 deque를 import. 앞에서 꺼내고 뒤에 추가하는 큐 자료구조.
# 
# def solution(priorities, location):  # def는 함수 정의. 우선순위 목록·찾을 초기 인덱스 입력.
#     queue = deque(enumerate(priorities))  # enumerate는 (초기 인덱스,값) 제공. 프로세스의 식별자와 우선순위를 큐에 보존.
#     executed = 0  # =는 대입. 실행한 프로세스 수 초기화.
#     while queue:  # while은 반복. 큐가 비지 않은 동안 진행.
#         index, priority = queue.popleft()  # popleft로 맨 앞을 꺼내 삭제하고 두 값 언패킹.
#         if any(other > priority for _, other in queue):  # any는 하나라도 참, >는 큼. _는 안 쓰는 ID. 더 높은 우선순위가 남았는지 검사.
#             queue.append((index, priority))  # append로 현재 프로세스를 큐 끝으로 이동.
#         else:  # else는 더 높은 우선순위가 없어 실행하는 경우.
#             executed += 1  # +=는 더해 저장. 실행 순서 증가.
#             if index == location:  # ==는 같음. 찾는 초기 인덱스의 프로세스인지 검사.
#                 return executed  # return으로 실행 순서 반환.

# 풀이 요약
# 큐 앞 프로세스보다 우선순위가 높은 것이 남아 있으면 뒤로 보내고, 없으면 실행합니다. 초기 인덱스로 대상 프로세스를 추적합니다.
# 예: [2,1,3,2]의 인덱스 2는 가장 먼저 실행되어 1. 우선순위 종류가 9개로 고정이므로 시간 O(N²), 공간 O(N).
