# 부대복귀

Level 3 · [132266 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/132266)

## 문제와 조건

여러 부대원의 출발 지역에서 하나의 목적지로 돌아오는 최단 이동 횟수를 각각 구합니다. 도달 불가능하면 −1입니다.

길은 양방향이고 중복 간선은 없습니다. 각 출발지에서 한 목적지까지 최단거리 또는 −1을 반환합니다.

`3≤n≤100,000; 2≤E≤500,000; 1≤S≤500; vertices∈[1,n]`

## 풀이를 따라가기

1. 길이 양방향이므로 각 출발지→목적지 거리와 목적지→각 출발지 거리가 같습니다. 목적지에서 BFS 한 번으로 모든 답을 구합니다.
2. 거리를 -1로 시작해 도달하지 못한 지역을 그대로 구분합니다. 시간 O(N+E+S), 공간 O(N+E).
3. 예: 두 번째 예제에서 5번부터 거리를 구하면 1번까지 2, 단절된 3번은 -1, 5번 자기 자신은 0입니다.

## 왜 이 방법으로 풀 수 있나

길이 양방향이므로 각 출발지→목적지 거리와 목적지→각 출발지 거리가 같습니다. 목적지에서 BFS 한 번으로 모든 답을 구합니다.

시간·공간: 시간 O(N+E+S), 공간 O(N+E).

## 다른 방법과 비교

출발지마다 BFS를 따로 수행합니다. 목적지 하나에서 거꾸로 탐색하는 기본 풀이와 같은 거리를 얻지만 출발지가 많으면 중복 탐색이 큽니다.

| 항목 | 기본 풀이 | 출발지별 BFS |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(N+E+S), 공간 O(N+E). | O(S(N+E)), 공간 O(N+E) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[3, [[1, 2], [2, 3]], [2, 3], 1]` | `[1, 2]` |
| `[5, [[1, 2], [1, 4], [2, 4], [2, 5], [4, 5]], [1, 3, 5], 5]` | `[2, -1, 0]` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Return each soldier’s shortest number of roads to the shared destination, or −1 if unreachable.

Roads are undirected without duplicate edges. Return each source’s shortest distance to one destination, or −1.

`3≤n≤100,000; 2≤E≤500,000; 1≤S≤500; vertices∈[1,n]`

### Method and correctness

The graph is undirected, so source-to-destination and destination-to-source distances are equal. One BFS from the destination computes every requested distance. Initialize distances to −1, preserving −1 for unreachable sources. BFS visits vertices by nondecreasing path length, so the first recorded distance is minimal.

Main complexity: O(N+E+S) time, O(N+E) space.

### Alternative and trade-offs

Run BFS separately from each source. Undirected distances match the single reverse BFS, but repeated searches duplicate work when many sources are queried.

Code: [alternative.py](alternative.py). Scope: alternative implementation.

Complexity: O(S(N+E)), space O(N+E).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 부대복귀](https://school.programmers.co.kr/learn/courses/30/lessons/132266) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 43개 입력에서 86회 검사를 통과했습니다.

Passed 86 implementation checks across 43 official, boundary and fixed-seed differential inputs.
