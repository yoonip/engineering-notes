from functools import lru_cache

def solution(storey):
    @lru_cache(None)
    def best(value):
        if value<10: return min(value,11-value)
        high,digit=divmod(value,10)
        return min(digit+best(high),10-digit+best(high+1))
    return best(storey)
