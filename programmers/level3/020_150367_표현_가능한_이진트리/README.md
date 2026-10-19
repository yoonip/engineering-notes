# 표현 가능한 이진트리

Level 3 · [150367 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/150367)

## 문제와 조건

각 정수를 포화 이진트리의 중위 순회 비트열로 표현할 수 있는지 1·0으로 반환합니다. 빈 노드 아래에는 실제 노드가 올 수 없습니다.

`1≤len(numbers)≤10,000; 1≤number≤10^15`

## 풀이를 따라가기

1. 이진 문자열을 노드 수 1·3·7·15...에 맞춰 왼쪽에 0을 채웁니다. 중위 순회이므로 각 부분 문자열의 가운데가 루트입니다.
2. 루트가 0이면 그 부분 트리 전체에 1이 없어야 합니다. 루트가 1이면 왼쪽·오른쪽을 같은 규칙으로 검사합니다. 문자열 길이 L에 대해 슬라이스를 포함한 시간 O(L log L), 추가 공간 O(L).
3. 예: 5는 101이고 가운데 루트가 0인데 실제 자식 1이 있으므로 불가. 42는 0101010이고 루트 1 아래의 각 부분 트리도 유효하므로 가능합니다.

## 왜 이 방법으로 풀 수 있나

이진 문자열을 노드 수 1·3·7·15...에 맞춰 왼쪽에 0을 채웁니다. 중위 순회이므로 각 부분 문자열의 가운데가 루트입니다.

시간·공간: 시간 O(L log L), 추가 공간 O(L).

## 다른 방법과 비교

문자열을 자르지 않고 인덱스 구간과 부모가 비어 있는지 여부를 전달합니다. 부모가 비어 있으면 모든 후손도 0이어야 합니다.

| 항목 | 기본 풀이 | 인덱스 구간 검사 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(L log L), 추가 공간 O(L). | O(L), 재귀 공간 O(log L) 및 문자열 O(L) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[[7, 42, 5]]` | `[1, 1, 0]` |
| `[[63, 111, 95]]` | `[1, 1, 0]` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

For each integer return whether its bits can represent a perfect-tree inorder layout with dummy zero nodes and no real descendant below an absent node.

`1≤len(numbers)≤10,000; 1≤number≤10^15`

### Method and correctness

Pad each binary representation with leading zeros to a perfect-tree length 1,3,7,15,… . In inorder layout the middle bit is the root. A zero root requires the entire subtree to contain no one bits. A one root allows independent recursive checks of both halves. This exactly enforces that a real node never descends from an absent node.

Main complexity: O(L log L) time with substring copies, O(L) peak extra space per number.

### Alternative and trade-offs

Pass index intervals and whether an ancestor is absent. Once an absent node is found, every descendant must also be absent. This avoids substring copies.

Code: [alternative.py](alternative.py). Scope: alternative implementation.

Complexity: O(L), recursive space O(log L) plus string O(L).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 표현 가능한 이진트리](https://school.programmers.co.kr/learn/courses/30/lessons/150367) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 43개 입력에서 86회 검사를 통과했습니다.

Passed 86 implementation checks across 43 official, boundary and fixed-seed differential inputs.
