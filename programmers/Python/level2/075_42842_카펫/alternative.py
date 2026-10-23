from math import isqrt

def solution(brown, yellow):
    total_side = (brown + 4) // 2
    difference = isqrt(total_side * total_side - 4 * (brown + yellow))
    return [(total_side + difference) // 2, (total_side - difference) // 2]
