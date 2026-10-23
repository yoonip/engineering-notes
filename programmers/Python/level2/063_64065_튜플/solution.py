from collections import Counter
from re import findall

def solution(s):
    # 앞선 튜플 원소일수록 더 많은 집합에 등장한다.
    counts = Counter(findall(r'\d+', s))
    return [int(value) for value, count in counts.most_common()]
