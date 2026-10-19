from collections import deque

def solution(queue1, queue2):
    current = sum(queue1)
    total = current + sum(queue2)
    if total % 2:
        return -1
    target = total // 2
    first, second = deque(queue1), deque(queue2)
    for moves in range(2 * (len(queue1) + len(queue2)) + 1):
        if current == target:
            return moves
        if current > target:
            value = first.popleft()
            second.append(value)
            current -= value
        else:
            value = second.popleft()
            first.append(value)
            current += value
    return -1

# 전체 코드 줄별 설명
# from collections import deque  # collections의 deque를 import. 앞에서 꺼내고 뒤에 넣는 작업이 빠른 큐.
# 
# def solution(queue1, queue2):  # def는 함수 정의, ()의 두 목록이 초기 큐 입력.
#     current = sum(queue1)  # sum은 합계. 첫 큐의 합 저장.
#     total = current + sum(queue2)  # +로 두 큐 전체 합 계산.
#     if total % 2:  # %는 나머지. 홀수면 두 정수 합을 같게 나눌 수 없음.
#         return -1  # 불가능한 경우 -1 반환.
#     target = total // 2  # //는 정수 몫. 각 큐가 가져야 할 목표 합.
#     first, second = deque(queue1), deque(queue2)  # 목록을 deque로 변환해 각각 대입.
#     for moves in range(2 * (len(queue1) + len(queue2)) + 1):  # len은 길이, range는 반복 범위. 경계의 순환을 충분히 검사할 이동 상한 설정.
#         if current == target:  # ==는 같음. 합이 목표에 도착했는지 검사.
#             return moves  # 처음 도착한 이동 횟수가 최소.
#         if current > target:  # >는 큼. 첫 큐가 더 무거우면 앞 원소를 반대 큐로 이동.
#             value = first.popleft()  # popleft는 맨 앞 원소를 꺼내 삭제.
#             second.append(value)  # append로 둘째 큐 뒤에 추가.
#             current -= value  # -=는 빼서 저장. 첫 큐 합 갱신.
#         else:  # else는 첫 큐 합이 목표보다 작은 경우.
#             value = second.popleft()  # 둘째 큐 앞 원소 꺼내기.
#             first.append(value)  # 첫 큐 뒤에 넣기.
#             current += value  # +=는 더해 저장. 첫 큐 합 증가.
#     return -1  # 모든 필요한 순환 구간을 검사해도 같아지지 않으면 -1.

# 풀이 요약
# 합이 큰 큐의 앞 원소를 작은 큐로 옮깁니다. 양수이므로 목표보다 큰 구간은 앞을 줄이고 작으면 뒤를 늘리는 두 포인터와 같습니다.
# 예: 첫 예제는 3을 옮긴 뒤 4를 받아 2회. 같은 길이 N인 큐에서 시간·공간 O(N).
