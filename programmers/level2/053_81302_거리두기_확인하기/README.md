# 거리두기 확인하기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/81302) · Level 2 · Python3

각 5×5 대기실의 모든 응시자가 파티션을 고려한 거리두기를 지키는지 확인한다.

## 조건과 입출력

입력 매개변수: `places`. 반환값은 수치 배열이며 아래 풀이의 조건을 만족하는 결과다.



## 풀이를 따라가기

응시자 쌍의 맨해튼 거리를 확인한다. 거리 1은 바로 위반이다. 거리 2는 일직선 가운데 칸 또는 대각선의 두 중간 칸이 파티션인지 검사한다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
from itertools import combinations

def solution(places):
    def valid(room):
        people = [(r, c) for r in range(5) for c in range(5) if room[r][c] == 'P']
        for (r1, c1), (r2, c2) in combinations(people, 2):
            distance = abs(r1 - r2) + abs(c1 - c2)
            # 바로 이웃한 응시자는 무조건 위반이다.
            if distance == 1:
                return 0
            if distance == 2:
                if r1 == r2:
                    if room[r1][(c1 + c2) // 2] != 'X':
                        return 0
                elif c1 == c2:
                    if room[(r1 + r2) // 2][c1] != 'X':
                        return 0
                # 대각선은 두 짧은 경로를 모두 파티션으로 막아야 한다.
                elif room[r1][c2] != 'X' or room[r2][c1] != 'X':
                    return 0
        return 1
    return [valid(room) for room in places]
```

## 왜 맞는가

거리 2 이하인 가장 짧은 경로는 일직선이면 하나, 대각선이면 둘이다. 모든 짧은 경로가 파티션에 막힌 경우만 허용하므로 조건과 일치한다.

고정 5×5 입력에서 O(1), 일반화하면 방마다 O(P²) / O(1) for fixed rooms; O(P²) per room when generalized

주의할 점: 대각선에서는 중간 칸 둘 다 X여야 한다. 한쪽만 막혀 있으면 다른 짧은 경로가 남는다.

## 다른 방법: 응시자별 깊이 2 BFS

기본 풀이와 같은 결과를 구하되 중간 상태와 계산 방식이 다르다.

```python
from collections import deque

def solution(places):
    def valid(room):
        for r in range(5):
            for c in range(5):
                if room[r][c]!='P': continue
                queue=deque([(r,c,0)])
                seen={(r,c)}
                while queue:
                    x,y,d=queue.popleft()
                    if d==2: continue
                    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                        nx,ny=x+dx,y+dy
                        if 0<=nx<5 and 0<=ny<5 and (nx,ny) not in seen and room[nx][ny]!='X':
                            if room[nx][ny]=='P': return 0
                            seen.add((nx,ny))
                            queue.append((nx,ny,d+1))
        return 1
    return [valid(room) for room in places]
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 응시자 쌍의 맨해튼 거리를 확인한다. 거리 1은 바로 위반이다. 거리 2는 일직선 가운데 칸 또는 대각선의 두 중간 칸이 파티션인지 검사한다. | 응시자별 깊이 2 BFS |
| 비용 | 고정 5×5 입력에서 O(1), 일반화하면 방마다 O(P²) / O(1) for fixed rooms; O(P²) per room when generalized | 방마다 O(P)개의 상수 크기 탐색, 공간 O(1) / O(P) constant-size searches per room, space O(1) |

## 검증

공식 예제 1개와 생성 입력 70개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Check whether every participant in each 5-by-5 room follows distancing rules with partitions.

### Conditions and input/output

Input arguments: `places`. The return value is a numeric list satisfying the task described below.

- 5 rooms, each 5×5; characters P,O,X
- return one validity flag per room

### Approach

Check Manhattan distance for every participant pair. Distance one is a violation. At distance two, test the middle cell for aligned pairs or both intermediate cells for diagonals.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

There is one shortest path for aligned distance-two pairs and two for diagonal pairs. The rule permits them exactly when all such short paths are blocked.

고정 5×5 입력에서 O(1), 일반화하면 방마다 O(P²) / O(1) for fixed rooms; O(P²) per room when generalized

Boundary cases: Both intermediate diagonal cells must be X. Blocking only one leaves another short path.

### Alternative: Depth-two BFS from each participant

It computes the same result using different intermediate states or evaluation steps. 방마다 O(P)개의 상수 크기 탐색, 공간 O(1) / O(P) constant-size searches per room, space O(1)

The main approach follows the steps described above. The alternative uses depth-two bfs from each participant; compare its intermediate state and cost with the main implementation before choosing it.

### Verification

Local checks covered 1 official examples and 70 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 거리두기 확인하기](https://school.programmers.co.kr/learn/courses/30/lessons/81302) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
