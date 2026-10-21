# 빛의 경로 사이클

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/86052) · Level 2 · Python3

격자에서 직진·좌회전·우회전하는 빛의 모든 경로 사이클 길이를 구합니다.

## 조건과 입출력

입력 매개변수: `grid`. 반환값은 수치 배열이며 아래 풀이의 조건을 만족하는 결과입니다.

- 1 ≤ grid의 길이 ≤ 500
- 1 ≤ grid의 각 문자열의 길이 ≤ 500

## 풀이를 따라가기

상태를 칸과 들어온 방향의 쌍으로 잡습니다. 지시대로 방향을 바꾸고 반대편으로 감아 이동합니다. 방문하지 않은 상태에서 출발해 다시 방문한 상태까지 길이를 셉니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(grid):
    rows, cols = len(grid), len(grid[0])
    # 칸뿐 아니라 들어온 방향까지 방문 상태에 넣는다.
    visited = [bytearray(cols * 4) for _ in range(rows)]
    directions = ((-1, 0), (0, 1), (1, 0), (0, -1))
    answer = []
    for r in range(rows):
        for c in range(cols):
            for direction in range(4):
                if visited[r][c * 4 + direction]:
                    continue
                x, y, d, length = r, c, direction, 0
                # 후속 상태가 하나이므로 경로를 따라가며 한 사이클 길이를 센다.
                while not visited[x][y * 4 + d]:
                    visited[x][y * 4 + d] = 1
                    length += 1
                    if grid[x][y] == 'L':
                        d = (d - 1) % 4
                    elif grid[x][y] == 'R':
                        d = (d + 1) % 4
                    dx, dy = directions[d]
                    x, y = (x + dx) % rows, (y + dy) % cols
                answer.append(length)
    return sorted(answer)
```

## 정답이 되는 이유

각 상태는 후속 상태 하나와 이전 상태 하나를 가집니다. 따라서 전체는 서로 겹치지 않는 순환들로 나뉘며, 방문 표시로 각 순환을 한 번만 셉니다.

시간 O(RC+I log I), 공간 O(RC) / Time O(RC+I log I), space O(RC); I=사이클 수 / cycle count

주의할 점: 같은 칸이라도 방향이 다르면 다른 상태입니다. 1행·1열 격자도 나머지 연산으로 처리합니다.

## 다른 방법: 상태 전이 간선을 분리 집합으로 합치기

```python
from collections import Counter

def solution(grid):
    rows,cols=len(grid),len(grid[0])
    count=rows*cols*4
    parent=list(range(count))
    size=[1]*count
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]
            x=parent[x]
        return x
    direction=((-1,0),(0,1),(1,0),(0,-1))
    for r in range(rows):
        for c in range(cols):
            for d in range(4):
                nd=(d+{'L':-1,'R':1,'S':0}[grid[r][c]])%4
                dr,dc=direction[nd]
                a=find((r*cols+c)*4+d)
                b=find((((r+dr)%rows)*cols+(c+dc)%cols)*4+nd)
                if a!=b:
                    if size[a]<size[b]: a,b=b,a
                    parent[b]=a
                    size[a]+=size[b]
    return sorted(Counter(find(i) for i in range(count)).values())
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 상태를 칸과 들어온 방향의 쌍으로 잡습니다. 지시대로 방향을 바꾸고 반대편으로 감아 이동합니다. 방문하지 않은 상태에서 출발해 다시 방문한 상태까지 길이를 셉니다. | 상태 전이 간선을 분리 집합으로 합치기 |
| 비용 | 시간 O(RC+I log I), 공간 O(RC) / Time O(RC+I log I), space O(RC); I=사이클 수 / cycle count | 시간 O(RC α(RC)+I log I), 공간 O(RC) / Time O(RC α(RC)+I log I), space O(RC) |

## 검증

공식 예제 3개와 생성 입력 60개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다. 제한 상한에 해당하는 크기·수치의 경계 검사도 저장된 테스트에 포함했습니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Find the lengths of all light-path cycles in a wrapping grid with straight, left and right instructions.

### Conditions and input/output

Input arguments: `grid`. The return value is a numeric list satisfying the task described below.

- 1 ≤ rows,columns ≤ 500; characters L,R,S; wrapping boundaries

### Approach

Use cell plus incoming direction as a state. Turn according to the cell, move with wraparound, and count steps until revisiting a state.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Every state has exactly one successor and one predecessor. The state space is a disjoint union of cycles, each counted once by visitation.

시간 O(RC+I log I), 공간 O(RC) / Time O(RC+I log I), space O(RC); I=사이클 수 / cycle count

Boundary cases: Different directions at one cell are different states. Modulo wrapping also handles one-row and one-column grids.

### Alternative: Union successor states with disjoint-set union

시간 O(RC α(RC)+I log I), 공간 O(RC) / Time O(RC α(RC)+I log I), space O(RC)

### Verification

Local checks covered 3 official examples and 60 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases. Saved tests also include a size or numeric boundary at the stated upper limit.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 빛의 경로 사이클](https://school.programmers.co.kr/learn/courses/30/lessons/86052) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
