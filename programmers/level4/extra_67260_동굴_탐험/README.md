# 동굴 탐험

[Level 4 목록 / Level 4 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

Level 4 · `67260` · Python3 · [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/67260)

[기본 풀이](solution.py) · [다른 풀이](alternative.py) · [예제 입력과 정답](examples.json) · [검증 코드](test_solution.py)

## 문제와 조건

0번 방에서 시작해 트리의 모든 방을 방문할 수 있는지 판단합니다. 특정 방은 정해진 선행 방을 방문한 뒤에만 들어갈 수 있습니다.

입력 범위와 상수는 다음과 같습니다. 기호는 코드의 매개변수에 맞췄습니다.

`2≤n≤200000; tree edges=n−1; 1≤len(order)≤n/2; start=0; prerequisite pairs have no repeated participants under the statement rules.`

## 풀이를 따라가기

주 풀이는 이동으로 도달했지만 아직 선행 조건이 안 풀린 방을 보류합니다. 선행 방을 방문하면 그 방을 다시 큐에 넣습니다. 잠긴 방 너머를 미리 방문하지 않습니다.

큐에 들어가 방문되는 방은 이동과 선행 조건을 모두 만족합니다. 가능한 방을 더 처리할 수 없는데 미방문 방이 남았다면 그 방으로 가는 길이나 선행 관계가 막힌 상태입니다.

## 다른 방법과 비교

대안은 트리를 0번에서 바깥 방향으로 잡고 부모→자식 관계와 선행 관계를 합쳐 위상 정렬합니다. 부모를 거치지 않고 자식에 갈 수 없는 트리 성질 때문에 모든 정점을 처리할 수 있는지가 방문 가능성과 같습니다.

| 구분 | 시간 | 추가 공간 |
|---|---|---|
| 기본 풀이 | `O(n)` | `O(n)` |
| 대안 풀이 | `O(n+len(order))` | `O(n+len(order))` |

## 코드와 검증

`solution.py`에는 상태의 뜻과 경계조건을 한국어 주석으로 적었습니다. `alternative.py`는 별도의 풀이이며, `test_solution.py`에서 공식 예제와 생성 입력을 비교합니다. 실행 기록은 [validation.json](validation.json)에 있습니다. 원본 제출 파일은 [submitted_original.py](submitted_original.py)에 그대로 보관했습니다.

```bash
python test_solution.py
```

## English

### Problem and constraints

Starting at room zero, determine whether every room in a tree can be visited while respecting prerequisite visits.

Input limits and constants, using the parameter names in the code:

`2≤n≤200000; tree edges=n−1; 1≤len(order)≤n/2; start=0; prerequisite pairs have no repeated participants under the statement rules.`

### Following the solution

The main solution suspends reached rooms whose prerequisite is still locked. Visiting the prerequisite requeues them; it never traverses beyond a locked room prematurely.

Every processed room satisfies both reachability and prerequisite conditions. If the queue exhausts with rooms missing, a required route or dependency remains blocked.

### Alternative and comparison

The alternative roots the tree at zero and topologically sorts parent-to-child edges together with prerequisites. A unique tree route must pass through the parent, making a complete topological order equivalent to feasible visitation.

The primary solution takes `O(n)` time and `O(n)` additional space. The alternative takes `O(n+len(order))` time. Its additional space is `O(n+len(order))`.

### Code and verification

Read `solution.py` for the primary implementation and `alternative.py` for the comparison. Comments explain states and boundary cases in Korean. Run `python test_solution.py` for the official examples and generated comparisons; [validation.json](validation.json) records the execution. The submitted source is preserved byte for byte in [submitted_original.py](submitted_original.py).

## 출처 / Source

- [Programmers — 동굴 탐험](https://school.programmers.co.kr/learn/courses/30/lessons/67260): 문제 조건·입출력 예 확인 / problem constraints and examples checked on 2026-10-19.
