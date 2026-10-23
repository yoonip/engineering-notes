def solution(grid):
    n, m = len(grid), len(grid[0])
    original = [value for row in grid for value in row]
    rails = original[:]
    size = n * m
    neighbors = []
    required = 0
    for pos, kind in enumerate(original):
        r, c = divmod(pos, m)
        neighbors.append((pos + 1 if c + 1 < m else -1, pos + m if r + 1 < n else -1, pos - 1 if c else -1, pos - m if r else -1))
        if kind > 0:
            required |= 1 << pos
    ends = (0, 5, 10, 15, 12, 9, 3, 6)
    choices = [[] for _ in range(4)]
    for direction in range(4):
        entry = (direction + 2) % 4
        for kind in (1, 2, 4, 5, 6, 7):
            if ends[kind] & (1 << entry):
                exit_bit = ends[kind] ^ (1 << entry)
                choices[direction].append((kind, exit_bit.bit_length() - 1))
    visited = [0] * size
    visited[0] = 1

    def dfs(pos, direction, remaining, pending):
        if pos < 0 or original[pos] == -1:
            return 0
        axis = 1 << (direction % 2)
        kind = rails[pos]
        used = visited[pos]
        if used:
            if used & axis or kind not in (1, 2, 3):
                return 0
            if kind != 3 and original[pos] != 0:
                return 0
            rails[pos] = 3
            visited[pos] = 3
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

