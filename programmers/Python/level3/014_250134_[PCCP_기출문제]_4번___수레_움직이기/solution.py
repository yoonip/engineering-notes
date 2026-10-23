def solution(maze):
    # 행·열 수 언패킹.
    n, m = len(maze), len(maze[0])
    locations = {}
    # 리스트 내포로 각 칸의 통행 가능한 이웃 목록 생성.
    neighbors = [[] for _ in range(n * m)]
    for r in range(n):
        # 모든 열 순회.
        for c in range(m):
            pos = r * m + c
            # 시작·도착 표식이면 위치 기록.
            if maze[r][c] in (1, 2, 3, 4):
                locations[maze[r][c]] = pos
            # () 튜플의 네 방향을 언패킹해 순회.
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                # 경계 안의 벽이 아닌 칸만 허용.
                if 0 <= nr < n and 0 <= nc < m and maze[nr][nc] != 5:
                    neighbors[pos].append(nr * m + nc)
    # 빨강·파랑의 목적지 위치.
    red_goal, blue_goal = locations[3], locations[4]
    red_distance = [abs(pos // m - red_goal // m) + abs(pos % m - red_goal % m) for pos in range(n * m)]
    # 파란 수레도 목적지까지 필요한 최소 이동 횟수의 하한 계산.
    blue_distance = [abs(pos // m - blue_goal // m) + abs(pos % m - blue_goal % m) for pos in range(n * m)]
    answer = n * m + 1
    seen = set()

    def dfs(red, blue, red_mask, blue_mask, turns):
        # nonlocal은 바깥 solution의 answer를 재대입하겠다는 선언.
        nonlocal answer
        if red == red_goal and blue == blue_goal:
            # 최소 턴 수 갱신.
            answer = min(answer, turns)
            return
        if turns + max(red_distance[red], blue_distance[blue]) >= answer:
            return
        # 불변 튜플로 미래 이동을 결정하는 상태 전체 묶음.
        state = (red, blue, red_mask, blue_mask)
        if state in seen:
            return
        # add로 방문 상태 추가.
        seen.add(state)
        reds = [red] if red == red_goal else sorted((pos for pos in neighbors[red] if not red_mask & (1 << pos)), key=lambda pos: red_distance[pos])
        # not은 부정, &와 <<는 방문 비트 검사.
        blues = [blue] if blue == blue_goal else sorted((pos for pos in neighbors[blue] if not blue_mask & (1 << pos)), key=lambda pos: blue_distance[pos])
        for next_red in reds:
            # 파란 수레 후보와 동시에 조합.
            for next_blue in blues:
                if next_red == next_blue or next_red == blue and next_blue == red:
                    continue
                dfs(next_red, next_blue, red_mask | (1 << next_red), blue_mask | (1 << next_blue), turns + 1)

    red, blue = locations[1], locations[2]
    dfs(red, blue, 1 << red, 1 << blue, 0)
    return 0 if answer == n * m + 1 else answer
