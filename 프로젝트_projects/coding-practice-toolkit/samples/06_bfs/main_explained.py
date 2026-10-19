# 자체 창작 연습 06 · 격자 통로의 최소 이동 
# 핵심 상태: dist[r][c]는 최소 이동 횟수이며 -1이면 미방문. 큐는 아직 이웃을 살피지 않은 칸이다.
# Python 3: 파일의 위에서 아래로 실행한다. 들여쓰기가 반복문·조건문·함수의 범위다.
# sys.stdin은 표준입력이다. 이 예제의 read는 readline의 별칭이라 한 줄씩 읽는다.
# 입력 헤더와 정해진 격자 행 수만 읽으므로 올바른 행을 모두 입력하면 EOF를 기다리지 않는다.

import sys
from collections import deque
# 이 문제는 숫자와 격자 행 문자열이 섞여 있어 한 줄씩 읽는다.
# read는 함수의 별칭이며 read()가 실제로 다음 한 줄을 읽는 호출이다.
# 격자 행은 strip으로 줄바꿈을 제거하고 decode로 문자열로 바꾼다.
read = sys.stdin.buffer.readline
n, m = map(int, read().split())
grid = [read().strip().decode() for _ in range(n)]
# 각 행을 새 리스트로 만들어 n행 m열 거리표를 -1로 초기화한다.
# [[-1]*m]*n으로 만들면 같은 행 객체를 공유해 한 칸 변경이 여러 행에 반영될 수 있다.
# deque는 양 끝 추가·제거가 빠른 큐다. list.pop(0) 대신 popleft를 쓴다.
dist = [[-1] * m for _ in range(n)]
q = deque()
# 시작칸이 통로일 때만 방문 표시와 큐 삽입을 한다.
# (0,0)은 좌표 두 개를 묶은 tuple이다. 큐에는 이러한 좌표들을 저장한다.
# 시작 거리 0은 지나간 칸 수가 아니라 이동 횟수를 센다는 뜻이다.
if grid[0][0] == '1':
    dist[0][0] = 0
    q.append((0, 0))
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
# deque가 비어 있지 않은 동안 가장 먼저 넣은 좌표를 popleft로 꺼낸다.
# 네 방향을 검사하면서 범위 밖·벽·이미 방문한 칸을 건너뛴다.
# 방문 표시는 큐에 넣을 때 하고 도착하지 못하면 마지막 거리 -1을 그대로 출력한다.
while q:
    r, c = q.popleft()
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if not (0 <= nr < n and 0 <= nc < m):
            continue
        if grid[nr][nc] == '0' or dist[nr][nc] != -1:
            continue
        dist[nr][nc] = dist[r][c] + 1  # 큐 삽입 전에 방문을 확정한다.
        q.append((nr, nc))
print(dist[n - 1][m - 1])

# 복잡도: 시간 O(NM), 공간 O(NM). 각 칸은 최대 한 번 큐에 들어가고 네 이웃을 확인한다.
# 마지막 경계 확인:
# - 벽·범위 밖·방문한 칸을 모두 제외한다.
# - 방문 표시를 큐에서 꺼낼 때 하면 중복 삽입이 생긴다.
# - 이 문제는 지나간 칸 수가 아니라 이동 횟수다. 시작 거리는 0.
# - Python list.pop(0)은 앞 원소 이동 비용이 있으므로 deque.popleft를 쓴다.
