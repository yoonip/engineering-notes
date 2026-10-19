from collections import deque

def solution(x, y, n):
    distance = [-1] * (y + 1)
    distance[x] = 0
    queue = deque([x])
    while queue:
        value = queue.popleft()
        if value == y:
            return distance[value]
        for next_value in (value + n, value * 2, value * 3):
            if next_value <= y and distance[next_value] == -1:
                distance[next_value] = distance[value] + 1
                queue.append(next_value)
    return -1

# 전체 코드 줄별 설명
# from collections import deque  # from~import로 collections의 deque 가져오기. 먼저 넣은 값을 먼저 꺼내는 큐에 사용.
# 
# def solution(x, y, n):  # def는 함수 정의, () 안은 시작 수·목표 수·더할 수 입력.
#     distance = [-1] * (y + 1)  # []는 리스트, *는 반복. 숫자별 최소 연산 수를 -1(미방문)로 초기화.
#     distance[x] = 0  # [x]는 x번째 원소. 시작 수의 연산 횟수는 0.
#     queue = deque([x])  # 시작 수 하나를 담은 큐 생성.
#     while queue:  # 큐가 비지 않은 동안 반복.
#         value = queue.popleft()  # popleft는 왼쪽의 가장 오래된 값을 꺼내 삭제.
#         if value == y:  # if는 조건 분기, ==는 같음. 목표에 도착했는지 검사.
#             return distance[value]  # BFS에서 첫 도착의 연산 횟수가 최솟값.
#         for next_value in (value + n, value * 2, value * 3):  # () 튜플의 세 연산 결과를 for로 순회. +는 덧셈, *는 곱셈.
#             if next_value <= y and distance[next_value] == -1:  # <=는 이하, and는 둘 다 참. 목표 이하의 미방문 수만 선택.
#                 distance[next_value] = distance[value] + 1  # 한 번 연산한 거리로 방문 표시.
#                 queue.append(next_value)  # append로 다음 수를 큐 끝에 추가.
#     return -1  # 모든 가능한 수를 탐색해도 목표가 없으면 -1 반환.

# 풀이 요약
# 숫자를 상태로 보고 세 연산을 한 번씩 적용하는 BFS를 합니다. 연산은 수를 증가시키므로 y를 넘으면 제외합니다.
# 예: 10→20→40은 2회, 2에서 5는 n=4로 만들 수 없어 -1. 시간·공간 O(y).