# 전체 코드 줄별 설명
# def solution(grid):  # def는 함수 정의. grid는 장애물·선로·빈칸이 담긴 2차원 리스트 입력.
#     n, m = len(grid), len(grid[0])  # len은 길이. 행 수와 열 수를 두 변수로 나눠 받는 언패킹.
#     original = [value for row in grid for value in row]  # 중첩 리스트 내포로 격자를 1차원 목록으로 펼침.
#     rails = original[:]  # [:]는 전체 슬라이스 복사. 탐색 중 설치할 선로를 별도로 저장.
#     size = n * m  # *는 곱셈. 전체 칸 수.
#     neighbors = []  # []는 빈 리스트. 각 칸에서 오른쪽·아래·왼쪽·위 이웃을 저장.
#     required = 0  # 반드시 지나야 하는 기존 선로 집합을 정수 비트마스크로 표시.
#     for pos, kind in enumerate(original):  # enumerate는 (인덱스, 값)을 제공. for는 원소 순회.
#         r, c = divmod(pos, m)  # divmod는 (몫, 나머지) 반환. 1차원 위치를 행·열로 변환.
#         neighbors.append((pos + 1 if c + 1 < m else -1, pos + m if r + 1 < n else -1, pos - 1 if c else -1, pos - m if r else -1))  # 조건식 a if 조건 else b로 경계 밖은 -1. append는 이웃 튜플 하나를 추가.
#         if kind > 0:  # if는 조건문. 양수는 원래 놓여 있던 선로.
#             required |= 1 << pos  # <<는 비트 이동, |=는 OR 후 저장. 해당 칸을 필수 집합에 추가.
#     ends = (0, 5, 10, 15, 12, 9, 3, 6)  # ()는 튜플. 선로별 연결 방향을 R=1,D=2,L=4,U=8 비트로 표현.
#     choices = [[] for _ in range(4)]  # 리스트 내포로 이동 방향별 가능한 일반 선로 목록 생성. _는 쓰지 않는 반복 변수.
#     for direction in range(4):  # range(4)는 0,1,2,3. 기차가 현재 칸에 들어오는 이동 방향.
#         entry = (direction + 2) % 4  # %는 나머지. 이동 방향의 반대쪽이 들어온 연결구.
#         for kind in (1, 2, 4, 5, 6, 7):  # 3번 교차 선로는 빈칸을 실제로 두 번 통과할 때만 확정.
#             if ends[kind] & (1 << entry):  # &는 비트 AND. 이 선로가 들어온 쪽과 연결되는지 검사.
#                 exit_bit = ends[kind] ^ (1 << entry)  # ^는 XOR. 들어온 쪽 비트를 지워 나갈 방향만 남김.
#                 choices[direction].append((kind, exit_bit.bit_length() - 1))  # bit_length는 필요한 이진 자릿수. 한 비트의 번호를 출구 방향으로 변환.
#     visited = [0] * size  # [0]*size는 방문 상태 초기화. 가로 1, 세로 2, 완전히 사용한 칸은 3.
#     visited[0] = 1  # 시작 선로는 가로 방향으로 이미 사용했다고 표시.
# 
#     def dfs(pos, direction, remaining, pending):  # dfs는 깊이 우선 재귀 탐색. 필수 미방문 집합과 미완성 교차 선로를 함께 전달.
#         if pos < 0 or original[pos] == -1:  # or는 하나라도 참. 경계 밖이나 장애물이면 불가능.
#             return 0  # return은 호출 종료. 이 경로의 배치 수 0 반환.
#         axis = 1 << (direction % 2)  # 짝수 방향은 가로 비트 1, 홀수 방향은 세로 비트 2.
#         kind = rails[pos]  # [pos]는 인덱스 접근. 현재 칸에 정해진 선로 종류.
#         used = visited[pos]  # 이 칸에서 이미 사용한 축을 읽음.
#         if used:  # 0 이외의 방문 상태는 조건에서 참.
#             if used & axis or kind not in (1, 2, 3):  # not in은 포함되지 않음. 같은 축 재방문과 곡선 재방문을 금지.
#                 return 0  # 재방문은 아직 쓰지 않은 교차 축으로만 가능.
#             if kind != 3 and original[pos] != 0:  # !=는 다름, and는 둘 다 참. 기존 직선 선로는 교차 선로로 바꿀 수 없음.
#                 return 0  # 변경할 수 없는 선로이므로 경로 제외.
#             rails[pos] = 3  # 빈칸에서 설치한 직선을 두 축으로 통과하면 교차 선로로 확정.
#             visited[pos] = 3  # 두 축을 모두 사용했으므로 더는 방문할 수 없음.
#             result = dfs(neighbors[pos][direction], direction, remaining, pending & ~(1 << pos))  # 교차에서는 직진. ~는 비트 반전, &로 이 칸의 미완성 표시 제거.
#             rails[pos] = kind  # 재귀가 끝나면 선로 종류를 복구하는 백트래킹.
#             visited[pos] = used  # 이전 방문 상태도 복구해 다음 후보가 같은 조건에서 시작하게 함.
#             return result  # 이 재방문에서 완성되는 배치 수 반환.
#         remaining &= ~(1 << pos)  # &=는 AND 후 저장. 이번에 방문한 칸을 필수 미방문 집합에서 제거.
#         if pos == size - 1:  # ==는 같음. 마지막 칸에 도착했는지 확인.
#             valid_entry = kind == 1 and direction == 0 or kind == 2 and direction == 1  # 마지막 가로 선로에는 오른쪽으로, 세로 선로에는 아래쪽으로 들어와야 함.
#             return int(valid_entry and remaining == 0 and pending == 0)  # int는 참·거짓을 1·0으로 변환. 모든 필수 선로와 교차 축이 완료되어야 한 가지.
#         visited[pos] = axis  # 처음 방문한 축 표시. 곡선은 아래에서 완전히 사용한 상태로 덮어씀.
#         if kind == 3:  # 이미 놓인 3번 선로는 두 축을 모두 연결해야 함.
#             result = dfs(neighbors[pos][direction], direction, remaining, pending | (1 << pos))  # |는 OR. 첫 축을 지나므로 다른 축 통과가 필요하다고 기록하고 직진.
#         else:  # else는 앞 조건이 거짓일 때 실행.
#             result = 0  # 이 칸에서 선택할 수 있는 배치들의 합 초기화.
#             for candidate, exit_direction in choices[direction]:  # 들어온 방향과 연결되는 선로 종류·출구를 순회.
#                 if kind != 0 and kind != candidate:  # 기존 선로가 있으면 그 종류와 같은 후보만 허용.
#                     continue  # continue는 이번 후보를 건너뛰고 다음 반복으로 진행.
#                 rails[pos] = candidate  # 빈칸 또는 기존 선로의 현재 후보를 저장.
#                 visited[pos] = axis if candidate <= 2 else 3  # 직선은 다른 축으로 재방문 가능. 곡선은 더 방문할 수 없음.
#                 result += dfs(neighbors[pos][exit_direction], exit_direction, remaining, pending)  # +=는 더해 저장. 출구 이웃부터 완성되는 배치 수를 합산.
#         rails[pos] = kind  # 현재 칸의 선로를 탐색 전 상태로 복구.
#         visited[pos] = 0  # 이번 방문 표시도 제거해 다른 경로를 탐색.
#         return result  # 현재 상태에서 가능한 배치 수 반환.
# 
#     return dfs(1, 0, required & ~1, 0)  # 시작점 오른쪽 칸에서 탐색. 시작점은 방문 완료, 미완성 교차 선로는 없음.

# 풀이 요약
# 기차가 실제로 움직이는 경로를 DFS로 만듭니다. 빈칸의 직선은 나중에 다른 축으로 다시 지날 때 교차 선로로 확정합니다.
# 기존 선로는 모두 지나야 하며, 기존 3번 선로는 두 축을 모두 사용해야 합니다. 같은 방향 재방문은 순환이므로 중단합니다.
# 예: [[1,7],[0,2]]는 오른쪽으로 간 뒤 아래로 도착하는 기존 경로 한 가지. 빈칸은 그대로 두므로 답 1입니다.
