# 가장 먼 노드

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

Level 3 · [49189 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/49189)

## 문제와 조건

1번 노드에서 최단거리 기준으로 가장 멀리 떨어진 노드가 몇 개인지 구합니다.

`2≤n≤20,000; 1≤E≤50,000`

## 풀이를 따라가기

1. 모든 간선의 길이가 1이므로 BFS를 사용합니다. 시작점에서 가까운 노드부터 방문하며 최단 거리를 기록합니다.
2. 예제에서는 거리 0에 1번, 거리 1에 2·3번, 거리 2에 4·5·6번이 있어 답은 3입니다.
3. 노드 N, 간선 M일 때 시간·공간 O(N+M).

## 왜 이 방법으로 풀 수 있나

모든 간선의 길이가 1이므로 BFS를 사용합니다. 시작점에서 가까운 노드부터 방문하며 최단 거리를 기록합니다.

시간·공간: 시간·공간 O(N+M).

## 다른 방법과 비교

모든 간선의 가중치를 1로 두고 다익스트라를 적용합니다. BFS와 거리는 같지만 힙 연산이 추가되므로 이 문제에서는 BFS가 더 간단하고 빠릅니다.

| 항목 | 기본 풀이 | 다익스트라 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간·공간 O(N+M). | O((N+E) log N), 공간 O(N+E) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

예제 입력과 결과는 [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/49189)에서 확인할 수 있습니다.

[examples.json](examples.json) contains the official example inputs and expected outputs, including narrative-format examples.

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Count nodes at the largest shortest-path distance from node one.

`2≤n≤20,000; 1≤E≤50,000`

### Method and correctness

All edges have unit length, so BFS records shortest distances from node one. Count nodes whose recorded distance is the largest reachable distance. Each vertex is enqueued at most once and each undirected edge is examined twice.

Main complexity: O(N+E) time and space.

### Alternative and trade-offs

Apply Dijkstra with unit edge weights. Distances match BFS, but heap operations are unnecessary overhead, so BFS is preferable for this unweighted graph.

Code: [alternative.py](alternative.py).

Complexity: O((N+E) log N), space O(N+E).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 가장 먼 노드](https://school.programmers.co.kr/learn/courses/30/lessons/49189) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 41개 입력에서 82회 검사를 통과했습니다.

Passed 82 implementation checks across 41 official, boundary and fixed-seed differential inputs.
