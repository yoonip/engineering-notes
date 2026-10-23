def solution(citations):
    n = len(citations)
    counts = [0] * (n + 1)
    for value in citations:
        counts[min(value, n)] += 1
    papers = 0
    for h in range(n, -1, -1):
        papers += counts[h]
        if papers >= h:
            return h
