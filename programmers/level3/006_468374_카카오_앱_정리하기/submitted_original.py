from collections import deque

def solution(board, commands):
    n, m = len(board), len(board[0])
    apps = {}
    for r, row in enumerate(board):
        for c, number in enumerate(row):
            if number:
                if number not in apps:
                    apps[number] = [r, c, 1]
                else:
                    apps[number][2] = max(apps[number][2], r - apps[number][0] + 1, c - apps[number][1] + 1)
    apps = [apps[number] for number in range(1, len(apps) + 1)]
    count = len(apps)
    for number, direction in commands:
        axis = direction % 2
        side = 1 - axis
        length = (n, m)[axis]
        reverse = direction >= 3
        positions = [length - app[2] - app[axis] if reverse else app[axis] for app in apps]
        graph = [[] for _ in apps]
        for i in range(count):
            for j in range(i):
                if apps[i][side] >= apps[j][side] + apps[j][2] or apps[j][side] >= apps[i][side] + apps[i][2]:
                    continue
                first, second = (i, j) if positions[i] < positions[j] else (j, i)
                graph[first].append((second, apps[first][2]))
                graph[second].append((first, apps[second][2] - length))

        def normalize(value, size):
            remainder = value % length
            if remainder > length - size:
                value += length - remainder
            return value

        number -= 1
        positions[number] = normalize(positions[number] + 1, apps[number][2])
        queue = deque([number])
        queued = [False] * count
        queued[number] = True
        while queue:
            current = queue.popleft()
            queued[current] = False
            for other, gap in graph[current]:
                needed = normalize(positions[current] + gap, apps[other][2])
                if needed > positions[other]:
                    positions[other] = needed
                    if not queued[other]:
                        queued[other] = True
                        queue.append(other)
        for i, app in enumerate(apps):
            coordinate = positions[i] % length
            app[axis] = length - app[2] - coordinate if reverse else coordinate
    answer = [[0] * m for _ in range(n)]
    for number, (r, c, size) in enumerate(apps, 1):
        for x in range(r, r + size):
            for y in range(c, c + size):
                answer[x][y] = number
    return answer

