from itertools import product

def solution(grid):
    rows, cols = len(grid), len(grid[0])
    original = [v for row in grid for v in row]
    empty = [i for i, v in enumerate(original) if v == 0]
    ports = (0, 5, 10, 15, 12, 9, 3, 6)
    moves = ((0, 1), (1, 0), (0, -1), (-1, 0))
    answer = 0
    for values in product(range(8), repeat=len(empty)):
        rails = original[:]
        for pos, kind in zip(empty, values):
            rails[pos] = kind
        seen, pos, direction = {0: 1}, 1, 0
        valid = False
        while 0 <= pos < rows * cols:
            kind = rails[pos]
            axis = 1 << (direction % 2)
            if kind <= 0 or seen.get(pos, 0) & axis:
                break
            entry = (direction + 2) % 4
            if not (ports[kind] >> entry & 1):
                break
            seen[pos] = seen.get(pos, 0) | axis
            if pos == rows * cols - 1:
                valid = True
                break
            outgoing = direction if kind == 3 else (ports[kind] ^ (1 << entry)).bit_length() - 1
            r, c = divmod(pos, cols)
            dr, dc = moves[outgoing]
            r, c = r + dr, c + dc
            if not (0 <= r < rows and 0 <= c < cols):
                break
            pos, direction = r * cols + c, outgoing
        if valid:
            for i, kind in enumerate(rails):
                if kind > 0 and (i not in seen or kind == 3 and seen[i] != 3):
                    valid = False
                    break
            answer += valid
    return answer
