from itertools import islice, permutations

def solution(n, k):
    return list(next(islice(permutations(range(1, n + 1)), k - 1, None)))
