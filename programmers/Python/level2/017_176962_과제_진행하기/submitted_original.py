def solution(plans):
    tasks = []
    for name, start, duration in plans:
        hour, minute = map(int, start.split(':'))
        tasks.append((hour * 60 + minute, name, int(duration)))
    tasks.sort()
    stack = []
    answer = []
    previous = 0
    for start, name, duration in tasks:
        free = start - previous
        while free > 0 and stack:
            old_name, remaining = stack.pop()
            if remaining <= free:
                free -= remaining
                answer.append(old_name)
            else:
                stack.append((old_name, remaining - free))
                free = 0
        stack.append((name, duration))
        previous = start
    while stack:
        answer.append(stack.pop()[0])
    return answer

# 전체 코드 줄별 설명
# def solution(plans):  # def는 함수 정의, plans는 과제 계획 입력. : 아래 들여쓰기가 본문.
#     tasks = []  # []는 빈 리스트. 시작 시각을 숫자로 바꾼 과제 저장.
#     for name, start, duration in plans:  # for~in으로 각 계획의 세 값을 변수로 언패킹.
#         hour, minute = map(int, start.split(':'))  # split은 문자열 나누기, map은 각 조각에 int를 적용해 정수 변환.
#         tasks.append((hour * 60 + minute, name, int(duration)))  # append는 끝에 추가, ()는 튜플. 시각·이름·소요 시간을 묶음.
#     tasks.sort()  # sort()는 리스트 제자리 정렬. 튜플의 첫 값인 시작 시각부터 비교.
#     stack = []  # 가장 최근에 멈춘 과제를 먼저 꺼내는 스택을 리스트로 구현.
#     answer = []  # 과제 완료 순서를 담는 리스트 초기화.
#     previous = 0  # =는 대입. 이전 시작 시각을 저장.
#     for start, name, duration in tasks:  # 시간 순 과제를 세 변수로 풀어 받아 순회.
#         free = start - previous  # 다음 과제가 시작되기 전까지 쓸 수 있는 시간 계산.
#         while free > 0 and stack:  # while은 반복, and는 둘 다 참. 남은 시간과 대기 과제가 있을 때 진행.
#             old_name, remaining = stack.pop()  # pop()으로 가장 최근 과제를 꺼내 삭제하고 두 값으로 언패킹.
#             if remaining <= free:  # if는 조건 분기, <=는 이하. 다음 시작 전에 완료 가능한지 검사.
#                 free -= remaining  # -=는 빼서 저장. 사용한 시간 차감.
#                 answer.append(old_name)  # 끝낸 과제 이름을 완료 목록에 추가.
#             else:  # else는 앞 조건이 거짓인 경우.
#                 stack.append((old_name, remaining - free))  # 남은 시간을 줄인 과제를 다시 스택에 저장.
#                 free = 0  # 여유 시간을 다 사용했으므로 반복 종료 준비.
#         stack.append((name, duration))  # 새 과제가 이전 과제보다 먼저 진행되도록 마지막에 추가.
#         previous = start  # 현재 시작 시각을 다음 반복의 기준으로 갱신.
#     while stack:  # 새 과제가 더 없으므로 스택이 빌 때까지 완료.
#         answer.append(stack.pop()[0])  # pop()으로 최근 과제를 꺼내 [0]의 이름만 완료 목록에 추가.
#     return answer  # return으로 완료 순서 리스트 반환.

# 풀이 요약
# 시작 시각 순으로 정렬하고, 다음 시작까지의 시간에 스택 위 과제를 처리합니다. 새 과제는 스택 위에 올립니다.
# 예: aaa를 멈추고 bbb를 끝낸 뒤 ccc, aaa 순으로 완료합니다. 시간 O(N log N), 공간 O(N).
