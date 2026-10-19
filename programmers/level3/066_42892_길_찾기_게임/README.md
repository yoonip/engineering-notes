# 길 찾기 게임

Level 3 · [42892 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/42892)

## 문제와 조건

좌표로 정의된 이진트리를 복원하고 노드 번호의 전위·후위 순회를 반환합니다.

좌표는 문제의 이진트리 규칙을 만족합니다. 노드 번호는 입력 순서 1부터입니다.

`1≤nodes≤10,000; 0≤x,y≤100,000; tree depth≤1,000`

## 풀이를 따라가기

1. x좌표는 이진 탐색 트리의 순서, y좌표는 부모가 더 높은 우선순위다. x순으로 읽으며 낮은 노드를 스택에서 꺼내 새 노드 아래에 붙인다.
2. 전위는 나→왼쪽→오른쪽, 후위는 왼쪽→오른쪽→나. 방문 완료 표시를 스택에 다시 넣어 두 순회를 함께 만든다.
3. 예제 루트는 7번이고 전위 첫 값·후위 마지막 값도 7이다. 정렬 포함 시간 O(N log N), 공간 O(N).

## 왜 이 방법으로 풀 수 있나

x좌표는 이진 탐색 트리의 순서, y좌표는 부모가 더 높은 우선순위다. x순으로 읽으며 낮은 노드를 스택에서 꺼내 새 노드 아래에 붙인다.

시간·공간: 시간 O(N log N), 공간 O(N).

## 다른 방법과 비교

높은 노드부터 x좌표 기준 이진 탐색 트리에 삽입합니다. 단조 스택보다 최악 O(N²)이지만 부모·자식 결정 규칙을 직접 구현합니다.

| 항목 | 기본 풀이 | 높이순 BST 삽입 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(N log N), 공간 O(N). | 최악 O(N²), 공간 O(N) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[[[5, 3], [11, 5], [13, 3], [3, 5], [6, 1], [1, 3], [8, 6], [7, 2], [2, 2]]]` | `[[7, 4, 6, 9, 1, 8, 5, 2, 3], [9, 6, 5, 8, 1, 4, 3, 2, 7]]` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Reconstruct the coordinate-defined binary tree and return preorder and postorder node IDs.

Coordinates satisfy the stated binary-tree geometry. Node IDs start at one in input order.

`1≤nodes≤10,000; 0≤x,y≤100,000; tree depth≤1,000`

### Method and correctness

Sort by x and construct a max-priority Cartesian tree using y as the heap priority. Pop lower nodes from a monotone stack to become the new node’s left subtree, and attach the new node as the remaining top’s right subtree. Iterative traversal yields preorder and postorder without recursion-depth failures.

Main complexity: O(N log N) time, O(N) space.

### Alternative and trade-offs

Insert nodes in descending height order into an x-ordered BST. This directly implements the parent rule, although it can take quadratic time unlike the monotone-stack construction.

Code: [alternative.py](alternative.py). Scope: alternative implementation.

Complexity: worst case O(N²), space O(N).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 길 찾기 게임](https://school.programmers.co.kr/learn/courses/30/lessons/42892) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 42개 입력에서 84회 검사를 통과했습니다.

Passed 84 implementation checks across 42 official, boundary and fixed-seed differential inputs.