# 전체 코드 줄별 설명
# from collections import deque  # collections에서 deque를 import. 먼저 넣은 작업을 먼저 꺼내는 큐로 사용.
# 
# def solution(board, commands):  # def는 함수 정의. board는 앱 배치, commands는 앱 번호·방향 목록.
#     n, m = len(board), len(board[0])  # len은 길이. 행·열 수를 두 변수로 나눠 받음.
#     apps = {}  # {}는 빈 딕셔너리. 앱 ID에 [맨 위 행, 맨 왼쪽 열, 한 변 길이]를 대응.
#     for r, row in enumerate(board):  # enumerate는 (인덱스, 값)을 제공. 각 행과 행 번호 순회.
#         for c, number in enumerate(row):  # 각 칸의 열 번호와 앱 ID 순회.
#             if number:  # 0은 거짓이므로 빈칸을 제외.
#                 if number not in apps:  # not in은 키가 아직 없다는 뜻. 처음 발견한 칸이 왼쪽 위.
#                     apps[number] = [r, c, 1]  # [] 리스트로 위치와 초기 크기 저장.
#                 else:  # 이미 발견한 앱이면 현재 칸으로 크기 갱신.
#                     apps[number][2] = max(apps[number][2], r - apps[number][0] + 1, c - apps[number][1] + 1)  # max는 최댓값. 앱이 정사각형이므로 행·열 범위로 한 변 길이 계산.
#     apps = [apps[number] for number in range(1, len(apps) + 1)]  # 리스트 내포로 ID 순서 목록으로 변환. 앱 번호 -1이 인덱스.
#     count = len(apps)  # 전체 앱 수.
#     for number, direction in commands:  # for~in으로 명령 순회. 한 명령의 두 값을 언패킹.
#         axis = direction % 2  # %는 나머지. 좌우 방향은 열 인덱스 1, 상하 방향은 행 인덱스 0.
#         side = 1 - axis  # 움직이지 않는 수직 축의 인덱스.
#         length = (n, m)[axis]  # () 튜플에서 이동 축의 격자 길이 선택.
#         reverse = direction >= 3  # >=는 이상. 왼쪽·위쪽이면 좌표를 반전해 모두 증가 방향으로 계산.
#         positions = [length - app[2] - app[axis] if reverse else app[axis] for app in apps]  # a if 조건 else b는 조건식. 앱의 왼쪽 위를 진행 방향 기준 시작 좌표로 변환.
#         graph = [[] for _ in apps]  # 앱마다 밀림을 전달할 이웃과 최소 간격을 저장하는 인접 리스트 생성.
#         for i in range(count):  # range는 끝 제외. 앱 쌍의 첫 번호 순회.
#             for j in range(i):  # 이전 앱들과만 비교해 중복 쌍을 만들지 않음.
#                 if apps[i][side] >= apps[j][side] + apps[j][2] or apps[j][side] >= apps[i][side] + apps[i][2]:  # or는 하나라도 참. 수직 축에서 안 겹치면 서로 밀 수 없음.
#                     continue  # continue는 다음 앱 쌍으로 이동.
#                 first, second = (i, j) if positions[i] < positions[j] else (j, i)  # 증가 방향에서 뒤쪽·앞쪽 앱 순서로 번호 배치.
#                 graph[first].append((second, apps[first][2]))  # 앞 앱은 뒤 앱의 시작+크기 이상에 있어야 겹치지 않음. append는 연결 하나 추가.
#                 graph[second].append((first, apps[second][2] - length))  # 앞 앱이 반대편으로 넘어오면 뒤 앱의 다음 바퀴를 밀 수 있음. 한 바퀴 length를 빼서 같은 좌표계로 표현.
# 
#         def normalize(value, size):  # 격자 끝에 앱이 걸치는 좌표를 반대편 시작으로 넘기는 중첩 함수.
#             remainder = value % length  # 한 바퀴 이상 움직인 좌표에서 실제 격자 안 위치 계산.
#             if remainder > length - size:  # 앱 전체가 들어가지 않는 시작 위치인지 검사.
#                 value += length - remainder  # +=는 더해 저장. 다음 바퀴 0번 위치로 건너뜀.
#             return value  # 실제로 앱 전체가 들어갈 수 있는 좌표 반환.
# 
#         number -= 1  # -=는 빼서 저장. 1 기반 앱 ID를 0 기반 인덱스로 변환.
#         positions[number] = normalize(positions[number] + 1, apps[number][2])  # 명령 대상 앱을 한 칸 전진시키고 필요하면 반대편으로 넘김.
#         queue = deque([number])  # 이동량 증가를 이웃에게 전달할 앱을 큐에 넣음.
#         queued = [False] * count  # False는 거짓. 같은 앱을 큐에 중복 저장하지 않기 위한 표시.
#         queued[number] = True  # True는 참. 시작 앱이 큐에 있음을 표시.
#         while queue:  # while은 큐가 비지 않은 동안 반복.
#             current = queue.popleft()  # popleft는 가장 먼저 넣은 앱 번호를 제거·반환.
#             queued[current] = False  # 꺼낸 앱은 나중에 더 밀리면 다시 큐에 들어갈 수 있음.
#             for other, gap in graph[current]:  # 현재 앱과의 순서를 유지해야 하는 이웃·최소 간격 순회.
#                 needed = normalize(positions[current] + gap, apps[other][2])  # 현재 앱과 겹치지 않으려면 이웃이 도달해야 하는 최소 위치.
#                 if needed > positions[other]:  # 이웃이 더 앞으로 밀려야 하는 경우만 갱신.
#                     positions[other] = needed  # 겹침을 해소할 최소 좌표로 이동.
#                     if not queued[other]:  # not은 참·거짓 반전. 큐에 없는 앱만 새로 추가.
#                         queued[other] = True  # 큐 포함 표시.
#                         queue.append(other)  # 밀려난 앱이 다른 앱을 미는 효과도 전파.
#         for i, app in enumerate(apps):  # 모든 앱의 증가 방향 좌표를 원래 행·열로 복원.
#             coordinate = positions[i] % length  # 한 바퀴 이동 횟수를 제거해 실제 위치만 남김.
#             app[axis] = length - app[2] - coordinate if reverse else coordinate  # 반전했던 방향은 다시 뒤집고 이동 축의 좌표 갱신.
#     answer = [[0] * m for _ in range(n)]  # 리스트 내포로 서로 독립된 빈 격자 행 생성. _는 사용하지 않는 반복 변수.
#     for number, (r, c, size) in enumerate(apps, 1):  # enumerate(...,1)은 앱 번호를 1부터 붙여 최종 정보 순회.
#         for x in range(r, r + size):  # range는 끝 제외. 앱이 차지하는 행 순회.
#             for y in range(c, c + size):  # 앱이 차지하는 열 순회.
#                 answer[x][y] = number  # 해당 칸에 앱 ID 기록.
#     return answer  # 최종 2차원 배치를 반환.

# 풀이 요약
# 앱은 왼쪽 위 좌표와 한 변 길이로 관리합니다. 한 바퀴를 넘는 좌표를 그대로 유지해 앱 사이의 앞뒤 순서를 보존하고, 일부가 격자를 벗어나면 다음 바퀴의 시작으로 넘깁니다.
# 서로 밀 수 있는 앱 사이에 최소 간격 조건을 만들고, 더 밀려야 하는 앱의 좌표를 큐로 전파합니다. 반대편에서 돌아온 앱이 이전 앱을 다시 미는 효과도 같은 조건으로 처리합니다.
# 예: 2x2 앱이 세로 2칸 격자에서 위로 움직이면 시작 행은 계속 0입니다. 왼쪽 끝에서 왼쪽으로 밀면 시작 열이 가능한 최댓값으로 바뀝니다.
