# 문제: 과제 진행하기
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/176962
# 풀이: 시작 시각순으로 정렬하고 중단한 과제를 스택에 넣는다. 빈 시간이 생기면 가장 최근에 멈춘 과제부터 재개한다.
# 복잡도: 과제 N개: 시간 O(N log N), 추가 공간 O(N).

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
