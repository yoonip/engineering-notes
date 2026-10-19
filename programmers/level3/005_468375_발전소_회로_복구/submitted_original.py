from collections import deque
from functools import lru_cache

def solution(h, grid, panels, seqs):
    n, m = len(grid), len(grid[0])
    k = len(panels)
    infinity = 10 ** 9
    elevator = next(r * m + c for r in range(n) for c in range(m) if grid[r][c] == '@')

    def bfs(start):
        distance = [infinity] * (n * m)
        distance[start] = 0
        queue = deque([start])
        while queue:
            pos = queue.popleft()
            r, c = divmod(pos, m)
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] != '#':
                    neighbor = nr * m + nc
                    if distance[neighbor] == infinity:
                        distance[neighbor] = distance[pos] + 1
                        queue.append(neighbor)
        return distance

    positions = [(r - 1) * m + c - 1 for _, r, c in panels]
    maps = [bfs(pos) for pos in positions]
    travel = [[0] * k for _ in range(k)]
    for i in range(k):
        for j in range(k):
            if panels[i][0] == panels[j][0]:
                travel[i][j] = maps[i][positions[j]]
            else:
                travel[i][j] = maps[i][elevator] + abs(panels[i][0] - panels[j][0]) + maps[j][elevator]
    required = [0] * k
    for a, b in seqs:
        required[b - 1] |= 1 << (a - 1)
    full = (1 << k) - 1

    @lru_cache(None)
    def dfs(mask, current):
        if mask == full:
            return 0
        answer = infinity
        for target in range(k):
            bit = 1 << target
            if mask & bit or required[target] & mask != required[target]:
                continue
            answer = min(answer, travel[current][target] + dfs(mask | bit, target))
        return answer

    return dfs(1 if required[0] == 0 else 0, 0)

