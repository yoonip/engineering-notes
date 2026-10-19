# 미로 탈출

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/159993) · Level 2 · Python3

레버를 먼저 당긴 다음 출구에 도착하는 최소 이동 시간을 구한다.

## 조건과 입출력

입력 매개변수: `maps`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과다.

- 5 ≤ maps의 길이 ≤ 100
- 5 ≤ maps[i]의 길이 ≤ 100

## 풀이를 따라가기

BFS로 시작→레버 거리와 레버→출구 거리를 따로 구한다. 하나라도 도달할 수 없으면 −1, 둘 다 가능하면 합을 반환한다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
from collections import deque

def solution(maps):
    rows, cols = len(maps), len(maps[0])
    positions = {}
    for r in range(rows):
        for c in range(cols):
            if maps[r][c] in 'SLE':
                positions[maps[r][c]] = (r, c)
    def bfs(start, goal):
        queue = deque([(start[0], start[1], 0)])
        visited = {start}
        while queue:
            r, c, distance = queue.popleft()
            if (r, c) == goal:
                return distance
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and maps[nr][nc] != 'X' and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc, distance + 1))
        return -1
    # 시작에서 레버까지, 레버에서 출구까지 최단 거리를 따로 구한다.
    first = bfs(positions['S'], positions['L'])
    second = bfs(positions['L'], positions['E'])
    # 두 구간 중 하나라도 막혔으면 탈출할 수 없다.
    return first + second if first >= 0 and second >= 0 else -1
```

## 왜 맞는가

모든 성공 경로는 레버를 거친다. 경로를 그 지점에서 나누면 각 부분은 해당 최단 거리보다 짧을 수 없고 두 최단 경로를 이어 붙이면 하한을 달성한다.

시간 O(RC), 공간 O(RC) / Time and space O(RC)

주의할 점: 레버를 당기기 전에도 출구 칸을 지나갈 수 있다. 레버 이후 방문 배열을 새로 만들어 이전 경로를 다시 지날 수 있게 한다.

## 다른 방법: 레버 상태를 포함한 한 번의 BFS

기본 풀이와 같은 결과를 구하되 중간 상태와 계산 방식이 다르다.

```python
from collections import deque

def solution(maps):
    rows,cols=len(maps),len(maps[0])
    r,c=next((r,c) for r in range(rows) for c in range(cols) if maps[r][c]=='S')
    queue=deque([(r,c,False,0)])
    seen={(r,c,False)}
    while queue:
        r,c,lever,d=queue.popleft()
        if maps[r][c]=='E' and lever: return d
        for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
            nr,nc=r+dr,c+dc
            if 0<=nr<rows and 0<=nc<cols and maps[nr][nc]!='X':
                active=lever or maps[nr][nc]=='L'
                state=(nr,nc,active)
                if state not in seen:
                    seen.add(state)
                    queue.append((nr,nc,active,d+1))
    return -1
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | BFS로 시작→레버 거리와 레버→출구 거리를 따로 구한다. 하나라도 도달할 수 없으면 −1, 둘 다 가능하면 합을 반환한다. | 레버 상태를 포함한 한 번의 BFS |
| 비용 | 시간 O(RC), 공간 O(RC) / Time and space O(RC) | 시간 O(RC), 공간 O(RC), 정점 수 최대 2RC / Time and space O(RC), at most 2RC states |

## 검증

공식 예제 2개와 생성 입력 50개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Find the shortest path that activates the lever before exiting.

### Conditions and input/output

Input arguments: `maps`. The return value is an integer satisfying the task described below.

- 5 ≤ rows,columns ≤ 100; characters S,E,L,O,X
- exactly one distinct S,E,L; cells may be revisited; E may be crossed before L

### Approach

Run BFS from start to lever and from lever to exit. Return −1 if either is unreachable; otherwise add the distances.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Every successful path passes through the lever. Splitting there gives a lower bound equal to the two shortest distances, and concatenating their paths attains it.

시간 O(RC), 공간 O(RC) / Time and space O(RC)

Boundary cases: The exit is traversable before activation. A fresh visited set permits revisiting cells after pulling the lever.

### Alternative: One BFS with a lever-state bit

It computes the same result using different intermediate states or evaluation steps. 시간 O(RC), 공간 O(RC), 정점 수 최대 2RC / Time and space O(RC), at most 2RC states

The main approach follows the steps described above. The alternative uses one bfs with a lever-state bit; compare its intermediate state and cost with the main implementation before choosing it.

### Verification

Local checks covered 2 official examples and 50 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 미로 탈출](https://school.programmers.co.kr/learn/courses/30/lessons/159993) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
