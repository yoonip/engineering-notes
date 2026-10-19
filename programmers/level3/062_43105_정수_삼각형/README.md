# 정수 삼각형

Level 3 · [43105 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/43105)

## 문제와 조건

삼각형 꼭대기부터 아래의 인접한 두 칸 중 하나씩 내려가며 얻을 수 있는 최대 합을 구합니다.

`1≤height≤500; 0≤value≤9,999`

## 풀이를 따라가기

1. 아래 칸에서 바닥까지의 최적값을 알고 있으면 현재 칸은 자기 값+두 자식 최적값 중 큰 값이다. 이를 바닥부터 반복한다.
2. 예: 7→3→8→7→5를 고르면 30. 왼쪽부터 갱신할 때 오른쪽 dp[i+1]은 아직 이전 행 값이라 한 배열을 재사용할 수 있다.
3. 높이 H일 때 시간 O(H²), 추가 공간 O(H). 입력 삼각형은 수정하지 않는다.

## 왜 이 방법으로 풀 수 있나

아래 칸에서 바닥까지의 최적값을 알고 있으면 현재 칸은 자기 값+두 자식 최적값 중 큰 값이다. 이를 바닥부터 반복한다.

시간·공간: 시간 O(H²), 추가 공간 O(H). 입력 삼각형은 수정하지 않는다.

## 다른 방법과 비교

각 칸으로 들어올 수 있는 두 부모의 최적값을 비교합니다. 아래에서 올라오는 기본 풀이와 달리 마지막 행의 최댓값이 답이 됩니다.

| 항목 | 기본 풀이 | 위에서 내려가는 DP |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(H²), 추가 공간 O(H). 입력 삼각형은 수정하지 않는다. | O(H²), 공간 O(H) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[[[7], [3, 8], [8, 1, 0], [2, 7, 4, 4], [4, 5, 2, 6, 5]]]` | `30` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Maximize the sum along a path from triangle top to bottom, choosing one of two adjacent children each step.

`1≤height≤500; 0≤value≤9,999`

### Method and correctness

Work from the bottom row upwards. The best suffix starting at a cell is its value plus the larger of the two child suffixes. Update a one-row array left to right so the right child still holds the previous row’s value. The input triangle remains unchanged.

Main complexity: O(H²) time, O(H) extra space.

### Alternative and trade-offs

Propagate maximum path sums from the top using the two possible parents. Unlike bottom-up DP, the answer is the maximum value in the final row.

Code: [alternative.py](alternative.py). Scope: alternative implementation.

Complexity: O(H²), space O(H).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 정수 삼각형](https://school.programmers.co.kr/learn/courses/30/lessons/43105) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 42개 입력에서 84회 검사를 통과했습니다.

Passed 84 implementation checks across 42 official, boundary and fixed-seed differential inputs.
