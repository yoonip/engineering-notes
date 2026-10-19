# 2차원 동전 뒤집기

Level 3 · [131703 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/131703)

## 문제와 조건

행 전체 또는 열 전체의 동전을 뒤집어 목표 배열로 만드는 최소 횟수를 구합니다. 만들 수 없으면 −1입니다.

`1≤N,M≤10; beginning[r][c],target[r][c]∈{0,1}`

## 풀이를 따라가기

1. 각 칸의 필요한 변화는 행 뒤집기 XOR 열 뒤집기입니다. 첫 행을 안 뒤집는다고 고정하면 나머지 모든 선택이 결정됩니다.
2. 모든 칸이 일치하는지 확인한 뒤, 그 선택과 모든 행·열 선택을 반대로 한 경우 두 개만 비교하면 됩니다. 같은 줄을 두 번 뒤집는 것은 불필요합니다. 시간·공간 O(NM).
3. 예: 첫 행 고정 해법이 행 2개·열 3개를 뒤집는다면 총 5번입니다. 선택을 전부 뒤집은 해법의 비용은 N+M-5입니다.

## 왜 이 방법으로 풀 수 있나

각 칸의 필요한 변화는 행 뒤집기 XOR 열 뒤집기입니다. 첫 행을 안 뒤집는다고 고정하면 나머지 모든 선택이 결정됩니다.

시간·공간: 시간·공간 O(NM).

## 다른 방법과 비교

행을 뒤집을지 모두 정한 뒤 각 열이 일치하는지, 전부 반대인지 확인합니다. 열 선택은 그 결과로 결정됩니다. 기본 XOR 풀이보다 느리지만 가능한 행 선택을 직접 확인합니다.

| 항목 | 기본 풀이 | 행 뒤집기 전수검사 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간·공간 O(NM). | O(2^N NM), 공간 O(N+M) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[[[0, 1, 0, 0, 0], [1, 0, 1, 0, 1], [0, 1, 1, 1, 0], [1, 0, 1, 1, 0], [0, 1, 0, 1, 0]], [[0, 0, 0, 1, 1], [0, 0, 0, 0, 1], [0, 0, 1, 0, 1], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]]]` | `5` |
| `[[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[1, 0, 1], [0, 0, 0], [0, 0, 0]]]` | `-1` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Minimize whole-row or whole-column coin flips to reach the target matrix; return −1 if impossible.

`1≤N,M≤10; beginning[r][c],target[r][c]∈{0,1}`

### Method and correctness

Let D[r,c] be the XOR of the initial and target coins. Required flips satisfy row[r] XOR col[c]=D[r,c]. Fixing the first row flip to zero determines all columns and rows. Verify every cell; if valid, the only other assignment complements every row and column flip. Compare the two counts, since flipping a line twice is unnecessary.

Main complexity: O(NM) time and space.

### Alternative and trade-offs

Enumerate row flips, then each column must either match entirely or be entirely opposite. Column choices are forced. This directly checks the faster XOR characterization.

Code: [alternative.py](alternative.py). Scope: alternative implementation.

Complexity: O(2^N NM), space O(N+M).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 2차원 동전 뒤집기](https://school.programmers.co.kr/learn/courses/30/lessons/131703) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 44개 입력에서 88회 검사를 통과했습니다.

Passed 88 implementation checks across 44 official, boundary and fixed-seed differential inputs.
