# 숫자 게임

Level 3 · [12987 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12987)

## 문제와 조건

A의 순서는 고정한 채 B를 재배치해 더 큰 수로 이기는 경기 수를 최대화합니다. 같은 수는 승리하지 못합니다.

`1≤N≤100,000; 1≤A[i],B[i]≤10^9`

## 풀이를 따라가기

1. B의 작은 숫자로 이길 수 있는 가장 작은 A부터 이깁니다. 못 이기는 B는 어떤 남은 상대도 이길 수 없으므로 승리 후보에서 버려도 됩니다.
2. 예: 정렬한 A=[1,3,5,7], B=[2,2,6,8]은 2>1, 6>3, 8>5로 세 번 승리합니다. 남은 숫자끼리는 패배 경기로 배치하면 됩니다.
3. 매칭할 A의 원래 순서는 그 상대 위치에 B를 배치하면 되므로 정렬해도 최대 승점은 같습니다. 시간 O(N log N), 공간 O(N).

## 왜 이 방법으로 풀 수 있나

B의 작은 숫자로 이길 수 있는 가장 작은 A부터 이깁니다. 못 이기는 B는 어떤 남은 상대도 이길 수 없으므로 승리 후보에서 버려도 됩니다.

시간·공간: 시간 O(N log N), 공간 O(N).

## 다른 방법과 비교

B의 모든 순서를 A와 직접 비교합니다. 정렬 후 탐욕으로 얻는 승점이 최대인지 작은 배열에서 확인합니다.

| 항목 | 기본 풀이 | 순열 완전탐색 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(N log N), 공간 O(N). | O(N!N), 작은 배열 비교용 |
| 용도 | 기본 제출 구현 | 작은 입력 비교·검증용 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[[5, 1, 3, 7], [2, 2, 6, 8]]` | `3` |
| `[[2, 2, 2, 2], [1, 1, 1, 1]]` | `0` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Reorder B against fixed A to maximize strictly greater comparisons; ties do not win.

`1≤N≤100,000; 1≤A[i],B[i]≤10^9`

### Method and correctness

Sort both teams and use the smallest B value that can beat the smallest still-unmatched A value. A B value that cannot beat that A cannot beat any remaining A and may be sacrificed. This exchange argument maximizes wins; the resulting matches can be placed back into A’s original order.

Main complexity: O(N log N) time, O(N) sorting space.

### Alternative and trade-offs

Compare every permutation of B against the original A. Tiny arrays independently verify the maximum score produced by sorted greedy matching.

Code: [alternative.py](alternative.py). Scope: tiny-input oracle; not for maximum-size submissions.

Complexity: O(N!N), small-array checking.

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 숫자 게임](https://school.programmers.co.kr/learn/courses/30/lessons/12987) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 43개 입력에서 86회 검사를 통과했습니다.

Passed 86 implementation checks across 43 official, boundary and fixed-seed differential inputs.
