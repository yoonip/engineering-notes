# 섬 연결하기

Level 3 · [42861 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/42861)

## 문제와 조건

주어진 건설 가능 다리 중 일부를 골라 모든 섬을 연결하는 최소 비용을 구합니다.

제공되지 않은 다리는 만들 수 없으며 모든 섬을 연결할 수 있습니다.

`1≤n≤100; E≤n(n−1)/2`

## 풀이를 따라가기

1. 싼 다리부터 선택하되 이미 이어진 집합 내부의 다리는 버립니다. 연결되지 않은 두 집합 사이의 가장 싼 간선은 최적 해에도 포함시킬 수 있습니다.
2. 예제는 0-1(1), 1-3(1), 0-2(2)를 골라 총 4. 유니온 파인드로 이미 연결되었는지 빠르게 확인합니다.
3. 다리 M개일 때 정렬이 주된 비용으로 시간 O(M log M), 공간 O(N+M).

## 왜 이 방법으로 풀 수 있나

싼 다리부터 선택하되 이미 이어진 집합 내부의 다리는 버립니다. 연결되지 않은 두 집합 사이의 가장 싼 간선은 최적 해에도 포함시킬 수 있습니다.

시간·공간: 시간 O(M log M), 공간 O(N+M).

## 다른 방법과 비교

이미 연결한 섬 집합에서 바깥으로 나가는 가장 싼 다리를 고릅니다. 전체 간선을 정렬하는 Kruskal과 달리 하나의 연결된 집합을 확장합니다.

| 항목 | 기본 풀이 | Prim 최소 신장 트리 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(M log M), 공간 O(N+M). | O(E log E), 공간 O(N+E) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[4, [[0, 1, 1], [0, 2, 2], [1, 2, 5], [1, 3, 1], [2, 3, 8]]]` | `4` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Choose supplied bridges of minimum total cost to connect every island.

Only supplied bridges may be built, and all islands can be connected.

`1≤n≤100; E≤n(n−1)/2`

### Method and correctness

Sort bridge costs and accept an edge only if it joins different components. Union–Find detects cycles efficiently. The cheapest edge crossing a component cut can be included in an MST, so each accepted edge is safe. A connected graph finishes with N−1 accepted edges.

Main complexity: O(E log E) time, O(N+E) space.

### Alternative and trade-offs

Grow one connected set by repeatedly choosing its cheapest outgoing edge. This is Prim’s MST algorithm, unlike Kruskal’s globally sorted edge selection.

Code: [alternative.py](alternative.py).

Complexity: O(E log E), space O(N+E).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 섬 연결하기](https://school.programmers.co.kr/learn/courses/30/lessons/42861) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 42개 입력에서 84회 검사를 통과했습니다.

Passed 84 implementation checks across 42 official, boundary and fixed-seed differential inputs.
