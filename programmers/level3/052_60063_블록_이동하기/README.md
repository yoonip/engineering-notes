# 블록 이동하기

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

Level 3 · [60063 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/60063)

## 문제와 조건

두 칸 로봇을 이동·회전해 어느 한 칸이 목표에 닿는 최소 시간을 구합니다. 각 이동·회전은 1초입니다.

로봇은 처음 가로로 놓이고 항상 목표에 도달할 수 있습니다. 회전 중 휩쓰는 칸도 비어야 합니다.

`5≤N≤100; entries∈{0,1}; start=(1,1),(1,2)`

## 풀이를 따라가기

1. 로봇의 두 칸 전체를 하나의 상태로 BFS합니다. 평행 이동 네 방향과 두 칸 각각을 축으로 한 회전을 검사합니다.
2. 회전은 도착 칸뿐 아니라 지나가는 대각선 공간도 비어 있어야 합니다. 예제에서는 이동·회전 7번으로 도착합니다.
3. 로봇 위치와 방향의 상태 수가 O(N²)이므로 시간·공간 O(N²).

## 왜 이 방법으로 풀 수 있나

로봇의 두 칸 전체를 하나의 상태로 BFS합니다. 평행 이동 네 방향과 두 칸 각각을 축으로 한 회전을 검사합니다.

시간·공간: 시간·공간 O(N²).

## 다른 방법과 비교

두 좌표 집합 대신 로봇의 왼쪽·위쪽 기준 칸과 가로·세로 방향을 저장합니다. 회전 시 두 칸이 휩쓰는 2×2 영역이 비었는지 확인합니다.

| 항목 | 기본 풀이 | 기준 칸과 방향 상태 BFS |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간·공간 O(N²). | O(N²), 공간 O(N²) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[[[0, 0, 0, 1, 1], [0, 0, 0, 1, 0], [0, 1, 0, 1, 1], [1, 1, 0, 0, 1], [0, 0, 0, 0, 0]]]` | `7` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Minimize unit-time translations and rotations until either cell of the two-cell robot reaches the goal.

The robot starts horizontally and is guaranteed to reach the goal. Swept cells must be empty during rotation.

`5≤N≤100; entries∈{0,1}; start=(1,1),(1,2)`

### Method and correctness

BFS states contain both robot cells in canonical order. Try four translations and rotations around either cell. A rotation is legal only if the full swept corner space is empty, not merely its destination. Unit-cost BFS returns the minimum number of moves and rotations to reach the goal with either cell.

Main complexity: O(N²) time and space.

### Alternative and trade-offs

Represent a robot by its upper/left anchor and horizontal/vertical orientation rather than a pair of cells. Every rotation requires the swept 2×2 region to be empty.

Code: [alternative.py](alternative.py).

Complexity: O(N²), space O(N²).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 블록 이동하기](https://school.programmers.co.kr/learn/courses/30/lessons/60063) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 41개 입력에서 82회 검사를 통과했습니다.

Passed 82 implementation checks across 41 official, boundary and fixed-seed differential inputs.
