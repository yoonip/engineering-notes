# 보행자 천국

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

Level 3 · [1832 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/1832)

## 문제와 조건

오른쪽·아래로만 이동하고 벽·직진 전용 교차로 조건을 지키며 출발점에서 도착점까지 가는 경로 수를 구합니다.

`1≤m,n≤500; city_map[r][c]∈{0,1,2}; modulus=20170805`

## 풀이를 따라가기

1. vertical[c]는 위에서 내려온 경로 수, horizontal은 왼쪽에서 온 경로 수입니다. 자유 통행 칸에서는 두 수를 합쳐 어느 방향으로도 출발할 수 있습니다.
2. 벽에서는 두 수를 0으로 만들고, 직진 전용 칸에서는 두 수를 섞지 않고 그대로 전달합니다. 예제 2는 방향 전환을 제한하면 두 경로만 남습니다.
3. 시작점 위에서 경로 하나가 들어온 것으로 초기화합니다. 시간 O(MN), 추가 공간 O(N).

## 왜 이 방법으로 풀 수 있나

vertical[c]는 위에서 내려온 경로 수, horizontal은 왼쪽에서 온 경로 수입니다. 자유 통행 칸에서는 두 수를 합쳐 어느 방향으로도 출발할 수 있습니다.

시간·공간: 시간 O(MN), 추가 공간 O(N).

## 다른 방법과 비교

각 칸에 위에서 온 수와 왼쪽에서 온 수를 따로 저장합니다. 직진 전용 칸을 떠날 때 방향을 유지하도록 검사합니다. 1차원 압축 전의 명시적 상태입니다.

| 항목 | 기본 풀이 | 방향별 2차원 DP |
|---|---|---|
| 코드 | [solution.cpp](solution.cpp) | [alternative.py](alternative.py) |
| 비용 | 시간 O(MN), 추가 공간 O(N). | O(MN), 공간 O(MN) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[3, 3, [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]` | `6` |
| `[3, 6, [[0, 2, 0, 0, 0, 2], [0, 0, 2, 0, 1, 0], [1, 0, 0, 2, 2, 0]]]` | `2` |

Python 대안은 examples.json과 별도 경계·무작위 입력으로 로컬 검증합니다. C++ 제출본의 실행 결과는 전체 검증 기록에서 구분합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.cpp)

## English

### Task and constraints

Count right/down routes obeying blocked and straight-only cells from start to destination.

`1≤m,n≤500; city_map[r][c]∈{0,1,2}; modulus=20170805`

### Method and correctness

Keep downward-arrival counts per column and one rightward count. At an unrestricted cell, combine both counts for either outgoing direction. At a wall, clear both; at a straight-only cell, keep directions separate. Initialize one path entering the start and reduce every merge modulo 20170805.

Main complexity: O(mn) time, O(n) extra space.

### Alternative and trade-offs

Keep separate incoming-down and incoming-right counts for every cell. A straight-only cell permits departure only in the incoming direction. This is an explicit 2D state model before memory compression.

Code: [alternative.py](alternative.py).

Complexity: O(MN), space O(MN).

### Verification

The Python alternative is checked with examples.json and separate edge/random cases; C++ execution is recorded separately in the repository validation report.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 보행자 천국](https://school.programmers.co.kr/learn/courses/30/lessons/1832) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 32개 입력에서 32회 검사를 통과했습니다.

Passed 32 implementation checks across 32 official, boundary and fixed-seed differential inputs.

[Python 비교 원본 / Stored Python comparison source](submitted_original.py)
