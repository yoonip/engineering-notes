# 몸짱 트레이너 라이언의 고민

Level 3 · [1838 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/1838)

## 문제와 조건

예약이 겹치는 손님들에게 락커를 배정할 때 가장 가까운 두 손님의 맨해튼 거리를 최대화합니다. 예약 종료 시각도 사용 중이며 이용이 겹치지 않으면 0입니다.

`1≤n≤10; 0≤m≤1,000; 600≤start<end≤1,320; simultaneous users≤n²`

## 풀이를 따라가기

1. 예약 구간의 양 끝을 포함해 최대 동시 인원 K를 센다. K개의 충분히 떨어진 락커를 준비하면 예약은 빈 락커로 배정할 수 있다.
2. 거리를 큰 값부터 내리며 첫 행의 시작 열을 바꾼 행 우선 배치를 검사한다. 첫 모서리만 쓰면 n=4,K=3의 거리 4 배치를 놓칠 수 있다.
3. 거리 후보 O(N), 시작 열 O(N), 칸 O(N²), 거리 비교 O(N²)로 상한 O(N⁶). N≤10이며 인원을 채우면 즉시 종료한다.

## 배치의 유효성과 확인 범위

예약 구간의 양 끝을 포함해 최대 동시 인원 K를 센다. K개의 충분히 떨어진 락커를 준비하면 예약은 빈 락커로 배정할 수 있다.

각 후보 배치는 모든 선택된 락커 쌍의 거리를 검사합니다. 시작점을 바꾸는 행 우선 배치는 저장된 100점 제출 구현이며, 작은 격자는 모든 락커 부분집합을 조사하는 정확 탐색과 대조합니다. 이 대조를 일반 격자 최적성의 증명으로 대신하지는 않습니다.

시간·공간: 후보 거리·시작 열·칸·기존 배치를 모두 비교하는 상한 O(n^6), 보조 공간 O(n²)

## 다른 방법과 비교

예약을 직접 세어 최대 동시 인원을 구한 뒤, 작은 격자에서 그 수만큼 락커를 고르는 모든 조합의 최소 맨해튼 거리를 비교합니다. 배치 탐욕의 작은 격자 기준값입니다.

| 항목 | 기본 풀이 | 락커 부분집합 정확 탐색 |
|---|---|---|
| 코드 | [solution.cpp](solution.cpp) | [alternative.py](alternative.py) |
| 비용 | 후보 거리·시작 열·칸·기존 배치를 모두 비교하는 상한 O(n^6), 보조 공간 O(n²) | O(조합(n²,K)·K²), 작은 격자 비교용 |
| 용도 | 기본 제출 구현 | 작은 입력 비교·검증용 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[3, 2, [[1170, 1210], [1200, 1260]]]` | `4` |
| `[2, 1, [[840, 900]]]` | `0` |
| `[2, 2, [[600, 630], [630, 700]]]` | `2` |
| `[4, 5, [[1140, 1200], [1150, 1200], [1100, 1200], [1210, 1300], [1220, 1280]]]` | `4` |

Python 대안은 examples.json과 별도 경계·무작위 입력으로 로컬 검증합니다. C++ 제출본의 실행 결과는 전체 검증 기록에서 구분합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.cpp)

## English

### Task and constraints

Assign lockers to maximize the minimum Manhattan distance between simultaneous users. Reservation end times are inclusive; return zero if no bookings overlap.

`1≤n≤10; 0≤m≤1,000; 600≤start<end≤1,320; simultaneous users≤n²`

### Method and verification scope

Count the maximum concurrent reservations with closed endpoints: a booking ending at t overlaps one starting at t. For each candidate Manhattan distance from largest to smallest, try row-major placements with every first-row offset. A feasible placement for the peak concurrent users supplies enough separated lockers; return zero when peak occupancy is at most one.

Main complexity: O(n^6) loose upper bound for candidate placements; n≤10.

Each candidate explicitly checks all chosen locker-pair distances. The row-major placement is the saved 100-point implementation; exact subset enumeration cross-checks tiny grids. These checks are not a general optimality proof.

### Alternative and trade-offs

Count concurrent closed booking intervals directly, then enumerate every locker subset of that size on a tiny grid and maximize its minimum Manhattan distance. This is an exact tiny-grid oracle for the placement heuristic.

Code: [alternative.py](alternative.py). Scope: tiny-input oracle; not for maximum-size submissions.

Complexity: O(C(n²,K)·K²), tiny-grid oracle.

### Verification

The Python alternative is checked with examples.json and separate edge/random cases; C++ execution is recorded separately in the repository validation report.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 몸짱 트레이너 라이언의 고민](https://school.programmers.co.kr/learn/courses/30/lessons/1838) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 34개 입력에서 34회 검사를 통과했습니다.

Passed 34 implementation checks across 34 official, boundary and fixed-seed differential inputs.

[Python 비교 원본 / Stored Python comparison source](submitted_original.py)
