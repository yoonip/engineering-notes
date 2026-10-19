# 문제: 순위 검색
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/72412
# 풀이: 지원자별 16개 조건 조합에 점수를 저장하고 정렬한다. 문의마다 bisect로 기준 점수의 경계를 찾아 전체 지원자 재탐색을 피한다.
# 복잡도: 지원자 N명·질의 Q개: 시간 O(16N log N+Q log N), 반환값 외 추가 공간 O(16N).

from collections import defaultdict
from itertools import product
from bisect import bisect_left

def solution(info, query):
    table = defaultdict(list)
    for record in info:
        parts = record.split()
        score = int(parts.pop())
        for key in product(*[(value, '-') for value in parts]):
            table[key].append(score)
    for scores in table.values():
        scores.sort()
    answer = []
    for request in query:
        parts = request.replace(' and ', ' ').split()
        minimum = int(parts.pop())
        scores = table.get(tuple(parts), [])
        answer.append(len(scores) - bisect_left(scores, minimum))
    return answer
