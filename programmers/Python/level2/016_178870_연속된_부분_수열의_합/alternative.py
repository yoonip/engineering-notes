def solution(sequence,k):
    latest = {0:-1}
    prefix = 0
    answer = None
    for right,value in enumerate(sequence):
        prefix += value
        if prefix-k in latest:
            left = latest[prefix-k]+1
            key = (right-left,left,right)
            if answer is None or key < answer:
                answer = key
        latest[prefix] = right
    return [answer[1],answer[2]]
