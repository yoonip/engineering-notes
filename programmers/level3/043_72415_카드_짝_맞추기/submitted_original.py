from collections import deque
from functools import lru_cache

def solution(board, r, c):
    positions = {}
    for row in range(4):
        for col in range(4):
            card = board[row][col]
            if card:
                positions.setdefault(card, []).append(row * 4 + col)
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

    @lru_cache(None)
    def distances(mask, start):
        distance = [-1] * 16
        distance[start] = 0
        queue = deque([start])
        while queue:
            point = queue.popleft()
            row, col = divmod(point, 4)
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if 0 <= nr < 4 and 0 <= nc < 4:
                    target = nr * 4 + nc
                    if distance[target] == -1:
                        distance[target] = distance[point] + 1
                        queue.append(target)
                nr, nc = row, col
                while 0 <= nr + dr < 4 and 0 <= nc + dc < 4:
                    nr, nc = nr + dr, nc + dc
                    card = board[nr][nc]
                    if card and mask & (1 << card):
                        break
                target = nr * 4 + nc
                if distance[target] == -1:
                    distance[target] = distance[point] + 1
                    queue.append(target)
        return tuple(distance)

    @lru_cache(None)
    def solve(mask, cursor):
        if mask == 0:
            return 0
        best = float('inf')
        start_distance = distances(mask, cursor)
        for card, (first, second) in positions.items():
            if mask & (1 << card):
                remaining = mask ^ (1 << card)
                forward = start_distance[first] + distances(mask, first)[second] + 2 + solve(remaining, second)
                backward = start_distance[second] + distances(mask, second)[first] + 2 + solve(remaining, first)
                best = min(best, forward, backward)
        return best

    mask = sum(1 << card for card in positions)
    return solve(mask, r * 4 + c)

