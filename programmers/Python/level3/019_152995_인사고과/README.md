# 인사고과

Level 3 · [152995 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/152995)

## 문제와 조건

두 평가점수가 모두 더 높은 사원이 있으면 인센티브에서 제외합니다. 남은 사원을 합계 점수로 매겼을 때 첫 사원의 등수를 구합니다.

`1≤N≤100,000; 0≤score≤100,000; target=scores[0]`

## 풀이를 따라가기

1. 첫 점수를 내림차순, 같은 첫 점수에서는 둘째 점수를 오름차순으로 정렬합니다. 이 순서면 앞에서 본 둘째 점수보다 낮은 직원만 두 점수 모두 낮은 제외 대상입니다.
2. 완호가 제외되면 -1, 아니면 유효 직원 중 점수 합이 완호보다 큰 사람 수+1을 반환합니다. 시간 O(N log N), 공간 O(N).
3. 예: [[2,2],[1,4],[3,2],[3,2],[2,1]]에서 [2,1]만 제외되고, 완호보다 합이 큰 유효 직원 세 명이 있어 4등입니다.

## 왜 이 방법으로 풀 수 있나

첫 점수를 내림차순, 같은 첫 점수에서는 둘째 점수를 오름차순으로 정렬합니다. 이 순서면 앞에서 본 둘째 점수보다 낮은 직원만 두 점수 모두 낮은 제외 대상입니다.

시간·공간: 시간 O(N log N), 공간 O(N).

## 다른 방법과 비교

각 사원보다 두 점수가 모두 높은 사원이 있는지 직접 검사합니다. 정렬의 동점 처리와 탈락 판정을 검증하는 기준 코드입니다.

| 항목 | 기본 풀이 | 지배 관계 직접 비교 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(N log N), 공간 O(N). | O(N²), 공간 O(N), 작은 입력 비교용 |
| 용도 | 기본 제출 구현 | 작은 입력 비교·검증용 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[[[2, 2], [1, 4], [3, 2], [3, 2], [2, 1]]]` | `4` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

An employee strictly dominated in both scores is ineligible. Return the first employee’s rank by total score among eligible employees.

`1≤N≤100,000; 0≤score≤100,000; target=scores[0]`

### Method and correctness

Sort by the first score descending and, for ties, the second score ascending. A second score strictly below the largest previously seen second score implies strict domination in both criteria; equal first scores cannot cause a false rejection because of the tie order. If the target is dominated, return −1. Otherwise count eligible employees with a strictly greater score sum and add one.

Main complexity: O(N log N) time, O(N) space.

### Alternative and trade-offs

Check every employee against every other employee for strict dominance in both scores. This directly checks the sorting solution and its tie handling.

Code: [alternative.py](alternative.py). Scope: tiny-input oracle; not for maximum-size submissions.

Complexity: O(N²), space O(N), small-input checking.

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 인사고과](https://school.programmers.co.kr/learn/courses/30/lessons/152995) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 43개 입력에서 86회 검사를 통과했습니다.

Passed 86 implementation checks across 43 official, boundary and fixed-seed differential inputs.
