# 입국심사

Level 3 · [43238 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/43238)

## 문제와 조건

서로 다른 속도의 심사관들이 n명을 모두 심사하는 데 필요한 최소 시간을 구합니다.

`1≤n≤10^9; 1≤inspectors≤100,000; 1≤times[i]≤10^9`

## 풀이를 따라가기

1. 심사관 M명·상한 U=n·min(times)에서 시간 O(M log U), 추가 공간 O(1)
2. 예: 28분에는 28//7+28//10=4+2=6명, 27분에는 3+2=5명이므로 정답 28.
3. 심사관 수 M, 상한 U=n·min(times)일 때 시간 O(M log U), 공간 O(1).

## 왜 이 방법으로 풀 수 있나

심사관 M명·상한 U=n·min(times)에서 시간 O(M log U), 추가 공간 O(1)

시간·공간: 심사관 M명·상한 U=n·min(times)에서 시간 O(M log U), 추가 공간 O(1)

## 다른 방법과 비교

다음 심사가 끝나는 시각을 힙에서 하나씩 꺼냅니다. 실제 사람 수만큼 이벤트를 처리하므로 n이 큰 원래 제한에는 이분탐색이 필요합니다.

| 항목 | 기본 풀이 | 심사 완료 이벤트 힙 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 심사관 M명·상한 U=n·min(times)에서 시간 O(M log U), 추가 공간 O(1) | O((심사관 수+n) log 심사관 수), 작은 n 비교용 |
| 용도 | 기본 제출 구현 | 작은 입력 비교·검증용 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[6, [7, 10]]` | `28` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Find the earliest time all n people can finish immigration through inspectors of different speeds.

`1≤n≤10^9; 1≤inspectors≤100,000; 1≤times[i]≤10^9`

### Method and correctness

At time T, inspector i can complete floor(T/time[i]) people. Summing these counts gives a monotone feasibility test. Binary-search the first feasible integer time between zero and n times the fastest inspection time. The upper bound is feasible even if only the fastest inspector works.

Main complexity: O(inspectors·log(n·min(times))) time, O(1) extra space.

### Alternative and trade-offs

Pop the next immigration-completion event from a heap for each person. This explicitly simulates n completions, so binary search is required when n is large.

Code: [alternative.py](alternative.py). Scope: tiny-input oracle; not for maximum-size submissions.

Complexity: O((inspectors+n) log inspectors), small-n oracle.

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 입국심사](https://school.programmers.co.kr/learn/courses/30/lessons/43238) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 42개 입력에서 84회 검사를 통과했습니다.

Passed 84 implementation checks across 42 official, boundary and fixed-seed differential inputs.
