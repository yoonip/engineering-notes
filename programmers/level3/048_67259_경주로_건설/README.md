# 경주로 건설

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

Level 3 · [67259 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/67259)

## 문제와 조건

벽을 피한 도로의 직선 한 칸 비용은 100원, 방향 전환 추가 비용은 500원입니다. 출발점부터 도착점까지 최소 건설비를 구합니다.

`3≤N≤25; board=N×N; entries∈{0,1}; board[0][0]=board[N−1][N−1]=0`

## 풀이를 따라가기

1. 같은 칸이라도 들어온 방향에 따라 다음 코너 비용이 달라집니다. (행,열,방향)을 각각 다른 상태로 두고 다익스트라를 실행합니다.
2. 예: 빈 3×3은 직선 4개와 코너 1개로 400+500=900원. 최소 이동 횟수 경로가 최소 건설 비용 경로와 항상 같지는 않습니다.
3. 즉시 되돌아가는 경로는 양수 비용만 늘려 최적 경로에 필요하지 않습니다. 시간 O(N² log N), 공간 O(N²).

## 왜 이 방법으로 풀 수 있나

같은 칸이라도 들어온 방향에 따라 다음 코너 비용이 달라집니다. (행,열,방향)을 각각 다른 상태로 두고 다익스트라를 실행합니다.

시간·공간: 시간 O(N² log N), 공간 O(N²).

## 다른 방법과 비교

방향을 포함한 모든 상태의 거리를 반복해서 완화합니다. 비용이 서로 달라 단순 BFS 최초 방문으로 확정할 수 없다는 점을 보여줍니다. 힙보다 느린 작은 보드 검증용입니다.

| 항목 | 기본 풀이 | 방향 상태 반복 완화 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(N² log N), 공간 O(N²). | 최악 O(N⁴), 공간 O(N²), 작은 보드 비교용 |
| 용도 | 기본 제출 구현 | 작은 입력 비교·검증용 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[[[0, 0, 0], [0, 0, 0], [0, 0, 0]]]` | `900` |
| `[[[0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0, 1, 0], [0, 1, 0, 0, 0, 1, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0]]]` | `3800` |
| `[[[0, 0, 1, 0], [0, 0, 0, 0], [0, 1, 0, 1], [1, 0, 0, 0]]]` | `2100` |
| `[[[0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 0], [0, 0, 1, 0, 0, 0], [1, 0, 0, 1, 0, 1], [0, 1, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0]]]` | `3200` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Build a road around walls with 100 per step and an additional 500 per turn, minimizing total cost to the destination.

`3≤N≤25; board=N×N; entries∈{0,1}; board[0][0]=board[N−1][N−1]=0`

### Method and correctness

The arrival direction is part of the state because it determines whether the next edge creates a corner. Dijkstra adds 100 for each step and another 500 for a direction change. Initialize all start directions at zero so the first move has no artificial corner cost. Take the smallest destination cost across directions.

Main complexity: O(N² log N) time, O(N²) space.

### Alternative and trade-offs

Repeatedly relax all directional states. Unequal edge costs mean first-visit BFS is insufficient; this slower Bellman–Ford-style method checks the heap solution on small boards.

Code: [alternative.py](alternative.py). Scope: tiny-input oracle; not for maximum-size submissions.

Complexity: worst case O(N⁴), space O(N²), small-board checking.

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 경주로 건설](https://school.programmers.co.kr/learn/courses/30/lessons/67259) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 45개 입력에서 90회 검사를 통과했습니다.

Passed 90 implementation checks across 45 official, boundary and fixed-seed differential inputs.
