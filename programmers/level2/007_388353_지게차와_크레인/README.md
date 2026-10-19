# 지게차와 크레인

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/388353) · Level 2 · Python3

지게차는 외부에서 닿는 컨테이너만, 크레인은 같은 글자를 모두 제거합니다.

## 조건과 입출력

입력 매개변수: `storage, requests`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과입니다.

- 2 ≤ storage의 길이 = n ≤ 50
- 2 ≤ storage[i]의 길이 = m ≤ 50
- 1 ≤ requests의 길이 ≤ 100
- 1 ≤ requests[i]의 길이 ≤ 2

## 풀이를 따라가기

창고 주위에 빈 테두리를 만듭니다. 지게차 요청은 바깥 빈칸에서 BFS해 맞닿은 대상만 모읍니다. 요청 하나의 탐색이 끝난 뒤 모은 칸을 한꺼번에 지웁니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
from collections import deque


def solution(storage, requests):
    n, m = len(storage), len(storage[0])
    board = [['.'] * (m + 2)]
    for row in storage:
        board.append(['.'] + list(row) + ['.'])
    board.append(['.'] * (m + 2))
    remaining = n * m
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

    for request in requests:
        target = request[0]
        removed = []
        if len(request) == 2:
            for r in range(1, n + 1):
                for c in range(1, m + 1):
                    if board[r][c] == target:
                        removed.append((r, c))
        else:
            visited = [[False] * (m + 2) for _ in range(n + 2)]
            # 추가한 바깥 테두리에서 접근 가능 영역을 찾는다.
            visited[0][0] = True
            queue = deque([(0, 0)])
            while queue:
                r, c = queue.popleft()
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if not (0 <= nr < n + 2 and 0 <= nc < m + 2):
                        continue
                    if visited[nr][nc]:
                        continue
                    visited[nr][nc] = True
                    # 빈칸만 통과하며 대상 컨테이너를 지나가지는 않는다.
                    if board[nr][nc] == '.':
                        queue.append((nr, nc))
                    elif board[nr][nc] == target:
                        removed.append((nr, nc))

        # 요청 한 번의 탐색이 끝난 뒤 한꺼번에 제거한다.
        for r, c in removed:
            board[r][c] = '.'
        remaining -= len(removed)

    return remaining
```

## 정답이 되는 이유

바깥에서 빈칸만 통과해 닿는 경계가 지게차 접근 가능 구역과 일치합니다. 제거를 나중에 반영해야 같은 요청 중 새로 뚫린 통로를 잘못 이용하지 않습니다.

시간 O(QRC), 공간 O(RC) / Time O(QRC), space O(RC)

주의할 점: 같은 글자를 두 번 적은 요청은 크레인입니다. 지게차로 안쪽의 같은 글자가 연쇄 제거되지 않도록 합니다.

## 다른 방법: 반복적인 외부 영역 확장

이 대안은 작은 입력에서 원리를 비교하는 검증용입니다. 최대 제한에 제출할 기본 풀이와 구분합니다.

```python
def solution(storage, requests):
    rows, cols = len(storage), len(storage[0])
    board = [list(row) for row in storage]
    for request in requests:
        outside = {(-1, c) for c in range(cols)} | {(rows, c) for c in range(cols)}
        outside |= {(r, -1) for r in range(rows)} | {(r, cols) for r in range(rows)}
        changed = True
        while changed:
            changed = False
            for r in range(rows):
                for c in range(cols):
                    if board[r][c] == '.' and (r,c) not in outside:
                        if any((r+dr,c+dc) in outside for dr,dc in ((1,0),(-1,0),(0,1),(0,-1))):
                            outside.add((r,c))
                            changed = True
        removed = []
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == request[0] and (len(request)==2 or any((r+dr,c+dc) in outside for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)))):
                    removed.append((r,c))
        for r,c in removed:
            board[r][c] = '.'
    return sum(cell != '.' for row in board for cell in row)
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 창고 주위에 빈 테두리를 만듭니다. 지게차 요청은 바깥 빈칸에서 BFS해 맞닿은 대상만 모읍니다. 요청 하나의 탐색이 끝난 뒤 모은 칸을 한꺼번에 지웁니다. | 반복적인 외부 영역 확장 |
| 비용 | 시간 O(QRC), 공간 O(RC) / Time O(QRC), space O(RC) | 시간 O(Q(RC)^2), 공간 O(RC) / Time O(Q(RC)^2), space O(RC); 작은 창고 비교용 / small-warehouse comparison |

## 검증

공식 예제 2개와 생성 입력 40개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

A forklift removes matching containers accessible from outside; a crane removes every matching container.

### Conditions and input/output

Input arguments: `storage, requests`. The return value is an integer satisfying the task described below.

- 2 ≤ rows,columns ≤ 50; uppercase A–Z cells
- 1 ≤ len(requests) ≤ 100; request length 1 or 2

### Approach

Pad the warehouse with empty cells. For a forklift request, BFS through outside-connected empties and collect adjacent targets. Remove the collected cells only after completing that request’s search.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

The boundary of the outside-connected empty region is precisely the forklift-accessible set. Delayed removal prevents newly opened passages from incorrectly expanding the same request.

시간 O(QRC), 공간 O(RC) / Time O(QRC), space O(RC)

Boundary cases: A two-letter request denotes a crane. A forklift must not remove a chain of newly exposed containers within one request.

### Alternative: Fixed-point expansion of the outside region

This alternative is for understanding and checking small inputs; use the main implementation for the full constraints. 시간 O(Q(RC)^2), 공간 O(RC) / Time O(Q(RC)^2), space O(RC); 작은 창고 비교용 / small-warehouse comparison

### Verification

Local checks covered 2 official examples and 40 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 지게차와 크레인](https://school.programmers.co.kr/learn/courses/30/lessons/388353) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
