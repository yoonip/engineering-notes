from functools import lru_cache

def solution(coin, cards):
    n = len(cards)
    @lru_cache(None)
    def play(index, money, hand):
        if index == n:
            return 1
        best = 1
        drawn = cards[index:index + 2]
        for purchase in range(4):
            price = purchase.bit_count()
            if price > money:
                continue
            owned = set(hand)
            owned.update(drawn[i] for i in range(2) if purchase >> i & 1)
            for first in sorted(owned):
                second = n + 1 - first
                if first < second and second in owned:
                    rest = tuple(sorted(owned - {first, second}))
                    best = max(best, 1 + play(index + 2, money - price, rest))
        return best
    return play(n // 3, coin, tuple(sorted(cards[:n // 3])))
