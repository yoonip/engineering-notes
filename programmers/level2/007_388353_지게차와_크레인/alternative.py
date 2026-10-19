def solution(storage, requests):
    rows, cols = len(storage), len(storage[0])
    board = [list(row) for row in storage]
    for request in requests:
        outside = {(-1, c) for c in range(cols)} | {(rows, c) for c in range(cols)}
        outside |= {(r, -1) for r in range(rows)} | {(r, cols) for r in range(rows)}
        changed = True
        while changed:
            changed = False
            for r in range(rows):
                for c in range(cols):
                    if board[r][c] == '.' and (r,c) not in outside:
                        if any((r+dr,c+dc) in outside for dr,dc in ((1,0),(-1,0),(0,1),(0,-1))):
                            outside.add((r,c))
                            changed = True
        removed = []
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == request[0] and (len(request)==2 or any((r+dr,c+dc) in outside for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)))):
                    removed.append((r,c))
        for r,c in removed:
            board[r][c] = '.'
    return sum(cell != '.' for row in board for cell in row)
