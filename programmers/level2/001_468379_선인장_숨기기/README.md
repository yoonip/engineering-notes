# 선인장 숨기기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/468379) · Level 2 · Python3

직사각형 구역에 첫 비가 내리는 시각을 최대화하고, 동률이면 위쪽·왼쪽 위치를 고른다.

## 조건과 입출력

입력 매개변수: `m, n, h, w, drops`. 반환값은 수치 배열이며 아래 풀이의 조건을 만족하는 결과다.

- 1 ≤ m, n ≤ 500,000
- 1 ≤ m × n ≤ 500,000
- 1 ≤ h ≤ m
- 1 ≤ w ≤ n
- 1 ≤ drops의 길이 ≤ m × n
- 0 ≤ r < m
- 0 ≤ c < n

## 풀이를 따라가기

각 칸에 비가 온 순서를 적는다. 구역의 첫 비는 그 안의 최솟값이다. 가로 구간의 최솟값을 단조 덱으로 구한 뒤 세로에도 같은 계산을 한다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
from collections import deque


def window_minimum(values, size):
    q = deque()
    result = []

    for i, value in enumerate(values):
        # 현재 창에서 빠진 후보를 앞에서 제거한다.
        while q and q[0] <= i - size:
            q.popleft()

        # 새 값보다 큰 후보는 이후에도 최솟값이 될 수 없다.
        while q and values[q[-1]] >= value:
            q.pop()

        q.append(i)

        if i >= size - 1:
            result.append(values[q[0]])

    return result


def solution(m, n, h, w, drops):
    never = len(drops) + 1
    rain = [never] * (m * n)

    for time, (r, c) in enumerate(drops, start=1):
        rain[r * n + c] = time

    cols = n - w + 1

    # 가로 창의 최솟값을 먼저 구한 뒤 세로 창을 계산한다.
    row_min = []

    for r in range(m):
        row = rain[r * n:(r + 1) * n]
        row_min.extend(window_minimum(row, w))

    best_time = -1
    answer = [0, 0]

    for c in range(cols):
        column = row_min[c::cols]
        area_times = window_minimum(column, h)

        for r, time in enumerate(area_times):
            if time > best_time or (
                time == best_time and [r, c] < answer
            ):
                best_time = time
                answer = [r, c]

    return answer
```

## 왜 맞는가

더 늦게 들어온 더 작은 값이 있으면 이전의 큰 값은 어떤 이후 구간에서도 최솟값이 될 수 없다. 덱의 앞이 항상 현재 구간의 최솟값이므로 두 번의 계산으로 모든 직사각형의 최솟값을 얻는다.

시간 O(mn), 공간 O(mn) / Time O(mn), space O(mn)

주의할 점: 비가 없는 칸은 모든 실제 시각보다 큰 값으로 둔다. 사각형을 회전하지 않으며, 같은 시각에는 행·열을 함께 비교한다.

## 다른 방법: 시각 이진 탐색 + 2차원 누적합

```python
def solution(m, n, h, w, drops):
    def find(dry_until):
        # 이 시각까지 젖은 칸을 1로 표시하고 누적합을 만든다.
        wet = [[0] * n for _ in range(m)]
        for r, c in drops[:dry_until]:
            wet[r][c] = 1
        prefix = [[0] * (n + 1) for _ in range(m + 1)]
        for r in range(m):
            running = 0
            for c in range(n):
                running += wet[r][c]
                prefix[r+1][c+1] = prefix[r][c+1] + running
        for r in range(m-h+1):
            for c in range(n-w+1):
                total = prefix[r+h][c+w]-prefix[r][c+w]-prefix[r+h][c]+prefix[r][c]
                if total == 0:
                    return [r, c]
        return None
    low, high = 0, len(drops)
    while low < high:
        mid = (low + high + 1) // 2
        if find(mid) is not None:
            low = mid
        else:
            high = mid - 1
    return find(low)
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 각 칸에 비가 온 순서를 적는다. 구역의 첫 비는 그 안의 최솟값이다. 가로 구간의 최솟값을 단조 덱으로 구한 뒤 세로에도 같은 계산을 한다. | 시각 이진 탐색 + 2차원 누적합 |
| 비용 | 시간 O(mn), 공간 O(mn) / Time O(mn), space O(mn) | O(mn log(D+1)) 시간, O(mn) 공간 / time O(mn log(D+1)), space O(mn); D=len(drops) |

## 검증

공식 예제 6개와 생성 입력 60개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다. 제한 상한에 해당하는 크기·수치의 경계 검사도 저장된 테스트에 포함했다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Choose an axis-aligned rectangle whose first raindrop arrives as late as possible; break ties by row, then column.

### Conditions and input/output

Input arguments: `m, n, h, w, drops`. The return value is a numeric list satisfying the task described below.

- 1 ≤ m,n ≤ 500000; m·n ≤ 500000
- 1 ≤ h ≤ m; 1 ≤ w ≤ n; 1 ≤ len(drops) ≤ m·n
- drops: unique cells, zero-based coordinates

### Approach

Record each cell’s rain time. A rectangle’s first rain is its minimum cell time. Compute horizontal window minima with a monotonic deque, then apply the same operation vertically.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

An older, larger value is dominated by a newer, smaller value in every future window containing both. The deque front is therefore the current minimum; two passes cover every rectangle.

시간 O(mn), 공간 O(mn) / Time O(mn), space O(mn)

Boundary cases: Use a sentinel later than every real drop. Do not rotate the rectangle; compare both row and column when times tie.

### Alternative: Binary search on time with 2D prefix sums

O(mn log(D+1)) 시간, O(mn) 공간 / time O(mn log(D+1)), space O(mn); D=len(drops)

### Verification

Local checks covered 6 official examples and 60 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases. Saved tests also include a size or numeric boundary at the stated upper limit.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 선인장 숨기기](https://school.programmers.co.kr/learn/courses/30/lessons/468379) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
