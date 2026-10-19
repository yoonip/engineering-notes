from collections import Counter

def solution(points, routes):
    occupied = Counter()
    for route in routes:
        row, col = points[route[0]-1]
        time = 0
        occupied[(time,row,col)] += 1
        for point in route[1:]:
            r, c = points[point-1]
            while row != r or col != c:
                if row != r:
                    row += 1 if row < r else -1
                else:
                    col += 1 if col < c else -1
                time += 1
                occupied[(time,row,col)] += 1
    return sum(count >= 2 for count in occupied.values())
