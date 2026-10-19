# 같은 보드·위치 상태의 결과를 저장해 재계산 방지.
from functools import lru_cache

# board는 초기 발판, aloc·bloc은 두 플레이어의 시작 행·열.
def solution(board, aloc, bloc):
    # 행 수·열 수를 언패킹.
    n, m = len(board), len(board[0])
    # 발판이 있는 칸의 비트를 sum으로 합친 정수 집합.
    mask = sum(1 << (r * m + c) for r in range(n) for c in range(m) if board[r][c])
    # [] 리스트 내포로 칸별 이웃 목록 생성.
    neighbors = [[] for _ in range(n * m)]
    for r in range(n):
        for c in range(m):
            # () 튜플의 네 방향 변화량 언패킹.
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                # 이웃 행·열 계산.
                nr, nc = r + dr, c + dc
                # 격자 내부의 이웃만 저장.
                if 0 <= nr < n and 0 <= nc < m:
                    # append는 이웃의 1차원 위치 하나 추가.
                    neighbors[r * m + c].append(nr * m + nc)

    # None은 캐시 용량 제한 없음.
    @lru_cache(None)
    # 현재 차례 관점의 승리 가능 여부·남은 최적 이동 수를 구하는 재귀 미니맥스.
    def play(remaining, current, other):
        # 자기 발판이 사라졌으면 즉시 패배.
        if not remaining & (1 << current):
            # (패배, 추가 이동 0) 튜플 반환.
            return False, 0
        # 이기는 선택·지는 선택의 이동 횟수를 담을 두 빈 리스트.
        winning, losing = [], []
        # 현재 플레이어가 이동할 이웃 후보 순회.
        for target in neighbors[current]:
            # 그 칸에 발판이 없으면 이동 불가.
            if not remaining & (1 << target):
                # continue는 다음 이웃으로 진행.
                continue
            # 다음 차례에는 상대와 자신의 역할·위치를 바꿔 호출.
            other_wins, turns = play(remaining ^ (1 << current), other, target)
            # 다음 플레이어가 이기면 현재 선택은 자기 패배.
            if other_wins:
                # 이번 이동 한 번을 더한 종료 횟수 저장.
                losing.append(turns + 1)
            else:
                # 이기는 선택의 이동 수 저장.
                winning.append(turns + 1)
        # 이기는 선택이 하나라도 있는지 검사.
        if winning:
            # 이길 수 있으면 가장 빨리 끝냄.
            return True, min(winning)
        # 이동이 없으면 default=0.
        return False, max(losing, default=0)

    # A 위치를 1차원으로 변환.
    start_a = aloc[0] * m + aloc[1]
    # B 위치도 같은 방식으로 변환.
    start_b = bloc[0] * m + bloc[1]
    # 승패 결과의 두 번째 원소인 이동 수만 반환.
    return play(mask, start_a, start_b)[1]
