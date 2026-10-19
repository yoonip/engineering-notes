# 리코쳇 로봇

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/169199) · Level 2 · Python3

장애물이나 벽까지 미끄러지는 로봇을 목표에 세우는 최소 이동 수를 구합니다.

## 조건과 입출력

입력 매개변수: `board`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과입니다.

- 3 ≤ board의 길이 ≤ 100
- 3 ≤ board의 원소의 길이 ≤ 100

## 풀이를 따라가기

정지할 수 있는 칸을 정점으로 봅니다. 네 방향으로 끝까지 미끄러진 위치에 간선 하나를 만들고 BFS로 이동 수를 셉니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
from collections import deque

def solution(board):
    rows, cols = len(board), len(board[0])
    distance = [[-1] * cols for _ in range(rows)]
    queue = deque()
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'R':
                distance[r][c] = 0
                queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        if board[r][c] == 'G':
            return distance[r][c]
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r, c
            # 한 번 움직이면 벽이나 장애물 앞까지 멈추지 않는다.
            while 0 <= nr + dr < rows and 0 <= nc + dc < cols and board[nr + dr][nc + dc] != 'D':
                nr += dr
                nc += dc
            # 같은 정지 위치는 BFS에서 처음 도달한 이동 수가 최소다.
            if distance[nr][nc] == -1:
                distance[nr][nc] = distance[r][c] + 1
                queue.append((nr, nc))
    return -1
```

## 정답이 되는 이유

슬라이드 한 번의 비용이 모두 1이므로 BFS가 처음 방문한 정지 칸의 거리가 최소입니다. 목표를 지나가기만 한 경우는 정지 간선의 끝이 아니어서 성공으로 세지 않습니다.

시간 O(RC(R+C)), 공간 O(RC) / Time O(RC(R+C)), space O(RC)

주의할 점: 장애물 바로 앞에서는 움직이지 않을 수도 있습니다. 시작 칸을 이미 방문 처리해 제자리 간선을 반복하지 않습니다.

## 다른 방법: 정지점 전처리 후 BFS

```python
from collections import deque

def solution(board):
    rows,cols=len(board),len(board[0])
    ends={}
    for r in range(rows):
        c=0
        while c<cols:
            if board[r][c]=='D': c+=1; continue
            start=c
            while c<cols and board[r][c]!='D': c+=1
            for y in range(start,c):
                ends[(r,y)]=[(r,start),(r,c-1)]
    for c in range(cols):
        r=0
        while r<rows:
            if board[r][c]=='D': r+=1; continue
            start=r
            while r<rows and board[r][c]!='D': r+=1
            for x in range(start,r):
                ends[(x,c)].extend(((start,c),(r-1,c)))
    start=next((r,c) for r in range(rows) for c in range(cols) if board[r][c]=='R')
    queue=deque([(start,0)])
    seen={start}
    while queue:
        point,d=queue.popleft()
        if board[point[0]][point[1]]=='G': return d
        for following in ends[point]:
            if following not in seen:
                seen.add(following)
                queue.append((following,d+1))
    return -1
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 정지할 수 있는 칸을 정점으로 봅니다. 네 방향으로 끝까지 미끄러진 위치에 간선 하나를 만들고 BFS로 이동 수를 셉니다. | 정지점 전처리 후 BFS |
| 비용 | 시간 O(RC(R+C)), 공간 O(RC) / Time O(RC(R+C)), space O(RC) | 시간 O(RC), 공간 O(RC) / Time and space O(RC) |

## 검증

공식 예제 2개와 생성 입력 50개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Find the minimum number of slides needed to stop a robot on the goal.

### Conditions and input/output

Input arguments: `board`. The return value is an integer satisfying the task described below.

- 3 ≤ rows,columns ≤ 100; characters '.', 'D', 'R', 'G'
- exactly one R and one G

### Approach

Treat stopping cells as vertices. Each direction produces one edge to the last free cell before a wall or obstacle; BFS counts slides.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Every slide costs one, so a cell’s first BFS visit is optimal. Passing through the goal without stopping does not end an edge and is not a success.

시간 O(RC(R+C)), 공간 O(RC) / Time O(RC(R+C)), space O(RC)

Boundary cases: An adjacent obstacle may cause no movement. Mark the start visited to avoid repeated self-transitions.

### Alternative: Precompute slide endpoints before BFS

시간 O(RC), 공간 O(RC) / Time and space O(RC)

### Verification

Local checks covered 2 official examples and 50 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 리코쳇 로봇](https://school.programmers.co.kr/learn/courses/30/lessons/169199) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
