def solution(maze):
    n, m = len(maze), len(maze[0])
    locations = {}
    neighbors = [[] for _ in range(n * m)]
    for r in range(n):
        for c in range(m):
            pos = r * m + c
            if maze[r][c] in (1, 2, 3, 4):
                locations[maze[r][c]] = pos
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < m and maze[nr][nc] != 5:
                    neighbors[pos].append(nr * m + nc)
    red_goal, blue_goal = locations[3], locations[4]
    red_distance = [abs(pos // m - red_goal // m) + abs(pos % m - red_goal % m) for pos in range(n * m)]
    blue_distance = [abs(pos // m - blue_goal // m) + abs(pos % m - blue_goal % m) for pos in range(n * m)]
    answer = n * m + 1
    seen = set()

    def dfs(red, blue, red_mask, blue_mask, turns):
        nonlocal answer
        if red == red_goal and blue == blue_goal:
            answer = min(answer, turns)
            return
        if turns + max(red_distance[red], blue_distance[blue]) >= answer:
            return
        state = (red, blue, red_mask, blue_mask)
        if state in seen:
            return
        seen.add(state)
        reds = [red] if red == red_goal else sorted((pos for pos in neighbors[red] if not red_mask & (1 << pos)), key=lambda pos: red_distance[pos])
        blues = [blue] if blue == blue_goal else sorted((pos for pos in neighbors[blue] if not blue_mask & (1 << pos)), key=lambda pos: blue_distance[pos])
        for next_red in reds:
            for next_blue in blues:
                if next_red == next_blue or next_red == blue and next_blue == red:
                    continue
                dfs(next_red, next_blue, red_mask | (1 << next_red), blue_mask | (1 << next_blue), turns + 1)

    red, blue = locations[1], locations[2]
    dfs(red, blue, 1 << red, 1 << blue, 0)
    return 0 if answer == n * m + 1 else answer

# 전체 코드 줄별 설명
# def solution(maze):  # def는 함수 정의. maze는 두 수레의 시작·도착·벽이 담긴 격자.
#     n, m = len(maze), len(maze[0])  # len은 길이. 행·열 수 언패킹.
#     locations = {}  # {}는 빈 딕셔너리. 표식 번호별 1차원 위치 저장.
#     neighbors = [[] for _ in range(n * m)]  # 리스트 내포로 각 칸의 통행 가능한 이웃 목록 생성.
#     for r in range(n):  # range는 끝 제외. 모든 행 순회.
#         for c in range(m):  # 모든 열 순회.
#             pos = r * m + c  # 2차원 좌표를 1차원 인덱스로 변환.
#             if maze[r][c] in (1, 2, 3, 4):  # in은 포함 검사. 시작·도착 표식이면 위치 기록.
#                 locations[maze[r][c]] = pos  # [키] 대입으로 표식의 위치 저장.
#             for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):  # () 튜플의 네 방향을 언패킹해 순회.
#                 nr, nc = r + dr, c + dc  # 이웃의 행·열 계산.
#                 if 0 <= nr < n and 0 <= nc < m and maze[nr][nc] != 5:  # and는 모두 참, !=는 다름. 경계 안의 벽이 아닌 칸만 허용.
#                     neighbors[pos].append(nr * m + nc)  # append는 이웃 위치 하나 추가.
#     red_goal, blue_goal = locations[3], locations[4]  # 빨강·파랑의 목적지 위치.
#     red_distance = [abs(pos // m - red_goal // m) + abs(pos % m - red_goal % m) for pos in range(n * m)]  # //는 몫, %는 나머지, abs는 절댓값. 벽을 무시한 맨해튼 거리 하한.
#     blue_distance = [abs(pos // m - blue_goal // m) + abs(pos % m - blue_goal % m) for pos in range(n * m)]  # 파란 수레도 목적지까지 필요한 최소 이동 횟수의 하한 계산.
#     answer = n * m + 1  # 자기 방문 칸을 다시 못 가므로 한 수레의 이동은 칸 수-1 이하. 그보다 큰 값은 아직 답 없음.
#     seen = set()  # set()은 빈 집합. 위치·각자 방문 기록이 모두 같은 상태의 중복 탐색 방지.
# 
#     def dfs(red, blue, red_mask, blue_mask, turns):  # 두 위치·두 방문 비트마스크·턴 수를 받는 깊이 우선 재귀 탐색.
#         nonlocal answer  # nonlocal은 바깥 solution의 answer를 재대입하겠다는 선언.
#         if red == red_goal and blue == blue_goal:  # ==는 같음. 두 수레 모두 목적지인지 검사.
#             answer = min(answer, turns)  # min은 작은 값. 최소 턴 수 갱신.
#             return  # return으로 현재 호출 종료.
#         if turns + max(red_distance[red], blue_distance[blue]) >= answer:  # max는 큰 값. 두 수레가 동시에 움직여도 이 하한보다 빠를 수 없으므로 개선 불가 가지 제거.
#             return  # 가지치기로 불필요한 탐색 중단.
#         state = (red, blue, red_mask, blue_mask)  # 불변 튜플로 미래 이동을 결정하는 상태 전체 묶음.
#         if state in seen:  # in은 집합 포함 검사. 이미 같은 상태를 충분히 탐색했는지 확인.
#             return  # 같은 위치여도 방문 기록이 다르면 다른 상태이므로 그 경우는 제외하지 않음.
#         seen.add(state)  # add로 방문 상태 추가.
#         reds = [red] if red == red_goal else sorted((pos for pos in neighbors[red] if not red_mask & (1 << pos)), key=lambda pos: red_distance[pos])  # 목적지면 제자리 고정. 아니면 자기 미방문 이웃을 목표에 가까운 순서로 정렬. lambda는 짧은 함수.
#         blues = [blue] if blue == blue_goal else sorted((pos for pos in neighbors[blue] if not blue_mask & (1 << pos)), key=lambda pos: blue_distance[pos])  # 파랑도 같은 규칙. not은 부정, &와 <<는 방문 비트 검사.
#         for next_red in reds:  # 빨간 수레의 다음 위치 후보 순회.
#             for next_blue in blues:  # 파란 수레 후보와 동시에 조합.
#                 if next_red == next_blue or next_red == blue and next_blue == red:  # or는 하나라도 참. 같은 칸 도착이나 서로 자리 교환을 금지.
#                     continue  # continue는 다음 이동 조합으로 진행.
#                 dfs(next_red, next_blue, red_mask | (1 << next_red), blue_mask | (1 << next_blue), turns + 1)  # |는 OR로 방문 칸 추가. 두 수레를 한 턴 동시에 이동.
# 
#     red, blue = locations[1], locations[2]  # 두 시작 위치 조회.
#     dfs(red, blue, 1 << red, 1 << blue, 0)  # 시작 칸을 각자 방문 처리하고 0턴부터 탐색.
#     return 0 if answer == n * m + 1 else answer  # 조건식으로 답 없음은 0, 가능하면 최소 턴 수 반환.

# 풀이 요약
# 한 턴에 두 수레의 이동을 동시에 골라 DFS로 탐색합니다. 방문 기록은 수레별로 분리하고, 같은 칸 도착·자리 교환을 금지하며 도착한 수레는 고정합니다.
# 위치뿐 아니라 두 방문 집합까지 같아야 같은 상태입니다. 맨해튼 거리 하한으로 현재 답보다 나아질 수 없는 가지를 제거합니다. 최악에는 가능한 방문 경로 조합을 탐색하는 지수 시간입니다.
# 예: 한 수레가 도착한 후에는 그 칸에서 기다리지만, 다른 수레는 그 칸을 지나갈 수 없습니다. 둘 모두 도착한 턴 수의 최솟값을 구합니다.
