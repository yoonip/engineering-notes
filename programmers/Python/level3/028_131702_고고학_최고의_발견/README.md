# 고고학 최고의 발견

Level 3 · [131702 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/131702)

## 문제와 조건

시계를 한 번 돌리면 자신과 상하좌우가 90도 돌아갑니다. 모든 시계를 12시 방향으로 맞추는 최소 회전 횟수를 구합니다.

`2≤N≤8; board=N×N; clockHands[r][c]∈{0,1,2,3}`

## 풀이를 따라가기

1. 첫 행의 회전 횟수만 0~3으로 모두 정하면, 각 행을 0으로 맞추기 위한 다음 행의 회전 횟수가 강제로 결정됩니다.
2. 원래 방향과 위·현재·좌우 회전의 합을 4의 배수로 만드는 아래쪽 회전을 구합니다. 마지막 행에서 아래쪽 회전이 전부 0이어야 유효합니다. 시간 O(4^N N²), 추가 공간 O(N).
3. 예: 위 칸에 남은 방향이 3이면 그 아래 시계를 한 번 돌려 위 칸을 0으로 만듭니다. 아래 행들은 이 선택을 순서대로 따라가므로 첫 행만 전수 탐색하면 됩니다.

## 왜 이 방법으로 풀 수 있나

첫 행의 회전 횟수만 0~3으로 모두 정하면, 각 행을 0으로 맞추기 위한 다음 행의 회전 횟수가 강제로 결정됩니다.

시간·공간: 시간 O(4^N N²), 추가 공간 O(N).

## 다른 방법과 비교

모든 칸의 회전 횟수를 직접 적용해 마지막 보드를 확인합니다. 첫 행만 정하면 나머지가 강제된다는 성질을 독립적으로 검사합니다. 2×2 같은 작은 보드에만 사용합니다.

| 항목 | 기본 풀이 | 전체 회전 조합 직접 적용 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(4^N N²), 추가 공간 O(N). | O(4^(N²)N²), 작은 보드 비교용 |
| 용도 | 기본 제출 구현 | 작은 입력 비교·검증용 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[[[0, 3, 3, 0], [3, 2, 2, 3], [0, 3, 2, 0], [0, 3, 3, 3]]]` | `3` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

One rotation turns a clock and its four orthogonal neighbors by 90 degrees. Minimize rotations until all clocks point up.

`2≤N≤8; board=N×N; clockHands[r][c]∈{0,1,2,3}`

### Method and correctness

Enumerate only the first row’s rotation counts, each from zero to three. Once the current row is known, the next row’s rotations are forced to cancel every clock immediately above it modulo four. Continue downwards; the last row must require no rotations below the board. Every complete solution has one enumerated first row, so the minimum valid cost is found.

Main complexity: O(4^N N²) time, O(N) auxiliary space.

### Alternative and trade-offs

Apply every cell-rotation combination directly and check the final board. This independently verifies the forced-row deduction, and is only practical on tiny boards such as 2×2.

Code: [alternative.py](alternative.py). Scope: tiny-input oracle; not for maximum-size submissions.

Complexity: O(4^(N²)N²), small-board checking.

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 고고학 최고의 발견](https://school.programmers.co.kr/learn/courses/30/lessons/131702) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 12개 입력에서 23회 검사를 통과했습니다.

Passed 23 implementation checks across 12 official, boundary and fixed-seed differential inputs.
