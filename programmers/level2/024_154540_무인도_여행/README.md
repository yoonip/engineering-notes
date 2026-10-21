# 무인도 여행

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/154540) · Level 2 · Python3

상하좌우로 연결된 섬마다 식량을 합산해 오름차순으로 반환합니다.

## 조건과 입출력

입력 매개변수: `maps`. 반환값은 수치 배열이며 아래 풀이의 조건을 만족하는 결과입니다.

- 3 ≤ maps의 길이 ≤ 100
- 3 ≤ maps[i]의 길이 ≤ 100

## 풀이를 따라가기

아직 방문하지 않은 육지에서 DFS를 시작합니다. 방문할 때 식량을 더하고 바다 표시로 바꿔 중복 방문을 막습니다. 섬별 합계를 정렬합니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(maps):
    board = [list(row) for row in maps]
    rows, cols = len(board), len(board[0])
    answer = []
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'X':
                continue
            food = int(board[r][c])
            # 방문한 육지를 지워 같은 식량을 중복해서 더하지 않는다.
            board[r][c] = 'X'
            stack = [(r, c)]
            while stack:
                x, y = stack.pop()
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and board[nx][ny] != 'X':
                        # 상하좌우로 이어진 섬의 식량을 모두 합한다.
                        food += int(board[nx][ny])
                        board[nx][ny] = 'X'
                        stack.append((nx, ny))
            answer.append(food)
    return sorted(answer) if answer else [-1]
```

## 정답이 되는 이유

DFS는 시작점과 연결된 육지 전부만 방문합니다. 방문 표시 때문에 각 칸의 식량은 정확히 한 섬 합계에 한 번 들어갑니다.

시간 O(RC+I log I), 공간 O(RC) / Time O(RC+I log I), space O(RC); I=섬 수 / island count

주의할 점: 대각선은 연결이 아닙니다. 육지가 없으면 빈 배열이 아니라 [-1]을 반환합니다.

## 다른 방법: 분리 집합과 루트별 식량 합산

```python
from collections import defaultdict

def solution(maps):
    rows,cols=len(maps),len(maps[0])
    parent=list(range(rows*cols))
    def find(x):
        if parent[x]!=x: parent[x]=find(parent[x])
        return parent[x]
    for r in range(rows):
        for c in range(cols):
            if maps[r][c]=='X': continue
            for dr,dc in ((-1,0),(0,-1)):
                nr,nc=r+dr,c+dc
                if nr>=0 and nc>=0 and maps[nr][nc]!='X':
                    a,b=find(r*cols+c),find(nr*cols+nc)
                    if a!=b: parent[max(a,b)]=min(a,b)
    totals=defaultdict(int)
    for r in range(rows):
        for c in range(cols):
            if maps[r][c]!='X': totals[find(r*cols+c)]+=int(maps[r][c])
    return sorted(totals.values()) or [-1]
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 아직 방문하지 않은 육지에서 DFS를 시작합니다. 방문할 때 식량을 더하고 바다 표시로 바꿔 중복 방문을 막습니다. 섬별 합계를 정렬합니다. | 분리 집합과 루트별 식량 합산 |
| 비용 | 시간 O(RC+I log I), 공간 O(RC) / Time O(RC+I log I), space O(RC); I=섬 수 / island count | 시간 O(RC α(RC)+I log I), 공간 O(RC) / Time O(RC α(RC)+I log I), space O(RC) |

## 검증

공식 예제 2개와 생성 입력 50개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Sum food on each four-connected island and return island totals in ascending order.

### Conditions and input/output

Input arguments: `maps`. The return value is a numeric list satisfying the task described below.

- 3 ≤ rows,columns ≤ 100; cells are 'X' or digits 1 … 9

### Approach

Start DFS at each unvisited land cell. Add food and mark the cell as sea to prevent repeats; sort the component totals.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

DFS visits exactly the land connected to its start. Marking ensures each food cell contributes once to exactly one island.

시간 O(RC+I log I), 공간 O(RC) / Time O(RC+I log I), space O(RC); I=섬 수 / island count

Boundary cases: Diagonal contact does not connect islands. Return [-1], not an empty list, if no land exists.

### Alternative: Disjoint-set union with food totals by root

시간 O(RC α(RC)+I log I), 공간 O(RC) / Time O(RC α(RC)+I log I), space O(RC)

### Verification

Local checks covered 2 official examples and 50 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 무인도 여행](https://school.programmers.co.kr/learn/courses/30/lessons/154540) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
