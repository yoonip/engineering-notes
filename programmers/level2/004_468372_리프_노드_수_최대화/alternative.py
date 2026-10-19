from functools import lru_cache

def solution(dist_limit, split_limit):
    if dist_limit > 10 or split_limit > 50:
        raise ValueError('작은 입력 검증용: 분배 노드 10개, 분배도 50 이하')
    @lru_cache(None)
    def search(product, available, remaining):
        best = 0
        for degree in (2, 3):
            if product * degree > split_limit:
                continue
            for chosen in range(1, min(available, remaining)+1):
                # 이 깊이에서 chosen개만 확장하고 나머지는 리프로 끝낸다.
                added = chosen * (degree-1)
                best = max(best, added + search(product*degree, chosen*degree, remaining-chosen))
        return best
    return 1 + search(1, 1, dist_limit)
