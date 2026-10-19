# 상담원 인원

Level 3 · [214288 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/214288)

## 문제와 조건

유형이 정해진 상담원 n명을 k개 상담 유형에 나눠 배치해 모든 참가자의 대기시간 합을 최소화합니다. 유형별로 최소 한 명이 필요합니다.

요청은 시작 시각순이고 시각이 중복되지 않습니다. [시작, 소요시간, 유형]별 대기시간 합을 최소화합니다.

`1≤k≤5; k≤n≤20; 3≤len(reqs)≤300; 1≤start≤1,000; 1≤duration≤100; 1≤type≤k`

## 풀이를 따라가기

1. 유형별로 멘토 수를 1명부터 늘려가며 대기 요청 R개, 유형 k개, 인원 n명에서 시간 O(R(n−k+1) log n+kn²), 보조 공간 O(R+n)
2. 이후 유형을 하나씩 추가하는 DP로 총 n명을 나눠 배정합니다. 각 유형에 최소 한 명을 배치합니다. 요청 수 R일 때 시간 O(R(n-k+1) log n+kn²), 공간 O(R+kn).
3. 예: 첫 예제는 유형별 2·1·2명으로 배치하면 대기 합이 5+20+0=25로 최소입니다.

## 왜 이 방법으로 풀 수 있나

유형별로 멘토 수를 1명부터 늘려가며 대기 요청 R개, 유형 k개, 인원 n명에서 시간 O(R(n−k+1) log n+kn²), 보조 공간 O(R+n)

시간·공간: 요청 R개, 유형 k개, 인원 n명에서 시간 O(R(n−k+1) log n+kn²), 보조 공간 O(R+n)

## 다른 방법과 비교

각 유형에 적어도 한 명씩 배정하는 모든 분배를 탐색합니다. 대기시간은 작은 배열의 최솟값으로 계산합니다. 기본 DP보다 느리지만 분배 누락을 확인하기 쉽습니다.

| 항목 | 기본 풀이 | 인원 분배 완전탐색 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 요청 R개, 유형 k개, 인원 n명에서 시간 O(R(n−k+1) log n+kn²), 보조 공간 O(R+n) | O(조합(n-1,k-1)·R·n), 작은 입력 비교용 |
| 용도 | 기본 제출 구현 | 작은 입력 비교·검증용 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[3, 5, [[10, 60, 1], [15, 100, 3], [20, 30, 1], [30, 50, 3], [50, 40, 1], [60, 30, 2], [65, 30, 1], [70, 100, 2]]]` | `25` |
| `[2, 3, [[5, 55, 2], [10, 90, 2], [20, 40, 2], [50, 45, 2], [100, 50, 2]]]` | `90` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Allocate n mentors across k fixed consultation types to minimize total waiting time, assigning at least one mentor to every type.

Requests [start,duration,type] have distinct sorted start times. Minimize total waiting time.

`1≤k≤5; k≤n≤20; 3≤len(reqs)≤300; 1≤start≤1,000; 1≤duration≤100; 1≤type≤k`

### Method and correctness

First simulate each consultation type with every feasible staff count. A min-heap always assigns the next request to the earliest available mentor. Then allocate staff across types by DP: dp[u] is the minimum total waiting time after allocating u mentors to the processed types. Every type receives at least one mentor. Taking every feasible split guarantees that the minimum allocation is included.

Main complexity: O(R(n−k+1) log n + kn²) time, O(R+n) working space.

### Alternative and trade-offs

Enumerate every positive staff allocation and simulate each type with an availability array. It is slower than the allocation DP, but independently checks that every allocation is covered.

Code: [alternative.py](alternative.py). Scope: tiny-input oracle; not for maximum-size submissions.

Complexity: O(C(n-1,k-1)·R·n), small-input checking.

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 상담원 인원](https://school.programmers.co.kr/learn/courses/30/lessons/214288) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 43개 입력에서 86회 검사를 통과했습니다.

Passed 86 implementation checks across 43 official, boundary and fixed-seed differential inputs.
