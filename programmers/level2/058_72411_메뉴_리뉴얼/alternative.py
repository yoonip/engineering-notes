from itertools import combinations

def solution(orders,course):
    order_sets=[set(order) for order in orders]
    answer=[]
    for size in course:
        candidates={''.join(c) for order in orders for c in combinations(sorted(order),size)}
        counts={candidate:sum(set(candidate)<=order for order in order_sets) for candidate in candidates}
        maximum=max(counts.values(),default=0)
        if maximum>=2: answer.extend(c for c,n in counts.items() if n==maximum)
    return sorted(answer)
