from collections import Counter

def solution(k, tangerine):
    # 많이 남은 크기부터 골라 종류 수를 줄인다.
    counts = sorted(Counter(tangerine).values(), reverse=True)
    for kinds, count in enumerate(counts, 1):
        k -= count
        if k <= 0:
            return kinds
