# GPS

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

Level 3 · [1837 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/1837)

## 문제와 조건

양 끝 거점은 고정한 채 GPS 기록의 최소 항목만 수정해 도로 이동·제자리 머물기와 맞는 기록으로 만듭니다. 불가능하면 −1입니다.

`2≤n≤200; 1≤m≤10,000; 2≤k≤100; vertex IDs∈[1,n]`

## 풀이를 따라가기

1. dp[v]는 현재 시각에 v에 있을 때 필요한 최소 GPS 수정 횟수입니다. 직전 시각에 같은 거점에 머물거나 인접 거점에서 이동한 경우 중 최소를 선택합니다.
2. 시작 거점만 비용 0으로 초기화하고 마지막에는 원래 도착 거점의 값만 반환해 양 끝을 고정합니다. 기록과 현재 거점이 다르면 수정 비용 1을 더합니다.
3. 예제 [1,2,3,3,6,7]은 네 번째 3을 5로 바꿔 한 번 수정합니다. 시간 O(K(N+M)), 공간 O(N+M).

## 왜 이 방법으로 풀 수 있나

dp[v]는 현재 시각에 v에 있을 때 필요한 최소 GPS 수정 횟수입니다. 직전 시각에 같은 거점에 머물거나 인접 거점에서 이동한 경우 중 최소를 선택합니다.

시간·공간: 시간 O(K(N+M)), 공간 O(N+M).

## 다른 방법과 비교

현재 시각과 거점을 상태로 두고 머물기·인접 이동을 모두 재귀 탐색합니다. 끝 기록은 고정합니다. 반복 DP와 달리 뒤에서 필요한 값만 계산합니다.

| 항목 | 기본 풀이 | 기록별 재귀 최단 수정 |
|---|---|---|
| 코드 | [solution.cpp](solution.cpp) | [alternative.py](alternative.py) |
| 비용 | 시간 O(K(N+M)), 공간 O(N+M). | O(K(N+M)), 공간 O(KN+N+M) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[7, 10, [[1, 2], [1, 3], [2, 3], [2, 4], [3, 4], [3, 5], [4, 6], [5, 6], [5, 7], [6, 7]], 6, [1, 2, 3, 3, 6, 7]]` | `1` |
| `[7, 10, [[1, 2], [1, 3], [2, 3], [2, 4], [3, 4], [3, 5], [4, 6], [5, 6], [5, 7], [6, 7]], 6, [1, 2, 4, 6, 5, 7]]` | `0` |

Python 대안은 examples.json과 별도 경계·무작위 입력으로 로컬 검증합니다. C++ 제출본의 실행 결과는 전체 검증 기록에서 구분합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.cpp)

## English

### Task and constraints

Correct the fewest GPS entries to form a valid road-or-stay route with fixed endpoints, returning −1 if impossible.

`2≤n≤200; 1≤m≤10,000; 2≤k≤100; vertex IDs∈[1,n]`

### Method and correctness

Let dp[v] be the fewest corrections at the current time when located at v. A transition may stay at v or arrive from an adjacent vertex, and adds one when v differs from the GPS log. Fix the first vertex initially and read only the original final vertex at the end. Return −1 if that final state is unreachable.

Main complexity: O(k(n+m)) time, O(n+m) space.

### Alternative and trade-offs

Memoize by time and current vertex, considering staying and every adjacent move. The final recorded vertex is fixed. This computes the recurrence on demand rather than layer by layer.

Code: [alternative.py](alternative.py).

Complexity: O(K(N+M)), space O(KN+N+M).

### Verification

The Python alternative is checked with examples.json and separate edge/random cases; C++ execution is recorded separately in the repository validation report.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: GPS](https://school.programmers.co.kr/learn/courses/30/lessons/1837) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 32개 입력에서 32회 검사를 통과했습니다.

Passed 32 implementation checks across 32 official, boundary and fixed-seed differential inputs.

[Python 비교 원본 / Stored Python comparison source](submitted_original.py)
