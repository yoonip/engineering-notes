# 양과 늑대

Level 3 · [92343 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/92343)

## 문제와 조건

루트에서 양을 모으되 어느 순간에도 늑대가 양 이상이 되지 않도록 방문해 모을 수 있는 최대 양 수를 구합니다.

0번이 양인 루트인 이진트리입니다. 방문 중 늑대 수가 양 수 이상이 되면 실패합니다.

`2≤N≤17; info[i]∈{0,1}; info[0]=0; edges=N−1`

## 풀이를 따라가기

1. 방문했던 노드 사이를 다시 이동해도 양·늑대 수는 변하지 않으므로, 현재 위치 대신 방문 집합만 상태로 사용합니다.
2. 방문한 부모들의 아직 안 간 자식 중 하나를 고릅니다. 늑대≥양이 되는 선택은 즉시 버리고, 같은 방문 집합은 캐시합니다. 시간 O(N2^N), 공간 O(2^N).
3. 예: 양이 두 마리·늑대가 한 마리일 때 늑대를 먼저 더 방문하면 즉시 실패합니다. 다른 가지의 양을 먼저 모으면 그 늑대도 나중에 안전하게 방문할 수 있습니다.

## 왜 이 방법으로 풀 수 있나

방문했던 노드 사이를 다시 이동해도 양·늑대 수는 변하지 않으므로, 현재 위치 대신 방문 집합만 상태로 사용합니다.

시간·공간: 시간 O(N2^N), 공간 O(2^N).

## 다른 방법과 비교

방문 가능한 자식 목록을 상태에 함께 넘깁니다. 방문 집합을 캐시하는 기본 풀이보다 같은 집합을 여러 순서로 방문할 수 있지만 후보 확장 과정이 직접 드러납니다.

| 항목 | 기본 풀이 | 다음 방문 후보 집합 DFS |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(N2^N), 공간 O(2^N). | 최악 O(N!·N), 작은 트리 비교용 |
| 용도 | 기본 제출 구현 | 작은 입력 비교·검증용 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[[0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1], [[0, 1], [1, 2], [1, 4], [0, 8], [8, 7], [9, 10], [9, 11], [4, 3], [6, 5], [4, 6], [8, 9]]]` | `5` |
| `[[0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0], [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5], [2, 6], [3, 7], [4, 8], [6, 9], [9, 10]]]` | `5` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Collect the maximum sheep from the root while keeping wolves strictly fewer than sheep at every step.

The input is a binary tree rooted at sheep node zero. Wolves must remain strictly fewer than sheep.

`2≤N≤17; info[i]∈{0,1}; info[0]=0; edges=N−1`

### Method and correctness

Use the visited-node set as a bitmask state: movement inside that set does not change animal counts. Candidates are unvisited children of visited nodes. Reject any extension with wolves at least equal to sheep, and memoize visited sets reached by different orders. Each valid set yields its sheep count and every legal next extension is considered.

Main complexity: O(N2^N) time, O(2^N) cached states.

### Alternative and trade-offs

Pass the available frontier explicitly through DFS. It may revisit the same visited set in multiple orders, but makes the frontier expansion rule explicit.

Code: [alternative.py](alternative.py). Scope: tiny-input oracle; not for maximum-size submissions.

Complexity: worst case O(N!·N), tiny-tree oracle.

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 양과 늑대](https://school.programmers.co.kr/learn/courses/30/lessons/92343) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 43개 입력에서 86회 검사를 통과했습니다.

Passed 86 implementation checks across 43 official, boundary and fixed-seed differential inputs.
