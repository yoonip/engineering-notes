# 최고의 집합

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

Level 3 · [12938 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12938)

## 문제와 조건

합이 s인 양의 정수 n개 중 원소의 곱이 가장 큰 오름차순 집합을 구합니다.

양의 정수 n개의 합을 s로 고정하고 곱을 최대화합니다. 오름차순 반환, 불가능하면 [−1]입니다.

`1≤n≤10,000; 1≤s≤100,000,000`

## 풀이를 따라가기

1. 두 수의 차이가 2 이상이면 큰 수에서 1을 빼 작은 수에 더할 때 합은 같고 곱은 증가합니다. 따라서 최적 집합의 수들은 차이가 최대 1입니다.
2. 예: 9를 2개로 나누면 몫 4·나머지 1이라 [4,5]. 몫을 n-r개, 몫+1을 r개 쓰면 합이 정확히 s가 됩니다.
3. 실제 큰 곱을 계산할 필요가 없습니다. 시간 O(N), 반환 배열을 포함한 공간 O(N).

## 왜 이 방법으로 풀 수 있나

두 수의 차이가 2 이상이면 큰 수에서 1을 빼 작은 수에 더할 때 합은 같고 곱은 증가합니다. 따라서 최적 집합의 수들은 차이가 최대 1입니다.

시간·공간: 시간 O(N), 반환 배열을 포함한 공간 O(N).

## 다른 방법과 비교

오름차순 자연수 분할을 직접 만들고 곱이 가장 큰 분할을 찾습니다. 몫·나머지로 균등하게 나누는 교환 논리를 작은 합에서 확인합니다.

| 항목 | 기본 풀이 | 자연수 분할 전수검사 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(N), 반환 배열을 포함한 공간 O(N). | 분할 수에 비례한 지수 시간, 작은 합 비교용 |
| 용도 | 기본 제출 구현 | 작은 입력 비교·검증용 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[2, 9]` | `[4, 5]` |
| `[2, 1]` | `[-1]` |
| `[2, 8]` | `[4, 4]` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Find a sorted set of n positive integers with sum s and maximum product.

Maximize the product of n positive integers summing to s. Return them sorted, or [−1] if impossible.

`1≤n≤10,000; 1≤s≤100,000,000`

### Method and correctness

If two positive values differ by at least two, moving one unit from the larger to the smaller increases their product while preserving the sum. Thus optimal values differ by at most one. Divide s by n and place the remainder among values one larger, returning them sorted. If s<n, no positive solution exists.

Main complexity: O(n) output time and space.

### Alternative and trade-offs

Enumerate nondecreasing positive integer partitions and maximize their product. Tiny totals check the balancing argument behind the quotient/remainder construction.

Code: [alternative.py](alternative.py). Scope: tiny-input oracle; not for maximum-size submissions.

Complexity: exponential time in the partition count, tiny-total oracle.

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 최고의 집합](https://school.programmers.co.kr/learn/courses/30/lessons/12938) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 45개 입력에서 90회 검사를 통과했습니다.

Passed 90 implementation checks across 45 official, boundary and fixed-seed differential inputs.
