from collections import defaultdict
from itertools import product
from bisect import bisect_left

def solution(info, query):
    table = defaultdict(list)
    for record in info:
        parts = record.split()
        score = int(parts.pop())
        # 네 조건의 유지·무시 조합 16개를 미리 준비한다.
        for key in product(*[(value, '-') for value in parts]):
            table[key].append(score)
    for scores in table.values():
        scores.sort()
    answer = []
    for request in query:
        parts = request.replace(' and ', ' ').split()
        minimum = int(parts.pop())
        scores = table.get(tuple(parts), [])
        # 기준 이상 점수는 정렬된 목록의 뒤쪽 연속 구간이다.
        answer.append(len(scores) - bisect_left(scores, minimum))
    return answer
