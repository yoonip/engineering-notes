# 자물쇠와 열쇠

Level 3 · [60059 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/60059)

## 문제와 조건

열쇠를 90도씩 회전·이동하여 자물쇠의 모든 홈을 채우고 돌기 충돌을 피할 수 있는지 판정합니다.

`3≤M≤N≤20; key=M×M; lock=N×N; entries∈{0,1}`

## 풀이를 따라가기

1. 열쇠 돌기를 네 방향으로 회전하고 모든 겹치는 위치로 이동시킵니다. 자물쇠 안에 들어온 돌기 좌표 집합이 홈 좌표 집합과 같으면 열립니다.
2. 예제는 90도 회전 후 오른쪽·아래 한 칸씩 옮기면 두 홈을 채웁니다. 자물쇠 밖의 돌기는 비교에서 제외합니다.
3. 시간 O((N+M)²·M² + N²), 공간 O(N²+M²). N,M≤20이므로 모든 배치를 검사해도 충분합니다.

## 왜 이 방법으로 풀 수 있나

열쇠 돌기를 네 방향으로 회전하고 모든 겹치는 위치로 이동시킵니다. 자물쇠 안에 들어온 돌기 좌표 집합이 홈 좌표 집합과 같으면 열립니다.

시간·공간: 시간 O((N+M)²·M² + N²), 공간 O(N²+M²). N,M≤20이므로 모든 배치를 검사해도 충분합니다.

## 다른 방법과 비교

자물쇠 주변에 여백을 만들고 회전한 열쇠를 실제로 더합니다. 자물쇠 영역의 모든 합이 정확히 1인지 검사합니다. 좌표 집합 비교와 독립된 배열 구현입니다.

| 항목 | 기본 풀이 | 확장 보드 합 검사 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O((N+M)²·M² + N²), 공간 O(N²+M²). N,M≤20이므로 모든 배치를 검사해도 충분합니다. | O((N+M)²(N²+M²)), 공간 O((N+M)²) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[[[0, 0, 0], [1, 0, 0], [0, 1, 1]], [[1, 1, 1], [1, 1, 0], [1, 0, 1]]]` | `true` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Decide whether a rotated and translated key can fill every lock hole without protrusion collisions.

`3≤M≤N≤20; key=M×M; lock=N×N; entries∈{0,1}`

### Method and correctness

Extract lock holes and key protrusions as coordinates. Try four rotations and all overlapping translations. Ignore key protrusions outside the lock and require the remaining protrusion set to equal the hole set exactly. Equality simultaneously ensures every hole is filled and no protrusion collides with a lock protrusion.

Main complexity: O((N+M)²M²+N²) time, O(N²+M²) space.

### Alternative and trade-offs

Place the lock in a padded board and add each rotated key placement. Every lock cell must sum to exactly one, independently checking the coordinate-set formulation.

Code: [alternative.py](alternative.py).

Complexity: O((N+M)²(N²+M²)), space O((N+M)²).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 자물쇠와 열쇠](https://school.programmers.co.kr/learn/courses/30/lessons/60059) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 42개 입력에서 84회 검사를 통과했습니다.

Passed 84 implementation checks across 42 official, boundary and fixed-seed differential inputs.
