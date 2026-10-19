# 삼각 달팽이

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/68645) · Level 2 · Python3

삼각형 배열을 아래·오른쪽·왼쪽 위 방향으로 채운 뒤 행 순서로 펼친다.

## 조건과 입출력

입력 매개변수: `n`. 반환값은 수치 배열이며 아래 풀이의 조건을 만족하는 결과다.

- n은 1 이상 1,000 이하입니다.

## 풀이를 따라가기

삼각형 행마다 r+1칸을 만든다. 방향을 세 가지로 순환하고 이동 길이를 n,n−1,…,1로 줄이며 숫자를 채운다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(n):
    board = [[0] * (r + 1) for r in range(n)]
    r, c, value = -1, 0, 1
    directions = ((1, 0), (0, 1), (-1, -1))
    # 이동 길이를 하나씩 줄이며 세 방향을 순환한다.
    for side in range(n):
        dr, dc = directions[side % 3]
        for _ in range(n - side):
            r += dr
            c += dc
            board[r][c] = value
            value += 1
    # 채운 경로 순서가 아니라 행 순서로 펼친다.
    return [number for row in board for number in row]
```

## 왜 맞는가

각 변을 채운 뒤 다음 방향의 길이를 하나 줄이면 바깥 테두리부터 안쪽으로 빈칸만 따라간다. 이동 수 합 n(n+1)/2가 전체 칸 수와 같아 모든 칸을 한 번 채운다.

시간 O(n²), 공간 O(n²) / Time and space O(n²)

주의할 점: 정사각형 n×n을 만들 필요가 없다. 마지막 출력은 이동 순서가 아니라 행 순서다.

## 다른 방법: 다음 칸의 경계·방문 여부로 방향 전환

기본 풀이와 같은 결과를 구하되 중간 상태와 계산 방식이 다르다.

```python
def solution(n):
    board=[[0]*(r+1) for r in range(n)]
    directions=((1,0),(0,1),(-1,-1))
    r=c=d=0
    for value in range(1,n*(n+1)//2+1):
        board[r][c]=value
        dr,dc=directions[d]
        nr,nc=r+dr,c+dc
        if not(0<=nr<n and 0<=nc<=nr) or board[nr][nc]:
            d=(d+1)%3
            dr,dc=directions[d]
            nr,nc=r+dr,c+dc
        r,c=nr,nc
    return [value for row in board for value in row]
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 삼각형 행마다 r+1칸을 만든다. 방향을 세 가지로 순환하고 이동 길이를 n,n−1,…,1로 줄이며 숫자를 채운다. | 다음 칸의 경계·방문 여부로 방향 전환 |
| 비용 | 시간 O(n²), 공간 O(n²) / Time and space O(n²) | 시간 O(n²), 공간 O(n²) / Time and space O(n²) |

## 검증

공식 예제 3개와 생성 입력 39개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다. 제한 상한에 해당하는 크기·수치의 경계 검사도 저장된 테스트에 포함했다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Fill a triangular array down, right and up-left, then flatten it row by row.

### Conditions and input/output

Input arguments: `n`. The return value is a numeric list satisfying the task described below.

- 1 ≤ n ≤ 1000

### Approach

Allocate row r with r+1 cells. Cycle through three directions while decreasing run lengths n,n−1,…,1.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Reducing each next run by one follows unfilled cells from the outer border inward. The total moves n(n+1)/2 equal the number of cells, filling each once.

시간 O(n²), 공간 O(n²) / Time and space O(n²)

Boundary cases: A full n-by-n square is unnecessary. Flatten by rows, not by traversal order.

### Alternative: Turn when the next cell is outside or already filled

It computes the same result using different intermediate states or evaluation steps. 시간 O(n²), 공간 O(n²) / Time and space O(n²)

The main approach follows the steps described above. The alternative uses turn when the next cell is outside or already filled; compare its intermediate state and cost with the main implementation before choosing it.

### Verification

Local checks covered 3 official examples and 39 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases. Saved tests also include a size or numeric boundary at the stated upper limit.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 삼각 달팽이](https://school.programmers.co.kr/learn/courses/30/lessons/68645) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