# 전체 코드 줄별 설명
# from collections import deque  # import는 도구 가져오기. deque는 양쪽 삽입·삭제가 빠른 큐. BFS에 사용.
# from functools import lru_cache  # lru_cache는 함수 인자별 결과를 저장해 중복 계산을 줄이는 도구.
# 
# def solution(board, r, c):  # def는 함수 정의. 보드와 시작 행·열을 받음.
#     positions = {}  # {}는 딕셔너리. 카드 번호별 두 위치를 저장.
#     for row in range(4):  # range(4)는 0~3. 행 순회.
#         for col in range(4):  # 열 순회.
#             card = board[row][col]  # 중첩 []로 해당 칸 카드 번호 조회.
#             if card:  # 0은 거짓, 다른 정수는 참. 카드가 있을 때만 처리.
#                 positions.setdefault(card, []).append(row * 4 + col)  # setdefault는 키가 없으면 기본값 생성. append로 1차원 위치 추가.
#     directions = ((1, 0), (-1, 0), (0, 1), (0, -1))  # ()는 튜플. 상하좌우 변화량.
# 
#     @lru_cache(None)  # @는 데코레이터. None은 캐시 크기 제한 없음. 같은 보드 상태·시작점의 BFS 재사용.
#     def distances(mask, start):  # mask는 남아 있는 카드 번호를 비트로 표시한 정수.
#         distance = [-1] * 16  # []는 리스트, *는 반복. -1은 아직 도달하지 않은 칸.
#         distance[start] = 0  # 시작점까지 이동 횟수는 0.
#         queue = deque([start])  # 선입선출 큐 생성. 먼저 발견한 칸부터 처리하는 너비 우선 탐색(BFS).
#         while queue:  # 큐에 원소가 있는 동안 반복.
#             point = queue.popleft()  # popleft는 맨 앞 원소를 꺼내 삭제.
#             row, col = divmod(point, 4)  # divmod는 몫·나머지 반환. 1차원 위치를 행·열로 복원.
#             for dr, dc in directions:  # 각 방향의 행·열 변화량을 언패킹.
#                 nr, nc = row + dr, col + dc  # 한 칸 이동 좌표.
#                 if 0 <= nr < 4 and 0 <= nc < 4:  # and는 모두 참. 보드 안인지 확인.
#                     target = nr * 4 + nc  # 이동 좌표를 1차원 번호로 변환.
#                     if distance[target] == -1:  # ==는 같음. 처음 발견한 경우에만 기록.
#                         distance[target] = distance[point] + 1  # 방향키 한 번의 비용 추가.
#                         queue.append(target)  # 나중에 주변을 탐색하도록 큐에 추가.
#                 nr, nc = row, col  # Ctrl 이동은 현재 칸에서 새로 시작.
#                 while 0 <= nr + dr < 4 and 0 <= nc + dc < 4:  # 다음 칸이 보드 안인 동안 같은 방향으로 이동.
#                     nr, nc = nr + dr, nc + dc  # 한 칸 전진.
#                     card = board[nr][nc]  # 도착 칸의 원래 카드 번호.
#                     if card and mask & (1 << card):  # <<는 비트 이동, &는 비트 AND. 아직 제거되지 않은 카드면 멈춤.
#                         break  # 가장 가까운 카드에 도착했으므로 while 종료. 카드가 없으면 경계까지 이동.
#                 target = nr * 4 + nc  # Ctrl 이동의 도착점.
#                 if distance[target] == -1:  # 처음 도달했다면 최단 거리 확정.
#                     distance[target] = distance[point] + 1  # Ctrl+방향키도 조작 한 번.
#                     queue.append(target)  # 큐 끝에 추가.
#         return tuple(distance)  # tuple은 변경할 수 없는 묶음. 모든 칸까지 최단 이동 횟수 반환.
# 
#     @lru_cache(None)  # 같은 남은 카드 상태·커서 위치에서의 최솟값을 저장하는 메모이제이션.
#     def solve(mask, cursor):  # 남은 카드를 모두 제거할 최소 추가 조작 수를 구하는 함수.
#         if mask == 0:  # 남은 카드가 없으면 종료.
#             return 0  # 추가 조작 없음.
#         best = float('inf')  # float('inf')는 무한대. 최솟값 비교의 초기값.
#         start_distance = distances(mask, cursor)  # 현재 상태에서 커서로부터의 BFS 거리.
#         for card, (first, second) in positions.items():  # items는 키·값 쌍 순회. 같은 카드의 두 위치를 언패킹.
#             if mask & (1 << card):  # 이 카드가 남아 있는 경우만 선택 후보로 사용.
#                 remaining = mask ^ (1 << card)  # ^는 비트 XOR. 켜진 해당 카드 비트를 꺼서 제거 상태 생성.
#                 forward = start_distance[first] + distances(mask, first)[second] + 2 + solve(remaining, second)  # 첫 카드→둘째 카드. 두 번째 Enter 전에는 두 카드 모두 이동을 막음. +2는 Enter 두 번.
#                 backward = start_distance[second] + distances(mask, second)[first] + 2 + solve(remaining, first)  # 두 카드 선택 순서를 반대로 한 경우도 계산.
#                 best = min(best, forward, backward)  # min은 최솟값. 카드 종류·선택 순서의 모든 경우 중 최소 보관.
#         return best  # 현재 상태의 최적 조작 수 반환.
# 
#     mask = sum(1 << card for card in positions)  # sum은 합계. 서로 다른 카드 종류의 비트를 켜서 최초 상태 생성.
#     return solve(mask, r * 4 + c)  # 시작 커서를 1차원 위치로 바꿔 최적값 반환.

# 풀이 요약
# 남은 카드 종류를 비트마스크로 표시하고, 다음에 없앨 카드 쌍과 두 장을 뒤집는 순서를 모두 비교한다.
# 각 상태의 이동 비용은 일반 이동·Ctrl 이동을 간선으로 한 BFS로 구한다. Enter 두 번 후에만 두 카드가 사라진다.
# 예제 첫 보드는 이동 8번+Enter 6번=14. 종류 K≤6, 보드 칸 수 V=16일 때 시간 O(2^K·V·(V+K)), 공간 O(2^K·V²).
# 