from collections import deque
# lru_cache는 함수 인자별 결과를 저장해 중복 계산을 줄이는 도구.
from functools import lru_cache

# 보드와 시작 행·열을 받음.
def solution(board, r, c):
    # 카드 번호별 두 위치를 저장.
    positions = {}
    for row in range(4):
        for col in range(4):
            # 중첩 []로 해당 칸 카드 번호 조회.
            card = board[row][col]
            # 카드가 있을 때만 처리.
            if card:
                # append로 1차원 위치 추가.
                positions.setdefault(card, []).append(row * 4 + col)
    # 상하좌우 변화량.
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

    # 같은 남은 카드 상태·커서 위치에서의 최솟값을 저장하는 메모이제이션.
    @lru_cache(None)
    # mask는 남아 있는 카드 번호를 비트로 표시한 정수.
    def distances(mask, start):
        # -1은 아직 도달하지 않은 칸.
        distance = [-1] * 16
        # 시작점까지 이동 횟수는 0.
        distance[start] = 0
        # 먼저 발견한 칸부터 처리하는 너비 우선 탐색(BFS).
        queue = deque([start])
        # 큐에 원소가 있는 동안 반복.
        while queue:
            # popleft는 맨 앞 원소를 꺼내 삭제.
            point = queue.popleft()
            # 1차원 위치를 행·열로 복원.
            row, col = divmod(point, 4)
            # 각 방향의 행·열 변화량을 언패킹.
            for dr, dc in directions:
                # 한 칸 이동 좌표.
                nr, nc = row + dr, col + dc
                # 보드 안인지 확인.
                if 0 <= nr < 4 and 0 <= nc < 4:
                    # Ctrl 이동의 도착점.
                    target = nr * 4 + nc
                    # 처음 도달했다면 최단 거리 확정.
                    if distance[target] == -1:
                        # Ctrl+방향키도 조작 한 번.
                        distance[target] = distance[point] + 1
                        queue.append(target)
                # Ctrl 이동은 현재 칸에서 새로 시작.
                nr, nc = row, col
                # 다음 칸이 보드 안인 동안 같은 방향으로 이동.
                while 0 <= nr + dr < 4 and 0 <= nc + dc < 4:
                    nr, nc = nr + dr, nc + dc
                    # 도착 칸의 원래 카드 번호.
                    card = board[nr][nc]
                    # 아직 제거되지 않은 카드면 멈춤.
                    if card and mask & (1 << card):
                        break
                # Ctrl 이동의 도착점.
                target = nr * 4 + nc
                # 처음 도달했다면 최단 거리 확정.
                if distance[target] == -1:
                    # Ctrl+방향키도 조작 한 번.
                    distance[target] = distance[point] + 1
                    queue.append(target)
        # 모든 칸까지 최단 이동 횟수 반환.
        return tuple(distance)

    # 같은 남은 카드 상태·커서 위치에서의 최솟값을 저장하는 메모이제이션.
    @lru_cache(None)
    # 남은 카드를 모두 제거할 최소 추가 조작 수를 구하는 함수.
    def solve(mask, cursor):
        # 남은 카드가 없으면 종료.
        if mask == 0:
            # 추가 조작 없음.
            return 0
        # 최솟값 비교의 초기값.
        best = float('inf')
        # 현재 상태에서 커서로부터의 BFS 거리.
        start_distance = distances(mask, cursor)
        # 같은 카드의 두 위치를 언패킹.
        for card, (first, second) in positions.items():
            # 이 카드가 남아 있는 경우만 선택 후보로 사용.
            if mask & (1 << card):
                # 켜진 해당 카드 비트를 꺼서 제거 상태 생성.
                remaining = mask ^ (1 << card)
                # +2는 Enter 두 번.
                forward = start_distance[first] + distances(mask, first)[second] + 2 + solve(remaining, second)
                # 두 카드 선택 순서를 반대로 한 경우도 계산.
                backward = start_distance[second] + distances(mask, second)[first] + 2 + solve(remaining, first)
                # 카드 종류·선택 순서의 모든 경우 중 최소 보관.
                best = min(best, forward, backward)
        # 현재 상태의 최적 조작 수 반환.
        return best

    # 서로 다른 카드 종류의 비트를 켜서 최초 상태 생성.
    mask = sum(1 << card for card in positions)
    # 시작 커서를 1차원 위치로 바꿔 최적값 반환.
    return solve(mask, r * 4 + c)
