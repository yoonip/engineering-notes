from functools import lru_cache

def solution(board, aloc, bloc):
    n, m = len(board), len(board[0])
    mask = sum(1 << (r * m + c) for r in range(n) for c in range(m) if board[r][c])
    neighbors = [[] for _ in range(n * m)]
    for r in range(n):
        for c in range(m):
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < m:
                    neighbors[r * m + c].append(nr * m + nc)

    @lru_cache(None)
    def play(remaining, current, other):
        if not remaining & (1 << current):
            return False, 0
        winning, losing = [], []
        for target in neighbors[current]:
            if not remaining & (1 << target):
                continue
            other_wins, turns = play(remaining ^ (1 << current), other, target)
            if other_wins:
                losing.append(turns + 1)
            else:
                winning.append(turns + 1)
        if winning:
            return True, min(winning)
        return False, max(losing, default=0)

    start_a = aloc[0] * m + aloc[1]
    start_b = bloc[0] * m + bloc[1]
    return play(mask, start_a, start_b)[1]

# 전체 코드 줄별 설명
# from functools import lru_cache  # functools의 lru_cache를 import. 같은 보드·위치 상태의 결과를 저장해 재계산 방지.
# 
# def solution(board, aloc, bloc):  # def는 함수 정의. board는 초기 발판, aloc·bloc은 두 플레이어의 시작 행·열.
#     n, m = len(board), len(board[0])  # len은 길이. 행 수·열 수를 언패킹.
#     mask = sum(1 << (r * m + c) for r in range(n) for c in range(m) if board[r][c])  # <<는 비트 이동. 발판이 있는 칸의 비트를 sum으로 합친 정수 집합.
#     neighbors = [[] for _ in range(n * m)]  # [] 리스트 내포로 칸별 이웃 목록 생성.
#     for r in range(n):  # range는 끝 제외. 모든 행 순회.
#         for c in range(m):  # 모든 열 순회.
#             for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):  # () 튜플의 네 방향 변화량 언패킹.
#                 nr, nc = r + dr, c + dc  # 이웃 행·열 계산.
#                 if 0 <= nr < n and 0 <= nc < m:  # if는 조건문, and는 모두 참. 격자 내부의 이웃만 저장.
#                     neighbors[r * m + c].append(nr * m + nc)  # append는 이웃의 1차원 위치 하나 추가.
# 
#     @lru_cache(None)  # @는 데코레이터 적용. None은 캐시 용량 제한 없음.
#     def play(remaining, current, other):  # 현재 차례 관점의 승리 가능 여부·남은 최적 이동 수를 구하는 재귀 미니맥스.
#         if not remaining & (1 << current):  # &는 비트 AND, not은 부정. 자기 발판이 사라졌으면 즉시 패배.
#             return False, 0  # False는 거짓. (패배, 추가 이동 0) 튜플 반환.
#         winning, losing = [], []  # 이기는 선택·지는 선택의 이동 횟수를 담을 두 빈 리스트.
#         for target in neighbors[current]:  # 현재 플레이어가 이동할 이웃 후보 순회.
#             if not remaining & (1 << target):  # 그 칸에 발판이 없으면 이동 불가.
#                 continue  # continue는 다음 이웃으로 진행.
#             other_wins, turns = play(remaining ^ (1 << current), other, target)  # ^는 XOR로 현재 발판 제거. 다음 차례에는 상대와 자신의 역할·위치를 바꿔 호출.
#             if other_wins:  # 다음 플레이어가 이기면 현재 선택은 자기 패배.
#                 losing.append(turns + 1)  # 이번 이동 한 번을 더한 종료 횟수 저장.
#             else:  # else는 상대가 지므로 자신이 이기는 선택.
#                 winning.append(turns + 1)  # 이기는 선택의 이동 수 저장.
#         if winning:  # 빈 리스트는 거짓. 이기는 선택이 하나라도 있는지 검사.
#             return True, min(winning)  # True는 참, min은 최소. 이길 수 있으면 가장 빨리 끝냄.
#         return False, max(losing, default=0)  # max는 최대. 질 수밖에 없으면 가장 오래 버팀. 이동이 없으면 default=0.
# 
#     start_a = aloc[0] * m + aloc[1]  # [0]·[1]은 행·열. A 위치를 1차원으로 변환.
#     start_b = bloc[0] * m + bloc[1]  # B 위치도 같은 방식으로 변환.
#     return play(mask, start_a, start_b)[1]  # 처음은 A 차례. 승패 결과의 두 번째 원소인 이동 수만 반환.

# 풀이 요약
# 미니맥스는 상대도 최적으로 움직인다고 보고 자신의 최선의 선택을 구하는 게임 탐색입니다. 현재 플레이어 기준으로 이기면 최소 이동, 반드시 지면 최대 이동을 택합니다.
# 이동할 때 발판 하나를 지우고 플레이어 역할을 바꿉니다. 보드 비트마스크·두 위치를 캐시 키로 써 같은 게임 상태를 재사용합니다. 시간·공간은 도달 가능한 상태 수에 비례하며 최악에는 지수적입니다.
# 예: 두 플레이어가 같은 칸에 있을 때 한 명이 떠나면 그 칸이 사라져 다음 플레이어가 즉시 집니다. 시작부터 이동할 곳이 없으면 이동 횟수는 0입니다.
# 