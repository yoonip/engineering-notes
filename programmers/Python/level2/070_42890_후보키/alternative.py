def solution(relation):
    c = len(relation[0])
    unique = [False] * (1 << c)
    for mask in range(1, 1 << c):
        values = {tuple(row[j] for j in range(c) if mask >> j & 1) for row in relation}
        unique[mask] = len(values) == len(relation)
    return sum(unique[mask] and all(not unique[mask ^ (1 << j)] for j in range(c) if mask >> j & 1)
               for mask in range(1, 1 << c))
