from collections import Counter
from itertools import combinations
from functools import lru_cache

def solution(dice):
    # len은 주사위 개수.
    n = len(dice)

    @lru_cache(None)
    def distribution(indices):
        # 빈 튜플이면 주사위를 고르지 않은 상태.
        if not indices:
            return Counter({0: 1})
        previous = distribution(indices[:-1])
        # 캐시된 previous는 수정하지 않음.
        counts = Counter()
        for total, count in previous.items():
            # 마지막 주사위의 여섯 면을 순회.
            for face in dice[indices[-1]]:
                counts[total + face] += count
        return counts

    best = -1
    answer = []
    # A가 가져갈 절반의 모든 조합 순회.
    for selected in combinations(range(n), n // 2):
        other = tuple(i for i in range(n) if i not in selected)
        # A·B의 합별 경우의 수를 언패킹으로 저장.
        left, right = distribution(selected), distribution(other)
        cumulative = [0]
        # 면 최댓값 100·최대 5개이므로 합은 500 이하.
        for value in range(501):
            cumulative.append(cumulative[-1] + right[value])
        # A의 각 합 경우의 수 × 그보다 작은 B 합 경우의 수.
        wins = sum(count * cumulative[value] for value, count in left.items())
        if wins > best:
            best = wins
            # combinations 순서가 오름차순을 보장.
            answer = [i + 1 for i in selected]
    return answer
