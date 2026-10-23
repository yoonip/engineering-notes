def solution(mats, park):
    rows = len(park)
    cols = len(park[0])

    for size in sorted(mats, reverse=True):
        for row in range(rows - size + 1):
            for col in range(cols - size + 1):
                possible = True

                for r in range(row, row + size):
                    for c in range(col, col + size):
                        if park[r][c] != "-1":
                            possible = False
                            break

                    if not possible:
                        break

                if possible:
                    return size

    return -1