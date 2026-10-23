from bisect import bisect_left
from itertools import combinations, product

def solution(dice):
    n, best, answer = len(dice), -1, []
    for chosen in combinations(range(n), n // 2):
        other = [i for i in range(n) if i not in chosen]
        a = [sum(faces) for faces in product(*(dice[i] for i in chosen))]
        b = sorted(sum(faces) for faces in product(*(dice[i] for i in other)))
        wins = sum(bisect_left(b, value) for value in a)
        if wins > best:
            best, answer = wins, [i + 1 for i in chosen]
    return answer
