from collections import deque

def solution(rectangle, characterX, characterY, itemX, itemY):
    board = [[0] * 102 for _ in range(102)]
    rectangles = [[value * 2 for value in rect] for rect in rectangle]
    for x1, y1, x2, y2 in rectangles:
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                board[y][x] = 1
    for x1, y1, x2, y2 in rectangles:
        for y in range(y1 + 1, y2):
            for x in range(x1 + 1, x2):
                board[y][x] = 0
    start_x, start_y = characterX * 2, characterY * 2
    target = (itemX * 2, itemY * 2)
    queue = deque([(start_x, start_y, 0)])
    board[start_y][start_x] = 0
    while queue:
        x, y, distance = queue.popleft()
        if (x, y) == target:
            return distance // 2
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < 102 and 0 <= ny < 102 and board[ny][nx] == 1:
                board[ny][nx] = 0
                queue.append((nx, ny, distance + 1))
    return 0

# 전체 코드 줄별 설명
# from collections import deque  # collections에서 deque를 import. 먼저 넣은 위치부터 탐색하는 BFS 큐로 사용.
# 
# def solution(rectangle, characterX, characterY, itemX, itemY):  # def는 함수 정의. 직사각형 목록·캐릭터 좌표·아이템 좌표 입력.
#     board = [[0] * 102 for _ in range(102)]  # [] 리스트 내포로 지도 생성. 좌표를 두 배로 만들므로 0~101 공간 확보.
#     rectangles = [[value * 2 for value in rect] for rect in rectangle]  # 중첩 리스트 내포와 *2로 모든 좌표 확대. 가까운 테두리 사이의 잘못된 지름길 방지.
#     for x1, y1, x2, y2 in rectangles:  # for~in으로 확대된 직사각형의 네 좌표를 언패킹.
#         for y in range(y1, y2 + 1):  # range는 끝 제외라 +1. 테두리를 포함한 행 순회.
#             for x in range(x1, x2 + 1):  # 테두리를 포함한 열 순회.
#                 board[y][x] = 1  # [행][열]인 [y][x]로 직사각형 전체를 채움.
#     for x1, y1, x2, y2 in rectangles:  # 모든 직사각형을 채운 다음 내부들을 제거.
#         for y in range(y1 + 1, y2):  # 위·아래 테두리를 제외한 내부 행.
#             for x in range(x1 + 1, x2):  # 왼쪽·오른쪽 테두리를 제외한 내부 열.
#                 board[y][x] = 0  # 어떤 직사각형의 내부든 통행 불가. 최종 합집합의 테두리만 남음.
#     start_x, start_y = characterX * 2, characterY * 2  # 캐릭터 위치도 같은 비율로 확대해 언패킹.
#     target = (itemX * 2, itemY * 2)  # () 튜플로 확대된 아이템 좌표 저장.
#     queue = deque([(start_x, start_y, 0)])  # (x,y,이동 수)를 담은 시작 큐.
#     board[start_y][start_x] = 0  # 큐에 넣을 때 방문 표시. 남은 테두리 1을 0으로 바꿔 중복 방문 방지.
#     while queue:  # while은 큐가 비지 않은 동안 반복.
#         x, y, distance = queue.popleft()  # popleft는 큐 맨 앞 항목 제거·반환. 가까운 위치부터 탐색.
#         if (x, y) == target:  # if는 조건문, ==는 같음. 아이템에 도착했는지 검사.
#             return distance // 2  # //는 정수 나눗셈. 확대 지도에서 이동한 거리를 원래 거리로 복원해 반환.
#         for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):  # 네 방향의 x·y 변화량 순회.
#             nx, ny = x + dx, y + dy  # 다음 위치 계산.
#             if 0 <= nx < 102 and 0 <= ny < 102 and board[ny][nx] == 1:  # and는 모두 참. 지도 안의 미방문 테두리만 이동.
#                 board[ny][nx] = 0  # 이웃을 즉시 방문 처리.
#                 queue.append((nx, ny, distance + 1))  # append로 한 칸 더 먼 이웃을 큐 끝에 추가.
#     return 0  # 정상적인 도달 가능 입력에서는 사용하지 않는 방어용 반환.

# 풀이 요약
# 좌표를 두 배로 확대하고 직사각형들을 전부 채운 뒤, 각 직사각형의 내부를 모두 지워 합친 지형의 테두리를 만듭니다.
# 테두리 위에서 BFS를 하면 최단 이동 거리입니다. 좌표 확대 때문에 생긴 거리 두 배를 마지막에 나눕니다. 좌표 최대값 C에 대해 시간·공간 O(C²), 직사각형 수는 최대 4입니다.
# 예: 원래 한 칸 너비의 굴곡도 두 칸 간격으로 표현되어, 인접해 보이는 서로 다른 테두리를 가로지르는 지름길을 막습니다.
# 