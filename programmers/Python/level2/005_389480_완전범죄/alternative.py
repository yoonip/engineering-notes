def solution(info, n, m):
    states = {(0, 0)}
    for a, b in info:
        following = set()
        for ta, tb in states:
            if ta+a < n:
                following.add((ta+a, tb))
            if tb+b < m:
                following.add((ta, tb+b))
        states = following
    return min((a for a, b in states), default=-1)
