from collections import Counter
from itertools import combinations

def solution(orders, course):
    orders = [sorted(order) for order in orders]
    answer = []
    for size in course:
        counts = Counter()
        for order in orders:
            # 주문마다 해당 크기 메뉴 조합의 빈도를 더한다.
            counts.update(combinations(order, size))
        highest = max(counts.values(), default=0)
        # 두 명 이상이 주문한 최빈 조합만 새 코스로 고른다.
        if highest >= 2:
            answer.extend(''.join(menu) for menu, count in counts.items() if count == highest)
    return sorted(answer)
