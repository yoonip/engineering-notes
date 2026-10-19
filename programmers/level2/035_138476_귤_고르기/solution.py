# 문제: 귤 고르기
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/138476
# 풀이: Counter로 크기별 개수를 센 뒤 많은 종류부터 고른다. 같은 종류 수에서 담을 수 있는 귤 수를 최대화하는 선택이다.
# 복잡도: 귤 N개·크기 U종류: 시간 O(N+U log U), 추가 공간 O(U).

from collections import Counter

def solution(k, tangerine):
    counts = sorted(Counter(tangerine).values(), reverse=True)
    for kinds, count in enumerate(counts, 1):
        k -= count
        if k <= 0:
            return kinds
