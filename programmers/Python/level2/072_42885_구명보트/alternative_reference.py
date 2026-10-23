from functools import lru_cache

def solution(people, limit):
    @lru_cache(None)
    def boats(mask):
        if not mask:
            return 0
        bit = mask & -mask
        i = bit.bit_length() - 1
        rest = mask ^ bit
        best = 1 + boats(rest)
        for j in range(i + 1, len(people)):
            if rest >> j & 1 and people[i] + people[j] <= limit:
                best = min(best, 1 + boats(rest ^ (1 << j)))
        return best
    return boats((1 << len(people)) - 1)
