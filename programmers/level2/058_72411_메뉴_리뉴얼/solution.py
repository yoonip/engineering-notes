# 문제: 메뉴 리뉴얼
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/72411
# 풀이: 정렬한 주문에서 코스 길이별 조합을 만들고 Counter로 센다. 두 번 이상 등장한 공동 최다 조합을 모두 고른다.
# 복잡도: 생성 조합 T개·조합 최대 길이 K·주문 최대 길이 L·주문 N개·결과 A개: 시간 상한 O(NL log L+TK+AK log A), 추가 공간 O(NL+TK).

from collections import Counter
from itertools import combinations

def solution(orders, course):
    orders = [sorted(order) for order in orders]
    answer = []
    for size in course:
        counts = Counter()
        for order in orders:
            counts.update(combinations(order, size))
        highest = max(counts.values(), default=0)
        if highest >= 2:
            answer.extend(''.join(menu) for menu, count in counts.items() if count == highest)
    return sorted(answer)
