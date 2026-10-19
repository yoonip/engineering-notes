from collections import deque

def solution(board, commands):
    # 행·열 수를 두 변수로 나눠 받음.
    n, m = len(board), len(board[0])
    apps = {}
    for r, row in enumerate(board):
        # 각 칸의 열 번호와 앱 ID 순회.
        for c, number in enumerate(row):
            if number:
                if number not in apps:
                    # [] 리스트로 위치와 초기 크기 저장.
                    apps[number] = [r, c, 1]
                else:
                    apps[number][2] = max(apps[number][2], r - apps[number][0] + 1, c - apps[number][1] + 1)
    # 앱 번호 -1이 인덱스.
    apps = [apps[number] for number in range(1, len(apps) + 1)]
    count = len(apps)
    # 한 명령의 두 값을 언패킹.
    for number, direction in commands:
        axis = direction % 2
        # 움직이지 않는 수직 축의 인덱스.
        side = 1 - axis
        length = (n, m)[axis]
        # 왼쪽·위쪽이면 좌표를 반전해 모두 증가 방향으로 계산.
        reverse = direction >= 3
        positions = [length - app[2] - app[axis] if reverse else app[axis] for app in apps]
        # 앱마다 밀림을 전달할 이웃과 최소 간격을 저장하는 인접 리스트 생성.
        graph = [[] for _ in apps]
        for i in range(count):
            # 이전 앱들과만 비교해 중복 쌍을 만들지 않음.
            for j in range(i):
                if apps[i][side] >= apps[j][side] + apps[j][2] or apps[j][side] >= apps[i][side] + apps[i][2]:
                    continue
                # 증가 방향에서 뒤쪽·앞쪽 앱 순서로 번호 배치.
                first, second = (i, j) if positions[i] < positions[j] else (j, i)
                graph[first].append((second, apps[first][2]))
                # 한 바퀴 length를 빼서 같은 좌표계로 표현.
                graph[second].append((first, apps[second][2] - length))

        def normalize(value, size):
            remainder = value % length
            # 앱 전체가 들어가지 않는 시작 위치인지 검사.
            if remainder > length - size:
                value += length - remainder
            return value

        number -= 1
        # 명령 대상 앱을 한 칸 전진시키고 필요하면 반대편으로 넘김.
        positions[number] = normalize(positions[number] + 1, apps[number][2])
        queue = deque([number])
        # 같은 앱을 큐에 중복 저장하지 않기 위한 표시.
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
