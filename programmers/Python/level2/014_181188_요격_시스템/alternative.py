def solution(targets):
    end = None
    answer = 0
    for start, stop in sorted(targets):
        if end is None or start >= end:
            answer += 1
            end = stop
        else:
            end = min(end,stop)
    return answer
