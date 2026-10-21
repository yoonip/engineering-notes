# 외벽 점검

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

Level 3 · [60062 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/60062)

## 문제와 조건

원형 외벽의 취약점을 시계·반시계 방향으로 점검할 때 주어진 거리의 친구를 최소 몇 명 투입해야 하는지 구합니다.

취약점은 중복 없이 정렬되어 있습니다. 친구를 전부 써도 불가능하면 −1입니다.

`1≤n≤200; 1≤W≤15; 0≤weak[i]<n; 1≤F≤8; 1≤dist[i]≤100`

## 풀이를 따라가기

1. 원을 두 배로 펼쳐 시작 취약점·친구 순서를 모두 시도합니다. 각 친구는 첫 미점검 취약점부터 최대한 멀리 점검합니다.
2. 반시계로 덮는 구간도 반대 끝에서 시계로 덮을 수 있으므로 시계 방향만 검사해도 됩니다. 같은 인원에서는 긴 거리 친구를 쓰는 것이 불리하지 않습니다.
3. 예제 1은 10→1과 5→6을 두 명이 담당합니다. 취약점 W≤15, 친구 F≤8일 때 시간 O(F!·W²), 공간 O(F!·F+W).

## 왜 이 방법으로 풀 수 있나

원을 두 배로 펼쳐 시작 취약점·친구 순서를 모두 시도합니다. 각 친구는 첫 미점검 취약점부터 최대한 멀리 점검합니다.

시간·공간: 시간 O(F!·W²), 공간 O(F!·F+W).

## 다른 방법과 비교

원형의 시작점을 고정하고 사용한 친구 집합마다 덮은 가장 먼 취약점 인덱스를 저장합니다. 같은 친구 집합에서는 더 멀리 덮은 상태만 남깁니다.

| 항목 | 기본 풀이 | 친구 부분집합 도달 DP |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(F!·W²), 공간 O(F!·F+W). | O(W²F2^F), 공간 O(2^F+W) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[12, [1, 5, 6, 10], [1, 2, 3, 4]]` | `2` |
| `[12, [1, 3, 4, 9, 10], [3, 5, 7]]` | `1` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Use the fewest friends with given travel limits to inspect all circular-wall weak points, in either direction.

Weak points are sorted and distinct. Return −1 if even all friends are insufficient.

`1≤n≤200; 1≤W≤15; 0≤weak[i]<n; 1≤F≤8; 1≤dist[i]≤100`

### Method and correctness

Duplicate weak points with a circumference offset to unwrap the circle. Try each start and each ordering of the chosen friends, greedily letting each cover from the first uncovered point as far as possible. For a fixed number of friends, using the longest ranges cannot hurt. Test counts in increasing order and return the first feasible count.

Main complexity: O(F! W²) time, O(F!F+W) space for materialized permutations.

### Alternative and trade-offs

For each circular starting point, store the farthest covered weak-point index for every subset of used friends. For a fixed subset, farther coverage dominates shorter coverage.

Code: [alternative.py](alternative.py).

Complexity: O(W²F2^F), space O(2^F+W).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 외벽 점검](https://school.programmers.co.kr/learn/courses/30/lessons/60062) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 43개 입력에서 86회 검사를 통과했습니다.

Passed 86 implementation checks across 43 official, boundary and fixed-seed differential inputs.
