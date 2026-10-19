# 코딩 테스트 공부

Level 3 · [118668 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/118668)

## 문제와 조건

공부와 해결 가능한 문제 풀이를 반복해 모든 문제의 요구 능력 이상이 되는 최소 시간을 구합니다. 같은 문제를 여러 번 풀어도 됩니다.

`0≤alp,cop,alp_req,cop_req≤150; 1≤P≤100; 0≤alp_rwd,cop_rwd≤30; 1≤cost≤100`

## 풀이를 따라가기

1. 모든 문제를 실제로 풀 필요는 없고, 알고력·코딩력이 각각 최대 요구치 이상이면 끝입니다. 공부와 문제 풀이를 같은 종류의 행동으로 처리합니다.
2. 능력은 감소하지 않으므로 작은 능력 상태부터 DP를 갱신합니다. 목표 이상의 능력은 하나로 묶습니다. 목표 능력 A·C와 문제 수 P에 대해 시간 O(AC(P+2)), 공간 O(AC).
3. 예: 이미 모든 요구치 이상이면 초기 상태가 목표이므로 추가 시간 0입니다. 같은 문제를 반복해 능력을 올리는 선택도 DP에 자연스럽게 포함됩니다.

## 왜 이 방법으로 풀 수 있나

모든 문제를 실제로 풀 필요는 없고, 알고력·코딩력이 각각 최대 요구치 이상이면 끝입니다. 공부와 문제 풀이를 같은 종류의 행동으로 처리합니다.

시간·공간: 시간 O(AC(P+2)), 공간 O(AC).

## 다른 방법과 비교

능력 쌍을 정점으로, 공부와 문제 풀이를 간선으로 만듭니다. 목표 능력에서 값을 자르는 규칙은 같고, 작은 능력 순서 대신 최소 시간 순서로 탐색합니다.

| 항목 | 기본 풀이 | 능력 상태 다익스트라 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(AC(P+2)), 공간 O(AC). | O(AC(P+2) log(AC)), 공간 O(AC) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[10, 10, [[10, 15, 2, 1, 2], [20, 20, 3, 3, 4]]]` | `15` |
| `[0, 0, [[0, 0, 2, 1, 2], [4, 5, 3, 1, 2], [4, 11, 4, 0, 2], [10, 4, 0, 4, 2]]]` | `13` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Minimize study and practice time until both skills meet every problem requirement. A problem may be solved repeatedly.

`0≤alp,cop,alp_req,cop_req≤150; 1≤P≤100; 0≤alp_rwd,cop_rwd≤30; 1≤cost≤100`

### Method and correctness

The goal is to reach the maximum required algorithm and coding skills; solving every problem is unnecessary. Add one-hour single-skill study actions to the available problems. Cap skills at the goal and update a two-dimensional minimum-time DP in increasing skill order. Since skills never decrease, every relevant transition is covered; a no-gain problem cannot improve a positive-cost state.

Main complexity: O(AC(P+2)) time, O(AC) space.

### Alternative and trade-offs

Use skill pairs as vertices and study/problem actions as edges. Both versions cap skills at their targets, but Dijkstra expands by elapsed time rather than by skill coordinates.

Code: [alternative.py](alternative.py). Scope: alternative implementation.

Complexity: O(AC(P+2) log(AC)), space O(AC).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 코딩 테스트 공부](https://school.programmers.co.kr/learn/courses/30/lessons/118668) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 43개 입력에서 86회 검사를 통과했습니다.

Passed 86 implementation checks across 43 official, boundary and fixed-seed differential inputs.
