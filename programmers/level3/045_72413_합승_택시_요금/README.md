# 합승 택시 요금

Level 3 · [72413 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/72413)

## 문제와 조건

두 승객이 출발지에서 일부 구간을 합승하고 각 목적지로 갈 때 최소 총요금을 구합니다.

요금은 양방향이고 동일한 두 지점의 중복 요금은 없습니다. 두 목적지까지 도달 가능합니다.

`3≤n≤200; s,a,b distinct∈[1,n]; 2≤E≤n(n−1)/2; 1≤fare≤100,000`

## 풀이를 따라가기

1. 분기점 i까지 합승하고 이후 각 목적지로 간다. s·a·b에서 다익스트라를 한 번씩 실행해 세 거리의 합을 최소화한다.
2. 예제 3은 4→6 합승 7원, 이후 6→5 11원으로 총 18원. 분기점=s이면 처음부터 따로 가는 경우도 포함된다.
3. 간선 수 M일 때 시간 O((N+M) log N), 공간 O(N+M).

## 왜 이 방법으로 풀 수 있나

분기점 i까지 합승하고 이후 각 목적지로 간다. s·a·b에서 다익스트라를 한 번씩 실행해 세 거리의 합을 최소화한다.

시간·공간: 시간 O((N+M) log N), 공간 O(N+M).

## 다른 방법과 비교

모든 지점 쌍의 최단요금을 계산한 뒤 합승 종료 지점을 모두 비교합니다. 세 번의 다익스트라보다 밀집 그래프에서 구현이 단순하지만 O(N³)입니다.

| 항목 | 기본 풀이 | Floyd–Warshall |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O((N+M) log N), 공간 O(N+M). | O(N³), 공간 O(N²) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[6, 4, 6, 2, [[4, 1, 10], [3, 5, 24], [5, 6, 2], [3, 1, 41], [5, 1, 24], [4, 6, 50], [2, 4, 66], [2, 3, 22], [1, 6, 25]]]` | `82` |
| `[7, 3, 4, 1, [[5, 7, 9], [4, 6, 4], [3, 6, 1], [3, 2, 3], [2, 1, 6]]]` | `14` |
| `[6, 4, 5, 6, [[2, 6, 6], [6, 3, 7], [4, 6, 7], [6, 5, 11], [2, 5, 12], [5, 3, 20], [2, 4, 8], [4, 3, 9]]]` | `18` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Minimize total taxi fare when two passengers may share an initial route before splitting to their destinations.

Fares are undirected without duplicate pairs; both destinations are reachable.

`3≤n≤200; s,a,b distinct∈[1,n]; 2≤E≤n(n−1)/2; 1≤fare≤100,000`

### Method and correctness

For each split point k, the total fare is dist(s,k)+dist(a,k)+dist(b,k). Undirected edges let three Dijkstra runs provide all these values. Any shared ride has such a split point, and shortest paths for its three parts cannot cost more. Evaluate every k to obtain the global minimum.

Main complexity: O((N+E) log N) time for three searches, O(N+E) space.

### Alternative and trade-offs

Compute all-pairs shortest fares, then test every shared-ride split point. Floyd–Warshall is simple for dense graphs but uses cubic time instead of three Dijkstra runs.

Code: [alternative.py](alternative.py). Scope: alternative implementation.

Complexity: O(N³), space O(N²).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 합승 택시 요금](https://school.programmers.co.kr/learn/courses/30/lessons/72413) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 44개 입력에서 88회 검사를 통과했습니다.

Passed 88 implementation checks across 44 official, boundary and fixed-seed differential inputs.
