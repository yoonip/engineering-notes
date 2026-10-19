# 등대

Level 3 · [133500 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/133500)

## 문제와 조건

모든 뱃길의 적어도 한쪽 등대에 불이 켜지도록 켤 등대의 최소 개수를 구합니다.

입력은 연결된 트리입니다. 모든 뱃길의 적어도 한쪽 등대가 켜져야 합니다.

`2≤n≤100,000; edges=n−1; 1≤a≠b≤n`

## 풀이를 따라가기

1. 모든 뱃길을 덮는 트리의 최소 정점 커버 문제입니다. 각 노드를 켜는 경우·끄는 경우의 최소 비용을 따로 둡니다.
2. 부모가 꺼져 있으면 자식은 켜야 하고, 부모가 켜져 있으면 자식 두 상태 중 싼 쪽을 택합니다. 방문 순서를 뒤집어 재귀 깊이 문제 없이 계산합니다. 시간·공간 O(N).
3. 예: 첫 예제에서 1번을 켜면 2·3·4번은 꺼도 되고, 5번을 켜면 6·7·8번도 꺼도 됩니다. 총 2개입니다.

## 왜 이 방법으로 풀 수 있나

모든 뱃길을 덮는 트리의 최소 정점 커버 문제입니다. 각 노드를 켜는 경우·끄는 경우의 최소 비용을 따로 둡니다.

시간·공간: 시간·공간 O(N).

## 다른 방법과 비교

불을 켤 등대 집합을 모두 만들어 모든 뱃길의 끝점 중 적어도 하나가 선택됐는지 확인합니다. 트리 DP를 직접 정의와 대조합니다.

| 항목 | 기본 풀이 | 정점 선택 집합 전수검사 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간·공간 O(N). | O(2^N N), 작은 트리 비교용 |
| 용도 | 기본 제출 구현 | 작은 입력 비교·검증용 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[8, [[1, 2], [1, 3], [1, 4], [1, 5], [5, 6], [5, 7], [5, 8]]]` | `2` |
| `[10, [[4, 1], [5, 1], [5, 6], [7, 6], [1, 2], [1, 3], [6, 8], [2, 9], [9, 10]]]` | `3` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Find the smallest set of lit lighthouses covering at least one endpoint of every sea route.

The input is a connected tree; every edge needs at least one lit endpoint.

`2≤n≤100,000; edges=n−1; 1≤a≠b≤n`

### Method and correctness

This is minimum vertex cover on a tree. For each node compute on=1+sum(min(child_on,child_off)) and off=sum(child_on). An unlit parent forces every child to be lit; a lit parent permits either child state. Reverse an iterative parent traversal to evaluate children before parents and avoid deep Python recursion.

Main complexity: O(N) time and space.

### Alternative and trade-offs

Enumerate lit-node subsets and require every edge to have a lit endpoint. This compares the tree DP directly with the definition of vertex cover.

Code: [alternative.py](alternative.py). Scope: tiny-input oracle; not for maximum-size submissions.

Complexity: O(2^N N), tiny-tree oracle.

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 등대](https://school.programmers.co.kr/learn/courses/30/lessons/133500) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 43개 입력에서 86회 검사를 통과했습니다.

Passed 86 implementation checks across 43 official, boundary and fixed-seed differential inputs.
