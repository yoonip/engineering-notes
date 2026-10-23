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
        # 다음 시작 전까지 가장 최근에 멈춘 과제부터 이어 한다.
        while free > 0 and stack:
            old_name, remaining = stack.pop()
            if remaining <= free:
                free -= remaining
                answer.append(old_name)
            else:
                # 끝내지 못한 작업의 남은 시간을 보존한다.
                stack.append((old_name, remaining - free))
                free = 0
        stack.append((name, duration))
        previous = start
    # 새 과제가 더 없으면 최근 중단 순서로 모두 끝낸다.
    while stack:
        answer.append(stack.pop()[0])
    return answer
