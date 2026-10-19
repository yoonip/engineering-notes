# 모두 0으로 만들기

Level 3 · [76503 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/76503)

## 문제와 조건

간선 양 끝의 무게를 1씩 반대로 바꿔 트리의 모든 정점을 0으로 만드는 최소 연산 수를 구합니다.

그래프는 트리이고 한 간선의 양 끝 무게를 1씩 반대로 바꿉니다. 불가능하면 −1입니다.

`2≤N≤300,000; −1,000,000≤a[i]≤1,000,000; edges=N−1`

## 풀이를 따라가기

1. 전체 가중치 합이 0일 때만 가능하다. 잎부터 가중치를 부모에게 넘기고 넘긴 양의 절댓값을 더한다.
2. 예: [-5,0,2,1,2]에서는 두 잎의 2씩과 가운데 누적 5를 옮겨 2+2+5=9번.
3. 트리의 간선을 끊으면 부분 트리의 합만큼 반드시 그 간선을 지나야 하므로 이 횟수가 최소. 시간·공간 O(N).

## 왜 이 방법으로 풀 수 있나

전체 가중치 합이 0일 때만 가능하다. 잎부터 가중치를 부모에게 넘기고 넘긴 양의 절댓값을 더한다.

시간·공간: 시간·공간 O(N).

## 다른 방법과 비교

현재 리프의 무게를 유일한 이웃으로 옮기고 그 리프를 제거합니다. 부모 배열을 먼저 만드는 기본 풀이와 달리 차수가 1인 정점부터 처리합니다.

| 항목 | 기본 풀이 | 리프 제거 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간·공간 O(N). | O(N), 공간 O(N) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[[-5, 0, 2, 1, 2], [[0, 1], [3, 4], [2, 3], [0, 3]]]` | `9` |
| `[[0, 1, 0], [[0, 1], [1, 2]]]` | `-1` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Minimize unit transfers along tree edges until all vertex weights become zero.

The graph is a tree; an operation increases one endpoint by one and decreases the other by one. Return −1 if impossible.

`2≤N≤300,000; −1,000,000≤a[i]≤1,000,000; edges=N−1`

### Method and correctness

Total weight must be zero because each operation preserves the sum. Root the tree and process children before parents. The entire child-subtree imbalance must cross its unique parent edge, requiring at least its absolute value in operations. Moving exactly that imbalance attains this bound on every edge, proving optimality.

Main complexity: O(N) time and space.

### Alternative and trade-offs

Repeatedly move a leaf weight to its only remaining neighbor, then remove the leaf. This uses degree-based pruning rather than a precomputed parent/postorder traversal.

Code: [alternative.py](alternative.py).

Complexity: O(N), space O(N).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 모두 0으로 만들기](https://school.programmers.co.kr/learn/courses/30/lessons/76503) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 44개 입력에서 88회 검사를 통과했습니다.

Passed 88 implementation checks across 44 official, boundary and fixed-seed differential inputs.
