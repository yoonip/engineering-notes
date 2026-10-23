# deque는 앞에서 꺼내기 빠른 선입선출 큐로 BFS에 사용.
from collections import deque

# 0은 빈칸, 1은 벽인 보드를 받음.
def solution(board):
    # len은 한 변의 길이.
    n = len(board)
    # 보드 바깥에 한 칸 두께의 벽을 둘러 범위 검사를 단순화.
    grid = [[1] * (n + 2) for _ in range(n + 2)]
    # 원래 보드의 행 순회.
    for row in range(n):
        # 테두리 안쪽에 보드 한 행 복사.
        grid[row + 1][1:n + 1] = board[row]
    # 로봇이 차지한 두 칸을 하나의 상태로 표현.
    start = ((1, 1), (1, 2))
    # (상태,걸린 시간)을 담은 BFS 큐 초기화.
    queue = deque([(start, 0)])
    # 이미 발견한 로봇 상태의 중복 방문 방지.
    visited = {start}
    # 큐가 비어 있지 않은 동안 너비 우선 탐색.
    while queue:
        # 가장 짧은 시간부터 처리.
        state, time = queue.popleft()
        # 두 좌표를 언패킹.
        first, second = state
        # 두 칸 중 하나라도 도착점이면 성공.
        if (n, n) in state:
            # 모든 이동 비용이 1이므로 처음 도착한 시간이 최소.
            return time
        # 첫 칸의 행·열 분리.
        r1, c1 = first
        # 둘째 칸의 행·열 분리.
        r2, c2 = second
        # 다음에 갈 수 있는 로봇 상태 목록.
        candidates = []
        # 상하좌우 평행 이동 변화량 순회.
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            # 두 도착 칸이 모두 비어 있어야 함.
            if grid[r1 + dr][c1 + dc] == 0 and grid[r2 + dr][c2 + dc] == 0:
                # 두 칸을 같은 방향으로 이동.
                candidates.append(((r1 + dr, c1 + dc), (r2 + dr, c2 + dc)))
        # 두 행이 같으면 가로 방향 로봇.
        if r1 == r2:
            # 위쪽·아래쪽으로 회전하는 경우.
            for dr in (-1, 1):
                # 회전 중 지나가는 2×2 영역의 나머지 두 칸이 모두 비어 있어야 함.
                if grid[r1 + dr][c1] == 0 and grid[r2 + dr][c2] == 0:
                    # 첫 칸을 축으로 회전.
                    candidates.append((first, (r1 + dr, c1)))
                    # 둘째 칸을 축으로 회전.
                    candidates.append((second, (r2 + dr, c2)))
        else:
            # 왼쪽·오른쪽 회전 확인.
            for dc in (-1, 1):
                # 회전 공간 두 칸 검사.
                if grid[r1][c1 + dc] == 0 and grid[r2][c2 + dc] == 0:
                    # 첫 칸을 축으로 회전.
                    candidates.append((first, (r1, c1 + dc)))
                    # 둘째 칸을 축으로 회전.
                    candidates.append((second, (r2, c2 + dc)))
        # 가능한 다음 상태를 순회.
        for candidate in candidates:
            # 두 칸 순서를 통일해 앞뒤가 바뀐 중복 제거.
            next_state = tuple(sorted(candidate))
            # 처음 보는 상태만 탐색.
            if next_state not in visited:
                # 큐에 넣을 때 방문 표시.
                visited.add(next_state)
                # 이동·회전 모두 1초 추가.
                queue.append((next_state, time + 1))
    # 문제에서는 도달 가능한 보드만 주어짐.
    return -1
