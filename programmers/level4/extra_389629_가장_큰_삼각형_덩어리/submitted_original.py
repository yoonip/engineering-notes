def solution(grid):
    n, m = len(grid), len(grid[0])
    count = n * m
    graph = [[] for _ in range(2 * count)]
    def connect(a, b):
        graph[a].append(b)
        graph[b].append(a)
    for r in range(n):
        for c in range(m):
            base = 2 * (r * m + c)
            if r + 1 < n:
                connect(base + 1, base + 2 * m)
            if c + 1 < m:
                right = base + (grid[r][c] == 1)
                left = base + 2 + (grid[r][c + 1] == -1)
                connect(right, left)
    seen = bytearray(2 * count)
    answer = 1
    def inspect(start):
        nonlocal answer
        order = []
        previous, current = -1, start
        while not seen[current]:
            seen[current] = 1
            order.append(current // 2)
            next_node = -1
            for neighbor in graph[current]:
                if neighbor != previous:
                    next_node = neighbor
                    break
            if next_node == -1:
                break
            previous, current = current, next_node
        is_cycle = current == start and len(graph[start]) == 2
        length = len(order)
        sequence = order + order if is_cycle else order
        last = {}
        left = 0
        for right, cell in enumerate(sequence):
            left = max(left, last.get(cell, -1) + 1, right - length + 1)
            last[cell] = right
            answer = max(answer, right - left + 1)
    for node in range(2 * count):
        if not seen[node] and len(graph[node]) < 2:
            inspect(node)
    for node in range(2 * count):
        if not seen[node]:
            inspect(node)
    return answer

# 전체 코드 줄별 설명
# def solution(grid):  # def는 함수 정의. grid는 대각선 방향을 담은 2차원 리스트.
#     n, m = len(grid), len(grid[0])  # len은 길이. 행 수와 열 수를 구함.
#     count = n * m  # *는 곱셈. 정사각형 칸의 전체 개수.
#     graph = [[] for _ in range(2 * count)]  # 리스트 내포로 삼각형마다 빈 이웃 목록을 생성. 한 칸에 위·아래 삼각형 두 개.
#     def connect(a, b):  # 연결을 추가하는 내부 함수. a,b는 삼각형 번호.
#         graph[a].append(b)  # append는 리스트 끝에 원소 추가. a에서 b로 연결.
#         graph[b].append(a)  # 양쪽에서 이동할 수 있으므로 반대 방향도 추가.
#     for r in range(n):  # range(n)은 0부터 n-1까지. 각 행을 순회.
#         for c in range(m):  # 각 열을 순회하여 모든 칸 확인.
#             base = 2 * (r * m + c)  # 칸 번호를 두 배하여 위 삼각형 번호 계산. 아래 삼각형은 base+1.
#             if r + 1 < n:  # if는 조건문. 아래에 다른 행이 있는지 확인.
#                 connect(base + 1, base + 2 * m)  # 현재 칸의 아래 삼각형과 아래 칸의 위 삼각형을 연결.
#             if c + 1 < m:  # 오른쪽 칸이 있으면 실행.
#                 right = base + (grid[r][c] == 1)  # 비교 결과 True는 계산에서 1. /이면 아래, 역슬래시이면 위 삼각형이 오른쪽 변을 가짐.
#                 left = base + 2 + (grid[r][c + 1] == -1)  # 오른쪽 칸에서 왼쪽 변을 가진 삼각형 번호 계산.
#                 connect(right, left)  # 공유하는 변을 가진 두 삼각형을 연결.
#     seen = bytearray(2 * count)  # bytearray는 0~255 정수 배열. 방문 여부를 적은 메모리로 저장.
#     answer = 1  # 칸이 최소 하나 있으므로 가능한 최소 덩어리 넓이는 1.
#     def inspect(start):  # 하나의 경로 또는 고리 성분을 검사하는 내부 함수.
#         nonlocal answer  # nonlocal은 바깥 solution의 answer를 이 함수에서 갱신하도록 지정.
#         order = []  # []는 빈 리스트. 연결된 삼각형의 칸 번호 순서를 담음.
#         previous, current = -1, start  # 이전 삼각형은 아직 없으므로 -1. 현재 삼각형은 시작점.
#         while not seen[current]:  # while은 반복. not은 부정이며 방문하지 않은 동안 이동.
#             seen[current] = 1  # 현재 삼각형을 방문 처리.
#             order.append(current // 2)  # //는 정수 나눗셈. 삼각형 번호를 칸 번호로 바꾸어 저장.
#             next_node = -1  # 다음 삼각형이 없다는 표시로 초기화.
#             for neighbor in graph[current]:  # 현재 삼각형의 최대 두 이웃을 순회.
#                 if neighbor != previous:  # !=는 다름 비교. 방금 지나온 삼각형은 제외.
#                     next_node = neighbor  # 앞으로 이동할 삼각형을 저장.
#                     break  # break는 가장 가까운 for 반복을 종료.
#             if next_node == -1:  # 더 이동할 삼각형이 없으면 경로 끝.
#                 break  # while 반복을 종료.
#             previous, current = current, next_node  # 동시 대입으로 이전·현재 삼각형 갱신.
#         is_cycle = current == start and len(graph[start]) == 2  # 시작으로 돌아왔고 양쪽이 연결되어 있으면 고리.
#         length = len(order)  # 성분의 삼각형 개수를 저장.
#         sequence = order + order if is_cycle else order  # 조건 표현식. 고리는 경계에 걸친 구간도 보도록 두 번 이어 붙임.
#         last = {}  # {}는 빈 딕셔너리. 칸 번호별 마지막 등장 위치를 저장.
#         left = 0  # 중복 칸이 없는 연속 구간의 왼쪽 끝.
#         for right, cell in enumerate(sequence):  # enumerate는 (인덱스, 값)을 제공. 오른쪽 끝을 한 칸씩 확장.
#             left = max(left, last.get(cell, -1) + 1, right - length + 1)  # get은 없으면 기본값 반환. 같은 칸 중복 및 고리 한 바퀴 초과를 방지.
#             last[cell] = right  # 이 칸의 마지막 등장 위치를 갱신.
#             answer = max(answer, right - left + 1)  # 중복 칸이 없는 연결 구간의 최대 길이 갱신.
#     for node in range(2 * count):  # 모든 삼각형 번호를 순회.
#         if not seen[node] and len(graph[node]) < 2:  # 경로는 끝점부터 순회해야 성분 전체를 순서대로 방문 가능.
#             inspect(node)  # 끝점에서 시작하는 경로 성분 검사.
#     for node in range(2 * count):  # 남은 삼각형을 다시 순회.
#         if not seen[node]:  # 아직 방문하지 않은 성분은 모든 삼각형의 이웃이 두 개인 고리.
#             inspect(node)  # 고리 성분 검사.
#     return answer  # return으로 가장 큰 넓이를 채점기에 반환.

# 풀이 요약
# 삼각형은 두 바깥 변으로만 연결되어 이웃이 최대 2개입니다. 따라서 전체 그래프는 경로 또는 고리로 나뉩니다.
# 덩어리는 그 위의 연속 구간이며, 같은 정사각형의 삼각형 두 개를 함께 고를 수 없으므로 중복 칸 없는 최장 구간을 찾습니다.
# 예: [[1]]은 넓이 1. 고리는 두 번 이어 경계를 넘는 구간도 확인합니다. 시간·공간 O(N*M).
# 