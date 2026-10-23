from itertools import permutations

def solution(A, B):
    return min(sum(a * b for a, b in zip(A, order)) for order in permutations(B))
