# 등산코스 정하기

Level 3 · [118669 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/118669)

## 문제와 조건

출입구에서 산봉우리 한 곳까지 갔다 돌아오는 코스의 최대 단일 구간 시간(intensity)을 최소화합니다.

출입구와 산봉우리는 겹치지 않고 그래프는 연결됩니다. 산봉우리 하나만 방문하며 다른 출입구를 경유하지 않습니다. 동점이면 작은 산봉우리 번호입니다.

`2≤n≤50,000; n−1≤E≤200,000; 1≤weight≤10,000,000; 1≤|gates|,|summits|≤n`

## 풀이를 따라가기

1. 모든 출입구에서 동시에 시작하는 다익스트라 형태의 탐색입니다. 거리 합 대신 경로의 최대 간선값을 최소화합니다.
2. 산봉우리에서는 더 확장하지 않으며 출입구는 이미 0이라 중간에 다시 들어가지 않습니다. 간 길을 그대로 돌아오면 왕복 intensity가 같으므로 올라가는 최적 경로만 찾으면 됩니다. 시간 O((N+E) log N), 공간 O(N+E).
3. 예: 간선이 3·2·3인 코스는 합 8이 아니라 intensity 3입니다. 같은 intensity라면 산봉우리 번호가 작은 코스를 고릅니다.

## 왜 이 방법으로 풀 수 있나

모든 출입구에서 동시에 시작하는 다익스트라 형태의 탐색입니다. 거리 합 대신 경로의 최대 간선값을 최소화합니다.

시간·공간: 시간 O((N+E) log N), 공간 O(N+E).

## 다른 방법과 비교

허용할 간선의 최대 시간을 정하고 출입구들에서 BFS로 산봉우리를 찾습니다. 가능한 강도는 단조이므로 이분탐색할 수 있습니다. 산봉우리는 경유하지 않습니다.

| 항목 | 기본 풀이 | 강도 한계값 이분탐색 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O((N+E) log N), 공간 O(N+E). | O((N+E) log W), 공간 O(N+E) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[6, [[1, 2, 3], [2, 3, 5], [2, 4, 2], [2, 5, 4], [3, 4, 4], [4, 5, 3], [4, 6, 1], [5, 6, 1]], [1, 3], [5]]` | `[5, 3]` |
| `[7, [[1, 4, 4], [1, 6, 1], [1, 7, 3], [2, 5, 2], [3, 7, 4], [5, 6, 6]], [1], [2, 3, 4]]` | `[3, 4]` |
| `[7, [[1, 2, 5], [1, 4, 1], [2, 3, 1], [2, 6, 7], [4, 5, 1], [5, 6, 1], [6, 7, 1]], [3, 7], [1, 5]]` | `[5, 1]` |
| `[5, [[1, 3, 10], [1, 4, 20], [2, 3, 4], [2, 4, 6], [3, 5, 20], [4, 5, 6]], [1, 2], [5]]` | `[5, 6]` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Minimize the largest edge time (intensity) of a round trip from a gate through exactly one summit.

Gates and summits are disjoint and the graph is connected. Visit exactly one summit and do not pass through another gate. Break intensity ties by smaller summit ID.

`2≤n≤50,000; n−1≤E≤200,000; 1≤weight≤10,000,000; 1≤|gates|,|summits|≤n`

### Method and correctness

Use multi-source minimax Dijkstra: a path cost is its largest edge weight rather than a sum. Relax an edge with max(current_intensity,edge_weight). Do not expand a summit. Gates already have zero intensity, so routes through another gate cannot improve them. Returning along the chosen ascent keeps the same intensity. Choose the smallest summit number on ties.

Main complexity: O((N+E) log N) time, O(N+E) space.

### Alternative and trade-offs

Binary-search an intensity threshold and run multi-source BFS using only allowed edges. Reachability is monotone, and summits are terminal vertices rather than transit nodes.

Code: [alternative.py](alternative.py). Scope: alternative implementation.

Complexity: O((N+E) log W), space O(N+E).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 등산코스 정하기](https://school.programmers.co.kr/learn/courses/30/lessons/118669) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 45개 입력에서 90회 검사를 통과했습니다.

Passed 90 implementation checks across 45 official, boundary and fixed-seed differential inputs.