# 전체 코드 줄별 설명
# from collections import deque  # collections에서 deque를 import. 양끝 삽입·삭제가 빠른 덱이며 BFS의 선입선출 큐로 사용.
# from functools import lru_cache  # functools의 lru_cache는 같은 인수의 함수 결과를 저장하는 메모이제이션 도구.
# 
# def solution(h, grid, panels, seqs):  # def는 함수 정의. h는 층 수, grid는 공통 평면도, panels는 위치, seqs는 선행 조건.
#     n, m = len(grid), len(grid[0])  # len은 길이. 행·열 수를 언패킹으로 나눠 받음.
#     k = len(panels)  # 회로 패널 수.
#     infinity = 10 ** 9  # **는 거듭제곱. 도달 불가능 거리를 나타낼 충분히 큰 값.
#     elevator = next(r * m + c for r in range(n) for c in range(m) if grid[r][c] == '@')  # 생성식으로 엘리베이터 칸을 찾고 next로 첫 값을 꺼냄. r*m+c는 1차원 위치.
# 
#     def bfs(start):  # 한 층에서 start부터 모든 칸까지 최단 이동 거리를 구하는 중첩 함수.
#         distance = [infinity] * (n * m)  # []는 리스트, *는 반복 초기화. 각 칸을 아직 미도달 상태로 설정.
#         distance[start] = 0  # 시작 칸까지 거리는 0.
#         queue = deque([start])  # []에 시작 위치를 담아 deque 큐 생성.
#         while queue:  # while은 반복. 빈 큐는 거짓이므로 모든 후보 처리 후 종료.
#             pos = queue.popleft()  # popleft는 먼저 넣은 위치를 맨 앞에서 제거·반환.
#             r, c = divmod(pos, m)  # divmod는 (몫, 나머지). 위치를 행·열로 복원.
#             for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):  # 튜플의 네 방향을 순회하며 행·열 변화량을 언패킹.
#                 nr, nc = r + dr, c + dc  # 이웃 칸의 좌표 계산.
#                 if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] != '#':  # and는 모두 참. 경계 안이며 폐쇄 구역이 아닌지 검사.
#                     neighbor = nr * m + nc  # 이웃의 1차원 위치 계산.
#                     if distance[neighbor] == infinity:  # ==는 같음. 아직 방문하지 않은 칸만 처리.
#                         distance[neighbor] = distance[pos] + 1  # BFS는 가까운 순서이므로 첫 방문이 최단 거리.
#                         queue.append(neighbor)  # append로 큐 맨 뒤에 이웃 추가.
#         return distance  # return은 모든 칸까지의 거리 목록 반환.
# 
#     positions = [(r - 1) * m + c - 1 for _, r, c in panels]  # 리스트 내포. 1부터 세는 행·열을 0 기반 위치로 변환, _는 여기서 안 쓰는 층.
#     maps = [bfs(pos) for pos in positions]  # 각 패널의 평면 위치에서 BFS를 한 번씩 실행.
#     travel = [[0] * k for _ in range(k)]  # 서로 독립인 행들로 패널 간 거리 표 생성.
#     for i in range(k):  # range(k)는 0부터 k-1까지. 출발 패널 순회.
#         for j in range(k):  # 도착 패널 순회.
#             if panels[i][0] == panels[j][0]:  # 두 패널의 층이 같으면 평면 최단 거리 사용.
#                 travel[i][j] = maps[i][positions[j]]  # i 위치에서 j 위치까지 BFS 거리.
#             else:  # else는 층이 다른 경우.
#                 travel[i][j] = maps[i][elevator] + abs(panels[i][0] - panels[j][0]) + maps[j][elevator]  # abs는 절댓값. 엘리베이터까지+층 이동+목적 패널까지의 거리.
#     required = [0] * k  # 패널별 선행 패널 집합을 정수 비트마스크로 저장.
#     for a, b in seqs:  # 안전 순서 쌍을 순회.
#         required[b - 1] |= 1 << (a - 1)  # <<는 비트 이동, |=는 OR 후 저장. b를 켜기 전에 필요한 a를 표시.
#     full = (1 << k) - 1  # k개 비트가 모두 1인 전체 활성화 상태.
# 
#     @lru_cache(None)  # @는 데코레이터 적용. None은 캐시 개수 제한을 두지 않음.
#     def dfs(mask, current):  # 활성화 집합 mask와 현재 패널 번호에서 남은 최소 시간을 구하는 재귀 DP.
#         if mask == full:  # 모든 패널이 켜졌는지 확인하는 종료 조건.
#             return 0  # 더 필요한 시간은 0.
#         answer = infinity  # 남은 최소 시간의 초기값.
#         for target in range(k):  # 다음에 활성화할 패널 후보를 모두 순회.
#             bit = 1 << target  # target 패널만 나타내는 비트.
#             if mask & bit or required[target] & mask != required[target]:  # &는 비트 AND, or는 하나라도 참. 이미 켰거나 선행 패널이 부족하면 제외.
#                 continue  # continue는 다음 후보로 이동.
#             answer = min(answer, travel[current][target] + dfs(mask | bit, target))  # min은 작은 값, |는 집합에 비트 추가. 이동 시간+이후 최소 시간 비교.
#         return answer  # 이 상태에서 남은 최소 시간 반환. 캐시에 저장되어 같은 상태를 재계산하지 않음.
# 
#     return dfs(1 if required[0] == 0 else 0, 0)  # 시작은 1번 패널 위치. 선행 조건이 없으면 즉시 켜고, 있으면 미활성화 상태로 출발.

# 풀이 요약
# 각 층의 구조가 같으므로 패널 위치에서 평면 BFS를 수행하고, 다른 층 사이는 엘리베이터 왕복 거리와 층 차이를 더합니다.
# 이후 (켜진 패널 집합, 현재 패널)의 비트마스크 DP로 선행 조건을 만족하는 다음 패널을 선택합니다. 시간 O(KNM+K²2^K), 공간 O(KNM+K2^K).
# 예: 1번 패널의 선행 조건이 4번이면 출발 위치에 있어도 켜지 않습니다. 4번을 먼저 방문한 후 돌아와 켤 수 있습니다.
