def solution(grid):
    # 행 수와 열 수를 두 변수로 나눠 받는 언패킹.
    n, m = len(grid), len(grid[0])
    original = [value for row in grid for value in row]
    # 탐색 중 설치할 선로를 별도로 저장.
    rails = original[:]
    size = n * m
    neighbors = []
    required = 0
    # 원소 순회.
    for pos, kind in enumerate(original):
        r, c = divmod(pos, m)
        # append는 이웃 튜플 하나를 추가.
        neighbors.append((pos + 1 if c + 1 < m else -1, pos + m if r + 1 < n else -1, pos - 1 if c else -1, pos - m if r else -1))
        if kind > 0:
            required |= 1 << pos
    # 선로별 연결 방향을 R=1,D=2,L=4,U=8 비트로 표현.
    ends = (0, 5, 10, 15, 12, 9, 3, 6)
    choices = [[] for _ in range(4)]
    # 기차가 현재 칸에 들어오는 이동 방향.
    for direction in range(4):
        entry = (direction + 2) % 4
        # 3번 교차 선로는 빈칸을 실제로 두 번 통과할 때만 확정.
        for kind in (1, 2, 4, 5, 6, 7):
            if ends[kind] & (1 << entry):
                # 들어온 쪽 비트를 지워 나갈 방향만 남김.
                exit_bit = ends[kind] ^ (1 << entry)
                choices[direction].append((kind, exit_bit.bit_length() - 1))
    # 가로 1, 세로 2, 완전히 사용한 칸은 3.
    visited = [0] * size
    visited[0] = 1

    def dfs(pos, direction, remaining, pending):
        # 경계 밖이나 장애물이면 불가능.
        if pos < 0 or original[pos] == -1:
            return 0
        axis = 1 << (direction % 2)
        # 현재 칸에 정해진 선로 종류.
        kind = rails[pos]
        used = visited[pos]
        if used:
            # 같은 축 재방문과 곡선 재방문을 금지.
            if used & axis or kind not in (1, 2, 3):
                return 0
            if kind != 3 and original[pos] != 0:
                return 0
            # 빈칸에서 설치한 직선을 두 축으로 통과하면 교차 선로로 확정.
            rails[pos] = 3
            visited[pos] = 3
            # ~는 비트 반전, &로 이 칸의 미완성 표시 제거.
            result = dfs(neighbors[pos][direction], direction, remaining, pending & ~(1 << pos))
            rails[pos] = kind
            visited[pos] = used
            return result
        remaining &= ~(1 << pos)
        if pos == size - 1:
            valid_entry = kind == 1 and direction == 0 or kind == 2 and direction == 1
            return int(valid_entry and remaining == 0 and pending == 0)
        visited[pos] = axis
        if kind == 3:
            result = dfs(neighbors[pos][direction], direction, remaining, pending | (1 << pos))
        else:
            result = 0
            for candidate, exit_direction in choices[direction]:
                if kind != 0 and kind != candidate:
                    continue
                rails[pos] = candidate
                visited[pos] = axis if candidate <= 2 else 3
                result += dfs(neighbors[pos][exit_direction], exit_direction, remaining, pending)
        rails[pos] = kind
        visited[pos] = 0
        return result

    return dfs(1, 0, required & ~1, 0)
