# 공 이동 시뮬레이션

Level 3 · [87391 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/87391)

## 문제와 조건

벽에 막히면 그 자리에 멈추는 이동 명령을 모두 적용해 목표 칸에 도착하는 시작 칸의 수를 구합니다.

`1≤n,m≤10^9; 0≤x<n; 0≤y<m; 1≤Q≤200,000; command∈{0,1,2,3}; 1≤distance≤10^9`

## 풀이를 따라가기

1. 10억×10억 격자를 직접 돌리지 않고 목표 한 점에서 명령을 역순으로 적용해 가능한 시작 구간을 확장·이동합니다.
2. 벽에 막혀 같은 좌표에 모일 수 있으므로 후보 구간이 0 또는 마지막 경계를 포함할 때 해당 끝을 그대로 둡니다. 빈 구간이면 0입니다. 시간 O(Q), 추가 공간 O(1).
3. 예: 마지막 열이 0이고 직전에 왼쪽으로 3칸 이동했다면 이전 열은 0~3 모두 가능하므로 역산 구간이 넓어집니다.

## 왜 이 방법으로 풀 수 있나

10억×10억 격자를 직접 돌리지 않고 목표 한 점에서 명령을 역순으로 적용해 가능한 시작 구간을 확장·이동합니다.

시간·공간: 시간 O(Q), 추가 공간 O(1).

## 다른 방법과 비교

작은 격자의 모든 시작점을 움직여 목표에 도착한 수를 셉니다. 벽에서 좌표가 합쳐지는 역연산을 실제 이동과 대조합니다.

| 항목 | 기본 풀이 | 모든 시작점 정방향 시뮬레이션 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(Q), 추가 공간 O(1). | O(NMQ), 작은 격자 비교용 |
| 용도 | 기본 제출 구현 | 작은 입력 비교·검증용 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[2, 2, 0, 0, [[2, 1], [0, 1], [1, 1], [0, 1], [2, 1]]]` | `4` |
| `[2, 5, 0, 1, [[3, 1], [2, 2], [1, 1], [2, 3], [0, 1], [2, 1]]]` | `2` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Count starting cells whose clamped grid movements end at the target.

`1≤n,m≤10^9; 0≤x<n; 0≤y<m; 1≤Q≤200,000; command∈{0,1,2,3}; 1≤distance≤10^9`

### Method and correctness

Work backwards from the target point, maintaining an interval for each independent axis. Reverse a clamped move by shifting the interval, but keep an endpoint pinned when it includes the wall where several earlier positions could collapse. Clip to the grid and stop if an interval becomes empty. The product of the final interval lengths counts starting cells.

Main complexity: O(Q) time, O(1) extra space.

### Alternative and trade-offs

Simulate every starting cell on a tiny grid and count arrivals at the target. This checks reverse interval expansion against actual clamped movements.

Code: [alternative.py](alternative.py). Scope: tiny-input oracle; not for maximum-size submissions.

Complexity: O(NMQ), tiny-grid oracle.

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 공 이동 시뮬레이션](https://school.programmers.co.kr/learn/courses/30/lessons/87391) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 43개 입력에서 86회 검사를 통과했습니다.

Passed 86 implementation checks across 43 official, boundary and fixed-seed differential inputs.
