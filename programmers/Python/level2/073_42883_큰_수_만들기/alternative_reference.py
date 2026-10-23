def solution(number, k):
    keep = len(number) - k
    start = 0
    output = []
    for remaining in range(keep, 0, -1):
        stop = len(number) - remaining + 1
        best = max(range(start, stop), key=number.__getitem__)
        output.append(number[best])
        start = best + 1
    return ''.join(output)
