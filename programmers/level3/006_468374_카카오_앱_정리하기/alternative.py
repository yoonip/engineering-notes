def solution(board, commands):
    rows, cols = len(board), len(board[0])
    locations = {}
    for r, row in enumerate(board):
        for c, app in enumerate(row):
            if app:
                if app not in locations:
                    locations[app] = [r, c, 1]
                else:
                    locations[app][2] = max(locations[app][2], r - locations[app][0] + 1, c - locations[app][1] + 1)
    apps = [locations[i] for i in range(1, len(locations) + 1)]
    for selected, direction in commands:
        axis, reverse = direction % 2, direction >= 3
        side, length = 1 - axis, (rows, cols)[axis]
        pos = [length - a[2] - a[axis] if reverse else a[axis] for a in apps]
        constraints = []
        for i in range(len(apps)):
            for j in range(i):
                if max(apps[i][side], apps[j][side]) < min(apps[i][side] + apps[i][2], apps[j][side] + apps[j][2]):
                    first, second = (i, j) if pos[i] < pos[j] else (j, i)
                    constraints += [(first, second, apps[first][2]), (second, first, apps[second][2] - length)]
        def normalize(value, size):
            remainder = value % length
            return value + length - remainder if remainder > length - size else value
        i = selected - 1
        pos[i] = normalize(pos[i] + 1, apps[i][2])
        changed = True
        while changed:
            changed = False
            for source, target, gap in constraints:
                required = normalize(pos[source] + gap, apps[target][2])
                if required > pos[target]:
                    pos[target], changed = required, True
        for i, app in enumerate(apps):
            coordinate = pos[i] % length
            app[axis] = length - app[2] - coordinate if reverse else coordinate
    output = [[0] * cols for _ in range(rows)]
    for number, (r, c, size) in enumerate(apps, 1):
        for x in range(r, r + size):
            for y in range(c, c + size):
                output[x][y] = number
    return output
