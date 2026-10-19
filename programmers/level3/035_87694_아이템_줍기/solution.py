# 먼저 넣은 위치부터 탐색하는 BFS 큐로 사용.
from collections import deque

# 직사각형 목록·캐릭터 좌표·아이템 좌표 입력.
def solution(rectangle, characterX, characterY, itemX, itemY):
    # 좌표를 두 배로 만들므로 0~101 공간 확보.
    board = [[0] * 102 for _ in range(102)]
    # 가까운 테두리 사이의 잘못된 지름길 방지.
    rectangles = [[value * 2 for value in rect] for rect in rectangle]
    # 모든 직사각형을 채운 다음 내부들을 제거.
    for x1, y1, x2, y2 in rectangles:
        # 테두리를 포함한 행 순회.
        for y in range(y1, y2 + 1):
            # 테두리를 포함한 열 순회.
            for x in range(x1, x2 + 1):
                # [행][열]인 [y][x]로 직사각형 전체를 채움.
                board[y][x] = 1
    # 모든 직사각형을 채운 다음 내부들을 제거.
    for x1, y1, x2, y2 in rectangles:
        # 위·아래 테두리를 제외한 내부 행.
        for y in range(y1 + 1, y2):
            # 왼쪽·오른쪽 테두리를 제외한 내부 열.
            for x in range(x1 + 1, x2):
                # 최종 합집합의 테두리만 남음.
                board[y][x] = 0
    # 캐릭터 위치도 같은 비율로 확대해 언패킹.
    start_x, start_y = characterX * 2, characterY * 2
    # () 튜플로 확대된 아이템 좌표 저장.
    target = (itemX * 2, itemY * 2)
    # (x,y,이동 수)를 담은 시작 큐.
    queue = deque([(start_x, start_y, 0)])
    # 남은 테두리 1을 0으로 바꿔 중복 방문 방지.
    board[start_y][start_x] = 0
    # while은 큐가 비지 않은 동안 반복.
    while queue:
        # 가까운 위치부터 탐색.
        x, y, distance = queue.popleft()
        # 아이템에 도착했는지 검사.
        if (x, y) == target:
            # 확대 지도에서 이동한 거리를 원래 거리로 복원해 반환.
            return distance // 2
        # 네 방향의 x·y 변화량 순회.
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            # 다음 위치 계산.
            nx, ny = x + dx, y + dy
            # 지도 안의 미방문 테두리만 이동.
            if 0 <= nx < 102 and 0 <= ny < 102 and board[ny][nx] == 1:
                # 이웃을 즉시 방문 처리.
                board[ny][nx] = 0
                # append로 한 칸 더 먼 이웃을 큐 끝에 추가.
                queue.append((nx, ny, distance + 1))
    # 정상적인 도달 가능 입력에서는 사용하지 않는 방어용 반환.
    return 0
