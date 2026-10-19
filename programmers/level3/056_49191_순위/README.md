# 순위

Level 3 · [49191 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/49191)

## 문제와 조건

주어진 승패와 추이 관계만으로 순위를 확정할 수 있는 선수 수를 구합니다.

`1≤n≤100; 1≤E≤4,500`

## 풀이를 따라가기

1. A가 B를 이기고 B가 C를 이기면 A도 C를 이긴다. 이 관계를 전부 전파한 뒤, 나머지 N-1명과 비교 가능한 선수만 센다.
2. 예제에서 2번은 세 명에게 지고 5번에게 이겨 4위, 5번은 모두에게 져 5위가 확정된다.
3. 순위는 자신보다 강한 선수 수+1이다. 시간 O(N³), 공간 O(N²). N≤100이라 삼중 반복문을 사용해도 된다.

## 왜 이 방법으로 풀 수 있나

A가 B를 이기고 B가 C를 이기면 A도 C를 이긴다. 이 관계를 전부 전파한 뒤, 나머지 N-1명과 비교 가능한 선수만 센다.

시간·공간: 시간 O(N³), 공간 O(N²). N≤100이라 삼중 반복문을 사용해도 된다.

## 다른 방법과 비교

각 선수에서 승리 방향과 패배 방향으로 각각 그래프 탐색합니다. 승자·패자 관계가 모두 합해 N−1명인 선수를 셉니다. Floyd 전파와 달리 인접 리스트를 사용합니다.

| 항목 | 기본 풀이 | 선수별 도달 탐색 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(N³), 공간 O(N²). N≤100이라 삼중 반복문을 사용해도 된다. | O(N(N+E)), 공간 O(N+E) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[5, [[4, 3], [4, 2], [3, 2], [1, 2], [2, 5]]]` | `2` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Count players whose exact rank is determined by the given wins and their transitive implications.

`1≤n≤100; 1≤E≤4,500`

### Method and correctness

Compute transitive wins: if A beats B and B beats C, A beats C. Floyd-style propagation obtains every implied comparison. A player has a fixed rank only when comparable to all other N−1 players; its rank is the number of stronger players plus one. The supplied results are consistent.

Main complexity: O(N³) time, O(N²) space.

### Alternative and trade-offs

For every player, search both win and loss directions. A rank is fixed when all other players are reachable in one direction. This uses graph searches instead of Floyd closure.

Code: [alternative.py](alternative.py). Scope: alternative implementation.

Complexity: O(N(N+E)), space O(N+E).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 순위](https://school.programmers.co.kr/learn/courses/30/lessons/49191) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 41개 입력에서 82회 검사를 통과했습니다.

Passed 82 implementation checks across 41 official, boundary and fixed-seed differential inputs.
