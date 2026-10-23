from bisect import insort

def solution(scoville, K):
    values = sorted(scoville)
    answer = 0
    while values[0] < K:
        if len(values) < 2:
            return -1
        first, second = values.pop(0), values.pop(0)
        insort(values, first + 2 * second)
        answer += 1
    return answer
