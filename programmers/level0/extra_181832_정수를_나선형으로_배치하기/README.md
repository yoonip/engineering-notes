# 정수를 나선형으로 배치하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181832) · Level 0 · Python3

## 풀이

현재 방향으로 채우다가 벽이나 이미 채운 칸을 만나면 시계방향으로 회전합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(n):
    board = [[0] * n for _ in range(n)]
    directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
    row, col, direction = 0, 0, 0
    for value in range(1, n * n + 1):
        board[row][col] = value
        dr, dc = directions[direction]
        nr, nc = row + dr, col + dc
        if not (0 <= nr < n and 0 <= nc < n) or board[nr][nc] != 0:
            direction = (direction + 1) % 4
            dr, dc = directions[direction]
            nr, nc = row + dr, col + dc
        row, col = nr, nc
    return board

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. 나선형 배열 크기 입력.
#     board = [[0] * n for _ in range(n)]  # 중첩 리스트 내포로 서로 독립적인 n개 행 생성. 0은 아직 채우지 않은 칸 표시.
#     directions = ((0, 1), (1, 0), (0, -1), (-1, 0))  # ()는 튜플. 오른쪽·아래·왼쪽·위 방향의 행·열 변화량 저장.
#     row, col, direction = 0, 0, 0  # 현재 행·열·방향 인덱스 초기화.
#     for value in range(1, n * n + 1):  # range는 끝 제외 정수 수열. 1부터 n²까지 순회.
#         board[row][col] = value  # [][]는 이차원 리스트 접근. 현재 위치에 숫자 기록.
#         dr, dc = directions[direction]  # 현재 방향의 행·열 변화량을 나누어 받음.
#         nr, nc = row + dr, col + dc  # 계속 직진했을 때 다음 위치 계산.
#         if not (0 <= nr < n and 0 <= nc < n) or board[nr][nc] != 0:  # not은 부정, and·or는 논리 조건. 범위 밖이거나 이미 채운 칸이면 방향 전환.
#             direction = (direction + 1) % 4  # %는 나머지. 방향을 0~3에서 순환해 시계방향으로 회전.
#             dr, dc = directions[direction]  # 회전한 방향의 변화량 조회.
#             nr, nc = row + dr, col + dc  # 회전 후 이동할 다음 위치 계산.
#         row, col = nr, nc  # 다음 반복의 현재 위치 갱신.
#     return board  # 완성된 나선형 이차원 리스트 반환.

# 풀이 요약
# 현재 방향으로 채우다가 벽이나 이미 채운 칸을 만나면 시계방향으로 회전합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
