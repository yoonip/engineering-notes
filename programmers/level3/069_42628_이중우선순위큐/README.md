# 이중우선순위큐

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

Level 3 · [42628 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/42628)

## 문제와 조건

삽입·최솟값 삭제·최댓값 삭제를 처리한 뒤 남은 최댓값·최솟값을 구합니다.

중복 값은 하나씩 지우고 빈 큐의 삭제는 무시합니다. 결과는 [최댓값, 최솟값]입니다.

`1≤Q≤1,000,000`

## 풀이를 따라가기

1. 두 힙을 사용하되 실제 남은 개수는 Counter 하나로 관리합니다. 한 힙에서 삭제한 값이 다른 힙 맨 위에 나오면 그때 버립니다.
2. 예: 3을 두 번 넣고 최댓값을 한 번 삭제해도 counts[3]=1이라 다른 3은 남습니다. 각 힙에는 같은 값의 오래된 복사본이 있어도 실제 개수로 판정합니다.
3. 명령 Q개일 때 각 삽입 원소는 힙마다 최대 한 번 삭제되므로 시간 O(Q log Q), 공간 O(Q).

## 왜 이 방법으로 풀 수 있나

두 힙을 사용하되 실제 남은 개수는 Counter 하나로 관리합니다. 한 힙에서 삭제한 값이 다른 힙 맨 위에 나오면 그때 버립니다.

시간·공간: 시간 O(Q log Q), 공간 O(Q).

## 다른 방법과 비교

삽입 위치를 이분탐색하고 최솟값·최댓값을 배열 양끝에서 삭제합니다. 오래된 힙 항목 처리가 없어서 단순하지만 삽입·앞 삭제가 선형 시간입니다.

| 항목 | 기본 풀이 | 정렬 배열 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(Q log Q), 공간 O(Q). | O(Q²), 공간 O(Q), 작은 명령 수 비교용 |
| 용도 | 기본 제출 구현 | 작은 입력 비교·검증용 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[["I 16", "I -5643", "D -1", "D 1", "D 1", "I 123", "D -1"]]` | `[0, 0]` |
| `[["I -45", "I 653", "D 1", "I -642", "I 45", "I 97", "D 1", "D -1", "I 333"]]` | `[333, -45]` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Process insertions and deletions of either extreme, then return the remaining maximum and minimum.

Delete only one duplicate at a time and ignore deletion on an empty queue. Return [maximum,minimum].

`1≤Q≤1,000,000`

### Method and correctness

Use a min-heap and max-heap with one shared multiplicity counter. Removing through one heap leaves a stale copy in the other; discard stale top values lazily. Duplicate numbers retain their actual remaining count. Ignore deletion from an empty queue and return [0,0] if no elements remain.

Main complexity: O(Q log Q) amortized time, O(Q) space.

### Alternative and trade-offs

Maintain a sorted array using binary-search insertion and endpoint deletion. It avoids stale heap entries, but insertion and front deletion are linear-time operations.

Code: [alternative.py](alternative.py). Scope: tiny-input oracle; not for maximum-size submissions.

Complexity: O(Q²), space O(Q), small-command oracle.

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 이중우선순위큐](https://school.programmers.co.kr/learn/courses/30/lessons/42628) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 43개 입력에서 86회 검사를 통과했습니다.

Passed 86 implementation checks across 43 official, boundary and fixed-seed differential inputs.
