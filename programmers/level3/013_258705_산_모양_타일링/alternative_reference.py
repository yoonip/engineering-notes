from functools import lru_cache

def solution(n, tops):
    # 아래쪽 지그재그 삼각형은 길이 2n+1의 경로를 이룬다.
    count = 2 * n + 1
    edges = [(i, i + 1) for i in range(count - 1)]
    for i, top in enumerate(tops):
        if top:
            edges.append((2 * i + 1, count))
            count += 1
    adjacent = [0] * count
    for a, b in edges:
        adjacent[a] |= 1 << b
        adjacent[b] |= 1 << a
    @lru_cache(None)
    def ways(mask):
        if not mask:
            return 1
        first = mask & -mask
        i = first.bit_length() - 1
        rest = mask ^ first
        result = ways(rest)
        neighbors = adjacent[i] & rest
        while neighbors:
            bit = neighbors & -neighbors
            neighbors ^= bit
            result += ways(rest ^ bit)
        return result % 10007
    return ways((1 << count) - 1)
